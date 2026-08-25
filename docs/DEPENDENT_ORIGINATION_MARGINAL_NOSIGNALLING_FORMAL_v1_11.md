# Dependent Origination Marginals and No-Signalling — Formal v1.11

## Purpose

v1.10 introduced a causal monoidal process layer with:

- causal orientation on context interfaces;
- categorical discarding;
- causal interventions;
- normalized-state preservation.

It deliberately stopped before general no-signalling.  v1.11 now adds the next
operational layer by defining explicit tensor marginals and proving
no-signalling for **tensor-separated causal interventions**.

The resulting implication is:

```text
causal discard normalization
  + explicit tensor separation
  -> explicit marginals
  -> one-way no-signalling
  -> two-way operational spacelike independence
```

This is stronger than v1.10 but still narrower than a no-signalling theorem for
arbitrary joint multi-condition processes.

## Explicit marginal processes

For `X ⊗ Y`, the left marginal is obtained by discarding `Y` and applying the
native right unitor:

```text
X ⊗ Y
  -- id_X ⊗ discard_Y -->
X ⊗ I
  -- rho_X -->
X.
```

The right marginal is dual:

```text
X ⊗ Y
  -- discard_X ⊗ id_Y -->
I ⊗ Y
  -- lambda_Y -->
Y.
```

These are formalized as:

- `leftMarginalProcess`
- `rightMarginalProcess`
- `leftMarginal`
- `rightMarginal`

For product states, normalization of the discarded factor recovers the retained
factor exactly:

- `leftMarginal_tensorState`
- `rightMarginal_tensorState`

Thus marginalization is not an informal projection operation; it is built from
the same discard/unit structure used by the causal process theory.

## Tensor-separated local interventions

A process `f : X -> X'` acts only on the left factor through

```text
f ⊗ id_Y : X ⊗ Y -> X' ⊗ Y.
```

Likewise a right-local process acts through

```text
id_X ⊗ g : X ⊗ Y -> X ⊗ Y'.
```

The definitions are:

- `leftLocalProcess`
- `rightLocalProcess`

## Source-level no-signalling equations

If `f` is a causal intervention, then

```text
(f ⊗ id_Y) >> rightMarginalProcess X' Y
=
rightMarginalProcess X Y.
```

This is theorem:

```text
rightMarginalProcess_after_left_causal
```

The proof uses only:

1. monoidal tensor/interchange;
2. associativity of composition;
3. the causal equation
   `f >> discard X' = discard X`.

The right-to-left theorem is:

```text
leftMarginalProcess_after_right_causal.
```

Therefore no-signalling is derived from the explicit causal/discard calculus in
the tensor-separated sector, rather than being inserted as a disconnected axiom.

## State-level one-way no-signalling

For a joint state `s : D(X ⊗ Y)`, a causal intervention on `X` cannot change the
right marginal:

```text
rightMarginal ((f ⊗ id_Y) s)
=
rightMarginal s.
```

This is:

```text
rightMarginal_after_leftIntervention.
```

Dually:

```text
leftMarginal_after_rightIntervention.
```

The corresponding predicates are:

- `OneWayNoSignallingLeftToRight`
- `OneWayNoSignallingRightToLeft`

and every tensor-separated causal intervention satisfies the appropriate
one-way predicate:

- `causal_left_noSignalling`
- `causal_right_noSignalling`

## Operational spacelike independence

v1.11 defines

```text
SpacelikeIndependent D C f g
```

as the conjunction of both one-way no-signalling equations for two local causal
interventions on separate tensor factors.

The theorem

```text
tensorSeparated_causal_spacelikeIndependent
```

proves that any such causal pair satisfies this operational independence
criterion.

This use of `spacelike` is intentionally operational and tensor-factor relative.
It does not assert a Lorentzian spacetime construction or physical microcausality.

## Critical scope boundary

The following implications are **not** claimed:

```text
causal process
=> arbitrary no-signalling joint process
```

or

```text
higher multi-condition operation
=> tensor-separated process.
```

An arbitrary v1.8 higher-multicategory operation may couple its inputs.  To
obtain no-signalling for such an operation one must supply an explicit marginal,
factorization, or conditional-independence law.

Likewise v1.11 does not claim:

- Markovianity;
- absence of memory;
- Lorentzian spacetime reconstruction;
- algebraic-QFT microcausality;
- braided or symmetric monoidal structure;
- compact closure or traced feedback;
- stack descent;
- enriched hom objects;
- infinity-categorical completion;
- quantum/process-tensor authority in the parent core;
- physical Yang--Mills authority.

## Structural reading

The dependent-origination causal axis now reads:

```text
context-dependent process
  -> causal orientation
  -> discard-preserving intervention
  -> normalized-state preservation
  -> explicit marginalization
  -> one-way no-signalling
  -> two-way operational spacelike independence.
```

The key principle remains the same as the wider KuuOS parent architecture:
stronger structure is added only when its hypotheses are explicitly carried;
it is never inferred from the word "causal" alone.
