import KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleUnitV5_53
import Mathlib.CategoryTheory.Bicategory.NaturalTransformation.Pseudo

namespace KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleCounitV5_54

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

set_option autoImplicit false

noncomputable section

/-!
# Non-strict counit postcomposition for the backward triangle v5.54

Prove mapped-square coherence before specializing any identity-functor
endpoint.  The resulting counit uses the old square between the two original
compositors of H.  No strictness, replacement comparison, or fresh equivalence
is introduced.  The concrete actual-lift specialization is assembled after
this generic kernel has been validated.
-/

universe uB vB wB uC vC wC uD vD wD uE vE wE u v uH vH uW uP

namespace MappedSquare

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable (H : Pseudofunctor B C)
variable {a b c x y z : B}

/-- Map a square with explicit four vertices before specializing its edges. -/
def iso (r : x ⟶ y) (f : a ⟶ b) (u : x ⟶ a) (v : y ⟶ b)
    (n : r ≫ v ≅ u ≫ f) :
    H.map r ≫ H.map v ≅ H.map u ≫ H.map f :=
  (H.mapComp r v).symm ≪≫ H.map₂Iso n ≪≫ H.mapComp u f

@[simp] theorem iso_hom (r : x ⟶ y) (f : a ⟶ b) (u : x ⟶ a) (v : y ⟶ b)
    (n : r ≫ v ≅ u ≫ f) :
    (iso H r f u v n).hom =
      (H.mapComp r v).inv ≫ H.map₂ n.hom ≫ (H.mapComp u f).hom := rfl

/-- Reverse the original associator preservation equality, without new data. -/
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

/-- Mapping respects an arbitrary 2-cell comparison between two squares. -/
theorem naturality (r s : x ⟶ y) (f g : a ⟶ b) (u : x ⟶ a) (v : y ⟶ b)
    (nf : r ≫ v ≅ u ≫ f) (ng : s ≫ v ≅ u ≫ g)
    (tau : r ⟶ s) (theta : f ⟶ g)
    (h : tau ▷ v ≫ ng.hom = nf.hom ≫ u ◁ theta) :
    H.map₂ tau ▷ H.map v ≫ (iso H s g u v ng).hom =
      (iso H r f u v nf).hom ≫ H.map u ◁ H.map₂ theta := by
  have hm := congrArg (fun t =>
    (H.mapComp r v).inv ≫ H.map₂ t ≫ (H.mapComp u g).hom) h
  dsimp only at hm
  rw [H.map₂_comp, H.map₂_comp, H.map₂_whisker_right,
    H.map₂_whisker_left] at hm
  simp only [Category.assoc] at hm
  rw [(H.mapComp r v).inv_hom_id_assoc,
    (H.mapComp u g).inv_hom_id, Category.comp_id] at hm
  simpa only [iso_hom, Category.assoc] using hm

/-- The image of an identity square retains the actual identity comparison. -/
theorem identity (r : x ⟶ x) (u : x ⟶ a) (e : r ≅ 𝟙 x)
    (n : r ≫ u ≅ u ≫ 𝟙 a)
    (h : n.hom = e.hom ▷ u ≫ (λ_ u).hom ≫ (ρ_ u).inv) :
    (iso H r (𝟙 a) u u n).hom ≫ H.map u ◁ (H.mapId a).hom =
      (H.map₂ e.hom ≫ (H.mapId x).hom) ▷ H.map u ≫
        (λ_ (H.map u)).hom ≫ (ρ_ (H.map u)).inv := by
  rw [iso_hom, h, H.map₂_comp, H.map₂_comp,
    H.map₂_whisker_right, H.map₂_left_unitor, H.mapComp_id_right_hom]
  simp only [Bicategory.comp_whiskerRight, Category.assoc]
  rw [(H.mapComp r u).inv_hom_id_assoc,
    (H.mapComp (𝟙 x) u).inv_hom_id_assoc,
    H.map₂_inv_hom_assoc (ρ_ u),
    Bicategory.whiskerLeft_inv_hom (H.map u) (H.mapId a), Category.comp_id]

