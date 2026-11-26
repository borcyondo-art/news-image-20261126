# SPDX-License-Identifier: MIT
"""Copy the finished newspaper artwork to the output directory.

Deterministic: this entrypoint does no rendering, no network access,
no randomness and no clock reads. It copies ``artwork/entry.png``
byte-for-byte to ``$MAKEFUN_OUTPUT_DIR`` (default ``/output``), so
repeated runs produce an identical output file.
"""

import os
import shutil
import sys

ARTWORK_NAME = "entry.png"
DEFAULT_OUTPUT_DIR = "/output"

ENTRY = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "artwork", ARTWORK_NAME
)


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)
    if not os.path.isfile(ENTRY):
        print("missing artwork file: %s" % ENTRY, file=sys.stderr)
        return 1
    os.makedirs(output_dir, exist_ok=True)
    shutil.copyfile(ENTRY, os.path.join(output_dir, ARTWORK_NAME))
    return 0


if __name__ == "__main__":
    sys.exit(main())
