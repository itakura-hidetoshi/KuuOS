# Qi v5.08 — 元P77自由六セル四重五角形・結合子指紋の真正高次obstruction

## 0. 唯一の正本とexact-source検証

2026年11月7日 JST。Repository `itakura-hidetoshi/KuuOS`、canonical `main`。
基点は Qi v5.07 補完定理・正式記録までMERGEDのmain `1d4796b32d42b69b76164430f4542e9cd2141893`。
Qi v5.08 は **新しい高次比較生成元を追加せず**、既存の独立 `MixedResidueEightCell` に残る実際の比較不能性を証明する段階。

| 検証項目 | 確認結果 |
|---|---|
| 定理PR | [#3242](https://github.com/itakura-hidetoshi/KuuOS/pull/3242) **MERGED** |
| 定理squash HEAD | `287dfaacd7129c92af4008bf8def9bf5dc464b63` |
| exact-source CI | [#42337686643](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42337686643) **SUCCESS** |
| Strict Lean | **10,308 / 10,308 SUCCESS** |
| Governance Gate | **30 / 30 SUCCESS** |
| 新規26宣言の公理監査 | **22件**が標準公理 `propext`・`Classical.choice`・`Quot.sound` のみ、**4件**は公理依存なし |
| `sorryAx` | **なし** |
| 変更Lean warning / error | **0 / 0** |
| exact-source検証HEAD | `820a98e84470ec58fa3a8cf5aa2afabbf442d8f9` |
| test-merge検証HEAD | `3bcc8a54328aa0d85965ef171f49d5201475e93e` |
| source/test-merge比較 | 双方向のGitHub compareで**変更ファイル0** |
| Lean / mathlib pin | `v4.30.0-rc2` / `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開集約・root | `KuuOSFormal`、**107維持** |
| 保護PR #1558 | **Draft／OPEN／未マージ** |

[Qi v5.08 Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77InversePentagonAssociatorObstructionV5_08.lean) ·
[Qi v5.07正式記録](Qi-v5_07-original-P77-mixed-residue-minimal-higher-completion.md) ·
[Qi v5.07補完記録](Qi-v5_07-balanced-unit-mixed-peak-integer-V-supplement.md)

## 1. 問題の位置：3つの残余観測量の先へ

前段の独立 `MixedResidueEightCell` は、次の残余観測量をすべての新旧比較構成子で保存する。

```text
V mod 2 — 元七セル合計消去整数の偶奇
R mod 2 — 元七セルidentity balance偶奇
U mod 2 — 元七セルunit-step整数偶奇
```

特に固定された元六セル始終点ではRとUの偶奇が元v5.04境界定理によって連動するため、これらを無条件に独立な三ビットとは扱わない。

ただし、これらの値が一致することが現行八セルの比較可能性に十分かどうかは未決であった。Qi v5.08では、**一致しても比較不能な真正な同端点七セル履歴の反例**を、元自由六セルの結合子だけで構成した。

## 2. 独立Type上の四重五角形結合付け

`PentagonAdjoinedSixCell W l r` の生構文で、元のadjoined `pentagon : l → r` を (p)、その生逆元を (p^{-1}:r→l) と記す。

四因子を

```text
a = symm(pentagon)  : r → l
b = pentagon        : l → r
c = symm(pentagon)  : r → l
d = pentagon        : l → r
```

と固定する。両側は**同じ元六セル生語**を始終点とする：

```text
source = (((a ; b) ; c) ; d)
target = (a ; (b ; (c ; d)))
```

元の13構成子を持つ自由 `SevenRewrite` だけから次の二つの異なる型付き履歴を作る。

```lean
sevenFourfoldInversePentagonThree l r -- 3 associator steps
sevenFourfoldInversePentagonTwo   l r -- 2 associator steps
```

一方は `congrComp(assoc(a,b,c),refl(d))`、`assoc(a,b;c,d)`、`congrComp(refl(a),assoc(b,c,d))` の三段。もう一方は `assoc(a;b,c,d)`、`assoc(a,b,c;d)` の二段。いずれも**新しい比較を仮定せず、元の七セル履歴を構成**する。

## 3. 新たな局所associator指紋

`sixIsRawPentagon` と `sixIsRawInversePentagon` は、新六セルTypeの`pentagon`と生`symm(pentagon)`のみを厳密に識別する。特に `symm(symm(pentagon))` を `pentagon` と勝手に同一視しない。

`sevenInversePentagonAssociatorCharge` を、元の自由七セル13構成子で構造的に定義する。署名は次の通り。

```text
Φ(refl) = 0
Φ(symm H) = -Φ(H)
Φ(trans H K) = Φ(H) + Φ(K)
Φ(congrInv H) = Φ(H)
Φ(congrComp H K) = Φ(H) + Φ(K)
Φ(assoc x y z) = 1  iff
    x = raw(symm pentagon), y = raw pentagon,
    z = raw(symm pentagon)
上記以外のすべての原始七セル規則のΦ = 0
```

`iff`の条件は**自由構文のパターン照合**である。元六セルstrict Eqへのquotientや元Sourceへの新公理ではない。従来の一律なT（associator総数）ではなく、**型とredex形状に依存する局所指紋**である。

四重結合付けの両経路で形式計算すると：

```text
                                    Three         Two
Φ (局所associator指紋)             1             0
V mod 2                             0             0
R mod 2                             0             0
U mod 2                             0             0
元六セルraw source                  同一          同一
元六セルraw target                  同一          同一
```

## 4. 現行全八セル比較に対する不変性を形式証明

`eightCell_preservesInversePentagonAssociatorCharge` は、元v4.91の**22構成子すべて**について構造帰納する。特に `zigzagDiamond` に出る `assoc(c,symm(c),c)` は、元の生構文では指定redex `(symm pentagon,pentagon,symm pentagon)` と一致せず、Φは両側0で保存される。

さらに次のすべての独立高次presentationに対して、`previous`だけでなく**新しい固有生成元と全型付き閉包**を含めて保存を証明した：

```text
EightCell → TriangleEightCell → InvolutionEightCell
 → InverseCompEightCell → IdentityEightCell
 → UnitDiamondEightCell → BalancedUnitEightCell
 → DoubleCompositeEightCell → MixedResidueEightCell
```

v5.07の新 `mixedResidue(w)` 両側においてもΦ=0であり、旧比較から引き継いだ比較証拠を保持する。新しい不変量は `Quotient.lift` により**現行MixedResidueHistoryの選択商へ真正に降下**する。

## 5. 新しい真正obstructionと非因子化

型付き帰納証明と具体的な値Φ(Three)=1、Φ(Two)=0から、以下をLean4で証明した。

```lean
sevenFourfoldInversePentagon_noMixedResidueComparison
sevenFourfoldInversePentagon_classGap
mixedResidueThreeResiduals_notComplete
sevenInversePentagonAssociator_notFactorThroughResiduals
```

これは、旧商でも新商でも未発見という意味ではない。**現行MixedResidueEightCellの全比較生成元をどのように合成しても、Φ保存に反するため比較が存在しないという形式的非存在定理**である。

したがって、三つの残余観測量 `(V mod2,R mod2,U mod2)` の一致では現行選択八セル比較可能性を完全に特徴付けられない。さらに、新Φはこれらの観測量の任意の非線形関数としても復元できない。

## 6. 元P77/GK5CG source境界と限界

`pentagonActualFourfoldInversePentagonObstruction` は、任意の元P77最終raw添字`i`で選ばれる真正GK5CG由来のlong/short五セル値を**そのまま**引数とし、同じ自由六セル四重結合付けobstructionを輸送する。元の `pentagonAdjoinedSixCell_generator` は `.pentagon` の定義であり、別のsurrogate sourceには置き換えない。

旧 `PentagonAdjoinedSixCellEqualityInterpreter` の不存在も保持する。

重要な限界：`Φ` は**選択した自由presentationに依存する構文的障害**であって、一般の高次圏や全モデルに対する自然変換不変量と主張していない。任意平行七セル履歴の比較不能性、global thinness、独立九セルの存在、新しい八セル原始生成元、旧F55/P77/GK5CG sourceのstrict Eq化は**証明・仮定していない**。

## 7. 次段Qi v5.09

今回の真正五角形局所coherence障害に対し、既存mixedResidue・doubleComposite・unitDiamond・balancedUnit等の比較で合流できる局所pairを除外したうえで、**一つの型付き五角形比較生成元が最小限かどうか**を調査する。原始生成元の追加は独立presentationでの必要性・保存量・obstruction・source authorityを証明できた場合に限る。

append-only／tighten-only／overwrite-forbidden／same-root。元F55/P77/GK5CGの全証明履歴を保持する。
