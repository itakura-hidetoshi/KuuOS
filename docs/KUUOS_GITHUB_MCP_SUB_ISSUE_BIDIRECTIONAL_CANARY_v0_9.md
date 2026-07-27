# KuuOS GitHub MCP Sub-Issue Bidirectional Canary v0.9

v0.9 extends the completed v0.8 reversible sub-issue transaction with an independent upward relationship observation from the child Issue.

## Completed v0.8 evidence

PR #1364 merged at `fb25c64fef34b6eeb38c97398c67465640b72261`.

The post-merge owner request Issue #1365 created child Issue #1366 through the immutable official GitHub MCP Server image. Live run `30289639281` completed successfully and verified the downward parent-to-child add/remove sequence. Artifact `8662244533` had digest `sha256:9e9adc3abe46a8220ac4bda9d6a726fadc7df14d42c6419b9605beeec9b6cf8d`.

v0.8 closed with no residual parent-to-child relationship, both Issues closed/completed, compensation unused, and no serialized token value.

## New bidirectional boundary

The official `issue_read` tool exposes `method=get_parent`. At the pinned official server commit `eb088dfe9d854dab6453a8d4ae5871a5ced20974`, the response contract is:

- attached child: `{"parent":{"number", "title", "state", "url", "repository"}}`;
- child without a parent: `{"parent":null}`.

v0.9 requires three upward observations:

1. immediately after child creation and before add, `get_parent` returns exactly `{"parent": null}`;
2. after `sub_issue_write(method=add)`, the downward singleton observation succeeds and `get_parent` returns the exact owner request parent;
3. after `sub_issue_write(method=remove)`, the downward empty-set observation succeeds and `get_parent` again returns exactly `{"parent": null}`.

The attached parent must match the exact Issue number, title, open state, repository, and Issue URL.

## Transaction

The primary transaction is:

1. reobserve the exact owner-created strict-JSON parent request;
2. require the parent sub-issue set to start empty;
3. create one nonce-bound child Issue;
4. reobserve the exact open child;
5. require the child parent to start null;
6. add the relationship;
7. reobserve the exact child from the parent;
8. reobserve the exact parent from the child;
9. remove the relationship;
10. reobserve the parent child set empty;
11. reobserve the child parent null;
12. close the child as completed;
13. reobserve the exact closed child.

Only the complete uncompensated sequence receives `KUUOS_GITHUB_MCP_SUB_ISSUE_BIDIRECTIONAL_CANARY_VERIFIED`.

## Compensation

After child creation, any failed primary step attempts:

- relationship removal;
- parent child-set empty reobservation;
- child parent-null reobservation;
- child close as `not_planned`;
- closed-child reobservation.

A cleaned transaction is `COMPENSATED`, never `VERIFIED`. Failure to prove both downward and upward relationship absence remains `BLOCKED`.

## Authority and evidence

The request is bound to the exact default-branch SHA, an 8–32 character nonce, the immutable official server digest, the `issues` toolset, and the three-tool allowlist `issue_write`, `issue_read`, and `sub_issue_write`.

Pull-request CI uses only deterministic mock transport. External writes occur only after merge through the exact owner request Issue trigger. The token remains environment-only and is never written to the receipt or append-only audit records.
