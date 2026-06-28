from __future__ import annotations

import json

from runtime.kuuos_repository_structure_types_v0_79 import RepositorySnapshot


def _manifest(name: str) -> dict[str, object]:
    version = name.capitalize()
    return {
        "manifest_version": f"fixture_{name}_v0_81",
        "repository_autorepair_contract": True,
        "runtime_modules": [f"runtime/{name}_v0_81.py"],
        "tests": f"tests/test_{name}_v0_81.py",
        "validator": f"scripts/check_{name}_v081.py",
        "documentation": f"docs/{name.upper()}_v0_81.md",
        "strict_formal_root": f"{version}FormalV0_81",
        "aggregate_lean_modules": [f"KUOS.WORLD.{version}V0_81"],
    }


def normal_dual_contract_snapshot() -> RepositorySnapshot:
    alpha = _manifest("alpha")
    beta = _manifest("beta")
    paths = (
        ".github/workflows/alignment-fixture-v081.yml",
        "docs/ALPHA_v0_81.md",
        "docs/BETA_v0_81.md",
        "formal/KuuOSFormal.lean",
        "lakefile.toml",
        "manifests/alpha_v0_81.json",
        "manifests/beta_v0_81.json",
        "notes/unrelated.txt",
        "runtime/alpha_v0_81.py",
        "runtime/beta_v0_81.py",
        "scripts/check_alpha_v081.py",
        "scripts/check_beta_v081.py",
        "scripts/run_kuuos_runtime_full_check_v0_55.py",
        "tests/test_alpha_v0_81.py",
        "tests/test_beta_v0_81.py",
    )
    texts = (
        (
            ".github/workflows/alignment-fixture-v081.yml",
            "name: alignment fixture\n\non:\n  workflow_dispatch:\n",
        ),
        ("docs/ALPHA_v0_81.md", "# Alpha\n"),
        ("docs/BETA_v0_81.md", "# Beta\n"),
        (
            "formal/KuuOSFormal.lean",
            "import KUOS\nimport KUOS.WORLD.AlphaV0_81\nimport KUOS.WORLD.BetaV0_81\n",
        ),
        (
            "lakefile.toml",
            "[[lean_lib]]\nname = \"KuuOSFormal\"\nroots = [\n  \"KuuOSFormal\",\n  \"AlphaFormalV0_81\",\n  \"BetaFormalV0_81\"\n]\n",
        ),
        ("manifests/alpha_v0_81.json", json.dumps(alpha, sort_keys=True)),
        ("manifests/beta_v0_81.json", json.dumps(beta, sort_keys=True)),
        ("notes/unrelated.txt", "unrelated-v1\n"),
        ("runtime/alpha_v0_81.py", "ALPHA = 1\n"),
        ("runtime/beta_v0_81.py", "BETA = 1\n"),
        ("scripts/check_alpha_v081.py", "def main(): return 0\n"),
        ("scripts/check_beta_v081.py", "def main(): return 0\n"),
        (
            "scripts/run_kuuos_runtime_full_check_v0_55.py",
            "VALIDATORS_AFTER_V055: tuple[str, ...] = (\n"
            "    \"scripts/check_alpha_v081.py\",\n"
            "    \"scripts/check_beta_v081.py\",\n"
            ")\n",
        ),
        ("tests/test_alpha_v0_81.py", "def test_alpha(): pass\n"),
        ("tests/test_beta_v0_81.py", "def test_beta(): pass\n"),
    )
    return RepositorySnapshot("incremental-fixture", paths, texts)


def replace_text(
    snapshot: RepositorySnapshot,
    path: str,
    text: str,
) -> RepositorySnapshot:
    if path not in snapshot.all_paths:
        raise ValueError(f"fixture_path_missing:{path}")
    texts = snapshot.texts
    texts[path] = text
    return RepositorySnapshot(
        snapshot.root_label,
        snapshot.all_paths,
        tuple(sorted(texts.items())),
    )


def add_text_path(
    snapshot: RepositorySnapshot,
    path: str,
    text: str,
) -> RepositorySnapshot:
    texts = snapshot.texts
    texts[path] = text
    return RepositorySnapshot(
        snapshot.root_label,
        tuple(sorted(set(snapshot.all_paths) | {path})),
        tuple(sorted(texts.items())),
    )


def remove_path(
    snapshot: RepositorySnapshot,
    path: str,
) -> RepositorySnapshot:
    texts = snapshot.texts
    texts.pop(path, None)
    return RepositorySnapshot(
        snapshot.root_label,
        tuple(item for item in snapshot.all_paths if item != path),
        tuple(sorted(texts.items())),
    )
