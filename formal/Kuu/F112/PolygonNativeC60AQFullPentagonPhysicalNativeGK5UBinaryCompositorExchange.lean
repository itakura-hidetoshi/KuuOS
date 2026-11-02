import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5TUnitCounitCompositeCoherence
import Mathlib.CategoryTheory.Equivalence
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK5U — genuine Mathlib binary compositor exchange
between successive pointwise equivalences e,g and their true
Mathlib composite e.trans g. This new theorem is the remaining
non-strict local obstruction behind GK5T's all-finite-tree criterion.

All comparison values below are WHOLE Mathlib NatIso, with actual
unit/counit and non-strict composite witnesses. Neither the two
equivalence inverses nor any GK5G compositor is strictified.
The exact-source CI must validate before any completion claim.

Fixed Lean v4.30.0-rc2 and mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Same-root107, append-only, #1558 Draft/open/unmerged.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uI vC uC

section GenuineTwoStageCompositor
variable {I : Type uI} {C D E : I → Cat.{vC,uC}}
variable (e : ∀ i : I, C i ≌ D i)
variable (g : ∀ i : I, D i ≌ E i)

/-- Real compositional compatibility of a pointwise genuine
category equivalence's nonstrict middle unit. The whole
Mathlib NatIso square compares the two real middle-unit
cancelations, not just their endpoint functors. -/
theorem nativeGK5UBinaryCompositor_whole
    {i j k : I} (R : C i ⥤ C j) (S : C j ⥤ C k) :
    (nativeGK5GChangeCompIso g
        (nativeGK5GChangeAtom e R) (nativeGK5GChangeAtom e S) ≪≫
      nativeGK5GChangeIso g (nativeGK5GChangeCompIso e R S)) ≪≫
      nativeGK5QAtomComparison e g (R ⋙ S) =
    ((Functor.isoWhiskerRight (nativeGK5QAtomComparison e g R)
        (nativeGK5GChangeAtom g (nativeGK5GChangeAtom e S))) ≪≫
      (Functor.isoWhiskerLeft
        (nativeGK5GChangeAtom (fun h : I => (e h).trans (g h)) R)
        (nativeGK5QAtomComparison e g S))) ≪≫
      nativeGK5GChangeCompIso
        (fun h : I => (e h).trans (g h)) R S := by
  apply Iso.ext
  ext X
  simp [nativeGK5GChangeCompIso, nativeGK5GChangeIso,
    nativeGK5QAtomComparison, nativeGK5QChangeAtom_comp,
    nativeGK5GChangeAtom, Equivalence.trans,
    Functor.comp_map, Functor.map_comp, Category.assoc]

#print axioms nativeGK5UBinaryCompositor_whole

end GenuineTwoStageCompositor
end
end Kuu.F112.Physical
