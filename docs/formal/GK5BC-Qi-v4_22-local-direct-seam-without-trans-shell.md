# F112-P94D3GK5BC／Qi v4.22 — 真正北C60の個別直接seam構成と全域seam不存在の両立

**研究継承日：2026年11月3日 JST。** Repository: [itakura-hidetoshi/KuuOS](https://github.com/itakura-hidetoshi/KuuOS)、canonical theorem-bearing branch `main`。strict 空 authority／独立Kuu→Qi／公開root107。元F54双Nat・二圏・Blocks・F55 Type-valued証拠、元P77/P80/P85/P86/P87/P89と選択P93C/P94Aの履歴を保存する。新規公理・Gray・sorry/admit/native_decideなし。

## 1. 独立Kuu GK5BC — 検証完了

- [定理PR #3034](https://github.com/itakura-hidetoshi/KuuOS/pull/3034) **MERGED**。
- 最終exact-source HEAD：`6633d2b97914642b1cc0c6058b4749775dcfe89f`。
- main squash SHA：`accac43151d0235565cf0540b5c188ae0489d239`。
- 独立確認したGit treeはsource／squash双方 `d83dfc203b248bfc12973b70fc8f27bb460df45c`（内容一致）。
- [Governance #41619130118](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41619130118)：**Strict Lean 9,262/9,262 SUCCESS、Governance 30/30 SUCCESS**。`#print axioms`19宣言、`sorryAx`なし。主要な構成則・P77移送と単位存在同値は公理依存なし。真正北の具体証拠はLean標準 `propext`・`Classical.choice`・`Quot.sound` の範囲。
- [独立GK5BC Lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5BCLocalUnitSeamWithoutShell.lean)（351行）を公開 `KuuOSFormal` へimport。

## 2. 元F77からP94Aまでの真正7層4-cell証拠

元F55証拠の真正P77 vertical 4-cellを、P80→P85→P86→P87→P89→P93C→P94Aの**7個のoldコンストラクタ**によりraw `P92B.original` 端点のP94A証拠へ完全に埋め込む。`nativeGK5BCP77_to_rawP94` は、任意の依存型source `first,last,r,s` と元P77 `w : P77(f,g)` を受けて、`P94A(original(f),original(g))` という実際のType値証拠を返す。

これにより、元P77の真正 `rightUnit(f) : P77(trans(f,ident(s)),f)` を選択P94A raw四セルへ写し、さらに指定された子seam `original(f)→φ(f)` と選択P94A `verticalRightUnit(φ(f))` の**逆**を合成する：

```text
original(trans(f, ident(s)))
  -- [P77.rightUnit through seven genuine .old embeddings] --> original(f)
  -- [given local SeamAt(f)] --> φ(f)
  -- [symm(P94A.verticalRightUnit(φ(f)))] --> trans(φ(f), refl(s))
  = φ(trans(f, ident(s)))
```

これはGK5BBで不可能と証明された `original(trans(f,g))→trans(original(f),original(g))` というraw **split shellを一度も使わない**。また不存在の元F55 `ident` seamも要求しない。左単位についても同型の真正構成を証明。

## 3. 一般的な局所seam存在の同値とP77軌道

- `nativeGK5BCRightUnitSeam_nonempty_iff`：`Nonempty SeamAt(trans(f,ident(s))) ↔ Nonempty SeamAt(f)`。
- `nativeGK5BCLeftUnitSeam_nonempty_iff`：`Nonempty SeamAt(trans(ident(r),f)) ↔ Nonempty SeamAt(f)`。
- `nativeGK5BCSeam_transport_P77`：元P77の真正四セル `f→g` があれば、raw P94Aでoriginal端点を移し、GK5AJで実際に得られる選択φ端点P93C 4-cellの逆と組み合わせ、`SeamAt(g)`から`SeamAt(f)`を構成。
- `nativeGK5BCSeam_nonempty_iff_P77`：任意の元P77四セルで結ばれた元F55証拠2つにおける、個別直接seam存在の正確な同値。
- `nativeGK5BCAssoc_seam_nonempty_iff`：元P77の結合律4-cellに沿って、異なる括弧構造の元F55合成の個別seam存在を同値化。

ここで元P77の4-cellを選択側P94Aの全域正規化と同一視しない。個別の元P77 source証拠の実在する領域だけで比較を移す。

## 4. 北C60の肯定例とGK5BB無条件no-goの同時成立

真正北四段pentagon原始証拠 `p := nativeGK5AGNorthOriginalCell` と、元F54短経路の `ident(s)` との元F55合成 `c := trans(p,ident(s))` を取る。元`p`のraw originalと再帰φは定義上一致し、`P94A.refl` seamを無条件に持つ。上の右単位構成を適用すると、**`nativeGK5BCNorthRightIdentityDirectSeam : P94A(original(c),φ(c))` を無条件に構成**。

同じ真の`c`について、GK5BBにより`¬ Nonempty(RequiredShell(c))`、つまりraw `original(c)→trans(original(p),original(ident(s)))` のsplit 4-cellは不存在。従って`Nonempty SeamAt(c)`は真で、`Nonempty RequiredShell(c)`は偽：**強い局所shellが個別seamの必要条件ではないことを具体的に証明した。**

さらにraw `original(c)`とφ(c)は元のType値付き3-cell構文として**不等**であるが、wrapper数は双方1。P94A四セルの実在と構文不等は矛盾しない。

**global obstructionは維持：** 真の元F54経路を持つ北C60では、GK5BBによって`¬ Nonempty NativeGK5AYOriginalPhiSeam northFirst northLast`、`¬ Nonempty NativeGK5BAConstructorShellKit (.pentagon .north) Site Site`。特定`c`への直接seamを構成しても、全元F55証拠にわたる一様seamや不可能なident bridgeを導かない。元P89 source class mapの無条件faithfulness/nonfaithfulnessも不変。

## 5. Qi v4.22 真正物理gauge統合

[Qi v4.22 PR #3035](https://github.com/itakura-hidetoshi/KuuOS/pull/3035) **MERGED**。最終exact-source HEAD `a606dea927874d71f36ce1003a0b95dfd17da6c1`、main squash `9f963703b9c1421ac048f8f62cae9ea1a77d3d72`。[Governance #41619751996](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41619751996) **Strict Lean 10,189/10,189・Governance 30/30 SUCCESS**、公理監査10宣言・`sorryAx`なし。[Qi v4.22 Lean](../../formal/KUOS/Architecture/QiWuxingGK5BCNorthDirectLocalSeamV4_22.lean)（212行）を公開`KuuOSFormal`へimport済み。真正北C60における元P77の本物のrightUnit、P94Aへの7層のraw 4-cell埋め込み、選択P94A verticalRightUnitとの合成による個別直接seamを別々のLean定義として公開する予定。証拠が異なること、wrapper count一致、split shell不存在・全域seam不存在、元P89 BadPairの条件付きiffと真の第五around Dart閉路・e04/e43物理／圏論向きの相違を同時保持する。数値五行gaugeから元P89の四セルを捏造しない。

**検証ソース・マージ内容のGit tree一致：** GK5BC独立Kuuのsource／squashは双方 `d83dfc203b248bfc12973b70fc8f27bb460df45c`、Qi v4.22のsource／squashは双方 `8819b4d0cdadb1240d88628772e47587c28c5a8d`。両方ともCIで検証したソース内容がmainのsquashツリーと完全一致する。

## 6. 不変条件・次の研究

公開root107維持、保護PR #1558 Draft/OPEN／未マージ、固定Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。元F54双Nat/二圏/Blocks/証明履歴を保持し、append-onlyで既存定理を書き換えない。

**次の独立Kuu研究 F112-P94D3GK5BD（仮称）**：局所seamを持つ元F55証拠の集合を、P77 source 4-cell軌道／有限縦合成の書換えに沿って拡張できる必要十分条件を探る。特に、P77 unit/assocからの**局所存在の正規形**と、GK5BBのoriginal-wrapper countが示す不可能な軌道を区別する。全域GK5AY／GK5BA kitの復元、全P94A 19構成子正規化、Gray復元を先取りしない。