import KUOS.DependentOriginationTruncatedIcosahedralKernelHexagonCyclesV5_157

namespace KUOS.DependentOriginationGrayKernelHexagonSixCellPastingV5_157

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralHexagonsV3_86
open KUOS.DependentOriginationTruncatedIcosahedralKernelHexagonCyclesV5_157
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayF55PhaseRealizationV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60AllNinetyEdgePastingV5_157
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F59-F4 / v5.157 — six original F55 Gray 3-cells around each C60 hexagon

F59-F3 independently constructed an axiom-clean C60 hexagon cycle
with all six endpoint equalities, including its closing sixth edge.
F59-F2 separately labelled ALL real C60 edges, including the thirty
hexagon/hexagon cross edges, with the same independently interpreted
genuine original F55 rotation square in the native symmetric braided
Gray 3-cell target. The necessary two F54 LocalRotation values are
still explicitly supplied, not invented from geometric incidence.

This file now takes EACH of the six ORIGINAL cyclic boundary edges
of each of the twenty real C60 hexagons and interprets its genuine
F55 square label in the SAME native graded three-cell target.
The six are composable there at the neutral Gray-grade boundary.
The exact charge and exchange phase of a single hexagon boundary are
(0,6) and 0. Summing the native composites for all twenty actual
hexagon boundaries gives (0,120), phase 0.

A carefully scoped numerical comparison in the full independent
TARGET identifies that global sum with all 90 edge labels plus the
30 cross-edge labels. This does NOT itself prove an incidence-multiset
identity: the next step must prove explicitly that each cross edge
is used by exactly two hexagon boundaries and each around edge
by exactly one. In particular neither a raw source F55 vertical
paste nor an unrestricted external Gray coherence law follows from
the presently typed target composite.

No old Stage-II obstruction class is equated with these charges.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section OriginalHexagonPasting
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

/-- Exactly SIX real geometric C60 hexagon boundary edges, in the
newly proved F59-F3 cyclic orientation, each labelled by a typed
original F55 square interpreter in the native F59 target. -/
def kernelC60HexagonGraySixSquareList (face : IcosahedralFace) :
    List (GradedThreeCell 0 0) :=
  (kernelCertifiedHexagonCycle face).edges.map
    (fun oriented =>
      c60AllNinetyGrayCell t₁ t₂ left right oriented.edge)

/-- The six genuine boundary edge-local original F55 squares all
carry the same *independently constructed* Gray generator value.
This does not identify their original geometric four-flag carriers. -/
theorem kernelC60HexagonGraySixSquareList_eq
    (face : IcosahedralFace) :
    kernelC60HexagonGraySixSquareList t₁ t₂ left right face =
      [originalF55BraidedSquareGenerator,
       originalF55BraidedSquareGenerator,
       originalF55BraidedSquareGenerator,
       originalF55BraidedSquareGenerator,
       originalF55BraidedSquareGenerator,
       originalF55BraidedSquareGenerator] := by
  simp only [kernelC60HexagonGraySixSquareList,
    OrientedHexagonCycle.edges, List.map_cons, List.map_nil,
    c60AllNinetyGrayCell_eq]

/-- The exact independent integer charge of the 6 boundary squares
is nonzero (0,6), while their six odd exchange phases cancel. -/
theorem kernelC60HexagonGraySixSquareSum_components
    (face : IcosahedralFace) :
    (kernelC60HexagonGraySixSquareList
      t₁ t₂ left right face).sum.charge =
        ((0 : Int), (6 : Int)) ∧
    (kernelC60HexagonGraySixSquareList
      t₁ t₂ left right face).sum.phase =
        (0 : ZMod 2) := by
  rw [kernelC60HexagonGraySixSquareList_eq t₁ t₂ left right face]
  constructor <;> decide

