import KUOS.DependentOriginationUniversalUnitorGaugeV3_64

namespace KUOS.DependentOriginationFixedGaugeUnitorAssociatorSeparationV3_65

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationThreeRouteCorrectionCompatibilityGapV3_09
open KUOS.DependentOriginationQuotientGaugeIntersectionObstructionV3_11
open KUOS.DependentOriginationUnitorWitnessCorrelationV3_35
open KUOS.DependentOriginationFiniteAssociatorScheduleV3_38
open KUOS.DependentOriginationInversePairBoundaryObstructionV3_55
open KUOS.DependentOriginationOctahedralInversePairV3_63
open KUOS.DependentOriginationUniversalUnitorGaugeV3_64

universe u v uH vH

set_option autoImplicit false

noncomputable section

/-!
# Fixed-gauge unitor/associator separation v3.65

v3.64 proves two facts that should be kept logically separate:

* every quotient-gauge carrier admits at least one fixed gauge correcting every
  left and right unitor;
* in the concrete v2.69 octahedral C2 model, there exists a fixed gauge that
  still carries the exact v3.55 inverse-pair fresh-boundary associator
  obstruction while correcting every unitor.

The second statement is stronger than merely saying that unitor and associator
equations are syntactically different.  It gives a concrete same-gauge
separation:

  all unitors corrected at Q
  does not force
  all associators corrected at that same Q.

This file packages that pointwise separation explicitly.  It does not claim
that no other gauge can correct the selected associator, nor that a fully
coherent gauge is impossible.  Those would be uncorrectability/existence
statements of a different logical strength.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (R : RawHigherContextualSystem.{u, v, uH, vH}
  (Context := Context))
variable (D : PointwiseWAdjointEquivalenceData (W := W) R)

/-- One fixed quotient gauge corrects every left/right unitor route. -/
def AllUnitorsCorrectedAt
    (Q : GeneratedQuotientGaugeParameters W R D) : Prop :=
  ∀ X (s : UnitorRouteAt W X),
    Q ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s)

/-- One fixed quotient gauge corrects every associator route. -/
def AllAssociatorsCorrectedAt
    (Q : GeneratedQuotientGaugeParameters W R D) : Prop :=
  ∀ a : AssociatorTask W,
    Q ∈ quotientRouteCorrectionLocus W R D (associatorTaskRoute W a)

/-- One fixed quotient gauge corrects every route in the quotient-coherence
three-route state space. -/
def AllQuotientRoutesCorrectedAt
    (Q : GeneratedQuotientGaugeParameters W R D) : Prop :=
  ∀ s : ThreeQuotientRouteState W,
    Q ∈ quotientRouteCorrectionLocus W R D s

/-- An exact inverse-pair fresh-boundary obstruction at one task immediately
prevents that same gauge from correcting all associators. -/
theorem not_allAssociatorsCorrectedAt_of_inversePairFreshBoundaryObstruction
    (Q : GeneratedQuotientGaugeParameters W R D)
    (a : AssociatorTask W)
    (hObstruction :
      InversePairFreshBoundaryLeadingObstruction W R D Q a) :
    ¬ AllAssociatorsCorrectedAt W R D Q := by
  intro hAll
  have hNotCorrect :
      Q ∉ quotientRouteCorrectionLocus W R D (associatorTaskRoute W a) :=
    (inversePairFreshBoundaryLeadingObstruction_iff_not_corrected
      W R D Q a hObstruction.1 hObstruction.2.1).1 hObstruction
  exact hNotCorrect (hAll a)

/-- The same exact obstruction prevents total correction of the whole
three-route state space at that gauge. -/
theorem not_allQuotientRoutesCorrectedAt_of_inversePairFreshBoundaryObstruction
    (Q : GeneratedQuotientGaugeParameters W R D)
    (a : AssociatorTask W)
    (hObstruction :
      InversePairFreshBoundaryLeadingObstruction W R D Q a) :
    ¬ AllQuotientRoutesCorrectedAt W R D Q := by
  intro hAll
  have hNotCorrect :
      Q ∉ quotientRouteCorrectionLocus W R D (associatorTaskRoute W a) :=
    (inversePairFreshBoundaryLeadingObstruction_iff_not_corrected
      W R D Q a hObstruction.1 hObstruction.2.1).1 hObstruction
  exact hNotCorrect (hAll (associatorTaskRoute W a))

