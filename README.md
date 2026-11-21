# KuuOS / 空OS

**空・縁起・二諦・中道を、観測・証拠・推論・修復・行為の規律として実装する研究プロジェクト。** Lean 4による形式化、Python runtime、各OS間の条件付き対応、KuuOS-native CodeAIを同じリポジトリで研究しています。

KuuOSの**縁起の一般理論はC60以前から存在**します。C60／陰陽五行／有限幾何は重要な具体的テストベッドですが、理論の出発点でも唯一のモデルでもありません。また、数学的構造に「空」「縁起」と名前を与えることは**解釈**であって、Leanが仏教思想そのものを証明したことにはなりません。

> **状態の読み方（2026-11-22 JST、GitHub MCP観測）**  
> Canonical: [`main`](https://github.com/itakura-hidetoshi/KuuOS/tree/main) @ [`ac5f7db4425e`](https://github.com/itakura-hidetoshi/KuuOS/commit/ac5f7db4425e7d377abce8cadee676b4e34341a4)。  
> 研究PRで成功したCIは、main採用・別PRの認証・行為権限を自動的に意味しません。下記の状態は観測時点のスナップショットです。

**このREADMEは現行案内、[ROADMAP.md](ROADMAP.md)は今後の認証条件です。** 従来の累積記録は削除せず、[旧README全文](README-HISTORY-THROUGH-20261121.md)・[旧ROADMAP全文](ROADMAP-HISTORY-THROUGH-20261121.md)として同一Git blobを保存しています。

## 1. 現在の研究状態

| 系統 | 検証済みの事実 | 残る境界・保留 |
| --- | --- | --- |
| **canonical main / Lean→Python** | [PR #3622](https://github.com/itakura-hidetoshi/KuuOS/pull/3622) **MERGED**。v0.60は、共通祖先を保持する2本のprivate履歴への追記と、既存観測／重なりの両立性・obstructionの保持を、**明示した保存仮定の下で**形式化。対応するPython監査・回帰テストを同じ段階で実装 | 元の全OSのLean↔Python意味論的一致や、外部発行者の真正性・PlanOS実行権限まで証明したわけではない |
| **KuuOS-native CodeAI v0.61** | [研究PR #3623](https://github.com/itakura-hidetoshi/KuuOS/pull/3623)のHEAD `6dee9e0792ca`：専用[独立CI #44950277004](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44950277004) **3/3 SUCCESS**、[Governance #44950276948](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44950276948) **30/30 SUCCESS**。候補A/Bの各8宣言を固定Leanで独立監査し、候補Cの2件の厳格lint失敗をそのまま保存 | **Draft／OPEN／未マージ**。v0.2独立評価器の実行結果は`blocked`。4系統・組織／生成来歴の独立性は`NO_DATA`、Memoryの`verified_useful`への昇格は**HOLD**。v0.61正式Lean採用・PRマージは不可 |
| **Dependent Origination / v1.x** | mainには型付きpresentation、endpoint、生成閉包、各段階のLeanソースがある。個別の認証と公開root全体の認証は分離して記録 | [修復PR #3555](https://github.com/itakura-hidetoshi/KuuOS/pull/3555)は**Draft／OPEN／未マージ**。HEAD `cae0b90098e8`の[Public Proof Roots CI #44955916210](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44955916210)は**FAILURE**。v1.83等の研究進捗をこのPR全体の認証に移してはならない |
| **Qi・五行・高次構造** | 旧18D／19D等の具体的Type値・比較・商・obstructionを段階ごとに形式化。例：[Qi v5.96 正式記録PR #3520](https://github.com/itakura-hidetoshi/KuuOS/pull/3520)はMERGED | あるpresentation上の局所的な降下や非忠実性を、全presentation・全fiberの大域定理へ拡張しない |
| **保護検証** | 固定Lean／mathlibと公開rootの既存規律を維持 | [PR #1558](https://github.com/itakura-hidetoshi/KuuOS/pull/1558)は**Draft／OPEN／未マージ**のまま保護 |

**状態の論理：** 候補生成 ≠ 直接Lean成功 ≠ 独立CI成功 ≠ 全体Governance成功 ≠ 正式採用 ≠ Memory再利用許可 ≠ GitHubマージ権限。特にCodeAI v0.61の**MemoryジョブSUCCESSは、HOLDを正しく検出したこと**を表し、学習知識の採用ではありません。

## 2. 四つの基盤と数学

| 基盤 | 運用上の規律 | 関係する数学（研究・設計層） |
| --- | --- | --- |
| **空** | 出力・証明・記憶・WORLD・presentationを自己権威化しない | 型と証拠の区別、関係的意味論、同値と不変量 |
| **縁起** | 条件、端点、出典、変換、局所関係の履歴を保つ | 依存型、圏論・高次圏論、局所化、層／降下、ホモトピー |
| **二諦** | 形式的な成立、runtimeでの妥当性、実世界の行為権限を混同しない | 型付き意味論、精密化関係、証明と実行の境界 |
| **中道** | 未認証を捏造して採用せず、証拠のない全面停止にも固定しない | 条件付き決定、保留状態、obstruction付きの局所—大域判定 |

これは[Fourfold Core](docs/KUOS_FOURFOLD_CORE_v0_1.md)と[Core Charter](docs/KUOS_CORE_CHARTER_v0_1.md)に沿った**設計上の対応**です。Lean認証が保証するのは各Lean宣言が正確な環境と仮定の下で成立することです。哲学的対応・全系の正しさ・許可された実行は、別の命題・別の審査を要します。

### 判断の経路

1. **観測**と推論を分け、出典・時点・HEADを固定する。
2. 文脈、WORLD、依存端点、仮定、利用できる権限を明示する。
3. 異なるpresentationや解釈を、互換性の証明なしに同一視しない。
4. 来歴と変換履歴、元のType値証拠を残す。
5. 局所的compatibilityを確かめ、降下／貼合の条件を証明する。
6. 貼合が成立しない場合はobstructionを消さずに保存する。
7. 独立再観測・公理監査・runtime試験と権限ゲートを通す。
8. 認証された範囲で最小十分な行為を行い、再観測する。

`Preference ⇏ Descent ⇏ Authority`。確率的な最良候補は証明ではなく、証明も実行許可ではありません。

## 3. 各OS、Lean形式化、Python runtimeの関係

この表は**機能設計の見取り図**であり、全行にわたる完全な形式的精密化が証明済みであるという宣言ではありません。

| 層 | 役割 | 特に守る境界 |
| --- | --- | --- |
| **MemoryOS / Plural / Wa** | 履歴、出典、異なる視点・文脈、版に拘束された記憶 | 要約一致・類似度一致は元証拠や発行者同一性を保証しない |
| **BeliefOS** | 証拠付きの信念・不確実性の更新 | 局所的支持と大域的確定を区別 |
| **DecisionOS** | 条件付き評価、選択肢と決定の証拠 | 選好と許可を区別 |
| **VerifyOS** | 形式・runtime・来歴・監査ゲート | 検証器のSUCCESSが別系統の成功を代替しない |
| **PlanOS** | 制約付き計画、証拠を持つ提案、obstruction管理 | 計画の構築はActOSの実行権限を付与しない |
| **ActOS / ObserveOS** | 許可された作用と、その効果の独立観測 | 要求受領・実行・効果・観測を別状態で扱う |
| **LearnOS / CodeAI** | 失敗分類、修復候補、版固定memory、独立検証を用いる条件付き学習 | 未認証・holdout由来・版違いの経験を再利用可能知識へ昇格させない |
| **Qi／陰陽五行／Mandala等** | 複数の有限・高次・関係的モデルとその比較 | 一つの表現を全世界・全OSの標準解としない |

資料は[形式ソース](formal/KUOS/)、[公開Lean root](formal/KuuOSFormal.lean)、[Python runtime](runtime/)、[実験・検査スクリプト](scripts/)、[テスト](tests/)に分かれています。実装と証明の接続は、対応するLean定義・Python関数・検証条件・source SHAを**個別に**確認してください。

代表的な現在の形式ソース：[Lean→Python v0.60](formal/KUOS/Architecture/LeanPythonTaggedPrivateAppendInvarianceV0_60.lean)。CodeAIのmain側評価器：[Independent Verifier Ensemble v0.2](runtime/kuuos_codeai_independent_verifier_ensemble_v0_2.py)。v0.61の研究用接続は[PR #3623の変更](https://github.com/itakura-hidetoshi/KuuOS/pull/3623/files)にあり、mainへ未採用です。

## 4. KuuOS-native CodeAIの学習経路

`Intent Repository Observation Envelope → Autonomous Structured Edit Synthesis → Candidate Patch Envelope → Typed Error Classification → Verification-Guided Regeneration → Bounded Repair Cycle → Independent Verifier Ensemble v0.2 → Version-Bound Repair Memory → Subtask-Level Version-Bound Memory → Trajectory-Grounded Specialist Router → Environment Capsule / Livelock Gate → Reobservation-Bounded Continuation Gate`

ここでいう**学習**は、ソース・固定版・依存閉包・失敗／成功診断・検証履歴に紐付けた経験を、将来の候補生成へ**条件付きで再利用**することです。モデル重みの更新ではありません。

v0.61のA/B/Cは**モデルから事前提供された全文候補**です。KuuOS-nativeカーネルを通した実際の候補選別・検証と、CodeAI内部のライブモデル生成の成否を混同しません。A/Bは同一構造に非常に近く、数学的戦略の真正な独立性は未認証です。Cのlint失敗は修復成功として扱いません。

v0.61の独立評価は、形式検証の1系統以外の`behavioral/regression`、`adversarial/falsification`、`maintainability/static`と独立来歴が不足しているため`blocked`を返しています。[実CI #44950277004](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44950277004)の成功は、この**fail-closed／HOLD**動作を確認したという限定的な意味です。

## 5. 形式検証の固定条件

| 項目 | 正本の固定条件 |
| --- | --- |
| Canonical branch | `main` |
| Lean | `leanprover/lean4:v4.30.0-rc2` |
| mathlib | `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| Strict validation | `-DwarningAsError=true`、`-DsorryAsError=true` |
| 公理監査 | 指定宣言について`#print axioms`を検査し、`propext`・`Classical.choice`・`Quot.sound`以外を許容しない |
| 保護 | append-only / tighten-only / overwrite-forbidden / same-root。PR #1558の未マージ状態を維持 |

標準的な全公開Lean rootの検証コマンド（計算量の大きいビルドです）：

```bash
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
```

実際の認証には、固定toolchain／mathlib、**完全なimport依存閉包**、source/test-merge tree一致、変更Lean全文の監査、個別宣言の公理監査、独立runnerでの終了状態が必要です。Lean内部のheartbeatやCI時間切れは、定理が偽であることの証明ではありません。反対に、局所的成功だけで全体成功と宣言してはいけません。**資料・文章のみの更新を新しいLean形式証明と扱わない**ことも同じ規律です。

## 6. 読む順番・研究への参加

まず[四基盤](docs/KUOS_FOURFOLD_CORE_v0_1.md)、[Core Charter](docs/KUOS_CORE_CHARTER_v0_1.md)、[ROADMAP](ROADMAP.md)を読み、次に対象の[Leanソース](formal/)と[Python実装](runtime/)を照合してください。具体的な認証の根拠は各PRのHEAD・workflow・job・Leanログを優先します。変更の提案は[CONTRIBUTING.md](CONTRIBUTING.md)を参照し、未認証の箇所は`NO_DATA`として残します。

**過去の経緯**：巨大な時系列を冒頭へ積み重ねていた[旧README](README-HISTORY-THROUGH-20261121.md)と[旧ROADMAP](ROADMAP-HISTORY-THROUGH-20261121.md)は参照可能です。歴史的な「次段」「最新」「SUCCESS」は**当時のHEAD限定**の記述で、2026-11-22の現行認証を表すものではありません。

## Author / License / English overview

KuuOS / 空OSの研究・設計：**Hidetoshi Itakura（板倉英俊）**。著作権・ライセンスに関しては、各ファイルの表示と[LICENSE](LICENSE)（Apache License 2.0）を参照してください。

**English:** KuuOS studies dependent origination, contextual presentations, local compatibility, conditional descent, and explicit obstructions, with Lean 4 proofs and a Python runtime. Philosophical interpretation is not a Lean theorem. Current main includes the Lean→Python v0.60 work; CodeAI v0.61 has successful research CI but remains a draft PR with its independent-ensemble and learning promotion gates deliberately blocked. Global semantic equivalence, unconditional gluing, and execution authority are not claimed.
