"""Apply digest PR checkbox selections after the PR merges.

Reads the merged PR body, promotes every checked candidate into _posts/, and
discards unchecked candidates from staging so the next digest starts clean.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from pipeline_io import iter_staging, load_front_matter
from promote_drafts import promote

CHECKED_RE = re.compile(r"^\s*-\s*\[[xX]\]\s.*?`id:([0-9a-f]{6,40})`", re.MULTILINE)
UNCHECKED_RE = re.compile(r"^\s*-\s*\[ \]\s.*?`id:([0-9a-f]{6,40})`", re.MULTILINE)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--body-file", required=True, help="file containing the merged PR body")
    args = parser.parse_args()

    body = Path(args.body_file).read_text(encoding="utf-8")
    checked = set(CHECKED_RE.findall(body))
    unchecked = set(UNCHECKED_RE.findall(body))

    promoted = 0
    discarded = 0
    for path in iter_staging():
        meta, post_body = load_front_matter(path)
        cid = str(meta.get("id", path.stem))
        if cid in checked:
            name = promote(path, meta, post_body)
            print(f"promoted {name}")
            promoted += 1
        elif cid in unchecked:
            path.unlink()
            discarded += 1

    print(f"promoted {promoted}, discarded {discarded}, "
          f"left {len(iter_staging())} untouched")
    return 0


if __name__ == "__main__":
    sys.exit(main())
