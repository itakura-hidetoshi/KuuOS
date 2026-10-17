import Kuu.F112.PolygonNativeF44ExchangeClassification
import Kuu.F112.PolygonNativeF45FunctorAxes

/-!
# F112-E7Q5-F4-N1 — true two-axis functor transport of raw F44 and its square

Use arbitrary independent functors on the original categorical axes.
Map every original F40 Blocks partition, primitive Type-valued F41
step and each step of the genuinely ordered F44 proof word.

The two exact Type-valued axis histories commute with transport.
Most importantly, the ONLY original-shaped F44 interchange
generator (the F19/F28 adjacent square and both suffix contexts)
is preserved as a proof of an actual adjacent square.

No historical KUOS/Gray imports and no interchange inferred from
a numerical grade, final Hom equality or proof-irrelevant shadow.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uA vA uB vB uC vC uD vD
variable {A : Type uA} [Category.{vA} A]
variable {B : Type uB} [Category.{vB} B]
variable {C : Type uC} [Category.{vC} C]
variable {D : Type uD} [Category.{vD} D]

/-- Transport a genuine F44 interleaving by independently mapping
each original category, block boundary and primitive Type witness. -/
def KuuNativeF44Ordered.mapAxes
    (F : A ⥤ C) (G : B ⥤ D)
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (h : KuuNativeF44Ordered n m ma pa mb pb) :
    KuuNativeF44Ordered n m
      (ma.map F) (pa.map G) (mb.map F) (pb.map G) := by
  induction h with
  | refl ma pa =>
      exact .refl (ma.map F) (pa.map G)
  | first h step ih =>
      exact .first ih (step.map F)
  | second h step ih =>
      exact .second ih (step.map G)

/-- Preserve the ACTUAL complete F19-like Type-valued history,
including every primitive step and intermediate categorical Blocks. -/
theorem KuuNativeF44Ordered.firstHistory_mapAxes
    (F : A ⥤ C) (G : B ⥤ D)
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (h : KuuNativeF44Ordered n m ma pa mb pb) :
    (h.mapAxes F G).firstHistory = h.firstHistory.map F := by
  induction h with
  | refl ma pa =>
      rfl
  | first h step ih =>
      change KuuNativeAxisTrace.snoc
          (h.mapAxes F G).firstHistory (step.map F) =
        KuuNativeAxisTrace.snoc (h.firstHistory.map F) (step.map F)
      exact congrArg (fun z => KuuNativeAxisTrace.snoc z (step.map F)) ih
  | second h step ih =>
      exact ih

/-- Independently preserve the ACTUAL complete F28-like Type history. -/
theorem KuuNativeF44Ordered.secondHistory_mapAxes
    (F : A ⥤ C) (G : B ⥤ D)
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (h : KuuNativeF44Ordered n m ma pa mb pb) :
    (h.mapAxes F G).secondHistory = h.secondHistory.map G := by
  induction h with
  | refl ma pa =>
      rfl
  | first h step ih =>
      exact ih
  | second h step ih =>
      change KuuNativeAxisTrace.snoc
          (h.mapAxes F G).secondHistory (step.map G) =
        KuuNativeAxisTrace.snoc (h.secondHistory.map G) (step.map G)
      exact congrArg (fun z => KuuNativeAxisTrace.snoc z (step.map G)) ih

/-- The FULL proof-relevant pair commutes with independent functors,
before ANY generated exchange quotient is imposed. -/
theorem KuuNativeF44Ordered.histories_mapAxes
    (F : A ⥤ C) (G : B ⥤ D)
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (h : KuuNativeF44Ordered n m ma pa mb pb) :
    (h.mapAxes F G).histories =
      (h.firstHistory.map F, h.secondHistory.map G) :=
  Prod.ext (h.firstHistory_mapAxes F G) (h.secondHistory_mapAxes F G)

/-- The actual generating F19/F28 adjacent square is respected,
with TWO arbitrarily unrelated category functors and the original
Type-valued witnesses transported by their exact constructors. -/
theorem KuuNativeF44AdjacentSwap.mapAxes
    (F : A ⥤ C) (G : B ⥤ D)
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {p q : KuuNativeF44Ordered n m ma pa mb pb}
    (h : KuuNativeF44AdjacentSwap p q) :
    KuuNativeF44AdjacentSwap (p.mapAxes F G) (q.mapAxes F G) := by
  induction h with
  | square initial hf hs =>
      exact .square (initial.mapAxes F G) (hf.map F) (hs.map G)
  | afterFirst h step ih =>
      exact .afterFirst ih (step.map F)
  | afterSecond h step ih =>
      exact .afterSecond ih (step.map G)

#print axioms KuuNativeF44Ordered.mapAxes
#print axioms KuuNativeF44Ordered.firstHistory_mapAxes
#print axioms KuuNativeF44Ordered.secondHistory_mapAxes
#print axioms KuuNativeF44Ordered.histories_mapAxes
#print axioms KuuNativeF44AdjacentSwap.mapAxes
end
end Kuu.F112.Physical
