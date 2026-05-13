# KuuOS / MGAP4D Roadmap

This roadmap records the current public-core alignment between KuuOS and the MGAP4D 4D mass gap proof program.

## Repository Relationship

The canonical Lean proof repository for the 4D mass gap proof architecture is:

```text
https://github.com/itakura-hidetoshi/4d-mass-gap
```

KuuOS references that repository as a physics-facing bridge and public-core governance surface.

```text
Canonical proof repo: itakura-hidetoshi/4d-mass-gap
KuuOS reference repo: itakura-hidetoshi/KuuOS
KuuOS reference document: docs/MGAP4D_CANONICAL_PROOF_REPO_REFERENCE_v0_1.md
4d-mass-gap bridge document: docs/kuuos_reference_bridge.md
```

KuuOS reference documents do not replace `itakura-hidetoshi/4d-mass-gap` as the canonical Lean proof source and do not independently open final theorem release.

## Current Checkpoint

The spectral gap formalization surface is CI green in the canonical proof repository under the inherited Lean Direct Elan CI record.

- Canonical proof repo: itakura-hidetoshi/4d-mass-gap
- Workflow: Lean Direct Elan CI
- Run ID: 25828960043
- Build job ID: 75889136130
- Verified commit: df99969343482d3030f6b6006edb082030dd1e87
- Ledger commit: acde03b389fabc7dec3c240a732f599d95fb1f42
- Local KuuOS reference ledger file: docs/spectral_gap_formalization_ci.md

## Formal Surfaces

The active MGAP4D spectral gap formalization chain is tracked through the following canonical proof repository surfaces:

```text
MGAP4D/Spectral.lean
MGAP4D/Spectral/GapFormalization.lean
MGAP4D/SpectralGapFormalizationGate.lean
MGAP4D/Phase3ReleaseGate.lean
```

Their current role is checkpoint/gate formalization, not final public theorem release.

## KuuOS Tracking Documents

The KuuOS public-core tracking documents are:

```text
docs/MGAP4D_CANONICAL_PROOF_REPO_REFERENCE_v0_1.md
docs/spectral_gap_formalization_ci.md
docs/MGAP4D_4D_MASS_GAP_PROOF_MEMORY_v0_1.md
docs/MGAP4D_PHASE3_RELEASE_GATE_MEMORY_v0_1.md
docs/MGAP4D_R1_R7_RELEASE_EVIDENCE_MAP_v0_1.md
docs/MGAP4D_PROOF_ARTIFACT_MAP_v0_1.md
docs/MGAP4D_NORMALIZATION_CONVENTION_RECORD_v0_1.md
docs/MGAP4D_FINAL_THEOREM_BOUNDARY_DECISION_RECORD_v0_1.md
```

These documents separate canonical proof-source reference, CI evidence, proof-memory content, Phase 3 release-gate semantics, R1--R7 release-evidence slots, proof-artifact mapping, normalization conventions, and the final public theorem boundary decision.

## Boundary Held

The following claims remain intentionally unopened:

- final release
- R1--R7 theorem completions
- Mathlib-on-main migration
- physical-unit interpretation of `33/20`
- public theorem boundary

This keeps the KuuOS repository aligned with the canonical proof repository while preserving proof-carrying development rather than premature theorem reification.

## Next Steps

1. Keep KuuOS README and roadmap synchronized with the canonical `4d-mass-gap` proof repository.
2. Keep the KuuOS reference documents append-only.
3. Maintain the pre-Mathlib main branch boundary of the canonical proof repository until a separate Mathlib migration path is explicitly opened there.
4. Separate checkpoint success from final theorem authority.
5. Use `docs/MGAP4D_CANONICAL_PROOF_REPO_REFERENCE_v0_1.md` as the KuuOS-side canonical repository reference surface.
6. Use `docs/MGAP4D_PHASE3_RELEASE_GATE_MEMORY_v0_1.md` as the Phase 3 gate-memory surface.
7. Use `docs/MGAP4D_R1_R7_RELEASE_EVIDENCE_MAP_v0_1.md` as the R1--R7 evidence-slot surface.
8. Use `docs/MGAP4D_PROOF_ARTIFACT_MAP_v0_1.md` as the proof-artifact mapping surface.
9. Use `docs/MGAP4D_NORMALIZATION_CONVENTION_RECORD_v0_1.md` as the normalization-convention surface.
10. Use `docs/MGAP4D_FINAL_THEOREM_BOUNDARY_DECISION_RECORD_v0_1.md` as the public theorem boundary decision surface.
11. Prepare later Phase 3 final-release documentation only after the relevant theorem surfaces are explicitly completed and verified in the canonical proof repository.

## KuuOS Interpretation

For KuuOS, the 4D mass gap bridge is read as a physics-facing expression of the Two Truths Gap:

```text
vacuum / ground phase
  -> nonzero spectral gap
  -> effective excitations
  -> observable record surfaces
  -> conventional-world operation
```

The gap prevents collapse between latent ground structure and effective-world excitations. In KuuOS language, this supports the distinction between emptiness, dependent origination, and conventional manifestation without treating emptiness as nihilism or treating excitations as self-subsisting entities.

The repository relation itself follows the same non-collapse principle:

```text
canonical Lean proof repository
  != KuuOS governance/reference repository
```

The Phase 3 release gate is therefore read as a proof-governance expression of the same non-collapse principle:

```text
CI-green checkpoint
  != theorem completion
  != final public theorem release
```

The R1--R7 evidence map extends this rule to each theorem-obligation slot:

```text
obligation slot
  != artifact present
  != CI green
  != theorem completed
  != final release
```

The proof artifact map adds the record-surface layer:

```text
artifact path listed
  != artifact verified
  != R-slot completed
  != final release
```

The normalization convention record adds the unit/meaning membrane:

```text
internal normalized target
  != physical-unit interpretation
  != final theorem statement
```

The final theorem boundary decision record adds the last membrane:

```text
release readiness
  != public theorem boundary opened
```

## Development Rule

The roadmap follows the same governance rule as the public KuuOS core:

```text
append-only / tighten-only / overwrite-forbidden
```
