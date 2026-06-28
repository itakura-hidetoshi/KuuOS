# KuuOS Solo Direct Path v0.77

## 目的

v0.77は、一人開発に追加承認層を持ち込まないことを明文化します。

概念上の役割分離だけを理由として、runtime stage、policy object、validator、receiptを追加しません。

## ソロ経路

`SOLO_RESEARCH`では、既存の経路をそのまま使用します。

```text
v0.74 review approval
→ v0.75 bounded application
→ v0.76 rollback when required
```

v0.77は、この経路の間に処理を追加しません。

次は存在しません。

- 追加の承認操作
- 追加のauthority actor
- role topology policyの生成
- role topology receiptの発行
- actor identityの比較
- v0.75適用前の追加validator
- v0.76 rollback前後の追加gate

したがって、ソロ経路で増える承認手順はゼロです。

## PRODUCTIONラベル

`PRODUCTION`は、独立承認を自動的に要求するラベルではありません。

`PRODUCTION`を選んでも、既存の限定権限、validity window、digest binding、single-use consumption、compare-and-swap、rollback境界だけを使用します。

運用ラベルから新しい手続きを導出しません。

## 残す境界

手続きを増やさなくても、既存層が保持する次の境界は残ります。

- review approvalは即時実行ではない
- application authorityは無制限権限ではない
- state transitionはv0.75で一度だけ行う
- stale stateと改変receiptはfail-closedで拒否する
- rollbackはv0.76の前向き補償transactionとして行う
- permission expansionを行わない

これらは新しい承認層ではなく、既存application pathの内部条件です。

## 複数人開発

複数人開発になったという事実だけでも、独立承認を自動追加しません。

実在する別主体、法的要件、契約上の分掌、または外部host境界が生じた場合に限り、その具体的境界へ追加規則を結びます。

将来の追加規則はソロ経路を変更せず、対象となる外部境界だけをtightenします。

## 過剰統治の禁止

次の原則を採用します。

```text
conceptual separation != mandatory runtime stage

possible future team != present approval gate

operating label != procedural burden

solo development != simulated organization
```

存在しない組織構造を先回りして模倣しません。

統治機構は、現実に制御すべき独立主体または外部作用が存在するときだけ追加します。
