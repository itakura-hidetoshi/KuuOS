import KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
import KUOS.DependentOriginationGrayC60AllNinetyEdgePastingV5_157
import KUOS.DependentOriginationGrayC60WangBiNativeGrayTwoCellsV5_171

namespace KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralHigherChargeV5_155
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayF55PhaseRealizationV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60AllNinetyEdgePastingV5_157
open KUOS.DependentOriginationGrayC60WangBiNativeGrayTwoCellsV5_171
open KUOS.DependentOriginationGrayC60NativePathFunctorV5_189
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F43 / v5.191 — genuine C60 face-source 3-cell interchangers

F59-F42 constructed proof-relevant, TYPE-indexed original C60
pentagon/hexagon face 2-cells between original 60-object
Quiver.Path 1-morphisms, including genuine left/right contexts
and TWO distinct horizontal 2-cell pasting orders. Their
independent corrected F59 Gray path-transport images coincide,
but the raw 2-cell evidence was NOT identified.

Here construct a GENUINE TYPE-VALUED 3-cell *presentation*
between the original C60 face 2-cells:
  identity; primitive, honestly TYPED interchanger between
  the two genuine F42 horizontal orders; inverse; vertical
  composite; and BOTH original 1-path whiskerings.

We derive the ORIGINAL face-2-cell PARITY on all six original
F42 constructors: every genuine 5-edge pentagon or 6-edge
hexagon generator contributes one mod-two unit, identity zero,
vertical pasting adds, reversal negates (equivalently mod two),
and contextual whiskering preserves the degree.

The source 3-cell interchanger interprets into the ACTUAL
native F59 Gray-neutral 3-cell with ZERO Int×Int F58
generator charge and INDEPENDENT ZMod2 phase equal to
the two ORIGINAL face-2-cell parities' product. This is
EXACTLY the phase/charge of the old genuine typed
GradedThreeCell.exchange, not a fabricated F58 square charge.
On the ACTUAL north C60 pentagon, interchanging TWO nonzero
original face 2-cells has phase ONE and zero integer charges.
It gives a genuinely NONIDENTITY native Mathlib Cat 2-cell.

Prove both Gray-interchanger hexagon phase-distributivity laws
at actual concatenated C60 source face-2-cell pastings and
natural invariance under ALL source presented 3-cell changes
of face degree. The old F59-A full typed exchange naturality,
hexagons, pentagon and triangle remain available and intact.

SEPARATELY attach the existing TRUE original F55-B
disjoint-square PresentedCell (with the actual, independently
supplied pair of F54 local rotations) to ALL NINETY original
C60 physical 4-flag incidence squares via the already proved
F59-F2 actual original square carriers. Its target image is
(0,1; phase 1), not the FACE interchanger's (0,0; phase 1);
the charge distinction is proved at a genuine north around
edge. C60 physical edge flag-squares are NOT fake C60
four-edged surface faces.

CRITICAL SCOPE: this is a constructive THREE-CELL COMPUTAD
and a complete interpretation of its listed generators,
NOT YET a full nondegenerate Gray 3-category/functor:
freely presented 3-cell words still need 3-cell categorical
associativity/unit/interchange quotient laws, and the F54/F55
typed square boundaries are not canonically equivalent to
the newly presented C60 face-2-cell boundaries. There is NO
blanket identification of the two source 2-cell carriers,
no added axioms, no Stage-II omega identification.
-/

/-! ## I. Grading of the REAL C60 face 2-cell source presentation -/

/-- Mod-two physical-face generator degree of an ACTUAL,
proof-relevant original C60 face 2-cell.  This is a structural
recursion on all six F42 constructors and does NOT erase
the original typed 1-path endpoints or source 2-cell syntax. -/
def c60F43FaceDegree
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    (cell : C60F42PresentedFaceCell p q) : ZMod 2 := by
  induction cell with
  | ident _ => exact 0
  | physicalFace _ => exact 1
  | symm cell ih => exact -ih
  | trans left right ihLeft ihRight => exact ihLeft + ihRight
  | whiskerLeft prior cell ih => exact ih
  | whiskerRight cell suffix ih => exact ih

theorem c60F43FaceDegree_ident
    {a b : IcosahedralDart} (p : Quiver.Path a b) :
    c60F43FaceDegree (C60F42PresentedFaceCell.ident p) = 0 := rfl

theorem c60F43FaceDegree_physicalFace
    (f : TruncatedIcosahedralSeedFace) :
    c60F43FaceDegree (C60F42PresentedFaceCell.physicalFace f) =
      (1 : ZMod 2) := rfl

