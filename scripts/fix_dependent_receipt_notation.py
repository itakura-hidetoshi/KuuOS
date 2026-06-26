#!/usr/bin/env python3
"""Expand dependent local `Receipt` notation into theorem binder types.

Lean macro hygiene does not capture section variables from a notation RHS.
This script only rewrites the exact generated pattern used by the vacuum
expectation receipt chain.  It leaves definitions and proof bodies unchanged.
"""

from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
FORMAL_ROOT = ROOT / "formal" / "KUOS"

NOTATION = re.compile(
    r'^local notation "Receipt" =>\n(?P<rhs>(?:[ \t]+[^\n]+\n)+)\n',
    re.MULTILINE,
)


def expand_receipt_notation(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    match = NOTATION.search(text)
    if match is None:
        return 0

    rhs_lines = [line.strip() for line in match.group("rhs").splitlines()]
    if not rhs_lines or not rhs_lines[0].endswith("Receipt"):
        raise RuntimeError(f"Unexpected Receipt notation in {path}")

    receipt_type = " ".join(rhs_lines)
    suffix = text[match.end():]
    rewritten_suffix, count = re.subn(r"\bReceipt\b", receipt_type, suffix)
    if count == 0:
        raise RuntimeError(f"Receipt notation has no downstream uses in {path}")

    rewritten = text[: match.start()] + rewritten_suffix
    path.write_text(rewritten, encoding="utf-8")
    return count


def main() -> None:
    changed: list[tuple[Path, int]] = []
    for path in sorted(FORMAL_ROOT.rglob("*.lean")):
        count = expand_receipt_notation(path)
        if count:
            changed.append((path.relative_to(ROOT), count))

    if not changed:
        print("No dependent Receipt notation remains.")
        return

    for path, count in changed:
        print(f"expanded {count:2d} Receipt type uses in {path}")


if __name__ == "__main__":
    main()
