import KUOS.DependentOriginationIndexedDuskinAdmissibilityV1_29
import KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42
import KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49

/-!
# Independent admissibility preservation and geometric horn rectification

Two distinct interfaces are proved here.

1. Standard type-(A) admissibility is preserved under any *genuine scaled*
   simplicial map.  This follows because its actual predicate records the
   inner index and both horn/simplex scalings, all of which the already
   certified scaled horn problem transport preserves exactly.  This is
   stronger than an index-only family, without identifying different
   universes or claiming a complete standard scaled-anodyne presentation.

2. Homotopy-to-strict rectification is CONSTRUCTED from the canonical
   scaled horn-cylinder attachment terminal RLP, using v1.41/v1.42 and the
   v1.37 homotopy-class boundary.  The requisite attachment fibrancy is
   still independent evidence: it is not asserted for an arbitrary Duskin
   nerve and is not silently inferred from a model equivalence.
-/

namespace KUOS.DependentOriginationIndependentAdmissibilityRectificationV1_29

open CategoryTheory Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27
open KUOS.DependentOriginationScaledDuskinHornTransportV1_29
open KUOS.DependentOriginationScaledDuskinUniverseLiftBridgeV1_29
open KUOS.DependentOriginationScaledHornHomotopyDescentV1_33
open KUOS.DependentOriginationHomotopyClassScaledHornInvariantV1_37
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationCoherentNormalizedScaledModelEquivalenceV1_32
open KUOS.DependentOriginationIndexedDuskinAdmissibilityV1_29

universe u u₁ u₂ v₁ v₂ w₁ w₂

/-- Type-(A) admissibility genuinely survives forward horn-map transport.
It includes the prescribed simplex and horn thinness predicates, not only
the inner-horn index.  No target family-map certificate is assumed. -/
theorem standardTypeA_admissible_map_iff
    {X Y : SSet.{u}}
    {sX : ScaledSimplicialSet X} {sY : ScaledSimplicialSet Y}
    {f : X ⟶ Y} (hf : IsScaledMap sX sY f)
    {n : Nat} {i : Fin (n + 1)}
    (P : ScaledHornExtensionProblem X sX n i) :
    (standardTypeAScaledHornFamily Y sY).admissible
      (mapScaledHornProblem hf P) ↔
        (standardTypeAScaledHornFamily X sX).admissible P :=
  Iff.rfl

/-- Consequently every scaled simplicial map constructs the actual
type-(A) chosen-family forward certificate. -/
def standardTypeAFamilyMap_of_scaledMap
    {X Y : SSet.{u}}
    {sX : ScaledSimplicialSet X} {sY : ScaledSimplicialSet Y}
    {f : X ⟶ Y} (hf : IsScaledMap sX sY f) :
    ScaledHornFamilyMap hf
      (standardTypeAScaledHornFamily X sX)
      (standardTypeAScaledHornFamily Y sY) where
  admissible_preserved := by
    intro n i P hP
    exact (standardTypeA_admissible_map_iff hf P).mpr hP

/-- The two-sided actual attachment lifting property produces homotopy-to-
strict horn-filler rectification.  The hypothesis is terminal RLP against
the fixed generator family, not another rectification axiom. -/
noncomputable def homotopyRectification_of_attachmentFibrant
    {X : SSet.{u}} {sX : ScaledSimplicialSet X}
    (hX : IsAttachmentFibrant (ScaledSSet.of X sX)) :
    ScaledHornHomotopyRectification X sX where
  rectify := by
    intro n i P h
    rcases h with ⟨Q⟩
    exact (problemTerminalRLPOfAttachmentFibrant hX P).strictify
      (homotopyClassScaledHornFillerOfHomotopy Q)

/-- Any compatible scaled-anodyne presentation has the same terminal RLP
as the canonical attachments, so its fibrancy yields rectification as well.
This does not equate arbitrary external generators with that presentation. -/
noncomputable def homotopyRectification_of_presentationFibrant
    {X : SSet.{u}} {sX : ScaledSimplicialSet X}
    (P : ScaledAnodynePresentation.{u})
    (hX : IsFibrantForPresentation P (ScaledSSet.of X sX)) :
    ScaledHornHomotopyRectification X sX :=
  homotopyRectification_of_attachmentFibrant
    ((isFibrantForPresentation_iff_attachmentFibrant P
      (ScaledSSet.of X sX)).mp hX)

/-- Native quasi-inverse now gives the ORIGINAL unlifted inner-horn
fibrancy equivalence with independently verified attachment fibrancy:
neither the two family maps nor homotopy rectification are hypotheses.
The two attachment-fibrancy requirements remain genuine geometric
lifting obligations and are not claimed for arbitrary bicategories. -/
theorem unliftedInnerHornFibrancy_iff_of_attachmentFibrant
    (B : Type u₁) [Bicategory.{w₁, v₁} B]
    (C : Type u₂) [Bicategory.{w₂, v₂} C]
    (F : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (G : StrictlyUnitaryBicategoricalModelEquivalence C B)
    (K : NormalizedCoherentQuasiInverse F G)
    (hB : IsAttachmentFibrant
      (ScaledSSet.of (normalizedDuskinSource B C)
        (normalizedDuskinSourceScaling B C)))
    (hC : IsAttachmentFibrant
      (ScaledSSet.of (normalizedDuskinTarget B C)
        (normalizedDuskinTargetScaling B C))) :
    HasScaledHornFillers (duskinNerve B) (duskinScaling B)
      (allInnerScaledHornFamily (duskinScaling B)) ↔
    HasScaledHornFillers (duskinNerve C) (duskinScaling C)
      (allInnerScaledHornFamily (duskinScaling C)) :=
  unliftedInnerHornFibrancy_iff_of_nativeQuasiInverse
    B C F G K
    (homotopyRectification_of_attachmentFibrant hB)
    (homotopyRectification_of_attachmentFibrant hC)

#print axioms standardTypeA_admissible_map_iff
#print axioms standardTypeAFamilyMap_of_scaledMap
#print axioms homotopyRectification_of_attachmentFibrant
#print axioms homotopyRectification_of_presentationFibrant
#print axioms unliftedInnerHornFibrancy_iff_of_attachmentFibrant

end KUOS.DependentOriginationIndependentAdmissibilityRectificationV1_29
