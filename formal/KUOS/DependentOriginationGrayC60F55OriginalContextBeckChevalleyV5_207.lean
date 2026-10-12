import KUOS.DependentOriginationGrayC60F55OriginalWhiskerNoLiftV5_206
import KUOS.DependentOriginationGrayC60F55CrossRotationCocycleV5_206

namespace KUOS.DependentOriginationGrayC60F55OriginalContextBeckChevalleyV5_207

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60FaceWhiskeringFunctorsV5_193
open KUOS.DependentOriginationGrayC60OriginalF55WhiskeringV5_193
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60MixedBoundaryWhiskeringV5_195
open KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196
open KUOS.DependentOriginationGrayC60AdjacentFaceMixedTransportV5_196
open KUOS.DependentOriginationGrayC60F55MixedOriginalContextV5_205
open KUOS.DependentOriginationGrayC60F55CrossRotationCocycleV5_206
open KUOS.DependentOriginationGrayC60F55OriginalWhiskerNoLiftV5_206
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.207 / F59-F58-A — original F42/F54 context vs mixed face choice
# Beck–Chevalley source natural isomorphism, left AND right

We do not just commute full-native integer/phase target images.
Four original F47 boundary tags and their original F42 face witnesses
are kept as source OBJECTS, and the old independent F54/F55 rotation
route witnesses stay independently typed.

Given two F47 frames on the SAME physical C60 edge, the original F42
face and F54/F55 sources may differ but must have proven identical
FULL original Gray image. For TWO independent real F42 context paths,
and a SHARED genuinely typed original F54 bracket-tree context,
we construct TWO actual source Mathlib categorical routes:

  first old source face-choice, THEN independent original contexts;
  first original contexts, THEN new correctly typed mixed face-choice.

They agree on ALL proof-relevant F47 mixed 3-Hom morphisms in the
existing full-native-kernel quotient and yield a Mathlib NatIso
with the four boundary objects retained. The corresponding
original F55 comparison Delta remains ADJOINED, not an original
nine-generator F55 primitive. This theorem does not identify
the differently typed raw original F42 or F54 source terms.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section GeneralActualOriginalContexts
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

/-- LEFT context: the two source C60 prior paths can have different
original endpoints, because two physically adjacent actual polygonal
F42 based loops need NOT start at the same C60 vertex. The old
F54/F55 later-context remains a separate actual rotation-tree. -/
def c60F58LeftAfterFaceChoice
    (hedge : B₀.edge = B₁.edge)
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrot : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    {u₀ u₁ : IcosahedralDart}
    (prior₀ : Quiver.Path u₀ v₀)
    (prior₁ : Quiver.Path u₁ v₁)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (later : OriginalF45BracketTree k l mb pb mc pc) :
    C60F47BoundaryPoint (c60F47WhiskerLeft B₀ prior₀ later) ⥤
      C60F47BoundaryPoint (c60F47WhiskerLeft B₁ prior₁ later) :=
  c60F56ContextMixedFunctor
    (c60F47WhiskerLeft B₀ prior₀ later)
    (c60F47WhiskerLeft B₁ prior₁ later)
    (by change B₀.edge = B₁.edge; exact hedge)
    (by
      calc
        c60F44FaceThreeEval
            (c60F47WhiskerLeft B₀ prior₀ later).faceStep =
          c60F44FaceThreeEval B₀.faceStep :=
            c60F45LeftWhiskerGrayMap prior₀ B₀.faceStep
        _ = c60F44FaceThreeEval B₁.faceStep := hface
        _ = c60F44FaceThreeEval
            (c60F47WhiskerLeft B₁ prior₁ later).faceStep :=
              (c60F45LeftWhiskerGrayMap prior₁ B₁.faceStep).symm)
    (by
      calc
        c60F44OriginalF55Eval
            (c60F47WhiskerLeft B₀ prior₀ later).rotationStep =
          c60F44OriginalF55Eval B₀.rotationStep :=
            c60F45F55LeftContextGrayMap later B₀.rotationStep
        _ = c60F44OriginalF55Eval B₁.rotationStep := hrot
        _ = c60F44OriginalF55Eval
            (c60F47WhiskerLeft B₁ prior₁ later).rotationStep :=
              (c60F45F55LeftContextGrayMap later B₁.rotationStep).symm)

