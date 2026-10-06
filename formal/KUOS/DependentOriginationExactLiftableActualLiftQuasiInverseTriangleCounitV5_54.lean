import Mathlib.CategoryTheory.Bicategory.NaturalTransformation.Pseudo

namespace KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleCounitV5_54

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

set_option autoImplicit false

noncomputable section

/-!
# Non-strict counit postcomposition for the backward triangle v5.54

First establish the construction in arbitrary bicategories.  All comparison
isomorphisms of the postcomposing pseudofunctor are retained.  The naturality
is the original mapped counit square between the two actual compositors.
The concrete actual-lift specialization is a subsequent assembly step.
-/

universe uB vB wB uC vC wC uD vD wD uE vE wE

namespace CounitPostcomposition

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable (H : Pseudofunctor B C) {R : Pseudofunctor B B}
variable (eps : Pseudofunctor.StrongTrans R (Pseudofunctor.id B))

/-- The mapped counit square, with both non-strict compositors intact. -/
def naturalityIso {a b : B} (f : a ⟶ b) :
    H.map (R.map f) ≫ H.map (eps.app b) ≅ H.map (eps.app a) ≫ H.map f :=
  (H.mapComp (R.map f) (eps.app b)).symm ≪≫
    H.map₂Iso (eps.naturality f) ≪≫ H.mapComp (eps.app a) f

@[simp] theorem naturalityIso_hom {a b : B} (f : a ⟶ b) :
    (naturalityIso H eps f).hom =
      (H.mapComp (R.map f) (eps.app b)).inv ≫
        H.map₂ (eps.naturality f).hom ≫ (H.mapComp (eps.app a) f).hom := rfl

/-- Reverse the existing associator preservation law as an equality of isos. -/
private theorem map_associator_inv {a b c d : B}
    (f : a ⟶ b) (g : b ⟶ c) (k : c ⟶ d) :
    H.map₂ (α_ f g k).inv =
      (H.mapComp f (g ≫ k)).hom ≫
        H.map f ◁ (H.mapComp g k).hom ≫
        (α_ (H.map f) (H.map g) (H.map k)).inv ≫
        (H.mapComp f g).inv ▷ H.map k ≫
        (H.mapComp (f ≫ g) k).inv := by
  have h : H.map₂Iso (α_ f g k) =
      H.mapComp (f ≫ g) k ≪≫
        Bicategory.whiskerRightIso (H.mapComp f g) (H.map k) ≪≫
        (α_ (H.map f) (H.map g) (H.map k)) ≪≫
        Bicategory.whiskerLeftIso (H.map f) (H.mapComp g k).symm ≪≫
        (H.mapComp f (g ≫ k)).symm := by
    apply Iso.ext
    exact H.map₂_associator f g k
  simpa only [Iso.trans_inv, Iso.symm_inv, Bicategory.whiskerLeftIso_inv,
    Bicategory.whiskerRightIso_inv, Category.assoc] using congrArg Iso.inv h

/-- Normalize only the comparison of the identity target, not that of R. -/
private theorem counit_id (a : B) :
    (eps.naturality (𝟙 a)).hom =
      (R.mapId a).hom ▷ eps.app a ≫
        (λ_ (eps.app a)).hom ≫ (ρ_ (eps.app a)).inv := by
  have h := eps.naturality_id a
  change (eps.naturality (𝟙 a)).hom ≫ eps.app a ◁ 𝟙 (𝟙 a) =
    (R.mapId a).hom ▷ eps.app a ≫
      (λ_ (eps.app a)).hom ≫ (ρ_ (eps.app a)).inv at h
  simpa only [Bicategory.whiskerLeft_id, Category.comp_id] using h

/-- The original composition law with only the identity target exposed. -/
private theorem counit_comp {a b c : B} (f : a ⟶ b) (g : b ⟶ c) :
    (eps.naturality (f ≫ g)).hom =
      (R.mapComp f g).hom ▷ eps.app c ≫
        (α_ (R.map f) (R.map g) (eps.app c)).hom ≫
        R.map f ◁ (eps.naturality g).hom ≫
        (α_ (R.map f) (eps.app b) g).inv ≫
        (eps.naturality f).hom ▷ g ≫ (α_ (eps.app a) f g).hom := by
  have h := eps.naturality_comp f g
  change (eps.naturality (f ≫ g)).hom ≫ eps.app a ◁ 𝟙 (f ≫ g) =
    (R.mapComp f g).hom ▷ eps.app c ≫
      (α_ (R.map f) (R.map g) (eps.app c)).hom ≫
      R.map f ◁ (eps.naturality g).hom ≫
      (α_ (R.map f) (eps.app b) g).inv ≫
      (eps.naturality f).hom ▷ g ≫ (α_ (eps.app a) f g).hom at h
  simpa only [Bicategory.whiskerLeft_id, Category.comp_id] using h

