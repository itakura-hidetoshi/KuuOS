import KuuOSFormal.HistoricalF36F40BridgeP20

/-!
# F112-P21 — integral orientation and historical H₂ generator

The genuine independent and preserved historical C60 chain complexes
are isomorphic, and P20 identifies the P17 and direct P19 fundamental
classes. This module transports the signed orientation from one
fundamental class to arbitrary integer multiples in the actual
categorical second homology and computes the original historical
generator's coordinate in the independently transported ℤ-isomorphism.

All assertions are for the original 32-polygon 2-chain and the original
physical 90-edge/60-vertex carriers. They do not imply any historical
F55 lift or F68/F77 higher coherence or obstruction vanishing.
-/

namespace KUOS.F112ActualHistoricalF36F40BridgeP4
namespace GenuineOriginalC60Geometry

open CategoryTheory Limits
open KUOS.DependentOriginationGrayC60NativeH2FundamentalClassV5_161
open KUOS.DependentOriginationGrayC60NativeChainComplexV5_160

set_option autoImplicit false
set_option warningAsError true
noncomputable section

/-- The historical F59 fundamental H₂ class has orientation
coordinate -1 under the canonical transport from the native P17
north-pentagon coordinate +1. It is NOT a separately chosen rank-one
identification with ℤ. -/
theorem p21HistoricalFundamentalClass_coordinate :
    historicalC60H2IsoInteger.hom.hom c60NativeH2FundamentalClass =
      (-1 : ℤ) := by
  have h :
      historicalC60H2IsoInteger.hom.hom
          (-c60NativeH2FundamentalClass) = (1 : ℤ) := by
    rw [← p20P17HistoricalH2_fundamental_sign]
    change independentC60H2IsoInteger.hom.hom
      (independentHistoricalC60H2Iso.inv.hom
        (independentHistoricalC60H2Iso.hom
          independentC60H2FundamentalClass)) = 1
    rw [independentHistoricalC60H2Iso.hom_inv_id_apply]
    exact independentC60H2FundamentalClass_coordinate
  have hn :
      -(historicalC60H2IsoInteger.hom.hom
        c60NativeH2FundamentalClass) = (1 : ℤ) := by
    simpa only [map_neg] using h
  have hx := congrArg (fun z : ℤ => -z) hn
  simpa only [neg_neg] using hx

/-- Integral strengthening of P20: the actual homology map of the
signed chain isomorphism carries EVERY integer multiple of the true
native P11 fundamental class to the oppositely oriented historical
fundamental class. -/
theorem p21IndependentHistoricalH2_sign_smul (n : ℤ) :
    independentHistoricalC60H2Iso.hom.hom
        (n • independentC60H2FundamentalClass) =
      (-n) • c60NativeH2FundamentalClass := by
  calc
    independentHistoricalC60H2Iso.hom.hom
        (n • independentC60H2FundamentalClass) =
      n • independentHistoricalC60H2Iso.hom.hom
        independentC60H2FundamentalClass := by
          simpa only [Int.cast_smul_eq_zsmul] using
            (map_intCast_smul (independentHistoricalC60H2Iso.hom.hom)
              ℤ ℤ n independentC60H2FundamentalClass)
    _ = n • (-c60NativeH2FundamentalClass) := by
          rw [p20P17HistoricalH2_fundamental_sign]
    _ = (-n) • c60NativeH2FundamentalClass := by
          exact zsmul_neg' c60NativeH2FundamentalClass n

/-- The real historical F59 fundamental H₂ class is of infinite
integer order, proved from the original categorical H₂ ≅ ℤ and its
computed orientation coordinate, not from a fabricated generator. -/
theorem p21HistoricalFundamentalClass_infinite_order :
    Function.Injective
      (fun n : ℤ => n • c60NativeH2FundamentalClass) := by
  intro a b hab
  have hh := congrArg historicalC60H2IsoInteger.hom.hom hab
  have hf (n : ℤ) :
      historicalC60H2IsoInteger.hom.hom
          (n • c60NativeH2FundamentalClass) =
        n • historicalC60H2IsoInteger.hom.hom
          c60NativeH2FundamentalClass := by
    simpa only [Int.cast_smul_eq_zsmul] using
      (map_intCast_smul (historicalC60H2IsoInteger.hom.hom)
        ℤ ℤ n c60NativeH2FundamentalClass)
  rw [hf a, hf b, p21HistoricalFundamentalClass_coordinate] at hh
  simpa [smul_eq_mul] using hh

#print axioms p21HistoricalFundamentalClass_coordinate
#print axioms p21IndependentHistoricalH2_sign_smul
#print axioms p21HistoricalFundamentalClass_infinite_order

end
end GenuineOriginalC60Geometry
end KUOS.F112ActualHistoricalF36F40BridgeP4
