import KUOS.DependentOriginationForwardSwallowtailModificationObstructionV5_70

namespace KUOS.DependentOriginationStrongTransPostcompositionVcompComparisonV5_71

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleCounitV5_54
open KUOS.DependentOriginationStrongTransModificationPostcompositionV5_62

set_option autoImplicit false

noncomputable section

/-!
# Postcomposition preserves StrongTrans vertical composition up to mapComp v5.71

For composable strong transformations

  alpha : F => G,
  beta  : G => K,

and a pseudofunctor H, there are two native strong transformations

  postcompose H (alpha ; beta)

and

  postcompose H alpha ; postcompose H beta.

They are not definitionally equal when H is non-strict.  At every object a
their components differ by exactly the compositor

  H.mapComp (alpha.app a) (beta.app a).

This file proves that these compositors satisfy modification naturality and
therefore form a native invertible modification.  The substantive proof uses
the already-established MappedSquare.composition theorem on the inverse
naturality squares of alpha and beta; no strictification of H is introduced.

This is the global coherence underlying the first mapComp step in the v5.68
forward-swallowtail component interchanger.
-/

namespace Generic

universe uB vB wB uC vC wC uD vD wD

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable {D : Type uD} [Bicategory.{wD, vD} D]

namespace PostcompositionVcomp

variable {F G K : Pseudofunctor B C}
variable (H : Pseudofunctor C D)
variable (alpha : Pseudofunctor.StrongTrans F G)
variable (beta : Pseudofunctor.StrongTrans G K)

/-- Postcompose the already vertically-composed transformation. -/
abbrev postVcomp :
    Pseudofunctor.StrongTrans
      (Pseudofunctor.comp F H)
      (Pseudofunctor.comp K H) :=
  StrongTransPostcomposition.strongTrans H
    (Pseudofunctor.StrongTrans.vcomp alpha beta)

/-- Vertically compose the two separately postcomposed transformations. -/
abbrev vcompPost :
    Pseudofunctor.StrongTrans
      (Pseudofunctor.comp F H)
      (Pseudofunctor.comp K H) :=
  Pseudofunctor.StrongTrans.vcomp
    (StrongTransPostcomposition.strongTrans H alpha)
    (StrongTransPostcomposition.strongTrans H beta)

/-- The only possible objectwise comparison supplied by pseudofunctoriality. -/
def componentIso (a : B) :
    (postVcomp H alpha beta).app a ≅
      (vcompPost H alpha beta).app a :=
  H.mapComp (alpha.app a) (beta.app a)

/-- The inverse naturality of a vertical StrongTrans composite, exposed in
the orientation required by MappedSquare.composition. -/
private theorem vcomp_naturality_inv
    {a b : B} (f : a ⟶ b) :
    ((Pseudofunctor.StrongTrans.vcomp alpha beta).naturality f).inv =
      ((((α_ (alpha.app a) (beta.app a) (K.map f)).hom ≫
          alpha.app a ◁ (beta.naturality f).inv) ≫
        (α_ (alpha.app a) (G.map f) (beta.app b)).inv) ≫
        (alpha.naturality f).inv ▷ beta.app b) ≫
        (α_ (F.map f) (alpha.app b) (beta.app b)).hom := by
  have h :=
    Pseudofunctor.StrongTrans.categoryStruct_comp_naturality_inv
      alpha beta f
  change
    ((Pseudofunctor.StrongTrans.vcomp alpha beta).naturality f).inv =
      ((((α_ (alpha.app a) (beta.app a) (K.map f)).hom ≫
          alpha.app a ◁ (beta.naturality f).inv) ≫
        (α_ (alpha.app a) (G.map f) (beta.app b)).inv) ≫
        (alpha.naturality f).inv ▷ beta.app b) ≫
        (α_ (F.map f) (alpha.app b) (beta.app b)).hom at h
  exact h

/-- Mapping the inverse naturality square is the inverse of the mapped
naturality square. -/
private theorem mapped_naturality_symm
    {P Q : Pseudofunctor B C}
    (gamma : Pseudofunctor.StrongTrans P Q)
    {a b : B} (f : a ⟶ b) :
    (MappedSquare.iso
      H
      (gamma.app a) (gamma.app b)
      (P.map f) (Q.map f)
      (gamma.naturality f).symm).hom =
      (StrongTransPostcomposition.naturalityIso H gamma f).inv := by
  simp only [MappedSquare.iso, StrongTransPostcomposition.naturalityIso,
    Iso.trans_inv, Iso.symm_inv, Iso.trans_hom, Iso.symm_hom,
    PrelaxFunctor.map₂Iso_hom, PrelaxFunctor.map₂Iso_inv,
    Category.assoc]

