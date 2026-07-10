"""Fetch curated RSS feeds and stage deduplicated candidates.

Reads feed URLs from rss-sources.md, pulls each feed, and writes new
candidates to _staging/candidates/. This script never touches _posts/.

Dedup happens on two axes:
  1. Canonicalized URL (tracking params and fragments stripped).
  2. Fuzzy normalized-title match via rapidfuzz, so the same story carried by
     multiple feeds collapses into one candidate with merged source links.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import time
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import feedparser
import requests
from rapidfuzz import fuzz

from pipeline_io import (
    ROOT,
    STAGING_DIR,
    POSTS_DIR,
    dump_front_matter,
    iter_staging,
    load_front_matter,
    strip_html,
    utcnow,
)
from vocab import RESEARCH_SOURCES

SOURCES_FILE = ROOT / "rss-sources.md"
FEED_LINE_RE = re.compile(r"^\s*-\s*\[([^\]]+)\]\((\S+)\)")
USER_AGENT = "ZeroWire/1.0 (+https://github.com/thapaswin125/zerowire)"
TITLE_MATCH_THRESHOLD = 90
MAX_AGE_DAYS = 3
TRACKING_PARAMS_RE = re.compile(r"^(utm_\w+|fbclid|gclid|mc_cid|mc_eid|ref|source|cmpid)$", re.I)


def read_sources() -> list[tuple[str, str]]:
    feeds = []
    for line in SOURCES_FILE.read_text(encoding="utf-8").splitlines():
        match = FEED_LINE_RE.match(line)
        if match:
            feeds.append((match.group(1).strip(), match.group(2).strip()))
    return feeds


def canonicalize_url(url: str) -> str:
    parts = urlsplit(url.strip())
    query = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
             if not TRACKING_PARAMS_RE.match(k)]
    path = parts.path.rstrip("/") or "/"
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path,
                       urlencode(query), ""))


def normalize_title(title: str) -> str:
    return re.sub(r"[^a-z0-9 ]+", " ", title.lower()).strip()


def candidate_id(canonical_url: str) -> str:
    return hashlib.sha1(canonical_url.encode("utf-8")).hexdigest()[:12]


def existing_index() -> tuple[set[str], list[str]]:
    """URLs and normalized titles already present in staging or _posts."""
    urls: set[str] = set()
    titles: list[str] = []
    for path in iter_staging() + sorted(POSTS_DIR.glob("*.md")):
        meta, _ = load_front_matter(path)
        for src in meta.get("sources") or []:
            if isinstance(src, dict) and src.get("url"):
                urls.add(canonicalize_url(src["url"]))
        if meta.get("title"):
            titles.append(normalize_title(str(meta["title"])))
    return urls, titles


def entry_timestamp(entry) -> float:
    for attr in ("published_parsed", "updated_parsed"):
        parsed = getattr(entry, attr, None)
        if parsed:
            return time.mktime(parsed)
    return time.time()


def fuzzy_match(title: str, known_titles: list[str]) -> bool:
    return any(fuzz.token_sort_ratio(title, known) >= TITLE_MATCH_THRESHOLD
               for known in known_titles)


def fetch_feed(url: str) -> feedparser.FeedParserDict | None:
    try:
        resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=30)
        resp.raise_for_status()
        return feedparser.parse(resp.content)
    except requests.RequestException as exc:
        print(f"  warn: failed to fetch {url}: {exc}", file=sys.stderr)
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-age-days", type=int, default=MAX_AGE_DAYS)
    parser.add_argument("--limit-per-feed", type=int, default=25)
    args = parser.parse_args()

    STAGING_DIR.mkdir(parents=True, exist_ok=True)
    known_urls, known_titles = existing_index()
    cutoff = time.time() - args.max_age_days * 86400
    staged = 0
    merged = 0

    for source_name, feed_url in read_sources():
        print(f"fetching {source_name} ...")
        feed = fetch_feed(feed_url)
        if feed is None:
            continue

        for entry in feed.entries[: args.limit_per_feed]:
            link = getattr(entry, "link", "") or ""
            title = strip_html(getattr(entry, "title", "") or "")
            if not link or not title:
                continue
            if entry_timestamp(entry) < cutoff:
                continue

            canonical = canonicalize_url(link)
            norm_title = normalize_title(title)
            cid = candidate_id(canonical)
            staging_path = STAGING_DIR / f"{cid}.md"

            if canonical in known_urls:
                continue

            if fuzzy_match(norm_title, known_titles):
                merged += merge_source(norm_title, source_name, link)
                known_urls.add(canonical)
                continue

            summary = strip_html(
                getattr(entry, "summary", "") or getattr(entry, "description", "") or ""
            )
            category = "Threat Research" if source_name in RESEARCH_SOURCES else "Daily Signal"
            meta = {
                "id": cid,
                "candidate": True,
                "title": title,
                "date": utcnow().strftime("%Y-%m-%d %H:%M:%S +0000"),
                "categories": [category],
                "tags": [],
                "severity": "info",
                "must_know": False,
                "sources": [{"name": source_name, "url": link}],
            }
            dump_front_matter(staging_path, meta, summary)
            known_urls.add(canonical)
            known_titles.append(norm_title)
            staged += 1

    print(f"staged {staged} new candidate(s), merged {merged} duplicate source link(s)")
    return 0


def merge_source(norm_title: str, source_name: str, link: str) -> int:
    """Attach an extra source link to the staged candidate with this title."""
    for path in iter_staging():
        meta, body = load_front_matter(path)
        if normalize_title(str(meta.get("title", ""))) != norm_title \
           and fuzz.token_sort_ratio(normalize_title(str(meta.get("title", ""))), norm_title) < TITLE_MATCH_THRESHOLD:
            continue
        sources = meta.setdefault("sources", [])
        if not any(s.get("url") == link for s in sources):
            sources.append({"name": source_name, "url": link})
            dump_front_matter(path, meta, body)
            return 1
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
