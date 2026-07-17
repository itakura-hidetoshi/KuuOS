# VerifyOS repository structure

VerifyOS is maintained as a first-class KuuOS subsystem. This index connects
verification requests, evidence-bound verification, formal invariants, manifests,
checks, and CI.

## Architecture

```text
ObserveOS v0.7 sequential epistemic observability envelope
  -> VerifyOS v0.13 independent verification handoff
  -> VerifyOS independent evidence collection and verification
```

## Stable ownership boundaries

```text
observability != verification
handoff != verification completion
verification request != truth
verification request != causal confirmation
verification request != WORLD mutation
verification request != policy activation
verification request != execution
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

## Relationship to existing VerifyOS lines

VerifyOS v0.11 performs maintenance-monitoring verification intake from the
ObserveOS v0.6 receipt. VerifyOS v0.12 reviews future-only policy activation.
VerifyOS v0.13 is an additive bridge for the richer ObserveOS v0.7 envelope and
does not claim that a handoff is a completed verification.
