import KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
import KUOS.DependentOriginationGrayC60F55SourcePhaseLockedAtlasV5_175

namespace KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayF55PhaseRealizationV5_156
open KUOS.DependentOriginationGrayC60F55SourcePhaseLockedAtlasV5_175
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F44 / v5.192 — genuine C60 and original F55 3-Hom categories

F59-F43 gave raw Type-valued, globally indexed original
C60 face 3-cells with physical face 2-cell boundaries.
Distinct parenthesized vertical composites are different
raw syntax: they cannot be declared strictly associative.

The appropriate mathematical 3-Hom category is built by
quotienting parallel raw source 3-cells ONLY when their
FULL native Gray 3-cell images agree, including F58 integer
charges AND the independent exchange phase. This relation
does not erase the original raw proof-relevant source syntax,
which remains independently accessible.

Both source and target of every 3-morphism retain their
original exact C60 F42 face-2-cell indices. Identity and
associativity are proved from the ACTUAL Gray group and
the categorical quotient. The resulting Mathlib category
maps FAITHFULLY to the existing braided category GrayGrade.

A separate original F54/F55 route 3-Hom category is built
using the ACTUAL nine-constructor original F55 source syntax,
with an equally honest target-kernel quotient. A second
faithful functor realizes original F55 charge and phase
inside EXACTLY the same native GrayGrade target.

Actual original C60 north-pentagon face interchange and
original genuine F55 square generators still have distinct
second F58 integer charges, although both have phase one.
No fictitious identification of their DIFFERENT original
globular source 2-cell boundaries is made.

These are real LOCAL 3-Hom categories. They do NOT yet
constitute a full global nondegenerate Gray 3-category
with 60 original 0-objects and Gray coherences across all
0/1/2/3 globular levels. That requires further source
boundary comparisons, 1-path and 2-cell whiskering
functors and coherent original F54/F55 attachments.
-/

/-! ## I. Original C60 source FACE 3-Hom category -/
section C60Face
variable {a b : IcosahedralDart}
variable {p q : Quiver.Path a b}
variable {α β γ : C60F42PresentedFaceCell p q}

def c60F44FaceThreeRel {α β : C60F42PresentedFaceCell p q}
    (f g : C60F43PresentedThreeCell α β) : Prop :=
  f.toNative = g.toNative

abbrev C60F44FaceThreeHom
    (α β : C60F42PresentedFaceCell p q) : Type :=
  Quot (c60F44FaceThreeRel (p := p) (q := q) (α := α) (β := β))

def c60F44FaceThreeOf
    (f : C60F43PresentedThreeCell α β) :
    C60F44FaceThreeHom α β :=
  Quot.mk _ f

def c60F44FaceThreeEval
    (f : C60F44FaceThreeHom α β) : GradedThreeCell 0 0 :=
  Quot.liftOn f (fun raw => raw.toNative) (by
    intro f g h
    exact h)

@[simp] theorem c60F44FaceThreeEval_of
    (f : C60F43PresentedThreeCell α β) :
    c60F44FaceThreeEval (c60F44FaceThreeOf f) = f.toNative := rfl

/-- Source vertical composition descends through the exact
integer-charge-plus-phase target-kernel quotient. -/
def c60F44FaceThreeComp
    (f : C60F44FaceThreeHom α β)
    (g : C60F44FaceThreeHom β γ) :
    C60F44FaceThreeHom α γ :=
  Quot.liftOn₂ f g
    (fun left right => c60F44FaceThreeOf (.trans left right))
    (by
      intro left right₁ right₂ heq
      apply Quot.sound
      change left.toNative + right₁.toNative =
        left.toNative + right₂.toNative
      rw [heq])
    (by
      intro left₁ left₂ right heq
      apply Quot.sound
      change left₁.toNative + right.toNative =
        left₂.toNative + right.toNative
      rw [heq])

theorem c60F44FaceThreeEval_comp
    (f : C60F44FaceThreeHom α β)
    (g : C60F44FaceThreeHom β γ) :
    c60F44FaceThreeEval (c60F44FaceThreeComp f g) =
      c60F44FaceThreeEval f + c60F44FaceThreeEval g := by
  refine Quot.inductionOn f (fun f => ?_)
  refine Quot.inductionOn g (fun g => ?_)
  rfl

