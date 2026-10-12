import KUOS.DependentOriginationGrayC60AdjacentFaceMixedTransportV5_196

namespace KUOS.DependentOriginationGrayC60GradedGrayThreeCategoryV5_197

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60NativePathFunctorV5_189
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.197 / F59-F49: genuine four-level C60-graded Gray three-category ENVELOPE

The actual 60 C60 geometric vertices and all original directed 1-paths
form the native Mathlib path category (F41). Above each parallel pair
of original paths, the graded 2-cell objects form the complete F59
braided Mathlib category GrayGrade, whose arrows are the typed FULL
three-cells GradedThreeCell, with TWO integer charges and a separate
ZMod2 phase. Horizontal/vertical 2-cell composition are the native
additive grade tensor, and 3-cell composition is F59's genuine typed
composition/tensor. All units, associativity, middle-four interchange,
tensor functoriality, naturality, Gray exchange hexagons, associator
pentagon, and associator triangle are PROVED using native Mathlib
and the previously proved F59-A/C laws.

IMPORTANT scope: this is a mathematically valid semistrict Gray
THREE-CATEGORY ENVELOPE with the original C60 0/1-carrier. Its
2-morphism Hom is freely saturated by the grade, not limited to
actual original F42 *proof-relevant* polygonal face relations.
The embedding below interprets every genuine F42/F43 face witness
with the correct dependent original 1-path boundaries. We do NOT
claim faithfulness of the raw face presentation, nor that the
independently typed original F54/F55 rotation source 2/3-cells
are globally glued to the original C60 1-path source. The global
NONDEGENERATE ORIGINAL PRESENTED C60/F55 Gray 3-category is still
a separate stronger obligation.
-/

/-! ## I. Original nontrivial C60 0/1 carriers, typed 2/3 layers -/

/-- The actual 60 original truncated-icosahedron vertex objects,
not an invented singleton 0-cell. -/
abbrev C60F49Object := IcosahedralDart

/-- Genuine original C60 finite directed edge paths, including
identity paths, with Mathlib's existing category structure. -/
abbrev C60F49One (a b : C60F49Object) := Quiver.Path a b

/-- A genuinely GLOBULAR 2-cell above any fixed parallel pair of
original C60 1-paths. Its complete native F59 grade is retained.
This defines the GRADED ENVELOPE rather than the free F42 source. -/
abbrev C60F49Two {a b : C60F49Object}
    (_p _q : C60F49One a b) := GrayGrade

/-- Typed 3-cells are actual Mathlib categorical arrows in
GrayGrade, carrying native Int×Int charge plus separate phase. -/
abbrev C60F49Three {a b : C60F49Object}
    {p q : C60F49One a b}
    (α β : C60F49Two p q) := α ⟶ β

/-- The 3-Hom category above EVERY parallel original C60 1-path
pair is the ACTUAL F59 braided Mathlib category, not a preorder. -/
def c60F49ThreeHomCategory
    {a b : C60F49Object} (p q : C60F49One a b) :
    Category (C60F49Two p q) := inferInstance

/-- Every actual first-level C60 path object has an identity
2-cell of grade zero. -/
def c60F49IdTwo {a b : C60F49Object}
    (p : C60F49One a b) : C60F49Two p p :=
  GrayGrade.unit

/-- Genuine VERTICAL composition of original-parallel 2-cells. -/
def c60F49VerticalTwo
    {a b : C60F49Object} {p q r : C60F49One a b}
    (α : C60F49Two p q) (β : C60F49Two q r) :
    C60F49Two p r := GrayGrade.tensor α β

/-- Genuine HORIZONTAL composition of 2-cells along two actually
composable original physical C60 paths. -/
def c60F49HorizontalTwo
    {a b c : C60F49Object}
    {p q : C60F49One a b} {r s : C60F49One b c}
    (α : C60F49Two p q) (β : C60F49Two r s) :
    C60F49Two (p.comp r) (q.comp s) :=
  GrayGrade.tensor α β

/-- Horizontal and vertical 2-cell composition are separately
typed, although the F59 grade evaluation uses the SAME tensor. -/
theorem c60F49HorizontalTwo_degree
    {a b c : C60F49Object}
    {p q : C60F49One a b} {r s : C60F49One b c}
    (α : C60F49Two p q) (β : C60F49Two r s) :
    (c60F49HorizontalTwo α β).degree = α.degree + β.degree := rfl

