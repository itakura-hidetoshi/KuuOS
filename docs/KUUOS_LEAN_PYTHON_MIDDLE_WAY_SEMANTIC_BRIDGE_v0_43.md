# Lean→Python v0.43 — 中道による条件付き意味論の運用

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## 正本・条件・目的

Repository: itakura-hidetoshi/KuuOS, canonical main.
Source parent: e9cd8a9c314fd78ee5038e79fe0d60fa3632a1f7 (v0.42).
Lean: v4.30.0-rc2; mathlib: 5450b53e5ddc75d46418fabb605edbf36bd0beb6.

「Lean/Python全言語の意味が完全一致するまで運用しない」と
「Pythonのテストが成功すればLeanと同一だとする」の二者択一を拒否し、
条件付きの局所意味対応を、非権限・read-onlyの助言に使用する。
普遍的refinement・大域的降下と局所観測を取り違えない。

## 新規Lean定理：形式層

Source: formal/KUOS/Architecture/LeanPythonMiddleWaySemanticBridgeV0_43.lean

既存VerifyOS中道条件、PlanOSのbounded synthesis intake、
CodeAIの版固定repair memoryをimportして以下を定義・証明する。

1. EvidenceStatus（noData/blocked/locallyChecked）とcombineEvidence：
   observed blockedがNO_DATAより優先し、NO_DATAを成功に変換しない。
   局所的にcheckedとなるための必要十分条件を定理化する。
2. ContextKey/SeamCompatible：WORLDスコープ・来歴・mission契約・
   root・解釈版という条件付き接続の識別。フィールドの一致だけで
   外部WORLDの真正性が証明されるわけではない。
3. LocalSimulation：Lean状態・Python状態、各遷移、
   source/target relation、admissibility、overlap compatibility、
   条件付きpreservationの証明引数を明示する。
4. VerifiedSeam：二つの局所関係の間のコンテキスト一致だけでなく、
   relation transportの証明引数を別途要求する。
5. twoStageConditionalTransport：各段の遷移・許容・overlapおよび
   明示されたseam witnessが存在する場合にのみ二段合成できる。
6. OperationalBoundary：read-onlyでlocally checkedでも
   全称的refinement・global descent・execution authorityは独立。
   成功と非権限の両立例と、任意の関係の無条件成立の否定も示す。
7. VerifyOS中道継続→PlanOS bounded intakeを接続し、
   source statusの一致条件下でもexecution permissionを付与しない。
8. CodeAI VersionBoundRepairMemoryの元HEAD不一致なら、
   repair hintをそのまま証拠に流用できないことを引き継ぐ。

重要：LocalSimulationのpreservesやVerifiedSeamのtransportsは
実際のPythonから自動生成されない。Leanの条件付き定理が
証明済みになっても、Python全実装のformal refinementにはならない。
これらの構造と「中道」「縁起」との対応は命名・解釈の層である。

## Python実運用：観測層

Source: runtime/kuuos_lean_python_middle_way_semantic_bridge_v0_43.py

native-v1.3 の同一の元状態群と単一のoriginal-cycle-rootを要求。
元のLean、Python kernel、Store、既存監査器は変更しない。

- 前半：v0.42のBeliefOS→DecisionOS→PluralOS→WaOS→PlanOSを
  本物の保存genesis/ledger/snapshot・最後の元receiptで再監査。
- 後半：v0.38のPlanOS→ActOS→ObserveOS→VerifyOS→LearnOSを
  既存の型付き接続・元のPlan/Act/Observe/Verify/Learn保存履歴で再監査。
- 貼合点：同一のPlanOS finalのtype-preserving digestと
  同一のoriginal PlanStore rootを要求する。全9 OSについて
  lineage_idとmission_contract_digestの局所的な文脈一致を照合する。
- 9つの元Storeの合計27ファイルを監査前後に観測し、
  変化を検出する。ただし同時刻の原子的スナップショットではない。
- 原本のBelief receipt時刻5000とDecision genesis時刻1000
  の数値差を、そのままobstructionとして返す。
  共通の因果時計は未認証であり全体順序へ昇格しない。

成功結果 SCOPED_MIDDLE_WAY_SEMANTIC_OPERATIONAL は
選択された局所観測が成立したというread-only運用結果に限る。
LeanのVerifiedSeam証明witnessや普遍的refinementを意味しない。

### 3状態

| 局所観測 | 状態 | 最小行為 |
|---|---|---|
| 正確な元保存履歴・receipt・seamが適合 | SCOPED_MIDDLE_WAY_SEMANTIC_OPERATIONAL | read-only助言 |
| 履歴または元receiptが未観測 | NO_DATA | HOLD、創作せず保留 |
| 特定された実際の矛盾 | BLOCKED | 当該文脈の接続だけを拒否 |

BLOCKEDはNO_DATAより優先するが、他の枝の不確実性を消さない。
BLOCKEDは「当該入力が条件を満たさなかった」ことであり、
全ての状況における一般的不可能性のLean証明ではない。

### 保留する障害

- Pythonの全実行についてのLean LocalSimulation.preservation未構成。
- 普遍的なLean/Python semantic refinement未証明。
- WORLD真正性、外部issuer認証、共通因果時計未確認。
- 大域降下と複数ストアの原子的整合未証明。
- ActOS jobs/slicesに対応する実数値witness未証明。
- いかなる実行・臨床・制度・Git・history overwriteの権限も未付与。

### CodeAI・MemoryOS・DecisionOS・PlanOSへの読み取り専用助言

- CodeAI: TEST_REQUIRED_NO_AUTO_MERGE。HEADと固定toolchainを
  独立認証した候補にしか再利用を認めない。
- MemoryOS: APPEND_ONLY_EVIDENCE_PROPOSAL_NOT_WRITTEN。
  追記候補であり、監査器は実際のメモリ書込みを行わない。
- DecisionOS: SCOPED_ADVISORY_NOT_TRUTH。相対的な判断材料のみ。
- PlanOS: REVIEW_ONLY_NOT_EXECUTION。人間または別の
  admission手順での審査材料のみ。計画合成もhost実行もしない。

NO_DATAまたはBLOCKEDのとき、すべての助言はHOLDに下がる。
これらは既存OSカーネルの実行権限を変更しない。

## 検証・認証境界

元のnative v1.3 fixture（9つの実Storeと元のreceipt）で試す。
fixture以外での未観測のreceiptは生成しない。
tests/lean_python_extensions/test_middle_way_semantic_bridge_v0_43.py
で局所成功、9組の3状態join、別段がBLOCKEDでも
他方が合格するケース、Plan-seamの不一致、元Store欠落、
偽造receipt、root symlink、全元ファイル非変更、
各OS非権限、時刻obstructionを検証する。

scripts/check_kuuos_lean_python_middle_way_semantic_sources_v0_43.py
では全旧ソースpinと14個の元Lean/runtime blobを固定し、
新Lean定理のimportsと名前を静的に確認する。
しかしsource文字列の確認はLeanの機械的証明ではない。

正式な形式認証は固定Lean4/Mathlib環境での実Lean build、
依存関係・changed Lean file全文・公理監査と、
Exact-head Strict Lean/Governance CIのcompleted/SUCCESSを条件にする。
候補が失敗した場合、新しい赤いPRを増やさず同一PR内で
CodeAIの失敗理由記録を持ちながら修正する。

差分は新規6ファイルのみ。正式認証後にmainへマージし、
実マージHEADに対してRuntime/Governance/Docsを独立に再観測する。
保護PR #1558 Draft/Open/未マージと固定pinを維持する。
