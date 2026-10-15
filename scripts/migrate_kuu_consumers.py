#!/usr/bin/env python3
"""Read-only migration verifier for existing consumers of the Kuu formal split.

All source changes are committed through GitHub MCP. This script performs no
network writes, creates no archives and cannot update any repository ref.
"""
from __future__ import annotations
import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Mapping

ROOT = Path(__file__).resolve().parents[1]
LEGACY = 'legacy/v5.291'
CURRENT_WORKFLOWS = {
    '.github/workflows/pr-governance-gate.yml',
    '.github/workflows/lean-formal-validation.yml',
    '.github/workflows/kuu-independent-foundation.yml',
}


def replace_once(text: str, old: str, new: str, path: str) -> str:
    if new in text:
        return text
    if text.count(old) != 1:
        raise ValueError(f'{path}: required source context not unique: {old[:80]}')
    return text.replace(old, new, 1)


def legacy_workflow(text: str) -> str:
    # Only actual shell-command prefixes, never documentation, quoted command
    # expectations, workflow names, trigger filters or the Python validators.
    pattern = re.compile(r'(?m)^(\s*(?:-\s+)?(?:run:\s*)?)lake(?=\s)')
    if not pattern.search(text):
        return text
    text = pattern.sub(r'\1python3 scripts/run_formal_package.py --legacy --', text)
    text = re.sub(r'(git diff --exit-code -- lake-manifest\.json)(?! legacy/v5\.291)',
                  r'\1 legacy/v5.291/lake-manifest.json', text)
    lines = text.splitlines(keepends=True)
    i = 0
    while i < len(lines):
        if 'uses: leanprover/lean-action@' not in lines[i]:
            i += 1
            continue
        raw_indent = len(lines[i]) - len(lines[i].lstrip())
        indent = raw_indent if lines[i].lstrip().startswith('- ') else raw_indent - 2
        end = i + 1
        while end < len(lines):
            line = lines[end]
            if line.strip() and len(line) - len(line.lstrip()) <= indent:
                break
            end += 1
        block = ''.join(lines[i:end])
        if 'lake-package-directory:' not in block:
            position = next((j for j in range(i+1,end) if lines[j].strip() == 'with:'), None)
            if position is None:
                lines[i+1:i+1] = [' '*(indent+2)+'with:\n', ' '*(indent+4)+'lake-package-directory: '+LEGACY+'\n']
                end += 2
            else:
                lines.insert(position+1, ' '*(indent+4)+'lake-package-directory: '+LEGACY+'\n')
                end += 1
        i = end
    return ''.join(lines)


