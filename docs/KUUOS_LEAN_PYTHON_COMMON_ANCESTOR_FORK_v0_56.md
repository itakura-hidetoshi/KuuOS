# KuuOS Lean→Python v0.56 — 同一局所祖先からの二後続履歴の分岐障害

**作業基点：** canonical `main 6518bb1c646980e421c31ce6fec41d6201f44203`（v0.55正本統合）。
Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`を固定。
append-only／tighten-only／overwrite-forbidden／same-root。

## 問題と必要条件

v0.55は「旧履歴Aに対して後続履歴Bが完全な厳密前置延長である」
という**二時点の局所的な条件**を判定する。しかし、A→BとA→Cが
ともに局所的に正しくても、B→CあるいはC→Bが成立するとは限らない。

v0.56はこの状況を、原本PlanOSの内容を変えずに、
**共通祖先から生じた二つの後続候補の比較可能性／分岐障害**として区別する。

- 旧証拠A、左後続B、右後続Cを、v0.54の分離証拠形式で受領する
- まず既存v0.55検証器で**A→BとA→Cを個別に**厳密な前置延長として検証する
- BとCが全行同じなら「同一の局所後続」／片方がもう片方の完全前置なら「比較可能な直列後続」
- 互いに前置延長でなければ「局所分岐obstruction」を出力する
- 異なる最初の行位置と両方の元manifest SHA-256を保つが、どちらかを選択しない
- 別途渡された**旧Aのmanifest SHA-256値**との不一致は分岐と同時にも保持する

分岐検知のために元のVerifyOS・PlanOSを再実行しない。
この三証拠の比較自体はSQLite・ネットワークを使わない。
テストにおいてのみ、同一v0.53台帳を二つのローカルファイルに分け、
別々の後続二行組をコミットしてv0.54分離証拠を作る。

## 形式Lean命題（11宣言を公理監査）

元のv0.55・v0.54及びPlanOS証明型を直接importする。

- 宣言された後続関係は反射的・推移的
- 一方が他方の後続であれば局所比較可能
- **共通の旧Listの直後に異なる最初の追加ticketが存在すれば、
  どちらの新Listも他方の前置延長にはならない**
- その場合に分岐obstructionが成立し、両履歴は一致しない
- 共通祖先の古いticketは両方で保持される
- それでも元PlanOSの実行権限は与えられない

このLean定理は抽象的な`List LocalReplayTicket`の等式である。
Python辞書やJSON SHA-256の同値性、実際の出来事や保管者の独立性は
Lean定理には含めない。

## Pythonの観測状態

`audit_two_local_successors(ancestor_manifest, left_manifest, right_manifest,
separately_supplied_ancestor_checkpoint_sha256=...)` は次を区別する。

- `LOCAL_DECLARED_SUCCESSOR_FORK_OBSTRUCTION`：二つとも旧Aを継承したが互いに比較不能
- `LOCALLY_COMPARABLE_SUCCESSOR_CHAIN_PROPOSAL_ONLY`：どちらかの履歴が他方の完全前置
- `LOCALLY_IDENTICAL_SUCCESSOR_PROPOSAL_ONLY`：二つの履歴が同じ
- `LOCAL_FORK_AND_PRIOR_CHECKPOINT_OBSTRUCTIONS`：分岐かつ提示された旧checkpoint値の不一致
- `LOCAL_PRIOR_CHECKPOINT_VALUE_OBSTRUCTION`：比較可能でも旧checkpoint値が不一致
- `LOCAL_COMMON_ANCESTOR_EXTENSION_OBSTRUCTION`：そもそも両方が旧Aを厳密に延長していない
- `BLOCKED`／`NO_DATA`：内部不正／必要な証拠の欠損

証拠には本当にどちらの分岐が発行されたのかを判定する情報が無い。
したがって`selected_successor`は常に`None`。
証拠の起源・保管・署名・外部時刻・実際の発行者、別ホストreplay阻止、
HMAC/SHA-256安全性のLean証明、原本PlanOS三つの結果Finset、
一般Lean↔CPython意味保存、全OSの降下・ホスト実行権限は
**未証明（NO_DATA）**のまま保持する。

## 対象限定の認証工程

新規6ファイルのみ。原本OS・証明・固定Lake・107公開roots・保護PRには変更なし。

独立CIでは、固定Leanで正本v0.55を直接compileし、新規v0.56
を`warningAsError`、`sorryAsError`の厳密Lakeでcompileする。
その後、direct Leanで11個の`#print axioms`出力を全件照合し、
標準3公理以外と`sorryAx`を拒否する。
さらにPythonの実際の6つのnative経路、同一祖先からの二つの
SQLite fork・直列後続・誤ったcheckpoint・元カーネル非実行・
誤ったsource SHAを検査する。

独立PR GovernanceのStrict Lean、累積Runtime、公開API保全、
Workflow整合性、Exact-HEAD、提出HEAD／テスト用マージtree一致を
全て再観測する。未完了は**認証済みではない**。
認証前マージは禁止し、統合後は新mainのpush CIを別件として確認する。
保護PR #1558 はDraft／OPEN／未マージ。

Preference ⇏ Descent ⇏ Authority。
