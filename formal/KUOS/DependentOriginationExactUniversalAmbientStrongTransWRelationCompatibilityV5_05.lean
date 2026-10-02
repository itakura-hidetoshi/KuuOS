import Mathlib.Tactic.CategoryTheory.Slice
import KUOS.DependentOriginationExactUniversalAmbientStrongTransTransportCompatibilityV5_04

namespace KUOS.DependentOriginationExactUniversalAmbientStrongTransWRelationCompatibilityV5_05

open CategoryTheory
open CategoryTheory.Functor
open CategoryTheory.Bicategory
open Opposite
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationHigherLocalizationNecessityV2_16
open KUOS.DependentOriginationExactUniversalAmbientStrongTransExtensionV4_95
open KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationNaturalityV4_97
open KUOS.DependentOriginationExactUniversalAmbientStrongTransWInverseNaturalityV4_98
open KUOS.DependentOriginationExactUniversalAmbientStrongTransCompositionNaturalityV4_99
open KUOS.DependentOriginationExactUniversalAmbientStrongTransIdentityNaturalityV5_01
open KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationTransportV5_03
open KUOS.DependentOriginationExactUniversalAmbientStrongTransTransportCompatibilityV5_04

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory
open scoped Bicategory

set_option autoImplicit false

noncomputable section

/-!
# W-inverse relation compatibility v5.05

The v4.98 inverse naturality constructor is characterized by an exact
fully-faithful preimage specification.  Here we use that specification together
with the unit/counit equalities of a localized isomorphism to close the two
remaining localization generators.

The generic statements are made for an arbitrary isomorphism in the localized
base.  The declared W-arrow cases are then immediate specializations to
Localization.Construction.wIso.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- The locally discrete 2-isomorphism recording hom followed by inv equals
identity for a localized base isomorphism. -/
noncomputable def higherLocalizedIsoHomInvRelation
    {X Y : LocalizedContext W} (e : X ≅ Y) :
    e.hom.op.op.toLoc ≫ e.inv.op.op.toLoc ≅
      𝟙 (LocallyDiscrete.mk (op (op X))) :=
  eqToIso (by
    apply Discrete.ext
    simp)

/-- The locally discrete 2-isomorphism recording inv followed by hom equals
identity for a localized base isomorphism. -/
noncomputable def higherLocalizedIsoInvHomRelation
    {X Y : LocalizedContext W} (e : X ≅ Y) :
    e.inv.op.op.toLoc ≫ e.hom.op.op.toLoc ≅
      𝟙 (LocallyDiscrete.mk (op (op Y))) :=
  eqToIso (by
    apply Discrete.ext
    simp)

/-- Functorial cancellation when an inverse-like morphism is already
composed with a following morphism.  The cancellation equality is supplied
explicitly so this lemma works directly with Cat 2-cell components, without
passing through the NatIso conversion and relying on definitional unfolding. -/
theorem functor_map_cancel_comp_assoc
    {C D : Type*} [Category C] [Category D]
    (H : C ⥤ D)
    {X Y Z : C} (f : X ⟶ Y) (g : Y ⟶ X) (r : X ⟶ Z)
    (hfg : f ≫ g = 𝟙 X)
    {T : D} (h : H.obj Z ⟶ T) :
    H.map f ≫ H.map (g ≫ r) ≫ h =
      H.map r ≫ h := by
  rw [H.map_comp]
  simp only [Category.assoc]
  rw [← H.map_comp_assoc, hfg, H.map_id, Category.id_comp]

/-- Functorial cancellation of an inverse-like pair when the second
morphism is already composed with one following morphism.  Unlike the reassociated
version below, this has no ambient tail metavariable, so it is stable under
`slice_lhs` on exactly two factors. -/
theorem functor_map_cancel_comp
    {C D : Type*} [Category C] [Category D]
    (H : C ⥤ D)
    {X Y Z : C} (f : X ⟶ Y) (g : Y ⟶ X) (r : X ⟶ Z)
    (hfg : f ≫ g = 𝟙 X) :
    H.map f ≫ H.map (g ≫ r) = H.map r := by
  rw [← H.map_comp]
  rw [← Category.assoc, hfg, Category.id_comp]

/-- Functorial cancellation of an inverse-like pair after applying a functor. -/
theorem functor_map_cancel
    {C D : Type*} [Category C] [Category D]
    (H : C ⥤ D)
    {X Y : C} (f : X ⟶ Y) (g : Y ⟶ X)
    (hfg : f ≫ g = 𝟙 X) :
    H.map f ≫ H.map g = 𝟙 (H.obj X) := by
  rw [← H.map_comp, hfg, H.map_id]

/-- Functorial cancellation of two explicitly supplied inverse-like
morphisms inside a longer composite.  Keeping the component morphisms explicit
avoids coercion-sensitive matching through NatIso wrappers. -/
theorem functor_map_cancel_assoc
    {C D : Type*} [Category C] [Category D]
    (H : C ⥤ D)
    {X Y : C} (f : X ⟶ Y) (g : Y ⟶ X)
    (hfg : f ≫ g = 𝟙 X)
    {T : D} (h : H.obj X ⟶ T) :
    H.map f ≫ H.map g ≫ h = h := by
  rw [← H.map_comp_assoc, hfg, H.map_id, Category.id_comp]

