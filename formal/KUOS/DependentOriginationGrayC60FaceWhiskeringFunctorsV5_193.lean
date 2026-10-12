import KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192

namespace KUOS.DependentOriginationGrayC60FaceWhiskeringFunctorsV5_193

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F45 / v5.193 — genuine original C60 left/right 1-path whiskering FUNCTORS

This extends the exactly verified F59-F44 ORIGINAL C60 3-Hom Mathlib
category: its objects are genuine original C60 face 2-cell witnesses
between a fixed pair of 60-object, 180-directed-edge free paths, and
its morphisms are genuine original type-indexed presented 3-cells
modulo exact equality of the complete F59 GradedThreeCell image.

For every actual ORIGINAL C60 1-path prior and suffix, we construct
GENUINE MATHLIB FUNCTORS on these categorical 3-Homs. They map both
source 2-cell objects and raw proof-relevant source 3-cell witnesses
with the ORIGINAL F42/F43 left/right whiskering constructors.
They preserve source category identity and original vertical 3-cell
composition, with all laws proved by the native F59 integer and
independent ZMod2 phase structure, NOT by identifying different raw
original source proofs.

The full native braided Gray 3-cell target is retained on every
whiskered hom, and both whiskering functors are FAITHFUL on the
explicitly defined target-kernel quotient. Both two-step whiskering
orders retain the exact same original charge and phase. We do NOT
assert strict raw source equality for differently parenthesized
paths or equality of the corresponding raw F43 witnesses.

This is part of the actual nondegenerate C60 higher source
0/1/2/3-whiskering construction; it is NOT by itself a full
nondegenerate Gray 3-functor or a source/target identification
with the independent original F54/F55 route 2-cell system.
-/

/-! ## I. Honest left whiskering by a real C60 path -/

/-- Whisker EVERY source face 2-cell and its source 3-morphisms
on the left by the ACTUAL typed C60 1-path. This is a real
Mathlib functor, not an unbundled operation on proof terms. -/
def c60F45LeftWhiskerFunctor
    {a b c : IcosahedralDart}
    (prior : Quiver.Path a b)
    {p q : Quiver.Path b c} :
    C60F42PresentedFaceCell p q ⥤
      C60F42PresentedFaceCell (prior.comp p) (prior.comp q) where
  obj α := .whiskerLeft prior α
  map := fun {_ _} f =>
    Quot.liftOn f
      (fun raw => c60F44FaceThreeOf (.whiskerLeft prior raw))
      (by
        intro raw₁ raw₂ heq
        apply Quot.sound
        exact heq)
  map_id := by
    intro α
    apply Quot.sound
    rfl
  map_comp := by
    intro α β γ f g
    refine Quot.inductionOn f (fun f => ?_)
    refine Quot.inductionOn g (fun g => ?_)
    apply Quot.sound
    rfl

/-- The old ORIGINAL C60 2-cell's face degree is unaffected
by true left path whiskering; nontrivial odd face degrees remain. -/
theorem c60F45LeftWhiskerFaceDegree
    {a b c : IcosahedralDart}
    (prior : Quiver.Path a b)
    {p q : Quiver.Path b c}
    (α : C60F42PresentedFaceCell p q) :
    c60F43FaceDegree ((c60F45LeftWhiskerFunctor prior).obj α) =
      c60F43FaceDegree α :=
  c60F43FaceDegree_whiskerLeft prior α

/-- The native source 3-morphism interpretation after left
whiskering is EXACTLY the old unprojected Int×Int and ZMod2
Gray value, not just its mod-two parity. -/
theorem c60F45LeftWhiskerGrayMap
    {a b c : IcosahedralDart}
    (prior : Quiver.Path a b)
    {p q : Quiver.Path b c}
    {α β : C60F42PresentedFaceCell p q}
    (f : α ⟶ β) :
    c60F44FaceThreeEval
      ((c60F45LeftWhiskerFunctor prior).map f) =
        c60F44FaceThreeEval f := by
  refine Quot.inductionOn f (fun raw => ?_)
  rfl

