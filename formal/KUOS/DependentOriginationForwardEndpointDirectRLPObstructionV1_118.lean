import KUOS.DependentOriginationDoubleDeloopingThinComparisonZeroV1_96
import KUOS.DependentOriginationStandardTypeATwoSimplexThinReplacementV1_93
import Mathlib.AlgebraicTopology.SimplicialSet.Monoidal

namespace KUOS.DependentOriginationForwardEndpointDirectRLPObstructionV1_118

open CategoryTheory
open CategoryTheory.Category
open MonoidalCategory
open CartesianMonoidalCategory
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationScaledHornAttachmentLiftingV1_40
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationCanonicalFibrancyAtomicTwoSimplexAuditV1_91
open KUOS.DependentOriginationStandardTypeATwoSimplexThinReplacementV1_93
open KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95
open KUOS.DependentOriginationDoubleDeloopingThinComparisonZeroV1_96

universe u

noncomputable section

/-!
# Forward endpoint RLP: an actual nonlifting square in the Duskin nerve of B²ℕ

The old v1.41 endpoint cylinder inclusion equips its SOURCE with the
minimal scaling while the full cylinder has the simplex-projected scaling.
Thus arbitrary endpoint simplices, including non-thin ones, give source maps.
An actual scaled cylinder lift would force the original endpoint simplex to
respect the full cylinder's thin triangles.

We construct the source map by first projection, prove directly from the
endpoint section and the extension equation that any cylinder lift forces
scaledness, and instantiate the resulting nonlifting square at the concrete
normal-lax triangle with comparison 1 in B²ℕ (v1.95/v1.96).

No ForwardEndpointScaledHornRLP, attachment-fibrancy, model structure,
choice of horn fillers, or external generated class is assumed.  This is a
counterexample to the *minimal-source* endpoint RLP, not to the induced-scaled
standard type-(A) endpoint Leibniz statement of v1.77.
-/

/-- A genuine map from the minimally scaled forward attachment, obtained by
restricting the constant-in-time cylinder over an arbitrary simplex sigma. -/
def projectedForwardAttachmentMap
    {X : SSet.{u}}
    (sX : ScaledSimplicialSet X)
    (n : Nat) (i : Fin (n + 1))
    (sigma : (Δ[n] : SSet.{u}) ⟶ X) :
    minimallyScaledHornCylinderAttachment n i 0 ⟶ ScaledSSet.of X sX where
  map := (hornCylinderAttachment n i 0).ι ≫
    (CartesianMonoidalCategory.fst _ _ ≫ sigma)
  scaled := minimalScaling_map _ _

/-- The chosen source map restricts to sigma at endpoint zero.  This is an
equation of genuine simplicial maps, not an abstract lifting hypothesis. -/
theorem projectedForwardAttachmentMap_endpoint_zero
    {X : SSet.{u}}
    (sX : ScaledSimplicialSet X)
    (n : Nat) (i : Fin (n + 1))
    (sigma : (Δ[n] : SSet.{u}) ⟶ X) :
    endpointIntoAttachment n i 0 ≫
        (projectedForwardAttachmentMap sX n i sigma).map = sigma := by
  change
    endpointIntoAttachment n i 0 ≫
      ((hornCylinderAttachment n i 0).ι ≫
        (CartesianMonoidalCategory.fst _ _ ≫ sigma)) = sigma
  rw [← Category.assoc, endpointIntoAttachment_ι_zero]
  simp only [SSet.ι₀_fst_assoc]

/-- A genuine cylinder filling map, constructed without any RLP hypothesis,
whenever the selected endpoint simplex is already scaled. The interval
coordinate is forgotten: this is the constant-in-time cylinder. -/
def projectedCylinderExtension
    {X : SSet.{u}}
    (sX : ScaledSimplicialSet X)
    (n : Nat)
    (sDelta : ScaledSimplicialSet (Δ[n] : SSet.{u}))
    (sigma : (Δ[n] : SSet.{u}) ⟶ X)
    (hsigma : IsScaledMap sDelta sX sigma) :
    scaledSimplexCylinder sDelta ⟶ ScaledSSet.of X sX where
  map := CartesianMonoidalCategory.fst _ _ ≫ sigma
  scaled := by
    intro t ht
    exact hsigma t.1 ht

/-- The explicit constant cylinder really extends the attachment map,
as an equality of morphisms in ScaledSSet. -/
theorem projectedCylinderExtension_restrict
    {X : SSet.{u}}
    (sX : ScaledSimplicialSet X)
    (n : Nat) (i : Fin (n + 1))
    (sDelta : ScaledSimplicialSet (Δ[n] : SSet.{u}))
    (sigma : (Δ[n] : SSet.{u}) ⟶ X)
    (hsigma : IsScaledMap sDelta sX sigma) :
    scaledHornCylinderAttachmentInclusion i 0 sDelta ≫
      projectedCylinderExtension sX n sDelta sigma hsigma =
        projectedForwardAttachmentMap sX n i sigma := by
  apply ScaledSSet.ScaledMap.ext
  rfl

