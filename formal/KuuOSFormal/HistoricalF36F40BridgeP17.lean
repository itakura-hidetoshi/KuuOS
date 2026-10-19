import KuuOSFormal.HistoricalF36F40BridgeP16
import Mathlib.Algebra.Homology.ShortComplex.ModuleCat
import Mathlib.Algebra.Homology.ShortComplex.HomologicalComplex
import Mathlib.Algebra.Module.Submodule.Equiv

/-!
# F112-P17 — genuine independent-polygon C60 chain complex and Mathlib H₂

P14 constructed an INDEPENDENT Z-linear d₂ on the native physical
32-polygon face basis and proved d₁ ∘ d₂ = 0 for all integer chains.
P15 established the fully signed degree-two comparison with the
original historical face basis, and P16 classified all native 2-cycles
as the integer multiples of the real native oriented fundamental cycle.

This file packages that native d₂ into a genuine Mathlib ChainComplex
(ModuleCat Z) Nat. The degree-two carrier is NATIVE (Polygon →₀ Z),
not the historical face carrier. Degrees zero and one deliberately
reuse the actual historical vertex and physical edge Finsupp types;
these degrees are NOT claimed to have fully independent Kuu carriers.
All degrees ≥ 3 are the zero object, with no invented three-cells.

Using the Mathlib homologyπ isomorphism for the proved zero incoming
d₃, we connect the categorical H₂ to the EXACT native ker d₂ and
then to Z by the previously kernel-verified P16 linear equivalence.

No Gray dependency enters KuuOSStrict; no unsupported F55 lift,
F68/F77 descent, three-dimensional cell, or homotopy equivalence is
asserted. No sorry, admit, or new unproved axiom is needed.
-/

namespace KUOS.F112ActualHistoricalF36F40BridgeP4
namespace GenuineOriginalC60Geometry

open CategoryTheory Limits
open Kuu.F112.Physical
open KUOS.DependentOriginationGrayC60IntegralBoundaryLinearMapV5_159
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationGrayC60NativeChainComplexV5_160

set_option autoImplicit false
set_option warningAsError true
noncomputable section

/-- Actual integer C60 cellular groups, using native independent Kuu
32-polygons in degree 2 and the original physically certified
90 edges / 60 vertices in degrees 1 / 0. Higher degrees vanish. -/
def independentC60ChainObjects : ℕ → ModuleCat ℤ
  | 0 => ModuleCat.of ℤ C60IntegralZeroChains
  | 1 => ModuleCat.of ℤ NativeC60IntegralOneChains
  | 2 => ModuleCat.of ℤ NativeC60IntegralTwoChains
  | _ + 3 => ModuleCat.of ℤ PUnit

/-- Native Kuu degree-two boundary and the original integer
physical edge-to-vertex boundary, without replacing native d₂
by the historical composition used only to PROVE the square. -/
def independentC60ChainDifferential :
    ∀ n : ℕ, independentC60ChainObjects (n + 1) ⟶
      independentC60ChainObjects n
  | 0 => ModuleCat.ofHom c60IntegralBoundaryOne
  | 1 => ModuleCat.ofHom nativeC60IntegralBoundaryTwo
  | _ + 2 => 0

/-- Entire square-zero chain law at every degree: degree 2 is
the actual P14 d₁ ∘ native d₂ theorem, and higher differentials
vanish because no positive-dimensional 3-cells are postulated. -/
theorem independentC60ChainDifferential_comp_zero (n : ℕ) :
    independentC60ChainDifferential (n + 1) ≫
      independentC60ChainDifferential n = 0 := by
  cases n with
  | zero =>
      apply ModuleCat.hom_ext
      exact originalBoundaryOne_comp_nativeBoundaryTwo_zero
  | succ n =>
      cases n <;> simp [independentC60ChainDifferential]

/-- A genuine native-polygon Mathlib ChainComplex object. -/
def independentC60IntegralCellularComplex :
    ChainComplex (ModuleCat ℤ) ℕ :=
  ChainComplex.of independentC60ChainObjects
    independentC60ChainDifferential
    independentC60ChainDifferential_comp_zero

/-- The degree-two carrier remains precisely the genuine native
polygon Finsupp free Z-module. -/
theorem independentC60IntegralCellularComplex_X2 :
    independentC60IntegralCellularComplex.X 2 =
      ModuleCat.of ℤ NativeC60IntegralTwoChains := rfl

