import KUOS.DependentOriginationStrictCorrectionPowerV2_90

namespace KUOS.DependentOriginationCorrectionProfileRealizationV2_91

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFreePathEvaluatorV2_57
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68
open KUOS.DependentOriginationCorrectionRealizationV2_74
open KUOS.DependentOriginationGeneratedHolonomyCorrectabilityV2_80
open KUOS.DependentOriginationHeterogeneousCorrectionAuthorityV2_86
open KUOS.DependentOriginationCorrectionPowerSemanticsV2_88
open KUOS.DependentOriginationCorrectionReachabilityProfileV2_89

universe u v w

/-!
# Correction-profile realization v2.91

The v2.89 reachability profile forgets correction-parameter presentation and
retains only the observable predicate of reachable defects. This layer proves
that no extensional information is lost at that semantic level: every profile
has a canonical functional correction realization.

The parameter carrier is State → D. At state x, a parameter f realizes the
defect f x and is admissible exactly when the profile admits f x at x. This
choice is important: a general correction effect may depend on state, so a
canonical authority morphism cannot in general map a source parameter to one
fixed defect value. The function-valued carrier preserves that dependence.

Consequently every correction realization has a canonical semantic
representative with exactly the same correction power, together with a
canonical authority morphism from the original presentation into that
representative.

No reverse authority morphism is asserted. Equality of extensional correction
power remains weaker than explicit mutual parameter transport.
-/

/-- Canonical functional correction mechanism realizing an arbitrary
reachability profile. -/
def functionalProfileCorrectionRealization
    {State : Type u} {D : Type w}
    (P : State → D → Prop) :
    CorrectionRealization State (State → D) D where
  admissible := fun x f => P x (f x)
  effect := fun x f => f x

/-- Correctability for the functional profile realization is exactly the
specified profile. -/
theorem functionalProfileCorrectionRealization_correctable_iff
    {State : Type u} {D : Type w}
    (P : State → D → Prop)
    (x : State) (d : D) :
    (functionalProfileCorrectionRealization P).CorrectableAt x d ↔ P x d := by
  constructor
  · rintro ⟨f, hf, heffect⟩
    dsimp [functionalProfileCorrectionRealization] at hf heffect
    rw [heffect] at hf
    exact hf
  · intro hd
    refine ⟨fun _ => d, ?_, rfl⟩
    change P x d
    exact hd

/-- The reachability profile of the functional realization is propositionally
equal to the original profile. -/
theorem functionalProfileCorrectionRealization_profile_eq
    {State : Type u} {D : Type w}
    (P : State → D → Prop) :
    CorrectionReachabilityProfile (functionalProfileCorrectionRealization P) =
      P := by
  funext x d
  apply propext
  exact functionalProfileCorrectionRealization_correctable_iff P x d

/-- Canonical presentation-free representative of an existing correction
mechanism. -/
def semanticRepresentative
    {State : Type u} {Param : Type v} {D : Type w}
    (C : CorrectionRealization State Param D) :
    CorrectionRealization State (State → D) D :=
  functionalProfileCorrectionRealization (CorrectionReachabilityProfile C)

/-- Every correction mechanism has exactly the same extensional correction
power as its semantic representative. -/
theorem semanticRepresentative_powerEq
    {State : Type u} {Param : Type v} {D : Type w}
    (C : CorrectionRealization State Param D) :
    CorrectionPowerEq C (semanticRepresentative C) := by
  apply (correctionPowerEq_iff_profile_eq C (semanticRepresentative C)).2
  exact (functionalProfileCorrectionRealization_profile_eq
    (CorrectionReachabilityProfile C)).symm

/-- The semantic representative has exactly the same reachability profile as
the original correction mechanism. -/
theorem semanticRepresentative_profile_eq
    {State : Type u} {Param : Type v} {D : Type w}
    (C : CorrectionRealization State Param D) :
    CorrectionReachabilityProfile (semanticRepresentative C) =
      CorrectionReachabilityProfile C := by
  exact functionalProfileCorrectionRealization_profile_eq
    (CorrectionReachabilityProfile C)

/-- Every concrete correction parameter canonically determines its full
state-indexed defect effect. This gives an authority morphism into the semantic
representative. -/
def toSemanticRepresentative
    {State : Type u} {Param : Type v} {D : Type w}
    (C : CorrectionRealization State Param D) :
    CorrectionAuthorityHom C (semanticRepresentative C) where
  mapParam := fun p x => C.effect x p
  admissible_map := by
    intro x p hp
    dsimp [semanticRepresentative,
      functionalProfileCorrectionRealization,
      CorrectionReachabilityProfile]
    exact ⟨p, hp, rfl⟩
  effect_map := by
    intro x p
    rfl

/-- The canonical authority morphism recovers the forward half of extensional
correction-power equivalence. -/
theorem toSemanticRepresentative_powerLE
    {State : Type u} {Param : Type v} {D : Type w}
    (C : CorrectionRealization State Param D) :
    CorrectionPowerLE C (semanticRepresentative C) :=
  CorrectionPowerLE.ofAuthorityHom (toSemanticRepresentative C)

/-- Hard-obstruction classification is unchanged by passage to the semantic
representative. -/
theorem semanticRepresentative_hardObstruction_iff
    {State : Type u} {Param : Type v} {D : Type w}
    (C : CorrectionRealization State Param D)
    (x : State) (d : D) :
    C.HardObstructionAt x d ↔
      (semanticRepresentative C).HardObstructionAt x d := by
  exact CorrectionPowerEq.hardObstruction_iff
    (semanticRepresentative_powerEq C)

end KUOS.DependentOriginationCorrectionProfileRealizationV2_91
