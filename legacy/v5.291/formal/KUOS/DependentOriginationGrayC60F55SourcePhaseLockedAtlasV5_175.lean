import KUOS.DependentOriginationGrayC60WangBiGlobalGrayDescentV5_174

namespace KUOS.DependentOriginationGrayC60F55SourcePhaseLockedAtlasV5_175

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayF55PhaseRealizationV5_156
open KUOS.DependentOriginationTruncatedIcosahedralHigherChargeV5_155
open KUOS.DependentOriginationGrayC60F55SharpRepairV5_168
open KUOS.DependentOriginationGrayC60WangBiZhouyiTimeV5_170
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60AllNinetyEdgePastingV5_157
open KUOS.DependentOriginationGrayC60WangBiNativeHigherCoherenceV5_171
open KUOS.DependentOriginationGrayC60WangBiFourImageSixQiF55NaturalityV5_172
open KUOS.DependentOriginationGrayC60WangBiGaugeCollarSixQiCoherenceV5_173
open KUOS.DependentOriginationGrayC60WangBiGlobalGrayDescentV5_174
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F27 / v5.175 — original F55 PresentedCells inside an exact
# phase-compatible braided Gray 3-cell subgroup, carried by Wang Bi

This theorem unit extends the merged v5.174 global C60 32-face
cochain/descent realization back to the original freely generated,
proof-relevant and fully typed F55 PresentedCell constructors.

Unlike arbitrary neutral GradedThreeCell values (where ZMod2 phase is
independent of Int×Int charge), an ORIGINAL F55 freely presented
source cell can be interpreted in the F59 braided target only with
the following COMPATIBILITY LAW:

  phase = (squareGeneratorCharge : ZMod 2).

This is a mathematical theorem by induction on all NINE constructors
of the actual original F55 presentation: ident, pentagon, square,
inverse, vertical transitivity and FOUR horizontal/contextual routes.
It is not a quotient axiom, a declaration of natural isomorphism,
or a suggestion that the ancient texts supplied a Gray category.

We construct a real AddSubgroup of the native category's graded
3-cell endomorphism group, prove the interpreted original F55 source
image is inside it, give an exact classification of resulting target
values by original F58 integer charge, and construct a Mathlib Cat
natural transformation for ALL original C60 geometric corners whose
second coordinate is this subgroup, not the unrestricted 3-cell type.

The original separately supplied F54 local rotations attach actual
source PresentedCells to ALL 90 physical C60 incidence squares.
Even after the F59-F20 canonical flat correction on EXACTLY 27 true
edges, the 90 graded values remain in the very same image-compatible
subgroup. The resulting 360-flag Wang Bi atlas remains natural and
all 32 physical signed face curvatures vanish.

Membership in the image-compatible subgroup is NECESSARY for a raw
F55 cell interpretation, but not asserted to be SUFFICIENT for a
specific fixed pair of typed F55 routes. A full raw-source Gray
3-functor, unrestricted whiskering and Stage-II omega identification
remain distinct unsolved obligations.
-/

/-- The EXACT compatibility subspace for neutral native F55 3-cell
values: exchange phase equals the second integer generator charge
reduced modulo two. The full braided Gray target is larger. -/
def c60F55PhaseLocked : AddSubgroup (GradedThreeCell 0 0) where
  carrier := {g | g.phase = (g.charge.2 : ZMod 2)}
  zero_mem' := by
    rfl
  add_mem' := by
    intro g h hg hh
    change g.phase = (g.charge.2 : ZMod 2) at hg
    change h.phase = (h.charge.2 : ZMod 2) at hh
    change (g + h).phase = ((g + h).charge.2 : ZMod 2)
    calc
      (g + h).phase = g.phase + h.phase := grayNeutral_add_phase g h
      _ = (g.charge.2 : ZMod 2) + (h.charge.2 : ZMod 2) := by
        rw [hg, hh]
      _ = ((g + h).charge.2 : ZMod 2) := by
        rw [grayNeutral_add_charge]
        change _ = ((g.charge.2 + h.charge.2 : ℤ) : ZMod 2)
        rw [Int.cast_add]
  neg_mem' := by
    intro g hg
    change g.phase = (g.charge.2 : ZMod 2) at hg
    change (-g).phase = ((-g).charge.2 : ZMod 2)
    have hp : (-g).phase = -g.phase := by rfl
    have hc : (-g).charge.2 = -g.charge.2 := by rfl
    rw [hp, hc, hg, Int.cast_neg]

