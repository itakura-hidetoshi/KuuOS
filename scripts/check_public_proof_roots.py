#!/usr/bin/env python3
"""Check repair wiring only. Existing mathematical proof status is not reset."""
from __future__ import annotations
import json
from pathlib import Path
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.check_kuu_foundation import lean_imports

def check(root: Path) -> dict:
    errors = []
    try:
        old = tomllib.loads((root / 'legacy/v5.291/lakefile.toml').read_text())
        new = tomllib.loads((root / 'lakefile.toml').read_text())
        expected = [r for lib in old['lean_lib'] for r in lib.get('roots', [])]
        published = [r for lib in new['lean_lib'] for r in lib.get('roots', [])]
        missing = sorted(set(expected) - set(published))
        if missing:
            errors.append('removed public roots: ' + ', '.join(missing))
        if len(published) != len(set(published)):
            errors.append('duplicate public roots')
        if {'KuuOSStrict', 'Kuu'} & set(published):
            errors.append('Kuu modules are internal modules, not separate published roots')
        for name in published:
            if not (root / 'formal' / (name.replace('.', '/') + '.lean')).is_file():
                errors.append('missing public source: ' + name)
        if new.get('defaultTargets') != ['KuuOSFormal']:
            errors.append('the standard public build must remain KuuOSFormal')
        old_imports = set(lean_imports((root / 'legacy/v5.291/formal/KuuOSFormal.lean').read_text()))
        new_imports = set(lean_imports((root / 'formal/KuuOSFormal.lean').read_text()))
        if old_imports - new_imports:
            errors.append('previous aggregate imports were omitted')
        if 'KuuOSStrict' not in new_imports:
            errors.append('independent core must remain available through the public aggregate')
        scope = json.loads((root / 'ci/kuu_legacy_consumer_scope.json').read_text())['paths']
        for path in scope:
            if path.startswith(('.github/workflows/', 'scripts/')):
                text = (root / path).read_text()
                if ('--legacy --' in text or 'legacy/v5.291/formal/' in text
                        or 'lake-package-directory: legacy/v5.291' in text):
                    errors.append('consumer still archived: ' + path)
        return {'ok': not errors, 'previous_public_roots': len(expected),
                'published_roots': len(published), 'missing_roots': missing,
                'errors': errors, 'scope': 'configuration repair, not theorem re-acceptance'}
    except (OSError, ValueError, KeyError) as exc:
        return {'ok': False, 'errors': [str(exc)]}

if __name__ == '__main__':
    report = check(ROOT)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report['ok'] else 1)
