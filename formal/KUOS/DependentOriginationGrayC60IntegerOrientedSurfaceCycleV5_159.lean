import KUOS.DependentOriginationGrayC60AllThirtyTwoFaceCycleV5_158

namespace KUOS.DependentOriginationGrayC60IntegerOrientedSurfaceCycleV5_159

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralHexagonsV3_86
open KUOS.DependentOriginationTruncatedIcosahedralKernelHexagonCyclesV5_157
open KUOS.DependentOriginationGrayKernelHexagonIncidenceMultiplicityV5_157
open KUOS.DependentOriginationGrayC60AllThirtyTwoFaceCycleV5_158

set_option autoImplicit false
noncomputable section

/-!
# F59-F8 / v5.159 — genuine C60 oriented integral two-cycle

F59-F7 proved the original 32 faces form a combinatorial 2-cycle
over ZMod2: each genuine geometric edge occurs exactly twice.
INTEGER cancellation requires stronger structure: each incident
face must traverse their common edge in OPPOSITE directions.

The original F59-F3 trusted hexagon cycles are oriented, but the
four face families in their source file do not all use globally
compatible orientations. We specify a CONSISTENT global orientation
of the actual 12 vertex-origin pentagons and 20 triangle-origin
hexagons, assigning a sign to each WHOLE face (not to each
individual edge to force an artificial local cancellation).

The intrinsic C60 orientations have these face signs:
  pentagon north=-1, south=+1, upper=+1, lower=-1;
  hexagon top=+1, bottom=-1, beltUpper=-1, beltLower=+1.
Original around pentagon boundaries are the v3.85 forward cycles;
original hexagon six-edge routes are the axiom-clean F59-F3
oriented cycles.

We prove by kernel-reduced finite arithmetic that the resulting
SIGNED boundary coefficient of each of the 90 actual physical
edges is exactly zero OVER THE INTEGERS, not merely mod2.
We assemble the coefficients into a genuine finitely supported
integer 1-chain and prove that the sum of the 32 face-boundary
chains equals ZERO AS A FINSUPP.

This is a finite oriented integral 2-cycle certificate for the
original C60 combinatorial surface, not a computation of H₂,
sphere homeomorphism, source F55 global 3-cell coherences, or
the historic Stage-II obstruction omega.
-/

/-- Orientation of the original twelve pentagonal C60 faces.
All five actual boundary edges of one pentagon share this sign. -/
def c60PentagonOrientation : IcosahedralVertex → ℤ
  | .north => -1
  | .south => 1
  | .upper _ => 1
  | .lower _ => -1

/-- Orientation of the original twenty genuine hexagonal C60 faces.
This adjusts only WHOLE-FACE orientations of the trusted F59-F3
six-edge cycles: it never flips an arbitrary edge in isolation. -/
def c60HexagonOrientation : IcosahedralFace → ℤ
  | .top _ => 1
  | .bottom _ => -1
  | .beltUpper _ => -1
  | .beltLower _ => 1

/-- Sign of an edge relative to its original truncated-edge endpoint
ordering. Forward is +1, reverse -1. -/
def c60OrientedEdgeDirection :
    OrientedTruncatedIcosahedralEdge → ℤ
  | .forward _ => 1
  | .reverse _ => -1

/-- Genuine 32-face *oriented* integer boundary list. For pentagons
use their five around-edge forward cycles with a whole-face sign.
For hexagons use the F59-F3 certified actual oriented six-edge cycle
with its whole-face sign. Every entry names an original C60 edge. -/
def c60IntegerOrientedFaceBoundary :
    TruncatedIcosahedralSeedFace →
      List (TruncatedIcosahedralEdge × ℤ)
  | .aroundVertex v =>
      (truncatedIcosahedralPentagonBoundary v).map
        (fun e => (e, c60PentagonOrientation v))
  | .fromTriangle f =>
      (kernelCertifiedHexagonCycle f).edges.map
        (fun e => (e.edge, c60HexagonOrientation f * c60OrientedEdgeDirection e))

/-- Length of every oriented boundary is the original geometric
face arity, five for pentagon, six for hexagon. -/
theorem c60IntegerOrientedFaceBoundary_length
    (f : TruncatedIcosahedralSeedFace) :
    (c60IntegerOrientedFaceBoundary f).length =
      (kernelC60FullFaceBoundaryEdges f).length := by
  cases f <;> rfl

/-- Forgetting integer signs recovers the EXACT original,
previously proved C60 face boundary edge list. -/
theorem c60IntegerOrientedFaceBoundary_forget
    (f : TruncatedIcosahedralSeedFace) :
    (c60IntegerOrientedFaceBoundary f).map Prod.fst =
      kernelC60FullFaceBoundaryEdges f := by
  cases f <;>
    simp only [c60IntegerOrientedFaceBoundary,
      kernelC60FullFaceBoundaryEdges, List.map_map,
      Function.comp_def]
  all_goals rfl

/-- Genuine signed boundary coefficient contributed by a single
oriented actual C60 face at a particular original physical edge. -/
def c60IntegerFaceEdgeCoefficient
    (f : TruncatedIcosahedralSeedFace)
    (e : TruncatedIcosahedralEdge) : ℤ :=
  ((c60IntegerOrientedFaceBoundary f).map
    (fun p => if p.1 = e then p.2 else (0 : ℤ))).sum

