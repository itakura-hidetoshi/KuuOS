# KuuOS Lean-LSP MCP Compatibility Probe v7.17

## Purpose

v7.16 registered `oOo0oOo/lean-lsp-mcp` as `experimental_high_value`.

v7.17 performs the missing empirical check against the exact KuuOS toolchain:

```text
Lean v4.30.0-rc2
mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6
```

The goal is not to run another full Strict Lean build.

The goal is to verify that the MCP server can actually:

```text
start
-> initialize MCP
-> expose the expected Lean tools
-> start/use lake serve in the KuuOS project
-> read a real KuuOS Lean file
-> obtain outline and diagnostic information
```

under the pinned project environment.

## Upstream pin

The compatibility target is:

```text
repository: oOo0oOo/lean-lsp-mcp
upstream main SHA: bb176c58a4f895061561685318e92b8db446f1b5
package: lean-lsp-mcp 0.30.0
```

The package declares:

```text
Python >= 3.10
leanclient >= 0.13.2
mcp[cli] == 2.0.0
```

The server documentation states that it runs `lake serve` in the active project root, so the project `lean-toolchain` controls Lean rather than a global Lean installation.

## Representative KuuOS file

The live probe uses:

```text
formal/KUOS/DependentOriginationFunctorialTransportV0_1.lean
```

This is an existing KuuOS theorem artifact that imports `Mathlib` directly and does not import another KuuOS module.

That makes it a good compatibility witness:

- it is genuinely inside KuuOS;
- it exercises the pinned Mathlib environment;
- it avoids building the full dependent-origination module graph merely to test MCP compatibility.

## Probe stages

### Pin verification

The checker requires exact:

```text
lean-toolchain = leanprover/lean4:v4.30.0-rc2
mathlib rev    = 5450b53e5ddc75d46418fabb605edbf36bd0beb6
```

### Representative compile

CI compiles only the representative existing file with the pinned toolchain.

This is not a replacement for Strict Lean and is not a full repository revalidation.

### MCP package version

The probe starts exactly:

```text
lean-lsp-mcp == 0.30.0
```

rather than an unpinned latest package.

### MCP lifecycle

The checker performs:

```text
initialize
notifications/initialized
tools/list
```

and checks the read/analysis tools required by KuuOS.

### Real LSP calls

The checker then calls:

```text
lean_file_outline
lean_diagnostic_messages(severity=error)
```

on the real representative KuuOS file.

A successful JSON-RPC response is required for both.

## Probe effect boundary

The compatibility probe deliberately disables tools that can execute snippets, rebuild the project, rewrite temporary theorem context, or use external theorem-search services.

Disabled during the probe:

```text
lean_run_code
lean_build
lean_profile_proof
lean_minimal_hypotheses
lean_multi_attempt
lean_leansearch
lean_loogle
lean_leanfinder
lean_state_search
lean_hammer_premise
```

This does not remove those capabilities from the development registry.

It only makes the compatibility test itself narrow and reproducible.

## Promotion

The initial exact-head live probe succeeded at:

```text
head: a5f16cbcafd3f698051a0afa51b7c8df5f2a2c9e
run:  36328215047
```

That run passed the representative compile, MCP initialize/tools-list, `lean_file_outline`, and `lean_diagnostic_messages` calls.

The v7.16 registry is therefore promoted in this PR:

```text
lean_lsp:
  experimental_high_value
->
  verified_compatible
```

The promoted final head must run the same live probe again before merge.

That status means:

> this exact lean-lsp-mcp package version has demonstrated interoperability with the pinned KuuOS project environment.

It does not mean:

- lean-lsp-mcp becomes theorem authority;
- diagnostics replace Strict Lean;
- external Lean search results become KuuOS authority;
- write authority is granted;
- future lean-lsp-mcp releases are automatically compatible.

## Expected development benefit

After promotion, the preferred KuuOS Lean workflow becomes:

```text
edit
-> Lean-LSP MCP diagnostics / goal / hover / local search
-> repair
-> focused local/pull-request validation
-> exact-head CI
-> merge
```

rather than relying primarily on:

```text
edit
-> push
-> wait for CI RED
-> inspect Lean error
-> repair
```

The final CI receipt remains authoritative for the repository head.
