# Dependent Origination Joint Causal Factorization — Formal v1.12

## Status

This layer connects two previously independent parent-level axes:

- higher-multicategory joint dependence from v1.8;
- causal monoidal marginals and no-signalling from v1.10–v1.11.

It does so by an explicit factorization certificate rather than by identifying
all joint dependence with tensor-parallel process structure.

## Exact structural move

A binary joint primitive has profile

```text
(X, Y) -> X' ⊗ Y'.
```

The primitive belongs to the higher-operadic signature and is evaluated by the
existing multi-condition algebra.

A `CausalTensorFactorization` additionally supplies causal local interventions

```text
f : X -> X'
g : Y -> Y'
```

such that for every pair of input states

```text
eval(op, x, y)
  = tensorState (D(f) x) (D(g) y).
```

This is semantic factorization on product inputs.  It is not a claim that the
operadic primitive is definitionally the monoidal tensor morphism in the source.

## Binary joint carrier

`BipartiteJointOperation` fixes the input profile to the ordered pair `(X,Y)`
and the output context to `X' ⊗ Y'`.

The ordered state argument function is supplied by `binaryStateArgs`, so the
existing v1.7/v1.8 positive-arity algebra is reused without changing its parent
signature.

## Joint no-signalling predicates

Two operational predicates are introduced.

Left-to-right:

```text
vary normalized x1,x2 in X;
keep y fixed;
rightMarginal (eval op x1 y)
  = rightMarginal (eval op x2 y).
```

Right-to-left is the dual statement.

Their conjunction is `JointNoSignalling`.

The varied side is required to be normalized because v1.11 marginal recovery
uses categorical discarding to remove that factor.  The opposite fixed input is
not required to be normalized.

## Factorization theorem

For a `CausalTensorFactorization`, each local causal intervention preserves
normalization by v1.10.  The v1.11 product-state marginal theorems then give

```text
rightMarginal (tensorState (D(f) x) (D(g) y)) = D(g) y
leftMarginal  (tensorState (D(f) x) (D(g) y)) = D(f) x
```

on the required normalized varied side.

Therefore:

```text
CausalTensorFactorization.leftToRight_noSignalling
CausalTensorFactorization.rightToLeft_noSignalling
CausalTensorFactorization.jointNoSignalling
```

establish

```text
explicit causal tensor factorization
  -> normalized-input two-way joint no-signalling.
```

## Higher coherence

A v1.8 primitive operation two-cell

```text
alpha : op => op'
```

is retained as higher source data.  The current set-truncated algebra sends it
to equality of joint evaluations.

Consequently:

- `BipartiteJointOperation.eval_eq_of_opCell` identifies the represented joint
  evaluations;
- `CausalTensorFactorization.ofOpCell` transports a factorization certificate to
  the higher-coherent representative;
- `jointNoSignalling_of_opCell` transports the operational no-signalling
  property itself.

Thus higher representation choice does not affect current set-valued causal
semantics, while the source-level operation cell is not erased.

## Boundary

The following implications are intentionally *not* asserted:

```text
joint dependence -> tensor factorization
joint dependence -> no-signalling
no-signalling -> tensor factorization
operadic composition = monoidal parallel composition
```

The factorization certificate is extra structure.  A genuinely coupled joint
operation may fail it while remaining a valid dependent-origination primitive.

This layer also does not claim Lorentzian spacetime reconstruction, physical
microcausality, quantum authority in the parent core, or physical Yang–Mills
authority.

## Files

- `formal/KUOS/DependentOriginationJointCausalFactorizationV1_12.lean`
- `formal/KUOS/DependentOriginationCoreSpineV1_12.lean`
- `docs/DEPENDENT_ORIGINATION_JOINT_CAUSAL_FACTORIZATION_FORMAL_v1_12.md`
