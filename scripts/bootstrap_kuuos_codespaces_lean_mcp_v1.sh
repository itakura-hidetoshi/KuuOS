#!/usr/bin/env bash
# Opt-in KuuOS Codespaces setup. Preserves pinned Lean, mathlib and Git source.
set -euo pipefail

usage() {
  echo "Usage: bash scripts/bootstrap_kuuos_codespaces_lean_mcp_v1.sh [--check|--install|--smoke]" >&2
  exit 64
}

mode="${1:---check}"
[[ $# -le 1 ]] || usage
[[ "$mode" == --check || "$mode" == --install || "$mode" == --smoke ]] || usage

root=$(pwd -P)
launcher="$root/scripts/run_kuuos_lean_mcp_stdio_v1.sh"
[[ -f "$launcher" ]] || { echo "Run at KuuOS checkout root" >&2; exit 66; }
bash "$launcher" --check-pins "$root"

if [[ "$mode" == --check ]]; then
  printf 'KUUOS_CODESPACES_PIN_PREFLIGHT_SUCCESS\n'
  exit 0
fi

# Keep the installation strictly within the codespace user home.
export PATH="$HOME/.elan/bin:$HOME/.local/bin:$PATH"
command -v curl >/dev/null || { echo 'curl is required' >&2; exit 69; }
command -v git >/dev/null || { echo 'git is required by elan/Lake' >&2; exit 69; }
command -v python3 >/dev/null || { echo 'python3 is required' >&2; exit 69; }

if [[ "$mode" == --install ]]; then
  if ! command -v elan >/dev/null; then
    tmp_init=$(mktemp)
    trap 'rm -f "$tmp_init"' EXIT
    curl --fail --silent --show-error --location \
      https://elan.lean-lang.org/elan-init.sh -o "$tmp_init"
    sh "$tmp_init" -y --default-toolchain none
  fi
  if ! command -v uvx >/dev/null; then
    tmp_uv=$(mktemp)
    trap 'rm -f "$tmp_uv"' EXIT
    curl --fail --silent --show-error --location \
      https://astral.sh/uv/install.sh -o "$tmp_uv"
    sh "$tmp_uv"
  fi
  # Elan resolves the current project's exact lean-toolchain; never install stable.
  elan toolchain install leanprover/lean4:v4.30.0-rc2
fi

command -v elan >/dev/null || { echo 'elan unavailable' >&2; exit 69; }
command -v lake >/dev/null || { echo 'lake unavailable' >&2; exit 69; }
command -v uvx >/dev/null || { echo 'uvx unavailable' >&2; exit 69; }

version=$(lake env lean --version)
printf 'Current project Lean: %s\n' "$version"
[[ "$version" == *'version 4.30.0-rc2'* ]] || {
  echo 'Lean binary version mismatch; refusing to proceed' >&2
  exit 65
}

if [[ "$mode" == --install ]]; then
  if [[ "${KUUOS_CODESPACES_SKIP_MATHLIB_CACHE:-0}" != 1 ]]; then
    # Downloads only the pinned cache. Does not rebuild the full KuuOS library.
    lake exe cache get
  else
    echo 'Mathlib cache skipped by explicit KUUOS_CODESPACES_SKIP_MATHLIB_CACHE=1' >&2
  fi
  uvx --from lean-lsp-mcp==0.30.0 lean-lsp-mcp --version

  # Install the separately pinned, checksum-verified official Tunnel CLI.
  # No API key or tunnel ID is read; no tunnel is started automatically.
  if [[ "${KUUOS_CODESPACES_SKIP_TUNNEL_CLIENT:-0}" != 1 ]]; then
    bash scripts/install_kuuos_tunnel_client_v1.sh --install
  else
    echo 'Tunnel client skipped by explicit KUUOS_CODESPACES_SKIP_TUNNEL_CLIENT=1' >&2
  fi
  bash "$launcher" --check-pins "$root"
  printf 'KUUOS_CODESPACES_LEAN_MCP_BOOTSTRAP_SUCCESS\n'
  echo 'Next: bash scripts/bootstrap_kuuos_codespaces_lean_mcp_v1.sh --smoke'
  exit 0
fi

# Only run a bounded, real Lean MCP trial on an existing representative module.
# Does not assert theorem certification or attempt a full Strict Lean build.
lake env lean -o /tmp/kuuos-codespaces-mcp-smoke.olean \
  formal/KUOS/DependentOriginationFunctorialTransportV0_1.lean
PYTHONPATH=. python3 scripts/check_kuuos_lean_lsp_mcp_multi_attempt_v1.py
bash "$launcher" --check-pins "$root"
printf 'KUUOS_CODESPACES_LEAN_MCP_SMOKE_SUCCESS\n'
