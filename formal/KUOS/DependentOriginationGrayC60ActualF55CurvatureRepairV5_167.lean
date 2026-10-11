import KUOS.DependentOriginationGrayC60CochainDescentV5_166
import KUOS.DependentOriginationGrayC60NativeH1ContractingHomotopyV5_164
import KUOS.DependentOriginationGrayC60AllNinetyEdgePastingV5_157

namespace KUOS.DependentOriginationGrayC60ActualF55CurvatureRepairV5_167

open CategoryTheory Limits
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayF55PhaseRealizationV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60AllNinetyEdgePastingV5_157
open KUOS.DependentOriginationGrayC60IntegerOrientedSurfaceCycleV5_159
open KUOS.DependentOriginationGrayC60IntegralBoundaryLinearMapV5_159
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationGrayC60NativeH1ContractingHomotopyV5_164
open KUOS.DependentOriginationGrayC60CochainDescentV5_166
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 3000000
noncomputable section

/-!
# F59-F19 / v5.167 — complete ORIGINAL F55 square curvature and flat-repair geometry

This is a single mathematical classification, not a collection of tiny
claims: the ACTUAL ninety C60 incidence square labels of original F55
have an explicit nonzero oriented local face curvature, whose globally
oriented fundamental-surface obstruction vanishes. This curvature is
EXACT (not a nonzero H² class), but the original edge field does NOT
descend to a vertex potential (a genuine local descent obstruction).

All repairs which make this original edge field flat are classified by
the vertex-gauge coboundaries from F59-F18. A canonical repair is built
from the ORIGINAL F59-F16 integral 59-edge spanning tree: it preserves
all those 59 square labels and can change at most 31 original edge
labels. The statements are made in the independently constructed
F59 braided 3-cell target, where the additive group law is literally
native categorical 3-cell composition.

A distinct global Gray 3-functor, an original F55 source 3-cell
pasting, geometric S² homeomorphism, and Stage-II omega equality
are NOT inferred from these calculations.
-/

/-- Signed integer sum of the ORIGINAL actual 5/6-edge oriented
face boundary. This is the integer character tested by a uniform
F55 edge-square label; it is not the unoriented perimeter length. -/
def c60F19SignedBoundaryDegree
    (face : TruncatedIcosahedralSeedFace) : ℤ :=
  ((c60IntegerOrientedFaceBoundary face).map Prod.snd).sum

/-- Complete original C60 signed integer face pattern:
12 pentagons have ±5; the north/south hexagon caps have -2/+2;
the 10 belt hexagons have ZERO signed sum. -/
def c60F19ExpectedBoundaryDegree :
    TruncatedIcosahedralSeedFace → ℤ
  | .aroundVertex .north => -5
  | .aroundVertex .south => 5
  | .aroundVertex (.upper _) => 5
  | .aroundVertex (.lower _) => -5
  | .fromTriangle (.top _) => -2
  | .fromTriangle (.bottom _) => 2
  | .fromTriangle (.beltUpper _) => 0
  | .fromTriangle (.beltLower _) => 0

/-- Kernel-checked COMPLETE 32-face signed incidence calculation,
using the actual F59-F3 six-edge cycles and F59-F8 orientations.
No numerical rank postulate and no native_decide axiom. -/
theorem c60F19SignedBoundaryDegree_complete :
    ∀ f : TruncatedIcosahedralSeedFace,
      c60F19SignedBoundaryDegree f =
        c60F19ExpectedBoundaryDegree f := by
  decide

/-- The original F55 braided exchange-square generator, assigned
uniformly to all ninety actual physical edge squares, as proved
for the true F55-labelled C60 sources in F59-F2. -/
def c60F19UniformF55EdgeLabels :
    TruncatedIcosahedralEdge → GradedThreeCell 0 0 :=
  fun _ => originalF55BraidedSquareGenerator

/-- Z-linear original F55 square edge assignment on TRUE C60
integer one-chains, not an unrelated abstract curvature carrier. -/
def c60F19OriginalF55EdgeCochain :
    C60IntegralOneChains →ₗ[ℤ] GradedThreeCell 0 0 :=
  c60F18GrayEdgeCochain c60F19UniformF55EdgeLabels

/-- Original oriented pentagon/hexagon F55 square curvature. -/
def c60F19OriginalF55FaceCurvature
    (face : TruncatedIcosahedralSeedFace) : GradedThreeCell 0 0 :=
  c60F18SignedGrayFacePasting c60F19UniformF55EdgeLabels face

