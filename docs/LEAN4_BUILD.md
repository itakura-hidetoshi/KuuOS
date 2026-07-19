# KuuOS Lean 4 build

KuuOS pins both Lean 4 and Mathlib in the repository:

- Lean toolchain: `lean-toolchain`
- Mathlib revision: `lakefile.toml`
- dependency lock: `lake-manifest.json`
- default Lake target: `KuuOSFormal`

The canonical build entrypoint is:

```bash
bash scripts/build_lean4.sh
```

This performs the following sequence:

```text
pinned Lean/Lake availability
→ lake update
→ committed lake-manifest.json consistency check
→ Mathlib olean cache retrieval
→ strict compilation of KuuOSFormal
```

Strict compilation treats Lean warnings and `sorry` as errors.

## First-time local setup

Install Git and elan. On macOS or Linux:

```bash
curl https://elan.lean-lang.org/elan-init.sh -sSf | sh
source "$HOME/.elan/env"
```

Clone and compile:

```bash
git clone https://github.com/itakura-hidetoshi/KuuOS.git
cd KuuOS
bash scripts/build_lean4.sh
```

The first build downloads the pinned Lean toolchain, Mathlib sources, and the
compatible Mathlib compiled cache. Later builds reuse `.lake`.

## Compile one target

```bash
bash scripts/build_lean4.sh KuuOSCodeAIV0_1
bash scripts/build_lean4.sh KUOS
```

Equivalent explicit form:

```bash
bash scripts/build_lean4.sh --target KuuOSFormal
```

## Faster rebuild after dependencies are present

```bash
bash scripts/build_lean4.sh --no-update --no-cache KuuOSFormal
```

## Non-strict exploratory build

```bash
bash scripts/build_lean4.sh --non-strict KuuOSFormal
```

CI and merge validation remain strict even when a local exploratory build is
non-strict.

## Clean rebuild

```bash
bash scripts/build_lean4.sh --clean KuuOSFormal
```

## Direct Lake commands

The wrapper corresponds to:

```bash
lake update
git diff --exit-code -- lake-manifest.json
lake exe cache get
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSFormal
```

## GitHub Actions

`.github/workflows/lean-formal-validation.yml` runs on:

- relevant pull requests;
- relevant pushes to `main`;
- manual `workflow_dispatch` runs.

A manual run can select a registered Lake target. Pull requests and pushes
compile the complete `KuuOSFormal` target.
