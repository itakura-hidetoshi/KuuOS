# Lean→Python v0.45 — VerifyOS→PlanOSの中道6経路を型付きで保存

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## 正本と先行成果

Canonical repository: itakura-hidetoshi/KuuOS, branch main.
Parent: 0be0755998af0d07ad7c66514293f15731d9f5e3 (v0.44).
Lean v4.30.0-rc2, pinned mathlib:
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only, tighten-only, overwrite-forbidden, same-root.

**今回の核心:** v0.44の一般的な三状態証拠合成の有限証明を、
既存VerifyOSの「条件付き状態の6種の分岐」から既存PlanOSの
「限定された計画合成リクエストの受理／保留」へ移す。
外部の真理や実行許可を自動的に与えない。

形式的な正本は変更しない：
- formal/KUOS/VerifyOS/MiddleWayConditionalContinuityVerificationV0_4.lean
- formal/KUOS/PlanOS/MiddleWayBoundedSynthesisIntakeV1_03.lean
- formal/KUOS/Architecture/LeanPythonMiddleWaySemanticBridgeV0_43.lean
- formal/KUOS/Architecture/LeanPythonFiniteEvidenceWitnessV0_44.lean

元のPython実装も変更しない：
- runtime/kuuos_verifyos_middle_way_conditional_continuity_verification_v0_4.py
- runtime/kuuos_planos_middle_way_bounded_synthesis_intake_kernel_v0_1.py

## Leanでの具体的二段LocalSimulation

新規:
formal/KUOS/Architecture/LeanPythonVerifyPlanSixRoutesV0_45.lean

Leanの元の型をそのまま用いる：

1. VerifyOS TransitionKind:
   retain, suspend, requestRevision, supersedeWithLineage,
   complete, terminate
2. VerifyOS ConditionalValidityStatus:
   valid, suspended, revisionRequired, superseded,
   completed, terminated
3. PlanOS IntakeDisposition:
   boundedSynthesisIntakeReady, awaitConditionChange,
   returnToDecisionOSRevision, successorLineageReverificationRequired,
   closeWithoutSynthesis, terminateWithoutSynthesis

Leanの元のstatusForTransition、dispositionForStatus、
admittedForStatusと、Pythonの実装ソースの
TRANSITION_TO_STATUS、STATUS_TO_DISPOSITIONの
**有限文字列モデル**を照合する。

- verifyRouteSimulationはLean TransitionKind → ValidityStatusと
  Python String → Stringの条件付き保存証明項を構成。
- intakeRouteSimulationはLean ValidityStatus → (Disposition, Bool)と
  Python String → (String, Bool)の条件付き保存証明項を構成。
- originalVerifyPlanIdentitySeamは、両者の中間関係の一致と
  明示したContextKeyについて輸送証明項を構成。
- sixRouteConditionalTwoStageWitnessはv0.43の
  twoStageConditionalTransportを実際にインスタンス化する。
- onlyRetainRouteAdmittedは、元の有限モデルでは
  retain/validだけがbounded intakeの対象であることを証明。
- supersession、completed、terminatedの各経路は
  指定された再検証・終了へ分岐し、計画合成を実行しない。
- 未定義の文字列経路はNoneを返すモデルであって、実世界の
  状態を勝手に作らない。
- sixRouteCannotLicenseExecutionは局所判定が
  実行ライセンスを付与しないことを明示する。

このLean定理は、Pythonの各カーネルやインタプリタ
全体についての普遍的semantic refinementではない。
モデルが実際のPythonで成り立つかは次の観測で別途検査する。

## Pythonによる元カーネルの直接実行

新規:
runtime/kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45.py

ユーザーまたはテストから供給された6つの元入力ケースだけを受ける。
未観測のDecisionOS受領書やVerifyOS証明書は実装内部で生成しない。

- 元のVerifyOS証明書ビルダーを**6経路それぞれで直接呼ぶ**。
  元の入力source receipt、遷移spec、policy、
  digest、lineage、異議・少数意見の保存も元のカーネルで検査。
- 元のVerifyOSが返した**証明書全体**と、PlanOSへ
  渡す証明書が型保存で同一であることを要求。
  digestだけ同じ・一部フィールドだけ似ている、は不可。
- 元のPlanOS intake証明書ビルダーを**6経路で直接呼ぶ**。
  入力policy、WORLD binding、候補・revision、
  責任来歴とsource digestは元の実装が検査する。
- Leanで証明した6分岐（受理可否を含む）と、
  元のPython関数の返すcertificateの各値を比較する。
  受理可はretainのbounded *intake*だけであり、
  PLANの合成・host実行権限とは異なる。
- 6経路はそれぞれの独立ケースであり、
  同一時系列に起きたことや共通時計での履歴を意味しない。
  ケース間で元のDecisionOS handoff source IDが違う場合は拒否。
- 入力は有限JSONのdeep copyで固定、実行前後の一致を検査。
  不正な型、偽造されたreceipt、源の権限フラグ0/False混同、
  完全証明書のすり替え、SOURCE tableの変更はBLOCKED。
  欠落したcaseはNO_DATAとして作らない。

### 形式3状態と運用効果

| 観測 | 出力 | 行為 |
|---|---|---|
| 元の6つのVerifyOS/PlanOS証明書が全部局所一致 | SCOPED_VERIFY_PLAN_SIX_NATIVE_MIDDLE_WAY_ROUTES_CHECKED | 読み取り専用助言 |
| 元の必要ケースがない | NO_DATA | 保留 |
| 元の判定で矛盾や証明書不一致 | BLOCKED | 当該証拠の利用を拒否 |

CodeAI/MemoryOS/DecisionOS/PlanOSへの助言は、
自動修復・memory書込・Decision選択・Plan合成・
Gitマージ・host実行を一切しない。

## 確認できることと未認証

この段階で独立認証を目指すのは、
Leanの6分岐の具体的な条件付きsimulationと、
**変更していない元のPythonの二つのカーネルの実際の実行結果**。
テストfixtureは元リポジトリの元のDecisionOSソース生成
スクリプトから作る。真正な外部発行者や実世界の記録ではない。

以下は継続して未証明：

- 全CPython実行規則のLeanへの普遍的refinement。
- 原本の外部発行者真正性。
- 6ケース間の因果的時間順序。
- 既存9ストアの原子的スナップショットと大域降下。
- ActOS jobs/slicesの実数値witness。
- 「計画合成の受理」から実際のPlan生成・ホスト実行への権限。
- 臨床判断、制度、Git/memory overwriteに関する権限。

## GitHub独立認証ゲート

新規Lean1、Python runtime1、source checker1、テスト2、文書1
の**6ファイル追加のみ**。既存ソース・CI・保護PR #1558を
変更しない。

今回Leanの新規ファイルがあるので、
Strict Leanを省略してはならない。
必要条件は、提出HEADとtest mergeのGit tree一致、
固定Lean実ビルド（warningAsError / sorryAsError）、
全改変Lean file全文とimport・既存API・公理監査、
元Python2カーネルの6経路テスト・累積Runtime、
独立Governance finalとExact-head terminalの全SUCCESS。
失敗があればPRを増やさず同じPRで原因を学習し修復する。
統合後にも**実マージHEAD**で独立Lean/Runtime/
Governance/Docsを再観測する。

保護PR #1558はDraft/Open/unmergedのまま維持。
