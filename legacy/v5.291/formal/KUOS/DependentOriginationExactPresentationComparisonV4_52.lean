import KUOS.DependentOriginationExactHigherPresentationInvarianceV4_51
import KUOS.DependentOriginationPointwiseEquivalenceTransportV2_17
import KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
import KUOS.DependentOriginationCoherentFactorForgetfulBridgeV2_20
import KUOS.DependentOriginationForwardFactorCoherenceSelectionV2_40
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
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationCoherentFactorForgetfulBridgeV2_20
open KUOS.DependentOriginationForwardFactorCoherenceSelectionV2_40
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

The purpose of v4.52 is to separate comparison levels rather than silently
identify them.

From P and Q alone one canonically has the common-target cospan

  restrict(P.carrier) --> R <-- restrict(Q.carrier),

whose two legs are pointwise equivalences.

The older v2.19 interface already gives the correct stronger notion of a
coherent directed factor comparison: a StrongTrans between localized lifts
together with an invertible modification witnessing compatibility with the raw
comparison maps.  We reuse that interface here instead of inventing a second
notion.

For exact presentations, a coherent directed factor comparison has two
unconditional consequences:

* its StrongTrans is a genuine directed 1-morphism between the DO₂ carriers,
  because DO₂ is full on 1-morphisms;
* after restriction to the raw context, its components are equivalences of
  categories.  This follows by two-out-of-three from the coherent comparison
  triangle and the two exact-presentation comparison equivalences.

What is *not* asserted is equally important.  The canonical cospan does not by
itself produce a coherent directed factor map.  A coherent directed comparison
is not automatically bundled here as a pseudonatural equivalence or an
equivalence in DO₂, and no essential uniqueness up to modification is inferred
without the corresponding universal-property hypothesis.
-/

universe u v uH vH
universe u₁ u₂ u₃ v₁ v₂ v₃

/-- Explicit two-out-of-three wrapper for category equivalences.

The Mathlib cancellation theorem takes its two equivalence witnesses as
instance-implicit arguments.  Keeping those witnesses as ordinary arguments at
this boundary prevents local `let` unfolding from changing the instance-search
key before the cancellation theorem is applied. -/
private theorem isEquivalenceOfCompRightExplicit
    {C : Type u₁} [Category.{v₁} C]
    {D : Type u₂} [Category.{v₂} D]
    {E : Type u₃} [Category.{v₃} E]
    (F : C ⥤ D) (G : D ⥤ E)
    (hG : G.IsEquivalence)
    (hFG : (F ⋙ G).IsEquivalence) :
    F.IsEquivalence := by
  let _ : G.IsEquivalence := hG
  let _ : (F ⋙ G).IsEquivalence := hFG
  exact Functor.isEquivalence_of_comp_right F G

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
  leftLeg :
    HigherPointwiseEquivalenceComparison
      (exactPresentationRestrictedCarrier (W := W) A P) R
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

@[simp] theorem exactPresentationComparisonCospan_left_comparison
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (P Q : ExactHigherDependentOriginationPresentation
      (W := W) A R) :
    (exactPresentationComparisonCospan (W := W) A P Q).leftLeg.comparison =
      P.comparison :=
  rfl

@[simp] theorem exactPresentationComparisonCospan_right_comparison
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (P Q : ExactHigherDependentOriginationPresentation
      (W := W) A R) :
    (exactPresentationComparisonCospan (W := W) A P Q).rightLeg.comparison =
      Q.comparison :=
  rfl

/-!
## Exact presentations as v2.10 factorizations
-/

/-- Forget only the stack witness of an exact presentation, retaining the
localized lift and its pointwise-equivalence comparison to the raw system. -/
def exactPresentationFactorization
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (P : ExactHigherDependentOriginationPresentation
      (W := W) A R) :
    HigherLocalizationFactorization (W := W) R :=
  (higherStackLocalizationFactorizationOfExactPresentation
    (W := W) A P).toHigherLocalizationFactorization

