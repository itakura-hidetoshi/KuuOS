# KuuOS Lean→Python v0.19 — rational shadow and conditional real-score proof

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Baseline, fixed context, original sources

Canonical baseline main: af8b47cc20d35e1a44b25df4917505a90a4a9709
(v0.18, PR #3579). Lean v4.30.0-rc2, pinned mathlib and all original OS
kernels/stores remain unchanged. The new independent formal source is
formal/KuuOSFormal/WaRationalBridgeV0_19.lean, importing the original
formal/KUOS/DecisionOS/WaRelationalHarmonyV0_3.lean.

The original Lean model defines Real-valued UnitInterval, ConvexWeight,
mixedLower, mixedUpper, waLower, waUpper and proves bounds/monotonicity.
Python's original Wa evaluator instead uses binary64 rounded operations,
sum/min/max, mixed score, alert penalty and clipping.

## Formal new theorems, exact mathematical scope

The additive Lean file defines rationalIdeal and realIdeal for the same
mathematical Wa formula, and proves:

- rationalIdeal_cast: rational exact-operation Wa formula casts to its Real
  formula for the same rational operands.
- certified_rational_error_is_real_error: an observed rational inequality
  |observed - ideal| <= budget implies the identical Real inequality.
- two_stage_score_error_bound: error budgets for the relational and output
  arithmetic compose under explicitly required 0 <= alert <= 1 and
  0 <= epsRel, bounding final Real absolute error by epsOut + epsRel.
- binary64_addition_is_not_exact_rational_addition: the exact represented
  Python 0.1, 0.2, 0.1+0.2 ratios exhibit a real rounding obstruction.
- rational_product_matches_original_waLower: if input rational shadows
  match relational.lower and alert.upper of the original Real UnitInterval,
  the rational product casts to the original Wa waLower formula.

These are Lean theorem proofs only when the exact source passes pinned
Lean compilation and the independent CI. Their proofs do NOT establish
a general IEEE-754 semantics theorem, an all-input Python refinement,
external source validity or any right to execute an action.

## Python exact rational finite observation

The new pure runtime/kuuos_lean_python_wa_rational_shadow_v0_19.py uses
Fraction and float.as_integer_ratio to interpret already-stored finite
Python float operands and computed outputs exactly as rational numbers.

For the original seven positive and seven alert axes, it computes exact
rational ideal weighted, weakest, relational, alert, Wa lower, upper with
native clipping at one, and width. It compares *all eleven* stored
native score fields to these exact rational shadows. It accepts a selected
native record only when each exact rational error is at most 1/2**40.
That fixed budget is a declared acceptance condition, NOT a theorem
that all IEEE-754 executions meet the budget.

The output lists exact numerator/denominator error fractions for each
field and its maximum. It does not change, clip, repair or reseal native
scores. Original v0.18 adapter behavior is preserved by the new pure
checked adapter: once after a precondition check, then postcondition
check. Native APPLIED/REPLAYED/REJECTED results remain unchanged.

Selected ordinary runtime tests explicitly build the original
process-isolated v0.18 fixture, recover its real local Wa, Decision,
Plural and Belief stores, and use existing committed Wa event data.
They compare v0.19 pure adapter results against original v0.18 results
on each original Wa event, reobserve final native scores, and check the
exact error fractions. This is NOT always-on all-store-write protection,
concurrent historical guard attestation, or host/store atomicity.

## Source tests and acceptance conditions

The v0.18 checker already pins 111 selected historical Git blobs;
v0.19 pins seven more exact v0.18 source blobs (118 cumulative) and
requires six new files: Lean source, Python pure adapter, source
checker, two ordinary test classes, and this document. Existing
registered test loader, CI, native source files and mathlib pin remain
unchanged.

Require independent PR Strict Lean to build
KuuOSFormal.WaRationalBridgeV0_19 with warnings and sorry as errors.
Axiom audit must distinguish standard axioms from sorryAx.
Require actual new Python test IDs successful, an exact PR source/test
merge Git tree, no skips or duplicates, and independent postmerge
main Runtime and Sharded Governance. Do not merge on AST presence,
CI selection, or a previous HEAD's receipt.

## Explicit obstructions

- No complete Lean model of the CPython interpreter or IEEE-754
  instruction evaluation is supplied here.
- The exact Python float score may fail the selected error budget on
  another input. Then report BLOCKED; never enlarge the budget silently.
- Even a passing source/data checksum does not prove stakeholder truth,
  issuer signature, independent history, external consent, or action
  authority.
- Python's normalization permits a native weight-sum tolerance 1e-9;
  an exact rational convex weight sum or original Lean UnitInterval
  witness cannot be silently assumed.
- Old recorded evidence and protected Draft/Open PR #1558 remain intact.

Interpretive terms such as emptiness or dependent origination do not
constitute extra formal Lean lemmas or transfer authority.
