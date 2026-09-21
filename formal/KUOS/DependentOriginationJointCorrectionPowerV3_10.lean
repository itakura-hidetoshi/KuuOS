import KUOS.DependentOriginationThreeRouteCorrectionCompatibilityGapV3_09

namespace KUOS.DependentOriginationJointCorrectionPowerV3_10

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationCorrectionRealizationV2_74
open KUOS.DependentOriginationCorrectionPowerSemanticsV2_88
open KUOS.DependentOriginationCompatibleThreeRouteCorrectionV3_08
open KUOS.DependentOriginationThreeRouteCorrectionCompatibilityGapV3_09

universe u v₁ v₂ w uC vC uH vH

/-!
# Joint correction power v3.10

v2.88--v2.95 intentionally quotient correction mechanisms by their extensional
pointwise reachability relation.  v3.09 shows that this forgetful semantics is
too coarse for the first higher-localization stage:

```text
pointwise correction power : ∀ s, ∃ p_s, ...
higher-localization need   : ∃ p,   ∀ s, ...
```

The missing datum is correlation of correction witnesses across states.

This file therefore introduces the joint correction profile of a realization.
A target profile `target : State → D` is jointly reachable when one single
parameter realizes the requested target at every state simultaneously.

Two facts are then proved.

1. Joint reachability always implies ordinary pointwise reachability.
2. The converse cannot be recovered from extensional correction power alone:
   two explicit Boolean correction mechanisms have identical pointwise
   correction power but different joint correction profiles.

For the quotient-stage realization of v3.09, joint reachability of the constant
Unit target is exactly existence of one compatible quotient gauge, hence exactly
existence of coherent quotient transport.

Thus the semantics required by higher localization is not a stronger value of
the old correction-power lattice.  It is a strictly more informative semantic
object which retains common-parameter correlation.
-/

/-- One parameter realizes an entire state-indexed target profile
simultaneously. -/
def JointlyCorrectable
    {State : Type u} {Param : Type v₁} {D : Type w}
    (C : CorrectionRealization State Param D)
    (target : State → D) : Prop :=
  ∃ p : Param, ∀ x : State,
    C.admissible x p ∧ C.effect x p = target x

/-- The presentation-free joint semantic profile of a correction mechanism. -/
def JointCorrectionProfile
    {State : Type u} {Param : Type v₁} {D : Type w}
    (C : CorrectionRealization State Param D) :
    (State → D) → Prop :=
  fun target => JointlyCorrectable C target

/-- A jointly reachable target is pointwise reachable at every state by reusing
the same parameter. -/
theorem correctableAt_of_jointlyCorrectable
    {State : Type u} {Param : Type v₁} {D : Type w}
    (C : CorrectionRealization State Param D)
    (target : State → D)
    (h : JointlyCorrectable C target)
    (x : State) :
    C.CorrectableAt x (target x) := by
  rcases h with ⟨p, hp⟩
  exact ⟨p, (hp x).1, (hp x).2⟩

/-- Equality of joint semantics means logical equivalence for every complete
state-indexed target profile. -/
def JointCorrectionPowerEq
    {State : Type u} {Param₁ : Type v₁} {Param₂ : Type v₂} {D : Type w}
    (C₁ : CorrectionRealization State Param₁ D)
    (C₂ : CorrectionRealization State Param₂ D) : Prop :=
  ∀ target : State → D,
    JointCorrectionProfile C₁ target ↔ JointCorrectionProfile C₂ target

/-! ## A concrete loss-of-correlation counterexample -/

/-- Each Boolean state can be corrected, but only by the matching Boolean
parameter. -/
def splitBoolCorrectionRealization :
    CorrectionRealization Bool Bool Unit where
  admissible := fun x p => x = p
  effect := fun _ _ => ()

/-- One single Unit parameter corrects both Boolean states simultaneously. -/
def uniformBoolCorrectionRealization :
    CorrectionRealization Bool Unit Unit where
  admissible := fun _ _ => True
  effect := fun _ _ => ()

/-- The two Boolean mechanisms have exactly the same ordinary pointwise
correction power: at every state the unique Unit defect is reachable. -/
theorem splitBoolCorrectionPowerEq_uniformBool :
    CorrectionPowerEq splitBoolCorrectionRealization
      uniformBoolCorrectionRealization := by
  constructor
  · intro x d _
    cases d
    exact ⟨(), True.intro, rfl⟩
  · intro x d _
    cases d
    exact ⟨x, rfl, rfl⟩

/-- The uniform mechanism jointly realizes the complete Unit target profile. -/
theorem uniformBool_jointlyCorrectable :
    JointlyCorrectable uniformBoolCorrectionRealization (fun _ => ()) := by
  exact ⟨(), fun _ => ⟨True.intro, rfl⟩⟩

/-- The split mechanism cannot jointly realize the same profile: a single Bool
parameter cannot equal both states. -/
theorem not_splitBool_jointlyCorrectable :
    ¬ JointlyCorrectable splitBoolCorrectionRealization (fun _ => ()) := by
  intro h
  rcases h with ⟨p, hp⟩
  have ht : true = p := (hp true).1
  have hf : false = p := (hp false).1
  have htf : true = false := ht.trans hf.symm
  have hne : true ≠ false := by decide
  exact hne htf

