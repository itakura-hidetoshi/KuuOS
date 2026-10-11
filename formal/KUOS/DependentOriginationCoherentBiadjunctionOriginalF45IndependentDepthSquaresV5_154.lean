import KUOS.DependentOriginationTruncatedIcosahedralPentagonRotationBridgeV5_154
import KUOS.DependentOriginationCoherentBiadjunctionOriginalF45DepthRotationInvariantsV5_152

namespace KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F57-C1 / v5.154 — actual independent depth-aware F45 square pasting

F55-B handles two independent local rotations at fixed depths.
F57-C1 handles TWO original finite DepthRotationRoute witnesses,
including actual F19 and F28 dependent Nat-depth transports.
The two actual Type-valued sequences perform the left then right
route, or right then left; they share exactly one original F45
source and target binary tree. They have equal *counts*, separately
proved original F44 class interpretations, and both COMPLETE
original F19/F28 histories.

This is an actual square of TWO concrete finite typed path sequences,
not a freely asserted tricategorical 3-cell between those paths.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

def OriginalF45BracketTree.DepthRotationRoute.disjointLeftThenRight
    {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : Blocks a b} {q₀ q₁ q₂ : Blocks x y}
    {leftBefore : OriginalF45BracketTree n m p₀ q₀ p₁ q₁}
    {leftAfter : OriginalF45BracketTree n' m' p₀ q₀ p₁ q₁}
    {rightBefore : OriginalF45BracketTree k l p₁ q₁ p₂ q₂}
    {rightAfter : OriginalF45BracketTree k' l' p₁ q₁ p₂ q₂}
    (left : OriginalF45BracketTree.DepthRotationRoute leftBefore leftAfter)
    (right : OriginalF45BracketTree.DepthRotationRoute rightBefore rightAfter) :
    OriginalF45BracketTree.DepthRotationRoute
      (OriginalF45BracketTree.node leftBefore rightBefore)
      (OriginalF45BracketTree.node leftAfter rightAfter) :=
  OriginalF45BracketTree.DepthRotationRoute.trans
    (OriginalF45BracketTree.DepthRotationRoute.leftContext left rightBefore)
    (OriginalF45BracketTree.DepthRotationRoute.rightContext leftAfter right)

def OriginalF45BracketTree.DepthRotationRoute.disjointRightThenLeft
    {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : Blocks a b} {q₀ q₁ q₂ : Blocks x y}
    {leftBefore : OriginalF45BracketTree n m p₀ q₀ p₁ q₁}
    {leftAfter : OriginalF45BracketTree n' m' p₀ q₀ p₁ q₁}
    {rightBefore : OriginalF45BracketTree k l p₁ q₁ p₂ q₂}
    {rightAfter : OriginalF45BracketTree k' l' p₁ q₁ p₂ q₂}
    (left : OriginalF45BracketTree.DepthRotationRoute leftBefore leftAfter)
    (right : OriginalF45BracketTree.DepthRotationRoute rightBefore rightAfter) :
    OriginalF45BracketTree.DepthRotationRoute
      (OriginalF45BracketTree.node leftBefore rightBefore)
      (OriginalF45BracketTree.node leftAfter rightAfter) :=
  OriginalF45BracketTree.DepthRotationRoute.trans
    (OriginalF45BracketTree.DepthRotationRoute.rightContext leftBefore right)
    (OriginalF45BracketTree.DepthRotationRoute.leftContext left rightAfter)

theorem OriginalF45BracketTree.DepthRotationRoute.disjointLeftThenRight_count
    {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : Blocks a b} {q₀ q₁ q₂ : Blocks x y}
    {leftBefore : OriginalF45BracketTree n m p₀ q₀ p₁ q₁}
    {leftAfter : OriginalF45BracketTree n' m' p₀ q₀ p₁ q₁}
    {rightBefore : OriginalF45BracketTree k l p₁ q₁ p₂ q₂}
    {rightAfter : OriginalF45BracketTree k' l' p₁ q₁ p₂ q₂}
    (left : OriginalF45BracketTree.DepthRotationRoute leftBefore leftAfter)
    (right : OriginalF45BracketTree.DepthRotationRoute rightBefore rightAfter) :
    (left.disjointLeftThenRight right).rotationCount =
      left.rotationCount + right.rotationCount := by
  rfl

theorem OriginalF45BracketTree.DepthRotationRoute.disjointRightThenLeft_count
    {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : Blocks a b} {q₀ q₁ q₂ : Blocks x y}
    {leftBefore : OriginalF45BracketTree n m p₀ q₀ p₁ q₁}
    {leftAfter : OriginalF45BracketTree n' m' p₀ q₀ p₁ q₁}
    {rightBefore : OriginalF45BracketTree k l p₁ q₁ p₂ q₂}
    {rightAfter : OriginalF45BracketTree k' l' p₁ q₁ p₂ q₂}
    (left : OriginalF45BracketTree.DepthRotationRoute leftBefore leftAfter)
    (right : OriginalF45BracketTree.DepthRotationRoute rightBefore rightAfter) :
    (left.disjointRightThenLeft right).rotationCount =
      right.rotationCount + left.rotationCount := by
  rfl

