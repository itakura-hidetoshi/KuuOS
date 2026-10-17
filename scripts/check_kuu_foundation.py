#!/usr/bin/env python3
"""Check current Kuu source closure, not mathematical completeness.

Existing KUOS proof authority is preserved. Inspect the independent Kuu
import closure for actual Gray dependencies, separately from the public API.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
import tomllib
from pathlib import Path

MODULE = re.compile(r'(?:[A-Za-z_][A-Za-z_0-9]*|«[^»\n]+»)(?:\.(?:[A-Za-z_][A-Za-z_0-9]*|«[^»\n]+»))*\Z')
COMMANDS = {'public', 'private', 'import', 'open', 'namespace', 'section', 'end',
            'universe', 'variable', 'variables', 'set_option', 'noncomputable',
            'def', 'abbrev', 'theorem', 'lemma', 'instance', 'structure', 'inductive',
            'example', 'attribute', 'export', 'class', 'module', 'initialize', 'infix',
            'syntax', 'macro', 'elab'}


def code_only(text: str) -> str:
    """Mask Lean strings and nested comments while preserving line breaks."""
    out = list(text)
    i, depth, string = 0, 0, False
    while i < len(text):
        if depth:
            if text.startswith('/-', i):
                out[i:i+2] = '  '; depth += 1; i += 2; continue
            if text.startswith('-/', i):
                out[i:i+2] = '  '; depth -= 1; i += 2; continue
            if text[i] != '\n': out[i] = ' '
            i += 1; continue
        if string:
            if text[i] == '\\' and i + 1 < len(text):
                out[i:i+2] = '  '; i += 2; continue
            if text[i] == '"': string = False
            if text[i] != '\n': out[i] = ' '
            i += 1; continue
        if text.startswith('/-', i):
            out[i:i+2] = '  '; depth = 1; i += 2; continue
        if text.startswith('--', i):
            j = text.find('\n', i)
            if j < 0: j = len(text)
            out[i:j] = ' ' * (j-i); i = j; continue
        if text[i] == '"':
            out[i] = ' '; string = True
        i += 1
    if depth or string:
        raise ValueError('unterminated Lean comment or string')
    return ''.join(out)


def lean_imports(text: str) -> list[str]:
    tokens = re.findall(r'\S+', code_only(text))
    result = []
    i = 0
    while i < len(tokens):
        if tokens[i] != 'import':
            i += 1; continue
        i += 1
        start = i
        while i < len(tokens) and tokens[i] not in COMMANDS and not tokens[i].startswith(('#', '@')):
            token = tokens[i]
            if not MODULE.fullmatch(token):
                raise ValueError(f'invalid or unsupported module syntax: {token}')
            result.append(token.replace("«", "").replace("»", ""))
            i += 1
        if start == i:
            raise ValueError('empty import command')
    return result


def check(root: Path) -> dict:
    root = root.resolve()
    errors: list[str] = []
    current = {'KuuOSStrict', 'Kuu'}
    for p in sorted((root / 'formal/Kuu').rglob('*.lean')):
        current.add('.'.join(p.relative_to(root / 'formal').with_suffix('').parts))
    try:
        config = tomllib.loads((root / 'lakefile.toml').read_text(encoding='utf-8'))
        if config.get('defaultTargets') != ['KuuOSFormal']:
            errors.append('defaultTargets must be exactly [KuuOSFormal]')
        libraries = config.get('lean_lib', [])
        if len(libraries) != 1 or libraries[0].get('name') != 'KuuOSFormal':
            errors.append('current package must expose only the KuuOSFormal library')
        elif libraries[0].get('srcDir') != 'formal':
            errors.append('current source directory must be formal')
        else:
            if not {'KuuOSStrict', 'Kuu'} <= set(libraries[0].get('roots', [])):
                errors.append('independent Kuu roots are missing from the public package')
    except (OSError, tomllib.TOMLDecodeError) as exc:
        errors.append(f'configuration: {exc}')
    pending = sorted(current)
    visited = set()
    edges = []
    while pending:
        module = pending.pop()
        if module in visited: continue
        visited.add(module)
        path = root / 'formal' / (module.replace('.', '/') + '.lean')
        if not path.is_file():
            errors.append(f'missing current module: {module}'); continue
        if not path.resolve().is_relative_to(root / 'formal'):
            errors.append(f'current source escapes formal: {module}'); continue
        try:
            source = path.read_text(encoding='utf-8')
            clean = code_only(source)
            if 'Gray' in module or re.search(r'\b(?:GrayGrade|GradedThreeCell)\b', clean):
                errors.append(f'{module}: Gray-dependent source in the independent foundation')
            is_new_core = module.startswith('Kuu.') or module in {'Kuu', 'KuuOSStrict'}
            if is_new_core:
                for bad in re.findall(r'\b(?:sorry|admit|axiom|native_decide)\b', clean):
                    errors.append(f'{module}: prohibited proof shortcut {bad}')
            for dependency in lean_imports(source):
                edges.append([module, dependency])
                if dependency.startswith('Mathlib.'):
                    continue
                if dependency == 'Mathlib':
                    if is_new_core:
                        errors.append(f'{module}: umbrella Mathlib import is prohibited')
                elif dependency == 'KuuOSFormal':
                    errors.append(f'{module}: public aggregate must not be a foundation prerequisite')
                elif dependency.startswith(('Kuu.', 'KUOS.')) or dependency in {'KuuOSStrict', 'Kuu', 'KUOS'}:
                    pending.append(dependency)
                else:
                    errors.append(f'{module}: legacy or unapproved dependency {dependency}')
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f'{module}: {exc}')
    return {'ok': not errors, 'current_modules': sorted(visited), 'import_edges': edges,
            'legacy_source_files': len(list((root / 'formal/KUOS').rglob('*.lean'))),
            'errors': errors,
            'scope': 'independent Kuu import closure; retained proof validity is unchanged'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = check(args.root)
    text = json.dumps(report, ensure_ascii=False, indent=2)
    print(text)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + '\n', encoding='utf-8')
    return 0 if report['ok'] else 1

if __name__ == '__main__':
    sys.exit(main())