/-- Map a composable pair of squares and their existing compositor law.
All seven cancellations use an original comparison and its own inverse. -/
theorem composition (r : x ⟶ y) (s : y ⟶ z) (k : x ⟶ z)
    (f : a ⟶ b) (g : b ⟶ c) (u : x ⟶ a) (v : y ⟶ b) (w : z ⟶ c)
    (e : k ≅ r ≫ s) (nf : r ≫ v ≅ u ≫ f) (ng : s ≫ w ≅ v ≫ g)
    (nfg : k ≫ w ≅ u ≫ (f ≫ g))
    (h : nfg.hom = e.hom ▷ w ≫ (α_ r s w).hom ≫
      r ◁ ng.hom ≫ (α_ r v g).inv ≫ nf.hom ▷ g ≫ (α_ u f g).hom) :
    (iso H k (f ≫ g) u w nfg).hom ≫ H.map u ◁ (H.mapComp f g).hom =
      (H.map₂ e.hom ≫ (H.mapComp r s).hom) ▷ H.map w ≫
        (α_ (H.map r) (H.map s) (H.map w)).hom ≫
        H.map r ◁ (iso H s g v w ng).hom ≫
        (α_ (H.map r) (H.map v) (H.map g)).inv ≫
        (iso H r f u v nf).hom ▷ H.map g ≫
        (α_ (H.map u) (H.map f) (H.map g)).hom := by
  rw [iso_hom H k (f ≫ g), h,
    H.map₂_comp, H.map₂_comp, H.map₂_comp, H.map₂_comp, H.map₂_comp,
    H.map₂_whisker_right, H.map₂_associator, H.map₂_whisker_left,
    map_associator_inv H, H.map₂_whisker_right, H.map₂_associator,
    iso_hom H s g, iso_hom H r f]
  simp only [Bicategory.whiskerLeft_comp, Bicategory.comp_whiskerRight, Category.assoc]
  rw [(H.mapComp k w).inv_hom_id_assoc,
    (H.mapComp (r ≫ s) w).inv_hom_id_assoc,
    (H.mapComp r (s ≫ w)).inv_hom_id_assoc,
    (H.mapComp r (v ≫ g)).inv_hom_id_assoc,
    (H.mapComp (r ≫ v) g).inv_hom_id_assoc,
    (H.mapComp (u ≫ f) g).inv_hom_id_assoc,
    (H.mapComp u (f ≫ g)).inv_hom_id_assoc,
    Bicategory.whiskerLeft_inv_hom (H.map u) (H.mapComp f g), Category.comp_id]

end MappedSquare

namespace CounitPostcomposition

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable (H : Pseudofunctor B C) {R : Pseudofunctor B B}
variable (eps : Pseudofunctor.StrongTrans R (Pseudofunctor.id B))

/-- The original three-isomorphism paste, without replacing the counit. -/
def naturalityIso {a b : B} (f : a ⟶ b) :
    H.map (R.map f) ≫ H.map (eps.app b) ≅ H.map (eps.app a) ≫ H.map f :=
  (H.mapComp (R.map f) (eps.app b)).symm ≪≫
    H.map₂Iso (eps.naturality f) ≪≫ H.mapComp (eps.app a) f

@[simp] theorem naturalityIso_hom {a b : B} (f : a ⟶ b) :
    (naturalityIso H eps f).hom =
      (H.mapComp (R.map f) (eps.app b)).inv ≫
        H.map₂ (eps.naturality f).hom ≫ (H.mapComp (eps.app a) f).hom := rfl

/-- Typed cancellation before specializing an identity-target endpoint. -/
private theorem erase_whiskerLeft_id {a b c : B}
    (u : a ⟶ b) (f : b ⟶ c) {k : a ⟶ c} (t : k ⟶ u ≫ f) :
    t ≫ u ◁ 𝟙 f = t := by
  rw [Bicategory.whiskerLeft_id, Category.comp_id]

private theorem counit_id (a : B) :
    (eps.naturality (𝟙 a)).hom =
      (R.mapId a).hom ▷ eps.app a ≫
        (λ_ (eps.app a)).hom ≫ (ρ_ (eps.app a)).inv :=
  (erase_whiskerLeft_id (eps.app a) (𝟙 a)
    (eps.naturality (𝟙 a)).hom).symm.trans (eps.naturality_id a)

private theorem counit_comp {a b c : B} (f : a ⟶ b) (g : b ⟶ c) :
    (eps.naturality (f ≫ g)).hom =
      (R.mapComp f g).hom ▷ eps.app c ≫
        (α_ (R.map f) (R.map g) (eps.app c)).hom ≫
        R.map f ◁ (eps.naturality g).hom ≫
        (α_ (R.map f) (eps.app b) g).inv ≫
        (eps.naturality f).hom ▷ g ≫ (α_ (eps.app a) f g).hom :=
  (erase_whiskerLeft_id (eps.app a) (f ≫ g)
    (eps.naturality (f ≫ g)).hom).symm.trans (eps.naturality_comp f g)

