# ObserveOS World Host-Effect Observation v0.4

## 位置づけ

ObserveOS v0.4は、WORLD v0.52のhost-effect intake candidateを入力として、独立証拠を収集し、effect-grounded observation receiptを生成する。

この層は検証、truth promotion、因果帰属、WORLD更新を行わない。

## 接続経路

```text
WORLD v0.52 intake candidate
→ exact Act cycle binding
→ upstream lineage preservation
→ source effect and expected-observation binding
→ independent evidence collection
→ uncertainty, calibration and provenance binding
→ matched / divergent / inconclusive / conflicted comparison
→ immutable ObserveOS receipt
→ conditional observation-debt discharge
→ VerifyOS handoff remains required
```

## source境界

```text
WORLD intake ready = true
candidate only = true
observation committed = false
verification committed = false
independent WORLD evidence present = false
```

## 独立証拠

```text
raw artifact collected = true
value collected = true
collector identity bound = true
independent source identity bound = true
collection time bound = true
uncertainty bound = true
calibration bound = true
context bound = true
tamper evidence bound = true
provenance bound = true
collector independent from ActOS = true
source independent from host receipt = true
host receipt used as independent evidence = false
collection count = 1
```

host receiptを独立証拠として再利用しない。

## verdict

既存ObserveOS v0.1の`ComparisonVerdict`を再利用する。

```text
matched
→ observation debt discharged
→ reobservation not required
→ qualifying observation supplied

divergent
→ observation debt discharged
→ reobservation not required
→ qualifying observation supplied

inconclusive
→ observation debt remains
→ reobservation required
→ qualifying observation not supplied

conflicted
→ observation debt remains
→ reobservation required
→ qualifying observation not supplied
```

`divergent`は観測成立を意味するが、因果帰属やtruth authorityを与えない。

## verification debt

全verdictで次を保持する。

```text
observation is not verification
verification required = true
VerifyOS receipt supplied = false
verified WORLD disposition supplied = false
fresh commit authorization supplied = false
atomic commit ready = false
```

## receipt

```text
receipt committed = true
receipt immutable = true
append only = true
exact replay idempotent = true
conflicting replay accepted = false
verification completed = false
truth promoted = false
causal attribution granted = false
WORLD updated = false
```

## event lineage

```text
WORLD v0.52 intake index
< ObserveOS evidence-collection index
< ObserveOS receipt index
```

Observe historyには2 recordをappendする。

## 所有権

```text
observation owner = ObserveOS
verification owner = VerifyOS
future atomic-commit owner = WORLD
```

## 非権限境界

```text
observation != verification
matched != truth
matched != causal proof
divergent != causal attribution
observation receipt != WORLD update
observation receipt != execution permission
observation receipt != memory overwrite
```

## Lean定理

```text
observation_requires_ready_uncommitted_world_intake
observation_uses_exact_act_cycle
observation_preserves_upstream_lineage
source_effect_and_identity_are_exactly_bound
evidence_collection_is_independent_complete_and_single
evidence_contract_reuses_world_intake_requirements
comparison_is_observation_not_verification_truth_or_causality
matched_observation_discharges_observation_debt
divergent_observation_discharges_observation_debt
inconclusive_observation_requires_reobservation
conflicted_observation_requires_reobservation
every_observation_receipt_preserves_verification_debt
observation_receipt_is_immutable_append_only_and_replay_safe
observation_receipt_grants_no_verification_truth_causality_or_world_update
evidence_collection_and_receipt_are_single_use
observation_events_append_strictly
observation_history_appends_two_records
ownership_is_separated
observation_receipt_digest_is_exact
```
