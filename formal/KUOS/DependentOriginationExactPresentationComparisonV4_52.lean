import KUOS.DependentOriginationExactHigherPresentationInvarianceV4_51
import KUOS.DependentOriginationPointwiseEquivalenceTransportV2_17
import KUOS.DependentOriginationHigherStackCarrierV2_9
import KUOS.DependentOriginationHigherStackDescentV2_8
import KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
import KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
import Mathlib

namespace KUOS.DependentOriginationExactPresentationComparisonV4_52

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseEquivalenceTransportV2_17
open KUOS.DependentOriginationExactHigherPresentationSectorV4_50
open KUOS.DependentOriginationExactHigherPresentationInvarianceV4_51

open scoped CategoryTheory.Pseudofunctor.StrongTrans

set_option autoImplicit false

noncomputable section

/-!
# Comparison data between exact higher presentations v4.52

Let

  P Q : ExactHigherDependentOriginationPresentation R

be two exact presentations of the same raw Cat-valued contextual system.

It is essential not to collapse several different notions of comparison.
From the exact-presentation data alone we canonically have the cospan

  restrict(P.carrier) --> R <-- restrict(Q.carrier),

and both legs are pointwise equivalences.  This is already genuine comparison
information, but it is not yet a directed strong transformation between the two
localized carriers, a pseudonatural equivalence, an equivalence in DO₂, or a
uniqueness statement up to modification.

This file records that exact boundary in the types.

First we package the canonical pointwise-equivalence cospan.  Then we show that
if a coherent reverse pointwise-equivalence comparison from R to one restricted
carrier is supplied, the v2.17 composition operation produces a directed
comparison between the restricted carriers.

Separately, we define the stronger localized-carrier comparison interface.  Any
ambient strong transformation between two stack carriers lifts to a 1-morphism
in DO₂ because the carrier is a full induced bicategory.  Pointwise equivalence
of such a localized transformation is recorded as an additional property rather
than inferred from the raw cospan.

Thus v4.52 proves exactly the comparison data currently available and exposes
the coherence still required for essential uniqueness.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- The raw contextual system obtained by restricting the DO₂ carrier of an
exact presentation back along the presentation-localization unit. -/
abbrev exactPresentationRestrictedCarrier
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (P : ExactHigherDependentOriginationPresentation
      (W := W) A R) :
    RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context) :=
  restrictHigherLocalizedSystem W
    (higherStackObjectVal (W := W) A P.carrier)

/-- Every exact presentation canonically gives a directed pointwise-equivalence
comparison from its restricted DO₂ carrier to the raw system it presents. -/
def exactPresentationToRawComparison
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (P : ExactHigherDependentOriginationPresentation
      (W := W) A R) :
    HigherPointwiseEquivalenceComparison
      (exactPresentationRestrictedCarrier (W := W) A P) R where
  comparison := P.comparison
  comparison_isEquivalence := P.comparison_isEquivalence

/-- The comparison data canonically available from two exact presentations of
the same raw system: a common-target cospan with pointwise-equivalence legs. -/
structure ExactPresentationComparisonCospan
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (P Q : ExactHigherDependentOriginationPresentation
      (W := W) A R) where
  /-- Left presentation leg into the common raw target. -/
  leftLeg :
    HigherPointwiseEquivalenceComparison
      (exactPresentationRestrictedCarrier (W := W) A P) R
  /-- Right presentation leg into the common raw target. -/
  rightLeg :
    HigherPointwiseEquivalenceComparison
      (exactPresentationRestrictedCarrier (W := W) A Q) R

/-- Two exact presentations always determine their canonical
pointwise-equivalence comparison cospan. -/
def exactPresentationComparisonCospan
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (P Q : ExactHigherDependentOriginationPresentation
      (W := W) A R) :
    ExactPresentationComparisonCospan (W := W) A P Q where
  leftLeg := exactPresentationToRawComparison (W := W) A P
  rightLeg := exactPresentationToRawComparison (W := W) A Q