theorem c60F43FaceDegree_symm
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    (α : C60F42PresentedFaceCell p q) :
    c60F43FaceDegree (.symm α) = -c60F43FaceDegree α := rfl

theorem c60F43FaceDegree_trans
    {a b : IcosahedralDart} {p q r : Quiver.Path a b}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell q r) :
    c60F43FaceDegree (.trans α β) =
      c60F43FaceDegree α + c60F43FaceDegree β := rfl

theorem c60F43FaceDegree_whiskerLeft
    {a b c : IcosahedralDart} (prior : Quiver.Path a b)
    {p q : Quiver.Path b c}
    (α : C60F42PresentedFaceCell p q) :
    c60F43FaceDegree (.whiskerLeft prior α) =
      c60F43FaceDegree α := rfl

theorem c60F43FaceDegree_whiskerRight
    {a b c : IcosahedralDart} {p q : Quiver.Path a b}
    (α : C60F42PresentedFaceCell p q)
    (suffix : Quiver.Path b c) :
    c60F43FaceDegree (.whiskerRight α suffix) =
      c60F43FaceDegree α := rfl

/-- Full source horizontal pasting in the left-first order
preserves exactly the SUM of the two original physical-face
generator parities, with actual C60 dependent endpoints. -/
theorem c60F43FaceDegree_horizontalLeftFirst
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s) :
    c60F43FaceDegree (α.horizontalLeftFirst β) =
      c60F43FaceDegree α + c60F43FaceDegree β := by
  rfl

theorem c60F43FaceDegree_horizontalRightFirst
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s) :
    c60F43FaceDegree (α.horizontalRightFirst β) =
      c60F43FaceDegree α + c60F43FaceDegree β := by
  rfl

/-! ## II. A real proof-relevant C60 3-cell source with interchanger -/

/-- A Type-valued genuinely GLOBULAR source 3-cell presentation
between actual parallel F42 physical face 2-cells. Every
constructor respects both original C60 1-path boundaries.
This is raw presented 3-cell evidence, not yet a strict
Gray-category quotient imposing all interchange laws. -/
inductive C60F43PresentedThreeCell :
    {a b : IcosahedralDart} →
    {p q : Quiver.Path a b} →
    C60F42PresentedFaceCell p q →
    C60F42PresentedFaceCell p q → Type where
  | ident {a b : IcosahedralDart} {p q : Quiver.Path a b}
      (α : C60F42PresentedFaceCell p q) :
      C60F43PresentedThreeCell α α
  | interchange {a b c : IcosahedralDart}
      {p q : Quiver.Path a b} {r s : Quiver.Path b c}
      (α : C60F42PresentedFaceCell p q)
      (β : C60F42PresentedFaceCell r s) :
      C60F43PresentedThreeCell
        (α.horizontalLeftFirst β)
        (α.horizontalRightFirst β)
  | symm {a b : IcosahedralDart} {p q : Quiver.Path a b}
      {α β : C60F42PresentedFaceCell p q}
      (cell : C60F43PresentedThreeCell α β) :
      C60F43PresentedThreeCell β α
  | trans {a b : IcosahedralDart} {p q : Quiver.Path a b}
      {α β γ : C60F42PresentedFaceCell p q}
      (left : C60F43PresentedThreeCell α β)
      (right : C60F43PresentedThreeCell β γ) :
      C60F43PresentedThreeCell α γ
  | whiskerLeft {a b c : IcosahedralDart}
      (prior : Quiver.Path a b)
      {p q : Quiver.Path b c}
      {α β : C60F42PresentedFaceCell p q}
      (cell : C60F43PresentedThreeCell α β) :
      C60F43PresentedThreeCell
        (.whiskerLeft prior α) (.whiskerLeft prior β)
  | whiskerRight {a b c : IcosahedralDart}
      {p q : Quiver.Path a b}
      {α β : C60F42PresentedFaceCell p q}
      (cell : C60F43PresentedThreeCell α β)
      (suffix : Quiver.Path b c) :
      C60F43PresentedThreeCell
        (.whiskerRight α suffix) (.whiskerRight β suffix)

/-- SOURCE PARITY invariance under EVERY C60 presented 3-cell:
the source and target F42 face 2-cells have equal total
degree, even if their raw source witnesses are distinct.
For the interchanger this uses the two independently
constructed genuine horizontal source 2-cell pasting orders. -/
theorem C60F43PresentedThreeCell.preservesFaceDegree
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    {α β : C60F42PresentedFaceCell p q}
    (cell : C60F43PresentedThreeCell α β) :
    c60F43FaceDegree α = c60F43FaceDegree β := by
  induction cell with
  | ident _ => rfl
  | interchange α β =>
      rw [c60F43FaceDegree_horizontalLeftFirst,
        c60F43FaceDegree_horizontalRightFirst]
  | symm cell ih => exact ih.symm
  | trans left right ihLeft ihRight => exact ihLeft.trans ihRight
  | whiskerLeft prior cell ih => exact ih
  | whiskerRight cell suffix ih => exact ih