/-- Any actual scaled extension of the displayed forward attachment forces
the entire endpoint simplex to preserve the target scaling. -/
theorem projectedForwardAttachment_extension_forces_scaled
    {X : SSet.{u}}
    (sX : ScaledSimplicialSet X)
    (n : Nat) (i : Fin (n + 1))
    (sDelta : ScaledSimplicialSet (Δ[n] : SSet.{u}))
    (sigma : (Δ[n] : SSet.{u}) ⟶ X)
    (l : scaledSimplexCylinder sDelta ⟶ ScaledSSet.of X sX)
    (hl : scaledHornCylinderAttachmentInclusion i 0 sDelta ≫ l =
      projectedForwardAttachmentMap sX n i sigma) :
    IsScaledMap sDelta sX sigma := by
  have hm := congrArg ScaledSSet.ScaledMap.map hl
  change
    (scaledHornCylinderAttachmentInclusion i 0 sDelta).map ≫ l.map =
      (projectedForwardAttachmentMap sX n i sigma).map at hm
  have hendpoint :
      endpointIntoAttachment n i 0 ≫
          (scaledHornCylinderAttachmentInclusion i 0 sDelta).map =
        (SSet.ι₀ : (Δ[n] : SSet.{u}) ⟶
          (Δ[n] : SSet.{u}) ⊗ Δ[1]) :=
    endpointIntoAttachment_ι_zero n i
  have hzero :
      (SSet.ι₀ : (Δ[n] : SSet.{u}) ⟶
          (Δ[n] : SSet.{u}) ⊗ Δ[1]) ≫ l.map = sigma := by
    calc
      _ = (endpointIntoAttachment n i 0 ≫
            (scaledHornCylinderAttachmentInclusion i 0 sDelta).map) ≫
              l.map := by rw [hendpoint]
      _ = endpointIntoAttachment n i 0 ≫
            (projectedForwardAttachmentMap sX n i sigma).map := by
              rw [Category.assoc, hm]
      _ = sigma :=
          projectedForwardAttachmentMap_endpoint_zero sX n i sigma
  have hscaled :
      IsScaledMap sDelta sX
        ((SSet.ι₀ : (Δ[n] : SSet.{u}) ⟶
           (Δ[n] : SSet.{u}) ⊗ Δ[1]) ≫ l.map) :=
    (endpointZero_scaled sDelta).comp l.scaled
  rw [hzero] at hscaled
  exact hscaled

/-- Sharp geometry of the explicitly projected family: a scaled endpoint
simplex has the constructed constant cylinder as a witness; conversely an
arbitrary scaled lift would force that endpoint simplex to be scaled. This
iff does not claim terminal RLP for *all* attachment maps. -/
theorem projectedForwardAttachment_extendable_iff_scaled
    {X : SSet.{u}}
    (sX : ScaledSimplicialSet X)
    (n : Nat) (i : Fin (n + 1))
    (sDelta : ScaledSimplicialSet (Δ[n] : SSet.{u}))
    (sigma : (Δ[n] : SSet.{u}) ⟶ X) :
    (∃ l : scaledSimplexCylinder sDelta ⟶ ScaledSSet.of X sX,
      scaledHornCylinderAttachmentInclusion i 0 sDelta ≫ l =
        projectedForwardAttachmentMap sX n i sigma) ↔
        IsScaledMap sDelta sX sigma := by
  constructor
  · rintro ⟨l, hl⟩
    exact projectedForwardAttachment_extension_forces_scaled
      sX n i sDelta sigma l hl
  · intro hsigma
    exact ⟨projectedCylinderExtension sX n sDelta sigma hsigma,
      projectedCylinderExtension_restrict sX n i sDelta sigma hsigma⟩

/-- Direct nonexistence of a cylinder extension if the chosen endpoint
simplex fails to be scaled.  The obstruction is already on the given face. -/
theorem projectedForwardAttachment_not_extendable
    {X : SSet.{u}}
    (sX : ScaledSimplicialSet X)
    (n : Nat) (i : Fin (n + 1))
    (sDelta : ScaledSimplicialSet (Δ[n] : SSet.{u}))
    (sigma : (Δ[n] : SSet.{u}) ⟶ X)
    (hnot : ¬ IsScaledMap sDelta sX sigma) :
    ¬ ∃ l : scaledSimplexCylinder sDelta ⟶ ScaledSSet.of X sX,
      scaledHornCylinderAttachmentInclusion i 0 sDelta ≫ l =
        projectedForwardAttachmentMap sX n i sigma := by
  rintro ⟨l, hl⟩
  exact hnot
    (projectedForwardAttachment_extension_forces_scaled
      sX n i sDelta sigma l hl)

