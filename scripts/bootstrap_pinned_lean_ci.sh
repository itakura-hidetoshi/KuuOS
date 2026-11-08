#!/usr/bin/env bash
# CI-only installer for the exact Lean 4 toolchain already fixed by lean-toolchain.
# Avoid the non-retrying Elan installer hop in lean-action@v1 when a release
# asset CDN returns 504. No change to Lean, mathlib, Lake targets or CI audits.
#
# Two trusted release routes are tried with bounded retries. Every successful
# download is validated against the digest published on the official Lean 4
# v4.30.0-rc2 GitHub release BEFORE extraction. Failure remains fatal.
set -euo pipefail

PINNED_TOOLCHAIN='leanprover/lean4:v4.30.0-rc2'
LEAN_VERSION='4.30.0-rc2'
TAR_SHA256='5b51625f154f0a13b37bd892f1d95f79e9fd5b9f0d095b4126215ee2bc8dbe86'
ZIP_SHA256='0006942b918c7fb9751a5e50b9e5ad570c5cc6aa758c980a3abc054dd8739d35'
TAR_SIZE=529580981
ZIP_SIZE=825954087

if [[ "$(tr -d '\r\n' < lean-toolchain)" != "$PINNED_TOOLCHAIN" ]]; then
  echo "ERROR: committed Lean toolchain is not the audited pin" >&2
  exit 1
fi
if [[ "$(uname -s)" != Linux || "$(uname -m)" != x86_64 ]]; then
  echo "ERROR: this pinned recovery path supports only Linux x86_64" >&2
  exit 1
fi

runner_tmp="$RUNNER_TEMP"
mkdir -p "$runner_tmp"
scratch="$(mktemp -d "$runner_tmp/kuuos-lean-download.XXXXXXXX")"
trap 'rm -rf "$scratch"' EXIT

download_official() {
  local url="$1" destination="$2"
  echo "Trying audited Lean $LEAN_VERSION release URL: $url"
  # Retry transient 5xx/connection errors without ignoring final failures.
  curl --fail --location --silent --show-error \
    --retry 4 --retry-delay 8 --retry-max-time 300 \
    --connect-timeout 25 --max-time 300 \
    --output "$destination" "$url"
}

validate_asset() {
  local file="$1" expected_size="$2" expected_sha="$3"
  local actual_size
  actual_size="$(stat -c '%s' "$file")"
  if [[ "$actual_size" != "$expected_size" ]]; then
    echo "ERROR: Lean release asset size mismatch ($actual_size)" >&2
    exit 1
  fi
  if ! printf '%s  %s\n' "$expected_sha" "$file" | sha256sum --check --status; then
    echo "ERROR: Lean release asset SHA256 mismatch" >&2
    exit 1
  fi
  echo "Pinned Lean release asset verified against official size and SHA256"
}

archive=''
kind=''
if command -v zstd >/dev/null 2>&1 && tar --help | grep -q -- '--zstd'; then
  tarball="$scratch/lean-$LEAN_VERSION-linux.tar.zst"
  for url in \
    "https://releases.lean-lang.org/lean4/v$LEAN_VERSION/lean-$LEAN_VERSION-linux.tar.zst" \
    "https://github.com/leanprover/lean4/releases/download/v$LEAN_VERSION/lean-$LEAN_VERSION-linux.tar.zst"; do
    if download_official "$url" "$tarball"; then
      validate_asset "$tarball" "$TAR_SIZE" "$TAR_SHA256"
      archive="$tarball"
      kind='tar'
      break
    fi
    rm -f "$tarball"
    echo "Pinned tarball endpoint failed; trying another official release URL" >&2
  done
else
  echo "zstd unavailable; trying official ZIP release with separate pinned digest"
fi

if [[ -z "$archive" ]]; then
  command -v unzip >/dev/null 2>&1 || {
    echo "ERROR: no supported extraction tool for audited Lean assets" >&2
    exit 1
  }
  zipfile="$scratch/lean-$LEAN_VERSION-linux.zip"
  for url in \
    "https://github.com/leanprover/lean4/releases/download/v$LEAN_VERSION/lean-$LEAN_VERSION-linux.zip"; do
    if download_official "$url" "$zipfile"; then
      validate_asset "$zipfile" "$ZIP_SIZE" "$ZIP_SHA256"
      archive="$zipfile"
      kind='zip'
      break
    fi
    rm -f "$zipfile"
    echo "Pinned ZIP endpoint failed" >&2
  done
fi

if [[ -z "$archive" ]]; then
  echo "ERROR: official pinned Lean release unavailable; strict CI must stay RED" >&2
  exit 1
fi

install_root="$runner_tmp/kuuos-lean-$LEAN_VERSION"
mkdir -p "$install_root"
if [[ "$kind" == tar ]]; then
  tar --zstd -xf "$archive" -C "$install_root"
else
  unzip -q "$archive" -d "$install_root"
fi

lean_executable="$(find "$install_root" -type f -path '*/bin/lean' -print -quit)"
if [[ -z "$lean_executable" ]]; then
  echo "ERROR: verified release archive has no Lean binary" >&2
  exit 1
fi
bin_dir="$(dirname "$lean_executable")"
if [[ ! -x "$bin_dir/lean" || ! -x "$bin_dir/lake" ]]; then
  echo "ERROR: verified release lacks executable Lean or Lake" >&2
  exit 1
fi

version_output="$("$bin_dir/lean" --version)"
if [[ "$version_output" != *"version $LEAN_VERSION"* ]]; then
  echo "ERROR: binary Lean version does not match exact pin: $version_output" >&2
  exit 1
fi
"$bin_dir/lake" --version
echo "$bin_dir" >> "$GITHUB_PATH"
echo "Selected verified Lean $LEAN_VERSION from $bin_dir"
git diff --exit-code -- lean-toolchain lake-manifest.json
