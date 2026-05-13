# MGAP4D Final Theorem Boundary Decision Record v0.1

This document defines the decision record required before the MGAP4D 4D mass gap proof program may open a final public theorem boundary.

It is a boundary-decision document. It does not open the boundary by itself.

## Purpose

The purpose of this document is to keep the following statuses separate:

```text
CI green
  != R-slot evidence filled
  != artifact map created
  != normalization record created
  != theorem completion
  != final release
  != public theorem boundary opened
```

A public theorem boundary is a separate decision surface. It must not be inferred automatically from CI success, documentation, roadmap status, artifact-map creation, normalization-record creation, or internal target statements.

## Current Boundary Status

```text
spectral gap formalization: CI green
Phase 3 release gate: spectral gap formalization gate included
R1--R7 release-evidence map: created
proof artifact map: created
normalization convention record: created
physical-unit interpretation of 33/20: not opened here
R1--R7 theorem completions: not claimed here
final release: not opened
public theorem boundary: held
```

## Required Inputs Before Boundary Opening

Before the public theorem boundary can be opened, the following inputs should exist:

1. final theorem statement
2. normalization convention record filled for final release
3. R1--R7 evidence map filled or explicitly remapped
4. proof artifact map filled with release-relevant artifact links
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
normalization_record: docs/MGAP4D_NORMALIZATION_CONVENTION_RECORD_v0_1.md
normalization_record_status: created_internal_units_only
r1_r7_evidence_status: not_completed_here
proof_artifact_map: docs/MGAP4D_PROOF_ARTIFACT_MAP_v0_1.md
proof_artifact_map_status: created_not_filled_for_final_release
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
- normalization convention record is missing or internal-units-only
- physical-unit interpretation is asserted without a separate record
- proof artifact map is missing or not filled for final release
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
docs/MGAP4D_PROOF_ARTIFACT_MAP_v0_1.md
docs/MGAP4D_NORMALIZATION_CONVENTION_RECORD_v0_1.md
```

These documents provide evidence, artifact mapping, normalization surface, and gate memory. They do not themselves open the final public theorem boundary.

## KuuOS Reading

In KuuOS terms, the final theorem boundary is a high-level governance membrane.

It separates:

```text
machine-checked checkpoint
  -> proof artifact map
  -> normalization convention
  -> proof-obligation evidence
  -> release readiness
  -> public theorem claim
```

The membrane prevents early identification of partial verification, artifact listing, or internal normalized values with final theorem authority.

## Fixed Boundary

Current fixed boundary:

```text
final theorem boundary decision record: created
proof artifact map: created
normalization convention record: created
physical-unit interpretation of 33/20: not opened here
public theorem boundary: held
final release: not opened
R1--R7 theorem completions: not claimed here
```

## Development Rule

```text
append-only / tighten-only / overwrite-forbidden
```
