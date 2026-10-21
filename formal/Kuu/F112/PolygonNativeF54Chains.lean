import Kuu.F112.PolygonNativeF54Rotation

/-!
# F112-E7N / original-shaped bidirectional F54 rotation edges/chains

E7M reconstructed the Type-valued native-category C60-sector
original-shaped F54 LocalRotation, including TWO independent
Nat.add_assoc casts, both original finite-path Blocks axes, both
proof-relevant primitive AxisTrace histories, and arbitrary typed
left/right binary-tree contexts.

The historical F54 next retains each forward local reassociation or
a backward reversal as a SPECIFIC Type-valued RotationEdge, and
assembles arbitrary FINITE RotationChain terms with all intermediate
original F45 trees. We reconstruct that exact COMBINATORIAL SHAPE
on the new independent E7M source.

Raw reversal is not equated to an identity proof. We prove concatenation
and reversal, genuine rotation count, count under concatenation,
preservation of the ordered real C60 sector list and the exact
double-Nat-indexed E7A physical-sector projection.

This is NOT a verified equivalence to the old KUOS F54 original route
source, and DOES NOT claim unproved equality of old F19/F28 raw
within-axis histories. No KUOS.*, Gray, F51 or F77 imports.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- An actual proof-relevant original-shaped elementary rotation
with its forward/backward orientation explicitly retained.
An arbitrary category-associator Hom equality is NOT a constructor. -/
inductive KuuNativeF45Tree.RotationEdge (p : Polygon) :
    ∀ {a b : D} {x y : E} {n m : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y},
      KuuNativeF45Tree p n m ma pa mb pb →
      KuuNativeF45Tree p n m ma pa mb pb →
      Type (max (max uD uE) (max vD vE)) where
  | forward
      {a b : D} {x y : E} {n m : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {before after : KuuNativeF45Tree p n m ma pa mb pb}
      (step : KuuNativeF45Tree.LocalRotation p before after) :
      RotationEdge p before after
  | backward
      {a b : D} {x y : E} {n m : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {before after : KuuNativeF45Tree p n m ma pa mb pb}
      (step : KuuNativeF45Tree.LocalRotation p before after) :
      RotationEdge p after before

/-- Reverse an ACTUAL stored local rotation witness without
fabricating an arbitrary inverse between unrelated native trees. -/
def KuuNativeF45Tree.RotationEdge.reverse
    {p : Polygon} {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (edge : KuuNativeF45Tree.RotationEdge p before after) :
    KuuNativeF45Tree.RotationEdge p after before := by
  cases edge with
  | forward step =>
      exact .backward step
  | backward step =>
      exact .forward step

/-- Reversing a specifically witnessed rotation twice recovers
the EXACT raw edge constructor, not only its category image. -/
theorem KuuNativeF45Tree.RotationEdge.reverse_reverse
    {p : Polygon} {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (edge : KuuNativeF45Tree.RotationEdge p before after) :
    edge.reverse.reverse = edge := by
  cases edge <;> rfl

/-- Each ACTUAL directed original-shaped rotation preserves the
complete actual ordered physical sector list even if reversed. -/
theorem KuuNativeF45Tree.RotationEdge.sectors_eq
    {p : Polygon} {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (edge : KuuNativeF45Tree.RotationEdge p before after) :
    before.sectors = after.sectors := by
  cases edge with
  | forward step =>
      exact step.sectors_eq
  | backward step =>
      exact step.sectors_eq.symm

/-- Type-valued finite sequences of ACTUAL native-F45 rotation
witnesses, retaining ALL intermediate differently parenthesized
original-shaped Blocks/AxisTrace source terms. -/
inductive KuuNativeF45Tree.RotationChain (p : Polygon) :
    ∀ {a b : D} {x y : E} {n m : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y},
      KuuNativeF45Tree p n m ma pa mb pb →
      KuuNativeF45Tree p n m ma pa mb pb →
      Type (max (max uD uE) (max vD vE)) where
  | refl
      {a b : D} {x y : E} {n m : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      (tree : KuuNativeF45Tree p n m ma pa mb pb) :
      RotationChain p tree tree
  | snoc
      {a b : D} {x y : E} {n m : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first middle last : KuuNativeF45Tree p n m ma pa mb pb}
      (prior : RotationChain p first middle)
      (edge : KuuNativeF45Tree.RotationEdge p middle last) :
      RotationChain p first last

/-- Count exactly the actual original-shaped physical local rotation
edges, including repetitions and honest nontrivial backtracks. -/
def KuuNativeF45Tree.RotationChain.length
    {p : Polygon} {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first last : KuuNativeF45Tree p n m ma pa mb pb} :
    KuuNativeF45Tree.RotationChain p first last → Nat
  | .refl _ => 0
  | .snoc chain _ => chain.length + 1

/-- Strictly typed concatenation: the two complete intermediate
original-shaped block carriers and both Nat indices MUST match. -/
def KuuNativeF45Tree.RotationChain.append
    {p : Polygon} {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first middle last : KuuNativeF45Tree p n m ma pa mb pb}
    (left : KuuNativeF45Tree.RotationChain p first middle)
    (right : KuuNativeF45Tree.RotationChain p middle last) :
    KuuNativeF45Tree.RotationChain p first last := by
  induction right with
  | refl =>
      exact left
  | snoc right edge ih =>
      exact .snoc ih edge

theorem KuuNativeF45Tree.RotationChain.length_append
    {p : Polygon} {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first middle last : KuuNativeF45Tree p n m ma pa mb pb}
    (left : KuuNativeF45Tree.RotationChain p first middle)
    (right : KuuNativeF45Tree.RotationChain p middle last) :
    (left.append right).length = left.length + right.length := by
  induction right with
  | refl =>
      rfl
  | snoc right edge ih =>
      simpa only [KuuNativeF45Tree.RotationChain.append,
        KuuNativeF45Tree.RotationChain.length,
        Nat.add_succ] using congrArg Nat.succ ih

/-- Reverse an arbitrary finite original-shaped chain, preserving
each actual rotation witness and reversing every edge in order. -/
def KuuNativeF45Tree.RotationChain.reverse
    {p : Polygon} {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first last : KuuNativeF45Tree p n m ma pa mb pb}
    (chain : KuuNativeF45Tree.RotationChain p first last) :
    KuuNativeF45Tree.RotationChain p last first := by
  induction chain with
  | refl =>
      exact .refl _
  | snoc chain edge ih =>
      exact
        (KuuNativeF45Tree.RotationChain.snoc (.refl _) edge.reverse).append ih

/-- No raw cancellation under reversal: even a genuine immediate
backtrack has length two, despite returning to its source object. -/
theorem KuuNativeF45Tree.RotationChain.length_reverse
    {p : Polygon} {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first last : KuuNativeF45Tree p n m ma pa mb pb}
    (chain : KuuNativeF45Tree.RotationChain p first last) :
    chain.reverse.length = chain.length := by
  induction chain with
  | refl =>
      rfl
  | snoc chain edge ih =>
      change
        ((KuuNativeF45Tree.RotationChain.snoc
          (KuuNativeF45Tree.RotationChain.refl _) edge.reverse).append
          chain.reverse).length = chain.length + 1
      rw [KuuNativeF45Tree.RotationChain.length_append, ih]
      change 1 + chain.length = chain.length + 1
      exact Nat.add_comm _ _

/-- Every arbitrary-length original-shaped finite local rotation
chain preserves ALL actual C60 sector witnesses and their order. -/
theorem KuuNativeF45Tree.RotationChain.sectors_eq
    {p : Polygon} {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first last : KuuNativeF45Tree p n m ma pa mb pb}
    (chain : KuuNativeF45Tree.RotationChain p first last) :
    first.sectors = last.sectors := by
  induction chain with
  | refl =>
      rfl
  | snoc chain edge ih =>
      exact ih.trans edge.sectors_eq

/-- The physical C60 sector projection retains the complete source
list across any arbitrary bidirectional genuine native rotation chain.
No equality of historical old-F54 proof trees is asserted. -/
theorem KuuNativeF45Tree.RotationChain.physical_leaves_eq
    {p : Polygon} {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first last : KuuNativeF45Tree p n m ma pa mb pb}
    (chain : KuuNativeF45Tree.RotationChain p first last) :
    first.erasePhysical.erase.leaves =
      last.erasePhysical.erase.leaves := by
  calc
    first.erasePhysical.erase.leaves = first.sectors :=
      first.erasePhysical_leaves
    _ = last.sectors := chain.sectors_eq
    _ = last.erasePhysical.erase.leaves :=
      last.erasePhysical_leaves.symm

/-- An ACTUAL north C60 original-shaped F45 three-sector local
rotation followed by its ACTUAL reverse; raw proof data remain. -/
def northNativeF45TripleBacktrack :
    KuuNativeF45Tree.RotationChain (.pentagon .north)
      (KuuNativeF45Tree.castDepths
        (Nat.add_assoc 1 1 1) (Nat.add_assoc 1 1 1)
        (KuuNativeF45Tree.node
          (KuuNativeF45Tree.node
            northNativeF45FirstStage northNativeF45SecondStage)
          northNativeF45ThirdStage))
      (KuuNativeF45Tree.castDepths
        (Nat.add_assoc 1 1 1) (Nat.add_assoc 1 1 1)
        (KuuNativeF45Tree.node
          (KuuNativeF45Tree.node
            northNativeF45FirstStage northNativeF45SecondStage)
          northNativeF45ThirdStage)) :=
  .snoc
    (.snoc (.refl _) (.forward northNativeF45TripleRotation))
    (.backward northNativeF45TripleRotation)

/-- An immediate forward/backward original-shaped path still has
TWO rotation edges, rather than collapsing to a raw identity. -/
theorem northNativeF45TripleBacktrack_length :
    northNativeF45TripleBacktrack.length = 2 := by
  rfl

/-- Source proof relevance is strict: the backtrack is NOT equal
to the raw zero-length constructor on the same F45 native tree. -/
theorem northNativeF45TripleBacktrack_ne_refl :
    northNativeF45TripleBacktrack ≠
      (KuuNativeF45Tree.RotationChain.refl
        (KuuNativeF45Tree.castDepths
          (Nat.add_assoc 1 1 1) (Nat.add_assoc 1 1 1)
          (KuuNativeF45Tree.node
            (KuuNativeF45Tree.node
              northNativeF45FirstStage northNativeF45SecondStage)
            northNativeF45ThirdStage))) := by
  intro h
  have hc := congrArg KuuNativeF45Tree.RotationChain.length h
  change (2 : Nat) = 0 at hc
  exact (by decide : (2 : Nat) ≠ 0) hc

#print axioms KuuNativeF45Tree.RotationEdge
#print axioms KuuNativeF45Tree.RotationEdge.reverse_reverse
#print axioms KuuNativeF45Tree.RotationEdge.sectors_eq
#print axioms KuuNativeF45Tree.RotationChain
#print axioms KuuNativeF45Tree.RotationChain.length_append
#print axioms KuuNativeF45Tree.RotationChain.reverse
#print axioms KuuNativeF45Tree.RotationChain.length_reverse
#print axioms KuuNativeF45Tree.RotationChain.sectors_eq
#print axioms KuuNativeF45Tree.RotationChain.physical_leaves_eq
#print axioms northNativeF45TripleBacktrack_length
#print axioms northNativeF45TripleBacktrack_ne_refl
end
end Kuu.F112.Physical