/-- The inverse naturality of the separately postcomposed vertical composite
has the expected five-factor form. -/
private theorem vcompPost_naturality_inv
    {a b : B} (f : a ⟶ b) :
    ((vcompPost H alpha beta).naturality f).inv =
      ((((α_
        (H.map (alpha.app a))
        (H.map (beta.app a))
        (H.map (K.map f))).hom ≫
        H.map (alpha.app a) ◁
          (StrongTransPostcomposition.naturalityIso H beta f).inv) ≫
        (α_
          (H.map (alpha.app a))
          (H.map (G.map f))
          (H.map (beta.app b))).inv) ≫
        (StrongTransPostcomposition.naturalityIso H alpha f).inv ▷
          H.map (beta.app b)) ≫
        (α_
          (H.map (F.map f))
          (H.map (alpha.app b))
          (H.map (beta.app b))).hom := by
  have h :=
    Pseudofunctor.StrongTrans.categoryStruct_comp_naturality_inv
      (StrongTransPostcomposition.strongTrans H alpha)
      (StrongTransPostcomposition.strongTrans H beta) f
  change
    ((vcompPost H alpha beta).naturality f).inv =
      ((((α_
        (H.map (alpha.app a))
        (H.map (beta.app a))
        (H.map (K.map f))).hom ≫
        H.map (alpha.app a) ◁
          (StrongTransPostcomposition.naturalityIso H beta f).inv) ≫
        (α_
          (H.map (alpha.app a))
          (H.map (G.map f))
          (H.map (beta.app b))).inv) ≫
        (StrongTransPostcomposition.naturalityIso H alpha f).inv ▷
          H.map (beta.app b)) ≫
        (α_
          (H.map (F.map f))
          (H.map (alpha.app b))
          (H.map (beta.app b))).hom at h
  exact h

/-- The compositor components satisfy the modification square.

The proof first applies MappedSquare.composition to the inverse alpha/beta
naturality squares.  This produces the inverse naturality equation.  We then
conjugate by the two naturality isomorphisms, cancelling each with its own
inverse, to obtain the ordinary modification-naturality orientation. -/
theorem naturality
    {a b : B} (f : a ⟶ b) :
    (Pseudofunctor.comp F H).map f ◁
          (componentIso H alpha beta b).hom ≫
        ((vcompPost H alpha beta).naturality f).hom =
      ((postVcomp H alpha beta).naturality f).hom ≫
        (componentIso H alpha beta a).hom ▷
          (Pseudofunctor.comp K H).map f := by
  let e :
      alpha.app a ≫ beta.app a ≅
        alpha.app a ≫ beta.app a :=
    Iso.refl _
  have hcomp :
      (((Pseudofunctor.StrongTrans.vcomp alpha beta).naturality f).symm).hom =
        e.hom ▷ K.map f ≫
          (α_ (alpha.app a) (beta.app a) (K.map f)).hom ≫
          alpha.app a ◁ ((beta.naturality f).symm).hom ≫
          (α_ (alpha.app a) (G.map f) (beta.app b)).inv ≫
          ((alpha.naturality f).symm).hom ▷ beta.app b ≫
          (α_ (F.map f) (alpha.app b) (beta.app b)).hom := by
    simp only [e, Iso.refl_hom, Bicategory.id_whiskerRight, Category.id_comp,
      Iso.symm_hom]
    simpa only [Category.assoc] using
      (vcomp_naturality_inv alpha beta f)
  have hmapped :=
    MappedSquare.composition
      H
      (alpha.app a) (beta.app a) (alpha.app a ≫ beta.app a)
      (alpha.app b) (beta.app b)
      (F.map f) (G.map f) (K.map f)
      e
      (alpha.naturality f).symm
      (beta.naturality f).symm
      ((Pseudofunctor.StrongTrans.vcomp alpha beta).naturality f).symm
      hcomp
  have hpost :
      (MappedSquare.iso H
        (alpha.app a ≫ beta.app a)
        (alpha.app b ≫ beta.app b)
        (F.map f) (K.map f)
        ((Pseudofunctor.StrongTrans.vcomp alpha beta).naturality f).symm).hom =
        ((postVcomp H alpha beta).naturality f).inv := by
    exact
      mapped_naturality_symm H
        (Pseudofunctor.StrongTrans.vcomp alpha beta) f
  have hbeta :
      (MappedSquare.iso H
        (beta.app a) (beta.app b)
        (G.map f) (K.map f)
        (beta.naturality f).symm).hom =
        (StrongTransPostcomposition.naturalityIso H beta f).inv :=
    mapped_naturality_symm H beta f
  have halpha :
      (MappedSquare.iso H
        (alpha.app a) (alpha.app b)
        (F.map f) (G.map f)
        (alpha.naturality f).symm).hom =
        (StrongTransPostcomposition.naturalityIso H alpha f).inv :=
    mapped_naturality_symm H alpha f
  have hinv :
      ((postVcomp H alpha beta).naturality f).inv ≫
          H.map (F.map f) ◁ (H.mapComp (alpha.app b) (beta.app b)).hom =
        (H.mapComp (alpha.app a) (beta.app a)).hom ▷ H.map (K.map f) ≫
          ((vcompPost H alpha beta).naturality f).inv := by
    rw [hpost, hbeta, halpha] at hmapped
    simp only [e, Iso.refl_hom, PrelaxFunctor.map₂_id,
      Category.id_comp] at hmapped
    have hv :
        ((vcompPost H alpha beta).naturality f).inv =
          (α_
            (H.map (alpha.app a))
            (H.map (beta.app a))
            (H.map (K.map f))).hom ≫
          H.map (alpha.app a) ◁
              (StrongTransPostcomposition.naturalityIso H beta f).inv ≫
          (α_
            (H.map (alpha.app a))
            (H.map (G.map f))
            (H.map (beta.app b))).inv ≫
          (StrongTransPostcomposition.naturalityIso H alpha f).inv ▷
              H.map (beta.app b) ≫
          (α_
            (H.map (F.map f))
            (H.map (alpha.app b))
            (H.map (beta.app b))).hom := by
      simpa only [Category.assoc] using
        (vcompPost_naturality_inv H alpha beta f)
    rw [← hv] at hmapped
    exact hmapped
  have hx :
      H.map (F.map f) ◁
          (H.mapComp (alpha.app b) (beta.app b)).hom =
        ((postVcomp H alpha beta).naturality f).hom ≫
          ((H.mapComp (alpha.app a) (beta.app a)).hom ▷ H.map (K.map f) ≫
            ((vcompPost H alpha beta).naturality f).inv) :=
    (((postVcomp H alpha beta).naturality f).inv_comp_eq).mp hinv
  change
    H.map (F.map f) ◁
          (H.mapComp (alpha.app b) (beta.app b)).hom ≫
        ((vcompPost H alpha beta).naturality f).hom =
      ((postVcomp H alpha beta).naturality f).hom ≫
        (H.mapComp (alpha.app a) (beta.app a)).hom ▷ H.map (K.map f)
  rw [hx]
  have hcancel := congrArg
    (fun t =>
      ((postVcomp H alpha beta).naturality f).hom ≫
        ((H.mapComp (alpha.app a) (beta.app a)).hom ▷ H.map (K.map f) ≫ t))
    ((vcompPost H alpha beta).naturality f).inv_hom_id
  simpa only [Category.assoc, Category.comp_id] using hcancel

