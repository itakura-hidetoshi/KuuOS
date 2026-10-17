import Kuu.F112.PolygonNativeF45PhysicalRealization
import Kuu.F112.PolygonNativeF45PropTraceComparison

/-!
# F112-E7Q5-F4-P1-A — exact historical-shaped Prop/Type evidence boundary

The FROZEN v5.291 original (not imported) contains
* F42 OneStep : ... → Prop (three generators: split/insertNil/whisker),
* F42 Trace : ... → Prop, and
* F45 AxisTrace : ... → Type, whose snoc field is the Prop OneStep.

These definitions can be read in the preserved
DependentOriginationCoherentBiadjunctionFiniteRefinementTracesV5_139
and ProofRelevantAxisTracesV5_142 files.

This file independently reconstructs the precise three-constructor
Prop-valued elementary-step grammar and the Type-valued exact-depth
history grammar over the NEW KuuNativeBlocks. It does NOT declare an
equivalence to frozen historical Chain.Path/Blocks or import KUOS/Gray.

A genuine equivalence between the three-generator Prop presentation
and existence of a native Type step is proved. The resulting two
independent Prop-step, Type-valued history presentations are
equivalent and retain their exact intermediate Blocks.

A native Type-valued witness can be erased to this old-shaped trace.
A right inverse exists by a NONCOMPUTABLE choice of a raw primitive
witness; a left inverse provably does not, even on genuine C60 axes.
The original raw constructors remain distinct.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe u v
variable {C : Type u} [Category.{v} C]

/-- Original F42 OneStep's three genuine syntactic shapes, with
the original Prop universe but the NEW Kuu native typed Blocks. -/
inductive KuuNativeHistoricalOneStep :
    ∀ {x y : C}, KuuNativeBlocks x y →
      KuuNativeBlocks x y → Prop where
  | split {w x y z : C}
      (p : KuuNativeBlocks w x)
      (q : KuuNativePath x y)
      (r : KuuNativePath y z) :
      KuuNativeHistoricalOneStep
        (.snoc p (q.append r)) (.snoc (.snoc p q) r)
  | insertNil {x y : C} (p : KuuNativeBlocks x y) :
      KuuNativeHistoricalOneStep p (.snoc p (.nil y))
  | whisker {x y z : C} {p q : KuuNativeBlocks x y}
      (h : KuuNativeHistoricalOneStep p q)
      (t : KuuNativePath y z) :
      KuuNativeHistoricalOneStep (.snoc p t) (.snoc q t)

/-- Every truly constructed Type-valued native primitive yields
the corresponding precise historical-shaped Prop constructor. -/
theorem KuuNativeOneStep.toHistorical
    {x y : C} {p q : KuuNativeBlocks x y}
    (h : KuuNativeOneStep p q) :
    KuuNativeHistoricalOneStep p q := by
  induction h with
  | split p q r => exact .split p q r
  | insertNil p => exact .insertNil p
  | whisker h t ih => exact .whisker ih t

/-- Every old-shaped step proposition is inhabited by an ACTUAL
Type-valued native constructor, stated in Prop without choice. -/
theorem KuuNativeHistoricalOneStep.hasNative
    {x y : C} {p q : KuuNativeBlocks x y}
    (h : KuuNativeHistoricalOneStep p q) :
    Nonempty (KuuNativeOneStep p q) := by
  induction h with
  | split p q r => exact ⟨.split p q r⟩
  | insertNil p => exact ⟨.insertNil p⟩
  | whisker h t ih =>
      rcases ih with ⟨step⟩
      exact ⟨.whisker step t⟩

/-- Exact constructor-by-constructor PROPOSITIONAL classification,
not just equality of categorical composite arrows. -/
theorem kuuNativeHistoricalOneStep_iff_nonempty
    {x y : C} {p q : KuuNativeBlocks x y} :
    KuuNativeHistoricalOneStep p q ↔
      Nonempty (KuuNativeOneStep p q) := by
  constructor
  · exact KuuNativeHistoricalOneStep.hasNative
  · rintro ⟨step⟩
    exact step.toHistorical

/-- Original F45-shaped history: TYPE-valued with every exact
intermediate Blocks and Nat depth, but Prop-valued step fields. -/
inductive KuuNativeHistoricalAxisTrace :
    ∀ {x y : C}, Nat → KuuNativeBlocks x y →
      KuuNativeBlocks x y → Type (max u v) where
  | refl {x y : C} (p : KuuNativeBlocks x y) :
      KuuNativeHistoricalAxisTrace 0 p p
  | snoc {x y : C} {n : Nat}
      {p q r : KuuNativeBlocks x y}
      (h : KuuNativeHistoricalAxisTrace n p q)
      (step : KuuNativeHistoricalOneStep q r) :
      KuuNativeHistoricalAxisTrace (n + 1) p r

