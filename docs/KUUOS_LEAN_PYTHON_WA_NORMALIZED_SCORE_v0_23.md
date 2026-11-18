# KuuOS Lean→Python v0.23 — original Wa final score versus mathematical normalized comparison

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Source, fixed environment and non-authority

Canonical predecessor \`main\`: \`d0d62b0bf15fda60900532b245f4e1b23b3222cc\` (v0.22).
Pinned Lean \`v4.30.0-rc2\`, mathlib
\`5450b53e5ddc75d46418fabb605edbf36bd0beb6\`.
Append-only, tighten-only, overwrite-forbidden, same-root.
No original KuuOS kernel, native Wa evaluator, persistent stores,
receipt schema, signed digest, Python test registry or shared CI is changed.
No authorization is derived from successful local proof checks.

## Proven formula and explicit hypotheses

The original exact rational Wa endpoint ideal, already defined in v0.19, is

\[
 F_\beta(W,u,a) = ((1-\beta)W+\beta u)(1-a).
\]

For \(\beta,a\in[0,1]\) the proposed v0.23 Lean4 lemma is

\[
 |F_\beta(W,u,a)-F_\beta(N,u,a)|\le |W-N|.
\]

This is a contraction in the weighted-input argument, not a claim about
float arithmetic or about the original native score interval.

For represented-rational positive-axis weights \(w_i\ge0\), endpoint
samples \(0\le x_i\le1\), total \(T=\sum w_i>0\), and exact normalized
comparison \(N=(\sum w_i x_i)/T\), the v0.22 theorem supplies,
**conditionally**, when native weight-sum and raw weighted-score
errors have been separately observed and checked,

\[
 |W_{\rm obs}-N|\le
   \varepsilon_{\rm weighted}
   + \bigl(\tau_{\rm native}+\varepsilon_{\rm weight\ sum}\bigr).
\]

The original observed native Wa scalar \(O\) has a separately
measured error against the original raw-weight ideal,
\(\varepsilon_{\rm Wa}=|O-F_\beta(W_{\rm obs},u,a)|\).
The v0.23 combined result is

\[
 \boxed{
 |O-F_\beta(N,u,a)|
 \le
 \varepsilon_{\rm Wa}+
 \varepsilon_{\rm weighted}+
 \tau_{\rm native}+
 \varepsilon_{\rm weight\ sum}.
 }
\]

Another theorem composes the actual observed relational-stage
and alert-multiplication stage discrepancies. A finite-list theorem
plugs in v0.21's seven independently midpoint-certified weighted
products, with the original list-to-vector sum identity supplied
explicitly. The final rational bound is conditionally transported
into the Real semantics of the original Wa mathematical model.

## Observed native source boundary

The original Wa v0.3 evaluator calculates lower and upper endpoints
with intentionally opposite alert-interval extrema:

- Lower: weighted.lower, weakest.lower, alert.upper, native wa.lower.
- Upper: weighted.upper, weakest.upper, alert.lower, native wa.upper
  (whose original native float may be clipped at one).

The proposed v0.23 Python observer reproduces the existing
\`trace_native_wa_score()\` and checks exact rational arithmetic on
the finite observed float representations. It reuses the original
v0.20 midpoint checks, v0.21 signed weighted-product checks, and
v0.22 strict source-state checks and normalized mathematical
comparison vector. Each intermediate identity and both final
inequalities are checked using \`fractions.Fraction\`; none of
the original weights, scores, ledger events or receipts is changed.

A successful certificate only proves the finite conditional
inequalities **for the supplied validated local state**.
It never authenticates the supplying Python runtime or issuer.

## What is NOT proven

- Native Python builtin \`sum()\`, \`min()\`, \`max()\`, clipping and
  every binary64 operation are not modeled by a global Lean IEEE
  operational semantics or bisimulation.
- The seven products and exact \`Fin 7\` vector have to be linked by
  explicit evidence. The finite-list theorem does not silently
  identify them.
- No algebraic theorem converts original Python tolerance \`1e-9\`
  into the false assertion that raw weights sum exactly to one.
- No native state is normalized or corrected. The mathematical
  normalized comparison score is distinct from the recorded original.
- Source/issuer authentication, independent external history,
  host/store rollback, generalized Lean↔Python refinement,
  clinical authority, moral veto, or permission to execute are
  not established. NO_DATA remains on these requirements.

## Independent release and CI constraints

The stage-one v0.23 Lean file must pass exact-head pinned Strict
Lean with \`-DwarningAsError\` and \`-DsorryAsError\`, and an actual
axiom audit of each new theorem with only the standard three
axioms (propext, Classical.choice, Quot.sound), no sorryAx.
Only then are additive Python observer, source checker, tests and
this document adopted to the SAME existing Draft PR.

The final six-file HEAD requires independent Runtime and terminal
Governance SUCCESS, source/test-merge Git-tree identity, no
previous-source mutation, and subsequent integrated-main independent
push Runtime/Governance/Full Lean checks. A prior HEAD's CI success is
not a certificate for a later HEAD. The original full-root main Lean
build is a separate long-running run; its cancellation or incomplete
status is retained as an obstruction, not silently promoted.
