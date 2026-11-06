# Qi v4.96 — 三つの整数不変量の高次履歴商フィルトレーションと線形剛性

## 0. canonical正本とexact-source検証

2026年11月6日 JST。Repository `itakura-hidetoshi/KuuOS`、唯一のcanonical branch `main`。

| 項目 | GitHub MCPで確認した状態 |
|---|---|
| 継承起点 | Qi v4.95、main `0dfc20fde8fec090e241df1e51b473ff01d0f2a9` |
| 定理PR | [#3215](https://github.com/itakura-hidetoshi/KuuOS/pull/3215) — MERGED |
| 検証済みexact-source HEAD | `d21d756917de9527270dbd80a6783a71e1cfd529` |
| 定理squash／定理正本HEAD | `4aa456cbd87dd10810414fd018120f9f763b9859` |
| source／test-merge／squash Git tree | `8cb01f5bf32a522b70bed7bee5b5c0b644debe31` — 完全一致 |
| exact-source CI | [#42220569477](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42220569477) — SUCCESS |
| Strict Lean | **10,295／10,295 SUCCESS** |
| Governance | **30／30 SUCCESS** |
| 新規公理監査 | **15宣言**、`propext`／`Classical.choice`／`Quot.sound`のみ、`sorryAx`なし |
| 変更Lean warning／error | **0／0** |
| Pin | Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開集約 | `KuuOSFormal`、公開root107維持 |
| 保護PR | #1558 Draft／OPEN／未マージ |

[検証済みLean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77ThreeChargeFiltrationRigidityV4_96.lean) · [Qi v4.95正式記録](Qi-v4_95-original-P77-inverse-composite-unit-critical-peaks.md) · [真正GK5CG source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5CGP77FiveCellAssociatorCharge.lean)

## 1. なぜ三つの整数障害をまとめるのか

Qi v4.93の`sevenTriangleCharge`（単位・結合三角形）、Qi v4.94の`sevenInvolutionCharge`（二重反転・逆元消去）、Qi v4.95の`sevenInverseCompCharge`（合成逆元展開・単位）は、いずれも**元の13構成子を持つ生の七セル履歴`SevenRewrite`**上で定義された符号付き整数である。

`sevenChargeTriple`は、それらを1つの積型として保持する。

\[
\boxed{
\mathbf Q(H)=(T(H),J(H),K(H))\in\mathbb Z^3.
}
\]

この値は旧六セル`degree`、元五セル値、七セル履歴の厳密Eq、八セル比較証拠、その各商のどれとも同一視しない。

## 2. 高次履歴商の段階別の保存則

`originalEightCell_preservesTriple`は、v4.91元`EightCell(H₁,H₂)`の比較があれば三成分すべてが一致することを形式証明する。`originalHistoryClass_eq_preservesTriple`は同じ性質を元八セル履歴商でのEqに対して証明する。なお逆方向の完全性は主張しない。

`triangleHistoryClass_eq_preservesTail`と`involutionHistoryClass_eq_preservesLast`はそれぞれ、次の段階で保持される成分を示す。

| 独立比較presentationと選択商 | Eqで保存される成分 |
|---|---|
| v4.91 `EightCell` | `(T,J,K)` |
| v4.93 `TriangleEightCell` | `(J,K)` |
| v4.94 `InvolutionEightCell` | `K` |
| v4.95 `InverseCompEightCell` | これら3成分の非自明な整数線形結合は普遍保存されない |

これは新しい八セル生成元を追加して旧商を粗くする各段階で、以前の保存量のどこが破れるかを正確に区別する表である。

## 3. 実際の三つのcritical peakが与える整数格子の基底

`sevenChargeTriple_trianglePivot`、`sevenChargeTriple_involutionPivot`、`sevenChargeTriple_inverseCompPivot`が、元v4.93／94／95で構築済みの**型付き生七セル履歴**の差を実際に計算する。

\[
\boxed{
\begin{aligned}
\Delta_{\triangle}&=(1,0,0),\\
\Delta_{\rm inv}&=(1,1,0),\\
\Delta_{\rm comp}&=(0,0,1).
\end{aligned}
}
\]

これらの列（または行）からなる整数行列は行列式1の単模行列である。さらに`threeChargePivot_linearIndependent`は、この三つの差に対して保存を要求される係数がすべて0になることを、整数等式の直接的なLean4証明として与える。全域の八セル比較や高次thin性を仮定する計算ではない。

## 4. v4.95の最終presentationに対する線形剛性

任意の整数係数`α β γ : ℤ`に対して

\[
L_{\alpha,\beta,\gamma}(H)
=\alpha T(H)+\beta J(H)+\gamma K(H)
\]

を`sevenLinearCharge`で定義する。

主定理`sevenLinearCharge_universal_iff_zero`は、v4.95の新`InverseCompEightCell`の**すべての比較証拠**がこの線形量を保存するという命題について、次の必要十分条件をLean4で証明した。

\[
\boxed{
\left[
\begin{array}{l}
\forall H_1,H_2,\ \mathrm{InverseCompEightCell}(H_1,H_2)\\
\qquad\Longrightarrow L(H_1)=L(H_2)
\end{array}
\right]
\iff
(\alpha,\beta,\gamma)=(0,0,0).
}
\]

証明は、**実際に存在する三つの高次比較生成元**を普遍保存仮定へ代入し、以下の整数連立条件を得る構成である。

\[
\alpha=0,\qquad \alpha+\beta=0,\qquad\gamma=0.
\]

そこから`β=0`を導く。逆方向は3係数が0なら線形量が常に0であるという基本事実。このため「三整数不変量の非自明な**線形結合**は最終八セル比較の普遍保存量にはならない」ことが証明された。

**注意：** これはすべての不変量が消失したという定理ではない。非線形・非数値のほかの不変量や、全七セル履歴に対する大域的coherenceの可能性は未解決のまま保持する。

## 5. 三つの高次商の真の粗化と元sourceへの輸送

`ThreeStageStrict`は、以前に証明済みの三段階の新旧商での厳密な差を同時に型付けした命題である。`threeStageStrict_forAny`は、任意の元新六セルgenerator型の実語`c:l⇒r`に対してその成立を構成する。

- v4.93三角形商では一致／v4.91元商では不一致という具体的七セル履歴対。
- v4.94二重反転商では一致／v4.93三角形商では不一致という別履歴対。
- v4.95合成逆元商では一致／v4.94二重反転商では不一致というさらに別履歴対。

`pentagonActualThreeStageStrictWithSourceObstruction`は、この三段階の証拠を**元GK5CG保守的五セルの真正二端点**と任意の元P77最終raw添字へ輸送し、旧`PentagonAdjoinedSixCellEqualityInterpreter`不存在を同時に確認する。

`pentagonActualThreeCharge_linearRigidity`は、同じ真正元P77添字上の新比較Typeにおいても線形剛性が成立することを証明した。

元F55/P77/GK5CGに追加の高次source生成元は付加しない。strict空中心、独立Kuu=presentation、元Type値証拠履歴と新高次比較を別層として保持する。

## 6. 数学的到達点と境界

Qi v4.96は三つの別々の障害を、**整合的なフィルトレーションと整数線形代数の非退化性**として一括形式化した段階である。新しい八セル生成元を追加せず、既証明の証拠からより強い総合定理を導出した。

ただし、「全高次不変量が0である」「元七セル生履歴が厳密一致する」「八セルがthinである」「任意の平行七セル履歴が比較可能」などは**証明していない**。

## 7. 次の候補：Qi v4.97

三つの既存整数不変量で検出できない七セルcritical pairを具体的に構成し、残る原始規則（特に`inverseId`、`inverseComp`、`doubleInverse`と文脈の交錯）を対象に、新しい有効な観測値を探す。大域thin性を仮定せず、局所的な導出可能性とobstructionを同時に吟味する。

---
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