/-- Specialize a proved mapped square; no rewriting through Id.obj is needed. -/
theorem naturality {a b : B} {f g : a ⟶ b} (theta : f ⟶ g) :
    H.map₂ (R.map₂ theta) ▷ H.map (eps.app b) ≫ (naturalityIso H eps g).hom =
      (naturalityIso H eps f).hom ≫ H.map (eps.app a) ◁ H.map₂ theta :=
  MappedSquare.naturality H (R.map f) (R.map g) f g (eps.app a) (eps.app b)
    (eps.naturality f) (eps.naturality g) (R.map₂ theta) theta
    (eps.naturality_naturality theta)

/-- Keep both H's and the composite's actual identity comparisons. -/
theorem naturality_id (a : B) :
    (naturalityIso H eps (𝟙 a)).hom ≫ H.map (eps.app a) ◁ (H.mapId a).hom =
      ((Pseudofunctor.comp R H).mapId a).hom ▷ H.map (eps.app a) ≫
        (λ_ (H.map (eps.app a))).hom ≫ (ρ_ (H.map (eps.app a))).inv :=
  MappedSquare.identity H (R.map (𝟙 a)) (eps.app a) (R.mapId a)
    (eps.naturality (𝟙 a)) (counit_id eps a)

/-- Keep both actual compositors, specializing the proved pasted-square law. -/
theorem naturality_comp {a b c : B} (f : a ⟶ b) (g : b ⟶ c) :
    (naturalityIso H eps (f ≫ g)).hom ≫
        H.map (eps.app a) ◁ (H.mapComp f g).hom =
      ((Pseudofunctor.comp R H).mapComp f g).hom ▷ H.map (eps.app c) ≫
        (α_ (H.map (R.map f)) (H.map (R.map g)) (H.map (eps.app c))).hom ≫
        H.map (R.map f) ◁ (naturalityIso H eps g).hom ≫
        (α_ (H.map (R.map f)) (H.map (eps.app b)) (H.map g)).inv ≫
        (naturalityIso H eps f).hom ▷ H.map g ≫
        (α_ (H.map (eps.app a)) (H.map f) (H.map g)).hom :=
  MappedSquare.composition H (R.map f) (R.map g) (R.map (f ≫ g))
    f g (eps.app a) (eps.app b) (eps.app c) (R.mapComp f g)
    (eps.naturality f) (eps.naturality g) (eps.naturality (f ≫ g)) (counit_comp eps f g)

/-- Native postcomposition of a counit by an arbitrary non-strict H. -/
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

/-- Compare the actual identity comparisons of the two native bracketings. -/
theorem mapId_hom (a : B) :
    ((Pseudofunctor.comp (Pseudofunctor.comp P Q) H).mapId a).hom =
      ((Pseudofunctor.comp P (Pseudofunctor.comp Q H)).mapId a).hom := by
  change H.map₂ (Q.map₂ (P.mapId a).hom ≫ (Q.mapId (P.obj a)).hom) ≫
      (H.mapId (Q.obj (P.obj a))).hom =
    H.map₂ (Q.map₂ (P.mapId a).hom) ≫
      H.map₂ (Q.mapId (P.obj a)).hom ≫ (H.mapId (Q.obj (P.obj a))).hom
  rw [PrelaxFunctor.map₂_comp, Category.assoc]

/-- Compare the original compositors without assuming strictness. -/
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

/-! ## Specialization to the original actual-lift G and counit -/

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactLiftableActualLiftOneCellV5_40
open KUOS.DependentOriginationExactLiftableActualLiftStrictPseudofunctorV5_42
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleUnitV5_53
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- The native left-associated source of the second backward-triangle factor:
    (G ; F) ; G. No reassociation is hidden in this definition. -/
