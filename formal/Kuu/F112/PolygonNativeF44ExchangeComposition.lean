import Kuu.F112.PolygonNativeF44AdjacentExchange

/-!
# F112-E7Q5-F4-M2 — native F44 exchange is a true compositional congruence

No source-history equivalence is postulated.  We prove that the
independent original-shaped generating square remains a generating
square after ANY real prefix or suffix of Type-valued F19/F28
operations; hence actual typed raw composition descends to Quot.

Both Type-valued axis histories are preserved separately by this
quotient composition.  We also descend the arbitrarily bracketed
genuine C60 F45 source's raw F44 execution, keeping its physical
bracket and its source categorical histories in separate components.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uA vA uB vB
variable {A : Type uA} [Category.{vA} A]
variable {B : Type uB} [Category.{vB} B]

/-- The actual primitive adjacent square survives any genuine
subsequent ordered F19/F28 operation chain. -/
theorem KuuNativeF44AdjacentSwap.appendSuffix
    {a b : A} {x y : B} {n m n' m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    {p q : KuuNativeF44Ordered n m ma pa mb pb}
    (h : KuuNativeF44AdjacentSwap p q)
    (later : KuuNativeF44Ordered n' m' mb pb mc pc) :
    KuuNativeF44AdjacentSwap (p.append later) (q.append later) := by
  induction later with
  | refl =>
      simpa only [KuuNativeF44Ordered.append, Nat.add_zero] using h
  | first later step ih =>
      simpa only [KuuNativeF44Ordered.append, Nat.add_succ] using
        (KuuNativeF44AdjacentSwap.afterFirst (ih h) step)
  | second later step ih =>
      simpa only [KuuNativeF44Ordered.append, Nat.add_succ] using
        (KuuNativeF44AdjacentSwap.afterSecond (ih h) step)

/-- The same generator survives arbitrary genuine earlier
F19/F28 prefixes, including all nested original intermediate Blocks. -/
theorem KuuNativeF44AdjacentSwap.appendPrefix
    {a b : A} {x y : B} {n m n' m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF44Ordered n m ma pa mb pb)
    {p q : KuuNativeF44Ordered n' m' mb pb mc pc}
    (h : KuuNativeF44AdjacentSwap p q) :
    KuuNativeF44AdjacentSwap (earlier.append p) (earlier.append q) := by
  induction h with
  | square initial hf hs =>
      simpa only [KuuNativeF44Ordered.append, Nat.add_succ] using
        (KuuNativeF44AdjacentSwap.square (earlier.append initial) hf hs)
  | afterFirst h step ih =>
      simpa only [KuuNativeF44Ordered.append, Nat.add_succ] using
        (KuuNativeF44AdjacentSwap.afterFirst (ih earlier) step)
  | afterSecond h step ih =>
      simpa only [KuuNativeF44Ordered.append, Nat.add_succ] using
        (KuuNativeF44AdjacentSwap.afterSecond (ih earlier) step)

/-- The generated adjacent-swap Quot carries a genuinely typed
original-shaped F44 concatenation.  Both congruence arguments are
independently discharged by actual local squares. -/
def KuuNativeF44ExchangeClass.append
    {a b : A} {x y : B} {n m n' m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (h : KuuNativeF44ExchangeClass n m ma mb pa pb)
    (k : KuuNativeF44ExchangeClass n' m' mb mc pb pc) :
    KuuNativeF44ExchangeClass (n + n') (m + m') ma mc pa pc :=
  Quot.liftOn₂ h k
    (fun p q => (p.append q).toExchangeClass)
    (by
      intro earlier later₁ later₂ hs
      exact Quot.sound (KuuNativeF44AdjacentSwap.appendPrefix earlier hs))
    (by
      intro earlier₁ earlier₂ later hs
      exact Quot.sound (KuuNativeF44AdjacentSwap.appendSuffix hs later))

/-- On representative witnesses, genuine quotient composition agrees
exactly with raw F44 source composition. -/
theorem KuuNativeF44Ordered.append_toExchangeClass
    {a b : A} {x y : B} {n m n' m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (h : KuuNativeF44Ordered n m ma pa mb pb)
    (k : KuuNativeF44Ordered n' m' mb pb mc pc) :
    (h.append k).toExchangeClass =
      h.toExchangeClass.append k.toExchangeClass :=
  rfl

/-- Exact history preservation extends to ANY pair of quotient
classes, using the source-level Type-valued history concatenation. -/
theorem KuuNativeF44ExchangeClass.histories_append
    {a b : A} {x y : B} {n m n' m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (h : KuuNativeF44ExchangeClass n m ma mb pa pb)
    (k : KuuNativeF44ExchangeClass n' m' mb mc pb pc) :
    (h.append k).histories =
      (h.histories.1.append k.histories.1,
        h.histories.2.append k.histories.2) := by
  refine Quot.inductionOn h ?_
  intro p
  refine Quot.inductionOn k ?_
  intro q
  exact KuuNativeF44Ordered.histories_append p q

/-- Both independently chosen original categorical composites agree
after composition ON THE GENUINE generated exchange quotient. -/
theorem KuuNativeF44ExchangeClass.append_composites
    {a b : A} {x y : B} {n m n' m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (h : KuuNativeF44ExchangeClass n m ma mb pa pb)
    (k : KuuNativeF44ExchangeClass n' m' mb mc pb pc) :
    ma.composite = mc.composite ∧ pa.composite = pc.composite :=
  ⟨(h.append k).histories.1.composite_eq,
    (h.append k).histories.2.composite_eq⟩

/-- Primitive first-axis context acts on the genuine exchange
quotient, since afterFirst is a proved generating congruence. -/
def KuuNativeF44ExchangeClass.afterFirst
    {a b : A} {x y : B} {n m : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (c : KuuNativeF44ExchangeClass n m ma mb pa pb)
    (hf : KuuNativeOneStep mb mc) :
    KuuNativeF44ExchangeClass (n + 1) m ma mc pa pb :=
  Quot.liftOn c (fun p => (KuuNativeF44Ordered.first p hf).toExchangeClass)
    (by
      intro p q h
      exact Quot.sound (KuuNativeF44AdjacentSwap.afterFirst h hf))

/-- The independent second-axis context also acts as a well-defined
operation on the actual generated quotient, preserving its order. -/
def KuuNativeF44ExchangeClass.afterSecond
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (c : KuuNativeF44ExchangeClass n m ma mb pa pb)
    (hs : KuuNativeOneStep pb pc) :
    KuuNativeF44ExchangeClass n (m + 1) ma mb pa pc :=
  Quot.liftOn c (fun p => (KuuNativeF44Ordered.second p hs).toExchangeClass)
    (by
      intro p q h
      exact Quot.sound (KuuNativeF44AdjacentSwap.afterSecond h hs))

/-- Any actual native F45 bracketing canonically produces a class of
F44 executions, with the physically real source retained separately. -/
def KuuNativeF45Tree.exchangePacket
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    PolygonDepthTree p n m ×
      KuuNativeF44ExchangeClass n m ma mb pa pb :=
  (tree.erasePhysical, tree.executeF44.toExchangeClass)

/-- No C60 boundary sector is lost by the independent actual
F44 generated quotient: the entire genuine bracketing is separate. -/
theorem KuuNativeF45Tree.exchangePacket_sectors
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    tree.exchangePacket.1.erase.leaves = tree.sectors :=
  tree.erasePhysical_leaves

/-- The F45 class recovers BOTH complete, independent source
Type-valued primitive-operation histories with all original Blocks. -/
theorem KuuNativeF45Tree.exchangePacket_histories
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    tree.exchangePacket.2.histories = tree.axisHistories := by
  exact (KuuNativeF44Ordered.histories_toExchangeClass
    tree.executeF44).trans tree.executeF44_histories

#print axioms KuuNativeF44AdjacentSwap.appendSuffix
#print axioms KuuNativeF44AdjacentSwap.appendPrefix
#print axioms KuuNativeF44ExchangeClass.append
#print axioms KuuNativeF44ExchangeClass.histories_append
#print axioms KuuNativeF44ExchangeClass.afterFirst
#print axioms KuuNativeF44ExchangeClass.afterSecond
#print axioms KuuNativeF45Tree.exchangePacket_sectors
#print axioms KuuNativeF45Tree.exchangePacket_histories
end
end Kuu.F112.Physical
