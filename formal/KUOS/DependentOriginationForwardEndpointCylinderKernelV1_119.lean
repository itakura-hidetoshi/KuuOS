import KUOS.DependentOriginationScaledTerminalRLPV1_41
import Mathlib.AlgebraicTopology.SimplicialSet.Monoidal

namespace KUOS.DependentOriginationForwardEndpointCylinderKernelV1_119

open CategoryTheory
open CategoryTheory.Category
open MonoidalCategory
open CartesianMonoidalCategory
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledHornAttachmentLiftingV1_40
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22

universe u

noncomputable section

/-!
# Forward-endpoint cylinder: actual extension and exact scaling obstruction v1.119

Independent strict-import verification kernel against parent PR #3522,
without any type-(A) or B²ℕ specialization that currently reaches the pinned
UnionProd import blocker in v1.61. No existing theorem is edited.

The source A is MINIMALLY scaled (v1.41). For the explicit attachment maps
built by projection along a given endpoint sigma, we construct a genuine
constant-in-time scaled cylinder when sigma is scaled, prove its restriction
equation, and prove the converse by endpoint-zero restriction.

The literal RLP against *all* such top arrows forces every endpoint simplex
sigma to preserve the chosen sDelta scaling. This exposes the exact obstruction
before any Duskin specialization.  In particular, this does not assert
forward endpoint RLP under arbitrary target scaling.
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
            (scaledHornCylinderAttachmentInclusion i 0 sDelta).map) ≫ l.map :=
              (congrArg (fun f => f ≫ l.map) hendpoint).symm
      _ = endpointIntoAttachment n i 0 ≫
            ((scaledHornCylinderAttachmentInclusion i 0 sDelta).map ≫ l.map) :=
              Category.assoc _ _ _
      _ = endpointIntoAttachment n i 0 ≫
            (projectedForwardAttachmentMap sX n i sigma).map :=
              congrArg (fun f => endpointIntoAttachment n i 0 ≫ f) hm
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


/-- A direct consequence of an actual terminal RLP: every freely chosen
projected endpoint simplex must already preserve the cylinder scaling. -/
theorem endpoint_simplex_scaled_of_forward_terminalRLP
    {X : SSet.{u}}
    (sX : ScaledSimplicialSet X)
    (n : Nat) (i : Fin (n + 1))
    (sDelta : ScaledSimplicialSet (Δ[n] : SSet.{u}))
    (hRLP : HasLiftingProperty
      (scaledHornCylinderAttachmentInclusion i 0 sDelta)
      (ScaledSSet.toPoint (ScaledSSet.of X sX)))
    (sigma : (Δ[n] : SSet.{u}) ⟶ X) :
    IsScaledMap sDelta sX sigma := by
  rcases
    (ScaledSSet.hasLiftingProperty_toPoint_iff
      (scaledHornCylinderAttachmentInclusion i 0 sDelta)).1
      hRLP (projectedForwardAttachmentMap sX n i sigma) with
      ⟨l, hl⟩
  exact projectedForwardAttachment_extension_forces_scaled
    sX n i sDelta sigma l hl

#print axioms projectedCylinderExtension
#print axioms projectedCylinderExtension_restrict
#print axioms projectedForwardAttachment_extendable_iff_scaled
#print axioms not_forwardEndpointRLP_of_unscaled_endpoint
#print axioms endpoint_simplex_scaled_of_forward_terminalRLP

end
end KUOS.DependentOriginationForwardEndpointCylinderKernelV1_119
