# Qi v5.09 — 真正元P77四重五角形の独立八セル最小補完と残余法2降下

## 0. 正本・再現可能な形式検証

2026年11月7日 JST。Repository `itakura-hidetoshi/KuuOS`、canonical `main`。基点はQi v5.08の真正四重五角形結合子obstructionと、元PR #3238の正本照合までMERGEDのHEAD `64fcd345cc79911ecb25c2070c057f215cad628b`。

| 項目 | 確定結果 |
|---|---|
| 定理PR | [#3270](https://github.com/itakura-hidetoshi/KuuOS/pull/3270) **MERGED** |
| 定理squash | `8b083af64228e20794fe9a07b4814edaa5b748de` |
| exact-source CI | [#42371991526](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42371991526) **SUCCESS** |
| Strict Lean | **10,322 / 10,322 SUCCESS** |
| Governance Gate | **30 / 30 SUCCESS** |
| 27宣言の`#print axioms` | `propext`・`Classical.choice`・`Quot.sound` または公理不要 |
| `sorryAx` | なし |
| 変更Lean warning/error | **0 / 0** |
| 検証source HEAD | `3de09e9ad7f8e5c531b37b66612f8a3ed379be03` |
| test-merge HEAD | `be28e9e03b7474e1e7c367aff479d6a7a73d339c` |
| source/test-merge Git tree | **`ec018c349001e54318585f64f65a624e98382319` 完全一致** |
| Lean / mathlib | `v4.30.0-rc2` / `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開集約・root | `KuuOSFormal`、**107不変** |
| 保護PR #1558 | Draft／OPEN／未マージを保持 |

[Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77FourfoldPentagonMinimalHigherCompletionV5_09.lean) · [前段Qi v5.08正式証明記録](Qi-v5_08-original-P77-fourfold-inverse-pentagon-associator-obstruction.md) · [元PR #3238正本照合記録](Qi-v5_07-PR3238-canonical-V2-parity-reconciliation-verified-20261107.md)

## 1. 真正元ソースの局所obstructionから最小補完へ

元のfree `PentagonAdjoinedSixCell W l r` の唯一の`pentagon:l→r`と生逆元 `symm(pentagon):r→l` から構成した同一raw始終点の2つの真正七セル履歴：

```lean
sevenFourfoldInversePentagonThree l r
sevenFourfoldInversePentagonTwo   l r
```

について、Qi v5.08は **局所結合子指紋Φ=1対0** を証明し、現行 `MixedResidueEightCell` の全比較生成元・型付き文脈で Φ が保存されることから **いかなる旧比較も存在しない** と示した。

同時に両経路の `V mod2`、`R mod2`、`U mod2` はそれぞれ一致する。R/Uは固定raw端点で連動するため、独立な自由三ビットと誤解しない。

## 2. 独立`PentagonAssocEightCell` Type

Qi v5.09は元`MixedResidueEightCell`とその商を**一切編集せず**、完全に独立の`PentagonAssocEightCell W l r s t : Type`を導入する。

新たに付加した**原始比較生成元は一種類だけ**である。

```lean
PentagonAssocEightCell.fourfoldPentagon
```

その添字は上記の真正 `sevenFourfoldInversePentagonThree/Two` そのものである。既存の全`MixedResidueEightCell`証拠は`previous`で型を保ったまま包含。ほかの生成元は `reverse`、`chain`、左右`whisker`、`inverseContext`、`compositeContext` の通常の型付き比較閉包に限定する。

`pentagonAssocEightCell_strictlyNew` は、**新八セル証拠の存在と旧証拠の不存在**を同時に示す。`pentagonAssocEightCell_noPreviousInterpreter`と`pentagonAssocEightCell_noStrictInterpreter`は、それを普遍的に旧八セルや自由七セルのstrict Eqへ戻せないことを証明。

**新しい九セルは存在定理としても原始生成元としても導入していない。** 元F55/P77/GK5CGの五セルType値・元七セル構文・既存独立八セルType・公理は一つも上書きしていない。

## 3. 新商の厳密な粗化とΦ非降下

独立の`pentagonAssocHistorySetoid`、`pentagonAssocHistoryClass`を定義した。旧商のclass一致は新商に一方向へ降下するが、元四重五角形二経路は

```text
[new] H_three = H_two
[old] H_three ≠ H_two
```

を満たすため、新商は旧商より**真に粗い**。

`pentagonAssocHistoryClass_noPhiDescent`によって、v5.08の局所結合子指紋Φは新商へ降下できないことも証明した。新しい比較を加えればΦの障害は解消されるが、`Φ`を代表元に依存しない新商観測量として残すことはできない。

## 4. 三つの残余法2観測量はすべて残る

次の三定理は、新独立八セルの**全構成子**を構造帰納して証明した。

```lean
pentagonAssocEightCell_preservesVParity
pentagonAssocEightCell_preservesRParity
pentagonAssocEightCell_preservesUParity
```

具体的な新`fourfoldPentagon`生成元は、前段で厳密に証明した同端点二履歴の残余一致を利用。従来の全比較は`previous`により定理を継承し、左右whiskering・逆・合成文脈は自由七セルの加法則と法2の整数演算で保存性を示す。

その上で三つの**真正Quotient.lift**を構築した。

```lean
pentagonAssocHistoryV2  -- ℤ値 V mod2
pentagonAssocHistoryR2  -- Bool値 R mod2
pentagonAssocHistoryU2  -- Bool値 U mod2
```

`..._onClass`計算定理3件も元の型付き七セル代表に対して証明済み。#3238から正式統合した`mixedResidueHistoryV2`と、新しい`pentagonAssocHistoryV2`は**異なる商**上の観測量だが、いずれも同じ元七セルの`V mod2`を代表値として持つ。

## 5. 真正mixedResidue局所critical pair

旧の原始生成元`MixedResidueEightCell.mixedResidue(r)`を、新`fourfoldPentagon`と型付き横合成する。

```lean
fourfoldMixedResidueFirst l r
fourfoldMixedResidueSecond l r
fourfoldMixedResidue_fill l r
```

両経路は元の自由六セル上で同一始終点を持つ。現行新商では唯一の新原始比較と旧`mixedResidue`の`previous`像だけで`compositeContext`を構成し**比較可能**。旧商では`mixedResidue`両枝の局所指紋が0に一致する一方、四重五角形因子のΦは1対0なので、**旧全比較生成元のΦ保存性から比較不存在**を証明。

これは具体的な選択mixed critical pairの充填であり、**任意平行七セル履歴の比較可能性やglobal thinnessではない**。

## 6. 真正元P77/GK5CG sourceと限界

`pentagonActualFourfoldPentagonCompletion` は任意の最終raw添字`i`での真正元五セルlong/shortをそのまま引数とする。新八セル比較存在・旧八セル比較不存在・元`PentagonAdjoinedSixCellEqualityInterpreter`不存在を同時に証明した。元のsource五セル値を新しい代理値へ変換せず、独立presentationのEqをsource strict Eqに昇格させない。

本成果は元の自由六セルの**選択した局所obstructionに対する最小の独立八セル補完**であり、一般の任意高次圏のcoherence完成、九セル、全比較、実AIの内部更新を証明したものではない。

## 7. 次段階

Qi v5.10では、今回の独立`PentagonAssocEightCell`の残余法2の背後にあるさらに新しい真正不変量を探索するか、選択した局所critical peakの型付き閉包を拡大する。ただし実際の非比較証明が得られない限り、新しい比較生成元を追加しない。

運用：append-only／tighten-only／overwrite-forbidden／same-root。
