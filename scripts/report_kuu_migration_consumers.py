#!/usr/bin/env python3
"""Report tracked validation references as JSON; do not package source files."""
from pathlib import Path
import argparse
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    paths = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
    consumers = []
    for name in paths:
        if not name.startswith(('scripts/', 'tests/', 'runtime/', '.github/workflows/', 'manifests/')):
            continue
        file = ROOT / name
        if file.suffix not in {'.py', '.json', '.yaml', '.yml'} or not file.is_file() or file.is_symlink():
            continue
        text = file.read_text(encoding='utf-8')
        matches = [{'line': i, 'text': line} for i, line in enumerate(text.splitlines(), 1)
                   if 'KuuOSFormal' in line or 'lakefile.toml' in line]
        if matches:
            consumers.append({'path': name, 'matches': matches})
    (args.output / 'consumers.json').write_text(json.dumps(consumers, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(consumers)} explicit source references recorded; no source archive generated')

if __name__ == '__main__':
    main()
