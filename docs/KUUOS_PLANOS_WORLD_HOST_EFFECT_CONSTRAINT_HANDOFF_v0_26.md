# PlanOS World Host-Effect Constraint Handoff v0.26

## 位置づけ

PlanOS v0.26は、PlanOS v0.25で生成したprimary候補とhold候補をhysteresisおよびconstraintで評価し、admissible setをDecisionOSへ渡す。

この層は候補を選択せず、計画を合成せず、実行しない。

## 接続経路

```text
PlanOS v0.25 generated candidates
→ hysteresis evaluation
→ mission and authority constraints
→ admissible primary candidate
→ always-available hold candidate
→ admissible-set handoff to DecisionOS
→ immutable handoff receipt
```

## phase prefix

```text
generate
→ constrain
→ deliberate
```

`synthesize`と`commitNext`へは自動遷移しない。

## primary候補

primary候補を含める場合、次を要求する。

```text
mission invariants preserved = true
authority boundary preserved = true
resource envelope satisfied = true
applicability condition valid = true
reversal condition visible = true
expiration condition valid = true
observation debt visible = true
verification debt visible = true
scope compatible = true
Qi transition ready = true
hysteresis passed = true
```

switch exemptでないprimary候補は、base threshold、Qi hysteresis、oscillation penalty、recovery-protection penaltyの合計以上のswitch benefitを必要とする。

## hold候補

```text
hold candidate = hold
switch exempt = true
included = true
admissible = true
hysteresis passed = true
forwarded to DecisionOS = true
```

holdは安全な非切替経路として常に保持する。

## DecisionOS handoff

```text
generated set bound = true
admissible set bound = true
all forwarded candidates admissible = true
identities preserved = true
alternatives preserved = true
dissent visible = true
minority preserved = true
DecisionOS owns selection = true
selection receipt supplied = false
selection performed = false
plan synthesis performed = false
decision not execution = true
silent substitution detected = false
handoff committed = true
```

## WORLD dispositionとの分離

```text
source disposition preserved = true
governance review preserved = true
WORLD commit separate = true
fresh commit authorization required = true
fresh commit authorization supplied = false
atomic commit ready = false
forwarded candidate is WORLD disposition = false
handoff resolves WORLD disposition = false
```

admissibleなreplan候補は、WORLD adoptionまたはrejectionの決定ではない。

## 所有権

```text
constraint owner = PlanOS
selection owner = DecisionOS
synthesis owner = PlanOS
execution owner = ActOS
WORLD disposition owner = WORLD
```

## receiptとledger

```text
receipt committed = true
receipt immutable = true
append only = true
exact replay idempotent = true
conflicting replay accepted = false

generation index
< constrain index
< handoff index
```

constraintとhandoffの2 recordをappendする。

## 非権限境界

```text
handoff != selection
handoff != synthesis
handoff != activation
handoff != execution
handoff != host license
handoff != WORLD disposition resolution
handoff != WORLD update
handoff != memory overwrite
```

## Leanファイル

```text
WorldHostEffectConstraintDecisionHandoffCoreV0_26.lean
WorldHostEffectConstraintDecisionHandoffTypesV0_26.lean
WorldHostEffectConstraintDecisionHandoffV0_26.lean
```

## Lean定理

```text
constraint_handoff_preserves_world_disposition
constraint_handoff_receipt_is_replay_safe
handoff_requires_committed_generation
follows_constraint_deliberation_prefix
hold_is_admissible_and_forwarded
hold_exemption_is_explicit
included_primary_requires_hysteresis_margin
handoff_preserves_admissible_set
handoff_is_not_selection_synthesis_or_execution
handoff_preserves_world_disposition_candidate
constraint_handoff_receipt_is_immutable_and_replay_safe
events_append_strictly
history_appends_two_records
bridge_preserves_os_ownership
bridge_grants_no_new_authority
constraint_handoff_digest_is_exact
```