/-- Integer scalar sums of a fixed actual braided Gray 3-cell. -/
theorem c60F19SignedScalarList_sum
    (l : List (TruncatedIcosahedralEdge × ℤ))
    (g : GradedThreeCell 0 0) :
    (l.map (fun p => p.2 • g)).sum =
      (l.map Prod.snd).sum • g := by
  induction l with
  | nil => simp
  | cons p ps ih =>
      simp only [List.map_cons, List.sum_cons, ih, add_smul]

/-- Exact physical F55 local curvature: each oriented real face
pastes its square generator exactly its SIGNED boundary degree. -/
theorem c60F19OriginalF55FaceCurvature_eq
    (f : TruncatedIcosahedralSeedFace) :
    c60F19OriginalF55FaceCurvature f =
      c60F19SignedBoundaryDegree f •
        originalF55BraidedSquareGenerator := by
  exact c60F19SignedScalarList_sum
    (c60IntegerOrientedFaceBoundary f)
    originalF55BraidedSquareGenerator

/-- The genuinely original 12 pentagon/20 hexagon local curvature
classification, at the level of native braided Gray 3-cells. -/
theorem c60F19OriginalF55FaceCurvature_complete
    (f : TruncatedIcosahedralSeedFace) :
    c60F19OriginalF55FaceCurvature f =
      c60F19ExpectedBoundaryDegree f •
        originalF55BraidedSquareGenerator := by
  rw [c60F19OriginalF55FaceCurvature_eq,
    c60F19SignedBoundaryDegree_complete f]

/-- The second ORIGINAL F58 charge of an arbitrary integer multiple
of the F55 square generator equals that integer. In particular,
the generator has infinite additive order even though its braided
exchange phase has order two. -/
theorem c60F19OriginalF55Scalar_secondCharge (n : ℤ) :
    (n • originalF55BraidedSquareGenerator).charge.2 = n := by
  have h := grayNeutralChargeHom.map_zsmul originalF55BraidedSquareGenerator n
  have h' := congrArg Prod.snd h
  simpa [originalF55BraidedSquareGenerator_complete.1] using h'

/-- The original F59 braided exchange phase of an integer F55
multiple is its parity, completely independent of the unbounded
integer generator charge. -/
theorem c60F19OriginalF55Scalar_phase (n : ℤ) :
    (n • originalF55BraidedSquareGenerator).phase = (n : ZMod 2) := by
  have h := grayNeutralPhaseHom.map_zsmul originalF55BraidedSquareGenerator n
  simpa [originalF55BraidedSquareGenerator_complete.2,
    zsmul_eq_mul] using h

/-- Real local curvature has exact original F58 charge and F59 phase,
not just a claimed nonzero abstract holonomy. -/
theorem c60F19OriginalF55FaceCurvature_components
    (f : TruncatedIcosahedralSeedFace) :
    (c60F19OriginalF55FaceCurvature f).charge.2 =
      c60F19ExpectedBoundaryDegree f ∧
    (c60F19OriginalF55FaceCurvature f).phase =
      (c60F19ExpectedBoundaryDegree f : ZMod 2) := by
  rw [c60F19OriginalF55FaceCurvature_complete]
  exact ⟨c60F19OriginalF55Scalar_secondCharge _,
    c60F19OriginalF55Scalar_phase _⟩

/-- An F55 face is flat precisely when its actual ORIGINAL signed
degree is zero. The belt hexagons are flat, but all twelve
pentagons and the ten cap hexagons are nonflat. -/
theorem c60F19OriginalF55FaceCurvature_zero_iff
    (f : TruncatedIcosahedralSeedFace) :
    c60F19OriginalF55FaceCurvature f = 0 ↔
      c60F19ExpectedBoundaryDegree f = 0 := by
  constructor
  · intro h
    have heq := congrArg
      (fun g : GradedThreeCell 0 0 => g.charge.2) h
    simpa [c60F19OriginalF55FaceCurvature_components f |>.1] using heq
  · intro h
    rw [c60F19OriginalF55FaceCurvature_complete, h, zero_smul]

/-- The north-pentagon locally obstructs descent: the exact
oriented five F55 squares carry integer charge -5 and odd phase 1. -/
theorem c60F19NorthPentagon_curvature_nonzero :
    c60F19OriginalF55FaceCurvature (.aroundVertex .north) ≠ 0 := by
  intro h
  have hz :=
    (c60F19OriginalF55FaceCurvature_zero_iff
      (.aroundVertex .north)).mp h
  norm_num [c60F19ExpectedBoundaryDegree] at hz

