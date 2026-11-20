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

## Leanの形式的範囲

新規:
`formal/KUOS/Architecture/LeanPythonDecisionVerifyPlanNativeHandoffV0_46.lean`

オリジナルの

- `KUOS.DecisionOS.BoundedPlanSynthesisRequestHandoffV0_8`
- `KUOS.Architecture.LeanPythonVerifyPlanSixRoutesV0_45`

をimportして、以下を構成する。

1. `originalDecisionAuthorityBoundary` — DecisionOSが限定付きリクエストのみを渡し、選択権限・実行権限・合成実施を渡さない条件。
2. `originalDecisionAuthorityBoundary_of_valid` — 原本の`BoundedPlanSynthesisRequestHandoffValid`があるとき上記条件を証明。
3. `WholeReceiptSeam` — **型付きの原本証明書全体の同一性を明示的前提とする**。digest一致だけでは構成できない。
4. `decisionVerifyPlanConditionalWitness` — 有効な原本DecisionOS条件、証明書全体の接続証明、v0.45の2段具体モデルを条件付きに組み合わせる。
5. `decisionHandoff_onlyRetainIsBoundedIntake` — 6経路モデルではretainのみ限定受理。
6. `decisionAndRouteCannotLicenseExecution` — DecisionOSの非実行条件とv0.45の非実行定理を並行して保持。

LeanのWholeReceiptSeamが実行時のPython dictに対して構成されたことを
Leanが証明したわけではない。Python検査でその条件の実際の成否を
**別に再観測**する。証明したのは条件を仮定した形式上の輸送と権限境界である。

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
