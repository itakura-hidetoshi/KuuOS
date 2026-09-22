import KUOS.DependentOriginationWCompositeCollisionClosureV3_51
import Mathlib.CategoryTheory.MorphismProperty.Composition

namespace KUOS.DependentOriginationGlobalCancellationFromSourceComplementsV3_52

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationQuotientGaugeIntersectionObstructionV3_11
open KUOS.DependentOriginationUnitorWitnessCorrelationV3_35
open KUOS.DependentOriginationFiniteAssociatorScheduleV3_38
open KUOS.DependentOriginationAssociatorIncidenceDecompositionV3_41
open KUOS.DependentOriginationFreshBoundaryCompatibilityV3_47
open KUOS.DependentOriginationCollisionAbsorptionReductionV3_49
open KUOS.DependentOriginationLeftIdentitySemanticRecoveryV3_50
open KUOS.DependentOriginationWCompositeSplitSeparationV3_34
open KUOS.DependentOriginationWCompositeCollisionClosureV3_51

universe u v uH vH

set_option autoImplicit false

noncomputable section

/-!
# Global localization cancellation from source complements v3.52

v3.51 closes collision residuals carrying a literal source-W-composite
presentation.  The remaining representation issue is that a general
localization arrow is a quotient of a path in Mathlib's `LocQuiver W`, not
necessarily one literal `W.Q.map f`.

Mathlib already provides the exact induction principle needed here:

`Localization.Construction.morphismProperty_eq_top`.

A morphism property on `W.Localization` which

* is stable under composition;
* contains every source image `W.Q.map f`;
* contains every formal inverse `wInv w hw`;

holds for every localization morphism.

The epi and mono properties are composition-stable.  Formal W-inverses are
isomorphisms, hence both epi and mono.  v3.34 supplies split epi/mono structures
on source images whenever source arrows admit suitable W-composite complements.

Therefore global left/right W-composite complement hypotheses on the source
category promote to epi/mono for every localization arrow.  This directly
discharges the collision-cancellation premise of v3.50 for all residual tasks.

The hypotheses below are intentionally explicit.  No existence of source
complements is inferred from weak admissibility, localization, or collision
geometry itself.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Every source arrow can be completed on the left to one arrow in W.  The
auxiliary source object may depend on the arrow. -/
def HasLeftWCompositeComplements : Prop :=
  ∀ {X Y : Context} (f : X ⟶ Y),
    ∃ (A : Context) (s : A ⟶ X), W (s ≫ f)

/-- Every source arrow can be completed on the right to one arrow in W.  The
auxiliary target object may depend on the arrow. -/
def HasRightWCompositeComplements : Prop :=
  ∀ {X Y : Context} (f : X ⟶ Y),
    ∃ (B : Context) (r : Y ⟶ B), W (f ≫ r)

/-- One left W-composite complement makes the localization image split epi,
hence epi. -/
theorem Q_map_epi_of_leftWCompositeComplement
    {X Y : Context} (f : X ⟶ Y)
    (h : ∃ (A : Context) (s : A ⟶ X), W (s ≫ f)) :
    Epi (W.Q.map f) := by
  rcases h with ⟨A, s, hs⟩
  letI : IsSplitEpi (W.Q.map f) :=
    isSplitEpi_Q_map_of_W_comp W f s hs
  infer_instance

/-- One right W-composite complement makes the localization image split mono,
hence mono. -/
theorem Q_map_mono_of_rightWCompositeComplement
    {X Y : Context} (f : X ⟶ Y)
    (h : ∃ (B : Context) (r : Y ⟶ B), W (f ≫ r)) :
    Mono (W.Q.map f) := by
  rcases h with ⟨B, r, hr⟩
  letI : IsSplitMono (W.Q.map f) :=
    isSplitMono_Q_map_of_W_comp W f r hr
  infer_instance

/-- Under global left W-composite complements, every morphism of the
localization is epi.  Mathlib performs the induction over quotient paths; no
new representative choice is made here. -/
theorem allLocalizationArrows_epi_of_leftWCompositeComplements
    (H : HasLeftWCompositeComplements W) :
    ∀ {X Y : W.Localization} (f : X ⟶ Y), Epi f := by
  have hTop :
      MorphismProperty.epimorphisms W.Localization = ⊤ := by
    apply Localization.Construction.morphismProperty_eq_top
    · intro X Y f
      rw [MorphismProperty.epimorphisms.iff]
      exact Q_map_epi_of_leftWCompositeComplement W f (H f)
    · intro X Y w hw
      rw [MorphismProperty.epimorphisms.iff]
      infer_instance
  intro X Y f
  exact
    (MorphismProperty.epimorphisms.iff).1
      (MorphismProperty.of_eq_top hTop f)

