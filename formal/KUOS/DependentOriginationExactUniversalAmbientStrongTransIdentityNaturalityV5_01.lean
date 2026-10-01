import KUOS.DependentOriginationExactUniversalAmbientStrongTransAllArrowNaturalityV5_00

namespace KUOS.DependentOriginationExactUniversalAmbientStrongTransIdentityNaturalityV5_01

open CategoryTheory
open CategoryTheory.Bicategory
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationExactUniversalAmbientStrongTransExtensionV4_95
open KUOS.DependentOriginationExactUniversalAmbientStrongTransCompositionNaturalityV4_99
open KUOS.DependentOriginationExactUniversalAmbientStrongTransAllArrowNaturalityV5_00

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory
open scoped Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Canonical StrongTrans identity naturality v5.01

v5.00 proves existence of a StrongTrans naturality isomorphism on every
localized arrow.  That existence theorem is intentionally only propositional:
it does not make an arbitrary global choice, because such a choice would not
automatically satisfy the StrongTrans identity/composition coherence fields.

The identity arrow is different: pinned Mathlib already gives the canonical
formula used by every genuine StrongTrans,

  mapId(F)
  -> left unitor
  -> right unitor^{-1}
  -> mapId(G)^{-1}.

This file installs that formula directly for the canonical v4.95 object
component and proves the exact v4.96 `naturality_id` equation.

Thus future global assembly never needs to choose identity naturality from the
v5.00 `Nonempty` witness.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Canonical StrongTrans naturality isomorphism on an identity arrow.

This is exactly Mathlib's `Pseudofunctor.StrongTrans.naturality_id_iso`
formula with `alpha.app a` replaced by the canonical v4.95 extension
component. -/
noncomputable def higherLocalizedStrongTransNaturality_id
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    (a : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)) :
    F.map (𝟙 a) ≫
          higherLocalizedStrongTransExtensionApp (W := W) gamma a ≅
      higherLocalizedStrongTransExtensionApp (W := W) gamma a ≫
        G.map (𝟙 a) :=
  Bicategory.whiskerRightIso
      (F.mapId a)
      (higherLocalizedStrongTransExtensionApp (W := W) gamma a) ≪≫
    (λ_ (higherLocalizedStrongTransExtensionApp (W := W) gamma a)) ≪≫
    (ρ_ (higherLocalizedStrongTransExtensionApp (W := W) gamma a)).symm ≪≫
    Bicategory.whiskerLeftIso
      (higherLocalizedStrongTransExtensionApp (W := W) gamma a)
      (G.mapId a).symm

/-- Hom expansion of the canonical identity naturality.

Using the public projection lemmas rather than `rfl` keeps this theorem robust
against reducibility changes in composed isomorphisms. -/
theorem higherLocalizedStrongTransNaturality_id_hom
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    (a : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)) :
    (higherLocalizedStrongTransNaturality_id
      (W := W) gamma a).hom =
      (F.mapId a).hom ▷
          higherLocalizedStrongTransExtensionApp (W := W) gamma a ≫
        (λ_ (higherLocalizedStrongTransExtensionApp (W := W) gamma a)).hom ≫
        (ρ_ (higherLocalizedStrongTransExtensionApp (W := W) gamma a)).inv ≫
        higherLocalizedStrongTransExtensionApp (W := W) gamma a ◁
          (G.mapId a).inv := by
  simp only [higherLocalizedStrongTransNaturality_id,
    Iso.trans_hom, Iso.symm_hom, whiskerLeftIso_hom, whiskerRightIso_hom]

/-- The canonical identity choice satisfies exactly the `naturality_id` field
required by the v4.96 one-cell coherence extension. -/
theorem higherLocalizedStrongTransNaturality_id_coherence
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    (a : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)) :
    (higherLocalizedStrongTransNaturality_id
        (W := W) gamma a).hom ≫
          higherLocalizedStrongTransExtensionApp (W := W) gamma a ◁
            (G.mapId a).hom =
      (F.mapId a).hom ▷
          higherLocalizedStrongTransExtensionApp (W := W) gamma a ≫
        (λ_ (higherLocalizedStrongTransExtensionApp (W := W) gamma a)).hom ≫
        (ρ_ (higherLocalizedStrongTransExtensionApp (W := W) gamma a)).inv := by
  rw [higherLocalizedStrongTransNaturality_id_hom]
  simp

/-- The canonical identity is, in particular, a witness of the v5.00
all-arrow existence property. -/
theorem higherLocalizedStrongTransNaturality_id_mem
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    (a : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)) :
    HigherLocalizedStrongTransNaturalityExists
      (W := W) gamma (𝟙 a) :=
  ⟨higherLocalizedStrongTransNaturality_id (W := W) gamma a⟩

/-! ## Regression checks -/

#print axioms higherLocalizedStrongTransNaturality_id
#print axioms higherLocalizedStrongTransNaturality_id_hom
#print axioms higherLocalizedStrongTransNaturality_id_coherence
#print axioms higherLocalizedStrongTransNaturality_id_mem

end

end KUOS.DependentOriginationExactUniversalAmbientStrongTransIdentityNaturalityV5_01
