import KUOS.DependentOriginationGrayC60IntegralBoundaryLinearMapV5_159

namespace KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralHexagonsV3_86
open KUOS.DependentOriginationTruncatedIcosahedralKernelHexagonCyclesV5_157
open KUOS.DependentOriginationGrayC60IntegerOrientedSurfaceCycleV5_159
open KUOS.DependentOriginationGrayC60IntegralBoundaryLinearMapV5_159

set_option autoImplicit false
noncomputable section

/-!
# F59-F10 / v5.160 — the actual C60 integral cellular chain complex

F59-F8 constructed globally consistent signed orientations for all 32
real pentagon/hexagon faces and a genuinely zero integral surface
boundary one-chain. F59-F9 constructed the genuine Z-linear d₂ from
free face chains C₂ to free 90-edge chains C₁, and a NONZERO integral
fundamental surface cycle in ker d₂.

Here we construct the ACTUAL free abelian zero-chain group on the
60 original C60 dart vertices, and the Z-LINEAR edge boundary d₁.
On each original oriented edge, d₁ assigns endpoint target MINUS
endpoint source. No alternate or merely counted geometry is used.

We use the F59-F8 certified signed FACE BOUNDARY LISTS to establish
that EVERY one of the 32 actual polygonal face 1-chains has zero
vertex boundary. This is checked at every actual dart vertex from
the genuine five/six cyclic edge paths, and generalized to the
formal differential identity d₁ ∘ d₂ = 0 on arbitrary integer
2-chains, as an equality of Z-linear maps.

Consequently im(d₂) is contained in ker(d₁), a genuine integer
three-term CELLULAR CHAIN COMPLEX on original C60 incidence data.

This does not yet calculate H₁, H₂, exact kernel ranks, connectedness
or a topological equivalence to a sphere; and it does not identify
the original independent Gray 3-cell phase with the Stage-II omega.
-/

/-- The cellular zero-chain group on all SIXTY actual C60 vertices,
each represented by one original icosahedral endpoint dart. -/
abbrev C60IntegralZeroChains := IcosahedralDart →₀ ℤ

/-- Original physical directed edge boundary: target MINUS source,
in the genuine integer free abelian zero-chain group. -/
def c60IntegralEdgeBoundaryChain
    (e : TruncatedIcosahedralEdge) : C60IntegralZeroChains :=
  Finsupp.single (truncatedIcosahedralEdgeEndpoints e).2 (1 : ℤ) -
    Finsupp.single (truncatedIcosahedralEdgeEndpoints e).1 (1 : ℤ)

/-- The actual Z-linear cellular edge-to-vertex differential d₁.
Each basis edge receives its certified original source/target
integer zero-chain boundary. -/
def c60IntegralBoundaryOne :
    C60IntegralOneChains →ₗ[ℤ] C60IntegralZeroChains :=
  Finsupp.linearCombination ℤ c60IntegralEdgeBoundaryChain

/-- The genuine linear differential's value on ANY edge basis
element, including its arbitrary signed integer coefficient. -/
theorem c60IntegralBoundaryOne_singleEdge
    (e : TruncatedIcosahedralEdge) (z : ℤ) :
    c60IntegralBoundaryOne (Finsupp.single e z) =
      z • c60IntegralEdgeBoundaryChain e := by
  simp [c60IntegralBoundaryOne]

/-- An independently readable original edge-to-vertex incidence
coefficient: +1 at the target, -1 at the source, 0 elsewhere. -/
def c60IntegralEdgeVertexIncidence
    (e : TruncatedIcosahedralEdge)
    (v : IcosahedralDart) : ℤ :=
  (if (truncatedIcosahedralEdgeEndpoints e).2 = v then 1 else 0) -
    (if (truncatedIcosahedralEdgeEndpoints e).1 = v then 1 else 0)

/-- The integer coefficient at any original vertex in an edge's
one-dimensional boundary is exactly the signed endpoint incidence. -/
theorem c60IntegralEdgeBoundaryChain_apply
    (e : TruncatedIcosahedralEdge) (v : IcosahedralDart) :
    c60IntegralEdgeBoundaryChain e v =
      c60IntegralEdgeVertexIncidence e v := by
  simp [c60IntegralEdgeBoundaryChain,
    c60IntegralEdgeVertexIncidence, Finsupp.single_apply, eq_comm]

