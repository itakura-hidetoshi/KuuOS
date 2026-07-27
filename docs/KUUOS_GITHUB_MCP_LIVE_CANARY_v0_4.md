# KuuOS GitHub MCP Live Canary v0.4

## 目的

空OSから公式 `github/github-mcp-server` を実際に起動し、GitHub上で可逆なwrite transactionを完結できることを確認する。

v0.4はIssueを作成するだけのsmoke testではない。次の全段階が成立した場合だけ成功する。

```text
manual authority
→ issue_write(method=create)
→ issue_read(method=get): open
→ issue_write(method=update): closed/completed
→ issue_read(method=get): closed
→ KUUOS_GITHUB_MCP_LIVE_CANARY_VERIFIED
```

sessionはwrite-capableである。

```text
write_capable = true
read_only = false
GITHUB_READ_ONLY = 0
```

## 通常CIとの分離

Pull Requestとpush CIはdeterministic mockだけを実行する。実GitHubへのwriteは行わない。

live canary workflowは次の条件をすべて要求する。

- `workflow_dispatch`からの手動実行
- refが`main`
- confirmationが`RUN_KUUOS_GITHUB_MCP_LIVE_CANARY`
- `contents: read`
- `issues: write`
- repository-scoped `GITHUB_TOKEN`
- official imageのversion tag、commit tag、またはdigest pin

schedule、push、pull_requestからlive canaryを起動しない。

## 公式server互換pin

既定値は次である。

```text
ghcr.io/github/github-mcp-server:v1.0.5
```

これは「常に最新版」という意味ではなく、v0.4の互換baselineである。`latest`は受理しない。

workflowはimageをpullした後、Dockerが解決したRepoDigestを取得してreceiptへ記録する。version tagで起動した場合でも、実際に動いたcontainer imageのdigestを監査できる。

許可する形式は次だけである。

```text
ghcr.io/github/github-mcp-server:vX.Y.Z
ghcr.io/github/github-mcp-server:sha-<commit>
ghcr.io/github/github-mcp-server@sha256:<digest>
```

## tool surface

live canaryは`issues` toolsetのうち次だけをallowlistする。

```text
issue_write
issue_read
```

`issue_write`はwrite toolとして発見されなければならない。`issue_read`は`readOnlyHint=true`でなければならない。

### 作成

```json
{
  "method": "create",
  "owner": "itakura-hidetoshi",
  "repo": "KuuOS",
  "title": "[KuuOS MCP Canary] reversible <run_identity>",
  "body": "KUUOS_GITHUB_MCP_LIVE_CANARY v0.4"
}
```

返却URLからIssue番号を導出する。番号へ束縛できない応答はFail-Closedとする。

### open再観測

```json
{
  "method": "get",
  "owner": "itakura-hidetoshi",
  "repo": "KuuOS",
  "issue_number": 123
}
```

次を照合する。

- Issue番号
- title
- body marker
- state=`open`

### close

```json
{
  "method": "update",
  "owner": "itakura-hidetoshi",
  "repo": "KuuOS",
  "issue_number": 123,
  "state": "closed",
  "state_reason": "completed"
}
```

### closed再観測

同じ`issue_read(method=get)`を使い、state=`closed`まで確認する。

## 補償close

Issue作成後にopen再観測、primary close、closed再観測のいずれかが失敗した場合、Issue番号が得られていれば補償closeを試みる。

補償closeが成功してもcanary成功とは扱わない。

```text
KUUOS_GITHUB_MCP_LIVE_CANARY_COMPENSATED
```

runnerは非0で終了する。GitHub上のcanary Issueを閉じつつ、transaction不成立を失敗証拠として残す。

補償closeまたはその再観測も失敗した場合は次となる。

```text
KUUOS_GITHUB_MCP_LIVE_CANARY_BLOCKED
```

## authority

次をすべて要求する。

```text
authority_status = KUUOS_GITHUB_MCP_LIVE_CANARY_AUTHORITY_READY
plan_read_allowed = true
tool_discovery_allowed = true
external_action_allowed = true
mcp_write_tool_call_allowed = true
post_write_reobservation_allowed = true
compensating_close_allowed = true
receipt_write_allowed = true
audit_append_allowed = true
```

confirmationは三重に照合する。

```text
workflow input
plan.confirmation
runtime confirmation
```

## 手動workflow

GitHubのActions画面から次を選ぶ。

```text
KuuOS GitHub MCP Reversible Live Canary v0.4
```

入力:

```text
confirmation = RUN_KUUOS_GITHUB_MCP_LIVE_CANARY
server_image = ghcr.io/github/github-mcp-server:v1.0.5
```

workflowは`main`をcheckoutし、`github.sha`をplanの`base_sha`とruntimeの`base_sha`へ同時に束縛する。

## ローカル実行

PATを環境変数へ置く。

```bash
export GITHUB_PERSONAL_ACCESS_TOKEN='...'
```

exampleをruntime rootへ展開する。

```bash
mkdir -p .kuuos/github-mcp-live-canary-v0-4
python3 - <<'PY'
import json
from pathlib import Path
src = json.loads(
    Path('examples/kuuos_github_mcp_live_canary_v0_4.json').read_text()
)
root = Path('.kuuos/github-mcp-live-canary-v0-4')
(root / 'github_mcp_live_canary_plan_v0_4.json').write_text(
    json.dumps(src['plan'], indent=2) + '\n'
)
(root / 'github_mcp_live_canary_authority_v0_4.json').write_text(
    json.dumps(src['authority_packet'], indent=2) + '\n'
)
PY
```

Dockerが解決したdigestを取得する。

```bash
IMAGE='ghcr.io/github/github-mcp-server:v1.0.5'
docker pull "$IMAGE"
DIGEST="$(docker image inspect "$IMAGE" --format '{{index .RepoDigests 0}}' | sed 's/.*@//')"
```

実行する。

```bash
PYTHONPATH=. python3 scripts/run_kuuos_github_mcp_live_canary_v0_4.py \
  .kuuos/github-mcp-live-canary-v0-4 \
  --confirmation RUN_KUUOS_GITHUB_MCP_LIVE_CANARY \
  --repository itakura-hidetoshi/KuuOS \
  --base-sha 938081d3bc8b54b1e06d59474d8ada39b60dafd9 \
  --run-identity local-manual \
  --resolved-image-digest "$DIGEST" \
  --execute-external-actions
```

## evidence

```text
github_mcp_live_canary_receipt_v0_4.json
github_mcp_live_canary_audit_v0_4.jsonl
```

receiptは次を含む。

- exact repository / branch / base SHA
- configured server image
- resolved image digest
- Issue番号とURL
- open verification
- close application
- closed verification
- compensationの有無と結果
- phaseごとのargument digest、response、observed payload、record digest

Tokenはplan、receipt、auditへ直列化しない。

## formal authority

```text
formal/KuuOSGitHubMCPServerBridgeV0_1/V0_4.lean
```

`LiveCanaryGate.Admitted`は次を要求する。

- explicit confirmation
- exact repository
- exact base SHA
- create applied
- created Issue observed open
- close applied
- same Issue observed closed
- official image pinned
- resolved image digest recorded

補償closeはcleanup証拠であり、admissionを与えない。

## 境界

```text
manual dispatch != authority
GITHUB_TOKEN available != write approved
Issue created != canary successful
Issue observed open != cleanup complete
close response success != closed state observed
compensation closed != verified transaction
version tag configured != resolved digest recorded
receipt != successor authority
```
