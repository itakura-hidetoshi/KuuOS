import KUOS.DependentOriginationStandardTypeAEndpointOppositeCellCertificateV1_77
import KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPPinnedV1_121

namespace KUOS.DependentOriginationDoubleDeloopingInducedEndpointRLPV1_121

open CategoryTheory
open CategoryTheory.Category
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58
open KUOS.DependentOriginationStandardABCLeibnizCellularComparisonV1_59
open KUOS.DependentOriginationStandardTypeAEndpointOppositeCellCertificateV1_77
open KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95
open KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106

noncomputable section

/-!
# Concrete induced-scaled type-(A) endpoint RLP for B²ℕ.

Pinned research source already proves:
- genuine A/B/C terminal right orthogonality for the concrete B²ℕ
  (pinned v1.106 bridge using actual type-C pushout cocycle witnesses);
- type-(A) endpoint prism cellularity/stability for the exact standard
  A/B/C presentation (v1.77).
This file glues the *same morphism properties* to a concrete lifting
statement for the induced-scaled endpoint map of v1.50.

The v1.118 counterexample involves the MINIMALLY scaled attachment,
which is a distinct morphism; nothing here denies that obstruction.
-/

/-- A concrete, unconditional terminal right lifting certificate for every
standard type-(A) *induced-scaled* endpoint pushout-product. -/
theorem natDoubleDelooping_typeA_inducedEndpoint_rlp
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    HasLiftingProperty
      (standardTypeAEndpointPushoutProductHom g)
      (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin) := by
  have hmem : standardGeneratedScaledAnodyneABC
      (standardTypeAEndpointPushoutProductHom g) :=
    (standardTypeAEndpointPushoutProducts_le_standardGenerated
      standardABCTypeAEndpointLeibnizStability_proved)
      _ (standardTypeAEndpointPushoutProductGenerator_mem g)
  exact hmem _ natDoubleDelooping_standardABC_generators_rlp

/-- Every actual admissible top arrow into the concrete B²ℕ Duskin nerve
has a scaled cylinder extension respecting the induced endpoint attachment. -/
theorem natDoubleDelooping_typeA_inducedEndpoint_actualExtension
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (f : standardTypeAEndpointPushoutProductSource g ⟶
      natDoubleDeloopingScaledDuskin) :
    ∃ l : scaledSimplexCylinder (standardTypeASimplexScaling g.i) ⟶
        natDoubleDeloopingScaledDuskin,
      standardTypeAEndpointPushoutProductHom g ≫ l = f := by
  exact (ScaledSSet.hasLiftingProperty_toPoint_iff
    (standardTypeAEndpointPushoutProductHom g)).mp
      (natDoubleDelooping_typeA_inducedEndpoint_rlp g) f

/-- A chosen literal scaled cylinder extension from the preceding
fully proven existence theorem, with no forward endpoint RLP assumption. -/
noncomputable def natDoubleDelooping_typeA_inducedEndpoint_chosenLift
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (f : standardTypeAEndpointPushoutProductSource g ⟶
      natDoubleDeloopingScaledDuskin) :
    scaledSimplexCylinder (standardTypeASimplexScaling g.i) ⟶
      natDoubleDeloopingScaledDuskin :=
  Classical.choose
    (natDoubleDelooping_typeA_inducedEndpoint_actualExtension g f)

/-- The chosen extension commutes with the *induced-scaled* attachment
inclusion, for the original arbitrary admissible top arrow. -/
theorem natDoubleDelooping_typeA_inducedEndpoint_chosenLift_fac
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (f : standardTypeAEndpointPushoutProductSource g ⟶
      natDoubleDeloopingScaledDuskin) :
    standardTypeAEndpointPushoutProductHom g ≫
      natDoubleDelooping_typeA_inducedEndpoint_chosenLift g f = f := by
  exact Classical.choose_spec
    (natDoubleDelooping_typeA_inducedEndpoint_actualExtension g f)

#print axioms natDoubleDelooping_typeA_inducedEndpoint_rlp
#print axioms natDoubleDelooping_typeA_inducedEndpoint_actualExtension
#print axioms natDoubleDelooping_typeA_inducedEndpoint_chosenLift
#print axioms natDoubleDelooping_typeA_inducedEndpoint_chosenLift_fac

end

end KUOS.DependentOriginationDoubleDeloopingInducedEndpointRLPV1_121
