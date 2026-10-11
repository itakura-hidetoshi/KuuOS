import KUOS.DependentOriginationGrayC60NativeH2FundamentalClassV5_161
import Mathlib.LinearAlgebra.Finsupp.Defs
import Mathlib.LinearAlgebra.Module.Torsion

namespace KUOS.DependentOriginationGrayC60NativeH2InfiniteOrderV5_161

open CategoryTheory Limits
open KUOS.DependentOriginationGrayC60IntegralBoundaryLinearMapV5_159
open KUOS.DependentOriginationGrayC60NativeChainComplexV5_160
open KUOS.DependentOriginationGrayC60NativeH2FundamentalClassV5_161
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84

set_option autoImplicit false
noncomputable section

/-!
# F59-F13 / v5.161 — primitive native C60 H2 fundamental class

F59-F12 established a REAL nonzero element in the native Mathlib H₂
of the verified original C60 integral cellular chain complex, using
its global signed sum of all 32 physically incident pentagonal and
hexagonal faces. F59-F11 also established that the genuine incoming
degree-three differential d₃ is ZERO, so native H₂ is canonically
isomorphic to the concrete kernel of d₂ on the original 32-face
free integer chain group.

This file proves the stronger INTEGRAL statement:
  (1) The native fundamental class is non-torsion (infinite order).
  (2) Its integer multiples constitute a LINEARLY INJECTED copy of ℤ.
  (3) This copy splits by an explicit Z-linear retraction from the
      actual native H₂ to ℤ, obtained by recovering the signed cycle
      via the native cycles/homology isomorphisms and evaluating the
      coefficient of the genuine original north-pentagon face.

Therefore H₂ has an explicit direct-summand copy of ℤ and is not
a finite torsion-only artifact. We DO NOT conclude H₂ ≅ ℤ,
determine all cycles, or identify a generator for the entire H₂:
surjectivity of the inclusion and vanishing of the complement
remain independent goals. No external Gray 3-functor, topological
sphere homeomorphism or old Stage-II omega comparison is asserted.
-/

/-- The genuinely native homologyπ ISO when the actual d₃=0,
not a free-standing quotient projection replacing the native API. -/
def c60NativeH2FundamentalπIso :
    c60NativeIntegralCellularComplex.cycles 2 ≅
      c60NativeIntegralCellularComplex.homology 2 :=
  c60NativeIntegralCellularComplex.isoHomologyπ 3 2
    (by simp) c60NativeIntegralCellularComplex_d32

/-- Canonical recovery of a genuine native H₂ homology class to
the concrete signed C60 2-cycle ker(d₂). Both arrows here are
ACTUAL mathlib category-theoretic isomorphisms; the incoming
boundary is zero by F59-F12. -/
def c60NativeH2ConcreteCycleIso :
    c60NativeIntegralCellularComplex.homology 2 ≅
      ModuleCat.of ℤ
        (LinearMap.ker (c60NativeIntegralCellularComplex.sc 2).g.hom) :=
  c60NativeH2FundamentalπIso.symm ≪≫
    (c60NativeIntegralCellularComplex.sc 2).moduleCatCyclesIso

/-- An honest native Z-LINEAR COEFFICIENT MAP from H₂ to ℤ,
obtained by decoding the native H₂ cycle and extracting the
coefficient of the actual north-pentagon face. -/
def c60NativeH2NorthPentagonCoefficient :
    (c60NativeIntegralCellularComplex.homology 2) →ₗ[ℤ] ℤ :=
  ((Finsupp.lapply (.aroundVertex .north) :
      C60IntegralTwoChains →ₗ[ℤ] ℤ).comp
    (LinearMap.ker
      (c60NativeIntegralCellularComplex.sc 2).g.hom).subtype).comp
      c60NativeH2ConcreteCycleIso.hom.hom

/-- The canonically decoded native H₂ fundamental class is EXACTLY
the global sum of 32 original oriented faces, as a concrete
kernel element, NOT merely equivalent in integer charge. -/
theorem c60NativeH2ConcreteCycleIso_fundamental :
    c60NativeH2ConcreteCycleIso.hom.hom
      c60NativeH2FundamentalClass =
      (⟨c60IntegralFundamentalSurfaceChain,
        c60NativeH2_fundamental_mem_native_cycles⟩ :
        LinearMap.ker (c60NativeIntegralCellularComplex.sc 2).g.hom) := by
  have hπ :
      c60NativeH2FundamentalπIso.inv.hom
        c60NativeH2FundamentalClass =
          c60NativeH2FundamentalCycle := by
    simpa only [c60NativeH2FundamentalClass,
      c60NativeH2FundamentalπIso] using
      (Iso.hom_inv_id_apply c60NativeH2FundamentalπIso
        c60NativeH2FundamentalCycle)
  change ((c60NativeIntegralCellularComplex.sc 2).moduleCatCyclesIso.hom).hom
    (c60NativeH2FundamentalπIso.inv.hom
      c60NativeH2FundamentalClass) = _
  rw [hπ]
  simpa only [c60NativeH2FundamentalCycle,
    Iso.inv_hom_id_apply]