/-- Genuine typed SIX-FOLD native 3-cell vertical composite,
respecting the actual F59-F3 cyclic edge order and all six source
edge labels; the last edge closes the original geometric hexagon. -/
def kernelC60HexagonGraySixNativePasting
    (face : IcosahedralFace) : GradedThreeCell 0 0 :=
  let cycle := kernelCertifiedHexagonCycle face
  (((((c60AllNinetyGrayCell t₁ t₂ left right cycle.e0.edge).comp
      (c60AllNinetyGrayCell t₁ t₂ left right cycle.e1.edge)).comp
      (c60AllNinetyGrayCell t₁ t₂ left right cycle.e2.edge)).comp
      (c60AllNinetyGrayCell t₁ t₂ left right cycle.e3.edge)).comp
      (c60AllNinetyGrayCell t₁ t₂ left right cycle.e4.edge)).comp
      (c60AllNinetyGrayCell t₁ t₂ left right cycle.e5.edge)

/-- The above six operations are exactly categorical vertical
composition on neutral native Grade 3-cells; no arbitrary monoidal
whiskering comparison is inserted or silently dropped. -/
theorem kernelC60HexagonGraySixNativePasting_isCategoryComp
    (face : IcosahedralFace) :
    kernelC60HexagonGraySixNativePasting t₁ t₂ left right face =
      (let cycle := kernelCertifiedHexagonCycle face
       (((((c60AllNinetyGrayCell t₁ t₂ left right cycle.e0.edge ≫
           c60AllNinetyGrayCell t₁ t₂ left right cycle.e1.edge) ≫
           c60AllNinetyGrayCell t₁ t₂ left right cycle.e2.edge) ≫
           c60AllNinetyGrayCell t₁ t₂ left right cycle.e3.edge) ≫
           c60AllNinetyGrayCell t₁ t₂ left right cycle.e4.edge) ≫
           c60AllNinetyGrayCell t₁ t₂ left right cycle.e5.edge :
             GrayGrade.unit ⟶ GrayGrade.unit)) := by
  rfl

/-- This is an honest composite in the NATIVE target Category, not
just the numeric sum of the six independent F58 charge coordinates. -/
theorem kernelC60HexagonGraySixNativePasting_components
    (face : IcosahedralFace) :
    (kernelC60HexagonGraySixNativePasting
      t₁ t₂ left right face).charge =
      ((0 : Int), (6 : Int)) ∧
    (kernelC60HexagonGraySixNativePasting
      t₁ t₂ left right face).phase =
      (0 : ZMod 2) := by
  dsimp [kernelC60HexagonGraySixNativePasting]
  simp only [c60AllNinetyGrayCell_eq]
  constructor <;> decide

/-- The categorical six-fold paste equals the independently
summed edge-labelled 3-cell of the same original hexagon,
including BOTH integer-charge and independent phase information. -/
theorem kernelC60HexagonGrayPasting_eq_sum
    (face : IcosahedralFace) :
    kernelC60HexagonGraySixNativePasting t₁ t₂ left right face =
      (kernelC60HexagonGraySixSquareList
        t₁ t₂ left right face).sum := by
  apply GradedThreeCell.ext
  · rw [(kernelC60HexagonGraySixNativePasting_components
      t₁ t₂ left right face).1,
      (kernelC60HexagonGraySixSquareSum_components
      t₁ t₂ left right face).1]
  · rw [(kernelC60HexagonGraySixNativePasting_components
      t₁ t₂ left right face).2,
      (kernelC60HexagonGraySixSquareSum_components
      t₁ t₂ left right face).2]

/-- Native additive composite over the original TWENTY real C60
hexagonal faces, each with its independently reconstructed closed
six-edge boundary; faces are indexed once by IcosahedralFace. -/
def kernelC60AllTwentyHexagonGrayTotal : GradedThreeCell 0 0 :=
  ∑ face : IcosahedralFace,
    kernelC60HexagonGraySixNativePasting t₁ t₂ left right face

