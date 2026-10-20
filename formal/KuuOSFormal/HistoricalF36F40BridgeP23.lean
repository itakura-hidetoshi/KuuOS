import KuuOSFormal.HistoricalF36F40BridgeP22
import Mathlib.LinearAlgebra.Finsupp.LSum

/-!
# F112-P23 — fully native C60 integer 0/1 carriers and chain comparison

Unlike P17, this complex uses independent Kuu `Dart`, `Edge`, and
`Polygon` in degrees 0, 1, and 2, respectively. The first boundary
is defined directly by the ordered endpoints of each native physical
edge. The second boundary is explicitly defined on the native edge
basis by the genuine native polygon orientation coefficients verified
in P10–P14.

The already proved constructor-level vertex/edge equivalences and their
endpoint compatibility certify the two commuting squares, hence the
full chain isomorphism with P17 and the signed all-class H₂ theorem.
There are no invented vertices, edges, faces or 3-cells. This does not
construct F47/F55 source 3-Homs or cancel higher descent obstructions.
-/

namespace KUOS.F112ActualHistoricalF36F40BridgeP4
namespace GenuineOriginalC60Geometry

open CategoryTheory Limits
open Kuu.F112.Physical
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayC60IntegralBoundaryLinearMapV5_159
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationGrayC60NativeChainComplexV5_160
open KUOS.DependentOriginationGrayC60NativeH2FundamentalClassV5_161

set_option autoImplicit false
set_option warningAsError true
noncomputable section

/-- True independent Kuu 60-dart integral zero-chains. -/
abbrev p23NativeZeroChains := Dart →₀ ℤ

/-- True independent Kuu 90-edge integral one-chains. -/
abbrev p23NativeOneChains := Edge →₀ ℤ

/-- Constructor-wise transport of each native dart, NOT a rank-count bijection. -/
def p23NativeZeroToHistorical :
    p23NativeZeroChains ≃ₗ[ℤ] C60IntegralZeroChains :=
  Finsupp.domLCongr dartEquiv

/-- Constructor-wise transport of each native physical edge. -/
def p23NativeOneToHistorical :
    p23NativeOneChains ≃ₗ[ℤ] C60IntegralOneChains :=
  Finsupp.domLCongr edgeEquiv

/-- Real native edge boundary, terminal dart minus initial dart. -/
def p23NativeEdgeBoundary (e : Edge) : p23NativeZeroChains :=
  Finsupp.single (edgeEndpoints e).2 (1 : ℤ) -
    Finsupp.single (edgeEndpoints e).1 (1 : ℤ)

/-- The independently defined integer boundary d₁ on ALL native edges. -/
def p23NativeBoundaryOne :
    p23NativeOneChains →ₗ[ℤ] p23NativeZeroChains :=
  Finsupp.linearCombination ℤ p23NativeEdgeBoundary

theorem p23NativeBoundaryOne_single (e : Edge) (z : ℤ) :
    p23NativeBoundaryOne (Finsupp.single e z) =
      z • p23NativeEdgeBoundary e := by
  simp [p23NativeBoundaryOne]

/-- Strong endpoint-level compatibility on each genuine native edge. -/
theorem p23NativeEdgeBoundary_transport (e : Edge) :
    p23NativeZeroToHistorical (p23NativeEdgeBoundary e) =
      c60IntegralEdgeBoundaryChain (edgeEquiv e) := by
  change (Finsupp.domLCongr dartEquiv)
      (Finsupp.single (edgeEndpoints e).2 (1 : ℤ) -
        Finsupp.single (edgeEndpoints e).1 (1 : ℤ)) =
    Finsupp.single
      (truncatedIcosahedralEdgeEndpoints (edgeEquiv e)).2 (1 : ℤ) -
      Finsupp.single
        (truncatedIcosahedralEdgeEndpoints (edgeEquiv e)).1 (1 : ℤ)
  rw [map_sub, Finsupp.domLCongr_single, Finsupp.domLCongr_single,
    ← (edgeEndpoints_equiv e).2, ← (edgeEndpoints_equiv e).1]