/-- Bicategorical hom form of the v4.98 fully-faithful specification.
This is the exact rewrite shape needed inside the v4.99 composition formula. -/
theorem higherLocalizedStrongTransNaturality_invOfIso_spec_hom
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : LocalizedContext W} (e : X ≅ Y)
    (hp :
      F.map e.hom.op.op.toLoc ≫
            higherLocalizedStrongTransExtensionApp (W := W) gamma
              (.mk (op (op Y))) ≅
        higherLocalizedStrongTransExtensionApp (W := W) gamma
              (.mk (op (op X))) ≫
          G.map e.hom.op.op.toLoc) :
    F.map e.hom.op.op.toLoc ◁
        (higherLocalizedStrongTransNaturality_invOfIso
          (W := W) gamma e hp).hom =
      (higherLocalizedStrongTransInverseWhiskeredSquare
        (W := W) gamma e hp).hom.toCatHom₂ := by
  apply Cat.Hom₂.ext
  change
    Functor.whiskerLeft
        (F.map e.hom.op.op.toLoc).toFunctor
        (higherLocalizedStrongTransNaturality_invOfIso
          (W := W) gamma e hp).hom.toNatTrans =
      (higherLocalizedStrongTransInverseWhiskeredSquare
        (W := W) gamma e hp).hom
  exact congrArg Iso.hom
    (higherLocalizedStrongTransNaturality_invOfIso_spec
      (W := W) gamma e hp)

/-- Generic hom-inv compatibility: composing a supplied forward naturality
with the canonical v4.98 inverse naturality gives exactly the canonical
identity naturality transported along the hom-inv relation. -/
theorem higherLocalizedStrongTransNaturality_hom_inv_transport
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : LocalizedContext W} (e : X ≅ Y)
    (hp :
      F.map e.hom.op.op.toLoc ≫
            higherLocalizedStrongTransExtensionApp (W := W) gamma
              (.mk (op (op Y))) ≅
        higherLocalizedStrongTransExtensionApp (W := W) gamma
              (.mk (op (op X))) ≫
          G.map e.hom.op.op.toLoc) :
    higherLocalizedStrongTransNaturality_comp
        (W := W) gamma
        e.hom.op.op.toLoc e.inv.op.op.toLoc
        hp
        (higherLocalizedStrongTransNaturality_invOfIso
          (W := W) gamma e hp) =
      higherLocalizedStrongTransNaturalityTransport
        (W := W) gamma
        (higherLocalizedIsoHomInvRelation (W := W) e)
        (higherLocalizedStrongTransNaturality_id
          (W := W) gamma (.mk (op (op X)))) := by
  apply Iso.ext
  apply Cat.Hom₂.ext
  apply NatTrans.ext
  funext x
  have hspec := congrArg
    (fun η => η.app x)
    (congrArg Iso.hom
      (higherLocalizedStrongTransNaturality_invOfIso_spec
        (W := W) gamma e hp))
  change
    (higherLocalizedStrongTransNaturality_invOfIso
        (W := W) gamma e hp).hom.toNatTrans.app
          ((F.map e.hom.op.op.toLoc).toFunctor.obj x) =
      (higherLocalizedStrongTransInverseWhiskeredSquare
        (W := W) gamma e hp).hom.app x at hspec
  simp only
    [higherLocalizedStrongTransNaturality_comp_hom,
      higherLocalizedStrongTransNaturalityTransport_hom,
      higherLocalizedStrongTransNaturality_id_hom,
      Cat.Hom₂.comp_app, Cat.whiskerLeft_app, Cat.whiskerRight_app]
  rw [hspec]
  dsimp
    [higherLocalizedStrongTransInverseWhiskeredSquare,
      higherLocalizedIsoHomInvRelation]
  simp only
    [Pseudofunctor.mapComp', Iso.trans_hom, Iso.trans_inv,
      PrelaxFunctor.map₂Iso_eqToIso, PrelaxFunctor.map₂_eqToHom,
      eqToIso.hom, eqToIso.inv]
  simp only
    [Cat.Hom.toNatTrans_comp, NatTrans.comp_app, CategoryTheory.Functor.map_comp,
      Category.id_comp, Category.comp_id]
  simp only [← Cat.Hom.toNatIso_hom, ← Cat.Hom.toNatIso_inv]
  slice_lhs 1 2 =>
    apply functor_map_cancel_comp
    exact Iso.hom_inv_id_app
      (Cat.Hom.toNatIso
        (F.mapComp e.hom.op.op.toLoc e.inv.op.op.toLoc)) x
  simp only [Category.assoc]
  slice_lhs 5 6 =>
    apply functor_map_cancel
    exact Iso.inv_hom_id_app (Cat.Hom.toNatIso hp) x
  simp only [Category.id_comp, Category.comp_id]
  slice_lhs 4 5 =>
    exact Iso.hom_inv_id_app
      (Cat.Hom.toNatIso
        (G.mapComp e.hom.op.op.toLoc e.inv.op.op.toLoc))
      ((higherLocalizedStrongTransExtensionApp
        (W := W) gamma (.mk (op (op X)))).toFunctor.obj x)
  simp

/-! ## Regression checks -/

#print axioms higherLocalizedIsoHomInvRelation
#print axioms higherLocalizedIsoInvHomRelation
#print axioms functor_map_cancel_comp
#print axioms functor_map_cancel
#print axioms functor_map_cancel_comp_assoc
#print axioms functor_map_cancel_assoc
#print axioms higherLocalizedStrongTransNaturality_invOfIso_spec_hom
#print axioms higherLocalizedStrongTransNaturality_hom_inv_transport

end

end KUOS.DependentOriginationExactUniversalAmbientStrongTransWRelationCompatibilityV5_05
