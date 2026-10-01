import KUOS.DependentOriginationExactUniversalAmbientStrongTransTransportCompatibilityV5_04

namespace KUOS.DependentOriginationExactUniversalAmbientStrongTransWRelationCompatibilityV5_05

open CategoryTheory
open CategoryTheory.Functor
open CategoryTheory.Bicategory
open Opposite
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
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
      𝟙 (.mk (op (op X))) :=
  eqToIso (by
    apply Discrete.ext
    simp)

/-- The locally discrete 2-isomorphism recording inv followed by hom equals
identity for a localized base isomorphism. -/
noncomputable def higherLocalizedIsoInvHomRelation
    {X Y : LocalizedContext W} (e : X ≅ Y) :
    e.inv.op.op.toLoc ≫ e.hom.op.op.toLoc ≅
      𝟙 (.mk (op (op Y))) :=
  eqToIso (by
    apply Discrete.ext
    simp)

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
  let p := e.hom.op.op.toLoc
  let q := e.inv.op.op.toLoc
  let aX :=
    higherLocalizedStrongTransExtensionApp (W := W) gamma
      (.mk (op (op X)))
  let aY :=
    higherLocalizedStrongTransExtensionApp (W := W) gamma
      (.mk (op (op Y)))
  let nu :=
    higherLocalizedStrongTransNaturality_invOfIso
      (W := W) gamma e hp
  letI : (F.map p).toFunctor.IsEquivalence := by
    dsimp [p]
    exact
      pseudofunctor_map_of_isIso_isEquivalence
        F e.hom.op.op
  apply Iso.ext
  apply ((Functor.whiskeringLeft
    (F.obj (.mk (op (op X))))
    (F.obj (.mk (op (op Y))))
    (G.obj (.mk (op (op X))))).obj
      (F.map p).toFunctor).map_injective
  have hspec :=
    congrArg Iso.hom
      (higherLocalizedStrongTransNaturality_invOfIso_spec
        (W := W) gamma e hp)
  dsimp [p, q, aX, aY, nu] at hspec ⊢
  simp only
    [higherLocalizedStrongTransNaturality_comp_hom,
      higherLocalizedStrongTransNaturalityTransport_hom,
      higherLocalizedStrongTransNaturality_id_hom,
      higherLocalizedIsoHomInvRelation,
      Iso.trans_hom, Iso.symm_hom,
      whiskerLeftIso_hom, whiskerRightIso_hom]
  rw [hspec]
  dsimp [higherLocalizedStrongTransInverseWhiskeredSquare]
  bicategory

/-! ## Regression checks -/

#print axioms higherLocalizedIsoHomInvRelation
#print axioms higherLocalizedIsoInvHomRelation
#print axioms higherLocalizedStrongTransNaturality_hom_inv_transport

end

end KUOS.DependentOriginationExactUniversalAmbientStrongTransWRelationCompatibilityV5_05
