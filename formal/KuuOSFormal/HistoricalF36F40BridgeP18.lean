import KuuOSFormal.HistoricalF36F40BridgeP17
import KUOS.DependentOriginationGrayC60NativeChainComplexV5_160
import Mathlib.Algebra.Homology.ShortComplex.HomologicalComplex

/-!
# F112-P18 — exact signed chain-complex equivalence and induced H₂ isomorphism

This OLD-SIDE-ONLY comparison connects the F112 independent 32-polygon
integer cellular complex from P17 to the genuinely historical F59
90-edge / 60-vertex chain complex.

Degree two is the P15 signed, invertible integral face transport.
Degrees one and zero are actual identity maps on the SAME physical
carriers (not newly claimed independently reconstructed carriers).
All degrees at least three have zero objects, with identity comparison.
The degree-two differential square is P14's separately verified
all-chain boundary commutativity, not a claimed F55/Gray lift.

The complex isomorphism, and the H₂ isomorphism obtained functorially
from it, are genuine mathlib category-theoretic constructions.
-/ 

namespace KUOS.F112ActualHistoricalF36F40BridgeP4
namespace GenuineOriginalC60Geometry

open CategoryTheory Limits
open KUOS.DependentOriginationGrayC60IntegralBoundaryLinearMapV5_159
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationGrayC60NativeChainComplexV5_160

set_option autoImplicit false
set_option warningAsError true
noncomputable section

/-- Exact degreewise isomorphism: signed P15 in degree two; identity
on the actual common 90-edge and 60-vertex types; identity above degree
two, where both complexes have zero groups. -/
def independentHistoricalC60DegreeIso :
    (n : ℕ) →
      independentC60IntegralCellularComplex.X n ≅
        c60NativeIntegralCellularComplex.X n
  | 0 => Iso.refl _
  | 1 => Iso.refl _
  | 2 => nativeP11OriginalFaceChainLinearEquiv.toModuleIso
  | _ + 3 => Iso.refl _

/-- Exactly the P14 integer boundary compatibility at degree two,
and literal identity compatibility at degree one / all higher degrees. -/
theorem independentHistoricalC60DegreeIso_comm (n : ℕ) :
    (independentHistoricalC60DegreeIso (n + 1)).hom ≫
      c60NativeChainDifferential n =
    independentC60ChainDifferential n ≫
      (independentHistoricalC60DegreeIso n).hom := by
  cases n with
  | zero =>
      simp [independentHistoricalC60DegreeIso,
        c60NativeChainDifferential, independentC60ChainDifferential]
  | succ n =>
      cases n with
      | zero =>
          apply ModuleCat.hom_ext
          change c60IntegralBoundaryTwo.comp nativeP11ToOriginalFaceChain =
            nativeC60IntegralBoundaryTwo
          exact nativeC60IntegralBoundaryTwo_commutes.symm
      | succ n =>
          simp [independentHistoricalC60DegreeIso,
            c60NativeChainDifferential, independentC60ChainDifferential]

/-- F112-P18 main chain-level result: a genuine mathlib isomorphism
of whole chain complexes, with its inverse constructed by mathlib
from degreewise integral equivalences (not simply asserted). -/
def independentHistoricalC60ChainIso :
    independentC60IntegralCellularComplex ≅
      c60NativeIntegralCellularComplex :=
  HomologicalComplex.Hom.isoOfComponents
    independentHistoricalC60DegreeIso
    (by
      intro i j hij
      change j + 1 = i at hij
      subst i
      simpa only [independentC60IntegralCellularComplex,
        c60NativeIntegralCellularComplex, ChainComplex.of_d]
        using independentHistoricalC60DegreeIso_comm j)

/-- The degree-two component of the genuine chain isomorphism
is precisely P15's independently proved signed integer map. -/
theorem independentHistoricalC60ChainIso_two :
    (independentHistoricalC60ChainIso.hom.f 2).hom =
      nativeP11ToOriginalFaceChain := by
  rfl

/-- The actual degree-zero and degree-one components are identity,
without an unsupported claim that new independent carriers exist. -/
theorem independentHistoricalC60ChainIso_one :
    independentHistoricalC60ChainIso.hom.f 1 = 𝟙 _ := by
  rfl

theorem independentHistoricalC60ChainIso_zero :
    independentHistoricalC60ChainIso.hom.f 0 = 𝟙 _ := by
  rfl

/-- Functorial mathlib second homology isomorphism induced by the
actual chain-complex isomorphism, not an unrelated chosen Z ≅ Z. -/
def independentHistoricalC60H2Iso :
    independentC60IntegralCellularComplex.homology 2 ≅
      c60NativeIntegralCellularComplex.homology 2 :=
  HomologicalComplex.homologyMapIso independentHistoricalC60ChainIso 2

/-- The forward homology arrow is exactly the arrow induced by
the whole signed chain map, rather than an arbitrary H₂ isomorphism. -/
theorem independentHistoricalC60H2Iso_hom :
    independentHistoricalC60H2Iso.hom =
      HomologicalComplex.homologyMap independentHistoricalC60ChainIso.hom 2 := by
  rfl

/-- P11's genuinely native oriented fundamental 2-chain is sent
to the *negative* of the true historical F59 fundamental 2-chain.
This is a strict equality in the original integer chain group. -/
theorem independentHistoricalC60ChainIso_fundamental_sign :
    (independentHistoricalC60ChainIso.hom.f 2).hom
      nativeP11FundamentalTwoChain =
        -c60IntegralFundamentalSurfaceChain := by
  rw [independentHistoricalC60ChainIso_two]
  exact nativeP11ToOriginalFaceChain_fundamental

#print axioms independentHistoricalC60DegreeIso
#print axioms independentHistoricalC60DegreeIso_comm
#print axioms independentHistoricalC60ChainIso
#print axioms independentHistoricalC60ChainIso_two
#print axioms independentHistoricalC60ChainIso_one
#print axioms independentHistoricalC60ChainIso_zero
#print axioms independentHistoricalC60H2Iso
#print axioms independentHistoricalC60H2Iso_hom
#print axioms independentHistoricalC60ChainIso_fundamental_sign

end
end GenuineOriginalC60Geometry
end KUOS.F112ActualHistoricalF36F40BridgeP4
