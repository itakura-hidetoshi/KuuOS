import KUOS.DependentOriginationGrayC60NativeH0AugmentationV5_162
import Mathlib.Algebra.Homology.ShortComplex.ModuleCat
import Mathlib.Algebra.Homology.ShortComplex.HomologicalComplex
import Mathlib.LinearAlgebra.Quotient.Basic

namespace KUOS.DependentOriginationGrayC60NativeH0ConnectivityV5_163

open CategoryTheory Limits
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayC60IntegralBoundaryLinearMapV5_159
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationGrayC60NativeChainComplexV5_160
open KUOS.DependentOriginationGrayC60NativeH0AugmentationV5_162

set_option autoImplicit false
noncomputable section

/-!
# F59-F15 / v5.163 — actual C60 connectivity and native H₀ ≅ ℤ

We use exclusively the original 60 darts and 90 oriented C60 edges.
A concrete 59-edge spanning construction consists of four around
edges at each of the twelve five-valent original vertices (48),
the five original north spokes, the five original aligned cross
edges, and one original south spoke (11).

Each integral dart difference [v] - [north] is thereby an actual
boundary of an integer physical 1-chain. Summing these witness
chains extends the augmentation argument of F59-F14 to the exact
identity d₁ P + root ε = id on ALL integer 0-chains.

Hence ker ε = im d₁, and the induced quotient augmentation is an
isomorphism. Via Mathlib's native ChainComplex H₀-to-opcycles
isomorphism and ModuleCat quotient isomorphism, the genuine
native C60 degree-zero homology object is ℤ.

No H₁ vanishing, complete H₂ classification, homeomorphism with S²,
or identification with the independent F55 Gray 3-cell is asserted.
-/

/-- The actual image of the physical integer 90-edge differential. -/
def c60IntegralEdgeRange : Submodule ℤ C60IntegralZeroChains :=
  LinearMap.range c60IntegralBoundaryOne

/-- Integral difference between genuine C60 vertex basis chains. -/
def c60VertexGap (a b : IcosahedralDart) : C60IntegralZeroChains :=
  Finsupp.single b (1 : ℤ) - Finsupp.single a (1 : ℤ)

/-- Every original physical edge joins two vertices modulo d₁-boundaries. -/
theorem c60VertexGap_edge (e : TruncatedIcosahedralEdge) :
    c60VertexGap (truncatedIcosahedralEdgeEndpoints e).1
      (truncatedIcosahedralEdgeEndpoints e).2 ∈ c60IntegralEdgeRange := by
  change c60VertexGap (truncatedIcosahedralEdgeEndpoints e).1
    (truncatedIcosahedralEdgeEndpoints e).2 ∈
      LinearMap.range c60IntegralBoundaryOne
  refine ⟨Finsupp.single e (1 : ℤ), ?_⟩
  simp [c60IntegralBoundaryOne_singleEdge,
    c60IntegralEdgeBoundaryChain, c60VertexGap]

/-- Physical edge-chain differences can be reversed over ℤ. -/
theorem c60VertexGap_symm {a b : IcosahedralDart}
    (h : c60VertexGap a b ∈ c60IntegralEdgeRange) :
    c60VertexGap b a ∈ c60IntegralEdgeRange := by
  have heq : c60VertexGap b a = -(c60VertexGap a b) := by
    unfold c60VertexGap
    abel
  rw [heq]
  exact c60IntegralEdgeRange.neg_mem h

/-- Two real integer edge-chain paths concatenate by adding chains. -/
theorem c60VertexGap_trans {a b c : IcosahedralDart}
    (hab : c60VertexGap a b ∈ c60IntegralEdgeRange)
    (hbc : c60VertexGap b c ∈ c60IntegralEdgeRange) :
    c60VertexGap a c ∈ c60IntegralEdgeRange := by
  have heq :
      c60VertexGap a c = c60VertexGap a b + c60VertexGap b c := by
    unfold c60VertexGap
    abel
  rw [heq]
  exact c60IntegralEdgeRange.add_mem hab hbc

/-- The next consecutive physical around-edge of a pentagon. -/
theorem c60AroundStep (v : IcosahedralVertex) (s : PentagonalSlot) :
    c60VertexGap (icosahedralIncidentDartAt v s)
        (icosahedralIncidentDartAt v (pentagonalSlotNext s)) ∈
      c60IntegralEdgeRange :=
  c60VertexGap_edge (.around ⟨v, s⟩)

