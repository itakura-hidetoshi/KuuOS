import Kuu.F112.PolygonNativeF44OrderedHistoricalComparison

/-!
# F112-E7Q5-F4-L2 — all independent F45 bracket trees execute as F44 words

The frozen v5.291 F44 construction concatenates original typed
F19/F28 primitive interleavings. The new independent F4-L grammar
reconstructs this precise *constructor shape* with genuinely Type
valued primitive steps (the frozen OneStep was Prop valued).

This file proves exact concatenation on both axes, then executes
EVERY constructor of the new genuine C60 F45 grammar as a genuine
two-axis F44 ordered word: refl, both original F45 leaf orders and
arbitrary binary-node compositions, with no bound on Nat depths.

The execution packet retains the full physical PolygonDepthTree
bracketing independently of the complete Type-valued two-axis
ordered witness. All axis histories and every ordered C60 sector
are preserved. The map does NOT assert a raw inverse, an original
F44 exchange quotient, or equivalence with any frozen KUOS type.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uA vA uB vB
variable {A : Type uA} [Category.{vA} A]
variable {B : Type uB} [Category.{vB} B]

/-- Compose two genuine ordered F19/F28 primitive sequences while
retaining both independent depths and all intermediate Blocks. -/
def KuuNativeF44Ordered.append
    {a b : A} {x y : B}
    {n m n' m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (h : KuuNativeF44Ordered n m ma pa mb pb)
    (k : KuuNativeF44Ordered n' m' mb pb mc pc) :
    KuuNativeF44Ordered (n + n') (m + m') ma pa mc pc := by
  induction k with
  | refl =>
      simpa only [Nat.add_zero] using h
  | first k step ih =>
      simpa only [Nat.add_succ] using
        (KuuNativeF44Ordered.first (ih h) step)
  | second k step ih =>
      simpa only [Nat.add_succ] using
        (KuuNativeF44Ordered.second (ih h) step)

/-- First history of a concatenated word is EXACT concatenation
of the genuine Type-valued independent primitive source traces. -/
theorem KuuNativeF44Ordered.firstHistory_append
    {a b : A} {x y : B}
    {n m n' m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (h : KuuNativeF44Ordered n m ma pa mb pb)
    (k : KuuNativeF44Ordered n' m' mb pb mc pc) :
    (h.append k).firstHistory =
      h.firstHistory.append k.firstHistory := by
  induction k with
  | refl =>
      rfl
  | first k step ih =>
      change KuuNativeAxisTrace.snoc
          (h.append k).firstHistory step =
        KuuNativeAxisTrace.snoc
          (h.firstHistory.append k.firstHistory) step
      exact congrArg (fun z => KuuNativeAxisTrace.snoc z step) ih
  | second k step ih =>
      exact ih

/-- Second history obeys the corresponding separate concatenation
law even when first-axis steps are arbitrarily interleaved. -/
theorem KuuNativeF44Ordered.secondHistory_append
    {a b : A} {x y : B}
    {n m n' m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (h : KuuNativeF44Ordered n m ma pa mb pb)
    (k : KuuNativeF44Ordered n' m' mb pb mc pc) :
    (h.append k).secondHistory =
      h.secondHistory.append k.secondHistory := by
  induction k with
  | refl =>
      rfl
  | first k step ih =>
      exact ih
  | second k step ih =>
      change KuuNativeAxisTrace.snoc
          (h.append k).secondHistory step =
        KuuNativeAxisTrace.snoc
          (h.secondHistory.append k.secondHistory) step
      exact congrArg (fun z => KuuNativeAxisTrace.snoc z step) ih

/-- Both proof-relevant native histories are exactly additive under
arbitrary concatenation of original F44-shaped ordered words. -/
theorem KuuNativeF44Ordered.histories_append
    {a b : A} {x y : B}
    {n m n' m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (h : KuuNativeF44Ordered n m ma pa mb pb)
    (k : KuuNativeF44Ordered n' m' mb pb mc pc) :
    (h.append k).histories =
      (h.firstHistory.append k.firstHistory,
       h.secondHistory.append k.secondHistory) :=
  Prod.ext (h.firstHistory_append k) (h.secondHistory_append k)

/-- An actual F44 interleaving can be compiled from EACH genuinely
proof-relevant F45 source constructor, including arbitrary
composable original categorical block-node presentations. -/
def KuuNativeF45Tree.executeF44
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    KuuNativeF44Ordered n m ma pa mb pb := by
  induction tree with
  | refl i ma pa =>
      exact .refl ma pa
  | leaf i order firstAxis secondAxis =>
      exact .fromF45Order order firstAxis secondAxis
  | node first second ihFirst ihSecond =>
      exact ihFirst.append ihSecond

/-- Exactly restore BOTH original complete independent
Type-valued histories after executing the WHOLE F45 binary tree.
No Prop evidence erasure or raw source quotient is used. -/
theorem KuuNativeF45Tree.executeF44_histories
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    tree.executeF44.histories = tree.axisHistories := by
  induction tree with
  | refl i ma pa =>
      rfl
  | leaf i order firstAxis secondAxis =>
      exact KuuNativeF44Ordered.fromF45Order_histories
        order firstAxis secondAxis
  | node first second ihFirst ihSecond =>
      apply Prod.ext
      · change
          (first.executeF44.append second.executeF44).firstHistory =
            KuuNativeAxisTrace.append
              first.axisHistories.1 second.axisHistories.1
        rw [KuuNativeF44Ordered.firstHistory_append]
        have hf : first.executeF44.firstHistory = first.axisHistories.1 :=
          congrArg (fun z => z.1) ihFirst
        have hs : second.executeF44.firstHistory = second.axisHistories.1 :=
          congrArg (fun z => z.1) ihSecond
        rw [hf, hs]
      · change
          (first.executeF44.append second.executeF44).secondHistory =
            KuuNativeAxisTrace.append
              first.axisHistories.2 second.axisHistories.2
        rw [KuuNativeF44Ordered.secondHistory_append]
        have hf : first.executeF44.secondHistory = first.axisHistories.2 :=
          congrArg (fun z => z.2) ihFirst
        have hs : second.executeF44.secondHistory = second.axisHistories.2 :=
          congrArg (fun z => z.2) ihSecond
        rw [hf, hs]

/-- A fully typed physical-and-categorical execution packet.
Physical bracketing is NOT inferred from the ordered F44 word,
and neither component is silently replaced by a numeric shadow. -/
def KuuNativeF45Tree.executionPacket
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    (PolygonDepthTree p n m) ×
      (KuuNativeF44Ordered n m ma pa mb pb) :=
  (tree.erasePhysical, tree.executeF44)

/-- The first component recovers the complete bracketed real
physical C60 source, including its ordered sector list. -/
theorem KuuNativeF45Tree.executionPacket_sectors
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    (tree.executionPacket.1).erase.leaves = tree.sectors :=
  tree.erasePhysical_leaves

/-- The other component restores both FULL independent source
axis histories, for every nested F45 node and original leaf order. -/
theorem KuuNativeF45Tree.executionPacket_histories
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    tree.executionPacket.2.histories = tree.axisHistories :=
  tree.executeF44_histories

/-- Two original categorical arrow composite equations hold
independently, derived from the actual executed F44 proof and
not from a "same grade" or historical Gray coherence axiom. -/
theorem KuuNativeF45Tree.executeF44_composites
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    ma.composite = mb.composite ∧ pa.composite = pb.composite :=
  ⟨tree.executeF44.firstHistory.composite_eq,
    tree.executeF44.secondHistory.composite_eq⟩

#print axioms KuuNativeF44Ordered.append
#print axioms KuuNativeF44Ordered.histories_append
#print axioms KuuNativeF45Tree.executeF44
#print axioms KuuNativeF45Tree.executeF44_histories
#print axioms KuuNativeF45Tree.executionPacket_sectors
#print axioms KuuNativeF45Tree.executionPacket_histories
#print axioms KuuNativeF45Tree.executeF44_composites
end
end Kuu.F112.Physical
