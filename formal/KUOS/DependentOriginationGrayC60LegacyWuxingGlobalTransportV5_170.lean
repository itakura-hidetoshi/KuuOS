import KUOS.DependentOriginationGrayC60LegacyHetuLuoshuV5_170
import KUOS.DependentOriginationGrayC60CochainDescentV5_166

namespace KUOS.DependentOriginationGrayC60LegacyWuxingGlobalTransportV5_170

open KUOS.Architecture
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayC60AllThirtyTwoFaceCycleV5_158
open KUOS.DependentOriginationGrayC60IntegerOrientedSurfaceCycleV5_159
open KUOS.DependentOriginationGrayC60IntegralBoundaryLinearMapV5_159
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationGrayC60CochainDescentV5_166
open KUOS.DependentOriginationGrayC60WuxingPentagramQuiverV5_169
open KUOS.DependentOriginationGrayC60WuxingPentagramIncidenceV5_169
open KUOS.DependentOriginationGrayC60LegacyWuxingFibonacciBridgeV5_170

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F22 — constructive local-frame Wuxing phase and protected-history transport

Original KuuOS FivePhase = ZMod5 is a LOCAL functional differentiation
of YinYang; it is NOT globally reified as an intrinsic element name
for every C60 dart. We give all 12 C60 pentagons independent
frame offsets (one FivePhase each).

Every actual 90-edge transport is defined by the difference of
true source/target dart phases. On every pentagon it is the physical
Sheng successor +1; on cross edges it compares DIFFERENT C60
pentagonal contexts via their offsets.

The phase transport is the actual cellular coboundary δφ, so its
oriented flux around all 32 original pentagonal/hexagonal faces is
exactly zero by the previously proved d1*d2=0. This is genuine
full-face GLUING, not a declaration that all charts are globally
identical.

The original history-aware shift is a DIFFERENT object. Traversing
an edge is one new event independent of reversing its sign.
Thus each pentagon carries (0,5), each hexagon (0,6):
base phase closes but protected Fibonacci lineage keeps advancing.
The original 60-90-32 cellular chain differential is not changed.
-/

/-- Position of one of the TRUE original 60 C60 dart vertices
among its parent icosahedral vertex's five incident slots.
The exhaustive table is taken from v3.85 original geometry. -/
def c60LegacyDartLocalPhase : IcosahedralDart → FivePhase
  | .first (.northSpoke i) => i
  | .second (.northSpoke _) => 0
  | .first (.southSpoke i) => i
  | .second (.southSpoke _) => 0
  | .first (.upperRing _) => 1
  | .second (.upperRing _) => 4
  | .first (.lowerRing _) => 1
  | .second (.lowerRing _) => 4
  | .first (.crossAligned _) => 2
  | .second (.crossAligned _) => 3
  | .first (.crossShifted _) => 3
  | .second (.crossShifted _) => 2

/-- The original LOCAL 5-slot coordinates are recovered
at each of 12 real pentagons without changing the C60 darts. -/
theorem c60LegacyDartLocalPhase_at_originalSlot :
    ∀ v : IcosahedralVertex, ∀ s : PentagonalSlot,
      c60LegacyDartLocalPhase (icosahedralIncidentDartAt v s) =
        pentagonalSlotIndex s := by decide

/-- A local KuuOS phase frame on each of the twelve
independent actual original C60 pentagons. No frame is preferred. -/
abbrev C60LegacyWuxingFrames := IcosahedralVertex → FivePhase

/-- An actual original C60 dart's current phase, in the locally
chosen chart of its parent icosahedral pentagon vertex. -/
def c60LegacyLocalDartPhase (frame : C60LegacyWuxingFrames)
    (d : IcosahedralDart) : FivePhase :=
  c60LegacyDartLocalPhase d + frame d.endpoint

/-- On each original pentagon a Sheng edge advances +1
independently of the arbitrary chart offset. -/
theorem c60LegacyLocalShengStep
    (frame : C60LegacyWuxingFrames)
    (v : IcosahedralVertex) (p : WuxingPhase) :
    c60LegacyLocalDartPhase frame
        (c60WuxingDart v (wuxingSheng p)) =
      generationPhase
        (c60LegacyLocalDartPhase frame (c60WuxingDart v p)) := by
  unfold c60LegacyLocalDartPhase generationPhase
  rw [c60WuxingDart, c60WuxingDart,
    c60LegacyDartLocalPhase_at_originalSlot,
    c60LegacyDartLocalPhase_at_originalSlot,
    wuxingSlotSheng_equivariant]
  rw [icosahedralIncidentDartAt_endpoint,
    icosahedralIncidentDartAt_endpoint]
  have hstep :
      ∀ s : PentagonalSlot,
        pentagonalSlotIndex (pentagonalSlotNext s) =
          pentagonalSlotIndex s + 1 := by
    intro s
    cases s <;> decide
  rw [hstep]
  ring

