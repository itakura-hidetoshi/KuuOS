# KuuOS Lean→Python v0.21 — certified finite weighted-sum error

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Fixed canonical source / non-authority

Baseline: \`itakura-hidetoshi/KuuOS\`, canonical main
\`3cad1cb96210ce88e9b7f1921c8dc7b9df198350\` (v0.20).
Lean v4.30.0-rc2 / mathlib
\`5450b53e5ddc75d46418fabb605edbf36bd0beb6\`.
Append-only, tighten-only, overwrite-forbidden, same-root.
No original Wa kernel, Python evaluator, ledger, receipt, digest, Lake
manifest, dependency pin, shared CI workflow or protected PR is modified.

## Mathematical proof scope

The v0.20 midpoint lemma establishes, under actual rational midpoint
certificates, a per-product error bound

\[
  |\widehat p_i - p_i| \le q_i / 2 .
\]

The new v0.21 Lean model uses a finite list of typed
\`CertifiedProduct\` values with each inequality explicitly present.
For the exact sum of represented input products
\`W = sum_i p_i\` and the exact rational sum of the individually
observed rounded products \`P = sum_i \widehat p_i\`, it proves

\[
  |P-W| \le \sum_i q_i/2 .
\]

The actual original Python \`sum()\` output \`S\` is a third, separate
observed rational value. The checker *measures*, rather than assumes,
the exact rational difference

\[
  \varepsilon_\mathrm{builtin}
   = |S-P|.
\]

The final certified implication is

\[
  \boxed{|S-W| \le
    \varepsilon_\mathrm{builtin} + \sum_i q_i/2} .
\]

The resulting rational error bound is also transported into Lean Reals.
The general finite-sum proof applies to arbitrary lengths of *supplied
certified lists*; the original native Wa model has exactly 7 positive
axes for the lower and upper weighted interval endpoints.

## Source binding / native observation

The additive Python checker calls the existing v0.20 independent
native trace, checks each product certificate from exact rational
\`float.as_integer_ratio\` pairs (including midpoint, gap and
signed-error consistency), then composes seven product error
certificates and the separate original \`sum(products)\` observation
at each endpoint. It compares the ideal rational weighted sum with
the unchanged v0.19 \`Fraction\` shadow and reproduces v0.20's
all-11-native-score and previous local-stored-receipt checks.

The optional read-only event adapter preserves the exact v0.20
native-state transition outcome while applying pre/post audits; it
does not write new stores, repair or reseal historical data.

The checker rejects missing or invalid data, changed exact rational
pairs, artificial sum and midpoint certificates, changed native
scores, or any attempt to label \`sum\` semantics formally proven.

## Obstructions and certification

- The Lean theorem proves the *conditional mathematical sum bound*;
  it does not certify arbitrary Python \`sum()\` implementation.
- The Python test validates a finite observation on selected native
  fixtures, not complete CPython or IEEE-754 operational semantics.
- There is no universal all-input error bound, rounding-mode,
  tie-to-even, signed-zero, overflow, underflow or subnormal theorem.
- Python weight-normalization tolerance is not converted into
  Lean's exact convex-weight assumption.
- Proven finite arithmetic does not confer issuer authenticity,
  global historical completeness, host/store atomicity,
  clinical authority, action rights, or a general Lean→Python
  refinement theorem.
- Original v0.19/v0.20 predecessor source-byte pins remain mandatory.
  Existing Full Lean main validation is independent of the PR checks.

PR merge requires exact full-source Lean compiler success with
warnings and \`sorry\` as errors, exact eight-or-new theorem axiom
audits (standard axioms only), ordinary Python Runtime success,
source/test-merge tree identity, terminal Governance SUCCESS,
and independent postmerge main CI. Never claim success from only
static source checks or from a prior HEAD.
