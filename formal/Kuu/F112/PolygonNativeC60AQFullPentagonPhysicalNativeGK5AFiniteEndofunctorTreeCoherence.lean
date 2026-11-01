import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4BZFiveTargetTwoUnitCoherence
import Mathlib.CategoryTheory.EqToHom
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK5A — Inductive arbitrary finite endofunctor-tree
coherence for the ACTUAL GK4BM arbitrary-choice inverse comparison.

GK4BZ proves all fourteen real five-stage Catalan vertices. This file
now constructs a true Mathlib NatIso for EVERY finite binary tree of
composable endofunctors of one genuine target category T; leaf nodes
carry actual target functors, unit nodes carry the real identity
functor, and internal nodes use GK4BW's ACTUAL typed binary pasting.

Structural induction proves each such whole NatIso EQUALS directly
constructed GK4BT Θ, with no new axioms. Actual GK4BU target
NatTrans modification is preserved for arbitrary pairs of tree
evaluations. A finite-list fold and leaf flattening yield a
canonical equality of target composites for any two trees with
the same ordered sequence of genuine leaves, and an explicit
eqToIso transport theorem identifies their whole chosen-inverse
NatIso after transporting both end functors.

This is bounded to existing genuine Mathlib functor categories.
No unconditional original F45 source faithfulness, source-Q
category laws, raw F54/F55/P92B Type-valued higher cells,
new Gray category, ambient integer-matrix reachability,
unrestricted higher hyperdescent, or definitional Q_T = P_T
is claimed. Strict 空 center; independent Kuu one presentation.

Append-only / tighten-only / overwrite-forbidden / same-root107.
Pinned Lean v4.30.0-rc2 and mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected validation-only PR #1558 remains Draft/OPEN/unmerged.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE uT vT

/-- Actual finite binary presentation of endofunctor target change:
unit = a real target identity, atom = an arbitrary real endofunctor,
paste = a genuine two-stage target composite. -/
inductive NativeGK5AFiniteTargetTree (T : Type uT) [Category.{vT} T] where
  | unit : NativeGK5AFiniteTargetTree T
  | atom (R : T ⥤ T) : NativeGK5AFiniteTargetTree T
  | paste (left right : NativeGK5AFiniteTargetTree T) : NativeGK5AFiniteTargetTree T

/-- Evaluate a finite target presentation in Mathlib's actual
endofunctor category, not in a fabricated raw high-cell category. -/
def nativeGK5ATreeComposite {T : Type uT} [Category.{vT} T] :
    NativeGK5AFiniteTargetTree T → T ⥤ T
  | .unit => 𝟭 T
  | .atom R => R
  | .paste left right => nativeGK5ATreeComposite left ⋙
      nativeGK5ATreeComposite right

/-- Underlying ordered leaves, ignoring formal identity nodes. -/
def nativeGK5ATreeLeaves {T : Type uT} [Category.{vT} T] :
    NativeGK5AFiniteTargetTree T → List (T ⥤ T)
  | .unit => []
  | .atom R => [R]
  | .paste left right => nativeGK5ATreeLeaves left ++ nativeGK5ATreeLeaves right

/-- A genuine right-associated composite for a finite ordered
list of target endofunctors; the empty word is the real identity. -/
def nativeGK5AListComposite {T : Type uT} [Category.{vT} T] :
    List (T ⥤ T) → T ⥤ T
  | [] => 𝟭 T
  | R :: rs => R ⋙ nativeGK5AListComposite rs

section FiniteTargetWords
variable {T : Type uT} [Category.{vT} T]

/-- A literal finite target word is compatible with concatenation,
as an equality of entire Mathlib endofunctors. -/
theorem nativeGK5AListComposite_append
    (xs ys : List (T ⥤ T)) :
    nativeGK5AListComposite (xs ++ ys) =
      nativeGK5AListComposite xs ⋙ nativeGK5AListComposite ys := by
  induction xs with
  | nil =>
      simp [nativeGK5AListComposite]
  | cons R xs ih =>
      change R ⋙ nativeGK5AListComposite (xs ++ ys) =
        (R ⋙ nativeGK5AListComposite xs) ⋙ nativeGK5AListComposite ys
      rw [ih]
      rfl

/-- Structural induction on the true binary presentation identifies
the whole composite with the finite ordered leaf-word composite. -/
theorem nativeGK5ATreeComposite_eq_list
    (t : NativeGK5AFiniteTargetTree T) :
    nativeGK5ATreeComposite t =
      nativeGK5AListComposite (nativeGK5ATreeLeaves t) := by
  induction t with
  | unit => rfl
  | atom R =>
      change R = R ⋙ 𝟭 T
      exact (Functor.comp_id R).symm
  | paste left right hl hr =>
      change nativeGK5ATreeComposite left ⋙
          nativeGK5ATreeComposite right =
        nativeGK5AListComposite
          (nativeGK5ATreeLeaves left ++ nativeGK5ATreeLeaves right)
      rw [hl, hr, nativeGK5AListComposite_append]

