# KuuOS Lean→Python v0.58 — 分岐を消さずに保持するタグ付き局所アーカイブ

**基点main：** `039727525018e695b409a3a87dbf6912d19fbee3`（v0.57正式統合）。
Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。
append-only／tighten-only／overwrite-forbidden／same-root。

## v0.57からの制約

v0.57のLean定理は、二つの宣言された履歴が一つの線形リストの
正確な前置部分として貼合できる必要十分条件が、二履歴の前置比較可能性
であると示す。互いに比較不能なforkは、**単一Listでは**共通後続を持たない。

しかし、単一Listに貼り合わせられないことは、同じ旧履歴と二つの後続
を**タグを分けて同時に記録することまで不可能**とは意味しない。

v0.58ではこの二層を明示する。

### 形式的対象

`TaggedForkArchive`は、宣言された共通祖先、左・右の
`DetachedReplayWitness`、それぞれが祖先を延長する証明を保持する。
`branchProjection archive true`は左、`false`は右を取り出す。

固定Leanの新規11宣言で、次を証明対象とする。

1. タグ付き左右の射影が元の二履歴と**正確に一致**する。
2. 左右のどちらも同じ共通祖先の前置延長を保持する。
3. 祖先にある要素は二つのタグそれぞれで保存される。
4. forkが与えられたときにタグ付きアーカイブを構成できる。
5. タグ付きアーカイブが存在しても、forkの比較不能性や
   **単一線形後続の不可能性は消えない**。
6. 元PlanOSに選択・実行権限は付与されない。

この構成を「分岐のあるデータ型で情報を失わない局所貼り合わせ」と
解釈することはできるが、v0.57が否定する**線形Listへの降下**とは
異なる。外部のhistorical issuance、独立の保管、cryptographic
SHA-256、数学的実世界同定、因果時刻までは証明しない。

### Pythonランタイム

`build_local_tagged_fork_archive(ancestor_manifest,left_manifest,right_manifest,...)`
は、元のv0.56監査により三つのv0.54分離manifestを検証してから、
次を含む標準形式の純粋な**JSON値**を構成する。

- 共通祖先の完全な分離snapshot
- `left`と`right`のタグを持つ**二つの別々の**snapshot
- `fork`か`comparable`かという局所的関係
- 指定された場合の、呼出元が提供した祖先manifest checkpoint値

`verify_local_tagged_fork_archive`はSQLiteや元OSにアクセスせず、
これらを再検証して同じアーカイブを再構成し、正準JSONの
SHA-256を返す。別途提供されたarchive SHA-256値も検査できるが、
値が一致することから保管者や発行者の真正性を導かない。

forkがあれば、`LOCAL_TAGGED_FORK_BOTH_BRANCHES_PRESERVED_PROPOSAL_ONLY`
として**左右両方を完全に保存**する。archive内の`declared_relation`
を`comparable`へ偽装しても再計算で拒否する。
祖先が異なる／tampered payload／不正なタグ順はBLOCKEDまたは
祖先obstructionとして保持する。

`selected_successor`は常に`None`。
アーカイブが作れたことは、単一線形履歴の貼合成功、世界の事実の
検証、元のPlanOSからの発行、ホスト実行許可とは独立である。

### 独立検証とマージ条件

新規6ファイルのみ（Lean、Python、test、静的ソースchecker、
文書、限定CI）。元のPlanOS/VerifyOS・v0.53〜v0.57・
107公開proof roots・固定Lakeを変更しない。

新規限定CIはmainのv0.57を正確なコミットからStrict Leanで
再検証し、v0.58のLeanをwarning/sorry-fatalビルドする。
11宣言すべての`#print axioms`を実行し、標準3公理
(`propext`,`Classical.choice`,`Quot.sound`)だけを許可、
`sorryAx`を禁止する。

Pythonでは6つのnative VerifyOS→PlanOS経路から作成した
共通祖先・左右分岐を、元OSの再実行なしにアーカイブし、
オフライン再照合、左右の射影保持、forkの非消去、署名・保管者の
未認証、過去checkpointの不一致、archive digestの不一致、
不正なタグ、branch tampering、原本source driftを検査する。

独立PR GovernanceのStrict Lean、累積Runtime、公開API、workflow、
Exact-head受領書、source/test-merge Git tree一致の全ゲートを
**同じHEAD**で確認した場合のみ統合を検討する。
PRはDraft/OPEN/HOLD MERGEで開始する。
統合後mainに対するpush CIは統合前と別に認証する。

原本PlanOS未出力の三つの結果Finset、独立の外部保管者、
真の二後続の発行、グローバルreplay保証、JSON/SHA-256の
Lean形式化、Lean↔CPythonの普遍的対応、大域的な降下、
ホスト実行権限は**NO_DATA／未証明**。

保護PR #1558 Draft/OPEN/未マージ。
Preference ⇏ Descent ⇏ Authority。
