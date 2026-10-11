import KUOS.DependentOriginationCoherentBiadjunctionOriginalF45RotationDepthRoutesV5_152

namespace KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F55-B / v5.152 — actual disjoint rotation square and typed path-cell presentation

F55-A constructs two genuine original F54 pentagon paths with 3 vs 2
individual associativity rotations and separately typed F19/F28
dependent-index transports. F55-B adds the *other* basic two-dimensional
critical shape: two disjoint contextual rotations, applied in either
order, both ending at the same original F45 binary tree.

The paths are truly constructed from original Type-valued LocalRotation,
RotationEdge, RotationChain and DepthRotationRoute constructors. The
proof-relevant PresentedCell below is a FREE TYPED PRESENTATION of the
pentagon and square relations and their formal 2-dimensional closure.
Its constructors do NOT claim that those generating cells have been
identified with any independently defined tricategorical 3-cells.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Embed exactly ONE original F54 local rotation in a genuine
RotationChain witness; no quotient-equality shortcut or omitted edge. -/
def OriginalF45BracketTree.DepthRotationRoute.ofLocalRotation
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {before after : OriginalF45BracketTree n m ma pa mb pb}
    (rotation : OriginalF45BracketTree.LocalRotation before after) :
    OriginalF45BracketTree.DepthRotationRoute before after :=
  OriginalF45BracketTree.DepthRotationRoute.chain
    (OriginalF45BracketTree.RotationChain.snoc
      (OriginalF45BracketTree.RotationChain.refl _)
      (OriginalF45BracketTree.RotationEdge.forward rotation))

theorem OriginalF45BracketTree.DepthRotationRoute.ofLocalRotation_count
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {before after : OriginalF45BracketTree n m ma pa mb pb}
    (rotation : OriginalF45BracketTree.LocalRotation before after) :
    (OriginalF45BracketTree.DepthRotationRoute.ofLocalRotation
      rotation).rotationCount = 1 := by
  rfl

section DisjointRotations

variable {a b : D} {x y : E}
variable {n m n' m' : Nat}
variable {p₀ p₁ p₂ : Blocks a b}
variable {q₀ q₁ q₂ : Blocks x y}
variable {leftBefore leftAfter : OriginalF45BracketTree n m p₀ q₀ p₁ q₁}
variable {rightBefore rightAfter : OriginalF45BracketTree n' m' p₁ q₁ p₂ q₂}
variable
  (left : OriginalF45BracketTree.LocalRotation leftBefore leftAfter)
  (right : OriginalF45BracketTree.LocalRotation rightBefore rightAfter)

/-- Two genuine rotations in disjoint binary contexts:
first in the left subtree, THEN in the right subtree. -/
def OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst :
    OriginalF45BracketTree.DepthRotationRoute
      (OriginalF45BracketTree.node leftBefore rightBefore)
      (OriginalF45BracketTree.node leftAfter rightAfter) :=
  OriginalF45BracketTree.DepthRotationRoute.trans
    (OriginalF45BracketTree.DepthRotationRoute.ofLocalRotation
      (OriginalF45BracketTree.LocalRotation.leftContext left rightBefore))
    (OriginalF45BracketTree.DepthRotationRoute.ofLocalRotation
      (OriginalF45BracketTree.LocalRotation.rightContext leftAfter right))

/-- The opposite order of the same TWO genuinely disjoint local
F54 rotations: right context first, then left context. -/
def OriginalF45BracketTree.DepthRotationRoute.squareRightFirst :
    OriginalF45BracketTree.DepthRotationRoute
      (OriginalF45BracketTree.node leftBefore rightBefore)
      (OriginalF45BracketTree.node leftAfter rightAfter) :=
  OriginalF45BracketTree.DepthRotationRoute.trans
    (OriginalF45BracketTree.DepthRotationRoute.ofLocalRotation
      (OriginalF45BracketTree.LocalRotation.rightContext leftBefore right))
    (OriginalF45BracketTree.DepthRotationRoute.ofLocalRotation
      (OriginalF45BracketTree.LocalRotation.leftContext left rightAfter))

/-- Both orders retain exactly two original Type-valued F54 steps. -/
theorem OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst_count :
    (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst
      left right).rotationCount = 2 := by
  rfl

theorem OriginalF45BracketTree.DepthRotationRoute.squareRightFirst_count :
    (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst
      left right).rotationCount = 2 := by
  rfl

end DisjointRotations

/-- A PROOF-RELEVANT two-dimensional presentation on parallel,
honestly typed ORIGINAL F45 DepthRotationRoute witnesses.

The nontrivial generators are the concrete original F55-A pentagon
and the F55-B square of independent F54 contextual rotations. The
other constructors provide formal identity, reversal, vertical
composition, horizontal path-composition, and left/right context
whiskering of the generated cells.

