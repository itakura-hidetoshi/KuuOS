# KuuOS CodeAI Autonomous Trajectory Synthesis Envelope v0.1

Status: additive sibling profile

Version: v0.1

Predecessor: CodeAI Independent Verification Envelope v0.1

## 1. Purpose

This surface turns a sealed, completed CodeAI Independent Verification receipt
into a deterministic, read-only trajectory representation and one internal next
step candidate. It increases bounded autonomy without acquiring execution or
external authority.

The outcome mapping is:

```text
passed       -> internal deliberation candidate
failed       -> internal repair candidate
inconclusive -> internal reverification candidate
```

An internal candidate is a future-only reasoning artifact. It is not candidate
selection, patch generation, test execution, patch application, repository
mutation, or permission to contact a person or external authority.

## 2. Additive boundary

This specification is a sibling of the existing CodeAI surfaces. It does not
modify their schemas, route orders, examples, or formal roots. It does not
replace ObserveOS, PlanOS, DecisionOS, ActOS, VerifyOS, MemoryOS, WORLD, or the
repository evolution lineage.

The kernel owns:

- exact intake of a supported Independent Verification v0.1 receipt;
- request and policy provenance validation;
- receipt, candidate, patch, repository, and commit correspondence;
- request window and replay routing;
- a two-node trajectory over the receipts available to this surface;
- deterministic passed, failed, and inconclusive next-step mapping;
- deferral of human or external-authority handover.

The kernel does not own:

- reconstruction of an unavailable full intent or observation history;
- generalized truth or correctness proof;
- candidate ranking or selection;
- patch generation, editing, application, or rollback;
- tool or test execution;
- execution lease issuance;
- working-tree, index, object-database, or Git-ref mutation;
- branch, commit, push, pull request, merge, release, or deployment;
- human notification or external-authority handover;
- secret access.

## 3. Preserved invariants

```text
verification receipt != successor authority
trajectory != truth
trajectory completeness over available receipts != full lineage reconstruction
internal deliberation candidate != candidate selection
internal repair candidate != patch generation or application
internal reverification candidate != test execution
handover request != handover permission
handover deferred != handover performed
autonomous synthesis != repository mutation
```

Every emitted receipt preserves the source commit and records:

- `history_read_only = true`;
- `future_only = true`;
- `active_now = false`;
- every effect field as `false`;
- every successor-authority grant as `false`;
- `human_handover_performed = false`;
- `external_authority_handover_performed = false`.

## 4. Inputs

### 4.1 `source_verification_receipt`

The source must be an exact, digest-valid CodeAI Independent Verification v0.1
receipt representing one completed supported outcome:

- `independent_verification_passed / verified_pass / passed`;
- `independent_verification_failed / verified_fail / failed`;
- `verification_inconclusive_hold / hold / inconclusive`; or
- `verification_inconclusive_degraded / degraded_verification / inconclusive`.

The source must remain read-only and must grant no selection, verification,
execution, merge, deployment, or secret authority. A repair, abstain, handover,
or rejected predecessor receipt cannot be promoted by this surface.

### 4.2 `trajectory_request`

The sealed request binds:

- trajectory, revision, session, and nonce provenance;
- source verification and candidate receipt digests;
- candidate patch and patch artifact digests;
- repository and source commit;
- trajectory format and requested step count;
- the two available lineage nodes;
- autonomous synthesis intent;
- effect requests and authority claims as explicit booleans;
- prior sessions, nonces, and trajectory receipt digests;
- request creation epoch and correspondence confirmations.

The v0.1 successful path requires exactly two nodes:

1. a candidate-lineage anchor; and
2. the independent-verification receipt.

### 4.3 `trajectory_policy`

The sealed policy binds expected source identities, allowed formats and
verification outcomes, maximum step count, next-step permissions, a bounded
evaluation window, and the handover switch.

`external_handover_enabled` does not grant handover authority. If it is true,
this surface still routes to deferred hold because v0.1 owns no external
handover operation.

## 5. Preflight

Preflight fails closed with `status = blocked` and no receipt when any input:

- is not a mapping;
- has missing or extra fields;
- has a wrong scalar or list type; or
- has a digest mismatch.

Semantic route evaluation begins only after all three sealed inputs pass
preflight.

## 6. Deterministic route order

The first matching route wins.

