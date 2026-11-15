# KuuOS MemoryOS × CodeAI — Lean4 repair learning v0.1

## Authority and evidence

MemoryOS stores observations and pointers, never mathematical truth or execution
authority. This module connects existing CodeAI Version-Bound Repair Memory
and Subtask-Level Version-Bound Memory with pinned Lean compiler and real MCP
evidence. The layers are deliberately different:

1. **L0 observed:** immutable GitHub workflow run, source HEAD/tree, candidate
   Git blob, pinned Lean and mathlib, raw log SHA. Complete logs remain in
   Actions artifacts. Never commit secrets or large raw compiler logs.
2. **L1 classified:** typed diagnostic family plus short redacted error;
   classification and causal interpretations remain hypotheses.
3. **L2 MemoryOS:** append-only, content-addressed, hash-chained JSONL with
   immutable case IDs, provenance, and authority external_pointer_only.
   The curated 9 observations in this repository are at
   memoryos/external/github/2026/11/kuuos_codeai_lean_observations_v1.json.
4. **L3 pre-generation recall:** match exact HEAD + tree + imported source
   blob + pinned Lean/mathlib + candidate blob. Exact duplicates of recorded
   direct Lean failures are quarantined before CodeAI. Cases from a different
   HEAD are analogy-only prompts, not mandatory edits or a rejection authority.
5. **Post-run evidence:** only after GitHub producer CI is completed/SUCCESS,
   normalize portfolio/MCP receipts into append-only MemoryOS journal, and
   upload it as an Actions artifact. No contents write permission, automatic
   Git change, or automatic theorem promotion.
6. **Independent certification:** separate exact-source Strict Lean completed
   CI is necessary for a formal proof claim; memory cannot upgrade a direct
   Lean or MCP success into independent certification.

## Concrete failed and successful history

v1.104: invalid-field strictLabel and timeouts in initial candidate; corrected
local label passed fixed Lean, real Lean MCP and separate independent CI.
An extra omega generated a tactic-does-nothing failure.

v1.105: universe mismatch and dependent-by-decide errors; explicit SSet.{0}
and Nat.le_refl 4 alternatives passed fixed Lean and real MCP. Independent
certification pointer: CI #43688610764.

v1.106: current Fin 5 case split has unresolved-goal, redundant-simp,
and non-progressing omega variants. GitHub producer #43690405377 gives real
counterexamples; for impossible ordered triples such as 0<0 or 4<4, the
hypothesis must be reduced before case splitting. That explanation is a
testable repair HYPOTHESIS, not a proven mathematical or compiler fact.

## Implementation

- runtime/kuuos_codeai_lean_failure_memoryos_v0_1.py:
  diagnosis taxonomy, provenance, hash-chain, exact replay filtering
- runtime/kuuos_codeai_lean_observation_intake_v0_1.py:
  curated GitHub pointer-only observations
- scripts/kuuos_codeai_lean_memoryos_sidecar_v1.py:
  read-only preflight and append-only evidence intake after producer run
- scripts/kuuos_v1106_codeai_memoryos_routed_v1.py:
  MemoryOS prior-hint retrieval before CodeAI proposals; then original
  direct pinned Lean and real Lean MCP on direct-green candidates only
- .github/workflows/kuuos-codeai-lean-memoryos-tests-v1.yml:
  deterministic invariants / tamper / replay / stale exclusion tests
- .github/workflows/kuuos-v1106-codeai-memoryos-round4-v1.yml:
  actual round4 CodeAI, direct pinned Lean and real Lean MCP
- .github/workflows/kuuos-codeai-lean-memoryos-intake-v1.yml:
  completion-gated, read-only post-run memory ingestion

## Prohibitions

No sorry, new Lean axiom, theorem weakening, fixed mathlib drift,
historical-success-as-proof, same-error cross-context automatic rejection,
Git write by MemoryOS, destructive overwrite, secret exfiltration, or
unverified CI claim. NO_DATA is preserved, not filled with guesses.
Preference does not imply descent; descent does not grant authority.
