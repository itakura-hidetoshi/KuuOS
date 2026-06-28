# KuuOS Governance Mode and Role Aggregation v0.75

## 目的

v0.75は、開発段階に応じてreview ownerとapplication authority ownerの役割を集約または分離できることを明示します。

一人開発の研究段階へproduction相当の多段承認を要求しません。

既存のv0.74 memory selection review、application authority、ActOS実行境界は変更しません。

## ガバナンスモード

### SOLO_RESEARCH

一人開発または単一責任主体による研究段階です。

```text
review owner = application authority owner
independent authority approval required = false
role aggregation permitted = true
```

単一approvalは、束縛された対象に限定したapplication authorityを付与できます。

ただし、approvalは即時実行、状態書込み、権限範囲の拡大を意味しません。

### TEAM_RESEARCH

複数人による研究段階です。

集約型と分離型の双方を許容します。

```text
aggregated policy
independent authority approval required = false
role aggregation permitted = true

separated policy
independent authority approval required = true
role aggregation permitted = false
```

チームの規模、責任分担、対象リスクに応じてtighten-onlyに切り替えます。

### PRODUCTION

実運用へ接続する段階です。

```text
review owner != application authority owner
independent authority approval required = true
role aggregation permitted = false
```

production適用権限は、evidence reviewだけでは完結しません。

## 維持される境界

すべてのモードで次を維持します。

```text
approval != immediate execution
application authority != unlimited authority
authority != state mutation
authority has bounded scope
authority has finite validity
rollback target remains fixed
effect requires a separate execution path
effect requires subsequent observation
```

## 移行原則

`SOLO_RESEARCH`から`TEAM_RESEARCH`または`PRODUCTION`への移行は、既存の履歴やreceiptを破壊せず、追加的またはtighten-onlyに行います。

```text
SOLO_RESEARCH
→ TEAM_RESEARCH aggregated
→ TEAM_RESEARCH separated
→ PRODUCTION
```

すべての段階を順番に通過する必要はありません。

リスクと組織構造に応じて、より厳しいモードへ直接移行できます。

## 非主張

v0.75は、単独開発者によるapprovalを外部監査、制度的承認、臨床承認、production安全性と同一視しません。

役割集約の許可は、実行権限の無制限化ではありません。

将来の役割分離可能性を保持することは、現在の開発手続きを増やすことを意味しません。
