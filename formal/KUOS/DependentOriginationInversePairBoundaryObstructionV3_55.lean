import KUOS.DependentOriginationCompositeIdentityInversePairReductionV3_54

namespace KUOS.DependentOriginationInversePairBoundaryObstructionV3_55

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationThreeRouteCorrectionCompatibilityGapV3_09
open KUOS.DependentOriginationQuotientGaugeIntersectionObstructionV3_11
open KUOS.DependentOriginationAssociatorUnitorTriangleResidualV3_26
open KUOS.DependentOriginationQuotientSplitDirectionalSeparationV3_33
open KUOS.DependentOriginationUnitorWitnessCorrelationV3_35
open KUOS.DependentOriginationFiniteAssociatorScheduleV3_38
open KUOS.DependentOriginationAssociatorIncidenceDecompositionV3_41
open KUOS.DependentOriginationFreshBoundaryCompatibilityV3_47
open KUOS.DependentOriginationGlobalCancellationFromSourceComplementsV3_52
open KUOS.DependentOriginationFreshBoundaryRightIdentityReductionV3_53
open KUOS.DependentOriginationCompositeIdentityInversePairReductionV3_54

universe u v uH vH

set_option autoImplicit false

noncomputable section

/-!
# Inverse-pair fresh-boundary obstruction v3.55

v3.54 shows that the final v3.53 composite-identity branch becomes an actual
two-sided inverse pair as soon as either directional global source-complement
hypothesis supplies the corresponding localization cancellation.

This module asks the next question without assuming its answer.

First, inverse-pair geometry is strong enough to remove the earlier semantic
separation issue.  If

```text
f : X ⟶ Y
g : Y ⟶ X
f ≫ g = 𝟙 X
g ≫ f = 𝟙 Y,
```

then the chosen quotient representative evaluations of both `f` and `g`
are essentially surjective and faithful by the v3.33 section/retraction
lemmas.  Consequently both middle-identity whiskering directions satisfy the
existing semantic separation predicate.

Second, this still does not manufacture the v3.47 solved-leading equation for
`associator f g h`.  We therefore name the exact remaining sector:
fresh-boundary + inverse-pair geometry + failure of the unique leading
compatibility equation.

Under a common unitor gauge and v3.52 left source complements, this new
predicate is equivalent to the previous fresh-boundary leading obstruction.
Thus the residual is no longer attributable to missing source cancellation or
missing representative EssSurj/Faithful separation.  It is exactly the
inverse-pair leading compatibility question.

The all-associator theorem is correspondingly sharpened: under both global
source-complement hypotheses, it is enough to assume boundary compatibility
only for fresh-boundary inverse-pair tasks.

No claim is made that inverse-pair compatibility is automatic.  In
particular, no pentagon propagation theorem for arbitrary quotient gauge
choices is assumed or inferred here.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (R : RawHigherContextualSystem.{u, v, uH, vH}
  (Context := Context))
variable (D : PointwiseWAdjointEquivalenceData (W := W) R)

/-- An actual inverse pair makes both quotient representative evaluations
essentially surjective and faithful. -/
theorem inversePair_representative_essSurj_faithful
    {X Y : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ X)
    (hfg : f ≫ g = 𝟙 X)
    (hgf : g ≫ f = 𝟙 Y) :
    (quotientRepresentativeMap W R D f).toFunctor.EssSurj ∧
      (quotientRepresentativeMap W R D f).toFunctor.Faithful ∧
      (quotientRepresentativeMap W R D g).toFunctor.EssSurj ∧
      (quotientRepresentativeMap W R D g).toFunctor.Faithful := by
  exact
    ⟨quotientRepresentativeMap_essSurj_of_section W R D f g hgf,
      quotientRepresentativeMap_faithful_of_retraction W R D f g hfg,
      quotientRepresentativeMap_essSurj_of_section W R D g f hfg,
      quotientRepresentativeMap_faithful_of_retraction W R D g f hgf⟩

