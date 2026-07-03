# KuuOS Lifecycle Bounded Transition Approval v0.20

## 位置づけ

Lifecycle Bounded Transition Approval v0.20は、repository mutation roadmapとは独立したlifecycle governance系列の段階です。

v0.20は、v0.19が次の状態で発行したpreparation recordだけをsourceとして受け取ります。

```text
LIFECYCLE_BOUNDED_TRANSITION_PREPARATION_READY_FOR_SEPARATE_TRANSITION_APPROVAL
```

処理順序は次です。

```text
Lifecycle Bounded Transition Preparation v0.19
→ Lifecycle Bounded Transition Approval v0.20
→ separate Lifecycle Bounded Transition Start Authorization
```

v0.20はprepared packageを承認または否認します。

v0.20はtransitionを開始せず、完了せず、lifecycle state mutationまたはrepository mutationを行いません。

## Source chain

v0.20はv0.1からv0.19までのsource artifactを完全再計算します。

source preparationは次を満たす必要があります。

- preparation recordが発行済みである。
- preparationが完了している。
- transition packageが構築済みである。
- separate transition approvalへ進むrouteが要求されている。
- lifecycle stateとrepositoryがread-onlyである。
- transition approval、start authorization、start、completion、mutationがまだ発生していない。

BLOCKEDまたはREJECTEDのv0.19 artifactはv0.20へ入力できません。

## Approval route

v0.20はv0.19のapproval route digestを再計算します。

次の差替えはREJECTEDです。

- source preparation record。
- transition package digest。
- transition approver。
- future operator。
- current lifecycle state digest。
- target lifecycle state digest。
- approval deadline。

v0.20は承認後のstart authorization routeも固定します。

このrouteは次を束縛します。

- source preparation ID。
- source preparation record digest。
- transition approval ID。
- transition package digest。
- transition approver。
- future operator。
- current and target lifecycle state digest。
- start authorization deadline。

## Status

v0.20は次の三状態を返します。

```text
LIFECYCLE_BOUNDED_TRANSITION_APPROVAL_APPROVED_FOR_SEPARATE_TRANSITION_START_AUTHORIZATION
LIFECYCLE_BOUNDED_TRANSITION_APPROVAL_DENIED
LIFECYCLE_BOUNDED_TRANSITION_APPROVAL_REJECTED
```

### APPROVED

source、route、approver、operator、state、time boundaryが有効です。

approver authority、package freshness、current state freshness、target state validity、hold/recovery/anomaly absenceも確認済みです。

有効なapproval recordを発行し、separate transition start authorizationへだけ進めます。

transitionはまだ開始しません。

### DENIED

source、route、identity、time boundaryは構造的に有効です。

ただし、authority、freshness、state validity、hold/recovery/anomalyなどの実質条件が承認に足りません。

有効なapproval recordを発行します。

start authorizationへは進めず、reapprovalまたはrepreparation routeを要求します。

### REJECTED

source recomputation、route binding、package binding、role separation、time boundaryなどが構造的に不正です。

有効なapproval recordを発行しません。

## 段階境界

v0.20が行うのはtransition package approvalだけです。

次は後続段階へ分離します。

- transition start authorization。
- transition start。
- transition completion。
- lifecycle state mutation。
- authority mutation。
- terminal marker writing。
- resource removal。
- external operation。
- repository mutation。

## Validation

focused auditはsource再計算、APPROVED、DENIED、REJECTED、route binding、actor separation、freshness、state staleness、hold/recovery/anomaly、time boundary、determinism、無effect性を検証します。

Strict Lean境界はAPPROVEDがseparate start authorizationへだけroutingされること、DENIEDがstart authorizationへ進まないこと、REJECTEDがrecordを発行しないこと、v0.20がtransitionまたはrepository effectを行わないことを固定します。
