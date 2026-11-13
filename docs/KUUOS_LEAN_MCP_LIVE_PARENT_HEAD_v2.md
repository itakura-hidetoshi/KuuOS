# KuuOS Lean MCP current-HEAD source and diagnostic binding v2

**Scope:** append-only read-only extension of the merged PR #3536 full-source
causal evidence engine. Does not change Lean sources, kernel, existing public
roots, imports, warning/sorry controls, proof signatures, or the fixed pins.

## Why this version exists

The earlier PR #3536 inspected all **91** Lean files changed in parent #3522
at immutable HEAD `520dc2ee8927fa40a51c0af31978816f2f41b5a9`.
That is a valid **historical snapshot**, not a license to apply results to a
newer HEAD. Parent #3522 is updated by independent hourly repair actions, so
its file set and errors can change.

This v2 route uses GitHub read-only APIs at run time, from the CI runner, to
capture the parent PR HEAD and base, collect every paginated PR changed path,
and bind the exact Git blob SHA of every changed Lean file. It then checks the
HEAD again. Every source and transitive imported local source is independently
read from a read-only checkout of that exact HEAD, using the already merged
`scripts/check_kuuos_lean_mcp_fullsource_v1.py`.

## Exact provenance and fail-closed checks

1. Confirm the repository, PR number 3522, `open` state, and both complete
   40-character source/base commit SHAs from GitHub.
2. Read every changed file page, enforce the PR's `changed_files` count, and
   reject duplicates, deletions or unsupported renames of Lean source,
   truncated pages, missing SHA or more than the explicit 150 Lean / 500 total
   file limits. These are obstruction states, **not** "no errors".
3. Recheck the exact HEAD and base before emitting the manifest.
4. Find the newest Governance workflow run only for **that exact source
   HEAD**. If it or its Strict Lean job is incomplete, keep `NO_DATA`.
   Never substitute a previous SHA's successful log or an older completed
   attempt while the newest attempt remains pending.
5. When the exact job is completed, download its real compiler log through
   GitHub's restricted API using `actions: read`. Follow only an HTTPS
   redirect on an approved GitHub Actions or Azure blob host. Never
   forward the GitHub API token to a redirected log-storage URL. Limit
   the log to 10 MB. A log receipt is **not** a theorem certificate.
6. Check out the exact observed HEAD without persisted credentials. The
   merged full-source engine verifies all changed blobs against on-disk
   bytes, snapshots the entire source/import closure and records original
   dependent signatures, known syntax/Lean errors and pinned API questions.
7. Recheck the live PR HEAD **and its base SHA** *after* the source inspection.
   Either change can alter the relevant source-diff scope. If the parent
   or its base changes during analysis, the workflow fails with
   `HEAD_DRIFT_OBSTRUCTION`, preserving source-bound historical evidence
   without claiming it belongs to the current revision.
8. Publish the full evidence as an artifact. No source edits, model
   calls, expensive persistent server, GitHub PR writes or merges are
   performed by this workflow. Only the authorized later bounded MCP
   repair + independent exact-head CI can establish a proof.

## Invocation and authority levels

Workflow: `.github/workflows/lean-mcp-live-parent-head-v2.yml`

On the new workflow's PR, CI runs two steps: a mock API regression unit
test followed by the real parent #3522 source-bound snapshot.

The core operator may also run locally in an isolated Linux environment:

```bash
GITHUB_TOKEN=<secure environment variable> python3 \
  scripts/check_kuuos_lean_mcp_live_pr_v2.py \
  --pr 3522 --include-ci-log \
  --output-dir /tmp/kuuos-current-parent-v2
```

After `actions/checkout` of the resulting `plan.json` HEAD, invoke
`check_kuuos_lean_mcp_fullsource_v1.py` with the generated manifest,
then run `--verify-head` against the original HEAD. An operator should
never paste the API token into committed files, comments, URLs or logs.

- **Observed** GitHub latest HEAD, exact path list and bound run ID.
- **Verified locally** complete file bytes, exact blob SHA and import closure.
- **Inferred** textual syntax causes; classification labels are not Lean
  elaboration proofs.
- **Verified by compiler** only after actual pinned `lake env lean`,
  `lean_goal` and `lean_multi_attempt` calls.
- **Certified by CI** only after independent Strict Lean, axiom audit,
  source/test-merge tree equality and `completed/SUCCESS`.

The KuuOS rights/safety governance boundaries still apply: an observed
preferred tactic does not create a proof or grant authority to modify a
historical theorem, and a locally green theorem cannot be promoted to
global success without the dependent closure and independent CI.

Official Lean references (advisory to syntax interpretation, not substitutes
for the pinned compiler):
- https://lean-lang.org/doc/reference/latest/Tactic-Proofs/Tactic-Reference
- https://leanprover.github.io/theorem_proving_in_lean4/Tactics/
- https://github.com/leanprover-community/mathlib4/tree/5450b53e5ddc75d46418fabb605edbf36bd0beb6