/-- Exact depth, original intermediate typed Blocks, and BOTH source
endpoints survive the primitive Type-to-Prop proof erasure. -/
def KuuNativeAxisTrace.toHistorical
    {x y : C} {n : Nat} {p q : KuuNativeBlocks x y}
    (h : KuuNativeAxisTrace n p q) :
    KuuNativeHistoricalAxisTrace n p q := by
  induction h with
  | refl p => exact .refl p
  | snoc h step ih => exact .snoc ih step.toHistorical

/-- Pass from independently reconstructed old-shaped Prop witnesses
to the previously certified existential-primitive comparison trace. -/
def KuuNativeHistoricalAxisTrace.toProp
    {x y : C} {n : Nat} {p q : KuuNativeBlocks x y}
    (h : KuuNativeHistoricalAxisTrace n p q) :
    KuuNativePropAxisTrace n p q := by
  induction h with
  | refl p => exact .refl p
  | snoc h step ih => exact .snoc ih step.hasNative

/-- Reverse correspondence of two precisely aligned Prop-step
presentations, retaining the exact Type-valued intermediate Blocks. -/
def KuuNativePropAxisTrace.toHistorical
    {x y : C} {n : Nat} {p q : KuuNativeBlocks x y}
    (h : KuuNativePropAxisTrace n p q) :
    KuuNativeHistoricalAxisTrace n p q := by
  induction h with
  | refl p => exact .refl p
  | snoc h step ih =>
      exact .snoc ih (kuuNativeHistoricalOneStep_iff_nonempty.mpr step)

theorem KuuNativeHistoricalAxisTrace.toProp_toHistorical
    {x y : C} {n : Nat} {p q : KuuNativeBlocks x y}
    (h : KuuNativeHistoricalAxisTrace n p q) :
    h.toProp.toHistorical = h := by
  induction h with
  | refl p => rfl
  | snoc h step ih =>
      exact congrArg
        (fun t => KuuNativeHistoricalAxisTrace.snoc t step) ih

theorem KuuNativePropAxisTrace.toHistorical_toProp
    {x y : C} {n : Nat} {p q : KuuNativeBlocks x y}
    (h : KuuNativePropAxisTrace n p q) :
    h.toHistorical.toProp = h := by
  induction h with
  | refl p => rfl
  | snoc h step ih =>
      exact congrArg (fun t => KuuNativePropAxisTrace.snoc t step) ih

/-- These TWO Prop-step Type-valued presentations are genuinely
equivalent, with no collapse of intermediate native Blocks. -/
def kuuNativeHistoricalPropAxisEquiv
    {x y : C} {n : Nat} {p q : KuuNativeBlocks x y} :
    KuuNativeHistoricalAxisTrace n p q ≃
      KuuNativePropAxisTrace n p q where
  toFun := KuuNativeHistoricalAxisTrace.toProp
  invFun := KuuNativePropAxisTrace.toHistorical
  left_inv := KuuNativeHistoricalAxisTrace.toProp_toHistorical
  right_inv := KuuNativePropAxisTrace.toHistorical_toProp

/-- Erasure to the actual historic-shaped Prop-step grammar agrees
with the older E7Q5-B existential trace, at EXACT depth. -/
theorem KuuNativeAxisTrace.toHistorical_toProp
    {x y : C} {n : Nat} {p q : KuuNativeBlocks x y}
    (h : KuuNativeAxisTrace n p q) :
    h.toHistorical.toProp = h.eraseStepEvidence := by
  induction h with
  | refl p => rfl
  | snoc h step ih =>
      exact congrArg
        (fun t => KuuNativePropAxisTrace.snoc t ⟨step⟩) ih

/-- Choosing a raw Type-valued operation out of the old-shaped Prop
evidence is NONCOMPUTABLE and may choose either overlapping split
or insertion at the same exact Blocks. -/
def KuuNativeHistoricalAxisTrace.chooseNative
    {x y : C} {n : Nat} {p q : KuuNativeBlocks x y}
    (h : KuuNativeHistoricalAxisTrace n p q) :
    KuuNativeAxisTrace n p q := by
  induction h with
  | refl p => exact .refl p
  | snoc h step ih => exact .snoc ih (Classical.choice step.hasNative)

