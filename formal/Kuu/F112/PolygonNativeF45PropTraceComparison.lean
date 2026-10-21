import Kuu.F112.PolygonNativeF41ComparisonObstruction

/-!
# F112-E7Q5-B — a typed, proposition-step F45 comparison carrier

Historical F42 OneStep is Prop-valued while historical F45 AxisTrace
is Type-valued and keeps the intermediate original Blocks. This
distinction matters: comparing the independent Type-valued F41
primitive histories only to a Prop-valued OneStep does not by itself
compare the ACTUAL historical depth-indexed Type-valued F45 source.

We therefore construct a NEW F45-shaped Type-valued trace which retains
ALL typed native intermediate Blocks and exact Nat depths, but carries
a Prop-valued existential certificate for each primitive move.
The independent native AxisTrace maps to this source by an explicit
constructor-preserving erasure. The target is a MODEL of the old
Type/Prop separation, not the frozen old KUOS.AxisTrace itself.

The erasure still preserves exact flattened category paths and Hom
evaluation, but is provably NONINJECTIVE on two genuinely distinct
depth-one source proofs with the same typed boundaries. There is NO
left inverse, including over an actual north C60 Site axis.

No reverse original F45/F55 comparison, historical Gray equivalence,
F68/F77 curvature or unproved braiding is asserted. No legacy imports.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe u v
variable {C : Type u} [Category.{v} C]

/-- The F45-shaped comparison TYPE: every original native Blocks
intermediate and exact Nat depth is retained; ONLY primitive
F41 step-proof witnesses are erased to a proposition.

This is NOT a definitional alias to the frozen historical source:
a genuinely historical comparison still needs old Chain.Path/Blocks
maps and original F19/F28 operation correspondences. -/
inductive KuuNativePropAxisTrace :
    ∀ {x y : C}, Nat → KuuNativeBlocks x y →
      KuuNativeBlocks x y → Type (max u v) where
  | refl {x y : C} (p : KuuNativeBlocks x y) :
      KuuNativePropAxisTrace 0 p p
  | snoc {x y : C} {n : Nat}
      {p q r : KuuNativeBlocks x y}
      (h : KuuNativePropAxisTrace n p q)
      (step : Nonempty (KuuNativeOneStep q r)) :
      KuuNativePropAxisTrace (n + 1) p r

/-- A CONSTRUCTED direction of comparison from native Type-valued
AxisTrace into a complete Type-valued trace with Prop step fields.
No new path or proof is inferred from an equality of evaluations. -/
def KuuNativeAxisTrace.eraseStepEvidence
    {x y : C} {n : Nat}
    {p q : KuuNativeBlocks x y}
    (h : KuuNativeAxisTrace n p q) :
    KuuNativePropAxisTrace n p q := by
  induction h with
  | refl p =>
      exact .refl p
  | snoc h step ih =>
      exact .snoc ih ⟨step⟩

/-- The weaker Prop-step F45 carrier still certifies the EXACT
uncollapsed arrow word, rather than only a composite Hom equality. -/
theorem KuuNativePropAxisTrace.flatten_eq
    {x y : C} {n : Nat}
    {p q : KuuNativeBlocks x y}
    (h : KuuNativePropAxisTrace n p q) :
    p.flatten = q.flatten := by
  induction h with
  | refl p =>
      rfl
  | snoc h step ih =>
      rcases step with ⟨raw⟩
      exact ih.trans raw.flatten_eq

/-- Forgetting primitive proof terms still retains original category
evaluation of both endpoint block presentations. -/
theorem KuuNativePropAxisTrace.composite_eq
    {x y : C} {n : Nat}
    {p q : KuuNativeBlocks x y}
    (h : KuuNativePropAxisTrace n p q) :
    p.composite = q.composite := by
  calc
    p.composite = p.flatten.composite :=
      KuuNativeBlocks.composite_eq_flatten p
    _ = q.flatten.composite :=
      congrArg KuuNativePath.composite h.flatten_eq
    _ = q.composite :=
      (KuuNativeBlocks.composite_eq_flatten q).symm

/-- Both distinct native ONE-STEP traces land at the identical
Type-valued, fully indexed F45-style propositional-step trace.
Only the primitive step proof, not its boundaries, is forgotten. -/
theorem nativeF41DoubleNilSplitTrace_erase_eq
    {x y : C} (p : KuuNativeBlocks x y) :
    (nativeF41DoubleNilSplitTrace p).eraseStepEvidence =
      (nativeF41DoubleNilInsertTrace p).eraseStepEvidence := by
  rfl

/-- Consequently even the original-shaped Type-valued AxisTrace
target with exact Nat depth and intermediate Blocks fails to retain
faithfulness when its primitive operations are only Prop certificates. -/
theorem nativeF41DoubleNil_eraseStepEvidence_not_injective
    {x y : C} (p : KuuNativeBlocks x y) :
    ¬ Function.Injective
      (fun t : KuuNativeAxisTrace 1
        (nativeF41DoubleNilSource p) (nativeF41DoubleNilTarget p) =>
        t.eraseStepEvidence) := by
  intro hinj
  exact nativeF41DoubleNilSplitTrace_ne_insert p
    (hinj (nativeF41DoubleNilSplitTrace_erase_eq p))

/-- No reconstruction can be a LEFT INVERSE of this exact typed
erasure. This is a local primitive-history nonreconstruction theorem,
NOT the historical F55/F77 global phase-loss theorem. -/
theorem nativeF41DoubleNil_eraseStepEvidence_no_leftInverse
    {x y : C} (p : KuuNativeBlocks x y)
    (recover : KuuNativePropAxisTrace 1
      (nativeF41DoubleNilSource p) (nativeF41DoubleNilTarget p) →
      KuuNativeAxisTrace 1
        (nativeF41DoubleNilSource p) (nativeF41DoubleNilTarget p)) :
    ¬ Function.LeftInverse recover
      (fun t : KuuNativeAxisTrace 1
        (nativeF41DoubleNilSource p) (nativeF41DoubleNilTarget p) =>
        t.eraseStepEvidence) := by
  intro hrecover
  apply nativeF41DoubleNil_eraseStepEvidence_not_injective p
  intro left right h
  calc
    left = recover left.eraseStepEvidence := (hrecover left).symm
    _ = recover right.eraseStepEvidence := congrArg recover h
    _ = right := hrecover right

/-- This is not a toy Bool axis: specialize the obstruction to the
ACTUAL original-site north C60 pentagon finite categorical Blocks. -/
theorem northPentagonNativeF41_eraseStepEvidence_not_injective :
    ¬ Function.Injective
      (fun t : KuuNativeAxisTrace 1
        (nativeF41DoubleNilSource
          northPentagonNativeDualAxisFrame.firstAxis)
        (nativeF41DoubleNilTarget
          northPentagonNativeDualAxisFrame.firstAxis) =>
        t.eraseStepEvidence) :=
  nativeF41DoubleNil_eraseStepEvidence_not_injective
    northPentagonNativeDualAxisFrame.firstAxis

#print axioms KuuNativePropAxisTrace
#print axioms KuuNativeAxisTrace.eraseStepEvidence
#print axioms KuuNativePropAxisTrace.flatten_eq
#print axioms KuuNativePropAxisTrace.composite_eq
#print axioms nativeF41DoubleNilSplitTrace_erase_eq
#print axioms nativeF41DoubleNil_eraseStepEvidence_not_injective
#print axioms nativeF41DoubleNil_eraseStepEvidence_no_leftInverse
#print axioms northPentagonNativeF41_eraseStepEvidence_not_injective

end
end Kuu.F112.Physical
