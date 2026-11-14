#!/usr/bin/env bash
# Install/inspect official OpenAI tunnel-client: no credentials, no remote start.
set -euo pipefail
version="v0.0.20"
mode="${1:---check}"
[[ $# -le 1 && ( "$mode" == --check || "$mode" == --install ) ]] || {
  echo 'Usage: bash scripts/install_kuuos_tunnel_client_v1.sh [--install|--check]' >&2
  exit 64
}
if [[ "$mode" == --check ]]; then
  command -v tunnel-client >/dev/null || {
    echo 'NO_DATA: tunnel-client not installed' >&2; exit 69;
  }
  tunnel-client --version
  tunnel-client help quickstart >/dev/null
  echo KUUOS_TUNNEL_CLIENT_LOCAL_CLI_READY
  exit 0
fi

for c in curl sha256sum python3; do
  command -v "$c" >/dev/null || { echo "Missing command: $c" >&2; exit 69; }
done
case "$(uname -s)/$(uname -m)" in
  Linux/x86_64) platform=linux-amd64 ;;
  Linux/aarch64|Linux/arm64) platform=linux-arm64 ;;
  *) echo 'Only Linux amd64/arm64 are supported' >&2; exit 65 ;;
esac
release="https://github.com/openai/tunnel-client/releases/download/$version"
archive="tunnel-client-$version-$platform.zip"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
curl -fLsS --retry 2 --connect-timeout 15 "$release/SHA256SUMS.txt" -o "$tmp/SHA256SUMS.txt"
curl -fLsS --retry 2 --connect-timeout 15 "$release/$archive" -o "$tmp/$archive"

expected="$(awk -v n="$archive" '$2 == n || $2 == ("*" n) {print $1}' "$tmp/SHA256SUMS.txt")"
[[ "$expected" =~ ^[[:xdigit:]]{64}$ ]] || {
  echo 'Exact release SHA256SUMS entry is absent or ambiguous' >&2; exit 65;
}
actual="$(sha256sum "$tmp/$archive")"
actual="${actual%% *}"
[[ "$actual" == "$expected" ]] || {
  echo 'Official release SHA256 check failed; no installation' >&2; exit 65;
}

dir="$HOME/.local/bin"
mkdir -p "$dir"
python3 - "$tmp/$archive" "$dir/tunnel-client" <<'PY'
import os, pathlib, shutil, sys, zipfile
archive, destination = map(pathlib.Path, sys.argv[1:])
with zipfile.ZipFile(archive) as z:
    matches = [x for x in z.infolist()
               if not x.is_dir() and pathlib.PurePosixPath(x.filename).name == "tunnel-client"]
    if len(matches) != 1:
        raise SystemExit(f"expected one tunnel-client executable, found {len(matches)}")
    staging = destination.with_suffix(".install-pending")
    try:
        with z.open(matches[0]) as source, staging.open("wb") as output:
            shutil.copyfileobj(source, output)
        staging.chmod(0o700)
        os.replace(staging, destination)
    finally:
        staging.unlink(missing_ok=True)
PY
"$dir/tunnel-client" --version
"$dir/tunnel-client" help quickstart >/dev/null
echo KUUOS_TUNNEL_CLIENT_PINNED_BINARY_VERIFIED
echo 'No tunnel_id, runtime API key, ChatGPT plugin or remote connection configured.'
