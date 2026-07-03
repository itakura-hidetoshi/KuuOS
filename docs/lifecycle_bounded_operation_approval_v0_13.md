# KuuOS Lifecycle Bounded Operation Approval v0.13

## 位置づけ

KuuOS Lifecycle Bounded Operation Approval v0.13は、独立したApoptosis Lifecycle Governance系列に属します。

この段階はrepository mutation roadmap v1.25ではありません。

v0.13は、v0.12が`LIFECYCLE_BOUNDED_AUTHORIZATION_DECISION_APPROVED_FOR_SEPARATE_OPERATION_APPROVAL`とした限定的なoperation packageについて、独立したoperation approverが実際のoperation approvalを記録する層です。

```text
lifecycle bounded authorization decision
→ lifecycle bounded operation approval
→ separate operation start
```

## Source authorization

v0.13はv0.1からv0.12までのsource chainを完全再計算します。

source authorization decisionは次をすべて満たす必要があります。

- authorization decision recordが発行済みである。
- authorization decisionが完了している。
- authorizationがapprovedである。
- separate operation approvalが次段階として要求されている。
- operation approval routeが束縛されている。
- operation approval、operation start、operation completionはまだ行われていない。
- lifecycle effectとrepository changeは行われていない。
- source artifactの完全再計算結果が一致する。

digestを再計算しただけのsource改変は、完全再計算との差によってrejectedになります。

## Operation approver

operation approverはpolicyで許可されたidentityとorganizationに属し、少なくとも次の主体から分離されます。

- subject。
- prior actor chain。
- bounded-request requester。
- v0.11 decision reviewer。
- v0.12 authorization decision maker。
- future operator。

operation approverとfuture operatorは同一主体ではありません。

## Approval evidence

v0.13 evidenceは次をimmutable digestへ束縛します。

- operation approval ID。
- operation approver identityとorganization。
- mandate、qualification、independence、conflict、jurisdiction、quorum。
- approval rationaleとproportionality review。
- v0.1からv0.12までのsource artifact digests。
- source authorization decision、requester、reviewer、future operator。
- operation approval route。
- approved scope、target resources、protected resources。
- reversible stepsとirreversible steps。
- execution package integrity。
- operator acknowledgement。
- resource reservation。
- rollback、recovery、stop conditions、abort channel。
- human oversight、monitoring、evidence capture、simulation。
- operation window。
- approval request、capture、completion、expiry。
- operation start windowとdeadline。
- protected-core exclusion、institutional hold、emergency state。
- appeal、dissent、minority opinion。

## Status

v0.13は次の三状態だけを返します。

```text
LIFECYCLE_BOUNDED_OPERATION_APPROVAL_APPROVED_FOR_SEPARATE_OPERATION_START
LIFECYCLE_BOUNDED_OPERATION_APPROVAL_DENIED
LIFECYCLE_BOUNDED_OPERATION_APPROVAL_REJECTED
```

### Approved

approvedは有効なoperation approvalです。

approved artifactでは次がtrueになります。

- operation approval record issued。
- operation approval made。
- operation approved。
- separate operation start required next。
- operation start route required next。

approvedはoperation startではありません。

### Denied

source chainとbindingが有効でも、approval条件が満たされない場合はdeniedになります。

deniedは有効なoperation-approval decisionとして記録されますが、operation startへ進みません。

### Rejected

source、policy、submission、evidence、identity、role separation、時間境界、route binding、scope bindingが構造的に不正な場合はrejectedになります。

rejected入力では有効なoperation approval recordを発行しません。

## 段階限定の実行境界

v0.13は実際にoperationをapproveします。

ただし、operation startとそれ以後のeffectは後続段階へ分離します。

この分離はv0.13の責務境界であり、将来のoperation start、operation completion、lifecycle effect、repository mutationを禁止する恒久的規範ではありません。

v0.13 artifactではoperation approvedだけがtrueとなり、次はfalseです。

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
operation approved
!= operation started
!= operation completed
!= lifecycle transition
!= repository mutation
```

## Validation

focused auditはvalid approval、source recomputation、fresh-digest tamper、immutable binding、route binding、identity policy、role separation、mandate、qualification、conflict、jurisdiction、quorum、reasoned approval、proportionality、operator acknowledgement、execution package、resource reservation、scope、rollback、monitoring、時間境界、決定性、record integrityを検証します。

Lean境界はapprovedが実際のoperation approvalであること、approvedが別のoperation-start層だけへroutingすること、deniedが後続へ進まないこと、rejectedが有効なapproval recordを発行しないこと、v0.13がoperation executionまたはlifecycle effectを行わないこと、同一入力に対する決定性を固定します。

Lean成功は、現実のmandate、qualification、independence、jurisdiction、quorum、resource safety、rollback effectiveness、法的適合性、または将来のoperation executionの妥当性を証明しません。
