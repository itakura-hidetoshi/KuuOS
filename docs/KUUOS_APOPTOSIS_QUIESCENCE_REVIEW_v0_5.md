# KuuOS Apoptosis Quiescence Review v0.5

## 位置づけ

KuuOS Apoptosis Quiescence Review v0.5は、Apoptosis Authority Review v0.4が`CLEAR_FOR_QUIESCENCE_REVIEW`とした候補について、停止準備の安全性を独立に再検証するread-only審査層です。

この層はquiescence transitionを実行しません。

この層はauthority revocation、terminal transition、削除、Git操作を実行しません。

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

v0.5は次を完全再計算します。

- v0.1 observation chain。
- v0.2 candidate chain。
- v0.3 dependency review chain。
- v0.4 authority evidence、policy、request、record。

source authority reviewは`APOPTOSIS_AUTHORITY_REVIEW_CLEAR_FOR_QUIESCENCE_REVIEW`でなければなりません。

record digestだけを信頼しません。

## Quiescence evidence

quiescence evidenceは次をdigestへ束縛します。

- subject identity、kind、version。
- execution snapshot digest。
- work snapshot digest。
- intake snapshot digest。
- state checkpoint digest。
- drain plan digest。
- recovery route digest。
- active execution identifiers。
- pending work identifiers。
- critical pending work identifiers。
- active lease identifiers。
- intake channel identifiers。
- open intake channel identifiers。
- blocking external dependency identifiers。
- quiescence closure completeness。
- new intake stopped。
- drain verified。
- checkpoint verified。
- recovery route verified。
- reentry possible。
- quiescence start time。
- last activity time。
- evidence capture time。
- emergency operation active。

critical pending workはpending workの部分集合でなければなりません。

open intake channelはdeclared intake channelの部分集合でなければなりません。

## Status

v0.5は次の三状態だけを返します。

```text
APOPTOSIS_QUIESCENCE_REVIEW_CLEAR_FOR_EXTERNAL_REVIEW
APOPTOSIS_QUIESCENCE_REVIEW_BLOCKED
APOPTOSIS_QUIESCENCE_REVIEW_REJECTED
```

`CLEAR_FOR_EXTERNAL_REVIEW`はquiescence transitionまたは終結許可ではありません。

外部審査へ進めることだけを示します。

## Clear条件

次をすべて満たす場合だけclearになります。

- source authority reviewが完全再計算と一致する。
- source authority reviewがclearである。
- subjectとexecution snapshotのbindingが一致する。
- reviewerがallowlistに含まれる。
- reviewerがsubject、candidate issuer、dependency reviewer、authority reviewer、responsible authorityから独立している。
- objectiveが`ASSESS_QUIESCENCE_SAFETY_ONLY`である。
- reviewとevidenceが時間境界内である。
- quiescence closureがcompleteである。
- active executionがない。
- pending workがない。
- critical pending workがない。
- active leaseがない。
- new intakeが停止している。
- open intake channelがない。
- blocking external dependencyがない。
- drainが検証済みである。
- state checkpointが検証済みである。
- recovery routeが検証済みである。
- reentry可能性が保持されている。
- authority review、last activity、quiescence start、evidence capture、reviewの時系列が有効である。
- minimum grace periodが経過している。
- emergency operationがactiveではない。

## Blocked条件

sourceと証拠が有効でも、停止準備の安全性を満たさない場合は`BLOCKED`になります。

主なblockerは次です。

- emergency operation。
- quiescence closure不完備。
- active execution。
- critical pending work。
- pending work。
- active lease。
- new intake継続。
- open intake channel。
- blocking external dependency。
- drain未検証。
- checkpoint未検証。
- recovery route未検証。
- reentry不能。
- quiescence時系列不整合。
- grace period不足。

blocked recordは監査のため発行されますが、後続reviewへ進みません。

## Rejected条件

次の場合は`REJECTED`になります。

- source authority reviewが不正または改変されている。
- source authority reviewがclearではない。
- policy、request、evidenceが不正である。
- reviewerが未許可または非独立である。
- objectiveが許可されていない。
- reviewまたはevidenceが時間境界を超えている。
- subject、snapshot、source artifactのbindingが一致しない。

## 復帰可能性

v0.5はquiescenceを不可逆な終結として扱いません。

clearには次を必要とします。

- verified state checkpoint。
- verified recovery route。
- reentry possible。

この条件はquiescence reviewとterminal decisionを分離します。

```text
quiescence-ready
!= terminal
!= deleted
!= unrecoverable
```

## 非権限境界

v0.5では次が常にfalseです。

- authority revocation performed。
- quiescence transition performed。
- terminal transition performed。
- tombstone write performed。
- physical deletion performed。
- live Git execution performed。
- repository mutation performed。

```text
quiescence review clear
!= quiescence transition
!= terminal authorization
!= deletion authority
```

## 形式境界

Lean moduleは次を固定します。

- clear reviewがexternal reviewとindependent authorizationを要求すること。
- clear reviewがcheckpoint、recovery route、reentry可能性を保持すること。
- blocked reviewが後続段階へ進まないこと。
- valid reviewがlifecycle effectとrepository mutationを実行しないこと。
- 同一入力に対する決定性。

Lean成功は、現実のexecution snapshotの完全性、grace periodの制度的十分性、対象を終結すべきこと、quiescence transitionの許可を証明しません。

## Validation

```bash
PYTHONPATH=. python3 -m unittest -v \
  tests.test_kuuos_apoptosis_quiescence_review_v0_5

PYTHONPATH=. python3 \
  runtime/kuuos_apoptosis_quiescence_review_check_v0_5.py

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  env lean formal/KuuOSApoptosisQuiescenceReviewV0_5.lean
```
