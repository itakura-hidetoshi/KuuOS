import KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
import KUOS.DependentOriginationGrayC60AllNinetyEdgePastingV5_157

namespace KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192

open CategoryTheory
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayF55PhaseRealizationV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60F55SourcePhaseLockedAtlasV5_175
open KUOS.DependentOriginationGrayC60AllNinetyEdgePastingV5_157
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F44 / v5.192 — independent native category of original F55 higher cells

An actual original F54 DepthRotationRoute is the object (original
typed 2-morphism), and an actual F55 PresentedCell of all NINE
original constructors is a raw proof-relevant 3-cell between them.

Unlike a free source 3-cell presentation, this actual Mathlib
category has unit and associativity only after we quotient the
parallel raw proof witnesses by exact equality of their verified
native F59 Gray Int×Int charge AND ZMod2 exchange phase.
This quotient is named explicitly and raw original source
PresentedCells are preserved in the repository separately.
No new source 3-cell constructors or axioms are introduced.

The original F55 category admits an honest faithful functor
to the ALREADY PROVED true braided GrayGrade category.
The full original ninety physical C60 four-flag incidence
squares still carry genuine typed original F55 category
arrows with native square charge 1 and phase 1; the
C60 face-interchange has second charge zero instead.
The two different source globular 2-cell boundaries
remain separate. A genuine boundary-comparison higher
functor, not a phase-only analogy, is still needed for the
FULL NONDEGENERATE C60 Gray 3-functor.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section GenuineF55
variable {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : Blocks a b} {pa pb : Blocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}
variable {r s t : OriginalF45BracketTree.DepthRotationRoute first last}

