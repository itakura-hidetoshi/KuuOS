import Kuu.F112.PolygonNativeF45Source

/-!
# F112-E7Q5-F4-L — original-shaped F19/F28 interleavings in independent Type

The frozen v5.291 F44 \`OrderedInterleaving\` has precisely three
source constructors: identity, an F19-axis refinement, and an
independent F28-axis refinement. Its original F41 \`AxisTrace\`
stores \`OneStep\` in Prop; the independent \`KuuNativeAxisTrace\`
stores the genuine primitive witness in Type.

We reconstruct the two-axis F44 ordered word *without importing*
any frozen KUOS module. Both Type-valued primitive axis histories,
their exact Nat depths and original F40-shaped categorical Blocks
are recoverable from the actual interleaved word. The two F45
orders give genuinely distinct raw routes but the same exact pair
of axis histories. Thus the history-pair observation has no global
left inverse, just as the historical F44 exchange quotient needed
an explicit adjacent-swap relation.

This is a structural constructor comparison, NOT an equivalence
of the frozen F19/F28/F44/F45 source types. In particular the
historical Prop-valued primitive proofs are not silently equated
with the new Type-valued \`KuuNativeOneStep\`.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uA vA uB vB
variable {A : Type uA} [Category.{vA} A]
variable {B : Type uB} [Category.{vB} B]

/-- Three original F44 constructor shapes, retaining the precise
type of BOTH axes and all original intermediate block presentations. -/
inductive KuuNativeF44Ordered :
    ∀ {a b : A} {x y : B},
      Nat → Nat →
      KuuNativeBlocks a b → KuuNativeBlocks x y →
      KuuNativeBlocks a b → KuuNativeBlocks x y →
      Type (max (max uA uB) (max vA vB)) where
  | refl {a b : A} {x y : B}
      (ma : KuuNativeBlocks a b) (pa : KuuNativeBlocks x y) :
      KuuNativeF44Ordered 0 0 ma pa ma pa
  | first {a b : A} {x y : B} {n m : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      (h : KuuNativeF44Ordered n m ma pa mb pb)
      (step : KuuNativeOneStep mb mc) :
      KuuNativeF44Ordered (n + 1) m ma pa mc pb
  | second {a b : A} {x y : B} {n m : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      (h : KuuNativeF44Ordered n m ma pa mb pb)
      (step : KuuNativeOneStep pb pc) :
      KuuNativeF44Ordered n (m + 1) ma pa mb pc

/-- Actual first-axis history, not only an existence statement
or equality of categorical composite arrows. -/
def KuuNativeF44Ordered.firstHistory
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (h : KuuNativeF44Ordered n m ma pa mb pb) :
    KuuNativeAxisTrace n ma mb := by
  induction h with
  | refl ma pa => exact .refl ma
  | first h step ih => exact .snoc ih step
  | second h step ih => exact ih

/-- Actual second-axis history remains independent of the first. -/
def KuuNativeF44Ordered.secondHistory
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (h : KuuNativeF44Ordered n m ma pa mb pb) :
    KuuNativeAxisTrace m pa pb := by
  induction h with
  | refl ma pa => exact .refl pa
  | first h step ih => exact ih
  | second h step ih => exact .snoc ih step

/-- Store the pair of ACTUAL Type-valued axis histories. This
observation is not asserted to be injective on ordered words. -/
def KuuNativeF44Ordered.histories
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (h : KuuNativeF44Ordered n m ma pa mb pb) :
    KuuNativeAxisTrace n ma mb × KuuNativeAxisTrace m pa pb :=
  (h.firstHistory, h.secondHistory)

/-- Realize the F19-only original history while keeping the whole
F28 categorical block presentation fixed at every intermediate step. -/
def KuuNativeF44Ordered.firstOnly
    {a b : A} {x y : B} {n : Nat}
    {ma mb : KuuNativeBlocks a b}
    (h : KuuNativeAxisTrace n ma mb) (pa : KuuNativeBlocks x y) :
    KuuNativeF44Ordered n 0 ma pa mb pa := by
  induction h with
  | refl ma => exact .refl ma pa
  | snoc h step ih => exact .first ih step

/-- Symmetric F28-only original history with all F19 blocks fixed. -/
def KuuNativeF44Ordered.secondOnly
    {a b : A} {x y : B} {m : Nat}
    (ma : KuuNativeBlocks a b)
    {pa pb : KuuNativeBlocks x y}
    (h : KuuNativeAxisTrace m pa pb) :
    KuuNativeF44Ordered 0 m ma pa ma pb := by
  induction h with
  | refl pa => exact .refl ma pa
  | snoc h step ih => exact .second ih step

/-- The exact F19-first original F45 execution order, built from
ALL the genuine primitive operations on both category axes. -/
def KuuNativeF44Ordered.firstThenSecond
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (h₁ : KuuNativeAxisTrace n ma mb)
    (h₂ : KuuNativeAxisTrace m pa pb) :
    KuuNativeF44Ordered n m ma pa mb pb := by
  induction h₂ with
  | refl pa => exact .firstOnly h₁ pa
  | snoc h₂ step ih => exact .second ih step

/-- The other actual original F45 execution order, F28 first,
without assuming that the two raw words commute definitionally. -/
def KuuNativeF44Ordered.secondThenFirst
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (h₁ : KuuNativeAxisTrace n ma mb)
    (h₂ : KuuNativeAxisTrace m pa pb) :
    KuuNativeF44Ordered n m ma pa mb pb := by
  induction h₁ with
  | refl ma => exact .secondOnly ma h₂
  | snoc h₁ step ih => exact .first ih step

theorem KuuNativeF44Ordered.firstOnly_firstHistory
    {a b : A} {x y : B} {n : Nat}
    {ma mb : KuuNativeBlocks a b}
    (h : KuuNativeAxisTrace n ma mb) (pa : KuuNativeBlocks x y) :
    (KuuNativeF44Ordered.firstOnly h pa).firstHistory = h := by
  induction h with
  | refl ma => rfl
  | snoc h step ih =>
      change KuuNativeAxisTrace.snoc
        (KuuNativeF44Ordered.firstOnly h pa).firstHistory step =
        KuuNativeAxisTrace.snoc h step
      exact congrArg (fun z => KuuNativeAxisTrace.snoc z step) ih

theorem KuuNativeF44Ordered.firstOnly_secondHistory
    {a b : A} {x y : B} {n : Nat}
    {ma mb : KuuNativeBlocks a b}
    (h : KuuNativeAxisTrace n ma mb) (pa : KuuNativeBlocks x y) :
    (KuuNativeF44Ordered.firstOnly h pa).secondHistory =
      KuuNativeAxisTrace.refl pa := by
  induction h with
  | refl ma => rfl
  | snoc h step ih => exact ih

theorem KuuNativeF44Ordered.secondOnly_firstHistory
    {a b : A} {x y : B} {m : Nat}
    (ma : KuuNativeBlocks a b)
    {pa pb : KuuNativeBlocks x y}
    (h : KuuNativeAxisTrace m pa pb) :
    (KuuNativeF44Ordered.secondOnly ma h).firstHistory =
      KuuNativeAxisTrace.refl ma := by
  induction h with
  | refl pa => rfl
  | snoc h step ih => exact ih

theorem KuuNativeF44Ordered.secondOnly_secondHistory
    {a b : A} {x y : B} {m : Nat}
    (ma : KuuNativeBlocks a b)
    {pa pb : KuuNativeBlocks x y}
    (h : KuuNativeAxisTrace m pa pb) :
    (KuuNativeF44Ordered.secondOnly ma h).secondHistory = h := by
  induction h with
  | refl pa => rfl
  | snoc h step ih =>
      change KuuNativeAxisTrace.snoc
        (KuuNativeF44Ordered.secondOnly ma h).secondHistory step =
        KuuNativeAxisTrace.snoc h step
      exact congrArg (fun z => KuuNativeAxisTrace.snoc z step) ih

/-- Both whole F19 histories survive F19-first execution, with
every primitive-step witness unchanged and not merely Prop-erased. -/
theorem KuuNativeF44Ordered.firstThenSecond_firstHistory
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (h₁ : KuuNativeAxisTrace n ma mb)
    (h₂ : KuuNativeAxisTrace m pa pb) :
    (KuuNativeF44Ordered.firstThenSecond h₁ h₂).firstHistory = h₁ := by
  induction h₂ with
  | refl pa => exact KuuNativeF44Ordered.firstOnly_firstHistory h₁ pa
  | snoc h₂ step ih => exact ih

theorem KuuNativeF44Ordered.firstThenSecond_secondHistory
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (h₁ : KuuNativeAxisTrace n ma mb)
    (h₂ : KuuNativeAxisTrace m pa pb) :
    (KuuNativeF44Ordered.firstThenSecond h₁ h₂).secondHistory = h₂ := by
  induction h₂ with
  | refl pa => exact KuuNativeF44Ordered.firstOnly_secondHistory h₁ pa
  | snoc h₂ step ih =>
      change KuuNativeAxisTrace.snoc
        (KuuNativeF44Ordered.firstThenSecond h₁ h₂).secondHistory step =
        KuuNativeAxisTrace.snoc h₂ step
      exact congrArg (fun z => KuuNativeAxisTrace.snoc z step) ih

/-- The F28-first word has the SAME full Type-valued F19 history. -/
theorem KuuNativeF44Ordered.secondThenFirst_firstHistory
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (h₁ : KuuNativeAxisTrace n ma mb)
    (h₂ : KuuNativeAxisTrace m pa pb) :
    (KuuNativeF44Ordered.secondThenFirst h₁ h₂).firstHistory = h₁ := by
  induction h₁ with
  | refl ma => exact KuuNativeF44Ordered.secondOnly_firstHistory ma h₂
  | snoc h₁ step ih =>
      change KuuNativeAxisTrace.snoc
        (KuuNativeF44Ordered.secondThenFirst h₁ h₂).firstHistory step =
        KuuNativeAxisTrace.snoc h₁ step
      exact congrArg (fun z => KuuNativeAxisTrace.snoc z step) ih

theorem KuuNativeF44Ordered.secondThenFirst_secondHistory
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (h₁ : KuuNativeAxisTrace n ma mb)
    (h₂ : KuuNativeAxisTrace m pa pb) :
    (KuuNativeF44Ordered.secondThenFirst h₁ h₂).secondHistory = h₂ := by
  induction h₁ with
  | refl ma => exact KuuNativeF44Ordered.secondOnly_secondHistory ma h₂
  | snoc h₁ step ih => exact ih

/-- Independently implement BOTH original F45 order constructors,
rather than replacing them with equality of their shadows. -/
def KuuNativeF44Ordered.fromF45Order
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (order : KuuNativeF45Order)
    (h₁ : KuuNativeAxisTrace n ma mb)
    (h₂ : KuuNativeAxisTrace m pa pb) :
    KuuNativeF44Ordered n m ma pa mb pb :=
  match order with
  | .firstAxisFirst => .firstThenSecond h₁ h₂
  | .secondAxisFirst => .secondThenFirst h₁ h₂

/-- Both source F45 ordering constructors retain the EXACT
uncollapsed histories for arbitrary depths and categories. -/
theorem KuuNativeF44Ordered.fromF45Order_histories
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (order : KuuNativeF45Order)
    (h₁ : KuuNativeAxisTrace n ma mb)
    (h₂ : KuuNativeAxisTrace m pa pb) :
    (KuuNativeF44Ordered.fromF45Order order h₁ h₂).histories =
      (h₁, h₂) := by
  cases order with
  | firstAxisFirst =>
      exact Prod.ext
        (KuuNativeF44Ordered.firstThenSecond_firstHistory h₁ h₂)
        (KuuNativeF44Ordered.firstThenSecond_secondHistory h₁ h₂)
  | secondAxisFirst =>
      exact Prod.ext
        (KuuNativeF44Ordered.secondThenFirst_firstHistory h₁ h₂)
        (KuuNativeF44Ordered.secondThenFirst_secondHistory h₁ h₂)

/-- Genuine C60 physical sector is carried in the original F45
leaf execution packet, not discarded as an untyped history tag. -/
def nativeF45LeafExecution
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (i : PolygonBoundarySector p)
    (order : KuuNativeF45Order)
    (h₁ : KuuNativeAxisTrace n ma mb)
    (h₂ : KuuNativeAxisTrace m pa pb) :
    (PolygonBoundarySector p) ×
      KuuNativeF44Ordered n m ma pa mb pb :=
  (i, KuuNativeF44Ordered.fromF45Order order h₁ h₂)

/-- F45 leaf execution retains its exact source C60 sector. -/
theorem nativeF45LeafExecution_sector
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (i : PolygonBoundarySector p)
    (order : KuuNativeF45Order)
    (h₁ : KuuNativeAxisTrace n ma mb)
    (h₂ : KuuNativeAxisTrace m pa pb) :
    (nativeF45LeafExecution i order h₁ h₂).1 = i :=
  rfl

theorem nativeF45LeafExecution_histories
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (i : PolygonBoundarySector p)
    (order : KuuNativeF45Order)
    (h₁ : KuuNativeAxisTrace n ma mb)
    (h₂ : KuuNativeAxisTrace m pa pb) :
    (nativeF45LeafExecution i order h₁ h₂).2.histories = (h₁, h₂) :=
  KuuNativeF44Ordered.fromF45Order_histories order h₁ h₂

/-- The two ACTUAL unit-step raw interleavings differ: one ends
with F28 while the other ends with F19, even though both recover
the exact same first and second Type-valued histories. -/
theorem nativeF44UnitOrders_ne
    {a b : A} {x y : B}
    (ma : KuuNativeBlocks a b) (pa : KuuNativeBlocks x y) :
    KuuNativeF44Ordered.fromF45Order .firstAxisFirst
        (KuuNativeAxisTrace.insertNilOnce ma)
        (KuuNativeAxisTrace.insertNilOnce pa) ≠
      KuuNativeF44Ordered.fromF45Order .secondAxisFirst
        (KuuNativeAxisTrace.insertNilOnce ma)
        (KuuNativeAxisTrace.insertNilOnce pa) := by
  intro h
  cases h

/-- A concrete no-go for recovering the raw F44 ordered word
from the pair of complete F19/F28 axis histories: the obstruction
persists even though each axis history is in Type and uncollapsed. -/
theorem nativeF44UnitHistoryObservation_not_injective
    {a b : A} {x y : B}
    (ma : KuuNativeBlocks a b) (pa : KuuNativeBlocks x y) :
    ¬ Function.Injective
      (fun h : KuuNativeF44Ordered 1 1 ma pa
          (.snoc ma (.nil b)) (.snoc pa (.nil y)) => h.histories) := by
  intro hinj
  apply nativeF44UnitOrders_ne ma pa
  apply hinj
  rw [KuuNativeF44Ordered.fromF45Order_histories,
    KuuNativeF44Ordered.fromF45Order_histories]

#print axioms KuuNativeF44Ordered
#print axioms KuuNativeF44Ordered.firstHistory
#print axioms KuuNativeF44Ordered.secondHistory
#print axioms KuuNativeF44Ordered.fromF45Order_histories
#print axioms nativeF45LeafExecution_histories
#print axioms nativeF44UnitOrders_ne
#print axioms nativeF44UnitHistoryObservation_not_injective
end
end Kuu.F112.Physical
