#!/usr/bin/env python3
"""Ship the finished front page for Friday 20 November 2026.

The picture itself was drawn at build time by draw.py (Pillow) and is
stored in this repository as entry.png. This program does the only job
the grader needs: place an exact copy of that picture at
<output>/entry.png, using nothing but the Python standard library, so
the sandbox (no network, nothing installed) can run it twice and get
the same bytes both times.

Run it the way the grader does:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

Or set the output directory with --out <dir>.
"""

import argparse
import hashlib
import os
import shutil
import sys
from pathlib import Path

SOURCE_NAME = "entry.png"
DEFAULT_OUT = "/output"


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _output_dir():
    if os.environ.get("MAKEFUN_OUTPUT_DIR"):
        return Path(os.environ["MAKEFUN_OUTPUT_DIR"])
    return Path(DEFAULT_OUT)


def _copy_entry(out_dir):
    source = Path(__file__).resolve().parent / SOURCE_NAME
    with open(source, "rb") as handle:
        magic = handle.read(8)
    if magic != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("refusing to ship %s: not a PNG file" % SOURCE_NAME)
    if source.stat().st_size > 1048576:
        raise SystemExit("refusing to ship %s: over the 1 MiB cap" % SOURCE_NAME)
    target = Path(out_dir) / SOURCE_NAME
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    if _sha256(source) != _sha256(target):
        raise SystemExit("copy check failed: %s != %s" % (source, target))
    return target


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default=None,
                        help="output directory (default: $MAKEFUN_OUTPUT_DIR or /output)")
    args = parser.parse_args(argv)
    out_dir = Path(args.out) if args.out else _output_dir()
    target = _copy_entry(out_dir)
    print("wrote %s (%d bytes)" % (target, target.stat().st_size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
