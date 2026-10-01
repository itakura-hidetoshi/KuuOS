import KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationTransportV5_03

namespace KUOS.DependentOriginationExactUniversalAmbientStrongTransTransportCompatibilityV5_04

open CategoryTheory
open CategoryTheory.Bicategory
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationExactUniversalAmbientStrongTransExtensionV4_95
open KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationNaturalityV4_97
open KUOS.DependentOriginationExactUniversalAmbientStrongTransCompositionNaturalityV4_99
open KUOS.DependentOriginationExactUniversalAmbientStrongTransIdentityNaturalityV5_01
open KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationCoherenceV5_02
open KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationTransportV5_03

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory
open scoped Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Identity/composition transport compatibility v5.04

v5.02 identifies the canonical v4.97 presentation naturality on identities and
composites with the native StrongTrans identity/composition formulas for the
restricted pseudofunctors.

v5.03 decomposes those restricted comparison isomorphisms through the
presentation pseudofunctor and defines the corresponding transported localized
candidates.

This file closes the remaining data-level comparison for the first two
localization generators:

* the transported canonical localized identity naturality is exactly the
  canonical presentation naturality of the raw identity;
* the transported canonical localized composition naturality is exactly the
  canonical presentation naturality of the raw composite.

Thus the identity and composition generators introduce no ambiguity in the
canonical naturality evaluator. The remaining generator-level work is the
Winv1/Winv2 pair.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- The v4.97 presentation naturality of an identity is exactly the v5.03
transport of the v5.01 canonical localized identity naturality along the
presentation pseudofunctor mapId isomorphism. -/
theorem higherLocalizedStrongTransPresentationNaturality_id_transport
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    (X : LocallyDiscrete Context) :
    higherLocalizedStrongTransPresentationNaturality
        (W := W) gamma (𝟙 X) =
      higherLocalizedStrongTransPresentationIdentityTransport
        (W := W) gamma X := by
  rw [higherLocalizedStrongTransPresentationNaturality_id_iso]
  apply Iso.ext
  simp only
    [higherLocalizedStrongTransPresentationIdentityTransport,
      higherLocalizedStrongTransNaturalityTransport_hom,
      higherLocalizedStrongTransNaturality_id_hom,
      restrictHigherLocalizedSystem_mapId_decomposition,
      Iso.trans_hom, Iso.symm_hom, whiskerLeftIso_hom, whiskerRightIso_hom]
  bicategory

/-- The v4.97 presentation naturality of a composite is exactly the v5.03
transport of the v4.99 canonical localized composition naturality along the
presentation pseudofunctor mapComp isomorphism. -/
theorem higherLocalizedStrongTransPresentationNaturality_comp_transport
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y Z : LocallyDiscrete Context}
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    higherLocalizedStrongTransPresentationNaturality
        (W := W) gamma (f ≫ g) =
      higherLocalizedStrongTransPresentationCompositionTransport
        (W := W) gamma f g := by
  rw [higherLocalizedStrongTransPresentationNaturality_comp_iso]
  apply Iso.ext
  simp only
    [higherLocalizedStrongTransPresentationCompositionTransport,
      higherLocalizedStrongTransNaturalityTransport_hom,
      higherLocalizedStrongTransNaturality_comp_hom,
      restrictHigherLocalizedSystem_mapComp_decomposition,
      Iso.trans_hom, Iso.symm_hom, whiskerLeftIso_hom, whiskerRightIso_hom]
  bicategory

/-! ## Regression checks -/

#print axioms higherLocalizedStrongTransPresentationNaturality_id_transport
#print axioms higherLocalizedStrongTransPresentationNaturality_comp_transport

end

end KUOS.DependentOriginationExactUniversalAmbientStrongTransTransportCompatibilityV5_04
