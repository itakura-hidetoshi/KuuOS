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

/-- Identity of a category is structurally neutral, but the
Type of primitive proofs is indexed by the actual mapped Blocks.
Use HEq to compare proof-relevant witnesses BEFORE the endpoint
casts are normalized; ordinary Eq would be ill-typed here. -/
theorem KuuNativeOneStep.map_id_heq
    {a b : A} {p q : KuuNativeBlocks a b}
    (h : KuuNativeOneStep p q) :
    HEq (h.map (𝟭 A)) h := by
  induction h with
  | split p q r =>
      simp only [KuuNativeOneStep.map]
      rw [KuuNativeBlocks.map_id p, KuuNativePath.map_id q,
        KuuNativePath.map_id r]
  | insertNil p =>
      simp only [KuuNativeOneStep.map]
      rw [KuuNativeBlocks.map_id p]
  | whisker h t ih =>
      simp only [KuuNativeOneStep.map]
      cases ih
      rw [KuuNativePath.map_id t]

/-- The same typed primitive proof comparison for composite functors.
HEq records the intermediate endpoint reindexing explicitly. -/
theorem KuuNativeOneStep.map_comp_heq
    (F : A ⥤ B) (G : B ⥤ C)
    {a b : A} {p q : KuuNativeBlocks a b}
    (h : KuuNativeOneStep p q) :
    HEq (h.map (F ⋙ G)) ((h.map F).map G) := by
  induction h with
  | split p q r =>
      simp only [KuuNativeOneStep.map]
      rw [KuuNativeBlocks.map_comp F G p, KuuNativePath.map_comp F G q,
        KuuNativePath.map_comp F G r]
  | insertNil p =>
      simp only [KuuNativeOneStep.map]
      rw [KuuNativeBlocks.map_comp F G p]
  | whisker h t ih =>
      simp only [KuuNativeOneStep.map]
      cases ih
      rw [KuuNativePath.map_comp F G t]

#print axioms KuuNativeOneStep.map_id_heq
#print axioms KuuNativeOneStep.map_comp_heq
end
end Kuu.F112.Physical
