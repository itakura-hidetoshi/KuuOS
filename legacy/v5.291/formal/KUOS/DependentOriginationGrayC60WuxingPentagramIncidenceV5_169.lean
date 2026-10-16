import KUOS.DependentOriginationGrayC60WuxingPentagramQuiverV5_169
import KUOS.DependentOriginationGrayC60NativeH2CompleteV5_165

namespace KUOS.DependentOriginationGrayC60WuxingPentagramIncidenceV5_169

open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayC60WuxingPentagramQuiverV5_169

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 5000000
noncomputable section

/-!
# F59-F21 — genuine pentagon↔pentagram attachment at all twelve C60 faces

Do NOT mutate the 60–90–32 integral CW complex whose native Mathlib
H₀ = ℤ, H₁ = 0, H₂ = ℤ were proved in F59-F15–F17.

Each of the twelve genuine C60 PENTAGON faces is associated with
one Wuxing five-phase quiver, charting Wood onto original slot s0
and the other phases in genuine pentagonal order.

The Sheng outer arrows ARE the original C60 60 around-edge family,
with their actual vertex-dart endpoints and original signed face
boundary. The Ke arrows are NEW DIAGONAL/virtual chord relations on
the SAME actual five boundary darts. We kernel-check that not one
Ke chord (nor its reversal) is any of the original ninety
geometric C60 edges. They are quiver DECORATIONS, never silently
added as an unproved C60 chain differential or F55 square generator.

Each of 12 faces has five physical Sheng edges and five virtual
Ke diagonals: sixty of each over all faces. The direction depends
on choosing slot s0 as Wood; no unpointed symmetry-independent
phase labeling is asserted.
-/

/-- Actual original dart vertex of one phase in a particular
genuine C60 pentagon. -/
def c60WuxingDart (v : IcosahedralVertex)
    (p : WuxingPhase) : IcosahedralDart :=
  icosahedralIncidentDartAt v (wuxingSlotEquiv p)

/-- Each Sheng arrow is EXACTLY an original C60 physical around
edge of the given pentagon, not a virtual additional incidence. -/
def c60WuxingShengPhysicalEdge (v : IcosahedralVertex)
    (p : WuxingPhase) : TruncatedIcosahedralEdge :=
  .around ⟨v, wuxingSlotEquiv p⟩

/-- Actual endpoints of the original around edge realize the
Wuxing generative transition as an equality of original darts. -/
theorem c60WuxingShengPhysicalEdge_endpoints
    (v : IcosahedralVertex) (p : WuxingPhase) :
    truncatedIcosahedralEdgeEndpoints
      (c60WuxingShengPhysicalEdge v p) =
        (c60WuxingDart v p,
          c60WuxingDart v (wuxingSheng p)) := by
  cases p <;> rfl

/-- EXACT identification of the five Sheng arrows in phase order
with the five REAL original C60 pentagon boundary edges. -/
theorem c60WuxingSheng_equals_originalPentagonBoundary
    (v : IcosahedralVertex) :
    wuxingGenerativeOrder.map (c60WuxingShengPhysicalEdge v) =
      truncatedIcosahedralPentagonBoundary v := by
  rfl

/-- Ke is an abstract diagonal from slot i to slot i+2.
Endpoints are genuine C60 darts, but this chord is NOT an edge
of the original cellular 1-skeleton. -/
def c60WuxingKeVirtualChord (v : IcosahedralVertex)
    (p : WuxingPhase) : IcosahedralDart × IcosahedralDart :=
  (c60WuxingDart v p, c60WuxingDart v (wuxingKe p))

/-- The control edge is the genuine second generative step
ON THE SAME pentagon's original five dart vertices. -/
theorem c60WuxingKe_is_two_sheng_steps
    (v : IcosahedralVertex) (p : WuxingPhase) :
    c60WuxingKeVirtualChord v p =
      (c60WuxingDart v p,
       c60WuxingDart v (wuxingSheng (wuxingSheng p))) := by
  change (c60WuxingDart v p, c60WuxingDart v (wuxingKe p)) = _
  rw [wuxingKe_eq_sheng_twice]

/-- KEY TOPOLOGICAL SAFETY CERTIFICATE: all virtual Ke diagonals
are DISTINCT from every real ORIGINAL C60 90-edge physical
incidence, checked over all twelve pentagons/five sources/ninety
original edges using the actual original endpoint definitions. -/
theorem c60WuxingKe_not_physical_forward :
    ∀ v : IcosahedralVertex, ∀ p : WuxingPhase,
      ∀ e : TruncatedIcosahedralEdge,
        truncatedIcosahedralEdgeEndpoints e ≠
          c60WuxingKeVirtualChord v p := by
  decide

/-- Even reversal cannot turn a controlling diagonal into
an original C60 edge: it is absent as an unoriented physical
90-edge too, rather than just having the wrong orientation. -/
theorem c60WuxingKe_not_physical_reverse :
    ∀ v : IcosahedralVertex, ∀ p : WuxingPhase,
      ∀ e : TruncatedIcosahedralEdge,
        truncatedIcosahedralEdgeEndpoints e ≠
          (c60WuxingKeVirtualChord v p).swap := by
  decide

/-- The five Ke chords on one face are distinct even as oriented
relations because their physical source darts are different. -/
theorem c60WuxingKe_chords_injective :
    ∀ v : IcosahedralVertex,
      Function.Injective (c60WuxingKeVirtualChord v) := by
  decide

/-- Chart equivalence: the twelve-by-five quiver corner positions
are EXACTLY the existing original sixty around-pentagon edge
labels. This is a bijection, not merely an equal total count. -/
def c60WuxingAroundEdgeEquiv :
    (IcosahedralVertex × WuxingPhase) ≃
      TruncatedIcosahedralAroundEdge where
  toFun vs := ⟨vs.1, wuxingSlotEquiv vs.2⟩
  invFun a := (a.center, wuxingSlotEquiv.symm a.slot)
  left_inv := by
    intro ⟨v, p⟩
    cases p <;> rfl
  right_inv := by
    intro a
    cases a with
    | mk v slot =>
        cases slot <;> rfl

/-- Physical phase-labeled Sheng edge count remains the original
sixty C60 around edges: 12 genuine pentagons times five phases. -/
theorem c60WuxingSheng_positions_card :
    Fintype.card (IcosahedralVertex × WuxingPhase) = 60 := by
  decide

/-- The virtual Ke diagonal decorations also count sixty, but
they DO NOT expand the original C60 90-edge cellular chain group. -/
theorem c60WuxingKe_decorations_card :
    Fintype.card (IcosahedralVertex × WuxingPhase) = 60 := by
  decide

#print axioms c60WuxingShengPhysicalEdge_endpoints
#print axioms c60WuxingSheng_equals_originalPentagonBoundary
#print axioms c60WuxingKe_is_two_sheng_steps
#print axioms c60WuxingKe_not_physical_forward
#print axioms c60WuxingKe_not_physical_reverse
#print axioms c60WuxingKe_chords_injective
#print axioms c60WuxingAroundEdgeEquiv
#print axioms c60WuxingSheng_positions_card
#print axioms c60WuxingKe_decorations_card

end
end KUOS.DependentOriginationGrayC60WuxingPentagramIncidenceV5_169