theorem OriginalF45BracketTree.DepthRotationRoute.disjointSquare_counts_eq
    {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : Blocks a b} {q₀ q₁ q₂ : Blocks x y}
    {leftBefore : OriginalF45BracketTree n m p₀ q₀ p₁ q₁}
    {leftAfter : OriginalF45BracketTree n' m' p₀ q₀ p₁ q₁}
    {rightBefore : OriginalF45BracketTree k l p₁ q₁ p₂ q₂}
    {rightAfter : OriginalF45BracketTree k' l' p₁ q₁ p₂ q₂}
    (left : OriginalF45BracketTree.DepthRotationRoute leftBefore leftAfter)
    (right : OriginalF45BracketTree.DepthRotationRoute rightBefore rightAfter) :
    (left.disjointLeftThenRight right).rotationCount =
      (left.disjointRightThenLeft right).rotationCount := by
  rw [left.disjointLeftThenRight_count, left.disjointRightThenLeft_count,
    Nat.add_comm]

/-- Genuine two-order independent Type-valued square plus complete
F44 and F19/F28 native axis-history endpoint certificates. -/
structure OriginalF45BracketTree.DepthRotationRoute.IndependentSquare
    {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : Blocks a b} {q₀ q₁ q₂ : Blocks x y}
    {leftBefore : OriginalF45BracketTree n m p₀ q₀ p₁ q₁}
    {leftAfter : OriginalF45BracketTree n' m' p₀ q₀ p₁ q₁}
    {rightBefore : OriginalF45BracketTree k l p₁ q₁ p₂ q₂}
    {rightAfter : OriginalF45BracketTree k' l' p₁ q₁ p₂ q₂}
    (left : OriginalF45BracketTree.DepthRotationRoute leftBefore leftAfter)
    (right : OriginalF45BracketTree.DepthRotationRoute rightBefore rightAfter) where
  leftFirst :
    OriginalF45BracketTree.DepthRotationRoute
      (OriginalF45BracketTree.node leftBefore rightBefore)
      (OriginalF45BracketTree.node leftAfter rightAfter)
  rightFirst :
    OriginalF45BracketTree.DepthRotationRoute
      (OriginalF45BracketTree.node leftBefore rightBefore)
      (OriginalF45BracketTree.node leftAfter rightAfter)
  counts_eq : leftFirst.rotationCount = rightFirst.rotationCount
  leftClass :
    ExchangeClass.castDepths leftFirst.depthEq.1 leftFirst.depthEq.2
      (OriginalF45BracketTree.node leftBefore rightBefore).toExchangeClass =
        (OriginalF45BracketTree.node leftAfter rightAfter).toExchangeClass
  rightClass :
    ExchangeClass.castDepths rightFirst.depthEq.1 rightFirst.depthEq.2
      (OriginalF45BracketTree.node leftBefore rightBefore).toExchangeClass =
        (OriginalF45BracketTree.node leftAfter rightAfter).toExchangeClass
  leftHistories :
    (OriginalF45BracketTree.castDepths leftFirst.depthEq.1 leftFirst.depthEq.2
      (OriginalF45BracketTree.node leftBefore rightBefore)).axisHistories =
        (OriginalF45BracketTree.node leftAfter rightAfter).axisHistories
  rightHistories :
    (OriginalF45BracketTree.castDepths rightFirst.depthEq.1 rightFirst.depthEq.2
      (OriginalF45BracketTree.node leftBefore rightBefore)).axisHistories =
        (OriginalF45BracketTree.node leftAfter rightAfter).axisHistories

def OriginalF45BracketTree.DepthRotationRoute.IndependentSquare.canonical
    {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : Blocks a b} {q₀ q₁ q₂ : Blocks x y}
    {leftBefore : OriginalF45BracketTree n m p₀ q₀ p₁ q₁}
    {leftAfter : OriginalF45BracketTree n' m' p₀ q₀ p₁ q₁}
    {rightBefore : OriginalF45BracketTree k l p₁ q₁ p₂ q₂}
    {rightAfter : OriginalF45BracketTree k' l' p₁ q₁ p₂ q₂}
    (left : OriginalF45BracketTree.DepthRotationRoute leftBefore leftAfter)
    (right : OriginalF45BracketTree.DepthRotationRoute rightBefore rightAfter) :
    OriginalF45BracketTree.DepthRotationRoute.IndependentSquare left right :=
  {
    leftFirst := left.disjointLeftThenRight right
    rightFirst := left.disjointRightThenLeft right
    counts_eq := left.disjointSquare_counts_eq right
    leftClass := (left.disjointLeftThenRight right).toExchangeClass_eq
    rightClass := (left.disjointRightThenLeft right).toExchangeClass_eq
    leftHistories := (left.disjointLeftThenRight right).axisHistories_eq
    rightHistories := (left.disjointRightThenLeft right).axisHistories_eq
  }

#print axioms OriginalF45BracketTree.DepthRotationRoute.disjointLeftThenRight
#print axioms OriginalF45BracketTree.DepthRotationRoute.disjointRightThenLeft
#print axioms OriginalF45BracketTree.DepthRotationRoute.disjointLeftThenRight_count
#print axioms OriginalF45BracketTree.DepthRotationRoute.disjointRightThenLeft_count
#print axioms OriginalF45BracketTree.DepthRotationRoute.disjointSquare_counts_eq
#print axioms OriginalF45BracketTree.DepthRotationRoute.IndependentSquare
#print axioms OriginalF45BracketTree.DepthRotationRoute.IndependentSquare.canonical

end
end KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
