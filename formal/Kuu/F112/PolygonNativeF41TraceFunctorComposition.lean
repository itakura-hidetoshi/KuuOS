import Kuu.F112.PolygonNativeF41FunctorCompositionAll

/-!
# F112-E7Q5-F4-O2-D4 — complete F41 history composition coherence

All genuine Type-valued primitive F41 steps already satisfy the
two-functor composition law as HEq, including any number of nested
right-whisker constructors (O2-D3). Use the proved dependent
snoc congruence to lift that law to the entire n-step history,
retaining the n intermediate F40 Blocks and each actual witness.

The proof is NOT a numerical-grade or Prop-certificate comparison.
No original KUOS or Gray imports and no extra axioms.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uA vA uB vB uC vC
variable {A : Type uA} [Category.{vA} A]
variable {B : Type uB} [Category.{vB} B]
variable {C : Type uC} [Category.{vC} C]

/-- Exact-depth genuine Type-valued native F41 source histories
transport coherently through arbitrary composed category functors,
with dependent reindexing explicitly retained in heterogeneous Eq. -/
theorem KuuNativeAxisTrace.map_comp_heq
    (F : A ⥤ B) (G : B ⥤ C)
    {x y : A} {n : Nat} {p q : KuuNativeBlocks x y}
    (h : KuuNativeAxisTrace n p q) :
    HEq (h.map (F ⋙ G)) ((h.map F).map G) := by
  induction h with
  | refl p =>
      simp only [KuuNativeAxisTrace.map]
      rw [KuuNativeBlocks.map_comp F G p]
      rfl
  | snoc h step ih =>
      exact KuuNativeAxisTrace.snoc_heq_of_heq
        (h.map (F ⋙ G)) ((h.map F).map G)
        (step.map (F ⋙ G)) ((step.map F).map G)
        (KuuNativeBlocks.map_comp F G _)
        (KuuNativeBlocks.map_comp F G _)
        (KuuNativeBlocks.map_comp F G _)
        ih (KuuNativeOneStep.map_comp_heq F G step)

#print axioms KuuNativeAxisTrace.map_comp_heq
end
end Kuu.F112.Physical
