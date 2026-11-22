"""news-image-20261121 entrypoint (page rebuilt 22 November 2026).

Stdlib-only copier: takes the committed entry.png beside this file and
writes it to the output directory as entry.png. It verifies the image
signature (PNG or JPEG) and the 1 MiB cap before copying, and exits 0
only when the copy is in place. Outside the grader, the environment
variable MAKEFUN_OUTPUT_DIR stands in for /output.
"""

import os
import shutil
import sys

# The competition's hard cap on the entry image: 1 MiB.
MAX_BYTES = 1_048_576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dst = os.path.join(out_dir, "entry.png")

    with open(src, "rb") as fh:
        head = fh.read(8)
    size = os.path.getsize(src)
    if size > MAX_BYTES:
        print(f"entry.png too large: {size} bytes", file=sys.stderr)
        return 1
    if not (head.startswith(PNG_MAGIC) or head.startswith(JPEG_MAGIC)):
        print("entry.png is neither PNG nor JPEG", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    os.chmod(dst, 0o644)
    if os.path.getsize(dst) != size:
        print("copy size mismatch", file=sys.stderr)
        return 1
    with open(dst, "rb") as fh:
        copied = fh.read(8)
    if not (copied.startswith(PNG_MAGIC) or copied.startswith(JPEG_MAGIC)):
        print("copied file lost its image signature", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
