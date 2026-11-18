# KuuOS Lean→Python v0.24 — original upper-Wa clipping under exact rational observation

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Fixed source and immutable boundary

Canonical predecessor: `main` `3f754ac305366a2c69627512a44d8fb86a788fff`, v0.23 formally merged.
Lean v4.30.0-rc2; mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`.
Append-only / tighten-only / overwrite-forbidden / same-root.
All six v0.23 files and 143 earlier source refs are preserved; this stage adds six new files.
The original Wa score kernel, store, ledger, event history and existing Lean declarations remain unmodified.

## The observed original source operation

The original v0.3 Wa upper endpoint does this sequence:

1. Calculate a **native float** relational upper and upper alert factor.
2. Multiply them to obtain an **unclipped native float** `rawUpper`.
3. Check the source-native range and then set `clippedUpper = min(1.0, rawUpper)`.
4. Preserve the originally stored Wa upper score.

The v0.20 operational observer already captures the actual multiplication certificate labeled
`wa:upper`, including exact rational representations of its input operands and observed output.
The new v0.24 observer requires this certificate, the original factor certificate, the
original clipped endpoint, and the previous v0.23 normalized score to match. It uses exact
`fractions.Fraction` comparison, without modifying a source score or assuming generalized
`min()` semantics.

## Conditional Lean mathematics

Let `N` be the v0.22 mathematically normalized weighted comparison and define

\[
 F_\beta(N,u,a)=((1-\beta)N+\beta u)(1-a).
\]

If `0≤β,N,u,a≤1`, then Lean v0.24 asserts the **rational ideal unit bound**

\[
 0\le F_\beta(N,u,a)\le1.
\]

For any rational `r` and ideal `I≤1`, the mathematical exact clamp satisfies

\[
 |\min(1,r)-I|\le |r-I|.
\]

When the actual native observed upper float has a separate source-validated identity
`C=min(1,R)` at the rational representation level, the original upper arithmetic
error `εWaRaw` is measured against `Fβ(Wobs,u,a)`, and v0.22 gives the
normalization budget `εweighted+τnative+εweightSum`, the composite inequality is

\[
\boxed{
|C-F_\beta(N,u,a)|
\le \varepsilon_{\mathrm{WaRaw}}
 + \varepsilon_{\mathrm{weighted}}
 + \tau_{\mathrm{native}}
 + \varepsilon_{\mathrm{weightSum}}.
}
\]

The file `formal/KuuOSFormal/WaUpperClipV0_24.lean` contains five new declarations:
normalized ideal unit interval; rational clamp nonexpansiveness; observed upper
clipped comparison; native normalized error composition; and a conditional transfer
to the Real ideal of v0.19.

This is a mathematical condition plus observed finite source evidence, **not** a proof
that every CPython execution implements these identities.

## Additive Python evidence and negative checks

`runtime/kuuos_lean_python_wa_upper_clip_v0_24.py` first reruns the existing v0.23
state and trace audits. It then extracts the `wa:upper` original observed result,
binds it to the actual upper native score and the v0.23 normalized upper ideal,
rechecks the exact arithmetic identity, and confirms that the observed clipped
error cannot exceed the preclipped normalized error or its explicit composed budget.

The pure rational helper permits independent tests with and without clipping,
but its result explicitly states that caller-provided source is not authenticated.
The full native-state audit validates source lineage first and preserves the
`NO_DATA` branch before evaluation. Static source checker inherits all earlier
pins, adds six predecessor blobs and verifies new file/test declarations.

## Remaining obstructions and authority

- No universal CPython/IEEE-754 binary64 arithmetic, `sum()`, `min()` or `max()`
  semantics is modeled.
- The positive-axis `min` and alert-axis `max` observations are not yet tied
  to a Lean finite-order-statistic theorem.
- The original source-native `1e-12` upper tolerance is not substituted for
  exact unit-interval arithmetic.
- Local state validity and conditional scalar inequalities do not prove an
  external issuer, causal history, host authority or whole Lean↔Python refinement.
- Success of source-marker checks alone is not Lean compilation, and no CI result
  can be borrowed across source HEADs.

## Exact-source release gate

The six-file Draft PR must obtain an independent pinned Strict Lean build for
`KuuOSFormal.WaUpperClipV0_24`, with axiom audits for all five new theorems
(only `propext`, `Classical.choice`, `Quot.sound`; no `sorryAx`),
cumulative Python Runtime tests, source checker and terminal Governance success
for the exact same HEAD. Verify the Git tree of the proposed source and
GitHub's test merge before merging. Retain the independent long-running
full-main Lean run's true status; never call an incomplete run successful.
