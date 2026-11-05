# Qi v4.58 — 元P77真正証拠付き到達可能像とのカテゴリー同値

**2026-11-05 JST**

| 項目 | 確定状態 |
|---|---|
| 定理PR | [#3136](https://github.com/itakura-hidetoshi/KuuOS/pull/3136) **MERGED** |
| exact-source HEAD | `a03b23c9e862e84b9e317a33198d81ff3c25aaf9` |
| 定理squash/main | `9118c840ba4dcb34f0b8d23ebb02d9bddc6f8590` |
| Git tree (source = test-merge) | `3ba33b73321a510f6d389e7f6dc687b75c7d05ba` 完全一致 |
| exact-source CI | [#41971808748](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41971808748) |
| Strict Lean | **10,255 / 10,255 SUCCESS** |
| Governance | **30 / 30 SUCCESS** |
| 新規公理監査 | **12 / 12**、標準 `propext` / `Classical.choice` / `Quot.sound` 以内、`sorryAx` なし |
| 変更 | [新規Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77CertifiedImageEquivalenceV4_58.lean) ＋公開 `formal/KuuOSFormal.lean` import 1行 |

固定Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、公開root107。保護validation-only PR #1558はDraft/open/unmerged、strict空中心・独立Kuuは一presentation。全ての上流元F54/F55/P77/P94Aの証拠履歴、真正C60 EdgeおよびQi signed CRTをそのまま保持する。

## 1. 真正sourceと元P77のcertified image

Qi v4.53の5本の本物の有向`FivefoldEdge`（`e01/e12/e23/e04/e43`）からの自由圏`FivefoldFreePathCategory`をsourceとする。Qi v4.54で真正元F55/P77のType値四セルを、元GK5CGの**保守的Type値5-cellの存在のみ**で商にしたtarget `FivefoldP77ConservativePoint f g h k` を保持する。

Qi v4.57の `FivefoldP77ImagePoint f g h k` は、各Homを

```text
{ z : GenuineOriginalP77ConservativeQuotientHom //
    ∃ sourcePath : OriginalFivefoldTypedFreePath,
      F.map sourcePath = z }
```

という**元P77の真正商クラス＋本物の型付き到達証拠**で構成した別圏。数値chargeの一致でも、物理C60 Edge列の一致でもない。v4.57は`fivefoldP77ImageFactor`のFull・Faithfulおよび元targetへの`fivefoldP77ImageInclusion`のFaithful・NonFullを既に証明していた。

## 2. Source→imageの対象全射性

今回の`fivefoldP77ImageFactor_obj_surjective`は、任意の像圏対象 `Y : FivefoldP77ImagePoint f g h k` に対し、元ラッパーが実際に保持する `Y.vertex : FivefoldPathVertex` が原像であることを示す：

```text
∃ X : FivefoldFreePathCategory,
  (fivefoldP77ImageFactor f g h k).obj X = Y
```

元`FivefoldIndex = FivePhase = ZMod 5`の型を崩さず、対象のsurjectivityを直接証明した。このため固定mathlibの`Functor.essSurj_of_surj`から、`fivefoldP77ImageFactor_essSurj`として真正`Functor.EssSurj`を得る。

## 3. 実際のMathlibカテゴリー同値

`fivefoldP77ImageFactor_isEquivalence`は、v4.57で証明した実際の`Functor.Full`・`Functor.Faithful`、v4.58の`Functor.EssSurj`を合成し、真の`Functor.IsEquivalence`を構成。固定mathlibの`Functor.asEquivalence`から

```text
fivefoldP77ImageEquivalence :
  FivefoldFreePathCategory ≌ FivefoldP77ImagePoint f g h k
```

を定義した。これは**データを持つ真正圏同値**であり、単なる論理的`Nonempty`や対象の個数合わせではない。

`fivefoldP77ImageEquivalence_functor`でそのforward functorが既存の`fivefoldP77ImageFactor`に**定義のうえで完全一致**することを形式証明。`fivefoldP77ImageQuasiInverse`は実際のinverse Functorを与え、`fivefoldP77ImageUnitIso`と`fivefoldP77ImageCounitIso`は、それぞれ

```text
𝟭 FreePathCategory ≅ ImageFactor ⋙ ImageQuasiInverse
ImageQuasiInverse ⋙ ImageFactor ≅ 𝟭 CertifiedImageCategory
```

という真正の自然同型を構成する。元のP77証拠クラスは置換されず、像のHomは旧GK5CG保守的5-cellによる商のまま。

## 4. 元P77全targetとの正確な障害

`fivefoldP77ImageEquivalence_comp_inclusion`：

```text
ImageEquivalence.functor ⋙ ImageInclusion
  = fivefoldP77ConservativeFunctor
```

を真正Mathlib functor等号で証明。これにより、旧v4.54元P77関手の因子分解を保持する。

ただし、Qi v4.56の**実際の元P77逆向きe01四セル**（元P77 `symm`構成子、charge `-1`）には、有向自由経路の像から到達できない。よって、旧`fivefoldP77ConservativeFunctor`と`fivefoldP77ImageInclusion`のどちらも`Full`ではない。この事実から、`fivefoldP77ConservativeFunctor_not_isEquivalence`・`fivefoldP77ImageInclusion_not_isEquivalence`が、それぞれ**その関手は`Functor.IsEquivalence`ではない**ことを証明した。他に一切のカテゴリー同値が存在しないという一般的非同値定理ではない。

最終`fivefoldP77ImageEquivalence_obstruction_split`は、真正source↔certified image同値の存在、元targetへの包含の非同値、元のsource→全targetの因子分解を一つの証明命題として保持する。

## 5. CI・Lean記載法の境界

既存Qi v4.53〜v4.57の新規Lean全文と、pinned mathlib `Mathlib/CategoryTheory/Equivalence.lean`、`Mathlib/CategoryTheory/EssentialImage.lean`、`Mathlib/CategoryTheory/Functor/FullyFaithful.lean`の定義・シグネチャを照合して実装した。特に`Functor.IsEquivalence`は`Full`・`Faithful`・`EssSurj`のPropであり、`Functor.asEquivalence`はデータ付き圏同値を作る。前段の`Functor.FullyFaithful`はTypeデータである点を区別する。

最終exact-source CI [#41971808748](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41971808748) は固定Leanで **10,255/10,255** ビルド成功。新規12件の `#print axioms` に標準三公理以外や`sorryAx`はなく、変更Leanのwarning/errorなし。Governance30/30 SUCCESS。GitHub MCPでsource HEAD `a03b23c9...` とtest-merge `17b711662b...` のGit treeが `3ba33b73321...` で完全一致を確認。検証HEAD指定でsquash MERGED（`9118c840...`）。

## 6. 今後の研究境界

**確定した対象:** 正真正銘の元FivefoldEdge自由経路圏と、元GK5CG保守的証拠により到達が認証されたP77商像圏との**カテゴリー同値**。完全な元targetの元四セル構文を不正にstrict化する主張ではない。

**未主張:** 元P77全商targetとのこの関手による圏同値、元P77逆向き四セルの有向自由経路による生成、元P94Aの無条件original→φ seam、数値CRTからの原型証拠復元、C60物理辺とP77四セルの型同一視、global strict高次圏。

**次Qi v4.59候補:** この同値の準逆による型付き有限経路の復元と`charge=length`の自然性、さらに全targetへ準逆を延長できない障害を元P77の`symm`証拠から調べる。旧source歴史・source-certified像圏・全P77保守的targetの3 authorityを分けたまま研究する。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
