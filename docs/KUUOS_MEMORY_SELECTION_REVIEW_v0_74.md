# KuuOS Memory Selection Review v0.74

## 目的

v0.74は、v0.73の選択recordを外部reviewへ渡し、明示的decisionをimmutable receiptとして固定します。

review requestは、selection record、source history、source kernel、family、選択member、選択kernel、選択connection、rollback targetへ完全束縛されます。

## decision

```text
APPROVE_MEMORY_SELECTION
REJECT_MEMORY_SELECTION
REQUEST_REEVALUATION
```

approvalは、束縛された選択kernelに限定したproduction適用権を付与します。

approval関数自体は状態を書き換えません。

rejectと再評価要求はproduction適用権を付与しません。

## governance

requestはreviewer ID、reviewer class、validity windowを固定します。

request外のreviewer class、期限外decision、digest改変をfail closedとします。

rollback targetはsource kernel digestに固定し、review時の置換を認めません。

## 実行境界

```text
writes_enabled = false
live_application_enabled = false
permission_expansion_enabled = false
rollback_target_replacement_enabled = false
```

production適用権の付与と、即時の状態変更は別の作用です。

## Lean形式化

Leanでは、approvalとapplication authorityの同値、non-approvalでのauthority否定、exact selection binding、validity window、rollback target固定、即時作用の禁止を証明します。
