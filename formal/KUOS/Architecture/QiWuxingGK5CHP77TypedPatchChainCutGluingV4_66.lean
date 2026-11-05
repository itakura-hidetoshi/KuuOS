import KUOS.Architecture.QiWuxingGK5CHP77FiniteTypedPatchChainDescentV4_65
import Mathlib.Combinatorics.Quiver.Path
import Mathlib.CategoryTheory.Equivalence
import Mathlib.Tactic

/-!
Qi v4.66 — ORIGINAL P77 FINITE TYPED PATCH-CHAIN CUT AND GLUING.

Qi v4.65 proved source-faithful Type-valued descent for every
finite dependent F55/P77 raw-four-cell patch chain. The next
logical step is to formalize typed chain concatenation at an
ACTUAL intermediate FivefoldPathVertex, transport the original
GK5CG Type-valued local patch witnesses through the cut, and
show compatibility iff at the two parts.

The original source free paths of the glued chain equal the
genuine composition of the two recovered source paths, and the
original P77 conservative quotient target equals the actual
vertical composition of the two separately evaluated raw
four-proof chains. An existing v4.62 partial source-certified
recovery restores this concatenated path without inventing
any new inverse source edges or target paths.

Only genuine source-certified patch chains descend. A failed
component blocks the designated factorwise gluing; a recovered
whole-target composite DOES NOT imply that arbitrary chosen
intermediate original P77 target Homs are source-reachable.
Do not identify five-cells with charge observations or the
physical north C60 gauge. No general sheaf descent, Gray,
new pentagonator or quasi-inverse definitional equality.

Append-only, same-root, root107. Strict 空 central, independent
Kuu one presentation. Original F55/P77/P94A, C60 physical
gauge and CRT remain separate authorities. No new axioms,
sorry, admit or native_decide. Lean v4.30.0-rc2,
pinned mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected validation-only PR #1558 Draft/open/unmerged.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace KUOS.Architecture.WuxingPentagonUnified
open KUOS.Architecture.WuxingCyclicPaths
open Kuu.F112.Physical
open CategoryTheory

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {p : Polygon} {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r₀ r₁ r₂ r₃ r₄ :
  KuuNativeF45Tree.DepthRotationRoute p first last}
