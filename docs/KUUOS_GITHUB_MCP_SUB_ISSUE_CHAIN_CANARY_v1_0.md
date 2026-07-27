# KuuOS GitHub MCP Sub-Issue Chain Canary v1.0

This stage extends the verified v0.9 single-edge transaction to a reversible three-level chain:

`owner request root → nonce child → nonce grandchild`.

The transaction requires an empty root, creates both nodes with no parent, binds and reobserves each edge from both directions, removes the leaf edge before the root edge, proves both upward parents absent, and closes grandchild then child.

A compensated cleanup is evidence of bounded recovery only. It never becomes `VERIFIED`.

## Request contract

The live request title is `[KuuOS MCP Sub-Issue Chain Canary v1.0]`. Its body is strict JSON with exactly:

- `version`
- `confirmation`
- `expected_main_sha`
- `transaction_nonce`
- `server_image`

## Verified transaction

1. Reobserve the exact owner-created root Issue.
2. Require the root sub-issue set to be empty.
3. Create and reobserve the nonce child with `parent = null`.
4. Create and reobserve the nonce grandchild with `parent = null`.
5. Bind root → child and reobserve the exact relation downward and upward.
6. Bind child → grandchild and reobserve the exact relation downward and upward.
7. Remove child → grandchild and prove child empty plus grandchild `parent = null`.
8. Remove root → child and prove root empty plus child `parent = null`.
9. Close grandchild and child and reobserve both closed.

## Compensation

After a partial write, cleanup removes the grandchild edge before the child edge, closes grandchild and child as `not_planned`, and proves both upward parents absent. Compensation remains a non-success terminal state.
