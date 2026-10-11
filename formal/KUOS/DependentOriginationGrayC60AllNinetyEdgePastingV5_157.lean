import KUOS.DependentOriginationTruncatedIcosahedralCrossHexagonFlagSquaresV5_157

namespace KUOS.DependentOriginationGrayC60AllNinetyEdgePastingV5_157

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154
open KUOS.DependentOriginationTruncatedIcosahedralHigherChargeV5_155
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayF55PhaseRealizationV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationTruncatedIcosahedralCrossHexagonFlagSquaresV5_157
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F59-F2 / v5.157 — honest original F55 labels on ALL NINETY C60 edges

F59-F1 constructed genuine four-flag hexagon/hexagon squares on all
THIRTY cross edges, with exact original distinct hexagon incident faces.
The original F59-E already certified pentagon/hexagon square labels on
the SIXTY around-vertex edges and their 12 actual pentagon collars.

Here separately supplied genuine original F54 local rotations decorate
the actual F59-F1 cross squares with original F55 disjoint-square
PresentedCells. Both cross and around square labels are sent through
the SAME independently defined F59-B braidedPhase HigherCellTarget
into the SAME genuine native F59-C symmetric braided groupoid.

Each physical edge is assigned exactly ONE square generator label
(with independent integer charge (0,1) and exchange phase 1).
The actual 30 cross edges therefore contribute (0,30;0), all 90 edges
contribute (0,90;0), and adding the genuine F59-E 12 pentagon labels
gives the native target 3-cell total (12,90;0).

IMPORTANT: This is a typed native-target composite of actually
labelled geometric incidence squares; the source original F55 cells
are not asserted to be independently composable, nor are the F54
rotation labels uniquely determined by C60 geometry. The 20 hexagons'
cyclic source-boundary coherence, and old native-dependent v3.86
six-edge endpoint proofs, require independent kernel-clean treatment.
No identification with Stage-II omega or external full Gray-category
coherence is made.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- An ACTUAL hexagon/hexagon four-flag C60 cross-edge square with
its independently supplied, strictly typed ORIGINAL F55 disjoint
rotation square generator. This is never a C60 quadrilateral face. -/
structure OriginalC60CrossHexagonSquareWithF55Generator
    (edge : IcosahedralEdge)
    {a b : D} {x y : E}
    {n m n' m' : Nat}
    {p₀ p₁ p₂ : Blocks a b}
    {q₀ q₁ q₂ : Blocks x y}
    {leftBefore leftAfter : OriginalF45BracketTree n m p₀ q₀ p₁ q₁}
    {rightBefore rightAfter : OriginalF45BracketTree n' m' p₁ q₁ p₂ q₂}
    (left : OriginalF45BracketTree.LocalRotation leftBefore leftAfter)
    (right : OriginalF45BracketTree.LocalRotation rightBefore rightAfter) where
  geometricSquare : TruncatedEdgeFlagSquare (.cross edge)
  firstHexagon :
    geometricSquare.firstFace =
      .fromTriangle (icosahedralEdgeIncidentFaces edge).1
  secondHexagon :
    geometricSquare.secondFace =
      .fromTriangle (icosahedralEdgeIncidentFaces edge).2
  squareCell :
    OriginalF45BracketTree.DepthRotationRoute.PresentedCell
      (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right)
      (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right)

/-- Construct this honestly supplied F55 label on each REAL
original cross edge and use the actual F59-F1 geometric square. -/
noncomputable def OriginalC60CrossHexagonSquareWithF55Generator.canonical
    (edge : IcosahedralEdge)
    {a b : D} {x y : E}
    {n m n' m' : Nat}
    {p₀ p₁ p₂ : Blocks a b}
    {q₀ q₁ q₂ : Blocks x y}
    {leftBefore leftAfter : OriginalF45BracketTree n m p₀ q₀ p₁ q₁}
    {rightBefore rightAfter : OriginalF45BracketTree n' m' p₁ q₁ p₂ q₂}
    (left : OriginalF45BracketTree.LocalRotation leftBefore leftAfter)
    (right : OriginalF45BracketTree.LocalRotation rightBefore rightAfter) :
    OriginalC60CrossHexagonSquareWithF55Generator edge left right where
  geometricSquare := crossHexagonHexagonSquare edge
  firstHexagon := rfl
  secondHexagon := rfl
  squareCell :=
    OriginalF45BracketTree.DepthRotationRoute.PresentedCell.disjointSquare left right