/-- Original F55 square labels on the ACTUAL ninety physical
edges DO NOT descend to ANY vertex potential, since one
original geometric pentagon already violates local flatness. -/
theorem c60F19OriginalF55EdgeCochain_no_vertexGauge :
    ¬ ∃ φ : C60IntegralZeroChains →ₗ[ℤ] GradedThreeCell 0 0,
      c60F19OriginalF55EdgeCochain =
        φ.comp c60IntegralBoundaryOne := by
  intro h
  have hflat :=
    (c60F18ClosedEdgeIffVertexPotential
      c60F19OriginalF55EdgeCochain).mpr h
  have hh := LinearMap.congr_fun hflat
    (Finsupp.single (.aroundVertex .north) (1 : ℤ))
  have hzero :
      c60F19OriginalF55FaceCurvature (.aroundVertex .north) = 0 := by
    change c60F19OriginalF55EdgeCochain
      (c60IntegralBoundaryTwo (Finsupp.single
        (.aroundVertex .north) (1 : ℤ))) = 0 at hh
    rw [c60IntegralBoundaryTwo_singleFace] at hh
    exact (c60F18SignedGrayFacePasting_eq
      c60F19UniformF55EdgeLabels (.aroundVertex .north)).trans hh
  exact c60F19NorthPentagon_curvature_nonzero hzero

/-- The oriented TOTAL of all 32 actual F55 face curvatures is
ZERO as a genuine native braided Gray 3-cell. This is exactness
δ²=0, NOT local flatness; twelve pentagonal obstructions survive. -/
theorem c60F19TotalOrientedCurvature_zero :
    (∑ f : TruncatedIcosahedralSeedFace,
      c60F19OriginalF55FaceCurvature f) = 0 := by
  calc
    (∑ f : TruncatedIcosahedralSeedFace,
        c60F19OriginalF55FaceCurvature f) =
      ∑ f : TruncatedIcosahedralSeedFace,
        c60F19OriginalF55EdgeCochain
          (c60IntegerFaceBoundaryChain f) := by
            apply Finset.sum_congr rfl
            intro f _
            exact c60F18SignedGrayFacePasting_eq _ f
    _ = c60F19OriginalF55EdgeCochain
          c60IntegerFullSurfaceBoundaryChain := by
            simp [c60IntegerFullSurfaceBoundaryChain, map_sum]
    _ = 0 := by
          rw [c60IntegerFullSurfaceBoundaryChain_zero, map_zero]

/-- Thus the local nonzero F55 curvature is COHOMOLOGICALLY EXACT,
not a nonzero degree-two class or automatic Stage-II obstruction:
its total original C60 surface class has exactly zero obstruction. -/
theorem c60F19OriginalF55Curvature_globalObstruction_zero :
    c60F18GraySurfaceObstruction
      c60F19OriginalF55FaceCurvature = 0 := by
  rw [c60F18GraySurfaceObstruction_eq_sum]
  exact c60F19TotalOrientedCurvature_zero

/-! ## Full affine classification of flat repairs, not just cancellation -/

/-- The genuine flatness of the original F55 edge field after an
arbitrary signed Gray-square correction is equivalent to that
correction differing from -w by a vertex coboundary. -/
theorem c60F19CompleteFlatCorrectionClassification
    (k : C60IntegralOneChains →ₗ[ℤ] GradedThreeCell 0 0) :
    (c60F19OriginalF55EdgeCochain + k).comp
        c60IntegralBoundaryTwo = 0 ↔
      ∃ φ : C60IntegralZeroChains →ₗ[ℤ] GradedThreeCell 0 0,
        k = φ.comp c60IntegralBoundaryOne -
          c60F19OriginalF55EdgeCochain := by
  constructor
  · intro hflat
    obtain ⟨φ, hφ⟩ :=
      (c60F18ClosedEdgeIffVertexPotential
        (c60F19OriginalF55EdgeCochain + k)).mp hflat
    refine ⟨φ, ?_⟩
    calc
      k = c60F19OriginalF55EdgeCochain + k -
        c60F19OriginalF55EdgeCochain := by abel
      _ = φ.comp c60IntegralBoundaryOne -
        c60F19OriginalF55EdgeCochain := by rw [hφ]
  · rintro ⟨φ, rfl⟩
    have h :
        c60F19OriginalF55EdgeCochain +
          (φ.comp c60IntegralBoundaryOne -
            c60F19OriginalF55EdgeCochain) =
          φ.comp c60IntegralBoundaryOne := by abel
    rw [h]
    exact c60F18Coboundary_squared_zero φ

