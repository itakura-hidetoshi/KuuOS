import KUOS.DependentOriginationGrayC60OriginalFaceUnitTriangleV5_202

namespace KUOS.DependentOriginationGrayC60OriginalF43RightHorizontalV5_203

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60NativePathFunctorV5_189
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalPresentationV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalThreeHomV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceAssociatorPresentationV5_200
open KUOS.DependentOriginationGrayC60OriginalFaceAssociatorThreeHomV5_200
open KUOS.DependentOriginationGrayC60OriginalFaceAssociatorNaturalityV5_200
open KUOS.DependentOriginationGrayC60OriginalFaceFourAssociatorPentagonV5_202
open KUOS.DependentOriginationGrayC60OriginalFaceUnitTriangleV5_202

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.203 / F59-F54-A: actual original F43 Gray interchanger as a natural
# comparison between genuine LEFT-FIRST and derived RIGHT-FIRST F52 3-Hom bifunctors

The original F42 face 2-cell witnesses remain objects of the same F52
source category. Its right-first composite is an INDEPENDENT original
F42 term. The F43 interchanger between these terms is a genuine older
source generator, preserved through F51/F52.

Right-first horizontal 3-arrow composition was not an original F43
constructor. We therefore DERIVE it via conjugation with the original
typed F43 interchange; it is not backdated into the old grammar.
The resulting bona-fide Mathlib bifunctor and its original-source
naturality transformation preserve BOTH integer charges and the
independent phase. The nonidentity north exchange remains nonzero.

The same functor acts on the genuine v5.202 2-vs-3 associator pentagon
and the unit triangle, with original physical C60 path indices and
proof-relevant F42 boundary witnesses unchanged. No F54/F55 primitive
or globally complete raw Gray 3-category is inferred.
-/

/-- The old genuine F43 exchange has a typed inverse in the F52
full-native-kernel 3-Hom. Its inverse is the inverse of an old
F43 generator, NOT a new fictitious F55 comparison. -/
def c60F54OriginalF43InterchangerIso
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (X : C60F52OriginalTwo p q)
    (Y : C60F52OriginalTwo r s) :
    c60F52OriginalTwoHorizontal X Y ≅
      c60F52OriginalTwoHorizontalRight X Y where
  hom := c60F52OriginalInterchanger X Y
  inv := c60F52Of
    (.symm (.ofF51 (.original (.interchange X.original Y.original))))
  hom_inv_id := by
    apply c60F52Hom_ext
    rw [c60F52Eval_catComp]
    change c60F43PhysicalInterchangerNative X.original Y.original +
      -(c60F43PhysicalInterchangerNative X.original Y.original) =
      (0 : GradedThreeCell 0 0)
    exact add_neg_cancel _
  inv_hom_id := by
    apply c60F52Hom_ext
    rw [c60F52Eval_catComp]
    change -(c60F43PhysicalInterchangerNative X.original Y.original) +
      c60F43PhysicalInterchangerNative X.original Y.original =
      (0 : GradedThreeCell 0 0)
    exact neg_add_cancel _

