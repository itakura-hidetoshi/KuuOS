# Dependent Origination Process-Tensor Memory Bridge — Formal v0.8

## Purpose

This layer connects the finite-history / memory-lifted dependent-origination
spine to a mathematically explicit process-tensor interface.

The central point is not to rename a history-dependent map as a process tensor.
Instead, the bridge introduces the extra structure needed for the usual
operational process-tensor idea: a response functional of an ordered sequence
of interventions that is causal under slot composition and linear in each
intervention slot.

The bridge then proves that a real-linear realization of the v0.7 enlarged
state dynamics `Visible × Memory` produces exactly such a process tensor.

## 1. Intervention words

For a real vector space `State`, an intervention is a linear endomorphism

\[
A : State \to_{\mathbb R} State.
\]

A finite intervention word

\[
[A_1,\ldots,A_n]
\]

is evaluated with the same KuuOS convention as the finite-history spine:

\[
\operatorname{Op}([])=I,
\qquad
\operatorname{Op}(A::w)=A\circ\operatorname{Op}(w).
\]

Hence

\[
\operatorname{Op}(L++R)
=
\operatorname{Op}(L)\circ\operatorname{Op}(R).
\]

This is the causal composition law: the right history prepares the state on
which the left history acts.

## 2. Operational linear process tensor

An operational linear process tensor in this structural layer consists of

- an initial enlarged state `initial`, and
- a real-linear readout `readout`.

Its finite-word response is

\[
\mathcal T[A_1,\ldots,A_n]
=
R\bigl(\operatorname{Op}([A_1,\ldots,A_n])\,s_0\bigr).
\]

The Lean theorem `response_slotwise_linear` proves the process response is
linear in every intervention slot with all other slots fixed.  For arbitrary
left/right contexts,

\[
\begin{aligned}
&\mathcal T[L,(aA+bB),R] \\
&\qquad=
a\,\mathcal T[L,A,R]
+b\,\mathcal T[L,B,R].
\end{aligned}
\]

Thus the word response has the operational multilinearity expected of a
process tensor, without introducing a particular tensor-product/Choi
representation.

## 3. Finite-memory realization

The v0.7 structure

\[
S:\quad Visible\times Memory \longrightarrow Visible\times Memory
\]

is generic and may be nonlinear.  v0.8 therefore requires an explicit
`LinearRealization` witness

\[
L_e : Visible\times Memory \to_{\mathbb R} Visible\times Memory
\]

for every event `e`, together with the exact equality

\[
L_e(s)=S_e(s).
\]

No nonlinear history update is silently promoted to a linear process tensor.

Mapping an event history

\[
w=[e_1,\ldots,e_n]
\]

to the intervention word

\[
[L_{e_1},\ldots,L_{e_n}]
\]

gives the core realization theorem

\[
\boxed{
\operatorname{Op}(L_w)s
=
H_S(w,s)
}
\]

for every finite history and enlarged state.

## 4. Exact visible and memory responses

Using the linear projections

\[
\pi_V:Visible\times Memory\to Visible,
\qquad
\pi_M:Visible\times Memory\to Memory,
\]

v0.8 defines visible and memory process tensors.

The formal bridge proves exact identities

\[
\boxed{
\mathcal T_V(w;x,m)=V_S(w;x,m)
}
\]

and

\[
\boxed{
\mathcal T_M(w;x,m)=M_S(w;x,m).
}
\]

These are equalities of the formal definitions, not heuristic analogies.

## 5. Non-Markov causal composition

The visible response satisfies

\[
\boxed{
\mathcal T_V(L++R;x,m)
=
\mathcal T_V
\left(
L;
\mathcal T_V(R;x,m),
\mathcal T_M(R;x,m)
\right).
}
\]

In words: the right history produces both the visible intermediate state and
the memory state; both are required for the later left history.

The memory response obeys the corresponding composition law.

This is the precise finite-memory realization of the non-Markov statement:

- the enlarged state is strictly causal/functorial;
- the visible state alone is not closed under composition unless the propagated
  memory is retained.

## 6. Genuine non-Markov history sensitivity

For an additive summary type `Time`, v0.7 defines genuine visible history
sensitivity by the existence of two histories

\[
L,R
\]

with

\[
\sum L=\sum R
\]

but, for some visible initial state at the same initial memory,

\[
V_S(L;x,m)\neq V_S(R;x,m).
\]

v0.8 defines the corresponding process-tensor statement by replacing
`visibleEval` with the visible process-tensor response.

The central theorem is the exact equivalence

\[
\boxed{
\text{ProcessTensorHistorySensitive}
\iff
\text{GenuinelyVisibleHistorySensitive}.
}
\]

Therefore the non-Markov history witness is neither weaker nor stronger after
passing to the process-tensor realization: under the explicit linear
realization, it is the same mathematical proposition.

## 7. Obstruction to semigroup collapse

Combining the equivalence above with v0.7 gives

\[
\boxed{
\text{genuine process-tensor history sensitivity}
\Longrightarrow
\neg\,\text{TotalTimeFactorization}.
}
\]

Conversely, a total-time factorization forces every pair of equal-summary event
histories to have identical visible process-tensor response.

Thus the formal alternatives are sharp:

```text
finite-memory process tensor
  |
  +-- total-time factorizable
  |     -> equal-summary histories are operationally identical
  |
  +-- genuinely history-sensitive
        -> no one-parameter total-time semigroup can encode the process
```

## 8. Relation to existing KuuOS non-Markov modules

`KUOS.WORLD.KuuOSNonMarkovMemoryConnectionV0_72` contains a read-only history
module and a linear memory kernel inside a historical connection.  It does not
itself define a discrete event-by-event evolution law for the history carrier.

Therefore v0.8 does **not** derive a process tensor directly from the historical
connection object.  To instantiate this bridge from that analytic layer, an
explicit evolution realization must still provide the event operators on the
enlarged state and prove their compatibility with the desired memory
connection.

This preserves the distinction between

- a connection / memory-kernel structure, and
- a causal multi-time process dynamics.

## 9. Process-tensor scope boundary

The v0.8 object is an operational real-linear process tensor / deterministic
linear comb.  It proves causality and slotwise linearity.

It does not yet assert:

- complete positivity,
- trace preservation,
- density operators,
- Choi--Jamiołkowski representation,
- quantum-comb normalization constraints,
- varying Hilbert spaces at different slots,
- a physical Yang--Mills process tensor.

Those require additional structures and separate proofs.  In particular,
`itakura-hidetoshi/4d-mass-gap` remains authoritative for physical Yang--Mills,
Hamiltonian, spectral, and mass-gap claims.

## 10. Formal spine after v0.8

```text
functorial dependent origination
  -> free finite histories
  -> memory-lifted enlarged state
  -> causal full-state history transport
  -> explicit real-linear event realization
  -> operational process tensor
       -> append causality
       -> slotwise intervention linearity
       -> exact visible/memory projection bridge
       -> non-Markov witness iff process-tensor witness
       -> obstruction to total-time semigroup collapse
```