def actualLiftQuasiInverseCounitTriple :
    Pseudofunctor
      (ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)
      (ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :=
  Pseudofunctor.comp
    (actualLiftTargetRoundtrip (W := W) A)
    (actualLiftQuasiInversePseudofunctor (W := W) A)

/-- Apply the original non-strict G to the original target counit.
The source remains literally (G ; F) ; G; reassociation to G ; (F ; G)
is a separate coherence obligation. -/
def actualLiftQuasiInverseRestrictedTargetCounit :
    Pseudofunctor.StrongTrans
      (actualLiftQuasiInverseCounitTriple (W := W) A)
      (actualLiftQuasiInversePseudofunctor (W := W) A) :=
  CounitPostcomposition.strongTrans
    (actualLiftQuasiInversePseudofunctor (W := W) A)
    (actualLiftTargetRoundtripCounit (W := W) A)

@[simp] theorem actualLiftQuasiInverseRestrictedTargetCounit_app
    (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftQuasiInverseRestrictedTargetCounit (W := W) A).app Y =
      (actualLiftQuasiInversePseudofunctor (W := W) A).map
        ((actualLiftTargetRoundtripCounit (W := W) A).app Y) := rfl

@[simp] theorem actualLiftQuasiInverseRestrictedTargetCounit_naturality
    {Y Z : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (k : Y ⟶ Z) :
    (actualLiftQuasiInverseRestrictedTargetCounit (W := W) A).naturality k =
      CounitPostcomposition.naturalityIso
        (actualLiftQuasiInversePseudofunctor (W := W) A)
        (actualLiftTargetRoundtripCounit (W := W) A) k := rfl

/-- The same original counit factor with the source bracketed exactly as the
v5.53 unit factor's target, G ; (F ; G). Only the source mapId/mapComp
coherence is reconciled by TripleComparison; app and naturality are unchanged. -/
def actualLiftQuasiInverseRestrictedTargetCounitReassociated :
    Pseudofunctor.StrongTrans
      (actualLiftQuasiInverseTriple (W := W) A)
      (actualLiftQuasiInversePseudofunctor (W := W) A) where
  app Y := (actualLiftQuasiInverseRestrictedTargetCounit (W := W) A).app Y
  naturality k := (actualLiftQuasiInverseRestrictedTargetCounit (W := W) A).naturality k
  naturality_naturality theta :=
    (actualLiftQuasiInverseRestrictedTargetCounit (W := W) A).naturality_naturality theta
  naturality_id Y := by
    rw [← TripleComparison.mapId_hom
      (actualLiftQuasiInversePseudofunctor (W := W) A)
      (exactLiftableActualLiftStrictPseudofunctor (W := W) A)
      (actualLiftQuasiInversePseudofunctor (W := W) A)]
    exact (actualLiftQuasiInverseRestrictedTargetCounit (W := W) A).naturality_id Y
  naturality_comp k l := by
    rw [← TripleComparison.mapComp_hom
      (actualLiftQuasiInversePseudofunctor (W := W) A)
      (exactLiftableActualLiftStrictPseudofunctor (W := W) A)
      (actualLiftQuasiInversePseudofunctor (W := W) A)]
    exact (actualLiftQuasiInverseRestrictedTargetCounit (W := W) A).naturality_comp k l

@[simp] theorem actualLiftQuasiInverseRestrictedTargetCounitReassociated_app
    (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftQuasiInverseRestrictedTargetCounitReassociated (W := W) A).app Y =
      (actualLiftQuasiInverseRestrictedTargetCounit (W := W) A).app Y := rfl

@[simp] theorem actualLiftQuasiInverseRestrictedTargetCounitReassociated_naturality
    {Y Z : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel} (k : Y ⟶ Z) :
    (actualLiftQuasiInverseRestrictedTargetCounitReassociated (W := W) A).naturality k =
      (actualLiftQuasiInverseRestrictedTargetCounit (W := W) A).naturality k := rfl

section GenericRegression

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]

-- Original regression specification: postcompose a counit by non-strict H.
example (H : Pseudofunctor B C) (R : Pseudofunctor B B)
    (eps : Pseudofunctor.StrongTrans R (Pseudofunctor.id B)) :
    Pseudofunctor.StrongTrans (Pseudofunctor.comp R H) H :=
  CounitPostcomposition.strongTrans H eps

end GenericRegression

#print axioms MappedSquare.naturality
#print axioms MappedSquare.identity
#print axioms MappedSquare.composition
#print axioms CounitPostcomposition.naturality
#print axioms CounitPostcomposition.naturality_id
#print axioms CounitPostcomposition.naturality_comp
#print axioms CounitPostcomposition.strongTrans
#print axioms TripleComparison.mapId_hom
#print axioms TripleComparison.mapComp_hom
#print axioms actualLiftQuasiInverseRestrictedTargetCounit
#print axioms actualLiftQuasiInverseRestrictedTargetCounitReassociated

end

end KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleCounitV5_54
