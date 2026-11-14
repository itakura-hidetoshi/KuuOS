import KUOS.DependentOriginationForwardEndpointProjectedCylinderCoreV1_118
import KUOS.DependentOriginationForwardEndpointNatWitnessV1_118
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
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49

universe u

noncomputable section

/-!
# Concrete B²ℕ obstruction to minimally-scaled forward endpoint RLP

The geometric cylinder extension and necessary endpoint scaling arguments
are proved separately in `ForwardEndpointProjectedCylinderCoreV1_118`.
This file applies those concrete constructions to the comparison-1 triangle
of B²ℕ. It neither assumes ForwardEndpointScaledHornRLP nor claims the
induced-scaled standard type-(A) endpoint Leibniz statement fails.
-/

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
