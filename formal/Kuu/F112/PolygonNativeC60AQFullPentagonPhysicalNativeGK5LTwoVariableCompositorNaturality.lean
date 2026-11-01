import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5KCompositorNaturality
import Mathlib.CategoryTheory.Equivalence
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK5L — genuine pointwise-equivalence binary compositor
left naturality and two-variable whole NatIso interchange.

GK5K proves the genuine right argument compositor naturality.
This additive continuation proves left argument naturality using the
actual inverse equivalence unit naturality, then composes the two
genuine whole NatIso squares into a two-variable interchange square.
Neither the inverse equivalence nor the combinatorial tree
presentation is strictified.

This is a local ingredient towards the arbitrary-subtree associator
obstruction of GK5H/GK5J, not a claim that unitor, whiskering or
every general finite typed path obstruction automatically vanishes.

Lean v4.30.0-rc2, mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only / root107 / protected #1558 Draft-open untouched.
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

section TwoVariableCompositor
variable {I : Type uI} {C D : I → Cat.{vC,uC}}
variable (e : ∀ i : I, C i ≌ D i)

/-- The actual GK5G binary compositor is natural in its LEFT
functor variable, for arbitrary true Mathlib natural transformations.
Unlike the right-variable case GK5K, this explicitly requires
naturality of the inverse unitIso of the intermediate equivalence. -/
theorem nativeGK5LChangeCompNat_left
    {i j k : I} {R T : C i ⥤ C j}
    (α : R ⟶ T) (S : C j ⥤ C k) :
    Functor.whiskerRight (nativeGK5GChangeNat e α)
        (nativeGK5GChangeAtom e S) ≫
      (nativeGK5GChangeCompIso e T S).hom =
    (nativeGK5GChangeCompIso e R S).hom ≫
      nativeGK5GChangeNat e (Functor.whiskerRight α S) := by
  ext X
  have hα := (e j).unitIso.inv.naturality
    (α.app ((e i).inverse.obj X))
  simp only [NatTrans.comp_app, Functor.whiskerRight_app,
    nativeGK5IChangeCompIso_hom_app]
  dsimp [nativeGK5GChangeNat, nativeGK5GChangeAtom]
  simpa only [Functor.comp_map, Functor.map_comp, Functor.id_map] using
    congrArg (fun f => (e k).functor.map (S.map f)) hα

/-- A whole Mathlib NatIso left-variable compositor square, not only
the corresponding component at a chosen object. -/
theorem nativeGK5LChangeCompIso_left
    {i j k : I} {R T : C i ⥤ C j}
    (α : R ≅ T) (S : C j ⥤ C k) :
    Functor.isoWhiskerRight (nativeGK5GChangeIso e α)
        (nativeGK5GChangeAtom e S) ≪≫
      nativeGK5GChangeCompIso e T S =
    nativeGK5GChangeCompIso e R S ≪≫
      nativeGK5GChangeIso e (Functor.isoWhiskerRight α S) := by
  apply Iso.ext
  simpa only [Iso.trans_hom, Functor.isoWhiskerRight_hom,
    nativeGK5IChangeIso_hom] using
    (nativeGK5LChangeCompNat_left e α.hom S)

/-- BOTH variable changes of a genuine nonstrict compositor now
commute as a WHOLE Mathlib NatIso, by pasting the actual GK5K right
and GK5L left squares. The source side uses the real horizontal
interchange of two genuine whiskered NatIso values. -/
theorem nativeGK5LChangeCompIso_both
    {i j k : I} {R T : C i ⥤ C j} {S U : C j ⥤ C k}
    (α : R ≅ T) (β : S ≅ U) :
    (Functor.isoWhiskerRight (nativeGK5GChangeIso e α)
        (nativeGK5GChangeAtom e S) ≪≫
      Functor.isoWhiskerLeft (nativeGK5GChangeAtom e T)
        (nativeGK5GChangeIso e β)) ≪≫
      nativeGK5GChangeCompIso e T U =
    nativeGK5GChangeCompIso e R S ≪≫
      nativeGK5GChangeIso e
        (Functor.isoWhiskerRight α S ≪≫
          Functor.isoWhiskerLeft T β) := by
  calc
    _ = (Functor.isoWhiskerRight (nativeGK5GChangeIso e α)
            (nativeGK5GChangeAtom e S) ≪≫
          nativeGK5GChangeCompIso e T S) ≪≫
        nativeGK5GChangeIso e (Functor.isoWhiskerLeft T β) := by
          simpa only [Iso.trans_assoc] using
            congrArg
              (fun γ => Functor.isoWhiskerRight (nativeGK5GChangeIso e α)
                (nativeGK5GChangeAtom e S) ≪≫ γ)
              (nativeGK5KChangeCompIso_right e T β)
    _ = (nativeGK5GChangeCompIso e R S ≪≫
          nativeGK5GChangeIso e (Functor.isoWhiskerRight α S)) ≪≫
        nativeGK5GChangeIso e (Functor.isoWhiskerLeft T β) := by
          rw [nativeGK5LChangeCompIso_left e α S]
    _ = nativeGK5GChangeCompIso e R S ≪≫
          nativeGK5GChangeIso e
            (Functor.isoWhiskerRight α S ≪≫
              Functor.isoWhiskerLeft T β) := by
          simp only [Iso.trans_assoc, ← nativeGK5HChangeIso_trans]

#print axioms nativeGK5LChangeCompNat_left
#print axioms nativeGK5LChangeCompIso_left
#print axioms nativeGK5LChangeCompIso_both

end TwoVariableCompositor
end
end Kuu.F112.Physical