def transform_sources(sources: Mapping[str, str]) -> dict[str, str]:
    changed: dict[str, str] = {}
    for name, original in sorted(sources.items()):
        text = original
        if name.startswith('scripts/check_') and name.endswith('.py') and name != 'scripts/check_kuu_foundation.py':
            text = text.replace('ROOT / "formal/KuuOSFormal.lean"',
                                'ROOT / "legacy/v5.291/formal/KuuOSFormal.lean"')
            if name.startswith('scripts/check_world_'):
                text = text.replace('ROOT / "lakefile.toml"', 'ROOT / "legacy/v5.291/lakefile.toml"')
        if name == 'scripts/run_pr_entry_check_v0_5.py':
            text = text.replace('"formal/KuuOSFormal.lean": [',
                                '"legacy/v5.291/formal/KuuOSFormal.lean": [')
        if name.startswith('manifests/') and name.endswith('.json'):
            payload = json.loads(text)
            dirty = False
            if isinstance(payload, dict):
                if payload.get('aggregate_formal_root') == 'formal/KuuOSFormal.lean':
                    payload['aggregate_formal_root'] = LEGACY + '/formal/KuuOSFormal.lean'
                    dirty = True
                if payload.get('repository_autorepair_contract') is True and payload.get('formal_package') != 'legacy-v5.291':
                    payload['formal_package'] = 'legacy-v5.291'
                    dirty = True
            if dirty:
                text = json.dumps(payload, ensure_ascii=False, indent=2) + '\n'
        if name.startswith('.github/workflows/') and name.endswith(('.yml','.yaml')) and name not in CURRENT_WORKFLOWS:
            text = legacy_workflow(text)
        if name == 'scripts/check_kuuos_repository_live_v079.py':
            old = '    paths = set(BASE_PATHS + MANIFESTS)\n'
            new = old + '    paths.update(("legacy/v5.291/formal/KuuOSFormal.lean", "legacy/v5.291/lakefile.toml"))\n'
            text = replace_once(text, old, new, name)
        if name == 'runtime/kuuos_repository_structure_observer_v0_79.py':
            old = '        runtime_modules = payload.get("runtime_modules", [])\n'
            new = old + '        formal_package = payload.get("formal_package", "current")\n'
            text = replace_once(text, old, new, name)
            old = '            or not isinstance(runtime_modules, list)\n'
            new = old + '            or formal_package not in {"current", "legacy-v5.291"}\n'
            text = replace_once(text, old, new, name)
            old = '        for key in ("fixture", "tests", "documentation"):\n'
            new = '        if formal_package == "legacy-v5.291":\n            references.update({"legacy/v5.291/formal/KuuOSFormal.lean", "legacy/v5.291/lakefile.toml"})\n' + old
            text = replace_once(text, old, new, name)
            old = '    for contract in contracts:\n        for path in contract.referenced_paths:\n'
            new = '''    for contract in contracts:
        package = json.loads(texts[contract.manifest_path]).get("formal_package", "current")
        prefix = "legacy/v5.291/" if package == "legacy-v5.291" else ""
        # An explicit manifest scope chooses its own formal inputs. No missing
        # historical result is ever repaired by importing it into current Kuu.
        lean_root = texts.get(prefix + LEAN_AGGREGATE_ROOT, "")
        lakefile = texts.get(prefix + LAKEFILE, "")
        for path in contract.referenced_paths:
'''
            text = replace_once(text, old, new, name)
        if name == 'runtime/kuuos_repository_repair_candidates_v0_79.py':
            # Frozen historical sources are never targets for automated repair;
            # nor may the old engine reinstate an old root in independent Kuu.
            old = '    for root_name in observation.missing_lake_roots:\n        add(\n'
            new = '''    for root_name in observation.missing_lake_roots:
        if "import KuuOSStrict" in texts.get(LEAN_AGGREGATE_ROOT, ""):
            if root_name not in {"KuuOSFormal", "KuuOSStrict", "Kuu"}:
                continue  # defect remains visible; no unauthorized legacy repair
        add(
'''
            text = replace_once(text, old, new, name)
            old = '    for module in observation.missing_aggregate_imports:\n        add(\n'
            new = '''    for module in observation.missing_aggregate_imports:
        if "import KuuOSStrict" in texts.get(LEAN_AGGREGATE_ROOT, ""):
            if not (module == "KuuOSStrict" or module == "Kuu" or module.startswith("Kuu.")):
                continue  # keep the obstruction, never import KUOS into Kuu
        add(
'''
            text = replace_once(text, old, new, name)
        if text != original:
            if name.endswith('.py'):
                compile(text, name, 'exec')
            changed[name] = text
    return changed


def tracked_sources(root: Path) -> dict[str,str]:
    files = subprocess.check_output(['git','ls-files','-z'], cwd=root).decode().split('\0')
    result = {}
    for name in files:
        if name.startswith(('scripts/','runtime/','manifests/','.github/workflows/')) and name.endswith(('.py','.json','.yaml','.yml')):
            path = root / name
            if path.is_symlink():
                raise ValueError('symlink not allowed: ' + name)
            result[name] = path.read_text(encoding='utf-8')
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    sources = tracked_sources(ROOT)
    changes = transform_sources(sources)
    # Idempotence matters: applying the plan must not progressively rewrite code.
    if transform_sources(dict(sources, **changes)):
        raise ValueError('migration is not idempotent')
    head = subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip()
    base_tree = subprocess.check_output(['git','rev-parse','HEAD^{tree}'], cwd=ROOT, text=True).strip()
    report = {'base_commit': head, 'base_tree': base_tree,
              'changed_count': len(changes), 'changed_paths': list(changes)}
    print('KUU_MIGRATION_RESULT=' + json.dumps(report, ensure_ascii=False))
    return 1 if args.check and changes else 0

if __name__ == '__main__':
    raise SystemExit(main())
