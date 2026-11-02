import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5MArbitraryTreeAssociator
import Mathlib.CategoryTheory.Equivalence
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK5N — genuine pointwise-equivalence unitors for
arbitrary finite heterogeneous functor trees.

GK5M establishes the whole NatIso associator generator square.
We now discharge the separate LEFT and RIGHT unitors without
strictifying any equivalence, using genuine Mathlib
unit/counit triangle laws and the recursive actual comparison Phi_t.
Both original and changed unit trees remain genuine identities.

Only verified local steps may later be used to discharge GK5H's
full-step predicate. Whiskering cases and unconditional all-path
naturality are not asserted here before their own Lean proofs.

Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only, same-root107, protected #1558 Draft/open/unmerged.
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

section GenuineUnitorCoherence
variable {I : Type uI} {C D : I → Cat.{vC,uC}}
variable (e : ∀ i : I, C i ≌ D i)

/-- True left-unit pseudofunctor law for ANY whole Mathlib functor R.
The counit inverse at the source and unit inverse at the source
cancel by the actual equivalence triangle. -/
theorem nativeGK5NLeft_unitLaw
    {i j : I} (R : C i ⥤ C j) :
    (Functor.isoWhiskerRight (nativeGK5GChangeUnitIso e i)
          (nativeGK5GChangeAtom e R) ≪≫
      nativeGK5GChangeCompIso e (𝟭 (C i)) R) ≪≫
        nativeGK5GChangeIso e (Functor.leftUnitor R) =
      Functor.leftUnitor (nativeGK5GChangeAtom e R) := by
  apply Iso.ext
  ext X
  have hTriangle := (e i).inverse_counitInv_comp X
  have hMap := congrArg (fun t => (e j).functor.map (R.map t)) hTriangle
  simp [nativeGK5GChangeUnitIso, nativeGK5GChangeIso,
    nativeGK5GChangeAtom, nativeGK5IChangeCompIso_hom_app,
    Functor.leftUnitor_hom_app,
    Functor.comp_map, Functor.map_comp, Category.assoc]
  have hMapId :
      (e j).functor.map (R.map (𝟙 ((e i).inverse.obj X))) =
        𝟙 ((e j).functor.obj (R.obj ((e i).inverse.obj X))) := by
    simp
  simpa only [Equivalence.counitInv, Equivalence.unitInv,
    Functor.map_comp] using hMap.trans hMapId

/-- True right-unit pseudofunctor law for ANY whole Mathlib functor R.
Here the second triangle cancels a counit inverse with a mapped
inverse unit at the target category. -/
theorem nativeGK5NRight_unitLaw
    {i j : I} (R : C i ⥤ C j) :
    (Functor.isoWhiskerLeft (nativeGK5GChangeAtom e R)
          (nativeGK5GChangeUnitIso e j) ≪≫
      nativeGK5GChangeCompIso e R (𝟭 (C j))) ≪≫
        nativeGK5GChangeIso e (Functor.rightUnitor R) =
      Functor.rightUnitor (nativeGK5GChangeAtom e R) := by
  apply Iso.ext
  ext X
  simp [nativeGK5GChangeUnitIso, nativeGK5GChangeIso,
    nativeGK5GChangeAtom, nativeGK5IChangeCompIso_hom_app,
    Equivalence.counitInv_functor_comp, Functor.rightUnitor_hom_app,
    Functor.comp_map, Functor.map_comp, Category.assoc]

