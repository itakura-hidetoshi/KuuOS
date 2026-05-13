# MGAP4D Final Theorem Boundary Decision Record v0.1

This document defines the decision record required before the MGAP4D 4D mass gap proof program may open a final public theorem boundary.

It is a boundary-decision document. It does not open the boundary by itself.

## Purpose

The purpose of this document is to keep the following statuses separate:

```text
CI green
  != R-slot evidence filled
  != theorem completion
  != final release
  != public theorem boundary opened
```

A public theorem boundary is a separate decision surface. It must not be inferred automatically from CI success, documentation, roadmap status, or internal target statements.

## Current Boundary Status

```text
spectral gap formalization: CI green
Phase 3 release gate: spectral gap formalization gate included
R1--R7 release-evidence map: created
R1--R7 theorem completions: not claimed here
final release: not opened
public theorem boundary: held
```

## Required Inputs Before Boundary Opening

Before the public theorem boundary can be opened, the following inputs should exist:

1. final theorem statement
2. normalization convention record
3. R1--R7 evidence map filled or explicitly remapped
4. proof artifact map
5. exact release commit
6. CI evidence for the exact release commit
7. known-gap closure or known-gap boundary statement
8. release packet
9. external-audit status statement
10. boundary decision entry

## Boundary Decision Fields

A future decision entry should include:

```yaml
decision_id: null
decision_date: null
decision_status: held
final_theorem_statement: null
normalization_record: null
r1_r7_evidence_status: not_completed_here
proof_artifact_map: null
release_commit: null
ci_evidence: null
known_gap_status: null
release_packet: null
external_audit_status: not_claimed
boundary_opened: false
boundary_reason: null
```

## Allowed Decision Status

Allowed decision statuses:

```text
held
review_ready
audit_ready
release_ready
opened
reverted
```

Current status is:

```text
held
```

## Opening Rule

The boundary may be opened only when the decision record explicitly states:

```text
boundary_opened: true
```

and all required inputs are present or explicitly justified.

## Non-Opening Rule

The boundary remains held when any of the following is true:

- R1--R7 evidence slots are unfilled
- final theorem statement is missing
- normalization convention record is missing
- proof artifact map is missing
- exact release commit is missing
- exact CI evidence is missing
- known gaps are unresolved without boundary statement
- release packet is absent
- external-audit status is unclear
- boundary decision entry is absent

## Relation to Existing Documents

This boundary decision record depends on, but is not replaced by, the following documents:

```text
docs/spectral_gap_formalization_ci.md
docs/MGAP4D_4D_MASS_GAP_PROOF_MEMORY_v0_1.md
docs/MGAP4D_PHASE3_RELEASE_GATE_MEMORY_v0_1.md
docs/MGAP4D_R1_R7_RELEASE_EVIDENCE_MAP_v0_1.md
```

These documents provide evidence and gate memory. They do not themselves open the final public theorem boundary.

## KuuOS Reading

In KuuOS terms, the final theorem boundary is a high-level governance membrane.

It separates:

```text
machine-checked checkpoint
  -> proof-obligation evidence
  -> release readiness
  -> public theorem claim
```

The membrane prevents early identification of partial verification with final theorem authority.

## Fixed Boundary

Current fixed boundary:

```text
final theorem boundary decision record: created
public theorem boundary: held
final release: not opened
R1--R7 theorem completions: not claimed here
```

## Development Rule

```text
append-only / tighten-only / overwrite-forbidden
```
