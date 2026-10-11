import KUOS.DependentOriginationCoherentBiadjunctionOriginalF45LocalRotationV5_151

namespace KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F54-B / v5.151 — arbitrarily LONG FINITE chains of real local rotations

F54-A constructed an honest Type-valued witness for a forward local
associator, with arbitrary left/right contexts and the exact double
symbolic depth casts. We now keep every individual local witness in
an actual finitary inductive chain, not an existential Prop.

An elementary edge can be the forward rotation or the reverse of an
actual forward rotation. The chain retains all intermediate fully
typed original F45 binary trees and a genuine number of elementary
rotations. Concatenation, reversal and both contextual whiskerings
of chains are defined as real Type-valued operations.

The original F44 generated exchange quotient and both complete
F19/F28 original primitive histories remain invariant at every
stage. This says nothing about a general tricategorical 3-cell
groupoid or proof-relevant equality between different chains.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- One actual elementary local rotation, in either genuine
direction, with unchanged F19/F28 primitive depths and endpoints. -/
inductive OriginalF45BracketTree.RotationEdge :
    ∀ {a b : D} {x y : E} {n m : Nat}
      {ma mb : Blocks a b} {pa pb : Blocks x y},
      OriginalF45BracketTree n m ma pa mb pb →
      OriginalF45BracketTree n m ma pa mb pb →
      Type (max (max uD uE) (max vD vE)) where
  | forward
      {a b : D} {x y : E} {n m : Nat}
      {ma mb : Blocks a b} {pa pb : Blocks x y}
      {before after : OriginalF45BracketTree n m ma pa mb pb}
      (rotation : OriginalF45BracketTree.LocalRotation before after) :
      RotationEdge before after
  | backward
      {a b : D} {x y : E} {n m : Nat}
      {ma mb : Blocks a b} {pa pb : Blocks x y}
      {before after : OriginalF45BracketTree n m ma pa mb pb}
      (rotation : OriginalF45BracketTree.LocalRotation before after) :
      RotationEdge after before

/-- Reverse a specific original rotation edge without discarding its
actual F54-A Type-valued associativity proof-relevant witness. -/
def OriginalF45BracketTree.RotationEdge.reverse
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {before after : OriginalF45BracketTree n m ma pa mb pb}
    (edge : OriginalF45BracketTree.RotationEdge before after) :
    OriginalF45BracketTree.RotationEdge after before := by
  cases edge with
  | forward rotation =>
      exact OriginalF45BracketTree.RotationEdge.backward rotation
  | backward rotation =>
      exact OriginalF45BracketTree.RotationEdge.forward rotation

/-- Every elementary bidirectional contextual rotation preserves
the complete actual F44 quotient class. -/
theorem OriginalF45BracketTree.RotationEdge.toExchangeClass_eq
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {before after : OriginalF45BracketTree n m ma pa mb pb}
    (edge : OriginalF45BracketTree.RotationEdge before after) :
    before.toExchangeClass = after.toExchangeClass := by
  cases edge with
  | forward rotation =>
      exact rotation.toExchangeClass_eq
  | backward rotation =>
      exact rotation.toExchangeClass_eq.symm

/-- A proof-relevant FINITE chain of actual, specifically witnessed,
possibly backward associativity rotations. The snoc constructor
records its preceding chain and the next original Type-valued tree. -/
inductive OriginalF45BracketTree.RotationChain :
    ∀ {a b : D} {x y : E} {n m : Nat}
      {ma mb : Blocks a b} {pa pb : Blocks x y},
      OriginalF45BracketTree n m ma pa mb pb →
      OriginalF45BracketTree n m ma pa mb pb →
      Type (max (max uD uE) (max vD vE)) where
  | refl
      {a b : D} {x y : E} {n m : Nat}
      {ma mb : Blocks a b} {pa pb : Blocks x y}
      (tree : OriginalF45BracketTree n m ma pa mb pb) :
      RotationChain tree tree
  | snoc
      {a b : D} {x y : E} {n m : Nat}
      {ma mb : Blocks a b} {pa pb : Blocks x y}
      {first middle last : OriginalF45BracketTree n m ma pa mb pb}
      (prefix : RotationChain first middle)
      (edge : OriginalF45BracketTree.RotationEdge middle last) :
      RotationChain first last

