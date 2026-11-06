# Qi v4.93 — 七セルの単位・結合三角形critical peakと八セル整数障害

## 0. 正本・証明検証

2026年11月6日 JST。唯一のcanonical repository/branch：`itakura-hidetoshi/KuuOS`／`main`。

| 項目 | exact-sourceで確認された状態 |
|---|---|
| 継承起点 | Qi v4.92、`9a53a765d8e287974ff013312b3940ed31ca640f` |
| 定理PR | [#3209](https://github.com/itakura-hidetoshi/KuuOS/pull/3209) — MERGED |
| 修正後の検証済みHEAD | `bacc45cc5234c8676a07078d16e16f0ffccbe77b` |
| 定理squash／定理正本HEAD | `0bf6ffb179754ad6ca895680dae960727636f2fe` |
| source／test-merge／squash Git tree | `cc04ac37aa0792567c310b47555f2d6997c3d7f5` — 完全一致 |
| exact-source CI | [#42213331171](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42213331171) — completed/SUCCESS |
| Strict Lean | **10,292／10,292 SUCCESS** |
| Governance | **30／30 SUCCESS** |
| 指定新規公理監査 | **22件**、`propext`／`Classical.choice`／`Quot.sound`のみ、`sorryAx`なし |
| 変更Lean warning／error | **0／0** |
| Pin | Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開集約・root | `KuuOSFormal`、root107維持 |
| 保護PR | #1558 Draft／OPEN／未マージ |

[検証済みLean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77TriangleOverlapEightCellObstructionV4_93.lean) · [Qi v4.92証明記録](Qi-v4_92-original-P77-eight-cell-critical-peak-closure-history-quotient.md) · [真正元GK5CG source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5CGP77FiveCellAssociatorCharge.lean)

## 1. 対象：v4.92の限定的LocalCriticalPeakの外側

v4.89の`SevenRewrite(c,d) : Type`は13種類の明示的な新七セル書換えを保持する。v4.91の独立した`EightCell(H₁,H₂) : Type`には22生成規則があり、v4.92ではzigzagと独立書換えの交換を起点とした局所critical peak族の合流を証明した。

その族だけでは、**六セルの単位則と結合則が重なった二つの七セル履歴**の比較可能性は証明されない。Qi v4.93では数学的に重要な一段強い主張、すなわち**元の八セル22生成規則からは実際に導出不能**であることを整数値で形式証明した。

## 2. 七セル生構文上の整数不変量

`sevenTriangleCharge : SevenRewrite(c,d) → ℤ`を六セル次数商とは別に、七セル構文の構造再帰で定義する。

\[
\begin{aligned}
Q(\mathrm{refl}) &= 0, &
Q(\mathrm{symm}\,H) &= -Q(H),\\
Q(\mathrm{trans}(H,K)) &= Q(H)+Q(K),&
Q(\mathrm{congrComp}(H,K)) &=Q(H)+Q(K),\\
Q(\mathrm{congrInv}(H)) &=Q(H),&
Q(\mathrm{assoc}) &=1,\\
Q(\mathrm{inverseRight}) &=1,
\end{aligned}
\]

他の元七セル局所規則（単位、左逆元消去、二重反転、恒等逆、合成逆）に対する値は0とする。この`Q`は元のGK5CGの五セル値、六セル`degree`、あるいは新高次商そのものではない。

`eightCell_preservesTriangleCharge`は、**v4.91の元八セル22構成子すべて**への構造帰納により

\[
\boxed{
E:\mathrm{EightCell}(H_1,H_2)
\;\Longrightarrow\;
Q(H_1)=Q(H_2)
}
\]

を形式証明する。特に元zigzagダイヤモンドの両経路で`Q=1`となり、元の比較生成元は矛盾しない。

## 3. 二つの真正な三角形critical peak

左側：六セル生語`((refl w ; c) ; d)`から`(c;d)`への二つの実七セル証明書を定義する。

- `sevenLeftTriangleDirect c d := congrComp (leftUnit c) (refl d)`：内側の単位を先に消去。
- `sevenLeftTriangleViaAssoc c d := trans (assoc (refl w) c d) (leftUnit (trans c d))`：結合変換を先に適用し、外側単位を消去。

右側：`((c;d);refl z)`から`(c;d)`への二つの証明書。

- `sevenRightTriangleDirect c d := rightUnit (trans c d)`。
- `sevenRightTriangleViaAssoc c d := trans (assoc c d (refl z)) (congrComp (refl c) (rightUnit d))`。

`sevenLeftTriangle_chargeGap`と`sevenRightTriangle_chargeGap`がどちらも

\[
\boxed{Q(H_{\mathrm{direct}})=0,\qquad
Q(H_{\mathrm{viaAssoc}})=1}
\]

を証明。既証明の八セル不変性と合わせ、

\[
\boxed{
\neg\operatorname{Nonempty}
\bigl(\mathrm{EightCell}_{\mathrm{old}}
(H_{\mathrm{direct}},H_{\mathrm{viaAssoc}})\bigr)
}
\]

を、左・右それぞれ`sevenLeftTriangle_noOldEightCell`／`sevenRightTriangle_noOldEightCell`で形式証明した。**既存22生成規則の範囲における真のobstruction**であって、単なる推測や検索不能の主張ではない。

## 4. sourceを保つ独立した八セル拡張

元の`EightCell`型は変更せず、**別のType値presentation**`TriangleEightCell`を新設した。元八セルの証拠を`.original`で保ち、追加した原始整合性生成元は左・右の三角形二種類のみ。他は反転・連鎖・whiskering・逆／合成文脈への型付き閉包である。

`triangleEightCell_leftNewNotOld`／`triangleEightCell_rightNewNotOld`は、新しい局所証拠が存在する一方、元八セルの同じ比較Typeは空であることを同時に示す。`triangleEightCell_noOldInterpreter`は、**すべての新比較を元八セルへ戻す関数**の存在を`¬ Nonempty (∀..., TriangleEightCell → EightCell)`という正しいLean4の命題で否定する。

重要：これは**元sourceの定理や構文を保った別presentation**への追加であり、八セル比較関係そのものについて「変更前と同値」という意味ではない。

## 5. 限定的critical peak族の拡張と構成的な合流

`TriangleCriticalPeak`は、v4.92`LocalCriticalPeak`、左三角形、右三角形を原始ピークとし、指定された型付き文脈・連鎖でのみ閉じた9構成子の新帰納Typeである。

`triangleCriticalPeak_fill`は全構成子に対して構造帰納を行い、各ピーク`P`から実際の新八セル証拠を構成する。

\[
\boxed{
P:\mathrm{TriangleCriticalPeak}(H_1,H_2)
\longmapsto
\mathrm{TriangleEightCell}(H_1,H_2)
}
\]

`triangleCriticalPeak_joinable`はその`Nonempty`版。**任意の七セル履歴同士が比較可能とする生成元は導入していない。**

## 6. 新旧八セル履歴商の関係

新しい`TriangleEightCell`による比較存在を`Setoid`として構成し、別の`triangleHistoryClass`商を導入。

`triangleHistoryClass_eq_iff`は

\[
[H_1]_{\triangle}=[H_2]_{\triangle}
\quad\Longleftrightarrow\quad
\operatorname{Nonempty}(\mathrm{TriangleEightCell}(H_1,H_2))
\]

を形式証明する。`oldHistoryClass_descendsToTriangle`は、旧八セル履歴商での一致が新商でも保存されることを証明。

さらに`triangleHistoryClass_strictlyNew`は上記三角形の二経路について

\[
\boxed{
[H_{\rm direct}]_{\triangle}=
[H_{\rm viaAssoc}]_{\triangle}
\quad\land\quad
[H_{\rm direct}]_{8}\ne
[H_{\rm viaAssoc}]_{8}
}
\]

を証明。**新商が旧八セル履歴商より真に粗い**ことを、元八セルの不変量から定量的に裏付けた。

## 7. 元P77・GK5CGへの適用と厳密戻り障害

`pentagonActualTriangle_newVsOldWithSourceObstruction`は、任意の真正P77最終raw添字`i`における、元GK5CGの**保守的五セル値二端点**に対応する本来の六セル生成元`c`とその反転を使う。

同じ元source添字で、新拡張三角形比較は存在し、元22規則八セル比較は存在しない。また元の`PentagonAdjoinedSixCellEqualityInterpreter`不存在も同時に証明する。

元F55/P77/GK5CGの五／六／七／八セルsource構成子を変更・追加していない。新七セル生構文の厳密Eq、旧sourceの厳密Eq、旧八セル証明、新拡張Type、二段階の履歴商は常に別々に保持する。

## 8. Lean4修正履歴と公理監査

初回exact-source CI #42212768586のStrict Leanは、数学的証明ではなくLean4の型／構文の2点で失敗した。

- `TriangleEightCell → EightCell`は`Type`値であり、その関数全体のPi型に命題否定`¬`を直接適用できない。正しい形`¬ Nonempty (∀ ..., TriangleEightCell → EightCell)`へ修正。
- namespace終端直前の宣言未接続docstring `/-- ... -/`を通常コメント `/- ... -/`に変更。

修正後のHEAD `bacc45cc...`で **全10,292 Leanジョブ SUCCESS**。22宣言の`#print axioms`は標準公理`propext`、`Classical.choice`、`Quot.sound`に限定、`sorryAx`なし。変更Lean warning/error0/0。

## 9. 次候補Qi v4.94

- 七セルの逆元消去・反転・結合則が重なる追加critical triangle／squareについて、旧Q不変量の障害判定と、新`TriangleEightCell`の局所整合性を検討。
- 新拡張の文脈合成の自然性と、元の`LocalCriticalPeak`からの証拠経路が複数ある場合のさらなる高次obstructionを区別。
- 任意の平行七セル履歴に対する八セル全域完全性や九セル比較は**未証明**として残す。

---
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
