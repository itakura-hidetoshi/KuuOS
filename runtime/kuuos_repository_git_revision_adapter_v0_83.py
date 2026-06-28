#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import subprocess
from typing import Iterable

from runtime.kuuos_repository_alignment_normal_form_v0_80 import (
    certify_repository_alignment_normal_form,
)
from runtime.kuuos_repository_certificate_chain_types_v0_82 import (
    RepositoryCertificateChainRecord,
)
from runtime.kuuos_repository_certificate_chain_v0_82 import (
    advance_repository_certificate_chain,
    start_repository_certificate_chain,
)
from runtime.kuuos_repository_git_revision_types_v0_83 import (
    GitRevisionAdapterReceipt,
    GitRevisionObservation,
    git_revision_adapter_receipt_digest,
    git_revision_observation_digest,
)
from runtime.kuuos_repository_structure_types_v0_79 import RepositorySnapshot


def _run_git(
    root: Path,
    arguments: list[str],
    *,
    text: bool,
) -> subprocess.CompletedProcess[str] | subprocess.CompletedProcess[bytes]:
    completed = subprocess.run(
        ["git", "-C", str(root), *arguments],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=text,
        check=False,
    )
    if completed.returncode != 0:
        stderr = completed.stderr
        if isinstance(stderr, bytes):
            message = stderr.decode("utf-8", errors="replace")
        else:
            message = stderr
        command = arguments[0] if arguments else "git"
        raise ValueError(f"git_command_failed:{command}:{message.strip()}")
    return completed


def _canonical_inventory(relative_paths: Iterable[str]) -> tuple[str, ...]:
    normalized: set[str] = set()
    for path in relative_paths:
        if not isinstance(path, str) or not path:
            raise ValueError("inventory_path_invalid")
        if "\x00" in path or "\\" in path or path.startswith("/"):
            raise ValueError(f"inventory_path_invalid:{path}")
        parts = path.split("/")
        if any(part in {"", ".", ".."} for part in parts):
            raise ValueError(f"inventory_path_invalid:{path}")
        normalized.add(path)
    return tuple(sorted(normalized))


def resolve_git_commit(root: Path, revision: str) -> str:
    result = _run_git(
        root.resolve(),
        ["rev-parse", "--verify", f"{revision}^{{commit}}"],
        text=True,
    )
    assert isinstance(result.stdout, str)
    return result.stdout.strip().lower()


def git_commit_parents(root: Path, commit_sha: str) -> tuple[str, ...]:
    result = _run_git(
        root.resolve(),
        ["show", "-s", "--format=%P", commit_sha],
        text=True,
    )
    assert isinstance(result.stdout, str)
    return tuple(item.lower() for item in result.stdout.strip().split() if item)


def git_changed_paths(
    root: Path,
    parent_commit_sha: str,
    current_commit_sha: str,
) -> tuple[str, ...]:
    result = _run_git(
        root.resolve(),
        [
            "diff",
            "--no-renames",
            "--name-only",
            "-z",
            parent_commit_sha,
            current_commit_sha,
        ],
        text=False,
    )
    assert isinstance(result.stdout, bytes)
    paths = tuple(
        item.decode("utf-8")
        for item in result.stdout.split(b"\x00")
        if item
    )
    return _canonical_inventory(paths)


