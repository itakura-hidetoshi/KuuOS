# Qi v4.77 — 元P77の交錯recut・細分履歴と先頭recut正規化

## 0. 検証済み正本

- 日付：2026年11月6日 JST。
- Repository：itakura-hidetoshi/KuuOS、canonical branch：main。
- 継承基点：Qi v4.76、2a936ec57a8cd8b2e81b845b6d33cada697781f7。
- 定理PR：[#3176](https://github.com/itakura-hidetoshi/KuuOS/pull/3176) — MERGED。
- exact-source HEAD：9e535d5946e39bbb4c8bde284b0d8b43b8982174。
- 定理squash：3851849eecf5bd18721e851a2697f8a21a2e0ac1。
- source/test-merge/squash Git tree：96d82eb5ef24f883e376d4b16e865b81012fd63f — 完全一致。
- [exact-source CI #42158145882](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42158145882)：SUCCESS。
- Strict Lean：**10276 / 10276 SUCCESS**。
- Governance：**30 / 30 SUCCESS**。
- 新規30宣言の実公理出力：標準公理のみ、sorryAx 0。
- 変更Lean warning/error：0/0。
- Lean：v4.30.0-rc2、mathlib：5450b53e5ddc75d46418fabb605edbf36bd0beb6。
- 公開集約KuuOSFormal、root107維持。保護PR #1558 Draft／OPEN／未マージ。

[Plan観測同値のLean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77RefinementPlanObservationV4_77.lean) · [交錯履歴のLean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77InterleavedRecutRefinementHistoriesV4_77.lean) · [v4.76正式記録](Qi-v4_76-original-P77-reassociated-refinement-schedules.md)

## 1. v4.76からの拡張と対象範囲

v4.76は、任意の部分Scheduleと再括弧付けrecutの二経路の自然性を証明した。今回、その四角形を任意有限回使えるように、recutと局所Stepが途中で交互に現れる元のType値履歴を構成した。

交錯するrecutは、v4.76のReassocRouteが各状態に誘導する元CutRouteである。同じ選択済み局所RefinementPlanと因子の空間的順序を保持し、両方向の結合子・有限合成・左右文脈を許す。局所計画の分割・置換や因子の順序交換を新たに導入するものではない。選択した葉のPlan自体には、既存の任意有限の細分・recut・presentation履歴が含まれ得る。

開始・終了状態を完成状態に限定せず、実際の履歴が結ぶ任意の部分状態を扱う。空履歴、連続Step、連続recutも含む。完成状態やcoverageの全射性は仮定しない。

## 2. 元Planの三つの全域観測

厳密に同じsource木A・target木Bを持つ元Plan p,qに対して、PlanObservedEq p qを次の三成分のPropとして定義した。

$$
\boxed{
\begin{aligned}
&\forall i:\operatorname{RawIndex}(B),&&F_p(i)=F_q(i),\\
&\forall j:\operatorname{RawIndex}(A),&&B_p(j)=B_q(j),\\
&\forall w:\operatorname{Witness}(B),&&P_p(w)=P_q(w).
\end{aligned}
}
$$

Fはforward添字写像、Bはbackward添字写像、Pは真正source証拠pullbackである。五セル値の等式やPlan構成子の等式を、この関係の成分には含めていない。商型も導入していない。

反射・対称・推移、Planの逐次合成との整合性、観測上の結合則、元の正規化経由recut reflの左右単位を証明した。一般の細分Planを逆向きにする操作は導入していない。

合成方向は、

$$
F_{p;q}=F_p\circ F_q,\qquad
B_{p;q}=B_q\circ B_p,\qquad
P_{p;q}=P_p\circ P_q
$$

である。観測の合成則は、この三方向に沿う点ごとの等式推移から導く。

二つの元recutの合成を一つのCutRoute.transへ集約する補題では、v4.76のraw添字bridgeを用いて、既存の正規化経由比較の写像を直接のCutRouteIndexEquivへ接続した。raw比較構造全体や五セル履歴の等式は使っていない。

一Stepとその終了状態でのrecutを交換する観測四角形は、v4.76のreassocStep_forward／backward／pullbackと、recut bridge・同値の逆法則から導いた。新しいsource復元の一致をsubsingleton性で置き換えていない。

## 3. 実際の交錯履歴とそのコンパイル

InterleavedHistory F s G tは、元のFamily Fの部分状態sから、Family Gの部分状態tへの実際の有限履歴である。

| 構成子 | 保持するもの |
|---|---|
| nil | 同じFamily・状態での空履歴 |
| step | 元のStep値と、その実行後の状態からの後続履歴 |
| recut | 元のReassocRoute値、そのrecutが起きる実際の状態、移送後の状態からの後続履歴 |

中間Family・状態は型の添字として保持され、各Step・recut語は構成子の実データとして残る。

historyPlanはこの元履歴を、既存のRefinementPlanへそのままコンパイルする。空履歴にも既存の正規化経由recut reflを使う。この五セル値を新しい反射五セルに置換していない。

historyAppendは厳密に同じFamily・部分状態で二つの履歴を連結する。連結履歴のPlanと、二つの元Planを逐次合成したPlanの三観測が一致することも証明した。

historyOfScheduleは旧Scheduleを交錯履歴へ埋め込み、そのコンパイル結果が旧schedulePlanと**実際のPlan値として等しい**ことを証明した。この限定された埋め込みの等式は、一般の正規化前後のPlanや五セル履歴を等置する主張ではない。

## 4. recutを先頭へ集約する構成

FrontNormal F s G tは、次の二つの実値を持つ。

- route：FからGへの累積ReassocRoute。
- schedule：最終Family G内で、routeにより移した開始状態からtまでのSchedule。

normalizeFrontは後続履歴から再帰する。

1. 空履歴はrefl routeと空Scheduleへ移す。
2. 先頭がStepなら、後続の正規形が持つ累積routeでそのStepを移送し、正規形のScheduleの先頭に付ける。
3. 先頭がrecutなら、そのrouteを後続の累積routeへ合成する。

ReassocRoute.transの状態同値は同値の合成として定義されているため、3番目では後続Scheduleをそのまま使える。逆routeや状態等式によるcastは不要である。

元InterleavedHistoryとhistoryPlanは明示的な実値として残し、FrontNormalとfrontPlanを別に構成する。正規形だけから元の交錯位置を復元できることや、正規化の単射性は主張しない。

## 5. 任意有限履歴の正規化正当性

元履歴Hと、その先頭recut正規形N(H)に対して、

$$
\boxed{
\begin{aligned}
F_{\operatorname{historyPlan}(H)}(i)
 &=F_{\operatorname{frontPlan}(N(H))}(i),\\
B_{\operatorname{historyPlan}(H)}(j)
 &=B_{\operatorname{frontPlan}(N(H))}(j),\\
P_{\operatorname{historyPlan}(H)}(w)
 &=P_{\operatorname{frontPlan}(N(H))}(w)
\end{aligned}
}
$$

を全域で証明した。iは最終raw添字の任意値、jは開始raw添字の任意値、wは最終因子族の任意真正source証拠である。

証明は元履歴の構造帰納法による。空履歴では元recutの観測単位則を使う。Step枝では後続の帰納仮定、観測合成、結合則、一Stepのrecut自然性を順に合成する。recut枝では後続の帰納仮定と、二つのrecutを集約する観測補題を使う。

一般の細分Planのforward／backwardが互いの逆であるとは仮定しない。同値の逆法則を使う対象は再括弧付けrecutである。

## 6. 真正五セル・source認証・obstruction

historyRawSquareは、元履歴の五セルと正規形の五セルを、証明済みforward添字一致に沿ってraw四セル端点を合わせて組にする。historyRawLoopは、一方の逆と他方を合成した元GK5CG五セル値である。

元履歴と正規形の五セル値は双方を保持する。五セル履歴の等式、loopの自明性／非自明性、さらに高いセルの存在は主張しない。

両Planのpullbackは元のQuiver.Pathとsource認証付きP77部分Homを保存する。実際の最終source証拠を与えて各側を認証したとき、認証後のraw比較は**その同じ側の選択済み比較**と等しい。

両側のRefinementPlanAllCompatibleは、それぞれのPlanに含まれる中間階層・端点・固定文脈のcompatibilityを表す。これが、共通の最終木tree G tの因子族のcompatibilityと同値であることを示した。各側の否定も、同じ最終因子族のobstructionと同値になる。

このtは任意の部分状態である。開始coarse状態と最終状態のobstruction同値や、細分Stepを含むすべての中間状態間でのobstruction不変性は主張しない。欠けた最終因子証拠を生成する操作は導入していない。

新しい正規化前後のsource復元等式は、v4.76の構造的自然性と観測合成から導いた。既存の経路・認証保存定理を使う部分は、それらの元の証明依存を継承する。

## 7. 公開宣言と実検証

新規Lean2モジュールと公開集約import2行を追加した。既存証明本文・名前・仮定・結論・固定依存・公開root・CI workflowsは維持した。

名前空間：`KUOS.Architecture.WuxingPentagonUnified.FivefoldP77FiniteRefinement`。

### 7.1 Plan観測同値：10宣言

| 宣言 | 実公理出力 |
|---|---|
| `PlanObservedEq` | `propext, Classical.choice, Quot.sound` |
| `planObservedEq_refl` | `propext, Classical.choice, Quot.sound` |
| `planObservedEq_symm` | `propext, Classical.choice, Quot.sound` |
| `planObservedEq_trans` | `propext, Classical.choice, Quot.sound` |
| `planObservedEq_comp` | `propext, Classical.choice, Quot.sound` |
| `planObservedEq_assoc` | `propext, Classical.choice, Quot.sound` |
| `planObservedEq_left_refl` | `propext, Classical.choice, Quot.sound` |
| `planObservedEq_right_refl` | `propext, Classical.choice, Quot.sound` |
| `planObservedEq_recut_trans` | `propext, Classical.choice, Quot.sound` |
| `planObservedEq_reassocStep` | `propext, Classical.choice, Quot.sound` |

### 7.2 交錯履歴と正規化：20宣言

| 宣言 | 実公理出力 |
|---|---|
| `InterleavedHistory` | `propext, Quot.sound` |
| `historyPlan` | `propext, Quot.sound` |
| `historyAppend` | `propext, Quot.sound` |
| `historyPlan_append` | `propext, Classical.choice, Quot.sound` |
| `historyOfSchedule` | `propext, Quot.sound` |
| `historyPlan_ofSchedule` | `propext, Quot.sound` |
| `FrontNormal` | `propext, Quot.sound` |
| `normalizeFront` | `propext, Quot.sound` |
| `frontPlan` | `propext, Quot.sound` |
| `normalizeFront_observed` | `propext, Classical.choice, Quot.sound` |
| `normalizeFront_forward` | `propext, Classical.choice, Quot.sound` |
| `normalizeFront_backward` | `propext, Classical.choice, Quot.sound` |
| `normalizeFront_pullback` | `propext, Classical.choice, Quot.sound` |
| `historyRawSquare` | `propext, Classical.choice, Quot.sound` |
| `historyRawLoop` | `propext, Classical.choice, Quot.sound` |
| `history_path` | `propext, Classical.choice, Quot.sound` |
| `history_certified` | `propext, Classical.choice, Quot.sound` |
| `history_certify_raw` | `propext, Classical.choice, Quot.sound` |
| `history_allCompatible_iff` | `propext, Classical.choice, Quot.sound` |
| `history_obstructed_iff` | `propext, Classical.choice, Quot.sound` |

### 7.3 検証過程

初回exact-source CIで全30宣言が成功した。既存の依存型recursorと再括弧付け同値の計算則を利用し、定理文・仮定を変更する修正は行っていない。実行step14は2026-11-06 03:44:48–03:45:50 UTCにcompleted/success、Strict Lean job127697231330と全32 jobsもcompleted/successである。全41 source check-runsは40successと既存条件による1skipで終了し、Strict Leanとexact-head terminalのstatus receiptはいずれもsuccessだった。

独立レビューは、新規2ファイル全文、v4.74の元Plan、v4.75のSchedule・recut単位・raw pair、v4.76両モジュール、下位recut／presentation同値・raw合成を照合した。数学的なblockerはなく、全域量化・空履歴・連続recut・appendの括弧方向・同じ最終因子族のobstruction範囲を確認した。静的レビューとは別に、最終exact-source CIでkernel検証を行った。

CI #42158145882についてworkflow・全job・Lean実行stepの終了、10276ビルド、Governance30件、新規30宣言の実公理出力、変更Lean warning/error0/0、source/test-merge tree一致を確認し、検証済みHEADを指定してsquashマージした。

旧基点830eb357…のscheduled MGAP poller [#42141972905](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42141972905)に確認済みのstate_store_missingは、今回の定理検証とは別のruntime状態ストア事象である。本変更ではruntime状態・workflow権限を変更していない。

## 8. 次の証明課題

Qi v4.78候補は、二つのFrontNormalから連結履歴の正規形を直接構成し、historyAppend後にnormalizeFrontする経路と、個別にnormalizeFrontしてから正規形を合成する経路の整合性を証明することである。累積recut・移送Schedule・元Type値履歴・全raw添字・実source復元・最終因子別obstructionを保持する。五セル履歴自体のhigher coherenceは別の課題として扱う。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
