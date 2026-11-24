#!/usr/bin/env python3
"""One-Line Roast: The Gadget You Use Every Day.

Writes a single original roast line about the smartwatch I wear every day
to /output/entry.txt. The line is validated against the competition gate
(1-200 UTF-8 characters, not only whitespace, single line) before writing,
then the file is re-read and verified byte-for-byte.
"""

import os
import sys

# The roast: my smartwatch's hourly "breathe" reminder, flipped on itself.
# The watch nags me to breathe while its own battery is the thing dying
# by early evening -- a specific, everyday gripe with a concrete detail.
ROAST = (
    "My smartwatch buzzes every hour to remind me to breathe, "
    "as if I'm the one whose battery dies by 6pm."
)

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200


def validate(line: str) -> None:
    """Enforce the competition gate on the roast line."""
    if not isinstance(line, str):
        raise ValueError("roast line must be a string")
    if len(line) < 1 or len(line) > MAX_CHARS:
        raise ValueError(
            f"roast line must be 1-{MAX_CHARS} characters, got {len(line)}"
        )
    if not line.strip():
        raise ValueError("roast line must not be only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("roast line must be a single line")
    # Must be encodable as UTF-8, since the gate reads the file as UTF-8.
    line.encode("utf-8")


def main() -> int:
    validate(ROAST)

    output_dir = os.path.dirname(OUTPUT_PATH)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(ROAST + "\n")

    # Re-read the file and verify its contents match exactly.
    with open(OUTPUT_PATH, "r", encoding="utf-8") as handle:
        written = handle.read()

    if written != ROAST + "\n":
        raise RuntimeError("verification failed: file contents do not match")
    # The file must hold exactly one line: the roast plus one newline.
    if written.count("\n") != 1:
        raise RuntimeError("verification failed: file must contain one line")
    if len(written.rstrip("\n")) != len(ROAST):
        raise RuntimeError("verification failed: character count mismatch")

    print(f"Wrote {len(ROAST)} characters to {OUTPUT_PATH}")
    print(ROAST)
    return 0


if __name__ == "__main__":
    sys.exit(main())
