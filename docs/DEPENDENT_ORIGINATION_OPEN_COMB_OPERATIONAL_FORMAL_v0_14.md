# Dependent-origination open quantum-comb operational formalization v0.14

## Purpose

v0.13 closed the generalized Born rule for a sequential process with an explicit initial density boundary and final trace. That result is exact, but it is deliberately a closed sequential realization.

v0.14 keeps the open deterministic `QuantumCombChoi` carrier itself and gives it a direct finite-dimensional operational semantics without first collapsing all intervention slots into one composed channel.

## Fixed-length Choi history

For a uniform matrix dimension `d`, `ChoiSlotWord d n` is an `n`-slot Choi history. The head is the newest slot and the tail is the earlier history, exactly matching the recursive comb index

```text
CombIndex d 0       = Unit
CombIndex d (n + 1) = CombIndex d n × (Fin d × Fin d).
```

The complete slot tensor is defined recursively:

\[
S_{0}=1,
\]

and

\[
S_{n+1}[(h,(i,a)),(k,(j,b))]
=
S_n[h,k]\,J_{n+1}[(i,a),(j,b)].
\]

This retains every intervention slot separately.

## Direct all-leg open-comb contraction

For an open comb Choi matrix `Q.choi = W_n`, define

\[
\mathcal R_{W_n}(J_1,\ldots,J_n)
=
\sum_{r,c}
W_n[r,c]\,S_n[c,r].
\]

The transpose in the bilinear pairing is explicit and matches the matrix-unit Choi conventions already used in the repository.

In Lean this is `QuantumCombChoi.tensorLinkScalar`.

For complex-linear interventions, every slot is encoded by the exact v0.9 Choi map, giving `QuantumCombChoi.interventionResponse`.

## Slotwise linearity

The newest slot is proved to enter the complete tensor and the final comb contraction complex-linearly:

\[
\mathcal R_W(A+B,\text{past})
=
\mathcal R_W(A,\text{past})
+
\mathcal R_W(B,\text{past}),
\]

and

\[
\mathcal R_W(aA,\text{past})
=
a\,\mathcal R_W(A,\text{past}).
\]

The recursive carrier exposes the same property at earlier slots by applying the same construction inside the past word. The formal layer records the newest-slot laws directly, where the tensor recursion is visible.

## External operational realization

`OpenCombOperationalRealization Q History` is an explicit witness connecting an external history carrier to one open comb.

It provides:

- a fixed-length intervention word for each history;
- an external complex response;
- an exact equality between that response and the direct open-comb tensor-link scalar.

No arbitrary history model is automatically promoted to a quantum process tensor. The bridge is an explicit equality obligation.

## Sequential factorization is only a specialization

`SequentialFactorization Q` records the special case in which the complete open-comb response can be written as

\[
\mathcal R_Q(H)
=
\ell\bigl(\Phi_H(\rho_0)\bigr),
\]

where:

- `ρ₀` is one fixed initial matrix;
- `Φ_H` is only the single complex-linear map obtained by composing all slots of history `H`;
- `ℓ` is one fixed final readout.

Thus this certificate deliberately forgets all internal history once the total composed channel is known.

## Genuine history sensitivity obstruction

Define `DistinguishesEqualOperatorHistories Q` by existence of two fixed-length intervention histories `left` and `right` such that

\[
\Phi_{left}=\Phi_{right}
\]

but

\[
\mathcal R_Q(left)\ne\mathcal R_Q(right).
\]

Then v0.14 proves

\[
\boxed{
\mathrm{DistinguishesEqualOperatorHistories}(Q)
\Longrightarrow
\neg\,\mathrm{Nonempty}(\mathrm{SequentialFactorization}(Q)).
}
\]

This is the open-comb analogue of the earlier KuuOS history-sensitivity / total-summary factorization obstruction.

It gives a direct Choi-side criterion for genuinely non-Markov process information: two intervention histories may induce the same total channel and yet the process tensor can still distinguish them because it retains slotwise temporal correlations.

## Relationship to v0.13

v0.13 proves an exact closed sequential identity:

```text
repeated Choi link + density/trace boundary
  = operational branch trace
  = joint Born weight.
```

v0.14 does not weaken or replace that theorem. Instead it places it inside a larger architecture:

```text
open process tensor / quantum comb
  |
  +-- direct slotwise all-leg response
  |
  +-- optional sequential factorization
        |
        +-- closed state propagation of the v0.13 type
```

Therefore the repository no longer needs to treat every quantum process tensor as a state-only Markov chain.

## Scope

This layer is finite-dimensional and uniform in the slot matrix dimension. It does not assert:

- an infinite-dimensional process-tensor Choi theorem;
- that every deterministic comb exhibits non-Markov history distinction;
- that every KuuOS history carrier has an open-comb realization;
- a physical Yang–Mills process tensor;
- cross-repository physical theorem authority.

The non-sequential conclusion requires an actual pair of equal-composite histories with distinct responses, or an external realization that supplies such a distinction.
