#!/usr/bin/env python3
from pathlib import Path
import json
import runpy

root = Path(__file__).resolve().parents[1]
doc = root / "docs" / "MEMORYOS_GITHUB_CHAT_LONG_TERM_WRITEBACK_v0_2.md"
manifest = root / "specs" / "memoryos_github_chat_long_term_writeback_manifest_v0_2.yaml"
packet = root / "examples" / "memoryos_github_chat_long_term_writeback_packet_v0_2.json"
finality = root / "scripts" / "check_memoryos_writeback_finality_v0_2.py"

for path in (doc, manifest, packet, finality):
    if not path.exists():
        raise SystemExit(f"missing: {path.relative_to(root)}")

assert "sequential_same_conversation" in manifest.read_text(encoding="utf-8")
data = json.loads(packet.read_text(encoding="utf-8"))
assert data["github_receipt"]["status"] == "verified"
assert data["memory_writeback_receipt"]["mode"] == "additive_only"
runpy.run_path(str(finality), run_name="__main__")
print("PASS: KuuOS MemoryOS GitHub chat long-term writeback v0.2 validates")
