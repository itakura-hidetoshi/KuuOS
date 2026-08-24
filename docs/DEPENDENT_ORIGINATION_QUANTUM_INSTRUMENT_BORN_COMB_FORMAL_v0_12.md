# Dependent-origination quantum instrument / Born / comb formalization v0.12

## Purpose

v0.10 proved the finite-dimensional Choi theorem directly against Mathlib native complete positivity,
and v0.11 closed native CPTP composition, finite Choi words, and density-state preservation.

v0.12 adds the first genuinely probabilistic operational layer.  It deliberately does **not** obtain
probabilities from an arbitrary linear readout.  Instead it proves normalization from the actual
quantum hypotheses that carry it.

Two normalization mechanisms are kept distinct:

1. **quantum instrument normalization** — each outcome is completely positive and the finite sum
   of all outcome maps is trace preserving;
2. **deterministic quantum-comb normalization** — the Choi matrix obeys the recursive newest-output
   partial-trace causality equation.

## Finite quantum instrument

For a finite outcome type `Outcome`, a `QuantumInstrument d Outcome` contains

\[
\Phi_o:M_d(\mathbb C)\to_{CP}M_d(\mathbb C)
\qquad(o\in Outcome)
\]

using Mathlib's native `CompletelyPositiveMap`, together with

\[
\operatorname{Tr}\!\left(\sum_o \Phi_o(X)\right)
=
\operatorname{Tr}(X).
\]

Individual outcomes are not assumed trace preserving.

For a density matrix

\[
\rho\succeq0,
\qquad
\operatorname{Tr}\rho=1,
\]

the outcome matrix is

\[
\rho_o=\Phi_o(\rho).
\]

Complete positivity gives

\[
\rho_o\succeq0.
\]

Therefore the Born weight

\[
w_o=\operatorname{Tr}(\rho_o)
\]

is nonnegative in the canonical complex order, hence real with nonnegative real part.  The exported
real probability is

\[
p_o=\operatorname{Re} w_o\ge0.
\]

The instrument trace-preserving sum gives the exact normalization

\[
\sum_o w_o=1,
\qquad
\sum_o p_o=1.
\]

The corresponding Lean theorems are:

- `QuantumInstrument.bornWeight_nonneg`
- `QuantumInstrument.bornProbability_nonneg`
- `QuantumInstrument.bornWeight_sum_eq_one`
- `QuantumInstrument.bornProbability_sum_eq_one`.

## Instrument Choi representation

Each outcome has Choi matrix

\[
J_o=J_{\Phi_o}\succeq0.
\]

The total instrument Choi matrix is

\[
J_{\mathrm{tot}}=\sum_oJ_o.
\]

Because Choi encoding is additive,

\[
J_{\mathrm{tot}}
=
J_{\sum_o\Phi_o}.
\]

The total trace-preserving condition is therefore exactly

\[
\operatorname{Tr}_{out}J_{\mathrm{tot}}=I.
\]

Thus the whole instrument determines a normalized positive Choi channel certificate, while the
individual positive Choi matrices retain outcome resolution.

## Finite-history Born law

A schedule is a finite chronological list of instruments.  A selected outcome list of matching
length determines an unnormalized branch state by repeated outcome-map application.

Every branch remains positive:

\[
\rho_{o_1,\dots,o_N}\succeq0.
\]

Hence the joint branch probability

\[
p(o_1,\dots,o_N)
=
\operatorname{Re}\operatorname{Tr}
\rho_{o_1,\dots,o_N}
\]

is nonnegative.

Instead of introducing a separate Cartesian-product enumeration, the complete outcome-tree weight
is defined recursively by iterated finite sums.  Slotwise instrument normalization telescopes:

\[
\sum_{o_1}\cdots\sum_{o_N}
\operatorname{Tr}ho_{o_1,\dots,o_N}
=
\operatorname{Tr}\rho.
\]

For a density matrix this gives

\[
\boxed{
\sum_{o_1,\dots,o_N}p(o_1,\dots,o_N)=1
}.
\]

The main Lean theorems are:

- `branchState_posSemidef`
- `jointBornWeight_nonneg`
- `jointBornProbability_nonneg`
- `totalJointWeight_eq_trace`
- `totalJointWeight_density_eq_one`
- `totalJointProbability_eq_one`.

## Deterministic quantum-comb scalar normalization

v0.9 defined a uniform-dimensional deterministic comb recursively by

\[
W_0=1,
\]

and

\[
\operatorname{Tr}_{out_{n+1}}W_{n+1}
=
I_{in_{n+1}}\otimes W_n,
\qquad
W_{n+1}\succeq0.
\]

v0.12 now derives the scalar trace law rather than leaving it implicit.  Taking ordinary trace at
one recursive step gives

\[
\operatorname{Tr}W_{n+1}
=
d\,\operatorname{Tr}W_n.
\]

Therefore

\[
\boxed{
\operatorname{Tr}W_n=d^n
}.
\]

This is theorem `combNormalized_trace`, exposed for bundled combs as
`QuantumCombChoi.trace_eq_dimension_pow`.

This result is important because it confirms that the recursive Choi causality condition carries
the expected deterministic scalar normalization independently of the instrument proof.

## Instrument / comb causal boundary

For a positive-length deterministic comb and a finite quantum instrument, v0.12 proves that both
normalization boundaries are simultaneously available:

\[
\operatorname{Tr}_{out_{new}}W_{n+1}
=
I_{in_{new}}\otimes W_n,
\]

and

\[
\operatorname{Tr}_{out}J_{\mathrm{tot}}=I.
\]

This is theorem `instrument_comb_causal_boundaries`.

It is intentionally **not** advertised as the full arbitrary tensor-link contraction theorem.  A
future layer can define the exact multi-slot link contraction and prove that contracting a
deterministic comb against normalized instruments reproduces the same nonnegative normalized joint
law.  v0.12 provides both sides of the normalization identity without replacing that missing
contraction by an informal identification.

## Architectural consequence

The formal quantum spine is now

```text
memory-lifted non-Markov transport
→ operational process tensor
→ complete finite-dimensional Choi representation
→ deterministic quantum-comb causality
→ Choi positivity iff Mathlib CP
→ native CPTP finite histories
→ density-state preservation
→ quantum instruments
→ nonnegative Born branches
→ normalized finite-history joint law
→ deterministic comb scalar normalization
```

## Scope

All statements are finite-dimensional and use complex matrix algebras.  No infinite-dimensional
Choi theorem, physical Yang–Mills process tensor, or automatic promotion of arbitrary real-linear
KuuOS interventions is asserted here.
