import KUOS.DependentOriginationInversePairBoundaryObstructionV3_55

namespace KUOS.DependentOriginationInversePairRepresentativeEquivalenceV3_56

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationGeneratedPointwiseChoiceV2_68
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationFiniteAssociatorScheduleV3_38
open KUOS.DependentOriginationCompositeIdentityInversePairReductionV3_54
open KUOS.DependentOriginationInversePairBoundaryObstructionV3_55

universe u v uH vH

set_option autoImplicit false

noncomputable section

/-!
# Inverse-pair representative equivalence v3.56

v3.55 proves that every surviving fresh-boundary obstruction under the v3.52
cancellation geometry lies over a two-sided inverse pair and that the two
chosen quotient representative evaluations are each essentially surjective
and faithful.

The source equation is stronger than those directional properties.  For

```text
f : X ⟶ Y
g : Y ⟶ X
f ≫ g = 𝟙 X
g ≫ f = 𝟙 Y,
```

the canonical generated composition comparisons give

```text
QRep(f) ⋙ QRep(g) ≅ QRep(𝟙 X)
QRep(g) ⋙ QRep(f) ≅ QRep(𝟙 Y),
```

and the canonical generated identity comparisons identify the right-hand
terms with identity functors.  Mathlib's `Functor.IsEquivalence.mk'` therefore
upgrades both representative functors to actual equivalences of categories.

This removes any remaining one-categorical weakness from the inverse-pair
boundary sector.  It still does not force the v3.47 leading gauge equation:
v2.69 already demonstrates within the KuuOS formal spine that pointwise
equivalence of all mapped arrows does not by itself remove nontrivial
automorphism-valued compositor/holonomy data.  Hence this module deliberately
separates representative equivalence from the still-open two-dimensional
coherence obstruction.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (R : RawHigherContextualSystem.{u, v, uH, vH}
  (Context := Context))
variable (D : PointwiseWAdjointEquivalenceData (W := W) R)

/-- A two-sided inverse pair in the localization makes the chosen quotient
representative of the first arrow an equivalence of categories. -/
theorem quotientRepresentativeMap_isEquivalence_of_inversePair_left
    {X Y : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ X)
    (hfg : f ≫ g = 𝟙 X)
    (hgf : g ≫ f = 𝟙 Y) :
    (quotientRepresentativeMap W R D f).toFunctor.IsEquivalence := by
  apply Functor.IsEquivalence.mk'
    (quotientRepresentativeMap W R D g).toFunctor
  · apply Cat.Hom.toNatIso
    refine (generatedIdentityMapIso W R D X).symm ≪≫ ?_
    simpa only [hfg] using
      (generatedCompositionMapIso W R D f g)
  · apply Cat.Hom.toNatIso
    refine ?_ ≪≫ generatedIdentityMapIso W R D Y
    simpa only [hgf] using
      (generatedCompositionMapIso W R D g f).symm

/-- The inverse arrow has the same representative-equivalence property. -/
theorem quotientRepresentativeMap_isEquivalence_of_inversePair_right
    {X Y : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ X)
    (hfg : f ≫ g = 𝟙 X)
    (hgf : g ≫ f = 𝟙 Y) :
    (quotientRepresentativeMap W R D g).toFunctor.IsEquivalence := by
  apply Functor.IsEquivalence.mk'
    (quotientRepresentativeMap W R D f).toFunctor
  · apply Cat.Hom.toNatIso
    refine (generatedIdentityMapIso W R D Y).symm ≪≫ ?_
    simpa only [hgf] using
      (generatedCompositionMapIso W R D g f)
  · apply Cat.Hom.toNatIso
    refine ?_ ≪≫ generatedIdentityMapIso W R D X
    simpa only [hfg] using
      (generatedCompositionMapIso W R D f g).symm

/-- Package both equivalences in one theorem. -/
theorem inversePair_representative_isEquivalence
    {X Y : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ X)
    (hfg : f ≫ g = 𝟙 X)
    (hgf : g ≫ f = 𝟙 Y) :
    (quotientRepresentativeMap W R D f).toFunctor.IsEquivalence ∧
      (quotientRepresentativeMap W R D g).toFunctor.IsEquivalence := by
  exact
    ⟨quotientRepresentativeMap_isEquivalence_of_inversePair_left
        W R D f g hfg hgf,
      quotientRepresentativeMap_isEquivalence_of_inversePair_right
        W R D f g hfg hgf⟩

/-- In particular every isomorphism of the ordinary localization category has
an equivalent chosen quotient representative evaluation. -/
theorem quotientRepresentativeMap_isEquivalence_of_isIso
    {X Y : W.Localization} (f : X ⟶ Y) [IsIso f] :
    (quotientRepresentativeMap W R D f).toFunctor.IsEquivalence := by
  exact
    quotientRepresentativeMap_isEquivalence_of_inversePair_left
      W R D f (inv f)
        (IsIso.hom_inv_id f)
        (IsIso.inv_hom_id f)

/-- Task-packaged form for the v3.54 inverse-pair sector. -/
theorem inversePairTask_representative_isEquivalence
    (a : AssociatorTask W)
    (hInverse : IsCompositeInversePairAssociatorTask W a) :
    (quotientRepresentativeMap W R D a.f).toFunctor.IsEquivalence ∧
      (quotientRepresentativeMap W R D a.g).toFunctor.IsEquivalence := by
  rcases hInverse with ⟨X, Y, T, f, g, h, hfg, hgf, rfl⟩
  exact inversePair_representative_isEquivalence
    W R D f g hfg hgf

/-- Every surviving v3.55 inverse-pair fresh-boundary obstruction therefore
already lives over representative functor equivalences.  Failure of correction
cannot be attributed to lack of representative essential surjectivity,
faithfulness, or categorical equivalence. -/
theorem inversePairFreshBoundaryObstruction_representative_isEquivalence
    (Q : GeneratedQuotientGaugeParameters W R D)
    (a : AssociatorTask W)
    (hObstruction :
      InversePairFreshBoundaryLeadingObstruction W R D Q a) :
    (quotientRepresentativeMap W R D a.f).toFunctor.IsEquivalence ∧
      (quotientRepresentativeMap W R D a.g).toFunctor.IsEquivalence := by
  exact inversePairTask_representative_isEquivalence
    W R D a hObstruction.2.1

/-!
## Boundary after v3.56

The inverse-pair residual is now fully separated from one-categorical
representative defects:

```text
inverse pair in W.Localization
  -> both chosen quotient representatives are category equivalences.
```

Nevertheless v3.55's exact obstruction remains a leading `gComp`
compatibility equation.  Equivalence of the representative 1-morphisms makes
whiskering cancellable, but it does not identify arbitrary automorphism-valued
composition gauges with the unique value demanded by associativity.

The next useful globalization is semantic rather than algebraic: reuse
`Localization.Construction.morphismProperty_eq_top` with the multiplicative
v3.33 EssSurj/Faithful sectors.  Under global left source complements every
quotient representative should be essentially surjective; under global right
source complements every representative should be faithful.  This would
globalize v3.28 separation exactly as v3.52 globalized ordinary Epi/Mono.

No automatic inverse-pair boundary correction, schedule/seed/W/R/D
independence, comparison-gauge equations, Stage I, Stage II, or final
universality is asserted here.  Protected validation-only PR #1558 is
untouched.
-/

end

end KUOS.DependentOriginationInversePairRepresentativeEquivalenceV3_56
