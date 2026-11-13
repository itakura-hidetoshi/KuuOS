# KuuOS: 全文・依存署名・固定mathlib APIを伴うLean MCP修復規約 v1

**Authority:** itakura-hidetoshi/KuuOS canonical `main` and the *current* target PR HEAD, then its complete Lean source and imports, then pinned Lean4/mathlib kernel results; this document and model hypotheses are not theorem authority.

**Environment:** `leanprover/lean4:v4.30.0-rc2`, mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`. Existing 107 public roots, source statements, axiom guards, `sorryAx` restrictions, and independent source/test-merge tree evidence are unchanged. `#1558` stays Draft/OPEN/unmerged. Actions on a parent PR must not mutate its child branch as a side effect.

## The actionable closed loop

1. **Observe** GitHub MCP `get_pr_info`, `list_pr_changed_filenames` and `fetch_file` at **one exact HEAD**. Materialize the **entire contents** of *every* changed Lean source in an isolated checkout. Build a manifest of `{path, git_blob_sha}` for each. An exhaustive claim requires `scope=all-changed` and `changed_lean_files` equal to the target set. In a scoped experiment, write `scope=scoped`; never call it full coverage.
2. **Pin and read everything** using `scripts/check_kuuos_lean_mcp_fullsource_v1.py`: verify the exact Git blob of every target and pinned Lake manifest, snapshot all files under `full_sources/`, read the full transitive local import closure up to a declared budget, extract declaration **headings, entire signature lines and hashes**, and record imported names actually *lexically* referenced. A truncated closure is an **obstruction**. No patch is written to source.
3. **Cross-check** CI errors with the source snapshot and the declaration containing the diagnostic. Error `line:column` is *not* the authorized replacement position; prove the actual tactic position with Lean MCP `lean_goal`. Capture detailed `pp.explicit`, hidden instance/cast/universe information as needed. Record source line ranges and local dependent signatures **before** proposing edits.
4. **Pin the API**, do not guess from online examples. Search the *installed* mathlib at the exact manifest revision; for doubtful names, run explicit scratch `#check Full.Name` with the precise `import` through `lake env lean`. `--probe-pinned-api` writes a compiler receipt and rejects absent symbols. Public web documentation is a supplementary explanation of how `rw`, `simp`, elaboration, and named arguments work; an unpinned website cannot override the pinned source.
5. **Classify structural causes**: namespace/missing API; dependent casts or normalized rewrite target; hidden implicit scaling/class instance; universe leakage; unsolved goals whose diagnostic precedes the actual incomplete tactic; or timeout. Keep multiple hypotheses where needed. `causal_casebook.jsonl` is append-only observational feedback; a previous accepted tactic is a *candidate*, not a new axiom or guaranteed repair. `--previous-casebook` only reuses history for the *same entire source SHA256*, and still labels it unverified.
6. **Attempt in isolation**: use the integrated `scripts/kuuos_lean_mcp_repair_loop_v1.py` and, when dependencies require it, `scripts/kuuos_lean_mcp_multifile_cycle_v1.py`. First `lean_diagnostic_messages` → `lean_goal` → `lean_multi_attempt`; then apply one bounded proof-only candidate in a disposable checkout, re-read the **entire modified source**, verify unchanged theorem signatures/imports and actual dependency `.olean` chain; run direct pinned Lean. Never auto-push a candidate that has NO_DATA, incomplete diagnostics, modified theorem statement, or unverified new axioms. For a difficult proof, candidate generation may involve an AI agent, but the AI is not the verifier.
7. **Gluing check:** locally successful files do not imply successful project-wide compilation. Read imported dependent signatures and any affected public roots; recompile the staged *whole dependency closure* in the same isolated workspace. If one file fails, keep the obstruction and restore baseline source/build artifacts. Preserve the exact failed candidate, goal, compiler log and experimental outcome **outside** the repo.
8. **Authority check:** only after local candidate is source-bound and Lean-clean, use GitHub MCP to create a proof-only commit on the authorized PR branch. Review and enroll its exact Git blob in existing source provenance tests **after** Lean success; never weaken the gate. Let independent exact-HEAD Strict Lean run with `-DwarningAsError=true` and `-DsorryAsError=true`, followed by `#print axioms`, warning/error audit, and source/test-merge Git tree equality. `completed/SUCCESS` must be observed, not assumed.
9. **Learn from feedback:** append a casebook record with prior diagnostic SHA, candidate text hash, what failed/succeeded, pinned compiler result, CI run/attempt, source and test-merge tree status. On a later HEAD recompute the snapshot and *re-evaluate* the hypothesis; old success is never promoted to the new HEAD automatically.
10. **Report** four independent statuses: (i) complete source observed; (ii) pinned API verified; (iii) local proof repair accepted; (iv) independent CI/formal validation certified. A failed or unrun stage stays `NO_DATA` or `OBSTRUCTION`.

## Command: create and inspect an exact-source evidence report

Generate a plan from **GitHub MCP** using `get_pr_info` and every `fetch_file` at the same PR HEAD. Example shape (replace the sample SHA/path with real current values):

```json
{
  "schema_version": "kuuos-lean-fullsource-v1",
  "source_head": "0123456789abcdef0123456789abcdef01234567",
  "scope": "scoped",
  "targets": [
    {
      "path": "formal/KUOS/Example.lean",
      "git_blob_sha": "0123456789abcdef0123456789abcdef01234567"
    }
  ],
  "api_probes": [
    {"name": "Nat.add_comm", "import_module": "Mathlib"}
  ]
}
```