/-- An explicit dependent four-boundary Hom cast. The two context/face
orders act on the SAME tagged final F47 source boundary only after
inspecting the original F42/F54 mixed tag. No original source word is
equated by this cast. -/
def c60F58LeftFaceContextHomCast
    (hedge : B₀.edge = B₁.edge)
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrot : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    {u₀ u₁ : IcosahedralDart}
    (prior₀ : Quiver.Path u₀ v₀)
    (prior₁ : Quiver.Path u₁ v₁)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (later : OriginalF45BracketTree k l mb pb mc pc)
    {X Y : C60F47BoundaryPoint B₀}
    (g :
      (c60F56OriginalLeftMixedContextFunctor B₁ prior₁ later).obj
        ((c60F56ContextMixedFunctor B₀ B₁ hedge hface hrot).obj X) ⟶
      (c60F56OriginalLeftMixedContextFunctor B₁ prior₁ later).obj
        ((c60F56ContextMixedFunctor B₀ B₁ hedge hface hrot).obj Y)) :
    (c60F58LeftAfterFaceChoice B₀ B₁ hedge hface hrot prior₀ prior₁ later).obj
        ((c60F56OriginalLeftMixedContextFunctor B₀ prior₀ later).obj X) ⟶
    (c60F58LeftAfterFaceChoice B₀ B₁ hedge hface hrot prior₀ prior₁ later).obj
        ((c60F56OriginalLeftMixedContextFunctor B₀ prior₀ later).obj Y) := by
  cases X <;> cases Y
  all_goals exact g

/-- TRUE SOURCE 3-Hom Beck–Chevalley square after two
independently typed original F42 left paths. Both sides are
MORPHISMS in exactly the SAME final F47 mixed category;
their original F42 face sources need never be identified. -/
theorem c60F58LeftFaceContext_BeckChevalley
    (hedge : B₀.edge = B₁.edge)
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrot : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    {u₀ u₁ : IcosahedralDart}
    (prior₀ : Quiver.Path u₀ v₀)
    (prior₁ : Quiver.Path u₁ v₁)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (later : OriginalF45BracketTree k l mb pb mc pc)
    {X Y : C60F47BoundaryPoint B₀} (f : X ⟶ Y) :
    (c60F58LeftAfterFaceChoice B₀ B₁ hedge hface hrot
      prior₀ prior₁ later).map
      ((c60F56OriginalLeftMixedContextFunctor B₀ prior₀ later).map f) =
    c60F58LeftFaceContextHomCast B₀ B₁ hedge hface hrot
      prior₀ prior₁ later
      ((c60F56OriginalLeftMixedContextFunctor B₁ prior₁ later).map
        ((c60F56ContextMixedFunctor B₀ B₁ hedge hface hrot).map f)) := by
  cases X <;> cases Y
  all_goals
    apply c60F47MixedGrayFunctor_faithful
      (c60F47WhiskerLeft B₁ prior₁ later)
    change c60F47MixedEval
        ((c60F58LeftAfterFaceChoice B₀ B₁ hedge hface hrot
          prior₀ prior₁ later).map
          ((c60F56OriginalLeftMixedContextFunctor
            B₀ prior₀ later).map f)) =
      c60F47MixedEval
        ((c60F56OriginalLeftMixedContextFunctor
          B₁ prior₁ later).map
          ((c60F56ContextMixedFunctor B₀ B₁ hedge hface hrot).map f))
    simp only [c60F58LeftAfterFaceChoice,
      c60F56OriginalLeftMixedContextFunctor,
      c60F56ContextMixedFunctor_fullNative]

/-- Mathlib NATURAL ISOMORPHISM, with real original F42 prior
paths (independent on the two sides) and actual original
F54/F55 later context. The components are typed source
isomorphisms at the four F47 boundary tags. -/
def c60F58LeftFaceContext_NatIso
    (hedge : B₀.edge = B₁.edge)
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrot : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    {u₀ u₁ : IcosahedralDart}
    (prior₀ : Quiver.Path u₀ v₀)
    (prior₁ : Quiver.Path u₁ v₁)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (later : OriginalF45BracketTree k l mb pb mc pc) :
    (c60F56OriginalLeftMixedContextFunctor B₀ prior₀ later) ⋙
      (c60F58LeftAfterFaceChoice B₀ B₁ hedge hface hrot
        prior₀ prior₁ later) ≅
    (c60F56ContextMixedFunctor B₀ B₁ hedge hface hrot) ⋙
      (c60F56OriginalLeftMixedContextFunctor B₁ prior₁ later) :=
  NatIso.ofComponents
    (fun X => by cases X <;> exact Iso.refl _)
    (by
      intro X Y f
      cases X <;> cases Y
      all_goals
        calc
          _ = (c60F58LeftAfterFaceChoice B₀ B₁ hedge hface hrot
                prior₀ prior₁ later).map
                ((c60F56OriginalLeftMixedContextFunctor
                  B₀ prior₀ later).map f) := Category.comp_id _
          _ = (c60F56OriginalLeftMixedContextFunctor
                B₁ prior₁ later).map
                ((c60F56ContextMixedFunctor
                  B₀ B₁ hedge hface hrot).map f) :=
              c60F58LeftFaceContext_BeckChevalley B₀ B₁
                hedge hface hrot prior₀ prior₁ later f
          _ = _ := (Category.id_comp _).symm)