/-- Map the old arbitrary-2-cell square, then cancel the outer compositors. -/
theorem naturality {a b : B} {f g : a ⟶ b} (theta : f ⟶ g) :
    H.map₂ (R.map₂ theta) ▷ H.map (eps.app b) ≫ (naturalityIso H eps g).hom =
      (naturalityIso H eps f).hom ≫ H.map (eps.app a) ◁ H.map₂ theta := by
  have heps : R.map₂ theta ▷ eps.app b ≫ (eps.naturality g).hom =
      (eps.naturality f).hom ≫ eps.app a ◁ theta :=
    eps.naturality_naturality theta
  have h := congrArg (fun t =>
    (H.mapComp (R.map f) (eps.app b)).inv ≫ H.map₂ t ≫
      (H.mapComp (eps.app a) g).hom) heps
  simpa only [naturalityIso_hom, PrelaxFunctor.map₂_comp,
    Pseudofunctor.map₂_whisker_left, Pseudofunctor.map₂_whisker_right,
    Category.assoc, Iso.inv_hom_id_assoc, Iso.inv_hom_id, Category.comp_id] using h

/-- The actual composite identity comparison, with H itself as target. -/
theorem naturality_id (a : B) :
    (naturalityIso H eps (𝟙 a)).hom ≫ H.map (eps.app a) ◁ (H.mapId a).hom =
      ((Pseudofunctor.comp R H).mapId a).hom ▷ H.map (eps.app a) ≫
        (λ_ (H.map (eps.app a))).hom ≫ (ρ_ (H.map (eps.app a))).inv := by
  change ((H.mapComp (R.map (𝟙 a)) (eps.app a)).inv ≫
    H.map₂ (eps.naturality (𝟙 a)).hom ≫
    (H.mapComp (eps.app a) (𝟙 a)).hom) ≫
      H.map (eps.app a) ◁ (H.mapId a).hom =
    (H.map₂ (R.mapId a).hom ≫ (H.mapId (R.obj a)).hom) ▷ H.map (eps.app a) ≫
      (λ_ (H.map (eps.app a))).hom ≫ (ρ_ (H.map (eps.app a))).inv
  rw [counit_id eps a]
  simp only [PrelaxFunctor.map₂_comp, Pseudofunctor.map₂_whisker_right,
    Pseudofunctor.map₂_left_unitor, H.mapComp_id_right_hom,
    Bicategory.comp_whiskerRight, Category.assoc, Iso.inv_hom_id_assoc,
    PrelaxFunctor.map₂_inv_hom_assoc, Bicategory.whiskerLeft_inv_hom,
    Category.comp_id]

/-- Map the original composition diagram, including its three associators.
Every cancelling comparison occurs together with its own inverse. -/
theorem naturality_comp {a b c : B} (f : a ⟶ b) (g : b ⟶ c) :
    (naturalityIso H eps (f ≫ g)).hom ≫
        H.map (eps.app a) ◁ (H.mapComp f g).hom =
      ((Pseudofunctor.comp R H).mapComp f g).hom ▷ H.map (eps.app c) ≫
        (α_ (H.map (R.map f)) (H.map (R.map g)) (H.map (eps.app c))).hom ≫
        H.map (R.map f) ◁ (naturalityIso H eps g).hom ≫
        (α_ (H.map (R.map f)) (H.map (eps.app b)) (H.map g)).inv ≫
        (naturalityIso H eps f).hom ▷ H.map g ≫
        (α_ (H.map (eps.app a)) (H.map f) (H.map g)).hom := by
  change ((H.mapComp (R.map (f ≫ g)) (eps.app c)).inv ≫
    H.map₂ (eps.naturality (f ≫ g)).hom ≫
    (H.mapComp (eps.app a) (f ≫ g)).hom) ≫
      H.map (eps.app a) ◁ (H.mapComp f g).hom =
    (H.map₂ (R.mapComp f g).hom ≫ (H.mapComp (R.map f) (R.map g)).hom) ▷
      H.map (eps.app c) ≫ _
  rw [counit_comp eps f g]
  simp only [naturalityIso_hom, PrelaxFunctor.map₂_comp,
    Pseudofunctor.map₂_whisker_left, Pseudofunctor.map₂_whisker_right,
    Pseudofunctor.map₂_associator, map_associator_inv,
    Bicategory.whiskerLeft_comp, Bicategory.comp_whiskerRight,
    Category.assoc, Iso.inv_hom_id_assoc, Iso.inv_hom_id,
    Bicategory.whiskerLeft_inv_hom, Category.comp_id]

