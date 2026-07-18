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
  + sealed structured-edit synthesis request
  + read-only path-bounded repository text snapshot
  + provider-neutral generation adapters
  + bounded synthesis and Candidate Patch policies
  -> CodeAI Autonomous Structured Edit Synthesis v0.1
  -> governed structured proposals and ranked unified diff portfolio

supported CodeAI v0.1 observation receipt
  + read-only repository text snapshot
  + one or more externally supplied structured add / modify / delete proposals
  + bounded Candidate Patch policy
  -> CodeAI Autonomous Unified Diff Candidates v0.1 ranked proposal portfolio

ranked Candidate Patch-supported portfolio
  + sealed selection request
  + bounded candidate-selection policy
  -> CodeAI Autonomous Candidate Portfolio Selection v0.1
  -> one selected independent-verification target or explicit no-selection receipt

selected independent-verification target
  + sealed selection receipt
  + canonical read-only source repository text snapshot
  + sealed isolated-application request and policy
  -> CodeAI Autonomous Isolated Candidate Application v0.1
  -> isolated verification snapshot and application receipt

supported CodeAI v0.1 observation receipt
  + externally supplied or synthesis-produced unified diff candidate
  + bounded candidate policy
  -> CodeAI Candidate Patch v0.1 proposal-only route receipt

isolated verification target/workspace
  + supported Candidate Patch v0.1 receipt
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

completed autonomous Git lifecycle receipt
  + sealed external-dependency request and observed state
  + bounded minimal external-authority policy
  -> internal substitute / unaffected work / preauthorized one-effect lease /
     minimal request packet / non-blocking hold
```

The observation frontier is read-only. Autonomous Structured Edit Synthesis
invokes bounded provider-neutral adapters and lets only governed `CANDIDATE`
output become semantic proposals. Autonomous Unified Diff Candidates renders
those proposals deterministically and produces an advisory ranking. Autonomous
Candidate Portfolio Selection consumes bounded selection authority to designate
at most one independent-verification target. Autonomous Isolated Candidate
Application checks exact selection/candidate/snapshot correspondence and applies
the selected canonical diff only to an in-memory copy, producing a verification
snapshot without touching a live repository or Git. Independent Verification
records supplied external evidence. Autonomous Git Lifecycle remains the first
CodeAI frontier that may issue active Git effect authority, one exact effect per
fresh receipt.

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
provider identity != authority
raw provider output != truth
raw provider output != structured proposal
CANDIDATE != selected candidate
HOLD / REPAIR / REJECT / QUARANTINE != structured proposal
provider call != repository mutation
structured edit proposal != unified diff candidate
unified diff generation != patch application
candidate ranking != candidate selection
rank 1 != selected patch
candidate selection != verification
selected verification target != verified patch
selected candidate != correct patch
selection authority != verification authority
selection authority != execution authority
selection receipt != verification lease
no admissible candidate != evidence deletion
selected candidate != applied live patch
isolated patch application != repository mutation
isolated snapshot != Git tree object
verification workspace ready != verification executed
materialization != verification
materialization != correctness proof
application receipt != Git or execution authority
candidate support != verification or execution lease
verification evidence != truth
passed != correctness proof
failed != rejection or rollback authority
inconclusive != evidence deletion
verification receipt != execution lease or mutation
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
source Git receipt != external authority
internal substitute != deploy authority
minimal request packet != external effect authority
secret mutation authority != secret access authority
opaque capability handle digest != secret material
external decision receipt != truth
validation != correctness proof
route receipt != successor authority
```

## Intent/Repository Observation v0.1 implementation map

- [Specification](../KUUOS_CODEAI_INTENT_REPOSITORY_OBSERVATION_ENVELOPE_v0_1.md)
- [Runtime](../../runtime/kuuos_codeai_intent_repository_observation_envelope_v0_1.py)
- [Route checker](../../scripts/check_codeai_intent_repository_observation_envelope_v0_1.py)
- [Unit test](../../tests/test_kuuos_codeai_intent_repository_observation_envelope_v0_1.py)
- [Example](../../examples/codeai_intent_repository_observation_envelope_v0_1.json)
- [Manifest](../../manifests/kuuos_codeai_intent_repository_observation_envelope_v0_1.json)
- [Formal kernel](../../formal/KUOS/CodeAI/IntentRepositoryObservationEnvelopeV0_1.lean)
- [Formal root](../../formal/KuuOSCodeAIV0_1.lean)
- [Dedicated workflow](../../.github/workflows/codeai-intent-repository-observation-envelope-v0-1.yml)

## Autonomous Structured Edit Synthesis v0.1 implementation map

- [Specification](../KUUOS_CODEAI_AUTONOMOUS_STRUCTURED_EDIT_SYNTHESIS_v0_1.md)
- [Runtime](../../runtime/kuuos_codeai_autonomous_structured_edit_synthesis_v0_1.py)
- [Route checker](../../scripts/check_codeai_autonomous_structured_edit_synthesis_v0_1.py)
- [Unit test](../../tests/test_kuuos_codeai_autonomous_structured_edit_synthesis_v0_1.py)
- [Example](../../examples/codeai_autonomous_structured_edit_synthesis_v0_1.json)
- [Manifest](../../manifests/kuuos_codeai_autonomous_structured_edit_synthesis_v0_1.json)
- [Formal kernel](../../formal/KUOS/CodeAI/AutonomousStructuredEditSynthesisV0_1.lean)
- [Formal root](../../formal/KuuOSCodeAIAutonomousStructuredEditSynthesisV0_1.lean)
- [Dedicated workflow](../../.github/workflows/codeai-autonomous-structured-edit-synthesis-v0-1.yml)

## Autonomous Unified Diff Candidates v0.1 implementation map

