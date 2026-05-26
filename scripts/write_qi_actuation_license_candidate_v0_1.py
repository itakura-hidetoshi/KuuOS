#!/usr/bin/env python3
from __future__ import annotations

import sys

MESSAGE = "Deprecated legacy entrypoint. Use scripts/write_qi_license_candidate_phase_v0_1.py with packets/qi_process_tensor_review_phase_boundary_packet_v0_1.json."


def main() -> int:
    print(MESSAGE, file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
