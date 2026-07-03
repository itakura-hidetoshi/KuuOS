# KuuOS Lifecycle Bounded Transition Decision v0.18

## 位置づけ

KuuOS Lifecycle Bounded Transition Decision v0.18は、独立したApoptosis Lifecycle Governance系列に属します。

この段階はrepository mutation roadmap v1.25ではありません。

v0.18は、v0.17が`LIFECYCLE_BOUNDED_TRANSITION_REVIEW_CLEAR_FOR_SEPARATE_TRANSITION_DECISION`としたproposalについて、独立したdecision makerがtransition preparationへ進めるかを決定するread-only層です。

```text
Lifecycle Bounded Transition Review v0.17
→ Lifecycle Bounded Transition Decision v0.18
→ separate Lifecycle Bounded Transition Preparation
```

## Source completion

v0.18はv0.1からv0.17までのsource chainを完全再計算します。

source transition reviewは次を満たす必要があります。

- transition review recordが発行済みである。
- transition reviewがcompletedである。
- clear for transition decisionである。
- transition decisionとそのrouteが次段階として要求されている。
- transition reassessmentは要求されていない。
- transition decisionはまだ行われていない。
- lifecycle transitionは実行されていない。
- authority、quiescence、terminal state、resource、repositoryにeffectがない。
- source artifactの完全再計算結果が一致する。

BLOCKEDまたはREJECTEDのv0.17 artifactはv0.18へ入力できません。

## Canonical lifecycle state

v0.18はlifecycle stateを次の正規化された状態スナップショットとして扱います。

```text
LifecycleState
=
AuthorityState
× QuiescenceState
× TerminalState
× ResourceState
× StateRevision
```

状態名を全系列共通の固定enumとして閉じません。

具体的な状態語彙と許可関係はpolicy-supplied artifactとして管理します。

state digestは状態成分とrevisionから決定的に導出します。

## Allowed transition relation

v0.18は、digest一致だけではtransitionの妥当性を認めません。

明示的なtransition ruleが次を束縛する必要があります。

- current state digest。
- transition kind。
- target state digest。
- policy basis digest。
- reversible requirementまたは不可逆例外要件。
- authority continuity requirement。
- ruleのactive状態。

`AllowedTransition current kind target rule`は次を要求します。

- current stateとtarget stateが正規である。
- ruleが正規かつactiveである。
- ruleのcurrent、kind、targetがproposalと一致する。
- currentとtargetが同一状態ではない。
- target state revisionがcurrent state revisionより新しい。

## Stale-state prevention

v0.17でreviewされたcurrent lifecycle state digestと、v0.18 decision時に取得されたcurrent state snapshot digestは一致しなければなりません。

一致しない場合、decisionはREJECTEDになります。

このexpected current state digestはAPPROVED artifactへ保持され、後続preparationでも再検証されます。

これはrepository CASそのものではありません。

古い状態前提に基づくdecisionを後続へ適用しないためのlifecycle-state bindingです。

## Independent decision maker

transition decision makerはv0.17 transition reviewerから分離されます。

さらに、少なくとも次から分離されます。

- subject。
- requester。
- v0.11 decision reviewer。
- v0.12 authorization decision maker。
- v0.13 operation approver。
- v0.14 operator。
- v0.15 completion reviewer。
- v0.16 post-operation reviewer。
- v0.17 transition reviewer。
- 将来のtransition preparer。

organizationもv0.17 transition reviewer organizationから分離します。

mandate、qualification、identity、conflict disclosure、jurisdiction、decision readinessを確認します。

## Immutable preparation route

APPROVED後のtransition preparation routeは次から決定的に導出します。

- source transition review IDとrecord digest。
- source review route digest。
- proposed transition kind。
- expected current state digest。
- target state digest。
- transition rule digest。
- transition preparer ID。
- preparation deadline。

decision makerはこのrouteを変更せずにdecision artifactへ記録します。

## Status

v0.18は次の三状態だけを返します。

```text
LIFECYCLE_BOUNDED_TRANSITION_DECISION_APPROVED_FOR_SEPARATE_TRANSITION_PREPARATION
LIFECYCLE_BOUNDED_TRANSITION_DECISION_DENIED
LIFECYCLE_BOUNDED_TRANSITION_DECISION_REJECTED
```

### Approved

APPROVEDはtransition preparationへ進めるというdecisionです。

次がtrueになります。

- transition decision record issued。
- transition decision made。
- transition approved for preparation。
- transition preparation required next。
- transition preparation route required next。

APPROVEDでもtransition packageはまだ構築されません。

transition approval、start、completion、state mutationも行われません。

### Denied

source、binding、state relation、authorityが有効でも、decision makerが承認しない場合、またはunresolved anomaly、recovery requirement、institutional hold、emergency stateが存在する場合はDENIEDになります。

DENIEDは有効なdecision recordです。

transition preparationへは進まず、appealまたはreconsideration経路を保持します。

### Rejected

source recomputation、identity、role separation、state snapshot、AllowedTransition、route、time boundaryなどが構造的に不正な場合はREJECTEDになります。

REJECTEDでは有効なdecision recordを発行しません。

## 段階限定の実行境界

v0.18はdecision artifactだけを発行します。

次は後続段階へ分離します。

- transition package construction。
- transition package approval。
- transition start。
- transition completion。
- authority change。
- quiescence state change。
- terminal state change。
- terminal marker write。
- resource removal。
- external operation。
- repository mutation。

この分離はv0.18の責務境界であり、将来のtransition capabilityを恒久的に禁止するものではありません。

```text
transition review
!= transition decision
!= transition preparation
!= transition execution
!= repository mutation
```

## Validation

focused auditはAPPROVED、DENIED、REJECTED、source recomputation、fresh-digest tamper、stale state、target-state substitution、inactive rule、non-advancing revision、reviewer separation、preparer separation、organization separation、route binding、time bounds、determinism、record integrityを検証します。

Lean境界はAPPROVEDがclear source review、non-stale current state、AllowedTransitionを必要とすること、APPROVEDが別のpreparationだけへroutingすること、DENIEDが有効なrecordを持つがpreparationを要求しないこと、REJECTEDが有効なrecordを発行しないこと、v0.18がtransitionまたはrepository effectを行わないことを固定します。

Lean成功は、現実のstate observation、policy basis、decision maker authority、法的適合性、将来のtransition preparationまたはexecutionの安全性を証明しません。
