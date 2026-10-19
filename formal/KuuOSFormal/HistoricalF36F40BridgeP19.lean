import KuuOSFormal.HistoricalF36F40BridgeP18
import KUOS.DependentOriginationGrayC60NativeH2FundamentalClassV5_161
import KUOS.DependentOriginationGrayC60NativeH2InfiniteOrderV5_161

/-!
# F112-P19 — genuine signed fundamental cycle transport on categorical H₂

This historical-comparison-only module proves the *homology-level*
orientation sign using the actual independent 32-polygon P11 cycle,
the actual original F59 fundamental cycle, and naturality of mathlib H₂.
The independent cycle is constructed directly through the native
ShortComplex.moduleCatCyclesIso, avoiding an unjustified identification
between the two different kernel presentations in P17.

The P17 class constructed from the separately converted kernel iso is
NOT identified with this direct representative without a further Lean
equality theorem. That is a separately exposed presentation-compatibility
obligation; no new axiom, sorry, arbitrary sign, or Gray lift is used.
-/

namespace KUOS.F112ActualHistoricalF36F40BridgeP4
namespace GenuineOriginalC60Geometry

open CategoryTheory Limits
open KUOS.DependentOriginationGrayC60IntegralBoundaryLinearMapV5_159
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationGrayC60NativeChainComplexV5_160
open KUOS.DependentOriginationGrayC60NativeH2FundamentalClassV5_161
open KUOS.DependentOriginationGrayC60NativeH2InfiniteOrderV5_161

set_option autoImplicit false
set_option warningAsError true
noncomputable section

/-- The exact P11 surface is a cycle in the *real* independent
Mathlib short complex, not only in the unbundled native d₂ kernel. -/
theorem p19IndependentFundamental_mem_cycles :
    nativeP11FundamentalTwoChain ∈ LinearMap.ker
      (independentC60IntegralCellularComplex.sc 2).g.hom := by
  change (independentC60IntegralCellularComplex.d 2
    ((ComplexShape.down ℕ).next 2)).hom
      nativeP11FundamentalTwoChain = 0
  have hn : (ComplexShape.down ℕ).next 2 = 1 := by simp
  rw [hn, independentC60IntegralCellularComplex_d21]
  exact nativeC60IntegralBoundaryTwo_fundamental_zero

/-- Genuine independent-polygon fundamental cycle, constructed
through the original ShortComplex cycles API and a verified
signed native two-chain representative. -/
def p19IndependentFundamentalCycle :
    independentC60IntegralCellularComplex.cycles 2 :=
  (independentC60IntegralCellularComplex.sc 2).moduleCatCyclesIso.inv
    (⟨nativeP11FundamentalTwoChain,
      p19IndependentFundamental_mem_cycles⟩ :
        LinearMap.ker
          (independentC60IntegralCellularComplex.sc 2).g.hom)

/-- Its image under the genuine cycles inclusion is exactly
the independently oriented P11 fundamental two-chain. -/
theorem p19IndependentFundamentalCycle_iCycles :
    (independentC60IntegralCellularComplex.iCycles 2)
      p19IndependentFundamentalCycle = nativeP11FundamentalTwoChain := by
  change (independentC60IntegralCellularComplex.sc 2).iCycles
    p19IndependentFundamentalCycle = nativeP11FundamentalTwoChain
  rw [← (independentC60IntegralCellularComplex.sc 2).moduleCatCyclesIso_hom_i]
  change
    ((independentC60IntegralCellularComplex.sc 2).moduleCatCyclesIso.hom.hom
      ((independentC60IntegralCellularComplex.sc 2).moduleCatCyclesIso.inv
        (⟨nativeP11FundamentalTwoChain,
          p19IndependentFundamental_mem_cycles⟩ :
          LinearMap.ker
            (independentC60IntegralCellularComplex.sc 2).g.hom))).val =
        nativeP11FundamentalTwoChain
  exact congrArg Subtype.val
    ((independentC60IntegralCellularComplex.sc 2).moduleCatCyclesIso.inv_hom_id_apply _)

