# KuuOS Lean→Python v0.49 — PlanOS未観測結果集合の形式的obstruction

**研究候補。認証前の定理と実行結果を混同しない。**

Base canonical main: `c9f3987b15adb0bfd818027090efd7ae85203ee4`. Lean `v4.30.0-rc2`,
mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`.
append-only／tighten-only／overwrite-forbidden／same-root。

## 正本の原本型から構成する証明

`formal/KUOS/Architecture/LeanPythonPlanResultObservationObstructionV0_49.lean`
は原本 `MiddleWayContinuityCertificate` および
`MiddleWayBoundedSynthesisIntakeCertificate` を直接使用する。

PlanOSの元Python実装で確認できる情報を反映する **限定型付き投影**
`VisiblePlanSourceProjection` を定義する。この投影は完全な
Pythonシリアライザや署名の数学モデルではなく、出力に含まれない
PlanOS resultingLineage／resultingDissent／resultingMinorityEvidence
を意図的に持たない。

- v0.48で構成した original-type inertPlan と、
  新たに余分な来歴・異議・少数意見を持つ原本PlanOS証明書を構成する
- 両方が原本の7フィールド `OriginalCertificateSeam` と
  `MiddleWayBoundedSynthesisIntakeCertificateValid` を満たす
- 限定投影は一致しても、freshな要素があれば元のFinsetは異なる
- 同一投影から両方の原本証明書を復元する関数は存在しえない（条件付き）
- 元の証明書が存在したこと、外部実行されたこと、因果履歴や
  元Python全体の非単射性は**主張しない**

## Pythonの独立実際観測

元のVerifyOS v0.4とPlanOS v1.03を変えずに、実出力に対しv0.48の
read-only監査を再実行。その局所検査に合格しても、元PlanOSが
上記3つの *resulting* 集合を出力しないため、観測結果は **NO_DATA**。

新規監査器
`runtime/kuuos_lean_python_plan_result_observation_obstruction_v0_49.py`
は、元実装に存在しない集合フィールドを追記してダイジェストを
再計算したケースも、元出力そのものとしてはBLOCKEDする。

実カーネル6経路と偽装／欠測／読み取り専用の独立回帰テストを追加。
既存Leanファイル、元Pythonカーネル、全107公開roots、Lake依存、
従来のworkflowは書き換えない。

未観測と不可能が証明された状態は別。ここで不可能と示すのは
**定義した投影から元の異なる二証明書を同時に完全復元すること**に限る。
新しい真正な出力字段や型付き証拠を将来導入する余地は残す。

## 認証と非認証

新規Lean宣言に対し厳格固定Lean、全 `#print axioms`、
Python Runtime全回帰、原本Git blob固定、公開API、workflow、
Governance、Exact-head/source-test-merge tree一致を別々に検証する。

局所認証をmain全体 `KuuOSFormal` SUCCESSへ昇格しない。
原本LeanからCPython全体への普遍的refinement、全ストアの大域降下、
外部発行者真正性、実行権限は未証明のまま保持する。

Preference ⇏ Descent ⇏ Authority。
