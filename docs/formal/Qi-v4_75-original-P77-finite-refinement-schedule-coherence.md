# Qi v4.75 — 元P77の有限独立細分スケジュールと共通recut下の順序整合性

## 0. 検証済み正本

- 日付：2026年11月6日 JST。
- Repository：itakura-hidetoshi/KuuOS、canonical branch：main。
- 継承基点：Qi v4.74、bb81010c4323ec755897d73779c2af86090bcf1d。
- 定理PR：[#3172](https://github.com/itakura-hidetoshi/KuuOS/pull/3172) — MERGED。
- exact-source検証HEAD：1c8c50808048051694fbcd376dce126c8de3448b。
- 定理squash：1fae94a1e805678e330b83409e278b745b623140。
- source/test-merge/squash Git tree：4748b0082660221a67c36e48e72199af890945a2 — 完全一致。
- [exact-source CI #42127038266](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42127038266)：SUCCESS。
- Strict Lean：**10,272 / 10,272 SUCCESS**。
- Governance：**30 / 30 SUCCESS**。
- 新規61宣言の実公理出力：標準公理のみ、sorryAx 0。
- 変更Lean warning/error：0/0。
- Lean：v4.30.0-rc2、mathlib：5450b53e5ddc75d46418fabb605edbf36bd0beb6。
- 公開集約KuuOSFormal、root107。保護PR #1558 Draft／OPEN／未マージ。

[Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77FiniteRefinementScheduleCoherenceV4_75.lean) · [v4.74正式記録](Qi-v4_74-original-P77-terminal-certified-refinement-hierarchy.md)

## 1. 二因子から任意有限の実行順序へ

v4.74の左右二因子の比較を、任意有限個の独立した元RefinementPlanへ拡張する。各局所計画そのものは、元raw五セル比較、細分、recut、表示変更、有限合成、左右文脈を保持する既存のType値である。

新しいFamilyは、操作を行わないfixed木、選択済み計画を持つleaf、型付き端点で接続するnodeから構成される。元の因子の空間的な順序や頂点は入れ替えず、独立した操作を実行する時間的な順序を変える。

Familyの各leafにはBool値の状態を置く。falseは未実施、trueは実施済みである。fixedはPUnit、nodeは状態の積を持つ。任意状態sから、その時点の元cut tree B(s)を実際に構成する。B(0)は全因子が粗い状態、B(1)は全因子を指定どおり細分した状態である。

Stepは一つのleafをfalseからtrueへ進めるか、その操作を左右の任意の深さへ持ち上げる。ScheduleはStepの有限列であり、全中間状態とその実行順序をType値履歴として保持する。

## 2. 実行可能性を構成で保証する

complete(F,s)は、任意の有限Family Fと任意状態sから、全実施済み状態への実際の有限Scheduleを返す。

- fixedでは空スケジュールを構成する。
- leafが未実施なら、その元計画を一度実行する。
- leafが実施済みなら、空スケジュールとする。
- nodeでは、左の完了を右の現在状態で持ち上げ、続いて右の完了を左の完了状態で持ち上げる。

したがって、完了順序すべてについての後続定理は、比較対象の存在を別の仮定に任せない。操作数0のFamilyも含む。局所計画が同じ始終木を持つ場合も、その選択済み履歴は実行ステップとして保持される。

## 3. 順序によらない三つの直接構成

元raw添字TypeをI、真正source証拠TypeをWと書く。各途中状態sについて、実行順序を入力せず、因子ごとの再帰だけで三つの写像を定義する。

$$
\Phi_s:I(B(1))\to I(B(s)),\qquad
\Psi_s:I(B(0))\to I(B(s)),\qquad
\Omega_s:W(B(1))\to W(B(s)).
$$

未実施leafでの\(\Phi_s\)と\(\Omega_s\)には、その元計画のforwardIndexとPullbackを使う。実施済みleafでは恒等写像を使う。\(\Psi_s\)では、未実施leafは恒等、実施済みleafは元計画のbackwardIndexを使う。nodeでは両成分の写像を実行する。

forwardIndexとbackwardIndexが互いの逆であるという仮定は置かない。両者は既存の真正五セル比較に含まれる独立のcoverage写像である。

## 4. 一ステップの計算から任意有限列へ

一つのStep e:s→tについて、構造帰納法で次を証明する。

$$
C(e)_{\mathrm{forward}}\circ\Phi_t=\Phi_s,
$$

$$
C(e)_{\mathrm{backward}}\circ\Psi_s=\Psi_t,
$$

$$
\operatorname{Pullback}(e)\circ\Omega_t=\Omega_s.
$$

これをScheduleの有限列へ帰納すると、任意の完了スケジュールq:0→1について、

$$
\boxed{
\begin{aligned}
C(q)_{\mathrm{forward}}&=\Phi_0,\\
C(q)_{\mathrm{backward}}&=\Psi_1,\\
\operatorname{Pullback}(q)&=\Omega_0.
\end{aligned}
}
$$

が得られる。Leanでは全添字・全終端証拠に対する点ごとの等式として証明している。

この順序独立性はsource証拠のsubsingleton性で得たものではなく、各成分の実計算から導く。元のQuiver.Pathも、任意の途中状態で保存される。

一般の部分Schedule s→tの帰納式はforward側ではΦ_tの像、backward側ではΨ_sの像上で成立する。全射性は仮定しない。全完了ScheduleではΦ_1とΨ_0が恒等になるため、全添字域での等式を得る。

## 5. 隣接交換と真正raw五セル履歴

左右の任意深さで選んだ独立Stepから、二つの隣接二ステップ列を実構成する。左先行では中間状態が(左完了,右未完了)、右先行では(左未完了,右完了)となる。

両列の全forwardIndex、全backwardIndex、実source証拠Pullbackは定義的に一致する。appendと左右への持ち上げにより、これらの列を任意の有限前後履歴・外側文脈へ組み込める。任意の二つの完全な実行順序に対する第4節の定理は、こうして構成した順序変更にも適用される。

有限交換履歴を独立のType値とするExchangeTraceや、任意の二つの完了Scheduleが隣接交換列で結ばれるという連結性定理は未導入である。全完了順序の作用の一致は、交換列の存在を介さず、構造帰納の不変量から直接証明する。

planRawSquareは、実際に証明されたforwardIndexの一致を用いて端点を合わせ、元GK5CG Type値五セル二つの組を返す。orderRawSquareは任意の二つの完了順序、adjacentRawSquareは部分状態での隣接交換にこれを適用する。

planRawLoopとorderRawLoopは、一方の五セルの逆を他方と合成した真正五セルloopを返す。五セル履歴同士の等式、loopとreflの等式、loopの非自明性は主張しない。

## 6. 共通recut・表示変更との接続

同じ元source側presentation routeとtarget側presentation routeで、二つの完了順序を包む。

$$
S\xrightarrow{\alpha}B(0)
\xrightarrow{q}B(1)
\xrightarrow{\beta}T.
$$

mixedPlanはこの元RefinementPlanを実構成する。共通の前後raw index写像を合成することにより、二つの順序の全forwardIndex・全backwardIndexは依然一致する。source証拠も、同じpresentationの逆写像と\(\Omega_0\)を合成するため一致する。

このmixed履歴が生成するraw五セル値を実際に保持し、認証時の同一計画の比較保存、元source経路の保存、元の終端因子族のcompatibilityとobstructionを接続する。

既存CutRouteRawComparisonはsource/targetの正規化とflattenの一致を経由して比較を構成する。元CutRoute値はPlan内に保持されるが、一つのrecut構成子の内部語をraw五セル解釈で逐語的に再生することは主張しない。今回保持するのは、それぞれのPlanから実際に生成される五セル値である。

ここで形式化したrecutの範囲は、**共通の前後presentation/recut、および各leafの元計画内部のrecut**である。任意の途中recutを別の細分ステップの前後へ動かす一般法則や、異なる括弧付けのFamily間の全スケジュール移送は、別の証明課題である。

## 7. 認証と因子別obstruction

終端の真正因子別証拠wを与えると、任意のScheduleから既存SubdivisionRouteを構成する。認証は同じScheduleが持つraw比較を完全に保存する。

$$
\operatorname{RawComparison}(\operatorname{certify}(q,w))
=
\operatorname{RawComparison}(\operatorname{schedulePlan}(q)).
$$

任意の途中状態から終端へのScheduleについて、

$$
\operatorname{AllCompatible}(\operatorname{schedulePlan}(q))
\iff
\operatorname{Compatible}(B(1))
$$

およびその否定と終端obstructionの同値が成立する。粗いsource証拠や実行順序の存在から、欠けた終端因子証拠は生成されない。

## 8. 公開宣言と検証

新規Leanモジュール1件と、公開集約KuuOSFormalのimport1行を追加。既存証明本文・仮定・結論・公開root・固定依存・CI workflowsは維持する。

すべて `KUOS.Architecture.WuxingPentagonUnified.FivefoldP77FiniteRefinement` namespace内にある。

1. `Family`
2. `State`
3. `tree`
4. `initial`
5. `terminal`
6. `Step`
7. `stepPlan`
8. `Schedule`
9. `schedulePlan`
10. `append`
11. `left`
12. `right`
13. `complete`
14. `forward`
15. `backward`
16. `pullback`
17. `forward_terminal`
18. `backward_initial`
19. `pullback_terminal`
20. `step_forward`
21. `step_backward`
22. `step_pullback`
23. `chainRefl_forward`
24. `chainRefl_backward`
25. `recutRefl_forward`
26. `recutRefl_backward`
27. `schedule_forward`
28. `schedule_backward`
29. `schedule_pullback`
30. `complete_forward`
31. `complete_backward`
32. `complete_pullback`
33. `pullback_path`
34. `planRawSquare`
35. `planRawLoop`
36. `order_forward`
37. `order_backward`
38. `order_pullback`
39. `orderRawSquare`
40. `orderRawLoop`
41. `adjacentLeftFirst`
42. `adjacentRightFirst`
43. `adjacent_forward`
44. `adjacent_backward`
45. `adjacent_pullback`
46. `adjacentRawSquare`
47. `certify`
48. `certify_raw`
49. `allCompatible_iff`
50. `obstructed_iff`
51. `mixedPlan`
52. `mixed_forward`
53. `mixed_backward`
54. `mixed_pullback`
55. `mixedRawSquare`
56. `mixedRawLoop`
57. `mixed_path`
58. `mixed_certified`
59. `mixed_certify_raw`
60. `mixed_allCompatible_iff`
61. `mixed_obstructed_iff`

初回CI [#42125028682](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42125028682)では、section変数と依存帰納に関する三つの原因を特定した。

1. State・initial・terminalの自己再帰で、section変数f/g/h/kを通常の明示引数として渡した。Leanではsection変数は定義本体のelaboration後に引数として追加されるため、自己参照時の引数と一致しなかった。三定義にf/g/h/kの明示binderを置いた。
2. Scheduleのfamilyは全構成子で一様なため、autoPromoteIndicesによりparameterになる。nil帰納枝でfamilyとstateの二つを束縛していたが、枝に残るのはstateだけである。六箇所のnil枝と、左右持ち上げ内の外側family参照を修正した。
3. appendでは後続Scheduleが中間状態に依存するため、帰納仮定が後続Scheduleを受け取る関数になる。cons枝で帰納仮定に実際のsecondScheduleを渡した。

第二回CI [#42125858008](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42125858008)では、残る二つの原因を特定した。

1. 空Scheduleのraw比較も既存のCutRouteRawComparisonを通るため、正規化と逆正規化が入る。添字写像は定義的に恒等ではない。chainRefl_forward/backwardを鎖の構造帰納で証明し、recutRefl_forward/backwardを真正TreeIndexNormalizeEquivのsymm_apply_applyで証明した。これを空Scheduleの帰納枝に適用した。五セル値そのものをreflと同一視していない。
2. 隣接二ステップ列の末尾で、Stateの積型から元Familyを逆推論できなかった。nilの引数に実際のnode familyを明示した。

変更Lean全文、既存v4.68〜4.74の依存定義、帰納原理、固定Equiv/Prod API、全actual error blocksを照合した。修正で定理の仮定・結論は弱めていない。失敗時のsorryAxはLeanのエラー回復で生じた未完成定義の伝播であり、成功判定には使用していない。

一次資料：[Lean公式・Namespaces and Sections](https://lean-lang.org/doc/reference/latest/Namespaces-and-Sections/)、[Lean公式・Inductive Types](https://lean-lang.org/doc/reference/latest/The-Type-System/Inductive-Types/)、[Lean公式・Recursive Definitions](https://lean-lang.org/doc/reference/latest/Definitions/Recursive-Definitions/)、[固定mathlibのEquiv定義](https://github.com/leanprover-community/mathlib4/blob/5450b53e5ddc75d46418fabb605edbf36bd0beb6/Mathlib/Logic/Equiv/Defs.lean)。



最終exact-source CI #42127038266でworkflow・全job・Lean実行stepの終了、全10,272ビルド、Governance30件、新規61宣言の実公理出力、変更Lean warning/error 0/0、source/test-merge Git tree一致を再確認した。検証済みHEADを指定してsquashマージした。

## 9. 次の証明課題

Qi v4.76候補は、同じ独立因子族の異なる括弧付けに対して、全途中状態のrecutと各Stepの移送を構成すること。今回の有限スケジュールの直接添字写像・source証拠写像を再利用し、recutを途中段で動かした場合の実比較diagramとobstruction保存を扱う。raw五セル履歴自体を等置するhigher coherenceは、引き続き別の課題である。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.

