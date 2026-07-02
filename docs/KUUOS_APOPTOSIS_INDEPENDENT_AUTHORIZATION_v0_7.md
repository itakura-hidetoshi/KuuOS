# KuuOS Apoptosis Independent Authorization v0.7

## 位置づけ

KuuOS Apoptosis Independent Authorization v0.7は、Apoptosis External Review v0.6が`CLEAR_FOR_INDEPENDENT_AUTHORIZATION`とした対象について、v0.6で事前指定された独立authorityが、後続のbounded execution preparationへ進めるかを決定するauthorization層です。

この層はauthorization decisionを記録します。

この層はexecution requestを発行しません。

この層はexecution decision、authority revocation、quiescence transition、terminal transition、削除、Git操作、repository mutationを実行しません。

```text
apoptosis observation
→ apoptosis candidate
→ dependency review
→ authority review
→ quiescence review
→ external review
→ independent authorization
→ bounded execution preparation
```

v0.7はrepository mutation roadmapのv1.25ではありません。

## Source review

v0.7はv0.1からv0.6までの全artifactを完全再計算します。

source external reviewは次をすべて満たす必要があります。

- statusが`APOPTOSIS_EXTERNAL_REVIEW_CLEAR_FOR_INDEPENDENT_AUTHORIZATION`である。
- external review recordが発行済みである。
- independent authorizationが次段階として要求されている。
- v0.1からv0.6までのsource artifact bindingが一致する。
- source subject bindingが一致する。
- external review recordの完全再計算結果が一致する。

record digestだけを信頼しません。

上流recordを変更してdigestを再計算した場合も、完全再計算との差によって検出します。

## Designated authority binding

v0.6のexternal review requestはfuture authorization authorityを指定します。

v0.7では次の三者が同一でなければなりません。

- v0.6 recordのfuture authorization authority。
- v0.7 requestのauthority ID。
- v0.7 evidenceのauthorization authority ID。

このbindingが一致しない入力は拒否します。

## Authorization evidence

v0.7 evidenceは次をimmutable digestへ束縛します。

- authorization ID。
- authorization authority identity。
- authorization authority organization。
- external reviewer identity。
- authority mandate receipt。
- authority qualification receipt。
- authority independence declaration。
- conflict-of-interest disclosure。
- jurisdiction receipt。
- quorum receipt。
- decision rationale。
- proportionality review。
- less restrictive alternatives review。
- irreversibility review。
- human impact review。
- subject identity、kind、version。
- v0.1からv0.6までのsource artifact digests。
- authorization requested time。
- evidence capture time。
- authorization completion time。
- authorization expiry time。
- appeal route。
- dissent route。
- minority opinion receipt。
- protected-core exclusion。
- institutional hold state。
- emergency state。

## Authority independence

independent authorization authorityは少なくとも次から独立していなければなりません。

- subject。
- candidate issuer。
- dependency reviewer。
- authority reviewer。
- responsible authority。
- quiescence reviewer。
- quiescence evidence producer。
- external reviewer。
- future execution authority。

同一主体がexternal reviewとauthorizationを兼務する入力は拒否します。

同一主体がauthorizationとfuture executionを兼務する入力も拒否します。

## Status

v0.7は次の三状態だけを返します。

```text
APOPTOSIS_INDEPENDENT_AUTHORIZATION_APPROVED_FOR_BOUNDED_EXECUTION_PREPARATION
APOPTOSIS_INDEPENDENT_AUTHORIZATION_DENIED
APOPTOSIS_INDEPENDENT_AUTHORIZATION_REJECTED
```

### Approved

承認はauthorization decisionです。

承認recordは次を示します。

- authorization recordが発行された。
- authorization decisionが行われた。
- bounded execution preparationへ進める。
- 別主体のexecution authorityが次段階に必要である。

承認はexecution requestではありません。

承認はexecution decisionではありません。

### Denied

入力とsource chainが有効でも、authorization条件が満たされない場合はdenyになります。

主なdeny理由は次です。

- authority mandate未検証。
- authority qualification未検証。
- authority independence declaration欠落。
- conflict disclosure不完全。
- material conflict存在。
- jurisdiction未検証。
- quorum未成立。
- reasoned decision不完全。
- proportionality不成立。
- less restrictive alternatives未検討または未尽力。
- irreversibility review不完全。
- human impact review不完全。
- appeal route欠落。
- dissent route欠落。
- protected core対象。
- institutional hold。
- emergency state。

否認recordはauthorization decisionとして発行されます。

否認recordは後続段階へ進みません。

### Rejected

次の場合はrejectedになります。

- source external reviewが不正、改変、blocked、rejectedである。
- policy、request、evidenceが構造的に不正である。
- subject bindingが一致しない。
- source artifact bindingが一致しない。
- v0.6で指定されたauthorityと一致しない。
- authorityまたはauthority organizationが未許可である。
- authority identity bindingが一致しない。
- authorityが既存review chainから独立していない。
- authorityがfuture execution authorityと同一である。
- objectiveが未許可である。
- authorization delayが上限を超える。
- evidenceがstaleである。
- authorization time orderが不正である。
- authorizationが期限切れである。

rejected入力では有効なauthorization decisionを発行しません。

## 非実行境界

v0.7では次が常にfalseです。

- execution request issued。
- execution decision made。
- authority revocation performed。
- quiescence transition performed。
- terminal transition performed。
- tombstone write performed。
- physical deletion performed。
- live Git execution performed。
- repository mutation performed。

```text
independent authorization approved
!= execution request
!= execution decision
!= lifecycle transition
```

## 形式境界

Lean moduleは次を固定します。

- approved authorizationが有効なauthorization decisionであること。
- approved authorizationが別主体のexecution authorityを要求すること。
- denied authorizationが後続段階へ進まないこと。
- rejected authorizationが有効なdecision recordを発行しないこと。
- valid authorizationがexecution effectとrepository mutationを実行しないこと。
- 同一入力に対する決定性。

Lean成功は、現実のauthority資格、組織的独立性、mandate、jurisdiction、quorum、比例原則、倫理的妥当性、対象を終結すべきことを証明しません。

## Validation

```bash
PYTHONPATH=. python3 -m unittest -v \
  tests.test_kuuos_apoptosis_independent_authorization_v0_7

PYTHONPATH=. python3 \
  runtime/kuuos_apoptosis_independent_authorization_check_v0_7.py

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  env lean formal/KuuOSApoptosisIndependentAuthorizationV0_7.lean
```
