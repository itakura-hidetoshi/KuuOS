import KUOS.DependentOriginationGrayC60NativeH1ContractingHomotopyV5_164
import KUOS.DependentOriginationGrayC60NativeH2InfiniteOrderV5_161
import Mathlib.Algebra.Homology.ShortComplex.ModuleCat

namespace KUOS.DependentOriginationGrayC60NativeH2CompleteV5_165

open CategoryTheory Limits
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayC60IntegerOrientedSurfaceCycleV5_159
open KUOS.DependentOriginationGrayC60IntegralBoundaryLinearMapV5_159
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationGrayC60NativeChainComplexV5_160
open KUOS.DependentOriginationGrayC60NativeH2FundamentalClassV5_161
open KUOS.DependentOriginationGrayC60NativeH2InfiniteOrderV5_161
open KUOS.DependentOriginationGrayC60NativeH1ContractingHomotopyV5_164

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F17 / v5.165 — COMPLETE native integral C60 H₂ classification

F59-F16 established a genuine integral chain contraction in degree one using
an actual 59-edge spanning tree and its complementary 31-edge dual tree of
the 60-dart, 90-edge, 32-face C60 cellular complex.

Here we reuse EXACTLY that existing dual-tree face-fill map Q and the
original all-32-face oriented fundamental cycle F. We kernel-check a new
32×32 integer matrix identity from the physical face boundary lists:
  Q d₂ + F ρ = id_C₂,
where ρ extracts the coefficient of the ORIGINAL north-pentagon face.
On actual integral 2-cycles, this gives z = ρ(z) F.

We then transport this equality through the already-proved mathlib native
H₂-to-concrete-cycle isomorphism, which uses the genuine zero incoming d₃.
The two existing split linear maps (native fundamental class and north-face
coefficient) become mutual inverses. The real native Mathlib homology H₂ of
the physical C60 complex is isomorphic, as an integer module, to ℤ.

No geometric homeomorphism C60≅S², F55 global Gray 3-functor, or historic
Stage-II omega identification is claimed.
-/

/-- The coefficient of an actual oriented C60 face in the existing
F59-F16 dual-tree face filling attached to one physical edge. -/
def c60F17DualFaceCoefficient
    (e : TruncatedIcosahedralEdge)
    (g : TruncatedIcosahedralSeedFace) : ℤ :=
  ((c60F16DualFaceFillList e).map
    (fun p => if p.1 = g then p.2 else (0 : ℤ))).sum

/-- The coefficient at face g after filling the original oriented
boundary of another face f using F59-F16 dual cuts. -/
def c60F17FaceReconstructionCoefficient
    (f g : TruncatedIcosahedralSeedFace) : ℤ :=
  ((c60IntegerOrientedFaceBoundary f).map
    (fun p => p.2 * c60F17DualFaceCoefficient p.1 g)).sum

/-- Real original 32×32 integer face certificate: applying dual
tree filling to a face boundary produces the given face, except
that the north-pentagon face produces itself minus the complete
oriented fundamental surface. This is fully kernel-checkable,
not native_decide or a numerical rank assumption. -/
theorem c60F17FiniteFaceReconstructionCertificate :
    ∀ f g : TruncatedIcosahedralSeedFace,
      c60F17FaceReconstructionCoefficient f g +
        (if f = .aroundVertex .north then (1 : ℤ) else 0) =
          (if f = g then (1 : ℤ) else 0) := by
  decide

/-- All genuine signed C60 face coefficients sum in the original
integer free abelian 2-chain module. -/
theorem c60F17SignedFaceList_apply
    (l : List (TruncatedIcosahedralSeedFace × ℤ))
    (f : TruncatedIcosahedralSeedFace) :
    ((l.map (fun p =>
      (Finsupp.single p.1 p.2 : C60IntegralTwoChains))).sum) f =
        (l.map (fun p => if p.1 = f then p.2 else (0 : ℤ))).sum := by
  induction l with
  | nil => simp
  | cons p ps ih =>
      simp [List.sum_cons, Finsupp.single_apply, ih, eq_comm]

/-- Evaluate the existing dual cut 2-chain at an actual face. -/
theorem c60F17FaceFill_apply (e : TruncatedIcosahedralEdge)
    (g : TruncatedIcosahedralSeedFace) :
    c60F16FaceFill e g = c60F17DualFaceCoefficient e g :=
  c60F17SignedFaceList_apply _ _

/-- A physical signed list of original edges is sent by Q to
the corresponding signed sum of ORIGINAL dual-tree face fillings. -/
theorem c60F17SignedEdgeListFill_apply
    (l : List (TruncatedIcosahedralEdge × ℤ))
    (g : TruncatedIcosahedralSeedFace) :
    (c60F16FaceFillLift
      ((l.map (fun p =>
        (Finsupp.single p.1 p.2 : C60IntegralOneChains))).sum)) g =
        (l.map (fun p =>
          p.2 * c60F17DualFaceCoefficient p.1 g)).sum := by
  induction l with
  | nil => simp
  | cons p ps ih =>
      simp only [List.map_cons, List.sum_cons, map_add, Finsupp.add_apply]
      rw [ih, c60F16FaceFillLift_single]
      simp [c60F17FaceFill_apply]

