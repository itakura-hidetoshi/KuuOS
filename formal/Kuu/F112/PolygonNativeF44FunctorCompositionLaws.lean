import Kuu.F112.PolygonNativeF41TraceFunctorComposition

/-!
# F112-E7Q5-F4-O3 — independent F44 raw two-axis functor laws

All genuine F41 primitive Type-valued proofs satisfy identity and
composition (O2-C/D4). For the F44 raw Ordered grammar each leaf
remains a typed F19- or F28-axis primitive. Here the actual raw
constructors, all intermediate F40 Blocks, and both source
categories are kept separate in dependent HEq congruences.

No generated adjacent-swap quotient is used to identify raw words.
No frozen original KUOS/Gray/F51/F77 import.
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

/-- Dependent congruence for a genuine FIRST-axis primitive in the
F44 ordered word, retaining all five original indexed Blocks and
both Type-valued source/history witnesses. -/
theorem KuuNativeF44Ordered.first_heq_of_heq
    {a b : A} {x y : B} {n m : Nat}
    {ma ma' mb mb' mc mc' : KuuNativeBlocks a b}
    {pa pa' pb pb' : KuuNativeBlocks x y}
    (h : KuuNativeF44Ordered n m ma pa mb pb)
    (h' : KuuNativeF44Ordered n m ma' pa' mb' pb')
    (step : KuuNativeOneStep mb mc)
    (step' : KuuNativeOneStep mb' mc')
    (hma : ma = ma') (hpa : pa = pa')
    (hmb : mb = mb') (hpb : pb = pb') (hmc : mc = mc')
    (hh : HEq h h') (hs : HEq step step') :
    HEq (KuuNativeF44Ordered.first h step)
      (KuuNativeF44Ordered.first h' step') := by
  cases hma
  cases hpa
  cases hmb
  cases hpb
  cases hmc
  have he : h = h' := eq_of_heq hh
  have se : step = step' := eq_of_heq hs
  cases he
  cases se
  rfl

/-- The corresponding genuine SECOND-axis context congruence
never conflates the two potentially unrelated category types. -/
theorem KuuNativeF44Ordered.second_heq_of_heq
    {a b : A} {x y : B} {n m : Nat}
    {ma ma' mb mb' : KuuNativeBlocks a b}
    {pa pa' pb pb' pc pc' : KuuNativeBlocks x y}
    (h : KuuNativeF44Ordered n m ma pa mb pb)
    (h' : KuuNativeF44Ordered n m ma' pa' mb' pb')
    (step : KuuNativeOneStep pb pc)
    (step' : KuuNativeOneStep pb' pc')
    (hma : ma = ma') (hpa : pa = pa')
    (hmb : mb = mb') (hpb : pb = pb') (hpc : pc = pc')
    (hh : HEq h h') (hs : HEq step step') :
    HEq (KuuNativeF44Ordered.second h step)
      (KuuNativeF44Ordered.second h' step') := by
  cases hma
  cases hpa
  cases hmb
  cases hpb
  cases hpc
  have he : h = h' := eq_of_heq hh
  have se : step = step' := eq_of_heq hs
  cases he
  cases se
  rfl

/-- Entire genuinely ordered F44 source words preserve identity
along both independent categorical axes, including every actual
Type-valued primitive witness. -/
theorem KuuNativeF44Ordered.mapAxes_id_heq
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (h : KuuNativeF44Ordered n m ma pa mb pb) :
    HEq (h.mapAxes (𝟭 A) (𝟭 B)) h := by
  induction h with
  | refl ma pa =>
      simp only [KuuNativeF44Ordered.mapAxes]
      rw [KuuNativeBlocks.map_id ma, KuuNativeBlocks.map_id pa]
      rfl
  | first h step ih =>
      exact KuuNativeF44Ordered.first_heq_of_heq
        (h.mapAxes (𝟭 A) (𝟭 B)) h (step.map (𝟭 A)) step
        (KuuNativeBlocks.map_id _) (KuuNativeBlocks.map_id _)
        (KuuNativeBlocks.map_id _) (KuuNativeBlocks.map_id _)
        (KuuNativeBlocks.map_id _) ih
        (KuuNativeOneStep.map_id_heq step)
  | second h step ih =>
      exact KuuNativeF44Ordered.second_heq_of_heq
        (h.mapAxes (𝟭 A) (𝟭 B)) h (step.map (𝟭 B)) step
        (KuuNativeBlocks.map_id _) (KuuNativeBlocks.map_id _)
        (KuuNativeBlocks.map_id _) (KuuNativeBlocks.map_id _)
        (KuuNativeBlocks.map_id _) ih
        (KuuNativeOneStep.map_id_heq step)

/-- Entire F44 raw words commute heterogeneously with arbitrary
compositions in EACH source category, retaining original primitive
witness trees rather than quotienting their order. -/
theorem KuuNativeF44Ordered.mapAxes_comp_heq
    (H : A ⥤ C) (J : C ⥤ E)
    (K : B ⥤ D) (L : D ⥤ F)
    {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (h : KuuNativeF44Ordered n m ma pa mb pb) :
    HEq (h.mapAxes (H ⋙ J) (K ⋙ L))
      ((h.mapAxes H K).mapAxes J L) := by
  induction h with
  | refl ma pa =>
      simp only [KuuNativeF44Ordered.mapAxes]
      rw [KuuNativeBlocks.map_comp H J ma,
        KuuNativeBlocks.map_comp K L pa]
      rfl
  | first h step ih =>
      exact KuuNativeF44Ordered.first_heq_of_heq
        (h.mapAxes (H ⋙ J) (K ⋙ L))
        ((h.mapAxes H K).mapAxes J L)
        (step.map (H ⋙ J)) ((step.map H).map J)
        (KuuNativeBlocks.map_comp H J _)
        (KuuNativeBlocks.map_comp K L _)
        (KuuNativeBlocks.map_comp H J _)
        (KuuNativeBlocks.map_comp K L _)
        (KuuNativeBlocks.map_comp H J _)
        ih (KuuNativeOneStep.map_comp_heq H J step)
  | second h step ih =>
      exact KuuNativeF44Ordered.second_heq_of_heq
        (h.mapAxes (H ⋙ J) (K ⋙ L))
        ((h.mapAxes H K).mapAxes J L)
        (step.map (K ⋙ L)) ((step.map K).map L)
        (KuuNativeBlocks.map_comp H J _)
        (KuuNativeBlocks.map_comp K L _)
        (KuuNativeBlocks.map_comp H J _)
        (KuuNativeBlocks.map_comp K L _)
        (KuuNativeBlocks.map_comp K L _)
        ih (KuuNativeOneStep.map_comp_heq K L step)

#print axioms KuuNativeF44Ordered.first_heq_of_heq
#print axioms KuuNativeF44Ordered.second_heq_of_heq
#print axioms KuuNativeF44Ordered.mapAxes_id_heq
#print axioms KuuNativeF44Ordered.mapAxes_comp_heq
end
end Kuu.F112.Physical
