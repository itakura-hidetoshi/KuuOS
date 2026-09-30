import KUOS.DependentOriginationExactUniversalAmbientCoverageReductionV4_90

namespace KUOS.DependentOriginationExactUniversalAmbientRestrictionUniversalityV4_91

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationExactHigherPresentationSectorV4_50
open KUOS.DependentOriginationExactPresentationEssentialUniquenessV4_53
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70
open KUOS.DependentOriginationExactUniversalLabelledBiequivalenceV4_89
open KUOS.DependentOriginationExactUniversalAmbientCoverageReductionV4_90

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory
open scoped Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Ambient restriction universality reduction v4.91

v4.90 reduces ambient Whitehead biequivalence for the actual v4.70 realization
to essential surjectivity on ambient DO₂ objects.

The next question is whether an arbitrary ambient object can itself be used as
the carrier of an exact-universal source object. There is a tautological first
half: if Z is already an object of DO₂, restrict its localized pseudofunctor
back to the raw context and present that raw system by Z itself. The comparison
is the identity StrongTrans and is pointwise an equivalence.

The non-tautological half is exactly the universal field of
ExactUniversalRawObject: the tautological exact presentation must be a
coherent universal target among all exact presentations of the same raw
restriction.

This file isolates that remaining condition. If every ambient object's
tautological restriction presentation is a coherent universal target, then
there is not merely essential object coverage: each ambient Z is literally the
carrier of a constructed source object. Hence v4.90 immediately yields ambient
Whitehead biequivalence data.

No claim is made here that this restriction-universality condition holds
unconditionally.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

abbrev Source :=
  ExactUniversalRawObject.{u, v, uH, vH} (W := W) A

/-- Raw system obtained by restricting one ambient DO₂ object along the
presentation-localization unit. -/
abbrev exactUniversalAmbientRestrictionRaw
    (Z : DependentOriginationCompletion2.{u, v, uH, uH, vH} (W := W) A) :
    RawHigherContextualSystem.{u, v, uH, vH} (Context := Context) :=
  restrictHigherLocalizedSystem W
    (higherStackObjectVal (W := W) A Z)

/-- Tautological exact presentation of the raw restriction of an ambient
object. The carrier is Z itself and the comparison is identity. -/
noncomputable def exactUniversalAmbientRestrictionPresentation
    (Z : DependentOriginationCompletion2.{u, v, uH, uH, vH} (W := W) A) :
    ExactHigherDependentOriginationPresentation
      (W := W) A
      (exactUniversalAmbientRestrictionRaw (W := W) A Z) where
  carrier := Z
  comparison := 𝟙 _
  comparison_isEquivalence := by
    intro X
    change
      (𝟭 ((exactUniversalAmbientRestrictionRaw
        (W := W) A Z).obj (.mk X))).IsEquivalence
    infer_instance

@[simp] theorem exactUniversalAmbientRestrictionPresentation_carrier
    (Z : DependentOriginationCompletion2.{u, v, uH, uH, vH} (W := W) A) :
    (exactUniversalAmbientRestrictionPresentation
      (W := W) A Z).carrier = Z :=
  rfl

@[simp] theorem exactUniversalAmbientRestrictionPresentation_comparison
    (Z : DependentOriginationCompletion2.{u, v, uH, uH, vH} (W := W) A) :
    (exactUniversalAmbientRestrictionPresentation
      (W := W) A Z).comparison = 𝟙 _ :=
  rfl

/-- The remaining non-tautological condition for one ambient object: its
identity-comparison restriction presentation is a coherent universal target. -/
def HasExactUniversalAmbientRestrictionUniversalTarget
    (Z : DependentOriginationCompletion2.{u, v, uH, uH, vH} (W := W) A) : Prop :=
  Nonempty
    (ExactPresentationCoherentUniversalTarget
      (W := W) A
      (exactUniversalAmbientRestrictionPresentation
        (W := W) A Z))

/-- Uniform restriction-universality over all ambient DO₂ objects.

The target-category universe `vH` occurs only inside this proposition's body,
not in the term parameters `W` or `A`.  Consequently callers must instantiate
this declaration explicitly as `.{u, v, uH, vH}`; otherwise Lean is free to
introduce a fresh universe metavariable for the final DO₂ level. -/
def ExactUniversalAmbientRestrictionUniversality : Prop :=
  ∀ Z : DependentOriginationCompletion2.{u, v, uH, uH, vH} (W := W) A,
    HasExactUniversalAmbientRestrictionUniversalTarget.{u, v, uH, vH}
      (W := W) A Z

/-- Once the tautological restriction presentation of Z is universal, it
packages directly as an exact-universal source object whose carrier is exactly
Z. -/
def exactUniversalAmbientSourceOfRestrictionUniversalTarget
    (Z : DependentOriginationCompletion2.{u, v, uH, uH, vH} (W := W) A)
    (T :
      ExactPresentationCoherentUniversalTarget
        (W := W) A
        (exactUniversalAmbientRestrictionPresentation
          (W := W) A Z)) :
    Source (W := W) A where
  raw := exactUniversalAmbientRestrictionRaw (W := W) A Z
  presentation :=
    exactUniversalAmbientRestrictionPresentation (W := W) A Z
  universal := T

