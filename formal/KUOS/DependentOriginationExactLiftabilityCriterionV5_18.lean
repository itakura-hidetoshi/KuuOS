import KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
import Mathlib

namespace KUOS.DependentOriginationExactLiftabilityCriterionV5_18

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationAbstractNonfactorizationV4_00
open KUOS.DependentOriginationAdmissibleNonfactorizationV4_01
open KUOS.DependentOriginationExactHigherPresentationSectorV4_50
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17

set_option autoImplicit false

noncomputable section

/-!
# Exact-liftability criterion v5.18

v5.17 separates weak semantic admissibility from exact liftability at the type
level.  The present theorem unit identifies the exact higher criterion that is
already justified by the formal development.

For a raw higher contextual system R, exact liftability means precisely:

* there exists a HigherLocalizationFactorization H of R; and
* the chosen localized lift H.lift satisfies genuine stack descent for the
  fixed refinement atlas A.

This is a complete iff criterion because v4.50 already proves that the above
data are equivalent to a carrier-first exact DO₂ presentation.

The obstruction boundary must remain precise.  The v4.00-v4.48 obstruction
chain proves concrete nonfactorization statements, including the octahedral C2
counterSystem.  It does not provide a presentation-general higher theorem of
the form

  vanishing obstruction class <-> exact liftability.

The exact obstruction iff of v4.49 is a 0-level Setoid/Quotient theorem and is
not silently promoted here to the Cat-valued bicategorical setting.

Accordingly this file:

1. packages factorization + stack descent as the exact-liftability criterion;
2. proves its equivalence with exact higher presentation;
3. upgrades a weak semantic object only when an explicit criterion witness is
   supplied;
4. retains the octahedral counterSystem as a regression theorem showing that
   weak admissibility alone cannot satisfy the criterion.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- The exact higher liftability criterion.

This is deliberately stated in the already-validated higher interfaces:
ordinary higher localization factorization plus genuine stack descent of its
chosen lift. -/
def ExactLiftabilityCriterion
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)) : Prop :=
  ∃ H : HigherLocalizationFactorization (W := W) R,
    IsHigherGrothendieckDescentComplete W A H.lift

/-- Exact carrier-first presentation exists iff the exact-liftability
criterion holds. -/
theorem hasExactHigherDependentOriginationPresentation_iff_exactLiftabilityCriterion
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)) :
    HasExactHigherDependentOriginationPresentation (W := W) A R ↔
      ExactLiftabilityCriterion (W := W) A R := by
  simpa [ExactLiftabilityCriterion] using
    (hasExactHigherDependentOriginationPresentation_iff_factorization_and_stack
      (W := W) A R)

/-- Equivalent spelling through the pre-existing stack-localization
factorization interface. -/
theorem exactLiftabilityCriterion_iff_stackFactorization
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)) :
    ExactLiftabilityCriterion (W := W) A R ↔
      HasHigherStackLocalizationFactorization (W := W) A R := by
  exact
    (hasExactHigherDependentOriginationPresentation_iff_exactLiftabilityCriterion
      (W := W) A R).symm.trans
      (hasExactHigherDependentOriginationPresentation_iff_stackFactorization
        (W := W) A R)

/-- The exact-liftability criterion implies weak semantic admissibility. -/
theorem exactLiftabilityCriterion_isHigherWAdmissible
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (hCriterion : ExactLiftabilityCriterion (W := W) A R) :
    IsHigherWAdmissible W R := by
  exact
    exactPresentation_isHigherWAdmissible
      (W := W) A R
      ((hasExactHigherDependentOriginationPresentation_iff_exactLiftabilityCriterion
        (W := W) A R).2 hCriterion)

/-! ## Classification-interface bridge -/

