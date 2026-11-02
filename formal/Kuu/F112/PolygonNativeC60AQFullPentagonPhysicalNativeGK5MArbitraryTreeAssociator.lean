import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5LTwoVariableCompositorNaturality
import Mathlib.CategoryTheory.Whiskering
import Mathlib.CategoryTheory.Equivalence
import Mathlib.Tactic

/-!
F112-P94D3GK5M — associator naturality for genuinely arbitrary
heterogeneous finite typed subtrees under pointwise category equivalences.

Following GK5I's three-atomic associator, GK5K and GK5L certified
non-strict compositor naturality in BOTH arguments, and GK5J's
endpoint obstruction criterion, test whether the whole comparison
Phi_t is pseudonatural for an actual associator step with
arbitrary recursively evaluated finite subtrees a,b,c.

All new evidence is genuine Mathlib whole NatIso; no axiom, sorry,
source raw high cell, Gray strictification, or unguarded descent.
Lean v4.30.0-rc2 and mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only, public root107, #1558 stays Draft/open.
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

section ArbitrarySubtreeAssociator
variable {I : Type uI} {C D : I → Cat.{vC,uC}}
variable (e : ∀ i : I, C i ≌ D i)

/-- A genuine arbitrary-three-functor compositor associativity,
extracted from GK5I's fully certified three-atom associator whole
Mathlib NatIso. The functors themselves have NO atom restriction:
they may be the whole evaluations of arbitrary finite typed trees. -/
theorem nativeGK5MCompositor_associator
    {i j k l : I} (R : C i ⥤ C j) (S : C j ⥤ C k)
    (T : C k ⥤ C l) :
    Functor.associator
        (nativeGK5GChangeAtom e R)
        (nativeGK5GChangeAtom e S)
        (nativeGK5GChangeAtom e T) ≪≫
      Functor.isoWhiskerLeft (nativeGK5GChangeAtom e R)
        (nativeGK5GChangeCompIso e S T) ≪≫
      nativeGK5GChangeCompIso e R (S ⋙ T) =
    Functor.isoWhiskerRight (nativeGK5GChangeCompIso e R S)
        (nativeGK5GChangeAtom e T) ≪≫
      nativeGK5GChangeCompIso e (R ⋙ S) T ≪≫
      nativeGK5GChangeIso e (Functor.associator R S T) := by
  simpa only [nativeGK5DStepIso, nativeGK5GChangeStep,
    nativeGK5GChangeTreeIso, nativeGK5GChangeTree,
    nativeGK5DTreeComposite,
    Functor.isoWhiskerRight_refl, Functor.isoWhiskerLeft_refl,
    Iso.refl_trans, Iso.trans_refl, Iso.trans_assoc] using
    (nativeGK5IAssociator_atoms e R S T)

/-- GK5M target: arbitrary genuinely dependent-typed subtree
associator, with their nontrivial recursive Phi_a,Phi_b,Phi_c.
Unlike GK5I this is NOT restricted to three atomic leaves. -/
theorem nativeGK5MAssociator_subtrees
    {i j k l : I}
    (a : NativeGK5DTypedTree C i j)
    (b : NativeGK5DTypedTree C j k)
    (c : NativeGK5DTypedTree C k l) :
    NativeGK5JPathSquare e
      (NativeGK5DTypedPath.basic
        (NativeGK5DTypedStep.assoc a b c)) := by
  apply Iso.ext
  ext X
  let g := (nativeGK5DTreeComposite b).map
    ((e j).unitIso.inv.app ((nativeGK5DTreeComposite a).obj ((e i).inverse.obj X)))
  have hPhiC := (nativeGK5GChangeTreeIso e c).hom.naturality
    ((e k).functor.map g)
  have hUnitK := (e k).unitIso.inv.naturality g
  simp [NativeGK5JPathSquare, nativeGK5DPathIso,
    nativeGK5DStepIso, nativeGK5GChangePath,
    nativeGK5GChangeStep, nativeGK5GChangeTreeIso,
    nativeGK5GChangeTree, nativeGK5DTreeComposite,
    nativeGK5GChangeAtom, nativeGK5GChangeIso,
    nativeGK5IChangeCompIso_hom_app,
    Functor.associator_hom_app, Functor.comp_obj,
    Functor.comp_map, Functor.map_comp,
    Category.assoc, hPhiC, hUnitK, g]
  cat_disch

#print axioms nativeGK5MCompositor_associator
#print axioms nativeGK5MAssociator_subtrees

end ArbitrarySubtreeAssociator
end
end Kuu.F112.Physical