/-- The degree-one integral boundary square commutes on EVERY 1-chain,
not just on one edge generator. -/
theorem p23NativeBoundaryOne_commutes :
    p23NativeZeroToHistorical.toLinearMap.comp p23NativeBoundaryOne =
      c60IntegralBoundaryOne.comp p23NativeOneToHistorical.toLinearMap := by
  apply Finsupp.lhom_ext
  intro e z
  change p23NativeZeroToHistorical
      (p23NativeBoundaryOne (Finsupp.single e z)) =
    c60IntegralBoundaryOne
      (p23NativeOneToHistorical (Finsupp.single e z))
  calc
    p23NativeZeroToHistorical
        (p23NativeBoundaryOne (Finsupp.single e z)) =
      z • p23NativeZeroToHistorical (p23NativeEdgeBoundary e) := by
        rw [p23NativeBoundaryOne_single, map_smul]
    _ = z • c60IntegralEdgeBoundaryChain (edgeEquiv e) := by
      rw [p23NativeEdgeBoundary_transport]
    _ = c60IntegralBoundaryOne
        (p23NativeOneToHistorical (Finsupp.single e z)) := by
      change z • c60IntegralEdgeBoundaryChain (edgeEquiv e) =
        c60IntegralBoundaryOne
          ((Finsupp.domLCongr edgeEquiv) (Finsupp.single e z))
      rw [Finsupp.domLCongr_single, c60IntegralBoundaryOne_singleEdge]

/-- The signed five-/six-sided native polygon boundary expressed
directly in the native 90-edge coefficient type. The coefficient is
computed from the certified native polygon orientation (P10–P14). -/
def p23NativeFaceBoundary (p : Polygon) : p23NativeOneChains :=
  Finsupp.onFinset Finset.univ
    (fun e : Edge => faceOrientedEdgeCoefficient p (edgeEquiv e))
    (by intro e _; exact Finset.mem_univ e)

/-- Exact coordinate match with P14's independently constructed
polygon boundary; no historical face basis is substituted. -/
theorem p23NativeFaceBoundary_transport (p : Polygon) :
    p23NativeOneToHistorical (p23NativeFaceBoundary p) =
      nativeC60OrientedFaceBoundary p := by
  apply Finsupp.ext
  intro e
  change ((Finsupp.domLCongr edgeEquiv) (p23NativeFaceBoundary p)) e =
    nativeC60OrientedFaceBoundary p e
  simp only [Finsupp.domLCongr_apply, Finsupp.domCongr_apply,
    Finsupp.equivMapDomain_apply]
  simp [p23NativeFaceBoundary, nativeC60OrientedFaceBoundary]

/-- True native 32-polygon to 90-native-edge integral boundary d₂. -/
def p23NativeBoundaryTwo :
    NativeC60IntegralTwoChains →ₗ[ℤ] p23NativeOneChains :=
  Finsupp.linearCombination ℤ p23NativeFaceBoundary

theorem p23NativeBoundaryTwo_single (p : Polygon) (z : ℤ) :
    p23NativeBoundaryTwo (Finsupp.single p z) =
      z • p23NativeFaceBoundary p := by
  simp [p23NativeBoundaryTwo]

/-- Second commuting boundary square on arbitrary native 2-chains. -/
theorem p23NativeBoundaryTwo_commutes :
    p23NativeOneToHistorical.toLinearMap.comp p23NativeBoundaryTwo =
      nativeC60IntegralBoundaryTwo := by
  apply Finsupp.lhom_ext
  intro p z
  change p23NativeOneToHistorical
      (p23NativeBoundaryTwo (Finsupp.single p z)) =
    nativeC60IntegralBoundaryTwo (Finsupp.single p z)
  calc
    p23NativeOneToHistorical
        (p23NativeBoundaryTwo (Finsupp.single p z)) =
      z • p23NativeOneToHistorical (p23NativeFaceBoundary p) := by
        rw [p23NativeBoundaryTwo_single, map_smul]
    _ = z • nativeC60OrientedFaceBoundary p := by
      rw [p23NativeFaceBoundary_transport]
    _ = nativeC60IntegralBoundaryTwo (Finsupp.single p z) := by
      rw [nativeC60IntegralBoundaryTwo_single]

