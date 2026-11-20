# KuuOS Lean→Python v0.46 — DecisionOS原本からVerifyOS／PlanOSの6経路へ

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## 正本・固定境界

Canonical repository: itakura-hidetoshi/KuuOS
Canonical branch: main
Parent HEAD: `959fad7db61f1f5a9f4a2ba219b04714e67c93f9` (v0.45 merged).
Lean `v4.30.0-rc2`; mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`.
append-only / tighten-only / overwrite-forbidden / same-root.

既存のLean・Pythonソースを変更せず、新規6ファイルのみを追加する。

## v0.45からの実質的変更

v0.45でVerifyOS→PlanOSの元Pythonカーネル6経路と全証明書の接続を検証した。
ただし、v0.45のテスト入口に使ったDecisionOS handoffは、VerifyOS原本テストの
`_source()` が構成する **原本テスト形式に従う模擬パケット** だった。

v0.46では、ここを一段遡る。原本の

- `runtime/kuuos_decisionos_bounded_plan_synthesis_request_handoff_v0_8.py`
- `runtime/kuuos_verifyos_middle_way_conditional_continuity_verification_v0_4.py`
- `runtime/kuuos_planos_middle_way_bounded_synthesis_intake_kernel_v0_1.py`

の **実際の3ビルダー** を順に呼ぶ。

DecisionOSに与えるv0.7 selection justificationは、テスト専用の元
`scripts/check_decisionos_bounded_plan_synthesis_request_handoff_v0_8.py`
の入力構築関数が生成する。実世界のDecisionOS発行者の真正性や、
v0.7証明書の全来歴を意味するものではない。

## Leanの形式的範囲と確認されたimport obstruction

新規:
`formal/KUOS/Architecture/LeanPythonDecisionVerifyPlanNativeHandoffV0_46.lean`

最初の候補は原本
`KUOS.DecisionOS.BoundedPlanSynthesisRequestHandoffV0_8`
を直接importしましたが、独立CI #44685828821 で、その依存先
`WorldConditionedDistributionHandoffIntakeValidationV0_5.lean` が
`import KuuOS.PlanOSV102` を要求し、現行の`lakefile.toml`の
公開・ビルド可能roots/globsにその歴史的`KuuOS.*`系がないため、
`unknown module prefix 'KuuOS'`で停止することが判明しました。

**原本のLeanファイル、lakefile、既存Mathlib設定は書き換えない。**
この不整合を隠して「元Lean型をimportして証明済み」とは述べない。

そこでv0.46のLean認証対象を、原本v0.8のreceipt構造の
**全35フィールド**と、原本Validity構造の全前提を
新名前空間にそのまま写した **別個のsource-mapped形式モデル**とする。
原本の全バイトはGit blobピンで固定する。ただしこの形式モデルと
未ビルドの元Lean型との**定義的一致は未証明**として障害を保持する。
前提を減らした近道ではなく、完全な原本条件の再形式化である。

v0.45の認証済み有限6経路モデルをimportし、以下の8宣言を構成する。

1. `SourceMappedDecisionHandoffReceipt` — 原本receiptの全フィールドの独立写像。
2. `SourceMappedDecisionHandoffValid` — 原本Validityの全前提の独立写像。
3. `sourceMappedDecisionAuthorityBoundary` — 合成受理と選択・実行権限の分離条件。
4. `sourceMappedDecisionAuthorityBoundary_of_valid` — 全前提から境界を再証明。
5. `WholeReceiptSeam` — 型付きの証明書全体の一致を明示的に要求。
6. `decisionVerifyPlanConditionalWitness` — 上記のsource-mapped前提、証明書全体の接続、v0.45の二段モデルを条件付きに結合。
7. `decisionHandoff_onlyRetainIsBoundedIntake` — retainのみ限定受理。
8. `decisionAndRouteCannotLicenseExecution` — 元の非実行条件の写像とv0.45の非実行定理を保持。

Lean側では原本v0.8型のimport成功・元型との形式的同型・
Python dictとの対応を認証していない。
Python側で**元の3つの実カーネル自体**を動かし、
全パケットの同一性を検査する事実とは分離する。

## Python読み取り専用監査

新規: `runtime/kuuos_lean_python_decision_verify_plan_native_handoff_v0_46.py`

呼び出し: `audit_original_decision_verify_plan_native_handoff(decision_args, six_cases)`

- DecisionOS元ビルダーに**与えられた引数だけ**を渡し、実出力receiptを得る。
- 全6経路について、VerifyOS入力の**原本パケット全体**と
  元DecisionOS出力の完全な型付きJSON同一性を要求する。
- 接続できない場合は、VerifyOS／PlanOSを一度も実行せずBLOCKED。
- 既存v0.45の監査器へ渡し、元VerifyOS 6回、元PlanOS 6回の
  実行結果・証明書全体・6状態・受理Bool・来歴・権限を再照合する。
- 引数と元入力の前後Fingerprintで変化がないことを再観測する。
- 6ケース不足はNO_DATA、不整合や偽造はBLOCKED。
- 3ビルダーは変更せず、計画合成もホスト実行も行わない。

元証明書のdigestだけ、または選択されたcandidate IDだけが同じでも
接続成功とはしない。少数意見・異議・責任・WORLD revisionを含め、
原本の全パケットが同一であることを要求する。

### 原本6経路

| VerifyOS transition | PlanOS disposition | 限定受理 |
|---|---|---|
| retain | bounded_synthesis_intake_ready | true |
| suspend | await_condition_change | false |
| request_revision | return_to_decisionos_revision | false |
| supersede_with_lineage | successor_lineage_reverification_required | false |
| complete | close_without_synthesis | false |
| terminate | terminate_without_synthesis | false |

`true` は限定したintake判定であり、実Plan生成やActOS実行権限ではない。
各経路は独立fixtureであり、共通因果時計を持つ一連の実時系列とはみなさない。

## 閉じないobstruction

- Lean定理からCPython全体への普遍的意味論的refinement: 未証明。
- 形式`WholeReceiptSeam`とnative JSON検査の一般的同値性: 未証明。
- 原本DecisionOS v0.8 Lean型の現行Lake依存閉包でのimportと、
  今回のsource-mapped型との形式的同一性: 未証明（import obstruction）。
  固定`KuuOS.*` root登録の互換性検査が必要。
- v0.7源の外部発行者認証、原本選択行為の真正性: 未確認。
- 複数ストアの原子的スナップショットと大域降下: 未証明。
- 6経路を結び付ける因果時計: 未構成。
- 実Plan生成、実行・臨床・制度・Git・memory書込権限: 付与しない。

Preference ⇏ Descent ⇏ Authority。

## 独立認証条件

新規Leanのため、**docs-only fast pathは使わず**、固定Lean厳格ビルドが必須。
元のLeanファイル全文、imports、dependent signaturesを確認し、元の
固定mathlib APIを変更せず、warningAsError／sorryAsError、
全Python回帰、14個の元Git blobピン、Retained public proof API、
workflow integrity、Governance／Exact-head terminalを全て検査する。

提出HEADとGitHub test-mergeのGit tree一致、独立workflow/job/step
completed／SUCCESSが揃うまでPRはDraft／未マージで保持する。
成功時のみ正式main統合し、**統合後のmain HEADを独立に再認証**する。
保護PR #1558はDraft／OPEN／未マージを維持する。
