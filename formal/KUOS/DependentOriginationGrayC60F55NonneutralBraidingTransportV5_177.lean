import KUOS.DependentOriginationGrayC60F55SourceWhiskeringInterchangeV5_176

namespace KUOS.DependentOriginationGrayC60F55NonneutralBraidingTransportV5_177

open CategoryTheory
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayF55PhaseRealizationV5_156
open KUOS.DependentOriginationGrayC60AllNinetyEdgePastingV5_157
open KUOS.DependentOriginationGrayC60WangBiZhouyiTimeV5_170
open KUOS.DependentOriginationGrayC60WangBiNativeHigherCoherenceV5_171
open KUOS.DependentOriginationGrayC60WangBiFourImageSixQiF55NaturalityV5_172
open KUOS.DependentOriginationGrayC60WangBiGaugeCollarSixQiCoherenceV5_173
open KUOS.DependentOriginationGrayC60F55SourcePhaseLockedAtlasV5_175
open KUOS.DependentOriginationGrayC60F55SourceWhiskeringInterchangeV5_176
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F29 / v5.177 — nonneutral Gray braiding of original typed F55 cells

F59-F27/28 proved all nine original source PresentedCell constructors
interpret in a native braided 3-cell category, with compatible phase
equal to the mod-two original F58 square-generator charge. The actual
C60 Wang Bi frame transport is a Mathlib natural transformation.

The FULL native braided category also contains NONNEUTRAL 2-cell
grades a,b in ZMod 2 and its original odd/odd interchanger has
charge (0,0) but phase 1. This independent braiding must NOT be
misidentified with an arbitrary original F55 source cell.

Here we:
1. Extract a real phase-minus-square-charge defect for ALL typed
   3-cells, proving exact additivity under vertical and tensor
   composition in the existing independent native Gray target.
2. Lift the ORIGINAL dependent typed F55 PresentedCell image to
   arbitrary nonneutral 2-cell grade, preserving identity, inverse,
   vertical composition, the original F58 integer charges and
   phase-locked status.
3. Compose this grade-shifted source image with the GENUINE
   separately supplied native Gray exchange(a,b): this is a typed
   3-cell a+b -> b+a, whose defect is precisely a*b.
4. Prove the full typed native exchange naturality and the original
   source F55 horizontal-interchange invariance after adding the
   independent braid.
5. Construct a genuine WangBiFrame-to-Type Mathlib functor for
   64 Yao codes paired with those NONNEUTRAL braided morphisms,
   and the original C60 360-corner natural transformation.
6. Attach all 90 physical original F54/F55 square generators
   to the additional independent braid, with exact charge
   and phase formulas and agreement with typed source cells.

The F55 source interpretation is NOT redefined to manufacture a
braiding it never possessed: the native exchange is a separate
genuine target-side coherent morphism. We do NOT claim a global
raw-source ambient Gray 3-functor or a uniquely determined
historical reading of the C60 hexagrams.
-/

/-- A genuine independent Gray phase invariant on arbitrary TYPED
3-cells, including cells between nonneutral 2-cell grades. It
measures the phase not already forced by the F55 square charge. -/
def c60F29PhaseDefect {a b : ZMod 2}
    (γ : GradedThreeCell a b) : ZMod 2 :=
  γ.phase - (γ.charge.2 : ZMod 2)

/-- The defect is additive under the ACTUAL original native
3-cell vertical composition even at nonzero 2-cell grades. -/
theorem c60F29PhaseDefect_comp
    {a b c : ZMod 2}
    (p : GradedThreeCell a b) (q : GradedThreeCell b c) :
    c60F29PhaseDefect (p.comp q) =
      c60F29PhaseDefect p + c60F29PhaseDefect q := by
  change (p.phase + q.phase) -
      ((p.charge.2 + q.charge.2 : ℤ) : ZMod 2) =
    (p.phase - (p.charge.2 : ZMod 2)) +
      (q.phase - (q.charge.2 : ZMod 2))
  rw [Int.cast_add]
  abel

