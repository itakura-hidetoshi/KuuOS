# KuuOS GitHub MCP Issue–Label Binding Canary v0.7

v0.7 verifies a reversible write that crosses two GitHub resources through the official GitHub MCP Server: a repository label is created, attached to the owner-created request Issue, independently observed, detached, independently observed empty, and deleted.

## Why this stage exists

v0.4 established reversible Issue lifecycle writes. v0.6 established reversible repository-label lifecycle writes. Neither proves that a relationship update between resources is observable and safely reversible. v0.7 closes that gap without creating an additional canary Issue: the owner request Issue itself is the bounded target.

## Authorized request

Create one Issue with the exact title:

`[KuuOS MCP Issue Label Binding Canary v0.7]`

Its body must be strict JSON with exactly these fields:

```json
{
  "version": "kuuos_github_mcp_issue_label_binding_canary_request_v0_7",
  "confirmation": "RUN_KUUOS_GITHUB_MCP_ISSUE_LABEL_BINDING_CANARY",
  "expected_main_sha": "<exact main SHA fetched immediately before Issue creation>",
  "transaction_nonce": "<8–32 characters: letters, digits, hyphen>",
  "server_image": "ghcr.io/github/github-mcp-server@sha256:2b0c48b070f61e9d3969269ead600f62d00fb237b60ac849ef3d166ee7de9ad3"
}
```

The Issue author must equal the repository owner and `author_association` must be `OWNER`.

## Transaction

1. Reobserve the request Issue with `issue_read(method=get)` and verify number, exact title, open state, strict JSON body, exact base SHA, confirmation, and nonce.
2. Reobserve its labels with `issue_read(method=get_labels)` and require an empty set. Any preexisting Issue label blocks all writes.
3. Prove the nonce repository label absent with `get_label`.
4. Create it with `label_write(method=create)`.
5. Reobserve exact name, color, and description with `get_label`.
6. Attach it with `issue_write(method=update, labels=[label])`.
7. Reobserve exactly that one label with `issue_read(method=get_labels)`.
8. Detach it with `issue_write(method=update, labels=[])`.
9. Reobserve an empty label set.
10. Delete the repository label with `label_write(method=delete)`.
11. Reobserve bounded not-found with `get_label`.

Only this complete sequence yields `KUUOS_GITHUB_MCP_ISSUE_LABEL_BINDING_CANARY_VERIFIED`.

## Compensation

After a partial write, the runtime first attempts to restore the request Issue label set to empty and reobserves it. Only after that cleanup is verified may it attempt to delete the nonce repository label and reobserve absence.

Successful compensation yields `KUUOS_GITHUB_MCP_ISSUE_LABEL_BINDING_CANARY_COMPENSATED`, never verified success. Failed cleanup remains `BLOCKED`. A preexisting Issue label set or preexisting repository label is never mutated.

## Evidence

The live workflow records the immutable image digest, exact main SHA, request Issue number, nonce label, each tool-call response, normalized observations, per-record digests, append-only JSONL audit, final receipt, blockers, and warnings. The GitHub token is passed only through the configured environment variable and is never serialized.

Pull-request CI uses only a deterministic mock transport. Actual writes are possible only after merge, through an owner-created request Issue bound to the then-current exact `main` SHA.
