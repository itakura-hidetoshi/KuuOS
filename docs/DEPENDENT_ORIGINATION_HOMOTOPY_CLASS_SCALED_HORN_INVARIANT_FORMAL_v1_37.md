# Dependent Origination v1.37 — presentation-independent homotopy-class horn filling

## Purpose

Versions 1.33–1.36 separated two logically different questions:

1. how a bicategorical strong quasi-inverse produces global Duskin simplicial homotopies;
2. whether a boundary homotopy can be rectified to literal strict horn equality.

Version 1.36 closes the first question by constructing canonical normal-lax cylinders from native `Pseudofunctor.StrongTrans` data. Version 1.37 therefore changes the invariant rather than silently assuming the second question.

## Homotopy-class filler

For a scaled horn problem `P`, a `HomotopyClassScaledHornFiller P` is a scaled simplex map

```text
q : Δ[n] -> X
```

such that the actual boundary and prescribed horn map determine the same Mathlib relative simplicial homotopy class:

```text
[Λ[n,i] -> Δ[n] -> X] = [P.hornMap].
```

This is weaker than a strict filler and also weaker than asking for one single direct simplicial homotopy between the two maps.

The weakening is deliberate. A single `SSet.Homotopy` is not used as a transitive relation. Mathlib's `RelativeMorphism.HomotopyClass` is the transitive carrier because equality of quotient classes composes by ordinary equality.

## Presentation invariance

Given coherent normalized scaled model-equivalence data

```text
B  <->  C
```

with forward/backward normalized strictly-unitary transports, full scaling preservation, admissible-family preservation, and native coherent quasi-inverse data, v1.36 canonically produces the global round-trip prisms

```text
N(B) -> N(C) -> N(B)  ~  id
N(C) -> N(B) -> N(C)  ~  id.
```

For an arbitrary admissible target horn, transport it backward, fill it up to boundary homotopy class in the source, transport that simplex forward, and then use the target global prism. At the boundary-class level the proof is the transitive equality

```text
actual boundary
  = round-trip prescribed boundary
  = original prescribed boundary.
```

The same argument in the opposite direction yields

```text
HasHomotopyClassScaledHornFillers N_D(B)
  iff
HasHomotopyClassScaledHornFillers N_D(C).
```

No hornwise coherence choices and no homotopy-to-strict rectification are required.

## Strictness boundary

The formal hierarchy is

```text
strict scaled horn filler
  -> one-step homotopy scaled horn filler
  -> homotopy-class scaled horn filler.
```

Version 1.37 proves presentation independence only for the last carrier. It does **not** claim a converse back to strict filling. Any such converse is a separate strictification or lifting theorem.

This avoids circularly using fibrancy to prove the very fibrancy invariance under discussion.
