import Mathlib.Tactic.CategoryTheory.BicategoryCoherence
import KUOS.DependentOriginationExactUniversalAmbientStrongTransWhiskerCompatibilityV5_06

namespace KUOS.DependentOriginationExactUniversalAmbientStrongTransCompositionCoherenceV5_06

open CategoryTheory
open CategoryTheory.Bicategory
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationExactUniversalAmbientStrongTransExtensionV4_95
open KUOS.DependentOriginationExactUniversalAmbientStrongTransCompositionNaturalityV4_99
open KUOS.DependentOriginationExactUniversalAmbientStrongTransIdentityNaturalityV5_01
open KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationTransportV5_03
open KUOS.DependentOriginationExactUniversalAmbientStrongTransWhiskerCompatibilityV5_06

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory
open scoped Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Composition coherence for canonical StrongTrans naturality v5.06

The v5.06 free-path evaluator normalizes singleton paths directly to generator
naturality.  To extend generator invariance through arbitrary retained
whiskering, we need the v4.99 composition constructor itself to be coherent
with the source bicategory unitors and associator.

These are purely bicategorical normalization theorems.  They do not use
localization relations.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Composing canonical identity naturality on the left with any supplied
naturality is the same as transporting that naturality along the source left
unitor. -/
theorem higherLocalizedStrongTransNaturality_comp_id_left
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {a b : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)}
    (f : a ⟶ b)
    (naturality_f :
      F.map f ≫ higherLocalizedStrongTransExtensionApp (W := W) gamma b ≅
        higherLocalizedStrongTransExtensionApp (W := W) gamma a ≫ G.map f) :
    higherLocalizedStrongTransNaturality_comp
        (W := W) gamma (𝟙 a) f
        (higherLocalizedStrongTransNaturality_id (W := W) gamma a)
        naturality_f =
      higherLocalizedStrongTransNaturalityTransport
        (W := W) gamma (λ_ f) naturality_f := by
  apply Iso.ext
  apply Cat.Hom₂.ext
  apply NatTrans.ext
  funext x
  have hnat :=
    naturality_f.hom.toNatTrans.naturality
      ((F.mapId a).inv.toNatTrans.app x)
  have hnat' :
      (higherLocalizedStrongTransExtensionApp (W := W) gamma b).toFunctor.map
            ((F.map f).toFunctor.map ((F.mapId a).inv.toNatTrans.app x)) ≫
          naturality_f.hom.toNatTrans.app
            ((F.map (𝟙 a)).toFunctor.obj x) =
        naturality_f.hom.toNatTrans.app x ≫
          (G.map f).toFunctor.map
            ((higherLocalizedStrongTransExtensionApp
              (W := W) gamma a).toFunctor.map
                ((F.mapId a).inv.toNatTrans.app x)) := by
    simpa only
      [Cat.Hom.comp_toFunctor, Functor.comp_obj, Functor.comp_map,
        Cat.Hom.id_toFunctor, Functor.id_obj] using hnat
  set_option backward.isDefEq.respectTransparency false in
    simp
      [-Pseudofunctor.map₂_left_unitor,
        higherLocalizedStrongTransNaturality_comp_hom,
        higherLocalizedStrongTransNaturality_id_hom,
        higherLocalizedStrongTransNaturalityTransport_hom,
        F.mapComp_id_left_hom_app,
        G.mapComp_id_left_inv_app,
        Strict.leftUnitor_eqToIso,
        PrelaxFunctor.map₂_eqToHom,
        eqToHom_map]
  slice_lhs 2 3 =>
    simp only
      [← Functor.map_comp,
        Cat.Hom.inv_hom_id_toNatTrans_app,
        Functor.map_id, Category.id_comp, Category.comp_id]

