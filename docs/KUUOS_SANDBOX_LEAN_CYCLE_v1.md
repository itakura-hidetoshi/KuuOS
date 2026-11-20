# KuuOS Sandbox 内部Lean反復・継承プロトコル v1

## 適用範囲と根拠

2026-11-20 の v1.76 修復では、隔離した Vercel Sandbox に固定 Lean
\`v4.30.0-rc2\` と mathlib
\`5450b53e5ddc75d46418fabb605edbf36bd0beb6\` を導入し、
正確な原本Git blobに対し候補を一時領域で繰り返し型検査した。
候補ごとの診断、元ファイルの保存、32宣言の \`#print axioms\`、
依存モジュールの別検証と GitHub MCP 再観測を区別した。

**この文書は再現手順であり、現行 PR 全体の認証結果ではない。**
現行状態は、その都度 GitHub MCP によって観測し直す。

関連既存実装：
- \`scripts/kuuos_lean_mcp_repair_loop_v1.py\`：MCPによる局所 proof-span
  修復・候補生成。旧正本を必ず復旧する。型や命題自体を変える修復は扱わない。
- \`scripts/kuuos_sandbox_prepare_v1.sh\`：隔離Linuxで固定toolchainを検証・準備。
- \`scripts/kuuos_sandbox_lean_cycle_v1.py\`：候補を受信して直接Lean・
  完全公理監査を反復し、append-only記録を残す。本体はAPIキー不要、GitHub書込不可。
- \`tests/test_kuuos_sandbox_lean_cycle_v1.py\`：オフライン回帰試験。
- `ci/check_registry.d/kuuos_sandbox_lean_cycle_v1.json`：将来の変更パスを
  既存Governanceへ限定的に登録する。Python/Shell/文書だけの変更で
  Strict Lean全体ビルドを選択しない一方、レジストリ自体の変更は
  引き続きfull auditとする。
- \`.github/workflows/kuuos-sandbox-lean-cycle-v1.yml\`：軽量Python契約試験のみ。

## 1. 初期観測と隔離

GitHub MCPで canonical main、作業PR HEAD、作業ファイルと履歴原本の
Git blob SHA-1、全変更Leanファイル、imports、従属定理のsignature、
CI workflow/job/Lean stepを読む。モデルの記憶や古いログのHEADを転用しない。

GitHubの作業PR/本流を書き換えず、Vercel Sandbox MCPで専用の名前付き
Sandboxを作る。Sandbox名・projectId・sessionId・snapshotIdは、作成時
に返された実値だけを使う。停止時は \`get_named_sandbox(resume=true)\`
でスナップショットから新しいセッションを取得する（古い sessionId は使わない）。

GitHub sourceはGitHub MCPが確定した commit SHA を参照する。
例えば公開アーカイブ
\`https://codeload.github.com/itakura-hidetoshi/KuuOS/zip/<exact-SHA>\`
を隔離Sandbox内へ取得して展開できるが、アーカイブ名・HEADや経路から
ソースの真正性を推定しない。各対象ファイルのblobを再検算する。
\`git\` や \`gh\` CLIでの変更・pushを行わない。

Sandboxは課金対象となり得る。作業ごとに資源・セッション期限を確認し、
永続スナップショットへの退避と再開を区別する。プロセス自体は停止時に
継続しない。ログと証拠はファイルとして残る。

## 2. 固定toolchainと依存ビルド

Sandboxに \`curl\`、\`sha256sum\`、\`unzstd\`、\`tar\`、
Python 3 を備える。次を repo snapshot 内から実行する。

\`\`\`bash
bash scripts/kuuos_sandbox_prepare_v1.sh "$PWD" \
  KUOS.DependentOriginationStandardTypeABoundaryPrismRankwiseSimultaneousBPhaseV1_75
\`\`\`

- \`lean-toolchain\` は \`leanprover/lean4:v4.30.0-rc2\`。
- \`lake-manifest.json\` のmathlib revは厳密SHA。
- Lean公式配布物は既存の固定SHA256/サイズで検証後に解凍。
- Lean/Lake自体のバージョンを実行して照合。
- \`lake exe cache get\` で固定mathlibを取得・再利用。
- 必要な依存モジュールだけ \`lake ... build\` する。
- \`.lake\` のキャッシュや未認証 \`.olean\` を正式正本とみなさない。
- 署名やSHA・依存の欠落は **NO_DATA/HOLD**、合格に丸めない。

このセットアップはVercelに固有ではなく、同条件の隔離Linuxでも使える。
通常のdirect runnerはLeanを**インストールしない**。未導入なら中止する。

## 3. 候補生成 → 内部型検査

候補生成は CodeAI / Lean MCP / 人手レビューなど別の入力段階。
旧MCP loopの出力 \`candidate.lean\`、あるいは型付き構造修正の
Leanファイルを **append-only inbox** に入れる。
候補を再生成するときは新規ファイルを置き、既存候補を上書きしない。

\`\`\`bash
mkdir -p /vercel/kuuos-lean-inbox /vercel/kuuos-lean-receipts
# CodeAIから出力された正式な候補を、別名でinboxへ配置。
# cp /isolated/export/candidate.lean /vercel/kuuos-lean-inbox/0001-candidate.lean

export PATH="/vercel/kuuos-lean-pinned-4.30.0-rc2/lean-4.30.0-rc2-linux/bin:$PATH"
PYTHONPATH=. python3 scripts/kuuos_sandbox_lean_cycle_v1.py \
  --project-root . \
  --source formal/KUOS/DependentOriginationStandardTypeABoundaryPrismRawTransfiniteV1_76.lean \
  --source-blob c7fd4eb959d05a2eeb430ea39a12d04ed4030ee9 \
  --source-head 35e2b55cf1a7d8c096a92684852c41c90ba611c6 \
  --namespace KUOS.DependentOriginationStandardTypeABoundaryPrismRawTransfiniteV1_76 \
  --candidates-dir /vercel/kuuos-lean-inbox \
  --receipt-dir /vercel/kuuos-lean-receipts \
  --max-attempts 12 --timeout-seconds 250
\`\`\`

上記のSHAは **2026-11-20の再現例**。次回の実行には必ず
GitHub MCPで再取得した正確なSHAへ差し替える。

直接実行は \`lake env lean -DwarningAsError=true
-Dweak.sorryAsError=true\`。出力 \`.olean\` は正本ではない隔離台帳内に生成し、
終了コード・エラー・タイムアウト・ログ全文・候補SHA256/Git blobを記録する。
失敗候補は次候補へ進み、合格候補で初めて公理監査を行う。

再起動後は同じreceiptディレクトリを渡す。
\`ledger.jsonl\` は追記専用で、処理済み候補SHA256は二重実行しない。
同じ候補を意図的に再検証するときは新しい隔離台帳と前回の根拠を
関連付ける。**未処理候補が無い場合には成功を捏造しない。**

\`--idle-seconds\` と \`--poll-seconds\` は、CodeAIが後続候補を置くまで
限定時間で受信するための設定で、AIの自律的再生成を意味しない。
セッション時間や最大試行数は有限で、超過時はHOLDを保持する。

## 4. 証明statementの変更は別権限

命題を変える修復を黙って「互換」としない。
公開宣言名・順序は厳密に保存し、変更した宣言文面はすべて申告する。
追加したimportも申告対象。候補に \`sorry\`、\`admit\`、\`axiom\`、
\`unsafe\`、\`native_decide\` 等を含めない。

例えば v1.76 の通常の等式から \`HEq\` への変更は、
Leanが合格しても元の等式の無条件な証明ではない。
必ずその宣言名と型輸送を要した理由を記載する。

\`--admission /vercel/v176-declared-changes.json\` のJSON形式：

\`\`\`json
{
  "signature_changes": [
    {
      "name": "standardTypeABoundaryPrismAlternatingStep_bit_false",
      "reason": "Old Eq required nondefinitional coercion; new HEq is explicit, and downstream signatures require independent review."
    }
  ],
  "import_additions": []
}
\`\`\`

実際には変更した全宣言を列挙し、余分な許可も拒否する。
このmanifestは呼出側の申告であり、数学的同値性やマージ権限ではない。
未認可変更は \`SIGNATURE_OBSTRUCTION\`。

## 5. 公理監査・来歴・独立CI

直接Lean合格後、候補と同じ宣言を含む一時auditファイルを作成し、
32件等の**実際の公開宣言数**に対して \`#print axioms\` を実行する。

監査条件：すべての宣言が報告され、許容公理は
\`propext\`、\`Classical.choice\`、\`Quot.sound\` のみ、
\`sorryAx\`なし、auditのLean終了コード0、エラー0。
1宣言でも確認できなければHOLD。

受領書は \`attempt-xxxxx-<sha>/receipt.json\`、ログは同じディレクトリ、
\`ledger.jsonl\` は追記のみ。
\`LOCAL_DIRECT_LEAN_AND_AXIOMS_GREEN_ONLY\` は**局所合格**であり、
\`independent_ci_success=false\`、\`git_write_performed=false\`、
\`authority=LOCAL_ONLY\`を常に明記する。

モデルがGitHubへ提出してよいのは：
1. 局所合格候補の全Leanソース、公開宣言signatureとimportの変更を確認し、
   従属モジュールへの影響を隔離環境で検証した後。
2. GitHub MCPで同じPR HEADと原本blob・歴史原本を再観測し、
   採用候補のGit blobを直接照合した後。
3. 既存の正当な作業PRへ**合格済み候補だけ**採用し、採用後
   Strict Leanと独立公理監査を新HEADに対して確認する。
4. GovernanceがFAILのPRはマージせず、拒否ではなく障害として残す。

**外部CIのqueued/in_progress、比較workflowのSUCCESS、
局所LeanのSUCCESSは、互いに独立した状態。**
比較workflowのSUCCESSを証明SUCCESSに昇格しない。

## 6. 再現した v1.76 の境界

今回の記録では、v1.76は内部direct Leanの終了コード0、
公理監査32/32（標準3公理のみ）、candidate blob
\`c5bcbb03f4b8a549647a061066762b6484c15fce\`。
候補を採用した既存 PR #3555 のHEAD
\`974de8f6b2c6f80a2e1e296066ce8100924025d5\` は
2026-11-20の観測値であり、現在のHEAD保証ではない。

続くv1.77には独立の未解決Lean診断が残った。
したがって **v1.76局所認証 ⇏ v1.77認証 ⇏ PR全体認証 ⇏ マージ権限**。
診断数だけでなく、実Leanの終了コード・公開宣言・公理・依存範囲を判定する。

### 履歴を失わないための障害分類

\`PIN_MISMATCH\`：toolchain/mathlib不一致。
\`SOURCE_OBSTRUCTION\`：対象のGit blob不一致。
\`IMPORT_OBSTRUCTION\`、\`SIGNATURE_OBSTRUCTION\`：型や依存変更未確認。
\`DIRECT_LEAN_FAILED\`：実Leanにエラー。
\`NO_DATA_TIMEOUT\`：時間切れ、**0診断扱い禁止**。
\`AXIOM_AUDIT_UNCERTIFIED\`、\`AXIOM_NO_DATA\`、\`AXIOM_OBSTRUCTION\`：
独立宣言監査が未完成。
\`LOCAL_DIRECT_LEAN_AND_AXIOMS_GREEN_ONLY\`：局所合格、GitHub未反映。

append-only／tighten-only／overwrite-forbidden／same-rootを維持。
CodeAIの選好、局所的な互換性、降下、正式な行為権限を混同しない。
