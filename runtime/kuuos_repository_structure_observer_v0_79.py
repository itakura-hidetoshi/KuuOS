#!/usr/bin/env python3
from __future__ import annotations

import json

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_structure_types_v0_79 import (
    RepositoryContract,
    RepositoryObservation,
    RepositorySnapshot,
)

RUNTIME_ROOT = "scripts/run_kuuos_runtime_full_check_v0_55.py"
LEAN_AGGREGATE_ROOT = "formal/KuuOSFormal.lean"
LAKEFILE = "lakefile.toml"


def parse_repository_contracts(
    snapshot: RepositorySnapshot,
) -> tuple[tuple[RepositoryContract, ...], tuple[str, ...]]:
    contracts: list[RepositoryContract] = []
    malformed: list[str] = []
    for path, text in snapshot.text_files:
        if not path.startswith("manifests/") or not path.endswith(".json"):
            continue
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            continue
        if payload.get("repository_autorepair_contract") is not True:
            continue
        validator = payload.get("validator")
        strict_root = payload.get("strict_formal_root")
        modules = payload.get("aggregate_lean_modules")
        runtime_modules = payload.get("runtime_modules", [])
        if (
            not isinstance(validator, str)
            or not isinstance(strict_root, str)
            or not isinstance(modules, list)
            or not all(isinstance(item, str) for item in modules)
            or not isinstance(runtime_modules, list)
        ):
            malformed.append(path)
            continue
        references = {
            validator,
            *(item for item in runtime_modules if isinstance(item, str)),
        }
        for key in ("fixture", "tests", "documentation"):
            value = payload.get(key)
            if isinstance(value, str):
                references.add(value)
        contracts.append(RepositoryContract(
            path,
            canonical_digest(payload),
            tuple(sorted(references)),
            validator,
            strict_root,
            tuple(sorted(modules)),
        ))
    contracts.sort(key=lambda item: item.manifest_path)
    return tuple(contracts), tuple(sorted(malformed))


def has_direct_pr_trigger(text: str) -> bool:
    in_on = False
    for line in text.splitlines():
        if line == "on:":
            in_on = True
            continue
        if in_on and line and not line.startswith(" "):
            return False
        if in_on and line.strip() == "pull_request:":
            return True
    return False


def observe_repository_structure(snapshot: RepositorySnapshot) -> RepositoryObservation:
    texts = snapshot.texts
    paths = set(snapshot.all_paths)
    contracts, malformed = parse_repository_contracts(snapshot)
    runtime_root = texts.get(RUNTIME_ROOT, "")
    lean_root = texts.get(LEAN_AGGREGATE_ROOT, "")
    lakefile = texts.get(LAKEFILE, "")

    missing_paths: set[str] = set()
    missing_validators: set[str] = set()
    missing_roots: set[str] = set()
    missing_imports: set[str] = set()
    for contract in contracts:
        for path in contract.referenced_paths:
            if path not in paths:
                missing_paths.add(f"{contract.manifest_path}:{path}")
        if contract.validator not in runtime_root:
            missing_validators.add(contract.validator)
        if f'"{contract.strict_formal_root}"' not in lakefile:
            missing_roots.add(contract.strict_formal_root)
        for module in contract.aggregate_lean_modules:
            if f"import {module}" not in lean_root:
                missing_imports.add(module)

    direct_pr = tuple(sorted(
        path
        for path, text in snapshot.text_files
        if path.startswith(".github/workflows/")
        and path != ".github/workflows/pr-governance-gate.yml"
        and "workflow_dispatch:" in text
        and has_direct_pr_trigger(text)
    ))
    score = (
        100 * len(malformed)
        + 100 * len(missing_paths)
        + 20 * len(missing_validators)
        + 20 * len(missing_roots)
        + 20 * len(missing_imports)
        + 10 * len(direct_pr)
    )
    return RepositoryObservation(
        snapshot.digest,
        tuple(contract.digest for contract in contracts),
        malformed,
        tuple(sorted(missing_paths)),
        tuple(sorted(missing_validators)),
        tuple(sorted(missing_roots)),
        tuple(sorted(missing_imports)),
        direct_pr,
        score,
    )