/-- The concrete inverse-pair associator task isolated in v3.63. -/
def counterInversePairAssociatorTask : AssociatorTask allMorphisms :=
  { X := counterX
    Y := counterY
    Z := counterX
    T := counterT
    f := counterInversePairForward
    g := counterInversePairBackward
    h := counterInversePairThird }

/-- Concrete same-gauge separation: there exists a quotient gauge correcting
all unitors while failing at least one associator. -/
theorem counterSystem_exists_fixedGauge_allUnitors_not_allAssociators :
    ∃ Q : GeneratedQuotientGaugeParameters
        allMorphisms counterSystem counterD,
      AllUnitorsCorrectedAt allMorphisms counterSystem counterD Q ∧
        ¬ AllAssociatorsCorrectedAt
          allMorphisms counterSystem counterD Q := by
  rcases
      counterSystem_exists_exactInversePairFreshBoundaryObstruction with
    ⟨Q, hUnit, hObstruction⟩
  have hObstruction' :
      InversePairFreshBoundaryLeadingObstruction
        allMorphisms counterSystem counterD Q
        counterInversePairAssociatorTask := by
    simpa [counterInversePairAssociatorTask] using hObstruction
  refine ⟨Q, ?_, ?_⟩
  · exact hUnit
  · exact
      not_allAssociatorsCorrectedAt_of_inversePairFreshBoundaryObstruction
        allMorphisms counterSystem counterD Q
        counterInversePairAssociatorTask hObstruction'

/-- Therefore the pointwise implication "all unitors corrected at Q implies all
associators corrected at the same Q" is false in the concrete v2.69 model. -/
theorem counterSystem_allUnitors_do_not_force_allAssociators :
    ¬ (∀ Q : GeneratedQuotientGaugeParameters
          allMorphisms counterSystem counterD,
        AllUnitorsCorrectedAt allMorphisms counterSystem counterD Q →
          AllAssociatorsCorrectedAt
            allMorphisms counterSystem counterD Q) := by
  intro hForce
  rcases
      counterSystem_exists_fixedGauge_allUnitors_not_allAssociators with
    ⟨Q, hUnit, hNotAssociators⟩
  exact hNotAssociators (hForce Q hUnit)

/-- The same witness separates complete unitor correction from correction of
the whole three-route quotient-coherence state space. -/
theorem counterSystem_exists_fixedGauge_allUnitors_not_allRoutes :
    ∃ Q : GeneratedQuotientGaugeParameters
        allMorphisms counterSystem counterD,
      AllUnitorsCorrectedAt allMorphisms counterSystem counterD Q ∧
        ¬ AllQuotientRoutesCorrectedAt
          allMorphisms counterSystem counterD Q := by
  rcases
      counterSystem_exists_exactInversePairFreshBoundaryObstruction with
    ⟨Q, hUnit, hObstruction⟩
  have hObstruction' :
      InversePairFreshBoundaryLeadingObstruction
        allMorphisms counterSystem counterD Q
        counterInversePairAssociatorTask := by
    simpa [counterInversePairAssociatorTask] using hObstruction
  refine ⟨Q, ?_, ?_⟩
  · exact hUnit
  · exact
      not_allQuotientRoutesCorrectedAt_of_inversePairFreshBoundaryObstruction
        allMorphisms counterSystem counterD Q
        counterInversePairAssociatorTask hObstruction'

/-!
## Boundary after v3.65

The concrete truth test now formally separates, at one and the same fixed
quotient gauge,

  complete unitor correction

from

  complete associator correction
  and complete three-route correction.

This is a pointwise fixed-gauge statement.  It does not prove:

* that every common-unitor gauge fails an associator;
* that no alternative gauge corrects all routes;
* that the v2.69 model is globally uncorrectable;
* that weak admissibility forbids coherent quotient transport;
* final Stage I or Stage II universality failure.

The next mathematically stronger question is therefore no longer whether one
bad fixed gauge exists; v3.64-v3.65 settle that.  It is whether the concrete
model admits any fully corrected quotient gauge at all, or whether an invariant
obstruction survives every gauge choice.  That question must be tested by a
gauge-independent argument rather than by another one-coordinate perturbation.
-/

end

end KUOS.DependentOriginationFixedGaugeUnitorAssociatorSeparationV3_65
