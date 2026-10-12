import KUOS.DependentOriginationGrayC60F55TwoContextBeckChevalleyV5_208

namespace KUOS.DependentOriginationGrayC60F55TwoContextPhysicalV5_208

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60F55SourcePhaseLockedAtlasV5_175
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60FaceWhiskeringFunctorsV5_193
open KUOS.DependentOriginationGrayC60OriginalF55WhiskeringV5_193
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60MixedBoundaryWhiskeringV5_195
open KUOS.DependentOriginationGrayC60F55MixedOriginalContextV5_205
open KUOS.DependentOriginationGrayC60F55OriginalWhiskerNoLiftV5_206
open KUOS.DependentOriginationGrayC60F55OriginalContextBeckChevalleyV5_207
open KUOS.DependentOriginationGrayC60F55PhysicalIncidenceBeckChevalleyV5_207
open KUOS.DependentOriginationGrayC60F55TwoContextBeckChevalleyV5_208
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.208 / F59-F59-B — source RIGHT two-context Beck–Chevalley,
# genuine C60 incidence and persistent ORIGINAL F55 obstruction

The two F42 C60 suffix-path stages and two independent F54/F55
earlier-tree stages are separately typed and not identified. Applying
the generic two-context pasting to actual F58 source NatIso gives the
RIGHT two-stage square. Both LEFT and RIGHT are then specialized to
every genuine C60 edge with the two distinct incident polygonal
faces and their independent original F42 loop base darts.

The adjoined F47 mixed correction stays nonliftable by the old nine-
constructor F55 source after either two-step context. No global
descent or raw F42/F54/F55 Gray 3-category is concluded.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section TwoSuccessiveOriginalRightContexts

variable {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : Blocks a b} {pa pb : Blocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}
variable {r s : OriginalF45BracketTree.DepthRotationRoute first last}
variable {v₀ w₀ v₁ w₁ : IcosahedralDart}
variable {p₀ q₀ : Quiver.Path v₀ w₀}
variable {p₁ q₁ : Quiver.Path v₁ w₁}
variable {α₀ β₀ : C60F42PresentedFaceCell p₀ q₀}
variable {α₁ β₁ : C60F42PresentedFaceCell p₁ q₁}
variable (B₀ : C60F47SquareFrame α₀ β₀ r s)
variable (B₁ : C60F47SquareFrame α₁ β₁ r s)

