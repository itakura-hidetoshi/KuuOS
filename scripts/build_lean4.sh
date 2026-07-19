#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scripts/build_lean4.sh [options] [TARGET]

Compile the pinned KuuOS Lean 4 package with Lake.

Options:
  --target TARGET  Lake target to compile (default: KuuOSFormal)
  --no-update      Skip `lake update` and manifest verification
  --no-cache       Skip `lake exe cache get`
  --non-strict     Do not promote Lean warnings or `sorry` to errors
  --clean          Run `lake clean` before compiling
  -h, --help       Show this help

Examples:
  scripts/build_lean4.sh
  scripts/build_lean4.sh KuuOSCodeAIV0_1
  scripts/build_lean4.sh --no-update --no-cache KUOS
EOF
}

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

target="KuuOSFormal"
run_update=true
run_cache=true
strict=true
clean=false
positional_target_seen=false

while (($#)); do
  case "$1" in
    --target)
      (($# >= 2)) || { echo "error: --target requires a value" >&2; exit 2; }
      target="$2"
      positional_target_seen=true
      shift 2
      ;;
    --no-update)
      run_update=false
      shift
      ;;
    --no-cache)
      run_cache=false
      shift
      ;;
    --non-strict)
      strict=false
      shift
      ;;
    --clean)
      clean=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --*)
      echo "error: unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
    *)
      if [[ "$positional_target_seen" == true ]]; then
        echo "error: only one target may be supplied" >&2
        exit 2
      fi
      target="$1"
      positional_target_seen=true
      shift
      ;;
  esac
done

if [[ ! "$target" =~ ^[A-Za-z0-9_.-]+$ ]]; then
  echo "error: invalid Lake target: $target" >&2
  exit 2
fi

for required in lean-toolchain lakefile.toml lake-manifest.json; do
  [[ -f "$required" ]] || { echo "error: missing $required" >&2; exit 2; }
done

if ! command -v lake >/dev/null 2>&1; then
  cat >&2 <<'EOF'
error: `lake` is not available.
Install Lean through elan, then reopen the shell:
  curl https://elan.lean-lang.org/elan-init.sh -sSf | sh
The repository's lean-toolchain file will select the pinned Lean version.
EOF
  exit 127
fi

echo "KuuOS Lean 4 build"
echo "  toolchain: $(tr -d '\r\n' < lean-toolchain)"
echo "  target:    $target"
echo "  strict:    $strict"
lean --version
lake --version

if [[ "$clean" == true ]]; then
  lake clean
fi

if [[ "$run_update" == true ]]; then
  lake update
  if command -v git >/dev/null 2>&1 && git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    git diff --exit-code -- lake-manifest.json
  fi
fi

if [[ "$run_cache" == true ]]; then
  lake exe cache get
fi

lake_args=()
if [[ "$strict" == true ]]; then
  lake_args+=(
    -KleanArgs=-DwarningAsError=true
    -KleanArgs=-DsorryAsError=true
  )
fi

LEAN_ABORT_ON_PANIC=1 lake "${lake_args[@]}" build "$target"