/-- Composing any supplied naturality with canonical identity naturality on the
right is the same as transporting along the source right unitor. -/
theorem higherLocalizedStrongTransNaturality_comp_id_right
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {a b : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)}
    (f : a ⟶ b)
    (naturality_f :
      F.map f ≫ higherLocalizedStrongTransExtensionApp (W := W) gamma b ≅
        higherLocalizedStrongTransExtensionApp (W := W) gamma a ≫ G.map f) :
    higherLocalizedStrongTransNaturality_comp
        (W := W) gamma f (𝟙 b)
        naturality_f
        (higherLocalizedStrongTransNaturality_id (W := W) gamma b) =
      higherLocalizedStrongTransNaturalityTransport
        (W := W) gamma (ρ_ f) naturality_f := by
  apply Iso.ext
  apply Cat.Hom₂.ext
  apply NatTrans.ext
  funext x
  have hnat :=
    (G.mapId b).hom.toNatTrans.naturality
      (naturality_f.hom.toNatTrans.app x)
  have hnat' :
      (G.map (𝟙 b)).toFunctor.map
            (naturality_f.hom.toNatTrans.app x) ≫
          (G.mapId b).hom.toNatTrans.app
            ((G.map f).toFunctor.obj
              ((higherLocalizedStrongTransExtensionApp
                (W := W) gamma a).toFunctor.obj x)) =
        (G.mapId b).hom.toNatTrans.app
            ((higherLocalizedStrongTransExtensionApp
              (W := W) gamma b).toFunctor.obj ((F.map f).toFunctor.obj x)) ≫
          naturality_f.hom.toNatTrans.app x := by
    simpa only
      [Cat.Hom.id_toFunctor, Functor.id_obj, Functor.id_map,
        Category.comp_id] using hnat
  set_option backward.isDefEq.respectTransparency false in
    simp
      [-Pseudofunctor.map₂_right_unitor,
        higherLocalizedStrongTransNaturality_comp_hom,
        higherLocalizedStrongTransNaturality_id_hom,
        higherLocalizedStrongTransNaturalityTransport_hom,
        F.mapComp_id_right_hom_app,
        G.mapComp_id_right_inv_app,
        Strict.rightUnitor_eqToIso,
        PrelaxFunctor.map₂_eqToHom,
        eqToHom_map]
  slice_lhs 2 3 => erw [hnat']
  simp only
    [← Functor.map_comp,
      Cat.Hom.inv_hom_id_toNatTrans_app,
      Functor.map_id, Category.id_comp, Category.comp_id,
      eqToHom_refl]

/-- The two parenthesizations of the v4.99 composition constructor agree after
transport along the source associator. -/
theorem higherLocalizedStrongTransNaturality_comp_assoc
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {a b c d : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)}
    (f : a ⟶ b) (g : b ⟶ c) (h : c ⟶ d)
    (naturality_f :
      F.map f ≫ higherLocalizedStrongTransExtensionApp (W := W) gamma b ≅
        higherLocalizedStrongTransExtensionApp (W := W) gamma a ≫ G.map f)
    (naturality_g :
      F.map g ≫ higherLocalizedStrongTransExtensionApp (W := W) gamma c ≅
        higherLocalizedStrongTransExtensionApp (W := W) gamma b ≫ G.map g)
    (naturality_h :
      F.map h ≫ higherLocalizedStrongTransExtensionApp (W := W) gamma d ≅
        higherLocalizedStrongTransExtensionApp (W := W) gamma c ≫ G.map h) :
    higherLocalizedStrongTransNaturality_comp
        (W := W) gamma (f ≫ g) h
        (higherLocalizedStrongTransNaturality_comp
          (W := W) gamma f g naturality_f naturality_g)
        naturality_h =
      higherLocalizedStrongTransNaturalityTransport
        (W := W) gamma (α_ f g h)
        (higherLocalizedStrongTransNaturality_comp
          (W := W) gamma f (g ≫ h)
          naturality_f
          (higherLocalizedStrongTransNaturality_comp
            (W := W) gamma g h naturality_g naturality_h)) := by
  apply Iso.ext
  apply Cat.Hom₂.ext
  apply NatTrans.ext
  funext x
  have hnatH :=
    naturality_h.hom.toNatTrans.naturality
      ((F.mapComp f g).hom.toNatTrans.app x)
  have hnatH' :
      (higherLocalizedStrongTransExtensionApp (W := W) gamma d).toFunctor.map
            ((F.map h).toFunctor.map
              ((F.mapComp f g).hom.toNatTrans.app x)) ≫
          naturality_h.hom.toNatTrans.app
            ((F.map g).toFunctor.obj ((F.map f).toFunctor.obj x)) =
        naturality_h.hom.toNatTrans.app
            ((F.map (f ≫ g)).toFunctor.obj x) ≫
          (G.map h).toFunctor.map
            ((higherLocalizedStrongTransExtensionApp
              (W := W) gamma c).toFunctor.map
                ((F.mapComp f g).hom.toNatTrans.app x)) := by
    simpa only
      [Cat.Hom.comp_toFunctor, Functor.comp_obj, Functor.comp_map] using hnatH
  have hnatG :=
    (G.mapComp g h).inv.toNatTrans.naturality
      (naturality_f.hom.toNatTrans.app x)
  have hnatG' :
      (G.map h).toFunctor.map
            ((G.map g).toFunctor.map
              (naturality_f.hom.toNatTrans.app x)) ≫
          (G.mapComp g h).inv.toNatTrans.app
            ((G.map f).toFunctor.obj
              ((higherLocalizedStrongTransExtensionApp
                (W := W) gamma a).toFunctor.obj x)) =
        (G.mapComp g h).inv.toNatTrans.app
            ((higherLocalizedStrongTransExtensionApp
              (W := W) gamma b).toFunctor.obj
                ((F.map f).toFunctor.obj x)) ≫
          (G.map (g ≫ h)).toFunctor.map
            (naturality_f.hom.toNatTrans.app x) := by
    simpa only
      [Cat.Hom.comp_toFunctor, Functor.comp_obj, Functor.comp_map] using hnatG
  set_option backward.isDefEq.respectTransparency false in
    simp
      [-Pseudofunctor.map₂_associator,
        higherLocalizedStrongTransNaturality_comp_hom,
        higherLocalizedStrongTransNaturalityTransport_hom,
        Strict.associator_eqToIso,
        PrelaxFunctor.map₂_eqToHom]
  slice_lhs 2 3 => erw [hnatH']
  slice_rhs 6 7 => erw [← hnatG']
  simp
    [F.mapComp_assoc_left_hom_app_assoc,
      G.mapComp_assoc_left_inv_app_assoc,
      Strict.associator_eqToIso,
      PrelaxFunctor.map₂_eqToHom]

/-! ## Regression checks -/

#print axioms higherLocalizedStrongTransNaturality_comp_id_left
#print axioms higherLocalizedStrongTransNaturality_comp_id_right
#print axioms higherLocalizedStrongTransNaturality_comp_assoc

end

end KUOS.DependentOriginationExactUniversalAmbientStrongTransCompositionCoherenceV5_06
