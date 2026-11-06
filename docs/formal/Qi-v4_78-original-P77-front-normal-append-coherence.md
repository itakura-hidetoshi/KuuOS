# Qi v4.78 — 元P77交錯履歴の正規形合成・連結整合性

## 0. 唯一の正本とLean検証

- 日付：2026年11月6日 JST。
- Repository：itakura-hidetoshi/KuuOS。canonical：main。
- 継承基点：Qi v4.77、main \`8769f62cb68bc993cd69a53b56543c0554dc30be\`。
- 定理PR：[#3178](https://github.com/itakura-hidetoshi/KuuOS/pull/3178) — **MERGED**。
- exact-source検証済みHEAD：\`435fc53c17b3a9e61c0472aaaaae9a5b0329c82d\`。
- 定理squash／統合時main：\`d5dccb06438e61fac2934bdd1e208dfdd37173da\`。
- source/test-merge/squash Git tree：\`a217f73fd753e24318d983c40e99e05a6dfd97ca\` — **完全一致**。
- [exact-source CI #42160560777](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42160560777) — completed/**SUCCESS**。30/30 jobs completed/success。
- Strict Lean job \`127705069108\` — completed/success。実Lean step 14 — completed/success。
- **Strict Lean 10,277／10,277 SUCCESS**。変更Lean error／warning 0／0。
- 新規16宣言の実\`#print axioms\`出力は\`propext\`、\`Classical.choice\`、\`Quot.sound\`のみ。\`sorryAx\`はなし。
- Lean v4.30.0-rc2、mathlib \`5450b53e5ddc75d46418fabb605edbf36bd0beb6\`。公開集約KuuOSFormal、root107維持。
- 保護PR #1558 は validation-only Draft／OPEN／未マージ。

[新規Leanモジュール全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77FrontNormalAppendCoherenceV4_78.lean) · [継承v4.77正式記録](Qi-v4_77-original-P77-interleaved-recut-refinement-histories.md)

## 1. 実際の正規形を連結する

v4.77の \`InterleavedHistory\` は元のFamily・中間部分State・Step・ReassocRouteを実際のType値として保持する。\`normalizeFront\` はこれと**別値**である \`FrontNormal\` を、累積recutと最終Familyの移送Scheduleとして構成する。

v4.78では任意の合成可能な正規形 \`N₁ : FrontNormal F s M m\`、\`N₂ : FrontNormal M m T t\` を対象とする。共通のFamily／部分Stateは**型として一致**し、一般の2状態間の履歴存在を仮定しない。

- \`frontNormalHistory N\`：正規形を、**実recut**の直後に**実Schedule**を実行する元の \`InterleavedHistory\` に埋め戻す。元の五セル構成を持つ\`historyPlan\`を使う。
- \`frontNormalHistory_plan\`：この埋め戻しの元Plan値は \`frontPlan N\` に**厳密に等しい**。ここだけは同じPlan値の等式であり、異なる履歴の五セル等式ではない。
- \`composeFrontNormal N₁ N₂\`：二つの埋め戻した真正履歴を、実際の中間Family／Stateで\`historyAppend\`し、その連結履歴にv4.77の\`normalizeFront\`を適用する。末尾からの帰納により累積ReassocRouteの合成と各Stepの型付き移送を行う。選択された合成route語を別表現の語と**構成子的に等しい**とは主張しない。

これにより二つの実正規形から、最後の部分状態まで到達する別の実 \`FrontNormal\` を構成した。元の\`N₁\`、\`N₂\`、埋め戻し履歴、連結履歴、正規形はすべてType値として保持する。

## 2. 観測同値の合成則

元Plan\`P\`について三つの全域観測を次のように書く。

\`\`\`text
Obs(P) = ( forwardIndex(P), backwardIndex(P), Pullback(P) )
\`\`\`

\`PlanObservedEq\`は、同じsource／targetのPlanについて、全target raw添字、全source raw添字、全target source witnessでの点ごとの一致である。\`forward\`・\`pullback\`は反変に合成し、\`backward\`は逆の向きに合成する。元Planの構成子、五セル履歴、ループの等式はこの観測には含まれない。

まず\`composeFrontNormal_observed\`により

$$
\operatorname{Obs}(\operatorname{frontPlan}(N_1\star N_2))
=
\operatorname{Obs}(\operatorname{frontPlan}(N_1)\,;\,\operatorname{frontPlan}(N_2))
$$

を証明した。証明は次の既検証定理から得られる。

1. v4.77 \`normalizeFront_observed\`：任意の実交錯履歴とその正規形の全域観測一致。
2. v4.77 \`historyPlan_append\`：実履歴連結と元Planの逐次合成の全域観測一致。
3. \`frontNormalHistory_plan\`：埋め戻した正規形の元Plan値一致。
4. v4.77 \`planObservedEq_symm\`・\`planObservedEq_trans\`：観測関係の対称・推移。

一般のRefinementPlanのcoverageが全単射であるという仮定は追加しない。

## 3. 主定理：連結後正規化と個別正規化後合成

任意の元履歴

\`\`\`text
H₁ : InterleavedHistory F s M m
H₂ : InterleavedHistory M m T t
\`\`\`

について、v4.78の \`normalizeAppend_observed\` は次を証明する。

$$
\boxed{
\operatorname{Obs}\bigl(\operatorname{frontPlan}
    (N(H_1\mathbin{+\!\!+}H_2))\bigr)
=
\operatorname{Obs}\bigl(\operatorname{frontPlan}
    (N(H_1)\star N(H_2))\bigr).
}
$$

証明は\`normalizeFront_observed\`を全連結履歴・二つの部分履歴それぞれに適用し、\`historyPlan_append\`、\`planObservedEq_comp\`、\`composeFrontNormal_observed\`を対称性・推移律でつなぐ。定理の新たな前提はない。

さらに\`originalAppend_composite_observed\`は、**正規化していない**元の連結履歴のPlanと、個別正規化後の合成正規形のPlanの観測一致を証明する。

三つの定理\`normalizeAppend_forward\`、\`normalizeAppend_backward\`、\`normalizeAppend_pullback\`では、次をすべて全域で明記する。

$$
\forall i\in\operatorname{RawIndex}(T),\quad F_{\rm direct}(i)=F_{\rm separate}(i)
$$
$$
\forall j\in\operatorname{RawIndex}(F),\quad B_{\rm direct}(j)=B_{\rm separate}(j)
$$
$$
\forall w\in\operatorname{Witness}(T),\quad P_{\rm direct}(w)=P_{\rm separate}(w).
$$

ここで最後の等式は**真正source Type値証拠**の復元等式であり、証拠型がsubsingletonという仮定には依存しない。

## 4. 真正五セル・source認証・最終obstruction

- \`normalizeAppend_rawSquare\`：二つの元Planの**別々の真正GK5CG五セル値**を、証明済みforward一致に沿って同じraw四セル端点にそろえる。
- \`normalizeAppend_rawLoop\`：その二辺から元の五セルloop値を構成する。loopの自明性やさらに高次のセル存在を**主張しない**。
- \`normalizeAppend_path\`・\`normalizeAppend_certified\`：どちらの元Planのpullbackも元Quiver.Pathとsource認証付きP77部分Homを保存。
- \`normalizeAppend_certify_raw\`：最後の真正source証拠で**それぞれの側**を認証したraw比較は、認証前の**同じ側**の選択済みraw比較に厳密一致。
- \`normalizeAppend_allCompatible_iff\`・\`normalizeAppend_obstructed_iff\`：両方の元Planの全段compatibility／その否定が、**共通の最終因子木**\`tree T t\`のcompatibility／obstructionにそれぞれ同値である。

途中の任意細分Stepを挟んだ全状態間でobstructionが不変とは主張しない。未提供の因子証拠を生成しない。

## 5. 形式証明・実公理監査

ファイル：\`formal/KUOS/Architecture/QiWuxingGK5CHP77FrontNormalAppendCoherenceV4_78.lean\`。新規16宣言と対応する\`#print axioms\`を16行追加し、\`formal/KuuOSFormal.lean\`へimport1行だけを追加した。既存定理本文やpins、root定義、runtime、workflowsは変えていない。

名前空間：\`KUOS.Architecture.WuxingPentagonUnified.FivefoldP77FiniteRefinement\`。

| 宣言 | 実公理 |
|---|---|
| \`frontNormalHistory\`、\`frontNormalHistory_plan\`、\`composeFrontNormal\` | propext, Quot.sound |
| \`composeFrontNormal_observed\` | propext, Classical.choice, Quot.sound |
| \`normalizeAppend_observed\`、\`originalAppend_composite_observed\` | propext, Classical.choice, Quot.sound |
| \`normalizeAppend_forward\`、\`normalizeAppend_backward\`、\`normalizeAppend_pullback\` | propext, Classical.choice, Quot.sound |
| \`normalizeAppend_rawSquare\`、\`normalizeAppend_rawLoop\` | propext, Classical.choice, Quot.sound |
| \`normalizeAppend_path\`、\`normalizeAppend_certified\`、\`normalizeAppend_certify_raw\` | propext, Classical.choice, Quot.sound |
| \`normalizeAppend_allCompatible_iff\`、\`normalizeAppend_obstructed_iff\` | propext, Classical.choice, Quot.sound |

**16/16実公理出力**すべて標準公理のみ、\`sorryAx\`なし。実Leanビルド\`10277/10277\`成功、該当ファイルにwarning/errorなし。出力はjob \`127705069108\`の完了ログで独立確認した。

### 5.1 初回syntax failureと修正

初回ソース\`b75bce3864a3311d7923ed74ac6d653c83ec980e\`に対するCI [#42160118647](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42160118647)は、行161で\`unexpected token '/--'; expected ')', ',' or ':'\`として失敗した。\`originalAppend_composite_observed\`内の入れ子の\`planObservedEq_trans\`に右括弧が1つ不足したため、後続文書コメントまで式が閉じなかった。

修正は**右括弧1文字の追加のみ**。変更Leanファイル全331行、imports、v4.77の依存定理・必要引数、元Plan型、括弧対応を再確認し、定理名・文・仮定・結論、既存ファイル、CI設定を変更せず再実行した。修正HEAD \`435fc53c17b3a9e61c0472aaaaae9a5b0329c82d\`の [#42160560777](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42160560777) は30/30 jobs・実Lean step14含めて全成功。失敗runは成功runの代用にしない。

GitHub MCPでsource／test-merge \`0599e6b9c0bacd7e1188d65a4df3aa57cd1d3ae1\`／定理squashのGit treeが\`a217f73fd753e24318d983c40e99e05a6dfd97ca\`で一致することを確認し、exact HEADを指定してsquashマージした。

## 6. 数学的限界・次の問題

今回の主結果は\`PlanObservedEq\`という三つの観測の一致である。\`FrontNormal\`間の構成子的等式、元交錯位置の逆復元、正規化の単射性、五セル値そのものの等式、五セルloopの自明性、新しい六セル等のhigher coherenceを主張しない。

次の候補は、累積routeを**直接**\`ReassocRoute.trans\`で束ね、第一Scheduleを第二routeで\`reassocSchedule\`移送して\`append\`する、より明示的な正規形合成と今回の\`composeFrontNormal\`の観測一致である。元raw五セル・source履歴を保持し、strict 空と独立Kuu/presentationのauthorityを越えない。

旧MGAP scheduled pollerの\`state_store_missing\`は別のruntime状態ストア問題であり、本定理・CI検証やpinsには混在させない。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
