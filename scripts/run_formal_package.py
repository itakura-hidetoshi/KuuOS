#!/usr/bin/env python3
"""Invoke pinned Lake in the explicitly selected package (current by default)."""
from __future__ import annotations
import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.formal_package_boundary import (
    CURRENT, LEGACY, SNAPSHOT_BLOBS, package_directory, snapshot_file, validate_targets,
)


def lake_command(root: Path, legacy: bool, arguments: list[str]) -> tuple[Path,list[str]]:
    package = LEGACY if legacy else CURRENT
    if arguments and arguments[0] == '--':
        arguments = arguments[1:]
    if not arguments:
        raise ValueError('an explicit Lake command is required')
    for arg in arguments:
        if arg in {'-d','--dir','-f','--file','--old'} or arg.startswith(('--dir=', '--file=', '-d=', '-f=')):
            raise ValueError('package overrides and incomplete rebuilds are not permitted')
    commands = [(i,x) for i,x in enumerate(arguments) if not x.startswith('-')]
    if not commands or commands[0][1] not in {'build','update','env','exe'}:
        raise ValueError('supported commands: build, update, env, exe')
    index, command = commands[0]
    if command == 'build':
        validate_targets(root, package, arguments[index+1:])
    directory = package_directory(root, package)
    if legacy:
        for relative in SNAPSHOT_BLOBS:
            snapshot_file(root, relative)
    return directory, ['lake', *arguments]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--legacy', action='store_true')
    parser.add_argument('arguments', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    try:
        directory, command = lake_command(ROOT, args.legacy, args.arguments)
        print(f'[formal package {LEGACY if args.legacy else CURRENT}] '+ ' '.join(command), flush=True)
        result = subprocess.run(command, cwd=directory, check=False)
        if args.legacy:
            for relative in SNAPSHOT_BLOBS:
                snapshot_file(ROOT, relative)
        return result.returncode
    except (OSError, ValueError) as exc:
        print(f'Formal package boundary: {exc}', file=sys.stderr)
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
