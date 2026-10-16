import KUOS.DependentOriginationExactUniversalTargetMutualUniquenessV4_54
import KUOS.DependentOriginationExactHigherPresentationInvarianceV4_51
import KUOS.DependentOriginationPointwiseEquivalenceTransportV2_17
import Mathlib

namespace KUOS.DependentOriginationExactUniversalTargetNaturalityV4_55

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseEquivalenceTransportV2_17
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationForwardFactorCoherenceSelectionV2_40
open KUOS.DependentOriginationExactHigherPresentationSectorV4_50
open KUOS.DependentOriginationExactHigherPresentationInvarianceV4_51
open KUOS.DependentOriginationExactPresentationComparisonV4_52
open KUOS.DependentOriginationExactPresentationEssentialUniquenessV4_53
open KUOS.DependentOriginationExactUniversalTargetMutualUniquenessV4_54

open scoped CategoryTheory.Pseudofunctor.StrongTrans

set_option autoImplicit false

noncomputable section

/-!
# Naturality of exact universal targets under coherent raw equivalence v4.55

The v4.51 transport theorem shows that an exact presentation can be pushed
forward along a pointwise-equivalence comparison R --> S by keeping the same
DO₂ carrier and composing the comparison map.

For universal targets, a one-way pointwise equivalence is not sufficient:
coherent factor triangles must also be transported.  The minimal input used here
is therefore a coherent two-sided raw equivalence:

  E : R --> S,
  B : S --> R,

both pointwise equivalences, together with invertible modifications

  𝟙 R ≅ E ≫ B,
  B ≫ E ≅ 𝟙 S.

These 2-cells allow comparison triangles to move between the R- and S-sectors
by associativity and whiskering.

The main result is that an exact coherent universal target for R transports to
an exact coherent universal target for S while keeping the same DO₂ carrier.
This is the first genuine naturality theorem for the exact universal object.

The theorem is intentionally stated only for coherent raw equivalences.  It
does not yet claim functoriality for arbitrary raw StrongTrans; that requires
the final mapping-property construction.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- Coherent two-sided equivalence data between raw higher contextual systems.

The forward and backward comparisons are pointwise equivalences of categories,
while the unit/counit are invertible modifications of StrongTrans.  Triangle
identities are not required for the transport theorem below. -/
structure HigherRawSystemCoherentEquivalence
    (R S : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)) where
  forward : HigherPointwiseEquivalenceComparison R S
  backward : HigherPointwiseEquivalenceComparison S R
  unit :
    𝟙 R ≅ forward.comparison ≫ backward.comparison
  counit :
    backward.comparison ≫ forward.comparison ≅ 𝟙 S

