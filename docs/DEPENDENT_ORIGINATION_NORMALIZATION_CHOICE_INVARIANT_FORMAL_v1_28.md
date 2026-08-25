# Dependent origination — normalization-choice invariant formalization v1.28

## Status

Version 1.28 advances the presentation-independent invariant beyond the choice
of a strictly-unitary representative used to obtain direct global Duskin
transport.

The parent dependent-origination notion is still unchanged:

```text
context-dependent establishment + composable transport.
```

No groupoid, stack, operad, process theory, enriched category, bicategory,
quasicategory, or Duskin nerve is promoted to the parent definition. They
remain structured specializations or higher realizations.

## Previous frontier

Version 1.26 established model independence at the intrinsic 1/2-cell level:

```text
source presentation
  -> source intrinsic carrier
  -> bicategorical model equivalence
  -> target intrinsic carrier
  -> target presentation.
```

Version 1.27 then proved that a strictly-unitary model equivalence induces a
genuine all-degree simplicial map

```text
N_Duskin(B) -> N_Duskin(C),
```

with exact comparison factorization

```text
target global comparison
  = pseudofunctor composition coherence
  ; transported intrinsic comparison.
```

The remaining issue was the chosen normal representative.

## Pinned Mathlib boundary

At the pinned Mathlib revision

```text
5450b53e5ddc75d46418fabb605edbf36bd0beb6
```

`StrictlyUnitaryPseudofunctor` is native, and strong transformations between
oplax functors are native. However `StrictlyUnitary.lean` still lists two
pieces of infrastructure as future work:

- automatic normalization of arbitrary pseudofunctors to strictly-unitary
  pseudofunctors;
- identity-component oplax transformations (`Icon`) bundled specifically for
  normal pseudofunctors.

Version 1.28 therefore does not assert either construction unconditionally.
Instead it isolates exact certificates for them.

## 1. Strictly-unitary normalization certificate

For a general v1.26 model equivalence

```text
E : BicategoricalModelEquivalence B C,
```

a

```text
StrictlyUnitaryNormalizationCertificate E
```

contains:

1. a normalized

   ```text
   normal : StrictlyUnitaryBicategoricalModelEquivalence B C;
   ```

2. a native Mathlib strong transformation

   ```text
   normal.forward  ==>  E.forward;
   ```

3. the assertion that every object component of that transformation is an
   intrinsic bicategorical adjoint equivalence.

This is an existence interface, not an existence theorem.

## 2. Comparison of two normalization choices

For two strictly-unitary model equivalences `E₁` and `E₂`, a

```text
NormalizationChoiceComparison E₁ E₂
```

contains a native strong transformation

```text
η : E₁.forward ==> E₂.forward
```

whose object components

```text
η_X : E₁(X) -> E₂(X)
```

are intrinsic equivalence 1-cells.

This is the correct replacement, at the pinned revision, for a bundled
invertible icon/pseudonatural equivalence between normal representatives.

## 3. One-cell normalization independence

For every source 1-cell

```text
f : X -> Y,
```

strong naturality gives the canonical isomorphism

```text
E₁(f) ; η_Y  ≅  η_X ; E₂(f).
```

Thus the two transported 1-cells need not be literally equal. They represent
the same intrinsic transport modulo coherent equivalence of their source and
target objects.

Version 1.28 packages this as

```text
normalizationOneCellIso.
```

It also defines `CoherentOneCellObservable`: an observable on 1-cells that is
unchanged under equivalence changes of endpoints and an isomorphism of the
resulting arrows.

For every such observable `Φ`, the theorem

```text
oneCellObservable_normalizationIndependent
```

proves

```text
Φ(E₁(f)) = Φ(E₂(f)).
```

This is a genuine presentation-independent statement because it does not pick
one normal presentation as canonical.

## 4. Two-cell normalization independence

For a source 2-cell

```text
α : f -> g,
```

the native strong-transformation naturality law is

```text
(E₁.map₂ α ▷ η_Y) ; η_g
  =
η_f ; (η_X ◁ E₂.map₂ α).
```

Here `η_f` and `η_g` are the strong-naturality isomorphisms of the two
transported 1-cells.

This exact square is re-exported as

```text
normalizationTwoCellNaturality.
```

