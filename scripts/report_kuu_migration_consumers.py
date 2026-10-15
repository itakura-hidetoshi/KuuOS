#!/usr/bin/env python3
"""Produce a review artifact for legacy build/validation consumers.

Only tracked repository source is read. No environment, credentials or
untracked workspace files are collected. This report does not change any
validator and is not a replacement for their tests.
"""
from pathlib import Path
import argparse
import json
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    paths = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
    consumers = []
    with zipfile.ZipFile(args.output / 'review-sources.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
        for name in paths:
            p = Path(name)
            if not name or name.startswith('legacy/'):
                continue
            included = name.startswith(('scripts/', 'tests/', 'runtime/', 'ci/', '.github/workflows/', 'src/', 'specs/', 'manifests/', 'contracts/'))
            included = included or name in {'lakefile.toml', 'lake-manifest.json', 'lean-toolchain', 'pyproject.toml', 'README.md', 'ROADMAP.md'}
            if not included or p.suffix not in {'.py', '.json', '.yaml', '.yml', '.toml', '.md', '.sh', '.txt'} and name != 'lean-toolchain':
                continue
            file = ROOT / p
            if not file.is_file() or file.is_symlink():
                continue
            text = file.read_text(encoding='utf-8')
            archive.writestr(name, text)
            if 'KuuOSFormal' in text or 'lakefile.toml' in text:
                consumers.append({'path': name, 'matches': [{'line': i, 'text': line} for i, line in enumerate(text.splitlines(), 1) if 'KuuOSFormal' in line or 'lakefile.toml' in line]})
    (args.output / 'consumers.json').write_text(json.dumps(consumers, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(consumers)} existing build/validation consumers recorded for migration review')

if __name__ == '__main__':
    main()