/-- The preserved historical F59 canonical cycle likewise
includes as the genuine full signed historical surface. -/
theorem p19HistoricalFundamentalCycle_iCycles :
    (c60NativeIntegralCellularComplex.iCycles 2)
      c60NativeH2FundamentalCycle = c60IntegralFundamentalSurfaceChain := by
  change (c60NativeIntegralCellularComplex.sc 2).iCycles
    c60NativeH2FundamentalCycle = c60IntegralFundamentalSurfaceChain
  rw [← (c60NativeIntegralCellularComplex.sc 2).moduleCatCyclesIso_hom_i]
  change
    ((c60NativeIntegralCellularComplex.sc 2).moduleCatCyclesIso.hom.hom
      ((c60NativeIntegralCellularComplex.sc 2).moduleCatCyclesIso.inv
        (⟨c60IntegralFundamentalSurfaceChain,
          c60NativeH2_fundamental_mem_native_cycles⟩ :
          LinearMap.ker
            (c60NativeIntegralCellularComplex.sc 2).g.hom))).val =
        c60IntegralFundamentalSurfaceChain
  exact congrArg Subtype.val
    ((c60NativeIntegralCellularComplex.sc 2).moduleCatCyclesIso.inv_hom_id_apply _)

/-- The categorical cycles map carries the direct P11 fundamental
cycle to the negative of the preserved historical fundamental cycle. -/
theorem p19IndependentHistoricalCyclesMap_sign :
    (HomologicalComplex.cyclesMap independentHistoricalC60ChainIso.hom 2)
      p19IndependentFundamentalCycle = -c60NativeH2FundamentalCycle := by
  apply (ModuleCat.mono_iff_injective
    (c60NativeIntegralCellularComplex.iCycles 2)).mp inferInstance
  have hnat := congrArg
    (fun f : independentC60IntegralCellularComplex.cycles 2 ⟶
        c60NativeIntegralCellularComplex.X 2 =>
      f p19IndependentFundamentalCycle)
    (HomologicalComplex.cyclesMap_i independentHistoricalC60ChainIso.hom 2)
  simp only [ModuleCat.comp_apply] at hnat
  calc
    (c60NativeIntegralCellularComplex.iCycles 2)
        ((HomologicalComplex.cyclesMap independentHistoricalC60ChainIso.hom 2)
          p19IndependentFundamentalCycle) =
      (independentHistoricalC60ChainIso.hom.f 2)
        ((independentC60IntegralCellularComplex.iCycles 2)
          p19IndependentFundamentalCycle) := hnat
    _ = -c60IntegralFundamentalSurfaceChain := by
      rw [p19IndependentFundamentalCycle_iCycles]
      exact independentHistoricalC60ChainIso_fundamental_sign
    _ = (c60NativeIntegralCellularComplex.iCycles 2)
        (-c60NativeH2FundamentalCycle) := by
      rw [map_neg, p19HistoricalFundamentalCycle_iCycles]

/-- The direct fundamental class in the actual independent
categorical H₂ object (zero incoming degree-three differential). -/
def p19IndependentFundamentalClass :
    independentC60IntegralCellularComplex.homology 2 :=
  (independentC60IntegralCellularComplex.homologyπ 2)
    p19IndependentFundamentalCycle

/-- Functorial orientation sign for the directly constructed
independent class and the ORIGINAL preserved F59 fundamental H₂ class. -/
theorem p19IndependentHistoricalH2_sign :
    independentHistoricalC60H2Iso.hom.hom p19IndependentFundamentalClass =
      -c60NativeH2FundamentalClass := by
  have hnat := congrArg
    (fun f : independentC60IntegralCellularComplex.cycles 2 ⟶
        c60NativeIntegralCellularComplex.homology 2 =>
      f p19IndependentFundamentalCycle)
    independentHistoricalC60H2_homologyπ_naturality
  simp only [ModuleCat.comp_apply] at hnat
  change (independentHistoricalC60H2Iso.hom)
    ((independentC60IntegralCellularComplex.homologyπ 2)
      p19IndependentFundamentalCycle) = _
  calc
    independentHistoricalC60H2Iso.hom
        ((independentC60IntegralCellularComplex.homologyπ 2)
          p19IndependentFundamentalCycle) =
      (c60NativeIntegralCellularComplex.homologyπ 2)
        ((HomologicalComplex.cyclesMap independentHistoricalC60ChainIso.hom 2)
          p19IndependentFundamentalCycle) := hnat
    _ = (c60NativeIntegralCellularComplex.homologyπ 2)
        (-c60NativeH2FundamentalCycle) := by
      rw [p19IndependentHistoricalCyclesMap_sign]
    _ = -c60NativeH2FundamentalClass := by
      rw [map_neg]
      rfl

#print axioms p19IndependentFundamental_mem_cycles
#print axioms p19IndependentFundamentalCycle
#print axioms p19IndependentFundamentalCycle_iCycles
#print axioms p19HistoricalFundamentalCycle_iCycles
#print axioms p19IndependentHistoricalCyclesMap_sign
#print axioms p19IndependentFundamentalClass
#print axioms p19IndependentHistoricalH2_sign

end
end GenuineOriginalC60Geometry
end KUOS.F112ActualHistoricalF36F40BridgeP4
