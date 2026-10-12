import KUOS.DependentOriginationGrayC60FaceWhiskeringFunctorsV5_193

namespace KUOS.DependentOriginationGrayC60OriginalF55WhiskeringV5_193

open CategoryTheory
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayF55PhaseRealizationV5_156
open KUOS.DependentOriginationGrayC60F55SourcePhaseLockedAtlasV5_175
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F45 / v5.193 — ALL original F54/F55 source 3-Hom whiskering FUNCTORS

F59-F44 constructed a genuine Mathlib category of the ORIGINAL
proof-relevant F54 DepthRotationRoute objects and F55 PresentedCell
3-morphisms modulo ONLY their independent full native Gray image.
The source has all NINE original constructors (pentagon, independent
square, identity, inverse, composition and FOUR original contexts).

This file proves, rather than assumes, that ALL FOUR original F55
contextual operations lift to honest Mathlib FUNCTORS between the
correct dependent source 3-Hom categories:
  1. leftContext with an original later F45 bracket tree;
  2. rightContext with an original earlier F45 bracket tree;
  3. precompose by an exact original F54 DepthRotationRoute;
  4. postcompose by an exact original F54 DepthRotationRoute.

Each functor acts on both original typed F54 source 2-cell objects
and original F55 3-cell witnesses. Each functor's identity,
vertical composition, complete native F58 integer charge and
independent ZMod2 exchange phase are proved preserved. All four
functors are FAITHFUL on the exact original target-kernel quotient.

This yields the next real piece of the original C60↔F55 higher
bridge: original C60 face-3-Hom whiskerings and original F54/F55
route-3-Hom whiskerings exist on BOTH sides as actual verified
functors into the SAME native GrayGrade category. However their
globular source 2-cell boundaries are still distinct, and merely
having corresponding functors does not fabricate a global
nondegenerate Gray 3-functor or identify original raw source proofs.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-! ## I. Context by an original later F45 bracket-tree -/

section LaterContext
variable {a b : D} {x y : E}
variable {n n' m m' k l : Nat}
variable {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}

/-- Exactly the ORIGINAL leftContext F54/F55 constructors,
now in a Mathlib Functor on the fully typed F55 3-Hom. -/
def c60F45F55LeftContextFunctor
    (later : OriginalF45BracketTree k l mb pb mc pc) :
    (OriginalF45BracketTree.DepthRotationRoute first last) ⥤
      (OriginalF45BracketTree.DepthRotationRoute
        (OriginalF45BracketTree.node first later)
        (OriginalF45BracketTree.node last later)) where
  obj route := .leftContext route later
  map := fun {_ _} f =>
    Quot.liftOn f
      (fun raw => c60F44OriginalF55Of (.leftContext raw later))
      (by
        intro raw₁ raw₂ heq
        apply Quot.sound
        exact heq)
  map_id := by
    intro route
    apply Quot.sound
    rfl
  map_comp := by
    intro r s t f g
    refine Quot.inductionOn f (fun f => ?_)
    refine Quot.inductionOn g (fun g => ?_)
    apply Quot.sound
    rfl

/-- Full independent Gray charge and phase survive original
F55 left tree context, not merely an integer/parity projection. -/
theorem c60F45F55LeftContextGrayMap
    (later : OriginalF45BracketTree k l mb pb mc pc)
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    (f : r ⟶ s) :
    c60F44OriginalF55Eval
      ((c60F45F55LeftContextFunctor later).map f) =
      c60F44OriginalF55Eval f := by
  refine Quot.inductionOn f (fun raw => ?_)
  rfl

/-- Faithfulness is on the ACTUAL original F55 target-kernel
quotient, without asserting raw proof irrelevance. -/
theorem c60F45F55LeftContext_faithful
    (later : OriginalF45BracketTree k l mb pb mc pc)
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    {f g : r ⟶ s}
    (h : (c60F45F55LeftContextFunctor later).map f =
      (c60F45F55LeftContextFunctor later).map g) : f = g := by
  have hh := congrArg
    (fun x : (c60F45F55LeftContextFunctor later).obj r ⟶
      (c60F45F55LeftContextFunctor later).obj s =>
      c60F44OriginalF55Eval x) h
  rw [c60F45F55LeftContextGrayMap,
    c60F45F55LeftContextGrayMap] at hh
  exact c60F44OriginalF55GrayFunctor_faithful hh

