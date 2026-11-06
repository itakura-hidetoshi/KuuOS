# Qi v4.85 — 真正GK5CG五セル選択証明語の構成子形状による厳密不一致

## 0. 唯一の正本とexact-source検証

2026年11月6日 JST。Repository: itakura-hidetoshi/KuuOS、canonical branch: main。

| 項目 | 検証済み最終状態 |
|---|---|
| 継承元 | Qi v4.84、main 0777f631245280acc5070c0bf124d916fd9010d0 |
| 定理PR | [#3193](https://github.com/itakura-hidetoshi/KuuOS/pull/3193) — MERGED |
| 最終source HEAD | 7c28f357d6f68706a6b9b2abcd3236bb668d812e |
| 定理squash SHA | 4c73d75392c3107b55b2cd1b90ea57ce0fe29f26 |
| source/test-merge/squash Git tree | 4fbb7748d5fc1feb1f09417add36cd57c2f0314f — 完全一致 |
| 最終exact-source CI | [#42178582859](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42178582859) — completed/SUCCESS |
| Strict Lean | **10,284 / 10,284 SUCCESS** |
| Governance | **30 / 30 jobs completed/success** |
| 新規宣言の実公理監査 | **13 / 13**、標準公理 propext・Classical.choice・Quot.sound のみ |
| sorryAx／変更Lean warning・error | **なし／0・0** |
| 固定Lean／mathlib | v4.30.0-rc2／5450b53e5ddc75d46418fabb605edbf36bd0beb6 |
| 公開と保護 | KuuOSFormal、公開root107維持、保護PR #1558 Draft/OPEN/未マージ |

[Leanソース全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77StrictPentagonWordShapeObstructionV4_85.lean) · [Qi v4.84正式記録](Qi-v4_84-original-P77-conservative-five-cell-loop-composition-obstruction.md) · [元GK5CG独立source](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5CGP77FiveCellAssociatorCharge.lean)

## 1. 正確な数学的問い

v4.83では、元Type値を保持した五角5辺について観測整合性を得た。v4.84では、同一の真正最終raw P77四セル上にあるGK5CG五セル自己loopを、長い三辺経路L₃(i)と短い二辺経路L₂(i)に沿って実際に合成した。しかし、L₃(i)=L₂(i)という選択済み五セル**構成子語の厳密等式**が成立するかは条件として残されていた。

元NativeGK5CGConservativeFiveCellは商や同値類でなく、別々のrefl/symm/trans等の構成子を持つ帰納的な**自由Type**である。v4.85は実際に選択した二経路の構成子語を、任意の真正最終raw添字に対して直接比較する。旧sourceや五セル生成元は書き換えない。

## 2. 構成子形状のBoolean証明書

新規originalConservativeFiveCell_rootTransは、元GK5CG五セル語の根がtrans構成子かどうかだけをBoolで読む。

originalConservativeFiveCell_rightLeftTransは、根の右子がtransである場合に、その右子の**左部分語の根**がtransかどうかを読む。元四セルの型添字・source/target・元五セル値は保持し、商やextensional equalityを一切使わない。

真正選択合成語の形状は次の通り。

~~~text
L₃(i) = trans loop01 (trans loop12 loop23)
          └─ right = trans (loop12) (loop23)
                           └─ loop12 = trans (symm u12) v12

L₂(i) = trans loop04 loop43
          └─ right = loop43 = trans (symm u43) v43
                                      └─ symm が左部分語
~~~

したがって、上記probeはL₃(i)でtrue、L₂(i)でfalseとなる。この二つの定理pentagonLongFiveCell_wordShape_trueとpentagonShortFiveCell_wordShape_falseはLean4のdefinitional reductionでrflとして検証された。

## 3. 主定理：全元raw添字での厳密語不一致

pentagonOriginalFiveCell_words_neは、任意の真正部分木A,B,C,Dと任意の最終raw添字iに対して

\[
\boxed{L_3(i)\ne L_2(i)}
\]

を証明する。仮に二つの元五セルType値が厳密に等しいなら、constructor-shape probeの関数合同性によりtrue=falseとなるため矛盾する。これは元の**選択された証明語同士の厳密な不一致**である。

既存fivefoldP77RawPatchTreeIndex_nonemptyを実際の最終因子木へ適用すると、任意の部分Stateでも真正raw添字iが存在する。したがってpentagonStrictFiveCellObstruction_existsがv4.84の障害命題の実在する証拠を与え、pentagonStrictFiveCellCoherence_falseが厳密一致命題の否定を得る。存在する添字は元sourceとして真正であり、人工的なダミー値ではない。

さらに差分五セルloop Δ(i)=L₃(i)・symm(L₂(i))は根がtransであり、既存の真正refl五セルとは構成子が異なる。pentagonDifferenceFiveCell_not_reflはその**自由語としての不一致**を証明した。

## 4. 元source no-goと高次充填の境界

pentagonSyntaxObstruction_and_originalSourceNoGoは、(a)今回の五セル語の厳密不一致、(b)独立F112/GK5CGの元F55/P77**四セル証明書**上側と下側の電荷差+1、(c)その別の二つの元四セルを結ぶ保守的五セルの不存在、を同時に保持する。

pentagonObservationsAgree_butFiveCellWordsDifferは、v4.83で証明済みの全forward/backward raw indexおよび真正source witness pullbackによる観測同値と、v4.85で証明した**選択済み元五セル自由語の厳密不一致**が両立することを示す。

**最大の数学的注意点：** 五セル自由語が厳密に等しくないことと、それらを結ぶ別の高次**六セル**が存在しないことは論理的に異なる。今回の不一致は群oid同値で割った後の非同値性や、任意のhigher presentationにおけるpentagonator不存在、nullhomotopy不存在を証明しない。元四セル電荷+1のno-goは別の厳密なsource/target問題であり、Qi五セル自己loopとの同一視はしない。

## 5. CI失敗と正確なLean4修正

初回HEAD 8132f952182c42cfdd2c03047bd89a984ba33f5bの[#42177787672](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42177787672)では、1回目のStrict LeanジョブがLakeキャッシュ復元中に失敗し実Lean工程に未到達。失敗ジョブのみの再実行をGitHub MCPで行い、同一sourceのattempt 2で実Leanコンパイルまで進んだ。

その実ログでは、pentagonOriginalFiveCell_words_neとpentagonDifferenceFiveCell_not_reflの2箇所でrewrite failedが出た。congrArgの結果が「(fun cell => probe cell) selectedWord」のラムダ適用を残していたため、書き換え補題の「probe selectedWord」と文面上一致していなかった。

元の定理文・仮定・GK5CG型・五角loop構成・他の証明を変更せず、各該当箇所にchangeでラムダ適用のβ簡約後の型を明示し、その後で既存probe等式をrwで適用するのみとした。

修正HEAD 7c28f357d6f68706a6b9b2abcd3236bb668d812eの[#42178582859](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42178582859)はStrict Lean全10,284 jobs SUCCESS、Governance全30 jobs SUCCESS。新規13宣言の公理出力は標準公理のみ、sorryAx・変更Lean warning/errorなし。source/test-merge/squash treeを全て再検証した上で、検証済みHEADを指定してPR #3193をsquashマージした。

## 6. 次段階 — Qi v4.86候補

構成子語の不一致が確定したので、次は**適切な高次比較のTypeの仕様**を作る。元GK5CG五セルの平行な二値をsource/targetに持つ新たな高次比較は、明示的に異なるpresentationの元としてのみ扱い、(1)比較証明書の正確なsource/target、(2)構造保存条件、(3)元sourceへのretraction/descentの障害を分ける。現存の六セルや元GK5CGに無条件な高次pentagonatorを後付けしない。

strict 空中心、独立Kuu＝presentation、元Type値・source証拠・authority・obstruction、append-only／tighten-only／same-rootを継続する。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