local instance postVcompStrongTransHomCategory :
    Category
      (Pseudofunctor.StrongTrans
        (Pseudofunctor.comp F H)
        (Pseudofunctor.comp K H)) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := B) (C := D)
    (F := Pseudofunctor.comp F H)
    (G := Pseudofunctor.comp K H)

/-- Postcomposition preserves StrongTrans vertical composition up to the
canonical pseudofunctor compositor, globally at modification level. -/
def comparisonIso :
    @CategoryTheory.Iso
      (Pseudofunctor.StrongTrans
        (Pseudofunctor.comp F H)
        (Pseudofunctor.comp K H))
      (Pseudofunctor.StrongTrans.homCategory
        (B := B) (C := D)
        (F := Pseudofunctor.comp F H)
        (G := Pseudofunctor.comp K H))
      (postVcomp H alpha beta)
      (vcompPost H alpha beta) :=
  Pseudofunctor.StrongTrans.isoMk
    (η := postVcomp H alpha beta)
    (θ := vcompPost H alpha beta)
    (componentIso H alpha beta)
    (by
      intro a b f
      exact naturality H alpha beta f)

@[simp] theorem comparisonIso_hom_app (a : B) :
    (comparisonIso H alpha beta).hom.as.app a =
      (H.mapComp (alpha.app a) (beta.app a)).hom :=
  rfl

@[simp] theorem comparisonIso_inv_app (a : B) :
    (comparisonIso H alpha beta).inv.as.app a =
      (H.mapComp (alpha.app a) (beta.app a)).inv :=
  rfl

end PostcompositionVcomp

end Generic

/-!
## Boundary after v5.71

The first structural envelope in the v5.68 forward-swallowtail component
interchanger is now a global invertible modification, not merely a pointwise
mapComp isomorphism.

The remaining v5.70 naturality proof can therefore factor through:

1. this postcomposition-vcomp comparison;
2. native associator modification coherence in the functor bicategory;
3. the v5.69 eta/eta inverse exchange;
4. counit-whiskering naturality already available from the earlier
   postcomposition infrastructure.

No swallowtail equation is claimed here.
-/

#print axioms Generic.PostcompositionVcomp.naturality
#print axioms Generic.PostcompositionVcomp.comparisonIso
#print axioms Generic.PostcompositionVcomp.comparisonIso_hom_app
#print axioms Generic.PostcompositionVcomp.comparisonIso_inv_app

end

end KUOS.DependentOriginationStrongTransPostcompositionVcompComparisonV5_71