/-- The actual twenty six-edge hexagon boundaries have 120 edge
OCCURRENCES (edge occurrences, not distinct geometric edges).
Each contributes the genuine original F55 square charge (0,1),
but even six-fold phase is zero on every one of the twenty faces. -/
theorem kernelC60AllTwentyHexagonGrayTotal_components :
    (kernelC60AllTwentyHexagonGrayTotal
      t₁ t₂ left right).charge =
        ((0 : Int), (120 : Int)) ∧
    (kernelC60AllTwentyHexagonGrayTotal
      t₁ t₂ left right).phase =
        (0 : ZMod 2) := by
  constructor
  · change grayNeutralChargeHom
      (∑ face : IcosahedralFace,
        kernelC60HexagonGraySixNativePasting
          t₁ t₂ left right face) =
        ((0 : Int), (120 : Int))
    rw [map_sum]
    calc
      (∑ face : IcosahedralFace, grayNeutralChargeHom
        (kernelC60HexagonGraySixNativePasting
          t₁ t₂ left right face)) =
          ∑ _face : IcosahedralFace, ((0 : Int), (6 : Int)) := by
            apply Finset.sum_congr rfl
            intro face _
            exact (kernelC60HexagonGraySixNativePasting_components
              t₁ t₂ left right face).1
      _ = ((0 : Int), (120 : Int)) := by
            simp only [Finset.sum_const, Finset.card_univ]
            rw [kernelCertifiedHexagonCycle_twenty]
            decide
  · change grayNeutralPhaseHom
      (∑ face : IcosahedralFace,
        kernelC60HexagonGraySixNativePasting
          t₁ t₂ left right face) =
        (0 : ZMod 2)
    rw [map_sum]
    calc
      (∑ face : IcosahedralFace, grayNeutralPhaseHom
        (kernelC60HexagonGraySixNativePasting
          t₁ t₂ left right face)) =
          ∑ _face : IcosahedralFace, (0 : ZMod 2) := by
            apply Finset.sum_congr rfl
            intro face _
            exact (kernelC60HexagonGraySixNativePasting_components
              t₁ t₂ left right face).2
      _ = (0 : ZMod 2) := by simp

/-- Exact comparison IN THE INDEPENDENT COMMUTATIVE NATIVE TARGET:
all 20 hexagons' 120 edge occurrences agree with the 90 distinct
edge labels plus the 30 cross labels, as typed 3-cells.

This does not REPLACE a future proof of the underlying geometric
incidence-multiset equality for each separate edge. -/
theorem kernelC60AllTwentyHexagonGrayTotal_eq_all90_add_cross30 :
    kernelC60AllTwentyHexagonGrayTotal t₁ t₂ left right =
      c60AllNinetyGrayTotal t₁ t₂ left right +
        c60CrossThirtyGrayTotal t₁ t₂ left right := by
  apply GradedThreeCell.ext
  · change
      (kernelC60AllTwentyHexagonGrayTotal
        t₁ t₂ left right).charge =
        (c60AllNinetyGrayTotal t₁ t₂ left right).charge +
          (c60CrossThirtyGrayTotal t₁ t₂ left right).charge
    rw [(kernelC60AllTwentyHexagonGrayTotal_components
        t₁ t₂ left right).1,
      (c60AllNinetyGrayTotal_components t₁ t₂ left right).1,
      (c60CrossThirtyGrayTotal_components t₁ t₂ left right).1]
    decide
  · change
      (kernelC60AllTwentyHexagonGrayTotal
        t₁ t₂ left right).phase =
        (c60AllNinetyGrayTotal t₁ t₂ left right).phase +
          (c60CrossThirtyGrayTotal t₁ t₂ left right).phase
    rw [(kernelC60AllTwentyHexagonGrayTotal_components
        t₁ t₂ left right).2,
      (c60AllNinetyGrayTotal_components t₁ t₂ left right).2,
      (c60CrossThirtyGrayTotal_components t₁ t₂ left right).2]
    decide

#print axioms kernelC60HexagonGraySixSquareList_eq
#print axioms kernelC60HexagonGraySixSquareSum_components
#print axioms kernelC60HexagonGraySixNativePasting
#print axioms kernelC60HexagonGraySixNativePasting_isCategoryComp
#print axioms kernelC60HexagonGraySixNativePasting_components
#print axioms kernelC60HexagonGrayPasting_eq_sum
#print axioms kernelC60AllTwentyHexagonGrayTotal
#print axioms kernelC60AllTwentyHexagonGrayTotal_components
#print axioms kernelC60AllTwentyHexagonGrayTotal_eq_all90_add_cross30

end OriginalHexagonPasting
end
end KUOS.DependentOriginationGrayKernelHexagonSixCellPastingV5_157
