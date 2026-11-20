#!/usr/bin/env bash
# Prepare an isolated KuuOS Sandbox for DIRECT Lean, never GitHub CI.
# No git/gh CLI, repository source edits, model API or GitHub writes.
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: bash scripts/kuuos_sandbox_prepare_v1.sh /absolute/KuuOS [Lean-dependency-module ...]" >&2
  exit 2
fi
ROOT="$(realpath "$1")"
shift
[[ -f "$ROOT/lean-toolchain" && -f "$ROOT/lake-manifest.json" ]] || {
  echo "NO_DATA: not a KuuOS repository snapshot" >&2
  exit 2
}
PIN="4.30.0-rc2"
EXPECTED_TAR_SHA256="5b51625f154f0a13b37bd892f1d95f79e9fd5b9f0d095b4126215ee2bc8dbe86"
EXPECTED_TAR_SIZE="529580981"
CACHE_ROOT="${KUUOS_LEAN_CACHE_ROOT:-/vercel/kuuos-lean-pinned-$PIN}"
BIN_DIR="${LEAN_BIN_DIR:-$CACHE_ROOT/lean-$PIN-linux/bin}"

python3 - "$ROOT" <<'PY'
import json,pathlib,sys
r=pathlib.Path(sys.argv[1])
assert (r/"lean-toolchain").read_text().strip()=="leanprover/lean4:v4.30.0-rc2"
m=json.loads((r/"lake-manifest.json").read_text())
math=[x.get("rev") for x in m.get("packages",[]) if x.get("name")=="mathlib"]
assert math==["5450b53e5ddc75d46418fabb605edbf36bd0beb6"], math
print("KUUOS_SANDBOX_ENV_MANIFEST_PIN_OK")
PY

if [[ ! -x "$BIN_DIR/lean" || ! -x "$BIN_DIR/lake" ]]; then
  [[ "$(uname -s)" == Linux && "$(uname -m)" == x86_64 ]] || {
    echo "PIN_MISMATCH: bundled installer supports Linux x86_64 only" >&2
    exit 2
  }
  command -v curl >/dev/null || exit 2
  command -v sha256sum >/dev/null || exit 2
  command -v unzstd >/dev/null || {
    echo "NO_DATA: install zstd/unzstd in the Sandbox first" >&2
    exit 2
  }
  mkdir -p "$CACHE_ROOT"
  TMP="$(mktemp -d "$CACHE_ROOT/.download.XXXXXXXX")"
  trap 'rm -rf "$TMP"' EXIT
  ASSET="$TMP/lean-$PIN-linux.tar.zst"
  curl --fail --location --silent --show-error --retry 3 --retry-delay 4 \
    --connect-timeout 25 --max-time 360 \
    "https://github.com/leanprover/lean4/releases/download/v$PIN/lean-$PIN-linux.tar.zst" \
    -o "$ASSET"
  [[ "$(stat -c '%s' "$ASSET")" == "$EXPECTED_TAR_SIZE" ]] || {
    echo "PIN_MISMATCH: Lean release size" >&2
    exit 2
  }
  printf '%s  %s\n' "$EXPECTED_TAR_SHA256" "$ASSET" | sha256sum --check --status || {
    echo "PIN_MISMATCH: Lean release SHA256" >&2
    exit 2
  }
  tar --use-compress-program=unzstd -xf "$ASSET" -C "$CACHE_ROOT"
fi

export PATH="$BIN_DIR:$PATH"
lean --version | grep -F "version $PIN" >/dev/null || {
  echo "PIN_MISMATCH: Lean binary" >&2
  exit 2
}
lake --version | grep -F "Lean version $PIN" >/dev/null || {
  echo "PIN_MISMATCH: Lake binary" >&2
  exit 2
}
cd "$ROOT"
# Lake may fetch pinned dependencies internally; no direct git/gh CLI call.
lake exe cache get
for MODULE in "$@"; do
  [[ "$MODULE" =~ ^[A-Za-z_][A-Za-z0-9_.]*$ ]] || {
    echo "Invalid dependency Lean module: $MODULE" >&2
    exit 2
  }
  lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true \
    build "$MODULE"
done
echo "KUUOS_SANDBOX_PINNED_ENV_READY"
echo "Lean $(lean --version)"
echo "Mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6"
echo "Next: put CodeAI candidates outside $ROOT; run scripts/kuuos_sandbox_lean_cycle_v1.py"
