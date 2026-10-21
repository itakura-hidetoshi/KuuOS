import Kuu.F112.PolygonNativeBlocks

/-!
# F112-E7K / genuine original-shaped OneStep and exact AxisTrace grammar

The historical F41/F45 source has three primitive block refinements:
splitting one actual native categorical path at a chosen breakpoint,
inserting one independent empty native block, and right-context
whiskering of an original refinement. It has NO freely invented
conversion between arbitrary equal numerical evaluations.

E7I reconstructs truly finite, category-polymorphic native paths
and subdivision Blocks. This file reconstructs the exact same THREE
shapes of primitive moves in a NEW Type-valued Kuu source, retaining
both the original categorical arrow paths and their subdivision
boundaries.

An arbitrary exactly-n-step axis history is an explicitly dependent
Type-valued sequence of those actual refinements, not a mere Nat or
a Prop stating that refinements exist. We prove preservation of the
whole flattened native path and its categorical evaluation, source
history concatenation, right-context closure, and a concrete
nontrivial one-step empty-block refinement.

This source is original-shaped but not identified with the frozen
historical F19 StrongTrans.Modification or original F28
compression-kernel AxisTrace. No KUOS.*, Gray, F51 or F77 imports.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe u v
variable {C : Type u} [Category.{v} C]

/-- The THREE actual original-shaped F41 elementary block moves,
retaining all source partition data, rather than only composite
equality of the original category. This new presentation is in Type. -/
inductive KuuNativeOneStep :
    ∀ {x y : C}, KuuNativeBlocks x y →
      KuuNativeBlocks x y → Type (max u v) where
  | split {w x y z : C}
      (p : KuuNativeBlocks w x)
      (q : KuuNativePath x y)
      (r : KuuNativePath y z) :
      KuuNativeOneStep
        (.snoc p (q.append r)) (.snoc (.snoc p q) r)
  | insertNil {x y : C} (p : KuuNativeBlocks x y) :
      KuuNativeOneStep p (.snoc p (.nil y))
  | whisker {x y z : C}
      {p q : KuuNativeBlocks x y}
      (h : KuuNativeOneStep p q) (t : KuuNativePath y z) :
      KuuNativeOneStep (.snoc p t) (.snoc q t)

/-- Each elementary original-shaped F41 refinement preserves
EXACTLY the original ordered finite native categorical arrow path;
this is stronger than equality of its final composite Hom. -/
theorem KuuNativeOneStep.flatten_eq
    {x y : C} {p q : KuuNativeBlocks x y}
    (h : KuuNativeOneStep p q) :
    p.flatten = q.flatten := by
  induction h with
  | split p q r =>
      simp only [KuuNativeBlocks.flatten]
      exact (KuuNativePath.append_assoc p.flatten q r).symm
  | insertNil p =>
      simp only [KuuNativeBlocks.flatten, KuuNativePath.append]
  | whisker h t ih =>
      simpa only [KuuNativeBlocks.flatten] using
        congrArg (fun z => z.append t) ih

/-- Actual category semantics is preserved for EACH primitive
refinement, derived from the independently PROVED flattening law. -/
theorem KuuNativeOneStep.composite_eq
    {x y : C} {p q : KuuNativeBlocks x y}
    (h : KuuNativeOneStep p q) :
    p.composite = q.composite := by
  calc
    p.composite = p.flatten.composite :=
      KuuNativeBlocks.composite_eq_flatten p
    _ = q.flatten.composite :=
      congrArg KuuNativePath.composite h.flatten_eq
    _ = q.composite :=
      (KuuNativeBlocks.composite_eq_flatten q).symm

/-- EXACTLY n original-shaped primitive steps between the two
specified native block partitions, with ALL intermediate source
proof trees carried at their typed original endpoints. -/
inductive KuuNativeAxisTrace :
    ∀ {x y : C}, Nat → KuuNativeBlocks x y →
      KuuNativeBlocks x y → Type (max u v) where
  | refl {x y : C} (p : KuuNativeBlocks x y) :
      KuuNativeAxisTrace 0 p p
  | snoc {x y : C} {n : Nat}
      {p q r : KuuNativeBlocks x y}
      (h : KuuNativeAxisTrace n p q)
      (step : KuuNativeOneStep q r) :
      KuuNativeAxisTrace (n + 1) p r