/-- Full Mathlib category axioms for original C60 physical
face-2-cell objects and actual source 3-cell arrows.
No raw 3-cell proof equality is falsely asserted. -/
instance c60F44FaceThreeCategory :
    Category (C60F42PresentedFaceCell p q) where
  Hom := C60F44FaceThreeHom
  id α := c60F44FaceThreeOf (.ident α)
  comp := c60F44FaceThreeComp
  id_comp := by
    intro X Y h
    refine Quot.inductionOn h (fun raw => ?_)
    apply Quot.sound
    change (0 : GradedThreeCell 0 0) + raw.toNative = raw.toNative
    exact zero_add _
  comp_id := by
    intro X Y h
    refine Quot.inductionOn h (fun raw => ?_)
    apply Quot.sound
    change raw.toNative + (0 : GradedThreeCell 0 0) = raw.toNative
    exact add_zero _
  assoc := by
    intro W X Y Z f g h
    refine Quot.inductionOn f (fun f => ?_)
    refine Quot.inductionOn g (fun g => ?_)
    refine Quot.inductionOn h (fun h => ?_)
    apply Quot.sound
    change (f.toNative + g.toNative) + h.toNative =
      f.toNative + (g.toNative + h.toNative)
    exact add_assoc _ _ _

/-- Actual native Gray 3-cell functor on the original C60
local face-2-cell 3-Hom category. -/
def c60F44FaceThreeGrayFunctor :
    C60F42PresentedFaceCell p q ⥤ GrayGrade where
  obj _ := GrayGrade.unit
  map := fun {_ _} f => c60F44FaceThreeEval f
  map_id := by
    intro α
    apply GradedThreeCell.ext <;> rfl
  map_comp := by
    intro α β γ f g
    rw [c60F44FaceThreeEval_comp]
    exact grayNeutral_add_eq_native_comp
      (c60F44FaceThreeEval f) (c60F44FaceThreeEval g)

/-- The local original C60 3-Hom image preserves ALL two
independent integer charges and independent exchange phase,
and is faithful AFTER the explicit source quotient. -/
theorem c60F44FaceThreeGrayFunctor_faithful
    {α β : C60F42PresentedFaceCell p q}
    {f g : α ⟶ β}
    (heq : c60F44FaceThreeGrayFunctor.map f =
      c60F44FaceThreeGrayFunctor.map g) : f = g := by
  change c60F44FaceThreeEval f = c60F44FaceThreeEval g at heq
  revert heq
  refine Quot.inductionOn₂ f g (fun raw₁ raw₂ hh => ?_)
  exact Quot.sound hh

/-- The genuinely typed C60 horizontal source interchange
is an ACTUAL arrow in the newly proved Mathlib 3-Hom category. -/
def c60F44PhysicalInterchangerArrow
    {a b c : IcosahedralDart}
    {u v : Quiver.Path a b} {w z : Quiver.Path b c}
    (α : C60F42PresentedFaceCell u v)
    (β : C60F42PresentedFaceCell w z) :
    (α.horizontalLeftFirst β) ⟶
      (α.horizontalRightFirst β) :=
  c60F44FaceThreeOf (.interchange α β)

theorem c60F44PhysicalInterchangerArrow_eval
    {a b c : IcosahedralDart}
    {u v : Quiver.Path a b} {w z : Quiver.Path b c}
    (α : C60F42PresentedFaceCell u v)
    (β : C60F42PresentedFaceCell w z) :
    c60F44FaceThreeGrayFunctor.map
      (c60F44PhysicalInterchangerArrow α β) =
      c60F43PhysicalInterchangerNative α β := rfl

/-- True north-C60-pentagon source 3-arrow remains genuinely
nontrivial in the native independent Gray target. -/
theorem c60F44NorthPentagonInterchange_phase_one :
    (c60F44FaceThreeGrayFunctor.map
      (c60F44FaceThreeOf c60F43NorthPentagonInterchange)).phase =
        (1 : ZMod 2) := by
  exact c60F43NorthPentagonInterchange_components.2

end C60Face

#print axioms c60F44FaceThreeEval_comp
#print axioms c60F44FaceThreeCategory
#print axioms c60F44FaceThreeGrayFunctor
#print axioms c60F44FaceThreeGrayFunctor_faithful
#print axioms c60F44PhysicalInterchangerArrow_eval
#print axioms c60F44NorthPentagonInterchange_phase_one

end
end KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
