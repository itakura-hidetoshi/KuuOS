import KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationCoherenceV5_02

namespace KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationTransportV5_03

open CategoryTheory
open CategoryTheory.Bicategory
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationExactUniversalAmbientStrongTransExtensionV4_95
open KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationNaturalityV4_97
open KUOS.DependentOriginationExactUniversalAmbientStrongTransCompositionNaturalityV4_99
open KUOS.DependentOriginationExactUniversalAmbientStrongTransIdentityNaturalityV5_01
open KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationCoherenceV5_02

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory
open scoped Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Presentation transport bridge v5.03

v5.02 proves identity and composition coherence on the raw presentation side.
The next bridge is controlled entirely by the coherence of the presentation
pseudofunctor.

For any 1-cell isomorphism `eta : f ≅ g` in the localized source, a
naturality isomorphism on `g` transports canonically back to one on `f`:

  F.map₂Iso(eta)
  -> naturality(g)
  -> G.map₂Iso(eta)^{-1}.

This file packages that construction once and exposes the exact decomposition
of the restricted pseudofunctor:

  restrict(F).mapId
    = F.map₂Iso(P.mapId) ≪≫ F.mapId,

  restrict(F).mapComp
    = F.map₂Iso(P.mapComp) ≪≫ F.mapComp,

where `P = (higherPresentationUnitFunctor W).toPseudofunctor`.

Using these two facts, we define the transported candidates associated to the
two presentation relations `id` and `comp`.  The next theorem unit only has
to prove that these transported candidates are equal to the canonical v4.97
presentation naturality choices.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Transport a StrongTrans naturality isomorphism backwards along an
isomorphism of source 1-cells. -/
noncomputable def higherLocalizedStrongTransNaturalityTransport
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {a b : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)}
    {f g : a ⟶ b}
    (eta : f ≅ g)
    (naturality_g :
      F.map g ≫ higherLocalizedStrongTransExtensionApp (W := W) gamma b ≅
        higherLocalizedStrongTransExtensionApp (W := W) gamma a ≫ G.map g) :
    F.map f ≫ higherLocalizedStrongTransExtensionApp (W := W) gamma b ≅
      higherLocalizedStrongTransExtensionApp (W := W) gamma a ≫ G.map f :=
  Bicategory.whiskerRightIso
      (F.map₂Iso eta)
      (higherLocalizedStrongTransExtensionApp (W := W) gamma b) ≪≫
    naturality_g ≪≫
    Bicategory.whiskerLeftIso
      (higherLocalizedStrongTransExtensionApp (W := W) gamma a)
      (G.map₂Iso eta).symm

/-- Hom expansion of the transport constructor. -/
theorem higherLocalizedStrongTransNaturalityTransport_hom
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {a b : LocallyDiscrete ((HigherLocalizedSite W)ᵒᵖ)}
    {f g : a ⟶ b}
    (eta : f ≅ g)
    (naturality_g :
      F.map g ≫ higherLocalizedStrongTransExtensionApp (W := W) gamma b ≅
        higherLocalizedStrongTransExtensionApp (W := W) gamma a ≫ G.map g) :
    (higherLocalizedStrongTransNaturalityTransport
        (W := W) gamma eta naturality_g).hom =
      F.map₂ eta.hom ▷
          higherLocalizedStrongTransExtensionApp (W := W) gamma b ≫
        naturality_g.hom ≫
        higherLocalizedStrongTransExtensionApp (W := W) gamma a ◁
          G.map₂ eta.inv := by
  simp [higherLocalizedStrongTransNaturalityTransport]