/-- Its source and target are BOTH real C60 hexagons and
all FOUR dart–face corner flags are actual distinct incidences. -/
theorem originalC60CrossHexagonSquareWithF55Generator_actual
    (edge : IcosahedralEdge)
    {a b : D} {x y : E}
    {n m n' m' : Nat}
    {p₀ p₁ p₂ : Blocks a b}
    {q₀ q₁ q₂ : Blocks x y}
    {leftBefore leftAfter : OriginalF45BracketTree n m p₀ q₀ p₁ q₁}
    {rightBefore rightAfter : OriginalF45BracketTree n' m' p₁ q₁ p₂ q₂}
    (left : OriginalF45BracketTree.LocalRotation leftBefore leftAfter)
    (right : OriginalF45BracketTree.LocalRotation rightBefore rightAfter) :
    (∀ i j : Bool,
      truncatedDartOnSeedFace
        ((OriginalC60CrossHexagonSquareWithF55Generator.canonical
          edge left right).geometricSquare.vertex i)
        ((OriginalC60CrossHexagonSquareWithF55Generator.canonical
          edge left right).geometricSquare.face j)) ∧
    Function.Injective
      (fun ij : Bool × Bool =>
        (((OriginalC60CrossHexagonSquareWithF55Generator.canonical
          edge left right).geometricSquare.vertex ij.1),
         ((OriginalC60CrossHexagonSquareWithF55Generator.canonical
          edge left right).geometricSquare.face ij.2))) := by
  exact crossHexagonHexagonSquare_fourFlags edge

section ActualAllEdges
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

/-- The actual hexagon/hexagon cross-edge F55 generator interpreted
in the same INDEPENDENT F59 braided Gray 3-cell target. -/
def c60CrossHexGrayCell (edge : IcosahedralEdge) :
    GradedThreeCell 0 0 :=
  (OriginalC60CrossHexagonSquareWithF55Generator.canonical
    edge left right).squareCell.interpret
      (OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.braidedPhase
        (D := D) (E := E))

/-- The older actual pentagon/hexagon around-edge F55 square
interpreted in exactly the same Gray target. -/
def c60AroundPentagonGrayCell
    (edge : TruncatedIcosahedralAroundEdge) :
    GradedThreeCell 0 0 :=
  (OriginalC60FlagSquareWithF55Generator.canonical
    edge left right).squareCell.interpret
      (OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.braidedPhase
        (D := D) (E := E))

/-- Actual C60 all-NINETY edge labeling: the original inductive
edge-carrier guarantees every genuine edge lies in exactly one case. -/
def c60AllNinetyGrayCell
    (edge : TruncatedIcosahedralEdge) :
    GradedThreeCell 0 0 :=
  match edge with
  | .around a => c60AroundPentagonGrayCell t₁ t₂ left right a
  | .cross e => c60CrossHexGrayCell t₁ t₂ left right e

/-- The chosen genuine F55 square generator is evaluated identically
in the SAME F59 target on EVERY cross edge. The geometry determines
the four-flag carrier, NOT the supplied pair of local rotations. -/
theorem c60CrossHexGrayCell_eq
    (edge : IcosahedralEdge) :
    c60CrossHexGrayCell t₁ t₂ left right edge =
      originalF55BraidedSquareGenerator := by
  rfl

theorem c60AroundPentagonGrayCell_eq
    (edge : TruncatedIcosahedralAroundEdge) :
    c60AroundPentagonGrayCell t₁ t₂ left right edge =
      originalF55BraidedSquareGenerator := by
  rfl

theorem c60AllNinetyGrayCell_eq
    (edge : TruncatedIcosahedralEdge) :
    c60AllNinetyGrayCell t₁ t₂ left right edge =
      originalF55BraidedSquareGenerator := by
  cases edge <;> rfl