/-- Postcompose a counit by an arbitrary pseudofunctor, retaining all its
comparison isomorphisms and all three native StrongTrans coherence fields. -/
def strongTrans : Pseudofunctor.StrongTrans (Pseudofunctor.comp R H) H where
  app a := H.map (eps.app a)
  naturality f := naturalityIso H eps f
  naturality_naturality theta := naturality H eps theta
  naturality_id a := naturality_id H eps a
  naturality_comp f g := naturality_comp H eps f g

@[simp] theorem strongTrans_app (a : B) :
    (strongTrans H eps).app a = H.map (eps.app a) := rfl

@[simp] theorem strongTrans_naturality {a b : B} (f : a ⟶ b) :
    (strongTrans H eps).naturality f = naturalityIso H eps f := rfl

end CounitPostcomposition

namespace TripleComparison

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable {D : Type uD} [Bicategory.{wD, vD} D]
variable {E : Type uE} [Bicategory.{wE, vE} E]
variable (P : Pseudofunctor B C) (Q : Pseudofunctor C D) (H : Pseudofunctor D E)

/-- The two native bracketings have equal identity comparisons by map2_comp. -/
theorem mapId_hom (a : B) :
    ((Pseudofunctor.comp (Pseudofunctor.comp P Q) H).mapId a).hom =
      ((Pseudofunctor.comp P (Pseudofunctor.comp Q H)).mapId a).hom := by
  change H.map₂ (Q.map₂ (P.mapId a).hom ≫ (Q.mapId (P.obj a)).hom) ≫
      (H.mapId (Q.obj (P.obj a))).hom =
    H.map₂ (Q.map₂ (P.mapId a).hom) ≫
      H.map₂ (Q.mapId (P.obj a)).hom ≫ (H.mapId (Q.obj (P.obj a))).hom
  rw [PrelaxFunctor.map₂_comp, Category.assoc]

/-- The compositor comparison does not require any of P, Q, H to be strict. -/
theorem mapComp_hom {a b c : B} (f : a ⟶ b) (g : b ⟶ c) :
    ((Pseudofunctor.comp (Pseudofunctor.comp P Q) H).mapComp f g).hom =
      ((Pseudofunctor.comp P (Pseudofunctor.comp Q H)).mapComp f g).hom := by
  change H.map₂ (Q.map₂ (P.mapComp f g).hom ≫
      (Q.mapComp (P.map f) (P.map g)).hom) ≫
      (H.mapComp (Q.map (P.map f)) (Q.map (P.map g))).hom =
    H.map₂ (Q.map₂ (P.mapComp f g).hom) ≫
      H.map₂ (Q.mapComp (P.map f) (P.map g)).hom ≫
      (H.mapComp (Q.map (P.map f)) (Q.map (P.map g))).hom
  rw [PrelaxFunctor.map₂_comp, Category.assoc]

end TripleComparison

section GenericRegression

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]

-- Original regression specification: postcompose a counit by non-strict H.
example (H : Pseudofunctor B C) (R : Pseudofunctor B B)
    (eps : Pseudofunctor.StrongTrans R (Pseudofunctor.id B)) :
    Pseudofunctor.StrongTrans (Pseudofunctor.comp R H) H :=
  CounitPostcomposition.strongTrans H eps

end GenericRegression

#print axioms CounitPostcomposition.naturality
#print axioms CounitPostcomposition.naturality_id
#print axioms CounitPostcomposition.naturality_comp
#print axioms CounitPostcomposition.strongTrans
#print axioms TripleComparison.mapId_hom
#print axioms TripleComparison.mapComp_hom

end

end KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleCounitV5_54
