# Qi v3.5 — 共通五相による五行・真正C60五角形・GK5五角形のプログラム統合

**Date:** 2026-11-02 JST  
**Theorem PR:** [#2950](https://github.com/itakura-hidetoshi/KuuOS/pull/2950) **MERGED**  
**Theorem squash/main SHA:** `5a6b2bf18ea57a41a1eea40985bba1127b3cbf42`  
**Canonical Lean:** [QiWuxingPentagonUnifiedV3_5.lean](../../formal/KUOS/Architecture/QiWuxingPentagonUnifiedV3_5.lean)  
**Exact-source CI:** [#41415829263](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41415829263) — PR Governance Strict Lean **10133/10133 SUCCESS**、Independent Kuu、workflow integrity、Governance全30 jobs SUCCESS。8/8公開`#print axioms`標準`propext/Classical.choice/Quot.sound`のみ、`sorryAx0`。Lean v4.30.0-rc2、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。

## 統合の意味

**三つの異なる型を無条件に等号で潰さず、プログラム上の座標を同一の `FivePhase = ZMod 5` にする。**

- **Qi五行:** 相生 `p ↦ p+1`、相剋 `p ↦ p+2`。元の型付き生成履歴と観測商の違いはv3.1–v3.3を保持。
- **C60真正五角形:** 原来の12五角形 `v : Vertex` の各5個の実スロットに対し、任意の局所ゲージ `frame(v)` の下で `fivefoldSlotEquiv frame v : FivePhase ≃ Slot` を構成。これは**全単射の証明を持つ真正型同値**。さらに `slotNext(fivefoldSlotEquiv p) = fivefoldSlotEquiv(p+1)`、真正`incidentDart`・`Edge.around`の両端一致を証明。
- **GK5高次圏論の五角形:** 4個の真正Mathlib圏同値の5括弧付け `P0..P4` を同じ `FivePhase` の `0..4` へ割当て。これは選択した**明示的な位相座標**であり、圏同値レコードの自動的な等号ではない。`fivefoldBracket` の5通りの式をLeanで保証。
- **共通の5辺:** `FivefoldEdge` の `01,12,23,04,43` を、物理側の実`Edge.around`と圏論側の真正whole `NatIso`の両方に与える。幾何学的順方向の`+1`巡回に対して、`04`と`43`は逆向きの実辺を使用。`fivefoldPhysicalEdge_joins`が元のC60ダート両端の一致を証明。
- **高次整合性:** `fivefoldCategoricalPentagon`は実`NatIso`に関する3辺対2辺の五角形等式。`fivefoldDirectPhi_allEdges` はGK5Yの5つの独立した再帰的direct Phiのwhole NatIso四角が**全部**可換となることを、統一した辺型で再証明。

```text
                 single canonical FivePhase = ZMod 5
                        (phase p)
             ┌──────────┼───────────┐
             │          │           │
         Qi phase    C60 real    GK5 bracket P(p)
           +1,+2     Slot/Dart   genuine equivalence
                        │           │
                        └── FivefoldEdge ──┘
                     actual Edge    whole NatIso
                       endpoint     5-edge coherence
```

## 五つの正確な位相対応

| 位相 | Qi v3.1相生順（名前は世俗的ラベル） | 真正C60スロット（ゼロゲージ） | GK5X括弧付け |
|---|---|---|---|
| 0 | 木 | s0 | P0 = (((eg)h)k) |
| 1 | 火 | s1 | P1 = ((e(gh))k) |
| 2 | 土 | s2 | P2 = (e((gh)k)) |
| 3 | 金 | s3 | P3 = (e(g(hk))) |
| 4 | 水 | s4 | P4 = ((eg)(hk)) |

五角形の辺の向きは`0→1→2→3`、および`0→4→3`（後半二辺は物理円周の逆向き）。五行の順序と五角形括弧付けの付番は**指定した座標系による同期**であり、五行の伝統的意味から圏同値を導出したのではない。

## 権限・証明境界

**証明したのは、共通型・正確な局所座標同値・真正幾何辺への対応・真正NatIso辺への対応および全五辺pentagon coherence。**

`FivePhase`、`Slot`、`Dart`、`Edge`、`Equivalence`、`NatIso` は異なる対象のままです。数学的に異なるものを不適切に`rfl`とすること、original F54/F55/P92B Type値3/4-cellを新しく生成すること、`FivefoldEdge`を元証拠そのものとすること、global strict 3/n・unrestricted hyperdescent、五行が臨床効果を示すことなどは一切主張しません。数学的意味が同一になるには追加の比較定理が必要です。

GK5Zまでの既存source・正本root107・保護PR #1558 Draft/open・strict空中心／独立Kuu一presentation・旧no-goを保持。新ファイルと既存`KuuOSFormal`への**1 import追加**のみで、旧定理・定理型は変更していません。

## Lean4エラー原因と修正

初回exact-source CI #41415374994は、`fivefoldSlotEquiv`関数包みが`nativeC60GaugeSlot`の書換えパターンに定義的に展開されず1件、`norm_num`だけでは`ZMod 5`の数値不等を繰り返し`if`から消去できず4件、計5件で不成功。`change`による正確な型付き展開、`by decide`による数値不等の明示補題へ修正。元の命題を弱めず、追加公理・`sorry`なし。最終exact-source CI #41415829263は10133/10133 SUCCESS、変更Lean error/warning0/0。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
