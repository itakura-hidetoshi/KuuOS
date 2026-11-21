# KuuOS Lean→Python v0.60 — 私有分岐追記下での観測互換性・障害保存

**研究正本基点:** `main fb30ac869f2f38bdbe59e2ce9ccf8140bdaeeaa8`（v0.59統合済み）。
Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。
append-only／tighten-only／overwrite-forbidden／same-root。保護PR #1558はDraft／OPEN／未マージ。

## 研究課題

v0.59は、左右の局所観測が共通祖先の**すべての位置で一致すること**と、
共通位置を一度だけ・左右の個別位置を別々に持つタグ付き位置集合に
観測値写像が**一意に貼り合うこと**の必要十分条件をLeanで証明した。

v0.60はさらに、左右分岐の私有部分に新しいticketが追記された場合に
この条件がどう変化するかを問う。

**仮定**：共通祖先が変更されておらず、旧左右履歴の全行と旧観測値が
正確に保存されている。追加するのは左右の私有suffixだけであり、
新しい履歴が**少なくとも一つの完全な二行組を追加**している。

## Leanで証明すること（新規18宣言）

旧`BranchPositionSpan`に対し、
`appendPrivate s additionalLeft additionalRight`は、
`s.shared`を**変更せず**、
`s.leftExtra`と`s.rightExtra`の末尾だけにListを連結する。

`AppendObservationRecord`は、旧左右の観測関数と新左右の観測関数を
**別々に保持し**、以下を明示的な証拠として要求する。

- 旧祖先のすべての位置で左右それぞれの観測値を保存する
- 左右の旧私有位置でも観測値を保存する
- 元の左右履歴が新しい履歴の正確な前置部分になる

この条件下で、以下の定理を証明する。

1. 旧共有位置が不変で、旧左右private位置が新しい分岐でも識別できる。
2. **新しい観測互換性 ↔ 古い観測互換性**（必要十分）。
3. 旧観測が互換なら新観測も互換。
4. 旧観測が互換でなければ、その不一致障害は新観測でも消えない。
5. **新タグ付き貼合写像の存在 ↔ 旧タグ付き貼合写像の存在**。
6. 指定された旧共有位置の値の不一致は、左右private追記によって解除できない。
7. 左右privateの位置を混同せず、v0.57の単一線形履歴のfork obstructionを保存する。
8. 元PlanOSの選択・実行権限は付与しない。

ここでは形式的な`AppendObservationRecord`の証拠が仮定であり、
Leanが実世界の任意のDB追記・署名発行を自動で証明するわけではない。

## Pythonで検証すること

`audit_tagged_private_append(`
`older_archive, newer_archive, older_left_values, older_right_values,`
`newer_left_values, newer_right_values,`
`separately_supplied_old_archive_sha256=...)`

観測する順序：

1. v0.58をそのまま用い、旧・新の双方のアーカイブを個別に再検証する。
2. **共通祖先の完全なmanifestが等しい**ことと、過去checkpointの
   宣言値を勝手に差し替えていないことを確認する。
3. 左右の新履歴が各々、旧行の正確な順序付き前置を保持することを確認する。
4. 一つ以上の新しい完全な二行組が追記されたことを要求する。
5. 新しい観測配列が、左右とも旧観測値の全件を変更せず保持することを確認する。
6. 共通位置の全不一致番号を比較し、不一致が残ればそれらをobstructionで保持する。
7. v0.59の元の貼合検証器を旧・新双方で独立に呼び出し、
   観測互換性／タグ付き貼合可否の判定が保存されていることを再照合する。
8. 旧アーカイブのチェックポイント提示値との不一致は、
   共通祖先の観測不一致とは別の障害として保持する。

入力用の実台帳は回帰テスト内だけで生成する。
v0.53のSQLiteに、既存6本のVerifyOS→PlanOS native経路で予約した
共通祖先・左右の最初の分岐と、その後に左右または一方だけへ
実際の二行組を追記してv0.54の分離証拠を作成する。

`audit_tagged_private_append`自体は**オフライン・read-only**。
SQLite／ネットワークや既存OSの再実行を行わず、
外部発行者・旧checkpointerの真正性、原本PlanOSの未発行3 Finsetも補完しない。

**不正な大域化の禁止**：局所的な値の一致や旧SHA-256値との照合は、
過去の出来事やその独立保管者を認証しない。枝の値貼合は、
v0.57が否定した「共通の単一線形後続」を生成しない。

## 独立認証・マージ条件

6つの**新規ファイルのみ**を追加し、原本PlanOS／VerifyOS、
v0.53–v0.59、public roots、固定mathlibとLean toolchainを上書きしない。

- 元v0.59の完全なLean moduleをcanonical parentの固定環境で独立確認。
- 新v0.60のLean module全体とimports/dependent signaturesを
  warning/sorry-fatal Lakeでビルド、直接Leanもwarning-fatalで実行する。
- 新規18宣言の`#print axioms`出力を**全件監査**、
  許可公理は`propext`・`Classical.choice`・`Quot.sound`のみ、
  `sorryAx`を禁止する。
- v0.60の22回帰テスト：六つのnative経路、
  旧行と旧観測の保持、私有一方だけの追記、追記なしの拒否、
  再ハッシュした旧行改変の検出、祖先変更の拒否、
  共通観測不一致の保持と不正な修復の拒否、
  旧checkpointの不一致、OS非実行・Git blob固定など。
- PR GovernanceのStrict Lean・累積Runtime・公開API・workflow保全、
  正確なHEADとsource/test-merge Git tree一致、
  Exact-head terminalの成功を**同一HEAD**で再確認する。

PRは初期Draft／OPEN／**HOLD MERGE**。
全独立CIが成功しない限りマージ禁止。
正式統合後のmain-push CIは別途再観測する。
全体KuuOSFormalの結果も対象限定CIと別に判定する。

未証明／NO_DATA：歴史的な発行者・独立保管者、因果時刻、
暗号学的保証のLean証明、global cross-host replay排除、
Python JSON/SQLiteからLean型までの一般的意味保存、
原本PlanOSの未出力3 Finset、大域的降下、実行権限。

Preference ⇏ Descent ⇏ Authority。