/-- RIGHT context: both original F42 suffix paths may end at
different C60 darts while one genuine original F54 earlier
bracket-tree supplies the independent rotation-route context. -/
def c60F58RightAfterFaceChoice
    (hedge : B₀.edge = B₁.edge)
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrot : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    {u₀ u₁ : IcosahedralDart}
    (suffix₀ : Quiver.Path w₀ u₀)
    (suffix₁ : Quiver.Path w₁ u₁)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (earlier : OriginalF45BracketTree k l mc pc ma pa) :
    C60F47BoundaryPoint (c60F47WhiskerRight B₀ suffix₀ earlier) ⥤
      C60F47BoundaryPoint (c60F47WhiskerRight B₁ suffix₁ earlier) :=
  c60F56ContextMixedFunctor
    (c60F47WhiskerRight B₀ suffix₀ earlier)
    (c60F47WhiskerRight B₁ suffix₁ earlier)
    (by change B₀.edge = B₁.edge; exact hedge)
    (by
      calc
        c60F44FaceThreeEval
            (c60F47WhiskerRight B₀ suffix₀ earlier).faceStep =
          c60F44FaceThreeEval B₀.faceStep :=
            c60F45RightWhiskerGrayMap suffix₀ B₀.faceStep
        _ = c60F44FaceThreeEval B₁.faceStep := hface
        _ = c60F44FaceThreeEval
            (c60F47WhiskerRight B₁ suffix₁ earlier).faceStep :=
              (c60F45RightWhiskerGrayMap suffix₁ B₁.faceStep).symm)
    (by
      calc
        c60F44OriginalF55Eval
            (c60F47WhiskerRight B₀ suffix₀ earlier).rotationStep =
          c60F44OriginalF55Eval B₀.rotationStep :=
            c60F45F55RightContextGrayMap earlier B₀.rotationStep
        _ = c60F44OriginalF55Eval B₁.rotationStep := hrot
        _ = c60F44OriginalF55Eval
            (c60F47WhiskerRight B₁ suffix₁ earlier).rotationStep :=
              (c60F45F55RightContextGrayMap earlier B₁.rotationStep).symm)

/-- Dependent right-context boundary cast: proof-relevant source
tags are inspected before comparing the two actual F47 3-arrows. -/
def c60F58RightFaceContextHomCast
    (hedge : B₀.edge = B₁.edge)
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrot : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    {u₀ u₁ : IcosahedralDart}
    (suffix₀ : Quiver.Path w₀ u₀)
    (suffix₁ : Quiver.Path w₁ u₁)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (earlier : OriginalF45BracketTree k l mc pc ma pa)
    {X Y : C60F47BoundaryPoint B₀}
    (g :
      (c60F56OriginalRightMixedContextFunctor B₁ suffix₁ earlier).obj
        ((c60F56ContextMixedFunctor B₀ B₁ hedge hface hrot).obj X) ⟶
      (c60F56OriginalRightMixedContextFunctor B₁ suffix₁ earlier).obj
        ((c60F56ContextMixedFunctor B₀ B₁ hedge hface hrot).obj Y)) :
    (c60F58RightAfterFaceChoice B₀ B₁ hedge hface hrot suffix₀ suffix₁ earlier).obj
        ((c60F56OriginalRightMixedContextFunctor B₀ suffix₀ earlier).obj X) ⟶
    (c60F58RightAfterFaceChoice B₀ B₁ hedge hface hrot suffix₀ suffix₁ earlier).obj
        ((c60F56OriginalRightMixedContextFunctor B₀ suffix₀ earlier).obj Y) := by
  cases X <;> cases Y
  all_goals exact g

