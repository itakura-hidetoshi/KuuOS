# KuuOS Lean→Python v0.25 — original finite weakest-positive and strongest-alert witnesses

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Canonical context

Previous canonical `main`: `6a9ec01adfd67ea17822612ad1cb9fa50c4f82bc` (v0.24 merged).
Pinned Lean `v4.30.0-rc2`; mathlib
`5450b53e5ddc75d46418fabb605edbf36bd0beb6`.
Append-only / tighten-only / overwrite-forbidden / same-root.
Original KuuOS kernels, Wa v0.3 evaluator, Python state/digests,
native stored scores and all prior 155 source references are untouched.

## Original native selection under observation

The original Wa scorer uses `min(samples)` for seven positive axes,
`max(alert_samples)` for the alert axes and opposite alert extrema
for its lower/upper Wa endpoints:

- Lower: minimum of the seven lower positive-axis samples;
  **maximum of the upper alert-axis samples**.
- Upper: minimum of the seven upper positive-axis samples;
  **maximum of the lower alert-axis samples** (then v0.24's original
  upper-score clipping remains in effect).

Each sample is the *actual observed finite native float*, converted
losslessly to a rational pair with `as_integer_ratio()`. No mathematical
renormalization changes the original axis values.

The v0.25 Python witness reruns the v0.20–v0.24 read-only checks,
retains original source axis names/order, checks both observed extrema
against exact rational finite-list selection, verifies member inequalities,
and requires the original normalized Wa ideal to be unchanged.
The pure `certify_finite_extrema` helper is intentionally NOT
source-authenticated; the state-level auditor first runs the full prior
source/state validation and verifies original option IDs.

## Exact rational Lean model

Define finite-list extrema using mathematical recursion:

\[
m([])=1,\quad m(x::xs)=\min(x,m(xs)),
\]

\[
M([])=0,\quad M(x::xs)=\max(x,M(xs)).
\]

These empty-list defaults are only mathematical **unit-range sentinels**;
the original Wa positive and alert axis lists are nonempty and checked.

The proposed six new Lean declarations establish:

1. For finite samples each in `[0,1]`, `0≤m(xs)≤1`.
2. For finite samples each in `[0,1]`, `0≤M(xs)≤1`.
3. The selected minimum is no greater than every list member.
4. Every list member is no greater than the selected maximum.
5. With `0≤β,N≤1`, the Wa ideal `Fβ(N,m(P),M(A))` lies in `[0,1]`.
6. When explicitly supplied native observations satisfy the finite-list
   extrema equalities, they can be substituted into the exact rational
   Wa ideal without changing it.

The v0.23 score model is

\[
F_\beta(W,u,a)=((1-\beta)W+\beta u)(1-a).
\]

Thus the v0.24 upper clipping contraction remains applicable when the
v0.25 selected extrema are used and all declared unit hypotheses hold.
This is a conditional local compositional observation, not a
universal interpreter refinement.

## Why this is a meaningful but bounded extension

Before this stage, v0.24 treated the original weakest-positive and
strongest-alert values as observed scalar inputs, with their membership
in a finite ordered axis list left outside that particular Lean theorem.

This stage records axis order, all source sample rationals, each
observed selected extremum, the membership witness indices (including
ties), and the original normalized Wa ideal equality.

The Python observation is separately checked for both lower and upper
native endpoints. The original score, Wa store, ledger, thresholds and
event adapter are unchanged. Missing/ill-typed data fails closed.
Prior to evaluation there is no claimed local extrema certificate.

## Remaining obstructions — DO NOT promote

- Finite rational min/max proofs do **not** prove arbitrary CPython
  `min()` / `max()` or binary64 semantics.
- No universal float sum, clipping, tie-breaking or execution-order
  bisimulation is established.
- The exact finite extrema result and observed source-linked scalar
  equality are local, not a global `Lean↔Python` refinement.
- No external source issuer, signed causality, complete history,
  institutional endorsement or execution authority is supplied.
- `NO_DATA` and failed source/reference bindings remain blockers.

## Release gate

Adopt the six new files in a single Draft PR on the exact v0.24 main
base. Independently compile `KuuOSFormal.WaFiniteExtremaV0_25` with
pinned Lean, `warningAsError=true` and `sorryAsError=true`. Audit
each new theorem with `#print axioms`; only `propext`,
`Classical.choice`, `Quot.sound` are permitted, no `sorryAx`.

The final PR HEAD must pass full cumulative Python Runtime, 155
transitive predecessor source pins, all new tests, all **paginated**
Governance jobs, exact-head terminal workflow `completed/SUCCESS`,
and source/test-merge Git-tree identity. Hold Draft/no merge otherwise.
Record post-merge push Runtime / Governance / full Lean independently,
never upgrading cancelled or in-progress full Lean to SUCCESS.