/-- KuuOS phase-valued zero-cochain on the 60 actual C60 darts. -/
def c60LegacyPhasePotential (frame : C60LegacyWuxingFrames) :
    C60IntegralZeroChains →ₗ[ℤ] FivePhase :=
  Finsupp.linearCombination ℤ (c60LegacyLocalDartPhase frame)

/-- Native physical C60 signed edge transport δφ: neither
a detached symbolic graph map nor a fictitious extra C60 edge. -/
def c60LegacyPhaseEdgeTransport (frame : C60LegacyWuxingFrames) :
    C60IntegralOneChains →ₗ[ℤ] FivePhase :=
  (c60LegacyPhasePotential frame).comp c60IntegralBoundaryOne

/-- An original actual 90-edge transport increments the
protected-history event counter by exactly one. -/
def c60LegacyActualEdgeShift (frame : C60LegacyWuxingFrames)
    (e : TruncatedIcosahedralEdge) : WuxingShift :=
  (c60LegacyPhaseEdgeTransport frame (Finsupp.single e (1 : ℤ)), 1)

/-- Reversing an original edge's geometric orientation NEGATES
the Z5 phase transport, but still records a NEW history event. -/
def c60LegacyActualReverseEdgeShift (frame : C60LegacyWuxingFrames)
    (e : TruncatedIcosahedralEdge) : WuxingShift :=
  (-c60LegacyPhaseEdgeTransport frame (Finsupp.single e (1 : ℤ)), 1)

theorem c60LegacyOppositeEdge_phase_inverse
    (frame : C60LegacyWuxingFrames)
    (e : TruncatedIcosahedralEdge) :
    (c60LegacyActualEdgeShift frame e).1 +
      (c60LegacyActualReverseEdgeShift frame e).1 = 0 := by
  simp [c60LegacyActualEdgeShift, c60LegacyActualReverseEdgeShift]

theorem c60LegacyOppositeEdge_history_retained
    (frame : C60LegacyWuxingFrames)
    (e : TruncatedIcosahedralEdge) :
    (c60LegacyActualEdgeShift frame e +
      c60LegacyActualReverseEdgeShift frame e).2 = 2 := by
  rfl

/-- Actual C60 facewise FULL protected-history transport.
Its phase coordinate uses the TRUE signed integer cellular
boundary. Its natural-number event count uses the true
oriented pentagon/hexagon edge LIST, never signed subtraction
of events. -/
def c60LegacyOriginalFaceShift (frame : C60LegacyWuxingFrames)
    (face : TruncatedIcosahedralSeedFace) : WuxingShift :=
  (c60LegacyPhaseEdgeTransport frame (c60IntegerFaceBoundaryChain face),
    (c60IntegerOrientedFaceBoundary face).length)

/-- Every original 12+20 face has zero Z5 phase shift:
the actual original C60 d₁∘d₂=0 is applied to a globally
consistent LOCAL-frame phase potential. -/
theorem c60LegacyEveryFace_phase_closed
    (frame : C60LegacyWuxingFrames)
    (face : TruncatedIcosahedralSeedFace) :
    (c60LegacyOriginalFaceShift frame face).1 = 0 := by
  change c60LegacyPhasePotential frame
    (c60IntegralBoundaryOne (c60IntegerFaceBoundaryChain face)) = 0
  rw [c60IntegralBoundaryOne_eachOrientedFace_zero, map_zero]

/-- The original 12 pentagons record five interaction events
each; the 20 genuine hexagons record six each, independently
of the local Wuxing chart and signed incidence orientation. -/
theorem c60LegacyEveryFace_history_event_count
    (frame : C60LegacyWuxingFrames)
    (face : TruncatedIcosahedralSeedFace) :
    (c60LegacyOriginalFaceShift frame face).2 =
      match face with
      | .aroundVertex _ => 5
      | .fromTriangle _ => 6 := by
  cases face <;> rfl

