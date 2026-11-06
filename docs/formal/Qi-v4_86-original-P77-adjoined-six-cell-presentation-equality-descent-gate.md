# Qi v4.86 — 真正元五セル値を両端とする別presentationの六セルと厳密等式への戻り障害

## 0. canonical正本と形式検証

2026年11月6日 JST。Repository：itakura-hidetoshi/KuuOS。Canonical branch：main。

| 項目 | 確定結果 |
|---|---|
| 継承起点 | Qi v4.85、main 0665446b35222b971fd5694512ba9474f5bfb615 |
| 定理PR | [#3195](https://github.com/itakura-hidetoshi/KuuOS/pull/3195) — MERGED |
| exact-source HEAD | 195e6676b6491d4ec49bd90be4596848b9d85d0c |
| 定理squash SHA | 1d43f998db2bccf2d732e34abe36336c0084adfd |
| source/test-merge/squash Git tree | 8f13c7dda67423aa4005d69543b9cb959a7f84b0 — 完全一致 |
| exact-source CI | [#42188314382](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42188314382) — completed/SUCCESS |
| Strict Lean | **10,285 / 10,285 SUCCESS** |
| Governance | **30 / 30 jobs SUCCESS** |
| 新規14宣言の実公理監査 | **14/14、標準公理のみ**（無公理3件、残り11件は propext／Classical.choice／Quot.sound の範囲） |
| sorryAx・変更Lean warning/error | **なし、0/0** |
| 固定pin | Lean v4.30.0-rc2／mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6 |
| 公開・保護 | KuuOSFormal、root107維持。保護PR #1558 Draft／OPEN／未マージ |

[検証済みLean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77AdjoinedSixCellPresentationV4_86.lean) · [v4.85正式記録](Qi-v4_85-original-P77-GK5CG-selected-word-shape-obstruction.md) · [独立GK5CG元source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5CGP77FiveCellAssociatorCharge.lean)

## 1. 新presentationと真正の元GK5CG五セル値

Qi v4.84では真正元GK5CG保守的五セルの三辺経路L₃(i)・二辺経路L₂(i)を元Type値として構成した。Qi v4.85では任意の真正最終raw添字iについて、この二値が元の自由構成子語として**厳密不一致**であることをLean4形式証明した。

v4.86では、元の既存GK5CG型を書き換えず、明確に異なる自由高次文法 PentagonAdjoinedSixCell W long short : W → W → Type を新たに導入する。構成子は refl（新presentationの六セル単位）、symm（反転）、trans（縦合成）、pentagon（明示的に**追加**したlong→short六セル生成元）である。このpentagonは元のF55/P77/GK5CGから既存の証拠を回収して得たものではない。

旧側 W には、実際のpentagonFinalConservativeLoop f g h k iを渡す。すなわち、全ての比較対象は元sourceの正真正銘のNativeGK5CGConservativeFiveCellのType値であり、整数charge、商、数値観測、raw添字だけの代替モデルではない。

略記 pentagonAdjoinedSixCellAt は、選択した真正部分木A/B/C/D₄、元Familyと部分State、真正最終raw添字i、元の五セル値w/zを添字に持つ。新しい六セルTypeのみが拡張され、元五セル・四セル・証明履歴は保持される。

## 2. 実際の六セル値・反転・合成の構成

pentagonAdjoinedSixCell_generator は、新しい六セルTypeの構成子pentagonにより、実際の元五セル値L₃(i)からL₂(i)への証拠を構成する。

pentagonAdjoinedSixCell_inverse はその反転、pentagonAdjoinedSixCell_roundtrip は新presentation内の合成generator ⋅ inverseであり、元五セルL₃(i)の自己六セルとなる。roundtripが六セルのreflと厳密等しい、という主張ではない。

pentagonAdjoinedSixCell_exists は、真正五セルを両端に持つこの**明示的に拡張したTypeのNonempty**を証明する。旧五セル証明語の厳密等号 h : w=z が既にある場合、pentagonOldEquality_embedsInAdjoined で新presentationへ送ることも可能。ただしこれは元に存在する六セルを輸入したという意味ではなく、Eq証明から新presentationのrefl構成子を選ぶ写像である。

## 3. 中心定理：元の厳密五セル等号への解釈不可能性

PentagonAdjoinedSixCellEqualityInterpreter は、**新presentationの全ての六セルを旧側の五セル証明語の厳密等式へ戻す**という命題である：

\[
\forall w,z:W,\quad
\operatorname{AdjoinedSixCell}_i(w,z)\longrightarrow(w=z).
\]

pentagonAdjoinedSixCell_noEqualityInterpreter はこれの否定を全ての真正最終raw添字iに対して形式証明した。もし解釈写像があれば、新たなpentagon生成元を適用してL₃(i)=L₂(i)が得られる。しかしこれはQi v4.85のpentagonOriginalFiveCell_words_neと矛盾する。

\[
\boxed{
\operatorname{Nonempty}\bigl(\operatorname{AdjoinedSixCell}_i(L_3,L_2)\bigr)
\quad\land\quad
\neg\exists \text{ 全元・端点保存の旧厳密等号への解釈}
}
\]

この分離をpentagonAdjoinedSixCell_exists_but_noEqualityDescentが一つの型付き命題としてまとめる。一般版 PentagonAdjoinedSixCell.noEqualityInterpreter も、自由文法に任意の異なるlong/shortを接続する生成元を追加した場合の一般的な障害を証明した。

これは**旧五セル語の厳密等号への戻り**という特定の強い解釈に対するno-goであり、すべてのhigher categoryによる比較、商の下での同値、弱いdescent、別の六セル充填が不可能であるという主張ではない。元のsourceには新しい六セル生成元を無条件に加えない。

## 4. F112/GK5CG独立sourceと観測の区別

pentagonNewSixCell_withOriginalSourceNoGo は、(a)新しい六セルの存在、(b)元五セルの厳密Eqへの戻り障害、(c)独立F112/GK5CGで真正に成立する元F55/P77の上側四セルと下側四セルのcharge差+1、(d)元保守的GK5CG五セルがそれら**別の二四セル**を結べない、という結論を同時に保存する。

Qiの比較六セルは元五セルの二値を結び、独立F112の旧五セルno-goは元四セルの上側／下側の二値を結ぶ問題。比較対象の次元とsource/targetを同一視しない。

pentagonAdjoinedSixCell_observation_boundary ではv4.83の全forward/backward raw index・真正source witness pullbackについての観測同値を保存しつつ、新比較の存在と厳密Eqへの戻り障害が両立することを示した。

## 5. 実装・正本・検証

新規Leanモジュール1件（287行）、formal/KuuOSFormal.leanへの公開import1行のみ。既存Lean定理、独立F112/GK5CG定義、manifest、workflow、pin、runtime、root107は変更しない。

最初の定理PR source HEAD 195e6676b6491d4ec49bd90be4596848b9d85d0c で exact-source CI #42188314382 は**初回から完全成功**。全14件の #print axioms 実出力をMCPで確認し、標準公理依存のみ、sorryAxなし、変更Lean warning/error0/0。source/test-mergeのGit tree完全一致を確認した後、head SHAを指定してsquashマージ。マージ後のtreeも同一。

## 6. 次段階 Qi v4.87 候補

高次presentationにおける可換性を調べるには、構成した新しい六セル同士の証明語、合成・反転の整合性、および**その上位の比較**の型が必要。観測を忘れる写像や選択した弱い高次同値の条件を明示して、旧厳密Eqとは別のdescentの可否を形式化する。新六セル同士を無条件に等置したり、旧元sourceの六セルの存在を推論しない。

strict 空中心・独立Kuu＝presentation・元Type値・authority・source証拠・obstructionを区別し、append-only／tighten-only／same-rootで継承する。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
