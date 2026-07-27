# KuuOS GitHub MCP Sub-Issue Binding Canary v0.8

v0.8 extends the verified official GitHub MCP Server integration from Issue–Label binding to the reversible hierarchy relation between two Issues.

## Authorized request

Create one owner-authored Issue with the exact title:

`[KuuOS MCP Sub-Issue Binding Canary v0.8]`

Its body is strict JSON with exactly these fields:

```json
{
  "version": "kuuos_github_mcp_sub_issue_binding_canary_request_v0_8",
  "confirmation": "RUN_KUUOS_GITHUB_MCP_SUB_ISSUE_BINDING_CANARY",
  "expected_main_sha": "<exact main SHA fetched immediately before Issue creation>",
  "transaction_nonce": "<8–32 letters, digits, or hyphens>",
  "server_image": "ghcr.io/github/github-mcp-server@sha256:2b0c48b070f61e9d3969269ead600f62d00fb237b60ac849ef3d166ee7de9ad3"
}
```

The Issue author and `author_association` must both identify the repository owner. The exact request-event `main` SHA is the transaction base.

## Transaction

1. Reobserve the parent request Issue through `issue_read(method=get)` and verify exact number, title, open state, strict JSON body, SHA, nonce, confirmation, and image.
2. Reobserve `issue_read(method=get_sub_issues)` and require an empty list. A preexisting child blocks all writes.
3. Create one nonce-bound child Issue through `issue_write(method=create)`.
4. Reobserve the exact child title, strict JSON body, open state, numeric database ID, and issue number.
5. Add the child through `sub_issue_write(method=add)`.
6. Reobserve exactly that child through `issue_read(method=get_sub_issues)`.
7. Remove the relation through `sub_issue_write(method=remove)`.
8. Reobserve the parent child-list as empty.
9. Close the child through `issue_write(method=update,state=closed,state_reason=completed)`.
10. Reobserve the same child as closed.

Only the complete sequence yields `KUUOS_GITHUB_MCP_SUB_ISSUE_BINDING_CANARY_VERIFIED`.

## Why the reaction surface is not used

The standard official `add_issue_comment` surface can add a comment or reaction, but the same standard surface does not expose a symmetric remove operation. v0.8 therefore selects `sub_issue_write(add/remove)`, which has an explicit reversible pair and an independent read path.

## Compensation

After child creation, any failed primary closeout attempts both:

- remove the parent–child relation and reobserve an empty parent child-list;
- close the child as `not_planned` and reobserve it closed.

Successful cleanup yields `KUUOS_GITHUB_MCP_SUB_ISSUE_BINDING_CANARY_COMPENSATED`, never verified success. If cleanup cannot be reobserved, the result remains `BLOCKED`.

## Evidence

The receipt and append-only JSONL audit bind the immutable server image, resolved digest, exact repository and base SHA, request parent, child database ID and issue number, nonce, every MCP response, normalized observation, record digests, blockers, warnings, and compensation state. The GitHub token is environment-only and is never serialized.

Pull-request validation uses deterministic mock transport. Actual GitHub writes are enabled only after merge by an owner-created request Issue.
