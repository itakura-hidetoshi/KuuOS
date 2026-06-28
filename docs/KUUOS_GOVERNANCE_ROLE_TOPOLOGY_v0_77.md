# KuuOS Governance Role Topology v0.77

## 目的

v0.77は、ガバナンスの運用モードと独立承認の要否を分離します。

`SOLO_RESEARCH`、`TEAM_RESEARCH`、`PRODUCTION`は運用文脈を表すラベルです。

これらのラベル自体は、reviewerとapplication authority ownerを別主体にすることを要求しません。

## 基本原則

```text
governance mode != role-separation requirement

PRODUCTION != independent approval mandatory

shared actor != immediate execution

application authority != state mutation
```

独立承認の要否は、各モードとは別のpolicyとして明示します。

```text
independent_authority_approval_required = false
```

の場合、reviewer自身をauthority actorとして使用できます。

追加の承認操作は発生しません。

```text
independent_authority_approval_required = true
```

の場合だけ、reviewerとは異なるauthority actorを要求します。

この設定は三つのどのモードでも選択できます。

## 既定動作

既定値は全モードで次のとおりです。

```text
independent_authority_approval_required = false
```

したがって、`PRODUCTION`であることだけを理由として独立承認は追加されません。

一人開発では、v0.74のreviewerが同じ操作内で限定的application authorityの主体となれます。

チーム開発でも、役割分離が必要な案件に限ってpolicyを有効化できます。

## v0.74との関係

v0.77はv0.74のreview receiptについて次を検査します。

- receipt self-digestが正しい
- statusがapprovedである
- production application authorityが存在する
- review receiptに未解決issueがない
- review関数がwriteまたはlive applicationを行っていない
- permission expansionまたはrollback target replacementがない

v0.77はv0.74のapproval decisionを再実行しません。

## v0.75およびv0.76との関係

v0.75の一回限りcompare-and-swap applicationと、v0.76の監査可能rollbackは変更しません。

v0.77はstate write、live application、permission expansionを行いません。

role topology receiptは、承認主体の構成が選択されたpolicyと整合することだけを表します。

## fail-closed条件

次を拒否します。

- policy digestの改変
- 未定義governance mode
- review receipt digestの改変
- 未承認review
- application authorityの欠如
- review境界でのwriteまたはlive application
- policyが独立主体を要求する場合の同一主体指定

## 将来の拡張

役割分離を導入するときは、運用モードを変更せずpolicyだけをtightenできます。

逆に、`PRODUCTION`へ移行しても、案件の規模、組織構造、法的要件、外部契約が独立承認を要求しない限り、追加手続きを自動的には導入しません。
