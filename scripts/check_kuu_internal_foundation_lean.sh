#!/usr/bin/env bash
# Compile internal Kuu modules explicitly with the pinned Lean toolchain.
#
# They are intentionally NOT additional public Lake roots. 'lake lean <file>'
# elaborates a source in the project context, and '-o' writes its importable
# .olean so the next internal file can import it on a clean checkout.
set -euo pipefail

mkdir -p .lake/build/lib/lean/Kuu

for name in Presentation Strict Incidence Checks; do
  lake lean "formal/Kuu/${name}.lean" -- \
    -DwarningAsError=true -DsorryAsError=true \
    -o ".lake/build/lib/lean/Kuu/${name}.olean"
done

lake lean formal/KuuOSStrict.lean -- \
  -DwarningAsError=true -DsorryAsError=true \
  -o .lake/build/lib/lean/KuuOSStrict.olean

git diff --exit-code -- lake-manifest.json lean-toolchain lakefile.toml
