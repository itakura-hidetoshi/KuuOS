import Kuu.F112.PolygonNativeF44FunctorCompositionLaws

/-!
# F112-E7Q5-F4-O4 — identity/composition on genuine F44 exchange classes

O3 proves identity and composition for the actual Type-valued,
strictly ordered independent F44 primitive words as HEq. Here those
laws descend through ONLY the generated adjacent F19/F28 swaps.
All source/target F40 Blocks remain indexed and require a typed
HEq comparison of quotient representatives.

No Gray action, numerical shadow, proof erasure, or frozen KUOS
historical equivalence is postulated.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uA vA uB vB uC vC uD vD uE vE uF vF
variable {A : Type uA} [Category.{vA} A]
variable {B : Type uB} [Category.{vB} B]
variable {C : Type uC} [Category.{vC} C]
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {F : Type uF} [Category.{vF} F]

/-- Carry a proof-relevant HEq of raw ordered witnesses through
the actual generated-exchange quotient, normalizing EVERY independent
F40 Blocks index before converting HEq to ordinary Eq. -/
theorem KuuNativeF44Ordered.toExchangeClass_heq_of_heq
    {a b : A} {x y : B} {n m : Nat}
    {ma ma' mb mb' : KuuNativeBlocks a b}
    {pa pa' pb pb' : KuuNativeBlocks x y}
    (h : KuuNativeF44Ordered n m ma pa mb pb)
    (k : KuuNativeF44Ordered n m ma' pa' mb' pb')
    (hma : ma = ma') (hmb : mb = mb')
    (hpa : pa = pa') (hpb : pb = pb')
    (hh : HEq h k) :
    HEq h.toExchangeClass k.toExchangeClass := by
  cases hma
  cases hmb
  cases hpa
  cases hpb
  have he : h = k := eq_of_heq hh
  cases he
  rfl

/-- The identity two-axis ordinary functor sends every genuine
F44 generated exchange class to itself UP TO its exact dependent
F40 Blocks reindexing. Quotient equality is not postulated. -/
theorem KuuNativeF44ExchangeClass.mapAxes_id_heq
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (c : KuuNativeF44ExchangeClass n m ma mb pa pb) :
    HEq (c.mapAxes (𝟭 A) (𝟭 B)) c := by
  refine Quot.inductionOn c ?_
  intro h
  exact KuuNativeF44Ordered.toExchangeClass_heq_of_heq
    (h.mapAxes (𝟭 A) (𝟭 B)) h
    (KuuNativeBlocks.map_id ma) (KuuNativeBlocks.map_id mb)
    (KuuNativeBlocks.map_id pa) (KuuNativeBlocks.map_id pb)
    (KuuNativeF44Ordered.mapAxes_id_heq h)

/-- Any independently chosen composable pair of ordinary
functors on BOTH axes satisfies the real F44 exchange-quotient
composition law, not just a history-count or Hom shadow law. -/
theorem KuuNativeF44ExchangeClass.mapAxes_comp_heq
    (H : A ⥤ C) (J : C ⥤ E)
    (K : B ⥤ D) (L : D ⥤ F)
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (c : KuuNativeF44ExchangeClass n m ma mb pa pb) :
    HEq (c.mapAxes (H ⋙ J) (K ⋙ L))
      ((c.mapAxes H K).mapAxes J L) := by
  refine Quot.inductionOn c ?_
  intro h
  exact KuuNativeF44Ordered.toExchangeClass_heq_of_heq
    (h.mapAxes (H ⋙ J) (K ⋙ L))
    ((h.mapAxes H K).mapAxes J L)
    (KuuNativeBlocks.map_comp H J ma)
    (KuuNativeBlocks.map_comp H J mb)
    (KuuNativeBlocks.map_comp K L pa)
    (KuuNativeBlocks.map_comp K L pb)
    (KuuNativeF44Ordered.mapAxes_comp_heq H J K L h)

#print axioms KuuNativeF44Ordered.toExchangeClass_heq_of_heq
#print axioms KuuNativeF44ExchangeClass.mapAxes_id_heq
#print axioms KuuNativeF44ExchangeClass.mapAxes_comp_heq
end
end Kuu.F112.Physical