| Priority | Disposition | Mode | Meaning |
|---:|---|---|---|
| 1 | `source_verification_receipt_repair_required` | `rejected` | predecessor is not a supported completed receipt |
| 2 | `trajectory_provenance_repair_required` | `rejected` | request identity or digest provenance is invalid |
| 3 | `trajectory_correspondence_repair_required` | `rejected` | source, request, and policy do not bind the same lineage |
| 4 | `trajectory_window_repair_required` | `rejected` | request is future-dated or stale |
| 5 | `trajectory_replay_conflict_rejected` | `rejected` | session, nonce, or receipt lineage conflicts |
| 6 | `repository_or_git_effect_request_rejected` | `rejected` | patch, execution, application, repository, or Git effect was requested |
| 7 | `authority_escalation_rejected` | `rejected` | successor authority was claimed |
| 8 | `external_handover_deferred` | `hold` | human or external-authority handover remains deferred |
| 9 | `unsupported_trajectory_format_abstained` | `abstain` | trajectory representation is unsupported |
| 10 | `trajectory_budget_rejected` | `rejected` | requested nodes or step count exceed v0.1 bounds |
| 11 | `verification_outcome_policy_repair_required` | `rejected` | the outcome-to-next-step mapping is not allowed by policy |
| 12 | `autonomous_repair_candidate_synthesized` | `autonomous_repair` | failed evidence maps to an internal repair candidate |
| 13 | `autonomous_reverification_candidate_synthesized` | `degraded_autonomy` | inconclusive evidence maps to an internal reverification candidate |
| 14 | `autonomous_deliberation_candidate_synthesized` | `autonomous_read_only` | passed evidence maps to an internal deliberation candidate |

## 7. Trajectory receipt

A successful synthesis records two node identifiers and two deterministic node
digests. The first anchors the supplied candidate lineage and the second anchors
the supplied independent-verification receipt.

For a successful outcome route:

```text
trajectory_synthesized_by_kernel = true
trajectory_read_only = true
trajectory_complete_for_available_receipts = true
full_intent_lineage_reconstructed = false
trajectory_step_count = 2
```

Exactly one of the three internal next-step candidate booleans is true.
Non-success routes emit no trajectory nodes and no next-step candidate.

The receipt digest seals the complete result. The result also binds the source
verification receipt, source candidate receipt, candidate patch, patch artifact,
verification evidence, repository, and source commit.

## 8. Deferred handover

Until a separate authority-owning surface is explicitly introduced and
authorized, a handover request has only this result:

```text
codeai_disposition = external_handover_deferred
operating_mode = hold
external_handover_deferred = true
human_handover_performed = false
external_authority_handover_performed = false
```

The route does not generate a message, notification, approval request, PR,
issue, lease, or external side effect.

## 9. Research provenance

Research is design provenance, not authority.

- [SWE-INTERACT (arXiv:2606.30573)](https://arxiv.org/abs/2606.30573)
  motivates preserving evolving requirements and avoiding over-agentic effects
  in multi-turn coding work.
- [RoadmapBench (arXiv:2605.15846)](https://arxiv.org/abs/2605.15846)
  motivates explicit trajectory structure for long-horizon, multi-file change.
- [LongCLI-Bench (arXiv:2602.14337)](https://arxiv.org/abs/2602.14337)
  motivates step-level trajectory evidence and bounded plan intervention.
- [The Verification Horizon (arXiv:2606.26300)](https://arxiv.org/abs/2606.26300)
  motivates keeping passed evidence distinct from correctness proof.
- [Scaling Test-Time Compute for Software Engineering
  (arXiv:2604.16529)](https://arxiv.org/abs/2604.16529) motivates making
  additional internal deliberation inspectable and bounded.
- [W3C PROV-O](https://www.w3.org/TR/prov-o/) motivates attributable source,
  session, artifact, and successor lineage.

No paper, benchmark, or external framework grants repository, execution, or
handover authority to this surface.

## 10. Validation surfaces

- Runtime:
  `runtime/kuuos_codeai_autonomous_trajectory_synthesis_envelope_v0_1.py`
- Route checker:
  `scripts/check_codeai_autonomous_trajectory_synthesis_envelope_v0_1.py`
- Unit tests:
  `tests/test_kuuos_codeai_autonomous_trajectory_synthesis_envelope_v0_1.py`
- Example:
  `examples/codeai_autonomous_trajectory_synthesis_envelope_v0_1.json`
- Manifest:
  `manifests/kuuos_codeai_autonomous_trajectory_synthesis_envelope_v0_1.json`
- Formal package:
  `formal/KUOS/CodeAI/AutonomousTrajectorySynthesisEnvelopeV0_1.lean`
- Independent formal root:
  `formal/KuuOSCodeAIAutonomousTrajectorySynthesisV0_1.lean`
- Dedicated workflow:
  `.github/workflows/codeai-autonomous-trajectory-synthesis-envelope-v0-1.yml`

The formal root is registered independently. It is not imported into the
canonical repository aggregate and does not change the current formal root.