/-- Therefore the v1.41 minimal-source forward inclusion cannot have
terminal RLP if even one endpoint simplex violates the intended scaling. -/
theorem not_forwardEndpointRLP_of_unscaled_endpoint
    {X : SSet.{u}}
    (sX : ScaledSimplicialSet X)
    (n : Nat) (i : Fin (n + 1))
    (sDelta : ScaledSimplicialSet (Δ[n] : SSet.{u}))
    (sigma : (Δ[n] : SSet.{u}) ⟶ X)
    (hnot : ¬ IsScaledMap sDelta sX sigma) :
    ¬ HasLiftingProperty
      (scaledHornCylinderAttachmentInclusion i 0 sDelta)
      (ScaledSSet.toPoint (ScaledSSet.of X sX)) := by
  intro hRLP
  obtain ⟨l, hl⟩ :=
    (ScaledSSet.hasLiftingProperty_toPoint_iff
      (scaledHornCylinderAttachmentInclusion i 0 sDelta)).1
      hRLP (projectedForwardAttachmentMap sX n i sigma)
  exact projectedForwardAttachment_not_extendable
    sX n i sDelta sigma hnot ⟨l, hl⟩

/-- The actual comparison-1 Duskin triangle is *not* scaled from the
standard degree-two type-(A) simplex. -/
theorem natNoninvertibleTriangle_not_standardTypeAScaled :
    ¬ IsScaledMap
      (standardTypeASimplexScaling (1 : Fin 3))
      (duskinScaling NatDoubleDelooping)
      (SSet.yonedaEquiv.symm natNoninvertibleTriangle) := by
  intro hscaled
  have hthin := hscaled
    (identityTwoSimplex : (Δ[2] : SSet).obj (op ⦋2⦌))
    (identityTwoSimplex_standardTypeA_thin)
  have htarget :
      (duskinScaling NatDoubleDelooping).thin
        natNoninvertibleTriangle := by
    simpa [identityTwoSimplex] using hthin
  exact natNoninvertibleTriangle_not_thin htarget

/-- The explicit incompatible square: its top map is the projection of
the comparison-1 normal-lax triangle onto the minimal-source attachment. -/
def natNoninvertibleTriangleForwardAttachment :
    minimallyScaledHornCylinderAttachment 2 (1 : Fin 3) 0 ⟶
      natDoubleDeloopingScaledDuskin :=
  projectedForwardAttachmentMap (duskinScaling NatDoubleDelooping)
    2 (1 : Fin 3)
    (SSet.yonedaEquiv.symm natNoninvertibleTriangle)

/-- No scaled cylinder extension exists for this concrete, fully specified
Duskin attachment map.  In particular this is not merely an opaque NOT_RLP
assertion: the top arrow and offending endpoint are both constructed. -/
theorem natDoubleDelooping_no_forward_endpoint_cylinder_extension :
    ¬ ∃ l :
      scaledSimplexCylinder
        (standardTypeASimplexScaling (1 : Fin 3)) ⟶
          natDoubleDeloopingScaledDuskin,
      scaledHornCylinderAttachmentInclusion (1 : Fin 3) 0
        (standardTypeASimplexScaling (1 : Fin 3)) ≫ l =
          natNoninvertibleTriangleForwardAttachment := by
  exact projectedForwardAttachment_not_extendable
    (duskinScaling NatDoubleDelooping)
    2 (1 : Fin 3)
    (standardTypeASimplexScaling (1 : Fin 3))
    (SSet.yonedaEquiv.symm natNoninvertibleTriangle)
    natNoninvertibleTriangle_not_standardTypeAScaled

/-- Failure of the literal, minimally-scaled forward endpoint terminal RLP
already for the standard type-(A) inner horn n=2, i=1 in B²ℕ. -/
theorem natDoubleDelooping_not_forward_endpoint_terminalRLP :
    ¬ HasLiftingProperty
      (scaledHornCylinderAttachmentInclusion (1 : Fin 3) 0
        (standardTypeASimplexScaling (1 : Fin 3)))
      (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin) := by
  exact not_forwardEndpointRLP_of_unscaled_endpoint
    (duskinScaling NatDoubleDelooping)
    2 (1 : Fin 3)
    (standardTypeASimplexScaling (1 : Fin 3))
    (SSet.yonedaEquiv.symm natNoninvertibleTriangle)
    natNoninvertibleTriangle_not_standardTypeAScaled

#print axioms projectedCylinderExtension
#print axioms projectedForwardAttachment_extendable_iff_scaled
#print axioms projectedForwardAttachment_extension_forces_scaled
#print axioms natDoubleDelooping_no_forward_endpoint_cylinder_extension
#print axioms natDoubleDelooping_not_forward_endpoint_terminalRLP

end

end KUOS.DependentOriginationForwardEndpointDirectRLPObstructionV1_118
