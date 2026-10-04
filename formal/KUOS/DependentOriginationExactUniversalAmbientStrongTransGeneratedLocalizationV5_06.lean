import KUOS.DependentOriginationExactUniversalAmbientStrongTransGeneratedCompClosureV5_06

namespace KUOS.DependentOriginationExactUniversalAmbientStrongTransGeneratedLocalizationV5_06

open CategoryTheory
open CategoryTheory.Bicategory
open Opposite
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68
open KUOS.DependentOriginationExactUniversalAmbientStrongTransExtensionV4_95
open KUOS.DependentOriginationExactUniversalAmbientStrongTransPresentationTransportV5_03
open KUOS.DependentOriginationExactUniversalAmbientStrongTransGeneratedRelationV5_06
open KUOS.DependentOriginationExactUniversalAmbientStrongTransGeneratedCompClosureV5_06

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory
open scoped Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Generated localization invariance v5.06

This file extends canonical StrongTrans path-naturality invariance from
`GeneratedCompClosure2Cell` to the full retained
`GeneratedLocalization2Cell` equivalence closure.

The source bicategory is locally discrete, so the exact equality proof used to
present a comparison 2-isomorphism is irrelevant once its source and target are
fixed.  The four constructors are therefore handled by:

* `ofCompClosure`: the v5.06 composition-closure theorem;
* `refl`: identity transport;
* `symm`: inverse-transport cancellation;
* `trans`: composition of transports.

No arbitrary relation witness is introduced.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Equality-induced source-arrow comparison attached to a fully retained
generated localization derivation. -/
noncomputable def higherLocalizedGeneratedLocalizationPathArrowIso
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (alpha : GeneratedLocalization2Cell W p q) :
    higherLocalizedPathArrow W p ≅ higherLocalizedPathArrow W q :=
  eqToIso (by
    change
      ((higherLocalizedPathQuotientFunctor W).map p).op.op.toLoc =
        ((higherLocalizedPathQuotientFunctor W).map q).op.op.toLoc
    exact
      congrArg (fun k => k.op.op.toLoc)
        (generatedLocalization2Cell_equalInLocalization W alpha))

