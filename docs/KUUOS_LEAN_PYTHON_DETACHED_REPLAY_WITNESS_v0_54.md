# KuuOS Lean→Python v0.54 — 局所replay台帳の分離証拠と条件付き照合

**Canonical source at branch creation:** `7407790bd23be7e13be3aa99c4637141bb7e127a` (v0.53 merged).
Lean `v4.30.0-rc2`、mathlib
`5450b53e5ddc75d46418fabb605edbf36bd0beb6`。
append-only／tighten-only／overwrite-forbidden／same-root。
元のVerifyOS／PlanOS、v0.53台帳、公開107 proof roots、既存Lake pinは**変更しない**。

## 研究上の隔たりと今回の最小実装

v0.53のSQLite追記は、同一ファイルに対する局所的二申告の原子性と
リプレイ拒否を提供するが、DB管理者は全履歴を置換し、digestを再計算できる。
従って局所chainの自己整合性から外部の証拠の真正性へ降下できない。

v0.54は次の**三つの層を明示的に分離**する。

1. **局所export**：
   `export_detached_local_replay_witness(absolute_path)` は、
   読み取り専用SQLite snapshotでv0.53の厳密なschemaとchainを照合し、
   row ID／非秘密のkey ID／context／sequence／nonce／message SHA-256／
   前行digest／現行digestと最後のheadを固定形式へ出力する。
   MAC秘密鍵・HMACタグ・原本claim内容は含めない。
   snapshot全体のcanonical JSONのSHA-256も返す。
2. **外部で再計算可能な検査**：
   `verify_detached_replay_witness(manifest)` は、SQLiteなしで
   形式・連番・二行組・重複鍵・全chain digestを検証できる。
   成立するのは**提示データの自己整合性のみ**。
3. **別途与えられたcheckpoint値との照合**：
   `separately_supplied_checkpoint_sha256` を明示的に渡した場合のみ、
   manifest全体のdigestとの一致／不一致を報告する。
   不一致はobstructionとして保持する。

## 判定と明示的に未認証のもの

- `DETACHED_REPLAY_SELF_CONSISTENT_UNANCHORED_PROPOSAL_ONLY`：
  chain自己整合性あり、独立checkpointは無い。
- `CALLER_SUPPLIED_CHECKPOINT_VALUE_MATCH_PROPOSAL_ONLY`：
  提示されたcheckpoint**値**と計算値の一致。
  同じ提示者が両方を与えた場合も成立するため、独立性の証拠ではない。
- `CALLER_SUPPLIED_CHECKPOINT_MISMATCH_OBSTRUCTION`：
  局所chain内部が整合していても、別途与えられたcheckpoint値と食い違う。
- `BLOCKED`：row改変、schema／hash／型／重複／断絶／異常なパス等。
- `NO_DATA`：入力manifestまたは台帳パスがない。

**重要**：checkpointの保管者・署名・作成時刻・発行者の真正性は
この関数は確認しない。後からローカルSQLite全体を置換し、すべての
row digestを再計算する攻撃では、**古い独立checkpointが保持されて
いる条件で初めて**値の不一致を検知できる。第三者の真正な署名証明も、
実際に独立した管理者の保持も、ここではまだ実装されていない。

ローカルファイルの物理的な不変性、cross-host replay防止、
common causal clock、HMAC-SHA256の暗号学的保証、外部主体による
発行・秘密の管理、原本PlanOS三つの結果Finsetの発行事実、
普遍的Lean↔CPython意味保存、全OSの降下、ホスト実行権限は
**未証明・NO_DATA**のまま保持する。

## Lean定理の強さ

原本PlanOS型とv0.53 finite local replay ledgerを直接import。
任意の抽象`step : String → LocalReplayTicket → String`に対して、

- 履歴の前後分割で`foldl`の合成が一致すること
- self-consistency と外部から宣言されたcheckpoint値の一致を
  **両方仮定したときに限り**再計算headがその値と一致すること
- 宣言値が異なれば、値の照合が否定されること
- v0.53のfresh二重予約における局所key保持と原本PlanOS権限なしを維持すること

を証明対象とする。抽象`step`がPythonのSHA-256と等しいこと、
SQLiteのserializationと同一であることは**証明していない**。
形式構造と縁起／空の意味づけも解釈層であり、Lean定理そのものとは区別する。

## 検証工程

新規Leanの厳格ビルドと全9宣言の公理監査を固定環境の独立CIで確認する。
Pythonの新規テストでは6つの実VerifyOS/PlanOS経路、DBを削除した
独立offline検証、元のchain書換、別途提供されたcheckpointと不一致、
secret不出力、元カーネル非実行、固定ソースGit blob検査を扱う。
PR全体のRuntime/Governance及び提交HEAD／テスト用マージtreeの一致、
main統合後の独立push CIも別段階で判定する。

PRはDraft/HOLDとし、未成功を成功として昇格しない。
保護PR #1558はDraft／OPEN／未マージを保持する。
Preference ⇏ Descent ⇏ Authority。
