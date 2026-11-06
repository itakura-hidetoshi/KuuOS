# Qi v4.82 — 元P77真正型付き有限二分括弧付け木・全域観測整合性

## 0. 正本・形式検証の確定記録

2026年11月6日 JST。Repository: `itakura-hidetoshi/KuuOS`、canonical branch `main`。

| 項目 | 確定結果 |
|---|---|
| 継承基点 | Qi v4.81、main `9937c7202929e339f49da9da3888b7566039fee2` |
| 定理PR | [#3187](https://github.com/itakura-hidetoshi/KuuOS/pull/3187) — MERGED |
| 最終exact-source HEAD | `e1d6325cbd0194df6596499c60fdc6031561913c` |
| 定理squash SHA | `62e950fc6e105c069ccd84332f729ca31d96c4bb` |
| source/test-merge/squash Git tree | `3eb18af42dda7ec5805b6331af93fc2661bf59c3` 完全一致 |
| 最終exact-source CI | [#42171411518](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42171411518) — completed/SUCCESS |
| Strict Lean | **10,281 / 10,281 SUCCESS** |
| Strict Lean job | `127739935972` completed/success、実Lean step 14 completed/success |
| Governance | **30 / 30 jobs completed/success** |
| 新規22宣言の実公理出力 | 22/22、標準公理のみ：`propext`・`Classical.choice`・`Quot.sound` |
| `sorryAx`／変更Lean warning・error | **0／0・0** |
| Pin | Lean `v4.30.0-rc2`／mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開・保護 | `KuuOSFormal`、public root107維持、PR #1558 Draft/OPEN/未マージ |

[検証済みLeanソース全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77TypedBinaryNormalBracketTreesV4_82.lean) · [Qi v4.81正式記録](Qi-v4_81-original-P77-finite-direct-normal-chains.md)

## 1. 問題と型付き木の真正構成

Qi v4.80で直接正規形三重合成の観測的結合則・左右単位則、Qi v4.81で任意有限長の型付き正規形鎖と連結・右foldの観測整合性が証明済みである。

Qi v4.82は次を主張する。

> 同じ**元の順序付き有限鎖**へflattenできる任意二つの**真正型付き二分木**の直接合成評価は、全forward／backward raw indexと真正source Type値witness pullbackで観測同値。

`DirectNormalBracketTree f g h k F s G t` は真正の依存型帰納的構成であり、次の三構成子を持つ。

- `nil F s`：完成を仮定しない任意の部分Family・State上の空木。
- `atom N`：元`FrontNormal F s G t`を**元Type値のまま**葉に保持。
- `node L R`：両側の共通中間Familyと部分Stateが**型レベルで一致**する場合のみ接続。

`bracketFlatten`はnil→元空鎖、atom→真正singleton、node→v4.81の`directChainAppend`とし、二分括弧を忘れても**実際の葉とその順序・元sourceデータ**を失わない。

一方、`bracketEval`はnil→真正`directNormalUnit`、atom→元normalそのもの、node→`directComposeFrontNormal`とする。元route語の`ReassocRoute.trans`とScheduleは選んだ二分木に依存する**別々のType値**として残る。`bracketEval_node_route`はその実構成子を明示する。

## 2. 全域観測整合性の主帰納

元`frontPlan`に対する三成分の`PlanObservedEq`を`Obs`と書く。主定理`bracketEval_fold_observed`は任意の真正型付き木Tに対し、

```text
Obs (frontPlan (bracketEval T))
    (frontPlan (directChainFold (bracketFlatten T)))
```

を証明した。

証明は`DirectNormalBracketTree`の真正構造帰納法である。

- nilでは双方が元`directNormalUnit`の同じ観測となる。
- atomではv4.81の`directChainSingleton_observed`を対称に適用する。
- nodeでは、左右部分木への帰納仮定をv4.80の`directCompose_observed_congr`で**実際の直接合成正規形へ**持ち上げ、さらにv4.81の`directChainFold_append_observed`を対称に適用する。

重要なのはPlanの`trans`値と`frontPlan (directComposeFrontNormal ...)`を無条件に同一視しない点である。上記合同性定理が、必要な観測関係を証明付きで媒介する。

## 3. 任意有限鎖・任意二分括弧付けの一致

任意の元`DirectNormalChain C`から`bracketRight C`を真正帰納的に構成し、`bracketRight_flatten`により、

```text
bracketFlatten (bracketRight C) = C
```

が**元鎖の構成子値について厳密に成立**する。これは全長・中間状態を保持した存在構成であり、正規形評価の構成子等式ではない。

`bracketSameChain_observed`は任意の木L,Rに対し、

```text
hFlat : bracketFlatten L = bracketFlatten R
------------------------------------------------
PlanObservedEq (frontPlan (bracketEval L))
               (frontPlan (bracketEval R))
```

を証明する。両側をv4.81の**同じ実鎖の右fold**へ比較し、元`PlanObservedEq`の推移性・対称性で接続する。`bracketOverChain_observed`は共通の指定元鎖Cへそれぞれflattenする場合を定式化する。

また`bracketNode_assoc_flatten`は三つの任意有限**部分木**A,B,Cの`((A B) C)`と`(A (B C))`のflattenが元鎖として厳密一致することを証明し、`bracketNode_assoc_observed`がその全域観測同値を与える。これは三つの原子正規形だけの定理でなく、任意長の部分木に適用できる。

## 4. source・元五セル・obstruction境界

- `bracketSameChain_forward`、`bracketSameChain_backward`、`bracketSameChain_pullback`：全域観測の各成分を公開。
- `bracketSameChain_rawSquare`、`bracketSameChain_rawLoop`：別々の元GK5CG五セル値の端点を、証明済みforward一致で揃えて**保持**。loopの自明性、五セルの等式、高次充填は主張しない。
- `bracketSameChain_path`、`bracketSameChain_certified`：両側それぞれについて、元Quiver.Pathと元source-certified P77 partial Homを保持。
- `bracketSameChain_certify_raw`：各側が**自身の**選択済み元raw比較へ戻ることを確認。異なる五セル履歴を同一視しない。
- `bracketSameChain_allCompatible_iff`、`bracketSameChain_obstructed_iff`：両側Planの全段compatibility／その否定が、**共通最終因子木**のcompatibility／obstructionと同値。

これらは元F55／P77 source権威を変更せず、既存の欠損証拠を作り出さない。途中の任意refinement間のobstruction不変、正常形の構成子的結合律、選択五セル値の等式やpentagonator/higher coherenceは別の研究課題として留保する。

## 5. Lean4初回失敗と正確な修正

新規Leanファイル1件と公開集約へのimport1行だけを追加。変更された既存Lean定理ファイル、toolchain pin、mathlib manifest、workflow、公開rootsはない。

初回HEAD `ace16162c4e4f5bae8e79c6f09a56398e2eea290` の[CI #42170852121](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42170852121)は実Leanで失敗した。ログ全文と新規Lean全文、v4.80/v4.81依存、型付き添字、固定pinを照合し二原因を確定した。

1. `bracketEval_fold_observed`のnode帰納で、`PlanObservedEq`の右端`frontPlan (directComposeFrontNormal ...)`と、単なる`(.trans (frontPlan ...) (frontPlan ...))`を直接接続しようとした型不一致。既証明の`directCompose_observed_congr`を介して二実合成結果を比較し、`directChainFold_append_observed`へ接続した。
2. `bracketSameChain_forward/backward/pullback`の証明で、statementに現れないsection変数`hFlat`をproofから参照したため`Unknown identifier`。Lean4のsection変数は定理本文に言及されないと暗黙の引数にならない。これら三定理とrawSquare/Loopの定義に、共通のflatten等式証拠を**明示的引数**として追加した。

仮定や結論を弱めず、proof placeholder、新規公理、warning隠蔽、透過性・recursion limit変更を導入していない。修正HEAD `e1d6325cbd0194df6596499c60fdc6031561913c`で全10,281 Lean jobsとGovernance30 jobsがSUCCESS。22宣言の実公理出力は上記標準三公理のみ、`sorryAx`なし、変更Lean warning/error0/0。source/test-merge/squashのGit tree一致をGitHub MCPで再確認しsquash統合した。

## 6. 次段階の正確な境界

Qi v4.83候補は、五角形の異なる二分木に沿う**観測的**な五角可換性を明示し、元GK5CG五セルloopが保持するhigher coherenceの障害を別に定式化する。v4.82から五セルの充填存在や自明性が自動で従うとはしない。

strict 空中心、独立Kuu＝presentation、元Type値・source証拠・authority・obstruction、same-root、append-only、tighten-onlyを継続。検証用PR #1558はDraft／OPEN／未マージで保持する。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