/-- Algebraic list identity independent of C60: accumulating the
integer coefficient of one fixed physical edge in a list of signed
edge generators equals evaluating the genuine Finsupp one-chain. -/
theorem c60SignedEdgeList_chain_apply
    (l : List (TruncatedIcosahedralEdge × ℤ))
    (e : TruncatedIcosahedralEdge) :
    ((l.map (fun p => (Finsupp.single p.1 p.2 : C60IntegralOneChains))).sum) e =
      (l.map (fun p => if p.1 = e then p.2 else (0 : ℤ))).sum := by
  induction l with
  | nil => simp
  | cons p ps ih =>
      simp [List.sum_cons, Finsupp.single_apply, ih, eq_comm]

/-- The F59-F8 integer boundary of EVERY actual pentagonal and
hexagonal face is precisely the sum of its genuine SIGNED edge
basis vectors, in its original physical cyclic order. -/
theorem c60IntegerFaceBoundaryChain_asSignedList
    (f : TruncatedIcosahedralSeedFace) :
    c60IntegerFaceBoundaryChain f =
      ((c60IntegerOrientedFaceBoundary f).map
        (fun p => (Finsupp.single p.1 p.2 : C60IntegralOneChains))).sum := by
  apply Finsupp.ext
  intro e
  change
    ((c60IntegerOrientedFaceBoundary f).map
      (fun p => if p.1 = e then p.2 else (0 : ℤ))).sum =
    ((c60IntegerOrientedFaceBoundary f).map
      (fun p => (Finsupp.single p.1 p.2 : C60IntegralOneChains))).sum e
  exact (c60SignedEdgeList_chain_apply _ e).symm

/-- By the actual Z-linearity of d₁, applying the differential to
a list of signed edge basis generators is exactly the list of
the corresponding signed endpoint differences. -/
theorem c60IntegralBoundaryOne_signedEdgeList
    (l : List (TruncatedIcosahedralEdge × ℤ)) :
    c60IntegralBoundaryOne
        ((l.map (fun p => (Finsupp.single p.1 p.2 : C60IntegralOneChains))).sum) =
      (l.map (fun p => p.2 • c60IntegralEdgeBoundaryChain p.1)).sum := by
  induction l with
  | nil => simp
  | cons p ps ih =>
      simp only [List.map_cons, List.sum_cons]
      rw [map_add, c60IntegralBoundaryOne_singleEdge, ih]

/-- The vertex coefficient of a signed-edge list's actual linear
boundary, obtained without silently replacing a source path by
its integer generator-charge sum. -/
theorem c60IntegralBoundaryOne_signedEdgeList_apply
    (l : List (TruncatedIcosahedralEdge × ℤ))
    (v : IcosahedralDart) :
    (c60IntegralBoundaryOne
      ((l.map (fun p =>
        (Finsupp.single p.1 p.2 : C60IntegralOneChains))).sum)) v =
      (l.map (fun p => p.2 * c60IntegralEdgeVertexIncidence p.1 v)).sum := by
  rw [c60IntegralBoundaryOne_signedEdgeList]
  induction l with
  | nil => simp
  | cons p ps ih =>
      simp only [List.map_cons, List.sum_cons, Finsupp.add_apply]
      rw [ih]
      simp [c60IntegralEdgeBoundaryChain_apply]

/-- STRONG LOCAL CYCLIC INTEGRAL FACE CONDITION.
Every one of the 32 genuine pentagonal or hexagonal boundary
edge lists has zero signed endpoint divergence at every one of
the 60 original C60 dart vertices.
The finite proof checks the TRUE original face orientation signs
and the NEW kernel-clean F59-F3 cyclic hexagon witnesses. -/
theorem c60IntegralEveryFaceVertexBoundary_zero :
    ∀ f : TruncatedIcosahedralSeedFace, ∀ v : IcosahedralDart,
      ((c60IntegerOrientedFaceBoundary f).map
        (fun p => p.2 * c60IntegralEdgeVertexIncidence p.1 v)).sum =
        (0 : ℤ) := by
  decide