The sample hashes above are **placeholders, not verified KuuOS refs**. The plan is rejected unless the actual source blobs match. On the checked-out exact HEAD:

```bash
python3 scripts/check_kuuos_lean_mcp_fullsource_v1.py \
  --project-root . \
  --plan /tmp/kuuos-exact-head-plan.json \
  --ci-log /tmp/kuuos-strict-lean-actual.log \
  --output-dir /tmp/kuuos-fullsource-evidence \
  --max-local-deps 1200 \
  --probe-pinned-api
```

Outputs are outside the repository: `full_source_evidence.json`, full raw source snapshots under `full_sources/formal/...`, and `causal_casebook.jsonl`. The casebook is observational; the script does *not* edit proofs or invoke an LLM. API probes are executed only with `--probe-pinned-api`. The `source_head` in an input plan is **asserted**, while the per-file blobs are cryptographically verified; a live GitHub ref and source/test-merge tree check remain separate required receipts.

## Current concrete structural lessons (CI observations, not theorems)

| CI observation | Hypothesis and required experiment | Status |
|---|---|---|
| v1.66: `simpa only [hindex, hmap]` expected casted map, actual core map | Rewrite the existing proof with the typed map equality before simplifying; recheck the entire source and affected import closure | Source proof advanced past v1.66 in earlier CI, but a later HEAD requires rechecking |
| v1.67: `SSet.stdSimplex.σ_apply` invalid field on the fixed package | Local evaluation lemma / exact pinned `.σ` API probe, then check `Fin.predAbove/succAbove` normalization | Partial repair; do not mark all v1.67 complete |
| v1.67: `scaling_eq_of_le_antisymm` unresolved | Locate theorem in its actual imported `V1_53` namespace and use the fully qualified constant; `#check` signature | Source-level candidate, must recheck at current HEAD |
| v1.67: `rw [hmax]` target already shows `ScaledSimplicialSet.thin t` | Hidden instance makes syntactic rewrite miss the target; test typed proposition equality via `congrArg` at correct universe | Trial with independent `{u}` led to universe mismatch; never blindly reuse |
| v1.67: proof with `congrArg` introduces `u/u_1` level mismatch | Let the compiler infer the universe from the actual source term; verify the complete declaration and all used signatures | Historical error observation, not an unconditional correction |
| any Lean timeout `124` | Inspect cache and last successfully compiled module; retry exact source with trusted cache, never treat timeout as theorem contradiction | Resource obstruction |

## Online sources and authority boundary

Official Lean language and tactic manuals explain tactics and elaboration; they are *not* pinned KuuOS theorem signatures:
- https://lean-lang.org/doc/reference/latest/Tactic-Proofs/Tactic-Reference
- https://leanprover.github.io/theorem_proving_in_lean4/Tactics/
- https://lean-lang.org/doc/reference/latest/
- Pinned mathlib code: https://github.com/leanprover-community/mathlib4/tree/5450b53e5ddc75d46418fabb605edbf36bd0beb6

The decisive evidence for any specific API is a `#check` or actual Lean/MCP tool call against the pinned local dependency closure, and the decisive proof evidence is independent exact-source CI. Form/empty-dependent-origination mapping is interpretive naming, not established by these Lean technical checks.

## Mandatory preflight entrypoint before a bounded Lean MCP repair

The integrated single-file bounded MCP repair engine is no longer called
directly by an agent that claims to have read the full source: the recommended
authorized entrypoint is now `scripts/check_kuuos_lean_mcp_fullsource_repair_v1.py`.

```bash
python3 scripts/check_kuuos_lean_mcp_fullsource_repair_v1.py \
  --project-root . \
  --plan /tmp/kuuos-exact-head-plan.json \
  --ci-log /tmp/kuuos-strict-lean-actual.log \
  --repair-target formal/KUOS/NamedTheorem.lean \
  --output-dir /tmp/kuuos-isolated-repair
```

Without the additional `--ack-isolated-checkout`, this performs **read-only
full-source preflight** and never calls a repair provider. For an explicitly
disposable checkout only, add that acknowledgment and the engine calls the
previously independently tested free `mcp-tactic` provider. The full-source
gate checks the exact blob on **all** manifest targets and their local import
closure before attempting repair; if an unknown identifier/field is in the
exact CI log, explicit pinned API probes must be supplied in the plan before
repair begins. API probes are executed in pinned Lean when repair is approved.

After local repair, the entrypoint checks that the original source has been
restored, the full candidate still has exactly the same imports and lexical
declaration signatures, and no new trust-bypassing constructs appear. Any
failure is `PROOF_INTERFACE_OBSTRUCTION`, never a green candidate.
A local success returns `LOCAL_FULLSOURCE_AND_LEAN_GREEN_CANDIDATE_ONLY`,
**not** `ci_certified`. GitHub MCP commit authority, independent exact-source
Strict Lean, `#print axioms`, warnings and test-merge tree receipts remain
separate required subsequent stages.

For multi-file repairs first gather a plan covering **every changed Lean
file**, then run the existing dependency-ordered
`kuuos_lean_mcp_multifile_cycle_v1.py` on a bounded, source-bound subset.
Do not pretend the four-file loop repairs all 91+ changed Lean modules merely
because their entire sources were observed.