/-- The genuine native endpoint boundary of every native polygon
boundary vanishes; a consequence of both proved commuting squares. -/
theorem p23NativeBoundaryOne_comp_boundaryTwo_zero :
    p23NativeBoundaryOne.comp p23NativeBoundaryTwo = 0 := by
  apply LinearMap.ext
  intro c
  apply p23NativeZeroToHistorical.injective
  rw [map_zero]
  calc
    p23NativeZeroToHistorical
        ((p23NativeBoundaryOne.comp p23NativeBoundaryTwo) c) =
      c60IntegralBoundaryOne
        (p23NativeOneToHistorical (p23NativeBoundaryTwo c)) := by
          have h := congrArg
            (fun L : p23NativeOneChains →ₗ[ℤ] C60IntegralZeroChains =>
              L (p23NativeBoundaryTwo c)) p23NativeBoundaryOne_commutes
          simpa only [LinearMap.comp_apply] using h
    _ = c60IntegralBoundaryOne (nativeC60IntegralBoundaryTwo c) := by
          have h := congrArg
            (fun L : NativeC60IntegralTwoChains →ₗ[ℤ] C60IntegralOneChains =>
              L c) p23NativeBoundaryTwo_commutes
          simpa only [LinearMap.comp_apply] using
            congrArg (fun v : C60IntegralOneChains =>
              c60IntegralBoundaryOne v) h
    _ = 0 := by
          have h := congrArg
            (fun L : NativeC60IntegralTwoChains →ₗ[ℤ] C60IntegralZeroChains =>
              L c) originalBoundaryOne_comp_nativeBoundaryTwo_zero
          simpa only [LinearMap.comp_apply, LinearMap.zero_apply] using h

/-- Entire native C60 cellular degree system, with native
Dart/Edge/Polygon in degrees 0/1/2 and no invented degree-3 cells. -/
def p23FullyNativeChainObjects : ℕ → ModuleCat ℤ
  | 0 => ModuleCat.of ℤ p23NativeZeroChains
  | 1 => ModuleCat.of ℤ p23NativeOneChains
  | 2 => ModuleCat.of ℤ NativeC60IntegralTwoChains
  | _ + 3 => ModuleCat.of ℤ PUnit

def p23FullyNativeChainDifferential :
    ∀ n : ℕ, p23FullyNativeChainObjects (n + 1) ⟶
      p23FullyNativeChainObjects n
  | 0 => ModuleCat.ofHom p23NativeBoundaryOne
  | 1 => ModuleCat.ofHom p23NativeBoundaryTwo
  | _ + 2 => 0

theorem p23FullyNativeDifferential_comp_zero (n : ℕ) :
    p23FullyNativeChainDifferential (n + 1) ≫
      p23FullyNativeChainDifferential n = 0 := by
  cases n with
  | zero =>
      apply ModuleCat.hom_ext
      exact p23NativeBoundaryOne_comp_boundaryTwo_zero
  | succ n =>
      cases n <;> simp [p23FullyNativeChainDifferential]

/-- Fully native C60 three-term integer chain complex in Mathlib. -/
def p23FullyNativeIntegralCellularComplex :
    ChainComplex (ModuleCat ℤ) ℕ :=
  ChainComplex.of p23FullyNativeChainObjects
    p23FullyNativeChainDifferential p23FullyNativeDifferential_comp_zero

/-- Degreewise true type change: darts, edges and identity on polygons. -/
def p23FullyNativeIndependentDegreeIso :
    (n : ℕ) →
      p23FullyNativeIntegralCellularComplex.X n ≅
        independentC60IntegralCellularComplex.X n
  | 0 => p23NativeZeroToHistorical.toModuleIso
  | 1 => p23NativeOneToHistorical.toModuleIso
  | 2 => Iso.refl _
  | _ + 3 => Iso.refl _

/-- Both new physical boundary squares are EXACTLY the compatibility
equations for a Mathlib chain-complex isomorphism. -/
theorem p23FullyNativeIndependentDegreeIso_comm (n : ℕ) :
    (p23FullyNativeIndependentDegreeIso (n + 1)).hom ≫
      independentC60ChainDifferential n =
    p23FullyNativeChainDifferential n ≫
      (p23FullyNativeIndependentDegreeIso n).hom := by
  cases n with
  | zero =>
      apply ModuleCat.hom_ext
      change c60IntegralBoundaryOne.comp
          p23NativeOneToHistorical.toLinearMap =
        p23NativeZeroToHistorical.toLinearMap.comp p23NativeBoundaryOne
      exact p23NativeBoundaryOne_commutes.symm
  | succ n =>
      cases n with
      | zero =>
          apply ModuleCat.hom_ext
          change nativeC60IntegralBoundaryTwo =
            p23NativeOneToHistorical.toLinearMap.comp p23NativeBoundaryTwo
          exact p23NativeBoundaryTwo_commutes.symm
      | succ n =>
          apply ModuleCat.hom_ext
          apply LinearMap.ext
          intro c
          simp [p23FullyNativeIndependentDegreeIso,
            independentC60ChainDifferential, p23FullyNativeChainDifferential]
          rfl

