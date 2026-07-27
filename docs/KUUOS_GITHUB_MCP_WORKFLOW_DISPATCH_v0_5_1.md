# KuuOS GitHub MCP Workflow Dispatch v0.5.1

v0.5.1 is the immutable-image correction for the repository-side GitHub MCP workflow-dispatch bridge.

The v0.5 request path used `ghcr.io/github/github-mcp-server:v1.0.5`. A real request reached the dispatcher, but the image pull failed with `manifest unknown`, so no MCP dispatch receipt or target run was produced.

v0.5.1 keeps the v0.5 runtime and verification semantics while replacing the unavailable tag with the verified immutable image reference:

`ghcr.io/github/github-mcp-server@sha256:2b0c48b070f61e9d3969269ead600f62d00fb237b60ac849ef3d166ee7de9ad3`

The request Issue title must be exactly:

`[KuuOS MCP Workflow Dispatch v0.5.1]`

The Issue body must be strict JSON with no Markdown fence:

```json
{
  "version": "kuuos_github_mcp_workflow_dispatch_request_v0_5_1",
  "confirmation": "RUN_KUUOS_GITHUB_MCP_WORKFLOW_DISPATCH",
  "expected_main_sha": "<exact main SHA obtained immediately before Issue creation>",
  "workflow_id": "kuuos-github-mcp-live-canary-v0-4.yml",
  "ref": "main",
  "dispatch_nonce": "<unique 8-64 character nonce>",
  "inputs": {
    "confirmation": "RUN_KUUOS_GITHUB_MCP_LIVE_CANARY",
    "server_image": "ghcr.io/github/github-mcp-server@sha256:2b0c48b070f61e9d3969269ead600f62d00fb237b60ac849ef3d166ee7de9ad3",
    "dispatch_nonce": "<same nonce>"
  }
}
```

The dispatcher accepts only an owner-authored Issue with `author_association=OWNER`, exact fields, exact main SHA, the allowlisted target workflow, `main` ref, a valid nonce, and the immutable image digest above.

A 204 workflow-dispatch response is not success. The v0.5 runtime must reobserve a new nonce-bound `workflow_dispatch` run with the exact expected head SHA. A nonce match with a different head SHA triggers cancellation and remains a failed closeout.

The request Issue is closed automatically only when the dispatcher receipt status is `KUUOS_GITHUB_MCP_WORKFLOW_DISPATCH_VERIFIED`.