/-- The canonical StrongTrans path naturality evaluator is invariant under the
full retained generated localization relation. -/
theorem higherLocalizedStrongTransPathNaturality_generatedLocalization_invariant
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (gamma :
      restrictHigherLocalizedSystem W F ⟶
        restrictHigherLocalizedSystem W G)
    {X Y : LocalizationPaths W} {p q : X ⟶ Y}
    (alpha : GeneratedLocalization2Cell W p q) :
    higherLocalizedStrongTransPathNaturality
        (W := W) gamma p =
      higherLocalizedStrongTransNaturalityTransport
        (W := W) gamma
        (higherLocalizedGeneratedLocalizationPathArrowIso
          (W := W) alpha)
        (higherLocalizedStrongTransPathNaturality
          (W := W) gamma q) := by
  induction alpha with
  | ofCompClosure alpha =>
      calc
        higherLocalizedStrongTransPathNaturality
              (W := W) gamma _ =
            higherLocalizedStrongTransNaturalityTransport
              (W := W) gamma
              (higherLocalizedGeneratedCompClosurePathArrowIso
                (W := W) alpha)
              (higherLocalizedStrongTransPathNaturality
                (W := W) gamma _) :=
          higherLocalizedStrongTransPathNaturality_generatedCompClosure_invariant
            (W := W) gamma alpha
        _ =
            higherLocalizedStrongTransNaturalityTransport
              (W := W) gamma
              (higherLocalizedGeneratedLocalizationPathArrowIso
                (W := W)
                (GeneratedLocalization2Cell.ofCompClosure alpha))
              (higherLocalizedStrongTransPathNaturality
                (W := W) gamma _) :=
          higherLocalizedStrongTransNaturalityTransport_eq_of_parallel_iso
            (W := W) gamma _ _ _
  | refl p =>
      calc
        higherLocalizedStrongTransPathNaturality
              (W := W) gamma p =
            higherLocalizedStrongTransNaturalityTransport
              (W := W) gamma
              (Iso.refl (higherLocalizedPathArrow W p))
              (higherLocalizedStrongTransPathNaturality
                (W := W) gamma p) :=
          (higherLocalizedStrongTransNaturalityTransport_refl
            (W := W) gamma
            (higherLocalizedPathArrow W p)
            (higherLocalizedStrongTransPathNaturality
              (W := W) gamma p)).symm
        _ =
            higherLocalizedStrongTransNaturalityTransport
              (W := W) gamma
              (higherLocalizedGeneratedLocalizationPathArrowIso
                (W := W) (GeneratedLocalization2Cell.refl p))
              (higherLocalizedStrongTransPathNaturality
                (W := W) gamma p) :=
          higherLocalizedStrongTransNaturalityTransport_eq_of_parallel_iso
            (W := W) gamma _ _ _
  | symm alpha ih =>
      let eta :=
        higherLocalizedGeneratedLocalizationPathArrowIso
          (W := W) alpha
      have hback :
          higherLocalizedStrongTransNaturalityTransport
              (W := W) gamma eta.symm
              (higherLocalizedStrongTransPathNaturality
                (W := W) gamma _) =
            higherLocalizedStrongTransPathNaturality
              (W := W) gamma _ := by
        have htransport :=
          congrArg
            (fun naturality_p =>
              higherLocalizedStrongTransNaturalityTransport
                (W := W) gamma eta.symm naturality_p)
            ih
        exact
          htransport.trans
            (higherLocalizedStrongTransNaturalityTransport_symm_left
              (W := W) gamma eta
              (higherLocalizedStrongTransPathNaturality
                (W := W) gamma _))
      calc
        higherLocalizedStrongTransPathNaturality
              (W := W) gamma _ =
            higherLocalizedStrongTransNaturalityTransport
              (W := W) gamma eta.symm
              (higherLocalizedStrongTransPathNaturality
                (W := W) gamma _) :=
          hback.symm
        _ =
            higherLocalizedStrongTransNaturalityTransport
              (W := W) gamma
              (higherLocalizedGeneratedLocalizationPathArrowIso
                (W := W) (GeneratedLocalization2Cell.symm alpha))
              (higherLocalizedStrongTransPathNaturality
                (W := W) gamma _) :=
          higherLocalizedStrongTransNaturalityTransport_eq_of_parallel_iso
            (W := W) gamma _ _ _
  | trans alpha beta ihAlpha ihBeta =>
      let etaAlpha :=
        higherLocalizedGeneratedLocalizationPathArrowIso
          (W := W) alpha
      let etaBeta :=
        higherLocalizedGeneratedLocalizationPathArrowIso
          (W := W) beta
      calc
        higherLocalizedStrongTransPathNaturality
              (W := W) gamma _ =
            higherLocalizedStrongTransNaturalityTransport
              (W := W) gamma etaAlpha
              (higherLocalizedStrongTransPathNaturality
                (W := W) gamma _) :=
          ihAlpha
        _ =
            higherLocalizedStrongTransNaturalityTransport
              (W := W) gamma etaAlpha
              (higherLocalizedStrongTransNaturalityTransport
                (W := W) gamma etaBeta
                (higherLocalizedStrongTransPathNaturality
                  (W := W) gamma _)) :=
          congrArg
            (fun naturality_q =>
              higherLocalizedStrongTransNaturalityTransport
                (W := W) gamma etaAlpha naturality_q)
            ihBeta
        _ =
            higherLocalizedStrongTransNaturalityTransport
              (W := W) gamma (etaAlpha ≪≫ etaBeta)
              (higherLocalizedStrongTransPathNaturality
                (W := W) gamma _) :=
          higherLocalizedStrongTransNaturalityTransport_trans
            (W := W) gamma etaAlpha etaBeta
            (higherLocalizedStrongTransPathNaturality
              (W := W) gamma _)
        _ =
            higherLocalizedStrongTransNaturalityTransport
              (W := W) gamma
              (higherLocalizedGeneratedLocalizationPathArrowIso
                (W := W) (GeneratedLocalization2Cell.trans alpha beta))
              (higherLocalizedStrongTransPathNaturality
                (W := W) gamma _) :=
          higherLocalizedStrongTransNaturalityTransport_eq_of_parallel_iso
            (W := W) gamma _ _ _

/-! ## Regression checks -/

#print axioms higherLocalizedGeneratedLocalizationPathArrowIso
#print axioms higherLocalizedStrongTransPathNaturality_generatedLocalization_invariant

end

end KUOS.DependentOriginationExactUniversalAmbientStrongTransGeneratedLocalizationV5_06