/-- This choice is a RIGHT inverse to evidence erasure, not a left
inverse. It preserves exact typed endpoints and Nat depths. -/
theorem KuuNativeHistoricalAxisTrace.toHistorical_chooseNative
    {x y : C} {n : Nat} {p q : KuuNativeBlocks x y}
    (h : KuuNativeHistoricalAxisTrace n p q) :
    h.chooseNative.toHistorical = h := by
  induction h with
  | refl p => rfl
  | snoc h step ih =>
      exact congrArg
        (fun t => KuuNativeHistoricalAxisTrace.snoc t step) ih

/-- Every old-shaped, fully typed history is reachable after
choosing Type witnesses, but no full inverse is claimed. -/
theorem KuuNativeAxisTrace.toHistorical_surjective
    {x y : C} {n : Nat} {p q : KuuNativeBlocks x y} :
    Function.Surjective
      (fun h : KuuNativeAxisTrace n p q => h.toHistorical) := by
  intro old
  exact ⟨old.chooseNative, old.toHistorical_chooseNative⟩

/-- The two actual Type constructors split/insertNil at the SAME
native Blocks have the SAME historic-shaped Prop-step trace. -/
theorem nativeF41DoubleNil_toHistorical_eq
    {x y : C} (p : KuuNativeBlocks x y) :
    (nativeF41DoubleNilSplitTrace p).toHistorical =
      (nativeF41DoubleNilInsertTrace p).toHistorical := by
  rfl

/-- Even though the historic-shaped trace is TYPE and carries all
intermediate Blocks, its Prop step fields still lose information. -/
theorem nativeF41DoubleNil_toHistorical_not_injective
    {x y : C} (p : KuuNativeBlocks x y) :
    ¬ Function.Injective
      (fun h : KuuNativeAxisTrace 1
        (nativeF41DoubleNilSource p) (nativeF41DoubleNilTarget p) =>
        h.toHistorical) := by
  intro hinj
  exact nativeF41DoubleNilSplitTrace_ne_insert p
    (hinj (nativeF41DoubleNil_toHistorical_eq p))

/-- A recovery of the complete raw Type witness cannot be a LEFT
inverse to historical-shaped erasure on these native endpoints. -/
theorem nativeF41DoubleNil_toHistorical_no_leftInverse
    {x y : C} (p : KuuNativeBlocks x y) :
    ¬ ∃ recover : KuuNativeHistoricalAxisTrace 1
        (nativeF41DoubleNilSource p) (nativeF41DoubleNilTarget p) →
          KuuNativeAxisTrace 1
            (nativeF41DoubleNilSource p) (nativeF41DoubleNilTarget p),
      Function.LeftInverse recover
        (fun h : KuuNativeAxisTrace 1
          (nativeF41DoubleNilSource p) (nativeF41DoubleNilTarget p) =>
          h.toHistorical) := by
  rintro ⟨recover, hleft⟩
  exact nativeF41DoubleNil_toHistorical_not_injective p hleft.injective

/-- The evidence obstruction is present on actual original north C60
Site-category block presentations, not only hypothetical objects. -/
theorem northPentagonNativeHistoricalTrace_not_injective :
    ¬ Function.Injective
      (fun h : KuuNativeAxisTrace 1
        (nativeF41DoubleNilSource northPentagonNativeDualAxisFrame.firstAxis)
        (nativeF41DoubleNilTarget northPentagonNativeDualAxisFrame.firstAxis) =>
          h.toHistorical) :=
  nativeF41DoubleNil_toHistorical_not_injective
    northPentagonNativeDualAxisFrame.firstAxis

#print axioms kuuNativeHistoricalOneStep_iff_nonempty
#print axioms KuuNativeAxisTrace.toHistorical
#print axioms KuuNativeHistoricalAxisTrace.toProp
#print axioms KuuNativePropAxisTrace.toHistorical
#print axioms kuuNativeHistoricalPropAxisEquiv
#print axioms KuuNativeAxisTrace.toHistorical_toProp
#print axioms KuuNativeHistoricalAxisTrace.chooseNative
#print axioms KuuNativeHistoricalAxisTrace.toHistorical_chooseNative
#print axioms KuuNativeAxisTrace.toHistorical_surjective
#print axioms nativeF41DoubleNil_toHistorical_eq
#print axioms nativeF41DoubleNil_toHistorical_not_injective
#print axioms nativeF41DoubleNil_toHistorical_no_leftInverse
#print axioms northPentagonNativeHistoricalTrace_not_injective
end
end Kuu.F112.Physical
