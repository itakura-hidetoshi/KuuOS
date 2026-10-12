import KUOS.DependentOriginationGrayC60OriginalFaceAssociatorThreeHomV5_200

namespace KUOS.DependentOriginationGrayC60OriginalFaceAssociatorNaturalityV5_200

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalPresentationV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalThreeHomV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalCompositionV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceAssociatorPresentationV5_200
open KUOS.DependentOriginationGrayC60OriginalFaceAssociatorThreeHomV5_200

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.200 / F59-F52-C: original F42 associator and units, naturality

All identities are equalities of GENUINELY PARALLEL source 3-arrows
in the full-native kernel quotient, not equalities of original
F42 2-cell witnesses and not assertions of raw syntax equality.
The source associator and unitors were expressly adjoined by F52;
F43 interchanger remains independently inherited and nontrivial.
-/

/-- Typed right and left contextual horizontal 3-arrow
composition over the original physical C60 path boundaries. -/
def c60F52HorizontalMap
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {X X' : C60F52OriginalTwo p q}
    {Y Y' : C60F52OriginalTwo r s}
    (f : X ⟶ X') (g : Y ⟶ Y') :
    c60F52OriginalTwoHorizontal X Y ⟶
      c60F52OriginalTwoHorizontal X' Y' :=
  Quot.liftOn₂ f g
    (fun rf rg => c60F52Of (.horizontal rf rg))
    (by
      intro rf rg₁ rg₂ hh
      apply Quot.sound
      change rf.toNative + rg₁.toNative =
        rf.toNative + rg₂.toNative
      rw [hh])
    (by
      intro rf₁ rf₂ rg hh
      apply Quot.sound
      change rf₁.toNative + rg.toNative =
        rf₂.toNative + rg.toNative
      rw [hh])

theorem c60F52HorizontalMap_eval
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {X X' : C60F52OriginalTwo p q}
    {Y Y' : C60F52OriginalTwo r s}
    (f : X ⟶ X') (g : Y ⟶ Y') :
    c60F52Eval (c60F52HorizontalMap f g) =
      c60F52Eval f + c60F52Eval g := by
  refine Quot.inductionOn f (fun rf => ?_)
  refine Quot.inductionOn g (fun rg => ?_)
  rfl

def c60F52HorizontalThreeHomFunctor
    {a b c : IcosahedralDart}
    (p q : Quiver.Path a b) (r s : Quiver.Path b c) :
    (C60F52OriginalTwo p q × C60F52OriginalTwo r s) ⥤
      C60F52OriginalTwo (p.comp r) (q.comp s) where
  obj z := c60F52OriginalTwoHorizontal z.1 z.2
  map := fun {_ _} f => c60F52HorizontalMap f.1 f.2
  map_id := by
    intro ⟨X, Y⟩
    apply Quot.sound
    change (0 : GradedThreeCell 0 0) + 0 = 0
    exact add_zero _
  map_comp := by
    intro ⟨X, Y⟩ ⟨X', Y'⟩ ⟨X'', Y''⟩ f g
    obtain ⟨f₁, f₂⟩ := f
    obtain ⟨g₁, g₂⟩ := g
    refine Quot.inductionOn f₁ (fun rf₁ => ?_)
    refine Quot.inductionOn f₂ (fun rf₂ => ?_)
    refine Quot.inductionOn g₁ (fun rg₁ => ?_)
    refine Quot.inductionOn g₂ (fun rg₂ => ?_)
    apply Quot.sound
    change (rf₁.toNative + rg₁.toNative) +
        (rf₂.toNative + rg₂.toNative) =
      (rf₁.toNative + rf₂.toNative) +
        (rg₁.toNative + rg₂.toNative)
    abel

/-- Genuine dependent reindexing of BOTH source and target
original 2-cell proof witnesses and their entire F52 3-arrow,
without collapsing any witnesses or equality of source terms. -/
def c60F52ReindexMap
    {a b : IcosahedralDart}
    {p q p' q' : Quiver.Path a b}
    (hp : p = p') (hq : q = q')
    {X Y : C60F52OriginalTwo p q}
    (f : X ⟶ Y) :
    (⟨c60F52ReindexFace hp hq X.original⟩ :
      C60F52OriginalTwo p' q') ⟶
    (⟨c60F52ReindexFace hp hq Y.original⟩ :
      C60F52OriginalTwo p' q') :=
  Quot.liftOn f
    (fun raw => c60F52Of (.reindex hp hq raw))
    (by
      intro rf rg heq
      apply Quot.sound
      exact heq)

theorem c60F52ReindexMap_eval
    {a b : IcosahedralDart}
    {p q p' q' : Quiver.Path a b}
    (hp : p = p') (hq : q = q')
    {X Y : C60F52OriginalTwo p q}
    (f : X ⟶ Y) :
    c60F52Eval (c60F52ReindexMap hp hq f) = c60F52Eval f := by
  refine Quot.inductionOn f (fun raw => ?_)
  rfl

/-- NATURALITY of the F52 source associator on ALL F52
generators, including F51 inherited original F43 cells and
newly adjoined higher contexts. The RHS is explicitly
transported along two *proved* Quiver.Path.comp_assoc laws. -/
theorem c60F52Associator_naturality
    {a b c d : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {t u : Quiver.Path c d}
    {X X' : C60F52OriginalTwo p q}
    {Y Y' : C60F52OriginalTwo r s}
    {Z Z' : C60F52OriginalTwo t u}
    (f : X ⟶ X') (g : Y ⟶ Y') (h : Z ⟶ Z') :
    c60F52HorizontalMap (c60F52HorizontalMap f g) h ≫
      c60F52Associator X' Y' Z' =
    c60F52Associator X Y Z ≫
      c60F52ReindexMap
        (Quiver.Path.comp_assoc p r t).symm
        (Quiver.Path.comp_assoc q s u).symm
        (c60F52HorizontalMap f (c60F52HorizontalMap g h)) := by
  apply c60F52Hom_ext
  simp only [c60F52Eval_comp, c60F52HorizontalMap_eval,
    c60F52Associator_eval, c60F52ReindexMap_eval]
  abel

/-- A genuinely typed source unit 2-cell at the actual C60 vertex. -/
def c60F52IdentityTwo (a : IcosahedralDart) :
    C60F52OriginalTwo
      (Quiver.Path.nil : Quiver.Path a a)
      (Quiver.Path.nil : Quiver.Path a a) :=
  ⟨C60F42PresentedFaceCell.ident Quiver.Path.nil⟩

/-- Left-unit naturality uses the actual C60 nil_comp equalities
as DEPENDENT source-and-target path reindexing. -/
theorem c60F52LeftUnitor_naturality
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    {X Y : C60F52OriginalTwo p q}
    (f : X ⟶ Y) :
    c60F52ReindexMap
        (Quiver.Path.nil_comp p) (Quiver.Path.nil_comp q)
        (c60F52HorizontalMap (𝟙 (c60F52IdentityTwo a)) f) ≫
      c60F52LeftUnitor Y =
    c60F52LeftUnitor X ≫ f := by
  apply c60F52Hom_ext
  simp only [c60F52Eval_comp, c60F52ReindexMap_eval,
    c60F52HorizontalMap_eval, c60F52Eval_id,
    c60F52LeftUnitor_eval, zero_add, add_zero]

theorem c60F52RightUnitor_naturality
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    {X Y : C60F52OriginalTwo p q}
    (f : X ⟶ Y) :
    c60F52ReindexMap
        (Quiver.Path.comp_nil p) (Quiver.Path.comp_nil q)
        (c60F52HorizontalMap f (𝟙 (c60F52IdentityTwo b))) ≫
      c60F52RightUnitor Y =
    c60F52RightUnitor X ≫ f := by
  apply c60F52Hom_ext
  simp only [c60F52Eval_comp, c60F52ReindexMap_eval,
    c60F52HorizontalMap_eval, c60F52Eval_id,
    c60F52RightUnitor_eval, zero_add, add_zero]

/-- The genuine F43 north-face generator survives the
source associator extension with independent ODD exchange. -/
def c60F52NorthFaceTwo :
    C60F52OriginalTwo
      (c60F41PentagonBoundaryLoop .north) Quiver.Path.nil :=
  ⟨c60F43NorthPentagonFaceTwoCell⟩

def c60F52NorthOriginalInterchanger :
    c60F52OriginalTwoHorizontal
      c60F52NorthFaceTwo c60F52NorthFaceTwo ⟶
    c60F52OriginalTwoHorizontalRight
      c60F52NorthFaceTwo c60F52NorthFaceTwo :=
  c60F52OriginalInterchanger c60F52NorthFaceTwo c60F52NorthFaceTwo

theorem c60F52NorthOriginalInterchanger_phaseOne :
    (c60F52Eval c60F52NorthOriginalInterchanger).phase =
      (1 : ZMod 2) := by
  change c60F43NorthPentagonInterchange.toNative.phase = 1
  exact c60F43NorthPentagonInterchange_components.2

theorem c60F52NorthOriginalInterchanger_nontrivial :
    c60F52Eval c60F52NorthOriginalInterchanger ≠
      (0 : GradedThreeCell 0 0) := by
  intro h
  have hp := congrArg GradedThreeCell.phase h
  change (1 : ZMod 2) = 0 at hp
  exact (by decide : (1 : ZMod 2) ≠ 0) hp

#print axioms c60F52HorizontalThreeHomFunctor
#print axioms c60F52HorizontalMap_eval
#print axioms c60F52ReindexMap_eval
#print axioms c60F52Associator_naturality
#print axioms c60F52LeftUnitor_naturality
#print axioms c60F52RightUnitor_naturality
#print axioms c60F52NorthOriginalInterchanger_phaseOne
#print axioms c60F52NorthOriginalInterchanger_nontrivial

end
end KUOS.DependentOriginationGrayC60OriginalFaceAssociatorNaturalityV5_200