end LaterContext

/-! ## II. Context by an original earlier F45 bracket-tree -/

section EarlierContext
variable {a b : D} {x y : E}
variable {k l n n' m m' : Nat}
variable {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
variable {first : OriginalF45BracketTree n m mb pb mc pc}
variable {last : OriginalF45BracketTree n' m' mb pb mc pc}

def c60F45F55RightContextFunctor
    (earlier : OriginalF45BracketTree k l ma pa mb pb) :
    (OriginalF45BracketTree.DepthRotationRoute first last) ⥤
      (OriginalF45BracketTree.DepthRotationRoute
        (OriginalF45BracketTree.node earlier first)
        (OriginalF45BracketTree.node earlier last)) where
  obj route := .rightContext earlier route
  map := fun {_ _} f =>
    Quot.liftOn f
      (fun raw => c60F44OriginalF55Of (.rightContext earlier raw))
      (by
        intro raw₁ raw₂ heq
        apply Quot.sound
        exact heq)
  map_id := by
    intro route
    apply Quot.sound
    rfl
  map_comp := by
    intro r s t f g
    refine Quot.inductionOn f (fun f => ?_)
    refine Quot.inductionOn g (fun g => ?_)
    apply Quot.sound
    rfl

theorem c60F45F55RightContextGrayMap
    (earlier : OriginalF45BracketTree k l ma pa mb pb)
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    (f : r ⟶ s) :
    c60F44OriginalF55Eval
      ((c60F45F55RightContextFunctor earlier).map f) =
      c60F44OriginalF55Eval f := by
  refine Quot.inductionOn f (fun raw => ?_)
  rfl

theorem c60F45F55RightContext_faithful
    (earlier : OriginalF45BracketTree k l ma pa mb pb)
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    {f g : r ⟶ s}
    (h : (c60F45F55RightContextFunctor earlier).map f =
      (c60F45F55RightContextFunctor earlier).map g) : f = g := by
  have hh := congrArg
    (fun x : (c60F45F55RightContextFunctor earlier).obj r ⟶
      (c60F45F55RightContextFunctor earlier).obj s =>
      c60F44OriginalF55Eval x) h
  rw [c60F45F55RightContextGrayMap,
    c60F45F55RightContextGrayMap] at hh
  exact c60F44OriginalF55GrayFunctor_faithful hh

end EarlierContext

/-! ## III. Original F54 route precomposition -/

section Precomposition
variable {a b : D} {x y : E}
variable {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
variable {ma mb : Blocks a b} {pa pb : Blocks x y}
variable {first : OriginalF45BracketTree n₁ m₁ ma pa mb pb}
variable {middle : OriginalF45BracketTree n₂ m₂ ma pa mb pb}
variable {last : OriginalF45BracketTree n₃ m₃ ma pa mb pb}

def c60F45F55PrecomposeFunctor
    (priorRoute : OriginalF45BracketTree.DepthRotationRoute first middle) :
    (OriginalF45BracketTree.DepthRotationRoute middle last) ⥤
      (OriginalF45BracketTree.DepthRotationRoute first last) where
  obj route := .trans priorRoute route
  map := fun {_ _} f =>
    Quot.liftOn f
      (fun raw => c60F44OriginalF55Of (.precompose priorRoute raw))
      (by
        intro raw₁ raw₂ heq
        apply Quot.sound
        exact heq)
  map_id := by
    intro route
    apply Quot.sound
    rfl
  map_comp := by
    intro r s t f g
    refine Quot.inductionOn f (fun f => ?_)
    refine Quot.inductionOn g (fun g => ?_)
    apply Quot.sound
    rfl

theorem c60F45F55PrecomposeGrayMap
    (priorRoute : OriginalF45BracketTree.DepthRotationRoute first middle)
    {r s : OriginalF45BracketTree.DepthRotationRoute middle last}
    (f : r ⟶ s) :
    c60F44OriginalF55Eval
      ((c60F45F55PrecomposeFunctor priorRoute).map f) =
      c60F44OriginalF55Eval f := by
  refine Quot.inductionOn f (fun raw => ?_)
  rfl

theorem c60F45F55Precompose_faithful
    (priorRoute : OriginalF45BracketTree.DepthRotationRoute first middle)
    {r s : OriginalF45BracketTree.DepthRotationRoute middle last}
    {f g : r ⟶ s}
    (h : (c60F45F55PrecomposeFunctor priorRoute).map f =
      (c60F45F55PrecomposeFunctor priorRoute).map g) : f = g := by
  have hh := congrArg
    (fun x : (c60F45F55PrecomposeFunctor priorRoute).obj r ⟶
      (c60F45F55PrecomposeFunctor priorRoute).obj s =>
      c60F44OriginalF55Eval x) h
  rw [c60F45F55PrecomposeGrayMap,
    c60F45F55PrecomposeGrayMap] at hh
  exact c60F44OriginalF55GrayFunctor_faithful hh

end Precomposition

/-! ## IV. Original F54 route postcomposition -/

section Postcomposition
variable {a b : D} {x y : E}
variable {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
variable {ma mb : Blocks a b} {pa pb : Blocks x y}
variable {first : OriginalF45BracketTree n₁ m₁ ma pa mb pb}
variable {middle : OriginalF45BracketTree n₂ m₂ ma pa mb pb}
variable {last : OriginalF45BracketTree n₃ m₃ ma pa mb pb}

def c60F45F55PostcomposeFunctor
    (suffix : OriginalF45BracketTree.DepthRotationRoute middle last) :
    (OriginalF45BracketTree.DepthRotationRoute first middle) ⥤
      (OriginalF45BracketTree.DepthRotationRoute first last) where
  obj route := .trans route suffix
  map := fun {_ _} f =>
    Quot.liftOn f
      (fun raw => c60F44OriginalF55Of (.postcompose raw suffix))
      (by
        intro raw₁ raw₂ heq
        apply Quot.sound
        exact heq)
  map_id := by
    intro route
    apply Quot.sound
    rfl
  map_comp := by
    intro r s t f g
    refine Quot.inductionOn f (fun f => ?_)
    refine Quot.inductionOn g (fun g => ?_)
    apply Quot.sound
    rfl

theorem c60F45F55PostcomposeGrayMap
    (suffix : OriginalF45BracketTree.DepthRotationRoute middle last)
    {r s : OriginalF45BracketTree.DepthRotationRoute first middle}
    (f : r ⟶ s) :
    c60F44OriginalF55Eval
      ((c60F45F55PostcomposeFunctor suffix).map f) =
      c60F44OriginalF55Eval f := by
  refine Quot.inductionOn f (fun raw => ?_)
  rfl

theorem c60F45F55Postcompose_faithful
    (suffix : OriginalF45BracketTree.DepthRotationRoute middle last)
    {r s : OriginalF45BracketTree.DepthRotationRoute first middle}
    {f g : r ⟶ s}
    (h : (c60F45F55PostcomposeFunctor suffix).map f =
      (c60F45F55PostcomposeFunctor suffix).map g) : f = g := by
  have hh := congrArg
    (fun x : (c60F45F55PostcomposeFunctor suffix).obj r ⟶
      (c60F45F55PostcomposeFunctor suffix).obj s =>
      c60F44OriginalF55Eval x) h
  rw [c60F45F55PostcomposeGrayMap,
    c60F45F55PostcomposeGrayMap] at hh
  exact c60F44OriginalF55GrayFunctor_faithful hh

end Postcomposition

#print axioms c60F45F55LeftContextFunctor
#print axioms c60F45F55LeftContextGrayMap
#print axioms c60F45F55LeftContext_faithful
#print axioms c60F45F55RightContextFunctor
#print axioms c60F45F55RightContextGrayMap
#print axioms c60F45F55RightContext_faithful
#print axioms c60F45F55PrecomposeFunctor
#print axioms c60F45F55PrecomposeGrayMap
#print axioms c60F45F55Precompose_faithful
#print axioms c60F45F55PostcomposeFunctor
#print axioms c60F45F55PostcomposeGrayMap
#print axioms c60F45F55Postcompose_faithful

end
end KUOS.DependentOriginationGrayC60OriginalF55WhiskeringV5_193
