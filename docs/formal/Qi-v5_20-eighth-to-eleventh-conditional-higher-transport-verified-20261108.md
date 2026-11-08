# Qi v5.20 — 第八セルから第十一セルへの条件付き型付き高次transportと履歴障害

## 0. 正本・exact-source検証

2026年11月8日 JST。唯一のcanonical repository `itakura-hidetoshi/KuuOS`、branch `main`。
v5.19の定理PR [#3290](https://github.com/itakura-hidetoshi/KuuOS/pull/3290)と
正式記録PR [#3291](https://github.com/itakura-hidetoshi/KuuOS/pull/3291)の統合済み
`c807a5d33f5c6caaf94d027f408dfb9b0a228ebe`を基点とする。

| 項目 | 独立再観測による検証 |
|---|---|
| 定理PR | [#3292](https://github.com/itakura-hidetoshi/KuuOS/pull/3292) MERGED |
| source HEAD | `52635055ccd306d7615044c5842663212d579f27` |
| test-merge HEAD | `5c953b7600126e952919752d122d490c00d285be` |
| squash / main | `1bd92631f8ea6bc2ab371bdebe13d6ba3721a016` |
| 3者同一Git tree | **`c38b498bae591f38cc6b86ad16b737036b12f023`** |
| exact-source CI | [#42430525355](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42430525355) SUCCESS |
| Strict Lean | **10,333 / 10,333 SUCCESS** |
| Governance | **30 / 30 SUCCESS** |
| 新規 `#print axioms` | **11 / 11、全11宣言とも公理不要** |
| `sorryAx` | **なし** |
| 新規Leanファイル | 300追加行、既存Leanの削除・修正なし |
| 公開集約 | `formal/KuuOSFormal.lean` にimport 1行追加、root107維持 |
| Lean/mathlib固定 | Lean v4.30.0-rc2 / mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 保護PR #1558 | Draft / OPEN / 未マージ維持 |

[Lean4原文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77EighthToEleventhConditionalTransportV5_20.lean)。
元のF55/P77/GK5CG、独立した第六〜第十二セル、元の証拠Type・添字・raw履歴には手を加えない。
運用原則はappend-only / tighten-only / overwrite-forbidden / same-root。

## 1. 第八セル境界compatibleと上位transportを区別

v5.18は、元の第七セルの異なる二つの括弧付けに対し、
始域・終域の両方の真正`EightCell.associate`比較を構成した。
しかし第八セル比較は生の`SevenRewrite`や
`FramedElevenExactSpine`の等号ではない。
v5.19はその区別を利用し、旧第十二セルへの降下条件に
真正の下位spine等号を必要とすることを証明した。

v5.20では独立Type `TraceFaithfulHigherTower` を導入する。
そのデータは実在する始域・終域第八セル比較
`sourceEight`、`targetEight`に加え、
元の証拠型から元の証拠型への次の依存関数である。

\[
\begin{aligned}
T_8 &: P_8(s,t) \to P_8(s',t'),\\
T_9 &: N_9(q,q') \to N_9(T_8q,T_8q'),\\
T_{10} &: U_{10}(\alpha,\beta)
  \to U_{10}(T_9\alpha,T_9\beta),\\
T_{11} &: X_{11}(\xi,\zeta)
  \to X_{11}(T_{10}\xi,T_{10}\zeta).
\end{aligned}
\]

ここで`P_8`、`N_9`、`U_{10}`、`X_{11}`は、それぞれ
**既存の** `PentagonAssocEightCell`、`MixedCancelNineCell`、
`MixedUnitAssocTenCell`、`MixedExchangeUnitElevenCell` である。
関数は独立の**追加の型付き証明データ**であり、
`sourceEight` / `targetEight`だけから自然に存在するとは主張しない。

## 2. 旧第十セルの履歴保存条件

上記towerでは全ての元の第十セル値について

\[
\boxed{\operatorname{Trace}_{10}(T_{10}\xi)
      =\operatorname{Trace}_{10}(\xi)}
\]

を`preserveTenthTrace`として要求する。
`Trace_{10}`はv5.18の`mixedTenWhiskerRawTrace`という
元の順序付きBool履歴である。新しい商を経由する観測ではない。

`traceFaithfulTowerId`は第八セルの真正`reflexive`と
各証拠型の恒等写像からなる基準例を構成する。
`traceFaithfulTowerComp`では第八セルの真正`chain`と
各段の型付き写像を合成し、
\(\operatorname{Trace}_{10}(B_{10}(A_{10}\xi))
 =\operatorname{Trace}_{10}(\xi)\)
を証明する。上位Typeを強制的に等号へ潰さない。

## 3. 元Type値のtransportと条件付き第十二セル比較

`traceFaithfulTowerTransportFrame`は与えられた真正元第十一セル
\(H:X_{11}(\xi,\zeta)\)を、元の第九・第十・第十一セル型に沿って
transportし、移送先の`FramedEleven`を構成する。

Lean定理：
- `traceFaithfulTowerTransportFrame_preservesTrace`：順序履歴の保存
- `traceFaithfulTowerTransportFrame_id`：元packetの恒等復元
- `traceFaithfulTowerTransportFrame_comp`：tower合成と元packet移送の一致

**元第十二セル比較の追加条件**も隠さない。
移送先の同一元fiberで真正旧v5.17
\(C:\operatorname{Twelve}_{\mathrm{old}}(T_{11}H,K)\)
が別途与えられた場合に限り、
`traceFaithfulTowerOldTwelfth`がv5.19の
**inherited-only** framed比較を構成し、
`traceFaithfulTowerOldTwelfth_toFull`がv5.18の全framed比較へ埋め込む。

これは**移送後packetと移送先Kとの比較**であり、
等しくない元の入力packetと出力packetに
旧same-fiber第十二セル比較を捏造するものではない。

## 4. 真正二重whiskeringの履歴障害

任意の元の第六〜第十一セル文脈`before, H, after`について、
v5.18の二つの真正framed packetはsource／targetの両方に
第八セル結合証拠を持つ。しかし元第十セルの順序列は

\[
\boxed{
\begin{aligned}
\operatorname{Trace}_{10}(\mathrm{leftAfterRight})
  &= [\mathrm{false},\mathrm{true}]\mathbin{+\!+} T,\\
\operatorname{Trace}_{10}(\mathrm{rightAfterLeft})
  &= [\mathrm{true},\mathrm{false}]\mathbin{+\!+} T.
\end{aligned}}
\]

`doubleWhisker_noTraceFaithfulTower`は、
**全ての真正元文脈で**、左入力を右framed packetそのものへ移す
`TraceFaithfulHigherTower`が存在しないことを証明する
（より正確には、右packetを出力するtowerの存在を否定する）。
`doubleWhiskerEightCompatible_notTraceLiftable`は
真正第八セル境界証拠の存在とこの不可能性を同時に証明する。

これはv5.19の「全spine strict Eq不能」を
**第八セルを起点とする条件付き上位証拠transport**へ拡張した障害であり、
trace保存を要求しない任意の将来のtransportまで
存在しないと主張していない。

## 5. authority境界・次段研究

本段で実際に示したのは、追加した型付きtowerの恒等・合成・元11D移送、
移送先の旧12D比較が与えられる場合の正しい取り込み、
および履歴保存と左右二重whiskeringとの不整合である。
**非恒等tower一般の存在、source8/target8からの自動的な上位写像、
普遍的な8D→11D強制昇格、完全な旧same-fiber降下、
一般thinness、高次商からのsource復元は未証明。**

次段Qi v5.21では、既存原始から構成可能な
*非恒等*上位transportと、trace-preserving条件を緩めた場合の
本物の高次naturality/interchangerの有無を分類する。
元の全証拠値・各presentation・obstruction・authorityを
独立して保持する。

---

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0。
