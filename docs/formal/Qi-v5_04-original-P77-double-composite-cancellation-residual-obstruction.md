# Qi v5.04 — 合成逆元消去の残余整数障害・二偶奇の境界依存

## 0. Canonical正本とexact-source検証

2026年11月7日 JST。Repository `itakura-hidetoshi/KuuOS`、canonical branch `main`。
継承元はQi v5.03の統合済み正本 `410cae12be6af4a8e49bcdd764561031bfa6bd7b`。

| 検証項目 | 結果 |
|---|---|
| 定理PR | [#3231](https://github.com/itakura-hidetoshi/KuuOS/pull/3231) **MERGED** |
| 定理squash | `37b3198b336b09cdffac165e9707133f97bb019e` |
| exact-source CI | [#42314003814](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42314003814) **SUCCESS** |
| Strict Lean | **10,303 / 10,303 SUCCESS** |
| Governance | **SUCCESS** |
| 新規宣言の公理監査 | **32宣言**、`propext`・`Classical.choice`・`Quot.sound`または公理不要 |
| `sorryAx` | **なし** |
| 変更Lean warning/error | **0 / 0** |
| 検証済みsource HEAD | `bb614fa975654c6d2fe3ab6a8d0a765735b0c994` |
| test-merge SHA | `ba219191a082069257c453e1902f3be05b4c341a` |
| source/test-merge Git tree | **`0fa7461e50515701428eac5495eda9ff733bba7d` 完全一致** |
| 固定Lean / mathlib | `v4.30.0-rc2` / `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開集約・root | `KuuOSFormal`、**107維持** |
| 保護PR #1558 | Draft／OPEN／未マージ（維持） |

[Qi v5.04 Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77DoubleCompositeCancellationResidualV5_04.lean) ·
[Qi v5.03正式記録](Qi-v5_03-original-P77-balanced-unit-minimal-higher-completion.md)

## 1. 問題設定：二つの偶奇は独立か

Qi v5.03で独立した`BalancedUnitEightCell`を追加し、元整数Uは新商へ降下しないが、
`R mod 2`と`U mod 2`はどちらもBool値として降下すると証明した。

ここで、二つのBool値を固定された七セル始終点上の独立した二ビットと仮定するのは正しくない。
元の自由六セル構文に含まれる`symm`と`trans`の数を数える
`sixRawShapeWeight`を新たに定義した。

```text
F(refl(w)) = 0                 F(pentagon) = 0
F(symm(c)) = F(c) + 1
F(trans(c,d)) = F(c) + F(d) + 1
```

任意の元13構成子の真正七セル履歴 `H : SevenRewrite ... c d` に対して、
Lean4で次のmod 2の境界コサイクル条件を構造帰納法で証明した。

```text
(F(c) + R(H) + U(H)) mod 2 = F(d) mod 2
```

ここで `R = sevenIdentityBalance`、
`U = sevenUnitStepCharge` であり、対象は商以前の**元の全七セル生構文**である。
したがって同じ元六セル始終点`c,d`をもつ任意の二つの平行履歴`H1,H2`について、

```text
R(H1) mod 2 = R(H2) mod 2
    iff
U(H1) mod 2 = U(H2) mod 2
```

という**必要十分な偶奇連動**が得られる。
Lean定理は`sevenRawBoundaryParitySound`、
`sevenParallelBoundaryParity`、`sevenParallelParityCoupling`である。
これは平行履歴間の比較存在や元source strict Eqを意味しない。

## 2. 新しい整数V：単位則と逆元消去の合計

新しく`sevenTotalReductionCharge : SevenRewrite ... → ℤ`を構造再帰で定義した。
元の13構成子のうち`leftUnit`、`rightUnit`、
`inverseLeft`、`inverseRight`へ+1、
残る局所生成元には0を与える。

`symm`で符号反転、`trans`と`congrComp`で加算、
`congrInv`で保持する。

```text
V(H) = signed_count(leftUnit, rightUnit, inverseLeft, inverseRight)
```

元の`EightCell`全22構成子、`TriangleEightCell`、
`InvolutionEightCell`、`InverseCompEightCell`、
`IdentityEightCell`、`UnitDiamondEightCell`、
そして最新v5.03の`BalancedUnitEightCell`の
**全生成元と文脈閉包に対して整数Vが厳密に保存される**
ことを定理ごとにLean4で証明した。

とくにv5.03の唯一の新原始生成元`balancedUnit`でも
元の二経路のVはともに3である。
新選択商上の真正な整数観測量
`balancedUnitHistoryTotalReduction`を`Quotient.lift`で構成した。
これは元の整数Uを再度降下させる操作ではない。

## 3. 合成逆元消去の二つの真正履歴

任意の`w : W`について、元六セル語
`(refl(w);refl(w));inverse(refl(w);refl(w))`を考える。

第一の七セル履歴は直接`inverseRight(refl(w);refl(w))`で消去する。
第二は、`inverseComp`で逆元を分配し、
`assoc`と`symm(assoc)`で順序を組み直した後、
`inverseRight`を二度、`leftUnit`を一度使って同じ`refl(w)`へ至る。

これらは同一のraw六セル始終点を持つ
`sevenCompositeInverseCancelDirect`と
`sevenCompositeInverseCancelVia`という元の型付き七セル履歴である。

```text
                     Direct       Via
整数V                  1           3
R mod 2                0           1
U mod 2                0           1
```

この単一ペアは二偶奇が異なるので、これだけを新たな偶奇不可視障害とは主張しない。

## 4. 二組の型付き横合成：二偶奇不可視の比較不能性

前段の元六セル平行履歴を**二つ横合成**した。
`sevenDoubleCompositeCancelFirst`と
`sevenDoubleCompositeCancelSecond`は元の
`SevenRewrite.congrComp`から構成した真正の七セルType値であり、
始終点は完全に同一である。

```text
                            First       Second
R mod 2                       0            0
U mod 2                       0            0
新しい整数V                   2            6
raw六セル始終点              完全一致
```

現行`BalancedUnitEightCell`のいかなる比較でもVは保存されるため、
比較証拠があると`2 = 6`が必要になり矛盾する。

Lean4で次の命題を形式証明した。

```lean
sevenDoubleCompositeCancel_noComparison
sevenDoubleCompositeCancel_distinctClasses
sevenDoubleParity_notCompleteForBalancedUnit
sevenTotalReduction_notFactorThroughParities
```

これにより**二偶奇が両方一致することは、現行高次商での比較可能性の十分条件ではない**と確定。
さらにVは二偶奇の任意の非線形関数からすら普遍的に復元できない。
なお、今回の二履歴について以前の三整数`(T,J,K)`の一致までは主張しない。

## 5. 真正P77最終raw添字への輸送とauthority境界

`sevenDoubleCompositeSourceFirst c`と
`sevenDoubleCompositeSourceSecond c`は、
二組横合成した比較不能な履歴に同じ真正六セル値`c`を貼ったものである。
元の型付き添字、元R/Uの偶奇一致と整数Vの2対6を保つ。

`pentagonActualDoubleCompositeResidualWithSourceObstruction`は、
**任意の真正P77最終raw添字**に対して、
元`pentagonAdjoinedSixCell_generator`により

- 同じ真正GK5CG sourceのType値証拠をもつ二履歴の両偶奇一致
- 完全な旧`BalancedUnitEightCell`構文で比較不可能
- `¬ PentagonAdjoinedSixCellEqualityInterpreter`の維持

を同時に示す。

旧八セルpresentation、商、自由七セル構文、
元F55/P77/GK5CG source・strict Eqと証拠履歴を変更していない。
独立Kuuのpresentationと元sourceのauthorityを混同しない。

## 6. CIエラーと全文点検による修正

初回PR HEAD `133a8ac27a0391f3e6535f1ec8e32eac85752e8f`のCI
[#42313556950](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42313556950) は
2件の構文エラーで失敗した。

変更Lean全文、imports、元六セル・七セル・八セルの署名、
固定mathlibのAPI、公理監査出力を照合した結果、原因は
冒頭の文章`eighth-/ninth-cell`中の`-/`が
Lean4のブロックコメントの終端として解釈されたことだった。
続く行がLeanコマンドとして解釈され、エラーを発生した。

定理本文は変えず、そのコメント1行を
`eighth- or ninth-cell`に訂正した。
修正版HEAD `bb614fa975654c6d2fe3ab6a8d0a765735b0c994`
でStrict Lean **10,303/10,303 SUCCESS**、
32宣言の標準公理のみ・`sorryAx`なし・
変更warning/error0/0・source/test-merge Git tree完全一致となった。

## 7. 今回証明していない事項・次のQi v5.05

今回、次の主張は**証明していない**。

- 任意の平行七セル履歴の比較可能性、すべての高次obstructionの完全分類
- Vが一致すれば新旧八セルの比較が存在するという十分性
- Vを用いた全線形・非線形観測量の普遍分類
- 元F55/P77/GK5CG strict Eqと独立商Eqの同一視
- 九セル以上の大域thin性

次のQi v5.05では、今回明示した二組の合成逆元消去critical pairについて
既存比較規則の全局所閉包を確認する。
**v5.04の証明済みV障害に限って**必要な場合は別の独立presentationへ
新原始比較を最小限追加し、Vの整数非降下と残余値の降下を切り分ける。

append-only／tighten-only／overwrite-forbidden／same-root。
公開root107、保護PR #1558 Draft／OPEN／未マージを維持する。
