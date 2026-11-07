# Qi v5.18 — 真正二重whiskeringのframed第十二セルと境界整合

## 0. Canonical正本・厳密な検証証跡

2026年11月8日 JST。Repository `itakura-hidetoshi/KuuOS`、canonical branch `main`。
Qi v5.17までの元F55/P77/GK5CGおよび独立第六〜第十二セル文法を変更せず、
異なるraw indexを持つ真正二重whiskering比較のため、独立したframed第十二セルを追加した。

| 項目 | exact-source確認値 |
|---|---|
| 定理PR | [#3288](https://github.com/itakura-hidetoshi/KuuOS/pull/3288) **MERGED** |
| 定理squash | `cc207c5a0f8aab07b29699ea1139ce62e4ac9b00` |
| exact-source CI | [#42426418988](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42426418988) **SUCCESS** |
| Strict Lean | **10,331 / 10,331 SUCCESS** |
| Governance | **30 / 30 SUCCESS** |
| 新規宣言の`#print axioms` | **43 / 43**、公理なし34・標準公理のみ9 |
| 公理集合 | `propext`／`Quot.sound`／`Classical.choice`のみ |
| `sorryAx` | なし |
| 変更Lean warning/error | **0 / 0** |
| 検証source HEAD | `b63f918c7b6713c2ea1c82f57dee540d9144c12d` |
| 検証test-merge | `3c774f7882f07e1497b74905d23bdc698d0df58b` |
| source/test-merge Git tree | **`fbb6d57db380d23ca14b8703773f3225d8cbec22` 完全一致** |
| 公開集約 | `KuuOSFormal`、公開root107維持 |
| 固定Lean | `v4.30.0-rc2` |
| 固定mathlib | `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 保護PR #1558 | Draft／OPEN／未マージ維持 |

[Lean 4証明全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77DoubleWhiskerFramedTwelfthV5_18.lean)。
新規独立Leanモジュールは修正後639行、公開集約はimport 1行追記のみ。
旧証拠型・既存定理・toolchain・workflowは変更していない。

## 1. 障害の正しい位置：二重whiskeringは同一fiberとは限らない

元の型付き第十一セル証拠 `H : MixedExchangeUnitElevenCell W l r xi zeta` に対して、
真正七セル `before` と `after` を使い、以下の元構成子を適用する：

\[
\begin{aligned}
L&=\operatorname{whiskerLeft}
 (before,\operatorname{whiskerRight}(H,after)),\\
R&=\operatorname{whiskerRight}
 (\operatorname{whiskerLeft}(before,H),after).
\end{aligned}
\]

元の第七セルsource indexはそれぞれ

\[
s_L=before\mathbin{\mathrm{trans}}(s\mathbin{\mathrm{trans}}after),
\qquad
s_R=(before\mathbin{\mathrm{trans}}s)\mathbin{\mathrm{trans}}after.
\]

target indexも `t` を代入して同様に異なる。これらは単なる第十一セルの異なる証明だけでなく、
**第七セルの生文法上の括弧付けが異なる**。
従って、従来の同一のraw tenth両端点に索引付けされた`MixedExchangeInverseTwelveCell`
へ、型の一致を偽装して押し込んではならない。

一方、v4.91の元`EightCell.associate`を反転した

\[
A_s:s_L\Rrightarrow s_R,\qquad A_t:t_L\Rrightarrow t_R
\]

は真正Type値の第八セルとして構成可能。`doubleWhiskerSourceBoundaryAssociate`、
`doubleWhiskerTargetBoundaryAssociate`、
`doubleWhiskerBoundaryCompatibility`で**sourceとtargetの両方**のcompatibilityを証明した。
これは旧七セルのstrict raw Eqではない。

## 2. 旧証拠を保持するframed第十一セルpacket

`FramedEleven W l r`は、元の証拠を忘れずに次のすべてを依存フィールドで保持する。

- 第六セル：`w,z,c,d`
- 第七セル：`s,t`
- 第八セル：`q₀,q₁`
- 第九セル：`alpha,beta`
- 第十セル：`xi,zeta`
- 第十一セル：真正のraw証拠 `H`

`framedEleven_ofRaw`は元の同一fiber第十一セルからframed packetへの忠実な**型付き包含**を与え、
`doubleWhiskerLeftAfterRightFrame`／`doubleWhiskerRightAfterLeftFrame`は、
二つの元二重whiskeringを、それぞれ完全なraw indexを保持したpacketとして構成する。

元Qi v5.16の真正 `exchangeUnit` に左右の七セル反射を作用させた
`originalDoubleWhiskerLeftFrame`／`originalDoubleWhiskerRightFrame` が実際の比較対象となる。

## 3. 新しい最小framed第十二セル

`FramedDoubleWhiskerTwelveCell`は独立した型付きcomparisonであり、
**全5構成子のうち、新しい局所primitiveは`doubleWhisker`ただ1種**：

1. `strict`：framed packet自体の反射
2. `previous`：Qi v5.17既存`MixedExchangeInverseTwelveCell`の同一fiber証拠を元index付きで継承
3. `doubleWhisker`：元の二つのraw順序を持つframed packetの唯一の新しい局所比較
4. `reverse`：型付き反転
5. `chain`：型付き連鎖

`originalDoubleWhiskerFramedCompletion`は、真正元`exchangeUnit`の二つのframed packetが
**新型で比較可能かつraw packetとして非等**であることを同時に証明する。

`framedDoubleWhiskerSetoid`と`framedDoubleWhiskerClass`で選択商を構成。
新商では両packetのクラスが等しい一方、
`framedDoubleWhisker_noRawEqualityInterpreter`はframed比較を生packetのEqへ変換する全称解釈の不存在、
`framedDoubleWhiskerClass_noRawRetraction`は新商からの全raw復元の左逆不存在を証明する。

**重要な境界**：これは旧同一fiber第十二セルが万能のinterchangerを得たという意味ではなく、
境界の整合証拠を型付きで持つ**別presentation**での局所的な降下である。

## 4. raw順序は失われ、3種の独立観測量は保存される

`mixedTenWhiskerRawTrace`は第十セルの真正 `whiskerLeft` と `whiskerRight` 構成子を
Bool列 `false`／`true` として記録する生履歴observerである。
元critical peakでは

\[
T(L)=[\mathrm{left},\mathrm{right}],\qquad
T(R)=[\mathrm{right},\mathrm{left}]
\]

という異なるprefixを持つ。元の十セル証拠自体にも任意の履歴がある場合、
このprefixの後ろにその元の履歴がそのまま続く。
`doubleWhiskerRawTraceValues`／`doubleWhiskerRawFrameGap`で厳密差を証明。
`framedDoubleWhiskerClass_noRawTraceDescent`は、**この順序列を忠実に再現する観測量は
新選択商上には存在しない**ことを形式証明した。

一方、保存する観測量は

\[
\boxed{
(N_{\mathrm{old}},N_{\mathrm{unit}},
 N_{\mathrm{tenSymm}})\in\mathbb N^3.
}
\]

それぞれ元Qi v5.16の旧十セル証拠数・単位第十セル数、
v5.17の真正第十一セル`tenSymm`wrapper数である。

3つの`framedDoubleWhisker_preserves...Count`定理は
**framed第十二セルの全5構成子**を構造帰納法で覆う。
各保存則について独立の `Quotient.lift` を持ち、
代表元評価の等式も形式証明済み。

元の二重whiskeringの二packetはどちらも

\[
(N_{\mathrm{old}},N_{\mathrm{unit}},N_{\mathrm{tenSymm}})
=(1,1,0)
\]

で一致する。順序は異なるが3成分の数は保存されるという構造は、
順序の消去と不変量の保持を明確に区別する。

## 5. 残存障害と非global thin性

v5.17から保持した真正の `tenSymm(strict rfl)` と対応する`strict rfl`を
framed packetとして再構成したところ、

\[
\boxed{N_{\mathrm{tenSymm}}(L)=1,\quad
       N_{\mathrm{tenSymm}}(R)=0.}
\]

従って、全5構成子の保存則からこの2つは新framed第十二セルでは比較不能。
`framedOriginalTenSymm_noComparison`、
`framedOriginalTenSymm_distinctClass`、
`framedDoubleWhisker_notGloballyThin`で証明されている。

元の第十セルの独立二往復障害 `(2,0)`／`(0,2)`に対する
旧第十一セル比較不存在は`framedDoubleWhisker_retainsOriginalTenthBarriers`で維持した。

さらに、`pentagonActualDoubleWhiskerFramedCompletion`は
任意の元P77 final raw indexにおける真正GK5CG long/short五セルType値で
新framed比較が成立し、同時に元
`PentagonAdjoinedSixCellEqualityInterpreter`の不存在が保持されることを証明する。

## 6. Lean4構文エラーの原因と修正

初回CI [#42426062238](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42426062238)は、
`framedDoubleWhiskerClass_noRawTraceDescent` の1証明箇所で失敗した。
`exact (by ... ) h`の匿名`by`に期待型が提供されず、
`invalid 'by' tactic, expected type has not been provided`が発生した。

修正では定理文・仮定・証明構成子を変更せず、
既に取得した等式`h`に対して`change ... at h`で具体的な
`false :: true :: ... = true :: false :: ...`へ形を固定し、`cases h`で矛盾を閉じた。
その後のexact-source CIは10,331ジョブSUCCESS、
43宣言の監査に`sorryAx`なし、変更Lean warning/error 0/0。
失敗局所のみでなく、新規Lean全文・imports・元依存signatureを照合した。

## 7. 次段Qi v5.19

次のfrontierは**framed第十二セルと元の同一fiber第十二セルの境界輸送の正確な条件**を調べること。
元第八セルassociatorによる境界の整合から、
第九セル・第十セル・第十一セルの型付きtransportをどこまで合成できるかを分離し、
**比較可能な場合だけ**元fiberへ戻す部分的descentを構成する。
効果的なreindexingを無条件に仮定せず、独立不変量と残存障害を保持する。

---

Copyright © 2026 Hidetoshi Itakura / 板倉英俊。Apache-2.0。