/-- The *genuine native category* composition of any two compatible
nontrivial F55 3-cells remains compatible. -/
theorem c60F55PhaseLocked_native_comp
    {g h : GradedThreeCell 0 0}
    (hg : g ∈ c60F55PhaseLocked)
    (hh : h ∈ c60F55PhaseLocked) :
    (g ≫ h : GrayGrade.unit ⟶ GrayGrade.unit) ∈ c60F55PhaseLocked := by
  rw [← grayNeutral_add_eq_native_comp]
  exact c60F55PhaseLocked.add_mem hg hh

/-- Genuine original F55 pentagon higher generator lies in the
phase-compatible braided subgroup with charge (1,0) and phase 0. -/
def c60F55PentagonNativeGenerator : GradedThreeCell 0 0 :=
  ⟨rfl, ((1 : Int), (0 : Int)), (0 : ZMod 2)⟩

theorem c60F55PentagonNativeGenerator_mem :
    c60F55PentagonNativeGenerator ∈ c60F55PhaseLocked := by
  rfl

/-- Each ORIGINAL F55 disjoint contextual square lies in the same
subgroup yet retains NONZERO exchange phase 1. -/
theorem c60F55SquareNativeGenerator_mem :
    originalF55BraidedSquareGenerator ∈ c60F55PhaseLocked := by
  change originalF55BraidedSquareGenerator.phase =
    (originalF55BraidedSquareGenerator.charge.2 : ZMod 2)
  rw [originalF55BraidedSquareGenerator_complete.1,
    originalF55BraidedSquareGenerator_complete.2]
  decide

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- The actual F56 interpreter of ALL original freely generated
F55 cells into the INDEPENDENT F59 native braided Gray target. -/
def c60F55SourceNative
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    (cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    GradedThreeCell 0 0 :=
  cell.interpret
    (OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.braidedPhase
      (D := D) (E := E))

/-- Complete nine-constructor INDUCTION: identity, original pentagon,
genuinely independent F55 square, inverse, vertical composition,
both horizontal contexts and both route-composition whiskerings
ALL remain in the same intrinsically defined native subgroup. -/
theorem c60F55SourceNative_mem
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    (cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    c60F55SourceNative cell ∈ c60F55PhaseLocked := by
  induction cell with
  | ident route =>
      change (GradedThreeCell.ident 0 : GradedThreeCell 0 0) ∈
        c60F55PhaseLocked
      rfl
  | pentagon t₁ t₂ t₃ t₄ =>
      change c60F55PentagonNativeGenerator ∈ c60F55PhaseLocked
      exact c60F55PentagonNativeGenerator_mem
  | disjointSquare left right =>
      change originalF55BraidedSquareGenerator ∈ c60F55PhaseLocked
      exact c60F55SquareNativeGenerator_mem
  | symm cell ih =>
      change (c60F55SourceNative cell).inv ∈ c60F55PhaseLocked
      have hinv : (c60F55SourceNative cell).inv =
        -(c60F55SourceNative cell) := by
        apply GradedThreeCell.ext <;> rfl
      rw [hinv]
      exact c60F55PhaseLocked.neg_mem ih
  | trans left right ihLeft ihRight =>
      change (c60F55SourceNative left).comp
        (c60F55SourceNative right) ∈ c60F55PhaseLocked
      have hcomp : (c60F55SourceNative left).comp
          (c60F55SourceNative right) =
        (c60F55SourceNative left) +
          (c60F55SourceNative right) :=
        (grayNeutral_add_eq_native_comp _ _).symm
      rw [hcomp]
      exact c60F55PhaseLocked.add_mem ihLeft ihRight
  | leftContext cell later ih => exact ih
  | rightContext earlier cell ih => exact ih
  | precompose priorRoute cell ih => exact ih
  | postcompose cell suffix ih => exact ih

/-- Exact realization of the original F55 source identity cell as
the actual identity morphism in the NATIVE mathlib Gray category. -/
theorem c60F55SourceNative_ident
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    (route : OriginalF45BracketTree.DepthRotationRoute first last) :
    c60F55SourceNative
      (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.ident route) =
      (𝟙 GrayGrade.unit : GrayGrade.unit ⟶ GrayGrade.unit) := by
  rfl

/-- The ACTUAL source F55 vertical composition constructor maps
to GENUINE native Gray 3-cell categorical composition, preserving
both independent integer charges and nonzero exchange phase. -/
theorem c60F55SourceNative_trans
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    {r s t : OriginalF45BracketTree.DepthRotationRoute first last}
    (α : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s)
    (β : OriginalF45BracketTree.DepthRotationRoute.PresentedCell s t) :
    c60F55SourceNative
      (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.trans α β) =
      (c60F55SourceNative α ≫ c60F55SourceNative β :
        GrayGrade.unit ⟶ GrayGrade.unit) := by
  rfl

/-- The supposedly independent F59 braided PHASE of a cell in
the ORIGINAL F55 free presentation is in fact constrained by the
existing independently proven F58 integer square-generator count.
No mod-two phase is omitted from the target value. -/
theorem c60F55SourceNative_phase_eq_F58SquareParity
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    (cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    (c60F55SourceNative cell).phase =
      ((cell.interpret
        (OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.generatorCharge
          (D := D) (E := E))).2 : ZMod 2) := by
  have hmem := c60F55SourceNative_mem cell
  change (c60F55SourceNative cell).phase =
    ((c60F55SourceNative cell).charge.2 : ZMod 2) at hmem
  have hc :
      (c60F55SourceNative cell).charge =
      cell.interpret
        (OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.generatorCharge
          (D := D) (E := E)) :=
    KUOS.DependentOriginationGrayF55PhaseRealizationV5_156.OriginalF45BracketTree.DepthRotationRoute.PresentedCell.braidedPhase_charge_eq_F58 cell
  rw [hc] at hmem
  exact hmem

/-- EXACT target classification of any two PARALLEL genuine
F55 source PresentedCells. The native braided target retains
charge and the nonzero square phase, but no extra distinctions
between two raw source cells having the same F58 signed charge. -/
theorem c60F55SourceNative_eq_iff_F58Charge_eq
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    (α β : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    c60F55SourceNative α = c60F55SourceNative β ↔
      α.interpret
        (OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.generatorCharge
          (D := D) (E := E)) =
      β.interpret
        (OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.generatorCharge
          (D := D) (E := E)) := by
  have hα :
      (c60F55SourceNative α).charge =
      α.interpret
        (OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.generatorCharge
          (D := D) (E := E)) :=
    KUOS.DependentOriginationGrayF55PhaseRealizationV5_156.OriginalF45BracketTree.DepthRotationRoute.PresentedCell.braidedPhase_charge_eq_F58 α
  have hβ :
      (c60F55SourceNative β).charge =
      β.interpret
        (OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.generatorCharge
          (D := D) (E := E)) :=
    KUOS.DependentOriginationGrayF55PhaseRealizationV5_156.OriginalF45BracketTree.DepthRotationRoute.PresentedCell.braidedPhase_charge_eq_F58 β
  constructor
  · intro h
    rw [← hα, ← hβ]
    exact congrArg GradedThreeCell.charge h
  · intro h
    apply GradedThreeCell.ext
    · rw [hα, hβ, h]
    · rw [c60F55SourceNative_phase_eq_F58SquareParity α,
        c60F55SourceNative_phase_eq_F58SquareParity β, h]

/-! ## A genuinely narrower Mathlib Cat functor and 2-cell atlas. -/

/-- An honest native Mathlib functor to all six-Yao symbols PAIRED
WITH A HIGHER 3-CELL THAT CARRIES ITS F55 PHASE COMPATIBILITY PROOF.
This is a proper subcarrier of the unrestricted v5.172 target. -/
def c60F55LockedSixYaoFunctor : WangBiFrame ⥤ Type 0 where
  obj _ := WangBiSixYao × c60F55PhaseLocked
  map := fun {a b} f =>
    TypeCat.ofHom
      (fun x : WangBiSixYao × c60F55PhaseLocked =>
        (wangBiChartArrow a b f x.1, x.2))
  map_id := by
    intro a
    apply TypeCat.homEquiv.injective
    funext x
    rcases x with ⟨code, grade⟩
    exact congrArg (fun y => (y, grade)) (wangBiChartArrow_id a code)
  map_comp := by
    intro a b c f g
    apply TypeCat.homEquiv.injective
    funext x
    rcases x with ⟨code, grade⟩
    exact congrArg (fun y => (y, grade))
      (wangBiChartArrow_comp a b c f g code)

/-- A real Mathlib natural transformation on ALL 90 genuine physical
edges times four flags. It transports Wang Bi representations and
RETAINS the exact F55 higher-data compatibility in the second field. -/
def c60F55LockedCornerNatTrans
    (side : C60DartSideGauge)
    (grade : TruncatedIcosahedralEdge → c60F55PhaseLocked) :
    c60ActualCornerFunctor ⟶ c60F55LockedSixYaoFunctor where
  app a := TypeCat.ofHom
    (fun corner : C60ActualSquareCorner =>
      (wangBiOriginalFaceEncoding a (c60GaugeSignedFace side corner),
        grade corner.1))
  naturality := by
    intro a b f
    apply TypeCat.homEquiv.injective
    funext corner
    exact (congrArg (fun y => (y, grade corner.1))
      (wangBiEncodingNaturality a b f
        (c60GaugeSignedFace side corner))).symm

/-- Forget ONLY the proof of compatibility, NOT the phase itself.
This is a genuine Mathlib natural transformation between genuine
six-Yao-with-grade functors on the same Wang Bi chart category. -/
def c60F55LockedInclusion :
    c60F55LockedSixYaoFunctor ⟶ c60GradedSixYaoFunctor where
  app _ := TypeCat.ofHom
    (fun x : WangBiSixYao × c60F55PhaseLocked => (x.1, x.2.1))
  naturality := by
    intros
    rfl

/-- The refined original-F55-compatible Cat 2-cell projects
EXACTLY to the already-proven v5.174 Wang Bi × independent Gray
natural transformation: no 3-cell charge or exchange phase is lost. -/
theorem c60F55LockedCornerNatTrans_forget
    (side : C60DartSideGauge)
    (grade : TruncatedIcosahedralEdge → c60F55PhaseLocked) :
    c60F55LockedCornerNatTrans side grade ≫ c60F55LockedInclusion =
      c60WangBiGlobalGradedAtlas side (fun e => (grade e).1) := by
  apply NatTrans.ext
  funext a
  apply TypeCat.homEquiv.injective
  funext corner
  rfl

/-- A single nontrivial original F55 square 3-cell always
produces a valid, phase-compatible Wang Bi local-chart label. -/
def c60F55OriginalLockedGrade
    (_edge : TruncatedIcosahedralEdge) : c60F55PhaseLocked :=
  ⟨originalF55BraidedSquareGenerator, c60F55SquareNativeGenerator_mem⟩

/- The physical F55 original edge assignment is EXACTLY the one
used in v5.174: for ANY independently supplied original F54 local
rotations its target value is the actual interpreted F55 square
PresentedCell, not a newly invented label. -/
section ActualOriginalF55Sources
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

/-- Each actual F54-generated, original F55 PresentedCell on all
ninety C60 incidence squares yields a native phase-locked grade. -/
def c60ActualF55PresentedLockedGrade
    (edge : TruncatedIcosahedralEdge) : c60F55PhaseLocked :=
  ⟨c60AllNinetyGrayCell t₁ t₂ left right edge, by
    rw [c60AllNinetyGrayCell_eq t₁ t₂ left right edge]
    exact c60F55SquareNativeGenerator_mem⟩

/-- A genuine Cat 2-cell transporting the ORIGINAL typed F55 square
generators together with all 64 Wang Bi symbolic encodings. -/
def c60ActualF55PresentedLockedAtlas (side : C60DartSideGauge) :
    c60ActualCornerFunctor ⟶ c60F55LockedSixYaoFunctor :=
  c60F55LockedCornerNatTrans side
    (c60ActualF55PresentedLockedGrade t₁ t₂ left right)

/-- After forgetting only the compatibility proof, the
genuinely ORIGINAL F54/F55 PresentedCell-based Wang Bi atlas is
identical to the original physical 90-edge Gray atlas of v5.174. -/
theorem c60ActualF55PresentedLockedAtlas_forget
    (side : C60DartSideGauge) :
    c60ActualF55PresentedLockedAtlas t₁ t₂ left right side ≫
      c60F55LockedInclusion =
    c60WangBiGlobalGradedAtlas side
      (fun e => c60AllNinetyGrayCell t₁ t₂ left right e) := by
  exact c60F55LockedCornerNatTrans_forget side
    (c60ActualF55PresentedLockedGrade t₁ t₂ left right)

/-- The typed source F55 generator's native grade and its
nonzero phase both survive at every one of the 360 actual corners. -/
theorem c60ActualF55PresentedLockedGrade_components
    (edge : TruncatedIcosahedralEdge) :
    (c60ActualF55PresentedLockedGrade t₁ t₂ left right edge).1.charge =
      ((0 : Int), (1 : Int)) ∧
    (c60ActualF55PresentedLockedGrade t₁ t₂ left right edge).1.phase =
      (1 : ZMod 2) := by
  rw [show (c60ActualF55PresentedLockedGrade t₁ t₂ left right edge).1 =
      originalF55BraidedSquareGenerator from
        c60AllNinetyGrayCell_eq t₁ t₂ left right edge]
  exact originalF55BraidedSquareGenerator_complete

end ActualOriginalF55Sources

/-! ## The actual 27-edge corrected target remains phase compatible. -/

/-- The ORIGINAL canonical F59-F20 flat repair, not an unrelated
approximate substitute, retains the proven necessary F55
source-image phase compatibility on every physical C60 edge. -/
theorem c60F55RepairedGrade_mem (edge : TruncatedIcosahedralEdge) :
    c60WangBiRepairedEdgeGrade edge ∈ c60F55PhaseLocked := by
  rw [c60WangBiRepairedEdgeGrade_formula]
  exact c60F55PhaseLocked.add_mem c60F55SquareNativeGenerator_mem
    (c60F55PhaseLocked.zsmul_mem
      c60F55SquareNativeGenerator_mem _)

/-- The actual fully repaired 90-edge F55 field lives in the
SAME native phase-compatible target as all raw original F55
PresentedCells, even at its precisely identified 27 changes. -/
def c60F55RepairedLockedGrade
    (edge : TruncatedIcosahedralEdge) : c60F55PhaseLocked :=
  ⟨c60WangBiRepairedEdgeGrade edge, c60F55RepairedGrade_mem edge⟩

/-- The 360-flag, 64-symbol Wang Bi natural transformation
of the canonical FLAT 32-face repaired C60 field can be
constructed within the original-source-compatible subgroup. -/
def c60F55RepairedLockedAtlas (side : C60DartSideGauge) :
    c60ActualCornerFunctor ⟶ c60F55LockedSixYaoFunctor :=
  c60F55LockedCornerNatTrans side c60F55RepairedLockedGrade

/-- The new phase-compatible repaired Cat 2-cell reduces
EXACTLY to the v5.174 canonical 27-edge corrected Wang Bi atlas.
Thus phase-compatibility was added WITHOUT altering its proven
cochain realization or any of the original physical C60 geometry. -/
theorem c60F55RepairedLockedAtlas_forget
    (side : C60DartSideGauge) :
    c60F55RepairedLockedAtlas side ≫ c60F55LockedInclusion =
      c60WangBiRepairedGlobalAtlas side := by
  exact c60F55LockedCornerNatTrans_forget side c60F55RepairedLockedGrade

/-- The real 12 original pentagon and 20 original hexagon
ORIENTED source boundaries each have ZERO braided Gray
face curvature for these very subgroup-valued atlas grades. -/
theorem c60F55RepairedLockedAtlas_all32_flat
    (face : TruncatedIcosahedralSeedFace) :
    c60WangBiSignedGrayFace
      (fun edge => (c60F55RepairedLockedGrade edge).1) face = 0 := by
  exact c60WangBiRepairedGrade_all32Faces_flat face

/-- The subgroup-compatible corrected field differs from the
actual ORIGINAL F55 square only at the same 27 genuine C60 edges. -/
theorem c60F55RepairedLockedAtlas_changes_exact27 :
    c60WangBiRepairedChangedSupport.card = 27 :=
  c60WangBiRepairedEdgeGrade_changed_card

/-- ALL remaining 63 physical edges still carry the original
nontrivial independent (0,1;1) F55 braided 3-cell. -/
theorem c60F55RepairedLockedAtlas_preserves_original
    (edge : TruncatedIcosahedralEdge)
    (h : c60F20IsChangedEdge edge = false) :
    (c60F55RepairedLockedGrade edge).1 =
      originalF55BraidedSquareGenerator :=
  c60WangBiRepairedEdgeGrade_preserved edge h

#print axioms c60F55PhaseLocked
#print axioms c60F55PhaseLocked_native_comp
#print axioms c60F55PentagonNativeGenerator_mem
#print axioms c60F55SquareNativeGenerator_mem
#print axioms c60F55SourceNative_mem
#print axioms c60F55SourceNative_ident
#print axioms c60F55SourceNative_trans
#print axioms c60F55SourceNative_phase_eq_F58SquareParity
#print axioms c60F55SourceNative_eq_iff_F58Charge_eq
#print axioms c60F55LockedSixYaoFunctor
#print axioms c60F55LockedCornerNatTrans
#print axioms c60F55LockedInclusion
#print axioms c60F55LockedCornerNatTrans_forget
#print axioms c60F55OriginalLockedGrade
#print axioms c60ActualF55PresentedLockedGrade
#print axioms c60ActualF55PresentedLockedAtlas
#print axioms c60ActualF55PresentedLockedAtlas_forget
#print axioms c60ActualF55PresentedLockedGrade_components
#print axioms c60F55RepairedGrade_mem
#print axioms c60F55RepairedLockedGrade
#print axioms c60F55RepairedLockedAtlas
#print axioms c60F55RepairedLockedAtlas_forget
#print axioms c60F55RepairedLockedAtlas_all32_flat
#print axioms c60F55RepairedLockedAtlas_changes_exact27
#print axioms c60F55RepairedLockedAtlas_preserves_original

end
end KUOS.DependentOriginationGrayC60F55SourcePhaseLockedAtlasV5_175