/-- The integer boundary coefficient at an edge for the SUM of
all 32 consistently oriented actual C60 face boundaries. -/
def c60IntegerFullSurfaceEdgeCoefficient
    (e : TruncatedIcosahedralEdge) : ℤ :=
  ∑ f : TruncatedIcosahedralSeedFace,
    c60IntegerFaceEdgeCoefficient f e

/-- EVERY real around/pentagon-hexagon edge receives opposite
integer signs from its adjacent pentagon and hexagon faces.
This is checked over all sixty physical edge cases, not inferred
from parity of its incidence multiplicity. -/
theorem c60IntegerAroundEdgeBoundary_zero :
    ∀ a : TruncatedIcosahedralAroundEdge,
      c60IntegerFullSurfaceEdgeCoefficient (.around a) = 0 := by
  decide

/-- EVERY real cross/hexagon-hexagon edge is traversed with
opposite integer signs by its two actual hexagonal faces.
All thirty physical cross edge cases are checked independently. -/
theorem c60IntegerCrossEdgeBoundary_zero :
    ∀ e : IcosahedralEdge,
      c60IntegerFullSurfaceEdgeCoefficient (.cross e) = 0 := by
  decide

/-- A full integral oriented cycle on the ACTUAL 90 physical edges,
proved COEFFICIENTWISE without reducing ℤ to parity. -/
theorem c60IntegerFullSurfaceEdgeCoefficient_zero
    (e : TruncatedIcosahedralEdge) :
    c60IntegerFullSurfaceEdgeCoefficient e = 0 := by
  cases e with
  | around a => exact c60IntegerAroundEdgeBoundary_zero a
  | cross e => exact c60IntegerCrossEdgeBoundary_zero e

/-- More strongly, the integer boundary coefficient vanishes as
a function of the entire original 90-edge source carrier. -/
theorem c60IntegerFullSurfaceBoundaryFunction_zero :
    c60IntegerFullSurfaceEdgeCoefficient =
      (fun _ : TruncatedIcosahedralEdge => (0 : ℤ)) := by
  funext e
  exact c60IntegerFullSurfaceEdgeCoefficient_zero e

/-- Each original oriented face has a GENUINE integer 1-chain,
with at most 90 support elements (in fact 5 or 6). Its coefficients
are actual signed physical-edge incidence coefficients. -/
def c60IntegerFaceBoundaryChain
    (f : TruncatedIcosahedralSeedFace) :
    TruncatedIcosahedralEdge →₀ ℤ :=
  Finsupp.onFinset Finset.univ
    (fun e => c60IntegerFaceEdgeCoefficient f e)
    (by intro e _; exact Finset.mem_univ e)

/-- The actual oriented global C60 boundary is an integer 1-CHAIN,
not a standalone scalar charge, and sums all 32 physical faces. -/
def c60IntegerFullSurfaceBoundaryChain :
    TruncatedIcosahedralEdge →₀ ℤ :=
  ∑ f : TruncatedIcosahedralSeedFace,
    c60IntegerFaceBoundaryChain f

/-- The full SOURCE integer 1-chain vanishes identically. This is
a certified oriented finite integral 2-cycle, strictly stronger
than the earlier F59-F7 mod-two boundary cancellation. -/
theorem c60IntegerFullSurfaceBoundaryChain_zero :
    c60IntegerFullSurfaceBoundaryChain = 0 := by
  apply Finsupp.ext
  intro e
  simp only [c60IntegerFullSurfaceBoundaryChain,
    c60IntegerFaceBoundaryChain, Finsupp.zero_apply]
  exact c60IntegerFullSurfaceEdgeCoefficient_zero e

/-- Signed integer boundary reduction gives the previously proved
F59-F7 mod-two zero boundary, while its integral result is stronger:
the original signs were fixed *globally* on all 32 faces. -/
theorem c60IntegralCycle_refines_modTwoCycle :
    c60IntegerFullSurfaceBoundaryChain = 0 ∧
    kernelC60FullFaceBoundaryModTwoCoefficient =
      (fun _ : TruncatedIcosahedralEdge => (0 : ZMod 2)) := by
  exact ⟨c60IntegerFullSurfaceBoundaryChain_zero,
    kernelC60FullFaceBoundaryModTwo_zero⟩

#print axioms c60PentagonOrientation
#print axioms c60HexagonOrientation
#print axioms c60IntegerOrientedFaceBoundary
#print axioms c60IntegerOrientedFaceBoundary_length
#print axioms c60IntegerOrientedFaceBoundary_forget
#print axioms c60IntegerFaceEdgeCoefficient
#print axioms c60IntegerAroundEdgeBoundary_zero
#print axioms c60IntegerCrossEdgeBoundary_zero
#print axioms c60IntegerFullSurfaceEdgeCoefficient_zero
#print axioms c60IntegerFullSurfaceBoundaryFunction_zero
#print axioms c60IntegerFaceBoundaryChain
#print axioms c60IntegerFullSurfaceBoundaryChain_zero
#print axioms c60IntegralCycle_refines_modTwoCycle

end
end KUOS.DependentOriginationGrayC60IntegerOrientedSurfaceCycleV5_159
