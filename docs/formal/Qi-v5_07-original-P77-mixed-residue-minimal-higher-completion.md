# Qi v5.07 — 混合逆元補償の独立八セル最小補完と法2降下

## 0. 正本とexact-source Lean検証

2026年11月7日 JST。Repository `itakura-hidetoshi/KuuOS`、canonical branch `main`。
基点はQi v5.06定理・正式記録統合済み正本 `9c294398ffd82916c2747c9204707c3e97ff91ad`。

| 検証項目 | 確認結果 |
|---|---|
| 定理PR | [#3237](https://github.com/itakura-hidetoshi/KuuOS/pull/3237) **MERGED** |
| 定理squash SHA | `e1f28b9604a5c4b280032992194bb5f3e3db52bc` |
| exact-source CI | [#42332928280](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42332928280) **SUCCESS** |
| Strict Lean | **10,306 / 10,306 SUCCESS** |
| Governance | **SUCCESS**（全job完了・失敗なし） |
| 新規宣言の公理監査 | **43宣言**、標準公理 `propext`・`Classical.choice`・`Quot.sound`または公理不要 |
| `sorryAx` | **なし** |
| 変更Lean warning/error | **0 / 0** |
| 正式検証source HEAD | `6cfe6e89d70c97d3d3c2fc7715fefde22894453e` |
| test-merge HEAD | `6bf9c9c1a427054064206a598c247c51a876e7ae` |
| source/test-merge Git tree | **`441eed24f72db0387e8688eca09e03e0cc24a36b` 完全一致** |
| 固定Lean / mathlib | `v4.30.0-rc2` / `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開集約・root | `KuuOSFormal`、**107維持** |
| 保護PR #1558 | Draft／OPEN／未マージ維持 |

[Qi v5.07 Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77MixedResidueMinimalHigherCompletionV5_07.lean) ·
[前段Qi v5.06正式記録](Qi-v5_06-original-P77-mixed-inverse-compensation-Vmod4-obstruction.md)

## 1. Qi v5.06で証明済みの真正obstruction

元の13構成子からなる型付き自由`SevenRewrite`の元六セル始終点が等しい二履歴

```lean
sevenMixedResidueFirst w
sevenMixedResidueSecond w
```

について、Qi v5.06で以下を形式証明している。

```text
観測量                         First         Second
旧三整数 (T,J,K)               (2,0,1)       (2,0,1)
旧第四整数 R mod 2             0             0
旧単位則整数 U mod 2           1             1
元合計消去整数 V               3             5
元 V mod 4                     3             1
元六セルraw始終点              同一          同一
```

旧選択`DoubleCompositeEightCell`は全構成子・型付き文脈で
`V mod 4`を保存するため、この二履歴に関する旧八セル比較は**存在しない**。
これは探索上の不発ではなく、3と1の異なる真正剰余値に基づく非存在定理である。

## 2. 新しい独立MixedResidueEightCell Type

元`DoubleCompositeEightCell`、元source、元七セル生構文は一切変更せず、
独立の`MixedResidueEightCell` Typeを導入した。

追加する**新原始八セル生成元は一種類だけ**である。

```lean
MixedResidueEightCell.mixedResidue (w : W)
```

この生成元の添字は、元v5.06の証明済み真正履歴
`sevenMixedResidueFirst w`と`sevenMixedResidueSecond w`そのものである。
既存の全`DoubleCompositeEightCell` Type値証拠は`previous`で包含する。
ほかは`reverse`、`chain`、`whiskerLeft`、
`whiskerRight`、`inverseContext`、`compositeContext`という
型付き比較の通常の閉包のみを持つ。

`mixedResidueEightCell_strictlyNew`は、新しいType値比較が存在する一方、
旧`DoubleCompositeEightCell`比較は存在しないことを同時に示す。
`mixedResidueEightCell_noPreviousInterpreter`および
`mixedResidueEightCell_noStrictInterpreter`によって、
新比較をすべて旧比較や元自由七セルの厳密Eqへ戻すことはできない。

## 3. 新商の厳密な粗化と観測量降下の境界

`mixedResidueHistorySetoid`と`mixedResidueHistoryClass`を別に構成した。
旧商でのclass一致は新商へ一方向に降下するが、
その逆の普遍的な復元は不可能である。

```text
[H_first]_(Qi v5.07) = [H_second]_(Qi v5.07)
[H_first]_(Qi v5.05) ≠ [H_second]_(Qi v5.05)
```

新原始比較の両側は`V mod 4 = 3`と`V mod 4 = 1`なので、
旧整数Vの法4剰余`sevenTotalReductionResidue`は新商へ降下しない。

一方、両側の`V mod 2`はともに1である。
新しい`sevenTotalReductionParity`を
`(V mod 4) mod 2`として構成し、全`MixedResidueEightCell`生成元と
型付き文脈閉包で保存されることを構造帰納法で証明した。

同様に、旧R mod 2とU mod 2の保存も全新構成子で証明した。
前段v5.04の`sevenParallelParityCoupling`が示した
固定六セル始終点でのR/U偶奇連動も保持する。

次の三つのBool値観測量を**それぞれ真正`Quotient.lift`で構成**した。

```lean
mixedResidueHistoryVParity
mixedResidueHistoryParity
mixedResidueHistoryUnitParity
```

元`V mod 4`を代表元に依存した形で復活させたり、
元sourceの厳密Eqと新高次商Eqを同一視する操作はしていない。

## 4. 二種類の混合critical pair

証明済みの新`mixedResidue`比較を、
旧`doubleComposite`および旧`unitDiamond`の真正比較証拠と
型付き横合成して、二つの新しい局所混合critical pairを構成した。

- `mixedResidue × doubleComposite`
- `mixedResidue × unitDiamond`

各pairは旧`DoubleCompositeEightCell`において
`V mod 4`の3対1の残差を持ち、比較不可能。
新`MixedResidueEightCell`では、唯一の新原始比較と
既存の`previous`および`compositeContext`で比較証拠を構成できる。

さらに限定`MixedResidueCriticalPeak`族には、
元v5.05の限定critical family、今回の新原始比較、二つの混合比較、
反転・連鎖・型付き文脈閉包を含めた。
`mixedResidueCriticalPeak_fill`は**この限定族の全構成子**について
真正なType値比較証拠を構造帰納法で構成した。

任意の平行七セル履歴の比較可能性、大域thin性、
九セルの存在は、この結果からは主張しない。

## 5. 真正P77 sourceへの輸送

元GK5CGの真正六セルsource証拠`c`を保存して、
次の二つの七セル平行履歴を構成した。

```lean
sevenMixedResidueCompositeFirst c
sevenMixedResidueCompositeSecond c
```

新`mixedResidueSource_fill`は、その同じ元source`c`を両側に用いて、
新高次比較のType値証拠を構成する。

`pentagonActualMixedResidueCompletionWithSourceObstruction`は、
**任意の真正P77最終raw添字**で次を同時に保証する。

1. 新`MixedResidueEightCell`比較が存在する。
2. 同じ七セル二端点に関する旧`DoubleCompositeEightCell`比較は存在しない。
3. 元三整数とR/U偶奇は両側で一致する。
4. 元GK5CG sourceの`PentagonAdjoinedSixCellEqualityInterpreter`は存在しない。

旧F55/P77/GK5CG source、strict空、独立Kuuのpresentationとその証拠履歴は
変更しない。新商のEqは元sourceのstrict Eqではない。

## 6. Lean4エラーの構造的原因・修正と監査

初回PR HEAD `f7c0b582ee5a4cff8441be1de534a2dda953d086`の
exact-source CI [#42332594166](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42332594166) は
二つの混合critical pair定理の**結論部分で暗黙引数long/shortが未確定**
だったため失敗した。後続の`#print axioms`では
型付け不能によって二つの定理が`Unknown constant`と報告された。

変更Lean全文、全imports、v5.05とv5.06の型付き依存署名を照合し、
該当二つの結論に
`(long := long) (short := short)`を明示した。
仮定、新原始比較、元sourceおよび数学的な結論は変更していない。

修正版HEAD `6cfe6e89d70c97d3d3c2fc7715fefde22894453e`のCIは
**10,306/10,306 SUCCESS**。
43宣言の公理依存は標準公理のみ、`sorryAx`なし、
変更warning/error0/0、source/test-merge treeの完全一致を確認した。

## 7. 未証明事項と次段階

この段階で次を仮定・証明していない。

- 任意の平行七セル履歴の比較存在、大域thin性、九セルの存在
- R/UおよびVの残余偶奇が一致すれば比較が存在する十分性
- 全高次obstructionの完全分類
- 元F55/P77/GK5CG sourceの厳密Eqへの昇格
- 以前の独立高次presentationや商の上書き

次の段階では、現行新presentationの全生成元が保存する観測量を再度調べ、
新規の比較不能性が**構成的に証明された場合に限り**
別の独立presentationへの最小局所補完を検討する。

append-only／tighten-only／overwrite-forbidden／same-root。
公開root107、保護PR #1558 Draft／OPEN／未マージを維持する。