/-- Therefore equality of v2.88 extensional correction power does not imply
equality of joint correction semantics. -/
theorem correctionPowerEq_does_not_determine_jointPower :
    CorrectionPowerEq splitBoolCorrectionRealization
        uniformBoolCorrectionRealization ∧
      ¬ JointCorrectionPowerEq splitBoolCorrectionRealization
        uniformBoolCorrectionRealization := by
  refine ⟨splitBoolCorrectionPowerEq_uniformBool, ?_⟩
  intro hJoint
  have hiff := hJoint (fun _ => ())
  have hsplit :
      JointCorrectionProfile splitBoolCorrectionRealization (fun _ => ()) :=
    hiff.mpr uniformBool_jointlyCorrectable
  exact not_splitBool_jointlyCorrectable hsplit

/-! ## Joint semantics for the three quotient route families -/

variable {Context : Type uC} [Category.{vC} Context]
variable (W : MorphismProperty Context)

/-- The exact common-parameter semantic condition needed at the quotient stage:
one quotient gauge jointly corrects every route state. -/
def ThreeQuotientRoutesJointlyCorrectable
    (R : RawHigherContextualSystem.{uC, vC, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) : Prop :=
  JointlyCorrectable
    (threeQuotientRouteCorrectionRealization W R D)
    (fun _ => ())

/-- Joint reachability of the constant Unit profile is literally the
`∃ Q, ∀ state` uniform-gauge condition. -/
theorem threeQuotientRoutesJointlyCorrectable_iff_exists_uniform_gauge
    (R : RawHigherContextualSystem.{uC, vC, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) :
    ThreeQuotientRoutesJointlyCorrectable W R D ↔
      ∃ Q : GeneratedQuotientGaugeParameters W R D,
        ∀ s : ThreeQuotientRouteState W,
          quotientRouteCorrectedBy W R D Q s := by
  constructor
  · rintro ⟨Q, hQ⟩
    exact ⟨Q, fun s => (hQ s).1⟩
  · rintro ⟨Q, hQ⟩
    exact ⟨Q, fun s => ⟨hQ s, rfl⟩⟩

/-- Main v3.10 identification: joint correction power is exactly the compatible
three-route correction notion isolated in v3.08. -/
theorem threeQuotientRoutesJointlyCorrectable_iff_compatible
    (R : RawHigherContextualSystem.{uC, vC, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) :
    ThreeQuotientRoutesJointlyCorrectable W R D ↔
      HasCompatibleThreeQuotientRouteCorrection W R D := by
  rw [threeQuotientRoutesJointlyCorrectable_iff_exists_uniform_gauge W R D]
  exact
    (hasCompatibleThreeQuotientRouteCorrection_iff_exists_uniform_gauge
      W R D).symm

/-- Hence joint correction of the three quotient routes is exactly existence of
the genuine coherent quotient pseudofunctor transport. -/
theorem threeQuotientRoutesJointlyCorrectable_iff_hasCoherentQuotientTransportData
    (R : RawHigherContextualSystem.{uC, vC, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) :
    ThreeQuotientRoutesJointlyCorrectable W R D ↔
      HasCoherentQuotientTransportData W R D := by
  rw [threeQuotientRoutesJointlyCorrectable_iff_compatible W R D]
  exact
    hasCompatibleThreeQuotientRouteCorrection_iff_hasCoherentQuotientTransportData
      W R D

/-- Joint quotient correction is strictly stronger semantically than maximal
pointwise correction power: it implies pointwise reachability, but the generic
Boolean example above proves that this implication cannot be inverted merely
from extensional correction-power information. -/
theorem allThreeQuotientRoutesIndividuallyReachable_of_jointlyCorrectable
    (R : RawHigherContextualSystem.{uC, vC, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (h : ThreeQuotientRoutesJointlyCorrectable W R D) :
    AllThreeQuotientRoutesIndividuallyReachable W R D := by
  intro s
  exact
    correctableAt_of_jointlyCorrectable
      (threeQuotientRouteCorrectionRealization W R D)
      (fun _ => ()) h s

/-!
## Factorization frontier after v3.10

The semantic mismatch exposed by v3.09 is now repaired:

```text
v2.95 extensional correction power
        |
        | forgets witness correlation
        v
pointwise profile: s ↦ reachable defects

v3.10 joint correction profile
        |
        | retains one common correction parameter
        v
target profile ↦ ∃ one p realizing all states
        |
        v
three quotient routes jointly correctable
        ↔
one compatible quotient gauge
        ↔
coherent quotient transport.
```

The Boolean counterexample proves formally that ordinary correction-power
equality cannot by itself establish the joint statement required for higher
localization.

The next mathematical question is now clean: prove joint reachability for the
actual quotient-gauge realization from additional algebraic structure of
`gId/gComp`, or construct a quotient-specific compatibility obstruction.  The
problem is no longer hidden inside the extensional v2.95 lattice.
-/

end KUOS.DependentOriginationJointCorrectionPowerV3_10