def capture_git_object_snapshot(
    root: Path,
    commit_sha: str,
    relative_paths: Iterable[str],
) -> RepositorySnapshot:
    root = root.resolve()
    inventory = _canonical_inventory(relative_paths)
    resolved_commit = resolve_git_commit(root, commit_sha)
    all_paths: list[str] = []
    text_files: list[tuple[str, str]] = []

    for relative in inventory:
        object_name = f"{resolved_commit}:{relative}"
        exists = subprocess.run(
            ["git", "-C", str(root), "cat-file", "-e", object_name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if exists.returncode != 0:
            continue
        content = _run_git(
            root,
            ["cat-file", "-p", object_name],
            text=False,
        )
        assert isinstance(content.stdout, bytes)
        all_paths.append(relative)
        try:
            text = content.stdout.decode("utf-8")
        except UnicodeDecodeError:
            continue
        text_files.append((relative, text))

    return RepositorySnapshot(
        f"{root.name}@{resolved_commit[:12]}",
        tuple(all_paths),
        tuple(text_files),
    )


def observe_git_revision(
    root: Path,
    parent_revision: str,
    current_revision: str,
    relative_paths: Iterable[str],
) -> tuple[RepositorySnapshot, RepositorySnapshot, GitRevisionObservation]:
    root = root.resolve()
    inventory = _canonical_inventory(relative_paths)
    parent_sha = resolve_git_commit(root, parent_revision)
    current_sha = resolve_git_commit(root, current_revision)
    current_parents = git_commit_parents(root, current_sha)
    if current_parents != (parent_sha,):
        raise ValueError("current_commit_parent_mismatch")

    changed_paths = git_changed_paths(root, parent_sha, current_sha)
    outside = tuple(sorted(set(changed_paths) - set(inventory)))
    if outside:
        raise ValueError(f"git_changed_path_outside_inventory:{outside[0]}")

    parent_snapshot = capture_git_object_snapshot(
        root,
        parent_sha,
        inventory,
    )
    current_snapshot = capture_git_object_snapshot(
        root,
        current_sha,
        inventory,
    )
    observation = GitRevisionObservation(
        root.name,
        parent_sha,
        current_sha,
        current_parents,
        changed_paths,
        inventory,
        parent_snapshot.digest,
        current_snapshot.digest,
        True,
        False,
        "",
    )
    observation = replace(
        observation,
        observation_digest=git_revision_observation_digest(observation),
    )
    return parent_snapshot, current_snapshot, observation


def start_repository_certificate_chain_from_git(
    chain_id: str,
    root: Path,
    revision: str,
    relative_paths: Iterable[str],
    max_chain_length: int = 1024,
) -> tuple[
    RepositorySnapshot,
    GitRevisionObservation,
    RepositoryCertificateChainRecord,
    GitRevisionAdapterReceipt,
]:
    root = root.resolve()
    inventory = _canonical_inventory(relative_paths)
    commit_sha = resolve_git_commit(root, revision)
    snapshot = capture_git_object_snapshot(root, commit_sha, inventory)
    normal_form = certify_repository_alignment_normal_form(snapshot)
    record = start_repository_certificate_chain(
        chain_id,
        commit_sha,
        snapshot,
        normal_form,
        max_chain_length=max_chain_length,
    )
    observation = GitRevisionObservation(
        root.name,
        "",
        commit_sha,
        git_commit_parents(root, commit_sha),
        (),
        inventory,
        snapshot.digest,
        snapshot.digest,
        True,
        False,
        "",
    )
    observation = replace(
        observation,
        observation_digest=git_revision_observation_digest(observation),
    )
    receipt = GitRevisionAdapterReceipt(
        "GENESIS",
        observation.observation_digest,
        record.record_digest,
        True,
        True,
        True,
        True,
        False,
        "",
    )
    receipt = replace(
        receipt,
        receipt_digest=git_revision_adapter_receipt_digest(receipt),
    )
    return snapshot, observation, record, receipt


def advance_repository_certificate_chain_from_git(
    chain_id: str,
    previous_record: RepositoryCertificateChainRecord,
    root: Path,
    parent_revision: str,
    current_revision: str,
    relative_paths: Iterable[str],
    max_states: int = 4096,
) -> tuple[
    RepositorySnapshot,
    RepositorySnapshot,
    GitRevisionObservation,
    RepositoryCertificateChainRecord,
    GitRevisionAdapterReceipt,
]:
    parent_snapshot, current_snapshot, observation = observe_git_revision(
        root,
        parent_revision,
        current_revision,
        relative_paths,
    )
    record = advance_repository_certificate_chain(
        chain_id,
        previous_record,
        parent_snapshot,
        current_snapshot,
        observation.parent_commit_sha,
        observation.current_commit_sha,
        observation.changed_paths,
        max_states=max_states,
    )
    receipt = GitRevisionAdapterReceipt(
        "ADVANCE",
        observation.observation_digest,
        record.record_digest,
        True,
        record.declared_changed_paths == record.computed_changed_paths,
        observation.object_database_read,
        not observation.working_tree_read,
        False,
        "",
    )
    receipt = replace(
        receipt,
        receipt_digest=git_revision_adapter_receipt_digest(receipt),
    )
    return parent_snapshot, current_snapshot, observation, record, receipt
