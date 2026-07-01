# KuuOS Apoptosis Candidate v0.2

## 位置づけ

KuuOS Apoptosis Candidate v0.2は、Apoptosis Observation v0.1の`REVIEW_RECOMMENDED`結果から、独立審査へ渡すcandidate artifactを構成する非実行層です。

candidateは終結判断ではありません。

candidateは実行権限ではありません。

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

## 入力

v0.2は次を入力として受け取ります。

- v0.1 observation policy。
- v0.1 observation input。
- v0.1 observation record。
- v0.2 candidate policy。
- v0.2 candidate request。

source observationは完全再計算されます。

record digestだけを信頼しません。

## Candidate policy

candidate policyは次を固定します。

- candidate artifact issuer allowlist。
- objective allowlist。
- observationからcandidate発行までの最大時間。
- source再計算の必須化。
- `REVIEW_RECOMMENDED` sourceの必須化。
- protected subjectの拒否。
- institutional holdの拒否。
- provenance binding。
- dependency snapshot binding。
- authority snapshot binding。
- independent dependency review。
- independent authority review。
- independent quiescence review。
- external review。
- independent authorization。

許可されるobjectiveは次の一つだけです。

```text
EVALUATE_FOR_GOVERNED_APOPTOSIS_ONLY
```

## Candidate request

requestは次をdigestで束縛します。

- candidate identity。
- issuer identity。
- objective。
- issuance time。
- source observation identity。
- source observation record digest。
- source observation input digest。
- source observation policy digest。
- subject identity、kind、version。
- provenance digest。
- dependency snapshot digest。
- authority snapshot digest。
- rationale digest。

rationale digestは、source observationが記録した劣化signalとactive surfaceから決定的に構成します。

## 受入条件

次をすべて満たす場合だけ`APOPTOSIS_CANDIDATE_PROPOSED`になります。

- candidate policyが有効である。
- candidate requestが有効である。
- source observationが完全再計算と一致する。
- source statusが`REVIEW_RECOMMENDED`である。
- sourceにdegradation signalがある。
- sourceがprotectedではない。
- institutional holdがない。
- subject bindingが一致する。
- provenance bindingが一致する。
- dependency bindingが一致する。
- authority bindingが一致する。
- rationale bindingが一致する。
- issuerがallowlistに含まれる。
- objectiveが限定目的と一致する。
- issuance delayがpolicy上限内である。

一つでも満たさない場合は`APOPTOSIS_CANDIDATE_REJECTED`になります。

## Candidate artifactの意味

proposed candidateは、対象が削除されるべきだと確定しません。

proposed candidateは、次の独立審査へ渡せる証拠束縛済みartifactであることだけを示します。

```text
candidate artifact issued
!= dependency review completed
!= authority review completed
!= quiescence approved
!= external approval
!= authorization decision
!= terminal transition
```

## 非権限境界

v0.2では、次が常にfalseです。

- authority revocation performed。
- quiescence transition performed。
- terminal transition performed。
- tombstone write performed。
- physical deletion performed。
- live Git execution performed。
- repository mutation performed。

candidate artifactの発行だけが許可されます。

これはrepository mutation authorityではありません。

## Protected subjectとhold

constitutional protected core、policy protected subject、institutional hold対象はcandidateへ昇格しません。

protected subjectの変更は通常のapoptosis系列ではなく、独立したconstitutional amendmentを必要とします。

## 決定性と改変検出

同一のsource、request、policyからは同一candidate recordを構成します。

candidate recordは完全再計算されます。

record本体を変更してdigestだけを更新した場合も、再計算不一致として拒否します。

## 形式境界

Lean moduleは次を固定します。

- proposed candidateが独立reviewを要求すること。
- candidate artifactの発行がterminal transitionではないこと。
- proposed candidateがlifecycle effectを実行しないこと。
- valid candidateがlive Git executionとrepository mutationを行わないこと。
- 同一入力に対する決定性。

Lean成功は、対象の終結必要性、医学的・制度的妥当性、法的削除権限、live executionの安全性を証明しません。

## Validation

```bash
PYTHONPATH=. python3 -m unittest -v \
  tests.test_kuuos_apoptosis_candidate_v0_2

PYTHONPATH=. python3 \
  runtime/kuuos_apoptosis_candidate_check_v0_2.py

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  env lean formal/KuuOSApoptosisCandidateV0_2.lean
```
