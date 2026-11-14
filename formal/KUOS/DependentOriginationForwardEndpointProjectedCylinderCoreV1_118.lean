import KUOS.DependentOriginationScaledTerminalRLPV1_41
import Mathlib.AlgebraicTopology.SimplicialSet.Monoidal

namespace KUOS.DependentOriginationForwardEndpointDirectRLPObstructionV1_118

open CategoryTheory
open CategoryTheory.Category
open MonoidalCategory
open CartesianMonoidalCategory
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledHornAttachmentLiftingV1_40
open KUOS.DependentOriginationScaledTerminalRLPV1_41

universe u

noncomputable section

/-!
# Concrete projected-cylinder constructions, independent of B²ℕ

Prove the extension criterion directly in the v1.41 scaled-simplicial category:
the constant-in-time projection gives an actual extension exactly when
the chosen endpoint simplex is scaled. An arbitrary extension forces its
endpoint to be scaled. No fibrancy, lifting property, or B²ℕ fact is assumed.
This deliberately isolates the geometric mechanism from the B²ℕ witness.
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

#print axioms projectedCylinderExtension
#print axioms projectedForwardAttachment_extendable_iff_scaled
#print axioms not_forwardEndpointRLP_of_unscaled_endpoint

end

end KUOS.DependentOriginationForwardEndpointDirectRLPObstructionV1_118