/-- The genuinely native d₂ on arbitrary polygon chains. -/
theorem independentC60IntegralCellularComplex_d21 :
    independentC60IntegralCellularComplex.d 2 1 =
      ModuleCat.ofHom nativeC60IntegralBoundaryTwo := by
  exact ChainComplex.of_d independentC60ChainObjects
    independentC60ChainDifferential
    independentC60ChainDifferential_comp_zero 1

/-- The actual degree-one outgoing edge-to-vertex differential. -/
theorem independentC60IntegralCellularComplex_d10 :
    independentC60IntegralCellularComplex.d 1 0 =
      ModuleCat.ofHom c60IntegralBoundaryOne := by
  exact ChainComplex.of_d independentC60ChainObjects
    independentC60ChainDifferential
    independentC60ChainDifferential_comp_zero 0

/-- The incoming degree-three differential is genuinely zero:
no fabricated C60 three-cells. -/
theorem independentC60IntegralCellularComplex_d32 :
    independentC60IntegralCellularComplex.d 3 2 = 0 := by
  exact ChainComplex.of_d independentC60ChainObjects
    independentC60ChainDifferential
    independentC60ChainDifferential_comp_zero 2

/-- Exact incoming zero map at degree two in Mathlib's
short-complex homology presentation. -/
theorem independentC60H2_incoming_zero :
    (independentC60IntegralCellularComplex.sc 2).f = 0 := by
  change independentC60IntegralCellularComplex.d
    ((ComplexShape.down ℕ).prev 2) 2 = 0
  have hp : (ComplexShape.down ℕ).prev 2 = 3 := by simp
  rw [hp]
  exact independentC60IntegralCellularComplex_d32

/-- Genuine Mathlib homologyπ ISO: no C₃ boundaries to quotient by. -/
def independentC60H2FundamentalπIso :
    independentC60IntegralCellularComplex.cycles 2 ≅
      independentC60IntegralCellularComplex.homology 2 :=
  independentC60IntegralCellularComplex.isoHomologyπ 3 2
    (by simp) independentC60IntegralCellularComplex_d32

/-- Actual H₂ of the new independent-polygon complex is isomorphic
to the concrete native integer kernel of P14 d₂: this is NOT an
external free abstract Z-module replacing the Mathlib H₂ object. -/
/-- Equality of the concrete native boundary kernel and the actual
ShortComplex kernel; this is a theorem about the two true differentials,
not a coercion silently inserted by `convert`. -/
theorem independentC60H2KernelSubmodule_eq :
    LinearMap.ker
        (independentC60IntegralCellularComplex.sc 2).g.hom =
      LinearMap.ker nativeC60IntegralBoundaryTwo := by
  change LinearMap.ker
    (independentC60IntegralCellularComplex.d 2
      ((ComplexShape.down ℕ).next 2)).hom =
        LinearMap.ker nativeC60IntegralBoundaryTwo
  have hn : (ComplexShape.down ℕ).next 2 = 1 := by simp
  rw [hn, independentC60IntegralCellularComplex_d21]
  rfl

/-- This explicit Mathlib linear equivalence remembers the real
submodule equality and preserves the underlying polygon chain.
It replaces an opaque `convert`-generated cast of an isomorphism. -/
noncomputable def independentC60H2KernelPresentationIso :
    (independentC60IntegralCellularComplex.sc 2).moduleCatLeftHomologyData.K ≅
      ModuleCat.of ℤ (LinearMap.ker nativeC60IntegralBoundaryTwo) :=
  (LinearEquiv.ofEq
    (LinearMap.ker
      (independentC60IntegralCellularComplex.sc 2).g.hom)
    (LinearMap.ker nativeC60IntegralBoundaryTwo)
    independentC60H2KernelSubmodule_eq).toModuleIso

/-- Actual categorical H₂-to-native-kernel isomorphism, factored
through the explicit, underlying-chain-preserving kernel equivalence. -/
def independentC60H2ConcreteCycleIso :
    independentC60IntegralCellularComplex.homology 2 ≅
      ModuleCat.of ℤ (LinearMap.ker nativeC60IntegralBoundaryTwo) :=
  (independentC60H2FundamentalπIso.symm ≪≫
    (independentC60IntegralCellularComplex.sc 2).moduleCatCyclesIso) ≪≫
      independentC60H2KernelPresentationIso

/-- F112-P17 main result: REAL categorical second homology of the
independent-polygon 32-face C60 chain complex is canonically Z,
via the exact native kernel and the physical north-pentagon charge. -/
def independentC60H2IsoInteger :
    independentC60IntegralCellularComplex.homology 2 ≅
      ModuleCat.of ℤ ℤ :=
  independentC60H2ConcreteCycleIso ≪≫
    nativeC60ClosedTwoChainModuleIsoInt

