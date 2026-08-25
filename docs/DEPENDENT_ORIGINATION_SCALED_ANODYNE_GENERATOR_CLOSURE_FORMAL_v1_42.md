# Dependent origination: scaled-anodyne generator closure v1.42

## Scope

Version 1.41 reduced strictification to native terminal right lifting
properties in an explicit category of scaled simplicial sets. Version 1.42
packages the canonical horn-cylinder attachment inclusions into a single
Mathlib `MorphismProperty` and takes its canonical lifting-theoretic Galois
closure.

This is a higher-categorical specialization of the KuuOS dependent-origination
spine. It does not redefine the parent contextual-transport structure.

## Canonical generators

A generator is indexed by

- a dimension `n`,
- a distinguished horn `i : Fin (n + 1)`,
- an endpoint `ε : Fin 2`, and
- a chosen scaling on `Δ[n]`.

Its morphism is the scaled inclusion

```text
((Δ[n] × {ε}) ∪ (Λ[n,i] × Δ[1]), minimal scaling)
  -->
(Δ[n] × Δ[1], simplex-projection scaling).
```

All such inclusions form `scaledHornAttachmentGenerators`, an actual
`MorphismProperty ScaledSSet` via Mathlib `MorphismProperty.ofHoms`.

## Canonical generated scaled-anodyne class

For the generator property `T`, define

```text
canonicalGeneratedScaledAnodyne := T.rlp.llp.
```

Mathlib proves the Galois identity

```text
(T.rlp.llp).rlp = T.rlp.
```

Hence passing from the literal generators to their canonical left-orthogonal
closure does not change the right lifting class.

## Compatible presentations

A `ScaledAnodynePresentation` is any morphism property `A` satisfying

```text
T <= A <= T.rlp.llp.
```

Antitonicity of `rlp` and the Galois identity give

```text
A.rlp = T.rlp = (T.rlp.llp).rlp.
```

Therefore every compatible intermediate presentation has exactly the same
fibrant objects. This is presentation independence at the morphism-property
level rather than an informal assertion about equivalent generating lists.

## Attachment fibrancy

A scaled simplicial set `X` is `IsAttachmentFibrant` when its terminal map

```text
X --> *
```

belongs to `T.rlp`.

This target-level property is independent of any later chosen horn family.
For every scaled horn problem `P`, attachment fibrancy supplies the two native
lifting properties needed by v1.41, hence

```text
ScaledHornProblemTerminalRLP P.
```

Consequently it supplies terminal RLP, attachment lifting, cylinder extension,
and homotopy-class strictification for every chosen horn family on `X`.

## Global Duskin consequence

For two bicategorical models `B` and `C`, a coherent normalized scaled model
equivalence together with attachment fibrancy of both global Duskin nerves
produces

```text
HasScaledHornFillers (N_D B) HB
  <->
HasScaledHornFillers (N_D C) HC.
```

The horn families `HB` and `HC` remain explicit, while the lifting hypothesis
is no longer repeated family-by-family.

## Exact remaining boundary

This version does **not** identify the canonical generated class with an
external standard/Lurie scaled-anodyne class. The pinned Mathlib revision does
not provide the required scaled-anodyne model structure.

The remaining external comparison is now sharply expressed as a theorem
between morphism properties. It is enough to show that a future standard class
`A_std` satisfies

```text
scaledHornAttachmentGenerators <= A_std
A_std <= canonicalGeneratedScaledAnodyne
```

(or directly prove equality). The v1.42 sandwich theorem then gives equality of
right classes and therefore equality of fibrant objects automatically.
