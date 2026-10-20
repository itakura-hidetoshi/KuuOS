import KuuOSFormal.HistoricalF36F40BridgeP23
import KUOS.DependentOriginationGrayC60NativeH1ContractingHomotopyV5_164

/-!
# F112-P24 — integral chain contraction and H₀/H₁ of fully native C60

P23 replaced ALL three low-degree carriers with the genuine independently
constructed Kuu physical Dart, Edge and Polygon types, and proved commuting
degreewise integral comparison isomorphisms with the original F59 complex.

The original F59-F16 primal-path and dual-face-filling operators satisfy
the verified 90-edge integer contracting identity d₂ Q + P d₁ = id.
We transport these actual operators back along the P23 physical
constructor-level equivalences (and P15 signed native polygon equivalence).
The result is a contracting identity ON THE FULLY NATIVE 90-EDGE MODULE,
not just an abstract invariance claim about first-homology dimensions.

Hence the fully native integer C60 complex is exact at degree one;
its actual categorical H₁ vanishes, and its actual categorical H₀ is ℤ.
The genuinely nonzero H₂ from P23 is preserved. This supplies the native
low-dimensional homology profile, without creating 3-cells, reconstructing
proof-relevant F47/F55 source 3-Homs, or discharging F68/F77 obstructions.
-/

namespace KUOS.F112ActualHistoricalF36F40BridgeP4
namespace GenuineOriginalC60Geometry

open CategoryTheory Limits
open Kuu.F112.Physical
open KUOS.DependentOriginationGrayC60IntegralBoundaryLinearMapV5_159
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationGrayC60NativeChainComplexV5_160
open KUOS.DependentOriginationGrayC60NativeH0AugmentationV5_162
open KUOS.DependentOriginationGrayC60NativeH0ConnectivityV5_163
open KUOS.DependentOriginationGrayC60NativeH1ContractingHomotopyV5_164

set_option autoImplicit false
set_option warningAsError true
noncomputable section

/-- The native augmentation is the genuine coefficient sum over sixty
native Kuu darts, identified constructor-wise with original C60 darts. -/
def p24NativeVertexAugmentation :
    p23NativeZeroChains →ₗ[ℤ] ℤ :=
  c60IntegralVertexAugmentation.comp
    p23NativeZeroToHistorical.toLinearMap

theorem p24NativeVertexAugmentation_single
    (d : Dart) (z : ℤ) :
    p24NativeVertexAugmentation (Finsupp.single d z) = z := by
  change c60IntegralVertexAugmentation
      (p23NativeZeroToHistorical (Finsupp.single d z)) = z
  rw [Finsupp.domLCongr_single, c60IntegralVertexAugmentation_single]

/-- Transport the original primal-tree edge path into a genuine
native edge chain, for EVERY native dart zero-chain. -/
def p24NativePrimalPathLift :
    p23NativeZeroChains →ₗ[ℤ] p23NativeOneChains :=
  p23NativeOneToHistorical.symm.toLinearMap.comp
    (c60F16PrimalPathLift.comp p23NativeZeroToHistorical.toLinearMap)

/-- Transport the original integral dual-face filling back into the
actual 32-polygon Kuu face carrier, including the proved P15 signs. -/
def p24NativeFaceFillLift :
    p23NativeOneChains →ₗ[ℤ] NativeC60IntegralTwoChains :=
  nativeP11OriginalFaceChainLinearEquiv.symm.toLinearMap.comp
    (c60F16FaceFillLift.comp p23NativeOneToHistorical.toLinearMap)

/-- P23 boundary square in the form needed by the primal-path term. -/
theorem p24NativeBoundaryOne_transport (x : p23NativeOneChains) :
    p23NativeZeroToHistorical (p23NativeBoundaryOne x) =
      c60IntegralBoundaryOne (p23NativeOneToHistorical x) := by
  have h := LinearMap.congr_fun p23NativeBoundaryOne_commutes x
  simpa only [LinearMap.comp_apply] using h

/-- Augmentation annihilates the actual native edge-to-dart boundary
on every integer edge chain. -/
theorem p24NativeVertexAugmentation_comp_boundaryOne_zero :
    p24NativeVertexAugmentation.comp p23NativeBoundaryOne = 0 := by
  apply LinearMap.ext
  intro x
  change c60IntegralVertexAugmentation
      (p23NativeZeroToHistorical (p23NativeBoundaryOne x)) = 0
  rw [p24NativeBoundaryOne_transport]
  have h := LinearMap.congr_fun
    c60IntegralVertexAugmentation_comp_boundaryOne_zero
    (p23NativeOneToHistorical x)
  simpa only [LinearMap.comp_apply, LinearMap.zero_apply] using h

