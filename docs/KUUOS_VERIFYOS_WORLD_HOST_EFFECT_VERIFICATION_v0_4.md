# VerifyOS World Host-Effect Verification v0.4

## 位置づけ

VerifyOS v0.4は、ObserveOS v0.4のqualifying observation receiptを独立検証し、WORLD disposition candidateを生成する。

この層はWORLD adoption、WORLD rejection、atomic commit、learning activationを自動実行しない。

## 接続経路

```text
WORLD v0.52 intake candidate
→ ObserveOS v0.4 independent observation receipt
→ qualifying-observation gate
→ exact Verify cycle and lineage binding
→ criterion and evidence binding
→ falsification challenge
→ independent corroboration
→ VerifyOS adjudication
→ passed / failed / indeterminate receipt
→ adopt / reject / defer-or-reobserve disposition candidate
```

## 入力資格

VerifyOS adjudicationには次を同時に要求する。

```text
source observation receipt committed = true
observation debt discharged = true
qualifying observation supplied = true
reobservation required = false
verification required = true
VerifyOS receipt already supplied = false
```

ObserveOSの`inconclusive`と`conflicted`はreceiptとして保存されるが、qualifying observationではないため、このgateを通過しない。

## 独立検証

```text
verify request authorized = true
verifier independent from ObserveOS = true
verifier independent from ActOS = true
verifier independent from host receipt = true
verification window bound = true
protocol bound = true
criterion bound before adjudication = true
evidence integrity rechecked = true
provenance integrity rechecked = true
uncertainty preserved = true
calibration preserved = true
verification count = 1
exact replay idempotent = true
conflicting replay accepted = false
```

## 再利用するVerifyOS surface

既存VerifyOS v0.1とv0.2の次を再利用する。

```text
SourceObservationBinding
CriterionEvidenceBinding
CriterionBinding
FalsificationBoundary
ChallengeRequirements
CorroborationSurface
AdjudicationBoundary
VerificationDebtSemantics
VerificationTruthBoundary
QiVerificationBoundary
FutureOnlyLearningBoundary
SingleUseVerification
```

## 判定意味論

```text
passed
→ verification debt discharged
→ verification required = false
→ corrective action required = false
→ adopt disposition candidate

failed
→ verification debt discharged
→ verification required = false
→ corrective action required = true
→ reject disposition candidate

indeterminate
→ verification debt remains
→ reobservation required = true
→ defer-or-reobserve disposition candidate
```

## WORLD disposition candidate

```text
disposition candidate committed = true
governance review required = true
WORLD commit separate = true
fresh commit authorization required = true
fresh commit authorization supplied = false
atomic commit ready = false
automatic WORLD adoption = false
automatic WORLD rejection = false
automatic WORLD commit = false
```

`passed`はWORLD adoptionそのものではない。

`failed`は自動WORLD rejectionやrollbackではない。

`indeterminate`はevidence deletionやforced collapseではない。

## future-only learning

全判定で次を保持する。

```text
learning required = true
learning future only = true
automatic learning = false
```

## receiptとevent lineage

```text
verification receipt committed = true
verification receipt immutable = true
append only = true
exact replay idempotent = true
conflicting replay accepted = false

ObserveOS receipt index
< VerifyOS request index
< VerifyOS receipt index
```

Verify historyには1 recordをappendする。

## 所有権

```text
observation owner = ObserveOS
verification owner = VerifyOS
disposition candidate owner = WORLD
future atomic-commit owner = WORLD
```

## 非権限境界

```text
verification != truth
verification != causal attribution
verification != WORLD adoption
verification != WORLD rejection
verification receipt != atomic commit
verification receipt != execution permission
verification receipt != memory overwrite
verification receipt != automatic learning
```

## Lean定理

```text
verification_requires_qualifying_observation
qualification_gate_is_complete
nonqualifying_observation_cannot_satisfy_gate
verification_uses_exact_observe_cycle
verification_preserves_full_lineage
source_observation_criterion_and_evidence_are_exact
criterion_challenge_and_falsification_are_complete
verification_execution_is_independent_single_and_replay_safe
passed_verification_maps_to_adopt_candidate
failed_verification_maps_to_reject_candidate
indeterminate_verification_maps_to_defer_or_reobserve
verification_remains_candidate_not_truth_causality_or_commit
verification_learning_handoff_is_future_only
verification_receipt_is_immutable_append_only_and_single_use
verification_events_append_exactly_once
verification_history_appends_one_record
verification_grants_no_downstream_authority
verification_receipt_digest_is_exact
```