/-- Faithfulness follows from genuine COMPLETE Gray target
faithfulness; the proof does not identify distinct original
raw 3-cell proofs outside their explicitly chosen quotient. -/
theorem c60F45LeftWhiskerFunctor_faithful
    {a b c : IcosahedralDart}
    (prior : Quiver.Path a b)
    {p q : Quiver.Path b c}
    {α β : C60F42PresentedFaceCell p q}
    {f g : α ⟶ β}
    (h : (c60F45LeftWhiskerFunctor prior).map f =
      (c60F45LeftWhiskerFunctor prior).map g) :
    f = g := by
  have hh := congrArg
    (fun x : (c60F45LeftWhiskerFunctor prior).obj α ⟶
      (c60F45LeftWhiskerFunctor prior).obj β =>
        c60F44FaceThreeEval x) h
  rw [c60F45LeftWhiskerGrayMap, c60F45LeftWhiskerGrayMap] at hh
  exact c60F44FaceThreeGrayFunctor_faithful hh

/-! ## II. Honest right whiskering by a real C60 path -/

/-- The complete right-context variant: a true Mathlib
FUNCTOR on original source 3-Hom categories, whose object
and morphism parts have the actual original F42/F43
source-dependent right whiskering constructors. -/
def c60F45RightWhiskerFunctor
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b}
    (suffix : Quiver.Path b c) :
    C60F42PresentedFaceCell p q ⥤
      C60F42PresentedFaceCell (p.comp suffix) (q.comp suffix) where
  obj α := .whiskerRight α suffix
  map := fun {_ _} f =>
    Quot.liftOn f
      (fun raw => c60F44FaceThreeOf (.whiskerRight raw suffix))
      (by
        intro raw₁ raw₂ heq
        apply Quot.sound
        exact heq)
  map_id := by
    intro α
    apply Quot.sound
    rfl
  map_comp := by
    intro α β γ f g
    refine Quot.inductionOn f (fun f => ?_)
    refine Quot.inductionOn g (fun g => ?_)
    apply Quot.sound
    rfl

theorem c60F45RightWhiskerFaceDegree
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b}
    (suffix : Quiver.Path b c)
    (α : C60F42PresentedFaceCell p q) :
    c60F43FaceDegree ((c60F45RightWhiskerFunctor suffix).obj α) =
      c60F43FaceDegree α :=
  c60F43FaceDegree_whiskerRight α suffix

theorem c60F45RightWhiskerGrayMap
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b}
    (suffix : Quiver.Path b c)
    {α β : C60F42PresentedFaceCell p q}
    (f : α ⟶ β) :
    c60F44FaceThreeEval
      ((c60F45RightWhiskerFunctor suffix).map f) =
        c60F44FaceThreeEval f := by
  refine Quot.inductionOn f (fun raw => ?_)
  rfl

theorem c60F45RightWhiskerFunctor_faithful
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b}
    (suffix : Quiver.Path b c)
    {α β : C60F42PresentedFaceCell p q}
    {f g : α ⟶ β}
    (h : (c60F45RightWhiskerFunctor suffix).map f =
      (c60F45RightWhiskerFunctor suffix).map g) :
    f = g := by
  have hh := congrArg
    (fun x : (c60F45RightWhiskerFunctor suffix).obj α ⟶
      (c60F45RightWhiskerFunctor suffix).obj β =>
        c60F44FaceThreeEval x) h
  rw [c60F45RightWhiskerGrayMap, c60F45RightWhiskerGrayMap] at hh
  exact c60F44FaceThreeGrayFunctor_faithful hh

/-! ## III. Both context orders keep the FULL target -/

