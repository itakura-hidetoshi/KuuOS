import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4ABBackwardFiberNormalForm
import Mathlib.Tactic

/-!
F112-P94D3GK4AC — genuine source-dependent F45 left-weight rank.

Every actual F45 leaf or refl counts as one strictly positive leaf.
Each real binary node contributes the number of leaves of its LEFT
subtree to the rank, in addition to the two subranks. At a true
forward local F54 associator ((A B) C) -> (A (B C)), the rank
decreases by exactly the positive leaf count of A. The two independent
original Nat-depth casts preserve the exact weight and leaf count.
Every genuinely typed left/right F54 context preserves this decrease.

For a real original F54 route whose ACTUAL backward RotationEdge count
is zero, the rank drops by at least its exact physical rotationCount.
In particular a type-correct self-route with no backward evidence
cannot contain ANY physical rotation. Proof is on the actual source
constructors: F45 trees, original LocalRotation, bidirectional
RotationEdge, intermediate-tree RotationChain, double-axis casts,
trans and the two dependent contexts; no shadow or new 3-cell.

This is about the independent native F54 presentation only.
No original P92B category laws, 14D unconditional Countable,
historical full typed equivalence, 19D filler, global strict n,
hyperdescent or S->K_AA global faithfulness are assumed.
Strict 空 central; independent Kuu one presentation, no Gray,
append-only / tighten-only / same-root 107.
Protected #1558 Draft/OPEN/unmerged. Pinned Lean v4.30.0-rc2,
mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE

section ActualTreeWeight
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {n m : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}

/-- Number of genuine nonempty terminal F45 pieces, INCLUDING the
original refl-shaped stage. No artificial empty leaf is allowed. -/
def KuuNativeF45Tree.gk4acLeafCount
    (tree : KuuNativeF45Tree p n m ma pa mb pb) : Nat := by
  induction tree with
  | refl _ _ _ => exact 1
  | leaf _ _ _ _ => exact 1
  | node left right ihLeft ihRight => exact ihLeft + ihRight

/-- Canonical natural-valued left-branch rank of the original
fully dependent two-category F45 binary tree. -/
def KuuNativeF45Tree.gk4acLeftRank
    (tree : KuuNativeF45Tree p n m ma pa mb pb) : Nat := by
  induction tree with
  | refl _ _ _ => exact 0
  | leaf _ _ _ _ => exact 0
  | node left right ihLeft ihRight =>
      exact ihLeft + ihRight + left.gk4acLeafCount

theorem KuuNativeF45Tree.gk4acLeafCount_pos
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    0 < tree.gk4acLeafCount := by
  induction tree with
  | refl _ _ _ => change 0 < (1 : Nat); omega
  | leaf _ _ _ _ => change 0 < (1 : Nat); omega
  | node left right ihLeft ihRight =>
      change 0 < left.gk4acLeafCount + right.gk4acLeafCount
      omega

