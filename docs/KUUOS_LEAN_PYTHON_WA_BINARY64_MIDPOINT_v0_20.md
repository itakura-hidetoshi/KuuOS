# KuuOS Lean→Python v0.20 — local binary64 midpoint observations

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Canonical source and fixed scope

Baseline canonical main \`73bba9d114c8f4fcdfe636ba46360f9e18b9977e\`;
Lean v4.30.0-rc2; pinned mathlib
\`5450b53e5ddc75d46418fabb605edbf36bd0beb6\`.
Existing 0.19 rational bridge, Wa/DecisionOS kernel, native store and CI workflows
are not changed. All new files are additive, append-only / same-root.

This v0.20 extension has TWO deliberately different mathematical models:

1. **Constructive unbounded uniform rational grid.**
   \`gridRound(x,q) = q * floor(x/q + 1/2)\` for \`q>0\`.
   Lean proves exact half-quantum error for grid rounding, for addition and
   multiplication using that model, its two-operation Wa propagation and
   conditional cast to the existing Lean Wa real score. Grid ties use
   half-up, NOT binary64 ties-to-even.

2. **Exact midpoint certificate for observed Python steps.**
   For finite native result \`z\`, its finite adjacent values \`p<n\`,
   and exact rationals \`x,z,p,n\` from \`as_integer_ratio\`, check

   \`(p+z)/2 <= x <= (z+n)/2\` and
   \`q = max(z-p, n-z)\`.

   Lean proves that these inequalities imply \`|z-x| <= q/2\`.
   It composes two independently verified Wa step bounds and transports
   the resulting conditional score bound to the v0.19 real formula.
   No claim is made that Python always satisfies the inequalities.

## Original native Wa path and Python checks

The optional pure v0.20 adapter reuses the original v0.18 → v0.19 checked
path, preserving actual native state, receipts, digests and store writes.

For the original seven positive axes, both interval endpoints and the seven
alert axes, it recomputes the original arithmetic without modifying the
native code. Every explicit float multiply, subtraction and addition in
the pure observational trace is checked against exact rational neighbor
midpoint bounds via \`math.nextafter\` and \`Fraction\`.

The original Python built-in \`sum()\` for each weighted endpoint is
replayed as \`sum(products)\`, **not** replaced by a naive seven-step addition.
Its exact rational discrepancy is retained as an observed quantity; its
internal Python float implementation is NOT proved or modeled. Min/max
and the upper-end clipping are copied as original selection operations,
not labeled as rounded additions.

All eleven stored original native score fields are checked against
the replayed float results by exact \`as_integer_ratio\` equality. The
existing v0.19 rational ideal error budget \`2^-40\` remains independently
mandatory; passing it is NOT a global error theorem.

The local midpoint audit fails closed for missing/malformed inputs,
nonfinite results, unavailable finite neighbors, out-of-midpoint results,
or any stored-score mismatch. Local observations include explicit
\`builtin_sum_semantics_proved=false\` and
\`ieee754_global_semantics_proved=false\`.

## Precise certification boundary

- A new Lean theorem is only certified after the exact-head pinned Lean build
  and real axiom log. Ordinary Python assertions do not certify Lean.
- A local midpoint receipt is a checked implication on the selected operands,
  NOT IEEE-754 machine semantics or Python interpreter refinement.
- Python \`sum()\` arithmetic, weight normalization tolerance, arbitrary
  machine rounding-mode/overflow/underflow behavior, subnormal transitions,
  signed zero and complete operational semantics remain outside the theorem.
- Finite selected ledger replay is not global history completeness,
  external issuer authenticity or host/store atomicity.
- No action, execution, consent, moral authority, truth authority or
  history overwrite is granted by source/CI success.
- Protected Draft/Open PR #1558 is outside this extension.

Do not merge until every final PR-head changed Lean source has an actual
Strict Lean success with \`sorryAsError\`, 0 errors/warnings, standard axiom
audit, successful ordinary Python IDs, all Governance jobs, and exact
PR source/test merge tree evidence. Post-merge main Runtime and Full Lean
checks are separate independent certification events.
