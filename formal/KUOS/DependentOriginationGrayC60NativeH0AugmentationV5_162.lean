import KUOS.DependentOriginationGrayC60NativeH2InfiniteOrderV5_161
import Mathlib.Algebra.Homology.ShortComplex.ModuleCat
import Mathlib.Algebra.Homology.ShortComplex.HomologicalComplex

namespace KUOS.DependentOriginationGrayC60NativeH0AugmentationV5_162

open CategoryTheory Limits
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayC60IntegralBoundaryLinearMapV5_159
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationGrayC60NativeChainComplexV5_160

set_option autoImplicit false
noncomputable section

/-!
# F59-F14 / v5.162 — nonzero native C60 H₀ via integral augmentation

The canonical KuuOS branch proves a genuine Mathlib integer
ChainComplex with 60 physical C60 dart vertices, 90 physical
edges, and 32 original oriented faces (F59-F10/11). F59-F12
established a nonzero native H₂ class, and F59-F13 exhibited a
split infinite-order copy of ℤ in genuine H₂.

Here we study a DIFFERENT native homology degree. Define
augmentation ε: C₀ →ₗ[ℤ] ℤ by summing coefficients of ACTUAL
vertex basis chains. Prove ε(d₁(e))=0 for every one of the
original oriented C60 physical edges, and ε∘d₁=0 as a linear
map for arbitrary edge chains.

A single actual north-pole dart vertex has augmentation +1.
It cannot be any original edge boundary because augmentation
annihilates ALL edge boundaries. Using the native ShortComplex
exactness API, prove the genuine C60 cellular complex is
NOT exact in degree 0. Therefore its actual native Mathlib
homology H₀ is NOT the zero object.

Scope: This is nonvanishing of native H₀ and a nonboundary
vertex witness, NOT a full computation H₀ ≅ ℤ, connectedness
of the 60-vertex graph, or vanishing of native H₁. Neither
the global F55 Gray 3-functor nor the old Stage-II omega is
identified with these integer cellular homology statements.
-/

/-- An actual ℤ-linear augmentation functional on the free
abelian zero chains of sixty REAL C60 dart vertices. -/
def c60IntegralVertexAugmentation :
    C60IntegralZeroChains →ₗ[ℤ] ℤ :=
  Finsupp.linearCombination ℤ (fun _ : IcosahedralDart => (1 : ℤ))

/-- Augmentation sends each original physical vertex
basis generator of arbitrary integer coefficient to precisely
that coefficient. No quotient vertex model is substituted. -/
theorem c60IntegralVertexAugmentation_single
    (v : IcosahedralDart) (z : ℤ) :
    c60IntegralVertexAugmentation (Finsupp.single v z) = z := by
  simp [c60IntegralVertexAugmentation]

/-- The boundary of ANY real original oriented C60 edge has
augmentation ZERO because it is target minus source. -/
theorem c60IntegralVertexAugmentation_edge_zero
    (e : TruncatedIcosahedralEdge) :
    c60IntegralVertexAugmentation
      (c60IntegralEdgeBoundaryChain e) = 0 := by
  simp [c60IntegralEdgeBoundaryChain,
    c60IntegralVertexAugmentation_single]

/-- Crucial true differential identity ε ∘ d₁ = 0 as a
Z-LINEAR MAP, not merely a sum of formal labels.
Every arbitrary integer C60 1-chain has augmentation-zero
boundary because each actual physical basis edge does. -/
theorem c60IntegralVertexAugmentation_comp_boundaryOne_zero :
    c60IntegralVertexAugmentation.comp
      c60IntegralBoundaryOne = 0 := by
  apply Finsupp.lhom_ext
  intro e z
  change c60IntegralVertexAugmentation
    (c60IntegralBoundaryOne (Finsupp.single e z)) = 0
  rw [c60IntegralBoundaryOne_singleEdge, map_smul,
    c60IntegralVertexAugmentation_edge_zero, smul_zero]

/-- Chosen GENUINE source C60 vertex at the north end of its
first original north-spoke edge (one of the true 60 darts). -/
def c60NorthDart : IcosahedralDart :=
  .first (.northSpoke 0)

/-- The actual north dart taken with integer coefficient +1. -/
def c60NorthDartChain : C60IntegralZeroChains :=
  Finsupp.single c60NorthDart (1 : ℤ)

/-- The physical north dart has nonzero augmentation +1. -/
theorem c60NorthDartChain_augmentation_one :
    c60IntegralVertexAugmentation c60NorthDartChain = 1 := by
  exact c60IntegralVertexAugmentation_single _ _

