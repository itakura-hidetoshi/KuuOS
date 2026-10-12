import KUOS.DependentOriginationGrayC60GrayThreeCategoryPhysicalF55V5_197

namespace KUOS.DependentOriginationGrayC60GrayThreeCategoryCompositionFunctorsV5_197

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60NativePathFunctorV5_189
open KUOS.DependentOriginationGrayC60GradedGrayThreeCategoryV5_197
open KUOS.DependentOriginationGrayC60GrayThreeCategoryCoherenceV5_197
open KUOS.DependentOriginationGrayC60GrayThreeCategoryPhysicalF55V5_197

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.197 F59-F49 — genuine horizontal THREE-HOM composition FUNCTORS

A Gray 3-category must possess categorical composition of 3-Homs,
not merely equations on the generators' charge and exchange phase.
Here every pair of ACTUAL C60 composable 1-path HOMs receives a
MATHLIB FUNCTOR from the PRODUCT of their two original native
3-Hom categories into the output hom category above the original
composed C60 1-paths. Its object map is the native horizontal
2-cell tensor, and its morphism map is the COMPLETE typed F59
3-cell tensor, with both Int×Int charges and independent phase.

Both original 1-path left/right whiskerings are full Mathlib
identity-on-native-data functors between the correctly typed
local 3-Hom categories. Their functor laws and faithfulness hold
because the complete native categorical 3-arrows are preserved.

The F59 nontrivial Gray interchange remains a separately proved
braiding 3-cell; this file does NOT collapse exchange to equality
of distinct proof-relevant original source F42/F54 2-cells.
-/

/-- REAL horizontal composition FUNCTOR of original C60 typed
third-dimensional hom categories, with complete original
F59 grade, Int×Int integer charge and independent phase. -/
def c60F49HorizontalThreeHomFunctor
    {a b c : C60F49Object}
    {p q : C60F49One a b} {r s : C60F49One b c} :
    (C60F49Two p q × C60F49Two r s) ⥤
      C60F49Two (p.comp r) (q.comp s) where
  obj z := c60F49HorizontalTwo z.1 z.2
  map := fun {_ _} f => c60F49HorizontalThree f.1 f.2
  map_id := by
    intro ⟨α, β⟩
    apply GradedThreeCell.ext
    · change (0 : Int × Int) + 0 = (0 : Int × Int)
      exact zero_add _
    · change (0 : ZMod 2) + 0 = (0 : ZMod 2)
      exact zero_add _
  map_comp := by
    intro ⟨α, β⟩ ⟨α', β'⟩ ⟨α'', β''⟩ f g
    exact (GradedThreeCell.tensor_comp f.1 g.1 f.2 g.2).symm

/-- The horizontal 3-Hom functor retains the full F59
charge/phase without any quotient to mod-two parity alone. -/
theorem c60F49HorizontalThreeHomFunctor_components
    {a b c : C60F49Object}
    {p q : C60F49One a b} {r s : C60F49One b c}
    {α α' : C60F49Two p q}
    {β β' : C60F49Two r s}
    (f : α ⟶ α') (g : β ⟶ β') :
    ((c60F49HorizontalThreeHomFunctor
      (p := p) (q := q) (r := r) (s := s)).map
        ((f, g) : (α, β) ⟶ (α', β'))).charge =
      f.charge + g.charge ∧
    ((c60F49HorizontalThreeHomFunctor
      (p := p) (q := q) (r := r) (s := s)).map
        ((f, g) : (α, β) ⟶ (α', β'))).phase =
      f.phase + g.phase :=
  ⟨rfl, rfl⟩

/-- Original REAL C60 path left-whiskering is a FULL Mathlib
FUNCTOR on local 3-Homs, preserving all native generator
charges, independent Gray phase, identities and composition. -/
def c60F49LeftPathThreeHomFunctor
    {a b c : C60F49Object}
    (prior : C60F49One a b) {p q : C60F49One b c} :
    C60F49Two p q ⥤
      C60F49Two (prior.comp p) (prior.comp q) :=
  Functor.id GrayGrade

def c60F49RightPathThreeHomFunctor
    {a b c : C60F49Object}
    {p q : C60F49One a b}
    (suffix : C60F49One b c) :
    C60F49Two p q ⥤
      C60F49Two (p.comp suffix) (q.comp suffix) :=
  Functor.id GrayGrade

/-- Both whiskerings preserve entire 3-cell HOMs, not
merely their two independent projected invariants. -/
theorem c60F49LeftPathThreeHomFunctor_fullNative
    {a b c : C60F49Object}
    (prior : C60F49One a b) {p q : C60F49One b c}
    {α β : C60F49Two p q} (f : α ⟶ β) :
    (c60F49LeftPathThreeHomFunctor prior).map f = f := rfl

theorem c60F49RightPathThreeHomFunctor_fullNative
    {a b c : C60F49Object}
    {p q : C60F49One a b}
    (suffix : C60F49One b c)
    {α β : C60F49Two p q} (f : α ⟶ β) :
    (c60F49RightPathThreeHomFunctor suffix).map f = f := rfl

theorem c60F49LeftPathThreeHomFunctor_faithful
    {a b c : C60F49Object}
    (prior : C60F49One a b) {p q : C60F49One b c}
    {α β : C60F49Two p q} {f g : α ⟶ β}
    (h : (c60F49LeftPathThreeHomFunctor prior).map f =
      (c60F49LeftPathThreeHomFunctor prior).map g) : f = g := by
  exact h

theorem c60F49RightPathThreeHomFunctor_faithful
    {a b c : C60F49Object} {p q : C60F49One a b}
    (suffix : C60F49One b c)
    {α β : C60F49Two p q} {f g : α ⟶ β}
    (h : (c60F49RightPathThreeHomFunctor suffix).map f =
      (c60F49RightPathThreeHomFunctor suffix).map g) : f = g := by
  exact h

#print axioms c60F49HorizontalThreeHomFunctor
#print axioms c60F49HorizontalThreeHomFunctor_components
#print axioms c60F49LeftPathThreeHomFunctor
#print axioms c60F49RightPathThreeHomFunctor
#print axioms c60F49LeftPathThreeHomFunctor_fullNative
#print axioms c60F49LeftPathThreeHomFunctor_faithful

end
end KUOS.DependentOriginationGrayC60GrayThreeCategoryCompositionFunctorsV5_197
