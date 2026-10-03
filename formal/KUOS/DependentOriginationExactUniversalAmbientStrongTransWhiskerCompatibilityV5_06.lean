import Mathlib.Tactic.CategoryTheory.BicategoryCoherence
import KUOS.DependentOriginationExactUniversalAmbientStrongTransGeneratorInvarianceV5_06

namespace KUOS.DependentOriginationExactUniversalAmbientStrongTransWhiskerCompatibilityV5_06

open CategoryTheory
open CategoryTheory.Bicategory
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationExactUniversalAmbientStrongTransExtensionV4_95
open KUOS.DependentOriginationExactUniversalAmbientStrongTransCompositionNaturalityV4_99
open KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationTransportV5_03
open KUOS.DependentOriginationExactUniversalAmbientStrongTransGeneratorInvarianceV5_06

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory
open scoped Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Whisker compatibility for retained StrongTrans naturality v5.06

The generated composition closure in v2.68 is obtained by left and right
whiskering retained localization generators.  This file isolates the generic
bicategorical fact needed for that structural descent:

transport of a StrongTrans naturality isomorphism along a source 2-isomorphism
commutes with the canonical v4.99 composition constructor, both in the first
and the second factor.

The proofs use the pinned Mathlib pseudofunctor laws
`map₂_whisker_left/right` and the bicategory coherence tactic.  No path syntax
or quotient proof is inspected here.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Transport in the first factor commutes with the canonical StrongTrans
composition constructor. -/
theorem higherLocalizedStrongTransNaturality_comp_transport_first
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {a b c : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)}
    {f g : a ⟶ b} (eta : f ≅ g)
    (naturality_g :
      F.map g ≫ higherLocalizedStrongTransExtensionApp (W := W) gamma b ≅
        higherLocalizedStrongTransExtensionApp (W := W) gamma a ≫ G.map g)
    (h : b ⟶ c)
    (naturality_h :
      F.map h ≫ higherLocalizedStrongTransExtensionApp (W := W) gamma c ≅
        higherLocalizedStrongTransExtensionApp (W := W) gamma b ≫ G.map h) :
    higherLocalizedStrongTransNaturality_comp
        (W := W) gamma f h
        (higherLocalizedStrongTransNaturalityTransport
          (W := W) gamma eta naturality_g)
        naturality_h =
      higherLocalizedStrongTransNaturalityTransport
        (W := W) gamma
        (Bicategory.whiskerRightIso eta h)
        (higherLocalizedStrongTransNaturality_comp
          (W := W) gamma g h naturality_g naturality_h) := by
  apply Iso.ext
  simp only
    [higherLocalizedStrongTransNaturality_comp_hom,
      higherLocalizedStrongTransNaturalityTransport_hom,
      Iso.trans_hom, Iso.symm_hom,
      whiskerLeftIso_hom, whiskerRightIso_hom,
      Pseudofunctor.map₂_whisker_right,
      Category.assoc]
  bicategory

/-- Transport in the second factor commutes with the canonical StrongTrans
composition constructor. -/
theorem higherLocalizedStrongTransNaturality_comp_transport_second
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {a b c : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)}
    (k : a ⟶ b)
    (naturality_k :
      F.map k ≫ higherLocalizedStrongTransExtensionApp (W := W) gamma b ≅
        higherLocalizedStrongTransExtensionApp (W := W) gamma a ≫ G.map k)
    {f g : b ⟶ c} (eta : f ≅ g)
    (naturality_g :
      F.map g ≫ higherLocalizedStrongTransExtensionApp (W := W) gamma c ≅
        higherLocalizedStrongTransExtensionApp (W := W) gamma b ≫ G.map g) :
    higherLocalizedStrongTransNaturality_comp
        (W := W) gamma k f
        naturality_k
        (higherLocalizedStrongTransNaturalityTransport
          (W := W) gamma eta naturality_g) =
      higherLocalizedStrongTransNaturalityTransport
        (W := W) gamma
        (Bicategory.whiskerLeftIso k eta)
        (higherLocalizedStrongTransNaturality_comp
          (W := W) gamma k g naturality_k naturality_g) := by
  apply Iso.ext
  simp only
    [higherLocalizedStrongTransNaturality_comp_hom,
      higherLocalizedStrongTransNaturalityTransport_hom,
      Iso.trans_hom, Iso.symm_hom,
      whiskerLeftIso_hom, whiskerRightIso_hom,
      Pseudofunctor.map₂_whisker_left,
      Category.assoc]
  bicategory

/-! ## Regression checks -/

#print axioms higherLocalizedStrongTransNaturality_comp_transport_first
#print axioms higherLocalizedStrongTransNaturality_comp_transport_second

end

end KUOS.DependentOriginationExactUniversalAmbientStrongTransWhiskerCompatibilityV5_06
