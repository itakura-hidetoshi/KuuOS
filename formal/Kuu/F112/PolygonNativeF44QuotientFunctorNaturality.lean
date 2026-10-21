import Kuu.F112.PolygonNativeF44FunctorTransport

/-!
# F112-E7Q5-F4-N2 — two-axis functor descent through the F44 exchange Quot

The original F19-shaped and F28-shaped categorical sources are
mapped INDEPENDENTLY by arbitrary ordinary functors.  N1 proves
that actual adjacent-swap generators map to actual generators.
Consequently the quotient functor can be built with Quot.liftOn,
not assumed by a Gray exchange or quotient shadow equation.

The entire Type-valued two-axis history pair is strictly natural.
This makes the verified M3 historyEquiv commute with the independently
functorial axis-history product.  Genuine quotient concatenation and
both source operation contexts commute with the same map.
No frozen KUOS, Gray, F51, or F77 import.
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

/-- The actual mapped exchange class is defined by Quot.liftOn:
its well-definedness is the explicit mapped adjacent square. -/
def KuuNativeF44ExchangeClass.mapAxes
    (F : A ⥤ C) (G : B ⥤ D)
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (c : KuuNativeF44ExchangeClass n m ma mb pa pb) :
    KuuNativeF44ExchangeClass n m
      (ma.map F) (mb.map F) (pa.map G) (pb.map G) :=
  Quot.liftOn c
    (fun p => (p.mapAxes F G).toExchangeClass)
    (by
      intro p q h
      exact Quot.sound (KuuNativeF44AdjacentSwap.mapAxes F G h))

/-- Every original raw representative computes exactly under
the newly defined quotient map — not by a chosen representative. -/
theorem KuuNativeF44Ordered.mapAxes_toExchangeClass
    (F : A ⥤ C) (G : B ⥤ D)
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (p : KuuNativeF44Ordered n m ma pa mb pb) :
    p.toExchangeClass.mapAxes F G =
      (p.mapAxes F G).toExchangeClass :=
  rfl

/-- Transport of any generated exchange equivalence follows from
the TRUE quotient action, not an asserted global Gray law. -/
theorem KuuNativeF44ExchangeEqv.mapAxes
    (F : A ⥤ C) (G : B ⥤ D)
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {p q : KuuNativeF44Ordered n m ma pa mb pb}
    (h : KuuNativeF44ExchangeEqv p q) :
    KuuNativeF44ExchangeEqv (p.mapAxes F G) (q.mapAxes F G) := by
  apply (kuuNativeF44ExchangeEqv_iff_class_eq _ _).2
  have hc : p.toExchangeClass = q.toExchangeClass :=
    (kuuNativeF44ExchangeEqv_iff_class_eq p q).1 h
  exact congrArg (fun c => c.mapAxes F G) hc

/-- Natural transport of the COMPLETE pair of Type-valued
histories from the generated exchange quotient, at all Nat depths. -/
theorem KuuNativeF44ExchangeClass.histories_mapAxes
    (F : A ⥤ C) (G : B ⥤ D)
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (c : KuuNativeF44ExchangeClass n m ma mb pa pb) :
    (c.mapAxes F G).histories =
      (c.histories.1.map F, c.histories.2.map G) := by
  refine Quot.inductionOn c ?_
  intro p
  exact p.histories_mapAxes F G

/-- Genuine M3 Mathlib historyEquiv is natural in EACH of the two
independent category axes, not merely in Hom evaluations or Nat grades. -/
theorem KuuNativeF44ExchangeClass.historyEquiv_mapAxes
    (F : A ⥤ C) (G : B ⥤ D)
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (c : KuuNativeF44ExchangeClass n m ma mb pa pb) :
    (KuuNativeF44ExchangeClass.historyEquiv
        (ma.map F) (mb.map F) (pa.map G) (pb.map G))
        (c.mapAxes F G) =
      (((KuuNativeF44ExchangeClass.historyEquiv ma mb pa pb) c).1.map F,
       ((KuuNativeF44ExchangeClass.historyEquiv ma mb pa pb) c).2.map G) :=
  c.histories_mapAxes F G

