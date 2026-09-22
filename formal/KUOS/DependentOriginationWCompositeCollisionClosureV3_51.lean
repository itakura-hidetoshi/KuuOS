import KUOS.DependentOriginationLeftIdentitySemanticRecoveryV3_50
import KUOS.DependentOriginationWCompositeSplitSeparationV3_34

namespace KUOS.DependentOriginationWCompositeCollisionClosureV3_51

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

universe u v uH vH

set_option autoImplicit false

noncomputable section

/-!
# Source-W-composite closure of the collision residual v3.51

v3.50 closes every collision residual once its first arrow is epi and its
middle arrow is mono.  Those cancellation classes were deliberately left as
actual hypotheses.

v3.34 already constructs the needed cancellation geometry for source-presented
localization arrows.  If

  s : A ⟶ X,  f : X ⟶ Y,  g : Y ⟶ Z,  r : Z ⟶ B

satisfy

  W (s ≫ f),  W (g ≫ r),

then Mathlib's localization construction gives a split epi structure on
`W.Q.map f` and a split mono structure on `W.Q.map g`.  The pinned Mathlib
instances

  IsSplitEpi.epi
  IsSplitMono.mono

therefore supply exactly the `Epi` / `Mono` witnesses consumed by v3.49-v3.50.

This layer packages that bridge for actual `AssociatorTask` data.  No claim is
made that every localization arrow is literally the image of one source arrow,
nor that every collision residual admits such a source presentation.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Package an associator task whose first two arrows are literal images of
source arrows under the localization functor. -/
def sourcePresentedAssociatorTask
    {X Y Z : Context} (f : X ⟶ Y) (g : Y ⟶ Z)
    {T : W.Localization} (h : W.Q.obj Z ⟶ T) :
    AssociatorTask W where
  X := W.Q.obj X
  Y := W.Q.obj Y
  Z := W.Q.obj Z
  T := T
  f := W.Q.map f
  g := W.Q.map g
  h := h

/-- Concrete cancellation presentation for one actual task.  The source
composites, rather than the individual arrows, are required to lie in `W`.
The auxiliary source and target objects may be unrelated to the middle object. -/
def HasWCompositeCancellationPresentation (a : AssociatorTask W) : Prop :=
  ∃ (A X Y Z B : Context)
      (s : A ⟶ X) (f : X ⟶ Y) (g : Y ⟶ Z) (r : Z ⟶ B)
      (T : W.Localization) (h : W.Q.obj Z ⟶ T),
    W (s ≫ f) ∧ W (g ≫ r) ∧
      a = sourcePresentedAssociatorTask W f g h

/-- v3.34 turns one source-W-composite presentation into the exact
cancellation classes used by v3.50. -/
theorem wCompositeCancellationPresentation_epi_mono
    (a : AssociatorTask W)
    (hPresentation : HasWCompositeCancellationPresentation W a) :
    Epi a.f ∧ Mono a.g := by
  rcases hPresentation with
    ⟨A, X, Y, Z, B, s, f, g, r, T, h, hs, hr, rfl⟩
  letI : IsSplitEpi (W.Q.map f) :=
    isSplitEpi_Q_map_of_W_comp W f s hs
  letI : IsSplitMono (W.Q.map g) :=
    isSplitMono_Q_map_of_W_comp W g r hr
  exact ⟨inferInstance, inferInstance⟩

/-- The narrower source-W-edge case is included using identity complements. -/
def HasWEdgeCancellationPresentation (a : AssociatorTask W) : Prop :=
  ∃ (X Y Z : Context)
      (f : X ⟶ Y) (g : Y ⟶ Z)
      (T : W.Localization) (h : W.Q.obj Z ⟶ T),
    W f ∧ W g ∧
      a = sourcePresentedAssociatorTask W f g h

/-- Literal W-edge presentation gives the more general v3.51
source-W-composite presentation without requiring multiplicativity of W. -/
theorem wCompositeCancellationPresentation_of_wEdgePresentation
    (a : AssociatorTask W)
    (hEdge : HasWEdgeCancellationPresentation W a) :
    HasWCompositeCancellationPresentation W a := by
  rcases hEdge with ⟨X, Y, Z, f, g, T, h, hf, hg, ha⟩
  refine ⟨X, X, Y, Z, Z, 𝟙 X, f, g, 𝟙 Z, T, h, ?_, ?_, ha⟩
  · simpa only [Category.id_comp] using hf
  · simpa only [Category.comp_id] using hg