/-- A real face basis boundary, after applying F59-F16's Q,
has the coefficients stated by the original oriented face list. -/
theorem c60F17FaceBoundaryFill_apply
    (f g : TruncatedIcosahedralSeedFace) :
    (c60F16FaceFillLift
      (c60IntegralBoundaryTwo (Finsupp.single f (1 : ℤ)))) g =
        c60F17FaceReconstructionCoefficient f g := by
  rw [c60IntegralBoundaryTwo_singleFace,
    c60IntegerFaceBoundaryChain_asSignedList]
  exact c60F17SignedEdgeListFill_apply _ _

/-- Evaluation at the genuine north-pentagon generator, Z-linear
on the original free integer 2-chains. -/
def c60F17NorthFaceCoefficient :
    C60IntegralTwoChains →ₗ[ℤ] ℤ :=
  Finsupp.lapply (.aroundVertex .north)

/-- Embed an arbitrary integer as that multiple of the existing,
globally oriented, ORIGINAL 32-face fundamental cycle. -/
def c60F17FundamentalSurfaceEmbedding :
    ℤ →ₗ[ℤ] C60IntegralTwoChains :=
  LinearMap.toSpanSingleton ℤ C60IntegralTwoChains
    c60IntegralFundamentalSurfaceChain

/-- The north-face coefficient of every physical basis face. -/
theorem c60F17NorthFaceCoefficient_single
    (f : TruncatedIcosahedralSeedFace) (z : ℤ) :
    c60F17NorthFaceCoefficient (Finsupp.single f z) =
      (if f = .aroundVertex .north then z else 0) := by
  simp [c60F17NorthFaceCoefficient, Finsupp.single_apply]

/-- Every face of the oriented all-32-face fundamental surface
has coefficient exactly +1, even after integer multiplication. -/
theorem c60F17FundamentalSurfaceEmbedding_apply
    (z : ℤ) (g : TruncatedIcosahedralSeedFace) :
    c60F17FundamentalSurfaceEmbedding z g = z := by
  rw [c60F17FundamentalSurfaceEmbedding,
    LinearMap.toSpanSingleton_apply, Finsupp.smul_apply,
    c60IntegralFundamentalSurfaceChain_coeff]
  simp

/-- Basiswise genuine integer degree-two chain contraction:
Q d₂ f + F ρ(f) = f on each of the thirty-two ACTUAL faces. -/
theorem c60F17FaceBasisReconstruction
    (f : TruncatedIcosahedralSeedFace) :
    c60F16FaceFillLift
        (c60IntegralBoundaryTwo (Finsupp.single f (1 : ℤ))) +
      c60F17FundamentalSurfaceEmbedding
        (c60F17NorthFaceCoefficient (Finsupp.single f (1 : ℤ))) =
          Finsupp.single f (1 : ℤ) := by
  apply Finsupp.ext
  intro g
  rw [Finsupp.add_apply, c60F17FaceBoundaryFill_apply,
    c60F17FundamentalSurfaceEmbedding_apply,
    c60F17NorthFaceCoefficient_single]
  simpa only [Finsupp.single_apply] using
    c60F17FiniteFaceReconstructionCertificate f g

/-- FULL integral C60 degree-two contracting identity, stated
as equality of Z-LINEAR MAPS on EVERY signed original 2-chain. -/
theorem c60F17TwoChainReconstruction :
    c60F16FaceFillLift.comp c60IntegralBoundaryTwo +
      c60F17FundamentalSurfaceEmbedding.comp c60F17NorthFaceCoefficient =
        LinearMap.id := by
  apply Finsupp.lhom_ext
  intro f z
  change c60F16FaceFillLift
      (c60IntegralBoundaryTwo (Finsupp.single f z)) +
    c60F17FundamentalSurfaceEmbedding
      (c60F17NorthFaceCoefficient (Finsupp.single f z)) =
        Finsupp.single f z
  have hs : (Finsupp.single f z : C60IntegralTwoChains) =
      z • Finsupp.single f (1 : ℤ) := by simp
  rw [hs, map_smul, map_smul, map_smul, map_smul,
    ← smul_add, c60F17FaceBasisReconstruction]

/-- Any real integer 2-cycle is EXACTLY its north-pentagon
integer coefficient times the original oriented fundamental surface. -/
theorem c60F17EveryTwoCycle_isFundamental
    (x : C60IntegralTwoChains)
    (hx : c60IntegralBoundaryTwo x = 0) :
    x = c60F17FundamentalSurfaceEmbedding
      (c60F17NorthFaceCoefficient x) := by
  have h := LinearMap.congr_fun c60F17TwoChainReconstruction x
  simp only [LinearMap.add_apply, LinearMap.comp_apply,
    LinearMap.id_apply] at h
  rw [hx, map_zero, zero_add] at h
  exact h.symm