/-- P23 followed by P14 sends an independently defined native polygon
boundary precisely to its orientation-corrected historical boundary. -/
theorem p24NativeBoundaryTwo_transport (x : NativeC60IntegralTwoChains) :
    p23NativeOneToHistorical (p23NativeBoundaryTwo x) =
      c60IntegralBoundaryTwo (nativeP11ToOriginalFaceChain x) := by
  calc
    p23NativeOneToHistorical (p23NativeBoundaryTwo x) =
        nativeC60IntegralBoundaryTwo x := by
          have h := LinearMap.congr_fun p23NativeBoundaryTwo_commutes x
          simpa only [LinearMap.comp_apply] using h
    _ = c60IntegralBoundaryTwo (nativeP11ToOriginalFaceChain x) := by
          have h := LinearMap.congr_fun nativeC60IntegralBoundaryTwo_commutes x
          simpa only [LinearMap.comp_apply] using h

/-- Primal path lift is compatible with the physical edge Equiv,
including arbitrary signed integer chains. -/
theorem p24NativePrimalPathLift_transport (x : p23NativeZeroChains) :
    p23NativeOneToHistorical (p24NativePrimalPathLift x) =
      c60F16PrimalPathLift (p23NativeZeroToHistorical x) := by
  change p23NativeOneToHistorical
    (p23NativeOneToHistorical.symm
      (c60F16PrimalPathLift (p23NativeZeroToHistorical x))) =
        c60F16PrimalPathLift (p23NativeZeroToHistorical x)
  exact p23NativeOneToHistorical.apply_symm_apply _

/-- P15 reverse map sends the signed native filling to the exact
historical original filling, for arbitrary integer one-chains. -/
theorem p24NativeFaceFillLift_transport (x : p23NativeOneChains) :
    nativeP11ToOriginalFaceChain (p24NativeFaceFillLift x) =
      c60F16FaceFillLift (p23NativeOneToHistorical x) := by
  change nativeP11OriginalFaceChainLinearEquiv
    (nativeP11OriginalFaceChainLinearEquiv.symm
      (c60F16FaceFillLift (p23NativeOneToHistorical x))) =
        c60F16FaceFillLift (p23NativeOneToHistorical x)
  exact nativeP11OriginalFaceChainLinearEquiv.apply_symm_apply _

/-- F112-P24 central theorem: an actual Z-linear CHAIN CONTRACTION
d₂ᴺ Qᴺ + Pᴺ d₁ᴺ = id on all 90 genuine native physical edge generators
and thus every integral one-chain. All maps have native Kuu carriers. -/
theorem p24NativeOneContractingIdentity :
    p23NativeBoundaryTwo.comp p24NativeFaceFillLift +
      p24NativePrimalPathLift.comp p23NativeBoundaryOne =
        LinearMap.id := by
  apply LinearMap.ext
  intro x
  apply p23NativeOneToHistorical.injective
  change p23NativeOneToHistorical
      (p23NativeBoundaryTwo (p24NativeFaceFillLift x) +
        p24NativePrimalPathLift (p23NativeBoundaryOne x)) =
    p23NativeOneToHistorical x
  rw [map_add, p24NativeBoundaryTwo_transport,
    p24NativeFaceFillLift_transport, p24NativePrimalPathLift_transport,
    p24NativeBoundaryOne_transport]
  have h := LinearMap.congr_fun c60F16ContractingIdentity
    (p23NativeOneToHistorical x)
  simpa only [LinearMap.add_apply, LinearMap.comp_apply,
    LinearMap.id_apply] using h

/-- Actual native closed integral one-chains are native boundaries,
with an explicit filler Qᴺ supplied by the previous contraction. -/
theorem p24NativeOneCycle_explicit_fill
    (x : p23NativeOneChains)
    (hx : x ∈ LinearMap.ker p23NativeBoundaryOne) :
    p23NativeBoundaryTwo (p24NativeFaceFillLift x) = x := by
  have h := LinearMap.congr_fun p24NativeOneContractingIdentity x
  have hz : p23NativeBoundaryOne x = 0 := hx
  simp only [LinearMap.add_apply, LinearMap.comp_apply,
    LinearMap.id_apply] at h
  rw [hz, map_zero, add_zero] at h
  exact h

/-- Every native one-cycle is in the range of the actual
native polygon boundary, not a numerical 90×32 proxy. -/
theorem p24NativeBoundaryOne_kernel_le_boundaryTwo_range :
    LinearMap.ker p23NativeBoundaryOne ≤
      LinearMap.range p23NativeBoundaryTwo := by
  intro x hx
  exact ⟨p24NativeFaceFillLift x, p24NativeOneCycle_explicit_fill x hx⟩

