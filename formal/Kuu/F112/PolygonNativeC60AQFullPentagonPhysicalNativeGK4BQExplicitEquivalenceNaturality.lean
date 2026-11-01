import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4BPExplicitInverseTargetNaturality
import Mathlib.CategoryTheory.Equivalence
import Mathlib.Tactic

/-!
F112-P94D3GK4BQ — strict object/Hom coherence of the GK4BP explicit
inverse, explicit natural unit/counit isomorphisms and comparison
with the choice-based GK4BM quasi-inverse.

The sources are the original F45-dependent structural category S
and the *actually attained* old-AH matrix category A; the target
compatible functor category is the genuine GK4BM FullSubcategory,
not the whole S ⥤ T category. The forward precomposition C_T and
GK4BP explicit inverse P_T are unchanged.
The chosen quasi-inverse from GK4BM asEquivalence is distinguished
from explicit P_T: any comparison is via a genuine NatIso, not
definitional equality. The laws do not imply original Q-category
axioms, S faithful, raw F54/F55 Type-valued cells, full integer
matrices, global Gray coherence or higher hyperdescent.

Append-only, tighten-only, overwrite-forbidden, same-root107.
Lean v4.30.0-rc2 / pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected PR #1558 Draft/OPEN/unmerged.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE uT vT

section ExplicitEquivalenceUnitCounit
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {T : Type uT} [Category.{vT} T]

/-- The explicit factor inverse followed by the original
structural observer acts as the actual identity compatible functor
on objects AND ALL genuine natural transformations. -/
theorem nativeGK4BQExplicitInverse_comp_precomposition
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    nativeGK4BPExplicitInverseFunctor (T := T) p ma mb pa pb ⋙
      nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb =
    𝟭 (NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb) := by
  apply CategoryTheory.Functor.toPrefunctor_injective
  refine Prefunctor.ext
    (fun H => nativeGK4BPExplicitInverse_compat_obj p ma mb pa pb H) ?_
  intro H K η
  apply ObjectProperty.hom_ext
  ext X
  rfl

/-- The actual attained AH forward observation followed by the
explicitly chosen factor inverse acts as the genuine identity
on its entire functor category (including NatTrans Homs). -/
theorem nativeGK4BQPrecomposition_comp_explicitInverse
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb ⋙
      nativeGK4BPExplicitInverseFunctor (T := T) p ma mb pa pb =
    𝟭 (NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T) := by
  apply CategoryTheory.Functor.toPrefunctor_injective
  refine Prefunctor.ext
    (fun G => nativeGK4BPExplicitInverse_attained_obj p ma mb pa pb G) ?_
  intro G H η
  ext X
  rfl

end ExplicitEquivalenceUnitCounit

#print axioms nativeGK4BQExplicitInverse_comp_precomposition
#print axioms nativeGK4BQPrecomposition_comp_explicitInverse

end
end Kuu.F112.Physical
