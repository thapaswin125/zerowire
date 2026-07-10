"""Triage staged candidates: summaries, tags, and MITRE mappings.

Default mode is rules-based and needs no API key at all:
  * Summary: clean the feed excerpt and keep 2 to 3 sentences.
  * Tags: keyword-match against the controlled vocabulary in vocab.py,
    assigning 3 to 5 tags.
  * MITRE: for Threat Research candidates, map matched tags to ATT&CK
    technique IDs via vocab.MITRE_MAP.

Optional enhanced mode (--llm) calls GitHub Models with the Actions-provided
GITHUB_TOKEN. It only rewrites summaries and refines tags; it never touches
cvss, epss, kev, severity, or must_know, which belong to enrich.py. Any
failure falls back to the rules-based output, so the run never fails.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time

import requests

from pipeline_io import dump_front_matter, iter_staging, load_front_matter, strip_html
from vocab import FALLBACK_TAGS, MAX_TAGS, MIN_TAGS, MITRE_MAP, TAG_KEYWORDS

# GitHub Models free tier: OpenAI-compatible, authenticated with GITHUB_TOKEN.
GITHUB_MODELS_ENDPOINT = "https://models.github.ai/inference"
GITHUB_MODELS_MODEL = "openai/gpt-4o-mini"
LLM_BATCH_SIZE = 6
LLM_BATCH_PAUSE_SECONDS = 10

SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")
MAX_SUMMARY_CHARS = 450

# Fields owned by enrich.py that triage must never modify.
PROTECTED_FIELDS = ("cve", "cvss", "epss", "kev", "severity", "must_know", "ghsa")


def rules_summary(text: str) -> str:
    text = strip_html(text)
    sentences = [s.strip() for s in SENTENCE_RE.split(text) if s.strip()]
    summary = " ".join(sentences[:3])
    if len(summary) > MAX_SUMMARY_CHARS:
        summary = " ".join(sentences[:2])
    if len(summary) > MAX_SUMMARY_CHARS:
        summary = summary[:MAX_SUMMARY_CHARS].rsplit(" ", 1)[0] + " ..."
    return summary


def rules_tags(title: str, body: str) -> list[str]:
    text = f" {title.lower()} {body.lower()} "
    scored: list[tuple[int, str]] = []
    for tag, keywords in TAG_KEYWORDS.items():
        hits = 0
        for kw in keywords:
            if len(kw) <= 4:
                if re.search(rf"\b{re.escape(kw)}\b", text):
                    hits += 1
            elif kw in text:
                hits += 1
        if hits:
            scored.append((hits, tag))
    scored.sort(key=lambda pair: (-pair[0], pair[1]))
    tags = [tag for _, tag in scored[:MAX_TAGS]]
    for filler in FALLBACK_TAGS:
        if len(tags) >= MIN_TAGS:
            break
        if filler not in tags:
            tags.append(filler)
    return tags


def rules_mitre(tags: list[str]) -> list[str]:
    techniques: list[str] = []
    for tag in tags:
        for tid in MITRE_MAP.get(tag, []):
            if tid not in techniques:
                techniques.append(tid)
    return techniques[:6]


def llm_refine(batch: list[dict], token: str) -> dict[str, dict] | None:
    """Ask GitHub Models to rewrite summaries and refine tags for a batch.

    Returns {candidate_id: {"summary": str, "tags": [str]}} or None on any
    failure, in which case the caller keeps the rules-based output.
    """
    vocab_tags = sorted(TAG_KEYWORDS)
    items = [
        {"id": c["id"], "title": c["title"], "text": c["summary"], "tags": c["tags"]}
        for c in batch
    ]
    prompt = (
        "You are triaging security news items for a personal digest. For each "
        "item, rewrite the summary as 2 to 3 tight sentences in plain first-person-"
        "free prose, and refine the tag list to 3 to 5 tags chosen ONLY from this "
        f"vocabulary: {', '.join(vocab_tags)}. Respond with JSON only: "
        '{"items": [{"id": "...", "summary": "...", "tags": ["..."]}]}\n\n'
        f"Items: {json.dumps(items)}"
    )
    try:
        resp = requests.post(
            f"{GITHUB_MODELS_ENDPOINT}/chat/completions",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json={
                "model": GITHUB_MODELS_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
                "response_format": {"type": "json_object"},
            },
            timeout=120,
        )
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        result = {}
        for item in parsed.get("items", []):
            tags = [t for t in item.get("tags", []) if t in TAG_KEYWORDS]
            summary = str(item.get("summary", "")).strip()
            if summary:
                result[str(item.get("id"))] = {"summary": summary, "tags": tags}
        return result or None
    except (requests.RequestException, ValueError, KeyError, TypeError) as exc:
        print(f"  warn: GitHub Models call failed, keeping rules output: {exc}", file=sys.stderr)
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--llm", action="store_true",
                        help="also refine summaries and tags via GitHub Models")
    args = parser.parse_args()

    candidates = []
    for path in iter_staging():
        meta, body = load_front_matter(path)
        summary = rules_summary(body)
        tags = rules_tags(str(meta.get("title", "")), summary)
        meta["tags"] = tags
        if "Threat Research" in (meta.get("categories") or []):
            mitre = rules_mitre(tags)
            if mitre:
                meta["mitre"] = mitre
        dump_front_matter(path, meta, summary)
        candidates.append({
            "path": path, "id": str(meta.get("id", path.stem)),
            "title": str(meta.get("title", "")), "summary": summary, "tags": tags,
        })

    print(f"rules triage done for {len(candidates)} candidate(s)")

    if args.llm and candidates:
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            print("  warn: --llm set but GITHUB_TOKEN missing, keeping rules output",
                  file=sys.stderr)
            return 0
        for i in range(0, len(candidates), LLM_BATCH_SIZE):
            batch = candidates[i : i + LLM_BATCH_SIZE]
            refined = llm_refine(batch, token)
            if refined:
                for cand in batch:
                    update = refined.get(cand["id"])
                    if not update:
                        continue
                    meta, _ = load_front_matter(cand["path"])
                    protected = {k: meta[k] for k in PROTECTED_FIELDS if k in meta}
                    if len(update["tags"]) >= MIN_TAGS:
                        meta["tags"] = update["tags"][:MAX_TAGS]
                    meta.update(protected)
                    dump_front_matter(cand["path"], meta, update["summary"])
                print(f"  llm refined batch of {len(batch)}")
            if i + LLM_BATCH_SIZE < len(candidates):
                time.sleep(LLM_BATCH_PAUSE_SECONDS)

    return 0


if __name__ == "__main__":
    sys.exit(main())