@[simp] theorem exactUniversalAmbientSourceOfRestrictionUniversalTarget_carrier
    (Z : DependentOriginationCompletion2.{u, v, uH, uH, vH} (W := W) A)
    (T :
      ExactPresentationCoherentUniversalTarget
        (W := W) A
        (exactUniversalAmbientRestrictionPresentation
          (W := W) A Z)) :
    (exactUniversalAmbientSourceOfRestrictionUniversalTarget
      (W := W) A Z T).carrier = Z :=
  rfl

/-- Objectwise restriction universality gives the stronger strict statement that
some source object has carrier literally equal to the prescribed ambient
object. -/
theorem exists_exactUniversalAmbientSource_carrier_eq
    (Z : DependentOriginationCompletion2.{u, v, uH, uH, vH} (W := W) A)
    (hZ :
      HasExactUniversalAmbientRestrictionUniversalTarget.{u, v, uH, vH}
        (W := W) A Z) :
    ∃ X : Source (W := W) A, X.carrier = Z := by
  rcases hZ with ⟨T⟩
  exact
    ⟨exactUniversalAmbientSourceOfRestrictionUniversalTarget
      (W := W) A Z T, rfl⟩

/-- Uniform restriction universality therefore discharges the v4.90 ambient
object-coverage condition. -/
theorem exactUniversalAmbientObjectCoverage_of_restrictionUniversality
    (hU :
      ExactUniversalAmbientRestrictionUniversality.{u, v, uH, vH}
        (W := W) A) :
    ExactUniversalAmbientObjectCoverage.{u, v, uH, vH}
      (W := W) A := by
  intro Z
  rcases hU Z with ⟨T⟩
  refine
    ⟨exactUniversalAmbientSourceOfRestrictionUniversalTarget
      (W := W) A Z T, ?_⟩
  change Nonempty (Bicategory.Equivalence Z Z)
  exact ⟨Bicategory.Equivalence.id Z⟩

/-- Hence the actual v4.70 realization has ambient Whitehead data under exactly
this sharpened canonical restriction-universality hypothesis. -/
def exactUniversalAmbientWhiteheadBiequivalenceOfRestrictionUniversality
    (hU :
      ExactUniversalAmbientRestrictionUniversality.{u, v, uH, vH}
        (W := W) A) :
    WhiteheadBiequivalenceData
      (ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
      (DependentOriginationCompletion2.{u, v, uH, uH, vH}
        (W := W) A) :=
  exactUniversalAmbientWhiteheadBiequivalenceOfCoverage.{u, v, uH, vH}
    (W := W) A
    (exactUniversalAmbientObjectCoverage_of_restrictionUniversality.{u, v, uH, vH}
      (W := W) A hU)

/-- Existence form of the same consequence, matching the v4.90 reduction
interface. -/
theorem exactUniversalAmbientWhiteheadExistence_of_restrictionUniversality
    (hU :
      ExactUniversalAmbientRestrictionUniversality.{u, v, uH, vH}
        (W := W) A) :
    ExactUniversalAmbientWhiteheadExistence.{u, v, uH, vH}
      (W := W) A :=
  (exactUniversalAmbientWhiteheadExistence_iff_objectCoverage.{u, v, uH, vH}
    (W := W) A).2
    (exactUniversalAmbientObjectCoverage_of_restrictionUniversality.{u, v, uH, vH}
      (W := W) A hU)

/-! ## Regression checks -/

variable (Z : DependentOriginationCompletion2.{u, v, uH, uH, vH} (W := W) A)

example :
    (exactUniversalAmbientRestrictionPresentation
      (W := W) A Z).carrier = Z :=
  rfl

example
    (T :
      ExactPresentationCoherentUniversalTarget
        (W := W) A
        (exactUniversalAmbientRestrictionPresentation
          (W := W) A Z)) :
    (exactUniversalAmbientSourceOfRestrictionUniversalTarget
      (W := W) A Z T).carrier = Z :=
  rfl

example
    (hU :
      ExactUniversalAmbientRestrictionUniversality.{u, v, uH, vH}
        (W := W) A) :
    ExactUniversalAmbientObjectCoverage.{u, v, uH, vH}
      (W := W) A :=
  exactUniversalAmbientObjectCoverage_of_restrictionUniversality.{u, v, uH, vH}
    (W := W) A hU

#print axioms exactUniversalAmbientRestrictionPresentation
#print axioms exactUniversalAmbientSourceOfRestrictionUniversalTarget
#print axioms exists_exactUniversalAmbientSource_carrier_eq
#print axioms exactUniversalAmbientObjectCoverage_of_restrictionUniversality
#print axioms exactUniversalAmbientWhiteheadBiequivalenceOfRestrictionUniversality
#print axioms exactUniversalAmbientWhiteheadExistence_of_restrictionUniversality

end

end KUOS.DependentOriginationExactUniversalAmbientRestrictionUniversalityV4_91
