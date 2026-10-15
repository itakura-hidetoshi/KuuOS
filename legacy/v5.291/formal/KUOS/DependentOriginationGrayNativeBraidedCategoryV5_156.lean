import KUOS.DependentOriginationGrayF55PhaseRealizationV5_156
import Mathlib.CategoryTheory.Monoidal.Braided.Basic

namespace KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156

open CategoryTheory
open scoped CategoryTheory.MonoidalCategory
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156

set_option autoImplicit false
noncomputable section

/-!
# F59-C / v5.156: native mathlib braided monoidal CATEGORY of Gray 3-cells

F59-A constructed the independently typed graded 3-cells (charge : Int×Int,
exchange phase : ZMod 2) and directly proved their additive vertical/groupoid,
tensor, associator and interchanger coherence. F59-B interpreted every F55
PresentedCell in this same target and proved exact projection to F58 charge.

The *new*, independently defined object type GrayGrade is a ZMod 2-graded
2-cell. Actual morphisms X ⟶ Y are F59-A GradedThreeCell X.degree Y.degree.
We construct:
  1. a genuine Mathlib Category instance (typed vertical composition);
  2. a genuine Mathlib MonoidalCategory instance with tensor on graded
     2-cells and typed 3-cells, including all naturality, pentagon, triangle;
  3. a genuine Mathlib BraidedCategory instance: braiding is F59-A's
     NONIDENTITY odd/odd interchanger, satisfying naturality and both hexagons.

This is a concrete braided monoidal *groupoid*, the monoidal category of
2- and 3-cell data underlying a doubly-degenerate Gray-category model.
It is not the entire global tricategory with arbitrary zero-cell and one-cell data,
nor an equivalence of KuuOS and any arbitrary ambient Gray category.
The original F58 integer charges and the extra F59 exchange phase remain
independent, and no old Stage-II omega class is identified with either.
-/

/-- New object carrier: a genuine grade, intentionally NOT a global
Category instance on the unrelated underlying ring ZMod 2 itself. -/
structure GrayGrade where
  degree : ZMod 2
  deriving DecidableEq

/-- Tensor on graded 2-cell objects. -/
def GrayGrade.tensor (X Y : GrayGrade) : GrayGrade :=
  ⟨X.degree + Y.degree⟩

/-- Unit graded 2-cell object. -/
def GrayGrade.unit : GrayGrade := ⟨0⟩

/-- Genuine mathlib category: its arrows are actual F59-A typed 3-cells,
not proof-only F44 observations or raw freely presented F55 syntax. -/
instance : Category GrayGrade where
  Hom X Y := GradedThreeCell X.degree Y.degree
  id X := GradedThreeCell.ident X.degree
  comp f g := GradedThreeCell.comp f g
  id_comp := by
    intro X Y f
    exact GradedThreeCell.ident_comp f
  comp_id := by
    intro X Y f
    exact GradedThreeCell.comp_ident f
  assoc := by
    intro W X Y Z f g h
    exact GradedThreeCell.comp_assoc f g h

/-- A native associator Iso with explicit F59-A 3-cell hom and inverse. -/
def GrayGrade.associatorIso (X Y Z : GrayGrade) :
    GrayGrade.tensor (GrayGrade.tensor X Y) Z ≅
      GrayGrade.tensor X (GrayGrade.tensor Y Z) where
  hom := GradedThreeCell.associator X.degree Y.degree Z.degree
  inv := GradedThreeCell.associatorInv X.degree Y.degree Z.degree
  hom_inv_id := GradedThreeCell.comp_inv
    (GradedThreeCell.associator X.degree Y.degree Z.degree)
  inv_hom_id := GradedThreeCell.inv_comp
    (GradedThreeCell.associator X.degree Y.degree Z.degree)

/-- Left unitor as a real invertible morphism in the new category. -/
def GrayGrade.leftUnitorIso (X : GrayGrade) :
    GrayGrade.tensor GrayGrade.unit X ≅ X where
  hom := GradedThreeCell.leftUnitor X.degree
  inv := (GradedThreeCell.leftUnitor X.degree).inv
  hom_inv_id := GradedThreeCell.comp_inv (GradedThreeCell.leftUnitor X.degree)
  inv_hom_id := GradedThreeCell.inv_comp (GradedThreeCell.leftUnitor X.degree)

