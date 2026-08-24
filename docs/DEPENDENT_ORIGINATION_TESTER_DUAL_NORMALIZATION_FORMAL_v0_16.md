# Dependent Origination Tester Dual Normalization — Formal v0.16

## Purpose

v0.15 introduced a closed quantum process tester with positive Choi matrix and
an operational normalization condition sufficient for finite Born laws:

```text
TesterNormalized W :=
  every fixed-length word of trace-preserving Choi slots has tester weight 1.
```

That predicate is intentionally weak.  It constrains complete deterministic
histories only.  It does **not** say that after inserting a deterministic newest
slot the remaining past tester is a unique history-independent residual.

The standard dual recursive tester normalization needs exactly that stronger
conditional causal statement.  v0.16 formalizes the missing layer rather than
asserting an unjustified converse from the weaker v0.15 predicate.

## One-step residual contraction

For

```text
W : Matrix (CombIndex d (n+1)) (CombIndex d (n+1)) ℂ
J : ChoiMat d d
```

define `contractNewest W J` by summing all newest input/output Choi indices and
retaining the full past `CombIndex d n` matrix.

The operational conditional condition is

```text
∀ J,
  partialTraceOutput J = 1 →
  contractNewest W J = previous.
```

Thus every deterministic newest channel leaves exactly the same residual
`previous`.

## Dual matrix form

Define a core

```text
X : Matrix (CombIndex d n × Fin d)
           (CombIndex d n × Fin d) ℂ
```

and the explicit newest-output identity lift

```text
liftNewestOutputIdentity X
```

with entries

```text
W[p,(i,a); q,(j,b)] = δ_ab X[(p,i),(q,j)].
```

Also define

```text
partialTraceNewestInput X [p,q]
  = Σ_i X[(p,i),(q,i)].
```

The one-step theorem is

```text
deterministicResidual_iff_exists_dualCore
```

and states exactly

```text
(∀ deterministic J, contractNewest W J = previous)
↔
∃ X,
  W = liftNewestOutputIdentity X ∧
  partialTraceNewestInput X = previous.
```

## Converse proof mechanism

The difficult direction is operational → matrix form.

Start from the identity-channel Choi matrix.  Add arbitrary matrices with zero
output partial trace.  The residual hypothesis forces every such perturbation
to contract to zero.

Two matrix-unit probe families are then sufficient:

1. output-off-diagonal units

```text
E_((j,b),(i,a)),  a ≠ b,
```

whose output partial trace is zero.  They force

```text
W[p,(i,a);q,(j,b)] = 0  for a ≠ b.
```

2. differences of output-diagonal units

```text
E_((j,a),(i,a)) - E_((j,b),(i,b)),
```

which also have zero output partial trace.  They force the output diagonal to be
independent of the output basis index.

Hence `W` is exactly an output-identity lift.  Contracting once with the
identity channel then identifies the input partial trace of the core with the
specified previous residual.

The degenerate `d = 0` case is handled inside the theorem: the successor comb
index is empty and the residual is forced to zero.

## Recursive equivalence

`CausalTesterNormalized d n W` is defined recursively by

```text
W_0 = 1
```

and, for each successor level, existence of one previous causal tester such that
all deterministic newest channels contract to that same previous tester.

`DualTesterNormalized d n W` is defined recursively by

```text
W_0 = 1
W_(n+1) = I_output ⊗ X_(n+1)
Tr_input X_(n+1) = W_n.
```

The main theorem is

```text
causalTesterNormalized_iff_dualTesterNormalized
```

so the conditional operational and dual matrix formulations are exactly
identical in finite dimensions.

## Relation to v0.15

The dual recursion directly reduces one deterministic slot at a time.  Therefore
v0.16 proves

```text
dualTesterNormalized_implies_testerNormalized
causalTesterNormalized_implies_testerNormalized
```

and bundles the strong forms as

```text
CausalQuantumProcessTesterChoi
DualQuantumProcessTesterChoi.
```

Both forget canonically to the v0.15 `QuantumProcessTesterChoi` and retain the
same Choi matrix.

The converse

```text
TesterNormalized W → DualTesterNormalized d n W
```

is deliberately **not** claimed.  The v0.15 predicate only probes complete
products of deterministic local slots and can leave linear directions
undetected.  Conditional residual causality supplies the missing information.

## Mathematical spine after v0.16

```text
history-sensitive dependent origination
→ memory-lifted transport
→ operational process tensor
→ exact finite-dimensional Choi representation
→ Mathlib complete positivity
→ CPTP finite words
→ quantum instruments and Born normalization
→ arbitrary multi-slot generalized Born rule
→ open-comb all-leg response
→ closed quantum process tester
→ causal residual normalization
↔ dual recursive partial-trace normalization
```

## Authority boundary

This is a finite-dimensional structural quantum process-tensor theorem inside
KuuOS.  It does not assert an infinite-dimensional process-tensor theorem and
does not transfer physical Yang--Mills spectral or mass-gap authority from the
separate `4d-mass-gap` repository.
