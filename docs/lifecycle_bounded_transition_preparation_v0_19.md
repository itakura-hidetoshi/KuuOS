# KuuOS Lifecycle Bounded Transition Preparation v0.19

## 位置づけ

Lifecycle Bounded Transition Preparation v0.19は、repository mutation roadmapとは独立したlifecycle governance系列の段階です。

v0.19は、v0.18が次の状態で承認したtransitionだけを入力として受け取ります。

```text
LIFECYCLE_BOUNDED_TRANSITION_DECISION_APPROVED_FOR_SEPARATE_TRANSITION_PREPARATION
```

処理順序は次です。

```text
Lifecycle Bounded Transition Decision v0.18
→ Lifecycle Bounded Transition Preparation v0.19
→ separate Lifecycle Bounded Transition Approval
```

v0.19は具体的なtransition packageを構築しますが、そのpackageを承認せず、transitionを開始または完了しません。

## Source chain

v0.19はv0.1からv0.18までのsource artifactを完全再計算します。

source decisionは次を満たす必要があります。

- decision recordが発行済みである。
- decisionが完了している。
- transition preparationへの進行が承認されている。
- preparationとそのrouteが次段階として要求されている。
- lifecycle stateとrepositoryがread-onlyである。
- transitionの後続effectがまだ発生していない。

DENIEDまたはREJECTEDのv0.18 artifactはv0.19へ入力できません。

## Transition package

packageは次を一つのdigestへ固定します。

- source transition decision ID。
- transition kind。
- expected current lifecycle state digest。
- proposed target lifecycle state digest。
- transition rule digest。
- 順序付きstep列。
- rollback plan。
- recovery plan。
- monitoring plan。
- evidence capture plan。
- resource reservation。
- authority continuity plan。
- irreversible stepの例外根拠。
- aggregate stop conditions。
- bounded execution window。

各stepは次を持ちます。

- 一意なstep ID。
- 連続したsequence number。
- action kind。
- target resource ID。
- expected pre-state digest。
- proposed post-state digest。
- reversibility。
- rollback step binding。
- evidence capture binding。
- stop condition binding。

最初のstepはv0.18が束縛したcurrent stateから開始します。

最後のstepはv0.18が束縛したtarget stateで終了します。

隣接stepのpost-stateとpre-stateは一致しなければなりません。

## Role separation

transition preparerはv0.18が事前に指定したpreparerと一致する必要があります。

preparerはsubject、requester、v0.11以後のreviewer、decision maker、approver、operatorなどのprior actorから分離されます。

preparer organizationはv0.18 decision maker organizationから分離されます。

将来のtransition approverはpreparer、decision maker、prior actor、future operatorから分離されます。

future operatorはpreparer、approver、decision maker、prior actorから分離されます。

## Approval route

v0.19は次をtransition approval routeへ固定します。

- source decision IDとrecord digest。
- v0.18 preparation route digest。
- transition package digest。
- transition approver ID。
- future operator ID。
- expected current state digest。
- proposed target state digest。
- approval deadline。

後続approval段階はこのrouteを再計算し、packageまたは担当者の差替えを拒否します。

## Status

v0.19は次の三状態を返します。

```text
LIFECYCLE_BOUNDED_TRANSITION_PREPARATION_READY_FOR_SEPARATE_TRANSITION_APPROVAL
LIFECYCLE_BOUNDED_TRANSITION_PREPARATION_BLOCKED
LIFECYCLE_BOUNDED_TRANSITION_PREPARATION_REJECTED
```

### PREPARED

source、package、role、time、routeが有効で、必要なplanとcontrolがすべて揃う場合です。

有効なpreparation recordを発行し、別のtransition approvalを要求します。

### BLOCKED

構造とsourceは有効ですが、rollback、recovery、monitoring、evidence、reservation、authority continuity、irreversible justification、stop conditions、またはinstitutional conditionが不十分な場合です。

有効なpreparation recordを発行しますが、approvalへ進まず、repreparationへ戻します。

### REJECTED

source recomputation、identity、state、rule、step chain、role separation、route、time boundaryなどが構造的に不正な場合です。

有効なpreparation recordを発行しません。

## 段階境界

v0.19が行うのはpackage preparationだけです。

次は後続段階へ分離します。

- transition package approval。
- transition start authorization。
- transition start。
- transition completion。
- lifecycle state change。
- external operation。
- repository mutation。

この責務境界は将来の能力を恒久的に禁止するものではありません。

## Validation

focused auditはsource再計算、PREPARED、BLOCKED、REJECTED、step order、step chain、state and rule binding、role separation、route binding、time bounds、determinism、無effect性を検証します。

Strict Lean境界はcomplete packageがseparate approvalへだけroutingされること、BLOCKEDがrepreparationへ戻ること、REJECTEDがrecordを発行しないこと、v0.19がtransitionまたはrepository effectを行わないことを固定します。