/-- Four true around-edges suffice to join the base dart to each
of the five darts of ANY actual pentagonal face. -/
theorem c60AroundConnected (v : IcosahedralVertex) :
    ∀ s : PentagonalSlot,
      c60VertexGap (icosahedralIncidentDartAt v .s0)
        (icosahedralIncidentDartAt v s) ∈ c60IntegralEdgeRange := by
  intro s
  cases s with
  | s0 =>
      simp [c60VertexGap]
  | s1 =>
      exact c60AroundStep v .s0
  | s2 =>
      exact c60VertexGap_trans (c60AroundStep v .s0)
        (c60AroundStep v .s1)
  | s3 =>
      exact c60VertexGap_trans
        (c60VertexGap_trans (c60AroundStep v .s0)
          (c60AroundStep v .s1))
        (c60AroundStep v .s2)
  | s4 =>
      exact c60VertexGap_trans
        (c60VertexGap_trans
          (c60VertexGap_trans (c60AroundStep v .s0)
            (c60AroundStep v .s1))
          (c60AroundStep v .s2))
        (c60AroundStep v .s3)

/-- Actual slot-zero dart over an original icosahedral vertex. -/
def c60BaseDart (v : IcosahedralVertex) : IcosahedralDart :=
  icosahedralIncidentDartAt v .s0

/-- The five cyclic slot indices cover every ZMod 5 element.
Unlike the earlier general slot equivalence this proof is kernel-checked
by finite `decide` and does not use a native-decide axiom. -/
theorem c60NorthIndexHasSlot :
    ∀ i : IcosahedralRingIndex,
      ∃ s : PentagonalSlot, pentagonalSlotIndex s = i := by
  decide

/-- Each of the five north spokes reaches the base dart of
its corresponding upper-ring original vertex. -/
theorem c60RootToUpper (i : IcosahedralRingIndex) :
    c60VertexGap c60NorthDart (c60BaseDart (.upper i)) ∈
      c60IntegralEdgeRange := by
  obtain ⟨s, hs⟩ := c60NorthIndexHasSlot i
  have h₁ : c60VertexGap c60NorthDart (.first (.northSpoke i)) ∈
      c60IntegralEdgeRange := by
    simpa [c60NorthDart, c60BaseDart, icosahedralIncidentDartAt,
      hs] using (c60AroundConnected .north s)
  have h₂ : c60VertexGap (.first (.northSpoke i))
      (c60BaseDart (.upper i)) ∈ c60IntegralEdgeRange :=
    c60VertexGap_edge (.cross (.northSpoke i))
  exact c60VertexGap_trans h₁ h₂

/-- Aligned physical cross edges join each upper-ring pentagon
to its lower-ring counterpart. -/
theorem c60RootToLower (i : IcosahedralRingIndex) :
    c60VertexGap c60NorthDart (c60BaseDart (.lower i)) ∈
      c60IntegralEdgeRange := by
  have h₁ := c60VertexGap_trans (c60RootToUpper i)
    (c60AroundConnected (.upper i) .s2)
  have h₂ : c60VertexGap
      (icosahedralIncidentDartAt (.upper i) .s2)
      (icosahedralIncidentDartAt (.lower i) .s3) ∈
      c60IntegralEdgeRange :=
    c60VertexGap_edge (.cross (.crossAligned i))
  have h₃ := c60VertexGap_symm (c60AroundConnected (.lower i) .s3)
  exact c60VertexGap_trans (c60VertexGap_trans h₁ h₂) h₃

/-- The original south spoke at index zero joins the remaining
south-pole pentagon to the already-connected lower-ring group. -/
theorem c60RootToSouth :
    c60VertexGap c60NorthDart (c60BaseDart .south) ∈
      c60IntegralEdgeRange := by
  exact c60VertexGap_trans (c60RootToLower 0)
    (c60VertexGap_symm
      (c60VertexGap_edge (.cross (.southSpoke 0))))

/-- The twelve actual original icosahedral pentagons are
connected by eleven explicitly identified C60 cross edges. -/
theorem c60RootToEveryPentagon :
    ∀ v : IcosahedralVertex,
      c60VertexGap c60NorthDart (c60BaseDart v) ∈
        c60IntegralEdgeRange := by
  intro v
  cases v with
  | north =>
      simp [c60VertexGap, c60NorthDart, c60BaseDart,
        icosahedralIncidentDartAt, pentagonalSlotIndex]
  | south => exact c60RootToSouth
  | upper i => exact c60RootToUpper i
  | lower i => exact c60RootToLower i