/-- An explicit correction selected by integrating the actual
original F55 square labels along F59-F16's spanning-tree paths. -/
def c60F19TreeVertexGauge :
    C60IntegralZeroChains →ₗ[ℤ] GradedThreeCell 0 0 :=
  c60F19OriginalF55EdgeCochain.comp c60F16PrimalPathLift

/-- The genuine canonical correction changes the original field
only enough to produce the exact coboundary of the spanning-tree
gauge. -/
def c60F19CanonicalTreeCorrection :
    C60IntegralOneChains →ₗ[ℤ] GradedThreeCell 0 0 :=
  c60F19TreeVertexGauge.comp c60IntegralBoundaryOne -
    c60F19OriginalF55EdgeCochain

/-- The canonical corrected F55 field is indeed flat on ALL
twelve pentagons and twenty hexagons simultaneously. -/
theorem c60F19CanonicalTreeCorrection_flat :
    (c60F19OriginalF55EdgeCochain +
      c60F19CanonicalTreeCorrection).comp
        c60IntegralBoundaryTwo = 0 :=
  (c60F19CompleteFlatCorrectionClassification
    c60F19CanonicalTreeCorrection).mpr
      ⟨c60F19TreeVertexGauge, rfl⟩

/-- The 59-edge physical original spanning tree used in F59-F16.
It has 48 around-pentagon edges (slots 0–3 of each pentagon)
plus eleven cross links (five north, five aligned, one south). -/
def c60F19IsPrimalTreeEdge : TruncatedIcosahedralEdge → Bool
  | .around a => decide (a.slot ≠ .s4)
  | .cross (.northSpoke _) => true
  | .cross (.crossAligned _) => true
  | .cross (.southSpoke i) => decide (i = 0)
  | _ => false

/-- Exactly 59 of the ACTUAL ninety original edges belong to
the spanning tree, so its complement has exactly 31 edges. -/
theorem c60F19PrimalTreeEdge_card :
    (Finset.univ.filter (fun e => c60F19IsPrimalTreeEdge e = true)).card = 59 := by
  decide

theorem c60F19PrimalTreeComplement_card :
    (Finset.univ.filter (fun e => c60F19IsPrimalTreeEdge e = false)).card = 31 := by
  decide

/-- The F59-F16 exact dual-tree filling is empty on every one
of the 59 original primal tree edges: this finite certificate
uses the actual F59-F16 list, not a new assumed tree model. -/
theorem c60F19TreeEdge_noDualFill :
    ∀ e : TruncatedIcosahedralEdge,
      c60F19IsPrimalTreeEdge e = true →
        c60F16DualFaceFillList e = [] := by
  decide

/-- Spanning-tree preservation: the actual canonical correction
is identically ZERO on all 59 original tree basis edges. -/
theorem c60F19CanonicalTreeCorrection_zero
    (e : TruncatedIcosahedralEdge)
    (he : c60F19IsPrimalTreeEdge e = true) :
    c60F19CanonicalTreeCorrection
      (Finsupp.single e (1 : ℤ)) = 0 := by
  have hface : c60F16FaceFill e = 0 := by
    simp [c60F16FaceFill, c60F19TreeEdge_noDualFill e he]
  have hpath := c60F16BasisContractingIdentity e
  rw [hface, map_zero, zero_add] at hpath
  have hboundary :
      c60IntegralBoundaryOne (Finsupp.single e (1 : ℤ)) =
        c60IntegralEdgeBoundaryChain e := by
    rw [c60IntegralBoundaryOne_singleEdge]
    simp
  change
    c60F19OriginalF55EdgeCochain
      (c60F16PrimalPathLift
        (c60IntegralBoundaryOne (Finsupp.single e (1 : ℤ)))) -
      c60F19OriginalF55EdgeCochain
        (Finsupp.single e (1 : ℤ)) = 0
  rw [hboundary, hpath, sub_self]

/-- The set of actually modified physical square edges. -/
noncomputable def c60F19CanonicalTreeCorrectionSupport :
    Finset TruncatedIcosahedralEdge := by
  classical
  exact Finset.univ.filter (fun e =>
    c60F19CanonicalTreeCorrection
      (Finsupp.single e (1 : ℤ)) ≠ 0)

