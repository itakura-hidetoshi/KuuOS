#!/usr/bin/env python3
"""Run the independent-boundary regression suite and verify the frozen snapshot."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def main():
    for command in [
        [sys.executable, '-m', 'unittest', '-v', 'tests.test_kuu_foundation',
         'tests.test_kuu_consumer_migration', 'tests.test_formal_package_boundary',
         'tests.test_kuu_formal_contract_scope', 'tests.test_kuu_historical_manifest_scope',
         'tests.test_kuu_legacy_ci_integration', 'tests.test_kuu_multiline_registration'],
        [sys.executable, 'scripts/migrate_kuu_consumers.py', '--check'],
        [sys.executable, 'scripts/check_kuu_foundation.py', '--output', 'artifacts/kuu-foundation/dependencies.json'],
    ]:
        result = subprocess.run(command, cwd=ROOT, check=False)
        if result.returncode:
            return result.returncode
    expected = {
        'legacy/v5.291/formal': 'd72e83b11ea316730ded81cd6d73612b2ce09919',
        'legacy/v5.291/lakefile.toml': 'e4cc0839908ffbd2aefe2c672c8841fe6f2ff4aa',
        'legacy/v5.291/lake-manifest.json': '4b795033645fd37e42e67014abc3e0d5925a227c',
        'legacy/v5.291/lean-toolchain': '6c7e31fffe3e03be3e0d7021acd9cd848e44db26',
    }
    for path, sha in expected.items():
        result = subprocess.run(['git', 'rev-parse', 'HEAD:' + path], cwd=ROOT,
                                text=True, capture_output=True, check=False)
        if result.returncode or result.stdout.strip() != sha:
            print(f'Legacy preservation check failed: {path}', file=sys.stderr)
            return 1
    print('PASS: independent current dependency boundary and exact historical source snapshot')
    return 0

if __name__ == '__main__':
    sys.exit(main())
