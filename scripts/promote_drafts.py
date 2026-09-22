"""Promote staged candidates into _posts/ and build digest PR bodies.

This is the only script allowed to write into _posts/. It has four modes:
  --pr-body       print the checkbox list used as the digest PR body
  --ids a,b,c     promote specific candidates by id
  --all           promote every staged candidate
  --auto          promote what the daily digest publishes unreviewed:
                  must_know candidates plus every Threat Research
                  candidate, since research feeds are curated by source.
                  The digest workflow runs this before opening the PR for
                  whatever is left.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime

from pipeline_io import POSTS_DIR, dump_front_matter, iter_staging, load_front_matter, slugify

# Staging-only keys stripped from front matter on promotion.
STAGING_KEYS = ("candidate", "id", "ghsa")


def load_candidates() -> list[tuple]:
    out = []
    for path in iter_staging():
        meta, body = load_front_matter(path)
        out.append((path, meta, body))
    return out


def is_auto_publishable(meta: dict) -> bool:
    """Items the daily digest publishes without me checking a box.

    Two cases: enrichment flagged it must-know (KEV or EPSS >= 0.5), or it
    came from a research feed I already trust at the source level.
    """
    if meta.get("must_know") is True:
        return True
    return "Threat Research" in (meta.get("categories") or [])


def pr_body() -> str:
    candidates = load_candidates()
    if not candidates:
        return "No new candidates today. Merging this PR is a no-op.\n"
    lines = [
        "Must-know and Threat Research items were auto-published during this",
        "run and are not listed here.",
        "I check the box next to anything else worth publishing, then merge.",
        "Unchecked items are discarded when this PR merges.",
        "",
    ]
    ordering = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
    candidates.sort(key=lambda c: ordering.get(str(c[1].get("severity", "info")), 4))
    for _, meta, _ in candidates:
        badges = [str(meta.get("severity", "info"))]
        if meta.get("kev"):
            badges.append("KEV")
        if meta.get("epss") is not None:
            badges.append(f"EPSS {meta['epss']}")
        if meta.get("cvss") is not None:
            badges.append(f"CVSS {meta['cvss']}")
        cat = (meta.get("categories") or ["Daily Signal"])[0]
        default_check = "x" if meta.get("must_know") else " "
        lines.append(
            f"- [{default_check}] **{meta.get('title', 'untitled')}** "
            f"({', '.join(badges)}; {cat}) `id:{meta.get('id')}`"
        )
    lines.append("")
    return "\n".join(lines)


def promote(path, meta: dict, body: str) -> str:
    date_raw = str(meta.get("date", ""))
    try:
        day = datetime.strptime(date_raw[:10], "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        day = datetime.utcnow().strftime("%Y-%m-%d")

    for key in STAGING_KEYS:
        meta.pop(key, None)
    meta.setdefault("severity", "info")
    meta.setdefault("must_know", False)
    meta.setdefault("tags", [])

    slug = slugify(str(meta.get("title", "item")))
    target = POSTS_DIR / f"{day}-{slug}.md"
    counter = 2
    while target.exists():
        target = POSTS_DIR / f"{day}-{slug}-{counter}.md"
        counter += 1

    dump_front_matter(target, meta, body)
    path.unlink()
    return target.name


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--pr-body", action="store_true")
    group.add_argument("--ids", help="comma-separated candidate ids to promote")
    group.add_argument("--all", action="store_true")
    group.add_argument("--auto", action="store_true",
                       help="promote must_know candidates and Threat Research candidates")
    args = parser.parse_args()

    if args.pr_body:
        print(pr_body())
        return 0

    wanted = None
    if args.ids:
        wanted = {i.strip() for i in args.ids.split(",") if i.strip()}
    promoted = 0
    for path, meta, body in load_candidates():
        if args.auto and not is_auto_publishable(meta):
            continue
        if wanted is not None and str(meta.get("id")) not in wanted:
            continue
        name = promote(path, meta, body)
        print(f"promoted {name}")
        promoted += 1

    print(f"promoted {promoted} candidate(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