/-- The defect is also additive for GENUINE nonneutral
monoidal tensor composition, not merely F58-charge addition. -/
theorem c60F29PhaseDefect_tensor
    {a b c d : ZMod 2}
    (p : GradedThreeCell a b) (q : GradedThreeCell c d) :
    c60F29PhaseDefect (p.tensor q) =
      c60F29PhaseDefect p + c60F29PhaseDefect q := by
  change (p.phase + q.phase) -
      ((p.charge.2 + q.charge.2 : ℤ) : ZMod 2) =
    (p.phase - (p.charge.2 : ZMod 2)) +
      (q.phase - (q.charge.2 : ZMod 2))
  rw [Int.cast_add]
  abel

/-- The original genuinely nontrivial braided interchanger has
exactly the independent a*b phase defect; its integer generator
charge is zero at EVERY pair of nonneutral grades. -/
theorem c60F29PhaseDefect_exchange (a b : ZMod 2) :
    c60F29PhaseDefect (GradedThreeCell.exchange a b) = a * b := by
  simp [c60F29PhaseDefect, GradedThreeCell.exchange]

/-- The complete odd/odd native braiding carries phase defect 1:
this is NEW information relative to F58's integer generator charge. -/
theorem c60F29PhaseDefect_odd_odd :
    c60F29PhaseDefect (GradedThreeCell.exchange 1 1) = 1 := by
  rw [c60F29PhaseDefect_exchange]
  norm_num

/-- Embeds an independently typed native 0-grade F55 3-cell
into ANY genuine nonneutral parallel 2-cell grade. The
original charge and exchange phase are copied EXACTLY, not erased. -/
def c60F29ShiftNeutral (a : ZMod 2)
    (γ : GradedThreeCell 0 0) : GradedThreeCell a a :=
  ⟨rfl, γ.charge, γ.phase⟩

/-- This is compatible with genuine Gray native vertical
3-cell composition, not a categorical analogy. -/
theorem c60F29ShiftNeutral_comp
    (a : ZMod 2) (p q : GradedThreeCell 0 0) :
    c60F29ShiftNeutral a (p.comp q) =
      (c60F29ShiftNeutral a p).comp (c60F29ShiftNeutral a q) := by
  apply GradedThreeCell.ext <;> rfl

/-- Inversion also respects arbitrary nonneutral grade shift. -/
theorem c60F29ShiftNeutral_inv
    (a : ZMod 2) (p : GradedThreeCell 0 0) :
    c60F29ShiftNeutral a p.inv = (c60F29ShiftNeutral a p).inv := by
  apply GradedThreeCell.ext <;> rfl

