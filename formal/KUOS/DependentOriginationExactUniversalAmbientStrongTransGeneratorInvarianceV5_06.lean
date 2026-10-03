import KUOS.DependentOriginationExactUniversalAmbientStrongTransGeneratedRelationV5_06

namespace KUOS.DependentOriginationExactUniversalAmbientStrongTransGeneratorInvarianceV5_06

open CategoryTheory
open CategoryTheory.Functor
open Opposite
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68
open KUOS.DependentOriginationExactUniversalAmbientStrongTransExtensionV4_95
open KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationNaturalityV4_97
open KUOS.DependentOriginationExactUniversalAmbientStrongTransCompositionNaturalityV4_99
open KUOS.DependentOriginationExactUniversalAmbientStrongTransIdentityNaturalityV5_01
open KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationTransportV5_03
open KUOS.DependentOriginationExactUniversalAmbientStrongTransTransportCompatibilityV5_04
open KUOS.DependentOriginationExactUniversalAmbientStrongTransWRelationCompatibilityV5_05
open KUOS.DependentOriginationExactUniversalAmbientStrongTransGeneratedRelationV5_06

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory
open scoped Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Generator invariance for retained StrongTrans path naturality v5.06

The free-path evaluator from v5.06 is now compared across each of the four
retained localization generators from v2.68.

The comparison 2-isomorphism on source 1-cells is not chosen from quotient
equality.  It is the canonical structural isomorphism already used by the
validated generator compatibility theorems:

* `id`: the presentation pseudofunctor `mapId`;
* `comp`: the presentation pseudofunctor `mapComp`;
* `Winv₁`: the hom-inv relation of `Localization.Construction.wIso`;
* `Winv₂`: the inv-hom relation of `Localization.Construction.wIso`.

Thus no arbitrary v5.00 witness and no new relation language are introduced.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Canonical source-arrow comparison attached to one retained localization
generator.  This is the exact comparison already used by v5.04/v5.05. -/
noncomputable def higherLocalizedGeneratingPathArrowIso
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (alpha : LocalizationGenerating2Cell W p q) :
    higherLocalizedPathArrow W p ≅ higherLocalizedPathArrow W q := by
  cases alpha with
  | id X =>
      change
        (W.Q.map (𝟙 X)).op.op.toLoc ≅
          𝟙 (LocallyDiscrete.mk (op (op (W.Q.obj X))))
      exact
        (higherPresentationUnitFunctor W).toPseudofunctor.mapId (.mk X)
  | comp f g =>
      change
        (W.Q.map (f ≫ g)).op.op.toLoc ≅
          (W.Q.map f).op.op.toLoc ≫ (W.Q.map g).op.op.toLoc
      exact
        (higherPresentationUnitFunctor W).toPseudofunctor.mapComp
          f.toLoc g.toLoc
  | Winv₁ w hw =>
      simpa
        [higherLocalizedPathArrow, higherLocalizedPathObject,
          higherLocalizedPathQuotientFunctor, Functor.map_comp] using
        (higherLocalizedIsoHomInvRelation
          (W := W) (Localization.Construction.wIso w hw))
  | Winv₂ w hw =>
      simpa
        [higherLocalizedPathArrow, higherLocalizedPathObject,
          higherLocalizedPathQuotientFunctor, Functor.map_comp] using
        (higherLocalizedIsoInvHomRelation
          (W := W) (Localization.Construction.wIso w hw))

/-- The canonical v5.06 path naturality evaluator is invariant under one
retained localization generator, after transport along that generator's
canonical source-arrow comparison. -/
theorem higherLocalizedStrongTransPathNaturality_generating_invariant
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (alpha : LocalizationGenerating2Cell W p q) :
    higherLocalizedStrongTransPathNaturality
        (W := W) gamma p =
      higherLocalizedStrongTransNaturalityTransport
        (W := W) gamma
        (higherLocalizedGeneratingPathArrowIso (W := W) alpha)
        (higherLocalizedStrongTransPathNaturality
          (W := W) gamma q) := by
  cases alpha with
  | id X =>
      simpa
        [higherLocalizedGeneratingPathArrowIso,
          higherLocalizedStrongTransPathNaturality,
          higherLocalizedPathArrow, higherLocalizedPathObject,
          higherLocalizedPathQuotientFunctor, higherPresentationUnitFunctor] using
        (higherLocalizedStrongTransPresentationNaturality_id_transport
          (W := W) gamma (.mk X))
  | comp f g =>
      simpa
        [higherLocalizedGeneratingPathArrowIso,
          higherLocalizedStrongTransPathNaturality,
          higherLocalizedPathArrow, higherLocalizedPathObject,
          higherLocalizedPathQuotientFunctor, higherPresentationUnitFunctor,
          Functor.map_comp, op_comp, Quiver.Hom.comp_toLoc] using
        (higherLocalizedStrongTransPresentationNaturality_comp_transport
          (W := W) gamma f.toLoc g.toLoc)
  | Winv₁ w hw =>
      simpa
        [higherLocalizedGeneratingPathArrowIso,
          higherLocalizedStrongTransPathNaturality,
          higherLocalizedPathArrow, higherLocalizedPathObject,
          higherLocalizedPathQuotientFunctor, higherPresentationUnitFunctor,
          Functor.map_comp, op_comp, Quiver.Hom.comp_toLoc] using
        (higherLocalizedStrongTransNaturality_Winv1_transport
          (W := W) gamma w hw)
  | Winv₂ w hw =>
      simpa
        [higherLocalizedGeneratingPathArrowIso,
          higherLocalizedStrongTransPathNaturality,
          higherLocalizedPathArrow, higherLocalizedPathObject,
          higherLocalizedPathQuotientFunctor, higherPresentationUnitFunctor,
          Functor.map_comp, op_comp, Quiver.Hom.comp_toLoc] using
        (higherLocalizedStrongTransNaturality_Winv2_transport
          (W := W) gamma w hw)

/-! ## Regression checks -/

#print axioms higherLocalizedGeneratingPathArrowIso
#print axioms higherLocalizedStrongTransPathNaturality_generating_invariant

end

end KUOS.DependentOriginationExactUniversalAmbientStrongTransGeneratorInvarianceV5_06
