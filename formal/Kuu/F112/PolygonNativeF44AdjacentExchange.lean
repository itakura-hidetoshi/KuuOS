import Mathlib.Logic.Relation
import Kuu.F112.PolygonNativeF45FullExecutionComparison

/-!
# F112-E7Q5-F4-M1 — genuinely proof-relevant native F44 adjacent exchange

The historical F44 generated congruence exchanges ONLY a consecutive
F19 operation and an independent F28 operation, keeping the two
original F40 Blocks axes and their separate primitive histories.
Here we reconstruct that square, its two right contexts, the generated
equivalence relation and its Quot in the NEW, independent Type-valued
F44 ordered grammar.  No frozen KUOS or Gray imports.

All primitive step proofs remain Type-valued; the exchange relation
is Prop-valued.  Histories descend by proving the actual square
preserves each *whole* Type-valued axis history, not by proof erasure,
endpoint arrows, numerical grade, or a Gray exchange axiom.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uA vA uB vB
variable {A : Type uA} [Category.{vA} A]
variable {B : Type uB} [Category.{vB} B]

/-- One independent adjacent F19/F28 interchange and its closure
under subsequent first-axis/second-axis primitive operations. -/
inductive KuuNativeF44AdjacentSwap :
    ∀ {a b : A} {x y : B} {n m : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y},
      KuuNativeF44Ordered n m ma pa mb pb →
      KuuNativeF44Ordered n m ma pa mb pb → Prop where
  | square {a b : A} {x y : B} {n m : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      (initial : KuuNativeF44Ordered n m ma pa mb pb)
      (hf : KuuNativeOneStep mb mc)
      (hs : KuuNativeOneStep pb pc) :
      KuuNativeF44AdjacentSwap
        (.second (.first initial hf) hs)
        (.first (.second initial hs) hf)
  | afterFirst {a b : A} {x y : B} {n m : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {p q : KuuNativeF44Ordered n m ma pa mb pb}
      (h : KuuNativeF44AdjacentSwap p q)
      (step : KuuNativeOneStep mb mc) :
      KuuNativeF44AdjacentSwap (.first p step) (.first q step)
  | afterSecond {a b : A} {x y : B} {n m : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      {p q : KuuNativeF44Ordered n m ma pa mb pb}
      (h : KuuNativeF44AdjacentSwap p q)
      (step : KuuNativeOneStep pb pc) :
      KuuNativeF44AdjacentSwap (.second p step) (.second q step)

/-- Adjacent swaps preserve the WHOLE Type-valued proof tree for
each axis, including each separately typed F40 Blocks presentation. -/
theorem KuuNativeF44AdjacentSwap.histories_eq
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {p q : KuuNativeF44Ordered n m ma pa mb pb}
    (h : KuuNativeF44AdjacentSwap p q) :
    p.histories = q.histories := by
  induction h with
  | square initial hf hs =>
      rfl
  | afterFirst h step ih =>
      exact Prod.ext
        (congrArg (fun z => KuuNativeAxisTrace.snoc z step)
          (congrArg (fun z => z.1) ih))
        (congrArg (fun z => z.2) ih)
  | afterSecond h step ih =>
      exact Prod.ext
        (congrArg (fun z => z.1) ih)
        (congrArg (fun z => KuuNativeAxisTrace.snoc z step)
          (congrArg (fun z => z.2) ih))

/-- No implicit endpoint-equality rule: ONLY the EqvGen closure
of the independent adjacent square and its genuine contexts. -/
def KuuNativeF44ExchangeEqv
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (p q : KuuNativeF44Ordered n m ma pa mb pb) : Prop :=
  Relation.EqvGen (fun r s => KuuNativeF44AdjacentSwap r s) p q

/-- The three equivalence laws come from EqvGen, not from added
source-cell laws or a synthetic identification of all paths. -/
theorem KuuNativeF44ExchangeEqv.equivalence
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y} :
    Equivalence (KuuNativeF44ExchangeEqv (A := A) (B := B)
      (n := n) (m := m) (ma := ma) (mb := mb) (pa := pa) (pb := pb)) :=
  Relation.EqvGen.is_equivalence _

/-- Proof-relevant ordered operations modulo the precise generated
independent adjacent-swap relation.  The raw witnesses remain
different before taking this explicitly selected quotient. -/
def KuuNativeF44ExchangeClass
    {a b : A} {x y : B} (n m : Nat)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    Type (max (max uA uB) (max vA vB)) :=
  Quot (fun p q : KuuNativeF44Ordered n m ma pa mb pb =>
    KuuNativeF44AdjacentSwap p q)

/-- The canonical map into the actual generated exchange quotient. -/
def KuuNativeF44Ordered.toExchangeClass
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (p : KuuNativeF44Ordered n m ma pa mb pb) :
    KuuNativeF44ExchangeClass n m ma mb pa pb :=
  Quot.mk _ p

/-- The quotient identifies EXACTLY the reflexive/symmetric/transitive
closure of the named primitive adjacent-exchange generators. -/
theorem kuuNativeF44ExchangeEqv_iff_class_eq
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (p q : KuuNativeF44Ordered n m ma pa mb pb) :
    KuuNativeF44ExchangeEqv p q ↔
      p.toExchangeClass = q.toExchangeClass := by
  constructor
  · exact Quot.eqvGen_sound
  · exact Quot.eqvGen_exact

/-- Honest descent of BOTH original-shaped, Type-valued complete
histories: the proof is the generating square's actual equality. -/
def KuuNativeF44ExchangeClass.histories
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (c : KuuNativeF44ExchangeClass n m ma mb pa pb) :
    KuuNativeAxisTrace n ma mb × KuuNativeAxisTrace m pa pb :=
  Quot.liftOn c (fun p => p.histories)
    (by
      intro p q h
      exact KuuNativeF44AdjacentSwap.histories_eq h)

/-- The quotient evaluator computes on each real representative,
not only on existence or a numerical grade. -/
theorem KuuNativeF44Ordered.histories_toExchangeClass
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (p : KuuNativeF44Ordered n m ma pa mb pb) :
    p.toExchangeClass.histories = p.histories :=
  rfl

/-- Every generated exchange preserves both full Type-valued
primitive histories, by quotient soundness and descent. -/
theorem KuuNativeF44ExchangeEqv.histories_eq
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {p q : KuuNativeF44Ordered n m ma pa mb pb}
    (h : KuuNativeF44ExchangeEqv p q) :
    p.histories = q.histories := by
  have hc : p.toExchangeClass = q.toExchangeClass :=
    (kuuNativeF44ExchangeEqv_iff_class_eq p q).1 h
  exact (p.histories_toExchangeClass).symm.trans
    ((congrArg KuuNativeF44ExchangeClass.histories hc).trans
      q.histories_toExchangeClass)

/-- The actual F19-then-F28 and F28-then-F19 raw unit-step words
are a specific source square, not only a charge coincidence. -/
theorem nativeF44UnitOrders_adjacentSwap
    {a b : A} {x y : B}
    (ma : KuuNativeBlocks a b) (pa : KuuNativeBlocks x y) :
    KuuNativeF44AdjacentSwap
      (KuuNativeF44Ordered.fromF45Order .firstAxisFirst
        (KuuNativeAxisTrace.insertNilOnce ma)
        (KuuNativeAxisTrace.insertNilOnce pa))
      (KuuNativeF44Ordered.fromF45Order .secondAxisFirst
        (KuuNativeAxisTrace.insertNilOnce ma)
        (KuuNativeAxisTrace.insertNilOnce pa)) := by
  change KuuNativeF44AdjacentSwap
    (.second (.first (.refl ma pa) (.insertNil ma)) (.insertNil pa))
    (.first (.second (.refl ma pa) (.insertNil pa)) (.insertNil ma))
  exact .square (.refl ma pa) (.insertNil ma) (.insertNil pa)

/-- These two raw-distinct orderings become equal only AFTER the
explicit independently generated F44 adjacent-swap quotient. -/
theorem nativeF44UnitOrders_class_eq
    {a b : A} {x y : B}
    (ma : KuuNativeBlocks a b) (pa : KuuNativeBlocks x y) :
    (KuuNativeF44Ordered.fromF45Order .firstAxisFirst
      (KuuNativeAxisTrace.insertNilOnce ma)
      (KuuNativeAxisTrace.insertNilOnce pa)).toExchangeClass =
    (KuuNativeF44Ordered.fromF45Order .secondAxisFirst
      (KuuNativeAxisTrace.insertNilOnce ma)
      (KuuNativeAxisTrace.insertNilOnce pa)).toExchangeClass :=
  Quot.sound (nativeF44UnitOrders_adjacentSwap ma pa)

#print axioms KuuNativeF44AdjacentSwap
#print axioms KuuNativeF44AdjacentSwap.histories_eq
#print axioms KuuNativeF44ExchangeEqv
#print axioms KuuNativeF44ExchangeEqv.equivalence
#print axioms KuuNativeF44ExchangeClass.histories
#print axioms kuuNativeF44ExchangeEqv_iff_class_eq
#print axioms KuuNativeF44ExchangeEqv.histories_eq
#print axioms nativeF44UnitOrders_adjacentSwap
#print axioms nativeF44UnitOrders_class_eq

end
end Kuu.F112.Physical
