import KuuOSFormal.HistoricalF36F40BridgeP21

/-!
# F112-P22 — genuine all-class integral H₂ reconstruction and signed naturality

The independent C60 H₂ ≅ ℤ was constructed from the actual
integer d₂-kernel of its 32 native polygons (P17). P20 proved
that the direct P19 cycle and the original P17 basic H₂ class coincide;
P21 proved the functorial sign on ALL integer multiples and identified
the actual historical F59 coordinate of its canonical generator as -1.

Here the existing genuine categorical isomorphisms, together with
the computed orientation coordinates, reconstruct EVERY class in both
original H₂ groups and prove the orientation formula for every
native H₂ class. No arbitrary replacement free ℤ-module, no external
axiom, no Gray lift into the independent Kuu basis, and no F55/F68/F77
higher-dimensional obstruction cancellation is assumed.
-/

namespace KUOS.F112ActualHistoricalF36F40BridgeP4
namespace GenuineOriginalC60Geometry

open CategoryTheory Limits
open KUOS.DependentOriginationGrayC60NativeH2FundamentalClassV5_161
open KUOS.DependentOriginationGrayC60NativeChainComplexV5_160

set_option autoImplicit false
set_option warningAsError true
noncomputable section

/-- Any actual independent C60 second homology class is its
certified north-pentagon integer coordinate times the original
P17 fundamental class, not an abstract chosen generator. -/
theorem p22IndependentH2Class_reconstruction
    (x : independentC60IntegralCellularComplex.homology 2) :
    x = (independentC60H2IsoInteger.hom.hom x) •
      independentC60H2FundamentalClass := by
  apply (ModuleCat.mono_iff_injective
    independentC60H2IsoInteger.hom).mp inferInstance
  change independentC60H2IsoInteger.hom.hom x =
    independentC60H2IsoInteger.hom.hom
      ((independentC60H2IsoInteger.hom.hom x) •
        independentC60H2FundamentalClass)
  have hs :
      independentC60H2IsoInteger.hom.hom
          ((independentC60H2IsoInteger.hom.hom x) •
            independentC60H2FundamentalClass) =
        (independentC60H2IsoInteger.hom.hom x) •
          independentC60H2IsoInteger.hom.hom
            independentC60H2FundamentalClass := by
    simpa only [Int.cast_smul_eq_zsmul] using
      (map_intCast_smul (independentC60H2IsoInteger.hom.hom)
        ℤ ℤ (independentC60H2IsoInteger.hom.hom x)
        independentC60H2FundamentalClass)
  rw [hs, independentC60H2FundamentalClass_coordinate]
  simp

/-- The original historical F59 H₂ class is reconstructed from its
actual transported integer coordinate with the opposite fundamental
orientation, because that historical generator has coordinate -1. -/
theorem p22HistoricalH2Class_reconstruction
    (y : c60NativeIntegralCellularComplex.homology 2) :
    y = (-(historicalC60H2IsoInteger.hom.hom y)) •
      c60NativeH2FundamentalClass := by
  apply (ModuleCat.mono_iff_injective
    historicalC60H2IsoInteger.hom).mp inferInstance
  change historicalC60H2IsoInteger.hom.hom y =
    historicalC60H2IsoInteger.hom.hom
      ((-(historicalC60H2IsoInteger.hom.hom y)) •
        c60NativeH2FundamentalClass)
  have hs :
      historicalC60H2IsoInteger.hom.hom
          ((-(historicalC60H2IsoInteger.hom.hom y)) •
            c60NativeH2FundamentalClass) =
        (-(historicalC60H2IsoInteger.hom.hom y)) •
          historicalC60H2IsoInteger.hom.hom
            c60NativeH2FundamentalClass := by
    simpa only [Int.cast_smul_eq_zsmul] using
      (map_intCast_smul (historicalC60H2IsoInteger.hom.hom)
        ℤ ℤ (-(historicalC60H2IsoInteger.hom.hom y))
        c60NativeH2FundamentalClass)
  rw [hs, p21HistoricalFundamentalClass_coordinate]
  simp

/-- The actual signed C60 chain-level equivalence induces an H₂
isomorphism that preserves the independently defined integral
coordinate even though it sends the original historical fundamental
class to the negative of the native fundamental class. -/
theorem p22IndependentHistoricalH2_coordinate_naturality
    (x : independentC60IntegralCellularComplex.homology 2) :
    historicalC60H2IsoInteger.hom.hom
        (independentHistoricalC60H2Iso.hom.hom x) =
      independentC60H2IsoInteger.hom.hom x := by
  change independentC60H2IsoInteger.hom.hom
    (independentHistoricalC60H2Iso.inv.hom
      (independentHistoricalC60H2Iso.hom.hom x)) =
        independentC60H2IsoInteger.hom.hom x
  rw [independentHistoricalC60H2Iso.hom_inv_id_apply]

/-- Fully natural oriented C60 H₂ theorem for ANY actual native
homology class x: the actual induced historical H₂ map equals its
native integer north-face coordinate with reversed historical
fundamental orientation. This strengthens the P21 integer-multiple
theorem to all categorical homology classes, not only the generator. -/
theorem p22IndependentHistoricalH2_sign_all
    (x : independentC60IntegralCellularComplex.homology 2) :
    independentHistoricalC60H2Iso.hom.hom x =
      (-(independentC60H2IsoInteger.hom.hom x)) •
        c60NativeH2FundamentalClass := by
  let n : ℤ := independentC60H2IsoInteger.hom.hom x
  have hx : x = n • independentC60H2FundamentalClass :=
    p22IndependentH2Class_reconstruction x
  calc
    independentHistoricalC60H2Iso.hom.hom x =
      independentHistoricalC60H2Iso.hom.hom
        (n • independentC60H2FundamentalClass) :=
          congrArg (fun z : independentC60IntegralCellularComplex.homology 2 =>
            independentHistoricalC60H2Iso.hom.hom z) hx
    _ = (-n) • c60NativeH2FundamentalClass :=
      p21IndependentHistoricalH2_sign_smul n

#print axioms p22IndependentH2Class_reconstruction
#print axioms p22HistoricalH2Class_reconstruction
#print axioms p22IndependentHistoricalH2_coordinate_naturality
#print axioms p22IndependentHistoricalH2_sign_all

end
end GenuineOriginalC60Geometry
end KUOS.F112ActualHistoricalF36F40BridgeP4