/-- The same inverse pair supplies the v3.26/v3.28 semantic whiskering
separation in both orientations. -/
theorem inversePair_middleIdentityWhiskerSeparating
    {X Y : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ X)
    (hfg : f ≫ g = 𝟙 X)
    (hgf : g ≫ f = 𝟙 Y) :
    MiddleIdentityWhiskerSeparating W R D f g ∧
      MiddleIdentityWhiskerSeparating W R D g f := by
  exact
    ⟨middleIdentityWhiskerSeparating_of_section_retraction
        W R D f g g f hgf hgf,
      middleIdentityWhiskerSeparating_of_section_retraction
        W R D g f f g hfg hfg⟩

/-- Task-packaged representative separation for the v3.54 inverse-pair
sector. -/
theorem inversePairTask_representative_essSurj_faithful
    (a : AssociatorTask W)
    (hInverse : IsCompositeInversePairAssociatorTask W a) :
    (quotientRepresentativeMap W R D a.f).toFunctor.EssSurj ∧
      (quotientRepresentativeMap W R D a.f).toFunctor.Faithful ∧
      (quotientRepresentativeMap W R D a.g).toFunctor.EssSurj ∧
      (quotientRepresentativeMap W R D a.g).toFunctor.Faithful := by
  rcases hInverse with ⟨X, Y, T, f, g, h, hfg, hgf, rfl⟩
  exact inversePair_representative_essSurj_faithful
    W R D f g hfg hgf

/-- Exact remaining fresh-boundary sector after the v3.54 inverse-pair
reduction. -/
noncomputable def InversePairFreshBoundaryLeadingObstruction
    (Q : GeneratedQuotientGaugeParameters W R D)
    (a : AssociatorTask W) : Prop :=
  FreshBoundaryAssociatorTask W a ∧
    IsCompositeInversePairAssociatorTask W a ∧
    ¬ AssociatorLeadingCompatible W R D Q a.f a.g a.h

/-- On a task already known to be fresh-boundary and inverse-pair, the new
predicate is exactly failure of correction. -/
theorem inversePairFreshBoundaryLeadingObstruction_iff_not_corrected
    (Q : GeneratedQuotientGaugeParameters W R D)
    (a : AssociatorTask W)
    (hBoundary : FreshBoundaryAssociatorTask W a)
    (hInverse : IsCompositeInversePairAssociatorTask W a) :
    InversePairFreshBoundaryLeadingObstruction W R D Q a ↔
      Q ∉ quotientRouteCorrectionLocus W R D
        (associatorTaskRoute W a) := by
  constructor
  · intro hObstruction hCorrect
    exact hObstruction.2.2
      ((freshBoundaryTask_corrected_iff_leadingCompatible
        W R D Q a hBoundary).1 hCorrect)
  · intro hNotCorrect
    refine ⟨hBoundary, hInverse, ?_⟩
    intro hCompatible
    exact hNotCorrect
      ((freshBoundaryTask_corrected_iff_leadingCompatible
        W R D Q a hBoundary).2 hCompatible)

/-- Under common unitors and global left source complements, the v3.47
fresh-boundary obstruction is exactly the inverse-pair obstruction above. -/
theorem freshBoundaryLeadingObstruction_iff_inversePair_of_unitors_of_leftSourceComplements
    (Q : GeneratedQuotientGaugeParameters W R D)
    (hUnit : ∀ X (s : UnitorRouteAt W X),
      Q ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s))
    (hLeft : HasLeftWCompositeComplements W)
    (a : AssociatorTask W) :
    FreshBoundaryLeadingObstruction W R D Q a ↔
      InversePairFreshBoundaryLeadingObstruction W R D Q a := by
  constructor
  · intro hObstruction
    refine ⟨hObstruction.1, ?_, hObstruction.2⟩
    exact
      freshBoundaryLeadingObstruction_isCompositeInversePair_of_leftSourceComplements
        W R D Q hUnit hLeft a hObstruction
  · intro hObstruction
    exact ⟨hObstruction.1, hObstruction.2.2⟩

