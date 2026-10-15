import KUOS.DependentOriginationLocallyFiniteRankedEnumerationV3_46

namespace KUOS.DependentOriginationFreshBoundaryCompatibilityV3_47

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationQuotientGaugeIntersectionObstructionV3_11
open KUOS.DependentOriginationQuotientGaugeCoordinateFootprintV3_12
open KUOS.DependentOriginationQuotientGaugeCoordinateKeyV3_14
open KUOS.DependentOriginationAssociatorThreeOfFourRigidityV3_23
open KUOS.DependentOriginationAssociatorUnitorBoundaryReductionV3_36
open KUOS.DependentOriginationFreshAssociatorCompletionV3_37
open KUOS.DependentOriginationFiniteAssociatorScheduleV3_38
open KUOS.DependentOriginationCountableAssociatorStabilizationV3_39
open KUOS.DependentOriginationCollisionSectorPreservationV3_40
open KUOS.DependentOriginationAssociatorIncidenceDecompositionV3_41
open KUOS.DependentOriginationFreshInteriorGlobalCoverageV3_42
open KUOS.DependentOriginationFiniteRankedScheduleV3_43
open KUOS.DependentOriginationCountableRankedEnumerationV3_44
open KUOS.DependentOriginationLowerRankFinitenessV3_45
open KUOS.DependentOriginationLocallyFiniteRankedEnumerationV3_46

universe u v uH vH

set_option autoImplicit false

/-!
# Fresh boundary compatibility obstruction v3.47

v3.41 leaves two kinds of local residual incidence away from the
middle-identity sector:

* a genuine collision of the associator leading key with one of its suffix
  keys;
* a fresh leading key which lies on the unitor-visible boundary.

v3.43-v3.46 construct schedules for the fresh/interior sector. This layer
returns to the second residual kind and makes its obstruction exact.

For every fresh associator, v3.37 already constructs the unique value which
the leading gauge coordinate must take if the other three footprint
coordinates stay fixed. We prove the converse as well:

  Q corrects the associator
    iff
  Q's current leading value is already the v3.37 solved value.

Thus a fresh-but-unitor-visible task does not require a new kind of local
completion. Its only obstruction at a fixed common gauge is a one-coordinate
compatibility equation between the value already fixed on the unitor boundary
and the unique solved associator leading value.

We also show that an actual composition coordinate can be unitor-visible only
through equality with a composition coordinate having an identity factor; the
identity-coordinate alternative is impossible by constructor disjointness.

After this reduction, if all such boundary equations hold, the only remaining
local residual sector is the non-middle leading-collision sector.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- The fresh slice of the v3.41 residual boundary sector. -/
def FreshBoundaryAssociatorTask (a : AssociatorTask W) : Prop :=
  FreshAssociatorLeadingCoordinate W a.f a.g a.h ∧
    UnitorVisibleCoordinate W (associatorTaskLeadingCoordinate W a)

/-- Actual composition coordinates cannot be visible through an identity-key
branch; visibility is exactly equality with a left- or right-unit composition
coordinate. -/
theorem composition_unitorVisible_iff_unitComposition
    {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z) :
    UnitorVisibleCoordinate W (.composition f g) ↔
      (∃ (A B : W.Localization) (k : A ⟶ B),
        (.composition f g : QuotientGaugeCoordinate W) =
          .composition (𝟙 A) k) ∨
      (∃ (A B : W.Localization) (k : A ⟶ B),
        (.composition f g : QuotientGaugeCoordinate W) =
          .composition k (𝟙 B)) := by
  constructor
  · intro hVisible
    rcases
        (unitorVisibleCoordinate_iff_identity_or_unitComposition
          W (.composition f g)).1 hVisible with
      hIdentity | hLeft | hRight
    · rcases hIdentity with ⟨A, hEq⟩
      cases hEq
    · exact Or.inl hLeft
    · exact Or.inr hRight
  · rintro (hLeft | hRight)
    · exact
        (unitorVisibleCoordinate_iff_identity_or_unitComposition
          W (.composition f g)).2 (Or.inr (Or.inl hLeft))
    · exact
        (unitorVisibleCoordinate_iff_identity_or_unitComposition
          W (.composition f g)).2 (Or.inr (Or.inr hRight))