/-- Invariance of the actual F43 Gray exchange on ALL F52
3-arrows, including the explicitly added associator/unitors and
the original F43/F51/202 higher source contexts. The product of
original F42 face degrees, not just untyped phase projection,
controls the comparison. -/
theorem c60F54OriginalF43Interchanger_eval_invariant
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {X X' : C60F52OriginalTwo p q}
    {Y Y' : C60F52OriginalTwo r s}
    (f : X ⟶ X') (g : Y ⟶ Y') :
    c60F52Eval (c60F52OriginalInterchanger X Y) =
      c60F52Eval (c60F52OriginalInterchanger X' Y') := by
  rw [c60F52OriginalInterchanger_eval,
    c60F52OriginalInterchanger_eval]
  apply GradedThreeCell.ext
  · rfl
  · change c60F43FaceDegree X.original * c60F43FaceDegree Y.original =
      c60F43FaceDegree X'.original * c60F43FaceDegree Y'.original
    rw [c60F52Hom_degreeEq f, c60F52Hom_degreeEq g]

/-- The horizontal 3-morphism pair in RIGHT-FIRST F42 context,
derived from existing F52 horizontal composition by a conjugation
with two true old F43 interchangers. Each boundary is the actual
original right-first proof term, not its degree. -/
def c60F54RightHorizontalMap
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {X X' : C60F52OriginalTwo p q}
    {Y Y' : C60F52OriginalTwo r s}
    (f : X ⟶ X') (g : Y ⟶ Y') :
    c60F52OriginalTwoHorizontalRight X Y ⟶
      c60F52OriginalTwoHorizontalRight X' Y' :=
  (c60F54OriginalF43InterchangerIso X Y).inv ≫
    c60F52HorizontalMap f g ≫
    (c60F54OriginalF43InterchangerIso X' Y').hom

/-- Conjugating with source F43 exchanges does not discard their
nonzero phase: the old exchange phases cancel only because f and
g are proof-relevant F52 arrows preserving their F42 degrees. -/
theorem c60F54RightHorizontalMap_eval
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {X X' : C60F52OriginalTwo p q}
    {Y Y' : C60F52OriginalTwo r s}
    (f : X ⟶ X') (g : Y ⟶ Y') :
    c60F52Eval (c60F54RightHorizontalMap f g) =
      c60F52Eval f + c60F52Eval g := by
  unfold c60F54RightHorizontalMap
  simp only [c60F52Eval_catComp, c60F52HorizontalMap_eval]
  change -(c60F43PhysicalInterchangerNative X.original Y.original) +
      (c60F52Eval f + c60F52Eval g) +
      c60F43PhysicalInterchangerNative X'.original Y'.original =
        c60F52Eval f + c60F52Eval g
  have hi :
      c60F43PhysicalInterchangerNative X.original Y.original =
        c60F43PhysicalInterchangerNative X'.original Y'.original := by
    simpa only [c60F52OriginalInterchanger_eval] using
      c60F54OriginalF43Interchanger_eval_invariant f g
  rw [← hi]
  abel

/-- An actual Mathlib horizontal source 3-Hom bifunctor with
RIGHT-FIRST genuine F42 2-cell terms as objects. -/
def c60F54RightHorizontalThreeHomFunctor
    {a b c : IcosahedralDart}
    (p q : Quiver.Path a b) (r s : Quiver.Path b c) :
    (C60F52OriginalTwo p q × C60F52OriginalTwo r s) ⥤
      C60F52OriginalTwo (p.comp r) (q.comp s) where
  obj z := c60F52OriginalTwoHorizontalRight z.1 z.2
  map := fun {_ _} f => c60F54RightHorizontalMap f.1 f.2
  map_id := by
    intro ⟨X, Y⟩
    apply c60F52Hom_ext
    change c60F52Eval (c60F54RightHorizontalMap (𝟙 X) (𝟙 Y)) =
      c60F52Eval (𝟙 (c60F52OriginalTwoHorizontalRight X Y))
    rw [c60F54RightHorizontalMap_eval]
    simp
  map_comp := by
    intro ⟨X, Y⟩ ⟨X', Y'⟩ ⟨X'', Y''⟩ f g
    obtain ⟨f₁, f₂⟩ := f
    obtain ⟨g₁, g₂⟩ := g
    apply c60F52Hom_ext
    change
      c60F52Eval (c60F54RightHorizontalMap (f₁ ≫ g₁) (f₂ ≫ g₂)) =
      c60F52Eval
        (c60F54RightHorizontalMap f₁ f₂ ≫
          c60F54RightHorizontalMap g₁ g₂)
    simp only [c60F54RightHorizontalMap_eval, c60F52Eval_catComp]
    abel

/-- Genuine original F43 interchange NATURALITY in the
source F52 3-Hom, now connecting two actual Mathlib bifunctors.
The interchanger is NEVER replaced by a neutral identity cell. -/
theorem c60F54OriginalF43Interchanger_naturality
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {X X' : C60F52OriginalTwo p q}
    {Y Y' : C60F52OriginalTwo r s}
    (f : X ⟶ X') (g : Y ⟶ Y') :
    c60F52HorizontalMap f g ≫
      c60F52OriginalInterchanger X' Y' =
    c60F52OriginalInterchanger X Y ≫
      c60F54RightHorizontalMap f g := by
  apply c60F52Hom_ext
  rw [c60F52Eval_catComp, c60F52Eval_catComp,
    c60F52HorizontalMap_eval, c60F54RightHorizontalMap_eval,
    c60F54OriginalF43Interchanger_eval_invariant f g]
  exact add_comm _ _

/-- An honest categorical natural transformation with original
F43 SOURCE components, from left-first to the DERIVED right-first
F52 horizontal 3-Hom bifunctor. -/
def c60F54OriginalF43InterchangerNatTrans
    {a b c : IcosahedralDart}
    (p q : Quiver.Path a b) (r s : Quiver.Path b c) :
    c60F52HorizontalThreeHomFunctor p q r s ⟶
      c60F54RightHorizontalThreeHomFunctor p q r s where
  app z := c60F52OriginalInterchanger z.1 z.2
  naturality := by
    intro ⟨X, Y⟩ ⟨X', Y'⟩ f
    obtain ⟨f₁, f₂⟩ := f
    exact c60F54OriginalF43Interchanger_naturality f₁ f₂

/-- Its north-pentagon component is the unchanged ORIGINAL
F43 three-cell with genuine phase 1 rather than the identity. -/
theorem c60F54NorthF43NatTrans_phaseOne :
    (c60F52Eval
      ((c60F54OriginalF43InterchangerNatTrans
        (c60F41PentagonBoundaryLoop .north) Quiver.Path.nil
        (c60F41PentagonBoundaryLoop .north) Quiver.Path.nil).app
          (c60F52NorthFaceTwo, c60F52NorthFaceTwo))).phase =
      (1 : ZMod 2) :=
  c60F52NorthOriginalInterchanger_phaseOne

theorem c60F54NorthF43NatTrans_nontrivial :
    c60F52Eval
      ((c60F54OriginalF43InterchangerNatTrans
        (c60F41PentagonBoundaryLoop .north) Quiver.Path.nil
        (c60F41PentagonBoundaryLoop .north) Quiver.Path.nil).app
          (c60F52NorthFaceTwo, c60F52NorthFaceTwo)) ≠
      (0 : GradedThreeCell 0 0) :=
  c60F52NorthOriginalInterchanger_nontrivial

/-- The SAME F43 natural interchange transports the ACTUAL
v5.202 two-route F42 3-arrow associator pentagon in any
genuine RIGHT-FIRST horizontal C60 context. -/
theorem c60F54RightHorizontal_pentagon_coherence
    {a b c d e f : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {t u : Quiver.Path c d} {v w : Quiver.Path d e}
    {z z' : Quiver.Path e f}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s)
    (γ : C60F42PresentedFaceCell t u)
    (δ : C60F42PresentedFaceCell v w)
    (Z : C60F52OriginalTwo z z') :
    c60F54RightHorizontalMap
      (c60F53BPentagonShort α β γ δ) (𝟙 Z) =
    c60F54RightHorizontalMap
      (c60F53BPentagonLong α β γ δ) (𝟙 Z) :=
  congrArg (fun h => c60F54RightHorizontalMap h (𝟙 Z))
    (c60F53BOriginalFourFacePentagon α β γ δ)

/-- The actual v5.202 source-typed unit triangle is equally
preserved in the independent right-first original F42 context. -/
theorem c60F54RightHorizontal_triangle_coherence
    {a b c d : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {z z' : Quiver.Path c d}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s)
    (Z : C60F52OriginalTwo z z') :
    c60F54RightHorizontalMap
      (c60F53CTriangleAssocLeft α β) (𝟙 Z) =
    c60F54RightHorizontalMap
      (c60F53CTriangleRight α β) (𝟙 Z) :=
  congrArg (fun h => c60F54RightHorizontalMap h (𝟙 Z))
    (c60F53COriginalFaceUnitTriangle α β)

#print axioms c60F54OriginalF43InterchangerIso
#print axioms c60F54OriginalF43Interchanger_eval_invariant
#print axioms c60F54RightHorizontalMap_eval
#print axioms c60F54RightHorizontalThreeHomFunctor
#print axioms c60F54OriginalF43Interchanger_naturality
#print axioms c60F54OriginalF43InterchangerNatTrans
#print axioms c60F54NorthF43NatTrans_phaseOne
#print axioms c60F54NorthF43NatTrans_nontrivial
#print axioms c60F54RightHorizontal_pentagon_coherence
#print axioms c60F54RightHorizontal_triangle_coherence

end
end KUOS.DependentOriginationGrayC60OriginalF43RightHorizontalV5_203
