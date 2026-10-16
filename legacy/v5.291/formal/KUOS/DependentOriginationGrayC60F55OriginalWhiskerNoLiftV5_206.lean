import KUOS.DependentOriginationGrayC60F55CrossRotationCocycleV5_206
import KUOS.DependentOriginationGrayC60MixedBoundaryWhiskeringV5_195

namespace KUOS.DependentOriginationGrayC60F55OriginalWhiskerNoLiftV5_206

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
open KUOS.DependentOriginationGrayC60CalibratedFaceF55BridgeV5_194
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60MixedBoundaryWhiskeringV5_195
open KUOS.DependentOriginationGrayC60F55MixedOriginalContextV5_205
open KUOS.DependentOriginationGrayC60F55CrossRotationCocycleV5_206
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.206 / F59-F57-B — original F42/F54 simultaneous left/right
# whiskering is FULL AND FAITHFUL, but cannot absorb genuine mixed Delta

F56-B showed faithful four-boundary mixed F47 source-context
functors obtained by actually applying original F42 Quiver.Path
left/right whiskering and the INDEPENDENT ORIGINAL F54/F55
bracket-tree contextual whiskerings to the original mixed square.

F57-A now supplies categorical fullness even between different
original F54 route TYPES, hence both real context functors are
fully faithful on ALL mixed source three-Homs. We also prove
that no ORIGINAL nine-constructor F55 PresentedCell between
the original contextualized rotation routes can substitute for
the adjoined mixed comparison after either actual whiskering.

The corresponding MIXED four-boundary source square still
commutes: existence in the adjoined F47 quotient, but
nonexistence in the original F55 grammar. This records the
precise lifting obstruction instead of inferring global descent.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section OriginalIndependentWhiskering

variable {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : Blocks a b} {pa pb : Blocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}
variable {v w : IcosahedralDart} {p q : Quiver.Path v w}
variable {α β : C60F42PresentedFaceCell p q}
variable {r s : OriginalF45BracketTree.DepthRotationRoute first last}

variable (B : C60F47SquareFrame α β r s)

/-- All FOUR real mixed-boundary positions are preserved and
EVERY full-native mixed three-Hom is bijectively mapped by
simultaneously whiskering the ORIGINAL F42 source path to the
left and adding a genuinely independent ORIGINAL F54/F55 later
bracket-tree context. Older F56 proved only faithfulness. -/
theorem c60F57OriginalLeftContext_hom_bijective
    {u : IcosahedralDart} (prior : Quiver.Path u v)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (later : OriginalF45BracketTree k l mb pb mc pc)
    {X Y : C60F47BoundaryPoint B} :
    Function.Bijective
      (fun (f : X ⟶ Y) =>
        (c60F56OriginalLeftMixedContextFunctor
          B prior later).map f) := by
  exact c60F57CrossOriginalContext_hom_bijective
    B (c60F47WhiskerLeft B prior later)
    rfl
    (c60F45LeftWhiskerGrayMap prior B.faceStep).symm
    (c60F45F55LeftContextGrayMap later B.rotationStep).symm

/-- The independently typed right Quiver.Path suffix and OLD
F54 earlier-bracket context also induce a full and faithful
mixed four-boundary source three-Hom functor, without erasing
either original source system. -/
theorem c60F57OriginalRightContext_hom_bijective
    {u : IcosahedralDart} (suffix : Quiver.Path w u)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (earlier : OriginalF45BracketTree k l mc pc ma pa)
    {X Y : C60F47BoundaryPoint B} :
    Function.Bijective
      (fun (f : X ⟶ Y) =>
        (c60F56OriginalRightMixedContextFunctor
          B suffix earlier).map f) := by
  exact c60F57CrossOriginalContext_hom_bijective
    B (c60F47WhiskerRight B suffix earlier)
    rfl
    (c60F45RightWhiskerGrayMap suffix B.faceStep).symm
    (c60F45F55RightContextGrayMap earlier B.rotationStep).symm

/-- Actual original F42/F54 LEFT contexts DO NOT turn an
adjoined F47 mixed comparison into an original F55 source.
For ANY proof-relevant original F55 raw nine-constructor word
at the precise later-whiskered original F54 2-cell endpoints,
full-native equality to the calibrated original rotation square
would force the forbidden non-phase-locked Delta=(0,1;0).
No new axiom or original F55 generator is introduced. -/
theorem c60F57OriginalLeftContext_noOriginalF55Lift
    {u : IcosahedralDart} (prior : Quiver.Path u v)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (later : OriginalF45BracketTree k l mb pb mc pc) :
    ¬ ∃ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell
      ((c60F45F55LeftContextFunctor later).obj r)
      ((c60F45F55LeftContextFunctor later).obj s),
      c60F44FaceThreeEval
        (c60F47WhiskerLeft B prior later).faceStep +
        c60F55SourceNative cell =
          c60F44OriginalF55Eval
            (c60F47WhiskerLeft B prior later).rotationStep := by
  rintro ⟨cell, heq⟩
  have hcal := (c60F47WhiskerLeft B prior later).calibrated
  have hreceiver :
      c60F55SourceNative cell =
        c60F46FaceF55ComparisonCalibration := by
    exact add_left_cancel (heq.trans hcal.symm)
  have hmem := c60F55SourceNative_mem cell
  rw [hreceiver] at hmem
  exact c60F46FaceF55ComparisonCalibration_notOriginalF55Locked hmem

