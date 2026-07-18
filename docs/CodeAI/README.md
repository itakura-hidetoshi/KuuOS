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

supported Independent Verification v0.1 receipt
  + sealed autonomous trajectory request
  + bounded trajectory policy
  -> CodeAI Autonomous Trajectory Synthesis v0.1 internal next-step candidate

supported passed trajectory receipt
  + sealed Git lifecycle request and observed state
  + bounded autonomous Git lifecycle policy
  -> one-effect commit / push / PR / readiness / merge lease
```

The observation frontier is read-only. The candidate frontier records a
proposal only. The verification frontier records supplied independent evidence.
The trajectory frontier synthesizes a read-only representation and an internal
deliberation, repair, or reverification candidate. No frontier selects, applies,
commits, or deploys code. Trajectory synthesis does not generate a patch or
execute verification. Autonomous Git Lifecycle is the first CodeAI frontier
that may issue active effect authority. It grants at most one exact next effect
per receipt and requires fresh observed state before advancing.

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
trajectory != truth or full intent lineage
internal deliberation candidate != candidate selection
internal repair candidate != generated or applied patch
internal reverification candidate != executed verification
handover deferred != handover performed
trajectory receipt != Git authority
commit authority != push authority
push authority != pull-request authority
pull-request creation != merge authority
required checks success != correctness proof
merge != truth
remote Git effect != human handover
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

## Autonomous Trajectory Synthesis v0.1 implementation map

- [Specification](../KUUOS_CODEAI_AUTONOMOUS_TRAJECTORY_SYNTHESIS_ENVELOPE_v0_1.md)
- [Runtime](../../runtime/kuuos_codeai_autonomous_trajectory_synthesis_envelope_v0_1.py)
- [Route checker](../../scripts/check_codeai_autonomous_trajectory_synthesis_envelope_v0_1.py)
- [Unit test](../../tests/test_kuuos_codeai_autonomous_trajectory_synthesis_envelope_v0_1.py)
- [Example](../../examples/codeai_autonomous_trajectory_synthesis_envelope_v0_1.json)
- [Manifest](../../manifests/kuuos_codeai_autonomous_trajectory_synthesis_envelope_v0_1.json)
- [Formal kernel](../../formal/KUOS/CodeAI/AutonomousTrajectorySynthesisEnvelopeV0_1.lean)
- [Formal root](../../formal/KuuOSCodeAIAutonomousTrajectorySynthesisV0_1.lean)
- [Dedicated workflow](../../.github/workflows/codeai-autonomous-trajectory-synthesis-envelope-v0-1.yml)

## Autonomous Git Lifecycle v0.1 implementation map

- [Specification](../KUUOS_CODEAI_AUTONOMOUS_GIT_LIFECYCLE_ENVELOPE_v0_1.md)
- [Runtime](../../runtime/kuuos_codeai_autonomous_git_lifecycle_envelope_v0_1.py)
- [Route checker](../../scripts/check_codeai_autonomous_git_lifecycle_envelope_v0_1.py)
- [Unit test](../../tests/test_kuuos_codeai_autonomous_git_lifecycle_envelope_v0_1.py)
- [Example](../../examples/codeai_autonomous_git_lifecycle_envelope_v0_1.json)
- [Manifest](../../manifests/kuuos_codeai_autonomous_git_lifecycle_envelope_v0_1.json)
- [Formal kernel](../../formal/KUOS/CodeAI/AutonomousGitLifecycleEnvelopeV0_1.lean)
- [Formal root](../../formal/KuuOSCodeAIAutonomousGitLifecycleV0_1.lean)
- [Dedicated workflow](../../.github/workflows/codeai-autonomous-git-lifecycle-envelope-v0-1.yml)

## Disposition surface

The profile preserves read-only/proposal-only, pass/fail, autonomous read-only,
autonomous repair, hold, degradation, abstention, handover, and rejection as
distinct modes. Exact readiness or a completed verification outcome does not
create next-stage authority. Autonomous Trajectory Synthesis v0.1 never performs
human or external-authority handover; it records such a request as deferred
hold. Autonomous Git Lifecycle v0.1 may grant local commit, push, pull request,
readiness, or merge authority as separate one-effect leases. Force push, remote
branch deletion, admin bypass, deployment, secret access, and human handover
remain unavailable.

## Conditional next stages

Possible later siblings include richer trajectory continuation, patch
generation, application receipts, rollback, and deployment. Patch generation
remains external to Candidate Patch v0.1, test execution remains external to the
verification kernel, and human or external-authority handover remains deferred.
The Git lifecycle composes with, rather than replaces, the existing repository
live-mutation lineage and Qi PR Merge Gate. Later authority sources, revocation
rules, and deployment integration points remain unowned.
