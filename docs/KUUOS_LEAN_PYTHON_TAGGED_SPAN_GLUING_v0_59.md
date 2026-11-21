# KuuOS Lean→Python v0.59 — タグ付き位置集合上の条件付き観測貼合

**固定正本基点：** `main 0c3bbfaa6894fd45723d4924f4f2d6508e06c341`（v0.58正式統合）。
Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。
append-only／tighten-only／overwrite-forbidden／same-root。保護PR #1558を変更しない。

## 数学的な対象：出来事の真正性でなく位置集合

v0.57が証明したのは、比較不能な二履歴を**一つの順序つきListの
正確な前置履歴**として共存させることの不可能性である。
v0.58は、祖先と左・右の履歴を別々のタグで保持するアーカイブを構成した。

v0.59はこのアーカイブの有限な**位置**を型として区別する。

- 共通祖先位置：`Fin common.length`
- 左だけの追加位置：`Fin leftExtra.length`
- 右だけの追加位置：`Fin rightExtra.length`

位置のタグは`common`、`left`、`right`である。
同じticket値・同じ注釈文字列があっても、左右の個別位置は
異なる位置であり続ける。共通祖先位置だけを同一視する。

左右の局所位置空間
`LeftPosition = common ⊕ leftExtra`、
`RightPosition = common ⊕ rightExtra`
から`TaggedPosition`への包含写像をLeanで構成する。
元のv0.58の`TaggedForkArchive`から追加suffixの
証拠を取り出し、両局所履歴が厳密に復元されることも示す。

## 証明対象：局所値の貼合の必要十分条件

任意の型`X`と、二つの局所観測写像
`fL : LeftPosition → X`、`fR : RightPosition → X`を考える。

**互換条件**：
`∀ i ∈ common, fL(inl i) = fR(inl i)`

**貼合条件**：
`∃ g : TaggedPosition → X`、
`g ∘ leftInclusion = fL`かつ`g ∘ rightInclusion = fR`。

Leanでこの二条件が**必要十分**であること、
条件が成立すれば`g`が**一意**であることを証明する。
祖先の一つの位置で値が違えば、貼合を阻害する
`obstruction`として残す。

これは**集合・型のレベルでの普遍的写像性（pushout-like property）**
である。mathlibの`CategoryTheory.IsPushout`として
認証したとは主張しない。また、貼り合わせる対象は
「観測写像の値」であり、線形な時系列そのものではない。
従ってv0.57の「forkの単一線形後続は存在しない」と矛盾しない。

証明は原本PlanOSからの実行権限を付与しない。

## Pythonの実行時構造

`glue_tagged_observations(archive,left_observations,right_observations,
separately_supplied_archive_sha256=...)`：

1. v0.58の既存の独立検証器でarchive全体とv0.54台帳証拠を再計算する。
2. 左右それぞれに、全行と一致した位置数の**不透明な文字列観測値**を要求する。
3. 共通祖先に対応する全位置の値の一致を一つずつ確認する。
4. 不一致は`shared_observation_disagreement:<position>`として全件保存し、貼合を構成しない。
5. 完全一致した場合のみ`common:000000`、`left:000000`、
   `right:000000`等の**相異なる位置ID**に値を割り当てる。
6. 左右の射影を元の観測列へ再構成して厳密一致を確認する。
7. archiveに存在する過去チェックポイント値の不一致は、
   共通部分の互換性とは別の障害として残す。

既存のVerifyOS・PlanOS・SQLiteを、この貼合検証器自身が再実行しない。
テストの入力作成時のみ、既存v0.53の本物のSQLite台帳と
6種類のnative経路を使用する。元の結果Finset3件は生成しない。

## 重要な二つの非含意

**枝の注釈値が一致すること**
`⇏`過去の発行者・独立保管者の真正性。

**タグ付き位置に観測写像を貼り合わせられること**
`⇏`比較不能な二履歴を単一の線形時系列へ降下させられること。

外部公開署名、因果時刻、別ホストreplay阻止、
SHA-256/HMACの暗号学的安全性、
Lean上での実Python・JSON・SQLite意味保存、
原本PlanOSが未発行の三つの結果Finset、
大域的な降下とホスト権限は未証明／NO_DATAのまま。

## 独立検証の条件

変更は新規6ファイル（Lean、Python、tests、source guard、
CI、文書）に限定し、原本OS・v0.53〜v0.58・公開proof rootsを
上書きしない。

- 正確なcanonical親v0.58を固定Lean環境で独立再ビルド。
- v0.59の新規Leanをwarning/sorry-fatalのLakeでコンパイル。
- 新規18宣言の直接`#print axioms`を**全件**実行し、
  標準`propext`、`Classical.choice`、`Quot.sound`以外を拒否し、
  `sorryAx`を許容しない。
- Pythonでは六経路・祖先一致・祖先不一致・同じ値でも枝IDが
  別であること・注釈不正・チェックポイント不一致・
  原本OS非実行・既存ソースSHA変更検知・
  重複unittestクラス排除を検証。
- PR GovernanceのStrict Lean、累積Python Runtime、
  公開API、workflow整合性、Exact-head terminalと
  source／test-merge tree一致を**同じHEAD**で全件SUCCESSにする。
- 認証後のみPRをマージし、統合後の新mainを独立push CIで再観測。
  全体`KuuOSFormal`の認証は別の証拠であり、
  対象限定CI成功から昇格させない。

初期状態はDraft／OPEN／HOLD MERGE。
Preference ⇏ Descent ⇏ Authority。