/-- The signed Wuxing phase returns but the NEW events persist:
one actual north/south/ring pentagon has original shift (0,5). -/
theorem c60LegacyPentagon_shift
    (frame : C60LegacyWuxingFrames)
    (v : IcosahedralVertex) :
    c60LegacyOriginalFaceShift frame (.aroundVertex v) =
      ((0 : FivePhase), (5 : Nat)) := by
  apply Prod.ext
  · exact c60LegacyEveryFace_phase_closed frame _
  · exact c60LegacyEveryFace_history_event_count frame _

/-- Each of the ACTUAL 20 six-edge faces produces a
phase-closed six-event protected shift (0,6). -/
theorem c60LegacyHexagon_shift
    (frame : C60LegacyWuxingFrames)
    (f : IcosahedralFace) :
    c60LegacyOriginalFaceShift frame (.fromTriangle f) =
      ((0 : FivePhase), (6 : Nat)) := by
  apply Prod.ext
  · exact c60LegacyEveryFace_phase_closed frame _
  · exact c60LegacyEveryFace_history_event_count frame _

/-- Original unit Fibonacci lineage after six events: history
is (5,8), distinctly more than the five-event (3,5) record. -/
theorem c60LegacyUnitHistory_after_six :
    advanceHistoryN 6 unitHistory = ⟨5, 8⟩ := by decide

/-- Literal v2.6 action of one original pentagon traversal:
phase returns, but original Fibonacci history becomes (3,5). -/
theorem c60LegacyPentagon_fibonacci_return
    (frame : C60LegacyWuxingFrames)
    (v : IcosahedralVertex) (phase : FivePhase) :
    applyShift (c60LegacyOriginalFaceShift frame (.aroundVertex v))
      ⟨phase, unitHistory⟩ = ⟨phase, ⟨3,5⟩⟩ := by
  rw [c60LegacyPentagon_shift]
  simp [applyShift]; decide

/-- Literal v2.6 action of one actual hexagon traversal:
phase returns, history becomes (5,8). -/
theorem c60LegacyHexagon_fibonacci_return
    (frame : C60LegacyWuxingFrames)
    (f : IcosahedralFace) (phase : FivePhase) :
    applyShift (c60LegacyOriginalFaceShift frame (.fromTriangle f))
      ⟨phase, unitHistory⟩ = ⟨phase, ⟨5,8⟩⟩ := by
  rw [c60LegacyHexagon_shift]
  simp [applyShift]; decide

/-- Across the true original closed C60, all 12 pentagonal
and 20 hexagonal boundaries record exactly 180 events.
This is a total over face incidences, not the count of
90 distinct geometric edges (each occurs twice). -/
theorem c60LegacyAllThirtyTwoFaces_history180
    (frame : C60LegacyWuxingFrames) :
    (∑ face : TruncatedIcosahedralSeedFace,
      (c60LegacyOriginalFaceShift frame face).2) = 180 := by
  classical
  rw [kernelC60SumOverAllRealFaces]
  simp [c60LegacyOriginalFaceShift,
    c60IntegerOrientedFaceBoundary_length,
    kernelC60FullFaceBoundary_length]

/-- Reframing all 12 local C60 pentagons arbitrarily does NOT
disturb the facewise phase closure. This is true for ANY
independently supplied local chart offsets, not just a fixed
north/south assignment. -/
theorem c60LegacyFrameChange_preserves_face_gluing
    (first second : C60LegacyWuxingFrames)
    (face : TruncatedIcosahedralSeedFace) :
    c60LegacyOriginalFaceShift first face =
      c60LegacyOriginalFaceShift second face := by
  cases face with
  | aroundVertex v =>
      rw [c60LegacyPentagon_shift, c60LegacyPentagon_shift]
  | fromTriangle f =>
      rw [c60LegacyHexagon_shift, c60LegacyHexagon_shift]

#print axioms c60LegacyDartLocalPhase_at_originalSlot
#print axioms c60LegacyLocalShengStep
#print axioms c60LegacyEveryFace_phase_closed
#print axioms c60LegacyEveryFace_history_event_count
#print axioms c60LegacyOppositeEdge_phase_inverse
#print axioms c60LegacyOppositeEdge_history_retained
#print axioms c60LegacyPentagon_shift
#print axioms c60LegacyHexagon_shift
#print axioms c60LegacyUnitHistory_after_six
#print axioms c60LegacyPentagon_fibonacci_return
#print axioms c60LegacyHexagon_fibonacci_return
#print axioms c60LegacyAllThirtyTwoFaces_history180
#print axioms c60LegacyFrameChange_preserves_face_gluing

end
end KUOS.DependentOriginationGrayC60LegacyWuxingGlobalTransportV5_170