theorem c60F58RightFaceContext_BeckChevalley
    (hedge : B₀.edge = B₁.edge)
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrot : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    {u₀ u₁ : IcosahedralDart}
    (suffix₀ : Quiver.Path w₀ u₀)
    (suffix₁ : Quiver.Path w₁ u₁)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (earlier : OriginalF45BracketTree k l mc pc ma pa)
    {X Y : C60F47BoundaryPoint B₀} (f : X ⟶ Y) :
    (c60F58RightAfterFaceChoice B₀ B₁ hedge hface hrot
      suffix₀ suffix₁ earlier).map
      ((c60F56OriginalRightMixedContextFunctor B₀ suffix₀ earlier).map f) =
    c60F58RightFaceContextHomCast B₀ B₁ hedge hface hrot
      suffix₀ suffix₁ earlier
      ((c60F56OriginalRightMixedContextFunctor B₁ suffix₁ earlier).map
        ((c60F56ContextMixedFunctor B₀ B₁ hedge hface hrot).map f)) := by
  cases X <;> cases Y
  all_goals
    apply c60F47MixedGrayFunctor_faithful
      (c60F47WhiskerRight B₁ suffix₁ earlier)
    change c60F47MixedEval
        ((c60F58RightAfterFaceChoice B₀ B₁ hedge hface hrot
          suffix₀ suffix₁ earlier).map
          ((c60F56OriginalRightMixedContextFunctor
            B₀ suffix₀ earlier).map f)) =
      c60F47MixedEval
        ((c60F56OriginalRightMixedContextFunctor
          B₁ suffix₁ earlier).map
          ((c60F56ContextMixedFunctor B₀ B₁ hedge hface hrot).map f))
    simp only [c60F58RightAfterFaceChoice,
      c60F56OriginalRightMixedContextFunctor,
      c60F56ContextMixedFunctor_fullNative]

def c60F58RightFaceContext_NatIso
    (hedge : B₀.edge = B₁.edge)
    (hface : c60F44FaceThreeEval B₀.faceStep =
      c60F44FaceThreeEval B₁.faceStep)
    (hrot : c60F44OriginalF55Eval B₀.rotationStep =
      c60F44OriginalF55Eval B₁.rotationStep)
    {u₀ u₁ : IcosahedralDart}
    (suffix₀ : Quiver.Path w₀ u₀)
    (suffix₁ : Quiver.Path w₁ u₁)
    {k l : Nat} {mc : Blocks a b} {pc : Blocks x y}
    (earlier : OriginalF45BracketTree k l mc pc ma pa) :
    (c60F56OriginalRightMixedContextFunctor B₀ suffix₀ earlier) ⋙
      (c60F58RightAfterFaceChoice B₀ B₁ hedge hface hrot
        suffix₀ suffix₁ earlier) ≅
    (c60F56ContextMixedFunctor B₀ B₁ hedge hface hrot) ⋙
      (c60F56OriginalRightMixedContextFunctor B₁ suffix₁ earlier) :=
  NatIso.ofComponents
    (fun X => by cases X <;> exact Iso.refl _)
    (by
      intro X Y f
      cases X <;> cases Y
      all_goals
        calc
          _ = (c60F58RightAfterFaceChoice B₀ B₁ hedge hface hrot
                suffix₀ suffix₁ earlier).map
                ((c60F56OriginalRightMixedContextFunctor
                  B₀ suffix₀ earlier).map f) := Category.comp_id _
          _ = (c60F56OriginalRightMixedContextFunctor
                B₁ suffix₁ earlier).map
                ((c60F56ContextMixedFunctor
                  B₀ B₁ hedge hface hrot).map f) :=
              c60F58RightFaceContext_BeckChevalley B₀ B₁
                hedge hface hrot suffix₀ suffix₁ earlier f
          _ = _ := (Category.id_comp _).symm)

#print axioms c60F58LeftFaceContextHomCast
#print axioms c60F58RightFaceContextHomCast
#print axioms c60F58LeftAfterFaceChoice
#print axioms c60F58LeftFaceContext_BeckChevalley
#print axioms c60F58LeftFaceContext_NatIso
#print axioms c60F58RightAfterFaceChoice
#print axioms c60F58RightFaceContext_BeckChevalley
#print axioms c60F58RightFaceContext_NatIso

end GeneralActualOriginalContexts
end
end KUOS.DependentOriginationGrayC60F55OriginalContextBeckChevalleyV5_207