/-- Each of the original 32 polygonal C60 face generators has
an integer one-chain boundary whose own vertex boundary is
ZERO under the actual Z-LINEAR d₁. This is stronger than the
single global all-face cancellation established in F59-F8/F9. -/
theorem c60IntegralBoundaryOne_eachOrientedFace_zero
    (f : TruncatedIcosahedralSeedFace) :
    c60IntegralBoundaryOne (c60IntegerFaceBoundaryChain f) = 0 := by
  apply Finsupp.ext
  intro v
  rw [Finsupp.zero_apply,
    c60IntegerFaceBoundaryChain_asSignedList,
    c60IntegralBoundaryOne_signedEdgeList_apply]
  exact c60IntegralEveryFaceVertexBoundary_zero f v

/-- ACTUAL integer cellular differential identity d₁∘d₂=0,
for the 60-vertex, 90-edge, 32-face C60 free abelian chain
groups, not merely for the single global fundamental cycle. -/
theorem c60IntegralBoundaryOne_comp_boundaryTwo_zero :
    c60IntegralBoundaryOne.comp c60IntegralBoundaryTwo = 0 := by
  apply Finsupp.lhom_ext
  intro f z
  change c60IntegralBoundaryOne
    (c60IntegralBoundaryTwo (Finsupp.single f z)) = 0
  calc
    c60IntegralBoundaryOne (c60IntegralBoundaryTwo (Finsupp.single f z)) =
      c60IntegralBoundaryOne (z • c60IntegerFaceBoundaryChain f) := by
        simp [c60IntegralBoundaryTwo]
    _ = z • c60IntegralBoundaryOne (c60IntegerFaceBoundaryChain f) := by
      rw [map_smul]
    _ = 0 := by
      rw [c60IntegralBoundaryOne_eachOrientedFace_zero, smul_zero]

/-- The square of the C60 cellular integer differential is zero
ON EVERY integer two-chain, not only on the 32 original generators. -/
theorem c60IntegralBoundaryOne_boundaryTwo_apply_zero
    (c : C60IntegralTwoChains) :
    c60IntegralBoundaryOne (c60IntegralBoundaryTwo c) = 0 := by
  have h := congrArg
    (fun L : C60IntegralTwoChains →ₗ[ℤ] C60IntegralZeroChains => L c)
    c60IntegralBoundaryOne_comp_boundaryTwo_zero
  exact h

/-- For the actual C60 integral chain complex,
the image of its 32-to-90 boundary map lies INSIDE the kernel
of its 90-to-60 boundary map, as a bona fide submodule inclusion. -/
theorem c60IntegralBoundaryTwo_range_le_boundaryOne_kernel :
    LinearMap.range c60IntegralBoundaryTwo ≤
      LinearMap.ker c60IntegralBoundaryOne := by
  intro x hx
  obtain ⟨c, rfl⟩ := hx
  change c60IntegralBoundaryOne (c60IntegralBoundaryTwo c) = 0
  exact c60IntegralBoundaryOne_boundaryTwo_apply_zero c

#print axioms c60IntegralEdgeBoundaryChain
#print axioms c60IntegralBoundaryOne
#print axioms c60IntegralBoundaryOne_singleEdge
#print axioms c60IntegralEdgeBoundaryChain_apply
#print axioms c60SignedEdgeList_chain_apply
#print axioms c60IntegerFaceBoundaryChain_asSignedList
#print axioms c60IntegralBoundaryOne_signedEdgeList
#print axioms c60IntegralBoundaryOne_signedEdgeList_apply
#print axioms c60IntegralEveryFaceVertexBoundary_zero
#print axioms c60IntegralBoundaryOne_eachOrientedFace_zero
#print axioms c60IntegralBoundaryOne_comp_boundaryTwo_zero
#print axioms c60IntegralBoundaryOne_boundaryTwo_apply_zero
#print axioms c60IntegralBoundaryTwo_range_le_boundaryOne_kernel

end
end KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
