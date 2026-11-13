# KuuOS: bounded Lean MCP → repair candidate → Lean zero-errors → GitHub CI

Status: **implementation + offline tests; real Lean MCP and fixture loop validation require new CI.**

This is an additive source-level connector between the pre-existing KuuOS CodeAI
repair-cycle governance and the already verified `lean-lsp-mcp==0.30.0` local
semantic tools. It does **not** supersede existing KuuOS CodeAI admission,
independent proof certification, or protected pull-request policies.

## Loop and exact scope

1. In a throwaway/isolated Codespace checkout of a selected exact GitHub HEAD,
   verify `lean-toolchain=leanprover/lean4:v4.30.0-rc2` and the pinned mathlib SHA
   `5450b53e5ddc75d46418fabb605edbf36bd0beb6`.
2. Verify expected **SHA256 of the entire selected Lean file**, not merely a
   line number from a previous CI log; reject stale/changed files.
3. Start the pinned Lean MCP; obtain **complete, typed, nonpartial** diagnostics
   from `lean_diagnostic_messages`. Read the full file plus its imports in the
   model request; query `lean_goal` and several `lean_multi_attempt` tactics at
   the first observed error line.
4. If errors remain, ask an explicitly selected provider for one **exact old
   span/new span** of an existing `:= by` proof. Require the expected source
   hash, unique match, unchanged declarations/imports, and no new
   `sorry`/`admit`/`axiom`/`unsafe` or trust bypass. Replace only the temporary
   local worktree source, reobserve the new bytes through MCP, and repeat with
   a bounded budget (default 3, max 5).
5. Only if MCP has a *typed* `success=true`, `partial=false`, empty error list,
   no dependency failures, and **independent** `lake env lean` returns zero does
   it export `candidate.lean` to a directory **outside** the checkout.
6. Always restore the original source bytes and file mode; never use `git` or
   `gh` CLI, modify GitHub, merge PRs, or claim that a patch applied in a
   transient process is already committed. Record a local receipt containing
   source/candidate SHA256, bounded rounds, failures and obstruction states.
7. The GitHub MCP caller independently reviews the candidate's entire content,
   original/changed Lean proof statements and diff, reconciles HEAD, commits
   **only the authorized changes**, and then waits for exact-source **Strict
   Lean** + three-standard-axiom audit + sorryAx absence + completed workflow,
   matching source and test-merge Git trees. An unverified CI means **not
   certified**, even when local Lean has zero errors.

**Not implemented:** general automatic GitHub posting; a multi-file repair
scheduler; full project/global Strict Lean success; a live connection from the
user's ChatGPT account to Codespaces. In particular, this loop's success is not
proof of all 77+ parent PR files compiling or the mass-gap research theorem.

## Free zero-API-cost regression

The separate `real-mcp-fixture` GitHub Actions job generates a temporary
broken Lean theorem *outside the public KuuOSFormal roots*, confirms Lean
rejects the original, invokes the real MCP, applies a deterministic `skip` →
`norm_num` provider patch, gets zero diagnostics, independently compiles, and
verifies original bytes were restored and no GitHub write occurred.

The `contract-unit` job tests rejection of `sorry`, statement edits, stale
SHA, ambiguous edits, partial/MCP NO_DATA and wrong export locations. These
checks exercise the real loop control structure, not a claimed model success.

This is a **closed repair loop for the fixed test fixture**, not evidence that
AI automatically found a solution for an arbitrary Lean theorem.

## On-demand AI provider — separate billable authorization

Run in the opt-in Codespace with the fixed exact **local** source bytes:

```bash
export PYTHONPATH=.
# Enter the key securely through the Codespace secret manager; never commit it.
# Set OPENAI_API_KEY in the process environment (not inside a tracked file).
export SOURCE_SHA256='<sha256 of the complete exact local Lean file>'
export OUTDIR="$(mktemp -d -t kuuos-repair-XXXXXX)"
python3 scripts/kuuos_lean_mcp_repair_loop_v1.py \
  --project-root . \
  --file formal/KUOS/REPLACE_WITH_REAL_EXISTING_MODULE.lean \
  --source-sha256 "$SOURCE_SHA256" --output-dir "$OUTDIR" \
  --provider openai --model YOUR_AUTHORIZED_API_MODEL \
  --paid-api-opt-in --max-iterations 3
```

The standard-library Responses API adapter sends the full file and the latest
Lean MCP observations to the explicitly selected model. It never runs without
both `--paid-api-opt-in` and `OPENAI_API_KEY`; the API can incur model charges
**separately** from any free GitHub Codespaces quota. `--provider fixture` is
strictly limited to `tests/mcp_repair_fixture/` and makes no model/API calls.

When no paid model is configured, the fixture can be tested without a model
fee. Arbitrary Lean proof repair is **not** fully free simply because the
Codespaces machine fits a GitHub Free quota.

## Independent approval and safety

A local receipt with `LOCAL_LEAN_GREEN_CANDIDATE_ONLY` means exactly that:
local diagnostics and direct Lean succeeded for an isolated candidate. It has
`independent_ci_success=false`. Never promote this to a green Strict Lean PR.

A diagnostic `partial=true`, lost connection, malformed success flags, failed
imports, compiler timeouts, or exhausted attempt budget remain explicit
obstructions. No background work or guaranteed eventual success is claimed.

Lean tactics and imported initializers can perform OS-level I/O; MCP
`readOnly` annotations are not an OS sandbox. Run on an isolated unprivileged
Codespace with least-privilege credentials. Candidate text comes from an
untrusted model, not theorem authority. All existing theorem, source,
protection, root, and toolchain authority remains at the canonical GitHub
repository and the independently checked Lean kernel.

**Future integration:** wire this narrowly verified loop to the existing
`runtime/kuuos_codeai_admission_gated_bounded_repair_cycle_execution_v0_1.py`
provider/admission policy and to the GitHub MCP commit + CI receipt path,
without weakening either existing authority requirement.

## Free Lean-MCP tactic candidate mode

The additional --provider mcp-tactic mode performs **no API request**. For a
single concrete error location it locates a nearby tactic line, reads the
actual lean_multi_attempt responses for assumption/simp/aesop, and selects a
candidate only when its reported goals and errors are both empty. It still
requires fresh whole-file MCP diagnostics and exact lake env lean compilation
after the patch, with original source bytes and file mode restored.

This is **narrow proof automation**, not a general proof-synthesis model.
If Lean MCP cannot establish a candidate or the independent compiler fails,
it leaves an explicit obstruction. No fee or model key is required.

Example, for a known local source with an error in the selected proof:

    PYTHONPATH=. python3 scripts/kuuos_lean_mcp_repair_loop_v1.py \
      --project-root . --file tests/mcp_repair_fixture/Repair.lean \
      --source-sha256 "$SOURCE_SHA256" --output-dir "$OUTDIR" \
      --provider mcp-tactic --max-iterations 2

The real MCP CI tests both the deterministic fixture provider and the free
MCP tactic-search provider against an untracked deliberately failing Lean
example. All candidate files remain outside the GitHub checkout; no commit,
PR mutation or full CI theorem authority is inferred from local success.