/-- The left leg of the canonical cospan is literally the comparison stored in
the first exact presentation. -/
@[simp] theorem exactPresentationComparisonCospan_left_comparison
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (P Q : ExactHigherDependentOriginationPresentation
      (W := W) A R) :
    (exactPresentationComparisonCospan (W := W) A P Q).leftLeg.comparison =
      P.comparison :=
  rfl

/-- The right leg of the canonical cospan is literally the comparison stored in
the second exact presentation. -/
@[simp] theorem exactPresentationComparisonCospan_right_comparison
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (P Q : ExactHigherDependentOriginationPresentation
      (W := W) A R) :
    (exactPresentationComparisonCospan (W := W) A P Q).rightLeg.comparison =
      Q.comparison :=
  rfl

/-- Existence of a directed pointwise-equivalence comparison between the two
restricted carriers.  This is deliberately stronger than the canonical cospan. -/
def HasDirectedRestrictedCarrierComparison
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (P Q : ExactHigherDependentOriginationPresentation
      (W := W) A R) : Prop :=
  Nonempty
    (HigherPointwiseEquivalenceComparison
      (exactPresentationRestrictedCarrier (W := W) A P)
      (exactPresentationRestrictedCarrier (W := W) A Q))

/-- A supplied coherent reverse comparison from the common raw target to the
second restricted carrier converts the canonical cospan into a directed
comparison from the first restricted carrier to the second. -/
noncomputable def directedRestrictedCarrierComparisonOfRightReverse
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (P Q : ExactHigherDependentOriginationPresentation
      (W := W) A R)
    (ERQ :
      HigherPointwiseEquivalenceComparison R
        (exactPresentationRestrictedCarrier (W := W) A Q)) :
    HigherPointwiseEquivalenceComparison
      (exactPresentationRestrictedCarrier (W := W) A P)
      (exactPresentationRestrictedCarrier (W := W) A Q) :=
  HigherPointwiseEquivalenceComparison.comp
    (exactPresentationToRawComparison (W := W) A P) ERQ

/-- Existence-level form of the preceding construction. -/
theorem hasDirectedRestrictedCarrierComparison_of_rightReverse
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (P Q : ExactHigherDependentOriginationPresentation
      (W := W) A R)
    (hERQ :
      Nonempty
        (HigherPointwiseEquivalenceComparison R
          (exactPresentationRestrictedCarrier (W := W) A Q))) :
    HasDirectedRestrictedCarrierComparison (W := W) A P Q := by
  rcases hERQ with ⟨ERQ⟩
  exact
    ⟨directedRestrictedCarrierComparisonOfRightReverse
      (W := W) A P Q ERQ⟩

/-- With coherent reverse comparisons from the common raw target to both
restricted carriers, one gets directed pointwise-equivalence comparisons in
both directions. -/
structure BidirectionalRestrictedCarrierComparison
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (P Q : ExactHigherDependentOriginationPresentation
      (W := W) A R) where
  forward :
    HigherPointwiseEquivalenceComparison
      (exactPresentationRestrictedCarrier (W := W) A P)
      (exactPresentationRestrictedCarrier (W := W) A Q)
  backward :
    HigherPointwiseEquivalenceComparison
      (exactPresentationRestrictedCarrier (W := W) A Q)
      (exactPresentationRestrictedCarrier (W := W) A P)

/-- Construct bidirectional restricted-carrier comparison data from reverse
pointwise-equivalence comparisons to both presentations. -/
noncomputable def bidirectionalRestrictedCarrierComparisonOfRawReverses
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (P Q : ExactHigherDependentOriginationPresentation
      (W := W) A R)
    (ERP :
      HigherPointwiseEquivalenceComparison R
        (exactPresentationRestrictedCarrier (W := W) A P))
    (ERQ :
      HigherPointwiseEquivalenceComparison R
        (exactPresentationRestrictedCarrier (W := W) A Q)) :
    BidirectionalRestrictedCarrierComparison (W := W) A P Q where
  forward :=
    directedRestrictedCarrierComparisonOfRightReverse
      (W := W) A P Q ERQ
  backward :=
    directedRestrictedCarrierComparisonOfRightReverse
      (W := W) A Q P ERP