/-- The north-pentagon coordinate of the native fundamental class
is exactly +1, its ORIGINAL INTEGRAL face coefficient.
This certificate detects nonzero integer multiples in native H₂. -/
theorem c60NativeH2NorthPentagonCoefficient_fundamental :
    c60NativeH2NorthPentagonCoefficient
      c60NativeH2FundamentalClass = (1 : ℤ) := by
  change
    ((Finsupp.lapply (.aroundVertex .north) :
      C60IntegralTwoChains →ₗ[ℤ] ℤ)
      ((LinearMap.ker
        (c60NativeIntegralCellularComplex.sc 2).g.hom).subtype
          (c60NativeH2ConcreteCycleIso.hom.hom
            c60NativeH2FundamentalClass))) = 1
  rw [c60NativeH2ConcreteCycleIso_fundamental]
  exact c60IntegralFundamentalSurfaceChain_coeff (.aroundVertex .north)

/-- A genuine Z-linear map from the integers into the NATIVE
mathlib H₂ object, sending n to n times the actual C60 fundamental
class, not to a detached formal generator. -/
def c60NativeH2FundamentalLinear :
    ℤ →ₗ[ℤ] (c60NativeIntegralCellularComplex.homology 2) :=
  LinearMap.toSpanSingleton ℤ
    (c60NativeIntegralCellularComplex.homology 2)
    c60NativeH2FundamentalClass

/-- This copy of the integers inside native C60 H₂ is SPLIT:
the north-pentagon coefficient map is a strict linear LEFT
INVERSE of the map sending n to n times the fundamental class. -/
theorem c60NativeH2FundamentalLinear_split :
    c60NativeH2NorthPentagonCoefficient.comp
      c60NativeH2FundamentalLinear = LinearMap.id := by
  apply LinearMap.ext
  intro n
  simp [c60NativeH2FundamentalLinear,
    c60NativeH2NorthPentagonCoefficient_fundamental]

/-- As a consequence, the full INTEGER span of the actual native
C60 H₂ fundamental class is isomorphic to ℤ: its inclusion
is INJECTIVE, not merely nonzero as in F59-F12. -/
theorem c60NativeH2FundamentalLinear_injective :
    Function.Injective c60NativeH2FundamentalLinear := by
  intro m n hmn
  have h := congrArg c60NativeH2NorthPentagonCoefficient hmn
  simpa only [← LinearMap.comp_apply,
    c60NativeH2FundamentalLinear_split,
    LinearMap.id_apply] using h

/-- No nonzero integer annihilates the REAL C60 native
fundamental homology class. This makes its infinite-order
nature mathematically explicit in the true native H₂ object. -/
theorem c60NativeH2FundamentalClass_zsmul_eq_zero_iff (n : ℤ) :
    n • c60NativeH2FundamentalClass = 0 ↔ n = 0 := by
  constructor
  · intro h
    have hh := congrArg c60NativeH2NorthPentagonCoefficient h
    simpa only [map_smul,
      c60NativeH2NorthPentagonCoefficient_fundamental,
      smul_eq_mul, mul_one, map_zero] using hh
  · rintro rfl
    simp

/-- There are infinitely many DISTINCT integer multiples of
the explicit native C60 H₂ fundamental class; it is not torsion. -/
theorem c60NativeH2FundamentalClass_infinite_order :
    Function.Injective
      (fun n : ℤ => n • c60NativeH2FundamentalClass) := by
  simpa only [c60NativeH2FundamentalLinear,
    LinearMap.toSpanSingleton_apply] using
      c60NativeH2FundamentalLinear_injective

#print axioms c60NativeH2FundamentalπIso
#print axioms c60NativeH2ConcreteCycleIso
#print axioms c60NativeH2NorthPentagonCoefficient
#print axioms c60NativeH2ConcreteCycleIso_fundamental
#print axioms c60NativeH2NorthPentagonCoefficient_fundamental
#print axioms c60NativeH2FundamentalLinear
#print axioms c60NativeH2FundamentalLinear_split
#print axioms c60NativeH2FundamentalLinear_injective
#print axioms c60NativeH2FundamentalClass_zsmul_eq_zero_iff
#print axioms c60NativeH2FundamentalClass_infinite_order

end
end KUOS.DependentOriginationGrayC60NativeH2InfiniteOrderV5_161
