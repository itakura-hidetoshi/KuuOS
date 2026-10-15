import KUOS.DependentOriginationExactUniversalAmbientStrongTransLocallyDiscreteV4_96

namespace KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationNaturalityV4_97

open CategoryTheory
open Opposite
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationExactUniversalAmbientStrongTransExtensionV4_95
open KUOS.DependentOriginationExactUniversalAmbientStrongTransLocallyDiscreteV4_96

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory
open scoped Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Presentation-arrow StrongTrans naturality v4.97

v4.96 removes two-cell naturality as an independent obstruction because the
higher-localized source is locally discrete.  The next task is to construct the
one-cell naturality isomorphisms themselves.

This file closes the ordinary presentation-generator case.

For a raw StrongTrans

  gamma :
    restrictHigherLocalizedSystem W F ⟶
      restrictHigherLocalizedSystem W G,

its existing naturality isomorphism on a raw arrow already has exactly the
required localized type after the presentation pseudofunctor is unfolded and
the v4.95 canonical object extension is evaluated on presentation objects.

We package that isomorphism directly, and prove the exact forward modification
square required by v4.95.  Thus no weaker equality of naturality components is
introduced and no later identity-whisker rewrite is required.

The remaining generator problem after this unit is the formal inverse of a
W-arrow.  That inverse square should be constructed as the mate of the present
raw-image square under the pseudofunctor images of the localization
adjunctions, before closing under composition and quotient relations.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-!
Lean 4 elaboration note.

The transparency override below is intentionally scoped only to the canonical
presentation-naturality declaration.  Without it, elaborating the retyping of
`gamma.naturality f` can insert a dependent `cast`; the pretty-printed source
and target then look identical while their `.hom` fields are no longer
definitionally equal.  The following `_hom` theorem is therefore deliberately
proved by plain `rfl` as a regression check that no cast survives.

After that cast-free boundary is established, the restriction square uses
`change` only for definitional unfolding and delegates the remaining identity
whiskers/unit coherence to the `bicategory` tactic, rather than trying to
normalize bicategorical whiskering with ordinary category rewrites.
-/
set_option backward.isDefEq.respectTransparency false in
/-- Canonical StrongTrans naturality on an arrow in the image of the
presentation unit.  It is exactly the raw StrongTrans naturality, merely viewed
at its localized endpoints. -/
noncomputable def higherLocalizedStrongTransPresentationNaturality
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : LocallyDiscrete Context} (f : X ⟶ Y) :
    F.map ((higherPresentationUnitFunctor W).toPseudofunctor.map f) ≫
          higherLocalizedStrongTransExtensionApp (W := W) gamma
            ((higherPresentationUnitFunctor W).toPseudofunctor.obj Y) ≅
      higherLocalizedStrongTransExtensionApp (W := W) gamma
            ((higherPresentationUnitFunctor W).toPseudofunctor.obj X) ≫
        G.map ((higherPresentationUnitFunctor W).toPseudofunctor.map f) := by
  rcases X with ⟨X⟩
  rcases Y with ⟨Y⟩
  exact gamma.naturality f

/-- On a presentation arrow, the canonical localized naturality is literally
the raw naturality after exposing the restriction definitions. -/
theorem higherLocalizedStrongTransPresentationNaturality_hom
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : LocallyDiscrete Context} (f : X ⟶ Y) :
    (higherLocalizedStrongTransPresentationNaturality (W := W) gamma f).hom =
      (gamma.naturality f).hom := by
  rcases X with ⟨X⟩
  rcases Y with ⟨Y⟩
  rfl

/-- The presentation-arrow choice satisfies exactly the forward modification
square stored by v4.95.

This is deliberately stated in the exact field shape rather than as a weaker
equality followed by later whisker normalization. -/
theorem higherLocalizedStrongTransPresentationNaturality_restrictionSquare
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : LocallyDiscrete Context} (f : X ⟶ Y) :
    (restrictHigherLocalizedSystem W F).map f ◁
          𝟙
            (higherLocalizedStrongTransExtensionApp (W := W) gamma
              ((higherPresentationUnitFunctor W).toPseudofunctor.obj Y)) ≫
        (gamma.naturality f).hom =
      (higherLocalizedStrongTransPresentationNaturality (W := W) gamma f).hom ≫
        𝟙
            (higherLocalizedStrongTransExtensionApp (W := W) gamma
              ((higherPresentationUnitFunctor W).toPseudofunctor.obj X)) ▷
          (restrictHigherLocalizedSystem W G).map f := by
  rcases X with ⟨X⟩
  rcases Y with ⟨Y⟩
  change
    (restrictHigherLocalizedSystem W F).map f ◁
          𝟙
            (higherLocalizedStrongTransExtensionApp (W := W) gamma
              ((higherPresentationUnitFunctor W).toPseudofunctor.obj (.mk Y))) ≫
        (gamma.naturality f).hom =
      (gamma.naturality f).hom ≫
        𝟙
            (higherLocalizedStrongTransExtensionApp (W := W) gamma
              ((higherPresentationUnitFunctor W).toPseudofunctor.obj (.mk X))) ▷
          (restrictHigherLocalizedSystem W G).map f
  bicategory

/-- The raw-image part of the v4.96 reduced extension package therefore needs
no additional existence hypothesis: both the naturality isomorphism and its
exact restriction square are canonical. -/
theorem exists_higherLocalizedStrongTransPresentationNaturality
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : LocallyDiscrete Context} (f : X ⟶ Y) :
    ∃ e :
        F.map ((higherPresentationUnitFunctor W).toPseudofunctor.map f) ≫
              higherLocalizedStrongTransExtensionApp (W := W) gamma
                ((higherPresentationUnitFunctor W).toPseudofunctor.obj Y) ≅
          higherLocalizedStrongTransExtensionApp (W := W) gamma
                ((higherPresentationUnitFunctor W).toPseudofunctor.obj X) ≫
            G.map ((higherPresentationUnitFunctor W).toPseudofunctor.map f),
      (restrictHigherLocalizedSystem W F).map f ◁
            𝟙
              (higherLocalizedStrongTransExtensionApp (W := W) gamma
                ((higherPresentationUnitFunctor W).toPseudofunctor.obj Y)) ≫
          (gamma.naturality f).hom =
        e.hom ≫
          𝟙
              (higherLocalizedStrongTransExtensionApp (W := W) gamma
                ((higherPresentationUnitFunctor W).toPseudofunctor.obj X)) ▷
            (restrictHigherLocalizedSystem W G).map f := by
  exact
    ⟨higherLocalizedStrongTransPresentationNaturality (W := W) gamma f,
      higherLocalizedStrongTransPresentationNaturality_restrictionSquare
        (W := W) gamma f⟩

/-! ## Regression checks -/

#print axioms higherLocalizedStrongTransPresentationNaturality
#print axioms higherLocalizedStrongTransPresentationNaturality_hom
#print axioms higherLocalizedStrongTransPresentationNaturality_restrictionSquare
#print axioms exists_higherLocalizedStrongTransPresentationNaturality

end

end KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationNaturalityV4_97
