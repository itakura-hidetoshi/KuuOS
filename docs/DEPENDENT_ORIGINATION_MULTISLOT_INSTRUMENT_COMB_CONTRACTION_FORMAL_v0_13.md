# Dependent-origination multi-slot instrument / comb contraction formalization v0.13

## Purpose

v0.12 established the operational finite-history Born law for quantum instruments:

\[
p(o_1,\ldots,o_n)\ge 0,
\qquad
\sum_{o_1,\ldots,o_n}p(o_1,\ldots,o_n)=1.
\]

It also established deterministic open-comb causality and the scalar trace law

\[
\operatorname{Tr}W_n=d^n.
\]

What remained open was the exact generalized-Born bridge between the Choi representation and the operational joint probability.

v0.13 closes that bridge.

## Open comb versus closed Born scalar

The existing `QuantumCombChoi d n` is an **open deterministic comb**. Its recursive normalization

\[
\operatorname{Tr}_{\mathrm{newest\ output}}W_{n+1}
=
I_{\mathrm{newest\ input}}\otimes W_n
\]

is a causal boundary law. By itself it is not yet a scalar probability rule because an initial state and a final trace closure are still required.

For the sequential finite-history process used by v0.12, the scalar closure is explicit. For a density matrix \(\rho\), define the closed density/trace boundary

\[
W_\rho[(i,a),(j,b)]
=
\rho_{ij}\,\delta_{ab}.
\]

This is `closedBornCombChoi`.

## Choi tensor-link scalar

In the repository convention,

\[
J_\Phi[(i,a),(j,b)]
=
\Phi(E_{ij})_{ab}.
\]

The scalar Choi contraction is defined entrywise by

\[
\langle W,J\rangle_{\mathrm{link}}
=
\sum_{p,q}W_{pq}J_{pq}.
\]

The usual transpose placement of generalized-Born formulas is absorbed into the coefficient placement of `closedBornCombChoi`; no hidden conjugation or transpose is inserted later.

The first central theorem is

\[
\boxed{
\langle W_\rho,J\rangle_{\mathrm{link}}
=
\operatorname{Tr}(\Phi_J(\rho))
}
\]

for **every** Choi matrix \(J\), where \(\Phi_J=\operatorname{fromChoi}(J)\).

Lean theorem:

```text
closedBornCombChoi_tensorLink_eq_trace_fromChoi
```

## Arbitrary multi-slot Choi lists

For arbitrary slot Choi matrices

\[
J_1,\ldots,J_n,
\]

v0.9 already defines repeated causal Choi composition by `choiWord`, i.e. repeated `choiLink`.

The closed sequential process-comb scalar is

\[
\mathcal C_\rho(J_1,\ldots,J_n)
=
\left\langle
W_\rho,
\operatorname{choiWord}(J_1,\ldots,J_n)
\right\rangle_{\mathrm{link}}.
\]

No positivity assumption is needed for the following algebraic identity:

\[
\boxed{
\mathcal C_\rho(J_1,\ldots,J_n)
=
\operatorname{Tr}\!\left[
\Phi_{J_1}\circ\cdots\circ\Phi_{J_n}(\rho)
\right]
}
\]

with the exact composition order determined by the existing v0.9 head-after-tail convention.

Lean theorem:

```text
ClosedSequentialProcessCombChoi.tensorLinkScalar_eq_decodedOperationalResponse
```

Thus arbitrary finite multi-slot Choi data can be linked first and decoded later with no change in the scalar response.

## Chronological instrument histories

v0.12 instrument schedules are chronological:

```text
[I₁, I₂, ..., Iₙ]
```

means `I₁` acts first.

v0.9 intervention words instead use head-after-tail composition. Therefore the selected outcome operations are assembled as

\[
[\Phi_n^{o_n},\ldots,\Phi_2^{o_2},\Phi_1^{o_1}].
\]

This ordering bridge is formalized, not left implicit.

The theorem

```text
branchState_eq_selectedReverseInterventionWord
```

proves exactly that the v0.12 recursive branch state equals evaluation of the reverse-chronological v0.9 intervention word.

## Exact generalized Born theorem

For any finite quantum-instrument schedule, any selected outcome history of matching length, and any density matrix \(\rho\), define the multi-slot Choi scalar by

1. selecting each outcome's native Mathlib CP map;
2. taking each map's Choi matrix;
3. reversing to the v0.9 causal word convention;
4. repeatedly applying `choiLink`;
5. contracting the linked Choi matrix against `closedBornCombChoi ρ`.

Then

\[
\boxed{
\mathcal C_\rho
\bigl(
J_{\Phi_1^{o_1}},\ldots,J_{\Phi_n^{o_n}}
\bigr)
=
\operatorname{Tr}\!\left(
\Phi_n^{o_n}\circ\cdots\circ\Phi_1^{o_1}(\rho)
\right)
}
\]

and the right-hand side is exactly v0.12 `jointBornWeight`.

Lean theorem:

```text
multiSlotInstrumentChoi_tensorLink_eq_jointBornWeight
```

Taking real parts yields

\[
\boxed{
\mathcal P^{\mathrm{Choi}}(o_1,\ldots,o_n)
=
p^{\mathrm{operational}}(o_1,\ldots,o_n)
}
\]

as theorem

```text
multiSlotInstrumentChoi_tensorLinkProbability_eq_jointBornProbability
```

and therefore

\[
\mathcal P^{\mathrm{Choi}}(o_1,\ldots,o_n)\ge 0.
\]

## Architectural consequence

The quantum dependent-origination spine now contains the exact chain

```text
non-Markov memory-lifted history
→ operational process tensor
→ finite-dimensional Choi representation
→ deterministic quantum-comb causality
→ Choi positivity iff Mathlib complete positivity
→ native CPTP finite words
→ quantum instruments and normalized Born histories
→ arbitrary multi-slot Choi link composition
→ closed process-comb contraction
→ exact equality with operational joint Born probability
```

## Scope boundary

This theorem closes the generalized Born rule for the **closed sequential process comb determined by the v0.12 initial density and final trace**.

It does not falsely identify every open `QuantumCombChoi` with the same state-only Markov process. A genuinely non-Markov open comb requires an explicit operational realization or boundary closure before its scalar contraction can be compared with a particular operational history law.

That distinction is necessary: open-comb causality alone does not determine which initial boundary state or which operational realization is intended.

## Canonical base

This layer is additive and same-root from

```text
main@8ea0c32c4913894b2c59675fdb13c7288b20d7f4
```

with no weakening of v0.1-v0.12 theorems and no promotion of external physical authority.