/-- Dually, global right W-composite complements make every localization
morphism mono. -/
theorem allLocalizationArrows_mono_of_rightWCompositeComplements
    (H : HasRightWCompositeComplements W) :
    ∀ {X Y : W.Localization} (f : X ⟶ Y), Mono f := by
  have hTop :
      MorphismProperty.monomorphisms W.Localization = ⊤ := by
    apply Localization.Construction.morphismProperty_eq_top
    · intro X Y f
      rw [MorphismProperty.monomorphisms.iff]
      exact Q_map_mono_of_rightWCompositeComplement W f (H f)
    · intro X Y w hw
      rw [MorphismProperty.monomorphisms.iff]
      infer_instance
  intro X Y f
  exact
    (MorphismProperty.monomorphisms.iff).1
      (MorphismProperty.of_eq_top hTop f)

/-- The two global source-complement hypotheses supply the exact cancellation
pair required by every associator task, independently of a chosen source
presentation of that task. -/
theorem associatorTask_cancellation_of_sourceComplements
    (hLeft : HasLeftWCompositeComplements W)
    (hRight : HasRightWCompositeComplements W)
    (a : AssociatorTask W) :
    Epi a.f ∧ Mono a.g := by
  exact
    ⟨allLocalizationArrows_epi_of_leftWCompositeComplements W hLeft a.f,
      allLocalizationArrows_mono_of_rightWCompositeComplements W hRight a.g⟩

variable (R : RawHigherContextualSystem.{u, v, uH, vH}
  (Context := Context))
variable (D : PointwiseWAdjointEquivalenceData (W := W) R)

/-- Every collision residual is corrected under global source-complement
geometry and the already correlated common unitor gauge. -/
theorem collisionResidual_corrected_of_sourceComplements
    (Q : GeneratedQuotientGaugeParameters W R D)
    (hUnit : ∀ X (s : UnitorRouteAt W X),
      Q ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s))
    (hLeft : HasLeftWCompositeComplements W)
    (hRight : HasRightWCompositeComplements W)
    (a : AssociatorTask W)
    (hResidual : CollisionResidualAssociatorTask W a) :
    Q ∈ quotientRouteCorrectionLocus W R D (associatorTaskRoute W a) := by
  rcases associatorTask_cancellation_of_sourceComplements
      W hLeft hRight a with ⟨hEpi, hMono⟩
  letI : Epi a.f := hEpi
  letI : Mono a.g := hMono
  exact collisionResidual_corrected_of_epi_mono_of_unitors
    W R D Q hUnit a hResidual

/-- Global source-complement geometry removes the separate per-collision
cancellation premise from v3.50.  The only remaining hypotheses here are the
already established common-unitor/nonresidual coverage and the v3.47
fresh-boundary compatibility equations. -/
theorem corrects_all_associators_of_boundaryCompatible_of_sourceComplements
    (Q : GeneratedQuotientGaugeParameters W R D)
    (hUnit : ∀ X (s : UnitorRouteAt W X),
      Q ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s))
    (hNonresidual :
      ∀ a : AssociatorTask W,
        ¬ ResidualAssociatorIncidence W a →
          Q ∈ quotientRouteCorrectionLocus W R D (associatorTaskRoute W a))
    (hBoundaryCompatible :
      ∀ a : AssociatorTask W,
        FreshBoundaryAssociatorTask W a →
          AssociatorLeadingCompatible W R D Q a.f a.g a.h)
    (hLeft : HasLeftWCompositeComplements W)
    (hRight : HasRightWCompositeComplements W) :
    ∀ a : AssociatorTask W,
      Q ∈ quotientRouteCorrectionLocus W R D (associatorTaskRoute W a) := by
  apply
    corrects_all_associators_of_boundaryCompatible_of_collisionCancellation
      W R D Q hUnit hNonresidual hBoundaryCompatible
  intro a _hResidual
  exact associatorTask_cancellation_of_sourceComplements
    W hLeft hRight a

/-!
## Boundary after v3.52

The representation issue isolated in v3.51 is eliminated under a global source
geometry assumption: left and right W-composite complements for every source
arrow force every localization morphism to be epi and mono, respectively.

The proof is not a new localization induction.  It reuses Mathlib's canonical
`morphismProperty_eq_top` theorem for the path-quotient construction.  In
particular formal inverse letters require no complement condition because they
are already isomorphisms.

This does not prove the global source-complement hypotheses from weak
admissibility, nor does it prove that they are necessary.  A more local future
refinement may certify only the `Quot.out` words occurring in collision
residuals rather than all localization arrows.

Fresh-boundary compatibility remains independent.  No schedule/seed/W/R/D
independence, comparison-gauge equations, general Stage I, Stage II, or final
DO universality is asserted.  Protected validation-only #1558 is untouched.
-/

end

end KUOS.DependentOriginationGlobalCancellationFromSourceComplementsV3_52
