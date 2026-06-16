#!/usr/bin/env python3
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.check_context_gerbe_coherence_kernel_v0_14 import main

if __name__ == "__main__":
    main()