/-- No original C60 signed edge chain can have boundary equal
to this one genuine vertex. This is a NONBOUNDARY statement
over integers, not merely a modulo-two obstruction. -/
theorem c60NorthDartChain_not_in_edge_range :
    c60NorthDartChain ∉ LinearMap.range
      c60IntegralBoundaryOne := by
  rintro ⟨x, hx⟩
  have hzero :
      c60IntegralVertexAugmentation
        (c60IntegralBoundaryOne x) = 0 := by
    have h := congrArg
      (fun L : C60IntegralOneChains →ₗ[ℤ] ℤ => L x)
      c60IntegralVertexAugmentation_comp_boundaryOne_zero
    simpa only [LinearMap.comp_apply, LinearMap.zero_apply] using h
  have hcontr : (1 : ℤ) = 0 := by
    calc
      (1 : ℤ) = c60IntegralVertexAugmentation c60NorthDartChain :=
        c60NorthDartChain_augmentation_one.symm
      _ = c60IntegralVertexAugmentation (c60IntegralBoundaryOne x) :=
        congrArg c60IntegralVertexAugmentation hx.symm
      _ = 0 := hzero
  exact one_ne_zero hcontr

/-- At native homology degree 0, the incoming differential
is exactly the true F59-F10 edge-to-vertex map d₁. -/
theorem c60NativeH0_incoming_eq_d1 :
    (c60NativeIntegralCellularComplex.sc 0).f =
      ModuleCat.ofHom c60IntegralBoundaryOne := by
  change c60NativeIntegralCellularComplex.d
    ((ComplexShape.down ℕ).prev 0) 0 = _
  have hp : (ComplexShape.down ℕ).prev 0 = 1 := by simp
  rw [hp]
  exact c60NativeIntegralCellularComplex_d10

/-- Outgoing differential from C₀ is zero, since its
lower successor degree is 0 and no degree-negative
vertex chains exist in this ℕ-indexed chain complex. -/
theorem c60NativeH0_outgoing_zero :
    (c60NativeIntegralCellularComplex.sc 0).g = 0 := by
  change c60NativeIntegralCellularComplex.d 0
    ((ComplexShape.down ℕ).next 0) = 0
  rw [ChainComplex.next_nat_zero]
  change (ChainComplex.of c60NativeChainObjects
      c60NativeChainDifferential
      c60NativeChainDifferential_comp_zero).d 0 0 = 0
  exact ChainComplex.of_d_ne c60NativeChainObjects
    c60NativeChainDifferential
    c60NativeChainDifferential_comp_zero (by omega)

/-- Real original C60 cellular chains are NOT EXACT in degree
ZERO: the north dart vertex is a true outgoing cycle but cannot
come from any incoming physical edge boundary. -/
theorem c60NativeChainComplex_not_exactAt_zero :
    ¬ c60NativeIntegralCellularComplex.ExactAt 0 := by
  intro hexact
  have hsurj :=
    (ShortComplex.moduleCat_exact_iff
      (c60NativeIntegralCellularComplex.sc 0)).mp hexact
  have hcycle :
      (c60NativeIntegralCellularComplex.sc 0).g
        c60NorthDartChain = 0 := by
    rw [c60NativeH0_outgoing_zero]
    rfl
  obtain ⟨x, hx⟩ := hsurj c60NorthDartChain hcycle
  rw [c60NativeH0_incoming_eq_d1] at hx
  exact c60NorthDartChain_not_in_edge_range ⟨x, hx⟩

/-- The actual NATIVE Mathlib degree-zero homology of the
original integral C60 chain complex is nonzero, and this
follows from a physical coefficient of a genuine dart vertex,
not from a freestanding invented topological assumption. -/
theorem c60NativeH0_not_isZero :
    ¬ IsZero (c60NativeIntegralCellularComplex.homology 0) := by
  intro hzero
  exact c60NativeChainComplex_not_exactAt_zero
    ((c60NativeIntegralCellularComplex.exactAt_iff_isZero_homology 0).mpr hzero)

#print axioms c60IntegralVertexAugmentation
#print axioms c60IntegralVertexAugmentation_single
#print axioms c60IntegralVertexAugmentation_edge_zero
#print axioms c60IntegralVertexAugmentation_comp_boundaryOne_zero
#print axioms c60NorthDartChain
#print axioms c60NorthDartChain_augmentation_one
#print axioms c60NorthDartChain_not_in_edge_range
#print axioms c60NativeH0_incoming_eq_d1
#print axioms c60NativeH0_outgoing_zero
#print axioms c60NativeChainComplex_not_exactAt_zero
#print axioms c60NativeH0_not_isZero

end
end KUOS.DependentOriginationGrayC60NativeH0AugmentationV5_162