A `CoherentTwoCellObservable` is required to be invariant under precisely this
kind of conjugacy square. The theorem

```text
twoCellObservable_normalizationIndependent
```

then proves equality of its values for the two normalizations.

## 5. Invertibility does not depend on normalization

Each strictly-unitary model equivalence contains, for every pair `X,Y`, a
categorical equivalence

```text
B(X,Y) ≃ C(E(X),E(Y))
```

whose forward functor is exactly the pseudofunctor's native hom-functor.

A categorical equivalence is fully faithful, hence reflects isomorphisms.
Therefore version 1.28 proves

```text
IsIso(E.map₂ α) <-> IsIso(α).
```

Consequently, for any two normal representatives,

```text
IsIso(E₁.map₂ α) <-> IsIso(E₂.map₂ α).
```

This is stronger than merely showing both directions preserve invertibility:
it identifies invertibility as an intrinsic source predicate, independent of
normalization.

For a Duskin comparison cell this specializes to

```text
IsIso(E₁.map₂(duskinComparison σ))
  <->
IsIso(E₂.map₂(duskinComparison σ)).
```

Thus the intrinsic thinness criterion does not depend on which strictly-unitary
representative is used.

## 6. Global Duskin edges

For a source global Duskin edge `σ`, direct v1.27 transport under the two
normalizations gives two target global edges. Version 1.28 proves that their
principal 1-cells satisfy

```text
edge(E₁ σ) ; η_target
  ≅
η_source ; edge(E₂ σ).
```

Therefore every coherent observable of the transported global edge has the
same value for either choice.

## 7. Why literal equality is the wrong goal

A normal representative is presentation data. Different normalizations may
change:

- target objects by adjoint equivalence;
- represented 1-cells by coherent isomorphism;
- represented 2-cells by a conjugacy square.

Demanding literal equality would make the invariant depend on implementation
choices that bicategorical mathematics intentionally quotients out.

The correct statement is therefore

```text
normalization choice
  -> coherent bicategorical equivalence
  -> identical invariant observable.
```

not

```text
normalization choice
  -> literal equality of pseudofunctors.
```

## 8. Resulting presentation-independent chain

The current formal chain is

```text
same B, local/global presentations
  -> intrinsic B(X,Y) invariant                         -- v1.25

B and C related by model-equivalence data
  -> intrinsic invariant transported across models     -- v1.26

strictly-unitary representative chosen
  -> direct all-degree global Duskin map                -- v1.27

two normal representatives strongly compared
  -> coherent 1-cell agreement
  -> coherent 2-cell agreement
  -> coherent observables equal
  -> intrinsic IsIso predicates equal                  -- v1.28
```

This moves the intended invariant substantially closer to

```text
presentation-independent invariant
```

in the strong sense: neither local/global encoding, nor biequivalent model, nor
chosen normal representative is taken as the invariant itself.

## Formal boundary after v1.28

Proved conditionally on explicit certificates:

- chosen strictly-unitary normalization interface;
- strong comparison of two normalized representatives;
- coherent 1-cell correspondence;
- exact 2-cell naturality square;
- normalization independence of arbitrary coherent 1-cell observables;
- normalization independence of arbitrary coherent 2-cell observables;
- preservation and reflection of intrinsic 2-cell invertibility;
- normalization independence of the Duskin intrinsic comparison `IsIso`
  predicate;
- coherent normalization independence for transported global edges.

Still open and not silently assumed:

1. existence of strictly-unitary normalization for every sufficiently general
   pseudofunctorial biequivalence;
2. canonical construction of a comparison between any two such
   normalizations;
3. a native pinned-Mathlib bundled `Icon` replacing the explicit certificate;
4. full preservation of the global scaling including degeneracy bookkeeping;
5. transport of chosen scaled-horn families and fillers;
6. equivalence of complete global `(∞,2)` models including all horn/fibrancy
   data;
7. independence of the final higher-model invariant from the chosen horn-family
   presentation.

The next mathematically coherent target is therefore the scaled/horn layer:
prove that normalized Duskin transport is a genuine scaled map, then formulate
and prove transport of admissible scaled-horn problems and fillers. This raises
the presentation-independent invariant from the intrinsic 2-skeleton to the
chosen global `(∞,2)` fibrancy interface without changing the parent dependent-
origination definition.