/-- The LEFT unitor comparison with any genuinely nontrivial
whole NatIso phi : S ≅ Change(R), not only a reflexive atomic leaf. -/
private theorem nativeGK5NLeft_unitor_withPhi
    {i j : I} (R : C i ⥤ C j) {S : D i ⥤ D j}
    (φ : S ≅ nativeGK5GChangeAtom e R) :
    Functor.leftUnitor S ≪≫ φ =
      ((Functor.isoWhiskerRight (nativeGK5GChangeUnitIso e i) S ≪≫
        Functor.isoWhiskerLeft
          (nativeGK5GChangeAtom e (𝟭 (C i))) φ) ≪≫
        nativeGK5GChangeCompIso e (𝟭 (C i)) R) ≪≫
          nativeGK5GChangeIso e (Functor.leftUnitor R) := by
  have hnat : Functor.leftUnitor S ≪≫ φ =
      Functor.isoWhiskerLeft (𝟭 (D i)) φ ≪≫
        Functor.leftUnitor (nativeGK5GChangeAtom e R) := by
    apply Iso.ext
    ext X
    simp
  rw [hnat, ← nativeGK5NLeft_unitLaw e R]
  have hinter := Functor.isoWhiskerLeft_trans_isoWhiskerRight
    (nativeGK5GChangeUnitIso e i) φ
  simpa only [Iso.trans_assoc] using
    congrArg (fun t =>
      t ≪≫ nativeGK5GChangeCompIso e (𝟭 (C i)) R ≪≫
        nativeGK5GChangeIso e (Functor.leftUnitor R)) hinter

/-- RIGHT unitor comparison with arbitrary genuine Phi, using the
naturality of the actual right unitor and the genuine right triangle. -/
private theorem nativeGK5NRight_unitor_withPhi
    {i j : I} (R : C i ⥤ C j) {S : D i ⥤ D j}
    (φ : S ≅ nativeGK5GChangeAtom e R) :
    Functor.rightUnitor S ≪≫ φ =
      ((Functor.isoWhiskerRight φ (𝟭 (D j)) ≪≫
        Functor.isoWhiskerLeft
          (nativeGK5GChangeAtom e R)
          (nativeGK5GChangeUnitIso e j)) ≪≫
        nativeGK5GChangeCompIso e R (𝟭 (C j))) ≪≫
          nativeGK5GChangeIso e (Functor.rightUnitor R) := by
  have hnat : Functor.rightUnitor S ≪≫ φ =
      Functor.isoWhiskerRight φ (𝟭 (D j)) ≪≫
        Functor.rightUnitor (nativeGK5GChangeAtom e R) := by
    apply Iso.ext
    ext X
    simp
  rw [hnat, ← nativeGK5NRight_unitLaw e R]
  simp only [Iso.trans_assoc]

/-- Genuine GK5D left unitor square for every arbitrarily deep
dependently typed finite subtree, with its actual recursive Phi. -/
theorem nativeGK5NLeftUnit_subtree
    {i j : I} (a : NativeGK5DTypedTree C i j) :
    NativeGK5JPathSquare e
      (NativeGK5DTypedPath.basic (NativeGK5DTypedStep.leftUnit a)) := by
  simpa only [NativeGK5JPathSquare,
    nativeGK5DPathIso, nativeGK5GChangePath,
    nativeGK5GChangeStep, nativeGK5DStepIso,
    nativeGK5GChangeTreeIso, nativeGK5GChangeTree,
    nativeGK5DTreeComposite, Iso.refl_trans, Iso.trans_refl,
    Iso.trans_assoc] using
    (nativeGK5NLeft_unitor_withPhi e
      (nativeGK5DTreeComposite a)
      (nativeGK5GChangeTreeIso e a))

/-- Genuine GK5D right unitor square for every arbitrarily deep
dependently typed finite subtree, with its actual recursive Phi. -/
theorem nativeGK5NRightUnit_subtree
    {i j : I} (a : NativeGK5DTypedTree C i j) :
    NativeGK5JPathSquare e
      (NativeGK5DTypedPath.basic (NativeGK5DTypedStep.rightUnit a)) := by
  simpa only [NativeGK5JPathSquare,
    nativeGK5DPathIso, nativeGK5GChangePath,
    nativeGK5GChangeStep, nativeGK5DStepIso,
    nativeGK5GChangeTreeIso, nativeGK5GChangeTree,
    nativeGK5DTreeComposite, Iso.refl_trans, Iso.trans_refl,
    Iso.trans_assoc] using
    (nativeGK5NRight_unitor_withPhi e
      (nativeGK5DTreeComposite a)
      (nativeGK5GChangeTreeIso e a))

#print axioms nativeGK5NLeft_unitLaw
#print axioms nativeGK5NRight_unitLaw
#print axioms nativeGK5NLeftUnit_subtree
#print axioms nativeGK5NRightUnit_subtree

end GenuineUnitorCoherence
end
end Kuu.F112.Physical
