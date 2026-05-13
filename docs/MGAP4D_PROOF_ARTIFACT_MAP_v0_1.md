# MGAP4D Proof Artifact Map v0.1

This document defines the proof-artifact map for the MGAP4D 4D mass gap proof program as tracked from the KuuOS public core.

It is an artifact-map document. It does not claim final theorem completion by itself.

## Purpose

The proof-artifact map connects theorem obligations to checkable artifacts, supporting documents, CI evidence, and release records.

It keeps the following statuses separate:

```text
artifact path listed
  != artifact verified
  != R-slot completed
  != final release
  != public theorem boundary opened
```

## Current Boundary Status

```text
spectral gap formalization: CI green
Phase 3 release gate: spectral gap formalization gate included
R1--R7 release-evidence map: created
final theorem boundary decision record: created
R1--R7 theorem completions: not claimed here
final release: not opened
public theorem boundary: held
```

## Artifact Map Fields

Each proof artifact entry should record:

- artifact_id
- artifact_path
- artifact_type
- theorem_or_obligation
- linked_R_slot
- role_in_proof
- dependencies
- normalization_relevance
- CI workflow
- CI run ID
- CI job ID
- verified commit
- verification status
- known gaps
- release relevance
- external record

## Current Known Artifact Surfaces

The inherited spectral gap formalization chain is tracked as:

| Artifact path | Type | Current role | Status |
|---|---|---|---|
| MGAP4D/Spectral.lean | Lean surface | spectral module entrypoint | inherited checkpoint |
| MGAP4D/Spectral/GapFormalization.lean | Lean surface | spectral gap formalization checkpoint | CI green in inherited record |
| MGAP4D/SpectralGapFormalizationGate.lean | Lean surface | Phase 3 global gate surface | gate included |
| MGAP4D/Phase3ReleaseGate.lean | Lean surface | Phase 3 release gate | includes spectral gap formalization gate |

These entries record the known formal surfaces. They do not by themselves open final release.

## Current CI Evidence Link

The inherited CI-green evidence is recorded in:

```text
docs/spectral_gap_formalization_ci.md
```

Known CI data:

```text
Workflow: Lean Direct Elan CI
Run ID: 25828960043
Build job ID: 75889136130
Verified commit: df99969343482d3030f6b6006edb082030dd1e87
Result: success
```

## R1--R7 Link

The R1--R7 release-evidence map is recorded in:

```text
docs/MGAP4D_R1_R7_RELEASE_EVIDENCE_MAP_v0_1.md
```

Each proof artifact should eventually be linked to one or more R-slots, or explicitly marked as supporting but not completing an R-slot.

Current status:

```text
R1--R7 artifact completion mapping: not filled here
R1--R7 theorem completions: not claimed here
```

## Minimal Artifact Record Shape

```yaml
artifact_id: null
artifact_path: null
artifact_type: lean_or_coq_or_doc_or_ci_or_release
linked_R_slots: []
theorem_or_obligation: null
role_in_proof: null
dependencies: []
normalization_relevance: null
ci:
  workflow: null
  run_id: null
  job_id: null
  verified_commit: null
verification_status: not_claimed_here
known_gaps: []
release_relevance: checkpoint_only
external_record: null
```

## Promotion Rule

An artifact may support release evidence only when:

```text
artifact path is fixed
and artifact type is known
and theorem or obligation link is explicit
and CI evidence exists for the exact commit
and known gaps are stated
and release relevance is stated
```

## Non-Promotion Rule

The following are not enough:

- path listed without verification
- local build claim without commit identity
- CI success for unrelated artifact
- documentation mention alone
- internal target statement alone
- downstream KuuOS interpretation alone

## Relation to Final Boundary Decision

The final theorem boundary decision record is:

```text
docs/MGAP4D_FINAL_THEOREM_BOUNDARY_DECISION_RECORD_v0_1.md
```

That record requires a proof artifact map before the public theorem boundary can be opened. This document supplies the map surface, but it does not fill every release artifact by itself.

## KuuOS Reading

In KuuOS terms, proof artifacts are record surfaces.

They mediate between formal proof work and public theorem claims:

```text
formal artifact
  -> verified checkpoint
  -> R-slot evidence
  -> release packet
  -> public theorem boundary
```

A proof artifact is therefore not merely a file. It is a governed record surface with a specific role in the proof membrane.

## Fixed Boundary

```text
proof artifact map: created
R1--R7 artifact completion mapping: not filled here
final release: not opened
public theorem boundary: held
```

## Development Rule

```text
append-only / tighten-only / overwrite-forbidden
```