@[simp] theorem exactPresentationFactorization_lift
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (P : ExactHigherDependentOriginationPresentation
      (W := W) A R) :
    (exactPresentationFactorization (W := W) A P).lift =
      higherStackObjectVal (W := W) A P.carrier :=
  rfl

@[simp] theorem exactPresentationFactorization_comparison
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (P : ExactHigherDependentOriginationPresentation
      (W := W) A R) :
    (exactPresentationFactorization (W := W) A P).comparison =
      P.comparison :=
  rfl

/-!
## Coherent directed comparison level

This is the existing v2.19 notion specialized to exact presentations.  Its
comparison triangle is an invertible modification, not merely an objectwise
family of unrelated natural isomorphisms.
-/

/-- A coherent directed comparison from exact presentation P to exact
presentation Q. -/
abbrev ExactPresentationCoherentComparison
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (P Q : ExactHigherDependentOriginationPresentation
      (W := W) A R) :=
  CoherentHigherLocalizationFactorMorphism
    (W := W)
    (exactPresentationFactorization (W := W) A P)
    (exactPresentationFactorization (W := W) A Q)

/-- Existence of a coherent directed comparison is deliberately kept separate
from the canonical pointwise-equivalence cospan. -/
def HasExactPresentationCoherentComparison
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (P Q : ExactHigherDependentOriginationPresentation
      (W := W) A R) : Prop :=
  Nonempty (ExactPresentationCoherentComparison (W := W) A P Q)

/-- Coherent comparison is reflexive. -/
noncomputable def exactPresentationCoherentComparisonId
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (P : ExactHigherDependentOriginationPresentation
      (W := W) A R) :
    ExactPresentationCoherentComparison (W := W) A P P :=
  coherentHigherLocalizationFactorMorphismId
    (W := W) (exactPresentationFactorization (W := W) A P)

/-- Coherent directed comparisons compose. -/
noncomputable def exactPresentationCoherentComparisonComp
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    {P Q T : ExactHigherDependentOriginationPresentation
      (W := W) A R}
    (alpha : ExactPresentationCoherentComparison (W := W) A P Q)
    (beta : ExactPresentationCoherentComparison (W := W) A Q T) :
    ExactPresentationCoherentComparison (W := W) A P T :=
  coherentHigherLocalizationFactorMorphismComp (W := W) alpha beta

/-- Any coherent directed exact-presentation comparison gives a genuine
1-morphism between the corresponding objects of DO₂. -/
noncomputable def exactPresentationCoherentComparisonToCompletion2Hom
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    {P Q : ExactHigherDependentOriginationPresentation
      (W := W) A R}
    (alpha : ExactPresentationCoherentComparison (W := W) A P Q) :
    P.carrier ⟶ Q.carrier := by
  apply completion2MkHom (W := W) A
  change
    (exactPresentationFactorization (W := W) A P).lift ⟶
      (exactPresentationFactorization (W := W) A Q).lift
  exact alpha.hom

/-!
## Pointwise-equivalence consequence on the raw restriction

A coherent factor map between exact presentations is automatically pointwise an
equivalence after restriction to every raw context object.  This is not assumed:
it follows from the modification triangle and the exactness of the two
presentation legs.
-/

/-- Componentwise equivalence of the coherent localized factor at every object
hit by the presentation unit. -/
def IsExactPresentationCoherentComparisonRestrictedPointwiseEquivalence
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    {P Q : ExactHigherDependentOriginationPresentation
      (W := W) A R}
    (alpha : ExactPresentationCoherentComparison (W := W) A P Q) : Prop :=
  ∀ X : Context,
    (alpha.hom.app
      (.mk ((higherPresentationUnitFunctor W).obj X))).toFunctor.IsEquivalence

