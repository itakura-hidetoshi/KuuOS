#!/usr/bin/env bash
# KuuOS-only pinned Lean MCP stdio launcher. No credentials or repo edits.
set -euo pipefail

usage() {
  printf 'Usage: %s [--check-pins] /absolute/path/to/KuuOS\n' "$0" >&2
  exit 64
}

check_only=0
if [[ ${1:-} == '--check-pins' ]]; then
  check_only=1
  shift
fi
[[ $# -eq 1 && $1 == /* && -d $1 ]] || usage
root=$(cd -- "$1" && pwd -P)

python3 - "$root" <<'PY'
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
expected_lean = 'leanprover/lean4:v4.30.0-rc2'
expected_mathlib = '5450b53e5ddc75d46418fabb605edbf36bd0beb6'
toolchain = (root / 'lean-toolchain').read_text(encoding='utf-8').strip()
if toolchain != expected_lean:
    raise SystemExit(f'Lean toolchain mismatch: expected {expected_lean}, found {toolchain}')
manifest = json.loads((root / 'lake-manifest.json').read_text(encoding='utf-8'))
matches = [p for p in manifest.get('packages', []) if p.get('name') == 'mathlib']
if len(matches) != 1 or matches[0].get('rev') != expected_mathlib:
    raise SystemExit('Mathlib pin mismatch or missing')
print('KUUOS_LEAN_MCP_PIN_CHECK_SUCCESS', file=sys.stderr)
PY

if (( check_only )); then
  exit 0
fi

command -v uvx >/dev/null || { echo 'uvx required (install uv)' >&2; exit 69; }
command -v lake >/dev/null || { echo 'lake required (install pinned Lean toolchain via elan)' >&2; exit 69; }

export LEAN_PROJECT_PATH="$root"
export LEAN_LOG_LEVEL='NONE'
export LEAN_MCP_SCRATCH_SLOTS="${LEAN_MCP_SCRATCH_SLOTS:-1}"
# Preserve semantic inspection, goals, and in-memory tactic trials.
# Disable generic code execution, builds, profiling, and network premise search.
export LEAN_MCP_DISABLED_TOOLS="${LEAN_MCP_DISABLED_TOOLS:-lean_run_code,lean_build,lean_profile_proof,lean_minimal_hypotheses,lean_leansearch,lean_loogle,lean_leanfinder,lean_state_search,lean_hammer_premise}"
cd -- "$root"
exec uvx --from lean-lsp-mcp==0.30.0 lean-lsp-mcp --transport stdio
