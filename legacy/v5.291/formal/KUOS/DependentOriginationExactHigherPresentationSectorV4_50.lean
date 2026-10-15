import KUOS.DependentOriginationAbstractPresentationDescentV4_49
import KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
import KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
import KUOS.DependentOriginationHigherStackCarrierV2_9
import KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
import KUOS.DependentOriginationHigherLocalizationNecessityV2_16
import KUOS.DependentOriginationAdmissibleNonfactorizationV4_01
import Mathlib

namespace KUOS.DependentOriginationExactHigherPresentationSectorV4_50

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

/-!
# Exact higher presentation sector for dependent origination v4.50

v4.49 returns the formal spine to a presentation-general statement at the
set-theoretic level:

  quotient factorization
    <-> presentation invariance,

with an exact obstruction criterion.

The long-range dependent-origination target, however, is Cat-valued and
bicategorical.  The existing v2.10 interface already identifies the correct
higher data:

* a localized Cat-valued pseudofunctor;
* a strong comparison back to the raw contextual system;
* pointwise equivalence of that comparison;
* stack descent for the generated topology.

The present file reorganizes exactly that data around an object of the
already-constructed higher carrier DO₂(C,W,A).

For a raw higher contextual system R, an exact higher presentation consists of

  X in DO₂(C,W,A)

together with a pointwise-equivalence strong comparison

  restrict(X) --> R.

This is not a new existence axiom.  We prove that existence of this carrier-
first presentation is equivalent to the already-defined
HigherStackLocalizationFactorization.

This gives the exact positive sector for the next universality stage:

* every exact presentation implies weak W-admissibility;
* weak W-admissibility alone is not enough;
* the octahedral countermodel is weakly admissible but lies outside the exact
  sector for every refinement atlas.

Thus the carrier, comparison map, descent condition, and obstruction boundary
are now stated in one interface.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- Carrier-first higher dependent-origination presentation data.

The carrier is an actual object of DO₂, hence its underlying localized
pseudofunctor already satisfies generated-topology stack descent.  The strong
comparison records how that localized stack presents the raw contextual
system. -/
structure ExactHigherDependentOriginationPresentation
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)) where
  /-- The localized stack object representing the raw system. -/
  carrier :
    DependentOriginationCompletion2 (W := W) A
  /-- Comparison from the restriction of the carrier back to the raw system. -/
  comparison :
    restrictHigherLocalizedSystem W
        (higherStackObjectVal (W := W) A carrier) ⟶
      R
  /-- Presentation comparison is pointwise an equivalence of categories. -/
  comparison_isEquivalence :
    ∀ X : Context,
      (comparison.app (.mk X)).toFunctor.IsEquivalence

/-- Forget the carrier-first packaging and recover the existing v2.10
stack-localization factorization. -/
def higherStackLocalizationFactorizationOfExactPresentation
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (P : ExactHigherDependentOriginationPresentation
      (W := W) A R) :
    HigherStackLocalizationFactorization (W := W) A R where
  lift :=
    higherStackObjectVal (W := W) A P.carrier
  comparison :=
    P.comparison
  comparison_isEquivalence :=
    P.comparison_isEquivalence
  isStack := by
    exact P.carrier.2

/-- Conversely, every existing stack-localization factorization determines a
carrier-first exact higher presentation. -/
def exactPresentationOfHigherStackLocalizationFactorization
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (H : HigherStackLocalizationFactorization (W := W) A R) :
    ExactHigherDependentOriginationPresentation (W := W) A R where
  carrier :=
    completion2OfHigherStackLocalizationFactorization (W := W) A H
  comparison := by
    change restrictHigherLocalizedSystem W H.lift ⟶ R
    exact H.comparison
  comparison_isEquivalence := by
    intro X
    change (H.comparison.app (.mk X)).toFunctor.IsEquivalence
    exact H.comparison_isEquivalence X

/-- The carrier-first conversion retains exactly the localized lift. -/
@[simp] theorem exactPresentationOfStack_carrier_val
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (H : HigherStackLocalizationFactorization (W := W) A R) :
    higherStackObjectVal (W := W) A
        (exactPresentationOfHigherStackLocalizationFactorization
          (W := W) A H).carrier =
      H.lift :=
  rfl

/-- Returning an exact presentation to the old interface and then extracting
its DO₂ object recovers the original carrier. -/
theorem completion2Of_exactPresentation_eq_carrier
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (P : ExactHigherDependentOriginationPresentation
      (W := W) A R) :
    completion2OfHigherStackLocalizationFactorization
        (W := W) A
        (higherStackLocalizationFactorizationOfExactPresentation
          (W := W) A P) =
      P.carrier := by
  apply Subtype.ext
  rfl

/-- Existence of carrier-first exact presentation data. -/
def HasExactHigherDependentOriginationPresentation
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)) : Prop :=
  Nonempty
    (ExactHigherDependentOriginationPresentation (W := W) A R)

/-- Carrier-first exact presentation exists exactly when the original v2.10
stack-localization factorization exists. -/
theorem hasExactHigherDependentOriginationPresentation_iff_stackFactorization
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)) :
    HasExactHigherDependentOriginationPresentation (W := W) A R ↔
      HasHigherStackLocalizationFactorization (W := W) A R := by
  constructor
  · rintro ⟨P⟩
    exact
      ⟨higherStackLocalizationFactorizationOfExactPresentation
        (W := W) A P⟩
  · rintro ⟨H⟩
    exact
      ⟨exactPresentationOfHigherStackLocalizationFactorization
        (W := W) A H⟩

