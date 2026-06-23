# ActOS Bounded Adapter Invocation v0.4

## 位置づけ

ActOS v0.4は、ActOS v0.3のactivation authorization receiptを入力として、plan activation、bounded adapter invocation、canonical host receiptを構成する。

この層はWORLD commitを行わない。

host effectが記録された場合でも、truth promotion、plan completion、rollbackは自動化しない。

## 接続経路

```text
ActOS v0.3 activation authorization
→ exact lease reservation binding
→ independent plan activation receipt
→ exact selected-step and operation-input binding
→ safety-preserving effect projection
→ bounded adapter invocation
→ effectRecorded / blocked / replayed route
→ canonical host receipt
→ post-effect observation debt
→ post-effect verification debt
```

## source authorization境界

入力receiptは次を満たす必要がある。

```text
authorization committed = true
activation authorized = true
plan activated = false
adapter invoked = false
external effect performed = false
effect record count = 0
lease reservation committed = true
reservation count = 1
```

v0.4は未実行のauthorization receiptだけを受け付ける。

## plan activation receipt

plan activationはadapter invocationと別のreceiptである。

```text
authorization bound = true
lease reservation bound = true
session and intent bound = true
activation committed = true
activation count = 1
adapter invoked = false
external effect performed = false
effect record count = 0
```

plan activation自体はexternal effectを意味しない。

## exact invocation binding

```text
activation receipt bound = true
authorization receipt bound = true
lease reservation receipt bound = true
selected step exact = true
operation identity exact = true
operation input exact = true
target cycle exact = true
adaptive epoch exact = true
capability epoch exact = true
session exact = true
action intent exact = true
adapter kind exact = true
host licence exact = true
capability exact = true
```

## effect projection

```text
selected step bound = true
operation identity bound = true
operation input bound = true
resource scope bound = true
stop conditions preserved = true
observation digest preserved = true
verification criterion preserved = true
projected effect within capability = true
projected effect within lease = true
projected only = true
```

projectionはhost invocationより前に確定する。

## bounded invocation

既存ActOS v0.1の`BoundedInvocation`を再利用する。

```text
jobs claimed <= 1
slices run <= 1
```

`effectRecorded` routeだけが次を許す。

```text
jobs claimed = 1
slices run = 1
host adapter called = true
external effect performed = true
effect record count = 1
```

## blocked route

```text
invocation attempted = true
host adapter called = false
external effect performed = false
effect record count = 0
```

blockedはeffectではない。

## replayed route

```text
invocation attempted = false
host adapter called = false
external effect performed = false
effect record count = 0
jobs claimed = 0
slices run = 0
```

正確なreceipt replayは新しいinvocationを開始しない。

## canonical host receipt

既存ActOS v0.1の`HostReceiptSemantics`を再利用する。

```text
host route = invocation route
host effect-record count = invocation effect-record count
activation receipt preserved = true
invocation receipt preserved = true
operation identity preserved = true
operation input preserved = true
selected step preserved = true
target cycle preserved = true
session preserved = true
action intent preserved = true
lease reservation consumed = true
host receipt canonical = true
```

host receiptはWORLD commit receiptではない。

## post-effect debt

`effectRecorded` routeでは次を要求する。

```text
observation required = true
verification required = true
```

`blocked`と`replayed`ではeffect-recorded debtを生成しない。

全routeで次を禁止する。

```text
automatic truth promotion = false
automatic plan completion = false
automatic rollback = false
```

## event lineage

```text
ActOS v0.3 lease reservation index
< ActOS v0.4 activation index
< ActOS v0.4 invocation index
< ActOS v0.4 host receipt index
```

Act historyにはactivation、invocation、host receiptの3 recordを追加する。

## 所有権

```text
plan activation owner = ActOS
adapter invocation owner = ActOS
canonical host receipt owner = host
WORLD commit owner = WORLD
```

host effect receiptからWORLD commitへ直接昇格しない。

## 非権限境界

```text
activation != adapter invocation
adapter invocation != WORLD commit
host receipt != WORLD truth
host receipt != automatic plan completion
host receipt != automatic rollback
host receipt != clinical authority
host receipt != legal authority
host receipt != institutional authority
host receipt != theorem authority
```

## Lean定理

```text
invocation_requires_committed_nonexecuting_authorization
invocation_consumes_exact_reserved_lease_use
activation_is_committed_before_invocation_without_effect
exact_invocation_binding_is_complete
invocation_projection_preserves_safety_and_effect_ceilings
adapter_invocation_is_bounded
effect_recorded_route_invokes_once_and_records_once
blocked_route_has_no_call_effect_or_record
replayed_route_is_idempotent_and_starts_no_new_invocation
host_receipt_is_canonical_and_preserves_identity
host_route_and_effect_count_are_exact
effect_recorded_preserves_observation_and_verification_debt
blocked_or_replayed_records_no_posteffect_effect
posteffect_debt_grants_no_automatic_promotion_completion_or_rollback
invocation_events_append_strictly
invocation_history_appends_three_records
bridge_preserves_separated_ownership
invocation_and_host_receipt_do_not_commit_world_or_promote_truth
invocation_digest_is_exact
```

## Honest classification

```text
an ActOS-owned bounded adapter-invocation layer over a committed v0.3
activation authorization and exact lease reservation, with a separate plan
activation receipt, at most one job and one slice, explicit effectRecorded,
blocked and replayed routes, a canonical host receipt, and mandatory
post-effect observation and verification debt, while leaving WORLD commit and
truth promotion outside this layer
```