@[simp] theorem KuuNativeF45Tree.gk4acLeafCount_node
    {k l : Nat} {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    (left : KuuNativeF45Tree p n m ma pa mb pb)
    (right : KuuNativeF45Tree p k l mb pb mc pc) :
    (KuuNativeF45Tree.node left right).gk4acLeafCount =
      left.gk4acLeafCount + right.gk4acLeafCount := rfl

@[simp] theorem KuuNativeF45Tree.gk4acLeftRank_node
    {k l : Nat} {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    (left : KuuNativeF45Tree p n m ma pa mb pb)
    (right : KuuNativeF45Tree p k l mb pb mc pc) :
    (KuuNativeF45Tree.node left right).gk4acLeftRank =
      left.gk4acLeftRank + right.gk4acLeftRank + left.gk4acLeafCount := rfl

@[simp] theorem KuuNativeF45Tree.gk4acLeafCount_cast
    {n' m' : Nat} (hn : n = n') (hm : m = m')
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    (KuuNativeF45Tree.castDepths hn hm tree).gk4acLeafCount =
      tree.gk4acLeafCount := by
  cases hn
  cases hm
  rfl

@[simp] theorem KuuNativeF45Tree.gk4acLeftRank_cast
    {n' m' : Nat} (hn : n = n') (hm : m = m')
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    (KuuNativeF45Tree.castDepths hn hm tree).gk4acLeftRank =
      tree.gk4acLeftRank := by
  cases hn
  cases hm
  rfl

end ActualTreeWeight

section TrueLocalRotationBound
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {before after : KuuNativeF45Tree p n m ma pa mb pb}

/-- The leaf count is preserved by ALL actual Type-valued local
associators, including nested left and right contexts. -/
theorem KuuNativeF45Tree.LocalRotation.gk4acLeafCount_eq
    (step : KuuNativeF45Tree.LocalRotation p before after) :
    before.gk4acLeafCount = after.gk4acLeafCount := by
  induction step with
  | assoc first second third =>
      simp only [KuuNativeF45Tree.gk4acLeafCount_cast,
        KuuNativeF45Tree.gk4acLeafCount_node]
      omega
  | leftContext step later ih =>
      simp only [KuuNativeF45Tree.gk4acLeafCount_node]
      omega
  | rightContext earlier step ih =>
      simp only [KuuNativeF45Tree.gk4acLeafCount_node]
      omega

/-- A genuine F54 forward local rotation decreases the rank STRICTLY
by at least 1, because its leftmost source subtree is nonempty.
No arbitrary untyped inverse associator is introduced. -/
theorem KuuNativeF45Tree.LocalRotation.gk4acLeftRank_drop
    (step : KuuNativeF45Tree.LocalRotation p before after) :
    after.gk4acLeftRank + 1 ≤ before.gk4acLeftRank := by
  induction step with
  | assoc first second third =>
      have hpositive := first.gk4acLeafCount_pos
      simp only [KuuNativeF45Tree.gk4acLeftRank_cast,
        KuuNativeF45Tree.gk4acLeftRank_node,
        KuuNativeF45Tree.gk4acLeafCount_node]
      omega
  | leftContext step later ih =>
      have hleaf := step.gk4acLeafCount_eq
      simp only [KuuNativeF45Tree.gk4acLeftRank_node]
      omega
  | rightContext earlier step ih =>
      simp only [KuuNativeF45Tree.gk4acLeftRank_node]
      omega

/-- The ORIGINAL stored orientation is decisive: a true backward
edge cannot have backwardCount zero. -/
theorem KuuNativeF45Tree.RotationEdge.gk4acForward_bound
    (edge : KuuNativeF45Tree.RotationEdge p before after)
    (hback : edge.gk4zBackwardCount = 0) :
    after.gk4acLeftRank + 1 ≤ before.gk4acLeftRank := by
  cases edge with
  | forward step =>
      exact step.gk4acLeftRank_drop
  | backward step =>
      simp only [KuuNativeF45Tree.RotationEdge.gk4zBackwardCount] at hback
      omega

theorem KuuNativeF45Tree.RotationEdge.gk4acLeafCount_eq
    (edge : KuuNativeF45Tree.RotationEdge p before after) :
    before.gk4acLeafCount = after.gk4acLeafCount := by
  cases edge with
  | forward step => exact step.gk4acLeafCount_eq
  | backward step => exact step.gk4acLeafCount_eq.symm

end TrueLocalRotationBound

section ActualChainAndRoute
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {n m : Nat} {n' m' : Nat}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}

/-- Actual intermediate trees preserve genuine leaf count along
any bidirectional original F54 RotationChain. -/
theorem KuuNativeF45Tree.RotationChain.gk4acLeafCount_eq
    {last : KuuNativeF45Tree p n m ma pa mb pb}
    (chain : KuuNativeF45Tree.RotationChain p first last) :
    first.gk4acLeafCount = last.gk4acLeafCount := by
  induction chain with
  | refl => rfl
  | snoc prior edge ih =>
      exact ih.trans edge.gk4acLeafCount_eq

/-- The rank drops by AT LEAST the actual number of primitive physical
rotations in any chain with ZERO genuine backward edges. -/
theorem KuuNativeF45Tree.RotationChain.gk4acNoBackward_bound
    {last : KuuNativeF45Tree p n m ma pa mb pb}
    (chain : KuuNativeF45Tree.RotationChain p first last)
    (hback : chain.gk4zBackwardCount = 0) :
    last.gk4acLeftRank + chain.length ≤ first.gk4acLeftRank := by
  induction chain with
  | refl =>
      change _ + 0 ≤ _
      omega
  | snoc prior edge ih =>
      have hp : prior.gk4zBackwardCount = 0 := by
        change prior.gk4zBackwardCount + edge.gk4zBackwardCount = 0 at hback
        omega
      have he : edge.gk4zBackwardCount = 0 := by
        change prior.gk4zBackwardCount + edge.gk4zBackwardCount = 0 at hback
        omega
      have hr := ih hp
      have hs := edge.gk4acForward_bound he
      simp only [KuuNativeF45Tree.RotationChain.length]
      omega

/-- ALL original dependent F54 route constructors preserve actual
positive-leaf binary-tree data, including both depth equality casts. -/
theorem KuuNativeF45Tree.DepthRotationRoute.gk4acLeafCount_eq
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    first.gk4acLeafCount = last.gk4acLeafCount := by
  induction route with
  | chain path => exact path.gk4acLeafCount_eq
  | castDepths hn hm tree =>
      exact (KuuNativeF45Tree.gk4acLeafCount_cast hn hm tree).symm
  | trans left right ihLeft ihRight => exact ihLeft.trans ihRight
  | leftContext path later ih =>
      simp only [KuuNativeF45Tree.gk4acLeafCount_node]
      omega
  | rightContext earlier path ih =>
      simp only [KuuNativeF45Tree.gk4acLeafCount_node]
      omega

/-- ACTUAL original F54 no-backward theorem for arbitrary typed
routes: each genuine forward physical edge costs >= 1 rank.
This includes arbitrary real Nat casts, vertical composition,
left/right typed contexts and all intermediate trees. -/
theorem KuuNativeF45Tree.DepthRotationRoute.gk4acNoBackward_bound
    (route : KuuNativeF45Tree.DepthRotationRoute p first last)
    (hback : route.gk4zBackwardCount = 0) :
    last.gk4acLeftRank + route.rotationCount ≤ first.gk4acLeftRank := by
  induction route with
  | chain path =>
      exact path.gk4acNoBackward_bound hback
  | castDepths hn hm tree =>
      simp only [KuuNativeF45Tree.gk4acLeftRank_cast]
      change tree.gk4acLeftRank + 0 ≤ tree.gk4acLeftRank
      omega
  | trans left right ihLeft ihRight =>
      have hb : left.gk4zBackwardCount + right.gk4zBackwardCount = 0 := hback
      have hl := ihLeft (by omega)
      have hr := ihRight (by omega)
      change _ + (left.rotationCount + right.rotationCount) ≤ _
      omega
  | leftContext path later ih =>
      have hr := ih hback
      have hleaf := path.gk4acLeafCount_eq
      have hcount :
          (KuuNativeF45Tree.DepthRotationRoute.leftContext path later).rotationCount =
            path.rotationCount := rfl
      rw [hcount]
      simp only [KuuNativeF45Tree.gk4acLeftRank_node]
      omega
  | rightContext earlier path ih =>
      have hr := ih hback
      have hcount :
          (KuuNativeF45Tree.DepthRotationRoute.rightContext earlier path).rotationCount =
            path.rotationCount := rfl
      rw [hcount]
      simp only [KuuNativeF45Tree.gk4acLeftRank_node]
      omega

/-- NO original F54 typed self-route can have positive physical
rotation count while all its ACTUAL backward witnesses are absent. -/
theorem KuuNativeF45Tree.DepthRotationRoute.gk4acNoBackward_self_zero
    (tree : KuuNativeF45Tree p n m ma pa mb pb)
    (route : KuuNativeF45Tree.DepthRotationRoute p tree tree)
    (hback : route.gk4zBackwardCount = 0) :
    route.rotationCount = 0 := by
  have hb := route.gk4acNoBackward_bound hback
  omega

#print axioms KuuNativeF45Tree.gk4acLeafCount
#print axioms KuuNativeF45Tree.gk4acLeftRank
#print axioms KuuNativeF45Tree.gk4acLeafCount_pos
#print axioms KuuNativeF45Tree.gk4acLeafCount_node
#print axioms KuuNativeF45Tree.gk4acLeftRank_node
#print axioms KuuNativeF45Tree.gk4acLeafCount_cast
#print axioms KuuNativeF45Tree.gk4acLeftRank_cast
#print axioms KuuNativeF45Tree.LocalRotation.gk4acLeafCount_eq
#print axioms KuuNativeF45Tree.LocalRotation.gk4acLeftRank_drop
#print axioms KuuNativeF45Tree.RotationEdge.gk4acForward_bound
#print axioms KuuNativeF45Tree.RotationEdge.gk4acLeafCount_eq
#print axioms KuuNativeF45Tree.RotationChain.gk4acLeafCount_eq
#print axioms KuuNativeF45Tree.RotationChain.gk4acNoBackward_bound
#print axioms KuuNativeF45Tree.DepthRotationRoute.gk4acLeafCount_eq
#print axioms KuuNativeF45Tree.DepthRotationRoute.gk4acNoBackward_bound
#print axioms KuuNativeF45Tree.DepthRotationRoute.gk4acNoBackward_self_zero

end ActualChainAndRoute
end
end Kuu.F112.Physical
