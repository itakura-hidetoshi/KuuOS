import KUOS.DependentOriginationStrongTransPostcompositionVcompComparisonV5_71

namespace KUOS.DependentOriginationUnitPostcompositionNativeSourceV5_72

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationStrongTransModificationPostcompositionV5_62

set_option autoImplicit false

noncomputable section

/-!
# Unit postcomposition with native source v5.72

This head is revalidated against the repaired v5.71 postcomposition-vcomp
base; the earlier cascade receipt from the failing parent is not reused.
Current stacked-base revalidation uses v5.71 head
`31dda2a31a7f72752517a1359a7f15d9279dcdab`.

For a pseudofunctor R : B -> B and a unit

  eta : Id_B => R,

the generic v5.62 postcomposition construction gives

  postcompose R eta : (Id_B ; R) => (R ; R).

The source pseudofunctor has the same object and morphism maps as R, but its
mapId/mapComp fields are presented through Pseudofunctor.comp.  For the
forward swallowtail we need the source literally to be R, without silently
identifying the two pseudofunctor structures.

This file proves that the source comparison cells reduce to R's own mapId and
mapComp, and then reuses the complete v5.62 mapped-square naturality proofs to
construct

  R => R ; R

with components R.map (eta.app X).

No strictness of R is assumed.
-/

namespace Generic

universe uB vB wB

variable {B : Type uB} [Bicategory.{wB, vB} B]

namespace UnitPostcomposition

variable (R : Pseudofunctor B B)
variable (eta : Pseudofunctor.StrongTrans (Pseudofunctor.id B) R)

/-- The source identity comparison of Id ; R is exactly the original R mapId
after removing the identity pseudofunctor's trivial 2-cell. -/
theorem sourceMapId_hom (a : B) :
    ((Pseudofunctor.comp (Pseudofunctor.id B) R).mapId a).hom =
      (R.mapId a).hom := by
  change R.map₂ (𝟙 (𝟙 a)) ≫ (R.mapId a).hom = _
  rw [PrelaxFunctor.map₂_id, Category.id_comp]

/-- Likewise the source compositor of Id ; R is exactly R.mapComp. -/
theorem sourceMapComp_hom
    {a b c : B} (f : a ⟶ b) (g : b ⟶ c) :
    ((Pseudofunctor.comp (Pseudofunctor.id B) R).mapComp f g).hom =
      (R.mapComp f g).hom := by
  change R.map₂ (𝟙 (f ≫ g)) ≫ (R.mapComp f g).hom = _
  rw [PrelaxFunctor.map₂_id, Category.id_comp]

/-- Reuse the v5.62 mapped naturality square, with source presented natively
as R rather than Id ; R. -/
def naturalityIso {a b : B} (f : a ⟶ b) :
    R.map f ≫ R.map (eta.app b) ≅
      R.map (eta.app a) ≫ R.map (R.map f) :=
  StrongTransPostcomposition.naturalityIso R eta f

@[simp] theorem naturalityIso_hom {a b : B} (f : a ⟶ b) :
    (naturalityIso R eta f).hom =
      (R.mapComp f (eta.app b)).inv ≫
        R.map₂ (eta.naturality f).hom ≫
        (R.mapComp (eta.app a) (R.map f)).hom := by
  simpa only using
    (StrongTransPostcomposition.naturalityIso_hom R eta f)

/-- 2-cell naturality is literally the already-proved postcomposition law. -/
theorem naturality_naturality
    {a b : B} {f g : a ⟶ b} (theta : f ⟶ g) :
    R.map₂ theta ▷ R.map (eta.app b) ≫
        (naturalityIso R eta g).hom =
      (naturalityIso R eta f).hom ≫
        R.map (eta.app a) ◁
          (Pseudofunctor.comp R R).map₂ theta := by
  exact StrongTransPostcomposition.naturality_naturality R eta theta

/-- Identity coherence with source R's original mapId. -/
theorem naturality_id (a : B) :
    (naturalityIso R eta (𝟙 a)).hom ≫
        R.map (eta.app a) ◁
          ((Pseudofunctor.comp R R).mapId a).hom =
      (R.mapId a).hom ▷ R.map (eta.app a) ≫
        (λ_ (R.map (eta.app a))).hom ≫
        (ρ_ (R.map (eta.app a))).inv := by
  have h := StrongTransPostcomposition.naturality_id R eta a
  rw [sourceMapId_hom R] at h
  exact h

/-- Composition coherence with source R's original compositor. -/
theorem naturality_comp
    {a b c : B} (f : a ⟶ b) (g : b ⟶ c) :
    (naturalityIso R eta (f ≫ g)).hom ≫
        R.map (eta.app a) ◁
          ((Pseudofunctor.comp R R).mapComp f g).hom =
      (R.mapComp f g).hom ▷ R.map (eta.app c) ≫
        (α_ (R.map f) (R.map g) (R.map (eta.app c))).hom ≫
        R.map f ◁ (naturalityIso R eta g).hom ≫
        (α_ (R.map f) (R.map (eta.app b)) (R.map (R.map g))).inv ≫
        (naturalityIso R eta f).hom ▷ R.map (R.map g) ≫
        (α_ (R.map (eta.app a)) (R.map (R.map f))
          (R.map (R.map g))).hom := by
  have h := StrongTransPostcomposition.naturality_comp R eta f g
  rw [sourceMapComp_hom R f g] at h
  exact h

/-- Postcompose the unit by R while keeping the source literally R. -/
def strongTrans :
    Pseudofunctor.StrongTrans R (Pseudofunctor.comp R R) where
  app a := R.map (eta.app a)
  naturality f := naturalityIso R eta f
  naturality_naturality theta :=
    naturality_naturality R eta theta
  naturality_id a := naturality_id R eta a
  naturality_comp f g := naturality_comp R eta f g

@[simp] theorem strongTrans_app (a : B) :
    (strongTrans R eta).app a = R.map (eta.app a) :=
  rfl

@[simp] theorem strongTrans_naturality
    {a b : B} (f : a ⟶ b) :
    (strongTrans R eta).naturality f =
      naturalityIso R eta f :=
  rfl

end UnitPostcomposition

end Generic

/-!
## Boundary after v5.72

The two eta/eta paths now share an exact native StrongTrans boundary:

* v5.53 UnitPrecomposition with H = R has components eta_(R X);
* v5.72 UnitPostcomposition has components R.map(eta_X).

Both run from R to R ; R.  Therefore the v5.67 eta/eta naturality isomorphism
can next be promoted to a modification between

  eta ; UnitPostcomposition(R, eta)

and

  eta ; UnitPrecomposition(R, eta),

with v5.69 supplying the substantive exchange law.
-/

#print axioms Generic.UnitPostcomposition.sourceMapId_hom
#print axioms Generic.UnitPostcomposition.sourceMapComp_hom
#print axioms Generic.UnitPostcomposition.naturality_naturality
#print axioms Generic.UnitPostcomposition.naturality_id
#print axioms Generic.UnitPostcomposition.naturality_comp
#print axioms Generic.UnitPostcomposition.strongTrans

end

end KUOS.DependentOriginationUnitPostcompositionNativeSourceV5_72
