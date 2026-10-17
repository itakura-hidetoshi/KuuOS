import Kuu.F112.PolygonNativeFunctorPathBlocksLaws

/-!
# F112-E7Q5-F4-O2 — identity/composition for proof-relevant F41 witnesses

Unlike historical Prop-valued primitive F41 steps, the independent
KuuNativeOneStep has actual Type-valued witnesses of split, empty
block insertion and right context.  The functor identity and
composition laws below concern these actual witnesses and the
whole arbitrarily long F41 AxisTrace, not merely their evaluations
or the Prop-step erasure. No frozen KUOS/Gray/F51/F77 imports.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uA vA uB vB uC vC
variable {A : Type uA} [Category.{vA} A]
variable {B : Type uB} [Category.{vB} B]
variable {C : Type uC} [Category.{vC} C]

/-- Every actual F41 primitive witness is preserved by identity,
including its concrete split/insert/context constructor. -/
theorem KuuNativeOneStep.map_id
    {a b : A} {p q : KuuNativeBlocks a b}
    (h : KuuNativeOneStep p q) :
    h.map (𝟭 A) = h := by
  induction h with
  | split p q r =>
      simp [KuuNativeOneStep.map, KuuNativeBlocks.map_id,
        KuuNativePath.map_id]
  | insertNil p =>
      simp [KuuNativeOneStep.map, KuuNativeBlocks.map_id,
        KuuNativePath.map_id]
  | whisker h t ih =>
      simp [KuuNativeOneStep.map, KuuNativeBlocks.map_id,
        KuuNativePath.map_id, ih]

/-- The two-stage functorial image of an actual F41 primitive is
identical to transport along the composite ordinary functor. -/
theorem KuuNativeOneStep.map_comp
    (F : A ⥤ B) (G : B ⥤ C)
    {a b : A} {p q : KuuNativeBlocks a b}
    (h : KuuNativeOneStep p q) :
    h.map (F ⋙ G) = (h.map F).map G := by
  induction h with
  | split p q r =>
      simp [KuuNativeOneStep.map,
        KuuNativeBlocks.map_comp, KuuNativePath.map_comp]
  | insertNil p =>
      simp [KuuNativeOneStep.map,
        KuuNativeBlocks.map_comp, KuuNativePath.map_comp]
  | whisker h t ih =>
      simp [KuuNativeOneStep.map,
        KuuNativeBlocks.map_comp, KuuNativePath.map_comp, ih]

/-- Identity preserves every original indexed intermediate F40
Blocks stage and its exact Type-valued F41 primitive witness. -/
theorem KuuNativeAxisTrace.map_id
    {a b : A} {n : Nat}
    {p q : KuuNativeBlocks a b}
    (h : KuuNativeAxisTrace n p q) :
    h.map (𝟭 A) = h := by
  induction h with
  | refl p =>
      simp only [KuuNativeAxisTrace.map, KuuNativeBlocks.map_id]
  | snoc h step ih =>
      simp only [KuuNativeAxisTrace.map,
        KuuNativeOneStep.map_id, ih]

/-- Composed functors preserve arbitrary unbounded full F41
derivations strictly, not only their Prop shadows. -/
theorem KuuNativeAxisTrace.map_comp
    (F : A ⥤ B) (G : B ⥤ C)
    {a b : A} {n : Nat}
    {p q : KuuNativeBlocks a b}
    (h : KuuNativeAxisTrace n p q) :
    h.map (F ⋙ G) = (h.map F).map G := by
  induction h with
  | refl p =>
      simp only [KuuNativeAxisTrace.map, KuuNativeBlocks.map_comp]
  | snoc h step ih =>
      simp only [KuuNativeAxisTrace.map,
        KuuNativeOneStep.map_comp, ih]

#print axioms KuuNativeOneStep.map_id
#print axioms KuuNativeOneStep.map_comp
#print axioms KuuNativeAxisTrace.map_id
#print axioms KuuNativeAxisTrace.map_comp
end
end Kuu.F112.Physical
