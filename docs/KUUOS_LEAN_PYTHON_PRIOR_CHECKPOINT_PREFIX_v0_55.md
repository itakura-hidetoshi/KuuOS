# KuuOS Lean→Python v0.55 — 二時点の分離証拠と過去チェックポイントの条件付き照合

正本基点 `main 8e28b40cc3869fac81fa8df98fd3412fb4df6ae7`（v0.54統合済み）。
Lean `v4.30.0-rc2`／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。
append-only／tighten-only／overwrite-forbidden／same-root。

## 問題：各時点で成立することと、時点をまたいで一致することは別

v0.54では一つの分離証拠に含まれる各行のhash-chainを再計算し、
外部から別途渡されたmanifest SHA-256の**値**と照合できる。
しかし**二つのスナップショットそれぞれの内部整合性**は、
以前の全履歴が後の履歴に本当に残っていることを意味しない。

今回の追加実装は、同一のv0.53台帳形式から取り出した
`older_manifest` と `newer_manifest` を**別々に**検査し、
新しい履歴の先頭が旧履歴の全行と**順序・内容まで完全一致**し、
後ろに最低1組の新しい二行観測が付加されている場合のみ
`strict_local_extension=True` とする。
行ID、nonce、sequence、message digest、前後hashも比較する。
既存の元OS・v0.53 SQLite・v0.54 export/read-only検証器は変更しない。

## 実装された照合

`audit_local_prior_checkpoint_prefix(`older_manifest`,`
`newer_manifest`, separately_supplied_prior_checkpoint_sha256=...)`

検査順序：

1. 二つとも独立してv0.54の形式・domain・全hash-chain・nonce/sequence重複検査を通過する
2. 後の履歴の最初の全行が、旧履歴と完全に一致する
3. 追加された行数が正かつ二行組である（v0.54側も両方偶数）
4. 旧最終row hashが新履歴の同じ位置で保持されている
5. 呼び手が過去manifest SHA-256値を**別途指定**した場合のみ、その値と旧manifest digestを比較する

過去チェックポイントを指定しない場合も局所的な前置整合は観測可能。
しかし「旧時点に実際にそのデータがあった」とは**言えない**。
古いデータと新しいデータを両方作り直し、互換するchainを再計算する
攻撃には、独立保管された真正な古いcheckpointがなければ無力。

### 結果の区別

- `STRICT_LOCAL_REPLAY_PREFIX_UNANCHORED_PROPOSAL_ONLY`：
  両履歴は内部整合し、strict prefixだが、古いcheckpoint値は未提示
- `STRICT_LOCAL_REPLAY_PREFIX_PRIOR_CHECKPOINT_VALUE_MATCH_PROPOSAL_ONLY`：
  strict prefixに加えて、**提示値**が旧manifest digestと一致しただけ
- `LOCAL_REPLAY_PREFIX_DIVERGENCE_OBSTRUCTION`：
  双方の履歴は内部整合していても、順序・内容が旧履歴と異なる
- `LOCAL_REPLAY_NO_STRICT_EXTENSION_OBSTRUCTION`：
  新規の完全二行組が増えていない
- `PRIOR_CHECKPOINT_VALUE_MISMATCH_OBSTRUCTION`：
  別途与えた旧checkpoint値との不一致
- `LOCAL_REPLAY_PREFIX_MULTIPLE_OBSTRUCTIONS`：
  旧行が変わり、同時にcheckpointも不一致など、**複数の障害を併記**
- `BLOCKED`：元manifest自体の破損、不正なschema/型/ハッシュ、未対応値
- `NO_DATA`：比較対象のどちらかが存在しない

署名検証、checkpointの取得時刻・出典、独立保管者の識別を行っていない。
そのため、`independent_checkpoint_custody_authenticated` 等は
常にfalseで、`host_execution_authorized` もfalseのまま。

## 形式構造（Lean）

v0.54の`DetachedReplayWitness`、`replayRoot`、
`selfConsistent`を直接importする。

11の新規宣言で、
- 旧履歴 ++ 追加履歴という**宣言された**正確な前置関係
- 非空追加では履歴長が真に増加し、旧要素が新履歴に含まれる
- 両方のabstract foldが整合すれば、旧rootからのfoldで新rootになる
- 前置不一致・checkpoint値不一致のobstruction
- 前置互換性・自己整合性・任意のdigest関数の値照合を
  **すべて仮定した時に限る**条件付き結論
- それでも原本PlanOSはhost実行権限を付与しない

を示す。形式証明されるのは抽象リスト・任意のfold関数・条件付き
文字列等式であり、Python dictのcanonical SHA-256／SQLite、
実際の過去履歴・cryptographic security、全OSの降下・
Lean↔CPython完全一致を示すものではない。
「空」「縁起」との対応は命名・解釈層でありLeanで証明される対象ではない。

## 実データ検証計画とマージ条件

新規Python回帰では、実際のVerifyOS→PlanOSの6経路を使った
v0.53台帳二組の時点別snapshotとv0.54 exportを実行し、
前置整合、二組追加、全履歴書換、古いcheckpointが残る場合の差異、
旧／新snapshot破損、rollback/半端な組、空再提出、
複数のobstruction、元カーネル非実行、秘密鍵非出力、
Git blob固定を検証する。

新規CIは固定Lean strict compile、全11宣言`#print axioms`
（標準公理`propext/Classical.choice/Quot.sound`のみ、
`sorryAx`なし）、新規Pythonテスト、既存正本v0.54の別個確認を実施する。
Governance全体のStrict Lean・累積Runtime・API保全・workflow整合性・
Exact-HEAD・ソース／テスト用マージtree一致は**別途**確認する。

このPRは **Draft / HOLD MERGE** で開始し、これら全条件の
独立成功を確認するまでmainに統合しない。
統合後pushの成功も統合前PRとは別に観測する。
全体KuuOSFormal aggregateはscope-limited SUCCESSから独断で昇格しない。

元PlanOSがまだ発行していない三つの結果Finset、外部発行者・
独立管理者の真正性、因果時刻、異なるホストのreplay、
HMAC/SHA-256安全性のLean証明、実行権限は**NO_DATA／未証明**。
保護PR #1558 はDraft／OPEN／未マージ。
Preference ⇏ Descent ⇏ Authority。