variable
  (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
  (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
  (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
  (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄)

/-- Typed concatenation of arbitrary original F55/P77 raw
patch chains. Its cut is a real intermediate FivefoldPathVertex,
not an untyped list boundary or charge-derived proxy. -/
def fivefoldP77RawPatchChainAppend
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄)
    {u v w : FivefoldPathVertex}
    (left : FivefoldP77RawPatchChain f g h k u v)
    (right : FivefoldP77RawPatchChain f g h k v w) :
    FivefoldP77RawPatchChain f g h k u w :=
  match left with
  | .nil _ => right
  | .cons block tail =>
      .cons block (fivefoldP77RawPatchChainAppend f g h k tail right)

/-- The empty original patch chain is a strict left unit. -/
theorem fivefoldP77RawPatchChainAppend_nil
    {u v : FivefoldPathVertex}
    (right : FivefoldP77RawPatchChain f g h k u v) :
    fivefoldP77RawPatchChainAppend f g h k (.nil u) right = right :=
  rfl

/-- Genuinely typed chain concatenation is associative even
when all intermediate source vertices and original raw patches
are retained. -/
theorem fivefoldP77RawPatchChainAppend_assoc
    {u v w t : FivefoldPathVertex}
    (left : FivefoldP77RawPatchChain f g h k u v)
    (middle : FivefoldP77RawPatchChain f g h k v w)
    (right : FivefoldP77RawPatchChain f g h k w t) :
    fivefoldP77RawPatchChainAppend f g h k
      (fivefoldP77RawPatchChainAppend f g h k left middle) right =
    fivefoldP77RawPatchChainAppend f g h k left
      (fivefoldP77RawPatchChainAppend f g h k middle right) := by
  induction left with
  | nil _ => rfl
  | cons block tail ih =>
      exact congrArg
        (fun q => FivefoldP77RawPatchChain.cons block q) (ih middle)

/-- A true Type-valued chain source witness can be glued from
the genuine dependent witnesses of its two halves. -/
def fivefoldP77RawPatchChainAppendWitness
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄)
    {u v w : FivefoldPathVertex}
    (left : FivefoldP77RawPatchChain f g h k u v)
    (right : FivefoldP77RawPatchChain f g h k v w) :
    FivefoldP77RawPatchChainWitness f g h k left →
    FivefoldP77RawPatchChainWitness f g h k right →
    FivefoldP77RawPatchChainWitness f g h k
      (fivefoldP77RawPatchChainAppend f g h k left right) := by
  induction left with
  | nil _ =>
      intro _ wRight
      exact wRight
  | cons block tail ih =>
      intro wLeft wRight
      exact (wLeft.1, ih right wLeft.2 wRight)

/-- Exact original Type-valued local compatibility at a cut:
the glued chain is compatible IFF BOTH original component chains
carry all their own GK5CG five-cell patch certificates. -/
theorem fivefoldP77RawPatchChainAppend_compatible_iff
    {u v w : FivefoldPathVertex}
    (left : FivefoldP77RawPatchChain f g h k u v)
    (right : FivefoldP77RawPatchChain f g h k v w) :
    fivefoldP77RawPatchChainCompatible f g h k
      (fivefoldP77RawPatchChainAppend f g h k left right) ↔
    fivefoldP77RawPatchChainCompatible f g h k left ∧
      fivefoldP77RawPatchChainCompatible f g h k right := by
  induction left with
  | nil _ =>
      change
        fivefoldP77RawPatchChainCompatible f g h k right ↔
          True ∧ fivefoldP77RawPatchChainCompatible f g h k right
      simp
  | cons block tail ih =>
      change
        (fivefoldP77RawPatchBlockCompatible f g h k block ∧
          fivefoldP77RawPatchChainCompatible f g h k
            (fivefoldP77RawPatchChainAppend f g h k tail right)) ↔
        ((fivefoldP77RawPatchBlockCompatible f g h k block ∧
          fivefoldP77RawPatchChainCompatible f g h k tail) ∧
          fivefoldP77RawPatchChainCompatible f g h k right)
      rw [ih]
      tauto

/-- Arbitrarily long finite source patch paths transport through
a typed cut by ACTUAL path composition, not charge addition. -/
theorem fivefoldP77RawPatchChainAppend_path
    {u v w : FivefoldPathVertex}
    (left : FivefoldP77RawPatchChain f g h k u v)
    (right : FivefoldP77RawPatchChain f g h k v w) :
    ∀ (wLeft : FivefoldP77RawPatchChainWitness f g h k left)
      (wRight : FivefoldP77RawPatchChainWitness f g h k right),
      fivefoldP77RawPatchChainPath f g h k
        (fivefoldP77RawPatchChainAppend f g h k left right)
        (fivefoldP77RawPatchChainAppendWitness
          f g h k left right wLeft wRight) =
      (fivefoldP77RawPatchChainPath f g h k left wLeft).comp
        (fivefoldP77RawPatchChainPath f g h k right wRight) := by
  induction left with
  | nil vertex =>
      intro _ wRight
      change
        fivefoldP77RawPatchChainPath f g h k right wRight =
          (Quiver.Path.nil : Quiver.Path vertex vertex).comp
            (fivefoldP77RawPatchChainPath f g h k right wRight)
      exact (Quiver.Path.nil_comp _).symm
  | cons block tail ih =>
      intro wLeft wRight
      rcases wLeft with ⟨head, rest⟩
      change
        head.val.comp
          (fivefoldP77RawPatchChainPath f g h k
            (fivefoldP77RawPatchChainAppend f g h k tail right)
            (fivefoldP77RawPatchChainAppendWitness
              f g h k tail right rest wRight)) =
        (head.val.comp (fivefoldP77RawPatchChainPath f g h k tail rest)).comp
          (fivefoldP77RawPatchChainPath f g h k right wRight)
      rw [ih right rest wRight]
      exact (Quiver.Path.comp_assoc _ _ _).symm

/-- Genuine original P77 conservative quotient after a cut:
the whole glued raw-four-cell chain equals original P77 vertical
composition of its two separately source-certified halves. -/
theorem fivefoldP77RawPatchChainAppend_target
    {u v w : FivefoldPathVertex}
    (left : FivefoldP77RawPatchChain f g h k u v)
    (right : FivefoldP77RawPatchChain f g h k v w)
    (wLeft : FivefoldP77RawPatchChainWitness f g h k left)
    (wRight : FivefoldP77RawPatchChainWitness f g h k right) :
    fivefoldP77RawPatchChainTarget f g h k
      (fivefoldP77RawPatchChainAppend f g h k left right) =
    fivefoldP77ConservativeCompose f g h k
      (fivefoldP77RawPatchChainTarget f g h k left)
      (fivefoldP77RawPatchChainTarget f g h k right) := by
  letI := fivefoldP77ConservativeCategory f g h k
  let joined := fivefoldP77RawPatchChainAppend f g h k left right
  let fullWitness :=
    fivefoldP77RawPatchChainAppendWitness f g h k left right wLeft wRight
  let leftPath := fivefoldP77RawPatchChainPath f g h k left wLeft
  let rightPath := fivefoldP77RawPatchChainPath f g h k right wRight
  let FF := fivefoldP77ConservativeFunctor f g h k
  have hPath : fivefoldP77RawPatchChainPath f g h k joined fullWitness =
      leftPath.comp rightPath :=
    fivefoldP77RawPatchChainAppend_path f g h k left right wLeft wRight
  have hEval : FF.map
      (fivefoldP77RawPatchChainPath f g h k joined fullWitness) =
        fivefoldP77RawPatchChainTarget f g h k joined :=
    fivefoldP77RawPatchChainPath_eval f g h k joined fullWitness
  have hL : FF.map leftPath =
      fivefoldP77RawPatchChainTarget f g h k left :=
    fivefoldP77RawPatchChainPath_eval f g h k left wLeft
  have hR : FF.map rightPath =
      fivefoldP77RawPatchChainTarget f g h k right :=
    fivefoldP77RawPatchChainPath_eval f g h k right wRight
  have hComp : FF.map (leftPath.comp rightPath) =
      fivefoldP77ConservativeCompose f g h k
        (fivefoldP77RawPatchChainTarget f g h k left)
        (fivefoldP77RawPatchChainTarget f g h k right) := by
    calc
      FF.map (leftPath.comp rightPath) =
          FF.map leftPath ≫ FF.map rightPath := FF.map_comp _ _
      _ = fivefoldP77ConservativeCompose f g h k
          (fivefoldP77RawPatchChainTarget f g h k left)
          (fivefoldP77RawPatchChainTarget f g h k right) := by
        rw [hL, hR]
        rfl
  exact hEval.symm.trans
    ((congrArg (fun path : Quiver.Path u w => FF.map path) hPath).trans hComp)

/-- The full original P77 source-certified value after gluing
is the vertical composite of the underlying REAL target
four-proof quotient classes of the separate certified chains. -/
theorem fivefoldP77RawPatchChainAppend_certified_val
    {u v w : FivefoldPathVertex}
    (left : FivefoldP77RawPatchChain f g h k u v)
    (right : FivefoldP77RawPatchChain f g h k v w)
    (wLeft : FivefoldP77RawPatchChainWitness f g h k left)
    (wRight : FivefoldP77RawPatchChainWitness f g h k right) :
    (fivefoldP77RawPatchChainCertified f g h k
      (fivefoldP77RawPatchChainAppend f g h k left right)
      (fivefoldP77RawPatchChainAppendWitness
        f g h k left right wLeft wRight)).val =
    fivefoldP77ConservativeCompose f g h k
      (fivefoldP77RawPatchChainCertified f g h k left wLeft).val
      (fivefoldP77RawPatchChainCertified f g h k right wRight).val := by
  rw [fivefoldP77RawPatchChainCertified_val,
    fivefoldP77RawPatchChainCertified_val,
    fivefoldP77RawPatchChainCertified_val]
  exact fivefoldP77RawPatchChainAppend_target f g h k left right wLeft wRight

/-- Source recovery of the WHOLE glued partial domain is the
actual composition of both previously source-certified paths. -/
theorem fivefoldP77RawPatchChainAppend_recover
    {u v w : FivefoldPathVertex}
    (left : FivefoldP77RawPatchChain f g h k u v)
    (right : FivefoldP77RawPatchChain f g h k v w)
    (wLeft : FivefoldP77RawPatchChainWitness f g h k left)
    (wRight : FivefoldP77RawPatchChainWitness f g h k right) :
    fivefoldP77PartialRecoverPath f g h k
      (fivefoldP77RawPatchChainCertified f g h k
        (fivefoldP77RawPatchChainAppend f g h k left right)
        (fivefoldP77RawPatchChainAppendWitness
          f g h k left right wLeft wRight)) =
      (fivefoldP77RawPatchChainPath f g h k left wLeft).comp
        (fivefoldP77RawPatchChainPath f g h k right wRight) := by
  exact
    (fivefoldP77RawPatchChainCertified_recover f g h k
      (fivefoldP77RawPatchChainAppend f g h k left right)
      (fivefoldP77RawPatchChainAppendWitness
        f g h k left right wLeft wRight)).trans
      (fivefoldP77RawPatchChainAppend_path f g h k left right wLeft wRight)

/-- Failed genuine local Type-valued evidence on the LEFT of
a cut obstructs only that designated factorwise glued chain. -/
theorem fivefoldP77RawPatchChainAppend_left_obstruction
    {u v w : FivefoldPathVertex}
    (left : FivefoldP77RawPatchChain f g h k u v)
    (right : FivefoldP77RawPatchChain f g h k v w)
    (hmissing : ¬ fivefoldP77RawPatchChainCompatible f g h k left) :
    ¬ fivefoldP77RawPatchChainCompatible f g h k
      (fivefoldP77RawPatchChainAppend f g h k left right) := by
  intro hc
  exact hmissing
    ((fivefoldP77RawPatchChainAppend_compatible_iff
      f g h k left right).1 hc).1

/-- The corresponding genuine RIGHT local Type-valued failure
also obstructs the designated source-factorized glued chain. -/
theorem fivefoldP77RawPatchChainAppend_right_obstruction
    {u v w : FivefoldPathVertex}
    (left : FivefoldP77RawPatchChain f g h k u v)
    (right : FivefoldP77RawPatchChain f g h k v w)
    (hmissing : ¬ fivefoldP77RawPatchChainCompatible f g h k right) :
    ¬ fivefoldP77RawPatchChainCompatible f g h k
      (fivefoldP77RawPatchChainAppend f g h k left right) := by
  intro hc
  exact hmissing
    ((fivefoldP77RawPatchChainAppend_compatible_iff
      f g h k left right).1 hc).2

#print axioms fivefoldP77RawPatchChainAppend
#print axioms fivefoldP77RawPatchChainAppend_nil
#print axioms fivefoldP77RawPatchChainAppend_assoc
#print axioms fivefoldP77RawPatchChainAppendWitness
#print axioms fivefoldP77RawPatchChainAppend_compatible_iff
#print axioms fivefoldP77RawPatchChainAppend_path
#print axioms fivefoldP77RawPatchChainAppend_target
#print axioms fivefoldP77RawPatchChainAppend_certified_val
#print axioms fivefoldP77RawPatchChainAppend_recover
#print axioms fivefoldP77RawPatchChainAppend_left_obstruction
#print axioms fivefoldP77RawPatchChainAppend_right_obstruction

end
end KUOS.Architecture.WuxingPentagonUnified