/-- Therefore every fresh boundary task has a leading key equal to an actual
unit-composition key. This is a coordinate equality; it does not silently
identify the underlying dependent morphisms. -/
theorem freshBoundary_leading_is_unitComposition
    (a : AssociatorTask W) (hBoundary : FreshBoundaryAssociatorTask W a) :
    (∃ (A B : W.Localization) (k : A ⟶ B),
      associatorTaskLeadingCoordinate W a =
        .composition (𝟙 A) k) ∨
    (∃ (A B : W.Localization) (k : A ⟶ B),
      associatorTaskLeadingCoordinate W a =
        .composition k (𝟙 B)) := by
  exact
    (composition_unitorVisible_iff_unitComposition
      W (a.f ≫ a.g) a.h).1 hBoundary.2

/-- Middle identity cannot lie in the fresh boundary sector because it already
fails freshness. -/
theorem freshBoundary_not_middleIdentity
    (a : AssociatorTask W) (hBoundary : FreshBoundaryAssociatorTask W a) :
    ¬ IsMiddleIdentityAssociatorTask W a := by
  intro hMiddle
  exact middleIdentityAssociatorTask_not_fresh W a hMiddle hBoundary.1

/-- The fresh part of v3.41 residual incidence is exactly the visible-boundary
sector defined above. -/
theorem residual_and_fresh_iff_freshBoundary
    (a : AssociatorTask W) :
    (ResidualAssociatorIncidence W a ∧
        FreshAssociatorLeadingCoordinate W a.f a.g a.h) ↔
      FreshBoundaryAssociatorTask W a := by
  constructor
  · rintro ⟨hResidual, hFresh⟩
    refine ⟨hFresh, ?_⟩
    by_contra hNotVisible
    exact hResidual.2 ⟨hFresh, hNotVisible⟩
  · intro hBoundary
    refine ⟨?_, hBoundary.1⟩
    refine ⟨freshBoundary_not_middleIdentity W a hBoundary, ?_⟩
    intro hInterior
    exact hInterior.2 hBoundary.2

variable (R : RawHigherContextualSystem.{u, v, uH, vH}
  (Context := Context))
variable (D : PointwiseWAdjointEquivalenceData (W := W) R)

/-- At one fresh associator, the current leading gauge already has the unique
value solved by v3.37 from the unchanged suffix. -/
noncomputable def AssociatorLeadingCompatible
    (Q : GeneratedQuotientGaugeParameters W R D)
    {X Y Z T : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T) : Prop :=
  Q.mapCompGauge (f ≫ g) h =
    associatorLeadingGaugeValue W R D Q f g h