/-- NONTRIVIAL FINITE REPAIR BOUND: the original F55 field can be
flattened without altering ANY of the 59 spanning-tree squares,
so at most 31 of the full ninety physical squares must change. -/
theorem c60F19CanonicalTreeCorrectionSupport_card_le31 :
    c60F19CanonicalTreeCorrectionSupport.card ≤ 31 := by
  classical
  have hs :
      c60F19CanonicalTreeCorrectionSupport ⊆
        Finset.univ.filter (fun e => c60F19IsPrimalTreeEdge e = false) := by
    intro e he
    simp only [c60F19CanonicalTreeCorrectionSupport,
      Finset.mem_filter, Finset.mem_univ, true_and] at he
    simp only [Finset.mem_filter, Finset.mem_univ, true_and]
    cases h : c60F19IsPrimalTreeEdge e with
    | false => rfl
    | true => exact False.elim
        (he (c60F19CanonicalTreeCorrection_zero e h))
  calc
    c60F19CanonicalTreeCorrectionSupport.card ≤
      (Finset.univ.filter
        (fun e => ¬ c60F19IsPrimalTreeEdge e)).card :=
          Finset.card_le_card hs
    _ = 31 := c60F19PrimalTreeComplement_card

/-! ## Connect the computation to ACTUAL parameter-dependent F55 cells -/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section ActualTypedF55
variable {a b : D} {x y : E}
variable {n₁ n₂ m₁ m₂ : Nat}
variable {p₀ p₁ p₂ : Blocks a b}
variable {q₀ q₁ q₂ : Blocks x y}
variable
  (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
  (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
variable
  {leftAfter : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁}
  {rightAfter : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂}
  (left : OriginalF45BracketTree.LocalRotation t₁ leftAfter)
  (right : OriginalF45BracketTree.LocalRotation t₂ rightAfter)

/-- This classification is literally about the ACTUAL F55
square generator attached to EACH original C60 edge, not an
invented detached constant cochain. -/
theorem c60F19ActualOriginalF55Labels_eq :
    (fun e : TruncatedIcosahedralEdge =>
      c60AllNinetyGrayCell t₁ t₂ left right e) =
        c60F19UniformF55EdgeLabels := by
  funext e
  exact c60AllNinetyGrayCell_eq t₁ t₂ left right e

/-- ACTUAL original F55 3-cell labels exhibit the signed real
pentagon/hexagon curvature table above, including its nonzero
local pentagon exchange phase and integer charge. -/
theorem c60F19ActualOriginalF55FaceCurvature
    (f : TruncatedIcosahedralSeedFace) :
    c60F18SignedGrayFacePasting
        (fun e : TruncatedIcosahedralEdge =>
          c60AllNinetyGrayCell t₁ t₂ left right e) f =
      c60F19ExpectedBoundaryDegree f •
        originalF55BraidedSquareGenerator := by
  rw [c60F19ActualOriginalF55Labels_eq]
  exact c60F19OriginalF55FaceCurvature_complete f

/-- The genuinely typed source F55 square labels fail exact
vertex descent along original C60 physical edges. -/
theorem c60F19ActualOriginalF55_noVertexGauge :
    ¬ ∃ φ : C60IntegralZeroChains →ₗ[ℤ] GradedThreeCell 0 0,
      c60F18GrayEdgeCochain
        (fun e : TruncatedIcosahedralEdge =>
          c60AllNinetyGrayCell t₁ t₂ left right e) =
        φ.comp c60IntegralBoundaryOne := by
  rw [c60F19ActualOriginalF55Labels_eq]
  exact c60F19OriginalF55EdgeCochain_no_vertexGauge

end ActualTypedF55

#print axioms c60F19SignedBoundaryDegree_complete
#print axioms c60F19OriginalF55FaceCurvature_complete
#print axioms c60F19OriginalF55Scalar_secondCharge
#print axioms c60F19OriginalF55Scalar_phase
#print axioms c60F19OriginalF55FaceCurvature_components
#print axioms c60F19OriginalF55FaceCurvature_zero_iff
#print axioms c60F19NorthPentagon_curvature_nonzero
#print axioms c60F19OriginalF55EdgeCochain_no_vertexGauge
#print axioms c60F19TotalOrientedCurvature_zero
#print axioms c60F19OriginalF55Curvature_globalObstruction_zero
#print axioms c60F19CompleteFlatCorrectionClassification
#print axioms c60F19CanonicalTreeCorrection_flat
#print axioms c60F19PrimalTreeEdge_card
#print axioms c60F19PrimalTreeComplement_card
#print axioms c60F19TreeEdge_noDualFill
#print axioms c60F19CanonicalTreeCorrection_zero
#print axioms c60F19CanonicalTreeCorrectionSupport_card_le31
#print axioms c60F19ActualOriginalF55Labels_eq
#print axioms c60F19ActualOriginalF55FaceCurvature
#print axioms c60F19ActualOriginalF55_noVertexGauge

end
end KUOS.DependentOriginationGrayC60ActualF55CurvatureRepairV5_167
