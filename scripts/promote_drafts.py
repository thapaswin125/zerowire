"""Promote staged candidates into _posts/ and build digest PR bodies.

This is the only script allowed to write into _posts/. It has three modes:
  --pr-body       print the checkbox list used as the digest PR body
  --ids a,b,c     promote specific candidates by id
  --all           promote every staged candidate
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


def pr_body() -> str:
    candidates = load_candidates()
    if not candidates:
        return "No new candidates today. Merging this PR is a no-op.\n"
    lines = [
        "I check the box next to every item I want published, then merge.",
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
    args = parser.parse_args()

    if args.pr_body:
        print(pr_body())
        return 0

    wanted = None if args.all else {i.strip() for i in args.ids.split(",") if i.strip()}
    promoted = 0
    for path, meta, body in load_candidates():
        if wanted is not None and str(meta.get("id")) not in wanted:
            continue
        name = promote(path, meta, body)
        print(f"promoted {name}")
        promoted += 1

    print(f"promoted {promoted} candidate(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
