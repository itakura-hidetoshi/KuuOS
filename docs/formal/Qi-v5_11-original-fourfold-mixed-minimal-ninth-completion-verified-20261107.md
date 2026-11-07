# Qi v5.11 — 真正四重五角形 × mixedResidue の独立最小九セル・出現回数降下・残余障害

## 0. 正本と再現可能な検証記録

2026年11月7日 JST。Repository `itakura-hidetoshi/KuuOS`、canonical branch `main`。
Qi v5.10（定理 #3272／記録 #3273）の真正原四重五角形critical diamondを継承し、選ばれた二本の**生の八セル完成経路**の間にただ一種類の独立した九セル比較を追加した。

| 項目 | 正式結果 |
|---|---|
| 定理PR | [#3274](https://github.com/itakura-hidetoshi/KuuOS/pull/3274) **MERGED** |
| 定理squash | `b997e8368e80fea444f6422da8dd2135f856180c` |
| Exact-source CI | [#42376080358](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42376080358) **SUCCESS** |
| Strict Lean | 選択対象・公開集約とも **SUCCESS** |
| Governance | **30 / 30 SUCCESS** |
| 26新規宣言の `#print axioms` | 標準公理 `propext`・`Quot.sound`（または公理不要） |
| `sorryAx` | なし |
| 変更Lean error／warning | 0／0 |
| 検証source HEAD | `9077c36485605926386791882e2037d4f92e7eef` |
| test-merge HEAD | `73894cc37ce6f942642de74202d5cdf6991ce8aa` |
| Git tree一致 | `c65f8302cb1d9440c1f41df258761cd1ab823532` |
| Lean / mathlib | `v4.30.0-rc2` / `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開集約・root | `KuuOSFormal`、**107維持** |
| 保護PR | #1558 Draft／OPEN／未マージ |

[Qi v5.11 Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77FourfoldMixedMinimalNinthCompletionV5_11.lean) · [Qi v5.10 正式記録](Qi-v5_10-original-fourfold-mixed-critical-diamond-verified-20261107.md)。

## 1. 元八セル証明Typeと唯一の新九セル生成元

同じoriginal sourceの自由六セル二端点上で、Qi v5.10が構成した

```lean
fourfoldMixedCriticalPThenM l r
fourfoldMixedCriticalMThenP l r
```

は、同じ添字を持つ `PentagonAssocEightCell W l r` の**異なる**生Type値である。
Qi v5.10の定理 `fourfoldMixedCriticalRawEightGap` はこのstrict不等をすでに証明している。

独立Type

```lean
FourfoldMixedNineCell W l r q q'
```

を新たに導入し、**真正な新しい原始比較は** `FourfoldMixedNineCell.interchange` 一種類に限る。その添字は上記の本来の二つの八セル完成経路そのものである。`strict` は八セルの元からのstrict Eqを受け取るだけで、恣意的な証拠の同一視ではない。さらに九セルの向き反転・連鎖、八セル側の反転・連結・左右whisker・逆・合成文脈について型付き閉包を構成した。

`fourfoldMixedNineCell_strictlyNew` は、新九セル比較が存在する一方、元の八セルstrict Eqは成り立たないことを同時に確認する。`fourfoldMixedNineCell_noRawEqualityInterpreter` は九セル比較を全て八セルstrict Eqへ戻す普遍的解釈が不可能であることを証明する。

これは**選択された独立の高次比較文法の構成定理**であって、従来の元F55/P77/GK5CG体系に最初から存在したcanonical九セルcoherenceの発見とは区別する。元の六セル・七セル・八セル定義には手を加えない。

## 2. 選択された九セル商と不可逆性

`fourfoldMixedNinthSetoid` は、同じ七セル二端点を持つ元八セル**証明値同士**の比較をSetoidにする。`fourfoldMixedNinthClass` は、その真正 `Quotient` への射影である。

`fourfoldMixedNinthClass_selectedGap` は

```text
class(PThenM) = class(MThenP)
PThenM ≠ MThenP    -- raw eighth proof Type
```

を同時に証明する。また `fourfoldMixedNinthClass_noRawRetraction` は、この選択商から元の**全ての**生八セル証拠を恒等的に復元する左逆の存在を否定する。

すなわち「商で比較可能」と「元Type値で同一」は異なる。商の同値による元source strict equalityの昇格は行わない。

## 3. 出現順序の非降下と、出現回数の真正降下

Qi v5.10は二つの生証拠の原始イベント列を

```text
PThenM : [true, false]     -- P then M
MThenP : [false, true]     -- M then P
```

と形式証明している。

選択した新九セル商はこの二履歴を同一視するため、`fourfoldMixedNinthClass_noOrderedTraceDescent` により、**順序付き生traceを商の観測量として忠実に降下させることは不可能**と証明した。

しかし各イベント種別 `b : Bool` について、その出現回数

```lean
ninthPrimitiveEventCount b (pentagonAssocPrimitiveTrace q) : Nat
```

を定義し、`ninthPrimitiveEventCount_append`、`ninthPrimitiveEventCount_reverse`、そして**全九セル構成子に対する構造帰納法**
`fourfoldMixedNineCell_preservesEventCount` によって比較可能な証拠間で各出現回数が一致することを示した。

`fourfoldMixedNinthEventCount` は単なる存在主張ではなく、実際の `Quotient.lift` により定義されたNat値観測量である。`fourfoldMixedNinthEventCount_onClass` は代表元計算を証明する。選択された二履歴はそれぞれP一回・M一回であり、いずれも二種別の出現回数が1になる。

重要なのは、**同じ出現回数なら任意の二八セル証拠が九セル比較可能**とは主張していないことである。降下の十分条件と任意比較の存在は別問題である。

## 4. 最小補完の後にも残る真正九セルobstruction

同じ七セル履歴を始終点とする次の二つの生八セル証拠を比較する。

```lean
ninthPentagonRoundtrip l r
  = .chain (.fourfoldPentagon) (.reverse .fourfoldPentagon)

ninthPentagonReflexive l r
  = pentagonAssocEightCell_refl (sevenFourfoldInversePentagonThree l r)
```

両者のP出現回数は、それぞれ**2と0**である。

`ninthPentagonRoundtrip_noNineComparison` は、出現回数が九セルの全構成子で不変であることから、その二者間には今回選択した `FourfoldMixedNineCell` が存在しないと証明する。`ninthPentagonRoundtrip_distinctClass` は新商でも両者が異なることを示す。`fourfoldMixedNineCell_notGloballyThin` は、任意の同じ端点を持つ元八セル証拠に普遍的な九セル比較を与える解釈の存在を否定する。

このobstructionは**今回の自由九セル文法に関するもの**である。新しい、さらに豊かな高次文法での別個の比較を普遍的に禁止するわけではない。

## 5. 元P77/GK5CGと観測境界

`pentagonActualFourfoldMixedNinthCompletion` により、任意の真正最終P77 raw index `i` に対し、実際の

```text
pentagonLongConservativeFiveCell ... i
pentagonShortConservativeFiveCell ... i
pentagonFinalConservativeLoop ... i
```

を用いて新九セル比較のType値存在を構成した。従来の `¬ PentagonAdjoinedSixCellEqualityInterpreter ... i` も同時に保持している。

`fourfoldMixedNineCell_observationCompatibility` は、もとの選択された七セル二端点に関するV/R/Uの法2観測量保存を維持する。

新しい第九セルの比較導入により、元のF55/P77/GK5CGの自由証拠値、Qi v5.09旧八セル商、元sourceのstrict Eqが書き換わることはない。

## 6. Lean4初回エラーと構造を保持した修正

初回CI [#42375772805](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42375772805) は `ninthPrimitiveEventCount_append` の空リスト基底で `rfl` が失敗。理由は `0 + n = n` が自動的にdefinitional equalityとして縮約されるとは限らないためである。これは数学的な帰納構造の欠陥ではなく、Lean4での加法正規化の不足だった。

その基底だけを

```lean
| nil => simp only [List.nil_append, ninthPrimitiveEventCount, Nat.zero_add]
```

へ修正したHEAD `9077c36485605926386791882e2037d4f92e7eef` を再検証し、CI #42376080358が全体SUCCESS。元定義・仮定・証明対象・他の構成子は修正していない。

## 7. 次の数学的課題：Qi v5.12

最小九セルによって一つのcritical diamondの完成履歴を比較可能にしたが、往復八セルと恒等八セルは依然比較できない。次段階では**往復・単位と新九セルの重なり**を、新しい独立presentationとして調査する。いずれの新比較も真正元の型付き始終点と証明履歴を保持し、局所比較可能性・観測降下・非比較obstructionを区別する。無条件の全局thinness、元source証拠の厳密等号、既存九セルcanonical一致を仮定しない。