/-- Strict raw F44 concatenation naturality retains the actual
intermediate original F40 Blocks and every Type-valued operation. -/
theorem KuuNativeF44Ordered.mapAxes_append
    (F : A ⥤ C) (G : B ⥤ D)
    {a b : A} {x y : B} {n m n' m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (h : KuuNativeF44Ordered n m ma pa mb pb)
    (k : KuuNativeF44Ordered n' m' mb pb mc pc) :
    (h.append k).mapAxes F G =
      (h.mapAxes F G).append (k.mapAxes F G) := by
  induction k with
  | refl =>
      rfl
  | first k step ih =>
      change KuuNativeF44Ordered.first
          ((h.append k).mapAxes F G) (step.map F) =
        KuuNativeF44Ordered.first
          ((h.mapAxes F G).append (k.mapAxes F G)) (step.map F)
      exact congrArg
        (fun z => KuuNativeF44Ordered.first z (step.map F)) (ih h)
  | second k step ih =>
      change KuuNativeF44Ordered.second
          ((h.append k).mapAxes F G) (step.map G) =
        KuuNativeF44Ordered.second
          ((h.mapAxes F G).append (k.mapAxes F G)) (step.map G)
      exact congrArg
        (fun z => KuuNativeF44Ordered.second z (step.map G)) (ih h)

/-- The actual exchange-quotient concatenation law is natural in
arbitrary independent F19/F28 source category functors. -/
theorem KuuNativeF44ExchangeClass.mapAxes_append
    (F : A ⥤ C) (G : B ⥤ D)
    {a b : A} {x y : B} {n m n' m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (h : KuuNativeF44ExchangeClass n m ma mb pa pb)
    (k : KuuNativeF44ExchangeClass n' m' mb mc pb pc) :
    (h.append k).mapAxes F G =
      (h.mapAxes F G).append (k.mapAxes F G) := by
  refine Quot.inductionOn h ?_
  intro p
  refine Quot.inductionOn k ?_
  intro q
  exact congrArg KuuNativeF44Ordered.toExchangeClass
    (KuuNativeF44Ordered.mapAxes_append F G p q)

/-- The first-axis primitive contextual action is natural at the
actual generated exchange quotient level. -/
theorem KuuNativeF44ExchangeClass.mapAxes_afterFirst
    (F : A ⥤ C) (G : B ⥤ D)
    {a b : A} {x y : B} {n m : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (c : KuuNativeF44ExchangeClass n m ma mb pa pb)
    (f : KuuNativeOneStep mb mc) :
    (c.afterFirst f).mapAxes F G =
      (c.mapAxes F G).afterFirst (f.map F) := by
  refine Quot.inductionOn c ?_
  intro p
  rfl

/-- The second-axis primitive contextual action is equally natural
without identifying first-axis and second-axis category types. -/
theorem KuuNativeF44ExchangeClass.mapAxes_afterSecond
    (F : A ⥤ C) (G : B ⥤ D)
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (c : KuuNativeF44ExchangeClass n m ma mb pa pb)
    (f : KuuNativeOneStep pb pc) :
    (c.afterSecond f).mapAxes F G =
      (c.mapAxes F G).afterSecond (f.map G) := by
  refine Quot.inductionOn c ?_
  intro p
  rfl

#print axioms KuuNativeF44ExchangeClass.mapAxes
#print axioms KuuNativeF44Ordered.mapAxes_toExchangeClass
#print axioms KuuNativeF44ExchangeEqv.mapAxes
#print axioms KuuNativeF44ExchangeClass.histories_mapAxes
#print axioms KuuNativeF44ExchangeClass.historyEquiv_mapAxes
#print axioms KuuNativeF44Ordered.mapAxes_append
#print axioms KuuNativeF44ExchangeClass.mapAxes_append
#print axioms KuuNativeF44ExchangeClass.mapAxes_afterFirst
#print axioms KuuNativeF44ExchangeClass.mapAxes_afterSecond
end
end Kuu.F112.Physical
