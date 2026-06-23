# WORLD Host-Effect Intake v0.52

## 位置づけ

WORLD v0.52は、ActOS v0.4のcanonical host receiptを、将来のWORLD保存処理に向けたintake candidateへ変換する。

この層は保存処理を実行しない。

既存のWORLD保存kernelは、ObserveOS receipt、VerifyOS receipt、verified WORLD disposition、fresh authorizationを前提とする。

未観測のhost effect receiptを直接WORLD stateへ昇格させない。

## 接続経路

```text
ActOS v0.4 effectRecorded host receipt
→ exact effect-record identity binding
→ ObserveOS source-effect binding
→ evidence requirements
→ immutable provenance trace
→ unpaid observation debt
→ unpaid verification debt
→ future prerequisite declaration
→ WORLD intake candidate
```

## effectRecorded限定

```text
host route = effectRecorded
effect record count = 1
external effect recorded = true
canonical host receipt = true
source WORLD update performed = false
```

`blocked`と`replayed`はeffect recordを持たないため、intake candidateにならない。

## identity binding

```text
operation identity preserved = true
operation input preserved = true
selected step preserved = true
target cycle preserved = true
session preserved = true
action intent preserved = true
lease reservation consumed = true
effect record immutable = true
```

## ObserveOS binding

既存ObserveOS v0.1の`SourceEffectBinding`を再利用する。

```text
committed Act state = true
effect recorded = true
canonical ready receipt = true
host invocation bound = true
selected step bound = true
operation bound = true
expected observation bound = true
verification criterion bound = true
```

## evidence requirements

```text
raw artifact digest
value digest
collector identity
independent source identity
collection time
uncertainty digest
calibration digest
context digest
tamper-evidence digest
provenance chain
```

source identityとraw artifactの不変性を保持する。

## unpaid evidence debt

```text
effect recorded = true
observation required = true
verification required = true
observation committed = false
verification committed = false
independent WORLD evidence present = false
```

host receiptは独立WORLD evidenceではない。

## future prerequisites

将来のWORLD保存には次を要求する。

```text
ObserveOS receipt
VerifyOS receipt
verified WORLD disposition
fresh authorization
successor generation
fresh fencing token
optimistic concurrency match
```

v0.52では次を固定する。

```text
ObserveOS receipt supplied = false
VerifyOS receipt supplied = false
verified WORLD disposition supplied = false
fresh authorization supplied = false
WORLD update ready = false
WORLD update performed = false
```

## event lineage

```text
ActOS v0.4 host receipt index
< WORLD v0.52 intake index
```

WORLD intake historyには1 recordをappendする。

## 所有権

```text
intake owner = WORLD
observation owner = ObserveOS
verification owner = VerifyOS
future WORLD update owner = WORLD
```

## 非権限境界

```text
intake candidate != WORLD update
host effect record != WORLD truth
host effect record != causal attribution
intake != observation authority
intake != verification authority
intake != execution authority
intake != plan activation
intake != memory overwrite
intake != constitutional-root rewrite
```

自動的なtruth promotion、plan completion、rollbackを禁止する。

## Lean定理

```text
intake_requires_canonical_effect_record
candidate_preserves_effect_identity
observeos_source_binding_is_complete
evidence_requirements_are_complete
provenance_is_complete_and_immutable
observation_and_verification_debts_remain_unpaid
atomic_commit_prerequisites_are_explicit_but_unsupplied
intake_is_not_atomic_commit
pending_debt_forbids_automatic_promotion_completion_or_rollback
intake_history_appends_one_record
intake_index_follows_host_receipt
ownership_boundaries_are_preserved
intake_grants_no_truth_causality_observation_verification_or_execution
intake_digest_is_exact
```