/-- Reverse coherent raw-equivalence data. -/
def HigherRawSystemCoherentEquivalence.symm
    {R S : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (E : HigherRawSystemCoherentEquivalence R S) :
    HigherRawSystemCoherentEquivalence S R where
  forward := E.backward
  backward := E.forward
  unit := E.counit.symm
  counit := E.unit.symm

/-- Push an exact presentation forward along coherent raw-equivalence data.
Only the forward pointwise-equivalence comparison is needed at object level. -/
noncomputable def transportExactPresentation
    {R S : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (E : HigherRawSystemCoherentEquivalence R S)
    (P : ExactHigherDependentOriginationPresentation
      (W := W) A R) :
    ExactHigherDependentOriginationPresentation (W := W) A S :=
  exactPresentationOfPointwiseEquivalenceComparison
    (W := W) A P E.forward

@[simp] theorem transportExactPresentation_carrier
    {R S : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (E : HigherRawSystemCoherentEquivalence R S)
    (P : ExactHigherDependentOriginationPresentation
      (W := W) A R) :
    (transportExactPresentation (W := W) A E P).carrier =
      P.carrier :=
  rfl

@[simp] theorem transportExactPresentation_comparison
    {R S : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (E : HigherRawSystemCoherentEquivalence R S)
    (P : ExactHigherDependentOriginationPresentation
      (W := W) A R) :
    (transportExactPresentation (W := W) A E P).comparison =
      P.comparison ≫ E.forward.comparison :=
  rfl

/-- Transport a coherent factor into an R-universal target to a coherent factor
in the S-sector.

The source P is first transported backward to R.  The resulting coherent factor
has the same localized StrongTrans.  Its comparison triangle is then pushed
forward through E using the raw counit B ≫ E ≅ 𝟙 S. -/
noncomputable def transportCoherentComparisonForward
    {R S : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (E : HigherRawSystemCoherentEquivalence R S)
    (P : ExactHigherDependentOriginationPresentation
      (W := W) A S)
    (Q : ExactHigherDependentOriginationPresentation
      (W := W) A R)
    (alpha :
      ExactPresentationCoherentComparison
        (W := W) A
        (transportExactPresentation (W := W) A E.symm P)
        Q) :
    ExactPresentationCoherentComparison
      (W := W) A P
      (transportExactPresentation (W := W) A E Q) where
  hom := alpha.hom
  comparison_triangle := by
    change
      (restrictHigherLocalizedStrongTrans (W := W) alpha.hom ≫
          (Q.comparison ≫ E.forward.comparison)) ≅
        P.comparison
    exact
      (Bicategory.associator
        (restrictHigherLocalizedStrongTrans (W := W) alpha.hom)
        Q.comparison E.forward.comparison).symm ≪≫
      Bicategory.whiskerRightIso
        alpha.comparison_triangle E.forward.comparison ≪≫
      Bicategory.associator
        P.comparison E.backward.comparison E.forward.comparison ≪≫
      Bicategory.whiskerLeftIso P.comparison E.counit ≪≫
      Bicategory.rightUnitor P.comparison

/-- Pull a coherent factor in the S-sector back to the R-sector.

This is the inverse-direction comparison-triangle transport needed to transfer
essential uniqueness.  The raw unit 𝟙 R ≅ E ≫ B is inserted and then the
S-sector triangle is whiskered by B. -/
noncomputable def transportCoherentComparisonBackward
    {R S : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (E : HigherRawSystemCoherentEquivalence R S)
    (P : ExactHigherDependentOriginationPresentation
      (W := W) A S)
    (Q : ExactHigherDependentOriginationPresentation
      (W := W) A R)
    (alpha :
      ExactPresentationCoherentComparison
        (W := W) A P
        (transportExactPresentation (W := W) A E Q)) :
    ExactPresentationCoherentComparison
      (W := W) A
      (transportExactPresentation (W := W) A E.symm P)
      Q where
  hom := alpha.hom
  comparison_triangle := by
    change
      (restrictHigherLocalizedStrongTrans (W := W) alpha.hom ≫
          Q.comparison) ≅
        P.comparison ≫ E.backward.comparison
    exact
      (Bicategory.rightUnitor
        (restrictHigherLocalizedStrongTrans (W := W) alpha.hom ≫
          Q.comparison)).symm ≪≫
      Bicategory.whiskerLeftIso
        (restrictHigherLocalizedStrongTrans (W := W) alpha.hom ≫
          Q.comparison) E.unit ≪≫
      (Bicategory.associator
        (restrictHigherLocalizedStrongTrans (W := W) alpha.hom ≫
          Q.comparison)
        E.forward.comparison E.backward.comparison).symm ≪≫
      Bicategory.whiskerRightIso
        (Bicategory.associator
          (restrictHigherLocalizedStrongTrans (W := W) alpha.hom)
          Q.comparison E.forward.comparison)
        E.backward.comparison ≪≫
      Bicategory.whiskerRightIso
        alpha.comparison_triangle E.backward.comparison

@[simp] theorem transportCoherentComparisonForward_hom
    {R S : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (E : HigherRawSystemCoherentEquivalence R S)
    (P : ExactHigherDependentOriginationPresentation
      (W := W) A S)
    (Q : ExactHigherDependentOriginationPresentation
      (W := W) A R)
    (alpha :
      ExactPresentationCoherentComparison
        (W := W) A
        (transportExactPresentation (W := W) A E.symm P)
        Q) :
    (transportCoherentComparisonForward
      (W := W) A E P Q alpha).hom =
      alpha.hom :=
  rfl

@[simp] theorem transportCoherentComparisonBackward_hom
    {R S : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (E : HigherRawSystemCoherentEquivalence R S)
    (P : ExactHigherDependentOriginationPresentation
      (W := W) A S)
    (Q : ExactHigherDependentOriginationPresentation
      (W := W) A R)
    (alpha :
      ExactPresentationCoherentComparison
        (W := W) A P
        (transportExactPresentation (W := W) A E Q)) :
    (transportCoherentComparisonBackward
      (W := W) A E P Q alpha).hom =
      alpha.hom :=
  rfl

/-- Factor existence transports from an R-universal exact presentation to its
forward transport in the S-sector. -/
theorem transportedUniversalTarget_hasFactor
    {R S : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (E : HigherRawSystemCoherentEquivalence R S)
    (Q : ExactHigherDependentOriginationPresentation
      (W := W) A R)
    (T : ExactPresentationCoherentUniversalTarget
      (W := W) A Q)
    (P : ExactHigherDependentOriginationPresentation
      (W := W) A S) :
    Nonempty
      (ExactPresentationCoherentComparison
        (W := W) A P
        (transportExactPresentation (W := W) A E Q)) := by
  rcases
      T.factor
        (transportExactPresentation (W := W) A E.symm P) with
    ⟨alpha⟩
  exact
    ⟨transportCoherentComparisonForward
      (W := W) A E P Q alpha⟩

/-- Essential uniqueness also transports: pull both S-sector coherent factors
back to R, apply uniqueness there, and use preservation of the underlying
StrongTrans. -/
theorem transportedUniversalTarget_essentialUnique
    {R S : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (E : HigherRawSystemCoherentEquivalence R S)
    (Q : ExactHigherDependentOriginationPresentation
      (W := W) A R)
    (T : ExactPresentationCoherentUniversalTarget
      (W := W) A Q)
    (P : ExactHigherDependentOriginationPresentation
      (W := W) A S)
    (alpha beta :
      ExactPresentationCoherentComparison
        (W := W) A P
        (transportExactPresentation (W := W) A E Q)) :
    Nonempty (alpha.hom ≅ beta.hom) := by
  let alphaR :=
    transportCoherentComparisonBackward
      (W := W) A E P Q alpha
  let betaR :=
    transportCoherentComparisonBackward
      (W := W) A E P Q beta
  rcases
      T.essential_unique
        (transportExactPresentation (W := W) A E.symm P)
        alphaR betaR with
    ⟨e⟩
  change alpha.hom ≅ beta.hom at e
  exact ⟨e⟩

/-- Main naturality theorem: exact coherent universal targets are preserved by
coherent equivalence of raw higher contextual systems.  The DO₂ carrier is
definitionally unchanged. -/
noncomputable def transportExactUniversalTarget
    {R S : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (E : HigherRawSystemCoherentEquivalence R S)
    (Q : ExactHigherDependentOriginationPresentation
      (W := W) A R)
    (T : ExactPresentationCoherentUniversalTarget
      (W := W) A Q) :
    ExactPresentationCoherentUniversalTarget
      (W := W) A
      (transportExactPresentation (W := W) A E Q) where
  factor P :=
    transportedUniversalTarget_hasFactor
      (W := W) A E Q T P
  essential_unique P alpha beta :=
    transportedUniversalTarget_essentialUnique
      (W := W) A E Q T P alpha beta

/-- The transported universal target has exactly the same object of DO₂ as the
original one. -/
@[simp] theorem transportExactUniversalTarget_carrier
    {R S : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)}
    (E : HigherRawSystemCoherentEquivalence R S)
    (Q : ExactHigherDependentOriginationPresentation
      (W := W) A R)
    (T : ExactPresentationCoherentUniversalTarget
      (W := W) A Q) :
    (transportExactPresentation (W := W) A E Q).carrier =
      Q.carrier :=
  rfl

/-!
## Boundary after v4.55

The exact universal realization is now natural under coherent equivalences of
raw higher contextual systems:

  R  <==coherent raw equivalence==>  S

transports an exact coherent universal target for R to one for S without
changing its DO₂ carrier.

Together with v4.54 fixed-R mutual essential uniqueness, this supplies the
object-level uniqueness and equivalence-naturality layers demanded by the
roadmap.

Still open is functoriality for arbitrary admissible raw morphisms and the final
mapping-property equivalence.  Those require constructing the realization on
morphisms rather than merely transporting it along equivalences.
-/

end

end KUOS.DependentOriginationExactUniversalTargetNaturalityV4_55