/-- The genuine independent oriented P11 fundamental 2-cycle
defines a class in Mathlib H₂ through the zero-incoming-boundary ISO. -/
def independentC60H2FundamentalClass :
    independentC60IntegralCellularComplex.homology 2 :=
  independentC60H2ConcreteCycleIso.inv
    (⟨nativeP11FundamentalTwoChain,
      nativeP11FundamentalTwoChain_mem_new_kernel⟩ :
      LinearMap.ker nativeC60IntegralBoundaryTwo)

/-- The integer invariant of this actual H₂ fundamental class is
exactly +1, so it is a primitive generator (not just nonzero). -/
theorem independentC60H2FundamentalClass_coordinate :
    independentC60H2IsoInteger.hom.hom
      independentC60H2FundamentalClass = (1 : ℤ) := by
  change nativeC60ClosedNorthCoefficient
    (independentC60H2ConcreteCycleIso.hom.hom
      independentC60H2FundamentalClass) = 1
  have hround :
      independentC60H2ConcreteCycleIso.hom.hom
        (independentC60H2ConcreteCycleIso.inv
          (⟨nativeP11FundamentalTwoChain,
            nativeP11FundamentalTwoChain_mem_new_kernel⟩ :
            LinearMap.ker nativeC60IntegralBoundaryTwo)) =
        (⟨nativeP11FundamentalTwoChain,
          nativeP11FundamentalTwoChain_mem_new_kernel⟩ :
          LinearMap.ker nativeC60IntegralBoundaryTwo) := by
    exact independentC60H2ConcreteCycleIso.inv_hom_id_apply _
  rw [independentC60H2FundamentalClass, hround]
  change nativeP11FundamentalTwoChain (.pentagon .north) = 1
  exact nativeC60FundamentalNorthCoefficient

/-- The real native H₂ class has no finite integer annihilator. -/
theorem independentC60H2FundamentalClass_infinite_order :
    Function.Injective
      (fun n : ℤ => n • independentC60H2FundamentalClass) := by
  intro a b hab
  have hh := congrArg independentC60H2IsoInteger.hom.hom hab
  change independentC60H2IsoInteger.hom.hom
      (a • independentC60H2FundamentalClass) =
    independentC60H2IsoInteger.hom.hom
      (b • independentC60H2FundamentalClass) at hh
  have hf (n : ℤ) :
      independentC60H2IsoInteger.hom.hom
        (n • independentC60H2FundamentalClass) =
      n • independentC60H2IsoInteger.hom.hom
        independentC60H2FundamentalClass := by
    have hlinear :=
      (independentC60H2IsoInteger.hom.hom).map_smul
        n independentC60H2FundamentalClass
    change independentC60H2IsoInteger.hom.hom
        ((inferInstance : Module ℤ
            (independentC60IntegralCellularComplex.homology 2)).smul
          n independentC60H2FundamentalClass) =
      n • independentC60H2IsoInteger.hom.hom
        independentC60H2FundamentalClass at hlinear
    rw [int_smul_eq_zsmul
      (inferInstance : Module ℤ
        (independentC60IntegralCellularComplex.homology 2))
      n independentC60H2FundamentalClass] at hlinear
    exact hlinear
  rw [hf a, hf b, independentC60H2FundamentalClass_coordinate] at hh
  simpa using hh

#print axioms independentC60ChainObjects
#print axioms independentC60ChainDifferential
#print axioms independentC60ChainDifferential_comp_zero
#print axioms independentC60IntegralCellularComplex
#print axioms independentC60IntegralCellularComplex_X2
#print axioms independentC60IntegralCellularComplex_d21
#print axioms independentC60IntegralCellularComplex_d10
#print axioms independentC60IntegralCellularComplex_d32
#print axioms independentC60H2_incoming_zero
#print axioms independentC60H2FundamentalπIso
#print axioms independentC60H2KernelSubmodule_eq
#print axioms independentC60H2KernelPresentationIso
#print axioms independentC60H2ConcreteCycleIso
#print axioms independentC60H2IsoInteger
#print axioms independentC60H2FundamentalClass
#print axioms independentC60H2FundamentalClass_coordinate
#print axioms independentC60H2FundamentalClass_infinite_order

end
end GenuineOriginalC60Geometry
end KUOS.F112ActualHistoricalF36F40BridgeP4
