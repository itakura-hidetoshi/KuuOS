# CodeAI repository structure

CodeAI is an additive KuuOS application profile for governed software
evolution. It does not replace ObserveOS, PlanOS, DecisionOS, ActOS, VerifyOS,
MemoryOS, WORLD, or the repository self-organization lineage.

## Current profile frontier

```text
supplied user intent
  + supplied repository observation
  + bounded observation policy
  -> CodeAI v0.1 intent/repository observation route receipt

supported CodeAI v0.1 observation receipt
  + externally supplied unified diff candidate
  + bounded candidate policy
  -> CodeAI Candidate Patch v0.1 proposal-only route receipt

supported Candidate Patch v0.1 receipt
  + externally executed independent verification evidence
  + bounded verification policy
  -> CodeAI Independent Verification v0.1 passed / failed / inconclusive receipt
```

The observation frontier is read-only. The candidate frontier records a
proposal only. The verification frontier records supplied independent evidence.
No frontier generates, selects, applies, commits, or deploys code.

## Stable boundaries

```text
intent != authority
intent != truth
repository observation != repository truth
observation intake != live collection
observation != patch candidate
observation != selection
observation != execution lease
observation != repository mutation
candidate != selected patch
candidate != verified patch
candidate != applied patch
candidate support != verification or execution lease
verification evidence != truth
passed != correctness proof
failed != rejection or rollback authority
inconclusive != evidence deletion
verification receipt != selection, execution lease, or mutation
validation != correctness proof
route receipt != successor authority
```

## v0.1 implementation map

- [Specification](../KUUOS_CODEAI_INTENT_REPOSITORY_OBSERVATION_ENVELOPE_v0_1.md)
- [Runtime](../../runtime/kuuos_codeai_intent_repository_observation_envelope_v0_1.py)
- [Route checker](../../scripts/check_codeai_intent_repository_observation_envelope_v0_1.py)
- [Unit test](../../tests/test_kuuos_codeai_intent_repository_observation_envelope_v0_1.py)
- [Example](../../examples/codeai_intent_repository_observation_envelope_v0_1.json)
- [Manifest](../../manifests/kuuos_codeai_intent_repository_observation_envelope_v0_1.json)
- [Formal kernel](../../formal/KUOS/CodeAI/IntentRepositoryObservationEnvelopeV0_1.lean)
- [Formal root](../../formal/KuuOSCodeAIV0_1.lean)
- [Dedicated workflow](../../.github/workflows/codeai-intent-repository-observation-envelope-v0-1.yml)

## Candidate Patch v0.1 implementation map

- [Specification](../KUUOS_CODEAI_CANDIDATE_PATCH_ENVELOPE_v0_1.md)
- [Runtime](../../runtime/kuuos_codeai_candidate_patch_envelope_v0_1.py)
- [Route checker](../../scripts/check_codeai_candidate_patch_envelope_v0_1.py)
- [Unit test](../../tests/test_kuuos_codeai_candidate_patch_envelope_v0_1.py)
- [Example](../../examples/codeai_candidate_patch_envelope_v0_1.json)
- [Manifest](../../manifests/kuuos_codeai_candidate_patch_envelope_v0_1.json)
- [Formal kernel](../../formal/KUOS/CodeAI/CandidatePatchEnvelopeV0_1.lean)
- [Formal root](../../formal/KuuOSCodeAICandidatePatchV0_1.lean)
- [Dedicated workflow](../../.github/workflows/codeai-candidate-patch-envelope-v0-1.yml)

## Independent Verification v0.1 implementation map

- [Specification](../KUUOS_CODEAI_INDEPENDENT_VERIFICATION_ENVELOPE_v0_1.md)
- [Runtime](../../runtime/kuuos_codeai_independent_verification_envelope_v0_1.py)
- [Route checker](../../scripts/check_codeai_independent_verification_envelope_v0_1.py)
- [Unit test](../../tests/test_kuuos_codeai_independent_verification_envelope_v0_1.py)
- [Example](../../examples/codeai_independent_verification_envelope_v0_1.json)
- [Manifest](../../manifests/kuuos_codeai_independent_verification_envelope_v0_1.json)
- [Formal kernel](../../formal/KUOS/CodeAI/IndependentVerificationEnvelopeV0_1.lean)
- [Formal root](../../formal/KuuOSCodeAIIndependentVerificationV0_1.lean)
- [Dedicated workflow](../../.github/workflows/codeai-independent-verification-envelope-v0-1.yml)

## Disposition surface

The profile preserves read-only/proposal-only, pass/fail, hold, degradation,
abstention, handover, and rejection as distinct modes. Exact readiness or a
completed verification outcome does not create next-stage authority.

## Conditional next stages

Possible later siblings include trajectory representation, bounded execution
leases, application receipts, and Draft PR handover. Patch generation remains
external to Candidate Patch v0.1, and test execution remains external to the
verification kernel. Later names, authority sources, revocation rules, and
integration points remain unowned by the current surfaces.
