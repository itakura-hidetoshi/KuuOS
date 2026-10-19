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
open KUOS.DependentOriginationGrayC60NativeH2FundamentalClassV5_161
open KUOS.DependentOriginationGrayC60NativeH2InfiniteOrderV5_161

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
      -- Category-level units can conceal different reducible ModuleCat
      -- presentations; prove the equality of the underlying linear maps.
      apply ModuleCat.hom_ext
      apply LinearMap.ext
      intro c
      rfl
  | succ n =>
      cases n with
      | zero =>
          -- This is precisely P14: d₂ᴴ ∘ T₂ = d₂ᴺ on ALL chains.
          apply ModuleCat.hom_ext
          change c60IntegralBoundaryTwo.comp nativeP11ToOriginalFaceChain =
            nativeC60IntegralBoundaryTwo
          exact nativeC60IntegralBoundaryTwo_commutes.symm
      | succ n =>
          -- Both differentials are zero at all degrees >= 3.
          -- Pointwise computation also covers the n=0 case where
          -- the degree-two target change of basis is nontrivial.
          apply ModuleCat.hom_ext
          apply LinearMap.ext
          intro c
          -- The unit and zero maps reduce definitionally after
          -- unfolding their actual ModuleCat linear-map carriers.
          simp [independentHistoricalC60DegreeIso,
            c60NativeChainDifferential, independentC60ChainDifferential]
          rfl

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

/-- The previously incomplete historical F59 H₂ classification follows
from the *actual chain-complex isomorphism* and P17's kernel-level
classification, not from abstract matching rank counts. -/
def historicalC60H2IsoInteger :
    c60NativeIntegralCellularComplex.homology 2 ≅ ModuleCat.of ℤ ℤ :=
  independentHistoricalC60H2Iso.symm ≪≫ independentC60H2IsoInteger

/-- Naturality of the true mathlib H₂ map on abstract cycles.
This is the key compatibility needed to compare oriented fundamental
homology representatives without confusing them with chain generators. -/
theorem independentHistoricalC60H2_homologyπ_naturality :
    independentC60IntegralCellularComplex.homologyπ 2 ≫
      independentHistoricalC60H2Iso.hom =
    HomologicalComplex.cyclesMap independentHistoricalC60ChainIso.hom 2 ≫
      c60NativeIntegralCellularComplex.homologyπ 2 := by
  exact HomologicalComplex.homologyπ_naturality
    independentHistoricalC60ChainIso.hom 2

/-! ## The signed comparison on the *actual* fundamental H₂ classes

The two incoming degree-three differentials vanish. We therefore use
mathlib's categorical cycles, their monic inclusions into 2-chains,
and homologyπ naturality. The sign is not inferred from equality of
ranks or from a separately chosen ℤ-coordinate map. -/

/-- The P17 native H₂ generator, lifted canonically through the zero-d₃
homologyπ isomorphism, has precisely the genuine P11 polygon chain
as underlying degree-two cycle. -/
theorem independentC60H2Fundamental_iCycles :
    (independentC60IntegralCellularComplex.iCycles 2)
      (independentC60H2FundamentalπIso.inv
        independentC60H2FundamentalClass) =
      nativeP11FundamentalTwoChain := by
  have hker :
      independentC60H2ConcreteCycleIso.hom.hom
        independentC60H2FundamentalClass =
        (⟨nativeP11FundamentalTwoChain,
          nativeP11FundamentalTwoChain_mem_new_kernel⟩ :
          LinearMap.ker nativeC60IntegralBoundaryTwo) := by
    unfold independentC60H2FundamentalClass
    exact independentC60H2ConcreteCycleIso.inv_hom_id_apply _
  change (independentC60IntegralCellularComplex.sc 2).iCycles
    (independentC60H2FundamentalπIso.inv
      independentC60H2FundamentalClass) = nativeP11FundamentalTwoChain
  rw [← (independentC60IntegralCellularComplex.sc 2).moduleCatCyclesIso_hom_i]
  change
    ((independentC60IntegralCellularComplex.sc 2).moduleCatCyclesIso.hom.hom
      (independentC60H2FundamentalπIso.inv
        independentC60H2FundamentalClass)).val =
      nativeP11FundamentalTwoChain
  have hg :
      (independentC60IntegralCellularComplex.sc 2).g.hom =
        nativeC60IntegralBoundaryTwo := by
    change (independentC60IntegralCellularComplex.d 2
      ((ComplexShape.down ℕ).next 2)).hom =
        nativeC60IntegralBoundaryTwo
    have hn : (ComplexShape.down ℕ).next 2 = 1 := by simp
    rw [hn, independentC60IntegralCellularComplex_d21]
    rfl
  simpa [independentC60H2ConcreteCycleIso, hg] using
    congrArg Subtype.val hker