/-- Every single intermediate original native categorical arrow in
ANY complete n-step history stays in its original order. -/
theorem KuuNativeAxisTrace.flatten_eq
    {x y : C} {n : Nat} {p q : KuuNativeBlocks x y}
    (h : KuuNativeAxisTrace n p q) :
    p.flatten = q.flatten := by
  induction h with
  | refl p => rfl
  | snoc h step ih =>
      exact ih.trans step.flatten_eq

/-- The original categorical composite is invariant under any
finite exactly-n-step genuinely proof-relevant refinement history. -/
theorem KuuNativeAxisTrace.composite_eq
    {x y : C} {n : Nat} {p q : KuuNativeBlocks x y}
    (h : KuuNativeAxisTrace n p q) :
    p.composite = q.composite := by
  calc
    p.composite = p.flatten.composite :=
      KuuNativeBlocks.composite_eq_flatten p
    _ = q.flatten.composite :=
      congrArg KuuNativePath.composite h.flatten_eq
    _ = q.composite :=
      (KuuNativeBlocks.composite_eq_flatten q).symm

/-- Independent source-axis concatenation keeps exactly n+m
original native primitive moves and does not identify intermediate
block subdivisions with mere equality of categorical arrows. -/
def KuuNativeAxisTrace.append
    {x y : C} {n m : Nat}
    {p q r : KuuNativeBlocks x y}
    (h : KuuNativeAxisTrace n p q)
    (k : KuuNativeAxisTrace m q r) :
    KuuNativeAxisTrace (n + m) p r := by
  induction k with
  | refl p =>
      simpa only [Nat.add_zero] using h
  | snoc k step ih =>
      simpa only [Nat.add_succ] using
        (KuuNativeAxisTrace.snoc (ih h) step)

/-- Original F41/F45 right-context whiskering preserves the EXACT
primitive depth of the entire independent axis history. -/
def KuuNativeAxisTrace.whisker
    {x y z : C} {n : Nat} {p q : KuuNativeBlocks x y}
    (h : KuuNativeAxisTrace n p q) (t : KuuNativePath y z) :
    KuuNativeAxisTrace n (.snoc p t) (.snoc q t) := by
  induction h with
  | refl p =>
      exact .refl _
  | snoc h step ih =>
      exact .snoc ih (.whisker step t)

/-- A real original-shaped one-step axis witness that inserts an
extra independent empty native categorical block, including exact
source and target partition carriers. -/
def KuuNativeAxisTrace.insertNilOnce
    {x y : C} (p : KuuNativeBlocks x y) :
    KuuNativeAxisTrace 1 p (.snoc p (.nil y)) :=
  .snoc (.refl p) (.insertNil p)

/-- Its source and target CARRY DIFFERENT raw block counts, despite
the proved exact path and categorical composite invariants. -/
theorem KuuNativeBlocks.ne_insertNil
    {x y : C} (p : KuuNativeBlocks x y) :
    p ≠ KuuNativeBlocks.snoc p (KuuNativePath.nil y) := by
  intro h
  have hc := congrArg KuuNativeBlocks.blockCount h
  change p.blockCount = p.blockCount + 1 at hc
  exact (Nat.ne_of_lt (Nat.lt_succ_self _)) hc

theorem KuuNativeAxisTrace.insertNilOnce_flatten
    {x y : C} (p : KuuNativeBlocks x y) :
    p.flatten =
      (KuuNativeBlocks.snoc p (KuuNativePath.nil y)).flatten :=
  (KuuNativeAxisTrace.insertNilOnce p).flatten_eq

#print axioms KuuNativeOneStep.flatten_eq
#print axioms KuuNativeOneStep.composite_eq
#print axioms KuuNativeAxisTrace.flatten_eq
#print axioms KuuNativeAxisTrace.composite_eq
#print axioms KuuNativeAxisTrace.append
#print axioms KuuNativeAxisTrace.whisker
#print axioms KuuNativeBlocks.ne_insertNil
#print axioms KuuNativeAxisTrace.insertNilOnce_flatten
end
end Kuu.F112.Physical
