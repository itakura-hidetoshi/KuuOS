import KUOS.DependentOriginationAbstractPresentationDescentV4_49
import KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
import KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
import KUOS.DependentOriginationHigherStackCarrierV2_9
import KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
import KUOS.DependentOriginationHigherLocalizationNecessityV2_16
import KUOS.DependentOriginationAdmissibleNonfactorizationV4_01
import Mathlib

namespace KUOS.DependentOriginationExactHigherAdmissibleV4_50

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationHigherLocalizationNecessityV2_16
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationAbstractNonfactorizationV4_00
open KUOS.DependentOriginationAdmissibleNonfactorizationV4_01
open KUOS.DependentOriginationAbstractPresentationDescentV4_49

open scoped CategoryTheory.Pseudofunctor.StrongTrans

set_option autoImplicit false

noncomputable section

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-!
# Exact higher dependent-origination admissibility v4.50

v4.49 returns the formal spine to a presentation-general statement at the
0-level:

  quotient factorization <-> presentation invariance,

with an exact obstruction criterion.

The higher Cat-valued theory already has the corresponding ingredients, but
they must be separated correctly.

Weak presentation invariance

  IsHigherWAdmissible W R

is necessary for higher localization factorization, but v4.01 proves that it
is not sufficient in general.  Therefore the general dependent-origination
positive sector must not be defined by weak W-admissibility alone.

This file defines the exact positive sector by the data that are actually
needed:

1. an object of the existing stack carrier DO₂(C,W,A);
2. a strong comparison from its restriction along the presentation unit back
   to the raw contextual system R;
3. pointwise equivalence of every comparison component.

This is exactly equivalent to the existing
HigherStackLocalizationFactorization interface, but is expressed with the
DO₂ carrier itself as the primary object.

Thus the general hierarchy becomes

  exact DO₂ realization
      => higher localization factorization
      => weak W-admissibility,

while the octahedral counterSystem is weakly admissible but lies outside the
first two classes.

This is an existence-level interface.  Essential uniqueness, naturality, and
the full classification equivalence remain the next theorem obligations.
-/

/-- A raw higher contextual system is realized by dependent origination when
it is represented by an actual object of the stack carrier DO₂ together with a
pointwise-equivalence comparison back to the raw presentation. -/
structure HigherDependentOriginationRealization
    (A : RefinementAtlas (LocalizedContext W))
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)) where
  /-- The actual stack object carrying the localized/descent-complete content. -/
  carrier : HigherStackObject.{u, v, uH, vH} (W := W) A
  /-- Comparison from the carrier restricted along the presentation unit back
  to the raw contextual system. -/
  comparison :
    restrictHigherLocalizedSystem W carrier.1 ⟶ R
  /-- The comparison is weakly exact: every component is an equivalence of
  categories. -/
  comparison_isEquivalence :
    ∀ X : Context, (comparison.app (.mk X)).toFunctor.IsEquivalence

/-- The exact positive class for higher dependent origination:
there exists a genuine DO₂ realization of the raw system. -/
def IsHigherDependentOriginationAdmissible
    (A : RefinementAtlas (LocalizedContext W))
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)) : Prop :=
  Nonempty (HigherDependentOriginationRealization (W := W) A R)

/-- Convert an existing higher stack-localization factorization into an
explicit realization by an object of DO₂. -/
def higherDependentOriginationRealizationOfStackFactorization
    (A : RefinementAtlas (LocalizedContext W))
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (H : HigherStackLocalizationFactorization (W := W) A R) :
    HigherDependentOriginationRealization (W := W) A R where
  carrier := ⟨H.lift, H.isStack⟩
  comparison := H.comparison
  comparison_isEquivalence := H.comparison_isEquivalence

/-- Conversely, a DO₂ realization gives exactly the existing
stack-localization factorization data. -/
def higherStackLocalizationFactorizationOfRealization
    (A : RefinementAtlas (LocalizedContext W))
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (D : HigherDependentOriginationRealization (W := W) A R) :
    HigherStackLocalizationFactorization (W := W) A R where
  lift := D.carrier.1
  comparison := D.comparison
  comparison_isEquivalence := D.comparison_isEquivalence
  isStack := D.carrier.2

/-- Exact admissibility is equivalent to the pre-existing proposition that a
stack-localization factorization exists. -/
theorem isHigherDependentOriginationAdmissible_iff_stackFactorization
    (A : RefinementAtlas (LocalizedContext W))
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)) :
    IsHigherDependentOriginationAdmissible (W := W) A R ↔
      HasHigherStackLocalizationFactorization (W := W) A R := by
  constructor
  · rintro ⟨D⟩
    exact
      ⟨higherStackLocalizationFactorizationOfRealization
        (W := W) A D⟩
  · rintro ⟨H⟩
    exact
      ⟨higherDependentOriginationRealizationOfStackFactorization
        (W := W) A H⟩

/-- Equivalent spelling that exposes the two logically separate requirements:
higher localization factorization and stack descent of its localized lift. -/
theorem isHigherDependentOriginationAdmissible_iff_factorization_and_stack
    (A : RefinementAtlas (LocalizedContext W))
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)) :
    IsHigherDependentOriginationAdmissible (W := W) A R ↔
      ∃ H : HigherLocalizationFactorization (W := W) R,
        IsHigherGrothendieckDescentComplete W A H.lift := by
  constructor
  · rintro ⟨D⟩
    let H : HigherLocalizationFactorization (W := W) R :=
      { lift := D.carrier.1,
        comparison := D.comparison,
        comparison_isEquivalence := D.comparison_isEquivalence }
    exact ⟨H, D.carrier.2⟩
  · rintro ⟨H, hStack⟩
    let HS : HigherStackLocalizationFactorization (W := W) A R :=
      { toHigherLocalizationFactorization := H,
        isStack := hStack }
    exact
      ⟨higherDependentOriginationRealizationOfStackFactorization
        (W := W) A HS⟩

