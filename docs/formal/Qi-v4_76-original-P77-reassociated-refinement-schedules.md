# Qi v4.76 — 元P77の再括弧付け付き有限細分スケジュールと真正recut自然性

## 0. 検証済み正本

- 日付：2026年11月6日 JST。
- Repository：itakura-hidetoshi/KuuOS、canonical branch：main。
- 継承基点：Qi v4.75、830eb3570718658d2037629c9e549a9628bd7c90。
- 定理PR：[#3174](https://github.com/itakura-hidetoshi/KuuOS/pull/3174) — MERGED。
- exact-source検証HEAD：1ccf71f015d0a275b3156b02bda150a8ccc85bf9。
- 定理squash：1ceca044669e140d312d9bd654f6ea04e8f2b51a。
- source/test-merge/squash Git tree：78b57778212488e89564794df8219a96880a8cc7 — 完全一致。
- [exact-source CI #42154950425](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42154950425)：SUCCESS。
- Strict Lean：**10274 / 10274 SUCCESS**。
- Governance：**30 / 30 SUCCESS**。
- 新規46宣言の実公理出力：標準公理のみ、sorryAx 0。
- 変更Lean warning/error：0/0。
- Lean：v4.30.0-rc2、mathlib：5450b53e5ddc75d46418fabb605edbf36bd0beb6。
- 公開集約KuuOSFormal、root107。保護PR #1558 Draft／OPEN／未マージ。

[recut添字整合性のLean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77RecutIndexCoherenceV4_76.lean) · [スケジュール移送のLean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77ReassociatedRefinementSchedulesV4_76.lean) · [v4.75正式記録](Qi-v4_75-original-P77-finite-refinement-schedule-coherence.md)

## 1. 今回の問題

v4.75は、固定した有限Familyの内部で完了する実行順序を比較した。今回扱うのは、そのFamilyの括弧付け自体を変えたときの移送である。

選択済みの各局所RefinementPlanと因子の空間的な順序を保持し、任意の途中状態s、その状態からの実際のStep、任意有限のScheduleを別の括弧付けへ移す。元のraw四セルは括弧付けを保持しているため、添字の組を移すだけで五セル値を同一視することはできない。元CutRouteのraw比較と、実スケジュールが生成するraw比較を使って二経路を構成する。

## 2. 全original CutRouteのraw添字写像と正規化の整合性

最初のモジュールはFamilyとは独立に、元CutRouteの全構成子を扱う。refl、cut、assoc、symm、trans、左右文脈のそれぞれを、元raw添字Typeの同値I_rとして解釈する。

cutでは、元のchain append添字同値の逆を使う。assocはmathlibのprodAssoc、symmとtransは同値の逆と合成、左右文脈はprodCongrである。

元raw比較はv4.72以来、sourceの正規化、flattenの等式によるchain比較、targetの逆正規化を通る。その添字写像が直接のI_rと一致することを、次の構造証明で接続した。

1. 元chainの等式に沿った依存添字castについて、反射・合成・逆・consの計算則を証明する。
2. appendの左右の等式輸送との可換性を証明する。
3. 左chainの構造帰納法により、元ChainAppend_assocの等式castと実際のappend添字の結合則が可換であることを証明する。
4. 全CutRouteの構造帰納法で、直接recutしてから正規化した添字と、正規化して正確なflatten等式でcastした添字が一致することを証明する。

N_S、N_Tをsource／targetの正規化同値、e_rを元のflatten等式とすると、

$$
N_T(I_r(i))=\operatorname{cast}_{e_r}(N_S(i)).
$$

この結果から、**既存のraw比較そのもの**について、

$$
\boxed{
C(r)_{\mathrm{backward}}(i)=I_r(i),\qquad
C(r)_{\mathrm{forward}}(j)=I_r^{-1}(j)
}
$$

を全raw添字域で得る。これは純粋recutについての結果である。一般のRefinementPlanのforward／backward coverageを互いの逆とは仮定しない。

この証明ではraw添字Typeの一意性を仮定しない。元五セル値は、従来の正規化経由の値をそのまま保持する。五セル解釈を別のものへ置き換えたわけではない。

## 3. 有限Familyの全途中状態・Step・Scheduleの移送

ReassocRouteはrefl、assoc、unassoc、trans、left、rightを持つTypeである。assocとunassocは両方向の原始再括弧付けであり、有限合成と文脈により任意有限の両方向再括弧付け語を保持する。局所計画を分解・置換する構成子や、因子の順序を交換する構成子は導入していない。

reassocStateEquivは、各途中状態にあるBool／PUnitの組をprodAssocなどで移す。initialとterminalを保存することも証明した。

各状態sに対しreassocCutRouteを構成し、元CutRoute値を実際に保持する。reassocStepは、結合子の三つの因子位置をそれぞれ扱い、同じ局所計画の実行を対応する位置へ移す。左右の任意の深さと、有限個の再括弧付けの合成を含む。

reassocScheduleは各Stepを移して有限列を再構成する。実際の全中間状態と実行順序を保持する。有限列のappendとの整合性を証明し、元の完了列から移送先の完了列も構成した。空スケジュールも対象である。

## 4. 任意の部分スケジュールに対する全域自然性

FからGへの再括弧付け語をr、その状態同値をe、元の部分スケジュールをq:s→tとする。移送したスケジュールをq^r:e(s)→e(t)と書く。

各状態のraw添字同値をI_s、真正source証拠同値をW_sとし、F_qとB_qを元raw比較のforward／backward写像、P_qを元source証拠のPullbackと書く。

一Stepでの成分別計算を、Scheduleの構造帰納法で合成することにより、

$$
\boxed{
\begin{aligned}
I_s(F_q(i))&=F_{q^r}(I_t(i)),\\
I_t(B_q(j))&=B_{q^r}(I_s(j)),\\
W_s(P_q(w))&=P_{q^r}(W_t(w))
\end{aligned}
}
$$

を得る。

iは元の終了状態tの任意raw添字、jは元の開始状態sの任意raw添字、wは終了状態tの任意真正source証拠である。**完了スケジュールであるという仮定も、coverageの全射性も必要ない。** v4.75の一般部分列で使った「終端／始端の直接写像の像」に制限されない全域の自然性である。

新しいsource証拠復元の等式は、各因子の実計算と同値の逆法則から導く。source証拠のsubsingleton性を用いた置換はしていない。元の経路保存定理の利用は、既存の証明依存をそのまま継承する。

## 5. 真正raw五セルを持つrecut／scheduleの二経路

共通のsourceは元の状態sの木、共通のtargetは移送後の状態e(t)の木である。次の二つの元RefinementPlan値を構成した。

- scheduleThenRecut：元スケジュールqを実行し、その終了状態で元recut r_tを実行する。
- recutThenSchedule：元開始状態で元recut r_sを実行し、移送したスケジュールq^rを実行する。

第2節の正規化bridgeと第4節の自然性から、この二計画の全forward添字写像、全backward添字写像、実際のsource証拠Pullbackが一致することを証明した。

reassocRawSquareは、添字一致でraw四セル端点を合わせた二つの**元GK5CG Type値五セル**の組を返す。reassocRawLoopは一方の五セルの逆と他方の合成である。元のrecut五セルと各局所計画の五セルを実際に保持する。

異なる五セル履歴の等式、loop=refl、loopの非自明性、さらに高いセルの存在は主張しない。

## 6. 元経路・認証・因子別obstruction

各部分状態で、再括弧付け前後のcompatibilityと因子別obstructionが同値であることを証明した。二経路とも、元のQuiver.Pathとsource認証付きP77部分Homを保存する。

二経路の終端に実際の真正source証拠を与えれば、それぞれを既存の証拠付きSubdivisionRouteへ認証できる。認証後のraw比較は、**同じ側の選択済みraw比較**と等しい。二つの側を互いに等置する定理ではない。

さらに、各側の`RefinementPlanAllCompatible`に含まれる全中間階層・端点・固定文脈のcompatibilityと、**最終再括弧付け前の元スケジュール終了状態tの因子族**のcompatibilityを結ぶ。対応する否定は、同じ元因子族のobstructionと同値になる。任意の部分列についての結果であるため、このtを全Familyのterminalと読み替えない。

粗いsource証拠、recut、実行順序の存在だけから、欠けた終了因子証拠は生成されない。

## 7. 公開宣言と検証

新規Leanモジュール2件と、公開集約KuuOSFormalのimport2行を追加。既存証明本文・名前・仮定・結論・公開root・固定依存・CI workflowsは維持した。

### 7.1 recut添字整合性：14宣言

名前空間：`KUOS.Architecture.WuxingPentagonUnified`。

| 宣言 | 実公理出力 |
|---|---|
| `fivefoldP77RawPatchChainIndexCast` | `propext, Quot.sound` |
| `fivefoldP77RawPatchChainIndexCast_refl` | `propext, Quot.sound` |
| `fivefoldP77RawPatchChainIndexCast_trans` | `propext, Quot.sound` |
| `fivefoldP77RawPatchChainIndexCast_symm_apply` | `propext, Quot.sound` |
| `fivefoldP77RawPatchChainIndexCast_cons` | `propext, Quot.sound` |
| `fivefoldP77RawPatchChainAppendIndexEquiv_cast_left` | `propext, Quot.sound` |
| `fivefoldP77RawPatchChainAppendIndexEquiv_cast_right` | `propext, Quot.sound` |
| `fivefoldP77RawPatchChainAppendIndexEquiv_assoc` | `propext, Quot.sound` |
| `fivefoldP77RawPatchCutRouteIndexEquiv` | `propext, Quot.sound` |
| `fivefoldP77RawPatchCutRouteIndexEquiv_normalize` | `propext, Quot.sound` |
| `fivefoldP77RawPatchChainComparisonOfEq_forwardIndex` | `propext, Quot.sound` |
| `fivefoldP77RawPatchChainComparisonOfEq_backwardIndex` | `propext, Quot.sound` |
| `fivefoldP77RawPatchCutRouteRawComparison_backwardIndex` | `propext, Quot.sound` |
| `fivefoldP77RawPatchCutRouteRawComparison_forwardIndex` | `propext, Quot.sound` |

### 7.2 再括弧付け付きスケジュール：32宣言

名前空間：`KUOS.Architecture.WuxingPentagonUnified.FivefoldP77FiniteRefinement`。

| 宣言 | 実公理出力 |
|---|---|
| `ReassocRoute` | `propext, Quot.sound` |
| `reassocStateEquiv` | `propext, Quot.sound` |
| `reassocState_initial` | `propext, Quot.sound` |
| `reassocState_terminal` | `propext, Quot.sound` |
| `reassocCutRoute` | `propext, Quot.sound` |
| `reassocIndexEquiv` | `propext, Quot.sound` |
| `reassocWitnessEquiv` | `propext, Classical.choice, Quot.sound` |
| `reassocStep` | `propext, Quot.sound` |
| `reassocSchedule` | `propext, Quot.sound` |
| `reassocSchedule_append` | `propext, Quot.sound` |
| `reassocComplete` | `propext, Quot.sound` |
| `reassocStep_forward` | `propext, Quot.sound` |
| `reassocStep_backward` | `propext, Quot.sound` |
| `reassocStep_pullback` | `propext, Classical.choice, Quot.sound` |
| `reassocSchedule_forward` | `propext, Quot.sound` |
| `reassocSchedule_backward` | `propext, Quot.sound` |
| `reassocSchedule_pullback` | `propext, Classical.choice, Quot.sound` |
| `reassocState_path` | `propext, Classical.choice, Quot.sound` |
| `reassocState_compatible_iff` | `propext, Quot.sound` |
| `reassocState_obstructed_iff` | `propext, Classical.choice, Quot.sound` |
| `scheduleThenRecut` | `propext, Quot.sound` |
| `recutThenSchedule` | `propext, Quot.sound` |
| `reassocSquare_forward` | `propext, Quot.sound` |
| `reassocSquare_backward` | `propext, Quot.sound` |
| `reassocSquare_pullback` | `propext, Classical.choice, Quot.sound` |
| `reassocRawSquare` | `propext, Quot.sound` |
| `reassocRawLoop` | `propext, Quot.sound` |
| `reassocSquare_path` | `propext, Classical.choice, Quot.sound` |
| `reassocSquare_certified` | `propext, Classical.choice, Quot.sound` |
| `reassocSquare_certify_raw` | `propext, Classical.choice, Quot.sound` |
| `reassocSquare_allCompatible_iff` | `propext, Classical.choice, Quot.sound` |
| `reassocSquare_obstructed_iff` | `propext, Classical.choice, Quot.sound` |

### 7.3 実CIと修正履歴

初回bridge-only CI [#42153431611](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42153431611)では、ChainAppendIndexEquiv_assocのcons枝で、rewriteが等式証拠の未解決メタ変数を副goalとして残した。実際のcons.eは元chainの結合則そのものだった。

変更モジュール全文、v4.66の元append／assoc、v4.72の正規化・比較定義、実error blockを照合した。cast_consのrewriteにblockと実際のChainAppend_assoc証拠を明示し、未指定の証拠引数を埋めた。仮定・結論は変更していない。失敗時のsorryAxはLeanのエラー回復で生じた未完成証明の伝播であり、成功判定に用いていない。

続くfull-source CI [#42154164197](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42154164197)では、bridge14宣言の成功と標準公理のみを確認した。一方、依存型Stepだけを場合分けした箇所で、始点・終点の状態添字が固定されたまま残り、patternの型不一致とその後続のrhs caseエラーが生じた。

新規2モジュール全文、元Step／Scheduleの依存型定義、28件の実error blockを確認し、[Lean公式の依存パターンマッチ仕様](https://lean-lang.org/doc/reference/latest/Terms/Pattern-Matching/)と照合した。16箇所のmatchで始点状態・終点状態・Stepを明示的に同時判別する形へ修正した。三つの因子位置の操作、定理文、仮定は維持した。最終CIではこの修正を含む46宣言がすべて成功した。

一次資料：[Lean公式のrewrite仕様](https://lean-lang.org/doc/reference/latest/Tactic-Proofs/Tactic-Reference/)、[固定mathlibの積同値](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/Logic/Equiv/Prod.lean)。

最終exact-source CI #42154950425でworkflow・全job・Lean実行stepの終了、全10274ビルド、Governance30件、新規46宣言の実公理出力、変更Lean warning/error0/0、source/test-merge Git tree一致を確認した。検証済みHEADを指定してsquashマージした。

基点再確認時には別件のscheduled MGAP poller [#42141972905](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42141972905)にstate_store_missingを確認した。これは定理のLean／governance／push検証とは別の状態ストア問題であり、本定理でruntime状態やworkflow権限を変更していない。

## 8. 次の証明課題

Qi v4.77候補は、複数の再括弧付けと局所Stepが途中で交互に現れる有限履歴を構成し、今回の自然性四角形を逐次合成して、recutを前後へ集約することである。選択した各局所計画、実際の元Type値履歴、全raw添字、source証拠、因子別obstructionを保持する。異なる五セル履歴自体のhigher coherenceは別の課題である。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
