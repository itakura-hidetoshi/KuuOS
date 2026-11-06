# Qi v5.03 — 強いP77 source輸送と整数U障害の独立八セル最小補完

## 0. Canonical正本とexact-source検証

2026年11月7日 JST。Repository `itakura-hidetoshi/KuuOS`、canonical branch `main`。
Qi v5.02までの統合済み正本 `8da730774fbc6d3be31c0f7dca20758ca0360872` を継承する。

| 検証項目 | 完了結果 |
|---|---|
| 定理PR | [#3229](https://github.com/itakura-hidetoshi/KuuOS/pull/3229) **MERGED** |
| 定理squash SHA | `35faf7d984855cca947c663fa76aaf70f1123c0d` |
| exact-source CI | [#42311449662](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42311449662) **SUCCESS** |
| Strict Lean | **10,302 / 10,302 SUCCESS** |
| Governance | **30 / 30 SUCCESS** |
| 新規宣言の公理監査 | **40件**、標準公理 `propext`・`Classical.choice`・`Quot.sound`のみ、または公理不要 |
| `sorryAx` | **なし** |
| 変更Lean warning/error | **0 / 0** |
| source HEAD | `f5370e8fc73731893afa00bb6992fb7f18fd987d` |
| test-merge HEAD | `01b5ed0d27f0073a07cb781dc1f9eef89bd0e44f` |
| source/test-merge Git tree | **`b422242b920e9940de6cae716a01e99dc80c8b0b` 完全一致** |
| Lean / mathlib | `v4.30.0-rc2` / `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開集約・root | `KuuOSFormal`、**107維持** |
| 保護PR #1558 | Draft／OPEN／未マージ（維持） |

[Qi v5.03 Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77BalancedUnitMinimalHigherCompletionV5_03.lean) ・
[前段Qi v5.02正式記録](Qi-v5_02-original-P77-balanced-inverse-unit-count-obstruction.md)

## 1. v5.02から継承した真正障害

Qi v5.02では、元の13構成子をもつ`SevenRewrite`型の七セル履歴について
`sevenUnitStepCharge : SevenRewrite ... → ℤ`という符号付き整数Uを構成した。
左右単位則生成元を各+1、反転で負、型付き縦横合成で加法とし、
旧v5.01 `UnitDiamondEightCell`の**全構成子で保存**されることを証明した。

同じ元のraw六セル始終点を持つ二つの真正三因子履歴

```lean
sevenBalancedUnitInvisibleFirst w
sevenBalancedUnitInvisibleSecond w
```

は次を満たす。

```text
                         H_first       H_second
元三整数 (T,J,K)           (1,0,0)       (1,0,0)
第四整数 R mod 2          0             0
単位則整数 U              1             3
raw六セル始終点           同一          同一
```

よって旧v5.01の比較全体でUが保存されるため、
`UnitDiamondEightCell(H_first,H_second)`は存在しない。
今回はこの**証明済みの局所比較不能性だけ**を新しい独立presentationで補完する。

## 2. 強い三因子障害の真正P77 sourceへの輸送

v5.02のP77定理で輸送できていたのは、左右逆元消去を結んだ
**二因子前駆例**だった。前駆例は第四整数Rの偶奇が一致しても、
元三整数のTには1対0の差が残る。

今回新たに

```lean
sevenBalancedStrongSourceFirst c
sevenBalancedStrongSourceSecond c
sevenBalancedStrongSource_values c
sevenBalancedStrongSource_noPrevious c
```

を構成した。任意の真正六セルsource証拠`c`に、
三角形critical pairによるT相殺を含む**強い三因子履歴**を
横合成したものである。

両者はraw六セル始終点が完全一致し、元三整数とR偶奇が一致する。
その一方、整数Uは1対3で異なるため、旧八セルでは比較不能である。

さらに`pentagonActualStrongBalancedUnitCompletionWithSourceObstruction`は、
**任意の真正P77最終raw添字**に対し、
`pentagonAdjoinedSixCell_generator`を使ってこの強い証拠を輸送する。
旧GK5CG五セルのType値sourceとその証拠履歴は一切変更せず、
`¬ PentagonAdjoinedSixCellEqualityInterpreter`を保持する。

## 3. 独立BalancedUnitEightCell — 原始比較は1種類

別の新`Type`値presentationとして

```lean
inductive BalancedUnitEightCell (W : Type uSix) (l r : W) : ...
```

を構成した。原始的に**新しく追加した比較は1種類だけ**である。

```lean
BalancedUnitEightCell.balancedUnit (w : W)
```

その添字は元v5.02で証明済みの
`sevenBalancedUnitInvisibleFirst w`と
`sevenBalancedUnitInvisibleSecond w`の二つであり、
新しい根拠なしの一般比較・source strict Eqを追加していない。

全旧`UnitDiamondEightCell`証拠は`previous`によって保存される。
残る`reverse`、`chain`、`whiskerLeft`、`whiskerRight`、
`inverseContext`、`compositeContext`は従来と同じ型付き文脈閉包だけである。

旧presentationの定義、旧quotient、自由七セルraw文法、
元F55/P77/GK5CG sourceおよび証拠履歴は変更していない。

## 4. 商の厳密な粗化と保存量の降下境界

新選択商は`balancedUnitHistorySetoid`と
`balancedUnitHistoryClass`により構成し、実際の
`BalancedUnitEightCell`証拠を`Nonempty`で保持する。

```text
[H_first]_new  = [H_second]_new
[H_first]_old ≠ [H_second]_old
```

旧v5.01 classの一致は新classの一致に降下するが、その逆の
普遍解釈は存在しないことを具体的な証拠で示した。

今回は新`balancedUnit`生成元で整数Uが1→3に変化するので、

```text
整数Uは新商へ降下しない。
一方、U mod 2 と R mod 2 は両方新商へ降下する。
```

次のLean定理を**全新比較構成子についての帰納法**で証明した。

```lean
balancedUnitEightCell_preservesParity
balancedUnitEightCell_preservesUnitCountParity
balancedUnitHistoryClass_noIntegerUnitDescent
```

真正な新商上で`Quotient.lift`を使い
`balancedUnitHistoryParity`と
`balancedUnitHistoryUnitCountParity`という
**二つのBool値観測量**を構成した。

重要なのは、Uという整数値を強引に新商の代表元に依存した形で
定義していない点である。旧整数Uの非降下と残余偶奇の降下は分離している。

## 5. 混合critical pairと限定局所合流

新`balancedUnit`と既存の二つの比較生成元を横合成した
実際の型付き混合critical pairを構成した。

- `balancedUnit × identityDouble`
- `balancedUnit × unitDiamond`

いずれも旧v5.01の比較ではU値の差が2のため不可能である。
新`BalancedUnitEightCell`では**唯一の新原始比較**と
既存`previous`証拠の`compositeContext`によって比較できる。

限定`BalancedUnitCriticalPeak`は旧選択critical family、
この新原始比較、二種類の混合比較と型付き反転・連鎖・文脈を含む。
`balancedUnitCriticalPeak_fill`は**その限定族の全構成子**に
真正なType値比較を構造帰納的に与える。

これは任意の平行七セル履歴の完全合流、大域thin性、
九セル構成の存在を意味しない。

## 6. CIの確認と変更範囲

新規Leanモジュール1件と`formal/KuuOSFormal.lean`の公開import1行のみを変更。
元のLean証明とsourceファイル、全旧presentationを上書きしていない。

exact-source CI #42311449662では、固定Lean/mathlibと
`-DwarningAsError=true`・`-DsorryAsError=true`で
`KuuOSFormal`と新モジュールのビルドが
**10,302/10,302 SUCCESS**となった。
新40宣言の全`#print axioms`に非標準公理や`sorryAx`はない。
変更警告・エラーなし、source/test-merge Git tree一致も独立確認済み。

## 7. 未証明事項と次段Qi v5.04

本段階では次の点を**証明していない**。

- 任意の平行七セル履歴の比較可能性・障害の完全分類
- R mod 2とU mod 2の同時一致からの無条件な比較存在
- 九セル以上の大域thin性や元sourceのstrict Eqへの昇格
- 全高次比較Type値を薄いPropへ縮約すること

次のQi v5.04では、残った二つのBool値観測量の組
`(R mod 2, U mod 2)`で判別できない真正な比較不能例の有無を、
現行新presentationの全構成子を先に照合して調べる。
**新原始生成元は具体的な非比較性が証明された場合に限り**
別の独立presentationへ最小追加する。

append-only／tighten-only／overwrite-forbidden／same-root、
公開root107、保護PR #1558 Draft／OPEN／未マージを継続する。
