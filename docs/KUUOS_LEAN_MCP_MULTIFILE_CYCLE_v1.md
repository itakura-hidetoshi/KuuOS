# KuuOS Lean MCP multi-file bounded repair cycle v1

## Status, scope and authority

This is an append-only extension of the single-file Lean MCP repair loop in
PR #3535. It does not introduce a new theorem statement or alter pinned Lean
or mathlib. The two-module test is deliberately outside all 107 published
roots. Local acceptance is **not** theorem certification.

GitHub source and proof authority stay separate from the ephemeral Lean MCP
worktree. Sources are unchanged after every run; generated candidates are
exported separately and are never automatically pushed or merged.

## Control sequence

1. Admit an ordered manifest (2 to 4 source modules), each bound to exact
   SHA256, module name, explicit direct dependency list, and 40-hex source HEAD.
2. Validate every path, SHA, module/path identity and direct import relation
   before modifying any file.
3. On a disposable checked-out workspace, invoke the existing single-file
   `run_loop` for the first target using `lean_diagnostic_messages`,
   `lean_goal` and `lean_multi_attempt`. Default provider:
   `mcp-tactic`; no paid model API required.
4. Accept only `LOCAL_LEAN_GREEN_CANDIDATE_ONLY`, exact source restoration,
   and a read-back candidate. Re-apply that candidate locally and compile it
   into a temporary worktree `.olean` for dependent modules.
5. Proceed in declared topological order. Stop on partial diagnostics,
   malformed responses, failed imports, invalid candidates or resource budget.
6. Recompile all the staged files in order with the entire candidate stack.
7. Export only the complete candidate set; unconditionally restore all
   original source bytes/modes and original or absent `.olean` artifacts.
8. In a separate GitHub Actions runner, check the exported candidate SHA,
   build both modules afresh with pinned Lean and inspect `#print axioms`.

A successful local result is
`LOCAL_MULTIFILE_LEAN_GREEN_CANDIDATES_ONLY`.
It never means the current parent PR #3522 or validation child #3530 is
globally green. The independent runner's receipt is also scoped to the exact
test-source tree. Full project Strict Lean and its public import/axiom audits
are distinct final gates for any actual proposed research edit.

## Safety limits

- Strict opt-in `--ack-isolated-worktree`. Never run on a non-disposable
  checkout; Lean tactics and imported initializers can perform OS I/O.
- Only `formal/KUOS/` and `tests/mcp_repair_fixture/` paths; no symlinks,
  no traversal, no hidden dependency-cache paths.
- Module names must be consistent with physical paths. Explicit prior
  dependencies must also appear in `import` statements.
- At most four source files and five repair iterations per file.
- Proof-only patch policy from the already tested single-file loop is reused.
  No `sorry`, `axiom`, `unsafe`, or trust-bypassing constructs can be
  introduced through the candidate generator.
- Exports must lie outside the source checkout. No `git` / `gh` commands,
  GitHub writes, commits, PR merges or private model API calls.
- A source or `.olean` rollback failure yields
  `ROLLBACK_OBSTRUCTION`, not a promotable success state.

## Evidence and known limitations

The initial live CI exercises two *synthetic but real Lean* modules:

`RepairMulti.Alpha` -> `RepairMulti.Beta`.

Both initially contain an unclosed `True` proof. The existing free
MCP tactic provider uses actual Lean goal state to select a tactic, then
rechecks and directly compiles the candidate. The dependent `.olean`
handoff tests the intermediate import boundary. A fresh CI runner then
compiles the exported pair and checks both axioms independently.

A production-ready agent that edits arbitrary complex Lean proofs without
a paid model or human reasoning is **not** demonstrated here. The current
tactic provider is bounded to `assumption`, `simp`, and `aesop`. More
powerful candidate generation must remain a separate opted-in provider with
the same exact-source validation and verification gates.

Before testing actual parent PR #3522, reobserve its *current* HEAD, all
modified Lean files and dependency signatures. Use source-specific
manifests and new receipts rather than treating this synthetic CI run as
authorization for a production source mutation.
