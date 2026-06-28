# KuuOS Authority Role Topology v0.76

## 目的

v0.76は、証拠reviewとapplication authorityの担当者構成を、運用文脈から分離します。

独立承認の要否は`RESEARCH`または`PRODUCTION`という文脈ではなく、明示されたrole topologyだけで決定します。

## role topology

```text
ROLE_AGGREGATED
ROLE_SEPARATED
```

### ROLE_AGGREGATED

一人開発または単一責任者の運用を表します。

v0.74の有効なapprovalが限定的application authorityを持つ場合、追加の独立承認を要求しません。

この規則は`RESEARCH`と`PRODUCTION`の双方で同じです。

```text
solo + research
→ independent approval not required

solo + production
→ independent approval not required
```

`PRODUCTION`という名称だけからrole separationを強制しません。

### ROLE_SEPARATED

複数担当者による独立承認を明示的に選択した運用を表します。

このtopologyでは、v0.74のreviewerとは異なるauthority actorによる追加approvalを要求します。

role separationは、チーム化、組織要件、契約、制度、外部規制などに応じて明示的に選択します。

## operating context

```text
RESEARCH
PRODUCTION
```

operating contextは記録と由来のために保持します。

operating contextは、独立承認要件を暗黙に変更しません。

```text
requires_independent_approval
= function(role_topology)
!= function(operating_context)
```

## ソロ運用

ソロ運用では、review ownerとapplication authority ownerを同一主体へ集約できます。

追加のapproval receipt、別actor、二段階操作を必須としません。

ただし、次の境界は維持します。

```text
approval != immediate execution
application authority != unlimited authority
authority != state mutation
authority has finite scope
authority has finite validity
rollback target is fixed
effect requires the v0.75 compare-and-swap transition
approval is consumed once
```

## 分離運用

`ROLE_SEPARATED`を選択した場合だけ、次を要求します。

```text
independent approval exists
independent approval binds the exact v0.74 review receipt
authority actor != review actor
approval is valid at evaluation time
approval digest is intact
```

## 外部要件

v0.76は、ソロproductionが自動的に安全、適法、制度承認済みであるとは主張しません。

法令、所属組織、契約、臨床、情報セキュリティ、deployment環境が独立承認を要求する場合、その外部要件が優先します。

リポジトリ内部では、productionというラベルだけを理由に手続きを増やしません。

## 形式化境界

Leanでは次を示します。

```text
role-aggregated topology never requires independent approval
research / production does not change that requirement
valid review authority suffices in solo production
role-separated topology requires independent approval
application authority still requires review authority
```

この形式化は、外部制度上の承認またはproduction safetyを付与しません。
