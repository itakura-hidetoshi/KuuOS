import KUOS.DependentOriginationGrayKernelHexagonWeightedDoubleCountV5_157

namespace KUOS.DependentOriginationGrayC60AllThirtyTwoFaceCycleV5_158

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralHexagonsV3_86
open KUOS.DependentOriginationGrayKernelHexagonIncidenceMultiplicityV5_157
open KUOS.DependentOriginationGrayKernelHexagonWeightedDoubleCountV5_157
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156

set_option autoImplicit false
noncomputable section

/-!
# F59-F7 / v5.158 — all thirty-two actual C60 faces form a mod-two 2-cycle

F59-F3/F5 certified twenty authentic six-edge hexagonal boundaries,
with each around edge appearing once and each cross edge twice.
F59-F6 proved UNIVERSAL double counting for any additive monoid
and any edge-dependent weight, not merely constant Gray charges.

The twelve original C60 pentagonal boundaries contribute each of
the SIXTY around edges exactly ONCE and no cross edge. Combining
them with the twenty kernel-certified hexagons proves that every
one of the NINETY physical C60 edges appears exactly TWICE among
the 32 complete face-boundary lists.

This is a genuine finite source-incidence statement independent
of the F55 generator charges or target exchange phase. Thus the
sum of ALL 32 faces has ZERO edge boundary COEFFICIENTWISE over
ZMod2. It realizes the mod-two 2-CYCLE of the original closed
5.6.6 C60 surface, without assuming a homology-group generator
or a geometric realization homeomorphic to a sphere.

For ANY AddCommMonoid and ANY edge-dependent weight, the sum
over all 32 real face boundaries is TWO TIMES the sum over the
90 distinct physical edges. For neutral F59-C Gray 3-cell values,
this gives a genuine typed target composite whose phase vanishes
for ANY label choice, not only the uniform original F55 square.

None of these equations identifies the old Stage-II obstruction
omega or supplies an unrestricted Gray 3-functor with original
F/G/eta/epsilon three-dimensional pasting coherence.
-/

/-- Actual original vertex-origin pentagon edge multiplicity:
count appearances of one physical C60 edge across ALL twelve
five-edge pentagon boundaries. -/
def kernelC60PentagonEdgeMultiplicity
    (edge : TruncatedIcosahedralEdge) : Nat :=
  ∑ v : IcosahedralVertex,
    (truncatedIcosahedralPentagonBoundary v).count edge

/-- Every original pentagon-to-hexagon around edge lies on EXACTLY
one of the original twelve pentagonal boundary lists. -/
theorem kernelC60PentagonAroundMultiplicity :
    ∀ a : TruncatedIcosahedralAroundEdge,
      kernelC60PentagonEdgeMultiplicity (.around a) = 1 := by
  decide

/-- Original hexagon-to-hexagon cross edges do not occur on any
of the genuine twelve original pentagonal boundary lists. -/
theorem kernelC60PentagonCrossMultiplicity :
    ∀ e : IcosahedralEdge,
      kernelC60PentagonEdgeMultiplicity (.cross e) = 0 := by
  decide

/-- The FULL C60 source-incidence multiplicity law, EDGE BY EDGE.
Both real face families together meet EVERY original physical edge
exactly twice. No integer charge or exchange phase is involved. -/
theorem kernelC60AllFacesEdgeMultiplicity_sum_eq_two
    (edge : TruncatedIcosahedralEdge) :
    kernelC60PentagonEdgeMultiplicity edge +
      kernelC60HexagonEdgeMultiplicity edge = 2 := by
  cases edge with
  | around a =>
      rw [kernelC60PentagonAroundMultiplicity a,
        kernelC60AroundEdge_hexagonMultiplicity a]
  | cross e =>
      rw [kernelC60PentagonCrossMultiplicity e,
        kernelC60CrossEdge_hexagonMultiplicity e]

