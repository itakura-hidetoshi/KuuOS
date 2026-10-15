#!/usr/bin/env python3
"""Produce a review artifact for existing build/validation consumers.

Only tracked source with explicit source/document suffixes is read. No
credentials, environment, Git metadata or untracked files are collected.
This report is not a replacement for running the validators.
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
    prefixes = ('scripts/', 'tests/', 'runtime/', 'ci/', '.github/workflows/',
                'src/', 'specs/', 'manifests/', 'contracts/', 'formal/',
                'docs/', 'examples/', 'validators/', 'validation_cases/',
                'memoryos/', 'tools/', 'policies/', 'packets/', 'chain_indexes/')
    suffixes = {'.py', '.json', '.yaml', '.yml', '.toml', '.md', '.sh', '.txt', '.lean', '.csv'}
    with zipfile.ZipFile(args.output / 'review-sources.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
        for name in paths:
            if not name or name.startswith('legacy/'):
                continue
            p = Path(name)
            included = name.startswith(prefixes) or name in {
                'lakefile.toml', 'lake-manifest.json', 'lean-toolchain',
                'pyproject.toml', 'README.md', 'ROADMAP.md', 'AGENTS.md',
                'Makefile', 'LICENSE', 'NOTICE', 'COPYRIGHT.md', 'GOVERNANCE.md'}
            if not included:
                continue
            if p.suffix not in suffixes and p.name not in {'lean-toolchain', 'Makefile', 'LICENSE', 'NOTICE'}:
                continue
            file = ROOT / p
            if not file.is_file() or file.is_symlink():
                continue
            text = file.read_text(encoding='utf-8')
            archive.writestr(name, text)
            if 'KuuOSFormal' in text or 'lakefile.toml' in text:
                consumers.append({'path': name, 'matches': [{'line': i, 'text': line} for i, line in enumerate(text.splitlines(), 1) if 'KuuOSFormal' in line or 'lakefile.toml' in line]})
        # The frozen source package is necessary to reproduce compatibility
        # checks locally; only its four declared version-controlled inputs enter.
        for name in paths:
            if name.startswith('legacy/v5.291/formal/') and name.endswith('.lean') or name in {
                'legacy/v5.291/lakefile.toml', 'legacy/v5.291/lake-manifest.json',
                'legacy/v5.291/lean-toolchain'}:
                file = ROOT / name
                if file.is_file() and not file.is_symlink():
                    archive.writestr(name, file.read_text(encoding='utf-8'))
    (args.output / 'consumers.json').write_text(json.dumps(consumers, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(consumers)} existing build/validation consumers recorded for migration review')

if __name__ == '__main__':
    main()
