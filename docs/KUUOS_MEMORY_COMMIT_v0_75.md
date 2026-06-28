# KuuOS Memory Commit v0.75

## 目的

v0.75は、v0.74で付与されたproduction適用権を一度だけ消費し、選択済みMemoryOS接続をproduction stateへ原子的に反映します。

review approvalと状態変更を分離したまま、承認後の適用経路を閉じません。

## production state

production stateは次を保持します。

- state ID
- revision
- source history digest
- module digest
- current memory kernel
- current memory connection
- 消費済みreview receipt digest
- 直前state digest

stateはimmutableです。

commit関数はsource stateを書き換えず、新しいstateを返します。

## compare-and-swap

application requestは次を固定します。

- expected state digest
- expected revision
- review receipt digest
- source kernel digest
- selected kernel digest
- selected connection digest
- rollback target digest
- application epoch

expected stateまたはrevisionが一致しない場合はcommitしません。

## approval

commitには次を要求します。

- v0.74 review receiptのself-digestが正しい
- review statusがapproved
- decisionがapproval
- production application authorityが存在する
- application epochがvalidity window内である
- applicationがreview decisionより後である
- selected payloadがreview receiptと一致する

## one-time consumption

承認receipt digestはcommit後のstateへ記録します。

同じapprovalを再利用したcommitは拒否します。

## atomic commit

成功時は一つのstate遷移として次を実行します。

```text
revision := revision + 1
current kernel := selected kernel
current connection := selected connection
consumed approvals := consumed approvals + review receipt digest
previous state digest := before state digest
```

成功receiptでは、state writeとlive applicationを真とします。

permission expansionは行いません。

rollback targetはcommit前のkernel digestに固定します。

## fail-closed条件

次を拒否します。

- requestまたはreview receiptのdigest改変
- 未承認review
- production適用権の欠如
- validity window外
- stale state digest
- stale revision
- source kernel不一致
- selected payload差替え
- historyまたはmodule binding不一致
- approval replay

拒否時はbefore stateをそのまま返します。

## 外部host境界

v0.75はKuuOS runtime内のproduction state遷移を実装します。

外部host processや永続ストレージadapterの呼出しは、この層では行いません。

## 次段階

自然な次段階は、commit receiptに基づく監査可能なrollback transactionです。