/-- Dual exact reduction using global right source complements. -/
theorem freshBoundaryLeadingObstruction_iff_inversePair_of_unitors_of_rightSourceComplements
    (Q : GeneratedQuotientGaugeParameters W R D)
    (hUnit : ∀ X (s : UnitorRouteAt W X),
      Q ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s))
    (hRight : HasRightWCompositeComplements W)
    (a : AssociatorTask W) :
    FreshBoundaryLeadingObstruction W R D Q a ↔
      InversePairFreshBoundaryLeadingObstruction W R D Q a := by
  constructor
  · intro hObstruction
    refine ⟨hObstruction.1, ?_, hObstruction.2⟩
    exact
      freshBoundaryLeadingObstruction_isCompositeInversePair_of_rightSourceComplements
        W R D Q hUnit hRight a hObstruction
  · intro hObstruction
    exact ⟨hObstruction.1, hObstruction.2.2⟩

/-- Under v3.52 global source geometry, compatibility is needed only on the
actual inverse-pair slice of the fresh boundary.  Right-identity boundary
tasks are already recovered by v3.53 and collision residuals by v3.52. -/
theorem corrects_all_associators_of_inversePairBoundaryCompatible_of_sourceComplements
    (Q : GeneratedQuotientGaugeParameters W R D)
    (hUnit : ∀ X (s : UnitorRouteAt W X),
      Q ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s))
    (hNonresidual :
      ∀ a : AssociatorTask W,
        ¬ ResidualAssociatorIncidence W a →
          Q ∈ quotientRouteCorrectionLocus W R D
            (associatorTaskRoute W a))
    (hInverseBoundaryCompatible :
      ∀ a : AssociatorTask W,
        FreshBoundaryAssociatorTask W a →
          IsCompositeInversePairAssociatorTask W a →
            AssociatorLeadingCompatible W R D Q a.f a.g a.h)
    (hLeft : HasLeftWCompositeComplements W)
    (hRight : HasRightWCompositeComplements W) :
    ∀ a : AssociatorTask W,
      Q ∈ quotientRouteCorrectionLocus W R D
        (associatorTaskRoute W a) := by
  apply
    corrects_all_associators_of_compositeBoundaryCompatible_of_sourceComplements
      W R D Q hUnit hNonresidual
  · intro a hBoundary hComposite
    exact
      hInverseBoundaryCompatible a hBoundary
        (compositeIdentityTask_isInversePair_of_leftSourceComplements
          W hLeft a hComposite)
  · exact hLeft
  · exact hRight

/-!
## Boundary after v3.55

The v3.54 inverse-pair reduction also removes the representative-level
separation concern: both inverse arrows evaluate to essentially-surjective and
faithful quotient representative functors, and both middle-identity
whiskering directions satisfy the existing semantic separation criterion.

Nevertheless, the actual fresh-boundary correction criterion remains the
v3.47 solved-leading equation.  Under global source complements, any surviving
obstruction is therefore exactly

```text
fresh boundary
+ two-sided inverse pair
+ leading gauge value ≠ solved associator leading value.
```

The next truth test should target that equation itself.  A legitimate route
would be an exact pentagon/defect propagation theorem for the adjusted
quotient choice, if such a theorem can be proved from the existing generated
transport algebra.  It must not be assumed merely because the source arrows
are invertible or because their representative functors are
EssSurj/Faithful.

No schedule/seed/W/R/D independence, comparison-gauge equations, general
Stage I, Stage II, or final DO universality is asserted.  Protected
validation-only PR #1558 remains untouched.
-/

end

end KUOS.DependentOriginationInversePairBoundaryObstructionV3_55