variable (R : RawHigherContextualSystem.{u, v, uH, vH}
  (Context := Context))
variable (D : PointwiseWAdjointEquivalenceData (W := W) R)

/-- A collision residual with a source-W-composite presentation is corrected
by the already common unitor gauge.  The proof introduces no new coherence
equation: v3.34 supplies splitness, Mathlib supplies epi/mono, and v3.50
supplies correction. -/
theorem collisionResidual_corrected_of_wCompositePresentation
    (Q : GeneratedQuotientGaugeParameters W R D)
    (hUnit : ∀ X (s : UnitorRouteAt W X),
      Q ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s))
    (a : AssociatorTask W)
    (hPresentation : HasWCompositeCancellationPresentation W a)
    (hResidual : CollisionResidualAssociatorTask W a) :
    Q ∈ quotientRouteCorrectionLocus W R D (associatorTaskRoute W a) := by
  rcases wCompositeCancellationPresentation_epi_mono
      W a hPresentation with ⟨hEpi, hMono⟩
  letI : Epi a.f := hEpi
  letI : Mono a.g := hMono
  exact collisionResidual_corrected_of_epi_mono_of_unitors
    W R D Q hUnit a hResidual

/-- The W-edge case is an immediate specialization of the source-composite
closure theorem. -/
theorem collisionResidual_corrected_of_wEdgePresentation
    (Q : GeneratedQuotientGaugeParameters W R D)
    (hUnit : ∀ X (s : UnitorRouteAt W X),
      Q ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s))
    (a : AssociatorTask W)
    (hEdge : HasWEdgeCancellationPresentation W a)
    (hResidual : CollisionResidualAssociatorTask W a) :
    Q ∈ quotientRouteCorrectionLocus W R D (associatorTaskRoute W a) := by
  exact collisionResidual_corrected_of_wCompositePresentation
    W R D Q hUnit a
      (wCompositeCancellationPresentation_of_wEdgePresentation W a hEdge)
      hResidual

/-- If every actual collision residual admits the concrete v3.34 source
presentation, then v3.50's nonresidual + fresh-boundary coverage extends to
all associators without separately postulating epi/mono witnesses. -/
theorem corrects_all_associators_of_boundaryCompatible_of_wCompositePresentations
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
    (hPresentation :
      ∀ a : AssociatorTask W,
        CollisionResidualAssociatorTask W a →
          HasWCompositeCancellationPresentation W a) :
    ∀ a : AssociatorTask W,
      Q ∈ quotientRouteCorrectionLocus W R D (associatorTaskRoute W a) := by
  apply
    corrects_all_associators_of_boundaryCompatible_of_collisionCancellation
      W R D Q hUnit hNonresidual hBoundaryCompatible
  intro a hResidual
  exact wCompositeCancellationPresentation_epi_mono
    W a (hPresentation a hResidual)

/-- A global W-edge presentation hypothesis is a concrete special case of
the source-composite criterion. -/
theorem corrects_all_associators_of_boundaryCompatible_of_wEdgePresentations
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
    (hEdgePresentation :
      ∀ a : AssociatorTask W,
        CollisionResidualAssociatorTask W a →
          HasWEdgeCancellationPresentation W a) :
    ∀ a : AssociatorTask W,
      Q ∈ quotientRouteCorrectionLocus W R D (associatorTaskRoute W a) := by
  exact
    corrects_all_associators_of_boundaryCompatible_of_wCompositePresentations
      W R D Q hUnit hNonresidual hBoundaryCompatible
      (fun a hResidual =>
        wCompositeCancellationPresentation_of_wEdgePresentation
          W a (hEdgePresentation a hResidual))

/-!
## Boundary after v3.51

The epi/mono premise in v3.50 is now discharged for collision tasks carrying
the concrete source-W-composite presentation already constructed in v3.34.
The W-edge case follows with identity complements.

This is not a representation theorem for arbitrary localization arrows.
A general localization morphism may be represented by a zigzag or quotient
word rather than by one literal `W.Q.map f`.  Therefore the remaining
geometric question is whether every actual collision residual can be
transported to, or certified by, a source presentation with the two required
W-composite complements.  Failure to exhibit such a presentation is not a
counterexample.

Fresh-boundary compatibility is still an independent equation.  No
schedule/seed/W/R/D independence, comparison-gauge equations, general Stage I,
Stage II, or final DO universality is asserted.  Protected validation-only
#1558 is untouched.
-/

end

end KUOS.DependentOriginationWCompositeCollisionClosureV3_51
