# KuuOS GitHub MCP Live Write Verification v0.3

## 目的

公式 `github/github-mcp-server` を空OSのwrite-capable authority内で起動し、書込み後のGitHub状態を同じMCP sessionから再観測してtransactionを閉じる。

v0.3はread-only運用へ戻すものではない。session全体は次の設定を維持する。

```text
write_capable = true
read_only = false
GITHUB_READ_ONLY = 0
```

verificationに使う個別toolだけは、公式serverが`readOnlyHint=true`として公開したtoolでなければならない。

## transaction

```text
KuuOS authority packet
→ exact repository / base branch / base SHA
→ official GitHub MCP Server stdio session
→ v0.2 write gate
→ issue_write(method=create)
→ write response URL
→ issue number binding
→ issue_read(method=get)
→ assertion comparison
→ VERIFIED receipt + append-only audit
```

`tools/call`が成功を返しただけではcloseoutしない。再観測したGitHub状態が宣言済みassertionと一致した場合だけ、次のstatusを発行する。

```text
KUUOS_GITHUB_MCP_LIVE_WRITE_VERIFIED
```

## 公式tool契約

標準transactionは、公式serverの通常tool surfaceにある次の組合せを使う。

- write: `issue_write`
- `issue_write.method`: `create`
- verification: `issue_read`
- `issue_read.method`: `get`

`create_issue`は`issues_granular` feature flag側のtoolであるため、標準exampleでは要求しない。`issue_write(method=create)`はissue URLを含む最小応答を返す。v0.3はURL末尾からissue番号を導出し、`issue_read.issue_number`へ束縛する。

```json
{
  "issue_number": {
    "$issue_number_from_write_url": "url"
  }
}
```

write URLがissue番号へ解決できない場合はFail-Closedとする。

## authority

次をすべて要求する。

```text
authority_status = KUUOS_GITHUB_MCP_LIVE_WRITE_VERIFICATION_AUTHORITY_READY
runtime.execute_external_actions = true
plan.execute_external_actions = true
external_action_allowed = true
mcp_write_tool_call_allowed = true
post_write_reobservation_allowed = true
verification_tool_call_allowed = true
receipt_write_allowed = true
audit_append_allowed = true
```

write operationにはv0.2と同じ条件を要求する。

```text
operation.approved = true
operation.expected_base_sha = plan.base_sha
operation repository = plan.repository_full_name
```

verification側にも同じrepository scopeを要求する。write先と異なるowner/repoを観測対象にはできない。

## assertion

v0.3は次のassertionを持つ。

### literal equality

```json
{
  "path": "title",
  "equals": "KuuOS GitHub MCP live write verification v0.3"
}
```

### write responseとの一致

```json
{
  "path": "number",
  "equals_write_url_issue_number": "url"
}
```

### containment

```json
{
  "path": "body",
  "contains": "authority-gated KuuOS"
}
```

pathはdot区切りでobject fieldまたはarray indexを指定する。path欠落、operator欠落、不一致はすべてcloseoutを阻止する。

## 導入

現在の`main` SHAを確認し、example内の次の2か所を同じexact SHAへ更新する。

```text
plan.base_sha
transactions[].write.expected_base_sha
```

PATを環境変数へ置く。

```bash
export GITHUB_PERSONAL_ACCESS_TOKEN='...'
```

runtime rootを作る。

```bash
mkdir -p .kuuos/github-mcp-live-v0-3
python3 - <<'PY'
import json
from pathlib import Path
src = json.loads(
    Path('examples/kuuos_github_mcp_live_write_verification_v0_3.json').read_text()
)
root = Path('.kuuos/github-mcp-live-v0-3')
(root / 'github_mcp_live_write_verification_plan_v0_3.json').write_text(
    json.dumps(src['plan'], indent=2) + '\n'
)
(root / 'github_mcp_live_write_verification_authority_v0_3.json').write_text(
    json.dumps(src['authority_packet'], indent=2) + '\n'
)
PY
```

実行する。

```bash
PYTHONPATH=. python3 scripts/run_kuuos_github_mcp_live_write_verification_v0_3.py \
  .kuuos/github-mcp-live-v0-3 \
  --execute-external-actions
```

このexampleは実際にKuuOS repositoryへIssueを1件作成し、そのIssueを`issue_read`で再観測する。

## outputs

v0.2 write evidence:

```text
github_mcp_server_bridge_receipt_v0_2.json
github_mcp_server_bridge_audit_v0_2.jsonl
```

v0.3 closeout evidence:

```text
github_mcp_live_write_verification_receipt_v0_3.json
github_mcp_live_write_verification_audit_v0_3.jsonl
```

v0.3 recordは次を含む。

- write record digest
- verification tool
- verification arguments digest
- observed payload
- observed payload digest
- assertion blockers
- transaction digest

PATはplan、receipt、auditへ直列化しない。

## 境界

```text
write tool available != write authority
write response success != GitHub effect observed
readback available != repository scope matched
observed object exists != declared effect matched
verification tool call != write session read-only
write applied != transaction closed
receipt != successor authority
```

## formal authority

```text
formal/KuuOSGitHubMCPServerBridgeV0_1/V0_3.lean
```

`LiveWriteVerificationGate.Admitted`は次を同時に要求する。

- v0.2 write authority admitted
- write applied
- reobservation allowed
- verification tool read-only
- repository matched
- observed effect matched

登録済み`KuuOSGitHubMCPServerBridgeV0_1` rootからimportし、`lakefile.toml`は変更しない。

## 検証

```bash
PYTHONPATH=. python3 scripts/check_kuuos_github_mcp_live_write_verification_v0_3.py
PYTHONPATH=. python3 -m unittest -v \
  tests.test_kuuos_github_mcp_live_write_verification_v0_3
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KuuOSGitHubMCPServerBridgeV0_1
```
