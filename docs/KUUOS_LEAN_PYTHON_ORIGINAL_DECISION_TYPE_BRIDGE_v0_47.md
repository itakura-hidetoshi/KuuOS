# KuuOS Lean→Python v0.47 — 原本DecisionOS Lean型の直接復元・双方向同値

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## 固定された正本と範囲

- Repo: itakura-hidetoshi/KuuOS
- Canonical: main
- Parent main HEAD: `410037a3bd8af5d78defb83e72b65f8b319caf3f` (v0.46統合)
- Lean: v4.30.0-rc2、mathlib: `5450b53e5ddc75d46418fabb605edbf36bd0beb6`
- 規律: append-only / tighten-only / overwrite-forbidden / same-root
- Lakeの**globsへの10件の列挙追加のみ**、新規Lean・監査・テスト・文書各1件、旧PlanOSの歴史的証明**1箇所**の修復、旧実数定義**6宣言（4ファイル）**への`noncomputable`追加、および歴史的Proof Root保全テストへの完全一致登録。
- 107既存公開roots、原本DecisionOS定理、旧OS Pythonカーネル、既存テスト、既存CI workflow、保護PR #1558は変更しない。
- **例外として原本のimport閉包で初めて露見した旧PlanOS証明1箇所のみを修正。** 定理文・仮定・他の証明は一切変更せず、既存`legacy/v5.291`の全97行と旧Git blobを保存し、原本からの正確な1差分を監査する。

## 元の障害と閉包の検証

v0.46で、原本
`KUOS.DecisionOS.BoundedPlanSynthesisRequestHandoffV0_8`
を直接importすると、その依存先の
`KUOS.DecisionOS.WorldConditionedDistributionHandoffIntakeValidationV0_5`
が `KuuOS.PlanOSV102` を要求し、従来のLake設定には
`KuuOS.*`名のモジュール登録がなく失敗した。

v0.47では原本のimportを弱めず、現行の同じ`[[lean_lib]]`
の **buildable module globs** に最小10個だけを登録する。
`roots`（公開ルート）は増やさず、`KuuOS.*`の全域ワイルドカードを
導入しない。

- `KuuOS.PlanOSV098` 〜 `KuuOS.PlanOSV102` の中継5本
- `PlanOSTemperatureTrajectoryStabilityCertificateKernelV01`
- `PlanOSQiConditionedInformationMetricCertificateKernelV01`
- `PlanOSWorldConditionedPathProjectionPullbackMetricKernelV01`
- `PlanOSWorldConditionedObjectiveDistributionUpdateKernelV01`
- `PlanOSWorldConditionedDistributionDecisionHandoffCertificateKernelV01`

上記は原本中継の現行importsから抽出された候補であり、
**この一覧の網羅性自体はまだ独立Leanで認証しなければならない**。
Lakeの追加行を除く元の全内容が親mainのGit blobと一致することを、
独立静的チェッカーで検査する。

## 再観測した固定Leanエラーの局所修復

最初のStrict Lean CI #44689581550では、
`formal/KuuOS/PlanOSTemperatureTrajectoryStabilityCertificateKernelV01.lean:26:23`
に`unsolved goals`が発生。

帰納法の`cons`場合：
`ih : 0 ≤ totalVariation steps`
から `0 ≤ |step| + totalVariation steps` を
`simp [totalVariation, abs_nonneg, ih]`だけでは解決できない。
このLean記法上の不成立は「定理が不成立」という意味ではない。

現役原本のこの部分だけを、
`simp only [totalVariation]` と
`exact add_nonneg (abs_nonneg step) ih` に修復した。

変更前の**完全な97行の歴史的Lean原本**は
`legacy/v5.291/formal/KuuOS/PlanOSTemperatureTrajectoryStabilityCertificateKernelV01.lean`
にGit blob `46d8a67594af17e6aa63f13600f90b9ab34c8ff8` として既存保存済み。
現役修復後blobは`a3d7e25d585da29e17eaef8f8c11d972948dbb40`。
両者を比較し、**同一の定理命題を持ち、ちょうど1箇所の証明だけが変化**したことを
v0.47静的監査・改変検出テストで検証する。
また、既存の`tests/test_public_root_restoration.py`が歴史的Leanソースの
未審査改変を正しく拒否したため、旧23件のPR #2339承認履歴や
`LINT_ONLY_SOURCE_EDITS`には混入せず、
`PR3608_REVIEWED_HISTORIC_PROOF_REPAIR`として独立登録した。
同テストでは旧blob・新blob・正確な一箇所差分・登録集合の一致を
全て確認し、他の歴史的原本への保護を弱めない。
上記の新しいproof root保全テスト自体も必ず再実行する。

これはすでに通過した原本型同値性の証明ではない。
修復後の全依存閉包を実Leanと公理監査で再認証する必要がある。

## 再観測したLean実数定義の計算可能性障害