/-- Every one of the original sixty darts really occurs in
one of the sixty incident-slot positions of the twelve
actual original icosahedral vertices. -/
theorem c60EveryDartHasIncidentSlot :
    ∀ d : IcosahedralDart,
      ∃ v : IcosahedralVertex, ∃ s : PentagonalSlot,
        icosahedralIncidentDartAt v s = d := by
  decide

/-- PHYSICAL CONNECTIVITY: each of the original 60 C60 darts
differs from the north dart by the boundary of an actual
integral 90-edge 1-chain; no abstract connectedness axiom. -/
theorem c60RootToEveryDart (d : IcosahedralDart) :
    c60VertexGap c60NorthDart d ∈ c60IntegralEdgeRange := by
  obtain ⟨v, s, hs⟩ := c60EveryDartHasIncidentSlot d
  rw [← hs]
  exact c60VertexGap_trans (c60RootToEveryPentagon v)
    (c60AroundConnected v s)

/-- A chosen integral physical edge-chain path from the original
north dart to each actual C60 vertex. The existence follows
from the 59-edge constructive connectivity certificate. -/
noncomputable def c60VertexPath (d : IcosahedralDart) :
    C60IntegralOneChains :=
  Classical.choose (c60RootToEveryDart d)

/-- The vertex path has EXACT original integer edge boundary. -/
theorem c60VertexPath_boundary (d : IcosahedralDart) :
    c60IntegralBoundaryOne (c60VertexPath d) =
      c60VertexGap c60NorthDart d :=
  Classical.choose_spec (c60RootToEveryDart d)

/-- Extend the physical spanning paths Z-linearly to all 0-chains. -/
noncomputable def c60VertexPathLift :
    C60IntegralZeroChains →ₗ[ℤ] C60IntegralOneChains :=
  Finsupp.linearCombination ℤ c60VertexPath

theorem c60VertexPathLift_single (d : IcosahedralDart) (z : ℤ) :
    c60VertexPathLift (Finsupp.single d z) =
      z • c60VertexPath d := by
  simp [c60VertexPathLift]

/-- Include the original north vertex as a Z-linear root anchor. -/
def c60RootEmbedding : ℤ →ₗ[ℤ] C60IntegralZeroChains :=
  Finsupp.lsingle c60NorthDart

theorem c60RootEmbedding_apply (z : ℤ) :
    c60RootEmbedding z = Finsupp.single c60NorthDart z := by
  simp [c60RootEmbedding]

/-- INTEGER CHAIN HOMOTOPY IDENTITY on all original 0-chains:
d₁·P + [north]·ε = id. -/
theorem c60VertexPathLift_homotopy :
    c60IntegralBoundaryOne.comp c60VertexPathLift +
      c60RootEmbedding.comp c60IntegralVertexAugmentation =
        LinearMap.id := by
  apply Finsupp.lhom_ext
  intro d z
  change c60IntegralBoundaryOne
      (c60VertexPathLift (Finsupp.single d z)) +
    c60RootEmbedding
      (c60IntegralVertexAugmentation (Finsupp.single d z)) =
    Finsupp.single d z
  rw [c60VertexPathLift_single, map_smul, c60VertexPath_boundary,
    c60IntegralVertexAugmentation_single, c60RootEmbedding_apply]
  simp [c60VertexGap, smul_sub]