/-- The genuine native d₁∘d₂ = 0 gives the reverse inclusion. -/
theorem p24NativeBoundaryTwo_range_le_boundaryOne_kernel :
    LinearMap.range p23NativeBoundaryTwo ≤
      LinearMap.ker p23NativeBoundaryOne := by
  intro x hx
  rcases hx with ⟨c, rfl⟩
  change p23NativeBoundaryOne (p23NativeBoundaryTwo c) = 0
  have h := LinearMap.congr_fun p23NativeBoundaryOne_comp_boundaryTwo_zero c
  simpa only [LinearMap.comp_apply, LinearMap.zero_apply] using h

/-- Independent native physical C60 integer cellular chain complex
is EXACT in degree one: every one-cycle is filled by true polygons. -/
theorem p24NativeBoundaryTwo_range_eq_boundaryOne_kernel :
    LinearMap.range p23NativeBoundaryTwo =
      LinearMap.ker p23NativeBoundaryOne := by
  exact le_antisymm
    p24NativeBoundaryTwo_range_le_boundaryOne_kernel
    p24NativeBoundaryOne_kernel_le_boundaryTwo_range

/-- Expose degree two's genuine native integer boundary in Mathlib. -/
theorem p24FullyNativeIntegralCellularComplex_d21 :
    p23FullyNativeIntegralCellularComplex.d 2 1 =
      ModuleCat.ofHom p23NativeBoundaryTwo := by
  exact ChainComplex.of_d p23FullyNativeChainObjects
    p23FullyNativeChainDifferential
    p23FullyNativeDifferential_comp_zero 1

/-- Expose the actual native edge-to-dart boundary in Mathlib. -/
theorem p24FullyNativeIntegralCellularComplex_d10 :
    p23FullyNativeIntegralCellularComplex.d 1 0 =
      ModuleCat.ofHom p23NativeBoundaryOne := by
  exact ChainComplex.of_d p23FullyNativeChainObjects
    p23FullyNativeChainDifferential
    p23FullyNativeDifferential_comp_zero 0

/-- Category-theoretic exactness at degree one of the fully
independent native C60 integer cellular chain complex. -/
theorem p24FullyNativeChainComplex_exactAt_one :
    p23FullyNativeIntegralCellularComplex.ExactAt 1 := by
  apply (p23FullyNativeIntegralCellularComplex.exactAt_iff'
    (i := 2) (j := 1) (k := 0) (by simp) (by simp)).mpr
  apply (ShortComplex.moduleCat_exact_iff_range_eq_ker
    (p23FullyNativeIntegralCellularComplex.sc' 2 1 0)).mpr
  change LinearMap.range (p23FullyNativeIntegralCellularComplex.d 2 1).hom =
    LinearMap.ker (p23FullyNativeIntegralCellularComplex.d 1 0).hom
  rw [p24FullyNativeIntegralCellularComplex_d21,
    p24FullyNativeIntegralCellularComplex_d10]
  exact p24NativeBoundaryTwo_range_eq_boundaryOne_kernel

/-- F112-P24: actual categorical first homology vanishes for the
three-degree FULLY NATIVE Kuu physical C60 chain complex. -/
theorem p24FullyNativeH1_isZero :
    IsZero (p23FullyNativeIntegralCellularComplex.homology 1) :=
  (p23FullyNativeIntegralCellularComplex.exactAt_iff_isZero_homology 1).mp
    p24FullyNativeChainComplex_exactAt_one

/-- F112-P24: independently typed degree-zero homology is ℤ,
using the original verified graph connectivity transported along the
genuine chain isomorphism, never merely counting sixty vertices. -/
def p24FullyNativeH0IsoInteger :
    p23FullyNativeIntegralCellularComplex.homology 0 ≅
      ModuleCat.of ℤ ℤ :=
  (HomologicalComplex.homologyMapIso
    p23FullyNativeHistoricalChainIso 0) ≪≫ c60NativeH0IsoInteger

/-- The degree-zero isomorphism is induced by the actual original
historical comparison followed by the certified F59 augmentation. -/
theorem p24FullyNativeH0IsoInteger_hom :
    p24FullyNativeH0IsoInteger.hom =
      (HomologicalComplex.homologyMap
        p23FullyNativeHistoricalChainIso.hom 0) ≫
          c60NativeH0IsoInteger.hom := by
  rfl

#print axioms p24NativeVertexAugmentation_single
#print axioms p24NativeVertexAugmentation_comp_boundaryOne_zero
#print axioms p24NativePrimalPathLift_transport
#print axioms p24NativeFaceFillLift_transport
#print axioms p24NativeOneContractingIdentity
#print axioms p24NativeOneCycle_explicit_fill
#print axioms p24NativeBoundaryTwo_range_eq_boundaryOne_kernel
#print axioms p24FullyNativeChainComplex_exactAt_one
#print axioms p24FullyNativeH1_isZero
#print axioms p24FullyNativeH0IsoInteger
#print axioms p24FullyNativeH0IsoInteger_hom

end
end GenuineOriginalC60Geometry
end KUOS.F112ActualHistoricalF36F40BridgeP4
