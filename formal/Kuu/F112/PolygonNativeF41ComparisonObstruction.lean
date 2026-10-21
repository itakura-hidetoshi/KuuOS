import Kuu.F112.NativeAxisTraces

/-!
# F112-E7Q5-A — a typed F41 comparison obstruction before historical F55

The frozen historical F42 OneStep is Prop-valued, whereas the independent
KuuNativeOneStep is Type-valued. The nine-constructor higher-cell grammar
cannot be compared faithfully before checking the primitive histories.

Here TWO DIFFERENT genuine native F41 primitive steps have EXACTLY
the same typed Blocks source and target:
* split a pair of empty native categorical paths in one existing block;
* insert an independent empty block at precisely that source.

We prove the steps are different raw constructors, as are the resulting
exactly-one-step native AxisTrace terms. Any map of either source type to
an arbitrary Prop is noninjective, by proof irrelevance. In particular,
a historical Prop-valued OneStep interpretation alone cannot serve as
a faithful comparison of this new primitive Type-valued evidence.

This is a LOCAL SOURCE obstruction; it is NOT a theorem ruling out all
historical F45/F55 comparisons after explicit enrichment or forgetting
with recorded losses. No legacy KUOS, Gray, F51, F77 imports/axioms.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe u v
variable {C : Type u} [Category.{v} C]

/-- Retain the actual constructor used by each primitive native
refinement, even when distinct operations have identical boundaries. -/
inductive KuuNativeOneStepKind where
  | split
  | insertNil
  | whisker
  deriving DecidableEq

/-- Constructor observation does not quotient raw primitive evidence. -/
def KuuNativeOneStep.kind
    {x y : C} {p q : KuuNativeBlocks x y}
    (h : KuuNativeOneStep p q) : KuuNativeOneStepKind :=
  match h with
  | .split _ _ _ => .split
  | .insertNil _ => .insertNil
  | .whisker _ _ => .whisker

/-- The final primitive constructor of an EXACT native F19/F28-shaped
history; depth zero has no final operation. -/
def KuuNativeAxisTrace.lastKind
    {x y : C} {n : Nat} {p q : KuuNativeBlocks x y}
    (h : KuuNativeAxisTrace n p q) :
    Option KuuNativeOneStepKind :=
  match h with
  | .refl _ => none
  | .snoc _ step => some step.kind

/-- A source presentation with one independently recorded empty path. -/
def nativeF41DoubleNilSource {x y : C}
    (p : KuuNativeBlocks x y) : KuuNativeBlocks x y :=
  .snoc p (.nil y)

/-- Its one-more-block target. Both operations below reach this
same exact original-shaped typed partition, not merely an equal Hom. -/
def nativeF41DoubleNilTarget {x y : C}
    (p : KuuNativeBlocks x y) : KuuNativeBlocks x y :=
  .snoc (nativeF41DoubleNilSource p) (.nil y)

/-- Split a native path nil.append nil, with exact shared boundaries. -/
def nativeF41DoubleNilSplit {x y : C}
    (p : KuuNativeBlocks x y) :
    KuuNativeOneStep
      (nativeF41DoubleNilSource p) (nativeF41DoubleNilTarget p) :=
  .split p (.nil y) (.nil y)

/-- Insert an empty block instead: same typed source and target,
but an independent, distinguishable primitive F41 constructor. -/
def nativeF41DoubleNilInsert {x y : C}
    (p : KuuNativeBlocks x y) :
    KuuNativeOneStep
      (nativeF41DoubleNilSource p) (nativeF41DoubleNilTarget p) :=
  .insertNil (nativeF41DoubleNilSource p)

