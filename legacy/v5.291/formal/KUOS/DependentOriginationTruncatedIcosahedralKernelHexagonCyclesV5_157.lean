import KUOS.DependentOriginationGrayC60AllNinetyEdgePastingV5_157

namespace KUOS.DependentOriginationTruncatedIcosahedralKernelHexagonCyclesV5_157

open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralHexagonsV3_86
open KUOS.DependentOriginationTruncatedIcosahedralCrossHexagonFlagSquaresV5_157

set_option autoImplicit false
noncomputable section

/-!
# F59-F3 / v5.157 — trusted twenty C60 hexagon six-edge cyclic boundaries

Earlier v3.86 had genuinely typed original oriented six-edge C60 hexagon
cycles but their pentagonal-slot inverse relied on older compiler-trusted
finite lemmas. Mere re-use of that old cycle can import unwanted axioms
into later higher-cell results, even when the final theorem uses 'rfl'.

We reconstruct the required slot RIGHT INVERSE with a fresh explicit
five-case function ZMod 5 → PentagonalSlot and kernel-checked equations.
We then build completely new original twenty oriented six-edge cycles,
with all SIX genuine edge-endpoint matching proofs performed here:
  h01, h12, h23, h34, h45, h50.
The exact old explicit C60 edge families/vertex labels are retained;
only the slot-index inverse and cycle proofs are independently rebuilt.

The hexagon has a real alternating around/cross six-edge boundary, and
the last edge meets the first without artificial endpoint quotienting.
These are true source incidence cycles, NOT C60 quadrilateral faces.
They are separate from the next F59-F4 step of assigning and composing
the original F55-generated target Gray 3-cells around each hexagon.

No trust in the old compiler-generated witnesses, no equation with old
Stage-II omega and no automatic external Gray tricategory functor.
-/

/-- A *new executable* inverse to the original five cyclic slot labels.
All five cases are explicit, with the final case covering the impossible
value >4 of a ZMod 5 representative. -/
def kernelCertifiedSlot (i : IcosahedralRingIndex) : PentagonalSlot :=
  match i.val with
  | 0 => .s0
  | 1 => .s1
  | 2 => .s2
  | 3 => .s3
  | _ => .s4

/-- Kernel-proved RIGHT INVERSE, replacing old non-kernel slot choice. -/
theorem kernelCertifiedSlot_index :
    ∀ i : IcosahedralRingIndex,
      pentagonalSlotIndex (kernelCertifiedSlot i) = i := by
  decide

/-- Crucial actual geometric successor property. This is
kernel-checked over the genuine five-element ring; it imports
no old compiler-trusted cyclic-slot theorem. -/
theorem kernelCertifiedSlot_nextIndex :
    ∀ i : IcosahedralRingIndex,
      pentagonalSlotIndex (pentagonalSlotNext (kernelCertifiedSlot i)) =
        i + 1 := by
  decide

/-- ORIGINAL twenty hexagonal faces, reconstructed with actual
oriented C60 edges and fresh six separate endpoint proofs.
The source proof fields themselves are part of this NEW structure,
not inherited from the old v3.86 cycle's certificate. -/
def kernelCertifiedHexagonCycle :
    IcosahedralFace → OrientedHexagonCycle
  | .top i =>
      {
        e0 := .forward
          (.around ⟨.north, kernelCertifiedSlot i⟩)
        e1 := .forward (.cross (.northSpoke (i + 1)))
        e2 := .reverse (.around ⟨.upper (i + 1), .s4⟩)
        e3 := .reverse (.cross (.upperRing i))
        e4 := .reverse (.around ⟨.upper i, .s0⟩)
        e5 := .reverse (.cross (.northSpoke i))
        h01 := by
          simp [icosahedralIncidentDartAt, kernelCertifiedSlot_nextIndex]
        h12 := by
          simp [icosahedralIncidentDartAt, pentagonalSlotNext]
        h23 := by
          simp [icosahedralIncidentDartAt]
        h34 := by
          simp [icosahedralIncidentDartAt, pentagonalSlotNext]
        h45 := by
          simp [icosahedralIncidentDartAt]
        h50 := by
          simp [icosahedralIncidentDartAt, kernelCertifiedSlot_index]
      }
  | .bottom i =>
      {
        e0 := .forward
          (.around ⟨.south, kernelCertifiedSlot i⟩)
        e1 := .forward (.cross (.southSpoke (i + 1)))
        e2 := .reverse (.around ⟨.lower (i + 1), .s4⟩)
        e3 := .reverse (.cross (.lowerRing i))
        e4 := .reverse (.around ⟨.lower i, .s0⟩)
        e5 := .reverse (.cross (.southSpoke i))
        h01 := by
          simp [icosahedralIncidentDartAt, kernelCertifiedSlot_nextIndex]
        h12 := by
          simp [icosahedralIncidentDartAt, pentagonalSlotNext]
        h23 := by
          simp [icosahedralIncidentDartAt]
        h34 := by
          simp [icosahedralIncidentDartAt, pentagonalSlotNext]
        h45 := by
          simp [icosahedralIncidentDartAt]
        h50 := by
          simp [icosahedralIncidentDartAt, kernelCertifiedSlot_index]
      }
  | .beltUpper i =>
      {
        e0 := .forward (.around ⟨.upper i, .s1⟩)
        e1 := .forward (.cross (.crossAligned i))
        e2 := .reverse (.around ⟨.lower i, .s2⟩)
        e3 := .reverse (.cross (.crossShifted i))
        e4 := .forward (.around ⟨.upper (i + 1), .s3⟩)
        e5 := .reverse (.cross (.upperRing i))
        h01 := by
          simp [icosahedralIncidentDartAt, pentagonalSlotNext]
        h12 := by
          simp [icosahedralIncidentDartAt, pentagonalSlotNext]
        h23 := by
          simp [icosahedralIncidentDartAt]
        h34 := by
          simp [icosahedralIncidentDartAt]
        h45 := by
          simp [icosahedralIncidentDartAt, pentagonalSlotNext]
        h50 := by
          simp [icosahedralIncidentDartAt]
      }
  | .beltLower i =>
      {
        e0 := .reverse (.around ⟨.upper (i + 1), .s2⟩)
        e1 := .forward (.cross (.crossAligned (i + 1)))
        e2 := .forward (.around ⟨.lower (i + 1), .s3⟩)
        e3 := .reverse (.cross (.lowerRing i))
        e4 := .forward (.around ⟨.lower i, .s1⟩)
        e5 := .reverse (.cross (.crossShifted i))
        h01 := by
          simp [icosahedralIncidentDartAt]
        h12 := by
          simp [icosahedralIncidentDartAt]
        h23 := by
          simp [icosahedralIncidentDartAt, pentagonalSlotNext]
        h34 := by
          simp [icosahedralIncidentDartAt]
        h45 := by
          simp [icosahedralIncidentDartAt, pentagonalSlotNext]
        h50 := by
          simp [icosahedralIncidentDartAt, pentagonalSlotNext]
      }