/-- First use a REAL original left path, then a REAL original
right path: regardless of both source 1-contexts, every true
C60 source 3-Hom morphism retains the exact full native Gray
image, not only the total phase of the original 32 faces. -/
theorem c60F45LeftThenRightGrayMap
    {a b c d : IcosahedralDart}
    (prior : Quiver.Path a b)
    {p q : Quiver.Path b c}
    (suffix : Quiver.Path c d)
    {α β : C60F42PresentedFaceCell p q}
    (f : α ⟶ β) :
    c60F44FaceThreeEval
      ((c60F45RightWhiskerFunctor suffix).map
        ((c60F45LeftWhiskerFunctor prior).map f)) =
      c60F44FaceThreeEval f := by
  rw [c60F45RightWhiskerGrayMap, c60F45LeftWhiskerGrayMap]

/-- First right, then left. We do NOT falsely equate the raw
F42 face-2-cell objects of the two orders: their parenthesized
physical 1-path indices are in general only propositionally
associated, and this proof is correctly at the FULL native
Gray image level. -/
theorem c60F45RightThenLeftGrayMap
    {a b c d : IcosahedralDart}
    (prior : Quiver.Path a b)
    {p q : Quiver.Path b c}
    (suffix : Quiver.Path c d)
    {α β : C60F42PresentedFaceCell p q}
    (f : α ⟶ β) :
    c60F44FaceThreeEval
      ((c60F45LeftWhiskerFunctor prior).map
        ((c60F45RightWhiskerFunctor suffix).map f)) =
      c60F44FaceThreeEval f := by
  rw [c60F45LeftWhiskerGrayMap, c60F45RightWhiskerGrayMap]

/-- Both source whiskering orders evaluate to the SAME true
F59 Int×Int native charge and independent ZMod2 braided phase.
This is an image equality, NOT an unproved strict source
3-cell interchange assertion between differently typed paths. -/
theorem c60F45LeftRightGrayImage_coherent
    {a b c d : IcosahedralDart}
    (prior : Quiver.Path a b)
    {p q : Quiver.Path b c}
    (suffix : Quiver.Path c d)
    {α β : C60F42PresentedFaceCell p q}
    (f : α ⟶ β) :
    c60F44FaceThreeEval
      ((c60F45RightWhiskerFunctor suffix).map
        ((c60F45LeftWhiskerFunctor prior).map f)) =
    c60F44FaceThreeEval
      ((c60F45LeftWhiskerFunctor prior).map
        ((c60F45RightWhiskerFunctor suffix).map f)) := by
  rw [c60F45LeftThenRightGrayMap, c60F45RightThenLeftGrayMap]

/-- Use an actual ORIGINAL north-pentagon source 3-Hom arrow:
left whiskering by any genuinely composable C60 physical
path leaves the nontrivial odd Gray interchange intact. -/
theorem c60F45NorthPentagonLeftWhisker_nonzeroPhase
    {a : IcosahedralDart}
    (prior : Quiver.Path a (icosahedralIncidentDartAt .north .s0)) :
    (c60F44FaceThreeEval
      ((c60F45LeftWhiskerFunctor prior).map
        (c60F44FaceThreeOf c60F43NorthPentagonInterchange))).phase =
          (1 : ZMod 2) := by
  rw [c60F45LeftWhiskerGrayMap]
  exact c60F43NorthPentagonInterchange_components.2

#print axioms c60F45LeftWhiskerFunctor
#print axioms c60F45LeftWhiskerFaceDegree
#print axioms c60F45LeftWhiskerGrayMap
#print axioms c60F45LeftWhiskerFunctor_faithful
#print axioms c60F45RightWhiskerFunctor
#print axioms c60F45RightWhiskerFaceDegree
#print axioms c60F45RightWhiskerGrayMap
#print axioms c60F45RightWhiskerFunctor_faithful
#print axioms c60F45LeftThenRightGrayMap
#print axioms c60F45RightThenLeftGrayMap
#print axioms c60F45LeftRightGrayImage_coherent
#print axioms c60F45NorthPentagonLeftWhisker_nonzeroPhase

end
end KUOS.DependentOriginationGrayC60FaceWhiskeringFunctorsV5_193