/-- Genuine proof-relevance: two distinct F41 constructors overlap
on exactly the same typed original native Blocks boundary. -/
theorem nativeF41DoubleNilSplit_ne_insert {x y : C}
    (p : KuuNativeBlocks x y) :
    nativeF41DoubleNilSplit p ≠ nativeF41DoubleNilInsert p := by
  intro h
  have hk := congrArg
    (fun s : KuuNativeOneStep
      (nativeF41DoubleNilSource p) (nativeF41DoubleNilTarget p) =>
      s.kind) h
  change KuuNativeOneStepKind.split = KuuNativeOneStepKind.insertNil at hk
  exact (by decide : KuuNativeOneStepKind.split ≠
    KuuNativeOneStepKind.insertNil) hk

/-- Both primitive witnesses occur as ACTUAL one-step full native
histories, without introducing fake shortcuts or graded equalities. -/
def nativeF41DoubleNilSplitTrace {x y : C}
    (p : KuuNativeBlocks x y) :
    KuuNativeAxisTrace 1
      (nativeF41DoubleNilSource p) (nativeF41DoubleNilTarget p) :=
  .snoc (.refl (nativeF41DoubleNilSource p)) (nativeF41DoubleNilSplit p)

def nativeF41DoubleNilInsertTrace {x y : C}
    (p : KuuNativeBlocks x y) :
    KuuNativeAxisTrace 1
      (nativeF41DoubleNilSource p) (nativeF41DoubleNilTarget p) :=
  .snoc (.refl (nativeF41DoubleNilSource p)) (nativeF41DoubleNilInsert p)

/-- The loss persists through the exact-Nat-depth F45 axis-history
carrier: two distinct raw trace witnesses have the same source,
target and depth ONE, while their final constructors differ. -/
theorem nativeF41DoubleNilSplitTrace_ne_insert {x y : C}
    (p : KuuNativeBlocks x y) :
    nativeF41DoubleNilSplitTrace p ≠
      nativeF41DoubleNilInsertTrace p := by
  intro h
  have hk := congrArg
    (fun t : KuuNativeAxisTrace 1
      (nativeF41DoubleNilSource p) (nativeF41DoubleNilTarget p) =>
      t.lastKind) h
  change some KuuNativeOneStepKind.split =
    some KuuNativeOneStepKind.insertNil at hk
  exact (by decide : (some KuuNativeOneStepKind.split :
    Option KuuNativeOneStepKind) ≠ some .insertNil) hk

/-- ANY direct erasure of these two primitive witnesses to a Prop
must identify them, and hence CANNOT be faithful/injective. This
includes possible historical F42 OneStep codomains AFTER any chosen
typed Blocks/path boundary map. -/
theorem nativeF41DoubleNil_no_injective_PropStep
    {x y : C} (p : KuuNativeBlocks x y)
    (P : Prop)
    (f : KuuNativeOneStep
      (nativeF41DoubleNilSource p) (nativeF41DoubleNilTarget p) → P) :
    ¬ Function.Injective f := by
  intro hf
  apply nativeF41DoubleNilSplit_ne_insert p
  exact hf (Subsingleton.elim _ _)

/-- The identical obstruction applies to any Prop-only observer of
the ACTUAL Type-valued complete one-step axis histories. It does
NOT claim that the old Type-valued F45 AxisTrace itself is Prop. -/
theorem nativeF41DoubleNil_no_injective_PropTrace
    {x y : C} (p : KuuNativeBlocks x y)
    (P : Prop)
    (f : KuuNativeAxisTrace 1
      (nativeF41DoubleNilSource p) (nativeF41DoubleNilTarget p) → P) :
    ¬ Function.Injective f := by
  intro hf
  apply nativeF41DoubleNilSplitTrace_ne_insert p
  exact hf (Subsingleton.elim _ _)

#print axioms KuuNativeOneStep.kind
#print axioms KuuNativeAxisTrace.lastKind
#print axioms nativeF41DoubleNilSplit
#print axioms nativeF41DoubleNilInsert
#print axioms nativeF41DoubleNilSplit_ne_insert
#print axioms nativeF41DoubleNilSplitTrace_ne_insert
#print axioms nativeF41DoubleNil_no_injective_PropStep
#print axioms nativeF41DoubleNil_no_injective_PropTrace
end
end Kuu.F112.Physical