/-- Right unitor as a real invertible morphism in the new category. -/
def GrayGrade.rightUnitorIso (X : GrayGrade) :
    GrayGrade.tensor X GrayGrade.unit ≅ X where
  hom := GradedThreeCell.rightUnitor X.degree
  inv := (GradedThreeCell.rightUnitor X.degree).inv
  hom_inv_id := GradedThreeCell.comp_inv (GradedThreeCell.rightUnitor X.degree)
  inv_hom_id := GradedThreeCell.inv_comp (GradedThreeCell.rightUnitor X.degree)

/-- Explicit native tensor and whiskering operations. -/
instance : MonoidalCategoryStruct GrayGrade where
  tensorObj := GrayGrade.tensor
  whiskerLeft := by
    intro X Y Z f
    exact (GradedThreeCell.ident X.degree).tensor f
  whiskerRight := by
    intro X Y f Z
    exact f.tensor (GradedThreeCell.ident Z.degree)
  tensorHom := by
    intro X Y Z W f g
    exact f.tensor g
  tensorUnit := GrayGrade.unit
  associator := GrayGrade.associatorIso
  leftUnitor := GrayGrade.leftUnitorIso
  rightUnitor := GrayGrade.rightUnitorIso

/-- Real monoidal class: all coherences are Lean fields proved from
F59-A's exact typed 3-cell composition and tensor laws. -/
instance : MonoidalCategory GrayGrade :=
  MonoidalCategory.ofTensorHom
    (id_tensorHom_id := by
      intro X Y
      apply GradedThreeCell.ext
      · change (0 : Int × Int) + 0 = (0 : Int × Int)
        exact zero_add _
      · change (0 : ZMod 2) + 0 = (0 : ZMod 2)
        exact zero_add _)
    (id_tensorHom := by
      intro X Y Z f
      rfl)
    (tensorHom_id := by
      intro X Y f Z
      rfl)
    (tensorHom_comp_tensorHom := by
      intro X Y Z U V W f g h k
      exact GradedThreeCell.tensor_comp f h g k)
    (associator_naturality := by
      intro X₁ X₂ X₃ Y₁ Y₂ Y₃ f g h
      apply GradedThreeCell.ext
      · change ((f.charge + g.charge) + h.charge) + (0 : Int × Int) =
          (0 : Int × Int) + (f.charge + (g.charge + h.charge))
        abel
      · change ((f.phase + g.phase) + h.phase) + (0 : ZMod 2) =
          (0 : ZMod 2) + (f.phase + (g.phase + h.phase))
        abel)
    (leftUnitor_naturality := by
      intro X Y f
      apply GradedThreeCell.ext
      · change ((0 : Int × Int) + f.charge) + 0 =
          (0 : Int × Int) + f.charge
        abel
      · change ((0 : ZMod 2) + f.phase) + 0 =
          (0 : ZMod 2) + f.phase
        abel)
    (rightUnitor_naturality := by
      intro X Y f
      apply GradedThreeCell.ext
      · change (f.charge + (0 : Int × Int)) + 0 =
          (0 : Int × Int) + f.charge
        abel
      · change (f.phase + (0 : ZMod 2)) + 0 =
          (0 : ZMod 2) + f.phase
        abel)
    (pentagon := by
      intro W X Y Z
      exact GradedThreeCell.associator_pentagon
        W.degree X.degree Y.degree Z.degree)
    (triangle := by
      intro X Y
      exact GradedThreeCell.associator_triangle X.degree Y.degree)

/-- Exact degree of the native monoidal tensor, with NO extra
identification of a geometric C60 face with a 2-cell. -/
@[simp] theorem GrayGrade.native_tensor_degree (X Y : GrayGrade) :
    (X ⊗ Y).degree = X.degree + Y.degree := rfl

/-- The genuine F59-A odd/odd exchange is the HOM component of a
native mathlib braiding isomorphism; the inverse is its typed inverse. -/
def GrayGrade.braidingIso (X Y : GrayGrade) :
    GrayGrade.tensor X Y ≅ GrayGrade.tensor Y X where
  hom := GradedThreeCell.exchange X.degree Y.degree
  inv := (GradedThreeCell.exchange X.degree Y.degree).inv
  hom_inv_id := GradedThreeCell.comp_inv
    (GradedThreeCell.exchange X.degree Y.degree)
  inv_hom_id := GradedThreeCell.inv_comp
    (GradedThreeCell.exchange X.degree Y.degree)

