# Dependent Origination Quantum Choi / Comb Formal v0.9

This document specifies the finite-dimensional quantum Choi layer added above the
v0.8 operational non-Markov process-tensor bridge.

The point of v0.9 is not to rename a real-linear process tensor as “quantum”.
Instead, the quantum layer is introduced only after explicit complex
matrix-algebra data and exact reconstruction theorems are present.

---

## 1. Starting point

v0.8 established an operational process tensor on a real vector-space carrier:

\[
\mathcal T[A_1,\ldots,A_n]
\]

with exact slotwise linearity and finite-memory realization.  It also proved
that visible non-Markov history sensitivity is exactly the same witness as
process-tensor history sensitivity under the explicit memory realization.

What v0.8 did **not** claim was:

- a complex Hilbert/matrix-algebra quantum carrier,
- complete positivity,
- trace preservation,
- Choi matrices,
- quantum-comb normalization.

v0.9 adds these as explicit mathematical structures rather than inferred labels.

---

## 2. Finite matrix algebra

For dimension `d`, define

\[
M_d(\mathbb C)
=
\operatorname{Matrix}(\mathrm{Fin}(d),\mathrm{Fin}(d),\mathbb C).
\]

In Lean this is

```lean
abbrev QMat (d : ℕ) := Matrix (Fin d) (Fin d) ℂ
```

For a complex-linear map

\[
\Phi:M_n(\mathbb C)\to M_m(\mathbb C),
\]

its Choi matrix is indexed by pairs `(input, output)`:

\[
J_\Phi[(i,a),(j,b)]
=
\Phi(E_{ij})_{ab}.
\]

---

## 3. Exact Choi encode/decode

The decoder is defined explicitly by

\[
\Phi_J(X)_{ab}
=
\sum_{i,j} X_{ij}J[(i,a),(j,b)].
\]

The formal layer proves both directions:

\[
\boxed{J_{\Phi_J}=J}
\]

and

\[
\boxed{\Phi_{J_\Phi}=\Phi}.
\]

Hence the Choi representation is not merely injective or observationally
equivalent.  It is an exact finite-dimensional encode/decode equivalence at the
level of complex-linear maps.

The relevant Lean theorems are:

```lean
choiMatrix_fromChoi
fromChoi_choiMatrix
```

and the arbitrary-input reconstruction formula is

```lean
apply_eq_sum_choi
```

corresponding to

\[
\Phi(X)_{ab}
=
\sum_{i,j}X_{ij}J_\Phi[(i,a),(j,b)].
\]

---

## 4. Trace preservation is exactly Choi partial-trace normalization

Define the output partial trace

\[
(\operatorname{Tr}_{out}J)_{ij}
=
\sum_a J[(i,a),(j,a)].
\]

The formal theorem is the exact equivalence

\[
\boxed{
\Phi\text{ trace preserving}
\iff
\operatorname{Tr}_{out}J_\Phi=I_n
}.
\]

Lean:

```lean
tracePreserving_iff_partialTraceOutput
```

This is proved in both directions, not stored as an assumption.

---

## 5. Positive Choi channel certificates

Two equivalent certificate surfaces are supplied.

### Operator-side

```lean
structure ChoiChannelCertificate (n m : ℕ) where
  map : QMat n →ₗ[ℂ] QMat m
  choiPositive : (choiMatrix map).PosSemidef
  tracePreserving : TracePreserving map
```

### Matrix-side

```lean
structure ChoiMatrixChannelCertificate (n m : ℕ) where
  choi : ChoiMat n m
  positive : choi.PosSemidef
  normalized : partialTraceOutput choi = 1
```

The matrix certificate decodes to an operator certificate, and the operator
certificate encodes to a matrix certificate.

The round trips are exact:

\[
\boxed{
\Phi\to J_\Phi\to\Phi
=
\Phi
}
\]

and

\[
\boxed{
J\to\Phi_J\to J
=
J.
}
\]

Lean:

```lean
channel_operator_roundtrip
channel_choi_roundtrip
```

The positivity obligation is stated directly as
`Matrix.PosSemidef`.  v0.9 does not silently identify this with any external CP
class whose equivalence theorem has not been imported/proved in this repository.
This prevents a theorem-authority jump while still giving the complete
matrix-side Choi channel representation.

---

## 6. Choi link product

For

\[
\Phi:M_n\to M_m,
\qquad
\Psi:M_m\to M_k,
\]

define

\[
(J_\Phi\star J_\Psi)[(i,c),(j,d)]
=
\sum_{a,b}
J_\Phi[(i,a),(j,b)]
J_\Psi[(a,c),(b,d)].
\]

Then the formal theorem is

\[
\boxed{
J_{\Psi\circ\Phi}
=
J_\Phi\star J_\Psi
}.
\]