- [Specification](../KUUOS_CODEAI_AUTONOMOUS_UNIFIED_DIFF_CANDIDATES_v0_1.md)
- [Runtime](../../runtime/kuuos_codeai_autonomous_unified_diff_candidates_v0_1.py)
- [Route checker](../../scripts/check_codeai_autonomous_unified_diff_candidates_v0_1.py)
- [Unit test](../../tests/test_kuuos_codeai_autonomous_unified_diff_candidates_v0_1.py)
- [Example](../../examples/codeai_autonomous_unified_diff_candidates_v0_1.json)
- [Manifest](../../manifests/kuuos_codeai_autonomous_unified_diff_candidates_v0_1.json)
- [Formal kernel](../../formal/KUOS/CodeAI/AutonomousUnifiedDiffCandidatesV0_1.lean)
- [Formal root](../../formal/KuuOSCodeAIAutonomousUnifiedDiffCandidatesV0_1.lean)
- [Dedicated workflow](../../.github/workflows/codeai-autonomous-unified-diff-candidates-v0-1.yml)

## Autonomous Candidate Portfolio Selection v0.1 implementation map

- [Specification](../KUUOS_CODEAI_AUTONOMOUS_CANDIDATE_PORTFOLIO_SELECTION_v0_1.md)
- [Runtime](../../runtime/kuuos_codeai_autonomous_candidate_portfolio_selection_v0_1.py)
- [Route checker](../../scripts/check_codeai_autonomous_candidate_portfolio_selection_v0_1.py)
- [Unit test](../../tests/test_kuuos_codeai_autonomous_candidate_portfolio_selection_v0_1.py)
- [Example](../../examples/codeai_autonomous_candidate_portfolio_selection_v0_1.json)
- [Manifest](../../manifests/kuuos_codeai_autonomous_candidate_portfolio_selection_v0_1.json)
- [Formal kernel](../../formal/KUOS/CodeAI/AutonomousCandidatePortfolioSelectionV0_1.lean)
- [Formal root](../../formal/KuuOSCodeAIAutonomousCandidatePortfolioSelectionV0_1.lean)
- [Dedicated workflow](../../.github/workflows/codeai-autonomous-candidate-portfolio-selection-v0-1.yml)

## Autonomous Isolated Candidate Application v0.1 implementation map

- [Specification](../KUUOS_CODEAI_AUTONOMOUS_ISOLATED_CANDIDATE_APPLICATION_v0_1.md)
- [Runtime](../../runtime/kuuos_codeai_autonomous_isolated_candidate_application_v0_1.py)
- [Route checker](../../scripts/check_codeai_autonomous_isolated_candidate_application_v0_1.py)
- [Unit test](../../tests/test_kuuos_codeai_autonomous_isolated_candidate_application_v0_1.py)
- [Example](../../examples/codeai_autonomous_isolated_candidate_application_v0_1.json)
- [Manifest](../../manifests/kuuos_codeai_autonomous_isolated_candidate_application_v0_1.json)
- [Formal kernel](../../formal/KUOS/CodeAI/AutonomousIsolatedCandidateApplicationV0_1.lean)
- [Formal root](../../formal/KuuOSCodeAIAutonomousIsolatedCandidateApplicationV0_1.lean)
- [Dedicated workflow](../../.github/workflows/codeai-autonomous-isolated-candidate-application-v0-1.yml)

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

## Minimal External Authority Dependency v0.1 implementation map

- [Specification](../KUUOS_CODEAI_MINIMAL_EXTERNAL_AUTHORITY_DEPENDENCY_ENVELOPE_v0_1.md)
- [Runtime](../../runtime/kuuos_codeai_minimal_external_authority_dependency_envelope_v0_1.py)
- [Route checker](../../scripts/check_codeai_minimal_external_authority_dependency_envelope_v0_1.py)
- [Unit test](../../tests/test_kuuos_codeai_minimal_external_authority_dependency_envelope_v0_1.py)
- [Example](../../examples/codeai_minimal_external_authority_dependency_envelope_v0_1.json)
- [Manifest](../../manifests/kuuos_codeai_minimal_external_authority_dependency_envelope_v0_1.json)
- [Formal kernel](../../formal/KUOS/CodeAI/MinimalExternalAuthorityDependencyEnvelopeV0_1.lean)
- [Formal root](../../formal/KuuOSCodeAIMinimalExternalAuthorityDependencyV0_1.lean)
- [Dedicated workflow](../../.github/workflows/codeai-minimal-external-authority-dependency-envelope-v0-1.yml)

## Disposition surface

The profile preserves read-only/proposal-only, provider-boundary candidate/hold/
repair/reject/quarantine, bounded selection/no-selection, isolated
materialization, pass/fail, autonomous repair, degradation, abstention, handover,
and rejection as distinct modes. Isolated Candidate Application applies only to a
value-level copy, records exact source/result digests, and does not verify or
mutate the live repository. Exact readiness or a completed verification outcome
does not create next-stage authority. Autonomous Git Lifecycle may grant local
commit, push, pull request, readiness, or merge authority as separate one-effect
leases. Force push, remote branch deletion, admin bypass, deployment, secret
access, and human handover remain unavailable in that lineage.

## Conditional next stages

Possible later siblings include concrete provider SDK adapters, autonomous
verification-command execution against the isolated snapshot, evidence binding
to the application receipt, candidate repair/regeneration loops, live application
receipts, rollback, and provider-specific capability adapters. The current
application sibling owns no live mutation or verification execution. Human
handover remains deferred unless one minimal nondelegable-decision packet is
explicitly routed. Existing repository mutation, merge-gate, deployment, secret,
and capability systems remain authoritative for their own effects.
