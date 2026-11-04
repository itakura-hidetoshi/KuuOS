# Qi v4.52 — 真正C60五角形と元F55/P77の全五辺を同じFivefoldEdgeで扱う

**Date:** 2026-11-05 JST  
**PR:** [#3124](https://github.com/itakura-hidetoshi/KuuOS/pull/3124) **MERGED**  
**Theorem main squash SHA:** `84e3afca1d6a4637e37b037ef7ae121201e16626`  
**Canonical Lean:** [QiWuxingGK5CGUnifiedFivefoldTypedEdgesV4_52.lean](../../formal/KUOS/Architecture/QiWuxingGK5CGUnifiedFivefoldTypedEdgesV4_52.lean) (231行 + EOF)  
**Exact-source final HEAD:** `de08640170a82fafca1d1ff0463aeed5847ad61f`  
**Final [Governance CI #41933415327](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41933415327):** **Strict Lean 10,249/10,249 SUCCESS**、Governance 30/30 SUCCESS、Independent KuuおよびWorkflow integrity SUCCESS。公開 `#print axioms` 8/8 は標準`propext`・`Classical.choice`・`Quot.sound`以内、`sorryAx`なし、変更Lean error/warningなし。

## 1. 三種類の「五」を単なる同じ個数ではなく型付きで接続

既存Qi v3.5で定義した**唯一の`FivefoldIndex = FivePhase = ZMod 5`と`FivefoldEdge`**（`e01,e12,e23,e04,e43`）を再利用し、新しい五点集合や五辺のコピーを定義しない。

新規`fivefoldF55OriginalAt f g h k q`は、五つの真正元F55 Type値付き3-cell合成`(((fg)h)k)`、`((f(gh))k)`、`f((gh)k)`、`f(g(hk))`、`((fg)(hk))`から、正準5相`q`に対応する元証拠そのものを返す。すべての元F54・F45依存型source/targetを保持する。

新規`fivefoldF55OriginalP77Edge f g h k edge`は真正元P77 Type値付き四セルを5本すべてで返す。特に：
- `e01`は元`P77Edge01`、`e12`は元`Edge12`、`e23`は元`Edge23`。
- `e04`は元`Edge40`の真の`symm`、`e43`は元`Edge34`の真の`symm`。したがって旧original cyclic向きと新Qi/GK5基底の向きを混同しない。

**元の証明構文に新規4-cell/5-cellを捏造していない**。`fivefoldF55OriginalP77Edge`は既存P77真の構成子の型付き実装。

## 2. 数学的な定理

`fivefoldF55OriginalP77Edge_assocCharge_one`は、任意元F55合成可能四項組・任意五辺について、`NativeF55RawVerticalFourCell.gk5cgAssocCharge = 1 : ℤ`を証明する。逆向きの2辺は元の`symm(.symm(assoc))`に対応するため正のchargeを持つ。

`fivefoldF55OriginalUpper`は`e01≫e12≫e23`、`fivefoldF55OriginalLower`は`e04≫e43`という**真正元P77四セル証拠の二経路**。その完全な依存型端点は一致するが証明項としては無条件には等しくない。各ルートの符号付き整数チャージは厳密に

```text
charge(upper) = 3
charge(lower) = 2
defect        = +1
```

`fivefoldF55Original_noConservativePentagonator`は、GK5CGの保守的5-cell構成子がこの整数チャージを保存することから、**両経路間の保守的五セル不存在**を任意の元F55四項に対して証明。これは新presentationに別途pentagonatorを追加したGK5CGの結果と矛盾しない。

## 3. C60の真正物理五角形への型付き対応

`fivefoldOriginalPhysicalPair frame v edge f g h k`は、任意の**実C60五角形`(.pentagon v)`**・局所ゲージ`frame`・5辺`edge`に対し、同時に次を返す。

1. 真正`Edge.around`と両端の原Dartに対する`edgeJoins`証明を持つ`Subtype`。
2. 同じ`FivefoldEdge`のsource/target indexによる元F55の**真正P77四セル**。元F45/F54・D/E二カテゴリー・2つのNat深さ・Blocks証拠を保持。

旧Qi v3.5の`fivefoldCategoricalEdge`も**同じFivefoldEdge**を入力するため、元のC60物理辺・F55/P77・Mathlib NatIsoが単一の共通indexで選択可能になった。ただしこれらは**異なる数学的型**であり、互いに自動的に等しいこと、また共通indexのみから完全忠実な高次関手が存在することは主張しない。

## 4. エラーと形式検証

初回PRソース [CI #41932948829](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41932948829) は、新規P77エッジを`simpa`で型変換した際に残る**依存型`cast`**が、チャージ計算を定義的に簡約できず失敗。新規Lean全文、`FivefoldIndex`のZMod 5 numerals、GK5CF各元P77四セル、GK5CG真のcharge再帰を照合し、エッジ各構成子を`exact original P77Edge..`で直接定義する修正を行った。原命題・仮定を弱めない。最終CI #41933415327で10,249/10,249 SUCCESS、標準公理のみ、sorryAxなし。

## 5. 依然として残るobstruction

数値`RingHom`/CRT pentagon、物理入射、元P77四セル存在、局所P94A original→φ seam、保守的五セル存在性は別の判定問題。Qi v4.51の符号付きGK5BQ CRT自然性と原始/二重反転seam差も保持。実元P77保守的五セルの不在は**5相共通化後も不変**であり、新たなpentagonatorが旧元証拠から無条件に復元されたわけではない。

次の研究課題は、**共通FivefoldEdgeに対する自然な型付き関手/ファイバーed descent**の必要十分条件、元F55 P77証拠とCat NatIsoの橋が`full/faithful`になる正確な条件、元GK5CG有限付加5-cellとのauthority境界の形式化。数値一致を証拠代用にしない。

Fixed Lean `v4.30.0-rc2`, mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`; original public roots107, `KuuOSFormal` unique public import, strict 空 centered, independent Kuu one presentation, no Gray, append-only/tighten-only/same-root/overwrite-forbidden, protected #1558 Draft/open/unmerged.

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