/-- Six edges of the freshly proved genuine cyclic hexagon. -/
theorem kernelCertifiedHexagonCycle_length (f : IcosahedralFace) :
    (kernelCertifiedHexagonCycle f).edges.length = 6 := by
  rfl

/-- The source and target darts agree at ALL SIX genuine cyclic
corners, including the closing sixth-to-first edge. -/
theorem kernelCertifiedHexagonCycle_allSixEndMatches
    (f : IcosahedralFace) :
    (kernelCertifiedHexagonCycle f).e0.target =
      (kernelCertifiedHexagonCycle f).e1.source ∧
    (kernelCertifiedHexagonCycle f).e1.target =
      (kernelCertifiedHexagonCycle f).e2.source ∧
    (kernelCertifiedHexagonCycle f).e2.target =
      (kernelCertifiedHexagonCycle f).e3.source ∧
    (kernelCertifiedHexagonCycle f).e3.target =
      (kernelCertifiedHexagonCycle f).e4.source ∧
    (kernelCertifiedHexagonCycle f).e4.target =
      (kernelCertifiedHexagonCycle f).e5.source ∧
    (kernelCertifiedHexagonCycle f).e5.target =
      (kernelCertifiedHexagonCycle f).e0.source := by
  exact ⟨(kernelCertifiedHexagonCycle f).h01,
    (kernelCertifiedHexagonCycle f).h12,
    (kernelCertifiedHexagonCycle f).h23,
    (kernelCertifiedHexagonCycle f).h34,
    (kernelCertifiedHexagonCycle f).h45,
    (kernelCertifiedHexagonCycle f).h50⟩

/-- A genuine C60 hexagon alternates three around-family
pentagon/hexagon edges and three cross-family hexagon/hexagon edges. -/
theorem kernelCertifiedHexagonCycle_families (f : IcosahedralFace) :
    ((kernelCertifiedHexagonCycle f).e0.family,
      (kernelCertifiedHexagonCycle f).e1.family,
      (kernelCertifiedHexagonCycle f).e2.family,
      (kernelCertifiedHexagonCycle f).e3.family,
      (kernelCertifiedHexagonCycle f).e4.family,
      (kernelCertifiedHexagonCycle f).e5.family) =
      (.around, .cross, .around, .cross, .around, .cross) := by
  cases f <;> rfl

/-- Exactly twenty original triangle-origin hexagons participate
in the newly constructed six-edge cycles. -/
theorem kernelCertifiedHexagonCycle_twenty :
    Fintype.card IcosahedralFace = 20 :=
  originalC60HexagonFace_card_kernel

#print axioms kernelCertifiedSlot
#print axioms kernelCertifiedSlot_index
#print axioms kernelCertifiedSlot_nextIndex
#print axioms kernelCertifiedHexagonCycle
#print axioms kernelCertifiedHexagonCycle_length
#print axioms kernelCertifiedHexagonCycle_allSixEndMatches
#print axioms kernelCertifiedHexagonCycle_families
#print axioms kernelCertifiedHexagonCycle_twenty

end
end KUOS.DependentOriginationTruncatedIcosahedralKernelHexagonCyclesV5_157