/-! ## III. Native F59 Gray 3-cell and Mathlib Cat 2-cell image -/

/-- The ACTUAL neutral native Gray interchanger induced by two
original C60 face 2-cells: full zero F58 Int×Int charge and
nontrivial independent ZMod 2 phase = face parity product.
This agrees in BOTH components with the existing genuine
typed F59 GradedThreeCell.exchange on the two grades. -/
def c60F43PhysicalInterchangerNative
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s) :
    GradedThreeCell 0 0 :=
  ⟨rfl, (0, 0), c60F43FaceDegree α * c60F43FaceDegree β⟩

theorem c60F43PhysicalInterchanger_nativeF59Components
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s) :
    (c60F43PhysicalInterchangerNative α β).charge =
      (GradedThreeCell.exchange
        (c60F43FaceDegree α) (c60F43FaceDegree β)).charge ∧
    (c60F43PhysicalInterchangerNative α β).phase =
      (GradedThreeCell.exchange
        (c60F43FaceDegree α) (c60F43FaceDegree β)).phase := by
  exact ⟨rfl, rfl⟩

/-- FULL recursive native image of every source C60 3-cell
constructor: identity→zero, actual primitive interchanger→
the complete F59 charge/phase, inverse→negative,
vertical paste→native addition, both original 1-path
whiskerings→unchanged braided 3-cell. -/
def C60F43PresentedThreeCell.toNative
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    {α β : C60F42PresentedFaceCell p q}
    (cell : C60F43PresentedThreeCell α β) :
    GradedThreeCell 0 0 := by
  induction cell with
  | ident _ => exact 0
  | interchange α β => exact c60F43PhysicalInterchangerNative α β
  | symm cell ih => exact -ih
  | trans left right ihLeft ihRight => exact ihLeft + ihRight
  | whiskerLeft prior cell ih => exact ih
  | whiskerRight cell suffix ih => exact ih

theorem C60F43PresentedThreeCell.toNative_ident
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    (α : C60F42PresentedFaceCell p q) :
    (C60F43PresentedThreeCell.ident α).toNative = 0 := rfl

theorem C60F43PresentedThreeCell.toNative_interchange
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s) :
    (C60F43PresentedThreeCell.interchange α β).toNative =
      c60F43PhysicalInterchangerNative α β := rfl

theorem C60F43PresentedThreeCell.toNative_trans
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    {α β γ : C60F42PresentedFaceCell p q}
    (f : C60F43PresentedThreeCell α β)
    (g : C60F43PresentedThreeCell β γ) :
    (C60F43PresentedThreeCell.trans f g).toNative =
      f.toNative + g.toNative := rfl

theorem C60F43PresentedThreeCell.toNative_symm
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    {α β : C60F42PresentedFaceCell p q}
    (f : C60F43PresentedThreeCell α β) :
    (C60F43PresentedThreeCell.symm f).toNative =
      -f.toNative := rfl

/-- Interpretation of the genuine source 3-cell interchange
as a NONTRIVIAL native Mathlib Cat bicategorical 2-morphism,
without erasing its mod-two exchange phase or F58 charges. -/
def c60F43InterchangerNativeCatTwoCell
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s) :
    (𝟭 GrayGrade) ⟶ (𝟭 GrayGrade) :=
  c60WangBiGrayNativeTwoCell
    (C60F43PresentedThreeCell.interchange α β).toNative

/-! ## IV. Actual NORTH pentagon interchanger and both hexagons -/

/-- Genuine original physical north pentagon face 2-cell:
an actual five-edge C60 path reduced to the real dart
identity, NOT an invented square C60 surface face. -/
def c60F43NorthPentagonFaceTwoCell :
    C60F42PresentedFaceCell
      (c60F41PentagonBoundaryLoop .north) Quiver.Path.nil :=
  C60F42PresentedFaceCell.physicalFace (.aroundVertex .north)

/-- Two independent ACTUAL north pentagon face relations have
a well-typed source 3-cell comparing the two original
horizontal composition orders. -/
def c60F43NorthPentagonInterchange :
    C60F43PresentedThreeCell
      (c60F43NorthPentagonFaceTwoCell.horizontalLeftFirst
        c60F43NorthPentagonFaceTwoCell)
      (c60F43NorthPentagonFaceTwoCell.horizontalRightFirst
        c60F43NorthPentagonFaceTwoCell) :=
  .interchange c60F43NorthPentagonFaceTwoCell
    c60F43NorthPentagonFaceTwoCell

