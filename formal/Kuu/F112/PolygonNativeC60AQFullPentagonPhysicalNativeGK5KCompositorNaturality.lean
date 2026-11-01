import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5JEndpointObstructionCanonicalization
import Mathlib.CategoryTheory.Equivalence
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK5K — genuine binary pointwise-equivalence compositor naturality.

Following the exact endpoint obstruction GK5J, start the actual generator
discharge by proving that the NONSTRICT middle-equivalence cancellation
comparison commutes with genuine natural transformations on a composable
right-hand functor. This is a nontrivial local 2-cell interchange
condition needed before general arbitrary-subtree associators.

We use GK5I's explicitly certified component of the genuine GK5G
composition comparison, and Mathlib's actual NatTrans.naturality at
the inverse unit of the intermediate pointwise category equivalence.
We do not replace unit/counit by strict inverses.

This first step does not prove the general arbitrary-subtree associator,
either unitor, both contextual whiskerings, or GK5H unconditional path
compatibility. All are still open until independently checked.

Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only, same-root107, #1558 Draft/open/unmerged.
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

section CompositorNaturality
variable {I : Type uI} {C D : I → Cat.{vC,uC}}
variable (e : ∀ i : I, C i ≌ D i)

/-- Genuine whole NatTrans naturality of the GK5G pointwise-equivalence
binary compositor in its RIGHT functor argument. The intermediate
unitIso.inv is nontrivial; its compatibility follows from the actual
naturality of β. -/
theorem nativeGK5KChangeCompNat_right
    {i j k : I} (R : C i ⥤ C j)
    {S T : C j ⥤ C k} (β : S ⟶ T) :
    Functor.whiskerLeft (nativeGK5GChangeAtom e R)
        (nativeGK5GChangeNat e β) ≫
      (nativeGK5GChangeCompIso e R T).hom =
    (nativeGK5GChangeCompIso e R S).hom ≫
      nativeGK5GChangeNat e (Functor.whiskerLeft R β) := by
  ext X
  have hβ := β.naturality
    ((e j).unitIso.inv.app (R.obj ((e i).inverse.obj X)))
  simp only [NatTrans.comp_app, Functor.whiskerLeft_app,
    nativeGK5IChangeCompIso_hom_app]
  dsimp [nativeGK5GChangeNat, nativeGK5GChangeAtom]
  simpa only [Functor.map_comp] using
    congrArg (fun f => (e k).functor.map f) hβ.symm

/-- The preceding componentwise naturality is genuinely an equality
of WHOLE Mathlib natural isomorphisms after iso-whiskering, not merely
a selected pointwise map. -/
theorem nativeGK5KChangeCompIso_right
    {i j k : I} (R : C i ⥤ C j)
    {S T : C j ⥤ C k} (β : S ≅ T) :
    Functor.isoWhiskerLeft (nativeGK5GChangeAtom e R)
        (nativeGK5GChangeIso e β) ≪≫
      nativeGK5GChangeCompIso e R T =
    nativeGK5GChangeCompIso e R S ≪≫
      nativeGK5GChangeIso e (Functor.isoWhiskerLeft R β) := by
  apply Iso.ext
  simpa only [Iso.trans_hom, Functor.isoWhiskerLeft_hom,
    nativeGK5IChangeIso_hom] using
    (nativeGK5KChangeCompNat_right e R β.hom)

#print axioms nativeGK5KChangeCompNat_right
#print axioms nativeGK5KChangeCompIso_right

end CompositorNaturality
end
end Kuu.F112.Physical
