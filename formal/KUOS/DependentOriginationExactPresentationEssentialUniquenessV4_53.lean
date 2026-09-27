import KUOS.DependentOriginationExactPresentationComparisonV4_52
import KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
import KUOS.DependentOriginationExactHigherPresentationSectorV4_50
import KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
import KUOS.DependentOriginationHigherStackCarrierV2_9
import KUOS.DependentOriginationHigherStackDescentV2_8
import KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
import KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
import Mathlib

namespace KUOS.DependentOriginationExactPresentationEssentialUniquenessV4_53

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationExactHigherPresentationSectorV4_50
open KUOS.DependentOriginationExactPresentationComparisonV4_52

open scoped CategoryTheory.Pseudofunctor.StrongTrans

set_option autoImplicit false

noncomputable section

/-!
# Essential uniqueness for a chosen exact presentation v4.53

v4.52 separates the comparison hierarchy for two exact presentations.  In
particular, exactness alone gives only a common-target pointwise-equivalence
cospan, while a coherent directed comparison is stronger data.

The existing v2.19 universal-property interface already contains the precise
missing uniqueness statement for higher-localization factorizations:

* every competing factorization admits a coherent factor into the chosen one;
* any two such coherent factors are isomorphic by an invertible modification.

The present theorem unit transports that statement into the exact DO₂
presentation sector whenever the chosen v2.19 localized lift is itself a stack
for the selected refinement atlas.

Thus the hypotheses are explicit:

  U : CoherentWeakHigherLocalizationUniversalProperty R
  hStack : IsHigherGrothendieckDescentComplete W A U.chosen.lift.

From these data we construct a chosen exact presentation Q_U in DO₂ and prove:

  for every exact presentation P,
    there exists a coherent directed comparison P --> Q_U;

  for any two such comparisons alpha and beta,
    Nonempty (alpha.hom ≅ beta.hom).

This is genuine modification-level essential uniqueness for the chosen exact
presentation.  It is still conditional on the coherent weak localization
universal property and the stack witness; neither hypothesis is silently
derived from weak W-admissibility.

No equivalence between arbitrary exact presentations and no naturality in R is
asserted yet.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- Add stack descent to the chosen factorization of a coherent weak higher
localization universal-property datum. -/
def coherentUniversalPropertyStackFactorization
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (U : CoherentWeakHigherLocalizationUniversalProperty
      (W := W) R)
    (hStack :
      IsHigherGrothendieckDescentComplete W A U.chosen.lift) :
    HigherStackLocalizationFactorization (W := W) A R where
  toHigherLocalizationFactorization := U.chosen
  isStack := hStack

/-- The chosen coherent universal factorization becomes an exact DO₂
presentation as soon as its localized lift satisfies stack descent. -/
def exactPresentationOfCoherentUniversalProperty
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (U : CoherentWeakHigherLocalizationUniversalProperty
      (W := W) R)
    (hStack :
      IsHigherGrothendieckDescentComplete W A U.chosen.lift) :
    ExactHigherDependentOriginationPresentation (W := W) A R :=
  exactPresentationOfHigherStackLocalizationFactorization
    (W := W) A
    (coherentUniversalPropertyStackFactorization
      (W := W) A U hStack)

/-- Forgetting the exact presentation just constructed recovers the chosen
v2.19 higher-localization factorization definitionally. -/
@[simp] theorem exactPresentationOfCoherentUniversalProperty_factorization
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (U : CoherentWeakHigherLocalizationUniversalProperty
      (W := W) R)
    (hStack :
      IsHigherGrothendieckDescentComplete W A U.chosen.lift) :
    exactPresentationFactorization
        (W := W) A
        (exactPresentationOfCoherentUniversalProperty
          (W := W) A U hStack) =
      U.chosen :=
  rfl

/-- The exact presentation produced from U has exactly the chosen localized lift
as its underlying DO₂ carrier value. -/
@[simp] theorem exactPresentationOfCoherentUniversalProperty_carrier_val
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (U : CoherentWeakHigherLocalizationUniversalProperty
      (W := W) R)
    (hStack :
      IsHigherGrothendieckDescentComplete W A U.chosen.lift) :
    higherStackObjectVal (W := W) A
        (exactPresentationOfCoherentUniversalProperty
          (W := W) A U hStack).carrier =
      U.chosen.lift :=
  rfl

/-!
## Exact-presentation universal target
-/

/-- A chosen exact presentation is a coherent universal target among exact
presentations when every exact presentation maps coherently into it and such
maps are essentially unique up to invertible modification. -/
structure ExactPresentationCoherentUniversalTarget
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (Q : ExactHigherDependentOriginationPresentation
      (W := W) A R) where
  factor :
    ∀ P : ExactHigherDependentOriginationPresentation
        (W := W) A R,
      Nonempty
        (ExactPresentationCoherentComparison
          (W := W) A P Q)
  essential_unique :
    ∀
      (P : ExactHigherDependentOriginationPresentation
        (W := W) A R)
      (alpha beta :
        ExactPresentationCoherentComparison
          (W := W) A P Q),
      Nonempty (alpha.hom ≅ beta.hom)

