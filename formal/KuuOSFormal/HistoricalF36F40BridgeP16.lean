import KuuOSFormal.HistoricalF36F40BridgeP15
import KUOS.DependentOriginationGrayC60NativeH2CompleteV5_165

/-!
# F112-P16 — complete independent integral C60 2-cycle classification

The F59-F17 historical theorem gives the genuine integral 32-face
reconstruction Q d₂ + F ρ = identity on arbitrary historical C60 2-chains.
The now-integrated P15 signed face LinearEquiv transports this result
BACK to the true independent Kuu polygon basis (12 pentagons, 20 hexagons).

We prove every closed independent integer 2-chain is an integer multiple
of the genuine P11 signed surface. The independent north-pentagon
coefficient recovers the integer uniquely, yielding a genuine Mathlib
Z-linear equivalence of the entire native degree-two cycle kernel with Z.

This is a complete classification of degree-two cycles / ker(d₂).
It does not yet construct the independent 0/1/2/3 chain complex or
claim that any F47/F55/F68/F77 higher obstruction has vanished.
-/

namespace KUOS.F112ActualHistoricalF36F40BridgeP4
namespace GenuineOriginalC60Geometry

open CategoryTheory
open Kuu.F112.Physical
open KUOS.DependentOriginationGrayC60IntegralBoundaryLinearMapV5_159
open KUOS.DependentOriginationGrayC60NativeH2CompleteV5_165

set_option autoImplicit false
set_option warningAsError true
noncomputable section

/-- ALL true independent C60 integral 2-cycles, with arbitrary integer
coefficients on genuine native polygons, are multiples of the actual
signed P11 fundamental surface. The coefficient is constructed via
the real historical north-face functional and the P15 inverse. -/
theorem nativeC60EveryClosedTwoChain_is_multiple
    (c : NativeC60IntegralTwoChains)
    (hc : c ∈ nativeC60IntegralBoundaryTwo.ker) :
    ∃ n : ℤ, c = n • nativeP11FundamentalTwoChain := by
  have hclosed : c60IntegralBoundaryTwo
      (nativeP11ToOriginalFaceChain c) = 0 :=
    nativeC60IntegralBoundaryTwo_kernel_transport c hc
  let z : ℤ := c60F17NorthFaceCoefficient (nativeP11ToOriginalFaceChain c)
  have hhistory : nativeP11ToOriginalFaceChain c =
      z • c60IntegralFundamentalSurfaceChain := by
    have hrec := c60F17EveryTwoCycle_isFundamental
      (nativeP11ToOriginalFaceChain c) hclosed
    simpa only [c60F17FundamentalSurfaceEmbedding,
      LinearMap.toSpanSingleton_apply] using hrec
  have htransport :
      nativeP11ToOriginalFaceChain ((-z) • nativeP11FundamentalTwoChain) =
        nativeP11ToOriginalFaceChain c := by
    calc
      nativeP11ToOriginalFaceChain ((-z) • nativeP11FundamentalTwoChain) =
          (-z) • (-c60IntegralFundamentalSurfaceChain) := by
            rw [map_smul, nativeP11ToOriginalFaceChain_fundamental]
      _ = z • c60IntegralFundamentalSurfaceChain := by
            simp only [neg_smul, smul_neg, neg_neg]
      _ = nativeP11ToOriginalFaceChain c := hhistory.symm
  refine ⟨-z, ?_⟩
  apply nativeP11OriginalFaceChainLinearEquiv.injective
  change nativeP11ToOriginalFaceChain c =
    nativeP11ToOriginalFaceChain ((-z) • nativeP11FundamentalTwoChain)
  exact htransport.symm

/-- The coefficient of the actual native north pentagon on the signed
fundamental surface is exactly one, not an arbitrary unit or rank proxy. -/
theorem nativeC60FundamentalNorthCoefficient :
    nativeP11FundamentalTwoChain (.pentagon .north) = (1 : ℤ) := by
  rw [nativeP11FundamentalTwoChain_coeff]
  rfl

/-- Strong normalization: the coefficient of the TRUE native north
pentagon uniquely determines EVERY closed integer C60 2-chain. -/
theorem nativeC60ClosedTwoChain_reconstruction
    (c : NativeC60IntegralTwoChains)
    (hc : c ∈ nativeC60IntegralBoundaryTwo.ker) :
    c = (c (.pentagon .north)) • nativeP11FundamentalTwoChain := by
  obtain ⟨n, rfl⟩ := nativeC60EveryClosedTwoChain_is_multiple c hc
  have hn : (n • nativeP11FundamentalTwoChain) (.pentagon .north) = n := by
    rw [Finsupp.smul_apply, nativeC60FundamentalNorthCoefficient]
    simp
  rw [hn]