/-- Every exact dependent-origination realization supplies an ordinary higher
localization factorization. -/
theorem higherDependentOriginationAdmissible_hasHigherLocalizationFactorization
    (A : RefinementAtlas (LocalizedContext W))
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (h : IsHigherDependentOriginationAdmissible (W := W) A R) :
    HasHigherLocalizationFactorization (W := W) R := by
  have hStack :
      HasHigherStackLocalizationFactorization (W := W) A R :=
    (isHigherDependentOriginationAdmissible_iff_stackFactorization
      (W := W) A R).1 h
  exact
    hasHigherLocalizationFactorization_of_stack
      (W := W) A R hStack

/-- Hence exact dependent-origination admissibility implies the weak
presentation-invariance condition. -/
theorem higherDependentOriginationAdmissible_isHigherWAdmissible
    (A : RefinementAtlas (LocalizedContext W))
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (h : IsHigherDependentOriginationAdmissible (W := W) A R) :
    IsHigherWAdmissible W R := by
  exact
    hasHigherLocalizationFactorization_isHigherWAdmissible W
      (higherDependentOriginationAdmissible_hasHigherLocalizationFactorization
        (W := W) A h)

/-- Any explicit higher factorization whose lift satisfies stack descent lies
in the exact dependent-origination positive sector. -/
theorem higherDependentOriginationAdmissible_of_factorization_and_stack
    (A : RefinementAtlas (LocalizedContext W))
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (H : HigherLocalizationFactorization (W := W) R)
    (hStack : IsHigherGrothendieckDescentComplete W A H.lift) :
    IsHigherDependentOriginationAdmissible (W := W) A R := by
  exact
    (isHigherDependentOriginationAdmissible_iff_factorization_and_stack
      (W := W) A R).2
      ⟨H, hStack⟩

/-- Exact carrier-level spelling: admissibility means there exists a stack
object and a pointwise-equivalence comparison back to the raw system. -/
theorem isHigherDependentOriginationAdmissible_iff_exists_carrier_comparison
    (A : RefinementAtlas (LocalizedContext W))
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)) :
    IsHigherDependentOriginationAdmissible (W := W) A R ↔
      ∃ X : HigherStackObject.{u, v, uH, vH} (W := W) A,
        ∃ η : restrictHigherLocalizedSystem W X.1 ⟶ R,
          ∀ C : Context, (η.app (.mk C)).toFunctor.IsEquivalence := by
  constructor
  · rintro ⟨D⟩
    exact
      ⟨D.carrier, D.comparison, D.comparison_isEquivalence⟩
  · rintro ⟨X, η, hη⟩
    exact
      ⟨{ carrier := X,
          comparison := η,
          comparison_isEquivalence := hη }⟩

/-!
## The octahedral boundary

The concrete Stage-II countermodel now serves as a direct negative test for
the general exact class rather than as the definition of the theory.
-/

/-- For every generated refinement atlas on the localized octahedral context,
the counterSystem is outside the exact higher dependent-origination positive
sector. -/
theorem counterSystem_not_higherDependentOriginationAdmissible
    (A : RefinementAtlas
      (LocalizedContext
        KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69.allMorphisms)) :
    ¬ IsHigherDependentOriginationAdmissible
      (W :=
        KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69.allMorphisms)
      A
      KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69.counterSystem := by
  intro h
  apply no_counterSystem_higherLocalizationFactorization
  exact
    higherDependentOriginationAdmissible_hasHigherLocalizationFactorization
      (W := allMorphisms) A h

/-- The exact logical boundary: the octahedral counterSystem is weakly
W-admissible but is not exactly dependent-origination admissible. -/
theorem counterSystem_weaklyAdmissible_but_not_exactHigherDependentOrigination
    (A : RefinementAtlas
      (LocalizedContext
        KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69.allMorphisms)) :
    IsHigherWAdmissible
        KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69.allMorphisms
        KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69.counterSystem ∧
      ¬ IsHigherDependentOriginationAdmissible
        (W :=
          KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69.allMorphisms)
        A
        KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69.counterSystem := by
  exact
    ⟨counterSystem_admissible,
      counterSystem_not_higherDependentOriginationAdmissible A⟩

/-!
## Boundary after v4.50

The general dependent-origination program now has an exact higher positive
sector.

A raw Cat-valued contextual system belongs to that sector precisely when it has

  raw system R
      ↑ pointwise-equivalence comparison
  DO₂ stack carrier X,

equivalently when it has both a genuine higher-localization factorization and
stack descent.

The implication chain is formally certified:

  exact higher DO admissible
      => HasHigherLocalizationFactorization
      => IsHigherWAdmissible.

The converse final arrow is false in general: the octahedral counterSystem is
weakly admissible but has no higher factorization and therefore no exact DO₂
realization for any atlas.

This places the Stage-II obstruction at the boundary of the general theory
rather than inside its definition.

The next theorem obligation is no longer geometric.  It is the genuine
universal-property step inside this exact positive sector:

* essential uniqueness of the DO₂ realization;
* naturality of the realization/comparison construction;
* presentation-invariant mapping properties between exact realizations.

Only after those are proved should the existence-level interface be promoted
to the full dependent-origination classification equivalence.
-/

end

end KUOS.DependentOriginationExactHigherAdmissibleV4_50