/-- The original formal H₂ cycle-to-ker(d₂) isomorphism really
decodes an element of the original C60 signed 2-cycle kernel. -/
theorem c60F17NativeH2Representative_boundary_zero
    (h : c60NativeIntegralCellularComplex.homology 2) :
    c60IntegralBoundaryTwo
        (c60NativeH2ConcreteCycleIso.hom.hom h).val = 0 := by
  have hh := (c60NativeH2ConcreteCycleIso.hom.hom h).property
  change (c60NativeIntegralCellularComplex.sc 2).g.hom
    (c60NativeH2ConcreteCycleIso.hom.hom h).val = 0 at hh
  change (c60NativeIntegralCellularComplex.d 2
    ((ComplexShape.down ℕ).next 2)).hom
      (c60NativeH2ConcreteCycleIso.hom.hom h).val = 0 at hh
  have hn : (ComplexShape.down ℕ).next 2 = 1 := by simp
  rw [hn, c60NativeIntegralCellularComplex_d21] at hh
  exact hh

/-- INVERSE COMPOSITION MISSING FROM F59-F13: the genuine native
fundamental-class map followed by north-face coefficient recovery
also acts as identity on ALL native Mathlib H₂ classes.
The proof transports the actual 32-face reconstruction, not
an assumed homological rank or external sphere identification. -/
theorem c60NativeH2FundamentalLinear_rightInverse :
    c60NativeH2FundamentalLinear.comp
      c60NativeH2NorthPentagonCoefficient = LinearMap.id := by
  apply LinearMap.ext
  intro h
  change c60NativeH2FundamentalLinear
    (c60NativeH2NorthPentagonCoefficient h) = h
  apply c60NativeH2ConcreteCycleIso.toLinearEquiv.injective
  change c60NativeH2ConcreteCycleIso.hom.hom
      (c60NativeH2FundamentalLinear (c60NativeH2NorthPentagonCoefficient h)) =
    c60NativeH2ConcreteCycleIso.hom.hom h
  rw [c60NativeH2FundamentalLinear_apply, map_smul,
    c60NativeH2ConcreteCycleIso_fundamental]
  apply Subtype.ext
  have hrec := c60F17EveryTwoCycle_isFundamental
    (c60NativeH2ConcreteCycleIso.hom.hom h).val
    (c60F17NativeH2Representative_boundary_zero h)
  change (c60NativeH2NorthPentagonCoefficient h •
    c60IntegralFundamentalSurfaceChain) =
    (c60NativeH2ConcreteCycleIso.hom.hom h).val
  simpa only [c60NativeH2NorthPentagonCoefficient,
    c60F17NorthFaceCoefficient, c60F17FundamentalSurfaceEmbedding,
    LinearMap.toSpanSingleton_apply,
    LinearMap.comp_apply, LinearMap.ker_subtype_apply] using hrec.symm

/-- The north-pentagon coordinate is BOTH injective and surjective
on the actual native degree-two C60 homology object. -/
theorem c60NativeH2NorthPentagonCoefficient_bijective :
    Function.Bijective c60NativeH2NorthPentagonCoefficient := by
  constructor
  · intro a b hab
    have h := congrArg c60NativeH2FundamentalLinear hab
    simpa only [← LinearMap.comp_apply,
      c60NativeH2FundamentalLinear_rightInverse,
      LinearMap.id_apply] using h
  · intro z
    refine ⟨c60NativeH2FundamentalLinear z, ?_⟩
    have h := LinearMap.congr_fun
      c60NativeH2FundamentalLinear_split z
    simpa only [LinearMap.comp_apply, LinearMap.id_apply] using h

/-- F59-F17 MAIN RESULT: genuine original C60 native Mathlib H₂,
not an external abstract combinatorial surrogate, IS Z as an
integer module, with inverse given by its fundamental surface class. -/
noncomputable def c60NativeH2IsoInteger :
    c60NativeIntegralCellularComplex.homology 2 ≅ ModuleCat.of ℤ ℤ :=
  (LinearEquiv.ofBijective c60NativeH2NorthPentagonCoefficient
    c60NativeH2NorthPentagonCoefficient_bijective).toModuleIso

#print axioms c60F17FiniteFaceReconstructionCertificate
#print axioms c60F17SignedFaceList_apply
#print axioms c60F17FaceBoundaryFill_apply
#print axioms c60F17NorthFaceCoefficient_single
#print axioms c60F17FundamentalSurfaceEmbedding_apply
#print axioms c60F17FaceBasisReconstruction
#print axioms c60F17TwoChainReconstruction
#print axioms c60F17EveryTwoCycle_isFundamental
#print axioms c60NativeH2FundamentalLinear_rightInverse
#print axioms c60NativeH2IsoInteger

end
end KUOS.DependentOriginationGrayC60NativeH2CompleteV5_165