/-- Full Mathlib braided monoidal CATEGORY, with all four substantive
braiding naturality and hexagon fields supplied by the REAL F59-A
nontrivial typed interchanger theorems. -/
instance : BraidedCategory GrayGrade where
  braiding := GrayGrade.braidingIso
  braiding_naturality_right := by
    intro X Y Z f
    exact GradedThreeCell.exchange_naturality
      (GradedThreeCell.ident X.degree) f
  braiding_naturality_left := by
    intro X Y f Z
    exact GradedThreeCell.exchange_naturality
      f (GradedThreeCell.ident Z.degree)
  hexagon_forward := by
    intro X Y Z
    apply GradedThreeCell.ext
    · change (0 : Int × Int) + 0 + 0 =
        ((0 : Int × Int) + 0) + 0 + ((0 : Int × Int) + 0)
      abel
    · dsimp [CategoryStruct.comp,
        MonoidalCategoryStruct.whiskerLeft,
        MonoidalCategoryStruct.whiskerRight,
        MonoidalCategoryStruct.associator,
        MonoidalCategoryStruct.tensorObj,
        GrayGrade.braidingIso, GrayGrade.associatorIso,
        GrayGrade.tensor, GradedThreeCell.comp,
        GradedThreeCell.tensor, GradedThreeCell.exchange,
        GradedThreeCell.associator, GradedThreeCell.ident]
      ring
  hexagon_reverse := by
    intro X Y Z
    apply GradedThreeCell.ext
    · change (0 : Int × Int) + 0 + 0 =
        ((0 : Int × Int) + 0) + 0 + ((0 : Int × Int) + 0)
      abel
    · dsimp [CategoryStruct.comp,
        MonoidalCategoryStruct.whiskerLeft,
        MonoidalCategoryStruct.whiskerRight,
        MonoidalCategoryStruct.associator,
        MonoidalCategoryStruct.tensorObj,
        GrayGrade.braidingIso, GrayGrade.associatorIso,
        GrayGrade.tensor, GradedThreeCell.comp,
        GradedThreeCell.tensor, GradedThreeCell.exchange,
        GradedThreeCell.associatorInv, GradedThreeCell.associator,
        GradedThreeCell.inv, GradedThreeCell.ident]
      ring

/-- The odd graded 2-cell object whose self-exchange is a nontrivial
native 3-morphism even though its F58 integer charge vanishes. -/
def GrayGrade.odd : GrayGrade := ⟨1⟩

/-- The native braiding cannot be the identity 3-morphism at odd/odd. -/
theorem GrayGrade.native_braiding_odd_nonidentity :
    (BraidedCategory.braiding GrayGrade.odd GrayGrade.odd).hom ≠
      (𝟙 (GrayGrade.tensor GrayGrade.odd GrayGrade.odd)) := by
  exact GradedThreeCell.exchange_odd_odd_ne_ident

/-- Projection of the NATIVE braiding into the original F58 higher
integer charge loses the nonzero Gray exchange phase. -/
theorem GrayGrade.native_odd_braiding_charge_zero :
    ((BraidedCategory.braiding GrayGrade.odd GrayGrade.odd).hom :
      GrayGrade.tensor GrayGrade.odd GrayGrade.odd ⟶
        GrayGrade.tensor GrayGrade.odd GrayGrade.odd).toHigherCharge =
      (0 : Int × Int) := by
  exact GradedThreeCell.exchange_charge_zero 1 1

#print axioms GrayGrade
#print axioms instCategoryGrayGrade
#print axioms GrayGrade.associatorIso
#print axioms GrayGrade.leftUnitorIso
#print axioms GrayGrade.rightUnitorIso
#print axioms instMonoidalCategoryStructGrayGrade
#print axioms instMonoidalCategoryGrayGrade
#print axioms GrayGrade.native_tensor_degree
#print axioms GrayGrade.braidingIso
#print axioms instBraidedCategoryGrayGrade
#print axioms GrayGrade.native_braiding_odd_nonidentity
#print axioms GrayGrade.native_odd_braiding_charge_zero

end
end KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
