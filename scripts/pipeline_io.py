"""Shared paths and front matter I/O for the ZeroWire pipeline.

Every pipeline stage works on staging files in _staging/candidates/, which
are normal markdown files with YAML front matter. Only promote_drafts.py is
allowed to write into _posts/.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
STAGING_DIR = ROOT / "_staging" / "candidates"
POSTS_DIR = ROOT / "_posts"
CACHE_DIR = ROOT / ".cache"

FRONT_MATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.DOTALL)


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def load_front_matter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return {}, text
    meta = yaml.safe_load(match.group(1)) or {}
    body = text[match.end():]
    return meta, body


def dump_front_matter(path: Path, meta: dict, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    front = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True, width=1000).strip()
    path.write_text(f"---\n{front}\n---\n\n{body.strip()}\n", encoding="utf-8")


def slugify(title: str, max_len: int = 60) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    if len(slug) > max_len:
        slug = slug[:max_len].rsplit("-", 1)[0]
    return slug or "item"


def iter_staging() -> list[Path]:
    if not STAGING_DIR.is_dir():
        return []
    return sorted(STAGING_DIR.glob("*.md"))


def strip_html(text: str) -> str:
    import html

    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()