/-- Nonzero local exchange phase survives on EACH real cross-edge
hexagon/hexagon incidence square, with independent square charge. -/
theorem c60CrossHexGrayCell_components (edge : IcosahedralEdge) :
    (c60CrossHexGrayCell t₁ t₂ left right edge).charge =
      ((0 : Int), (1 : Int)) ∧
    (c60CrossHexGrayCell t₁ t₂ left right edge).phase =
      (1 : ZMod 2) := by
  rw [c60CrossHexGrayCell_eq t₁ t₂ left right edge]
  exact originalF55BraidedSquareGenerator_complete

/-- Native target vertical composite of exactly the thirty actual
cross/hexagon-to-hexagon F55 square labels, counted ONCE each. -/
def c60CrossThirtyGrayTotal : GradedThreeCell 0 0 :=
  ∑ edge : IcosahedralEdge,
    c60CrossHexGrayCell t₁ t₂ left right edge

/-- Native target vertical composite of exactly the sixty actual
around/pentagon-to-hexagon edge F55 square labels, counted once each. -/
def c60AroundSixtyGrayTotal : GradedThreeCell 0 0 :=
  ∑ edge : TruncatedIcosahedralAroundEdge,
    c60AroundPentagonGrayCell t₁ t₂ left right edge

/-- Native target vertical composite of exactly the NINETY real
C60 edge square generators with NO duplicated edge labels. -/
def c60AllNinetyGrayTotal : GradedThreeCell 0 0 :=
  ∑ edge : TruncatedIcosahedralEdge,
    c60AllNinetyGrayCell t₁ t₂ left right edge

/-- Both faithful integer charge and extra mod-two phase on the
actual thirty hexagon/hexagon cross-square generators. -/
theorem c60CrossThirtyGrayTotal_components :
    (c60CrossThirtyGrayTotal t₁ t₂ left right).charge =
      ((0 : Int), (30 : Int)) ∧
    (c60CrossThirtyGrayTotal t₁ t₂ left right).phase =
      (0 : ZMod 2) := by
  constructor
  · change grayNeutralChargeHom
      (∑ edge : IcosahedralEdge,
        c60CrossHexGrayCell t₁ t₂ left right edge) =
        ((0 : Int), (30 : Int))
    rw [map_sum]
    calc
      (∑ edge : IcosahedralEdge, grayNeutralChargeHom
        (c60CrossHexGrayCell t₁ t₂ left right edge)) =
          ∑ _edge : IcosahedralEdge, ((0 : Int), (1 : Int)) := by
            apply Finset.sum_congr rfl
            intro edge _
            rw [c60CrossHexGrayCell_eq t₁ t₂ left right edge]
            exact originalF55BraidedSquareGenerator_complete.1
      _ = ((0 : Int), (30 : Int)) := by
            simp only [Finset.sum_const, Finset.card_univ]
            rw [crossOriginalEdge_card_kernel]
            decide
  · change grayNeutralPhaseHom
      (∑ edge : IcosahedralEdge,
        c60CrossHexGrayCell t₁ t₂ left right edge) =
        (0 : ZMod 2)
    rw [map_sum]
    calc
      (∑ edge : IcosahedralEdge, grayNeutralPhaseHom
        (c60CrossHexGrayCell t₁ t₂ left right edge)) =
          ∑ _edge : IcosahedralEdge, (1 : ZMod 2) := by
            apply Finset.sum_congr rfl
            intro edge _
            rw [c60CrossHexGrayCell_eq t₁ t₂ left right edge]
            exact originalF55BraidedSquareGenerator_complete.2
      _ = (0 : ZMod 2) := by
            simp only [Finset.sum_const, Finset.card_univ]
            rw [crossOriginalEdge_card_kernel]
            decide