/-- Genuine full chain isomorphism from fully native C60 physical
cells to P17's mixed-carrier (native face) presentation. -/
def p23FullyNativeIndependentChainIso :
    p23FullyNativeIntegralCellularComplex ≅
      independentC60IntegralCellularComplex :=
  HomologicalComplex.Hom.isoOfComponents
    p23FullyNativeIndependentDegreeIso
    (by
      intro i j hij
      change j + 1 = i at hij
      subst i
      simpa only [p23FullyNativeIntegralCellularComplex,
        independentC60IntegralCellularComplex, ChainComplex.of_d]
        using p23FullyNativeIndependentDegreeIso_comm j)

/-- Compose with P18: the historical F59 complex is isomorphic
to the fully independently typed physical C60 chain complex. -/
def p23FullyNativeHistoricalChainIso :
    p23FullyNativeIntegralCellularComplex ≅
      c60NativeIntegralCellularComplex :=
  p23FullyNativeIndependentChainIso ≪≫ independentHistoricalC60ChainIso

/-- The new native complex has genuine categorical H₂ ≅ Z,
through its proven full physical chain isomorphism, not a rank proxy. -/
def p23FullyNativeIndependentH2Iso :
    p23FullyNativeIntegralCellularComplex.homology 2 ≅
      independentC60IntegralCellularComplex.homology 2 :=
  HomologicalComplex.homologyMapIso p23FullyNativeIndependentChainIso 2

def p23FullyNativeH2IsoInteger :
    p23FullyNativeIntegralCellularComplex.homology 2 ≅
      ModuleCat.of ℤ ℤ :=
  p23FullyNativeIndependentH2Iso ≪≫ independentC60H2IsoInteger

/-- The actual historical H₂ comparison, constructed from the two
existing functorially induced homology isomorphisms. -/
def p23FullyNativeHistoricalH2Iso :
    p23FullyNativeIntegralCellularComplex.homology 2 ≅
      c60NativeIntegralCellularComplex.homology 2 :=
  p23FullyNativeIndependentH2Iso ≪≫ independentHistoricalC60H2Iso

/-- Mathlib's homology functor proves that this composed H₂ map is
exactly the map induced by the composed, fully native chain isomorphism. -/
theorem p23FullyNativeHistoricalH2Iso_homologyMap :
    p23FullyNativeHistoricalH2Iso.hom =
      (HomologicalComplex.homologyMapIso
        p23FullyNativeHistoricalChainIso 2).hom := by
  change
    HomologicalComplex.homologyMap
        p23FullyNativeIndependentChainIso.hom 2 ≫
      HomologicalComplex.homologyMap
        independentHistoricalC60ChainIso.hom 2 =
      HomologicalComplex.homologyMap
        (p23FullyNativeIndependentChainIso.hom ≫
          independentHistoricalC60ChainIso.hom) 2
  exact (HomologicalComplex.homologyMap_comp
    p23FullyNativeIndependentChainIso.hom
    independentHistoricalC60ChainIso.hom 2).symm

/-- Preserve P22's original signed naturality for EVERY H₂ class
after replacing both lower chain carriers by genuine independent types. -/
theorem p23FullyNativeHistoricalH2_sign_all
    (x : p23FullyNativeIntegralCellularComplex.homology 2) :
    p23FullyNativeHistoricalH2Iso.hom.hom x =
      (-(p23FullyNativeH2IsoInteger.hom.hom x)) •
        c60NativeH2FundamentalClass := by
  change independentHistoricalC60H2Iso.hom.hom
      (p23FullyNativeIndependentH2Iso.hom.hom x) =
    (-(independentC60H2IsoInteger.hom.hom
      (p23FullyNativeIndependentH2Iso.hom.hom x))) •
        c60NativeH2FundamentalClass
  exact p22IndependentHistoricalH2_sign_all _

#print axioms p23NativeEdgeBoundary_transport
#print axioms p23NativeBoundaryOne_commutes
#print axioms p23NativeFaceBoundary_transport
#print axioms p23NativeBoundaryTwo_commutes
#print axioms p23NativeBoundaryOne_comp_boundaryTwo_zero
#print axioms p23FullyNativeIntegralCellularComplex
#print axioms p23FullyNativeIndependentChainIso
#print axioms p23FullyNativeHistoricalChainIso
#print axioms p23FullyNativeH2IsoInteger
#print axioms p23FullyNativeHistoricalH2Iso_homologyMap
#print axioms p23FullyNativeHistoricalH2_sign_all

end
end GenuineOriginalC60Geometry
end KUOS.F112ActualHistoricalF36F40BridgeP4
