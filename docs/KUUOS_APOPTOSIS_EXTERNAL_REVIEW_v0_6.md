# KuuOS Apoptosis External Review v0.6

## 位置づけ

KuuOS Apoptosis External Review v0.6は、Apoptosis Quiescence Review v0.5が`CLEAR_FOR_EXTERNAL_REVIEW`とした対象について、組織外部または既存意思決定系列から独立した審査者が、後続の独立authorizationへ進める条件だけを再検証するread-only審査層です。

この層はauthorization requestを発行しません。

この層はauthorization decisionを行いません。

この層はauthority revocation、quiescence transition、terminal transition、削除、Git操作、repository mutationを実行しません。

```text
apoptosis observation
→ apoptosis candidate
→ dependency review
→ authority review
→ quiescence review
→ external review
→ independent authorization
```

v0.6はrepository mutation roadmapのv1.25ではありません。

## Source review

v0.6はv0.1からv0.5までの全artifactを完全再計算します。

対象は次のartifactです。

- v0.1 observation input、policy、record。
- v0.2 candidate request、policy、record。
- v0.3 dependency evidence、request、policy、record。
- v0.4 authority evidence、request、policy、record。
- v0.5 quiescence evidence、request、policy、record。

source quiescence reviewは`APOPTOSIS_QUIESCENCE_REVIEW_CLEAR_FOR_EXTERNAL_REVIEW`でなければなりません。

`BLOCKED`または`REJECTED`のsourceは受理しません。

record digestだけを信頼しません。

上流recordの内容を変更してdigestを再計算した場合も、完全再計算との差によって検出します。

## External review evidence

external review evidenceは次をimmutable digestへ束縛します。

- external review ID。
- external reviewer identity。
- external reviewer organization。
- quiescence evidence producer identity。
- reviewer qualification receipt digest。
- reviewer independence declaration digest。
- conflict-of-interest disclosure digest。
- institutional affiliation digest。
- review scope。
- review methodology digest。
- review evidence receipt digest。
- subject identity、kind、version。
- source quiescence review ID。
- v0.1からv0.5までのsource artifact digests。
- review requested time。
- evidence capture time。
- review completion time。
- review expiry time。
- appeal route digest。
- dissent route digest。
- minority opinion receipt digest。
- protected-core exclusion。
- institutional hold state。
- emergency state。

## Reviewer independence

external reviewerは少なくとも次から独立していなければなりません。

- subject。
- candidate issuer。
- dependency reviewer。
- authority reviewer。
- responsible authority。
- quiescence reviewer。
- quiescence evidence producer。
- future authorization authority。
- future execution authority。

同一主体がexternal reviewと後続authorizationを兼務する入力は拒否します。

同一主体がexternal reviewと後続executionを兼務する入力も拒否します。

## Status

v0.6は次の三状態だけを返します。

```text
APOPTOSIS_EXTERNAL_REVIEW_CLEAR_FOR_INDEPENDENT_AUTHORIZATION
APOPTOSIS_EXTERNAL_REVIEW_BLOCKED
APOPTOSIS_EXTERNAL_REVIEW_REJECTED
```

`CLEAR_FOR_INDEPENDENT_AUTHORIZATION`はauthorizationではありません。

後続の独立authorizationへ進めることだけを示します。

## Clear条件

次をすべて満たす場合だけclearになります。

- source quiescence reviewが完全再計算と一致する。
- source quiescence reviewがclearである。
- subject bindingが一致する。
- v0.1からv0.5までのsource artifact bindingが一致する。
- reviewerとreviewer organizationがallowlistに含まれる。
- reviewer identityとevidence identityが一致する。
- reviewer qualificationが検証済みである。
- reviewer independence declarationが存在する。
- reviewerが既存系列とfuture authoritiesから独立している。
- objectiveが`ASSESS_EXTERNAL_REVIEW_ONLY`である。
- review delayが上限内である。
- evidenceがfreshである。
- review time orderが有効である。
- reviewが期限切れではない。
- conflict-of-interest disclosureが完全である。
- material conflictがない。
- review scopeが完全である。
- review methodologyが存在する。
- evidence receiptが完全である。
- appeal routeが存在する。
- dissent routeが存在する。
- protected coreが対象から除外されている。
- institutional holdがactiveではない。
- emergency stateがactiveではない。

## Blocked条件

source、policy、request、evidenceが有効でも、外部審査の制度的条件が未完了の場合は`BLOCKED`になります。

主なblockerは次です。

- reviewer qualification未検証。
- reviewer independence declaration欠落。
- conflict disclosure不完全。
- material conflict存在。
- review scope不完全。
- review methodology欠落。
- review evidence receipt不完全。
- appeal route欠落。
- dissent route欠落。
- protected core対象。
- institutional hold。
- emergency state。

blocked recordは監査用に発行します。

blocked recordは独立authorizationへ進みません。

## Rejected条件

次の場合は`REJECTED`になります。

- source quiescence reviewが不正または改変されている。
- source quiescence reviewがclearではない。
- policy、request、evidenceが不正である。
- subject bindingが一致しない。
- source artifact bindingが一致しない。
- reviewerが未許可である。
- reviewer organizationが未許可である。
- reviewer identity bindingが一致しない。
- reviewerが既存系列から独立していない。
- reviewerがfuture authorization authorityと同一である。
- reviewerがfuture execution authorityと同一である。
- objectiveが未許可である。
- review delayが上限を超えている。
- evidenceがstaleである。
- review time orderが不正である。
- reviewが期限切れである。

rejected recordでは有効なexternal review recordを発行しません。

## 非権限境界

v0.6では次が常にfalseです。

- authorization request issued。
- authorization decision made。
- authority revocation performed。
- quiescence transition performed。
- terminal transition performed。
- tombstone write performed。
- physical deletion performed。
- live Git execution performed。
- repository mutation performed。

```text
external review clear
!= authorization request
!= authorization decision
!= execution
```

## 形式境界

Lean moduleは次を固定します。

- clear external reviewがindependent authorizationを要求すること。
- clear external review自体はauthorization requestを発行しないこと。
- clear external review自体はauthorization decisionを行わないこと。
- external reviewerが既存reviewer、authorization authority、execution authorityから独立すること。
- blocked external reviewが後続段階へ進まないこと。
- rejected external reviewが有効recordを発行しないこと。
- valid external reviewがlifecycle effectとrepository mutationを実行しないこと。
- 同一入力に対する決定性。

Lean成功は、現実のreviewer資格、組織的独立性、利益相反開示の完全性、対象を終結すべきこと、authorizationの妥当性を証明しません。

## Validation

```bash
PYTHONPATH=. python3 -m unittest -v \
  tests.test_kuuos_apoptosis_external_review_v0_6

PYTHONPATH=. python3 \
  runtime/kuuos_apoptosis_external_review_check_v0_6.py

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  env lean formal/KuuOSApoptosisExternalReviewV0_6.lean
```