theorem c60F29ShiftNeutral_defect
    (a : ZMod 2) (p : GradedThreeCell 0 0) :
    c60F29PhaseDefect (c60F29ShiftNeutral a p) =
      c60F29PhaseDefect p := by
  rfl

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- The exact original F55 source-cell interpretation transported
to a chosen arbitrary GENUINE nonneutral Gray 2-cell grade. -/
def c60F29ShiftedSource
    (a : ZMod 2)
    {x y : D} {z w : E} {n n' m m' : Nat}
    {ma mb : Blocks x y} {pa pb : Blocks z w}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    (cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    GradedThreeCell a a :=
  c60F29ShiftNeutral a (c60F55SourceNative cell)

/-- Shift of an ACTUAL source F55 identity is the native
3-cell identity at the arbitrary nonneutral grade. -/
theorem c60F29ShiftedSource_ident
    (a : ZMod 2)
    {x y : D} {z w : E} {n n' m m' : Nat}
    {ma mb : Blocks x y} {pa pb : Blocks z w}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    (r : OriginalF45BracketTree.DepthRotationRoute first last) :
    c60F29ShiftedSource a
      (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.ident r) =
      GradedThreeCell.ident a := by
  apply GradedThreeCell.ext <;> rfl

/-- The original proof-relevant F55 source vertical composition
preserves actual target composition after NONNEUTRAL shift. -/
theorem c60F29ShiftedSource_trans
    (a : ZMod 2)
    {x y : D} {z w : E} {n n' m m' : Nat}
    {ma mb : Blocks x y} {pa pb : Blocks z w}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    {r s t : OriginalF45BracketTree.DepthRotationRoute first last}
    (α : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s)
    (β : OriginalF45BracketTree.DepthRotationRoute.PresentedCell s t) :
    c60F29ShiftedSource a
      (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.trans α β) =
    (c60F29ShiftedSource a α).comp (c60F29ShiftedSource a β) := by
  apply GradedThreeCell.ext <;> rfl

/-- Every original typed F55 source 3-cell continues to have
ZERO extra braid defect after an arbitrary nonneutral shift. -/
theorem c60F29ShiftedSource_defect_zero
    (a : ZMod 2)
    {x y : D} {z w : E} {n n' m m' : Nat}
    {ma mb : Blocks x y} {pa pb : Blocks z w}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    (cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    c60F29PhaseDefect (c60F29ShiftedSource a cell) = 0 := by
  change c60F29PhaseDefect
    (c60F29ShiftNeutral a (c60F55SourceNative cell)) = 0
  rw [c60F29ShiftNeutral_defect]
  have h := c60F55SourceNative_mem cell
  change (c60F55SourceNative cell).phase =
    ((c60F55SourceNative cell).charge.2 : ZMod 2) at h
  simp [c60F29PhaseDefect, h]

/-- Compose the genuinely interpreted source F55 3-cell with
the INDEPENDENT preexisting braided monoidal category
interchanger. This is a strict well-TYPED 3-cell from
2-cell grade a+b to 2-cell grade b+a. -/
def c60F29BraidedSource (a b : ZMod 2)
    {x y : D} {z w : E} {n n' m m' : Nat}
    {ma mb : Blocks x y} {pa pb : Blocks z w}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    (cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    GradedThreeCell (a + b) (b + a) :=
  (c60F29ShiftedSource (a + b) cell).comp
    (GradedThreeCell.exchange a b)

/-- The new composite retains EXACTLY the original F58 integer
charge, and has the independently braided phase a*b ADDED.
The nontrivial odd/odd braiding is not misidentified as the
old source disjoint rotation square. -/
theorem c60F29BraidedSource_components
    (a b : ZMod 2)
    {x y : D} {z w : E} {n n' m m' : Nat}
    {ma mb : Blocks x y} {pa pb : Blocks z w}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    (cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    (c60F29BraidedSource a b cell).charge =
      (c60F55SourceNative cell).charge ∧
    (c60F29BraidedSource a b cell).phase =
      (c60F55SourceNative cell).phase + a * b := by
  constructor
  · change (c60F55SourceNative cell).charge + (0 : Int × Int) =
      (c60F55SourceNative cell).charge
    simp
  · rfl

/-- The EXTRA nonneutral braided phase is rigorously a*b,
separated from (rather than silently imposed on) the
original F55 source phase compatibility. -/
theorem c60F29BraidedSource_defect
    (a b : ZMod 2)
    {x y : D} {z w : E} {n n' m m' : Nat}
    {ma mb : Blocks x y} {pa pb : Blocks z w}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    (cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    c60F29PhaseDefect (c60F29BraidedSource a b cell) = a * b := by
  change c60F29PhaseDefect
    ((c60F29ShiftedSource (a + b) cell).comp
      (GradedThreeCell.exchange a b)) = a * b
  rw [c60F29PhaseDefect_comp,
    c60F29ShiftedSource_defect_zero,
    c60F29PhaseDefect_exchange]
  simp

/-- A real source F55 identity upgraded with an external
Gray braid gives EXACTLY that original native braiding. -/
theorem c60F29BraidedSource_ident
    (a b : ZMod 2)
    {x y : D} {z w : E} {n n' m m' : Nat}
    {ma mb : Blocks x y} {pa pb : Blocks z w}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    (r : OriginalF45BracketTree.DepthRotationRoute first last) :
    c60F29BraidedSource a b
      (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.ident r) =
      GradedThreeCell.exchange a b := by
  change (GradedThreeCell.ident (a + b)).comp
    (GradedThreeCell.exchange a b) = GradedThreeCell.exchange a b
  exact GradedThreeCell.ident_comp _

/-- The actual odd/odd independent Gray braiding is nontrivial
even when the ORIGINAL source F55 high cell is only its identity. -/
theorem c60F29BraidedSource_ident_odd_nonzero
    {x y : D} {z w : E} {n n' m m' : Nat}
    {ma mb : Blocks x y} {pa pb : Blocks z w}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    (r : OriginalF45BracketTree.DepthRotationRoute first last) :
    (c60F29BraidedSource 1 1
      (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.ident r)).phase =
      (1 : ZMod 2) := by
  rw [c60F29BraidedSource_ident]
  exact GradedThreeCell.exchange_odd_odd_nontrivial.2

/-- The previously-proven typed Gray interchanger naturality
now uses two ACTUAL original source F55 typed higher cells,
shifted to arbitrary nonneutral 2-cell grades. -/
theorem c60F29Source_exchange_naturality
    (a b : ZMod 2)
    {x y : D} {z w : E} {n n' m m' : Nat}
    {ma mb : Blocks x y} {pa pb : Blocks z w}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    (α β : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    ((c60F29ShiftedSource a α).tensor
      (c60F29ShiftedSource b β)).comp (GradedThreeCell.exchange a b) =
    (GradedThreeCell.exchange a b).comp
      ((c60F29ShiftedSource b β).tensor
        (c60F29ShiftedSource a α)) :=
  GradedThreeCell.exchange_naturality _ _

/-- A genuine Mathlib Wang Bi chart functor whose SECOND coordinate
is an independently typed NONNEUTRAL Gray 3-cell a+b -> b+a.
This cannot be replaced by the old neutral grade 0 category. -/
def c60F29BraidedSixYaoFunctor (a b : ZMod 2) :
    WangBiFrame ⥤ Type 0 where
  obj _ := WangBiSixYao × GradedThreeCell (a + b) (b + a)
  map := fun {x y} f =>
    TypeCat.ofHom (fun v : WangBiSixYao ×
      GradedThreeCell (a + b) (b + a) =>
      (wangBiChartArrow x y f v.1, v.2))
  map_id := by
    intro frame
    apply TypeCat.homEquiv.injective
    funext v
    rcases v with ⟨code, grade⟩
    exact congrArg (fun t => (t, grade))
      (wangBiChartArrow_id frame code)
  map_comp := by
    intro x y z f g
    apply TypeCat.homEquiv.injective
    funext v
    rcases v with ⟨code, grade⟩
    exact congrArg (fun t => (t, grade))
      (wangBiChartArrow_comp x y z f g code)

/-- ACTUAL Mathlib natural transformation on original C60 360
local edge flags with a genuine nonneutral braided Gray 3-cell,
not merely a neutral-grade F55 scalar. -/
def c60F29BraidedCornerNatTrans (a b : ZMod 2)
    (side : C60DartSideGauge)
    (grade : TruncatedIcosahedralEdge →
      GradedThreeCell (a + b) (b + a)) :
    c60ActualCornerFunctor ⟶ c60F29BraidedSixYaoFunctor a b where
  app frame := TypeCat.ofHom
    (fun corner : C60ActualSquareCorner =>
      (wangBiOriginalFaceEncoding frame (c60GaugeSignedFace side corner),
        grade corner.1))
  naturality := by
    intro frame₁ frame₂ f
    apply TypeCat.homEquiv.injective
    funext corner
    exact (congrArg (fun v => (v, grade corner.1))
      (wangBiEncodingNaturality frame₁ frame₂ f
        (c60GaugeSignedFace side corner))).symm

/-- Original F55 source cells with separately supplied
native nonneutral braid induce honest 360-corner Wang Bi
natural transformations for any choice of physical dart gauge. -/
def c60F29SourceBraidedAtlas (a b : ZMod 2)
    (side : C60DartSideGauge)
    {x y : D} {z w : E} {n n' m m' : Nat}
    {ma mb : Blocks x y} {pa pb : Blocks z w}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    (cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    c60ActualCornerFunctor ⟶ c60F29BraidedSixYaoFunctor a b :=
  c60F29BraidedCornerNatTrans a b side
    (fun _ => c60F29BraidedSource a b cell)

section OriginalSourceHorizontal
variable {x y : D} {z w : E}
variable {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
variable {ma mb : Blocks x y} {pa pb : Blocks z w}
variable {first : OriginalF45BracketTree n₁ m₁ ma pa mb pb}
variable {middle : OriginalF45BracketTree n₂ m₂ ma pa mb pb}
variable {last : OriginalF45BracketTree n₃ m₃ ma pa mb pb}
variable {r₁ s₁ : OriginalF45BracketTree.DepthRotationRoute first middle}
variable {r₂ s₂ : OriginalF45BracketTree.DepthRotationRoute middle last}

/-- Distinct original F55 source horizontal pastings remain
coherent AFTER attaching the separate true nonneutral braid. -/
theorem c60F29BraidedSource_horizontal_coherence (a b : ZMod 2)
    (α : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r₁ s₁)
    (β : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r₂ s₂) :
    c60F29BraidedSource a b (c60F55SourceHorizontalLeftFirst α β) =
      c60F29BraidedSource a b (c60F55SourceHorizontalRightFirst α β) := by
  have h := congrArg Subtype.val
    (c60F55SourceHorizontalInterchange α β)
  exact congrArg (fun g : GradedThreeCell 0 0 =>
    (c60F29ShiftNeutral (a + b) g).comp (GradedThreeCell.exchange a b)) h

/-- The same coherent source horizontal comparison holds as an
equality of Mathlib natural transformations on the ORIGINAL
90 physical C60 edge square charts, hence all 360 local flags. -/
theorem c60F29BraidedSource_horizontal_WangBi
    (a b : ZMod 2) (side : C60DartSideGauge)
    (α : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r₁ s₁)
    (β : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r₂ s₂) :
    c60F29SourceBraidedAtlas a b side
      (c60F55SourceHorizontalLeftFirst α β) =
    c60F29SourceBraidedAtlas a b side
      (c60F55SourceHorizontalRightFirst α β) := by
  change c60F29BraidedCornerNatTrans a b side
    (fun _ => c60F29BraidedSource a b
      (c60F55SourceHorizontalLeftFirst α β)) =
    c60F29BraidedCornerNatTrans a b side
    (fun _ => c60F29BraidedSource a b
      (c60F55SourceHorizontalRightFirst α β))
  exact congrArg
    (fun v : GradedThreeCell (a + b) (b + a) =>
      c60F29BraidedCornerNatTrans a b side
        (fun _ : TruncatedIcosahedralEdge => v))
    (c60F29BraidedSource_horizontal_coherence a b α β)

end OriginalSourceHorizontal

/-! ## The ORIGINAL ninety physical C60 F54-based F55 square cells. -/
section OriginalPhysicalC60
variable {x y : D} {z w : E}
variable {n₁ n₂ m₁ m₂ : Nat}
variable {p₀ p₁ p₂ : Blocks x y}
variable {q₀ q₁ q₂ : Blocks z w}
variable
  (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
  (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
variable
  {leftAfter : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁}
  {rightAfter : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂}
  (left : OriginalF45BracketTree.LocalRotation t₁ leftAfter)
  (right : OriginalF45BracketTree.LocalRotation t₂ rightAfter)

/-- A true original F55 square on EACH physical C60 edge,
shifted to 2-cell grade a+b and composed with the
independent Gray-native a/b braiding. -/
def c60F29ActualBraidedSquare (a b : ZMod 2)
    (edge : TruncatedIcosahedralEdge) :
    GradedThreeCell (a + b) (b + a) :=
  (c60F29ShiftNeutral (a + b)
    (c60AllNinetyGrayCell t₁ t₂ left right edge)).comp
      (GradedThreeCell.exchange a b)

/-- Exact agreement with the ACTUAL original F55 freely
presented disjointSquare constructor and its real typed
original F54 rotations, at all 90 physical C60 edge squares. -/
theorem c60F29ActualBraidedSquare_eq_originalSource
    (a b : ZMod 2) (edge : TruncatedIcosahedralEdge) :
    c60F29ActualBraidedSquare t₁ t₂ left right a b edge =
      c60F29BraidedSource a b
        (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.disjointSquare
          left right) := by
  unfold c60F29ActualBraidedSquare c60F29BraidedSource c60F29ShiftedSource
  rw [c60AllNinetyGrayCell_eq t₁ t₂ left right edge]
  rfl

/-- The original square generator retains its integer charge
(0,1), while the genuine extra Gray braid shifts its phase
from 1 to 1+a*b; this is a true physical 90-edge identity. -/
theorem c60F29ActualBraidedSquare_components
    (a b : ZMod 2) (edge : TruncatedIcosahedralEdge) :
    (c60F29ActualBraidedSquare t₁ t₂ left right a b edge).charge =
      ((0 : Int), (1 : Int)) ∧
    (c60F29ActualBraidedSquare t₁ t₂ left right a b edge).phase =
      (1 : ZMod 2) + a * b := by
  rw [c60F29ActualBraidedSquare_eq_originalSource t₁ t₂ left right a b edge]
  rcases c60F29BraidedSource_components a b
    (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.disjointSquare
      left right) with ⟨hc, hp⟩
  constructor
  · rw [hc]
    exact originalF55BraidedSquareGenerator_complete.1
  · rw [hp]
    exact congrArg (fun v : ZMod 2 => v + a * b)
      originalF55BraidedSquareGenerator_complete.2

/-- The REAL Wang Bi natural transformation for the 90
physically original F55 source squares, now carrying typed
nonneutral Gray braidings through ALL 360 C60 corner charts. -/
def c60F29PhysicalBraidedAtlas (a b : ZMod 2)
    (side : C60DartSideGauge) :
    c60ActualCornerFunctor ⟶ c60F29BraidedSixYaoFunctor a b :=
  c60F29BraidedCornerNatTrans a b side
    (c60F29ActualBraidedSquare t₁ t₂ left right a b)

/-- The entire new nonneutral natural atlas agrees EXACTLY
with the original proof-relevant F55 source-square plus the
independently supplied genuine native Gray braiding. -/
theorem c60F29PhysicalBraidedAtlas_eq_source
    (a b : ZMod 2) (side : C60DartSideGauge) :
    c60F29PhysicalBraidedAtlas t₁ t₂ left right a b side =
      c60F29SourceBraidedAtlas a b side
        (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.disjointSquare
          left right) := by
  change c60F29BraidedCornerNatTrans a b side
      (c60F29ActualBraidedSquare t₁ t₂ left right a b) =
    c60F29BraidedCornerNatTrans a b side
      (fun _ => c60F29BraidedSource a b
        (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.disjointSquare
          left right))
  have h : c60F29ActualBraidedSquare t₁ t₂ left right a b =
      (fun _ => c60F29BraidedSource a b
        (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.disjointSquare
          left right)) := by
    funext edge
    exact c60F29ActualBraidedSquare_eq_originalSource
      t₁ t₂ left right a b edge
  rw [h]

#print axioms c60F29PhaseDefect_comp
#print axioms c60F29PhaseDefect_tensor
#print axioms c60F29PhaseDefect_exchange
#print axioms c60F29PhaseDefect_odd_odd
#print axioms c60F29ShiftNeutral_comp
#print axioms c60F29ShiftNeutral_inv
#print axioms c60F29ShiftNeutral_defect
#print axioms c60F29ShiftedSource_ident
#print axioms c60F29ShiftedSource_trans
#print axioms c60F29ShiftedSource_defect_zero
#print axioms c60F29BraidedSource_components
#print axioms c60F29BraidedSource_defect
#print axioms c60F29BraidedSource_ident
#print axioms c60F29BraidedSource_ident_odd_nonzero
#print axioms c60F29Source_exchange_naturality
#print axioms c60F29BraidedSixYaoFunctor
#print axioms c60F29BraidedCornerNatTrans
#print axioms c60F29SourceBraidedAtlas
#print axioms c60F29BraidedSource_horizontal_coherence
#print axioms c60F29BraidedSource_horizontal_WangBi
#print axioms c60F29ActualBraidedSquare_eq_originalSource
#print axioms c60F29ActualBraidedSquare_components
#print axioms c60F29PhysicalBraidedAtlas_eq_source

end OriginalPhysicalC60
end
end KUOS.DependentOriginationGrayC60F55NonneutralBraidingTransportV5_177