/-- The true 32-face type, distinguished into twelve vertex-origin
pentagons and twenty triangle-origin hexagons, is equivalent to the
original disjoint union of its two authentic face families. -/
def kernelC60FullFaceEquiv :
    TruncatedIcosahedralSeedFace ≃
      (IcosahedralVertex ⊕ IcosahedralFace) where
  toFun
    | .aroundVertex v => .inl v
    | .fromTriangle f => .inr f
  invFun
    | .inl v => .aroundVertex v
    | .inr f => .fromTriangle f
  left_inv := by
    intro face
    cases face <;> rfl
  right_inv := by
    intro s
    cases s <;> rfl

/-- The actual boundary edges of EACH of the 32 original C60
polygonal faces, not an invented collection of quadrilateral faces. -/
def kernelC60FullFaceBoundaryEdges :
    TruncatedIcosahedralSeedFace → List TruncatedIcosahedralEdge
  | .aroundVertex v => truncatedIcosahedralPentagonBoundary v
  | .fromTriangle f => kernelC60HexagonBoundaryEdges f

/-- A real vertex-origin face has five actual original edges;
a real triangle-origin face has six. -/
theorem kernelC60FullFaceBoundary_length
    (face : TruncatedIcosahedralSeedFace) :
    (kernelC60FullFaceBoundaryEdges face).length =
      match face with
      | .aroundVertex _ => 5
      | .fromTriangle _ => 6 := by
  cases face <;> rfl

/-- A generic finite SUM on the actual 32-face type splits
exactly over its original 12 pentagons and 20 hexagons. -/
theorem kernelC60SumOverAllRealFaces
    {A : Type*} [AddCommMonoid A]
    (w : TruncatedIcosahedralSeedFace → A) :
    (∑ face : TruncatedIcosahedralSeedFace, w face) =
      (∑ v : IcosahedralVertex, w (.aroundVertex v)) +
        (∑ f : IcosahedralFace, w (.fromTriangle f)) := by
  classical
  calc
    (∑ face : TruncatedIcosahedralSeedFace, w face) =
        ∑ s : IcosahedralVertex ⊕ IcosahedralFace,
          w (kernelC60FullFaceEquiv.symm s) := by
            apply Fintype.sum_equiv kernelC60FullFaceEquiv
            intro face
            cases face <;> rfl
    _ = (∑ v : IcosahedralVertex, w (.aroundVertex v)) +
        (∑ f : IcosahedralFace, w (.fromTriangle f)) := by
          rw [Fintype.sum_sum_type]
          rfl

/-- Count a given physical edge across the genuinely complete
original 32-face list. This tracks FACE-EDGE OCCURRENCES, not
different geometric edge objects. -/
def kernelC60FullFaceEdgeMultiplicity
    (edge : TruncatedIcosahedralEdge) : Nat :=
  ∑ face : TruncatedIcosahedralSeedFace,
    (kernelC60FullFaceBoundaryEdges face).count edge

/-- Certified actual C60 face-geometry, not a mere equation
between two integer target invariant values: EVERY physical edge
appears EXACTLY twice across all original 32 face boundaries. -/
theorem kernelC60FullFaceEdgeMultiplicity_two
    (edge : TruncatedIcosahedralEdge) :
    kernelC60FullFaceEdgeMultiplicity edge = 2 := by
  unfold kernelC60FullFaceEdgeMultiplicity
  rw [kernelC60SumOverAllRealFaces]
  change kernelC60PentagonEdgeMultiplicity edge +
    kernelC60HexagonEdgeMultiplicity edge = 2
  exact kernelC60AllFacesEdgeMultiplicity_sum_eq_two edge

/-- The original polygonal 32-face sum is a mod-two cycle:
its 1-chain boundary COEFFICIENT at EVERY physical C60 edge
is zero, because each such edge is contained twice. -/
def kernelC60FullFaceBoundaryModTwoCoefficient
    (edge : TruncatedIcosahedralEdge) : ZMod 2 :=
  (kernelC60FullFaceEdgeMultiplicity edge : ZMod 2)

