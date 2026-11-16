import KUOS.DependentOriginationForwardEndpointDirectRLPObstructionV1_118
import KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50

namespace KUOS.DependentOriginationForwardEndpointInducedCompatibilityV1_120

open CategoryTheory
open CategoryTheory.Category
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledHornAttachmentLiftingV1_40
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationScaledAnodyneAttachmentFactorizationV1_48
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95
open KUOS.DependentOriginationForwardEndpointDirectRLPObstructionV1_118

universe u

noncomputable section

/-!
The v1.118 minimally-scaled forward endpoint nonlifting square does not
automatically live over the induced-scaled endpoint pushout-product.
Here we compute the exact admission condition for the source-scaling
enrichment, preserving the original geometric witness and all hypotheses.
This is NOT an induced-scaled endpoint RLP or fibrancy certificate.
-/

/-- A map defined on the minimal attachment factors through the identity
source-scaling enrichment precisely when it preserves the stronger induced
scaling. No proof of an extension across the cylinder is assumed. -/
theorem minimalForward_factor_through_induced_iff_scaled
    {X : SSet.{u}}
    (sX : ScaledSimplicialSet X)
    (n : Nat) (i : Fin (n + 1))
    (sDelta : ScaledSimplicialSet (Δ[n] : SSet.{u}))
    (f : minimallyScaledHornCylinderAttachment n i 0 ⟶ ScaledSSet.of X sX) :
    (∃ k : inducedScaledHornCylinderAttachment i 0 sDelta ⟶ ScaledSSet.of X sX,
      minimalToInducedHornCylinderAttachment i 0 sDelta ≫ k = f) ↔
      IsScaledMap (inducedHornCylinderAttachmentScaling i 0 sDelta) sX f.map := by
  constructor
  · rintro ⟨k, hk⟩
    have hmap : k.map = f.map := by
      have h := congrArg ScaledSSet.ScaledMap.map hk
      simpa [minimalToInducedHornCylinderAttachment] using h
    rw [← hmap]
    exact k.scaled
  · intro hf
    refine ⟨⟨f.map, hf⟩, ?_⟩
    apply ScaledSSet.ScaledMap.ext
    simp [minimalToInducedHornCylinderAttachment]

/-- The full endpoint-zero simplex is scaled into the induced attachment,
unlike the minimal attachment where the stronger scaling is absent. -/
theorem endpointZero_into_induced_scaled
    {n : Nat} (i : Fin (n + 1))
    (sDelta : ScaledSimplicialSet (Δ[n] : SSet.{u})) :
    IsScaledMap sDelta (inducedHornCylinderAttachmentScaling i 0 sDelta)
      (endpointIntoAttachment n i 0) := by
  change IsScaledMap sDelta (simplexCylinderScaling sDelta)
    (endpointIntoAttachment n i 0 ≫ (hornCylinderAttachment n i 0).ι)
  rw [endpointIntoAttachment_ι_zero n i]
  exact endpointZero_scaled sDelta

/-- For the concrete projected family, factoring the minimal-source map
through induced scaling is equivalent to scaling of the original endpoint.
This is an exact statement about admissibility of the TOP arrow. -/
theorem projectedForward_factor_induced_iff_endpoint_scaled
    {X : SSet.{u}}
    (sX : ScaledSimplicialSet X)
    (n : Nat) (i : Fin (n + 1))
    (sDelta : ScaledSimplicialSet (Δ[n] : SSet.{u}))
    (sigma : (Δ[n] : SSet.{u}) ⟶ X) :
    (∃ k : inducedScaledHornCylinderAttachment i 0 sDelta ⟶ ScaledSSet.of X sX,
      minimalToInducedHornCylinderAttachment i 0 sDelta ≫ k =
        projectedForwardAttachmentMap sX n i sigma) ↔
        IsScaledMap sDelta sX sigma := by
  constructor
  · rintro ⟨k, hk⟩
    have hmap : k.map = (projectedForwardAttachmentMap sX n i sigma).map := by
      have h := congrArg ScaledSSet.ScaledMap.map hk
      simpa [minimalToInducedHornCylinderAttachment] using h
    have hs : IsScaledMap sDelta sX
        (endpointIntoAttachment n i 0 ≫ k.map) :=
      (endpointZero_into_induced_scaled i sDelta).comp k.scaled
    have heq : endpointIntoAttachment n i 0 ≫ k.map = sigma := by
      rw [hmap]
      exact projectedForwardAttachmentMap_endpoint_zero sX n i sigma
    rw [heq] at hs
    exact hs
  · intro hs
    refine ⟨inducedScaledHornCylinderAttachmentInclusion i 0 sDelta ≫
      projectedCylinderExtension sX n sDelta sigma hs, ?_⟩
    rw [← Category.assoc, scaledHornCylinderAttachmentInclusion_factorization]
    exact projectedCylinderExtension_restrict sX n i sDelta sigma hs

/-- The comparison-one B²Nat minimal forward square does NOT even define
an induced-scaled TOP map with the same underlying projected attachment.
This does not assert non-RLP for arbitrary induced-scaled attachment maps. -/
theorem natComparisonOne_minimal_forward_not_induced_admissible :
    ¬ ∃ k : inducedScaledHornCylinderAttachment (1 : Fin 3) 0
      (standardTypeASimplexScaling (1 : Fin 3)) ⟶
        natDoubleDeloopingScaledDuskin,
      minimalToInducedHornCylinderAttachment (1 : Fin 3) 0
        (standardTypeASimplexScaling (1 : Fin 3)) ≫ k =
          natNoninvertibleTriangleForwardAttachment := by
  intro h
  have hs := (projectedForward_factor_induced_iff_endpoint_scaled
    (duskinScaling NatDoubleDelooping)
    2 (1 : Fin 3) (standardTypeASimplexScaling (1 : Fin 3))
    (SSet.yonedaEquiv.symm natNoninvertibleTriangle)).mp h
  exact natNoninvertibleTriangle_not_standardTypeAScaled hs

#print axioms minimalForward_factor_through_induced_iff_scaled
#print axioms endpointZero_into_induced_scaled
#print axioms projectedForward_factor_induced_iff_endpoint_scaled
#print axioms natComparisonOne_minimal_forward_not_induced_admissible

end

end KUOS.DependentOriginationForwardEndpointInducedCompatibilityV1_120
