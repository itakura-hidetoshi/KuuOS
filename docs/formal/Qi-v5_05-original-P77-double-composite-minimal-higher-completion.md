# Qi v5.05 — 合成逆元消去の独立八セル最小補完と法4降下

## 0. Canonical正本・exact-source Lean検証

2026年11月7日 JST。Repository `itakura-hidetoshi/KuuOS`、canonical `main`。
前段のQi v5.04統合正本 `be16e47b6a90862274b4bfe2b7a9524aebcd212d` を継承する。

| 検証項目 | 完了結果 |
|---|---|
| 定理PR | [#3233](https://github.com/itakura-hidetoshi/KuuOS/pull/3233) **MERGED** |
| 定理squash SHA | `ff405462d271eae6d1f0466cbb5d5017c0527f3b` |
| exact-source CI | [#42317162670](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42317162670) **SUCCESS** |
| Strict Lean | **10,304 / 10,304 SUCCESS** |
| Governance | **30 / 30 SUCCESS** |
| 新規宣言の公理監査 | **42宣言**、標準公理 `propext`、`Classical.choice`、`Quot.sound`のみ、または公理不要 |
| `sorryAx` | **なし** |
| 変更Lean warning/error | **0 / 0** |
| exact-source HEAD | `45a0afb5dccd797706a1f69a64747567c5b4fdda` |
| test-merge HEAD | `e191eb63e70f76fcf8bdabaf3f8e7a5fec738a2f` |
| source/test-merge Git tree | **`e7d00aa9c1a667666ae0ec595a128146e41284a5` 完全一致** |
| 固定Lean / mathlib | `v4.30.0-rc2` / `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開集約・root | `KuuOSFormal`、**107維持** |
| 保護PR #1558 | Draft／OPEN／未マージ（維持） |

[Qi v5.05 Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77DoubleCompositeMinimalHigherCompletionV5_05.lean) ·
[Qi v5.04正式記録](Qi-v5_04-original-P77-double-composite-cancellation-residual-obstruction.md)

## 1. 前段Qi v5.04で確定した真正obstruction

旧`BalancedUnitEightCell`の全比較構成子で、
左右単位則と左右逆元消去の符号付き合計回数を数える整数

```text
V(H) = sevenTotalReductionCharge(H)
```

が厳密に保存されることはQi v5.04で証明されている。

元の自由六セルraw構文の同一始終点を持つ二つの真正七セルType値履歴

```lean
sevenDoubleCompositeCancelFirst w
sevenDoubleCompositeCancelSecond w
```

は、次の性質を同時に持つ。

```text
                                 First       Second
残余 R mod 2                     0           0
単位則 U mod 2                   0           0
合計消去整数 V                   2           6
元六セルのraw始終点              同一        同一
```

そのため元`BalancedUnitEightCell`ではいかなる比較も存在しないことを
`sevenDoubleCompositeCancel_noComparison`が保証する。
今回の新比較はこの**構成済みのobstructionにだけ**依拠する。

またQi v5.04の`sevenParallelParityCoupling`により、
同じ元六セル始終点を持つ任意の平行七セル履歴では
R mod 2の一致とU mod 2の一致が同値である。
二つのBool値は商上に存在しても、固定された始終点の下で独立な二ビットではない。

## 2. 独立DoubleCompositeEightCellの最小追加

前段の`BalancedUnitEightCell`を**改変せず**、新しい型付き
`DoubleCompositeEightCell`を独立に構成した。

新しい**原始比較生成元は一種類のみ**である。

```lean
DoubleCompositeEightCell.doubleComposite (w : W)
```

これは`sevenDoubleCompositeCancelFirst w`と
`sevenDoubleCompositeCancelSecond w`を始終点とする。
元の六セル・七セルType値はそのまま使う。

- `previous`は、前段の全`BalancedUnitEightCell` Type値証拠を保存する。
- `reverse`と`chain`は比較の反転・連接を与える。
- `whiskerLeft`、`whiskerRight`、`inverseContext`、
  `compositeContext`は元の型付き文脈閉包を与える。

元F55/P77/GK5CG source、旧独立presentation、旧高次商、
元七セル証拠履歴の原始構文は一切変更しない。

`doubleCompositeEightCell_strictlyNew`と
`doubleCompositeEightCell_noPreviousInterpreter`により、
新比較は旧presentationでは不可能だった真正な追加であると確認した。
新比較から元の七セル自由構文の厳密なEqも導けない。

## 3. 商の厳密な粗化

新しく`doubleCompositeHistorySetoid`と
`doubleCompositeHistoryClass`を構成した。
旧classの一致は新classへ降下するが、新比較による一致から旧class一致へ戻す
普遍的操作は存在しない。

```text
[H_first]_(Qi v5.05) = [H_second]_(Qi v5.05)
[H_first]_(Qi v5.03) ≠ [H_second]_(Qi v5.03)
```

これは単に「未探索だから旧比較不能」という主張ではない。
Qi v5.04で証明した整数Vの全旧比較保存定理と2対6の差を利用した
**具体的な比較不能性の証明**である。

`doubleCompositeHistoryClass_noPreviousReturn`、
`doubleCompositeHistoryClass_noStrictReturn`も形式証明済みである。

## 4. 整数Vの非降下とV mod 4の真正降下

新原始生成元は整数V=2とV=6の七セル履歴を比較するため、
整数Vは新商へは降下しない。

```text
V(H_first) = 2, V(H_second) = 6
しかし [H_first]_new = [H_second]_new
整数Vは新商上の代表元独立な観測量にはならない。
```

一方、今回の新比較によるVの差は正確に4である。

```text
V(H_first) mod 4 = 2
V(H_second) mod 4 = 2
```

前段の全比較は整数Vを厳密に保存する。
新原始比較もV mod 4を保存し、残りの型付き文脈への保存は
構造帰納法と整数剰余演算によって証明した。

```lean
doubleCompositeEightCell_preservesTotalReductionResidue
doubleCompositeHistoryV4
doubleCompositeHistoryV4_onClass
doubleCompositeHistoryClass_noIntegerVDescent
```

新商上の観測量`doubleCompositeHistoryV4`は
`Quotient.lift`により真正に構成し、単に代表元を選んで値を割り当てていない。

さらに旧R mod 2およびU mod 2についても、
全新比較構成子での保存と、別々のBool値`Quotient.lift`を形式証明した。

```lean
doubleCompositeEightCell_preservesParity
doubleCompositeEightCell_preservesUnitCountParity
doubleCompositeHistoryParity
doubleCompositeHistoryUnitCountParity
```

RとUの偶奇連動性について前段の境界条件を保持している。

## 5. 混合critical pairの局所比較

新`doubleComposite`を旧`balancedUnit`、
および旧`unitDiamond`と型付き横合成し、
次の二つの真正七セル平行履歴対を構成した。

- `doubleComposite × balancedUnit`
- `doubleComposite × unitDiamond`

いずれも旧v5.03`BalancedUnitEightCell`では
整数Vの値に差4が残るため比較不可能である。
しかし新`DoubleCompositeEightCell`では、
**唯一の新原始生成元**と、
既存の`previous`比較証拠の`compositeContext`だけで合流できる。

この事実を`mixedDoubleCompositeBalanced_newVsOld`と
`mixedDoubleCompositeUnit_newVsOld`で形式化し、
その二つを含む限定`DoubleCompositeCriticalPeak`族の全構成子について
`doubleCompositeCriticalPeak_fill`で実際の型付き比較証拠を構造帰納的に構成した。

これは任意の平行七セル履歴の大域完全合流を主張するものではない。

## 6. 真正P77 sourceへの輸送とstrict Eqの境界

元の`pentagonAdjoinedSixCell_generator`をそのまま用い、
二つの合成逆元消去七セル履歴へ同じ真正GK5CG source六セルを貼った
`doubleCompositeSource_fill`を構成した。

`pentagonActualDoubleCompositeCompletionWithSourceObstruction`では
任意の元P77最終raw添字について、次を同時に示す。

- 新`DoubleCompositeEightCell`には型付き比較証拠がある。
- 同じ七セル二端点に対する旧`BalancedUnitEightCell`比較証拠は存在しない。
- 既証明のR mod 2とU mod 2の一致は維持される。
- 元GK5CG sourceの`PentagonAdjoinedSixCellEqualityInterpreter`は存在しない。

新しい商のEqは、元sourceの厳密Eqを意味しない。
独立Kuu、strict空、元F55/P77/GK5CG sourceのauthority境界は不変である。

## 7. Lean4初回エラーの構造理由と修正

初回PR HEAD `82f5178820358c8a451160799e28c387d8553d86`の
CI [#42316761503](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42316761503)
は、新モジュールの`doubleCompositeHistoryClass_eq_iff`における
タクティク構文`intro h => exact`が受理されなかったため失敗した。

この記法は`by`内の箇条書きタクティクとして解釈されず、
途中のゴールが残ることで後続の商に関する公理監査へ
`sorryAx`が連鎖する状態だった。

該当箇所を

```lean
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h
```

と修正した。型・仮定・証明対象は変更していない。
修正版HEAD `45a0afb5dccd797706a1f69a64747567c5b4fdda`で
全42宣言が標準公理のみ・`sorryAx`なし、変更警告・エラー0件となり、
Strict Lean 10,304/10,304とsource/test-merge tree一致も検証した。

## 8. 未証明事項と次段階Qi v5.06

本段階で証明していない事項を明確に保持する。

- 任意の平行七セル履歴の比較可能性・完全な高次obstruction分類
- V mod 4とR/U mod 2の一致から新比較が必ず存在する十分性
- 元F55/P77/GK5CG strict Eqと独立高次商Eqの同一視
- 九セル以上の存在、大域thin性、元の自由履歴Typeの縮約
- 他の臨界組に対する無条件な合流

次のQi v5.06では、今回残った`V mod 4`と既存R/U偶奇の境界を観測し、
**新presentationの全比較構成子を先に調べる**。
具体的な比較不能性が形式的に示されたときだけ、
別の独立presentationへの新原始比較の最小追加を検討する。

append-only／tighten-only／overwrite-forbidden／same-root。
公開root107、保護PR #1558 Draft／OPEN／未マージを維持する。
