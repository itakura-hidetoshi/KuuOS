# v0.61 — CodeAI学習経路の現行正本再照合（提案・監査資料）

**対象正本**：`itakura-hidetoshi/KuuOS` canonical `main`
`ac5f7db4425e7d377abce8cadee676b4e34341a4`、
Git tree `f043d43e953cd793122acdb64beaf83ab68e6585`。
固定 Lean `v4.30.0-rc2`、
mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`。

この文書はGitHub MCPと隔離Sandbox MCPの今回の実観測、および
**現行mainのLean・Python一次ソース**を結び付ける追記型の継承記録。
CodeAIを学習済みモデルとして主張せず、未認証の候補を認証しない。
本ファイルは研究候補ブランチにのみ追加し、main・既存Lean・
保護PR #1558の内容を変更しない。

## 1. 現行ソースの学習経路

歴史原本 `docs/CodeAI/README.md` は2026-07-18の更新で、
後続の学習・制御経路を網羅しない。後から追加されたLean・Python仕様：

1. `TypedErrorClassificationV0_1`：
   正確なsource候補＋static preflight finding＋baseline digestを
   版・candidate単位で分類。分類は観測であって構造原因の証明ではない。
   **Leanの実elaborator/linter診断を勝手にstatic taxonomyに写さない。**
2. `VerificationGuidedCandidateRepairRegenerationV0_1`：
   独立検証実行が失敗またはbudget-abortした場合のみ、
   完全な受領書・証拠・候補・sourceのdigest連鎖を検証し、
   check ID、reason IDs、exit、stderr/stdout **digestとbounded excerpt**
   を修復文脈として次候補に渡す。成功した検証は失敗修復に入れない。
3. `BoundedRepairCycleOrchestrationV0_1`：
   失敗した候補を同じcycleの再選択から外し、
   別候補をin-memory isolateへ置いて限定検証。
   次cycleは条件付き提案に留まり自動起動しない。
4. `VersionBoundRepairMemoryV0_1`：
   **独立した**修復者・検証者・記憶管理者が発行した
   `verified_effective`／`verified_ineffective`／`inconclusive`
   を同一commit・source snapshot・候補・typed error・fingerprint・
   schema・Lean toolchain・dependency manifest・repair policyの
   完全一致で照合。`verified_effective`だけ再利用候補。
   Memory自身はread-onlyで永続追記も修復実行もしない。
5. `SubtaskLevelVersionBoundMemoryV0_1`（2026-07-21）：
   `localize`／`diagnose`／`edit`／`verify`各subtaskに
   exact source SHA・source-tree digest・temporal holdout corpus・
   context pack・verifier ensemble・subtask contract・
   predecessor output・dependency slice・toolchain・environment・
   memory policyを結び付ける。
   `verified_useful`の有効で独立検証された履歴のみ
   policyに従いヒント化。stale/superseded/holdout-derivedは除外。
6. `TrajectoryGroundedSpecialistRouterAdmissionV0_1`：
   exact memory packと部分実行軌跡・測定済み独立証拠を照合し、
   formal等の専門処理先を**提案**する。実dispatchをしない。
7. `EnvironmentCapsuleLivelockEfficiencyGateV0_1`：
   exact toolchain、依存、固定runner環境、観測可能な進捗、
   zero-progress/cycles、tool/token/time budgetを検証。
   livelock・version差異・自己申告だけの結果はHOLD。
8. `ReobservationBoundedContinuationProposalGateV0_1`：
   前段のexact受領書、導出された残余budget、必須の
   新規観測・checkpoint・再entryを要求し、
   `observe_repository`、`inspect_artifact`、
   `run_read_only_check`、`run_formal_verification`から
   **1件のみ**read-only次行為を提案。予約/実行/権限は付けない。
9. `ExternalGeneralBenchmarkSWEBenchVerifiedAdapterV0_1`：
   2026-07-21のさらに後段の外部評価用のprotocol-only。
   gold patch・holdout labelsを候補生成・prompt・memoryへ逆流
   させない。評価結果は自動で学習許可やGit権限にならない。

この「学習」は**版・作業単位に拘束された検証済み履歴の検索・
次候補への再投入**であり、モデル重みの更新ではない。
現行のsubtask memory関数はread-only lookupだけを実装し、
実GitHubへの永続保存・CodeAI次候補への無条件自動流入はしない。

## 2. v0.61の実験観測と未接続箇所

正本mainをGitHub MCPで再観測し、原本Lean4 importと
Git blobを固定した上で、研究ブランチ
`codeai/lean-v061-two-stage-candidate-20261121`上に
モデル由来の候補3件を提案として作成。

KuuOSの実CodeAIランタイムによる
read-only source observation → provider boundary →
structured edit synthesis → governed Candidate Patch/Diff：
`CANDIDATE/CANDIDATE/CANDIDATE/REJECT`。
`REJECT`は架空の権限主張入力に対する安全境界試験であって
第四の証明候補ではない。候補選択・Git mutation・実行権限は
すべてfalse。モデル提案は実live CodeAIモデル呼出しではない。

- A: SHA-256 `2a33b3acccf3d18aa4caedb15b95e546e2bd6bb8d25f601175f44abd507c9642`。
  固定Lean 8397／8397ビルド成功。実Lean MCP診断成功、partial=false、
  errors=0、再直接Lean exit=0、ソース復旧済み。
  受領書状態：`LOCAL_LEAN_GREEN_CANDIDATE_ONLY`、
  `independent_ci_success=false`。8宣言の公理出力は
  `propext`、`Quot.sound`のみ。
- B: SHA-256 `c33f470532d9757226f4e05bf3c0182beff8cf52c3c658bc1ec8aa346126643a`。
  隔離direct Lean用のoleanを観測したが、MCP/独立CIは未認証。
- C: SHA-256 `2d2a7ab6a42c6e73d6644b4eaa8facd8406d14bb8a6495d8fed3bf33350761de`。
  直接Leanで2件の`try simp instead of simpa`厳格lint失敗
  （隔離候補の140行、159行）。**これは原因の推定と局所診断であり、
  CodeAI v0.1静的Typed Error Classificationの定義済み
  finding codeとして認証されていない。**
  CodeAI修復feedbackへ昇格する前に、当該正確なversionと
  failed verification-evidence/receiptの明示的対応づけが必要。

現行mainの旧**参考**subtask memoryコーパスはcommit
`2e3801430959946c1d2ecc784cf9e37dab139632`を参照する9件。
v0.61の実main SHA/treeを検索条件としてquery/policyを再封印して
照合した**負の参考テスト**は `READY`、
`no_exact_subtask_version_bound_memory`、
matched=0、excluded=9。これは**旧サンプルだけ**の結果であり、
真の全保存記憶の検索や新学習の完了ではない。

5つの既存reference checker
(VersionBoundMemory、SubtaskMemory、TrajectoryRouter、
EnvironmentLivelock、ReobservationBoundedContinuation)は
隔離Sandboxで各 exit=0。これらは公式reference fixtureの
再現成功であり、v0.61の証明や学習済み状態の認証ではない。

## 3. 次の採用条件（現時点NO_DATA）

- sourceを固定して、局所Lean成功候補A/Bだけを
  正確なv0.61 Independent CI・公理監査へ送る。
  各候補の**全Leanファイル・imports・dependent signatures**
  と変換履歴、`sorryAx`、全公理と同一source Git blobを監査。
- Cの実診断は`verify`工程の観測証拠として保存し、
  既存CodeAI verification-guided repairの必要な
  独立execution/evidence受領書ができるまでは
  `verified_effective`や再使用可能Memory hintへ昇格しない。
- independent verifier（実CI）とrepair producer、
  memory curatorの実識別子・独立性と、holdout非漏洩を確認して
  source-bound・subtask-boundの履歴を**外部追記台帳**へ記録する。
  memory reader自身による永続更新と混同しない。
- 認証済みの同一contextだけを次候補生成の**参考ヒント**に渡し、
  Specialist Router → Environment Gate → Reobservation Gateを
  実際の各前段digestで再評価。判定はread-only・提案のみ。
- 検証済みの完全ファイルだけをGitHub MCPによるPR候補へ採用し、
  採用後Strict Lean、独立CI、公理監査、Git tree一致で認証。
  **PR merge authorityはこれらとは別**。
- 比較評価用SWE-bench/gold/holdoutの結果を
  開発Memoryに入れる行為は禁止。評価での対応関係を保持する。

**状態：CodeAI候補の局所検証まで。一部は未合格。
v0.61の独立CIはNO_DATA。新規学習済みMemoryなし。
正本main unchanged。**

Preference ⇏ Descent ⇏ Authority。

## 4. 2026-11-22追記 — 候補Cの生Lean診断・source境界（研究PR）

[研究PR #3623](https://github.com/itakura-hidetoshi/KuuOS/pull/3623) で、候補Cの独立Lean拒否を、実CI artifactに保存された `model-c/lean.log` と、元のモデル提供Lean全文のSHA-256で再結合する **read-only compiler-lint boundary** を追加した。

- 正確な候補ソースSHA、失敗ログSHA、失敗exitと `diagnostics` 2件、元Lean候補140/159行の `simpa only` を照合する。
- log、source、line、diagnostics、status、利用許可のいずれかが改変されればfail-closed。対応する負の回帰テストを追加。
- 元CodeAI `Typed Error Classification v0.1` の分類対象は **static preflight**。Lean elaborator/linterの出力は現在のtaxonomyに含まれず、実形式分類の受領書は発行しない。
- `simp` への置換は**修復仮説**としてのみ残し、修復実行・独立再コンパイル・保証された原因同定とはしない。
- `verification-guided regeneration` 用の真正な独立execution/repair受領書、4系統・組織の独立性、`verified_useful` Memory昇格は依然 **NO_DATA／HOLD**。候補Cの成功再利用ヒント、正式Lean採用、Git権限は発行しない。

この追記はGitHub研究ブランチに実装した**候補コード**の説明であり、新HEADのCI completed/SUCCESSおよび独立検証が観測されるまでは認証済みと扱わない。
