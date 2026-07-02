# KuuOS Apoptosis Authority Review v0.4

## 位置づけ

KuuOS Apoptosis Authority Review v0.4は、Apoptosis Dependency Review v0.3が`CLEAR_FOR_FURTHER_REVIEW`とした候補について、権限構造の安全性を独立に再検証するread-only審査層です。

この層はauthority revocationを実行しません。

この層はquiescence、terminal transition、削除、Git操作を実行しません。

```text
apoptosis observation
→ apoptosis candidate
→ dependency review
→ authority review
→ quiescence review
→ external review
→ independent authorization
```

## Source review

v0.4は次を完全再計算します。

- v0.1 observation chain。
- v0.2 candidate chain。
- v0.3 dependency evidence、policy、request、record。

source dependency reviewは`APOPTOSIS_DEPENDENCY_REVIEW_CLEAR_FOR_FURTHER_REVIEW`でなければなりません。

record digestだけを信頼しません。

## Authority evidence

authority evidenceは次をdigestへ束縛します。

- subject identity、kind、version。
- candidateが束縛したauthority snapshot digest。
- authority graph snapshot digest。
- responsible authority identifier。
- active authority identifiers。
- 順序を保持したdelegation chain identifiers。
- protected authority identifiers。
- unresolved authority identifiers。
- authority cycle member identifiers。
- authority closure completeness。
- delegation chain completeness。
- responsibility acknowledgement。
- subject control of responsible authority。
- institutional hold。
- constitutional protection。
- emergency override。

## Status

v0.4は次の三状態だけを返します。

```text
APOPTOSIS_AUTHORITY_REVIEW_CLEAR_FOR_QUIESCENCE_REVIEW
APOPTOSIS_AUTHORITY_REVIEW_BLOCKED
APOPTOSIS_AUTHORITY_REVIEW_REJECTED
```

`CLEAR_FOR_QUIESCENCE_REVIEW`はauthority revocationまたは終結許可ではありません。

quiescence reviewへ進めることだけを示します。

## Clear条件

次をすべて満たす場合だけclearになります。

- source dependency reviewが完全再計算と一致する。
- source dependency reviewがclearである。
- subjectとauthority snapshotのbindingが一致する。
- reviewerがallowlistに含まれる。
- reviewerがsubject、candidate issuer、dependency reviewer、responsible authorityから独立している。
- objectiveが`ASSESS_AUTHORITY_SAFETY_ONLY`である。
- reviewとevidenceが時間境界内である。
- authority closureがcompleteである。
- responsible authorityがactive authorityとして存在する。
- responsible authorityが責任を受諾している。
- delegation chainがcompleteである。
- subjectがresponsible authorityを支配していない。
- institutional holdがない。
- constitutional protectionがない。
- protected authorityが関与していない。
- unresolved authorityがない。
- authority cycleがない。
- emergency overrideがactiveではない。

## Blocked条件

sourceと証拠が有効でも、権限安全性を満たさない場合は`BLOCKED`になります。

主なblockerは次です。

- institutional hold。
- constitutional protection。
- authority closure不完備。
- responsible authority不在。
- responsibility未受諾。
- subjectによるresponsible authority支配。
- delegation chain不完備。
- protected authorityの関与。
- unresolved authority。
- authority cycle。
- emergency override。

blocked recordは監査のため発行されますが、後続reviewへ進みません。

## Rejected条件

次の場合は`REJECTED`になります。

- source dependency reviewが不正または改変されている。
- source dependency reviewがclearではない。
- policy、request、evidenceが不正である。
- reviewerが未許可または非独立である。
- objectiveが許可されていない。
- reviewまたはevidenceが時間境界を超えている。
- subject、snapshot、source artifactのbindingが一致しない。

## 非権限境界

v0.4では次が常にfalseです。

- authority revocation performed。
- quiescence transition performed。
- terminal transition performed。
- tombstone write performed。
- physical deletion performed。
- live Git execution performed。
- repository mutation performed。

```text
authority review clear
!= authority revocation
!= quiescence approval
!= terminal authorization
!= deletion authority
```

## 形式境界

Lean moduleは次を固定します。

- clear reviewでreviewerがallowedかつindependentであること。
- clear reviewがquiescence、external review、independent authorizationを要求すること。
- blocked reviewが後続段階へ進まないこと。
- valid reviewがlifecycle effectとrepository mutationを実行しないこと。
- 同一入力に対する決定性。

Lean成功は、現実のauthority graphの完全性、責任主体の制度的正当性、対象を終結すべきこと、権限失効の許可を証明しません。

## Validation

```bash
PYTHONPATH=. python3 -m unittest -v \
  tests.test_kuuos_apoptosis_authority_review_v0_4

PYTHONPATH=. python3 \
  runtime/kuuos_apoptosis_authority_review_check_v0_4.py

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  env lean formal/KuuOSApoptosisAuthorityReviewV0_4.lean
```
