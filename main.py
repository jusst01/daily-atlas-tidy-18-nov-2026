#!/usr/bin/env python3
import os
import sys
import tempfile

def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(script_dir, "entry.png")

    if not os.path.exists(src_path):
        print(f"Error: bundled entry.png not found at {src_path}", file=sys.stderr)
        sys.exit(1)

    with open(src_path, "rb") as f:
        src_data = f.read()
    src_size = len(src_data)

    dest_path = os.path.join(output_dir, "entry.png")

    fd, tmp_path = tempfile.mkstemp(dir=output_dir, prefix="entry_tmp_", suffix=".png")
    try:
        with os.fdopen(fd, "wb") as tmp_f:
            tmp_f.write(src_data)
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, dest_path)
    finally:
        if os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

    actual_size = os.path.getsize(dest_path)
    if actual_size != src_size:
        print(f"Error: deployed file size {actual_size} does not match expected {src_size}", file=sys.stderr)
        sys.exit(1)

    print(f"Deployed {dest_path} ({actual_size} bytes)")
    sys.exit(0)

if __name__ == "__main__":
    main()
