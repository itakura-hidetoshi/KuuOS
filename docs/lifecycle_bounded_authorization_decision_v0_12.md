# KuuOS Lifecycle Bounded Authorization Decision v0.12

## 位置づけ

KuuOS Lifecycle Bounded Authorization Decision v0.12は、独立したApoptosis Lifecycle Governance系列に属します。

この段階はrepository mutation roadmap v1.25ではありません。

v0.12は、v0.11が`LIFECYCLE_BOUNDED_DECISION_REVIEW_CLEAR_FOR_AUTHORIZATION_DECISION`とした限定的なlifecycle requestについて、指定済みのauthorization decision makerが認可判断を記録する層です。

v0.12はauthorization decisionを行います。

しかし、v0.12はoperation approval、operation start、operation completion、authority change、quiescence change、terminal-state change、terminal marker write、resource removal、external operation、repository mutationを行いません。

```text
lifecycle bounded request
→ lifecycle bounded decision review
→ lifecycle bounded authorization decision
→ separate operation approval
```

## Source review

v0.12はv0.1からv0.11までの全source chainを完全再計算します。

source decision reviewは次をすべて満たす必要があります。

- statusが`LIFECYCLE_BOUNDED_DECISION_REVIEW_CLEAR_FOR_AUTHORIZATION_DECISION`である。
- review recordが発行済みである。
- reviewが完了している。
- authorization decisionが次段階として要求されている。
- authorization decisionがまだ行われていない。
- operation approval、operation start、operation completionが行われていない。
- lifecycle effectとrepository changeが行われていない。
- source subject bindingとsource artifact bindingが一致する。
- v0.1からv0.11までの完全再計算結果が一致する。

record digestだけを信頼しません。

上流recordを変更してdigestを再計算した場合も、完全再計算との差によって検出します。

## Designated decision maker binding

v0.10はfuture authorization decision makerを指定します。

v0.11はその指定をreviewします。

v0.12では次のidentityが一致しなければなりません。

- v0.11 submissionのauthorization decision maker。
- v0.11 recordのauthorization decision maker。
- v0.12 evidenceのauthorization decision maker。
- v0.12 submissionのauthorization decision maker。

このbindingが一致しない入力はrejectedになります。

authorization decision makerは、subject、prior actor chain、bounded-request requester、v0.11 decision reviewer、future operatorから独立していなければなりません。

authorization decision makerとfuture operatorは同一主体であってはなりません。

## Authorization evidence

v0.12 evidenceは次をimmutable digestへ束縛します。

- authorization decision ID。
- authorization decision maker identityとorganization。
- mandate receipt。
- qualification receipt。
- independence declaration。
- conflict disclosure。
- jurisdiction receipt。
- quorum receipt。
- decision rationale。
- proportionality review。
- less restrictive alternatives review。
- irreversibility review。
- human impact review。
- subject identity、kind、version。
- v0.1からv0.11までのsource artifact digests。
- v0.11 decision reviewer identity。
- bounded-request requester identity。
- future operator identity。
- operation scopeとtarget resources。
- protected resources。
- reversible stepsとirreversible steps。
- rollback planとrecovery route。
- stop conditionsとabort channel。
- human oversightとmonitoring。
- evidence capture planとsimulation receipt。
- operation window。
- authorization decision requested time。
- evidence capture time。
- decision completion time。
- authorization decision expiry time。
- separate operation approval deadline。
- separate operation approval route。
- appeal route。
- dissent route。
- minority opinion。
- protected-core exclusion。
- institutional hold state。
- emergency state。

## Status

v0.12は次の三状態だけを返します。

```text
LIFECYCLE_BOUNDED_AUTHORIZATION_DECISION_APPROVED_FOR_SEPARATE_OPERATION_APPROVAL
LIFECYCLE_BOUNDED_AUTHORIZATION_DECISION_DENIED
LIFECYCLE_BOUNDED_AUTHORIZATION_DECISION_REJECTED
```

### Approved

approvedは有効なauthorization decisionです。

approved recordはauthorization decision recordが発行され、authorization decisionが行われ、別のoperation-approval層へ進めることを示します。

approvedはoperation approvalではありません。

approvedはoperation startまたはoperation completionではありません。

### Denied

source chainとbindingが有効でも、authorization条件が満たされない場合はdeniedになります。

deniedは有効なauthorization decisionとして記録されます。

deniedは別のoperation-approval層へ進みません。

主なdenial理由は次です。

- mandate未検証。
- qualification未検証。
- independence declaration欠落。
- conflict disclosure不完全。
- material conflict存在。
- jurisdiction未検証。
- quorum未成立。
- reasoned decision不完全。
- proportionality不成立。
- less restrictive alternatives未検討または未尽力。
- irreversibility review不完全。
- human impact review不完全。
- operation approval route欠落。
- package safety不成立。
- appeal route欠落。
- dissent route欠落。
- minority opinion未記録。
- protected core対象。
- institutional hold。
- emergency state。

### Rejected

source、policy、submission、evidence、identity、role separation、時間境界、またはimmutable bindingが構造的に不正な場合はrejectedになります。

rejected入力では有効なauthorization decision recordを発行しません。

## 段階限定の非実行境界

v0.12ではauthorization decisionを実際に行います。

ただし、operation approvalとoperation executionは後続の責務として分離します。

この分離はv0.12の段階境界であり、将来段階におけるoperation approval、operation execution、lifecycle effect、repository mutationの能力を禁止する恒久的な規範ではありません。

v0.12 artifactでは次をすべてfalseに固定します。

- operation approved。
- operation started。
- operation completed。
- authority changed。
- quiescence state changed。
- terminal state changed。
- terminal marker written。
- resource removed。
- external operation performed。
- repository changed。

```text
authorization decision approved
!= operation approval
!= operation start
!= lifecycle transition
!= repository mutation
```

## Validation

focused auditは20項目で構成します。

監査対象はvalid approval、non-clear source rejection、完全再計算、fresh-digest tamper、immutable binding、identity policy、designated decision maker binding、role separation、mandate、qualification、conflict、jurisdiction、quorum、reasoned decision、proportionality、alternatives、irreversibility、human impact、route、package safety、時間境界、段階限定の非実行境界、決定性、record integrityです。

Lean境界はapprovedがauthorization decisionであること、approvedが別のoperation-approval層だけへroutingすること、deniedが後続へ進まないこと、rejectedが有効なdecision recordを発行しないこと、v0.12の全状態がoperation effectとlifecycle effectを行わないこと、同一入力に対する決定性を固定します。

Lean成功は、現実のmandate、qualification、independence、jurisdiction、quorum、比例原則、倫理的妥当性、resource safety、rollback effectiveness、法的適合性、または将来のoperationの妥当性を証明しません。
