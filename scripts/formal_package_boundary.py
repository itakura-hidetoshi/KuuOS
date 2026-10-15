"""Explicit package boundaries for current proofs and historical validation.

The current Kuu root is never changed to satisfy a historical import check.
A historical artifact is checked against its recorded Git blob before use.
This helper does not claim that a historical theorem has been ported.
"""
from __future__ import annotations

import hashlib
import re
import tomllib
from pathlib import Path
from collections.abc import Sequence

CURRENT = 'current'
LEGACY = 'legacy-v5.291'
CURRENT_ROOTS = frozenset({'KuuOSFormal', 'KuuOSStrict', 'Kuu'})
SNAPSHOT_BLOBS = {
    'formal/KuuOSFormal.lean': 'b01bee482bb8a34f3f5ccc2746028dda56ff35f2',
    'lakefile.toml': 'e4cc0839908ffbd2aefe2c672c8841fe6f2ff4aa',
    'lake-manifest.json': '4b795033645fd37e42e67014abc3e0d5925a227c',
    'lean-toolchain': '6c7e31fffe3e03be3e0d7021acd9cd848e44db26',
}


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()


def package_directory(root: Path, package: str) -> Path:
    root = root.resolve()
    if package == CURRENT:
        return root
    if package == LEGACY:
        path = root / 'legacy/v5.291'
        if not path.is_dir() or not path.resolve().is_relative_to(root):
            raise ValueError('missing or external legacy snapshot directory')
        return path
    raise ValueError(f'unknown formal package: {package}')


def snapshot_file(root: Path, relative: str) -> Path:
    if relative not in SNAPSHOT_BLOBS:
        raise ValueError(f'undeclared snapshot artifact: {relative}')
    base = package_directory(root, LEGACY)
    path = base / relative
    if not path.is_file() or not path.resolve().is_relative_to(base.resolve()):
        raise ValueError(f'missing or external snapshot artifact: {relative}')
    if git_blob_sha(path.read_bytes()) != SNAPSHOT_BLOBS[relative]:
        raise ValueError(f'changed snapshot artifact: {relative}')
    return path


def historical_aggregate(root: Path) -> Path:
    return snapshot_file(root, 'formal/KuuOSFormal.lean')


def historical_lakefile(root: Path) -> Path:
    return snapshot_file(root, 'lakefile.toml')


def validate_targets(root: Path, package: str, targets: Sequence[str]) -> None:
    if not targets:
        raise ValueError('at least one explicit target is required')
    if package == CURRENT:
        roots = CURRENT_ROOTS
    elif package == LEGACY:
        config = tomllib.loads(historical_lakefile(root).read_text(encoding='utf-8'))
        roots = {name for lib in config.get('lean_lib', []) for name in lib.get('roots', [])}
    else:
        raise ValueError(f'unknown formal package: {package}')
    for target in targets:
        if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*', target):
            raise ValueError(f'invalid formal target: {target}')
        if not any(target == name or target.startswith(name + '.') for name in roots):
            hint = '; historical targets require the explicit --legacy package' if package == CURRENT else ''
            raise ValueError(f'{target} is not a target of {package}{hint}')