/-- The historical H₂ class represented by the transported genuine
native surface is exactly its signed historical integer 2-cycle. -/
theorem transportedNativeP11OriginalH2Class_iCycles :
    (c60NativeIntegralCellularComplex.iCycles 2)
      (c60NativeH2FundamentalπIso.inv
        transportedNativeP11OriginalH2Class) =
      nativeP11ToOriginalFaceChain nativeP11FundamentalTwoChain := by
  change (c60NativeIntegralCellularComplex.sc 2).iCycles
    (c60NativeH2FundamentalπIso.inv
      transportedNativeP11OriginalH2Class) =
      nativeP11ToOriginalFaceChain nativeP11FundamentalTwoChain
  rw [← (c60NativeIntegralCellularComplex.sc 2).moduleCatCyclesIso_hom_i]
  change
    (c60NativeH2ConcreteCycleIso.hom.hom
      transportedNativeP11OriginalH2Class).val =
      nativeP11ToOriginalFaceChain nativeP11FundamentalTwoChain
  unfold transportedNativeP11OriginalH2Class
  rw [Iso.inv_hom_id_apply]

/-- The cycles map induced by the actual signed chain isomorphism
carries the genuine P11 fundamental cycle to the historical cycle.
Faithfulness here is the mono property of mathlib's cycles inclusion. -/
theorem independentHistoricalC60CyclesMap_fundamental :
    HomologicalComplex.cyclesMap independentHistoricalC60ChainIso.hom 2
      (independentC60H2FundamentalπIso.inv
        independentC60H2FundamentalClass) =
    c60NativeH2FundamentalπIso.inv
      transportedNativeP11OriginalH2Class := by
  apply (ModuleCat.mono_iff_injective
    (c60NativeIntegralCellularComplex.iCycles 2)).mp inferInstance
  have hnatural := congrArg
    (fun f : independentC60IntegralCellularComplex.cycles 2 ⟶
        c60NativeIntegralCellularComplex.X 2 =>
      f (independentC60H2FundamentalπIso.inv
        independentC60H2FundamentalClass))
    (HomologicalComplex.cyclesMap_i
      independentHistoricalC60ChainIso.hom 2)
  have hcycle := independentC60H2Fundamental_iCycles
  have htransport := transportedNativeP11OriginalH2Class_iCycles
  have hface :
      (independentHistoricalC60ChainIso.hom.f 2)
        nativeP11FundamentalTwoChain =
      nativeP11ToOriginalFaceChain nativeP11FundamentalTwoChain := by
    exact independentHistoricalC60ChainIso_fundamental_sign.trans
      nativeP11ToOriginalFaceChain_fundamental.symm
  simp only [ModuleCat.comp_apply] at hnatural
  rw [hcycle] at hnatural
  rw [hface] at hnatural
  exact hnatural.trans htransport.symm

/-- P18 signed HOMOLOGY theorem, stronger than the previously proved
chain-level sign: the functorially induced H₂ morphism maps the
independent P11 generator to the negative historical F59 generator. -/
theorem independentHistoricalC60H2_fundamental_sign :
    independentHistoricalC60H2Iso.hom.hom
      independentC60H2FundamentalClass =
        -c60NativeH2FundamentalClass := by
  calc
    independentHistoricalC60H2Iso.hom
      independentC60H2FundamentalClass =
        (c60NativeIntegralCellularComplex.homologyπ 2)
          (HomologicalComplex.cyclesMap
            independentHistoricalC60ChainIso.hom 2
              (independentC60H2FundamentalπIso.inv
                independentC60H2FundamentalClass)) := by
          have hn := congrArg
            (fun f : independentC60IntegralCellularComplex.cycles 2 ⟶
                c60NativeIntegralCellularComplex.homology 2 =>
              f (independentC60H2FundamentalπIso.inv
                independentC60H2FundamentalClass))
            independentHistoricalC60H2_homologyπ_naturality
          have hround :
              (independentC60IntegralCellularComplex.homologyπ 2)
                (independentC60H2FundamentalπIso.inv
                  independentC60H2FundamentalClass) =
                independentC60H2FundamentalClass := by
            change independentC60H2FundamentalπIso.hom
              (independentC60H2FundamentalπIso.inv
                independentC60H2FundamentalClass) = _
            exact independentC60H2FundamentalπIso.inv_hom_id_apply _
          simp only [ModuleCat.comp_apply] at hn
          rw [hround] at hn
          exact hn
    _ = (c60NativeIntegralCellularComplex.homologyπ 2)
          (c60NativeH2FundamentalπIso.inv
            transportedNativeP11OriginalH2Class) := by
            rw [independentHistoricalC60CyclesMap_fundamental]
    _ = transportedNativeP11OriginalH2Class :=
      c60NativeH2FundamentalπIso.inv_hom_id_apply _
    _ = -c60NativeH2FundamentalClass :=
      transportedNativeP11OriginalH2Class_eq_neg

#print axioms independentC60H2Fundamental_iCycles
#print axioms transportedNativeP11OriginalH2Class_iCycles
#print axioms independentHistoricalC60CyclesMap_fundamental
#print axioms independentHistoricalC60H2_fundamental_sign

#print axioms historicalC60H2IsoInteger
#print axioms independentHistoricalC60H2_homologyπ_naturality

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