/-- Exact higher presentation exists iff there is an ordinary higher
localization factorization whose chosen lift satisfies stack descent. -/
theorem hasExactHigherDependentOriginationPresentation_iff_factorization_and_stack
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)) :
    HasExactHigherDependentOriginationPresentation (W := W) A R ↔
      ∃ H : HigherLocalizationFactorization (W := W) R,
        IsHigherGrothendieckDescentComplete W A H.lift := by
  constructor
  · rintro ⟨P⟩
    let HS :=
      higherStackLocalizationFactorizationOfExactPresentation
        (W := W) A P
    exact ⟨HS.toHigherLocalizationFactorization, HS.isStack⟩
  · rintro ⟨H, hStack⟩
    let HS : HigherStackLocalizationFactorization (W := W) A R :=
      { toHigherLocalizationFactorization := H,
        isStack := hStack }
    exact
      ⟨exactPresentationOfHigherStackLocalizationFactorization
        (W := W) A HS⟩

/-- Exact presentation in particular yields an ordinary higher-localization
factorization. -/
theorem hasHigherLocalizationFactorization_of_exactPresentation
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (hExact :
      HasExactHigherDependentOriginationPresentation
        (W := W) A R) :
    HasHigherLocalizationFactorization (W := W) R := by
  rcases hExact with ⟨P⟩
  exact
    ⟨(higherStackLocalizationFactorizationOfExactPresentation
      (W := W) A P).toHigherLocalizationFactorization⟩

/-- Therefore every exactly presentable higher contextual system satisfies the
necessary weak W-admissibility condition. -/
theorem exactPresentation_isHigherWAdmissible
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (hExact :
      HasExactHigherDependentOriginationPresentation
        (W := W) A R) :
    IsHigherWAdmissible W R := by
  exact
    hasHigherLocalizationFactorization_isHigherWAdmissible W
      (hasHigherLocalizationFactorization_of_exactPresentation
        (W := W) A R hExact)

/-- The exact positive sector: raw higher contextual systems admitting a
carrier in DO₂ together with a pointwise-equivalence comparison. -/
def ExactHigherDependentOriginationSector :=
  { R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context) //
    HasExactHigherDependentOriginationPresentation (W := W) A R }

/-- Every object of the exact positive sector is weakly W-admissible. -/
theorem exactHigherDependentOriginationSector_isHigherWAdmissible
    (R : ExactHigherDependentOriginationSector
      (W := W) A) :
    IsHigherWAdmissible W R.1 := by
  exact
    exactPresentation_isHigherWAdmissible
      (W := W) A R.1 R.2

/-!
## Octahedral obstruction boundary

The concrete countermodel from v4.00-v4.01 is weakly admissible, but it has no
higher-localization factorization at all.  Therefore it cannot lie in the
exact positive sector for any refinement atlas.
-/

/-- The octahedral countermodel has no exact DO₂ presentation for any atlas. -/
theorem counterSystem_no_exactHigherDependentOriginationPresentation
    (A :
      RefinementAtlas
        (LocalizedContext allMorphisms)) :
    ¬ HasExactHigherDependentOriginationPresentation
        (W := allMorphisms) A counterSystem := by
  intro hExact
  apply no_counterSystem_higherLocalizationFactorization
  exact
    hasHigherLocalizationFactorization_of_exactPresentation
      (W := allMorphisms) A counterSystem hExact

/-- Exact positive-sector inclusion is strictly stronger than weak
W-admissibility already on the finite octahedral context. -/
theorem counterSystem_weaklyAdmissible_but_not_exact
    (A :
      RefinementAtlas
        (LocalizedContext allMorphisms)) :
    IsHigherWAdmissible allMorphisms counterSystem ∧
      ¬ HasExactHigherDependentOriginationPresentation
        (W := allMorphisms) A counterSystem := by
  exact
    ⟨counterSystem_admissible_but_no_higherLocalizationFactorization.1,
      counterSystem_no_exactHigherDependentOriginationPresentation A⟩

/-- Consequently weak W-admissibility cannot characterize the exact positive
sector, even after an arbitrary refinement atlas is fixed. -/
theorem not_all_weaklyAdmissible_octahedral_systems_are_exact
    (A :
      RefinementAtlas
        (LocalizedContext allMorphisms)) :
    ¬ ∀
      (R : RawHigherContextualSystem.{0, 0, 0, 0}
        (Context := OctahedralVertex)),
      IsHigherWAdmissible allMorphisms R →
        HasExactHigherDependentOriginationPresentation
          (W := allMorphisms) A R := by
  intro h
  have hCounter :=
    h counterSystem
      counterSystem_admissible_but_no_higherLocalizationFactorization.1
  exact
    counterSystem_no_exactHigherDependentOriginationPresentation
      A hCounter

/-!
## Boundary after v4.50

The long-range dependent-origination program now has an exact positive sector.

A raw higher contextual system belongs to that sector precisely when there is

  X in DO₂(C,W,A)

and a pointwise-equivalence strong comparison

  restrict(X) --> R.

Existence of this carrier-first data is exactly equivalent to the pre-existing
HigherStackLocalizationFactorization interface.  Equivalently, it is an
ordinary HigherLocalizationFactorization plus an actual stack-descent witness
for its chosen lift.

This separates three levels cleanly:

  weak W-admissibility
      necessary, but not sufficient;

  higher localization factorization
      presentation-localized comparison data;

  exact higher dependent-origination presentation
      factorization whose lift is an actual DO₂ stack object.

The octahedral countermodel lies at the obstruction boundary: it is weakly
admissible but has no object in the exact positive sector for any atlas.

The next theorem unit should address the next genuine universal-property
obligation: essential uniqueness/comparison between two exact presentations
of the same raw system, rather than returning to carrier-specific geometry.
-/

end

end KUOS.DependentOriginationExactHigherPresentationSectorV4_50