theorem kernelC60FullFaceBoundaryModTwoCoefficient_zero
    (edge : TruncatedIcosahedralEdge) :
    kernelC60FullFaceBoundaryModTwoCoefficient edge = 0 := by
  rw [kernelC60FullFaceBoundaryModTwoCoefficient,
    kernelC60FullFaceEdgeMultiplicity_two]
  decide

/-- All ninety boundary coefficients vanish simultaneously, as
an EQUALITY OF EDGE-INDEXED FUNCTIONS, not merely a sum of scalars.
This is a genuine source-incidence mod-two 2-cycle certificate. -/
theorem kernelC60FullFaceBoundaryModTwo_zero :
    kernelC60FullFaceBoundaryModTwoCoefficient =
      (fun _ : TruncatedIcosahedralEdge => (0 : ZMod 2)) := by
  funext edge
  exact kernelC60FullFaceBoundaryModTwoCoefficient_zero edge

/-- Arbitrary additive edge weights on the twelve original
pentagon boundaries can be regrouped by their TRUE incidence
counts, independently of the weights and of any F55 choices. -/
theorem kernelC60PentagonWeightedDoubleCount
    {A : Type*} [AddCommMonoid A]
    (w : TruncatedIcosahedralEdge → A) :
    (∑ v : IcosahedralVertex,
      ((truncatedIcosahedralPentagonBoundary v).map w).sum) =
      ∑ edge : TruncatedIcosahedralEdge,
        kernelC60PentagonEdgeMultiplicity edge • w edge := by
  classical
  calc
    (∑ v : IcosahedralVertex,
      ((truncatedIcosahedralPentagonBoundary v).map w).sum) =
        ∑ v : IcosahedralVertex,
          ∑ edge : TruncatedIcosahedralEdge,
            ((truncatedIcosahedralPentagonBoundary v).count edge) • w edge := by
              apply Finset.sum_congr rfl
              intro v _
              exact c60ListWeightedSumByMultiplicity w _
    _ = ∑ edge : TruncatedIcosahedralEdge,
          ∑ v : IcosahedralVertex,
            ((truncatedIcosahedralPentagonBoundary v).count edge) • w edge := by
              rw [Finset.sum_comm]
    _ = ∑ edge : TruncatedIcosahedralEdge,
          (∑ v : IcosahedralVertex,
            (truncatedIcosahedralPentagonBoundary v).count edge) • w edge := by
              apply Finset.sum_congr rfl
              intro edge _
              rw [Finset.sum_smul]
    _ = ∑ edge : TruncatedIcosahedralEdge,
          kernelC60PentagonEdgeMultiplicity edge • w edge := rfl

/-- UNIVERSAL FULL-C60 32-FACE DOUBLE COUNTING:
for EVERY AddCommMonoid A and arbitrary edge-dependent w, the
total of ALL real pentagon and hexagon edge-occurrence weights
equals twice the weight of each of the ninety physical edges.
This is a source-incidence theorem, not a hypothesis of Gray
coherence or source F55 3-cell pasting. -/
theorem kernelC60FullSurfaceWeightedDoubleCount
    {A : Type*} [AddCommMonoid A]
    (w : TruncatedIcosahedralEdge → A) :
    (∑ face : TruncatedIcosahedralSeedFace,
      ((kernelC60FullFaceBoundaryEdges face).map w).sum) =
        (2 : Nat) • (∑ edge : TruncatedIcosahedralEdge, w edge) := by
  calc
    (∑ face : TruncatedIcosahedralSeedFace,
      ((kernelC60FullFaceBoundaryEdges face).map w).sum) =
        (∑ v : IcosahedralVertex,
          ((truncatedIcosahedralPentagonBoundary v).map w).sum) +
        (∑ f : IcosahedralFace,
          ((kernelC60HexagonBoundaryEdges f).map w).sum) :=
            kernelC60SumOverAllRealFaces _
    _ = (∑ edge : TruncatedIcosahedralEdge,
          kernelC60PentagonEdgeMultiplicity edge • w edge) +
        (∑ edge : TruncatedIcosahedralEdge,
          kernelC60HexagonEdgeMultiplicity edge • w edge) := by
            rw [kernelC60PentagonWeightedDoubleCount w,
              kernelC60HexagonWeightedDoubleCount w]
    _ = ∑ edge : TruncatedIcosahedralEdge, (2 : Nat) • w edge := by
          rw [← Finset.sum_add_distrib]
          apply Finset.sum_congr rfl
          intro edge _
          rw [← add_nsmul,
            kernelC60AllFacesEdgeMultiplicity_sum_eq_two edge]
    _ = (2 : Nat) • (∑ edge : TruncatedIcosahedralEdge, w edge) := by
          rw [Finset.sum_nsmul]

