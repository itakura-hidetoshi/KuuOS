# Qi v4.95 — 合成逆元展開・単位則のcritical peakと第三の独立整数障害

## 0. canonical正本とexact-source検証

2026年11月6日 JST。Repository `itakura-hidetoshi/KuuOS`、唯一canonical branch `main`。

| 項目 | 検証済み状態 |
|---|---|
| 継承起点 | Qi v4.94、main `8dd4f324bbda9b2e45a4112b8e87a35d1eeab02c` |
| 定理PR | [#3213](https://github.com/itakura-hidetoshi/KuuOS/pull/3213) — MERGED |
| exact-source HEAD | `ffb902e4e35736a8450ce65eec9bf9cd8b2810ee` |
| 定理squash／定理正本HEAD | `f64beb73aca7220795e8eef64579655409b923c8` |
| source／test-merge／squash tree | `d0ba40b1af8a9deaf6e3eb56371e8b8c37ed17f2` — 完全一致 |
| Exact-source CI | [#42218451283](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42218451283) — SUCCESS |
| Strict Lean | **10,294／10,294 SUCCESS** |
| Governance | **30／30 SUCCESS** |
| 新規公理監査 | **26宣言**、標準公理`propext`／`Classical.choice`／`Quot.sound`のみ、`sorryAx`なし |
| 変更Lean warning／error | **0／0** |
| Pin | Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開集約 | `KuuOSFormal`、公開root107維持 |
| 保護PR | #1558 Draft／OPEN／未マージ |

[検証済みLean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77InverseCompositeUnitOverlapV4_95.lean) · [Qi v4.94正式証明記録](Qi-v4_94-original-P77-involution-critical-peak-higher-obstruction.md) · [真正元GK5CG source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5CGP77FiveCellAssociatorCharge.lean)

## 1. 第三の整数障害の位置づけ

v4.91の元`EightCell`には22個の具体的局所生成元がある。v4.93では単位・結合重なりから第一の整数障害`sevenTriangleCharge`を、v4.94では二重反転・逆元消去重なりから第二の整数障害`sevenInvolutionCharge`を形式証明し、その都度、**元の高次presentationを書き換えず**に必要な新規則を独立Typeに追加した。

v4.95では、元の13構成子からなる**生の`SevenRewrite`履歴**に対し、`inverseComp`（合成の逆元を逆順合成に展開する局所規則）だけを数える第三の独立整数`sevenInverseCompCharge`を構成する。

\[
\begin{aligned}
K(\mathrm{inverseComp}(c,d)) &= 1,\\
K(\mathrm{symm}(H)) &= -K(H),\\
K(\mathrm{trans}(H,L)) &= K(H)+K(L),\\
K(\mathrm{congrComp}(H,L)) &= K(H)+K(L),\\
K(\mathrm{congrInv}(H)) &= K(H),
\end{aligned}
\]

その他の原始七セル規則は0とする。六セル次数商や元GK5CG五セル値とは別の不変量である。

## 2. 既存の高次比較すべてで保存することの形式証明

三つのLean4定理は、各八セル帰納Typeの**全構成子**を帰納的に確認する。

- `eightCell_preservesInverseCompCharge`：v4.91の元22八セル規則全件。
- `triangleEightCell_preservesInverseCompCharge`：v4.93の左右三角形二規則とその文脈閉包を含む全規則。
- `involutionEightCell_preservesInverseCompCharge`：v4.94の左右二重反転ピーク二規則とその文脈閉包を含む全規則。

したがって

\[
\boxed{
E:\mathrm{InvolutionEightCell}(H_1,H_2)
\implies K(H_1)=K(H_2)
}
\]

が成立。前段の局所coherence拡張によって失われない不変量として、新たな重なりを判定できる。

## 3. 合成逆元展開／単位則の二つの実critical peak

任意の新六セル生語`c:w⇒z`に対し、次の二つの始終点を保つ七セル履歴対を具体的に構成した。

**左側：** `symm (trans (refl w) c) ⇒ symm c`。

- 直接経路 `sevenInvCompLeftDirect c := congrInv (leftUnit c)`。
- 展開経路 `sevenInvCompLeftVia c := trans (inverseComp (refl w) c) (trans (congrComp (refl (symm c)) (inverseId w)) (rightUnit (symm c)))`。

**右側：** `symm (trans c (refl z)) ⇒ symm c`。

- 直接経路 `sevenInvCompRightDirect c := congrInv (rightUnit c)`。
- 展開経路 `sevenInvCompRightVia c := trans (inverseComp c (refl z)) (trans (congrComp (inverseId z) (refl (symm c))) (leftUnit (symm c)))`。

`sevenInvCompLeft_chargeGap`と`sevenInvCompRight_chargeGap`によって、**両方の重なり**で

\[
\boxed{
K(H_{\rm direct})=0,\qquad K(H_{\rm via})=1
}
\]

をLean4で証明した。保存則を用いた`sevenInvCompLeft_noInvolutionEightCell`／`sevenInvCompRight_noInvolutionEightCell`は、

\[
\boxed{
\neg\operatorname{Nonempty}
\left(\mathrm{InvolutionEightCell}(H_{\rm direct},H_{\rm via})\right)
}
\]

を確立する。これは**従来の全八セル生成規則の範囲での真正のobstruction**であり、計算時間不足や未探索ではない。

## 4. 独立Type値の必要最小限補完

元の`EightCell`・`TriangleEightCell`・`InvolutionEightCell`のソースと定理は変更しない。別presentation`InverseCompEightCell`を追加し、`.previous`で旧比較全件を包含、`.leftOverlap`／`.rightOverlap`という**二つだけ**の新しい原始局所比較生成元を付加する。その他は反転・連鎖・前後whiskering・六セル反転／合成文脈への型付き閉包。

`inverseCompEightCell_leftNewNotPrevious`／`inverseCompEightCell_rightNewNotPrevious`は、旧八セル比較が存在しないのに新比較が存在することを同時に示す。`inverseCompEightCell_noPreviousInterpreter`は全新比較を旧Typeへ戻す関数が存在しないことを`¬ Nonempty (∀..., InverseCompEightCell→InvolutionEightCell)`として証明し、`inverseCompEightCell_noStrictInterpreter`は新八セルから生七セル厳密Eqへの全域解釈を否定する。

## 5. 制限付きcritical peakと真に粗い高次履歴商

`InverseCompCriticalPeak`は前段の`InvolutionCriticalPeak`を含み、左右`inverseComp`重なりを原始ピークとして足し、指定の型付き文脈・連鎖に限って閉じる別帰納Typeである。

`inverseCompCriticalPeak_fill`は全構成子の構造帰納で、任意のその族の`P`から実際の`InverseCompEightCell`証明を構成する。

比較証拠の存在を反射・対称・推移関係とする`inverseCompHistorySetoid`と選択商`inverseCompHistoryClass`について、次を形式証明した。

\[
[H_1]_{\rm comp}=[H_2]_{\rm comp}
\quad\Longleftrightarrow\quad
\operatorname{Nonempty}
(\mathrm{InverseCompEightCell}(H_1,H_2)).
\]

`involutionHistoryClass_descendsToInverseComp`は旧商の一致を新商へ降下させ、`inverseCompHistoryClass_strictlyNew`は

\[
\boxed{
[H_{\rm direct}]_{\rm comp}=
[H_{\rm via}]_{\rm comp}
\quad\land\quad
[H_{\rm direct}]_{\rm inv}\ne
[H_{\rm via}]_{\rm inv}
}
\]

という**真の商の粗化**を証明した。旧生七セル値の厳密Eqは一切主張しない。

## 6. 元P77全raw添字への応用とsource authority

`pentagonActualInverseCompOverlap_newVsInvolutionWithSourceObstruction`は真正元P77の各最終raw添字`i`に対応する元GK5CG保守的五セルの二端点、およびそこから独立に付加された六セルpentagon生成元`c`を使用する。新比較は存在し、旧比較は不在であり、元`PentagonAdjoinedSixCellEqualityInterpreter`は引き続き存在しないことを同時に形式証明。

**元F55/P77/GK5CGに新しい六／七／八セルsource生成元は追加していない。** 独立Kuu=presentation、strict空中心、元Type値と依存証明履歴を別々に保持する。

## 7. 証明境界と次候補

本段階は第三の障害の検出と、**限定したcritical peak族での局所補完**までの結果である。任意の平行七セル履歴が新八セルで比較できるという大域完全性や九セル自然性は未証明である。

次候補Qi v4.96：三つの独立整数不変量の組`(sevenTriangleCharge, sevenInvolutionCharge, sevenInverseCompCharge)`を、**どの段階の高次商でwell-definedになるか**に応じて区別する。原始七セル規則の残るcritical peakの具体例を抽出し、既存補完での合流性または新しいobstructionを形式証明する。

---
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