/-- Equal ordered leaves give equal whole target functors,
for arbitrary depths and arbitrary insertion of unit nodes. -/
theorem nativeGK5ATreeComposite_eq_of_leaves
    (left right : NativeGK5AFiniteTargetTree T)
    (h : nativeGK5ATreeLeaves left = nativeGK5ATreeLeaves right) :
    nativeGK5ATreeComposite left = nativeGK5ATreeComposite right := by
  rw [nativeGK5ATreeComposite_eq_list,
    nativeGK5ATreeComposite_eq_list, h]

/-- The right-associated genuine binary tree of a finite list. -/
def nativeGK5ATreeOfList : List (T ⥤ T) → NativeGK5AFiniteTargetTree T
  | [] => .unit
  | R :: rs => .paste (.atom R) (nativeGK5ATreeOfList rs)

/-- The actual interpretation of the canonical tree is the
strict whole Mathlib functor composite of its finite list. -/
theorem nativeGK5ATreeOfList_eval (rs : List (T ⥤ T)) :
    nativeGK5ATreeComposite (nativeGK5ATreeOfList rs) =
      nativeGK5AListComposite rs := by
  induction rs with
  | nil => rfl
  | cons R rs ih =>
      change R ⋙ nativeGK5ATreeComposite (nativeGK5ATreeOfList rs) =
        R ⋙ nativeGK5AListComposite rs
      rw [ih]

end FiniteTargetWords

section FiniteChosenInverseTree
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {T : Type uT} [Category.{vT} T]

/-- Recursively pasted ACTUAL GK4BW whole NatIso, one for EVERY
finite binary tree (not just the five-stage Catalan fourteen).
All internal nodes retain real associators, left/right whiskering
and both typed target-composition equality transports. -/
noncomputable def nativeGK5AChosenInverse_treeIso
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (t : NativeGK5AFiniteTargetTree T) :
    (nativeGK4BNPostcompCompatible p ma mb pa pb
        (nativeGK5ATreeComposite t) ⋙
      nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb) ≅
    (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙
      nativeGK4BNPostcompAttained p ma mb pa pb
        (nativeGK5ATreeComposite t)) :=
  match t with
  | .unit =>
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (𝟭 T)
  | .atom R =>
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb R
  | .paste left right =>
      nativeGK4BWChosenInverse_binaryPasting p ma mb pa pb
        (nativeGK5ATreeComposite left)
        (nativeGK5ATreeComposite right)
        (nativeGK5AChosenInverse_treeIso p ma mb pa pb left)
        (nativeGK5AChosenInverse_treeIso p ma mb pa pb right)

/-- Main GK5A: for EVERY finite genuine endofunctor tree, the
actually constructed recursive NatIso equals the direct GK4BT
chosen-inverse Θ as a WHOLE Mathlib NatIso, not just its components. -/
theorem nativeGK5AChosenInverse_treeIso_eq_direct
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (t : NativeGK5AFiniteTargetTree T) :
    nativeGK5AChosenInverse_treeIso p ma mb pa pb t =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb
        (nativeGK5ATreeComposite t) := by
  induction t with
  | unit => rfl
  | atom R => rfl
  | paste left right hl hr =>
      change nativeGK4BWChosenInverse_binaryPasting p ma mb pa pb
          (nativeGK5ATreeComposite left)
          (nativeGK5ATreeComposite right)
          (nativeGK5AChosenInverse_treeIso p ma mb pa pb left)
          (nativeGK5AChosenInverse_treeIso p ma mb pa pb right) =
        nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb
          (nativeGK5ATreeComposite left ⋙ nativeGK5ATreeComposite right)
      rw [hl, hr]
      exact
        (nativeGK4BWChosenInverse_binaryPasting_ofTheta p ma mb pa pb
          (nativeGK5ATreeComposite left) (nativeGK5ATreeComposite right)).trans
        (nativeGK4BVChosenInverse_composition_coherence p ma mb pa pb
          (nativeGK5ATreeComposite left) (nativeGK5ATreeComposite right))

/-- Genuine target-NatTrans MODIFICATION square for any pair of
finite trees and ANY real natural transformation between their
evaluated target endofunctors. -/
theorem nativeGK5AChosenInverse_treeNat_square
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (left right : NativeGK5AFiniteTargetTree T)
    (ρ : nativeGK5ATreeComposite left ⟶ nativeGK5ATreeComposite right) :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb ρ)
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb) ≫
      (nativeGK5AChosenInverse_treeIso p ma mb pa pb right).hom =
    (nativeGK5AChosenInverse_treeIso p ma mb pa pb left).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb ρ) := by
  simpa only [nativeGK5AChosenInverse_treeIso_eq_direct] using
    (nativeGK4BUChosenInverse_targetNat_square p ma mb pa pb ρ)

