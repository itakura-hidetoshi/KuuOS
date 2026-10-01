import KUOS.DependentOriginationExactUniversalAmbientStrongTransCompositionNaturalityV4_99

namespace KUOS.DependentOriginationExactUniversalAmbientStrongTransAllArrowNaturalityV5_00

open CategoryTheory
open Opposite
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationExactUniversalAmbientStrongTransExtensionV4_95
open KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationNaturalityV4_97
open KUOS.DependentOriginationExactUniversalAmbientStrongTransWInverseNaturalityV4_98
open KUOS.DependentOriginationExactUniversalAmbientStrongTransCompositionNaturalityV4_99

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory
open scoped Bicategory

set_option autoImplicit false

noncomputable section

/-!
# All-arrow StrongTrans naturality existence v5.00

v4.97 constructs naturality on presentation-image arrows.
v4.98 proves stability under inversion of an isomorphism in the localized base.
v4.99 proves stability under composition.

Mathlib's constructed localization already packages exactly the generation
principle needed to combine these three facts:

  Localization.Construction.morphismProperty_eq_top'

A morphism property on the localized category is top once

* every arrow in the image of the presentation functor has the property;
* the property is stable under composition;
* for every isomorphism, the property passes from the forward arrow to its
  inverse.

Therefore there is no need to choose free-path representatives or to redo the
quotient relation induction.  This file packages StrongTrans naturality
existence as a MorphismProperty and applies the pinned Mathlib generator theorem
directly.

The result closes existence of a naturality isomorphism on every localized
one-cell.  It does not yet choose these isomorphisms coherently, so identity and
composition coherence for a global StrongTrans extension remain the next
obligation.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Existence of a StrongTrans naturality isomorphism, viewed as a property of
an ordinary morphism in the constructed localization.  The double opposite
restores the variance of the higher-localized site. -/
def higherLocalizedStrongTransNaturalityProperty
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G) :
    MorphismProperty (LocalizedContext W) :=
  fun _ _ f =>
    HigherLocalizedStrongTransNaturalityExists
      (W := W) gamma f.op.op.toLoc

/-- The property holds on every presentation-image arrow by v4.97. -/
theorem higherLocalizedStrongTransNaturalityProperty_map
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : Context} (f : X ⟶ Y) :
    higherLocalizedStrongTransNaturalityProperty
      (W := W) gamma (W.Q.map f) := by
  refine ⟨?_⟩
  simpa
      [higherLocalizedStrongTransNaturalityProperty,
        HigherLocalizedStrongTransNaturalityExists,
        higherPresentationUnitFunctor] using
    (higherLocalizedStrongTransPresentationNaturality
      (W := W) gamma f.toLoc)

/-- The property is stable under composition by v4.99. -/
theorem higherLocalizedStrongTransNaturalityProperty_comp
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y Z : LocalizedContext W}
    (f : X ⟶ Y) (g : Y ⟶ Z)
    (hf :
      higherLocalizedStrongTransNaturalityProperty (W := W) gamma f)
    (hg :
      higherLocalizedStrongTransNaturalityProperty (W := W) gamma g) :
    higherLocalizedStrongTransNaturalityProperty (W := W) gamma (f ≫ g) := by
  dsimp [higherLocalizedStrongTransNaturalityProperty] at hf hg ⊢
  simpa only [op_comp, Quiver.Hom.comp_toLoc] using
    (HigherLocalizedStrongTransNaturalityExists.comp
      (W := W) gamma f.op.op.toLoc g.op.op.toLoc hf hg)

/-- The property passes from an isomorphism to its inverse by v4.98. -/
theorem higherLocalizedStrongTransNaturalityProperty_inv
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : LocalizedContext W}
    (e : X ≅ Y)
    (h :
      higherLocalizedStrongTransNaturalityProperty
        (W := W) gamma e.hom) :
    higherLocalizedStrongTransNaturalityProperty
      (W := W) gamma e.inv := by
  rcases h with ⟨naturality_hom⟩
  exact
    ⟨higherLocalizedStrongTransNaturality_invOfIso
      (W := W) gamma e naturality_hom⟩

/-- Typeclass packaging of composition stability for Mathlib's localization
generator theorem. -/
instance higherLocalizedStrongTransNaturalityProperty_isStableUnderComposition
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G) :
    MorphismProperty.IsStableUnderComposition
      (higherLocalizedStrongTransNaturalityProperty (W := W) gamma) where
  comp_mem f g hf hg :=
    higherLocalizedStrongTransNaturalityProperty_comp
      (W := W) gamma f g hf hg

/-- StrongTrans naturality existence is therefore satisfied by every morphism of
Mathlib's constructed localization. -/
theorem higherLocalizedStrongTransNaturalityProperty_eq_top
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G) :
    higherLocalizedStrongTransNaturalityProperty (W := W) gamma = ⊤ := by
  exact
    Localization.Construction.morphismProperty_eq_top'
      (W := W)
      (higherLocalizedStrongTransNaturalityProperty (W := W) gamma)
      (fun {_ _} f =>
        higherLocalizedStrongTransNaturalityProperty_map
          (W := W) gamma f)
      (fun {_ _} e he =>
        higherLocalizedStrongTransNaturalityProperty_inv
          (W := W) gamma e he)

/-- Pointwise all-arrow form of the top-property theorem. -/
theorem higherLocalizedStrongTransNaturalityProperty_all
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : LocalizedContext W}
    (f : X ⟶ Y) :
    higherLocalizedStrongTransNaturalityProperty
      (W := W) gamma f := by
  rw [higherLocalizedStrongTransNaturalityProperty_eq_top
    (W := W) gamma]
  exact MorphismProperty.top_apply f

/-- Unpacked statement: every localized one-cell carries at least one
StrongTrans naturality isomorphism with the canonical v4.95 object
components. -/
theorem exists_higherLocalizedStrongTransNaturality_all
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : LocalizedContext W}
    (f : X ⟶ Y) :
    Nonempty
      (F.map f.op.op.toLoc ≫
            higherLocalizedStrongTransExtensionApp (W := W) gamma
              (.mk (op (op Y))) ≅
        higherLocalizedStrongTransExtensionApp (W := W) gamma
              (.mk (op (op X))) ≫
          G.map f.op.op.toLoc) := by
  exact
    higherLocalizedStrongTransNaturalityProperty_all
      (W := W) gamma f

/-! ## Regression checks -/

#print axioms higherLocalizedStrongTransNaturalityProperty_map
#print axioms higherLocalizedStrongTransNaturalityProperty_comp
#print axioms higherLocalizedStrongTransNaturalityProperty_inv
#print axioms higherLocalizedStrongTransNaturalityProperty_eq_top
#print axioms higherLocalizedStrongTransNaturalityProperty_all
#print axioms exists_higherLocalizedStrongTransNaturality_all

end

end KUOS.DependentOriginationExactUniversalAmbientStrongTransAllArrowNaturalityV5_00
