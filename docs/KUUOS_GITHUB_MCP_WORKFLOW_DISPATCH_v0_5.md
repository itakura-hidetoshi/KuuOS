# KuuOS GitHub MCP Workflow Dispatch v0.5

## 目的

空OSから公式 `github/github-mcp-server` の `actions_run_trigger` を使用し、`workflow_dispatch`をwrite-capable authorityの下で発火する。

v0.5はHTTP 204を受け取った時点では成功としない。発火前のworkflow run集合を保存し、発火後に新規runを再観測して、次をすべて照合する。

```text
baseline workflow runs
→ actions_run_trigger(method=run_workflow)
→ HTTP 204 accepted
→ actions_list(method=list_workflow_runs)
→ new run ID
→ event=workflow_dispatch
→ exact ref
→ unique dispatch nonce
→ exact expected head SHA
→ KUUOS_GITHUB_MCP_WORKFLOW_DISPATCH_VERIFIED
```

session全体はwrite-capableである。

```text
write_capable = true
read_only = false
GITHUB_READ_ONLY = 0
```

## 公式tool契約

互換baselineは公式GitHub MCP Server v1.0.5である。

```text
actions_run_trigger
  method=run_workflow
  owner
  repo
  workflow_id
  ref
  inputs

actions_list
  method=list_workflow_runs
  resource_id=workflow_id
  workflow_runs_filter.branch
  workflow_runs_filter.event=workflow_dispatch
```

公式serverの`run_workflow`はGitHub Actions workflow dispatch APIを呼び、成功時に次を含む応答を返す。

```text
message = Workflow run has been queued
workflow_id
a ref
inputs
status_code = 204
```

204応答にはrun IDが含まれない。そのため、v0.5は発火前後のrun集合差分とnonceを使って対象runを束縛する。

## exact SHA境界

GitHubのworkflow dispatch APIはrefを受け取るが、expected SHAのatomic preconditionを持たない。

v0.5は次の形でこの差を閉じる。

```text
plan.base_sha
= target.expected_head_sha
= runtime base_sha
```

発火後に観測したrunの`head_sha`が一致しなければ、そのrunは成功証拠にならない。

不一致runを観測した場合、authorityで許可された`actions_run_trigger(method=cancel_workflow_run)`を呼び、cancelを試みる。

```text
KUUOS_GITHUB_MCP_WORKFLOW_DISPATCH_MISMATCH_CANCELLED
```

cancel成功はdispatch成功へ昇格しない。runの副作用を停止した失敗closeoutである。

## nonce correlation

同じworkflowが別経路から同時にdispatchされても誤認しないよう、各requestに一意の`dispatch_nonce`を要求する。

```json
{
  "dispatch_nonce": "dispatch-v05-example-001"
}
```

nonceは次の2箇所へ同一値で入る。

```text
target.dispatch_nonce
target.inputs.dispatch_nonce
```

対象workflowはnonceを`run-name`へ含める。v0.5は新規runの`display_title`からnonceを確認する。

## authority

次をすべて要求する。

```text
authority_status = KUUOS_GITHUB_MCP_WORKFLOW_DISPATCH_AUTHORITY_READY
plan_read_allowed = true
tool_discovery_allowed = true
external_action_allowed = true
workflow_dispatch_allowed = true
run_reobservation_allowed = true
mismatched_run_cancel_allowed = true
receipt_write_allowed = true
audit_append_allowed = true
```

confirmationはplanとruntimeで一致しなければならない。

```text
RUN_KUUOS_GITHUB_MCP_WORKFLOW_DISPATCH
```

## connector-facing action

現在のChatGPT GitHub connectorには新規`workflow_dispatch`を作成するactionがない。このbootstrap gapを閉じるため、v0.5はrepository ownerが作成した専用request Issueを入口とするworkflowを追加する。