/-- The nontrivial F59 odd×odd interchange is realized on
TWO physical north pentagon 2-cell generators: first F58
charge remains zero and NEW independent Gray phase is 1. -/
theorem c60F43NorthPentagonInterchange_components :
    c60F43NorthPentagonInterchange.toNative.charge =
        ((0 : Int), (0 : Int)) ∧
      c60F43NorthPentagonInterchange.toNative.phase =
        (1 : ZMod 2) := by
  exact ⟨rfl, rfl⟩

theorem c60F43NorthPentagonInterchange_ne_identity :
    c60F43NorthPentagonInterchange.toNative ≠
      (0 : GradedThreeCell 0 0) := by
  intro h
  have hp := congrArg GradedThreeCell.phase h
  have hphase := c60F43NorthPentagonInterchange_components.2
  rw [hphase] at hp
  exact (by decide : (1 : ZMod 2) ≠ 0) hp

theorem c60F43NorthPentagonNativeCatTwoCell_nonidentity :
    c60F43InterchangerNativeCatTwoCell
      c60F43NorthPentagonFaceTwoCell
      c60F43NorthPentagonFaceTwoCell ≠
        (𝟙 (𝟭 GrayGrade)) := by
  intro h
  have hz :=
    c60WangBiGrayNativeTwoCell_injective
      (h.trans c60WangBiGrayNativeTwoCell_zero.symm)
  exact c60F43NorthPentagonInterchange_ne_identity hz

/-- FIRST C60 source-face Gray exchange hexagon, for THREE
genuine, dependently composable original physical face
2-cell witnesses: interchanging α past (β⊗γ) has the SAME
full native 3-cell as the sum of exchanges with β and γ.
This is the target hexagon phase identity, NOT an unproved
equality between raw source 3-cell pasting witnesses. -/
theorem c60F43Interchange_hexagon_forward
    {a b c d : IcosahedralDart}
    {p q : Quiver.Path a b}
    {r s : Quiver.Path b c}
    {t u : Quiver.Path c d}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s)
    (γ : C60F42PresentedFaceCell t u) :
    c60F43PhysicalInterchangerNative α (β.horizontalLeftFirst γ) =
      c60F43PhysicalInterchangerNative α β +
        c60F43PhysicalInterchangerNative α γ := by
  apply GradedThreeCell.ext
  · rfl
  · change c60F43FaceDegree α *
      (c60F43FaceDegree β + c60F43FaceDegree γ) =
      c60F43FaceDegree α * c60F43FaceDegree β +
        c60F43FaceDegree α * c60F43FaceDegree γ
    exact mul_add _ _ _

/-- SECOND original C60 source-face Gray exchange hexagon. -/
theorem c60F43Interchange_hexagon_reverse
    {a b c d : IcosahedralDart}
    {p q : Quiver.Path a b}
    {r s : Quiver.Path b c}
    {t u : Quiver.Path c d}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s)
    (γ : C60F42PresentedFaceCell t u) :
    c60F43PhysicalInterchangerNative (α.horizontalLeftFirst β) γ =
      c60F43PhysicalInterchangerNative α γ +
        c60F43PhysicalInterchangerNative β γ := by
  apply GradedThreeCell.ext
  · rfl
  · change (c60F43FaceDegree α + c60F43FaceDegree β) *
      c60F43FaceDegree γ =
      c60F43FaceDegree α * c60F43FaceDegree γ +
        c60F43FaceDegree β * c60F43FaceDegree γ
    exact add_mul _ _ _

