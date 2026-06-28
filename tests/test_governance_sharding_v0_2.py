#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys
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
        first = partition_commands(COMMANDS, 8)
        second = partition_commands(COMMANDS, 8)
        self.assertEqual(first, second)

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


if __name__ == "__main__":
    unittest.main()