/-- Genuine Z-linear independent north-pentagon coefficient map
on the ENTIRE native kernel of the actual native boundary d₂. -/
def nativeC60ClosedNorthCoefficient :
    nativeC60IntegralBoundaryTwo.ker →ₗ[ℤ] ℤ :=
  (Finsupp.lapply (.pentagon .north) :
    NativeC60IntegralTwoChains →ₗ[ℤ] ℤ).comp
      nativeC60IntegralBoundaryTwo.ker.subtype

/-- Its inverse will be integer scalar multiplication of the actual
P11 oriented fundamental surface. In particular the map is bijective
on ALL closed independent C60 degree-two integer chains. -/
theorem nativeC60ClosedNorthCoefficient_bijective :
    Function.Bijective nativeC60ClosedNorthCoefficient := by
  constructor
  · intro a b hab
    change a.val (.pentagon .north) = b.val (.pentagon .north) at hab
    apply Subtype.ext
    calc
      a.val = (a.val (.pentagon .north)) • nativeP11FundamentalTwoChain :=
        nativeC60ClosedTwoChain_reconstruction a.val a.property
      _ = (b.val (.pentagon .north)) • nativeP11FundamentalTwoChain := by
        rw [hab]
      _ = b.val :=
        (nativeC60ClosedTwoChain_reconstruction b.val b.property).symm
  · intro n
    refine ⟨⟨n • nativeP11FundamentalTwoChain, ?_⟩, ?_⟩
    · change nativeC60IntegralBoundaryTwo
        (n • nativeP11FundamentalTwoChain) = 0
      rw [map_smul, nativeC60IntegralBoundaryTwo_fundamental_zero, smul_zero]
    · change (n • nativeP11FundamentalTwoChain) (.pentagon .north) = n
      rw [Finsupp.smul_apply, nativeC60FundamentalNorthCoefficient]
      simp

/-- F112-P16 main theorem: COMPLETE genuine native C60 closed 2-chain
module is Z, with coordinate the actual north-pentagon coefficient.
No new axioms or numerical Fin 32 substitute are introduced. -/
noncomputable def nativeC60ClosedTwoChainLinearEquivInt :
    nativeC60IntegralBoundaryTwo.ker ≃ₗ[ℤ] ℤ :=
  LinearEquiv.ofBijective nativeC60ClosedNorthCoefficient
    nativeC60ClosedNorthCoefficient_bijective

/-- The same result as an actual Mathlib ModuleCat isomorphism,
ready for a later degreewise chain-complex and H₂ comparison. -/
noncomputable def nativeC60ClosedTwoChainModuleIsoInt :
    ModuleCat.of ℤ nativeC60IntegralBoundaryTwo.ker ≅
      ModuleCat.of ℤ ℤ :=
  nativeC60ClosedTwoChainLinearEquivInt.toModuleIso

/-- The genuine independent fundamental 2-cycle has infinite Z-order:
its actual native north-pentagon coordinate detects every multiple. -/
theorem nativeC60FundamentalTwoChain_integer_multiple_injective :
    Function.Injective (fun n : ℤ => n • nativeP11FundamentalTwoChain) := by
  intro m n h
  have hn := congrArg
    (fun c : NativeC60IntegralTwoChains => c (.pentagon .north)) h
  simpa only [Finsupp.smul_apply, nativeC60FundamentalNorthCoefficient,
    smul_eq_mul, mul_one] using hn

#print axioms nativeC60EveryClosedTwoChain_is_multiple
#print axioms nativeC60FundamentalNorthCoefficient
#print axioms nativeC60ClosedTwoChain_reconstruction
#print axioms nativeC60ClosedNorthCoefficient
#print axioms nativeC60ClosedNorthCoefficient_bijective
#print axioms nativeC60ClosedTwoChainLinearEquivInt
#print axioms nativeC60ClosedTwoChainModuleIsoInt
#print axioms nativeC60FundamentalTwoChain_integer_multiple_injective

end
end GenuineOriginalC60Geometry
end KUOS.F112ActualHistoricalF36F40BridgeP4
