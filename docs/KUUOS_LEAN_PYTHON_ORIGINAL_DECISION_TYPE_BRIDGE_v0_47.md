# KuuOS Lean→Python v0.47 — 原本DecisionOS Lean型の直接復元・双方向同値

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## 固定された正本と範囲

- Repo: itakura-hidetoshi/KuuOS
- Canonical: main
- Parent main HEAD: `410037a3bd8af5d78defb83e72b65f8b319caf3f` (v0.46統合)
- Lean: v4.30.0-rc2、mathlib: `5450b53e5ddc75d46418fabb605edbf36bd0beb6`
- 規律: append-only / tighten-only / overwrite-forbidden / same-root
- 変更はlakefile.tomlの **globsへの10個の列挙追加のみ**、新規Lean形式ファイル1件、静的検査1件、テスト1件、文書1件。
- 107既存公開roots、全旧Lean定理、旧OS Pythonカーネル、既存テスト、既存CI workflow、保護PR #1558は変更しない。

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