/-- New F59-F15 result: precisely the augmentation-zero integer
0-chains, and NO others, are physical 90-edge boundaries. -/
theorem c60IntegralVertexAugmentation_kernel_eq_edgeRange :
    LinearMap.ker c60IntegralVertexAugmentation =
      c60IntegralEdgeRange := by
  apply le_antisymm
  · intro c hc
    have hc' : c60IntegralVertexAugmentation c = 0 := hc
    have h := LinearMap.congr_fun c60VertexPathLift_homotopy c
    simp only [LinearMap.add_apply, LinearMap.comp_apply,
      LinearMap.id_apply] at h
    rw [hc', map_zero, add_zero] at h
    exact ⟨c60VertexPathLift c, h⟩
  · intro c hc
    obtain ⟨x, rfl⟩ := hc
    have h := LinearMap.congr_fun
      c60IntegralVertexAugmentation_comp_boundaryOne_zero x
    simpa only [LinearMap.comp_apply, LinearMap.zero_apply] using h

/-- The genuine physical augmentation descends to integer
zero-chains modulo the actual original edge boundary image. -/
def c60AugmentationQuotient :
    (C60IntegralZeroChains ⧸ c60IntegralEdgeRange) →ₗ[ℤ] ℤ :=
  c60IntegralEdgeRange.liftQ c60IntegralVertexAugmentation (by
    rw [c60IntegralVertexAugmentation_kernel_eq_edgeRange])

/-- A geometric north-dart representative of every integer. -/
theorem c60AugmentationQuotient_surjective :
    Function.Surjective c60AugmentationQuotient := by
  intro z
  refine ⟨Submodule.Quotient.mk
    (Finsupp.single c60NorthDart z), ?_⟩
  simpa [c60AugmentationQuotient] using
    (c60IntegralVertexAugmentation_single c60NorthDart z)

/-- No nontrivial class of actual 0-chains has zero augmentation:
the kernel equals the exact original signed edge boundary image. -/
theorem c60AugmentationQuotient_injective :
    Function.Injective c60AugmentationQuotient := by
  intro a b hab
  obtain ⟨x, rfl⟩ := Submodule.Quotient.mk_surjective
    c60IntegralEdgeRange a
  obtain ⟨y, rfl⟩ := Submodule.Quotient.mk_surjective
    c60IntegralEdgeRange b
  apply (Submodule.Quotient.eq c60IntegralEdgeRange).mpr
  have hker : x - y ∈ LinearMap.ker
      c60IntegralVertexAugmentation := by
    change c60IntegralVertexAugmentation (x - y) = 0
    rw [map_sub, sub_eq_zero]
    simpa [c60AugmentationQuotient] using hab
  rw [c60IntegralVertexAugmentation_kernel_eq_edgeRange] at hker
  exact hker

/-- A fully invertible Z-linear quotient-augmentation map,
obtained from original graph connectivity, not an assumed rank. -/
noncomputable def c60IntegralH0QuotientEquivInt :
    (C60IntegralZeroChains ⧸ c60IntegralEdgeRange) ≃ₗ[ℤ] ℤ :=
  LinearEquiv.ofBijective c60AugmentationQuotient
    ⟨c60AugmentationQuotient_injective,
      c60AugmentationQuotient_surjective⟩

/-- Main F59-F15 result in NATIVE Mathlib homology, not an
informal group computed outside the actual chain complex. -/
noncomputable def c60NativeH0IsoInteger :
    c60NativeIntegralCellularComplex.homology 0 ≅
      ModuleCat.of ℤ ℤ := by
  have hRange :
      LinearMap.range
          (c60NativeIntegralCellularComplex.sc 0).f.hom =
        c60IntegralEdgeRange := by
    change LinearMap.range
      (c60NativeIntegralCellularComplex.d
        ((ComplexShape.down ℕ).prev 0) 0).hom =
        c60IntegralEdgeRange
    rw [ChainComplex.prev]
    change LinearMap.range
      (c60NativeIntegralCellularComplex.d 1 0).hom = c60IntegralEdgeRange
    rw [c60NativeIntegralCellularComplex_d10]
    rfl
  have hQuot :
      ModuleCat.of ℤ
        ((c60NativeIntegralCellularComplex.sc 0).X₂ ⧸
          LinearMap.range (c60NativeIntegralCellularComplex.sc 0).f.hom) ≅
        ModuleCat.of ℤ ℤ := by
    change ModuleCat.of ℤ
      (C60IntegralZeroChains ⧸ LinearMap.range
        (c60NativeIntegralCellularComplex.sc 0).f.hom) ≅ ModuleCat.of ℤ ℤ
    rw [hRange]
    exact c60IntegralH0QuotientEquivInt.toModuleIso
  exact c60NativeIntegralCellularComplex.isoHomologyι₀ ≪≫
    (c60NativeIntegralCellularComplex.sc 0).moduleCatOpcyclesIso ≪≫
      hQuot

#print axioms c60VertexGap_edge
#print axioms c60AroundConnected
#print axioms c60RootToEveryPentagon
#print axioms c60EveryDartHasIncidentSlot
#print axioms c60RootToEveryDart
#print axioms c60VertexPathLift_homotopy
#print axioms c60IntegralVertexAugmentation_kernel_eq_edgeRange
#print axioms c60AugmentationQuotient_injective
#print axioms c60IntegralH0QuotientEquivInt
#print axioms c60NativeH0IsoInteger

end
end KUOS.DependentOriginationGrayC60NativeH0ConnectivityV5_163
