#!/usr/bin/env python3
from __future__ import annotations

import re

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_structure_observer_v0_79 import (
    LAKEFILE,
    LEAN_AGGREGATE_ROOT,
    RUNTIME_ROOT,
)
from runtime.kuuos_repository_structure_types_v0_79 import (
    RepositoryObservation,
    RepositoryPatch,
    RepositoryRepairCandidate,
    RepositorySnapshot,
)

ALLOWED_REPAIR_PATHS = (
    RUNTIME_ROOT,
    LEAN_AGGREGATE_ROOT,
    LAKEFILE,
)


def _register_runtime_validator(text: str, validator: str) -> str:
    if validator in text:
        return text
    pattern = re.compile(
        r"(VALIDATORS_AFTER_V055:\s*tuple\[str, \.\.\.\]\s*=\s*\()(.*?)(\n\))",
        re.DOTALL,
    )
    match = pattern.search(text)
    if match is None:
        raise ValueError("runtime_validator_tuple_missing")
    body = match.group(2).rstrip()
    replacement = f'{match.group(1)}{body}\n    "{validator}",{match.group(3)}'
    return text[:match.start()] + replacement + text[match.end():]


def _register_lake_root(text: str, root_name: str) -> str:
    if f'"{root_name}"' in text:
        return text
    match = re.search(r"roots\s*=\s*\[(.*?)\n\]", text, flags=re.DOTALL)
    if match is None:
        raise ValueError("lake_roots_block_missing")
    body = match.group(1).rstrip()
    if body and not body.endswith(","):
        body += ","
    replacement = f'roots = [{body}\n  "{root_name}"\n]'
    return text[:match.start()] + replacement + text[match.end():]


def _register_aggregate_import(text: str, module: str) -> str:
    import_line = f"import {module}"
    if import_line in text:
        return text
    return text.rstrip() + f"\n{import_line}\n"


def _remove_direct_pr_trigger(text: str) -> str:
    lines = text.splitlines(keepends=True)
    start = None
    end = None
    in_on = False
    for index, line in enumerate(lines):
        if line.rstrip("\r\n") == "on:":
            in_on = True
            continue
        if in_on and line and not line.startswith(" "):
            break
        if in_on and line.strip() == "pull_request:":
            start = index
            end = index + 1
            while end < len(lines):
                candidate = lines[end]
                if candidate.strip() and len(candidate) - len(candidate.lstrip()) <= 2:
                    break
                end += 1
            break
    if start is None or end is None:
        return text
    return "".join(lines[:start] + lines[end:])


def _patch(
    snapshot: RepositorySnapshot,
    path: str,
    after_text: str,
    kind: str,
    reason: str,
) -> RepositoryPatch:
    before = snapshot.texts.get(path)
    if before is None:
        raise ValueError(f"repair_target_missing:{path}")
    return RepositoryPatch(
        path,
        canonical_digest(before),
        after_text,
        kind,
        reason,
    )


def generate_repository_repair_candidates(
    snapshot: RepositorySnapshot,
    observation: RepositoryObservation,
    max_candidates: int = 32,
) -> tuple[RepositoryRepairCandidate, ...]:
    if observation.snapshot_digest != snapshot.digest:
        raise ValueError("observation_snapshot_mismatch")
    if max_candidates <= 0:
        raise ValueError("max_candidates_invalid")

    candidates: list[RepositoryRepairCandidate] = []
    texts = snapshot.texts

    def add(path: str, after: str, kind: str, reason: str) -> None:
        if len(candidates) >= max_candidates or after == texts.get(path):
            return
        patch = _patch(snapshot, path, after, kind, reason)
        candidates.append(RepositoryRepairCandidate(
            f"repository-repair-{len(candidates):03d}",
            snapshot.digest,
            observation.digest,
            (patch,),
            path in ALLOWED_REPAIR_PATHS or path.startswith(".github/workflows/"),
        ))

    for validator in observation.missing_runtime_validator_registrations:
        add(
            RUNTIME_ROOT,
            _register_runtime_validator(texts.get(RUNTIME_ROOT, ""), validator),
            "REGISTER_RUNTIME_VALIDATOR",
            validator,
        )
    for root_name in observation.missing_lake_roots:
        add(
            LAKEFILE,
            _register_lake_root(texts.get(LAKEFILE, ""), root_name),
            "REGISTER_LAKE_ROOT",
            root_name,
        )
    for module in observation.missing_aggregate_imports:
        add(
            LEAN_AGGREGATE_ROOT,
            _register_aggregate_import(texts.get(LEAN_AGGREGATE_ROOT, ""), module),
            "REGISTER_AGGREGATE_IMPORT",
            module,
        )
    for workflow in observation.direct_pr_trigger_workflows:
        add(
            workflow,
            _remove_direct_pr_trigger(texts.get(workflow, "")),
            "REMOVE_DUPLICATE_PR_TRIGGER",
            workflow,
        )
    return tuple(candidates)
