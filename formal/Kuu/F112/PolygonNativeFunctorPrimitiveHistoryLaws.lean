import Kuu.F112.PolygonNativeFunctorPathBlocksLaws

/-!
# F112-E7Q5-F4-O2 — primitive dependent-index boundary and certified cases

The F41 elementary proof source is Type-valued and indexed by
original categorical Blocks.  A naive homogeneous identity law
between `h.map (𝟭 A)` and `h` is ILL-TYPED because the endpoints
are `p.map (𝟭 A)` / `q.map (𝟭 A)` versus `p` / `q`.
The O1 strict Blocks laws prove both endpoint equalities.

This file certifies the genuinely proof-relevant identity law
as HEq for the TWO root constructors `split` and `insertNil`,
without discarding the original primitive proof. It deliberately
does NOT assert the remaining arbitrarily nested `whisker`
comparison or the general two-functor composition of primitive
witnesses; both require cast-aware dependent proof normalization.

No frozen KUOS/Gray/F51/F77 imports, no axioms or sorry.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uA vA uB vB uC vC
variable {A : Type uA} [Category.{vA} A]
variable {B : Type uB} [Category.{vB} B]
variable {C : Type uC} [Category.{vC} C]

/-- Identity changes neither fully typed F40 endpoint of ANY
original-shaped primitive Type-valued witness. -/
theorem KuuNativeOneStep.map_id_endpoints
    {a b : A} {p q : KuuNativeBlocks a b}
    (_h : KuuNativeOneStep p q) :
    p.map (𝟭 A) = p ∧ q.map (𝟭 A) = q :=
  ⟨KuuNativeBlocks.map_id p, KuuNativeBlocks.map_id q⟩

/-- For composite ordinary functors the two ORIGINAL F40 endpoints
of any primitive witness reindex consistently and independently. -/
theorem KuuNativeOneStep.map_comp_endpoints
    (F : A ⥤ B) (G : B ⥤ C)
    {a b : A} {p q : KuuNativeBlocks a b}
    (_h : KuuNativeOneStep p q) :
    p.map (F ⋙ G) = (p.map F).map G ∧
      q.map (F ⋙ G) = (q.map F).map G :=
  ⟨KuuNativeBlocks.map_comp F G p, KuuNativeBlocks.map_comp F G q⟩

/-- The genuine split CONSTRUCTOR itself obeys identity as HEq,
including all three primitive Type-valued source objects. -/
theorem KuuNativeOneStep.map_id_split_heq
    {w x y z : A} (p : KuuNativeBlocks w x)
    (q : KuuNativePath x y) (r : KuuNativePath y z) :
    HEq ((KuuNativeOneStep.split p q r).map (𝟭 A))
      (KuuNativeOneStep.split p q r) := by
  simp [KuuNativeOneStep.map]
  rw [KuuNativeBlocks.map_id p, KuuNativePath.map_id q,
    KuuNativePath.map_id r]

/-- The actual empty-block insertion proof remains unchanged by
the identity functor, with its exact Type-valued evidence preserved. -/
theorem KuuNativeOneStep.map_id_insertNil_heq
    {x y : A} (p : KuuNativeBlocks x y) :
    HEq ((KuuNativeOneStep.insertNil p).map (𝟭 A))
      (KuuNativeOneStep.insertNil p) := by
  simp [KuuNativeOneStep.map]
  rw [KuuNativeBlocks.map_id p]

#print axioms KuuNativeOneStep.map_id_endpoints
#print axioms KuuNativeOneStep.map_comp_endpoints
#print axioms KuuNativeOneStep.map_id_split_heq
#print axioms KuuNativeOneStep.map_id_insertNil_heq
end
end Kuu.F112.Physical
