# Lean→Python v0.44 — 中道の有限3状態モデルに対する具体的意味保存witness

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## 正本・限定された研究目的

Repository: itakura-hidetoshi/KuuOS, canonical main.
Parent: e14b193e8b4f735008c3d97fb6bca61671213130 (v0.43).
Lean: v4.30.0-rc2; mathlib:
5450b53e5ddc75d46418fabb605edbf36bd0beb6.

v0.43でLean4形式化された一般的なLocalSimulationは、
保存関係の証明を引数として**要求するだけ**だった。
「実行中のPython全体がLeanと完全一致する」という仮定は置かない。

v0.44では、元のv0.43 Python関数
runtime.kuuos_lean_python_middle_way_semantic_bridge_v0_43.combine_evidence
の**有限3状態の判定**に対象を限定し、具体的な証明構造と
Python実行観測を接続する。

これは「有限に列挙できる局所対応を、実装変更なしに検証して運用する」
という中道の段階であり、普遍的な意味論的一致を宣言するものではない。

## Lean — 実際にインスタンス化する有限意味保存

新規:
formal/KUOS/Architecture/LeanPythonFiniteEvidenceWitnessV0_44.lean

既存の証明済み形式成果物:
formal/KUOS/Architecture/LeanPythonMiddleWaySemanticBridgeV0_43.lean

定義：

- EvidenceStatusはnoData / blocked / locallyChecked。
- encodeStatusはそれぞれNO_DATA / BLOCKED / LOCALLY_CHECKEDへ写像する。
- pythonJoinModelは文字列の独立した有限モデルであり、
  未登録の入力は、NO_DATAと組んでもBLOCKEDを返す。
- finiteEvidenceSimulationは、v0.43 LocalSimulationの
  sourceRelation、targetRelation、両遷移と局所仮定を
  **具体的に設定**し、preservesの証明項を構成する。
- finiteIdentitySeamは明示された単一ContextKeyについて
  VerifiedSeamの文脈一致と関係の輸送証明を構成する。
  ContextKey自体の外部真正性は証明しない。

主な定理：

- encodeStatus_injective
- encodedJoin_commutes（3×3の完全な9通り）
- finiteTwoStageSimulation
  （v0.43 twoStageConditionalTransportを具体的witnessで呼ぶ）
- encodedTwoStage_commutes（3×3×3の27通り）
- combineEvidence_assoc
- pythonJoinModel_assoc_on_encoded
- invalidPythonStatus_blocks / invalidPythonStatus_with_noData_blocks
- unknownPythonStatus_is_not_success
- finiteCheckedWitness_grants_no_execution

ここでLeanがモデル化するPythonの要素は、**Stringの
入力に対する特定の純粋な関数形状**である。
本物のCPythonの評価器、呼出時の任意のメモリ状態、
OS全体のホスト副作用、乱数、外部発行者の署名等を
Leanから検証したわけではない。

## Python — 同じ局所範囲の実装を独立に実行検査

新規:
runtime/kuuos_lean_python_finite_evidence_witness_v0_44.py

既存v0.43のcombine_evidenceを一切変更せず、
独立した判定表実装と次を比較する。

1. 3状態の全9入力組を、実際の元Python関数で実行。
2. 3状態の左結合2段遷移、全27入力組を同様に実行。
3. 「PASS」「CHECKED」、空文字、表記ゆれ、None、
   bool、整数、floatなど8種の未登録値について、
   3状態の各パートナーと左右で48組の拒否を独立に検査。
4. 意図的に元Python関数の出力を誤らせた時、検査が
   BLOCKEDとなり局所認証を取り消す反例試験。
5. さらに元のnative v1.3 full cycleの9保存ストア、
   Belief/Decision/Plural/Wa/Plan/Act/Observe/Verify/Learn
   と正規のPlanOS seamを、変更していないv0.43監査で再観測。
   これも独立した外部真正性・同時スナップショットではない。

返却値：

- SCOPED_FINITE_PYTHON_EVIDENCE_TABLE_MATCH：
  Pythonの**今回の有限入力範囲**で表が一致した。
- SCOPED_FINITE_MIDDLE_WAY_NATIVE_INSTANCE_COMPATIBLE：
  有限表の照合と選択された9保存ストアのread-only監査が
  同じ要求に対して合格した。
- NO_DATA：
  元記録や受領書が欠落。有限表だけ成功しても、
  9保存ストアが正しいと主張しない。
- BLOCKED：
  実測した局所不一致・未登録入力の受理・履歴矛盾。
  これは普遍的な数学的不可能性の証明ではない。

各局所成功がコード上で返すのは、CodeAI、MemoryOS、
DecisionOS、PlanOSへの**助言**のみ。ホスト実行、
Gitマージ、MemoryOS書込、臨床判断、真理主張の権限を与えない。

## 証拠の強さ・未認証部分

今回認証し得ること：

- Lean4カーネルが有限モデルの条件付き形式定理を認証する。
- 元のPython関数が全9組・27経路・48不正値試験に合格する。
- 元のv0.43監査で9保存ストアの来歴・局所接続を観測する。

今回**証明しない**こと：

- Leanモデルと任意のCPythonバージョンの評価規則の完全同値。
- 全OSのPython実装がLocalSimulation.preservesを満たすという全称命題。
- 原本9ストアの原子的スナップショットまたは大域的降下。
- Belief受領書5000とDecision genesis1000の共通因果時計。
- 外部issuer真正性、ActOS実数値witness、実行権限・Git権限。

Preference ⇏ Descent ⇏ Authority の境界を保持する。

## 独立検証

追加ファイル6件のみ。既存Lean定理・Pythonカーネル・store・
既存監査器・CI workflowを変更しない。

変更されたLeanファイル全文とimport/pinned Mathlibを、
固定Lean環境の実際のLean elaborationでチェックする。
Source-string inventoryだけではLeanの証明にはならない。

実行コマンド：

    python3 -m scripts.check_kuuos_lean_python_finite_evidence_sources_v0_44
    python3 -m unittest discover -s tests/lean_python_extensions -p 'test_finite_evidence_*v0_44.py' -v

Lean:
    lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true \
      build KUOS.Architecture.LeanPythonFiniteEvidenceWitnessV0_44

GitHubの同一提出HEADに対するStrict Lean、
Runtime、Governance集約、Exact-head受領書が
completed/SUCCESSであること、提出HEADとtest-mergeの
Git tree一致を確認してからマージする。
失敗時は同じPRで修正し、エラー原因を追記する。
統合後も実マージHEADの独立push CIを別に認証する。
保護PR #1558はDraft/Open/未マージ。
