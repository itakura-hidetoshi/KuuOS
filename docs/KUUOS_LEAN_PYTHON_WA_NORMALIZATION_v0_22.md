# KuuOS Lean→Python v0.22 — represented-rational native Wa weight tolerance

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Canonical context

Predecessor: canonical \`main\` \`9304e28e8f8391f49a7989f3f04a84ed56231ef6\`
(v0.21 MERGED). Lean \`v4.30.0-rc2\`; pinned mathlib
\`5450b53e5ddc75d46418fabb605edbf36bd0beb6\`.
No prior Lean proof, source file, native Wa score, event, store, receipt, digest,
CI workflow, toolchain or public library root is modified.
No alteration of protected PR #1558.

## What the original native code actually accepts

Original \`runtime/kuuos_decision_os_wa_types_v0_3.py\` parses
seven nonnegative weights, each at most one, and tests the float result

\`\`\`python
total = sum(weights.values())
if abs(total - 1.0) > 1e-9:
    raise ValueError("wa_weights_must_sum_to_one")
\`\`\`

Neither \`total\` nor \`abs(total-1.0)\` is the corresponding exact
rational expression in general. Passing this Python comparison is
*not* proof that the exact represented weights sum to one, or proof
that they satisfy a rational or Real total-weight bound by 1e-9.

## Mathematical quantities and the proof hypothesis

For represented exact rational weights \`w_i\` and endpoints
\`x_i\` within [0,1], define

\[
  T=\sum_{i=1}^{7} w_i,\qquad
  W=\sum_{i=1}^{7} w_i x_i,\qquad
  N=W/T \quad (T>0).
\]

Lean proves for arbitrary finite index sets with explicitly
nonnegative \`w_i\`, bounded \`x_i\`, and \`T>0\`:

\[
  0\le W\le T,\qquad 0\le N\le 1,\qquad
  |W-N|\le |T-1|.
\]

Let \`S_w\` be the observed native Python float sum, interpreted
as a represented exact rational number, and \`S_W\` the
observed native weighted score. Define independently verified
rational bounds

\[
 |S_w-1|\le \tau,\qquad
 |S_w-T|\le \varepsilon_{\rm sum},\qquad
 |S_W-W|\le \varepsilon_W.
\]

Then Lean proves the **conditional implication**

\[
 \boxed{|S_W-N|\le \varepsilon_W+\tau+\varepsilon_{\rm sum}.}
\]

The same conditional rational bound is transported into Lean Reals.

The mathematical normalization \`N\` and the exact normalized
rational weights \`w_i/T\` are **comparison witnesses**, not a
modification or correction of native Wa data.

## Exact source observations

The optional additive Python checker:

1. Reads the original seven positive-axis weights, validates exact
   axis names/types and [0,1] values, preserves the native ordering.
2. Computes the original \`sum(weights.values())\` over converted
   floats and records its \`as_integer_ratio()\` result.
3. Computes \`T\` by exact \`Fraction\` addition of those represented
   float values, separately records \`|S_w-T|\`.
4. Replays the original native comparison with \`1e-9\` and **also**
   checks \`|S_w-1|\le\tau\` as an exact rational certificate, using
   \`Fraction(*(1e-9).as_integer_ratio())\` for \`tau\`. An observation
   passing only the native floating-point comparison can still be
   BLOCKED by the stronger exact rational certificate.
5. Requires \`T>0\` and constructs exact normalized rational weights
   with sum one.
6. Runs the existing v0.21 native-Wa audit, including v0.20 step
   midpoint checks and v0.19 strict source data checks. For both lower
   and upper original weighted intervals, compares its already
   certified \`W\`, \`S_W\`, and \`epsilon_W\` to the new normalized
   rational witness and verifies the derived inequality.
7. Leaves native score, original weights, ledger, receipt, digest,
   action authority and caller-owned state entirely unchanged.

No new native store schema or historic event is introduced.

## Non-proved and fail-closed boundaries

- The exact native \`1e-9\` Python literal is a *represented binary64
  number* used as a declared exact rational comparison threshold.
  The v0.22 checker imposes its explicit extra rational check; it does
  not infer that from a machine-comparison theorem.
- No theorem formalizes arbitrary CPython built-in \`sum()\`,
  IEEE-754 operations/rounding, compensated algorithms, subnormal
  transitions, signed zero, overflow, underflow, or Python interpreter.
- No theorem states original weights sum to exactly one: an exact
  normalized comparison vector is constructed only when \`T>0\`.
- A mathematical normalized vector is not automatically the
  original Lean \`UnitInterval\` or \`ConvexWeight\` witness until
  all type and interval compatibility conditions are separately
  certified; there is no forged type coercion.
- Successful selected local measurements do not prove general
  Lean↔Python refinement, global history completeness, external
  issuer signature, host/store atomicity or right to execute.

Independent certification requires exact-head pinned Strict Lean
with \`warningAsError\` and \`sorryAsError\`, actual axiom audit
of all newly added theorems, ordinary Python Regression IDs and
source-byte preservation, final PR Governance terminal SUCCESS,
source/test-merge tree identity, and separate exact postmerge main
CI. Older green heads never certify a changed head. The v0.21
full-root main CI remains independent.
