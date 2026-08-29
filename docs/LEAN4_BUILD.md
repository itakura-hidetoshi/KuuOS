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

## Fast changed-target validation

After the first setup, validate only changed Lean modules and the immediate
non-aggregate modules that import them:

```bash
bash scripts/check_changed_lean.sh --base origin/main --head HEAD
```

The changed-target path uses the repository's pinned Lean 4.31.0 and Mathlib
4.31.0, and always passes both `warningAsError=true` and `sorryAsError=true` to
Lake. It records direct targets, dependent targets, and skipped broad aggregate
roots in its receipt. A changed `lean-toolchain`, `lakefile.toml`,
`lake-manifest.json`, `KuuOSFormal`, or `KUOS` root degrades to the full
`KuuOSFormal` target because cache and aggregate compatibility are then in
scope.

To inspect the selected targets without compiling:

```bash
bash scripts/check_changed_lean.sh --base origin/main --head HEAD --plan-only
```

Changed-target success is local evidence, not a replacement for the full merge
boundary.

## Faster full rebuild after dependencies are present

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

Pull-request compilation is centralized in `.github/workflows/pr-governance-gate.yml`.
Its existing `lean-formal` surface first performs the strict changed-target and
dependent-frontier build. Draft pull requests stop there. Marking a pull request
ready for review runs the full strict `KuuOSFormal` job after the fast job, so
the full build remains a merge boundary. A manual governance run can request the
same full job with `full_lean=true` when broad validation is needed earlier.

`.github/workflows/lean-formal-validation.yml` remains available for:

- relevant pushes to `main`;
- manual `workflow_dispatch` runs.

A manual run can select any registered Lake target. Relevant pushes compile the
complete `KuuOSFormal` target.
