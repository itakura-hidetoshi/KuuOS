from __future__ import annotations

import json

from runtime.kuuos_repository_structure_types_v0_79 import RepositorySnapshot


def defective_repository_snapshot() -> RepositorySnapshot:
    manifest = {
        "manifest_version": "fixture_v0_79",
        "repository_autorepair_contract": True,
        "runtime_modules": ["runtime/fixture_v0_79.py"],
        "tests": "tests/test_fixture_v0_79.py",
        "validator": "scripts/check_fixture_v079.py",
        "strict_formal_root": "FixtureFormalV0_79",
        "aggregate_lean_modules": ["KUOS.WORLD.FixtureV0_79"],
    }
    paths = (
        ".github/workflows/fixture-v079.yml",
        "formal/KUOS/WORLD/FixtureV0_79.lean",
        "formal/FixtureFormalV0_79.lean",
        "formal/KuuOSFormal.lean",
        "lakefile.toml",
        "manifests/fixture_v0_79.json",
        "runtime/fixture_v0_79.py",
        "scripts/check_fixture_v079.py",
        "scripts/run_kuuos_runtime_full_check_v0_55.py",
        "tests/test_fixture_v0_79.py",
    )
    texts = (
        (
            ".github/workflows/fixture-v079.yml",
            "name: fixture\n\non:\n  workflow_dispatch:\n  pull_request:\n    paths:\n      - 'runtime/**'\n\npermissions:\n  contents: read\n",
        ),
        ("formal/KuuOSFormal.lean", "import KUOS\n"),
        (
            "lakefile.toml",
            "[[lean_lib]]\nname = \"KuuOSFormal\"\nroots = [\n  \"KuuOSFormal\"\n]\n",
        ),
        ("manifests/fixture_v0_79.json", json.dumps(manifest, sort_keys=True)),
        (
            "scripts/run_kuuos_runtime_full_check_v0_55.py",
            "VALIDATORS_AFTER_V055: tuple[str, ...] = (\n)\n\n\ndef _runtime_environment():\n    return {}\n",
        ),
    )
    return RepositorySnapshot("fixture", paths, texts)
