import KUOS.DependentOriginationCoherentBiadjunctionOriginalF45ConditionalHigherCellTargetV5_153

namespace KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F56-B / v5.153 — strict target paste/whisker compatibility and count no-go

The F56-A conditional higher-cell interpreter sends the genuine
Type-valued original F55 pentagon and disjoint-context square to
SEPARATELY SUPPLIED cells in a chosen target family. We verify here
its four context/pasting equations, holding with EXACT original typed
F19/F28 indices. These are definitional consequences of the F55
inductive cell constructors, not postulated tricategorical 3-cell laws.

There is also a real obstruction. The honest F55 pentagon relates a
three-rotation witness to a two-rotation witness. Therefore NO such
higher-cell target may globally assert that *each* supplied target
cell preserves the literal number of individual F54 rotations,
whenever the required four concrete original F45 subtrees exist.

The obstruction is not a missing Lean proof: 3 != 2, and we keep
the raw routes distinct while allowing a presented higher comparison.
-/

universe uD vD uE vE uH
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- The target interpretation preserves actual left contextual
whiskering of a freely presented higher F55 cell without erasing its
original Type-valued path evidence. -/
theorem OriginalF45BracketTree.DepthRotationRoute.PresentedCell.interpret_leftContext
    (target : OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget D E)
    {a b : D} {x y : E} {n n' m m' k l : Nat}
    {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    (cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s)
    (later : OriginalF45BracketTree k l mb pb mc pc) :
    (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.leftContext
      cell later).interpret target =
      target.leftContext (cell.interpret target) later :=
  rfl

/-- The right contextual original F45 whiskering, independently of
the F19/F28 source-tree depths, commutes with conditional semantics. -/
theorem OriginalF45BracketTree.DepthRotationRoute.PresentedCell.interpret_rightContext
    (target : OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget D E)
    {a b : D} {x y : E} {k l n n' m m' : Nat}
    {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
    (earlier : OriginalF45BracketTree k l ma pa mb pb)
    {first : OriginalF45BracketTree n m mb pb mc pc}
    {last : OriginalF45BracketTree n' m' mb pb mc pc}
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    (cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.rightContext
      earlier cell).interpret target =
      target.rightContext earlier (cell.interpret target) :=
  rfl

/-- Pasting a fixed actual original depth-aware route BEFORE the
cell respects the independently supplied target precomposition map. -/
theorem OriginalF45BracketTree.DepthRotationRoute.PresentedCell.interpret_precompose
    (target : OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget D E)
    {a b : D} {x y : E} {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n₁ m₁ ma pa mb pb}
    {middle : OriginalF45BracketTree n₂ m₂ ma pa mb pb}
    {last : OriginalF45BracketTree n₃ m₃ ma pa mb pb}
    (priorRoute : OriginalF45BracketTree.DepthRotationRoute first middle)
    {r s : OriginalF45BracketTree.DepthRotationRoute middle last}
    (cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.precompose
      priorRoute cell).interpret target =
      target.precompose priorRoute (cell.interpret target) :=
  rfl

/-- Pasting an actual original route AFTER the cell respects the
independently supplied target postcomposition operation. -/
theorem OriginalF45BracketTree.DepthRotationRoute.PresentedCell.interpret_postcompose
    (target : OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget D E)
    {a b : D} {x y : E} {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n₁ m₁ ma pa mb pb}
    {middle : OriginalF45BracketTree n₂ m₂ ma pa mb pb}
    {last : OriginalF45BracketTree n₃ m₃ ma pa mb pb}
    {r s : OriginalF45BracketTree.DepthRotationRoute first middle}
    (cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s)
    (suffix : OriginalF45BracketTree.DepthRotationRoute middle last) :
    (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.postcompose
      cell suffix).interpret target =
      target.postcompose (cell.interpret target) suffix :=
  rfl

/-- A chosen target's interpretation of the F55 identity witness
is EXACTLY its independently supplied higher identity cell. -/
theorem OriginalF45BracketTree.DepthRotationRoute.PresentedCell.interpret_ident
    (target : OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget D E)
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    (route : OriginalF45BracketTree.DepthRotationRoute first last) :
    (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.ident
      route).interpret target = target.ident route :=
  rfl

/-- There is NO possible global count-preserving interpretation of all
F55 presented higher comparisons in a separately supplied target
which realizes the ACTUAL five-vertex pentagon. The concrete
three-step path and concrete two-step path share endpoints but have
different lengths, and the target pentagon relates them.

This is a no-go under the explicit presence of four composable
original F45 trees; it does not claim the external target itself is
inconsistent or that it lacks a non-count-preserving interpretation. -/
theorem OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.no_global_rotationCount
    (target : OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget D E)
    {a b : D} {x y : E}
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    {p₀ p₁ p₂ p₃ p₄ : Blocks a b}
    {q₀ q₁ q₂ q₃ q₄ : Blocks x y}
    (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : OriginalF45BracketTree n₃ m₃ p₂ q₂ p₃ q₃)
    (t₄ : OriginalF45BracketTree n₄ m₄ p₃ q₃ p₄ q₄)
    (count_preserving :
      ∀ {a b : D} {x y : E} {n n' m m' : Nat}
        {ma mb : Blocks a b} {pa pb : Blocks x y}
        {first : OriginalF45BracketTree n m ma pa mb pb}
        {last : OriginalF45BracketTree n' m' ma pa mb pb}
        {r s : OriginalF45BracketTree.DepthRotationRoute first last},
        target.Cell r s → r.rotationCount = s.rotationCount) : False := by
  have h :=
    count_preserving (target.pentagon t₁ t₂ t₃ t₄)
  have h32 : (3 : Nat) = 2 := by
    simpa only [
      OriginalF45BracketTree.DepthRotationRoute.pentagonLong_rotationCount,
      OriginalF45BracketTree.DepthRotationRoute.pentagonShort_rotationCount
    ] using h
  exact (by decide : (3 : Nat) ≠ 2) h32

#print axioms OriginalF45BracketTree.DepthRotationRoute.PresentedCell.interpret_leftContext
#print axioms OriginalF45BracketTree.DepthRotationRoute.PresentedCell.interpret_rightContext
#print axioms OriginalF45BracketTree.DepthRotationRoute.PresentedCell.interpret_precompose
#print axioms OriginalF45BracketTree.DepthRotationRoute.PresentedCell.interpret_postcompose
#print axioms OriginalF45BracketTree.DepthRotationRoute.PresentedCell.interpret_ident
#print axioms OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.no_global_rotationCount

end
end KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
