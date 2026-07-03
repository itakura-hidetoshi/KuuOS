# KuuOS Lifecycle Bounded Authorization Decision v0.12

## 位置づけ

KuuOS Lifecycle Bounded Authorization Decision v0.12は、Apoptosis Lifecycle Governance系列に属します。

repository mutation roadmap v1.19からv1.24とは独立しており、v1.25ではありません。

v0.12は、v0.11が`LIFECYCLE_BOUNDED_DECISION_REVIEW_CLEAR_FOR_AUTHORIZATION_DECISION`としたbounded requestについて、事前指定されたauthorization decision makerが認可判断を行う層です。

v0.11までの非認可境界は恒久的な禁止ではありません。

v0.12では、その境界を一段進めます。

```text
v0.11 decision review CLEAR
→ v0.12 authorization decision APPROVED
→ separate operation-start layer
```

## 実際に行うこと

APPROVEDでは、次を実際に記録します。

- authorization decision recordを発行する。
- authorization decisionを行う。
- bounded operationを承認する。
- separate operation-start layerが次に必要であることを記録する。

したがって、APPROVED artifactでは次が`true`です。

```text
authorization_decision_made
operation_approved
operation_start_required_next
```

v0.12は単なるreview artifactではありません。

## Source-chain再計算

v0.12はv0.1からv0.11までのsource chainを完全再計算します。

v0.11 recordのdigestだけを信頼しません。

source reviewは次を満たす必要があります。

- statusがCLEARである。
- review recordが発行済みである。
- authorization decisionが次段階として要求されている。
- authorization decisionが未実施である。
- operationが未承認かつ未開始である。
- subject、scope、requester、reviewer、authorization decision maker、future operatorのbindingが一致する。

## 役割分離

Authorization decision makerは次から分離します。

- subjectおよび既存source chainのactor。
- v0.11 decision reviewer。
- v0.10 requester。
- future operator。

future operatorは、APPROVED後も別主体としてoperation-start layerを担当します。

## 判断条件

APPROVEDには次を要求します。

- authority mandate。
- authority qualification。
- independence declaration。
- conflict disclosureおよびmaterial conflict不在。
- jurisdiction。
- quorum。
- reasoned decision。
- proportionality。
- less restrictive alternativesの検討。
- irreversibility review。
- human impact review。
- exact scope binding。
- rollback、recovery、stop、abort、oversight、monitoring、evidence capture、simulationの各条件。
- protected core exclusion。
- institutional holdおよびemergency stateの不在。
- appeal、dissent、minority opinionの各route。

## 状態

v0.12は次の三状態を返します。

```text
LIFECYCLE_BOUNDED_AUTHORIZATION_DECISION_APPROVED
LIFECYCLE_BOUNDED_AUTHORIZATION_DECISION_DENIED
LIFECYCLE_BOUNDED_AUTHORIZATION_DECISION_REJECTED
```

APPROVEDは認可判断とoperation approvalです。

DENIEDも有効な認可判断ですが、operationを承認しません。

REJECTEDはsource、policy、identity、binding、期限などの構造的不正を示し、有効な認可判断を発行しません。

## 次層との境界

v0.12はoperationを承認しますが、operation start自体は次層へ分離します。

これはoperation startを恒久的に禁止するものではありません。

v0.12の責務がauthorization decisionとapprovalであり、future operatorによる開始を別の監査可能な遷移として残すためです。

v0.12では次はまだ`false`です。

- operation started。
- operation completed。
- authority changed。
- quiescence state changed。
- terminal state changed。
- terminal marker written。
- resource removed。
- external operation performed。
- repository changed。

## 形式境界

Lean moduleは次を証明します。

- APPROVEDがauthorization decisionとoperation approvalを伴うこと。
- APPROVEDがseparate operation-start layerへ進むこと。
- DENIEDが有効なdecisionである一方、operationを承認しないこと。
- REJECTEDが有効なauthorization decisionを発行しないこと。
- v0.12 artifactがoperation start以後のeffectを偽造しないこと。
- 同一入力に対する導出の決定性。

Lean成功は、現実のauthority資格、組織的独立性、法的権限、倫理的妥当性、対象を終結すべきこと、将来operationの成功を証明しません。

## Validation

```bash
PYTHONPATH=. python3 runtime/kuuos_lifecycle_authorization_decision_check_v0_12.py

lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  env lean formal/KuuOSLifecycleStageV0_12.lean
```
