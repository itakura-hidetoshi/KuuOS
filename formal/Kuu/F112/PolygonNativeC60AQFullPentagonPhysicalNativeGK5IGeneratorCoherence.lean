import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5HLocalToGlobalPathCoherence
import Mathlib.CategoryTheory.Equivalence
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK5I — genuinely typed generator-coherence investigation.

We retain the GK5G comparison Phi and GK5H exact local-to-global
obstruction criterion. This additive file begins explicit discharge
of its basic associator/unit generators from REAL Mathlib equivalence
unit/counit and category coherence. No new axioms, no sorry,
no raw Type-valued source high-cells, no Gray or hyperdescent.

Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only, same-root107, protected PR #1558 stays Draft/open.
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

section BasicGeneratorCoherence
variable {I : Type uI} {C D : I → Cat.{vC,uC}}
variable (e : ∀ i : I, C i ≌ D i)

/-- Actual pinned Mathlib equivalence triangle at every source object.
This is a real identity between morphisms, not a fabricated filler. -/
theorem nativeGK5IForwardTriangle (i : I) (X : C i) :
    (e i).functor.map ((e i).unitIso.hom.app X) ≫
      (e i).counitIso.hom.app ((e i).functor.obj X) =
        𝟙 ((e i).functor.obj X) :=
  (e i).functor_unitIso_comp X

/-- Dual actual Mathlib equivalence triangle for the chosen inverse,
needed for typed right-unit changes in the new category family. -/
theorem nativeGK5IInverseTriangle (i : I) (Y : D i) :
    (e i).unitIso.hom.app ((e i).inverse.obj Y) ≫
      (e i).inverse.map ((e i).counitIso.hom.app Y) =
        𝟙 ((e i).inverse.obj Y) :=
  (e i).unit_inverse_comp Y

/-- Conjugation of an actual Mathlib NatIso has exactly the
corresponding whole NatTrans obtained by true double whiskering. -/
theorem nativeGK5IChangeIso_hom
    {i j : I} {R S : C i ⥤ C j} (α : R ≅ S) :
    (nativeGK5GChangeIso e α).hom =
      nativeGK5GChangeNat e α.hom := rfl

/-- Exact genuine pointwise component of the GK5G middle
equivalence cancellation. Both structural endpoint eqToIso factors
are retained but simplify to the real unitIso inverse component. -/
theorem nativeGK5IChangeCompIso_hom_app
    {i j k : I} (R : C i ⥤ C j) (S : C j ⥤ C k) (X : D i) :
    (nativeGK5GChangeCompIso e R S).hom.app X =
      (e k).functor.map
        (S.map ((e j).unitIso.inv.app (R.obj ((e i).inverse.obj X)))) := by
  dsimp [nativeGK5GChangeCompIso, nativeGK5GChangeAtom]
  simp

/-- The first finite heterogeneous three-ATOM associator case.
Real equivalence units at the two intermediate categories are
compared by the naturality of the inverse unitIso, not a postulated
strict equality of pointwise equivalences. -/
theorem nativeGK5IAssociator_atoms
    {i j k l : I}
    (F : C i ⥤ C j) (G : C j ⥤ C k) (H : C k ⥤ C l) :
    nativeGK5DStepIso
        (nativeGK5GChangeStep e
          (NativeGK5DTypedStep.assoc
            (NativeGK5DTypedTree.atom F)
            (NativeGK5DTypedTree.atom G)
            (NativeGK5DTypedTree.atom H))) ≪≫
      nativeGK5GChangeTreeIso e
        (NativeGK5DTypedTree.paste (.atom F) (.paste (.atom G) (.atom H))) =
    nativeGK5GChangeTreeIso e
        (NativeGK5DTypedTree.paste (.paste (.atom F) (.atom G)) (.atom H)) ≪≫
      nativeGK5GChangeIso e
        (nativeGK5DStepIso (NativeGK5DTypedStep.assoc
          (NativeGK5DTypedTree.atom F)
          (NativeGK5DTypedTree.atom G)
          (NativeGK5DTypedTree.atom H))) := by
  apply Iso.ext
  ext X
  let u := G.map ((e j).unitIso.inv.app (F.obj ((e i).inverse.obj X)))
  have hK := (e k).unitIso.inv.naturality u
  simp [nativeGK5DStepIso, nativeGK5GChangeStep,
    nativeGK5GChangeTreeIso, nativeGK5GChangeTree,
    nativeGK5DTreeComposite, nativeGK5GChangeAtom, nativeGK5GChangeIso,
    nativeGK5IChangeCompIso_hom_app,
    Functor.comp_obj, Functor.comp_map,
    Functor.associator_hom_app,
    Functor.map_comp, Category.assoc, hK, u]
  have hCancel :
      (e k).unitIso.hom.app (G.obj (F.obj ((e i).inverse.obj X))) ≫
        (e k).unitIso.inv.app (G.obj (F.obj ((e i).inverse.obj X))) =
          𝟙 (G.obj (F.obj ((e i).inverse.obj X))) :=
    (e k).unitIso.hom_inv_id_app _
  simpa only [Equivalence.unit, Equivalence.unitInv,
    Category.assoc, ← Functor.map_comp, hCancel,
    Functor.map_id, Category.comp_id]

#print axioms nativeGK5IForwardTriangle
#print axioms nativeGK5IInverseTriangle
#print axioms nativeGK5IChangeIso_hom
#print axioms nativeGK5IChangeCompIso_hom_app
#print axioms nativeGK5IAssociator_atoms

end BasicGeneratorCoherence
end
end Kuu.F112.Physical
