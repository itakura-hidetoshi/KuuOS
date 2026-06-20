#!/usr/bin/env python3
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]
path = root / "packets" / "memoryos_github_chat_long_term_writeback_finality_v0_2.json"
data = json.loads(path.read_text(encoding="utf-8"))
assert data["schema_version"] == "v0.2-finality"
assert data["integration"]["global_governance_runner_contains_v0_2_validator"] is True
assert data["integration"]["canonical_validator_entrypoint_exists"] is True
assert data["workflow"]["fallback"] == "global governance runner integration"
assert data["authority"]["github"] == "external_pointer_only"
assert data["release_mode"]["append_only"] is True
for relative in data["completed"].values():
    assert (root / relative).exists(), relative
print("PASS: KuuOS MemoryOS writeback finality v0.2 validates")
