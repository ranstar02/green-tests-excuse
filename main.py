#!/usr/bin/env python3
"""green-tests-excuse: one-line excuse for green tests that prove nothing.

Writes a single excuse (<=140 chars) to /output/entry.txt, falling back
to ./output/entry.txt when /output is not writable.
"""

import os

ENTRY = "I shipped the test suite by mistake \u2014 the green checkmarks were the product all along."


def main():
    assert 1 <= len(ENTRY) <= 140, "ENTRY must be 1-140 characters"
    assert ENTRY.strip(), "ENTRY must not be only whitespace"
    assert "\n" not in ENTRY, "ENTRY must be a single line"

    candidates = ["/output/entry.txt", os.path.join("output", "entry.txt")]
    written_path = None
    last_error = None
    for path in candidates:
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(ENTRY)
            written_path = path
            break
        except OSError as exc:  # /output not writable in this environment
            last_error = exc
    if written_path is None:
        raise RuntimeError(f"could not write entry: {last_error}")

    with open(written_path, "r", encoding="utf-8", newline="") as f:
        back = f.read()
    assert back == ENTRY, "round-trip mismatch"
    assert 1 <= len(back) <= 140, "written entry out of gate range"

    print(f"Wrote {len(ENTRY)} chars ({len(ENTRY.encode('utf-8'))} bytes) to {written_path}")
    print(ENTRY)


if __name__ == "__main__":
    main()
