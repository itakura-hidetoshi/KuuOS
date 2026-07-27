# KuuOS GitHub MCP Server Bridge v0.1

## 目的

GitHubが保守する公式 `github/github-mcp-server` を、空OSの有限権限・由来・receipt・Fail-Closed境界の内側から利用する。

既存の `Qi GitHub Tool Bridge v2.3` を置換しない。v2.3はGitHub REST action planを直接実行する層であり、本層はMCPの `tools/list` / `tools/call` を公式serverへ接続するprotocol adapterである。

```text
KuuOS plan
→ exact repository / base binding
→ toolset allowlist
→ tool allowlist
→ MCP initialize
→ tools/list observation
→ per-operation admissibility gate
→ tools/call
→ receipt + append-only audit
```

## 実装面

- `runtime/kuuos_github_mcp_server_bridge_v0_1.py`
  - MCP 2025-11-25 stdio lifecycle
  - newline-delimited JSON-RPC 2.0
  - `initialize` / `notifications/initialized`
  - `tools/list` / `tools/call`
  - 公式Docker imageまたは明示された絶対pathのbinary launcher
- `scripts/run_kuuos_github_mcp_server_bridge_v0_1.py`
  - planとauthority packetを読み、実接続を起動
- `scripts/check_kuuos_github_mcp_server_bridge_v0_1.py`
  - network mutationなしの決定論的mock検証
- `tests/test_kuuos_github_mcp_server_bridge_v0_1.py`
  - read/write分類、scope、base SHA、Git object mutation hold、token非露出を検証

## 既定profile

既定はread-onlyである。

```text
read_only = true
lockdown_mode = true
toolsets = explicit allowlist
tools = explicit allowlist
execute_external_actions = false
```

`all` toolsetは受理しない。tool discoveryでallowlist中のtoolが実際にserverから提示されない場合も実行前に停止する。

## 導入

Dockerを起動し、GitHub tokenを環境変数へ置く。

```bash
export GITHUB_PERSONAL_ACCESS_TOKEN='...'
```

exampleからruntime rootを作る。

```bash
mkdir -p .kuuos/github-mcp
python3 - <<'PY'
import json
from pathlib import Path
src = json.loads(Path('examples/kuuos_github_mcp_server_bridge_v0_1.json').read_text())
root = Path('.kuuos/github-mcp')
(root / 'github_mcp_server_bridge_plan.json').write_text(
    json.dumps(src['plan'], indent=2) + '\n'
)
(root / 'github_mcp_server_bridge_authority.json').write_text(
    json.dumps(src['authority_packet'], indent=2) + '\n'
)
PY
PYTHONPATH=. python3 scripts/run_kuuos_github_mcp_server_bridge_v0_1.py \
  .kuuos/github-mcp
```

成功時には次が生成される。

```text
github_mcp_server_bridge_receipt.json
github_mcp_server_bridge_audit.jsonl
```

PAT自体はplan、receipt、auditへ書き込まれない。

## 書込みprofile

GitHub MCP Serverにwrite toolが見えていても、それだけでは実行権限にならない。write callには次を同時に要求する。

```text
plan.read_only = false
runtime.execute_external_actions = true
plan.execute_external_actions = true
authority.external_action_allowed = true
authority.write_tool_call_allowed = true
operation.approved = true
operation.expected_base_sha = plan.base_sha
operation repository = plan.repository_full_name
```

runnerではruntime側のgateを `--execute-external-actions` で開く。残りのgateはplanとauthority packetに明示する。

公式MCP toolがexact base SHAまたはexpected head SHAを原子的に受け取れないGit object mutationは、v0.1では実行しない。対象は `create_branch`、`create_or_update_file`、`delete_file`、`push_files`、`update_pull_request_branch`、`merge_pull_request` である。これらは観測には使えても、空OSのGit authorityには昇格しない。

```bash
PYTHONPATH=. python3 scripts/run_kuuos_github_mcp_server_bridge_v0_1.py \
  .kuuos/github-mcp \
  --execute-external-actions
```

## 境界

```text
MCP server configured != tool discovered

tool discovered != tool allowlisted

tool allowlisted != operation admitted

operation admitted != result verified

MCP write capability != Git authority

receipt != successor authority
```

本層は公式GitHub MCP Serverへの接続を可能にするが、候補生成、選択、独立検証、PR ready化、merge判断を一体化しない。

## 検証

```bash
PYTHONPATH=. python3 scripts/check_kuuos_github_mcp_server_bridge_v0_1.py
PYTHONPATH=. python3 -m unittest -v \
  tests.test_kuuos_github_mcp_server_bridge_v0_1
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSGitHubMCPServerBridgeV0_1
```