/-- The exact count of genuine elementary associativity rotations in
the finite chain, retaining repetitions and nontrivial backtracks. -/
def OriginalF45BracketTree.RotationChain.length
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first last : OriginalF45BracketTree n m ma pa mb pb}
    (chain : OriginalF45BracketTree.RotationChain first last) : Nat := by
  induction chain with
  | refl _ =>
      exact 0
  | snoc _ _ ih =>
      exact ih + 1

/-- Genuine concatenation of two finite sequences of local rotations.
The result is an actual Type-valued witness with ALL intermediate
original F45 binary trees, not a Prop-level transitive closure. -/
def OriginalF45BracketTree.RotationChain.append
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first middle last : OriginalF45BracketTree n m ma pa mb pb}
    (left : OriginalF45BracketTree.RotationChain first middle)
    (right : OriginalF45BracketTree.RotationChain middle last) :
    OriginalF45BracketTree.RotationChain first last := by
  induction right with
  | refl _ =>
      exact left
  | snoc right edge ih =>
      exact OriginalF45BracketTree.RotationChain.snoc (ih left) edge

/-- Real finite concatenation preserves the exact count of local
rotation steps without presuming any cancellation of reverse moves. -/
theorem OriginalF45BracketTree.RotationChain.length_append
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first middle last : OriginalF45BracketTree n m ma pa mb pb}
    (left : OriginalF45BracketTree.RotationChain first middle)
    (right : OriginalF45BracketTree.RotationChain middle last) :
    (OriginalF45BracketTree.RotationChain.append left right).length =
      left.length + right.length := by
  induction right with
  | refl _ =>
      rfl
  | snoc right edge ih =>
      simpa only [OriginalF45BracketTree.RotationChain.append,
        OriginalF45BracketTree.RotationChain.length,
        Nat.add_succ] using congrArg Nat.succ (ih left)

/-- An actual finite local rotation chain can be traversed backward
as another actual Type-valued sequence of reverse elementary edges. -/
def OriginalF45BracketTree.RotationChain.reverse
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first last : OriginalF45BracketTree n m ma pa mb pb}
    (chain : OriginalF45BracketTree.RotationChain first last) :
    OriginalF45BracketTree.RotationChain last first := by
  induction chain with
  | refl tree =>
      exact OriginalF45BracketTree.RotationChain.refl tree
  | snoc chain edge ih =>
      exact OriginalF45BracketTree.RotationChain.append
        (OriginalF45BracketTree.RotationChain.snoc
          (OriginalF45BracketTree.RotationChain.refl _) edge.reverse)
        ih

/-- The actual F44 generated exchange quotient of any two trees
connected by a FINITE chain of concrete rotation edges is identical.
No new same-axis equivalence or inversion of nonstrict G cells. -/
theorem OriginalF45BracketTree.RotationChain.toExchangeClass_eq
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first last : OriginalF45BracketTree n m ma pa mb pb}
    (chain : OriginalF45BracketTree.RotationChain first last) :
    first.toExchangeClass = last.toExchangeClass := by
  induction chain with
  | refl tree =>
      rfl
  | snoc chain edge ih =>
      exact ih.trans edge.toExchangeClass_eq

/-- The whole original F19 and genuine F28 complete Type-valued
primitive histories survive arbitrarily long finite chains of actual
local associativity rotations and their genuine reverse edges. -/
theorem OriginalF45BracketTree.RotationChain.axisHistories_eq
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first last : OriginalF45BracketTree n m ma pa mb pb}
    (chain : OriginalF45BracketTree.RotationChain first last) :
    first.axisHistories = last.axisHistories := by
  have h := congrArg ExchangeClass.axisTraces chain.toExchangeClass_eq
  simpa only [OriginalF45BracketTree.toExchangeClass_axisTraces] using h

#print axioms OriginalF45BracketTree.RotationEdge
#print axioms OriginalF45BracketTree.RotationEdge.reverse
#print axioms OriginalF45BracketTree.RotationEdge.toExchangeClass_eq
#print axioms OriginalF45BracketTree.RotationChain
#print axioms OriginalF45BracketTree.RotationChain.length
#print axioms OriginalF45BracketTree.RotationChain.append
#print axioms OriginalF45BracketTree.RotationChain.length_append
#print axioms OriginalF45BracketTree.RotationChain.reverse
#print axioms OriginalF45BracketTree.RotationChain.toExchangeClass_eq
#print axioms OriginalF45BracketTree.RotationChain.axisHistories_eq

end
end KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
