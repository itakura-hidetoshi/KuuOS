# Qi v4.98 — identity／doubleInverseの最小高次局所補完・第四整数の非降下

## 0. Canonical正本・exact-source検証

2026年11月7日 JST。Repository `itakura-hidetoshi/KuuOS`、唯一のcanonical branch `main`。
Qi v4.97の統合済み正本 `e50937b1f7af0adeb188c4ab4cee8f21bfd3a707` から継承。
既存Lean定理・元GK5CG五セルsource・旧八セル構成子・旧商は一切上書きしない。

| 項目 | GitHub MCPでの確定結果 |
|---|---|
| Lean定理PR | [#3219](https://github.com/itakura-hidetoshi/KuuOS/pull/3219) — MERGED |
| 検証済みexact-source HEAD | `a3e1e88e4a7d3ffbb3233e81752c0ab5c1164058` |
| 定理squash／定理正本HEAD | `8bab61588ad8823c082a81534bcb34578c483ffe` |
| source/test-merge Git tree | `0007ca7c8c64970f37d8f692c4b91ed60d31c0cf` — 完全一致 |
| exact-source CI | [#42297159427](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42297159427) — SUCCESS |
| Strict Lean | **10,297／10,297 SUCCESS** |
| Governance | **30／30 SUCCESS** |
| 追加公理監査 | **23宣言**、標準公理 `propext`／`Classical.choice`／`Quot.sound` のみ |
| `sorryAx`／変更Lean warning・error | **なし／0・0** |
| pin | Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開集約 | `KuuOSFormal`、公開root107維持 |
| 保護PR #1558 | Draft／OPEN／未マージ |

[Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77IdentityDoubleHigherLocalCompletionV4_98.lean) · [前段Qi v4.97正式記録](Qi-v4_97-original-P77-identity-balance-hidden-seven-cell-critical-pair.md)

## 1. 前段の第四整数障害を局所的に埋める意義

元v4.89の真正13構成子 `SevenRewrite` に対して、Qi v4.97で導入した第四整数 `sevenIdentityBalance`（略記 `R`）は、v4.95の最終 `InverseCompEightCell` grammarで保存される。

ただし真正の二つの七セル履歴

- `sevenIdentityDoubleDirect(w)`: `doubleInverse(refl(w))` の直接簡約
- `sevenIdentityDoubleVia(w)`: 二回の `inverseId(w)` による簡約

は元六セルの同じ始終点を持ちながら

\[
R(H_{\mathrm{direct}})=0,\qquad R(H_{\mathrm{via}})=2
\]

となる。Lean定理 `sevenIdentityDouble_balanceGap` がこの差を実計算し、`sevenIdentityDouble_noPrevious` が旧比較の不存在を証明する。これは探索不足でなく、全v4.95構成子でのR保存則からの形式的な不可能性である。

## 2. 独立したIdentityEightCellと新生成元1種類

新規の高次比較 `IdentityEightCell(W,l,r,s,t) : Type` を定義し、

- `previous`: 旧 `InverseCompEightCell` の全証拠を保存する
- `identityDouble(w)`: 上の直接・via二経路を比較する**唯一の新しい原始八セル生成元**
- `reverse`・`chain`・`whiskerLeft`・`whiskerRight`・`inverseContext`・`compositeContext`: 型付き証拠の閉包

を構成した。元の `EightCell`、`TriangleEightCell`、`InvolutionEightCell`、`InverseCompEightCell` および元sourceには追記すら行わない。

`identityEightCell_strictlyNew` と `identityEightCell_noPreviousInterpreter` により、**新比較が成立するが旧比較が成立しない**真正履歴を指定し、旧presentationへの普遍的逆Interpreterが存在しないことを証明する。

## 3. v4.97で三整数では見えなかった複合critical pairの実際の補完

前段で構成した `sevenHiddenCriticalFirst(w)` と `sevenHiddenCriticalSecond(w)` は、

\[
(T,J,K)(H_1)=(T,J,K)(H_2)=(1,1,0),
\qquad R(H_1)=0,\ R(H_2)=2
\]

を満たす。旧v4.95 `InverseCompEightCell` による比較は不可能。

新しい `identityHiddenCritical_fill` は、この複合二経路を**原始的なhidden専用八セル生成元なし**で比較する。具体的には、三つの型付き区間の比較を

1. 新 `IdentityEightCell.identityDouble`（二重反転・恒等元）
2. 旧 `InvolutionEightCell.leftOverlap`（二重反転と逆元消去）
3. 旧 `TriangleEightCell.leftTriangle` の向きを反転（単位・結合三角形）

として構成し、既存の `compositeContext` によって貼り合わせる。

`identityHiddenCritical_newVsOld` は新規Type値比較の存在と旧比較の不存在を同時に証明する。

## 4. 限定critical peak族の全構成子合流証拠

`IdentityCriticalPeak` は従来の `InverseCompCriticalPeak`、新原始 `identityDouble`、すでに構成された複合 `hiddenComposite` と、指定した型付き文脈閉包からなる。

`identityCriticalPeak_fill` は全構成子に対する構造帰納法で、具体的 `IdentityEightCell` の値を構成する。続く `identityCriticalPeak_joinable` と `identityCriticalPeak_classEq` は、指定族のすべてに新比較と新商での等式が成立することを保証する。

これは**指定族に限る局所完全性**であり、任意の平行七セル履歴が比較可能、あるいは新八セルがthinであるという主張ではない。

## 5. 高次商の厳密な粗化と第四整数の非降下

`identityHistorySetoid`、`identityHistoryClass` を定義し、`identityHistoryClass_eq_iff` が新商でのEqと新Type値八セル証拠のNonemptyを同値化する。

`inverseCompHistoryClass_descendsToIdentity` により、旧商で一致する履歴は新商でも一致する。逆方向は成立しない。

`identityHistoryClass_strictlyNew` と `identityHiddenCritical_strictlyNew` は、それぞれ原始二経路およびv4.97の三整数不可視の複合二経路を使い、

\[
[H_1]_{4.98}=[H_2]_{4.98},
\qquad
[H_1]_{4.95}\ne[H_2]_{4.95}
\]

を形式証明する。

さらに `identityHistoryClass_noBalanceDescent` により、第四整数 `R` は旧v4.95の商では保存されるが、新v4.98の商に対して普遍的にはwell-definedでないと確定する。特定の二つの比較履歴に0≠2の差があるためである。

`identityHistoryClass_noPreviousReturn` と `identityHistoryClass_noStrictReturn` は、新商Eqから旧商Eqや生の七セルraw Eqへの全域的な戻りが不可能であることを保証する。

## 6. 元GK5CG真正sourceへの輸送とauthority境界

`pentagonActualHiddenCriticalCompletionWithSourceObstruction` は、元P77の任意最終raw添字について、

- 新 `IdentityEightCell` ではv4.97の三整数不可視複合二経路の比較が存在する
- 旧 `InverseCompEightCell` ではその比較が存在しない
- 元 `PentagonAdjoinedSixCellEqualityInterpreter` は引き続き存在しない

を同じ真正GK5CG五セル二端点上で証明する。

strict 空中心と独立Kuu = presentationは同一視せず、元五セルType値、六セル生履歴、七セル生履歴、選択した八セルpresentation、それぞれの商・観測値の権限を保持する。

## 7. 到達点・次段階

Qi v4.97は三整数には見えない第四整数障害の存在を証明した。Qi v4.98はそれを**比較生成元1種類の局所補完で構成的に埋めた**。さらに、埋めたこと自体が第四整数の非降下と新旧高次商の厳密な差を生み出すことをLean4形式証明した。

次段階Qi v4.99では、今回の新原始 `identityDouble` と既存 `inverseComp`・`doubleInverse` の複合文脈内で生じる高次critical peakを探索する。現在までの限定局所完全性を一般大域coherenceと混同しない。

---
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
