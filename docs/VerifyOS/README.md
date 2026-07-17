# VerifyOS repository structure

VerifyOS is maintained as a first-class KuuOS subsystem. This index connects
verification requests, independent evidence verification, formal invariants,
manifests, checks, and CI.

## Architecture

```text
ObserveOS v0.7 sequential epistemic observability envelope
  -> VerifyOS v0.13 independent verification handoff
  -> VerifyOS v0.14 independent evidence verification
  -> passed / failed / indeterminate verification receipt
```

## Stable ownership boundaries

```text
observability != verification
handoff != verification completion
verification != truth
verification outcome != causal attribution
passed != WORLD adoption
failed != WORLD rejection
indeterminate != evidence deletion
verification receipt != WORLD mutation
verification receipt != policy activation
verification receipt != execution authority
```

## v0.13 implementation map

- Specification:
  [`../KUUOS_VERIFYOS_SEQUENTIAL_EPISTEMIC_OBSERVATION_VERIFICATION_HANDOFF_v0_1.md`](../KUUOS_VERIFYOS_SEQUENTIAL_EPISTEMIC_OBSERVATION_VERIFICATION_HANDOFF_v0_1.md)
- Runtime:
  [`../../runtime/kuuos_verifyos_sequential_epistemic_observation_verification_handoff_v0_1.py`](../../runtime/kuuos_verifyos_sequential_epistemic_observation_verification_handoff_v0_1.py)
- Formal kernel:
  [`../../formal/KUOS/VerifyOS/SequentialEpistemicObservationVerificationHandoffV0_13.lean`](../../formal/KUOS/VerifyOS/SequentialEpistemicObservationVerificationHandoffV0_13.lean)
- Formal root:
  [`../../formal/KuuOSVerifyOSV0_13.lean`](../../formal/KuuOSVerifyOSV0_13.lean)
- Manifest:
  [`../../manifests/kuuos_verifyos_sequential_epistemic_observation_verification_handoff_v0_1.json`](../../manifests/kuuos_verifyos_sequential_epistemic_observation_verification_handoff_v0_1.json)
- Route checker:
  [`../../scripts/check_verifyos_sequential_epistemic_observation_verification_handoff_v0_1.py`](../../scripts/check_verifyos_sequential_epistemic_observation_verification_handoff_v0_1.py)
- GitHub Actions:
  [`../../.github/workflows/verifyos-sequential-epistemic-observation-verification-handoff-v0-1.yml`](../../.github/workflows/verifyos-sequential-epistemic-observation-verification-handoff-v0-1.yml)

## v0.14 implementation map

- Specification:
  [`../KUUOS_VERIFYOS_INDEPENDENT_EVIDENCE_VERIFICATION_v0_1.md`](../KUUOS_VERIFYOS_INDEPENDENT_EVIDENCE_VERIFICATION_v0_1.md)
- Runtime:
  [`../../runtime/kuuos_verifyos_independent_evidence_verification_v0_1.py`](../../runtime/kuuos_verifyos_independent_evidence_verification_v0_1.py)
- Formal kernel:
  [`../../formal/KUOS/VerifyOS/IndependentEvidenceVerificationV0_14.lean`](../../formal/KUOS/VerifyOS/IndependentEvidenceVerificationV0_14.lean)
- Formal root:
  [`../../formal/KuuOSVerifyOSV0_14.lean`](../../formal/KuuOSVerifyOSV0_14.lean)
- Manifest:
  [`../../manifests/kuuos_verifyos_independent_evidence_verification_v0_1.json`](../../manifests/kuuos_verifyos_independent_evidence_verification_v0_1.json)
- Route checker:
  [`../../scripts/check_verifyos_independent_evidence_verification_v0_1.py`](../../scripts/check_verifyos_independent_evidence_verification_v0_1.py)
- GitHub Actions:
  [`../../.github/workflows/verifyos-independent-evidence-verification-v0-1.yml`](../../.github/workflows/verifyos-independent-evidence-verification-v0-1.yml)

## Outcome semantics

```text
passed        -> verification completed, debt closed
failed        -> verification completed, debt closed
indeterminate -> verification completed, debt open, reobservation required
```

All outcome receipts preserve WORLD revision and lineage. None generates a WORLD
adoption or rejection candidate, policy activation, learning activation, tool
invocation, or execution authority.

## Relationship to existing VerifyOS lines

VerifyOS v0.11 performs maintenance-monitoring verification intake from the
ObserveOS v0.6 receipt. VerifyOS v0.12 reviews future-only policy activation.
VerifyOS v0.13 is an additive bridge for the richer ObserveOS v0.7 envelope.
VerifyOS v0.14 consumes only a supported v0.13 handoff and records an independent
evidence-verification outcome without treating that outcome as truth, causality,
WORLD mutation, or execution authority.
