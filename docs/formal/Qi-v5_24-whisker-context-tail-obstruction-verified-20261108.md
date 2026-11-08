# Qi v5.24 — 保存される末尾履歴・三重whiskeringの欠けた面・商作用の非降下

## 1. 正本とexact-source検証

2026年11月8日 JST。Canonical repositoryは `itakura-hidetoshi/KuuOS`、branchは `main`。
Qi v5.23の定理#3298・正式記録#3299が統合された
`22bc1f72b12efdfbcb0b7345fd84de6d09deadb2`を継承した。

| 項目 | 確認済みの結果 |
|---|---|
| 定理PR | [#3300](https://github.com/itakura-hidetoshi/KuuOS/pull/3300) MERGED |
| source HEAD | `99a4ab5d79740e983634eeaa36f762f8f35059ae` |
| test-merge HEAD | `8fcdd5139f4e75a14df50c617c7a3aaebe717066` |
| squash / 定理main HEAD | `b954a76f452660d85158623aed0fdd7b1b7f8ec4` |
| 上記3 commitのGit tree | `0d688241b71fa787750b8fa6f74fe0ab2abcf916` 完全一致 |
| exact-source CI | [#42436351661](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42436351661) completed / SUCCESS |
| Strict Lean | 10,337 / 10,337 SUCCESS |
| Governance選択チェック | 30 / 30 passed、欠落receipt・失敗チェック・workflow failureなし |
| 新規宣言 | 27 / 27の `#print axioms` を確認 |
| 公理依存 | 24宣言は公理不要、3宣言は `propext`・`Quot.sound` のみ |
| `sorryAx` / 新規axiom | なし / なし |
| 変更Lean warning / error | 0 / 0 |
| 差分 | 新規Lean366行＋公開集約import1行、367追加・0削除 |
| Lean / mathlib | `v4.30.0-rc2` / `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開root / 保護PR | root107不変、#1558 Draft / OPEN / 未マージ |

[Lean証明全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77WhiskerContextTailObstructionV5_24.lean)。

Lean receiptはreturn code 0、実行対象test-merge SHAを記録し、完全ログの末尾は
`Build completed successfully (10337 jobs)`。
公理を使う3宣言は `tripleWhisker_threeClassSplit`、
`framedRightWhisker_noQuotientDescent`、`framedLeftWhisker_noQuotientDescent`。
これは新規27宣言の公理依存についての記録であり、過去の全リポジトリ宣言が公理不要だという主張ではない。

## 2. 比較生成元を増やさず、既存の全第十二セルに不変量を与える

元の第十セル順序履歴を `Trace10(F) = framedWhiskerRawTrace F` とする。
新しい観測量は、先頭2項だけを除いた末尾列：

\[
\boxed{I(F)=\operatorname{drop}_2(\operatorname{Trace}_{10}(F)).}
\]

`framedDoubleWhisker_preservesTail` は、既存の **全**
`FramedDoubleWhiskerTwelveCell` の5構成子を帰納して

\[
T:\mathrm{Framed12}(F,G)\quad\Longrightarrow\quad I(F)=I(G)
\]

を証明する。`previous`は元の同一fiberを保ち、`doubleWhisker`は
先頭の `[false,true]` と `[true,false]` だけを交換する。
`reverse`・`chain`でも等式が保存される。

`framedDoubleWhiskerTail` はこの結果を使う `Quotient.lift` で、
**既存のfull framed十二セル商**から `List Bool` への写像を構成する。
完全なraw traceはこの商へ降下しないが、この末尾観測は降下する。
全体の分類不変量であるという逆方向は主張しない。

## 3. 真正三重whiskeringの存在する面と存在しない面

元の型付き第十一セル `H` と第七セル文脈 `before,inner,outer` を使う。
以下のLRR/RLR/RRLは **構成子を外側から内側へ読む順序** であり、
操作を適用する時間順序とは逆である。右文脈の添字も明示する：

\[
\begin{aligned}
F_{LRR}&=L_{before}(R_{outer}(R_{inner}(H))),\\
F_{RLR}&=R_{outer}(L_{before}(R_{inner}(H))),\\
F_{RRL}&=R_{outer}(R_{inner}(L_{before}(H))).
\end{aligned}
\]

三つとも元の第六〜第十一セル証拠をそのまま保持した `FramedEleven` であり、
異なる依存fiberをEqで同一視していない。
`t = mixedTenWhiskerRawTrace xi` と置けば、

\[
\operatorname{Trace}_{10}(F_{LRR})=[0,1,1]++t,\quad
\operatorname{Trace}_{10}(F_{RLR})=[1,0,1]++t,\quad
\operatorname{Trace}_{10}(F_{RRL})=[1,1,0]++t.
\]

既存の `doubleWhisker before (whiskerRight H inner) outer` から
`tripleWhisker_outerAdjacentFace` が **実際の** `Framed12(F_LRR,F_RLR)` を構成する。
一方、保存末尾は

\[
I(F_{LRR})=I(F_{RLR})=1::t,\qquad I(F_{RRL})=0::t.
\]

したがって `tripleWhisker_missingInnerFace` と
`tripleWhisker_firstLastDisconnected` は

\[
\boxed{\neg\operatorname{Nonempty}(\mathrm{Framed12}(F_{RLR},F_{RRL})),}
\qquad
\neg\operatorname{Nonempty}(\mathrm{Framed12}(F_{LRR},F_{RRL}))
\]

を証明する。これは単に二つのraw証拠が異なるという結果ではなく、
**既存のprevious/reverse/chainをすべて使っても比較証拠が存在しない**という結果である。
`tripleWhisker_threeClassSplit` はこれを既存商における

\[
\boxed{[F_{LRR}]=[F_{RLR}]\ne[F_{RRL}]}
\]

へ接続する。分類対象はこの三つの実際のpacketであり、全packetの完全分類ではない。

## 4. 旧比較は外側文脈へ運べるが、full比較とその商は運べない

`framedUnitRightWhisker` と `framedUnitLeftWhisker` は、各packetの実際の
境界に反射第七セルを置き、元の十一セルwhiskeringを適用する。
この反射文脈でも、生証拠上は恒等操作ではない。

`framedUnitRightWhiskerInherited` と `framedUnitLeftWhiskerInherited` は、
旧 `FramedInheritedTwelfth` の全証拠をそれぞれの外側文脈へ移す。
旧v5.17の真正 `whiskerRight` / `whiskerLeft` が使えるためである。

これに対し、元 `exchangeUnit` から作った実際のdouble-whisker critical pairは
full商では等しいが、外側の左右いずれかの反射文脈を付けると末尾不変量が異なる。
`framedRightWhisker_noFullLift` / `framedLeftWhisker_noFullLift` は、
full比較の全証拠を同じfull比較内へ移す普遍的liftの不存在を証明する。
さらに左右それぞれの `noQuotientDescent` は、既存商 `Q12` 上に

\[
\phi:Q_{12}\to Q_{12},\qquad
\phi([F])=[\operatorname{Whisker}(F)]\quad(\forall F)
\]

を満たす写像が存在しないことを証明する。
**raw packet上で操作が定義できることと、選択した比較・商に作用が降下することは別である。**

## 5. 選択第十四セルでは欠けた下位の面を自動生成できない

v5.23の `CompositionalWhiskerThirteen` は実在する平行framed12D経路 `P,Q` を、
`SelectedCompositionFourteen` はその上の実在13D経路 `C,D` を添字に要求する。
`framedTailGap_noSelectedFourteen` と
`tripleWhisker_noSelectedFourteenthOverMissingFace` は、末尾不一致で12D経路自体がない
端点に対して、これら全境界証拠を伴う14D比較の存在も否定する。

これは、v5.23の条件付き合成cubeと矛盾しない。
v5.23が扱うのはすでに存在する12D経路間の選択比較であり、
今回欠けているのは、その比較以前に必要な **下位12Dの面** である。
新しいpresentationでcontext閉包を追加する可能性まで否定してはいない。

## 6. 次段階の研究境界

Qi v5.25では、元証拠を保持したまま、必要な外側文脈へのliftを持つ
**独立したcontext-closed十二セルpresentation** を検討する。
既存full比較の埋込み、実際の欠損面の補完、保持できる観測量と失われる末尾情報を
切り分けて証明する。単に十五セルなどを追加して欠けた下位境界を隠すことはしない。

今回の変更では、旧6D〜14Dの定義・生成元・仮定を一切変更していない。
この文書は新規の正式記録1件であり、README.md / ROADMAP.mdの既存本文は変更していない。
append-only / tighten-only / overwrite-forbidden / same-root。

---

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0。
