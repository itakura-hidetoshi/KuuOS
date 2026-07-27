# KuuOS GitHub MCP Server Bridge v0.2

## 目的

GitHubが保守する公式 `github/github-mcp-server` を、空OSの書込みauthority・repository scope・base SHA・receipt・append-only auditの内側から実運用する。

v0.2の標準profileはwrite-capableである。`read_only`を標準にはしない。

```text
KuuOS write plan
→ exact repository / base / SHA binding
→ official GitHub MCP Server tool discovery
→ direct MCP write gate
→ tools/call
→ receipt + append-only audit

Git object mutation
→ exact_git_action
→ existing Qi GitHub Tool Bridge v2.3
→ exact SHA / expected head SHA endpoint
→ unified receipt + audit
```

## v0.1からの変更

v0.1はread-onlyを既定とし、Git object mutationをholdした。v0.2は次を主経路にする。

- `read_only = false`
- 公式serverのwrite toolをallowlistへ含める
- Issue、Pull Request、コメント、レビュー、ラベル、Actions等のwrite toolをMCP経由で直接実行する
- branch作成、既存fileのcontent-SHA更新、mergeは、MCP toolを直接呼ばず`exact_git_action`として既存のbounded REST bridgeへ委譲する
- direct writeとdelegated writeを一つのreceipt・auditで閉じる

## 公式server設定

公式serverは現在、`GITHUB_TOOLSETS`と`GITHUB_TOOLS`でtool surfaceを限定できる。write toolを使う場合は`GITHUB_READ_ONLY`を有効化しない。

- official repository: `https://github.com/github/github-mcp-server`
- official image: `ghcr.io/github/github-mcp-server`
- token environment: `GITHUB_PERSONAL_ACCESS_TOKEN`

v0.2 runnerはplanの`read_only=false`を`GITHUB_READ_ONLY=0`へ変換する。`all` toolsetは受理しない。

## 直接MCP書込み

次をすべて要求する。

```text
plan.write_capable = true
plan.read_only = false
runtime.execute_external_actions = true
plan.execute_external_actions = true
authority.external_action_allowed = true
authority.mcp_write_tool_call_allowed = true
operation.approved = true
operation.expected_base_sha = plan.base_sha
operation repository = plan.repository_full_name
```

例:

```json
{
  "kind": "call_tool",
  "tool": "create_issue",
  "arguments": {
    "owner": "itakura-hidetoshi",
    "repo": "KuuOS",
    "title": "空OSからのIssue",
    "body": "GitHub MCP Server write-capable bridge v0.2"
  },
  "approved": true,
  "expected_base_sha": "<40-character-main-sha>"
}
```

公式serverのtool annotationで`readOnlyHint=false`と示された操作、またはwrite名規則に該当する操作はwrite gateを通る。

## Git object mutation

以下のMCP toolはv0.2でも直接呼ばない。

```text
create_branch
create_or_update_file
delete_file
push_files
update_pull_request_branch
merge_pull_request
```

理由は、空OSが要求するexact base SHAまたはexpected head SHAを、各MCP tool callが原子的preconditionとして受け取るとは限らないためである。

代わりに`exact_git_action`を使う。

### exact branch creation

```json
{
  "kind": "exact_git_action",
  "approved": true,
  "expected_base_sha": "<40-character-main-sha>",
  "action": {
    "kind": "create_branch",
    "repository_full_name": "itakura-hidetoshi/KuuOS",
    "base_branch": "main",
    "branch": "integration/example",
    "sha": "<40-character-main-sha>"
  }
}
```

### expected-head merge

```json
{
  "kind": "exact_git_action",
  "approved": true,
  "expected_base_sha": "<40-character-main-sha>",
  "action": {
    "kind": "merge_pr",
    "repository_full_name": "itakura-hidetoshi/KuuOS",
    "base_branch": "main",
    "pr_number": 123,
    "merge_method": "merge",
    "expected_base_sha": "<40-character-main-sha>",
    "expected_head_sha": "<40-character-pr-head-sha>"
  }
}
```

この経路は`runtime/kuuos_runtime_daemon_qi_github_tool_bridge_v2_3.py`へplanを生成する。branch作成はexact commit SHA、既存file更新はcurrent content SHA、mergeはexpected head SHAをGitHub REST endpointへ渡す。新規file作成はatomic ref CAS materializerが追加されるまでv0.2では受理しない。

## Formal authority

v0.2定理は登録済みrootのsubmoduleとして配置する。

```text
formal/KuuOSGitHubMCPServerBridgeV0_1/V0_2.lean
```

`formal/KuuOSGitHubMCPServerBridgeV0_1.lean`がこのsubmoduleをimportする。`lakefile.toml`のrootsは変更せず、登録済みrootのstrict buildでv0.1とv0.2を同時に検証する。

## 導入

Dockerを起動し、tokenを環境変数へ置く。

```bash
export GITHUB_PERSONAL_ACCESS_TOKEN='...'
```

exampleからruntime rootを作る。

```bash
mkdir -p .kuuos/github-mcp-v0-2
python3 - <<'PY'
import json
from pathlib import Path
src = json.loads(Path('examples/kuuos_github_mcp_server_bridge_v0_2.json').read_text())
root = Path('.kuuos/github-mcp-v0-2')
(root / 'github_mcp_server_bridge_plan_v0_2.json').write_text(
    json.dumps(src['plan'], indent=2) + '\n'
)
(root / 'github_mcp_server_bridge_authority_v0_2.json').write_text(
    json.dumps(src['authority_packet'], indent=2) + '\n'
)
PY
```

write-capable sessionを実行する。

```bash
PYTHONPATH=. python3 scripts/run_kuuos_github_mcp_server_bridge_v0_2.py \
  .kuuos/github-mcp-v0-2 \
  --execute-external-actions
```

成功時には次を生成する。

```text
github_mcp_server_bridge_receipt_v0_2.json
github_mcp_server_bridge_audit_v0_2.jsonl
```

exact Git actionが含まれる場合は次も生成する。

```text
github_tool_bridge_plan.json
github_tool_bridge_receipt.json
github_tool_bridge_audit.jsonl
```

PAT自体はplan、receipt、auditへ書き込まれない。

## 境界

```text
write tool discovered != write authority granted

operation approved != repository scope matched

base SHA observed != Git mutation atomically guarded

MCP Git mutation available != direct MCP mutation admitted

REST exact-SHA delegation != unrestricted REST authority

receipt != successor authority
```

v0.2はread-only adapterではない。書込みを実行するためのauthority adapterである。ただしtool availabilityだけからauthorityを生成しない。

## 検証

```bash
PYTHONPATH=. python3 scripts/check_kuuos_github_mcp_server_bridge_v0_2.py
PYTHONPATH=. python3 -m unittest -v \
  tests.test_kuuos_github_mcp_server_bridge_v0_2
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSGitHubMCPServerBridgeV0_1
```
