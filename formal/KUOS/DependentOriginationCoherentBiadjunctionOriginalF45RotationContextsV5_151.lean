import KUOS.DependentOriginationCoherentBiadjunctionOriginalF45FiniteRotationChainsV5_151

namespace KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F54-C / v5.151 — whisker complete finite rotation sequences in either context

An arbitrary FINITE proof-relevant chain of local associativity
rotations is stable under placement within any independent F19/F28
left or right original F45 binary context. The construction keeps
every original intermediate bracket tree and every actual forward/
backward rotation witness. It does not merely invoke a Prop-level
congruence or reselect any source/target pseudofunctor.

Both contextual operations preserve the exact number of individual
rotation edges; the original F44 generated quotient classes and both
complete Type-valued within-axis histories remain equal.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Genuine contextual left whiskering of one individually typed
original F54 associativity edge; reverse witnesses remain reverse. -/
def OriginalF45BracketTree.RotationEdge.leftContext
    {a b : D} {x y : E} {n m n' m' : Nat}
    {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
    {first second : OriginalF45BracketTree n m ma pa mb pb}
    (edge : OriginalF45BracketTree.RotationEdge first second)
    (later : OriginalF45BracketTree n' m' mb pb mc pc) :
    OriginalF45BracketTree.RotationEdge
      (OriginalF45BracketTree.node first later)
      (OriginalF45BracketTree.node second later) := by
  cases edge with
  | forward rotation =>
      exact OriginalF45BracketTree.RotationEdge.forward
        (OriginalF45BracketTree.LocalRotation.leftContext rotation later)
  | backward rotation =>
      exact OriginalF45BracketTree.RotationEdge.backward
        (OriginalF45BracketTree.LocalRotation.leftContext rotation later)

/-- Genuine contextual right whiskering of an actual local rotation
edge by any original finite left-hand F45 bracket tree. -/
def OriginalF45BracketTree.RotationEdge.rightContext
    {a b : D} {x y : E} {n m n' m' : Nat}
    {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
    (earlier : OriginalF45BracketTree n m ma pa mb pb)
    {first second : OriginalF45BracketTree n' m' mb pb mc pc}
    (edge : OriginalF45BracketTree.RotationEdge first second) :
    OriginalF45BracketTree.RotationEdge
      (OriginalF45BracketTree.node earlier first)
      (OriginalF45BracketTree.node earlier second) := by
  cases edge with
  | forward rotation =>
      exact OriginalF45BracketTree.RotationEdge.forward
        (OriginalF45BracketTree.LocalRotation.rightContext earlier rotation)
  | backward rotation =>
      exact OriginalF45BracketTree.RotationEdge.backward
        (OriginalF45BracketTree.LocalRotation.rightContext earlier rotation)

/-- Whisker an ENTIRE actual finite rotation chain in the LEFT
context of its original binary F45 computation. This retains
every intermediate tree and each original local rotation edge. -/
def OriginalF45BracketTree.RotationChain.leftContext
    {a b : D} {x y : E} {n m n' m' : Nat}
    {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
    {first second : OriginalF45BracketTree n m ma pa mb pb}
    (chain : OriginalF45BracketTree.RotationChain first second)
    (later : OriginalF45BracketTree n' m' mb pb mc pc) :
    OriginalF45BracketTree.RotationChain
      (OriginalF45BracketTree.node first later)
      (OriginalF45BracketTree.node second later) := by
  induction chain with
  | refl tree =>
      exact OriginalF45BracketTree.RotationChain.refl
        (OriginalF45BracketTree.node tree later)
  | snoc chain edge ih =>
      exact OriginalF45BracketTree.RotationChain.snoc ih
        (OriginalF45BracketTree.RotationEdge.leftContext edge later)

/-- Whisker an ENTIRE real finite rotation chain in the RIGHT
context by an earlier genuine original F45 binary tree. -/
def OriginalF45BracketTree.RotationChain.rightContext
    {a b : D} {x y : E} {n m n' m' : Nat}
    {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
    (earlier : OriginalF45BracketTree n m ma pa mb pb)
    {first second : OriginalF45BracketTree n' m' mb pb mc pc}
    (chain : OriginalF45BracketTree.RotationChain first second) :
    OriginalF45BracketTree.RotationChain
      (OriginalF45BracketTree.node earlier first)
      (OriginalF45BracketTree.node earlier second) := by
  induction chain with
  | refl tree =>
      exact OriginalF45BracketTree.RotationChain.refl
        (OriginalF45BracketTree.node earlier tree)
  | snoc chain edge ih =>
      exact OriginalF45BracketTree.RotationChain.snoc ih
        (OriginalF45BracketTree.RotationEdge.rightContext earlier edge)

/-- Left contextual whiskering has EXACTLY the same FINITE number
of actual elementary rotations, with no proof-irrelevance erasure. -/
theorem OriginalF45BracketTree.RotationChain.leftContext_length
    {a b : D} {x y : E} {n m n' m' : Nat}
    {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
    {first second : OriginalF45BracketTree n m ma pa mb pb}
    (chain : OriginalF45BracketTree.RotationChain first second)
    (later : OriginalF45BracketTree n' m' mb pb mc pc) :
    (chain.leftContext later).length = chain.length := by
  induction chain with
  | refl tree =>
      rfl
  | snoc chain edge ih =>
      exact congrArg (fun t => t + 1) ih

/-- Right contextual whiskering likewise keeps the exact recorded
finite number of ACTUAL local rotation witnesses. -/
theorem OriginalF45BracketTree.RotationChain.rightContext_length
    {a b : D} {x y : E} {n m n' m' : Nat}
    {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
    (earlier : OriginalF45BracketTree n m ma pa mb pb)
    {first second : OriginalF45BracketTree n' m' mb pb pc}
    (chain : OriginalF45BracketTree.RotationChain first second) :
    (chain.rightContext earlier).length = chain.length := by
  induction chain with
  | refl tree =>
      rfl
  | snoc chain edge ih =>
      exact congrArg (fun t => t + 1) ih

/-- A finite local rotation chain under an ARBITRARY left context
preserves the original generated F44 exchange class, not just Hom. -/
theorem OriginalF45BracketTree.RotationChain.leftContext_toClass_eq
    {a b : D} {x y : E} {n m n' m' : Nat}
    {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
    {first second : OriginalF45BracketTree n m ma pa mb pb}
    (chain : OriginalF45BracketTree.RotationChain first second)
    (later : OriginalF45BracketTree n' m' mb pb mc pc) :
    (OriginalF45BracketTree.node first later).toExchangeClass =
      (OriginalF45BracketTree.node second later).toExchangeClass :=
  (chain.leftContext later).toExchangeClass_eq

/-- The corresponding full finite right-context rotation operation
preserves the exact generated F44 adjacent-exchange quotient class. -/
theorem OriginalF45BracketTree.RotationChain.rightContext_toClass_eq
    {a b : D} {x y : E} {n m n' m' : Nat}
    {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
    (earlier : OriginalF45BracketTree n m ma pa mb pb)
    {first second : OriginalF45BracketTree n' m' mb pb pc}
    (chain : OriginalF45BracketTree.RotationChain first second) :
    (OriginalF45BracketTree.node earlier first).toExchangeClass =
      (OriginalF45BracketTree.node earlier second).toExchangeClass :=
  (chain.rightContext earlier).toExchangeClass_eq

#print axioms OriginalF45BracketTree.RotationEdge.leftContext
#print axioms OriginalF45BracketTree.RotationEdge.rightContext
#print axioms OriginalF45BracketTree.RotationChain.leftContext
#print axioms OriginalF45BracketTree.RotationChain.rightContext
#print axioms OriginalF45BracketTree.RotationChain.leftContext_length
#print axioms OriginalF45BracketTree.RotationChain.rightContext_length
#print axioms OriginalF45BracketTree.RotationChain.leftContext_toClass_eq
#print axioms OriginalF45BracketTree.RotationChain.rightContext_toClass_eq

end
end KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