/-- The first original RIGHT C60 path whiskering preserves equality of
the complete original F43 image across the two source F47 frames. -/
theorem c60F59RightIntermediateFaceNative
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    {u₀ u₁ : IcosahedralDart}
    (suffix₀ : Quiver.Path w₀ u₀) (suffix₁ : Quiver.Path w₁ u₁)
    {k₁ l₁ : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (earlier₁ : OriginalF45BracketTree k₁ l₁ mc pc ma pa) :
    c60F44FaceThreeEval
        (c60F47WhiskerRight B₀ suffix₀ earlier₁).faceStep =
      c60F44FaceThreeEval
        (c60F47WhiskerRight B₁ suffix₁ earlier₁).faceStep := by
  calc
    c60F44FaceThreeEval (c60F47WhiskerRight B₀ suffix₀ earlier₁).faceStep =
        c60F44FaceThreeEval B₀.faceStep :=
      c60F45RightWhiskerGrayMap suffix₀ B₀.faceStep
    _ = c60F44FaceThreeEval B₁.faceStep := hface
    _ = c60F44FaceThreeEval
        (c60F47WhiskerRight B₁ suffix₁ earlier₁).faceStep :=
      (c60F45RightWhiskerGrayMap suffix₁ B₁.faceStep).symm

/-- Original F54/F55 right-context preservation of BOTH integer
charges and the exchange phase, independently of the F42 suffixes. -/
theorem c60F59RightIntermediateRotationNative
    (hrot : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    {u₀ u₁ : IcosahedralDart}
    (suffix₀ : Quiver.Path w₀ u₀) (suffix₁ : Quiver.Path w₁ u₁)
    {k₁ l₁ : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (earlier₁ : OriginalF45BracketTree k₁ l₁ mc pc ma pa) :
    c60F44OriginalF55Eval
        (c60F47WhiskerRight B₀ suffix₀ earlier₁).rotationStep =
      c60F44OriginalF55Eval
        (c60F47WhiskerRight B₁ suffix₁ earlier₁).rotationStep := by
  calc
    c60F44OriginalF55Eval
        (c60F47WhiskerRight B₀ suffix₀ earlier₁).rotationStep =
      c60F44OriginalF55Eval B₀.rotationStep :=
      c60F45F55RightContextGrayMap earlier₁ B₀.rotationStep
    _ = c60F44OriginalF55Eval B₁.rotationStep := hrot
    _ = c60F44OriginalF55Eval
        (c60F47WhiskerRight B₁ suffix₁ earlier₁).rotationStep :=
      (c60F45F55RightContextGrayMap earlier₁ B₁.rotationStep).symm

/-- Real second-stage source F47 face-choice after independently
contextualizing the F42 paths and the F54/F55 bracket-tree routes. -/
def c60F59RightSecondFaceChoice
    (hedge : B₀.edge = B₁.edge)
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrot : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    {u₀ u₁ z₀ z₁ : IcosahedralDart}
    (suffix₀ : Quiver.Path w₀ u₀) (suffix₁ : Quiver.Path w₁ u₁)
    (outer₀ : Quiver.Path u₀ z₀) (outer₁ : Quiver.Path u₁ z₁)
    {k₁ l₁ k₂ l₂ : Nat}
    {mc md : Blocks a b} {pc pd : Blocks x y}
    (earlier₁ : OriginalF45BracketTree k₁ l₁ mc pc ma pa)
    (earlier₂ : OriginalF45BracketTree k₂ l₂ md pd mc pc) :
    C60F47BoundaryPoint
        (c60F47WhiskerRight (c60F47WhiskerRight B₀ suffix₀ earlier₁)
          outer₀ earlier₂) ⥤
      C60F47BoundaryPoint
        (c60F47WhiskerRight (c60F47WhiskerRight B₁ suffix₁ earlier₁)
          outer₁ earlier₂) :=
  c60F58RightAfterFaceChoice
    (c60F47WhiskerRight B₀ suffix₀ earlier₁)
    (c60F47WhiskerRight B₁ suffix₁ earlier₁)
    (by change B₀.edge = B₁.edge; exact hedge)
    (c60F59RightIntermediateFaceNative B₀ B₁ hface suffix₀ suffix₁ earlier₁)
    (c60F59RightIntermediateRotationNative B₀ B₁ hrot suffix₀ suffix₁ earlier₁)
    outer₀ outer₁ earlier₂

/-- Mathlib source NatIso after two independently typed ORIGINAL
F42 suffix paths and two ORIGINAL F54 bracket-tree earlier contexts.
All intermediate and final categories carry four genuine source tags. -/
def c60F59RightTwoContextNatIso
    (hedge : B₀.edge = B₁.edge)
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrot : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    {u₀ u₁ z₀ z₁ : IcosahedralDart}
    (suffix₀ : Quiver.Path w₀ u₀) (suffix₁ : Quiver.Path w₁ u₁)
    (outer₀ : Quiver.Path u₀ z₀) (outer₁ : Quiver.Path u₁ z₁)
    {k₁ l₁ k₂ l₂ : Nat}
    {mc md : Blocks a b} {pc pd : Blocks x y}
    (earlier₁ : OriginalF45BracketTree k₁ l₁ mc pc ma pa)
    (earlier₂ : OriginalF45BracketTree k₂ l₂ md pd mc pc) :
    ((c60F56OriginalRightMixedContextFunctor B₀ suffix₀ earlier₁) ⋙
      (c60F56OriginalRightMixedContextFunctor
        (c60F47WhiskerRight B₀ suffix₀ earlier₁) outer₀ earlier₂)) ⋙
      (c60F59RightSecondFaceChoice B₀ B₁ hedge hface hrot
        suffix₀ suffix₁ outer₀ outer₁ earlier₁ earlier₂) ≅
    (c60F56ContextMixedFunctor B₀ B₁ hedge hface hrot) ⋙
      ((c60F56OriginalRightMixedContextFunctor B₁ suffix₁ earlier₁) ⋙
        (c60F56OriginalRightMixedContextFunctor
          (c60F47WhiskerRight B₁ suffix₁ earlier₁) outer₁ earlier₂)) := by
  let B₀' := c60F47WhiskerRight B₀ suffix₀ earlier₁
  let B₁' := c60F47WhiskerRight B₁ suffix₁ earlier₁
  let hedge' : B₀'.edge = B₁'.edge := by
    change B₀.edge = B₁.edge
    exact hedge
  let hface' : c60F44FaceThreeEval B₀'.faceStep =
      c60F44FaceThreeEval B₁'.faceStep :=
    c60F59RightIntermediateFaceNative B₀ B₁ hface suffix₀ suffix₁ earlier₁
  let hrot' : c60F44OriginalF55Eval B₀'.rotationStep =
      c60F44OriginalF55Eval B₁'.rotationStep :=
    c60F59RightIntermediateRotationNative B₀ B₁ hrot suffix₀ suffix₁ earlier₁
  exact c60F59TwoContextPasting
    (c60F56OriginalRightMixedContextFunctor B₀ suffix₀ earlier₁)
    (c60F56OriginalRightMixedContextFunctor B₀' outer₀ earlier₂)
    (c60F56OriginalRightMixedContextFunctor B₁ suffix₁ earlier₁)
    (c60F56OriginalRightMixedContextFunctor B₁' outer₁ earlier₂)
    (c60F56ContextMixedFunctor B₀ B₁ hedge hface hrot)
    (c60F58RightAfterFaceChoice B₀ B₁ hedge hface hrot suffix₀ suffix₁ earlier₁)
    (c60F58RightAfterFaceChoice B₀' B₁' hedge' hface' hrot' outer₀ outer₁ earlier₂)
    (c60F58RightFaceContext_NatIso B₀ B₁ hedge hface hrot
      suffix₀ suffix₁ earlier₁)
    (c60F58RightFaceContext_NatIso B₀' B₁' hedge' hface' hrot'
      outer₀ outer₁ earlier₂)

end TwoSuccessiveOriginalRightContexts

section RealPhysicalC60TwoContext
variable {a b : D} {x y : E}
variable {n₁ n₂ m₁ m₂ : Nat}
variable {p₀ p₁ p₂ : Blocks a b} {q₀ q₁ q₂ : Blocks x y}
variable
  (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
  (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
variable
  {leftAfter : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁}
  {rightAfter : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂}
  (left : OriginalF45BracketTree.LocalRotation t₁ leftAfter)
  (right : OriginalF45BracketTree.LocalRotation t₂ rightAfter)

/-- For EVERY real C60 edge, LEFT two-context BC: two independently
based true original face loops and two separately typed F54 later trees. -/
def c60F59PhysicalLeftTwoContextNatIso
    (edge : TruncatedIcosahedralEdge)
    {u₀ u₁ z₀ z₁ : IcosahedralDart}
    (prior₀ : Quiver.Path u₀ (c60F58OriginalPhysicalFaceBase edge false))
    (prior₁ : Quiver.Path u₁ (c60F58OriginalPhysicalFaceBase edge true))
    (outer₀ : Quiver.Path z₀ u₀) (outer₁ : Quiver.Path z₁ u₁)
    {k₁ l₁ k₂ l₂ : Nat}
    {mc md : Blocks a b} {pc pd : Blocks x y}
    (later₁ : OriginalF45BracketTree k₁ l₁ p₂ q₂ mc pc)
    (later₂ : OriginalF45BracketTree k₂ l₂ mc pc md pd) :=
  c60F59LeftTwoContextNatIso
    (c60F58PhysicalMixedFrame t₁ t₂ left right edge false)
    (c60F58PhysicalMixedFrame t₁ t₂ left right edge true)
    rfl
    (c60F58PhysicalTwoFaces_sameOriginalF43 t₁ t₂ left right edge)
    (c60F58PhysicalTwoFaces_sameOriginalF55 t₁ t₂ left right edge)
    prior₀ prior₁ outer₀ outer₁ later₁ later₂

/-- For EVERY real C60 edge, RIGHT two-context BC: two independently
based true original face loops and two separately typed F54 earlier trees. -/
def c60F59PhysicalRightTwoContextNatIso
    (edge : TruncatedIcosahedralEdge)
    {u₀ u₁ z₀ z₁ : IcosahedralDart}
    (suffix₀ : Quiver.Path (c60F58OriginalPhysicalFaceBase edge false) u₀)
    (suffix₁ : Quiver.Path (c60F58OriginalPhysicalFaceBase edge true) u₁)
    (outer₀ : Quiver.Path u₀ z₀) (outer₁ : Quiver.Path u₁ z₁)
    {k₁ l₁ k₂ l₂ : Nat}
    {mc md : Blocks a b} {pc pd : Blocks x y}
    (earlier₁ : OriginalF45BracketTree k₁ l₁ mc pc p₀ q₀)
    (earlier₂ : OriginalF45BracketTree k₂ l₂ md pd mc pc) :=
  c60F59RightTwoContextNatIso
    (c60F58PhysicalMixedFrame t₁ t₂ left right edge false)
    (c60F58PhysicalMixedFrame t₁ t₂ left right edge true)
    rfl
    (c60F58PhysicalTwoFaces_sameOriginalF43 t₁ t₂ left right edge)
    (c60F58PhysicalTwoFaces_sameOriginalF55 t₁ t₂ left right edge)
    suffix₀ suffix₁ outer₀ outer₁ earlier₁ earlier₂

/-- Despite TWO genuine left source contexts, the new mixed receiver
Delta cannot come from the OLD F55 nine-constructor PresentedCell. -/
theorem c60F59PhysicalLeftTwoContext_noOriginalF55Delta
    (edge : TruncatedIcosahedralEdge) (side : Bool)
    {u z : IcosahedralDart}
    (prior : Quiver.Path u (c60F58OriginalPhysicalFaceBase edge side))
    (outer : Quiver.Path z u)
    {k₁ l₁ k₂ l₂ : Nat}
    {mc md : Blocks a b} {pc pd : Blocks x y}
    (later₁ : OriginalF45BracketTree k₁ l₁ p₂ q₂ mc pc)
    (later₂ : OriginalF45BracketTree k₂ l₂ mc pc md pd) :
    ¬ ∃ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell
      ((c60F45F55LeftContextFunctor later₂).obj
        ((c60F45F55LeftContextFunctor later₁).obj
          (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right)))
      ((c60F45F55LeftContextFunctor later₂).obj
        ((c60F45F55LeftContextFunctor later₁).obj
          (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right))),
      c60F44FaceThreeEval
        (c60F47WhiskerLeft
          (c60F47WhiskerLeft
            (c60F58PhysicalMixedFrame t₁ t₂ left right edge side)
            prior later₁) outer later₂).faceStep +
        c60F55SourceNative cell =
          c60F44OriginalF55Eval
            (c60F47WhiskerLeft
              (c60F47WhiskerLeft
                (c60F58PhysicalMixedFrame t₁ t₂ left right edge side)
                prior later₁) outer later₂).rotationStep :=
  c60F57OriginalLeftContext_noOriginalF55Lift
    (c60F47WhiskerLeft
      (c60F58PhysicalMixedFrame t₁ t₂ left right edge side) prior later₁)
    outer later₂

/-- The same independently original nine-constructor obstruction
persists after BOTH right source F42/F54 contextualizations. -/
theorem c60F59PhysicalRightTwoContext_noOriginalF55Delta
    (edge : TruncatedIcosahedralEdge) (side : Bool)
    {u z : IcosahedralDart}
    (suffix : Quiver.Path (c60F58OriginalPhysicalFaceBase edge side) u)
    (outer : Quiver.Path u z)
    {k₁ l₁ k₂ l₂ : Nat}
    {mc md : Blocks a b} {pc pd : Blocks x y}
    (earlier₁ : OriginalF45BracketTree k₁ l₁ mc pc p₀ q₀)
    (earlier₂ : OriginalF45BracketTree k₂ l₂ md pd mc pc) :
    ¬ ∃ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell
      ((c60F45F55RightContextFunctor earlier₂).obj
        ((c60F45F55RightContextFunctor earlier₁).obj
          (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right)))
      ((c60F45F55RightContextFunctor earlier₂).obj
        ((c60F45F55RightContextFunctor earlier₁).obj
          (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right))),
      c60F44FaceThreeEval
        (c60F47WhiskerRight
          (c60F47WhiskerRight
            (c60F58PhysicalMixedFrame t₁ t₂ left right edge side)
            suffix earlier₁) outer earlier₂).faceStep +
        c60F55SourceNative cell =
          c60F44OriginalF55Eval
            (c60F47WhiskerRight
              (c60F47WhiskerRight
                (c60F58PhysicalMixedFrame t₁ t₂ left right edge side)
                suffix earlier₁) outer earlier₂).rotationStep :=
  c60F57OriginalRightContext_noOriginalF55Lift
    (c60F47WhiskerRight
      (c60F58PhysicalMixedFrame t₁ t₂ left right edge side) suffix earlier₁)
    outer earlier₂

#print axioms c60F59RightIntermediateFaceNative
#print axioms c60F59RightIntermediateRotationNative
#print axioms c60F59RightSecondFaceChoice
#print axioms c60F59RightTwoContextNatIso
#print axioms c60F59PhysicalLeftTwoContextNatIso
#print axioms c60F59PhysicalRightTwoContextNatIso
#print axioms c60F59PhysicalLeftTwoContext_noOriginalF55Delta
#print axioms c60F59PhysicalRightTwoContext_noOriginalF55Delta

end RealPhysicalC60TwoContext
end
end KUOS.DependentOriginationGrayC60F55TwoContextPhysicalV5_208