```text
issues.opened
→ exact request title
→ repository owner author
→ author_association=OWNER
→ strict JSON request body
→ request.expected_main_sha = issue-event github.sha
→ target workflow allowlist
→ v0.5 official MCP dispatch
→ exact run reobservation
→ receipt summary comment
→ request Issue close
```

request title:

```text
[KuuOS MCP Workflow Dispatch v0.5]
```

request body:

```json
{
  "version": "kuuos_github_mcp_workflow_dispatch_request_v0_5",
  "confirmation": "RUN_KUUOS_GITHUB_MCP_WORKFLOW_DISPATCH",
  "expected_main_sha": "<current main SHA>",
  "workflow_id": "kuuos-github-mcp-live-canary-v0-4.yml",
  "ref": "main",
  "dispatch_nonce": "dispatch-v05-live-001",
  "inputs": {
    "confirmation": "RUN_KUUOS_GITHUB_MCP_LIVE_CANARY",
    "server_image": "ghcr.io/github/github-mcp-server:v1.0.5",
    "dispatch_nonce": "dispatch-v05-live-001"
  }
}
```

v0.5のconnector-facing workflowが許可するtargetは、初期段階では次だけである。

```text
kuuos-github-mcp-live-canary-v0-4.yml
```

汎用workflow dispatch authorityへ自動拡張しない。

## v0.4 nonce対応

v0.4 live canary workflowへ任意入力`dispatch_nonce`を追加する。

手動実行では省略できる。v0.5経由では必須であり、run-nameとcanary run identityへ含める。

## 実行

exampleをruntime rootへ展開する。

```bash
mkdir -p .kuuos/github-mcp-workflow-dispatch-v0-5
python3 - <<'PY'
import json
from pathlib import Path
src = json.loads(Path('examples/kuuos_github_mcp_workflow_dispatch_v0_5.json').read_text())
root = Path('.kuuos/github-mcp-workflow-dispatch-v0-5')
(root / 'github_mcp_workflow_dispatch_plan_v0_5.json').write_text(
    json.dumps(src['plan'], indent=2) + '\n'
)
(root / 'github_mcp_workflow_dispatch_authority_v0_5.json').write_text(
    json.dumps(src['authority_packet'], indent=2) + '\n'
)
PY
```

PATまたはrepository-scoped tokenを環境変数へ置く。

```bash
export GITHUB_PERSONAL_ACCESS_TOKEN='...'
```

実行する。

```bash
PYTHONPATH=. python3 scripts/run_kuuos_github_mcp_workflow_dispatch_v0_5.py \
  .kuuos/github-mcp-workflow-dispatch-v0-5 \
  --confirmation RUN_KUUOS_GITHUB_MCP_WORKFLOW_DISPATCH \
  --repository itakura-hidetoshi/KuuOS \
  --base-sha <current-main-sha> \
  --execute-external-actions
```

## evidence

```text
github_mcp_workflow_dispatch_receipt_v0_5.json
github_mcp_workflow_dispatch_audit_v0_5.jsonl
```

receiptは次を含む。

- exact repository / branch / base SHA
- target workflow / ref / nonce
- dispatch accepted
- observed run ID / URL / status / head SHA
- mismatch cancellation attempt and result
- phase別argument digest / response / observed digest / record digest

Tokenはplan、receipt、auditへ直列化しない。

## formal authority

```text
formal/KuuOSGitHubMCPServerBridgeV0_1/V0_5.lean
```

`WorkflowDispatchGate.Admitted`は、v0.2 write authority、明示確認、tool annotation、exact workflow/ref/SHA、nonce binding、204 acceptance、新規run再観測、head SHA一致を要求する。

mismatch cancellationを使用したtransactionはadmissionを得ない。

## 境界

```text
actions_run_trigger discovered != dispatch authority
HTTP 204 accepted != workflow run identified
new run observed != requested run correlated
nonce matched != exact head SHA matched
wrong-SHA run cancelled != dispatch verified
request Issue created != authority granted
receipt != successor authority
```