set_option backward.isDefEq.respectTransparency false in
/-- The restricted pseudofunctor identity comparison is the presentation
identity comparison mapped by `F`, followed by the localized `F.mapId`. -/
theorem restrictHigherLocalizedSystem_mapId_decomposition
    {F : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (X : LocallyDiscrete Context) :
    (restrictHigherLocalizedSystem W F).mapId X =
      F.map₂Iso
          ((higherPresentationUnitFunctor W).toPseudofunctor.mapId X) ≪≫
        F.mapId
          ((higherPresentationUnitFunctor W).toPseudofunctor.obj X) := by
  rfl

set_option backward.isDefEq.respectTransparency false in
/-- The restricted pseudofunctor composition comparison is the presentation
composition comparison mapped by `F`, followed by the localized
`F.mapComp`. -/
theorem restrictHigherLocalizedSystem_mapComp_decomposition
    {F : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    {X Y Z : LocallyDiscrete Context}
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    (restrictHigherLocalizedSystem W F).mapComp f g =
      F.map₂Iso
          ((higherPresentationUnitFunctor W).toPseudofunctor.mapComp f g) ≪≫
        F.mapComp
          ((higherPresentationUnitFunctor W).toPseudofunctor.map f)
          ((higherPresentationUnitFunctor W).toPseudofunctor.map g) := by
  rfl

/-- The transported localized identity constructor, now living on the raw
presentation image of an identity arrow. -/
noncomputable def higherLocalizedStrongTransPresentationIdentityTransport
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    (X : LocallyDiscrete Context) :
    F.map
          ((higherPresentationUnitFunctor W).toPseudofunctor.map (𝟙 X)) ≫
        higherLocalizedStrongTransExtensionApp (W := W) gamma
          ((higherPresentationUnitFunctor W).toPseudofunctor.obj X) ≅
      higherLocalizedStrongTransExtensionApp (W := W) gamma
          ((higherPresentationUnitFunctor W).toPseudofunctor.obj X) ≫
        G.map
          ((higherPresentationUnitFunctor W).toPseudofunctor.map (𝟙 X)) :=
  higherLocalizedStrongTransNaturalityTransport
    (W := W) gamma
    ((higherPresentationUnitFunctor W).toPseudofunctor.mapId X)
    (higherLocalizedStrongTransNaturality_id
      (W := W) gamma
      ((higherPresentationUnitFunctor W).toPseudofunctor.obj X))

/-- The transported localized composition constructor, now living on the raw
presentation image of the composite arrow. -/
noncomputable def higherLocalizedStrongTransPresentationCompositionTransport
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y Z : LocallyDiscrete Context}
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    F.map
          ((higherPresentationUnitFunctor W).toPseudofunctor.map (f ≫ g)) ≫
        higherLocalizedStrongTransExtensionApp (W := W) gamma
          ((higherPresentationUnitFunctor W).toPseudofunctor.obj Z) ≅
      higherLocalizedStrongTransExtensionApp (W := W) gamma
          ((higherPresentationUnitFunctor W).toPseudofunctor.obj X) ≫
        G.map
          ((higherPresentationUnitFunctor W).toPseudofunctor.map (f ≫ g)) :=
  higherLocalizedStrongTransNaturalityTransport
    (W := W) gamma
    ((higherPresentationUnitFunctor W).toPseudofunctor.mapComp f g)
    (higherLocalizedStrongTransNaturality_comp
      (W := W) gamma
      ((higherPresentationUnitFunctor W).toPseudofunctor.map f)
      ((higherPresentationUnitFunctor W).toPseudofunctor.map g)
      (higherLocalizedStrongTransPresentationNaturality (W := W) gamma f)
      (higherLocalizedStrongTransPresentationNaturality (W := W) gamma g))

/-! ## Regression checks -/

#print axioms higherLocalizedStrongTransNaturalityTransport
#print axioms higherLocalizedStrongTransNaturalityTransport_hom
#print axioms restrictHigherLocalizedSystem_mapId_decomposition
#print axioms restrictHigherLocalizedSystem_mapComp_decomposition
#print axioms higherLocalizedStrongTransPresentationIdentityTransport
#print axioms higherLocalizedStrongTransPresentationCompositionTransport

end

end KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationTransportV5_03