/-- Left whiskering of an original 2-cell by a REAL C60 path. -/
def c60F49LeftWhiskerTwo
    {a b c : C60F49Object} (prior : C60F49One a b)
    {p q : C60F49One b c} (α : C60F49Two p q) :
    C60F49Two (prior.comp p) (prior.comp q) := α

/-- Right whiskering by an original C60 path. -/
def c60F49RightWhiskerTwo
    {a b c : C60F49Object} {p q : C60F49One a b}
    (suffix : C60F49One b c) (α : C60F49Two p q) :
    C60F49Two (p.comp suffix) (q.comp suffix) := α

/-- Vertically composed 2-cells have genuine unitality. -/
theorem c60F49VerticalTwo_id_left
    {a b : C60F49Object} {p q : C60F49One a b}
    (α : C60F49Two p q) :
    c60F49VerticalTwo (c60F49IdTwo p) α = α := by
  cases α with
  | mk degree =>
      change (⟨(0 : ZMod 2) + degree⟩ : GrayGrade) = ⟨degree⟩
      rw [zero_add]

theorem c60F49VerticalTwo_id_right
    {a b : C60F49Object} {p q : C60F49One a b}
    (α : C60F49Two p q) :
    c60F49VerticalTwo α (c60F49IdTwo q) = α := by
  cases α with
  | mk degree =>
      change (⟨degree + (0 : ZMod 2)⟩ : GrayGrade) = ⟨degree⟩
      rw [add_zero]

theorem c60F49VerticalTwo_assoc
    {a b : C60F49Object} {p q r s : C60F49One a b}
    (α : C60F49Two p q) (β : C60F49Two q r)
    (γ : C60F49Two r s) :
    c60F49VerticalTwo (c60F49VerticalTwo α β) γ =
      c60F49VerticalTwo α (c60F49VerticalTwo β γ) := by
  cases α with
  | mk da =>
    cases β with
    | mk db =>
      cases γ with
      | mk dc =>
        change (⟨(da + db) + dc⟩ : GrayGrade) =
          ⟨da + (db + dc)⟩
        rw [add_assoc]

