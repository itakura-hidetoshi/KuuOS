# KuuOS GitHub MCP Repository Label Canary v0.6

## 目的

公式 `github/github-mcp-server` のrepository-label書込みを、空OSのauthority、exact repository、exact `main` SHA、nonce、receipt、append-only auditの内側で可逆に実証する。

v0.6は既存Issueへのラベル付与ではなく、repository labelそのものを短時間だけ作成・再観測・削除・不在再観測する。そのため既存IssueやPull Requestのmetadataを変更しない。

## 実行系列

```text
get_label
→ nonce-bound labelが存在しないことを確認
→ label_write(method=create)
→ get_label
→ exact name / color / descriptionを照合
→ label_write(method=delete)
→ get_label
→ bounded not-foundを確認
→ KUUOS_GITHUB_MCP_LABEL_CANARY_VERIFIED
```

成功条件はcreateやdeleteの応答だけでは満たされない。公式MCP Serverによる独立した`get_label`再観測を必須とする。

## 公式tool契約

使用するtool surfaceは次の2つだけである。

- `label_write`: write tool。`create`と`delete`を使用する。
- `get_label`: read-only tool。作成後のexact metadataと削除後の不在を確認する。

`label_write`がread-onlyとして発見された場合、または`get_label`がwriteとして分類された場合はfail-closedとする。

## immutable image

公式server imageは次のdigestへ固定する。

`ghcr.io/github/github-mcp-server@sha256:2b0c48b070f61e9d3969269ead600f62d00fb237b60ac849ef3d166ee7de9ad3`

実行時にDockerが解決したdigestをreceiptへ記録する。

## repository-side request

request Issue titleは完全一致で次を使う。

`[KuuOS MCP Label Canary v0.6]`

Issue bodyはMarkdown fenceを付けず、strict JSONだけを書く。

```json
{
  "version": "kuuos_github_mcp_label_canary_request_v0_6",
  "confirmation": "RUN_KUUOS_GITHUB_MCP_LABEL_CANARY",
  "expected_main_sha": "<Issue作成直前に取得したmainのexact SHA>",
  "label_nonce": "<一意な8〜32文字の英数字またはハイフン>",
  "server_image": "ghcr.io/github/github-mcp-server@sha256:2b0c48b070f61e9d3969269ead600f62d00fb237b60ac849ef3d166ee7de9ad3"
}
```

requestは次をすべて満たさなければならない。

- Issue作成者がrepository owner
- `author_association=OWNER`
- top-level fieldが完全一致
- `expected_main_sha`がIssue eventに束縛されたexact `main` SHAと一致
- `label_nonce`が`[A-Za-z0-9][A-Za-z0-9-]{7,31}`に一致
- imageが上記immutable digestと完全一致

## 生成されるlabel

label name:

`kuuos-mcp-canary-<label_nonce>`

color:

`5319e7`

description:

`KUUOS_GITHUB_MCP_LABEL_CANARY v0.6 <label_nonce>`

preflightで同名labelが既に存在した場合、createもdeleteも行わずBLOCKEDとする。既存labelをcanary対象として削除してはならない。

## 補償

preflightで不在を確認した後、createを試みた時点から、正常な削除・不在再観測が完了しなかった場合は補償deleteを試みる。

```text
補償delete成功 != 正常成功
```

補償後に不在が確認できた場合のstatusは`KUUOS_GITHUB_MCP_LABEL_CANARY_COMPENSATED`であり、`VERIFIED`へ昇格させない。補償後もlabelが残る場合は`BLOCKED`とする。

## receipt

成功時には次を記録する。

- exact repository / branch / base SHA
- configured image / resolved digest
- nonce-bound label name / color / description
- preflight absence
- exact created-label observation
- deleted-label absence observation
- compensationの有無
- 各tool callのarguments digest、response、observation digest

PATや`GITHUB_TOKEN`自体はplan、receipt、auditへ保存しない。