/-- Exact target-kernel relation on original F55 parallel
proof-relevant 3-morphisms, conserving integer charge AND phase. -/
def c60F44OriginalF55Rel
    (f g : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    Prop := c60F55SourceNative f = c60F55SourceNative g

abbrev C60F44OriginalF55Hom
    (r s : OriginalF45BracketTree.DepthRotationRoute first last) : Type :=
  Quot (c60F44OriginalF55Rel (r := r) (s := s))

def c60F44OriginalF55Of
    (f : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    C60F44OriginalF55Hom r s :=
  Quot.mk _ f

def c60F44OriginalF55Eval
    (f : C60F44OriginalF55Hom r s) : GradedThreeCell 0 0 :=
  Quot.liftOn f (fun raw => c60F55SourceNative raw) (by
    intro left right h
    exact h)

@[simp] theorem c60F44OriginalF55Eval_of
    (f : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    c60F44OriginalF55Eval (c60F44OriginalF55Of f) =
      c60F55SourceNative f := rfl

/-- Genuine source vertical trans descends to the parallel
target-kernel quotient, preserving all F58/F59 coordinates. -/
def c60F44OriginalF55Comp
    (f : C60F44OriginalF55Hom r s)
    (g : C60F44OriginalF55Hom s t) :
    C60F44OriginalF55Hom r t :=
  Quot.liftOn₂ f g
    (fun left right => c60F44OriginalF55Of (.trans left right))
    (by
      intro left right₁ right₂ heq
      apply Quot.sound
      change (c60F55SourceNative left).comp
          (c60F55SourceNative right₁) =
        (c60F55SourceNative left).comp
          (c60F55SourceNative right₂)
      rw [heq])
    (by
      intro left₁ left₂ right heq
      apply Quot.sound
      change (c60F55SourceNative left₁).comp
          (c60F55SourceNative right) =
        (c60F55SourceNative left₂).comp
          (c60F55SourceNative right)
      rw [heq])

theorem c60F44OriginalF55Eval_comp
    (f : C60F44OriginalF55Hom r s)
    (g : C60F44OriginalF55Hom s t) :
    c60F44OriginalF55Eval (c60F44OriginalF55Comp f g) =
      (c60F44OriginalF55Eval f).comp
        (c60F44OriginalF55Eval g) := by
  refine Quot.inductionOn f (fun f => ?_)
  refine Quot.inductionOn g (fun g => ?_)
  rfl

/-- Full categorical 3-Hom category of original F54/F55,
strictly retaining exact original parallel source routes.
The honest native Gray-kernel quotient supplies all laws. -/
instance c60F44OriginalF55Category :
    Category (OriginalF45BracketTree.DepthRotationRoute first last) where
  Hom := C60F44OriginalF55Hom
  id route := c60F44OriginalF55Of (.ident route)
  comp := c60F44OriginalF55Comp
  id_comp := by
    intro X Y f
    refine Quot.inductionOn f (fun f => ?_)
    apply Quot.sound
    change (GradedThreeCell.ident 0).comp
        (c60F55SourceNative f) = c60F55SourceNative f
    exact GradedThreeCell.ident_comp _
  comp_id := by
    intro X Y f
    refine Quot.inductionOn f (fun f => ?_)
    apply Quot.sound
    change (c60F55SourceNative f).comp
        (GradedThreeCell.ident 0) = c60F55SourceNative f
    exact GradedThreeCell.comp_ident _
  assoc := by
    intro W X Y Z f g h
    refine Quot.inductionOn f (fun f => ?_)
    refine Quot.inductionOn g (fun g => ?_)
    refine Quot.inductionOn h (fun h => ?_)
    apply Quot.sound
    change ((c60F55SourceNative f).comp
        (c60F55SourceNative g)).comp (c60F55SourceNative h) =
      (c60F55SourceNative f).comp
        ((c60F55SourceNative g).comp (c60F55SourceNative h))
    exact GradedThreeCell.comp_assoc _ _ _

/-- True Mathlib faithful F55 original higher-source functor
into the SAME braided GrayGrade category as original C60
face-three-cell source functor, full F58 integer and
independent F59 phase intact. -/
def c60F44OriginalF55GrayFunctor :
    (OriginalF45BracketTree.DepthRotationRoute first last) ⥤
      GrayGrade where
  obj _ := GrayGrade.unit
  map := fun {_ _} f => c60F44OriginalF55Eval f
  map_id := by
    intro route
    change c60F55SourceNative
      (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.ident route) =
        (𝟙 GrayGrade.unit : GrayGrade.unit ⟶ GrayGrade.unit)
    exact c60F55SourceNative_ident route
  map_comp := by
    intro r s t f g
    change c60F44OriginalF55Eval (c60F44OriginalF55Comp f g) =
      (c60F44OriginalF55Eval f ≫ c60F44OriginalF55Eval g :
        GrayGrade.unit ⟶ GrayGrade.unit)
    exact c60F44OriginalF55Eval_comp f g

theorem c60F44OriginalF55GrayFunctor_faithful
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    {f g : r ⟶ s}
    (heq : c60F44OriginalF55GrayFunctor.map f =
      c60F44OriginalF55GrayFunctor.map g) : f = g := by
  change c60F44OriginalF55Eval f = c60F44OriginalF55Eval g at heq
  revert heq
  refine Quot.inductionOn f (fun raw₁ => ?_)
  refine Quot.inductionOn g (fun raw₂ hh => ?_)
  exact Quot.sound hh

end GenuineF55

/-- The genuine original independent F55 disjoint-rotation
square is a 3-morphism in its OWN exact typed source category.
It realizes exactly original native square integer charge ONE
and independent Gray phase ONE; its actual source and target
are specific original F54 bracket-tree routes. -/
theorem c60F44GenuineF55Square_categorical_components
    {a b : D} {x y : E}
    {n₁ n₂ m₁ m₂ : Nat}
    {p₀ p₁ p₂ : Blocks a b} {q₀ q₁ q₂ : Blocks x y}
    {t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁}
    {t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂}
    {leftAfter : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁}
    {rightAfter : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂}
    (left : OriginalF45BracketTree.LocalRotation t₁ leftAfter)
    (right : OriginalF45BracketTree.LocalRotation t₂ rightAfter) :
    (c60F44OriginalF55GrayFunctor.map
      (c60F44OriginalF55Of
        (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.disjointSquare
          left right))).charge = ((0 : Int), (1 : Int)) ∧
    (c60F44OriginalF55GrayFunctor.map
      (c60F44OriginalF55Of
        (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.disjointSquare
          left right))).phase = (1 : ZMod 2) := by
  exact originalF55BraidedSquareGenerator_complete

/-- Across all NINETY genuine original C60 edges, the actual
four-flag F55 source square is categorically realizable
with precisely the same native F58 integer charge and
Gray exchange phase. This does NOT substitute 4-flag
squares for 4-edge C60 faces. -/
theorem c60F44All90OriginalF55FlagSquares_categorical
    {a b : D} {x y : E}
    {n₁ n₂ m₁ m₂ : Nat}
    {p₀ p₁ p₂ : Blocks a b} {q₀ q₁ q₂ : Blocks x y}
    (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
    {leftAfter : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁}
    {rightAfter : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂}
    (left : OriginalF45BracketTree.LocalRotation t₁ leftAfter)
    (right : OriginalF45BracketTree.LocalRotation t₂ rightAfter)
    (edge : TruncatedIcosahedralEdge) :
    ∃ f :
      (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right) ⟶
        (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right),
      c60F44OriginalF55GrayFunctor.map f =
        c60AllNinetyGrayCell t₁ t₂ left right edge := by
  obtain ⟨cell, hcell⟩ :=
    c60F43AllNinetyPhysicalFlags_haveGenuineF55Square
      t₁ t₂ left right edge
  exact ⟨c60F44OriginalF55Of cell, hcell⟩

/-- The authentic original F55 categorical square image is NOT
the independent C60 face-interchange categorical image:
the latter has zero independent F58 square charge, while
the former has square charge 1. This is the precise
remaining source 2-cell boundary compatibility obstruction. -/
theorem c60F44OriginalF55Square_ne_C60FaceInterchanger
    {a b : D} {x y : E}
    {n₁ n₂ m₁ m₂ : Nat}
    {p₀ p₁ p₂ : Blocks a b} {q₀ q₁ q₂ : Blocks x y}
    {t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁}
    {t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂}
    {leftAfter : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁}
    {rightAfter : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂}
    (left : OriginalF45BracketTree.LocalRotation t₁ leftAfter)
    (right : OriginalF45BracketTree.LocalRotation t₂ rightAfter) :
    c60F44OriginalF55GrayFunctor.map
      (c60F44OriginalF55Of
        (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.disjointSquare
          left right)) ≠
    c60F44FaceThreeGrayFunctor.map
      (c60F44FaceThreeOf c60F43NorthPentagonInterchange) := by
  intro h
  have hc := congrArg
    (fun x : GradedThreeCell 0 0 => x.charge.2) h
  have hone := (c60F44GenuineF55Square_categorical_components left right).1
  have hzero := c60F43NorthPentagonInterchange_components.1
  change (1 : Int) = (0 : Int) at hc
  exact (by decide : (1 : Int) ≠ 0) hc

#print axioms c60F44OriginalF55Eval_comp
#print axioms c60F44OriginalF55Category
#print axioms c60F44OriginalF55GrayFunctor
#print axioms c60F44OriginalF55GrayFunctor_faithful
#print axioms c60F44GenuineF55Square_categorical_components
#print axioms c60F44All90OriginalF55FlagSquares_categorical
#print axioms c60F44OriginalF55Square_ne_C60FaceInterchanger

end
end KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