/-- Fresh associator correction is equivalent to the single solved-leading
compatibility equation. The forward direction is v3.23 three-of-four
rigidity; the reverse direction transfers v3.37's completed correction back
to Q using equality on all four route coordinates. -/
theorem associator_corrected_iff_leadingCompatible_of_fresh
    (Q : GeneratedQuotientGaugeParameters W R D)
    {X Y Z T : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T)
    (hFresh : FreshAssociatorLeadingCoordinate W f g h) :
    Q ∈ quotientRouteCorrectionLocus W R D (.associator f g h) ↔
      AssociatorLeadingCompatible W R D Q f g h := by
  let Q' := completeAssociatorLeading W R D Q f g h
  have hDone :
      Q' ∈ quotientRouteCorrectionLocus W R D (.associator f g h) := by
    dsimp [Q']
    exact completeAssociatorLeading_corrected W R D Q f g h hFresh
  have hfg :
      Q'.mapCompGauge f g = Q.mapCompGauge f g := by
    dsimp [Q']
    exact quotientGaugeUpdate_value_of_ne W R D Q
      (.composition (f ≫ g) h)
      (associatorLeadingGaugeValue W R D Q f g h)
      (.composition f g) hFresh.1
  have hgh :
      Q'.mapCompGauge g h = Q.mapCompGauge g h := by
    dsimp [Q']
    exact quotientGaugeUpdate_value_of_ne W R D Q
      (.composition (f ≫ g) h)
      (associatorLeadingGaugeValue W R D Q f g h)
      (.composition g h) hFresh.2.1
  have hfgh :
      Q'.mapCompGauge f (g ≫ h) = Q.mapCompGauge f (g ≫ h) := by
    dsimp [Q']
    exact quotientGaugeUpdate_value_of_ne W R D Q
      (.composition (f ≫ g) h)
      (associatorLeadingGaugeValue W R D Q f g h)
      (.composition f (g ≫ h)) hFresh.2.2
  have hAt :
      Q'.mapCompGauge (f ≫ g) h =
        associatorLeadingGaugeValue W R D Q f g h := by
    dsimp [Q']
    exact quotientGaugeUpdate_value_self W R D Q
      (.composition (f ≫ g) h)
      (associatorLeadingGaugeValue W R D Q f g h)
  constructor
  · intro hQ
    have hLead :
        Q.mapCompGauge (f ≫ g) h = Q'.mapCompGauge (f ≫ g) h :=
      associator_mapComp_fgg_h_eq_of_corrected_of_other_three_eq
        W R D f g h Q Q' hQ hDone hfg.symm hgh.symm hfgh.symm
    exact hLead.trans hAt
  · intro hCompatible
    have hLead :
        Q'.mapCompGauge (f ≫ g) h = Q.mapCompGauge (f ≫ g) h :=
      hAt.trans hCompatible.symm
    have hAgree :
        QuotientGaugesAgreeOnRouteState W R D Q' Q
          (.associator f g h) :=
      ⟨hLead, hfg, hgh, hfgh⟩
    exact
      (mem_quotientRouteCorrectionLocus_congr_of_agreesOnRouteState
        W R D Q' Q (.associator f g h) hAgree).1 hDone

/-- Task-packaged form of the preceding exact criterion. -/
theorem freshAssociatorTask_corrected_iff_leadingCompatible
    (Q : GeneratedQuotientGaugeParameters W R D)
    (a : AssociatorTask W)
    (hFresh : FreshAssociatorLeadingCoordinate W a.f a.g a.h) :
    Q ∈ quotientRouteCorrectionLocus W R D (associatorTaskRoute W a) ↔
      AssociatorLeadingCompatible W R D Q a.f a.g a.h := by
  simpa [associatorTaskRoute] using
    associator_corrected_iff_leadingCompatible_of_fresh
      W R D Q a.f a.g a.h hFresh

/-- On the fresh boundary residual sector, the same one-coordinate equality is
the complete local obstruction at a fixed gauge. -/
theorem freshBoundaryTask_corrected_iff_leadingCompatible
    (Q : GeneratedQuotientGaugeParameters W R D)
    (a : AssociatorTask W)
    (hBoundary : FreshBoundaryAssociatorTask W a) :
    Q ∈ quotientRouteCorrectionLocus W R D (associatorTaskRoute W a) ↔
      AssociatorLeadingCompatible W R D Q a.f a.g a.h :=
  freshAssociatorTask_corrected_iff_leadingCompatible
    W R D Q a hBoundary.1

/-- Explicit obstruction predicate for the fresh boundary sector. -/
noncomputable def FreshBoundaryLeadingObstruction
    (Q : GeneratedQuotientGaugeParameters W R D)
    (a : AssociatorTask W) : Prop :=
  FreshBoundaryAssociatorTask W a ∧
    ¬ AssociatorLeadingCompatible W R D Q a.f a.g a.h

/-- For a task known to be fresh-boundary, obstruction is equivalent to
failure of correction. -/
theorem freshBoundaryLeadingObstruction_iff_not_corrected
    (Q : GeneratedQuotientGaugeParameters W R D)
    (a : AssociatorTask W)
    (hBoundary : FreshBoundaryAssociatorTask W a) :
    FreshBoundaryLeadingObstruction W R D Q a ↔
      Q ∉ quotientRouteCorrectionLocus W R D (associatorTaskRoute W a) := by
  rw [FreshBoundaryLeadingObstruction]
  simp only [hBoundary, true_and]
  exact not_congr
    (freshBoundaryTask_corrected_iff_leadingCompatible
      W R D Q a hBoundary).symm

/-- After the fresh boundary compatibility equations are satisfied, the only
remaining local residual shape is the non-middle leading-collision sector. -/
def CollisionResidualAssociatorTask (a : AssociatorTask W) : Prop :=
  ¬ IsMiddleIdentityAssociatorTask W a ∧
    HasAssociatorLeadingCoordinateCollision W a

/-- Any task outside the collision residual is either already nonresidual or
belongs to the fresh boundary sector. -/
theorem not_collisionResidual_implies_nonresidual_or_freshBoundary
    (a : AssociatorTask W)
    (hNotCollision : ¬ CollisionResidualAssociatorTask W a) :
    ¬ ResidualAssociatorIncidence W a ∨
      FreshBoundaryAssociatorTask W a := by
  by_cases hResidual : ResidualAssociatorIncidence W a
  · right
    rcases
        (residualAssociatorIncidence_iff_collision_or_boundary W a).1 hResidual with
      ⟨hNotMiddle, hCollision | ⟨hFresh, hVisible⟩⟩
    · exact False.elim (hNotCollision ⟨hNotMiddle, hCollision⟩)
    · exact ⟨hFresh, hVisible⟩
  · exact Or.inl hResidual

/-- If one gauge already corrects every nonresidual task and satisfies all
fresh-boundary leading compatibility equations, then it corrects every task
outside the collision residual sector. -/
theorem corrects_all_except_collisionResidual_of_boundaryCompatible
    (Q : GeneratedQuotientGaugeParameters W R D)
    (hNonresidual :
      ∀ a : AssociatorTask W,
        ¬ ResidualAssociatorIncidence W a →
          Q ∈ quotientRouteCorrectionLocus W R D (associatorTaskRoute W a))
    (hBoundaryCompatible :
      ∀ a : AssociatorTask W,
        FreshBoundaryAssociatorTask W a →
          AssociatorLeadingCompatible W R D Q a.f a.g a.h) :
    ∀ a : AssociatorTask W,
      ¬ CollisionResidualAssociatorTask W a →
        Q ∈ quotientRouteCorrectionLocus W R D (associatorTaskRoute W a) := by
  intro a hNotCollision
  rcases
      not_collisionResidual_implies_nonresidual_or_freshBoundary
        W a hNotCollision with
    hNonres | hBoundary
  · exact hNonresidual a hNonres
  · exact
      (freshBoundaryTask_corrected_iff_leadingCompatible
        W R D Q a hBoundary).2
        (hBoundaryCompatible a hBoundary)

/-!
## Boundary after v3.47

The fresh/unitor-visible residual is no longer opaque. At any fixed quotient
gauge, a fresh associator is corrected exactly when its current leading value
equals the unique value solved from the other three coordinates. For a visible
leading key this is precisely a compatibility equation with a coordinate
already lying on the unitor boundary.

This does not prove that every common unitor gauge automatically satisfies
those equations. It identifies the exact obstruction that must be checked or
derived from stronger coherence.

If all fresh-boundary compatibility equations hold for a gauge which already
corrects the nonresidual sector, then the only remaining local incidence is
the non-middle leading-collision sector.

No collision-sector elimination beyond middle identity, no schedule
independence, no comparison-gauge equations, no general Stage I, Stage II, or
final DO universality is asserted. Protected validation-only #1558 is
untouched.
-/

end KUOS.DependentOriginationFreshBoundaryCompatibilityV3_47
