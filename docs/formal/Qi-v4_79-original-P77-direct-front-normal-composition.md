# Qi v4.79 — 元P77の直接正規形合成と全域観測整合性

## 0. 検証済み正本

2026年11月6日 JST。Repository `itakura-hidetoshi/KuuOS`、canonical branch `main`。

| 項目 | 検証結果 |
|---|---|
| 継承基点 | Qi v4.78、`c6a705a08c34991d23aceddb0ac1f3aa1f668f30` |
| 定理PR | [#3180](https://github.com/itakura-hidetoshi/KuuOS/pull/3180) MERGED |
| exact-source HEAD | `3ac60c90c57ed80f2c80d16a78004974121cd90c` |
| 定理squash | `dd413b98fe6dd4c65d420231998de9127adcd453` |
| test-merge | `f311844d52a2606d71d6fc6b265a57346c1b2fe4` |
| source/test-merge/squash共通Git tree | `deb3a3a2d6f7caf300139e278846fa4b9a1e3bbd` |
| exact-source CI | [#42164523390](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42164523390) completed / SUCCESS |
| Strict Lean | **10,278 / 10,278 SUCCESS** |
| Strict Lean job | `127717853242` completed / success、実Lean step14もcompleted / success |
| 今回選択されたGovernance workflow jobs | 4 / 4 completed / success |
| 新規宣言の実公理出力 | 20 / 20、標準公理のみ、sorryAxなし |
| コンパイラwarning / error | 0 / 0 |
| Lean / mathlib | v4.30.0-rc2 / `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 公開集約 / roots | KuuOSFormal / 107維持 |
| 保護PR #1558 | validation-only Draft / OPEN / 未マージ |

[Lean全文](../../formal/KUOS/Architecture/QiWuxingGK5CHP77DirectFrontNormalCompositionV4_79.lean) · [Qi v4.78記録](Qi-v4_78-original-P77-front-normal-append-coherence.md)

## 1. v4.78からの相違

v4.78の `composeFrontNormal` は、二つの正規形を真正交錯履歴へ埋め戻し、その実履歴を連結して `normalizeFront` を適用した。

v4.79では同じ共通Familyと部分Stateで合成可能な二つの正規形を対象に、累積routeと移送Scheduleを直接組み立てる。元の正規形・route語・Step・ScheduleはType値としてそのまま保持する。

```lean
def directComposeFrontNormal : FrontNormal f g h k source s target t where
  route := .trans N₁.route N₂.route
  schedule := append f g h k
    (reassocSchedule f g h k N₂.route N₁.schedule) N₂.schedule
```

すなわち、`N₁=(r₁,S₁)`、`N₂=(r₂,S₂)`について

$$
\boxed{N_1\diamond N_2=(r_1;r_2,\;r_{2*}S_1\mathbin{+\!\!+}S_2).}
$$

この定義は `normalizeFront` や履歴埋め戻しを呼ばない。第二routeによる第一Scheduleの移送後、終状態が第二Scheduleの始状態に一致する。合成routeの開始状態は既存の `reassocStateEquiv` のtrans計算規則で定義的に一致するため、逆route・追加の状態cast・新仮定は不要である。

`directComposeFrontNormal_route` と `directComposeFrontNormal_schedule` は、この選択されたroute・Scheduleの射影が上記の元構成子に厳密に等しいことを `rfl` で証明する。これはv4.78の異なるroute語との等式ではない。

## 2. 全域観測の証明構造

三観測は元の `PlanObservedEq` を使う。全target raw添字でforwardが一致し、全source raw添字でbackwardが一致し、全target真正source証拠に対してpullbackが一致する。

最初に `schedulePlan_append_observed` を第一Scheduleへの構造帰納法で証明した。空Scheduleは既存の正規化経由recut-reflを使い続け、その観測単位則を適用する。consでは元Stepの観測反射、後続列の帰納仮定、観測上の結合則を接続する。

次に `planObservedEq_reassocSchedule` がv4.76の三つの全域自然性定理を束ねる。

$$
S_1;r_2\sim_{\mathrm{obs}}r_2;r_{2*}S_1.
$$

`planObservedEq_whiskerSquare` は、この観測四角形に実際の前置・後置Planを付けても観測同値が保たれることを、結合則と合成合同性だけで証明する。

直接合成の主証明では、逐次Plan

$$
(r_1;S_1);(r_2;S_2)
$$

の中央で上記自然性四角形を適用し、二つのrecutを `ReassocRoute.trans` に集約し、二つのScheduleを元の `append` にまとめる。これにより

$$
\boxed{\operatorname{frontPlan}(N_1\diamond N_2)
\sim_{\mathrm{obs}}
\operatorname{frontPlan}(N_1);\operatorname{frontPlan}(N_2)}
$$

が成立する。一般細分coverageの可逆性や全射性、source証拠型のsubsingleton性を追加仮定していない。

## 3. 旧合成・元履歴連結との比較

`directComposeFrontNormal_historyObserved` は、上記主定理とv4.78の `composeFrontNormal_observed` を通じて、直接合成と履歴経由合成の観測一致を証明する。

対応するforward・backward・pullbackの三定理では、全域量化をそれぞれ明記した。

任意の実際に合成可能な交錯履歴 `H₁,H₂` について、`normalizeAppend_direct_observed` が

$$
\boxed{N(H_1\mathbin{+\!\!+}H_2)
\sim_{\mathrm{obs}}N(H_1)\diamond N(H_2)}
$$

を証明する。ここで正規形間の観測は、その `frontPlan` に対する `PlanObservedEq` を意味する。

`originalAppend_direct_observed` は、正規化していない元連結履歴の `historyPlan` も同じ直接合成Planと観測同値であることを示す。任意の部分状態における空履歴二本の回帰例もコンパイルした。一般の二状態間に履歴が必ず存在するとは主張しない。

## 4. 真正五セル・source・obstruction

直接合成と旧合成の五セルは別々の元GK5CG Type値として残す。`directComposeFrontNormal_rawSquare` は証明済みforward一致に沿って両側のraw四セル端点をそろえ、`directComposeFrontNormal_rawLoop` はその二辺から元の五セルloopを構成する。

両側のPlanは元Quiver.Pathとsource認証付きP77部分Homを保存する。真正の最終source証拠で各側を認証したraw比較は、認証前のその同じ側のraw比較と厳密に一致する。

両Planの `AllCompatible` とその否定は、それぞれ共通の最終因子木 `tree target t` のcompatibilityとobstructionに同値である。`t` は部分状態でもよい。細分途中の全状態間でobstructionが不変であるとは言わず、欠けたsource証拠を生成しない。

## 5. 新規20宣言と実公理依存

名前空間は `KUOS.Architecture.WuxingPentagonUnified.FivefoldP77FiniteRefinement`。

| 宣言 | 完了ログの実公理 |
|---|---|
| `schedulePlan_append_observed` | propext, Classical.choice, Quot.sound |
| `planObservedEq_reassocSchedule` | propext, Classical.choice, Quot.sound |
| `planObservedEq_whiskerSquare` | propext, Classical.choice, Quot.sound |
| `directComposeFrontNormal` | propext, Quot.sound |
| `directComposeFrontNormal_route` | propext, Quot.sound |
| `directComposeFrontNormal_schedule` | propext, Quot.sound |
| `directComposeFrontNormal_observed` | propext, Classical.choice, Quot.sound |
| `directComposeFrontNormal_historyObserved` | propext, Classical.choice, Quot.sound |
| `directComposeFrontNormal_forward` | propext, Classical.choice, Quot.sound |
| `directComposeFrontNormal_backward` | propext, Classical.choice, Quot.sound |
| `directComposeFrontNormal_pullback` | propext, Classical.choice, Quot.sound |
| `directComposeFrontNormal_rawSquare` | propext, Classical.choice, Quot.sound |
| `directComposeFrontNormal_rawLoop` | propext, Classical.choice, Quot.sound |
| `directComposeFrontNormal_path` | propext, Classical.choice, Quot.sound |
| `directComposeFrontNormal_certified` | propext, Classical.choice, Quot.sound |
| `directComposeFrontNormal_certify_raw` | propext, Classical.choice, Quot.sound |
| `directComposeFrontNormal_allCompatible_iff` | propext, Classical.choice, Quot.sound |
| `directComposeFrontNormal_obstructed_iff` | propext, Classical.choice, Quot.sound |
| `normalizeAppend_direct_observed` | propext, Classical.choice, Quot.sound |
| `originalAppend_direct_observed` | propext, Classical.choice, Quot.sound |

実成果物 `13477958990` のSHA-256をGitHubのdigestと比較し、`add227ff14332c2b7719449944cf0518b02ae47ebef63b7797a98946322eef6e` で一致した。収録 `lean-formal/receipt.json` はstatus passed、return_code 0、run_id 42164523390、run_attempt 1、git_shaは上記test-mergeである。実行時刻は2026-11-06 04:49:55–04:50:33 UTC。

収録 `lean-formal/check.log` 全文から、新規20件の公理出力がすべて存在し、標準公理だけであること、sorryAx不在、warning/error 0/0、Build completed successfully (10278 jobs)を確認した。先行依存の別定理まで一律に標準公理のみとは主張しない。

全10 PR-triggered workflowsは9 successと既存条件によるIndependent Kuu Foundationの1 skipで終了。Strict Leanとexact-head terminalのstatus receiptsもsuccessである。今回Governance workflowで選択された実jobは4件であり、以前の30件選択の数字を流用しない。

## 6. 構文修正と全文照合

初回CI #42163539368では、補題の引数名 `prefix` がLean構文予約語と衝突し、続く構文解析と補題参照が失敗した。また匿名 `example` の直前に `/-- ... -/` 文書コメントを置いたことで、名前付き宣言を期待する構文エラーが出た。

固定Lean v4.30.0-rc2の `src/Lean/Parser/Syntax.lean` を照合し、引数と参照を `prefixPlan` にalpha-renamingした。匿名検証例のコメントは `/- ... -/` の通常コメントに修正した。定理名・型・仮定・結論・空履歴の検証例は維持した。修正後の新規ファイル全文363行、imports、下位の依存型Schedule/FrontNormalと観測補題の引数・計算規則を照合し、最終ソースに対するCIで検証した。失敗runの公理出力を成功の証拠には使わない。

公開集約への追記時に発生した既存importの転記誤りも、PR作成前のGit差分照合で元表記へ復元した。最終差分は新規Leanファイル363行と集約import1行だけで、削除0行である。既存証明・pin・runtime・workflow・root定義は変更していない。

## 7. 次の課題と明確な境界

次の研究候補は、三つ以上の直接合成に対する観測上の結合則・単位則と、型付き有限列への拡張である。両括弧付けの累積route語と移送Scheduleは別の実値として保持し、必要な等式の層を明示する。

今回証明したのは三つの全域観測の一致であり、異なるFrontNormalの構成子的等式、元交錯位置の逆復元、正規化の単射性、五セル値の等式、loopの自明性、新しい高次セルの存在は主張しない。strict 空と独立Kuu/presentationの区別を保持する。

本記録は新規ファイルとして追加する。ルートREADME.mdとROADMAP.mdのQi v4.79追記は本記録の変更範囲に含めず、別の文書同期作業として残す。旧scheduled MGAP pollerのstate_store_missingは本定理とは別のruntime状態ストア問題であり、ここでは変更しない。

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