/-- Two-out-of-three proves restricted pointwise equivalence for every coherent
comparison between exact presentations. -/
theorem exactPresentationCoherentComparison_restrictedPointwiseEquivalence
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    {P Q : ExactHigherDependentOriginationPresentation
      (W := W) A R}
    (alpha : ExactPresentationCoherentComparison (W := W) A P Q) :
    IsExactPresentationCoherentComparisonRestrictedPointwiseEquivalence
      (W := W) A alpha := by
  intro X
  let F :=
    (alpha.hom.app
      (.mk ((higherPresentationUnitFunctor W).obj X))).toFunctor
  let G :=
    (Q.comparison.app (.mk X)).toFunctor
  let H :=
    (P.comparison.app (.mk X)).toFunctor
  have hG : G.IsEquivalence := by
    change (Q.comparison.app (.mk X)).toFunctor.IsEquivalence
    exact Q.comparison_isEquivalence X
  have hH : H.IsEquivalence := by
    change (P.comparison.app (.mk X)).toFunctor.IsEquivalence
    exact P.comparison_isEquivalence X
  have htriangle : F ⋙ G ≅ H := by
    dsimp [F, G, H]
    simpa [exactPresentationFactorization] using
      (coherentComparisonTriangleNatIso (W := W) alpha X)
  have hFG : (F ⋙ G).IsEquivalence :=
    (Functor.isEquivalence_iff_of_iso htriangle).2 hH
  have hF : F.IsEquivalence :=
    isEquivalenceOfCompRightExplicit F G hG hFG
  simpa [F] using hF

/-- Therefore every coherent exact-presentation comparison restricts to the
v2.17 notion of directed pointwise-equivalence comparison between the two raw
restricted carriers. -/
noncomputable def
    restrictedPointwiseEquivalenceComparisonOfExactCoherentComparison
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    {P Q : ExactHigherDependentOriginationPresentation
      (W := W) A R}
    (alpha : ExactPresentationCoherentComparison (W := W) A P Q) :
    HigherPointwiseEquivalenceComparison
      (exactPresentationRestrictedCarrier (W := W) A P)
      (exactPresentationRestrictedCarrier (W := W) A Q) where
  comparison := by
    change
      restrictHigherLocalizedSystem W
          (exactPresentationFactorization (W := W) A P).lift ⟶
        restrictHigherLocalizedSystem W
          (exactPresentationFactorization (W := W) A Q).lift
    exact restrictHigherLocalizedStrongTrans (W := W) alpha.hom
  comparison_isEquivalence := by
    intro X
    simpa [exactPresentationRestrictedCarrier, exactPresentationFactorization] using
      exactPresentationCoherentComparison_restrictedPointwiseEquivalence
        (W := W) A alpha X

/-- Existence of a coherent comparison implies existence of a directed
pointwise-equivalence comparison between the restricted carriers. -/
theorem hasDirectedRestrictedPointwiseComparison_of_coherentComparison
    {R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    {P Q : ExactHigherDependentOriginationPresentation
      (W := W) A R}
    (h :
      HasExactPresentationCoherentComparison (W := W) A P Q) :
    Nonempty
      (HigherPointwiseEquivalenceComparison
        (exactPresentationRestrictedCarrier (W := W) A P)
        (exactPresentationRestrictedCarrier (W := W) A Q)) := by
  rcases h with ⟨alpha⟩
  exact
    ⟨restrictedPointwiseEquivalenceComparisonOfExactCoherentComparison
      (W := W) A alpha⟩

/-!
## Boundary after v4.52

The proven hierarchy is now explicit:

  two exact presentations P,Q
        |
        | unconditional
        v
  restrict(P) --> R <-- restrict(Q)
  both legs pointwise equivalences

  coherent directed factor P --> Q
        |
        +--> directed DO₂ 1-morphism
        |
        +--> restricted pointwise-equivalence comparison
             restrict(P) --> restrict(Q).

Identity and composition of coherent directed factors are inherited from the
already-proved v2.40 constructions.

The missing implications are intentionally not asserted:

* the canonical cospan does not yet produce a coherent directed factor P --> Q;
* restricted pointwise equivalence is not promoted here to a chosen
  pseudonatural inverse/equivalence;
* a directed DO₂ 1-morphism is not identified with an equivalence in DO₂;
* essential uniqueness up to modification requires a genuine universal-property
  hypothesis.

This is the exact comparison frontier required before v4.53 essential
uniqueness and naturality.
-/

end

end KUOS.DependentOriginationExactPresentationComparisonV4_52
