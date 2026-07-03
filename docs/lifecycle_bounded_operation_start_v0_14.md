# KuuOS Lifecycle Bounded Operation Start v0.14

## 位置づけ

KuuOS Lifecycle Bounded Operation Start v0.14は、独立したApoptosis Lifecycle Governance系列に属します。

この段階はrepository mutation roadmap v1.25ではありません。

v0.14は、v0.13が`LIFECYCLE_BOUNDED_OPERATION_APPROVAL_APPROVED_FOR_SEPARATE_OPERATION_START`とした限定的なoperationについて、承認時に指定されたfuture operatorが実際のoperation startを記録する層です。

```text
lifecycle bounded operation approval
→ lifecycle bounded operation start
→ separate operation completion
```

## Source approval

v0.14はv0.1からv0.13までのsource chainを完全再計算します。

source operation approvalは次をすべて満たす必要があります。

- operation approval recordが発行済みである。
- operation approval decisionが完了している。
- operationがapprovedである。
- separate operation startが次段階として要求されている。
- operation start routeが要求されている。
- operation startとoperation completionはまだ行われていない。
- lifecycle effect、external operation、repository changeは行われていない。
- source artifactの完全再計算結果が一致する。

record digestだけを更新したsource改変は、完全再計算との差によってrejectedになります。

## Immutable start binding

v0.14は次をoperation start evidenceへimmutableに束縛します。

- v0.13 operation approval IDとrecord digest。
- v0.1からv0.13までのsource artifact digests。
- operation approver、authorization decision maker、decision reviewer、requester。
- subject identity、kind、version。
- approved future operator identity。
- approved scope、target resources、protected resources。
- reversible stepsとirreversible steps。
- execution package、resource reservation、rollback、recovery。
- stop conditions、abort channel、human oversight、monitoring、evidence capture。
- operation start window、deadline、operation window。

operation start route digestは、source approval record、approved future operator、approval route、approved scope、start deadlineから決定的に導出します。

## Operator

operatorはv0.13で指定されたfuture operatorと一致する必要があります。

operatorは少なくとも次の主体から分離されます。

- subject。
- bounded-request requester。
- v0.11 decision reviewer。
- v0.12 authorization decision maker。
- v0.13 operation approver。

v0.14はoperator mandate、qualification、identity confirmation、conflict disclosure、jurisdiction、readinessを再確認します。

## Start-time revalidation

operation approval後に状態が変化し得るため、v0.14は開始直前に次を再確認します。

- execution package integrity。
- resource reservation。
- rollback readiness。
- recovery readiness。
- stop conditions。
- abort channel。
- human oversight。
- monitoring。
- evidence capture。
- protected-core exclusion。
- institutional holdの不存在。
- emergency stateの不存在。

承認済みscopeの変更、irreversible stepの追加、start window外の開始、期限切れapprovalの利用はstructural rejectionになります。

## Status

v0.14は次の三状態だけを返します。

```text
LIFECYCLE_BOUNDED_OPERATION_START_STARTED_FOR_SEPARATE_OPERATION_COMPLETION
LIFECYCLE_BOUNDED_OPERATION_START_DENIED
LIFECYCLE_BOUNDED_OPERATION_START_REJECTED
```

### Started

startedは有効なoperation startです。

started artifactでは次がtrueになります。

- operation start record issued。
- operation start decision made。
- operation started。
- separate operation completion required next。
- operation completion route required next。

startedはoperation completionではありません。

### Denied

source chainとbindingが有効でも、開始直前のauthority、readiness、安全性、監視条件が満たされない場合はdeniedになります。

deniedは有効なstart decisionとして記録されますが、operationは開始しません。

### Rejected

source、policy、submission、evidence、identity、role separation、時間境界、route binding、scope bindingが構造的に不正な場合はrejectedになります。

rejected入力では有効なoperation start recordを発行しません。

## 段階限定の実行境界

v0.14は実際にoperation startを行い、`operation_started = true`を記録します。

ただし、この段階で許可するeffectはgovernance上のstart transitionに限定します。

次は後続段階へ分離します。

- operation completion。
- authority change。
- quiescence state change。
- terminal state change。
- terminal marker write。
- resource removal。
- external operation。
- repository mutation。

この分離はv0.14の責務境界であり、将来のcompletion、lifecycle transition、external operation、repository mutationを禁止する恒久的規範ではありません。

```text
operation approved
!= operation started
!= operation completed
!= lifecycle transition
!= repository mutation
```

## Validation

focused auditはvalid start、source recomputation、fresh-digest tamper、immutable binding、route binding、operator identity、approver-operator separation、mandate、qualification、conflict、jurisdiction、readiness、execution package、resource reservation、scope、rollback、monitoring、時間境界、決定性、record integrityを検証します。

Lean境界はstartedが実際のoperation startであること、startedが別のoperation-completion層だけへroutingすること、deniedがoperationを開始しないこと、rejectedが有効なstart recordを発行しないこと、v0.14がoperation completionまたはlifecycle effectを行わないこと、同一入力に対する決定性を固定します。

Lean成功は、現実のoperator mandate、qualification、jurisdiction、resource safety、rollback effectiveness、法的適合性、または将来のoperation completionの妥当性を証明しません。
