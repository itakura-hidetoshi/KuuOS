# KuuOS Lean→Python v0.26 — extrema-reference error gluing

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Source, pins and original authority boundary

Canonical predecessor: main `9dc7e05a8deb2852698abdaa260ce143f45f8c35`
(v0.25 formally merged). Lean v4.30.0-rc2 and mathlib
`5450b53e5ddc75d46418fabb605edbf36bd0beb6`.
Append-only / tighten-only / overwrite-forbidden / same-root.

This stage adds six independent files and changes **none** of the original
Wa scorer, event adapter, weights, source-state snapshots, scores, receipts,
ledgers, prior Lean declarations, or shared CI definitions. All 161 selected
predecessor source identities remain pinned transitively.

## Mathematical statement — explicit hypotheses

The original exact rational Wa score is

\[
F_\beta(W,u,a)=((1-\beta)W+\beta u)(1-a).
\]

Assume `0≤β≤1` and `0≤a≤1`. Then for any two weakest-axis values

\[
|F_\beta(W,u,a)-F_\beta(W,u',a)|\le |u-u'|.
\]

For `0≤N,u'≤1` and `0≤β≤1`, we also have

\[
|F_\beta(N,u',a)-F_\beta(N,u',a')|\le |a-a'|.
\]

Therefore, when the original observed extrema `u,a` are compared with
**explicitly identified** unit-range reference extrema `u',a'`,

\[
|F_\beta(N,u,a)-F_\beta(N,u',a')|
\le |u-u'|+|a-a'|.
\]

Combine this with the independently observed native final Wa score `O`,
the measured original native weighted value `Wobs`, and the v0.22/v0.23
normalized ideal comparison `N`. Given separately verified hypotheses

\[
|O-F_\beta(W_{obs},u,a)|\le \varepsilon_{Wa},\qquad
|W_{obs}-N|\le \varepsilon_{weighted}+\tau_{native}
 +\varepsilon_{weightSum},
\]
\[
|u-u'|\le \varepsilon_{weakest},\qquad
|a-a'|\le \varepsilon_{alert},
\]

the combined conditional inequality is

\[
\boxed{
|O-F_\beta(N,u',a')|
\le \varepsilon_{Wa}+\varepsilon_{weighted}
 +\tau_{native}+\varepsilon_{weightSum}
 +\varepsilon_{weakest}+\varepsilon_{alert}.
}
\]

Crucially, the proof **does not require the raw observed weighted score
to be exactly in [0,1]**. The alert sensitivity uses the mathematically
normalized score `N`, for which v0.22 supplies the unit-interval theorem.
The v0.26 source also transports the result conditionally to the existing
Real-valued Wa ideal.

Six new Lean theorem declarations are written in
`formal/KuuOSFormal/WaExtremaStabilityV0_26.lean`:
weakest-input contraction, alert-input contraction, two-extrema
stability, observed Wa and normalized-weight gluing, and its conditional
rational-to-Real transport. Compiler and axiom certification are separate
release gates and cannot be inferred from source-marker presence.

## Python: strictly source-bound native observation plus a counterfactual

The native-state audit first verifies all existing v0.25 source and
original-state certificates. It selects both *actual original* endpoint
observations of the **same Wa option**. It uses each endpoint's
opposite endpoint as an explicitly identified mathematical
**counterfactual reference**, never as a claimed native computation
at that reference.

The new read-only observer checks, using exact `fractions.Fraction`
representations:

- the original Wa score and weighted native observation, and their
  v0.23 raw/normalized discrepancy evidence;
- each endpoint's v0.25 native weakest-positive and strongest-alert
  identity, with the original positive/alert axis order;
- two reference extrema drawn from the opposite observed endpoint of
  the same original option;
- exact weakest/alert arithmetic differences and their nonnegative
  error budgets;
- the counterfactual final ideal score and composed error bound;
- all original option IDs, state digest and caller-state immutability.

A pure rational helper can verify supplied numbers but cannot
authenticate an external caller or certify an original source by itself.
The full-state audit performs the prior validation before comparisons.

This work does **not** recompute or substitute stored original scores.
The comparison reference does not authorize changes to original Wa
weights, policy, interpretation, clinical judgment, or downstream actions.

## Fail-closed and remaining obstructions

Unknown or wrong-typed evidence, altered source, noncanonical rational
pairs, negative budgets and invalid unit-range preconditions block the
new certificate. Prior to evaluation, NO_DATA must not become SUCCESS.

Neither the six conditional rational/Real theorems nor the Python
observations prove arbitrary CPython binary64, `sum()`, `min()`,
`max()`, clipping, or native execution-order semantics. They do not
prove all Lean↔Python program states correspond, external issuing source
authenticity, complete causal history or action authority.

## Exact-head independent release gate

The final six-file Draft PR requires pinned Strict Lean compilation
`KuuOSFormal.WaExtremaStabilityV0_26` with
`-DwarningAsError=true -DsorryAsError=true`, all six theorem axiom
audits (only `propext`, `Classical.choice`, `Quot.sound`, no
`sorryAx`), full cumulative Python Runtime, all new source checks,
GitHub test-merge/source Git-tree identity, and *every paginated job*
and terminal PR Governance workflow `completed/SUCCESS` for the
**same HEAD**. Hold Draft/no merge otherwise; repair only the existing
PR. After merge, reobserve independent main push Runtime/Governance/
Full Lean; an in-progress or cancelled Full Lean is not certified.
