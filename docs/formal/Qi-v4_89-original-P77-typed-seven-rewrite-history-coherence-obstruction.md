# Qi v4.89 — 真正元五セルTypeを保持した新七セル書換え履歴・次数健全性・厳密戻り障害

## 0. canonical正本・実検証

2026年11月6日 JST。Repository `itakura-hidetoshi/KuuOS`、canonical branch `main`。

| 項目 | 確定結果 |
|---|---|
| 継承元 | Qi v4.88、canonical main `1d91df4d3ccd7265c69dfc24288efd9e0a9aac48` |
| 定理PR | [#3201](https://github.com/itakura-hidetoshi/KuuOS/pull/3201) — MERGED |
| exact-source HEAD | `fac510534322bbca21b556db68aee716ae45db29` |
| 定理squash／定理正本HEAD | `4f8f400cd4b9622cbceb187c2436f05840f939f9` |
| source／test-merge／squash Git tree | `6df0683ca4a82c1650550860ea8d2752f83b7605` — 完全一致 |
| exact-source CI | [#42198422164](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42198422164) — completed/SUCCESS |
| Strict Lean | **10,288／10,288 SUCCESS** |
| Governance | **30／30 SUCCESS** |
| 公理監査 | 指定17宣言の`#print axioms`を実ログで確認。標準公理の範囲内（`propext`、`Classical.choice`、`Quot.sound`）、`sorryAx`なし |
| 変更Lean warning／error | **0／0** |
| pin | Lean v4.30.0-rc2／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| source／公開 | 元独立F55/P77/GK5CGを保持。公開root107と`KuuOSFormal`維持 |
| 保護PR | #1558 Draft／OPEN／未マージ |

[Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77TypedSevenRewriteHistoryV4_89.lean) · [Qi v4.88正式記録](Qi-v4_88-original-P77-six-cell-endpoint-normal-forms-degree-completeness.md) · [真正独立GK5CG source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5CGP77FiveCellAssociatorCharge.lean)

## 1. Qi v4.88からの数学的問題

Qi v4.86では、元の真正GK5CG保守的五セルTypeから得た選択五セル語 `L₃(i)`、`L₂(i)` を始終点とする、**別presentationの六セル自由語** `PentagonAdjoinedSixCell` を追加。Qi v4.85では元の五セル語の厳密不一致を形式証明済み。

Qi v4.87では、新六セルの構文次数 `degree` が等しい**平行**な生証明語を商に送った。Qi v4.88では真正`L₃(i)≠L₂(i)`を使い、次数は端点のポテンシャル差だけで決まり、新商が局所thinであると証明した。しかしこの商の等号だけでは、元の生六セル語`c`が`d`へどう書き換えられるかという**証拠履歴**を保持しない。

v4.89ではその証拠履歴自体を**新たなType値**として作る。元sourceに六セル／七セルがすでに存在したという主張ではない。

## 2. 新七セルType値帰納文法

`PentagonAdjoinedSixCell.SevenRewrite W l r c d : Type` は、元の**生の**六セル証明語 `c,d : PentagonAdjoinedSixCell W l r w z` を添字として両方保持する。

書換え生成元は13種：

1. `refl` — 証拠履歴の反射
2. `symm` — 七セル履歴の反転
3. `trans` — 履歴の縦合成
4. `congrInv` — 六セル反転への文脈適用
5. `congrComp` — 六セル合成への左右文脈適用
6. `leftUnit` — 左単位
7. `rightUnit` — 右単位
8. `assoc` — 合成の結合則
9. `inverseRight` — 右逆元消去
10. `inverseLeft` — 左逆元消去
11. `doubleInverse` — 二重反転
12. `inverseId` — 恒等の反転
13. `inverseComp` — 合成の反転則

**次数一致を要求するだけの任意の`degreeWitness`生成元は追加していない。** したがって商の等号と実際の書換え履歴は混同されない。局所書換えの導出可能性は個別に構成・検査する。

## 3. 全構成子に対する次数健全性

`sevenRewrite_degreeSound` は、13構成子すべての帰納法で

\[
\boxed{\mathrm{SevenRewrite}(c,d)\Longrightarrow\deg(c)=\deg(d)}
\]

を証明。合成文脈では加法の整合、逆元文脈では符号反転、結合則では整数加法の結合則、`inverseComp`では反転した和の整合をLeanの整数群計算で導いた。

`sevenRewrite_quotientSound` はこの証明をv4.87の`CoherentHom`商の等号 `[c]=[d]` に送る。ただし **`c=d` という生六セル証明語の厳密等号へは送らない**。

`sevenRewrite_degreeObstruction` は `deg(c)≠deg(d)` なら新七セルの`Nonempty`を否定。特に`selfPentagonLoop_noSevenRewrite`は、新presentationで追加元の両端を同一視した場合`l=r=w`、`pentagon:w→w` の次数が1、`refl:w→w`の次数が0となり、**その両者をつなぐ七セル書換えは存在しない**ことを証明した。これは元sourceの七セル不存在とは別問題である。

## 4. 非自明な履歴・旧厳密等号への戻り障害

`sevenRewrite_zigzagRight` は、次の書換えを`congrComp`・`inverseRight`・`leftUnit`の証拠を合成した**Type値**で構成する：

\[
(c\circ c^{-1})\circ c\xRightarrow{\mathrm{new\ seven}} c.
\]

`sevenRewrite_zigzagLeft` も対称的に構成する。

`sevenRewrite_roundtrip_exists_notStrict` は、新しい`pentagon`生成元について

\[
\mathrm{Nonempty}(\mathrm{SevenRewrite}(p\circ p^{-1},\mathrm{refl}))
\quad\land\quad
(p\circ p^{-1}\ne\mathrm{refl})_{\mathrm{raw}}
\]

を同時に証明。したがって、**新七セルの全証拠を生六セル語の厳密等式に解釈する写像は存在しない**（`sevenRewrite_noStrictInterpreter`）。元の五セルへの全端点保存EqualityInterpreter不存在も引き続き保持する。

## 5. 真正全P77 raw terminalへの型付き適用

`pentagonActualSevenRewrite_roundtrip`、`pentagonActualSevenRewrite_exists_notStrict`、`pentagonActualSevenRewrite_zigzag`、`pentagonActualSevenRewrite_zigzagQuotientSound`、`pentagonActualSevenRewrite_withOriginalNoGo`、`pentagonActualSevenRewrite_noStrictInterpreter`を形式証明。

任意の真正最終raw添字`i`に対して元の五セル値`L₃(i)`／`L₂(i)`を厳密なType値として保持し、それらを両端とする**新六セル**の往復とジグザグを、**新七セル**の証拠履歴として型付き構成。元F55/P77/GK5CG source、元四セル電荷+1 no-go、五セルの厳密不一致を変更しない。

この結果は具体的な局所書換えの健全性・存在証明であり、**商で同じ次数を持つ任意の平行六セル語が必ずこの13種の局所書換えで接続できること（完全性）はまだ証明していない**。

## 6. CI・実装・再観測

新規Leanモジュール1件（約376行）＋`formal/KuuOSFormal.lean`へのimport1行。他の既存Lean・manifest・pin・workflow・root107・保護PRは不変。最新exact-source CIは初回から全体SUCCESS。指定17件の`#print axioms`の実ログをGitHub MCPで確認し、`sorryAx`なし・変更警告／エラー0／0。source/test-merge Git treeを比較した上でHEADを指定しsquashマージし、mainのtree同一性も確認済み。

## 7. 次の研究候補 Qi v4.90

明示的な七セル局所書換えが、元の五セル端点が異なるとき**すべての平行な六セル証明語を接続するか**という完全性が次の真の課題。証拠履歴を保存した正規化アルゴリズム・上下文脈との可換性と停止性を、帰納Type値で構成する。v4.88のthin商だけを根拠に局所書換えの完全性を推論しない。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