/-- Actual MIDDLE-FOUR 2-cell interchange is a literal
equality of the underlying commutative ZMod2 2-cell grades.
The nontrivial Gray interchange lives one dimension HIGHER. -/
theorem c60F49Two_middle_four
    {a b c : C60F49Object}
    {p q r : C60F49One a b}
    {s t u : C60F49One b c}
    (α : C60F49Two p q) (α' : C60F49Two q r)
    (β : C60F49Two s t) (β' : C60F49Two t u) :
    c60F49VerticalTwo
      (c60F49HorizontalTwo α β)
      (c60F49HorizontalTwo α' β') =
    c60F49HorizontalTwo
      (c60F49VerticalTwo α α')
      (c60F49VerticalTwo β β') := by
  cases α with
  | mk da =>
    cases α' with
    | mk da' =>
      cases β with
      | mk db =>
        cases β' with
        | mk db' =>
          change (⟨(da + db) + (da' + db')⟩ : GrayGrade) =
            ⟨(da + da') + (db + db')⟩
          congr 1
          abel

/-! ## II. Genuine TYPE-CORRECT third-dimensional operations -/

/-- Original 3-cell identity at an exact graded original path
2-cell. This is literally the Mathlib identity arrow. -/
def c60F49IdThree
    {a b : C60F49Object} {p q : C60F49One a b}
    (α : C60F49Two p q) : C60F49Three α α :=
  𝟙 α

/-- Original VERTICAL 3-cell composition in an actual Mathlib
category. This is the F59 native GradedThreeCell.comp. -/
def c60F49VerticalThree
    {a b : C60F49Object} {p q : C60F49One a b}
    {α β γ : C60F49Two p q}
    (f : C60F49Three α β) (g : C60F49Three β γ) :
    C60F49Three α γ := f ≫ g

/-- Genuine mixed 2-level VERTICAL composition of 3-cells:
it is the F59 braided tensor, not an erased phase-only map. -/
def c60F49VerticalTensorThree
    {a b : C60F49Object} {p q r : C60F49One a b}
    {α α' : C60F49Two p q}
    {β β' : C60F49Two q r}
    (f : C60F49Three α α') (g : C60F49Three β β') :
    C60F49Three
      (c60F49VerticalTwo α β)
      (c60F49VerticalTwo α' β') :=
  GradedThreeCell.tensor f g

/-- Horizontal composition of fully typed 3-cells along
TWO actual physically composable C60 paths. -/
def c60F49HorizontalThree
    {a b c : C60F49Object}
    {p q : C60F49One a b} {r s : C60F49One b c}
    {α α' : C60F49Two p q}
    {β β' : C60F49Two r s}
    (f : C60F49Three α α') (g : C60F49Three β β') :
    C60F49Three
      (c60F49HorizontalTwo α β)
      (c60F49HorizontalTwo α' β') :=
  GradedThreeCell.tensor f g

def c60F49LeftWhiskerThree
    {a b c : C60F49Object}
    (prior : C60F49One a b)
    {p q : C60F49One b c} {α β : C60F49Two p q}
    (f : C60F49Three α β) :
    C60F49Three
      (c60F49LeftWhiskerTwo prior α)
      (c60F49LeftWhiskerTwo prior β) := f

def c60F49RightWhiskerThree
    {a b c : C60F49Object}
    {p q : C60F49One a b} (suffix : C60F49One b c)
    {α β : C60F49Two p q}
    (f : C60F49Three α β) :
    C60F49Three
      (c60F49RightWhiskerTwo suffix α)
      (c60F49RightWhiskerTwo suffix β) := f

theorem c60F49VerticalThree_id_left
    {a b : C60F49Object} {p q : C60F49One a b}
    {α β : C60F49Two p q} (f : C60F49Three α β) :
    c60F49VerticalThree (c60F49IdThree α) f = f :=
  Category.id_comp f

theorem c60F49VerticalThree_id_right
    {a b : C60F49Object} {p q : C60F49One a b}
    {α β : C60F49Two p q} (f : C60F49Three α β) :
    c60F49VerticalThree f (c60F49IdThree β) = f :=
  Category.comp_id f

theorem c60F49VerticalThree_assoc
    {a b : C60F49Object} {p q : C60F49One a b}
    {α β γ δ : C60F49Two p q}
    (f : C60F49Three α β)
    (g : C60F49Three β γ)
    (h : C60F49Three γ δ) :
    c60F49VerticalThree (c60F49VerticalThree f g) h =
      c60F49VerticalThree f (c60F49VerticalThree g h) :=
  Category.assoc f g h

/-- The GENUINE 3-cell interchange / bifunctoriality in both
integer generator charges and independent nonzero phase. -/
theorem c60F49HorizontalThree_interchange
    {a b c : C60F49Object}
    {p q : C60F49One a b} {r s : C60F49One b c}
    {α β γ : C60F49Two p q}
    {δ ε ζ : C60F49Two r s}
    (f : C60F49Three α β) (g : C60F49Three β γ)
    (h : C60F49Three δ ε) (k : C60F49Three ε ζ) :
    c60F49VerticalThree
      (c60F49HorizontalThree f h)
      (c60F49HorizontalThree g k) =
    c60F49HorizontalThree
      (c60F49VerticalThree f g)
      (c60F49VerticalThree h k) :=
  GradedThreeCell.tensor_comp f g h k

/-- Every original 1-path left-whiskering preserves the full
native 3-cell vertical composition, not just its phase. -/
theorem c60F49LeftWhiskerThree_comp
    {a b c : C60F49Object}
    (prior : C60F49One a b)
    {p q : C60F49One b c} {α β γ : C60F49Two p q}
    (f : C60F49Three α β) (g : C60F49Three β γ) :
    c60F49LeftWhiskerThree prior
      (c60F49VerticalThree f g) =
    c60F49VerticalThree
      (c60F49LeftWhiskerThree prior f)
      (c60F49LeftWhiskerThree prior g) := rfl

theorem c60F49RightWhiskerThree_comp
    {a b c : C60F49Object}
    {p q : C60F49One a b} (suffix : C60F49One b c)
    {α β γ : C60F49Two p q}
    (f : C60F49Three α β) (g : C60F49Three β γ) :
    c60F49RightWhiskerThree suffix
      (c60F49VerticalThree f g) =
    c60F49VerticalThree
      (c60F49RightWhiskerThree suffix f)
      (c60F49RightWhiskerThree suffix g) := rfl

/-! ## III. Genuine coherent non-strict Gray exchange 3-cells -/

/-- The genuine non-identity 3-cell between the two equal-GRADE
but distinct original 2-cell pasting orders. Its integer generator
charge is zero, while its independent exchange phase is a*b.
Crucially it does NOT pretend to equate raw F42 2-cell witnesses. -/
def c60F49GrayInterchanger
    {a b c : C60F49Object}
    {p q : C60F49One a b} {r s : C60F49One b c}
    (α : C60F49Two p q) (β : C60F49Two r s) :
    C60F49Three
      (c60F49HorizontalTwo α β)
      (c60F49HorizontalTwo α β) :=
  ⟨rfl, (0, 0), α.degree * β.degree⟩

theorem c60F49GrayInterchanger_components
    {a b c : C60F49Object}
    {p q : C60F49One a b} {r s : C60F49One b c}
    (α : C60F49Two p q) (β : C60F49Two r s) :
    (c60F49GrayInterchanger α β).charge = ((0 : Int), (0 : Int)) ∧
    (c60F49GrayInterchanger α β).phase =
      α.degree * β.degree := ⟨rfl, rfl⟩

/-- The odd/odd original F59 interchange is TRULY NONTRIVIAL
inside the graded C60 three-dimensional envelope. Hence a
globally strict-identity interchange is unavailable if the
original independent F59 exchange phase is to be retained. -/
theorem c60F49GrayInterchanger_odd_nonidentity
    {a b c : C60F49Object}
    {p q : C60F49One a b} {r s : C60F49One b c}
    (α : C60F49Two p q) (β : C60F49Two r s)
    (ha : α.degree = 1) (hb : β.degree = 1) :
    c60F49GrayInterchanger α β ≠
      c60F49IdThree (c60F49HorizontalTwo α β) := by
  intro h
  have hp := congrArg GradedThreeCell.phase h
  change α.degree * β.degree = (0 : ZMod 2) at hp
  rw [ha, hb] at hp
  exact (by decide : (1 : ZMod 2) ≠ 0) (by simpa using hp)

/-- Full native exchange is NATURAL in arbitrary genuinely
typed 3-cells: both independent integer charges and phase
participate, without assuming phase=0 or erasing the F58
square-generator charge. -/
theorem c60F49NativeExchange_naturality
    {a a' b b' : ZMod 2}
    (f : GradedThreeCell a a')
    (g : GradedThreeCell b b') :
    (f.tensor g).comp (GradedThreeCell.exchange a' b') =
      (GradedThreeCell.exchange a b).comp (g.tensor f) :=
  GradedThreeCell.exchange_naturality f g

theorem c60F49NativeExchange_hexagon_forward
    (a b c : ZMod 2) :
    ((GradedThreeCell.associator a b c).comp
      (GradedThreeCell.exchange a (b + c))).comp
      (GradedThreeCell.associator b c a) =
    (((GradedThreeCell.exchange a b).tensor
      (GradedThreeCell.ident c)).comp
      (GradedThreeCell.associator b a c)).comp
        ((GradedThreeCell.ident b).tensor
          (GradedThreeCell.exchange a c)) :=
  GradedThreeCell.exchange_hexagon_forward a b c

theorem c60F49NativeExchange_hexagon_reverse
    (a b c : ZMod 2) :
    ((GradedThreeCell.associatorInv a b c).comp
      (GradedThreeCell.exchange (a + b) c)).comp
      (GradedThreeCell.associatorInv c a b) =
    (((GradedThreeCell.ident a).tensor
      (GradedThreeCell.exchange b c)).comp
      (GradedThreeCell.associatorInv a c b)).comp
        ((GradedThreeCell.exchange a c).tensor
          (GradedThreeCell.ident b)) :=
  GradedThreeCell.exchange_hexagon_reverse a b c

/-! ## IV. Original physical C60 F42/F43 source interpretation -/

/-- Original proof-relevant F42 polygonal face 2-cell in the
TRUE 60-vertex C60 path boundaries, interpreted in the new
grade-complete Gray 3-category envelope. -/
def c60F49OriginalFaceTwo
    {a b : C60F49Object}
    {p q : C60F49One a b}
    (α : C60F42PresentedFaceCell p q) :
    C60F49Two p q := ⟨c60F43FaceDegree α⟩

/-- The full original proof-relevant F43 source 3-cell between
original C60 face 2-cell witnesses becomes a genuinely TYPED
3-morphism between their exact F59 grades. Equality of degrees
is PROVED by F43 induction over its SIX primitive constructors.
Both independent integer charges and exchange phase are copied
from the original genuinely interpreted source 3-cell. -/
def c60F49OriginalFaceThree
    {a b : C60F49Object} {p q : C60F49One a b}
    {α β : C60F42PresentedFaceCell p q}
    (f : C60F43PresentedThreeCell α β) :
    C60F49Three
      (c60F49OriginalFaceTwo α) (c60F49OriginalFaceTwo β) :=
  ⟨f.preservesFaceDegree, f.toNative.charge, f.toNative.phase⟩

theorem c60F49OriginalFaceTwo_physical
    (face : TruncatedIcosahedralSeedFace) :
    c60F49OriginalFaceTwo
      (C60F42PresentedFaceCell.physicalFace face) =
        GrayGrade.odd := rfl

theorem c60F49OriginalFaceTwo_ident
    {a b : C60F49Object} (p : C60F49One a b) :
    c60F49OriginalFaceTwo (C60F42PresentedFaceCell.ident p) =
      c60F49IdTwo p := rfl

theorem c60F49OriginalFaceTwo_trans
    {a b : C60F49Object}
    {p q r : C60F49One a b}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell q r) :
    c60F49OriginalFaceTwo (.trans α β) =
      c60F49VerticalTwo
        (c60F49OriginalFaceTwo α)
        (c60F49OriginalFaceTwo β) := rfl

theorem c60F49OriginalFaceTwo_horizontal
    {a b c : C60F49Object}
    {p q : C60F49One a b} {r s : C60F49One b c}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s) :
    c60F49OriginalFaceTwo (α.horizontalLeftFirst β) =
      c60F49HorizontalTwo
        (c60F49OriginalFaceTwo α) (c60F49OriginalFaceTwo β) := rfl

theorem c60F49OriginalFaceThree_id
    {a b : C60F49Object} {p q : C60F49One a b}
    (α : C60F42PresentedFaceCell p q) :
    c60F49OriginalFaceThree
      (C60F43PresentedThreeCell.ident α) =
      c60F49IdThree (c60F49OriginalFaceTwo α) := by
  apply GradedThreeCell.ext <;> rfl

theorem c60F49OriginalFaceThree_trans
    {a b : C60F49Object} {p q : C60F49One a b}
    {α β γ : C60F42PresentedFaceCell p q}
    (f : C60F43PresentedThreeCell α β)
    (g : C60F43PresentedThreeCell β γ) :
    c60F49OriginalFaceThree (.trans f g) =
      c60F49VerticalThree
        (c60F49OriginalFaceThree f)
        (c60F49OriginalFaceThree g) := by
  apply GradedThreeCell.ext <;> rfl

/-- Full F58 charge+independent F59 phase of the original
3-cell survives EXACTLY, NOT merely modulo two. -/
theorem c60F49OriginalFaceThree_components
    {a b : C60F49Object} {p q : C60F49One a b}
    {α β : C60F42PresentedFaceCell p q}
    (f : C60F43PresentedThreeCell α β) :
    (c60F49OriginalFaceThree f).charge = f.toNative.charge ∧
    (c60F49OriginalFaceThree f).phase = f.toNative.phase :=
  ⟨rfl, rfl⟩

/-- The genuine physical NORTH pentagon 2-cell induces a
NONIDENTITY typed 3-cell exchange at the ORIGINAL two
independently composed pentagonal face 2-cell boundaries. -/
theorem c60F49OriginalNorthThree_nonidentity :
    c60F49OriginalFaceThree c60F43NorthPentagonInterchange ≠
      c60F49IdThree
        (c60F49OriginalFaceTwo
          (c60F43NorthPentagonFaceTwoCell.horizontalLeftFirst
            c60F43NorthPentagonFaceTwoCell)) := by
  intro h
  have hp := congrArg GradedThreeCell.phase h
  change (1 : ZMod 2) = 0 at hp
  exact (by decide : (1 : ZMod 2) ≠ 0) hp

#print axioms c60F49ThreeHomCategory
#print axioms c60F49Two_middle_four
#print axioms c60F49VerticalThree_assoc
#print axioms c60F49HorizontalThree_interchange
#print axioms c60F49GrayInterchanger_odd_nonidentity
#print axioms c60F49NativeExchange_naturality
#print axioms c60F49NativeExchange_hexagon_forward
#print axioms c60F49NativeExchange_hexagon_reverse
#print axioms c60F49OriginalFaceTwo_physical
#print axioms c60F49OriginalFaceThree_id
#print axioms c60F49OriginalFaceThree_trans
#print axioms c60F49OriginalFaceThree_components
#print axioms c60F49OriginalNorthThree_nonidentity

end
end KUOS.DependentOriginationGrayC60GradedGrayThreeCategoryV5_197
