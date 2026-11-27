#!/usr/bin/env python3
"""Hand the rendered front page to the grader.

entry.png sits beside this file, already finished. The only job here is
to drop a copy of it into the directory the grader names through
MAKEFUN_OUTPUT_DIR. Because nothing is drawn or computed at this point,
repeated runs always hand over identical bytes."""

from pathlib import Path
import os
import sys


def main() -> int:
    here = Path(__file__).resolve().parent
    picture = here / "entry.png"
    named = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not named:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    folder = Path(named)
    folder.mkdir(parents=True, exist_ok=True)
    folder.joinpath("entry.png").write_bytes(picture.read_bytes())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