Lean:

```lean
choiMatrix_comp
```

Thus causal operator composition has an exact Choi-side composition law.

---

## 7. Finite intervention words

For a finite complex intervention word

\[
w=[A_1,\ldots,A_N],
\]

the operator semantics is the ordered composition

\[
A_1\circ A_2\circ\cdots\circ A_N
\]

in the same head-after-tail convention used in v0.4–v0.8.

The Choi semantics recursively links the individual Choi matrices.

The theorem

```lean
choiMatrix_complexInterventionWordOperator
```

proves

\[
\boxed{
J_{\operatorname{Op}(w)}
=
\operatorname{ChoiWord}(J_{A_1},\ldots,J_{A_N})
}.
\]

---

## 8. Complete operational Choi response

A finite-dimensional complex operational process tensor consists of

- an initial matrix state,
- a complex-linear readout.

Its direct response is

\[
R(\operatorname{Op}(w)\rho_0).
\]

Its Choi response first reconstructs the linked Choi word and then applies the
same readout.

The exact theorem is

\[
\boxed{
\operatorname{response}(w)
=
\operatorname{choiResponse}(w)
}.
\]

Lean:

```lean
OperationalComplexProcessTensor.response_eq_choiResponse
```

This is the point where the whole finite intervention history has been replaced
by its Choi representation without changing the operational answer.

---

## 9. Deterministic quantum comb

A genuine multi-time process tensor requires more than one channel Choi matrix.
Its Choi operator must also satisfy causal normalization.

v0.9 introduces an explicit recursive index type `CombIndex d n`.  Each new slot
adds an input/output pair.

For an `n+1`-slot Choi operator `W`, define the partial trace over the newest
output leg:

\[
\operatorname{Tr}_{out_{n+1}}W.
\]

The deterministic comb recursion is

\[
\boxed{
\operatorname{Tr}_{out_{n+1}}W_{n+1}
=
I_{in_{n+1}}\otimes W_n
}.
\]

with

\[
W_{n+1}\ge0,
\]

and base normalization

\[
W_0=1.
\]

In Lean this is the recursive predicate

```lean
CombNormalized d n W
```

and the bundled Choi process tensor is

```lean
structure QuantumCombChoi (d n : ℕ) where
  choi : Matrix (CombIndex d n) (CombIndex d n) ℂ
  normalized : CombNormalized d n choi
```

For positive length, theorems expose both required facts:

```lean
QuantumCombChoi.positive_succ
QuantumCombChoi.exists_previous
```

Thus the comb is not represented by a free matrix plus a comment saying
“causal”.  Causality is the recursive partial-trace equation itself.

---

## 10. Why this is the non-Markov / process-tensor continuation

The v0.7–v0.8 state-space picture was

\[
(V,M)
\xrightarrow{\text{event}}
(V',M').
\]

The enlarged state is compositional, while the visible state alone is
non-Markov because later visible evolution depends on propagated memory.

v0.8 then encoded finite interventions operationally.

v0.9 adds the quantum representation layer:

\[
\boxed{
\text{memory-lifted non-Markov dynamics}
\to
\text{operational process tensor}
\to
\text{complex matrix-algebra lift}
\to
\text{exact Choi representation}
\to
\text{positive causally normalized quantum comb}
}.
\]

This is the mathematically correct order: process history first, quantum Choi
structure only after the additional quantum witnesses are supplied.

---

## 11. Explicit quantum lift from v0.8

A v0.8 process tensor is **not automatically** a quantum process tensor.
The new structure

```lean
QuantumChoiLift P d
```

requires:

1. a lift of every real intervention to a complex-linear matrix-algebra
   intervention;
2. a finite-dimensional complex operational process;
3. a real-linear decoder from complex readout back to the original output;
4. an exact response equality for every finite intervention word.

Only after those witnesses exist does the theorem

```lean
QuantumChoiLift.response_eq_complete_choi
```

produce

\[
\boxed{
\text{v0.8 response}
=
\text{decoded complete Choi response}.
} 
\]

This is the formal bridge from the non-Markov/process-tensor layer to the Choi
quantum layer.

---

## 12. Scope and authority boundary

v0.9 proves a complete finite-dimensional **matrix-side** Choi representation
and recursive deterministic quantum-comb normalization.

It does not claim, without a separate theorem:

- an equivalence to Mathlib's `CompletelyPositiveMap` class;
- a Stinespring or Kraus representation theorem for every certificate;
- infinite-dimensional process-tensor Choi operators;
- a physical Yang–Mills quantum process tensor;
- any physical mass-gap theorem.

Those are separate bridges.

The important point is that no missing theorem is replaced by terminology.
Every structure used in v0.9 carries the exact positivity, normalization,
composition, and reconstruction equations that the current claim requires.