/-- Associative rebracketing of ANY three (already arbitrarily
deep) chosen-inverse target trees, as a whole NatIso equality. -/
theorem nativeGK5AChosenInverse_tree_assoc
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (left middle right : NativeGK5AFiniteTargetTree T) :
    nativeGK5AChosenInverse_treeIso p ma mb pa pb
      (.paste (.paste left middle) right) =
    nativeGK5AChosenInverse_treeIso p ma mb pa pb
      (.paste left (.paste middle right)) := by
  simp only [nativeGK5AChosenInverse_treeIso_eq_direct,
    nativeGK5ATreeComposite]
  all_goals rfl

/-- A real identity node inserted on the LEFT of an arbitrary
finite target tree does not affect its whole chosen-inverse NatIso. -/
theorem nativeGK5AChosenInverse_tree_leftUnit
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (t : NativeGK5AFiniteTargetTree T) :
    nativeGK5AChosenInverse_treeIso p ma mb pa pb
      (.paste .unit t) =
    nativeGK5AChosenInverse_treeIso p ma mb pa pb t := by
  simp only [nativeGK5AChosenInverse_treeIso_eq_direct,
    nativeGK5ATreeComposite, Functor.id_comp]

/-- A real identity node inserted on the RIGHT of an arbitrary
finite target tree does not affect its whole chosen-inverse NatIso. -/
theorem nativeGK5AChosenInverse_tree_rightUnit
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (t : NativeGK5AFiniteTargetTree T) :
    nativeGK5AChosenInverse_treeIso p ma mb pa pb
      (.paste t .unit) =
    nativeGK5AChosenInverse_treeIso p ma mb pa pb t := by
  simp only [nativeGK5AChosenInverse_treeIso_eq_direct,
    nativeGK5ATreeComposite, Functor.comp_id]

/-- TRUE target-level equality-transport coherence for arbitrary
F=G of genuine Mathlib endofunctors. Both boundary eqToIso
transports are kept; no definitional equality of Q and P is used. -/
theorem nativeGK5AChosenInverse_eqTransport
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (F G : T ⥤ T) (h : F = G) :
    eqToIso (congrArg
        (fun K : T ⥤ T =>
          nativeGK4BNPostcompCompatible p ma mb pa pb K ⋙
            nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb) h) ≪≫
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb G ≪≫
      eqToIso (congrArg
        (fun K : T ⥤ T =>
          nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙
            nativeGK4BNPostcompAttained p ma mb pa pb K) h.symm) =
    nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb F := by
  cases h
  simp

/-- GLOBAL FINITE-TREE PRESENTATION COHERENCE: for arbitrary finite
depth, bracketings and inserted units, equal ordered leaf words imply
equality of recursively pasted *WHOLE* NatIso after the two actual
Mathlib equality transports on both ends. This is a scoped
finite-context theorem, not a new raw Gray/hyperdescent structure. -/
theorem nativeGK5AChosenInverse_sameLeaves_transport
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (left right : NativeGK5AFiniteTargetTree T)
    (h : nativeGK5ATreeLeaves left = nativeGK5ATreeLeaves right) :
    eqToIso (congrArg
        (fun K : T ⥤ T =>
          nativeGK4BNPostcompCompatible p ma mb pa pb K ⋙
            nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK5ATreeComposite_eq_of_leaves left right h)) ≪≫
      nativeGK5AChosenInverse_treeIso p ma mb pa pb right ≪≫
      eqToIso (congrArg
        (fun K : T ⥤ T =>
          nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙
            nativeGK4BNPostcompAttained p ma mb pa pb K)
        (nativeGK5ATreeComposite_eq_of_leaves left right h).symm) =
    nativeGK5AChosenInverse_treeIso p ma mb pa pb left := by
  simp only [nativeGK5AChosenInverse_treeIso_eq_direct]
  exact nativeGK5AChosenInverse_eqTransport p ma mb pa pb
    (nativeGK5ATreeComposite left)
    (nativeGK5ATreeComposite right)
    (nativeGK5ATreeComposite_eq_of_leaves left right h)

end FiniteChosenInverseTree

#print axioms nativeGK5ATreeComposite
#print axioms nativeGK5ATreeLeaves
#print axioms nativeGK5AListComposite
#print axioms nativeGK5AListComposite_append
#print axioms nativeGK5ATreeComposite_eq_list
#print axioms nativeGK5ATreeComposite_eq_of_leaves
#print axioms nativeGK5ATreeOfList
#print axioms nativeGK5ATreeOfList_eval
#print axioms nativeGK5AChosenInverse_treeIso
#print axioms nativeGK5AChosenInverse_treeIso_eq_direct
#print axioms nativeGK5AChosenInverse_treeNat_square
#print axioms nativeGK5AChosenInverse_tree_assoc
#print axioms nativeGK5AChosenInverse_tree_leftUnit
#print axioms nativeGK5AChosenInverse_tree_rightUnit
#print axioms nativeGK5AChosenInverse_eqTransport
#print axioms nativeGK5AChosenInverse_sameLeaves_transport

end
end Kuu.F112.Physical