/-- A weak semantic classification object can be promoted to the exact-liftable
layer when, and only when, an explicit exact-liftability criterion witness is
available.  No implication from weak admissibility alone is used. -/
def WeakSemanticClassificationObject.toExactLiftableOfCriterion
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      WeakSemanticClassificationObject
        (W := W) WorldLabel PresentationLabel)
    (hCriterion :
      ExactLiftabilityCriterion (W := W) A X.raw) :
    ExactLiftableClassificationObject
      (W := W) A WorldLabel PresentationLabel where
  label := X.label
  raw := X.raw
  exact :=
    (hasExactHigherDependentOriginationPresentation_iff_exactLiftabilityCriterion
      (W := W) A X.raw).2 hCriterion

@[simp] theorem WeakSemanticClassificationObject.toExactLiftableOfCriterion_label
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      WeakSemanticClassificationObject
        (W := W) WorldLabel PresentationLabel)
    (hCriterion :
      ExactLiftabilityCriterion (W := W) A X.raw) :
    (X.toExactLiftableOfCriterion (W := W) A hCriterion).label =
      X.label :=
  rfl

@[simp] theorem WeakSemanticClassificationObject.toExactLiftableOfCriterion_raw
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      WeakSemanticClassificationObject
        (W := W) WorldLabel PresentationLabel)
    (hCriterion :
      ExactLiftabilityCriterion (W := W) A X.raw) :
    (X.toExactLiftableOfCriterion (W := W) A hCriterion).raw =
      X.raw :=
  rfl

/-- Every exact-liftable classification object satisfies the exact-liftability
criterion for its raw system. -/
theorem ExactLiftableClassificationObject.satisfiesExactLiftabilityCriterion
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject
        (W := W) A WorldLabel PresentationLabel) :
    ExactLiftabilityCriterion (W := W) A X.raw := by
  exact
    (hasExactHigherDependentOriginationPresentation_iff_exactLiftabilityCriterion
      (W := W) A X.raw).1 X.exact

/-! ## Concrete obstruction regression -/

/-- The octahedral C2 counterSystem fails the exact-liftability criterion for
every refinement atlas.  The failure already occurs at factorization existence;
the stack condition is therefore unreachable. -/
theorem counterSystem_not_exactLiftabilityCriterion
    (A :
      RefinementAtlas
        (LocalizedContext allMorphisms)) :
    ¬ ExactLiftabilityCriterion
        (W := allMorphisms) A counterSystem := by
  rintro ⟨H, _hStack⟩
  exact no_counterSystem_higherLocalizationFactorization ⟨H⟩

/-- The counterSystem packaged as a weak semantic classification object with
trivial external labels. -/
def counterSystemWeakSemanticClassificationObject :
    WeakSemanticClassificationObject
      (W := allMorphisms) Unit Unit where
  label := ⟨(), ()⟩
  raw := counterSystem
  admissible :=
    counterSystem_admissible_but_no_higherLocalizationFactorization.1

/-- Weak semantic admissibility does not imply the exact-liftability criterion,
already for the finite octahedral counterSystem. -/
theorem not_all_weakSemantic_octahedral_objects_satisfy_exactLiftabilityCriterion
    (A :
      RefinementAtlas
        (LocalizedContext allMorphisms)) :
    ¬ ∀
      X :
        WeakSemanticClassificationObject
          (W := allMorphisms) Unit Unit,
      ExactLiftabilityCriterion
        (W := allMorphisms) A X.raw := by
  intro hAll
  exact
    counterSystem_not_exactLiftabilityCriterion A
      (hAll counterSystemWeakSemanticClassificationObject)

/-!
## Boundary after v5.18

The exact-liftability boundary is now theorem-level and classification-ready:

  exact presentation
    <-> higher localization factorization + stack descent
    <-> higher stack-localization factorization
    -> weak semantic admissibility.

The reverse implication from weak semantic admissibility is false, witnessed by
the octahedral counterSystem.

No generic higher obstruction-class vanishing iff theorem has been invented.
The concrete obstruction results v4.00-v4.48 remain negative certificates on
specific systems; v4.49 remains an exact 0-level presentation-descent theorem.

The next theorem unit may therefore address factor existence / coherent
uniqueness for objects already satisfying this exact criterion, before any
final mapping/classification equivalence is stated.
-/

end

end KUOS.DependentOriginationExactLiftabilityCriterionV5_18
