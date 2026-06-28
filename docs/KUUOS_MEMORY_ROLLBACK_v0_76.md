# KuuOS Memory Rollback v0.76

## 目的

v0.76は、v0.75のcommit receiptとpre-commit snapshotに基づき、MemoryOS production payloadを監査可能に復元します。

rollbackは過去のstateへ時間を逆行させる操作ではありません。

kernelとconnection payloadを復元しながら、production revisionとrollback ledger revisionを前進させる補償transactionです。

## 入力

rollback requestは次を固定します。

- current state digestとrevision
- rollback ledger digestとrevision
- v0.75 commit receipt digest
- pre-commit snapshot digest
- rollback kernel digest
- rollback connection digest
- rollback epoch

## commit evidence

次を照合します。

- commit receipt self-digest
- committed status
- atomic commit
- state writeとlive applicationの実施
- permission expansionなし
- rollback target置換なし
- current stateがcommit後stateと一致
- snapshotがcommit前stateと一致
- selected payloadがcurrent payloadと一致
- source kernelとrollback targetがsnapshot kernelと一致

## monotonic compensation

成功時は次を実行します。

```text
production revision := current revision + 1
current kernel := snapshot kernel
current connection := snapshot connection
previous state digest := rollback前state digest
rollback ledger revision := ledger revision + 1
ledger consumed commits := consumed commits + commit receipt digest
```

commit前revisionには戻しません。

## approval consumption

v0.75で消費されたreview approvalは、rollback後も消費済みのままです。

rollbackによってapproval権限を再有効化しません。

## fail-closed条件

次を拒否します。

- requestまたはcommit receiptのdigest改変
- committedでないreceipt
- stale current stateまたはrevision
- stale ledger digestまたはrevision
- snapshot不一致
- state chain不一致
- source、selected、rollback payload不一致
- base connection不一致
- rollback replay
- commitより前のrollback epoch
- review consumption欠損

拒否時はcurrent stateとledgerを変更しません。

## 境界

v0.76はKuuOS runtime内のproduction stateとrollback ledgerを更新します。

外部host adapterや永続ストレージへの反映は別のadapter層です。

## 次段階

自然な次段階は、commitとrollbackのreceipt chainをVerifyOSへ渡すpost-application verificationです。