/-- The SIXTY around-vertex original edges carry the independent
total (0,60), and their even exchange phases cancel. -/
theorem c60AroundSixtyGrayTotal_components :
    (c60AroundSixtyGrayTotal t₁ t₂ left right).charge =
      ((0 : Int), (60 : Int)) ∧
    (c60AroundSixtyGrayTotal t₁ t₂ left right).phase =
      (0 : ZMod 2) := by
  constructor
  · change grayNeutralChargeHom
      (∑ edge : TruncatedIcosahedralAroundEdge,
        c60AroundPentagonGrayCell t₁ t₂ left right edge) =
        ((0 : Int), (60 : Int))
    rw [map_sum]
    calc
      (∑ edge : TruncatedIcosahedralAroundEdge, grayNeutralChargeHom
        (c60AroundPentagonGrayCell t₁ t₂ left right edge)) =
          ∑ _edge : TruncatedIcosahedralAroundEdge,
            ((0 : Int), (1 : Int)) := by
            apply Finset.sum_congr rfl
            intro edge _
            rw [c60AroundPentagonGrayCell_eq t₁ t₂ left right edge]
            exact originalF55BraidedSquareGenerator_complete.1
      _ = ((0 : Int), (60 : Int)) := by
            simp only [Finset.sum_const, Finset.card_univ]
            rw [aroundOriginalEdge_card_kernel]
            decide
  · change grayNeutralPhaseHom
      (∑ edge : TruncatedIcosahedralAroundEdge,
        c60AroundPentagonGrayCell t₁ t₂ left right edge) =
        (0 : ZMod 2)
    rw [map_sum]
    calc
      (∑ edge : TruncatedIcosahedralAroundEdge, grayNeutralPhaseHom
        (c60AroundPentagonGrayCell t₁ t₂ left right edge)) =
          ∑ _edge : TruncatedIcosahedralAroundEdge,
            (1 : ZMod 2) := by
            apply Finset.sum_congr rfl
            intro edge _
            rw [c60AroundPentagonGrayCell_eq t₁ t₂ left right edge]
            exact originalF55BraidedSquareGenerator_complete.2
      _ = (0 : ZMod 2) := by
            simp only [Finset.sum_const, Finset.card_univ]
            rw [aroundOriginalEdge_card_kernel]
            decide

/-- All NINETY actual C60 edge-local higher square labels
aggregate to signed integer (0,90) and ZERO mod-two phase. -/
theorem c60AllNinetyGrayTotal_components :
    (c60AllNinetyGrayTotal t₁ t₂ left right).charge =
      ((0 : Int), (90 : Int)) ∧
    (c60AllNinetyGrayTotal t₁ t₂ left right).phase =
      (0 : ZMod 2) := by
  constructor
  · change grayNeutralChargeHom
      (∑ edge : TruncatedIcosahedralEdge,
        c60AllNinetyGrayCell t₁ t₂ left right edge) =
        ((0 : Int), (90 : Int))
    rw [map_sum]
    calc
      (∑ edge : TruncatedIcosahedralEdge, grayNeutralChargeHom
        (c60AllNinetyGrayCell t₁ t₂ left right edge)) =
          ∑ _edge : TruncatedIcosahedralEdge,
            ((0 : Int), (1 : Int)) := by
            apply Finset.sum_congr rfl
            intro edge _
            rw [c60AllNinetyGrayCell_eq t₁ t₂ left right edge]
            exact originalF55BraidedSquareGenerator_complete.1
      _ = ((0 : Int), (90 : Int)) := by
            simp only [Finset.sum_const, Finset.card_univ]
            rw [allOriginalTruncatedEdge_card_kernel]
            decide
  · change grayNeutralPhaseHom
      (∑ edge : TruncatedIcosahedralEdge,
        c60AllNinetyGrayCell t₁ t₂ left right edge) =
        (0 : ZMod 2)
    rw [map_sum]
    calc
      (∑ edge : TruncatedIcosahedralEdge, grayNeutralPhaseHom
        (c60AllNinetyGrayCell t₁ t₂ left right edge)) =
          ∑ _edge : TruncatedIcosahedralEdge,
            (1 : ZMod 2) := by
            apply Finset.sum_congr rfl
            intro edge _
            rw [c60AllNinetyGrayCell_eq t₁ t₂ left right edge]
            exact originalF55BraidedSquareGenerator_complete.2
      _ = (0 : ZMod 2) := by
            simp only [Finset.sum_const, Finset.card_univ]
            rw [allOriginalTruncatedEdge_card_kernel]
            decide

