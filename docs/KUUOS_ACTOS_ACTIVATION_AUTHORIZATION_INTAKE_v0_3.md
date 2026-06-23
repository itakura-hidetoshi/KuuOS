# ActOS Activation Authorization Intake v0.3

## 位置づけ

ActOS v0.3は、PlanOS v0.23のactivation-admission handoffをActOS側で独立に再検証し、activation authorization receiptとlease-use reservationを生成する。

この層はadapterを呼び出さず、external effectを発生させず、effect recordを作らない。

## 接続経路

```text
PlanOS v0.23 ActOS handoff
→ exact Act cycle revalidation
→ committed-plan and exact-step binding
→ independent freshness revalidation
→ capability registry confirmation
→ lease validity and remaining-use confirmation
→ session concordance
→ action-intent replay exclusion
→ single-use staged-effect authorization
→ one lease-use reservation
→ activation authorization receipt
```

## PlanOS handoff intake

入力receiptは次を満たす必要がある。

```text
PlanOS handoff committed = true
PlanOS admission committed = true
plan activated = false
execution performed = false
lease use reserved = false
```

ActOSはPlanOSのadmission結果を受け取るが、そのまま実行許可として扱わない。

## exact Act cycle

```text
Act plan cycle = PlanOS target cycle
Act cycle = Act plan cycle
Act phase = true
```

前周期のauthority materialを再利用しない。

## fivefold binding

既存ActOS v0.1のfivefold bindingを再利用する。

```text
committed plan bound = true
exact step bound = true
Act phase bound = true
host licence bound = true
projection receipt bound = true
```

## effectful step safety

```text
selected step is Act candidate = true
selected step is effectful = true
stop conditions present = true
observation digest present = true
verification criterion present = true
```

stop、observation、verificationの境界を失ったstepはauthorizeしない。

## independent freshness revalidation

ActOSはPlanOS v0.23のfreshness判定を単に信頼せず、独立に再検証する。

```text
handoff fresh = true
human approval fresh = true
host licence fresh = true
capability fresh = true
lease fresh = true
session fresh = true
action intent fresh = true
```

ActOS側のtarget cycle、adaptive epoch、capability epochはPlanOS側の値と厳密に一致する。

## capability registry confirmation

```text
registry entry present = true
registry entry revoked = false
owner exact = true
lineage exact = true
capability identity exact = true
adapter kind exact = true
capability epoch exact = true
operation allowed = true
resource allowed = true
effect within ceiling = true
```

registry entryが存在しても、revoked entryはauthorizeしない。

## lease-use reservation

```text
lease valid = true
lease expired = false
holder exact = true
scope exact = true
session exact = true
intent exact = true
remaining uses before > 0
remaining uses after + 1 = remaining uses before
reservation count = 1
reservation committed = true
```

一回のauthorizationで一回だけlease useを予約する。

正確なreceipt replayは冪等であり、重複予約を作らない。

## sessionとintent replay

```text
session open = true
session identity exact = true
generation exact = true
action intent bound = true
action intent distinct from DecisionOS selection = true
intent nonce fresh = true
intent previously consumed = false
conflicting replay detected = false
exact receipt replay idempotent = true
```

DecisionOS selectionをaction intentとして流用しない。

## single-use authorization

既存ActOS v0.1とv0.2のauthorization boundaryを再利用する。

```text
explicit step authorization = true
human approval when required = true
single use = true
licence not widened = true
inner authorization canonical = true
inner authorization unchanged = true
```

## staged effect

```text
selected step bound = true
operation input bound = true
stop, observation and verification preserved = true
projected only = true
host adapter invoked = false
external effect performed = false
effect record count = 0
```

authorizationはstaged effectを許可するだけであり、effectを実行しない。

## activation authorization receipt

```text
handoff intake bound = true
freshness revalidated = true
capability registry confirmed = true
lease reservation bound = true
session and intent confirmed = true
staged effect confirmed = true
activation authorized = true
authorization committed = true
plan activated = false
adapter invoked = false
external effect performed = false
effect record count = 0
```

**activation authorized**は**plan activated**と同一ではない。

## event lineage

```text
PlanOS v0.23 handoff index
< ActOS intake index
< ActOS authorization index
< ActOS lease reservation index
```

Act historyにはintake、authorization、reservationの3 recordを追加する。

## 所有権

```text
activation authorization owner = ActOS
adapter invocation owner = ActOS
execution owner = ActOS
```

同じActOS所有でも、authorization、invocation、executionは別receiptである。

## 非権限境界

```text
authorization != plan activation
authorization != adapter invocation
authorization != external effect
authorization != effect record
authorization != clinical authority
authorization != legal authority
authorization != institutional authority
authorization != theorem authority
```

## Lean定理

```text
intake_requires_committed_nonexecuting_planos_handoff
exact_act_cycle_revalidates_planos_target
fivefold_binding_is_complete
selected_step_is_effectful_and_safety_bound
freshness_is_independently_revalidated
freshness_epochs_match_exact_target
registry_entry_is_present_unrevoked_and_exact
registry_scope_and_effect_are_allowed
lease_reservation_consumes_exactly_one_remaining_use
lease_reservation_preserves_holder_scope_session_and_intent
lease_reservation_is_replay_safe
session_and_intent_are_fresh_distinct_and_nonreplayed
authorization_is_single_use_and_cannot_widen_license
authorization_envelope_preserves_operation_receipts_and_approval
staged_effect_remains_projected_and_noninvoked
activation_authorization_is_committed_without_activation_or_effect
act_events_append_strictly_from_planos_handoff
act_history_appends_three_records
bridge_preserves_actos_ownership
bridge_grants_no_activation_invocation_or_effect
authorization_digest_is_exact
```

## Honest classification

```text
an ActOS-owned activation-authorization intake over a committed PlanOS v0.23
handoff, with independent freshness and registry revalidation, exact single-use
lease reservation, session and intent replay exclusion, and a committed
nonexecuting authorization receipt, but without plan activation, adapter
invocation, external effect or effect record
```