/-- The v2.19 factor-existence field specializes directly to exact
presentations once the chosen factorization is stack-complete. -/
theorem coherentUniversalProperty_hasExactPresentationFactor
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (U : CoherentWeakHigherLocalizationUniversalProperty
      (W := W) R)
    (hStack :
      IsHigherGrothendieckDescentComplete W A U.chosen.lift)
    (P : ExactHigherDependentOriginationPresentation
      (W := W) A R) :
    Nonempty
      (ExactPresentationCoherentComparison
        (W := W) A P
        (exactPresentationOfCoherentUniversalProperty
          (W := W) A U hStack)) := by
  simpa [ExactPresentationCoherentComparison,
    exactPresentationOfCoherentUniversalProperty,
    coherentUniversalPropertyStackFactorization,
    exactPresentationFactorization] using
      U.factor (exactPresentationFactorization (W := W) A P)

/-- The v2.19 essential-uniqueness field becomes modification-level essential
uniqueness of coherent comparisons into the chosen exact presentation. -/
theorem coherentUniversalProperty_exactPresentation_essential_unique
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (U : CoherentWeakHigherLocalizationUniversalProperty
      (W := W) R)
    (hStack :
      IsHigherGrothendieckDescentComplete W A U.chosen.lift)
    (P : ExactHigherDependentOriginationPresentation
      (W := W) A R)
    (alpha beta :
      ExactPresentationCoherentComparison
        (W := W) A P
        (exactPresentationOfCoherentUniversalProperty
          (W := W) A U hStack)) :
    Nonempty (alpha.hom ≅ beta.hom) := by
  simpa [ExactPresentationCoherentComparison,
    exactPresentationOfCoherentUniversalProperty,
    coherentUniversalPropertyStackFactorization,
    exactPresentationFactorization] using
      U.essential_unique
        (exactPresentationFactorization (W := W) A P)
        alpha beta

/-- A coherent weak higher-localization universal property whose chosen lift is
a stack therefore canonically determines a coherent universal target in the
exact presentation sector. -/
def exactPresentationCoherentUniversalTargetOfCoherentUniversalProperty
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (U : CoherentWeakHigherLocalizationUniversalProperty
      (W := W) R)
    (hStack :
      IsHigherGrothendieckDescentComplete W A U.chosen.lift) :
    ExactPresentationCoherentUniversalTarget
      (W := W) A
      (exactPresentationOfCoherentUniversalProperty
        (W := W) A U hStack) where
  factor P :=
    coherentUniversalProperty_hasExactPresentationFactor
      (W := W) A U hStack P
  essential_unique P alpha beta :=
    coherentUniversalProperty_exactPresentation_essential_unique
      (W := W) A U hStack P alpha beta

/-- In particular, every coherent endomorphism comparison of the chosen exact
presentation is isomorphic, as a StrongTrans, to its coherent identity factor. -/
theorem chosenExactPresentation_endomorphism_iso_identity
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (U : CoherentWeakHigherLocalizationUniversalProperty
      (W := W) R)
    (hStack :
      IsHigherGrothendieckDescentComplete W A U.chosen.lift)
    (alpha :
      ExactPresentationCoherentComparison
        (W := W) A
        (exactPresentationOfCoherentUniversalProperty
          (W := W) A U hStack)
        (exactPresentationOfCoherentUniversalProperty
          (W := W) A U hStack)) :
    Nonempty
      (alpha.hom ≅
        (exactPresentationCoherentComparisonId
          (W := W) A
          (exactPresentationOfCoherentUniversalProperty
            (W := W) A U hStack)).hom) := by
  exact
    coherentUniversalProperty_exactPresentation_essential_unique
      (W := W) A U hStack
      (exactPresentationOfCoherentUniversalProperty
        (W := W) A U hStack)
      alpha
      (exactPresentationCoherentComparisonId
        (W := W) A
        (exactPresentationOfCoherentUniversalProperty
          (W := W) A U hStack))

/-!
## Boundary after v4.53

The exact-presentation spine now has a conditional but genuine essential-
uniqueness theorem.

Given a v2.19 coherent weak higher-localization universal property whose chosen
localized lift is a stack, its chosen exact DO₂ presentation Q_U satisfies:

  every exact P has a coherent comparison P --> Q_U;

  any two coherent comparisons P --> Q_U are isomorphic by an invertible
  modification of their underlying StrongTrans.

Therefore the passage

  coherent universal localization + stack descent
      --> chosen exact presentation
      --> factor existence + essential uniqueness

is now formal.

Still open are the stronger global obligations:

* deriving the coherent universal property from the intended admissibility class;
* constructing comparisons between arbitrary exact presentations without first
  choosing a universal target;
* promoting two-sided coherent comparisons to equivalences in DO₂;
* naturality in the raw contextual system;
* the final dependent-origination mapping-property equivalence.
-/

end

end KUOS.DependentOriginationExactPresentationEssentialUniquenessV4_53