/-- The all-32-face global boundary equation holds inside the
INDEPENDENT NATIVE F59-C Gray 3-cell endomorphism group for any
edge-dependent 3-cell labels, not only uniformly chosen squares. -/
theorem kernelC60FullSurfaceAnyNativeGrayLabels
    (w : TruncatedIcosahedralEdge → GradedThreeCell 0 0) :
    (∑ face : TruncatedIcosahedralSeedFace,
      ((kernelC60FullFaceBoundaryEdges face).map w).sum) =
      (2 : Nat) • (∑ edge : TruncatedIcosahedralEdge, w edge) :=
  kernelC60FullSurfaceWeightedDoubleCount w

/-- ALL 32 original C60 face boundaries have vanishing total
exchange phase, for ANY assignment of independent neutral-grade
F59 Gray 3-cells to the ninety original physical edges. Unlike
the original F59-F2 result this needs no uniformity of labels. -/
theorem kernelC60FullSurfaceAnyGrayPhase_zero
    (w : TruncatedIcosahedralEdge → GradedThreeCell 0 0) :
    (∑ face : TruncatedIcosahedralSeedFace,
      ((kernelC60FullFaceBoundaryEdges face).map w).sum).phase =
      (0 : ZMod 2) := by
  rw [kernelC60FullSurfaceAnyNativeGrayLabels w]
  rw [two_nsmul]
  rw [grayNeutral_add_phase]
  have htwo : (2 : ZMod 2) = 0 := by decide
  calc
    (∑ edge : TruncatedIcosahedralEdge, w edge).phase +
      (∑ edge : TruncatedIcosahedralEdge, w edge).phase =
        (2 : ZMod 2) * (∑ edge : TruncatedIcosahedralEdge, w edge).phase := by
          ring
    _ = 0 := by rw [htwo, zero_mul]

#print axioms kernelC60PentagonEdgeMultiplicity
#print axioms kernelC60PentagonAroundMultiplicity
#print axioms kernelC60PentagonCrossMultiplicity
#print axioms kernelC60AllFacesEdgeMultiplicity_sum_eq_two
#print axioms kernelC60FullFaceEquiv
#print axioms kernelC60FullFaceBoundary_length
#print axioms kernelC60SumOverAllRealFaces
#print axioms kernelC60FullFaceEdgeMultiplicity_two
#print axioms kernelC60FullFaceBoundaryModTwoCoefficient_zero
#print axioms kernelC60FullFaceBoundaryModTwo_zero
#print axioms kernelC60PentagonWeightedDoubleCount
#print axioms kernelC60FullSurfaceWeightedDoubleCount
#print axioms kernelC60FullSurfaceAnyNativeGrayLabels
#print axioms kernelC60FullSurfaceAnyGrayPhase_zero

end
end KUOS.DependentOriginationGrayC60AllThirtyTwoFaceCycleV5_158