/-!
## Stronger localized-carrier comparison level

A strong transformation between the localized stack carriers is strictly more
data than the canonical raw cospan.  We therefore name it separately.
-/

/-- A directed ambient strong transformation between the actual localized
stack carriers of two exact presentations. -/
abbrev LocalizedCarrierStrongComparison
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (P Q : ExactHigherDependentOriginationPresentation
      (W := W) A R) :=
  higherStackObjectVal (W := W) A P.carrier ⟶
    higherStackObjectVal (W := W) A Q.carrier

/-- Pointwise equivalence is an additional property of a localized-carrier
strong comparison; it is not identified with mere existence of that
transformation. -/
def IsLocalizedCarrierPointwiseEquivalence
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    {P Q : ExactHigherDependentOriginationPresentation
      (W := W) A R}
    (η : LocalizedCarrierStrongComparison (W := W) A P Q) : Prop :=
  ∀ S : HigherLocalizedSite W,
    (η.app S).toFunctor.IsEquivalence

/-- Bundled directed localized comparison together with the stronger
pointwise-equivalence property. -/
structure ExactPresentationLocalizedPointwiseEquivalenceComparison
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (P Q : ExactHigherDependentOriginationPresentation
      (W := W) A R) where
  comparison : LocalizedCarrierStrongComparison (W := W) A P Q
  comparison_isEquivalence :
    IsLocalizedCarrierPointwiseEquivalence (W := W) A comparison

/-- Since DO₂ is the full induced bicategory on stack objects, every ambient
localized strong comparison canonically becomes a 1-morphism in DO₂. -/
noncomputable def completion2HomOfLocalizedCarrierStrongComparison
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    {P Q : ExactHigherDependentOriginationPresentation
      (W := W) A R}
    (η : LocalizedCarrierStrongComparison (W := W) A P Q) :
    P.carrier ⟶ Q.carrier :=
  completion2MkHom W A η

/-- The bundled pointwise-equivalence localized comparison therefore supplies a
directed 1-morphism in DO₂, while equivalence *inside* DO₂ remains a separate
stronger obligation. -/
noncomputable def
    ExactPresentationLocalizedPointwiseEquivalenceComparison.toCompletion2Hom
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    {P Q : ExactHigherDependentOriginationPresentation
      (W := W) A R}
    (E :
      ExactPresentationLocalizedPointwiseEquivalenceComparison
        (W := W) A P Q) :
    P.carrier ⟶ Q.carrier :=
  completion2HomOfLocalizedCarrierStrongComparison
    (W := W) A E.comparison

/-!
## Boundary after v4.52

For two exact presentations P and Q of the same raw system R, the theorem-level
data now established without extra hypotheses is exactly

  restrict(P.carrier) --> R <-- restrict(Q.carrier),

with both legs pointwise equivalences.

A directed comparison between the two restricted carriers follows once a
coherent reverse pointwise-equivalence comparison from R to one leg is supplied.
A strong transformation between the *localized* carriers is separately packaged;
because DO₂ is full, such a transformation yields a directed DO₂ 1-morphism.
Pointwise equivalence of that localized transformation is another explicit
property.

No theorem here identifies any of these with:

* a pseudonatural equivalence;
* an equivalence object/1-cell in DO₂;
* uniqueness up to modification.

Those are precisely the essential-uniqueness/coherence obligations for v4.53+.
-/

end

end KUOS.DependentOriginationExactPresentationComparisonV4_52
