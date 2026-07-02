# KuuOS Apoptosis Dependency Review v0.3

## 位置づけ

KuuOS Apoptosis Dependency Review v0.3は、Apoptosis Candidate v0.2が発行した候補について、依存関係の安全性を独立に再検証するread-only審査層です。

この層は終結判断を行いません。

この層はquiescence、authority revocation、terminal transition、削除を実行しません。

```text
apoptosis observation
→ apoptosis candidate
→ dependency review
→ authority review
→ quiescence review
→ external review
→ bounded authorization request
→ explicit authorization decision
```

## Source candidate

v0.3は次を再計算します。

- v0.1 observation policy。
- v0.1 observation input。
- v0.1 observation record。
- v0.2 candidate policy。
- v0.2 candidate request。
- v0.2 candidate record。

source candidateは`APOPTOSIS_CANDIDATE_PROPOSED`でなければなりません。

candidate digestだけを信頼しません。

## Dependency evidence

dependency evidenceは次を正規化してdigestへ束縛します。

- subject identity、kind、version。
- evidence capture time。
- candidateが束縛したdependency snapshot digest。
- dependency graph snapshot digest。
- direct dependency identifiers。
- direct dependent identifiers。
- critical dependent identifiers。
- replacement-covered dependent identifiers。
- unresolved dependency identifiers。
- cycle member identifiers。
- active-execution dependent identifiers。
- dependency closure completeness。

critical dependent、replacement-covered dependent、active-execution dependentはdirect dependentの部分集合でなければなりません。

unresolved dependencyはdirect dependencyの部分集合でなければなりません。

## Status

v0.3は次の三状態だけを返します。

```text
APOPTOSIS_DEPENDENCY_REVIEW_CLEAR_FOR_FURTHER_REVIEW
APOPTOSIS_DEPENDENCY_REVIEW_BLOCKED
APOPTOSIS_DEPENDENCY_REVIEW_REJECTED
```

`CLEAR_FOR_FURTHER_REVIEW`は終結許可ではありません。

後続のauthority review、quiescence review、external review、independent authorizationへ進めることだけを示します。

## Clear条件

次をすべて満たす場合だけ`CLEAR_FOR_FURTHER_REVIEW`になります。

- review policyが有効である。
- review requestが有効である。
- source candidateが完全再計算と一致する。
- source candidateがproposedである。
- subject bindingが一致する。
- candidate、request、policy bindingが一致する。
- dependency snapshot bindingが一致する。
- reviewerがallowlistに含まれる。
- objectiveが`ASSESS_DEPENDENCY_SAFETY_ONLY`である。
- review delayが上限内である。
- evidenceが有効かつfreshである。
- evidence subject bindingが一致する。
- dependency closureがcompleteである。
- 対象を通るdependency cycleがない。
- unresolved dependencyがない。
- orphaned dependentがない。
- uncovered critical dependentがない。
- active execution dependenceがない。
- すべてのdirect dependentがreplacement-coveredである。

## Blocked条件

source、request、policy、evidenceが有効でも、依存安全性を満たさない場合は`BLOCKED`になります。

主なblockerは次です。

- dependency closureが不完全である。
- 対象を通る循環がある。
- 未解決のdirect dependencyがある。
- replacementされないdependentが残る。
- critical dependentがreplacement-coveredではない。
- active executionが対象へ依存している。

`BLOCKED` recordは監査のため発行されますが、後続reviewへ進みません。

## Rejected条件

次の場合は`REJECTED`になります。

- source candidateが不正または改変されている。
- candidateがproposedではない。
- requestまたはpolicyが不正である。
- reviewerまたはobjectiveが許可されていない。
- reviewまたはevidenceが時間境界を超えている。
- subject、snapshot、candidate、evidence bindingが一致しない。
- evidence構造が不正である。

rejected inputからdependency review recordは発行しません。

## 非権限境界

v0.3では次が常にfalseです。

- authority revocation performed。
- quiescence transition performed。
- terminal transition performed。
- tombstone write performed。
- physical deletion performed。
- live Git execution performed。
- repository mutation performed。

`CLEAR_FOR_FURTHER_REVIEW`も実行権限ではありません。

## 形式境界

Lean moduleは次を固定します。

- clear reviewが後続reviewとindependent authorizationを要求すること。
- clear reviewがlifecycle effectを実行しないこと。
- blocked reviewが後続段階へ進まないこと。
- valid reviewがlive Git executionとrepository mutationを行わないこと。
- 同一入力に対する決定性。

Lean成功は、依存graph evidenceの現実世界での完全性、対象の終結必要性、制度的妥当性、削除権限を証明しません。

## Validation

```bash
PYTHONPATH=. python3 -m unittest -v \
  tests.test_kuuos_apoptosis_dependency_review_v0_3

PYTHONPATH=. python3 \
  runtime/kuuos_apoptosis_dependency_review_check_v0_3.py

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  env lean formal/KuuOSApoptosisDependencyReviewV0_3.lean
```