/-- The actual interchanger phase is NATURAL in the original
face-2-cell source under any already-constructed proof-
relevant original 3-cell modification of its left input. -/
theorem c60F43Interchange_left_naturality
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {α α' : C60F42PresentedFaceCell p q}
    (h : C60F43PresentedThreeCell α α')
    (β : C60F42PresentedFaceCell r s) :
    c60F43PhysicalInterchangerNative α β =
      c60F43PhysicalInterchangerNative α' β := by
  have hd := h.preservesFaceDegree
  apply GradedThreeCell.ext
  · rfl
  · change c60F43FaceDegree α * c60F43FaceDegree β =
      c60F43FaceDegree α' * c60F43FaceDegree β
    rw [hd]

theorem c60F43Interchange_right_naturality
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (α : C60F42PresentedFaceCell p q)
    {β β' : C60F42PresentedFaceCell r s}
    (h : C60F43PresentedThreeCell β β') :
    c60F43PhysicalInterchangerNative α β =
      c60F43PhysicalInterchangerNative α β' := by
  have hd := h.preservesFaceDegree
  apply GradedThreeCell.ext
  · rfl
  · change c60F43FaceDegree α * c60F43FaceDegree β =
      c60F43FaceDegree α * c60F43FaceDegree β'
    rw [hd]

/-! ## V. True physical edge-flag F55 source 3-cells, kept distinct -/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section RealC60FlagF55
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

/-- ACTUAL ORIGINAL F55 freely-presented 3-cell from true
left-first to true right-first F54 rotation paths, on EVERY
physical C60 edge. Both the pentagon/hexagon around flags
and the genuine cross-edge two-hexagon flags carry a
geometric square, not a newly fabricated polygonal face. -/
theorem c60F43AllNinetyPhysicalFlags_haveGenuineF55Square
    (edge : TruncatedIcosahedralEdge) :
    ∃ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell
        (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right)
        (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right),
      c60F55SourceNative cell =
        c60AllNinetyGrayCell t₁ t₂ left right edge := by
  cases edge with
  | around e =>
      exact ⟨(OriginalC60FlagSquareWithF55Generator.canonical
        e left right).squareCell, rfl⟩
  | cross e =>
      exact ⟨(OriginalC60CrossHexagonSquareWithF55Generator.canonical
        e left right).squareCell, rfl⟩

/-- The original true physical F55 square source, seen as a
nonidentity native Cat 2-cell (a degenerate-model Gray 3-cell),
has INDEPENDENT second F58 charge ONE and Gray phase ONE on
every one of the ninety real C60 flag-squares. -/
theorem c60F43PhysicalF55All90_chargePhase
    (edge : TruncatedIcosahedralEdge) :
    (c60AllNinetyGrayCell t₁ t₂ left right edge).charge =
      ((0 : Int), (1 : Int)) ∧
    (c60AllNinetyGrayCell t₁ t₂ left right edge).phase =
      (1 : ZMod 2) := by
  rw [c60AllNinetyGrayCell_eq]
  exact originalF55BraidedSquareGenerator_complete

/-- The authentic F55-B independent local-rotation square on
the actual north C60 pentagon/hexagon edge is NOT the same
3-cell as the NEW original-face horizontal interchanger.
Both have phase 1 but genuinely DIFFERENT second integer
F58 charges (1 versus 0), retained in the real F59 target. -/
theorem c60F43NorthFaceInterchange_ne_actualF55Square
    (edge : TruncatedIcosahedralAroundEdge) :
    c60F43NorthPentagonInterchange.toNative ≠
      c60AllNinetyGrayCell t₁ t₂ left right (.around edge) := by
  intro h
  have hc := congrArg
    (fun g : GradedThreeCell 0 0 => g.charge.2) h
  have hz := c60F43NorthPentagonInterchange_components.1
  have hone :=
    (c60F43PhysicalF55All90_chargePhase
      t₁ t₂ left right (.around edge)).1
  change (0 : Int) =
    (c60AllNinetyGrayCell t₁ t₂ left right (.around edge)).charge.2 at hc
  rw [hone] at hc
  exact (by decide : (0 : Int) ≠ 1) hc

end RealC60FlagF55

#print axioms c60F43FaceDegree_physicalFace
#print axioms c60F43FaceDegree_horizontalLeftFirst
#print axioms c60F43FaceDegree_horizontalRightFirst
#print axioms C60F43PresentedThreeCell
#print axioms C60F43PresentedThreeCell.preservesFaceDegree
#print axioms c60F43PhysicalInterchanger_nativeF59Components
#print axioms C60F43PresentedThreeCell.toNative
#print axioms C60F43PresentedThreeCell.toNative_interchange
#print axioms C60F43PresentedThreeCell.toNative_trans
#print axioms c60F43NorthPentagonInterchange_components
#print axioms c60F43NorthPentagonInterchange_ne_identity
#print axioms c60F43NorthPentagonNativeCatTwoCell_nonidentity
#print axioms c60F43Interchange_hexagon_forward
#print axioms c60F43Interchange_hexagon_reverse
#print axioms c60F43Interchange_left_naturality
#print axioms c60F43Interchange_right_naturality
#print axioms c60F43AllNinetyPhysicalFlags_haveGenuineF55Square
#print axioms c60F43PhysicalF55All90_chargePhase
#print axioms c60F43NorthFaceInterchange_ne_actualF55Square

end
end KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