/-- A full ACTUAL edge partition 60+30, as an equality of native
target 3-cells—not merely the numerical equality of edge counts. -/
theorem c60AllNinetyGrayTotal_split :
    c60AllNinetyGrayTotal t₁ t₂ left right =
      c60AroundSixtyGrayTotal t₁ t₂ left right +
        c60CrossThirtyGrayTotal t₁ t₂ left right := by
  apply GradedThreeCell.ext
  · rw [(c60AllNinetyGrayTotal_components t₁ t₂ left right).1,
      (c60AroundSixtyGrayTotal_components t₁ t₂ left right).1,
      (c60CrossThirtyGrayTotal_components t₁ t₂ left right).1]
    decide
  · rw [(c60AllNinetyGrayTotal_components t₁ t₂ left right).2,
      (c60AroundSixtyGrayTotal_components t₁ t₂ left right).2,
      (c60CrossThirtyGrayTotal_components t₁ t₂ left right).2]
    decide

end ActualAllEdges

section All32OriginalFaces
variable {a b : D} {x y : E}
variable {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
variable {p₀ p₁ p₂ p₃ p₄ : Blocks a b}
variable {q₀ q₁ q₂ q₃ q₄ : Blocks x y}
variable
  (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
  (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
  (t₃ : OriginalF45BracketTree n₃ m₃ p₂ q₂ p₃ q₃)
  (t₄ : OriginalF45BracketTree n₄ m₄ p₃ q₃ p₄ q₄)
variable
  {leftAfter : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁}
  {rightAfter : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂}
  (left : OriginalF45BracketTree.LocalRotation t₁ leftAfter)
  (right : OriginalF45BracketTree.LocalRotation t₂ rightAfter)

/-- Add all genuine 12 F59-E pentagon collars (which count each
around edge ONCE) to the NEW thirty cross-edge hexagon/hexagon
square labels. This covers exactly 12 pentagon generators and
90 distinct C60 edge-local square generators. -/
def c60FullPentagonAndNinetyEdges : GradedThreeCell 0 0 :=
  c60GrayPatch t₁ t₂ t₃ t₄ left right Finset.univ +
    c60CrossThirtyGrayTotal t₁ t₂ left right

/-- In that same actual NATIVE target 3-cell, all ninety
square-generator labels and the twelve pentagon generators have
nonzero integer charge (12,90), while the 90 square phases cancel.
This does not construct twenty new hexagon higher-cell generators. -/
theorem c60FullPentagonAndNinetyEdges_components :
    (c60FullPentagonAndNinetyEdges t₁ t₂ t₃ t₄ left right).charge =
      ((12 : Int), (90 : Int)) ∧
    (c60FullPentagonAndNinetyEdges t₁ t₂ t₃ t₄ left right).phase =
      (0 : ZMod 2) := by
  have hp := c60GrayGlobal_components t₁ t₂ t₃ t₄ left right
  have hc := c60CrossThirtyGrayTotal_components t₁ t₂ left right
  constructor
  · change
      (c60GrayPatch t₁ t₂ t₃ t₄ left right Finset.univ).charge +
        (c60CrossThirtyGrayTotal t₁ t₂ left right).charge =
          ((12 : Int), (90 : Int))
    rw [hp.1, hc.1]
    decide
  · change
      (c60GrayPatch t₁ t₂ t₃ t₄ left right Finset.univ).phase +
        (c60CrossThirtyGrayTotal t₁ t₂ left right).phase =
          (0 : ZMod 2)
    rw [hp.2, hc.2]
    decide

end All32OriginalFaces

#print axioms OriginalC60CrossHexagonSquareWithF55Generator
#print axioms OriginalC60CrossHexagonSquareWithF55Generator.canonical
#print axioms originalC60CrossHexagonSquareWithF55Generator_actual
#print axioms c60CrossHexGrayCell_eq
#print axioms c60AroundPentagonGrayCell_eq
#print axioms c60AllNinetyGrayCell_eq
#print axioms c60CrossHexGrayCell_components
#print axioms c60CrossThirtyGrayTotal_components
#print axioms c60AroundSixtyGrayTotal_components
#print axioms c60AllNinetyGrayTotal_components
#print axioms c60AllNinetyGrayTotal_split
#print axioms c60FullPentagonAndNinetyEdges_components

end
end KUOS.DependentOriginationGrayC60AllNinetyEdgePastingV5_157