続く独立CI [#44705107155](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44705107155)
では、既存のPlanOS実数定義が
`Real.instDivInvMonoid` という実行不能な実数除算を要求した。
Leanの診断は
`PlanOSQiConditionedInformationMetricCertificateKernelV01.lean:21:4`
`failed to compile definition, consider marking it as 'noncomputable'`。

元の依存モジュール全文と関連定義を検査し、
除算、実数指数、または先に定義した非計算的な関数への
明示的な依存がある**計6宣言**のみ、定義名の前へ
`noncomputable`を追加した。

- Qi条件付き情報計量：`diagonalQuadraticForm`
- WORLD投影・引き戻し計量：`planQuadraticForm`,
  `worldPullbackQuadraticForm`, `combinedTransitionAction`
- WORLD条件付き分布：`worldConditionedGibbsFactor`
- WORLD条件付きDecision handoff：`effectiveSupport`

これらの関数の数学的定義、引数、型、依存する定理文や証明は一切変更していない。
`noncomputable`は**Leanの実行用コード生成が不可能であることの明示**であって、
Pythonで数値計算できるという意味ではなく、空OSの行為権限を与えるものでもない。

`legacy/v5.291/formal/KuuOS`の各ファイルは変更しない。
元の全Git blob、修正後の全Git blobと各々の正確な
`def` → `noncomputable def` 差分は、
`scripts/check_kuuos_lean_python_original_decision_type_sources_v0_47.py`と
`tests/test_public_root_restoration.py`の
`PR3608_REVIEWED_REAL_NONCOMPUTABLE_DECLARATIONS`で独立監査する。
他の歴史的Proof Rootや旧PR #2339の例外群は変更しない。

今回の選別は構文・数学的依存に基づく事前候補であり、
全修正宣言・その依存閉包と新規v0.47の
`Equiv`・`Iff`が固定Leanで成功したという主張ではない。
独立CIを改めて取得する。

## 形式目標: 原本型への双方向接続

新規Lean:
`formal/KUOS/Architecture/LeanPythonOriginalDecisionTypeBridgeV0_47.lean`

直接import:
1. 原本 `KUOS.DecisionOS.BoundedPlanSynthesisRequestHandoffV0_8`
2. v0.46 `KUOS.Architecture.LeanPythonDecisionVerifyPlanNativeHandoffV0_46`

構成する宣言:

- `originalToMapped`: **原本実型**の35フィールドをv0.46のsource-mapped型へ写す。
- `mappedToOriginal`: 全35フィールドを元の型へ戻す。
- `originalReceiptEquiv`: これらが左右逆写像であることを示す **Lean Equiv**。
- `originalValid_iff_mappedValid`: 原本の`BoundedPlanSynthesisRequestHandoffValid`とv0.46のValidity35条件が**必要十分**であること。
- `originalDecisionBoundaries`: 原本v0.8の形式定理から非実行・非選択権限を取り出す。
- `originalDecisionSixRouteConditionalWitness`: 原本Validityを仮定し、上記同値性とv0.46の`WholeReceiptSeam`条件付きに、v0.45のVerifyOS→PlanOS六経路へ移す。
- `originalHandoffNeverLicensesHostExecution`: LocalSimulation成功を実行権限へ昇格しない。

この段階はsource-mapped型の似た名前を見て満足するのでなく、
**importされた本来のLean型と、その全Validityについて実際にEquivとIffの証明項を構成する**ことが研究対象である。

## Python接続と非認証事項

v0.46の読み取り専用監査器と、実DecisionOS v0.8・VerifyOS v0.4・PlanOS v1.03の
6経路試験は、元カーネルに変更を加えず再利用する。

これにより証明できるのは、原本Lean **型同士の構造的同値性** と
既存の条件付き形式定理だけであり、以下は未証明として保持する。

- 原本Leanの実型とCPython dictの一般的意味論的一致
- 3カーネルのPython実行意味論そのものの形式的証明
- 偽造困難性、外部発行者真正性、全局的因果時計
- 6ケースがひとつの原子的履歴であるという主張
- 全ストア・全OSの普遍的 refinementと大域降下
- DecisionOSの選択からPlan合成またはActOSホスト実行への権限移譲

Preference ⇏ Descent ⇏ Authority。

## 認証ゲート

この変更はLeanおよびLakeを含むので、docs-only経路は不可。
親main/既存Lean依存API/新Leanファイル全文を照合し、
固定mathlibで`-DwarningAsError=true` と `-DsorryAsError=true`を付与する。

元Pythonの累積回帰、既存公開Lean roots、workflow整合、
source/test-merge Git tree同一性、PR Governance、Exact-head terminalの
独立completed/SUCCESSが揃った場合に限りmainに統合する。
統合後は **実際のmain push HEAD** に対する独立CIを再観測する。

失敗する場合は新しいPRを増やさず、同じPRでエラーを全文・依存
signature・現行Lake登録・固定Mathlib APIから再分析する。