/-- Analogous original-F55 NO-LIFT after simultaneous true
RIGHT original F42 suffix and independently typed old F54
earlier bracket-tree context. -/
theorem c60F57OriginalRightContext_noOriginalF55Lift
    {u : IcosahedralDart} (suffix : Quiver.Path w u)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (earlier : OriginalF45BracketTree k l mc pc ma pa) :
    ¬ ∃ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell
      ((c60F45F55RightContextFunctor earlier).obj r)
      ((c60F45F55RightContextFunctor earlier).obj s),
      c60F44FaceThreeEval
        (c60F47WhiskerRight B suffix earlier).faceStep +
        c60F55SourceNative cell =
          c60F44OriginalF55Eval
            (c60F47WhiskerRight B suffix earlier).rotationStep := by
  rintro ⟨cell, heq⟩
  have hcal := (c60F47WhiskerRight B suffix earlier).calibrated
  have hreceiver :
      c60F55SourceNative cell =
        c60F46FaceF55ComparisonCalibration := by
    exact add_left_cancel (heq.trans hcal.symm)
  have hmem := c60F55SourceNative_mem cell
  rw [hreceiver] at hmem
  exact c60F46FaceF55ComparisonCalibration_notOriginalF55Locked hmem

/-- GENUINE typed original F42/F54/F55 LEFT-whiskered
four-boundary source square coexists with uniform OLD ORIGINAL
F55 nine-constructor non-representability of the NEW receiver.
It cannot be removed by adding original path/tree context. -/
theorem c60F57LeftContext_mixedSquare_and_noOriginalLift
    {u : IcosahedralDart} (prior : Quiver.Path u v)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (later : OriginalF45BracketTree k l mb pb mc pc) :
    (c60F47FaceArrow (c60F47WhiskerLeft B prior later) ≫
        c60F47CompareAfter (c60F47WhiskerLeft B prior later) =
      c60F47CompareBefore (c60F47WhiskerLeft B prior later) ≫
        c60F47OriginalF55Arrow (c60F47WhiskerLeft B prior later)) ∧
    (¬ ∃ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell
      ((c60F45F55LeftContextFunctor later).obj r)
      ((c60F45F55LeftContextFunctor later).obj s),
      c60F44FaceThreeEval
        (c60F47WhiskerLeft B prior later).faceStep +
        c60F55SourceNative cell =
          c60F44OriginalF55Eval
            (c60F47WhiskerLeft B prior later).rotationStep) :=
  ⟨c60F47WhiskerLeft_mixedSquare B prior later,
    c60F57OriginalLeftContext_noOriginalF55Lift B prior later⟩

theorem c60F57RightContext_mixedSquare_and_noOriginalLift
    {u : IcosahedralDart} (suffix : Quiver.Path w u)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (earlier : OriginalF45BracketTree k l mc pc ma pa) :
    (c60F47FaceArrow (c60F47WhiskerRight B suffix earlier) ≫
        c60F47CompareAfter (c60F47WhiskerRight B suffix earlier) =
      c60F47CompareBefore (c60F47WhiskerRight B suffix earlier) ≫
        c60F47OriginalF55Arrow (c60F47WhiskerRight B suffix earlier)) ∧
    (¬ ∃ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell
      ((c60F45F55RightContextFunctor earlier).obj r)
      ((c60F45F55RightContextFunctor earlier).obj s),
      c60F44FaceThreeEval
        (c60F47WhiskerRight B suffix earlier).faceStep +
        c60F55SourceNative cell =
          c60F44OriginalF55Eval
            (c60F47WhiskerRight B suffix earlier).rotationStep) :=
  ⟨c60F47WhiskerRight_mixedSquare B suffix earlier,
    c60F57OriginalRightContext_noOriginalF55Lift B suffix earlier⟩

/-- The contextual functors map the GENUINE new F47 comparison
generator itself, not only the two original face/F55 composite
arrows: Delta is retained as an explicitly adjoined source
three-morphism and is never relabeled as old F55 syntax. -/
theorem c60F57LeftContext_compareAfter
    {u : IcosahedralDart} (prior : Quiver.Path u v)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (later : OriginalF45BracketTree k l mb pb mc pc) :
    (c60F56OriginalLeftMixedContextFunctor B prior later).map
      (c60F47CompareAfter B) =
        c60F47CompareAfter (c60F47WhiskerLeft B prior later) := by
  apply Quot.sound
  rfl

theorem c60F57RightContext_compareAfter
    {u : IcosahedralDart} (suffix : Quiver.Path w u)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (earlier : OriginalF45BracketTree k l mc pc ma pa) :
    (c60F56OriginalRightMixedContextFunctor B suffix earlier).map
      (c60F47CompareAfter B) =
        c60F47CompareAfter (c60F47WhiskerRight B suffix earlier) := by
  apply Quot.sound
  rfl

#print axioms c60F57OriginalLeftContext_hom_bijective
#print axioms c60F57OriginalRightContext_hom_bijective
#print axioms c60F57OriginalLeftContext_noOriginalF55Lift
#print axioms c60F57OriginalRightContext_noOriginalF55Lift
#print axioms c60F57LeftContext_mixedSquare_and_noOriginalLift
#print axioms c60F57RightContext_mixedSquare_and_noOriginalLift
#print axioms c60F57LeftContext_compareAfter
#print axioms c60F57RightContext_compareAfter

end OriginalIndependentWhiskering
end
end KUOS.DependentOriginationGrayC60F55OriginalWhiskerNoLiftV5_206
