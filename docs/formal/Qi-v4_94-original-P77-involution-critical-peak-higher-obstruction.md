# Qi v4.94 — 二重反転／逆元消去の高次critical peak・独立整数障害と局所八セル補完

## 0. 正本／exact-source検証

2026年11月6日 JST。唯一のcanonical repository/branch：`itakura-hidetoshi/KuuOS`／`main`。

| 項目 | 確定状態 |
|---|---|
| 継承起点 | Qi v4.93、`8cba11392275f8125b994f385d283404769cc675` |
| 定理PR | [#3211](https://github.com/itakura-hidetoshi/KuuOS/pull/3211) — MERGED |
| 検証済みexact-source HEAD | `fe9f1452823a2b619b791bffd1bf363e904c2700` |
| 定理squash／定理正本HEAD | `d41f2aed91d7dc4b9aded5987343f99456f9d4fb` |
| source／test-merge／squash Git tree | `f094dc464e87792e03a991e108ceea9645280e7d` — 完全一致 |
| Exact-source CI | [#42216666765](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42216666765) — completed/SUCCESS |
| Strict Lean | **10,293／10,293 SUCCESS** |
| Governance | **30／30 SUCCESS** |
| 新規公理監査 | 25宣言、標準公理`propext`／`Classical.choice`／`Quot.sound`のみ、`sorryAx`なし |
| 変更Lean warning／error | **0／0** |
| Pin | Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開集約・root | `KuuOSFormal`、root107維持 |
| 保護PR | #1558 Draft／OPEN／未マージ |

[検証済みLean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77InvolutionOverlapHigherObstructionV4_94.lean) · [Qi v4.93正式証明記録](Qi-v4_93-original-P77-triangle-critical-peak-eight-cell-charge-obstruction.md) · [真正独立GK5CG元source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5CGP77FiveCellAssociatorCharge.lean)

## 1. 前段階と新しい問題

Qi v4.91では新しい八セル`EightCell(H₁,H₂)`を自由生成し、v4.92で局所zigzag／独立書換えの限定critical peakの合流と履歴商を構成した。Qi v4.93では、七セル結合・単位の三角形ピークを既存22八セル生成規則では埋められないことを整数`sevenTriangleCharge`で証明し、**元のEightCellを変更せず**に別Type`TriangleEightCell`を導入した。

v4.94はこの拡張でもなお残る、七セルの`doubleInverse`と`inverseLeft`／`inverseRight`が重なる**二つの新critical peak**を具体的に扱う。

## 2. 第二の独立した七セル整数不変量

`sevenInvolutionCharge` は元の13構成子による`SevenRewrite`の**生の七セル履歴**を入力し、`doubleInverse`だけを+1で数える。他の基本局所規則は0、七セル履歴`symm`は符号反転、`trans`・`congrComp`は加法、`congrInv`は値を保持する。

\[
\begin{aligned}
J(\mathrm{doubleInverse}(c))&=1,\\
J(\mathrm{symm}(H))&=-J(H),\\
J(\mathrm{trans}(H,K))&=J(H)+J(K),\\
J(\mathrm{congrComp}(H,K))&=J(H)+J(K),\\
J(\mathrm{congrInv}(H))&=J(H).
\end{aligned}
\]

`eightCell_preservesInvolutionCharge`は元v4.91の22八セル構成子すべてへの構造帰納により、この値が保存されることを証明する。

さらに重要な`triangleEightCell_preservesInvolutionCharge`は、v4.93で追加した**左右三角形二生成元を含むすべての`TriangleEightCell`**について同じ保存を構造帰納で証明する。

\[
\boxed{
Q:\mathrm{TriangleEightCell}(H_1,H_2)
\Longrightarrow J(H_1)=J(H_2).
}
\]

ここで`J`はv4.93の`sevenTriangleCharge`とは**別の不変量**である。前回の三角形補完で消えない新たなobstructionを検出する。

## 3. 実際の二重反転／逆元消去critical peak

任意の新六セル生語`c:w⇒z`について、左右に対応する型付きの二つの重なりを扱う。

**左側：** 生六セル語`symm(symm c);symm c ⇒ refl w`への七セル比較。

- `sevenLeftDoubleInverseDirect c := inverseLeft (symm c)`：直ちに逆元消去。
- `sevenLeftDoubleInverseVia c := trans (congrComp (doubleInverse c) (refl (symm c))) (inverseRight c)`：先に二重反転を消去し、その後右逆元消去。

**右側：** 生六セル語`symm c;symm(symm c) ⇒ refl z`への七セル比較。

- `sevenRightDoubleInverseDirect c := inverseRight (symm c)`。
- `sevenRightDoubleInverseVia c := trans (congrComp (refl (symm c)) (doubleInverse c)) (inverseLeft c)`。

`sevenLeftDoubleInverse_chargeGap`と`sevenRightDoubleInverse_chargeGap`でそれぞれ

\[
\boxed{
J(H_{\rm direct})=0,\qquad J(H_{\rm via})=1
}
\]

を形式証明。既存拡張での保存則から

\[
\boxed{
\neg\operatorname{Nonempty}
\bigl(\mathrm{TriangleEightCell}(H_{\rm direct},H_{\rm via})\bigr)
}
\]

が左右のピークで成立する（`sevenLeftDoubleInverse_noTriangleEightCell`／`sevenRightDoubleInverse_noTriangleEightCell`）。これは**元の三角形八セル拡張の全構成子に対する証明済み非合流**であり、単に証明書が見つからないという意味ではない。

`sevenLeftDoubleInverse_notStrict`は生の七セル履歴そのものの厳密不一致も明示する。

## 4. 新しく独立に付加した八セルType

元の`EightCell`や`TriangleEightCell`は書き換えない。別の`InvolutionEightCell(H₁,H₂):Type`を導入し、`.previous`により旧`TriangleEightCell`を全て包含し、左・右の二重反転ピークの**二つだけ**を新たなprimitive generator `.leftOverlap`・`.rightOverlap`として追加する。残りは反転・連鎖・左右whiskering・六セル反転／合成文脈への閉包である。

`involutionEightCell_leftNewNotPrevious`および`involutionEightCell_rightNewNotPrevious`は、以前の比較Typeでは空、新拡張では居住することを同時に証明。

`involutionEightCell_noPreviousInterpreter`は、全新証拠を旧`TriangleEightCell`へ送る普遍関数が存在しないことを、**Type値Pi型について正しく**`¬ Nonempty (∀ ..., InvolutionEightCell → TriangleEightCell)`として証明する。`involutionEightCell_noStrictInterpreter`は新証拠から生七セル構文の厳密Eqへの戻りも不可能であると示す。

## 5. 限定的critical peak族と商の厳密な区別

`InvolutionCriticalPeak`は前版`TriangleCriticalPeak`の全証拠を包含し、上の左右二重反転ピークを付加し、反転・連鎖・前後whiskering・反転／合成文脈にのみ閉じる**限定された9構成子**の帰納Type。任意平行七セル履歴という無条件構成子を持たない。

`involutionCriticalPeak_fill`では帰納法により各`P : InvolutionCriticalPeak(H₁,H₂)`から実際の`InvolutionEightCell(H₁,H₂)`を構成し、`involutionCriticalPeak_joinable`が存在定理を与える。

`involutionHistorySetoid`は比較存在から作る反射・対称・推移を満たすSetoid。選択商`involutionHistoryClass`について

\[
[H_1]_{\mathrm{inv}}=[H_2]_{\mathrm{inv}}
\iff \operatorname{Nonempty}
\bigl(\mathrm{InvolutionEightCell}(H_1,H_2)\bigr)
\]

を形式証明する。旧`triangleHistoryClass`で成立する商の等号は新商へ降下し、逆方向の普遍的な復帰はできない。

特に`involutionHistoryClass_strictlyNew`により

\[
\boxed{
[H_{\rm direct}]_{\mathrm{inv}} =
[H_{\rm via}]_{\mathrm{inv}}
\quad\land\quad
[H_{\rm direct}]_{\triangle}\ne
[H_{\rm via}]_{\triangle}
}
\]

がLean4で成立。高次比較可能性の増大を**新旧商の厳密な非同値**で確認した。

## 6. 真正P77元sourceとの境界

`pentagonActualInvolutionOverlap_newVsTriangleWithSourceObstruction`は任意の元P77最終raw添字`i`において、元GK5CG保守的五セル値の真正指定二端点から六セルpentagon生成元`c`を選ぶ。

同じ元source添字上で、新`InvolutionEightCell`比較は存在し、元`TriangleEightCell`比較は存在せず、元`PentagonAdjoinedSixCellEqualityInterpreter`も存在しないことを同時に証明する。

これは元F55/P77/GK5CGの六／七／八セルsource構成子を追加したことではない。真正五セル値の厳密不一致と元電荷no-goはそのまま保持する。

## 7. 検証境界と次の研究候補

今回の定理は**すべての平行な七セル履歴に対する高次coherence完全性ではない**。二つの独立整数不変量と、各段階で必要と証明できた有限種類の局所生成元という区別を保持する。第九セルや元sourceへの無条件の降下も主張しない。

次候補Qi v4.95：二つの整数不変量を同時に用いたobstruction判定、さらに`inverseComp`と`assoc`・単位の重なりの具体的peak分類。新拡張で消えない障害を確認してから最小限の新規則を判断する。

---
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
