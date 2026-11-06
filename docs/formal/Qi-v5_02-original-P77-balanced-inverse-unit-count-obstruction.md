# Qi v5.02 — 左右逆元消去・単位則カウントの整数高次障害

## 0. 正本・exact-source Lean検証

2026年11月7日 JST。Repository `itakura-hidetoshi/KuuOS`、canonical branch `main`。
Qi v5.01統合正本 `9707ed5eb96b97a8c234deb0e366131c56ee6e91` を継承する。

| 項目 | 確認結果 |
|---|---|
| 定理PR | [#3227](https://github.com/itakura-hidetoshi/KuuOS/pull/3227) **MERGED** |
| 定理squash SHA | `3b7e205d3820dadf4954dc398b97d35db3794a3d` |
| exact-source CI | [#42308824344](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42308824344) **SUCCESS** |
| Strict Lean | **10,301 / 10,301 SUCCESS** |
| Governance | **30 / 30 SUCCESS** |
| 公理依存監査 | **41宣言**、依存は `propext`、`Classical.choice`、`Quot.sound`、または公理不要 |
| `sorryAx` | **なし** |
| 変更Lean warning/error | **0 / 0** |
| 検証済みsource HEAD | `f821aef132efeff078fb187785b0f01a39f42932` |
| test-merge SHA | `5235c659585c10cb06a65de5f5b6cf2108906826` |
| source/test-merge Git tree | **`c6abe79391ab2bb7df9a760187a091122c2da466` 完全一致** |
| 固定Lean | `v4.30.0-rc2` |
| 固定mathlib | `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開集約・root | `KuuOSFormal`、**107維持** |
| 保護PR #1558 | Draft／OPEN／未マージ（維持） |

[Qi v5.02 Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77BalancedInverseUnitCountObstructionV5_02.lean) ·
[Qi v5.01正式記録](Qi-v5_01-original-P77-unit-diamond-minimal-higher-completion.md)

## 1. 問題設定

Qi v5.01では独立の`UnitDiamondEightCell`に一つの`unitDiamond`比較を加え、
旧法4整数観測量Sの降下は失われたが、第四整数Rの偶奇は新商へ降下した。

残る課題は、**同じraw六セル始終点の二つの七セル履歴で、
Rの偶奇が等しくても現行`UnitDiamondEightCell`で比較できない例**の形式構成である。

今回は新原始八セル・九セルを追加せず、現在の全型付き比較構成子に保存される
新たな整数観測量から不可能性を証明した。

## 2. 13構成子上の整数単位則カウント

`sevenUnitStepCharge : SevenRewrite W long short c d → ℤ`を、
元の自由七セル証拠履歴Typeに対して構造再帰で定義する。

- `leftUnit`、`rightUnit`の原始生成元に重み+1。
- ほかの原始生成元`assoc`、`inverseLeft`、`inverseRight`、
  `doubleInverse`、`inverseId`、`inverseComp`は0。
- `refl`は0、`symm H`では符号反転、`trans H K`と
  `congrComp H K`では加算、`congrInv H`では保存。

```text
U(H) = signed_count(leftUnit in H) + signed_count(rightUnit in H)
```

重要なのは、旧v4.91 `EightCell`の22構成子すべてにおいて、
この**整数値のまま**等式が成り立つことである。
とくに`zigzagDiamond`は左経路に左単位則1回、
右経路に右単位則1回を含み、いずれもU=1となる。

既存の`TriangleEightCell`、`InvolutionEightCell`、
`InverseCompEightCell`、`IdentityEightCell`、
`UnitDiamondEightCell`の追加生成元と全型付き文脈に対しても
帰納法で整数Uの保存を形式証明した。

```lean
theorem unitDiamondEightCell_preservesUnitStepCharge
    (q : UnitDiamondEightCell W long short s t) :
    sevenUnitStepCharge s = sevenUnitStepCharge t
```

この全構成子保存定理から`Quotient.lift`を用いて
`unitDiamondHistoryUnitCount`を新商上の真の整数値観測量として構成した。

## 3. 左右逆元消去とinverseIdの二因子前駆例

`w:W`の元のraw六セルに対し、次の左右別々の二経路を取る。

```lean
sevenInverseUnitLeftDirect w  := .inverseLeft (.refl w)
sevenInverseUnitLeftVia w     := inverseId ; leftUnit
sevenInverseUnitRightDirect w := .inverseRight (.refl w)
sevenInverseUnitRightVia w    := inverseId ; rightUnit
```

正確なLean定義では`congrComp`を通じた中間六セルと
`trans`を保持し、上の表記は適用順序の略記である。
左右を横合成して`sevenBalancedInverseUnitFirst/Second`を得る。

この二因子前駆例では、U=0対2、R mod 2=0対0であり、
既存の`UnitDiamondEightCell`では比較不能と証明した。

**重要な訂正：** 旧三整数のTは、第一経路が1、第二経路が0である。
`inverseRight`がT=1を持つためであり、
最初の同一視仮説は成立しない。Qi v5.02ではこれを
`sevenBalancedInverseUnit_tripleValues`として明示的に証明した。

## 4. 真正三角形critical pairによるTの相殺

旧`sevenLeftTriangleDirect(.refl w)(.refl w)`と
`sevenLeftTriangleViaAssoc(.refl w)(.refl w)`は、
元の型付き三角形critical pairである。
前者のTは0、後者のTは1となり、いずれもUは1である。

これを二因子前駆例の左右の経路に逆向きに割り振って
`sevenBalancedUnitInvisibleFirst/Second`という
**真正な三因子平行七セル履歴**を作った。

```text
                         H_first       H_second
元三整数 (T,J,K)          (1,0,0)        (1,0,0)
元第四整数 R mod 2        0              0
新整数U                   1              3
raw六セル始終点           完全一致
```

全`UnitDiamondEightCell`比較でUが保存されるので、
もし`UnitDiamondEightCell(H_first,H_second)`が存在すれば
整数等式1=3が導かれて矛盾する。

```lean
sevenBalancedUnitInvisible_noComparison
sevenBalancedUnitInvisible_distinctClasses
sevenTripleAndParity_notCompleteAfterUnitDiamond
```

これらをLean4で形式証明した。**元の三整数と残余偶奇の両方が等しくても、
現行選択八セル商では比較可能性を導けない**という具体的な反例である。
全平行履歴の分類・大域thin性を主張するものではない。

また二因子前駆例から、
`sevenUnitStepCharge_notFactorThroughParity`によって、
整数Uが残余偶奇の任意の非線形関数から普遍的に復元できないことも示した。

## 5. 元P77 raw最終添字と厳密Eq境界

`pentagonActualBalancedInverseUnitWithSourceObstruction`では、
任意の元P77 raw最終添字に対し、
元`pentagonAdjoinedSixCell_generator`を用いて
**二因子前駆例の比較不能性と同じ偶奇**を真正GK5CGのsource付き文脈へ輸送した。

同時に`¬ PentagonAdjoinedSixCellEqualityInterpreter`を維持している。

三整数も一致する強い三因子例は本Leanモジュールで任意のW上の
型付きraw七セル履歴として証明した。
その三因子例を**元P77の真正六セルsourceとの追加横合成で輸送する定理は、
今回のP77定理とは区別する**。新規source Eqを仮定していない。

元F55/P77/GK5CG source、元七セル証拠履歴、旧高次商、
strict空と独立Kuu presentationのauthority境界は変更していない。

## 6. Leanエラーの構造的原因と修正履歴

初回PR HEAD `1d9871f3e2a78a8f9393e680720f21bedcdadd2b`で
`sevenBalancedInverseUnit_sameTriple`の未解決ゴールが出た。
調査で元Tの`inverseRight`生成元の重み+1を再確認し、
誤った同一三整数主張を撤回して、
真正三角形critical pairによる明示的補償を加えた。

2回目HEAD `82f18b171aae53e69909399b85198e8cfc7c48ec`では、
宣言用`/-- ... -/`コメントを`end`の直前に置いたため、
Lean4のパーサが後続宣言を期待する構文エラーが1件発生した。
これは定理失敗ではなくコメントの位置／種類の問題である。
通常コメント`/- ... -/`に置換し、
修正版HEAD `f821aef132efeff078fb187785b0f01a39f42932`で
全体のexact-source CIが成功した。

元source・既存Lean定理・固定mathlib API・公開rootは一切変更していない。
過去のエラーを隠す`sorry`や新公理は導入していない。

## 7. 未証明事項と次段階Qi v5.03

今回も次を証明していない。

- 任意の平行七セル履歴の比較可能性、全高次障害の完全分類
- Uの一致から比較証拠が必ず存在するという十分性
- 九セル以上のthin性、または元sourceのstrict Eqへの昇格
- 強い三因子証拠の追加source文脈輸送（今回のP77定理は二因子前駆例）

次のQi v5.03では、まずこの新たなU障害に対する局所合流を精査する。
新原始比較生成元が本当に必要な場合に限り別の独立presentationに
最小追加し、整数Uと残余偶奇の降下境界を再評価する。

append-only／tighten-only／overwrite-forbidden／same-root、
公開root107、保護PR #1558 Draft／OPEN／未マージを継続する。
