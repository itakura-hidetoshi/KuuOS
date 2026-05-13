# MGAP4D R1--R7 Release Evidence Map v0.1

This document defines the release-evidence map for the R1--R7 theorem-obligation surface of the MGAP4D 4D mass gap proof program.

It is an evidence-map document. It does not claim that R1--R7 are completed.

## Purpose

This map separates the following statuses:

```text
obligation slot
  != artifact present
  != CI green
  != theorem completed
  != final release
```

Each R-slot is an obligation that requires explicit evidence before it can support final release.

## Current Status

```text
spectral gap formalization: CI green
Phase 3 release gate: spectral gap formalization gate included
R1--R7 theorem completions: not claimed here
final release: not opened
public theorem boundary: held
```

## Evidence Fields Per R-Slot

Each R-slot should eventually record:

- slot_id
- obligation_name
- mathematical_statement
- normalization_conventions
- Lean or Coq artifacts
- supporting documents
- CI workflow
- CI run ID
- CI job ID
- verified commit
- proof status
- known gaps
- release boundary status
- external acceptance status

No R-slot should be promoted without explicit evidence or an explicit not-applicable note.

## R1--R7 Evidence Slots

| Slot | Current status | Required before final release |
|---|---|---|
| R1 | not claimed here | theorem statement, proof artifact, CI evidence, boundary status |
| R2 | not claimed here | theorem statement, proof artifact, CI evidence, boundary status |
| R3 | not claimed here | theorem statement, proof artifact, CI evidence, boundary status |
| R4 | not claimed here | theorem statement, proof artifact, CI evidence, boundary status |
| R5 | not claimed here | theorem statement, proof artifact, CI evidence, boundary status |
| R6 | not claimed here | theorem statement, proof artifact, CI evidence, boundary status |
| R7 | not claimed here | theorem statement, proof artifact, CI evidence, boundary status |

## Minimal Record Shape

```yaml
slot_id: R1
obligation_name: null
mathematical_statement: null
normalization_conventions:
  internal_units: null
  physical_units: null
  hamiltonian_normalization: null
lean_or_coq_artifacts: []
supporting_docs: []
ci:
  workflow: null
  run_id: null
  job_id: null
  verified_commit: null
proof_status: not_claimed_here
known_gaps: []
release_boundary_status: held
external_acceptance_status: not_claimed
```

## Promotion Rule

An R-slot may be promoted only when these are present:

```text
explicit theorem statement
normalization conventions
proof artifact path
CI evidence for exact commit
known-gap status
release boundary status
public theorem boundary decision
```

## Non-Promotion Rule

The following are not enough:

- file existence alone
- unrelated CI success
- README mention
- roadmap mention
- internal target statement alone
- numerical value alone
- KuuOS usefulness alone

## Relation to Existing Tracking Documents

The spectral gap CI ledger is:

```text
docs/spectral_gap_formalization_ci.md
```

The proof memory surface is:

```text
docs/MGAP4D_4D_MASS_GAP_PROOF_MEMORY_v0_1.md
```

The Phase 3 gate memory is:

```text
docs/MGAP4D_PHASE3_RELEASE_GATE_MEMORY_v0_1.md
```

This R1--R7 evidence map supplies the release-evidence surface that must be filled before Phase 3 final release can be opened.

## KuuOS Reading

In KuuOS terms, R1--R7 are proof-obligation membranes.

Each membrane preserves this order:

```text
formal artifact
  -> verified checkpoint
  -> theorem obligation
  -> release evidence
  -> public theorem boundary
```

A lower layer should not be mistaken for a higher layer.

## Fixed Boundary

```text
R1--R7 completion: not claimed here
R1--R7 evidence map: created
final release: not opened
public theorem boundary: held
```

## Development Rule

```text
append-only / tighten-only / overwrite-forbidden
```
