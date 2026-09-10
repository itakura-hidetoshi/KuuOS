import KUOS.DependentOriginationIsoClassHigherLocalizationExistenceV2_55

namespace KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10

universe u v uH vH

/-!
# Pointwise W-adjoint-equivalence data v2.56

The v2.55 layer closes higher-localization factorization existence when every
arrow in `W` was already an isomorphism in the base category.  For general `W`,
the v2.10 admissibility condition is weaker: each `R.map w` is required only to
be an equivalence of categories.

Before introducing any additional global coherence assumption, it is important
to separate two logically different issues.

1. **Pointwise inversion:** for every `w ∈ W`, choose a quasi-inverse together
   with unit, counit, and the adjoint-equivalence triangle law.
2. **Coherent descent:** make all of those choices compatible with identities,
   composition, the pseudofunctor compositors, and the relations defining the
   presentation localization.

Mathlib already shows that the first issue carries no extra mathematical
obstruction.  A functor satisfying `Functor.IsEquivalence` canonically yields a
bundled half-adjoint equivalence via `Functor.asEquivalence`.

This file records that fact in the exact KuuOS higher-localization interface.  It
proves that weak `W`-admissibility is equivalent to the existence of pointwise
bundled adjoint-equivalence data whose forward functor is exactly `R.map w`.
Therefore the remaining general-W obstruction cannot be attributed merely to
choosing inverses one arrow at a time; it lies in the higher compatibility of
those choices across the localization relations.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Pointwise chosen half-adjoint equivalences on the images of the arrows in
`W`.

The bundled `CategoryTheory.Equivalence` contains a chosen inverse functor,
unit isomorphism, counit isomorphism, and the triangle law.  The second field
forces its forward functor to be exactly the underlying functor of `R.map f`, so
this datum cannot change the raw higher system or silently strictify it. -/
structure PointwiseWAdjointEquivalenceData
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)) where
  chosen :
    ∀ {X Y : Context} (f : X ⟶ Y), W f →
      R.obj (.mk X) ≌ R.obj (.mk Y)
  chosen_functor :
    ∀ {X Y : Context} (f : X ⟶ Y) (hf : W f),
      (chosen f hf).functor = (R.map f.toLoc).toFunctor

/-- Weak higher `W`-admissibility canonically supplies pointwise
half-adjoint-equivalence data.

No global strictification is used.  For each `f ∈ W`, the existing
`Functor.IsEquivalence` instance is passed directly to Mathlib's
`Functor.asEquivalence`. -/
noncomputable def pointwiseWAdjointEquivalenceDataOfAdmissible
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (hR : IsHigherWAdmissible W R) :
    PointwiseWAdjointEquivalenceData (W := W) R where
  chosen := by
    intro X Y f hf
    letI : (R.map f.toLoc).toFunctor.IsEquivalence := hR f hf
    exact (R.map f.toLoc).toFunctor.asEquivalence
  chosen_functor := by
    intro X Y f hf
    rfl

/-- Conversely, pointwise chosen adjoint-equivalence data implies the original
v2.10 weak admissibility condition. -/
theorem isHigherWAdmissible_of_pointwiseWAdjointEquivalenceData
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (D : PointwiseWAdjointEquivalenceData (W := W) R) :
    IsHigherWAdmissible W R := by
  intro X Y f hf
  rw [← D.chosen_functor f hf]
  infer_instance

/-- Exact pointwise normal form for weak higher `W`-admissibility.

Thus the existence of a quasi-inverse/unit/counit/triangle package for each
individual `W`-arrow is neither stronger nor weaker than v2.10 admissibility.
Any additional hypothesis needed for general higher-localization factorization
must therefore concern compatibility *between* these local packages. -/
theorem isHigherWAdmissible_iff_nonempty_pointwiseWAdjointEquivalenceData
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)) :
    IsHigherWAdmissible W R ↔
      Nonempty (PointwiseWAdjointEquivalenceData (W := W) R) := by
  constructor
  · intro hR
    exact ⟨pointwiseWAdjointEquivalenceDataOfAdmissible W hR⟩
  · rintro ⟨D⟩
    exact isHigherWAdmissible_of_pointwiseWAdjointEquivalenceData W D

/-- The chosen inverse functor can be recovered as an actual 1-cell of `Cat`.
This is a convenience projection for the next path-level localization layer. -/
noncomputable def PointwiseWAdjointEquivalenceData.inverse
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : Context} (f : X ⟶ Y) (hf : W f) :
    R.obj (.mk Y) ⟶ R.obj (.mk X) :=
  (Cat.Hom.equivFunctor (R.obj (.mk Y)) (R.obj (.mk X))).symm
    (D.chosen f hf).inverse

/-- The forward functor of the chosen adjoint equivalence is definitionally
anchored, through `chosen_functor`, to the original `R.map f` rather than to a
replacement presentation. -/
theorem PointwiseWAdjointEquivalenceData.forward_toFunctor_eq
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : Context} (f : X ⟶ Y) (hf : W f) :
    (D.chosen f hf).functor = (R.map f.toLoc).toFunctor :=
  D.chosen_functor f hf

/-!
## Boundary fixed by v2.56

The proved implication is exactly

```text
IsHigherWAdmissible W R
      ↕
for every w ∈ W:
  chosen half-adjoint equivalence
  with forward functor = R.map w.
```

This does **not** construct a pseudofunctor on `W.Localization` and does not yet
prove

```text
IsHigherWAdmissible W R
  ⇒ HasHigherLocalizationFactorization W R.
```

The next genuine obligation is now sharper.  Mathlib's canonical localization is
the quotient of the free path category generated by ordinary arrows and formal
`W`-inverses by the `id`, `comp`, `Winv₁`, and `Winv₂` relations.  The next layer
must express and then use coherence that transports the pointwise data above
through those relations, together with `R.mapId` and `R.mapComp`, so that the
result descends to an actual pseudofunctor on the localized source and yields the
v2.10 strong comparison.
-/

end KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