This is a *presented* path-cell carrier, NOT a theorem identifying
these freely generated cells with arbitrary external Gray/tricategory
3-morphisms, and NOT a global contractibility assertion. -/
inductive OriginalF45BracketTree.DepthRotationRoute.PresentedCell :
    ∀ {a b : D} {x y : E}
      {n n' m m' : Nat}
      {ma mb : Blocks a b} {pa pb : Blocks x y}
      {first : OriginalF45BracketTree n m ma pa mb pb}
      {last : OriginalF45BracketTree n' m' ma pa mb pb},
      OriginalF45BracketTree.DepthRotationRoute first last →
      OriginalF45BracketTree.DepthRotationRoute first last →
      Type (max (max uD uE) (max vD vE)) where
  | ident
      {a b : D} {x y : E}
      {n n' m m' : Nat}
      {ma mb : Blocks a b} {pa pb : Blocks x y}
      {first : OriginalF45BracketTree n m ma pa mb pb}
      {last : OriginalF45BracketTree n' m' ma pa mb pb}
      (route : OriginalF45BracketTree.DepthRotationRoute first last) :
      PresentedCell route route
  | pentagon
      {a b : D} {x y : E}
      {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
      {p₀ p₁ p₂ p₃ p₄ : Blocks a b}
      {q₀ q₁ q₂ q₃ q₄ : Blocks x y}
      (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
      (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
      (t₃ : OriginalF45BracketTree n₃ m₃ p₂ q₂ p₃ q₃)
      (t₄ : OriginalF45BracketTree n₄ m₄ p₃ q₃ p₄ q₄) :
      PresentedCell
        (OriginalF45BracketTree.DepthRotationRoute.pentagonLong
          t₁ t₂ t₃ t₄)
        (OriginalF45BracketTree.DepthRotationRoute.pentagonShort
          t₁ t₂ t₃ t₄)
  | disjointSquare
      {a b : D} {x y : E}
      {n m n' m' : Nat}
      {p₀ p₁ p₂ : Blocks a b}
      {q₀ q₁ q₂ : Blocks x y}
      {leftBefore leftAfter :
        OriginalF45BracketTree n m p₀ q₀ p₁ q₁}
      {rightBefore rightAfter :
        OriginalF45BracketTree n' m' p₁ q₁ p₂ q₂}
      (left : OriginalF45BracketTree.LocalRotation leftBefore leftAfter)
      (right : OriginalF45BracketTree.LocalRotation rightBefore rightAfter) :
      PresentedCell
        (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right)
        (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right)
  | symm
      {a b : D} {x y : E}
      {n n' m m' : Nat}
      {ma mb : Blocks a b} {pa pb : Blocks x y}
      {first : OriginalF45BracketTree n m ma pa mb pb}
      {last : OriginalF45BracketTree n' m' ma pa mb pb}
      {r s : OriginalF45BracketTree.DepthRotationRoute first last}
      (cell : PresentedCell r s) : PresentedCell s r
  | trans
      {a b : D} {x y : E}
      {n n' m m' : Nat}
      {ma mb : Blocks a b} {pa pb : Blocks x y}
      {first : OriginalF45BracketTree n m ma pa mb pb}
      {last : OriginalF45BracketTree n' m' ma pa mb pb}
      {r s t : OriginalF45BracketTree.DepthRotationRoute first last}
      (left : PresentedCell r s) (right : PresentedCell s t) :
      PresentedCell r t
  | leftContext
      {a b : D} {x y : E}
      {n n' m m' k l : Nat}
      {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
      {first : OriginalF45BracketTree n m ma pa mb pb}
      {last : OriginalF45BracketTree n' m' ma pa mb pb}
      {r s : OriginalF45BracketTree.DepthRotationRoute first last}
      (cell : PresentedCell r s)
      (later : OriginalF45BracketTree k l mb pb mc pc) :
      PresentedCell
        (OriginalF45BracketTree.DepthRotationRoute.leftContext r later)
        (OriginalF45BracketTree.DepthRotationRoute.leftContext s later)
  | rightContext
      {a b : D} {x y : E}
      {k l n n' m m' : Nat}
      {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
      (earlier : OriginalF45BracketTree k l ma pa mb pb)
      {first : OriginalF45BracketTree n m mb pb mc pc}
      {last : OriginalF45BracketTree n' m' mb pb mc pc}
      {r s : OriginalF45BracketTree.DepthRotationRoute first last}
      (cell : PresentedCell r s) :
      PresentedCell
        (OriginalF45BracketTree.DepthRotationRoute.rightContext earlier r)
        (OriginalF45BracketTree.DepthRotationRoute.rightContext earlier s)
  | precompose
      {a b : D} {x y : E}
      {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
      {ma mb : Blocks a b} {pa pb : Blocks x y}
      {first : OriginalF45BracketTree n₁ m₁ ma pa mb pb}
      {middle : OriginalF45BracketTree n₂ m₂ ma pa mb pb}
      {last : OriginalF45BracketTree n₃ m₃ ma pa mb pb}
      (priorRoute : OriginalF45BracketTree.DepthRotationRoute first middle)
      {r s : OriginalF45BracketTree.DepthRotationRoute middle last}
      (cell : PresentedCell r s) :
      PresentedCell
        (OriginalF45BracketTree.DepthRotationRoute.trans priorRoute r)
        (OriginalF45BracketTree.DepthRotationRoute.trans priorRoute s)
  | postcompose
      {a b : D} {x y : E}
      {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
      {ma mb : Blocks a b} {pa pb : Blocks x y}
      {first : OriginalF45BracketTree n₁ m₁ ma pa mb pb}
      {middle : OriginalF45BracketTree n₂ m₂ ma pa mb pb}
      {last : OriginalF45BracketTree n₃ m₃ ma pa mb pb}
      {r s : OriginalF45BracketTree.DepthRotationRoute first middle}
      (cell : PresentedCell r s)
      (suffix : OriginalF45BracketTree.DepthRotationRoute middle last) :
      PresentedCell
        (OriginalF45BracketTree.DepthRotationRoute.trans r suffix)
        (OriginalF45BracketTree.DepthRotationRoute.trans s suffix)

#print axioms OriginalF45BracketTree.DepthRotationRoute.ofLocalRotation
#print axioms OriginalF45BracketTree.DepthRotationRoute.ofLocalRotation_count
#print axioms OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst
#print axioms OriginalF45BracketTree.DepthRotationRoute.squareRightFirst
#print axioms OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst_count
#print axioms OriginalF45BracketTree.DepthRotationRoute.squareRightFirst_count
#print axioms OriginalF45BracketTree.DepthRotationRoute.PresentedCell

end
end KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
