#!/usr/bin/env bash
# Compile only the independent Kuu import subgraph, using the pinned Lake
# dependency graph instead of manually building .olean files.
#
# This is an incremental compilation target, not a new public theorem root.
# The library's leanOptions already enables warningAsError=true. Lean v4.30.0-rc2
# does NOT have a -DsorryAsError option. The foundation boundary checker and
# theorem #print axioms audit enforce the no-sorry/no-new-axiom policy.
set -euo pipefail

# This internal module is buildable through lakefile globs, not a public root.
lake build +KuuOSStrict:olean

git diff --exit-code -- lake-manifest.json lean-toolchain lakefile.toml
