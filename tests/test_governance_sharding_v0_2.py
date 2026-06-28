#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from run_all_governance_full_checks_v0_1 import COMMANDS
from run_all_governance_shard_v0_2 import partition_commands


class GovernanceShardingV02Tests(unittest.TestCase):
    def test_every_command_is_assigned_exactly_once(self) -> None:
        shards = partition_commands(COMMANDS, 8)
        flattened = [command for shard in shards for command in shard]
        self.assertEqual(len(flattened), len(COMMANDS))
        self.assertEqual(
            sorted(tuple(command) for command in flattened),
            sorted(tuple(command) for command in COMMANDS),
        )

    def test_partition_is_deterministic(self) -> None:
        self.assertEqual(
            partition_commands(COMMANDS, 8),
            partition_commands(COMMANDS, 8),
        )

    def test_round_robin_preserves_inventory_order_per_shard(self) -> None:
        shards = partition_commands(COMMANDS, 8)
        for shard_index, shard in enumerate(shards):
            expected = [
                list(COMMANDS[index])
                for index in range(shard_index, len(COMMANDS), 8)
            ]
            self.assertEqual(shard, expected)

    def test_empty_inventory_is_supported(self) -> None:
        self.assertEqual(partition_commands([], 3), [[], [], []])

    def test_nonpositive_shard_count_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            partition_commands(COMMANDS, 0)

    def test_selection_builder_emits_all_expected_receipts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = pathlib.Path(directory) / "selection.json"
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/build_full_audit_selection_v0_2.py",
                    "--output",
                    str(output),
                    "--count",
                    "8",
                ],
                cwd=ROOT,
                check=False,
            )
            self.assertEqual(result.returncode, 0)
            payload = json.loads(output.read_text(encoding="utf-8"))
            ids = {item["id"] for item in payload["selected_checks"]}
            self.assertEqual(
                ids,
                {"workflow-integrity"}
                | {f"full-governance-{index:02d}" for index in range(8)},
            )

    def test_selection_builder_rejects_nonpositive_count(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/build_full_audit_selection_v0_2.py",
                    "--output",
                    str(pathlib.Path(directory) / "selection.json"),
                    "--count",
                    "0",
                ],
                cwd=ROOT,
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            self.assertNotEqual(result.returncode, 0)

    def test_workflow_uses_eight_bounded_shards(self) -> None:
        text = (
            ROOT / ".github/workflows/all_governance_sharded_v0_2.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("max-parallel: 4", text)
        self.assertIn("index: [0, 1, 2, 3, 4, 5, 6, 7]", text)
        self.assertIn("scripts/build_audit_summary.py", text)

    def test_workflow_has_post_merge_main_trigger(self) -> None:
        text = (
            ROOT / ".github/workflows/all_governance_sharded_v0_2.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("push:", text)
        self.assertIn("branches: [main]", text)
        self.assertIn("- 'tests/**'", text)
        self.assertNotIn("pull_request:", text)

    def test_superseded_push_audits_cancel_without_canceling_manual_audits(self) -> None:
        text = (
            ROOT / ".github/workflows/all_governance_sharded_v0_2.yml"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "group: sharded-full-governance-${{ github.event_name }}-${{ github.ref }}",
            text,
        )
        self.assertIn(
            "cancel-in-progress: ${{ github.event_name == 'push' }}",
            text,
        )
        self.assertNotIn("cancel-in-progress: false", text)

    def test_stable_manual_entry_delegates_to_sharded_workflow(self) -> None:
        text = (
            ROOT / ".github/workflows/all_governance_validation.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("workflow_dispatch:", text)
        self.assertIn(
            "uses: ./.github/workflows/all_governance_sharded_v0_2.yml",
            text,
        )
        self.assertNotIn("push:", text)
        self.assertNotIn("pull_request:", text)


if __name__ == "__main__":
    unittest.main()
