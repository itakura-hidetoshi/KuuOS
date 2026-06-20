#!/usr/bin/env python3
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]
doc = root / "docs" / "MEMORYOS_GITHUB_CHAT_LONG_TERM_WRITEBACK_v0_2.md"
manifest = root / "specs" / "memoryos_github_chat_long_term_writeback_manifest_v0_2.yaml"
packet = root / "examples" / "memoryos_github_chat_long_term_writeback_packet_v0_2.json"

for path in (doc, manifest, packet):
    if not path.exists():
        raise SystemExit(f"missing: {path.relative_to(root)}")

assert "sequential_same_conversation" in manifest.read_text(encoding="utf-8")
data = json.loads(packet.read_text(encoding="utf-8"))
assert data["github_receipt"]["status"] == "verified"
assert data["memory_writeback_receipt"]["mode"] == "additive_only"
print("PASS: KuuOS MemoryOS GitHub chat long-term writeback v0.2 validates")
