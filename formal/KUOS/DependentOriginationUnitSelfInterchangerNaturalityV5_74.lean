import KUOS.DependentOriginationUnitSelfInterchangerBoundaryV5_73

namespace KUOS.DependentOriginationUnitSelfInterchangerNaturalityV5_74

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleUnitV5_53
open KUOS.DependentOriginationUnitPostcompositionNativeSourceV5_72
open KUOS.DependentOriginationUnitPostcompositionNativeSourceV5_72.Generic
open KUOS.DependentOriginationUnitSelfInterchangerBoundaryV5_73
open KUOS.DependentOriginationUnitSelfInterchangerBoundaryV5_73.Generic
open KUOS.DependentOriginationUnitSelfInterchangerBoundaryV5_73.Generic.UnitSelfInterchanger

set_option autoImplicit false

noncomputable section

/-!
# Unit self-interchanger naturality v5.74

The v5.73 boundary compares the two native eta/eta paths

  eta ; UnitPostcomposition(R, eta)
  eta ; UnitPrecomposition(R, eta)

by the inverse of eta.naturality(eta_X).

It is cleaner to prove the opposite orientation first.  In that direction the
component is eta.naturality(eta_X).hom, and the unique non-structural square is
exactly eta.naturality_naturality applied to eta.naturality(f).hom.  Mathlib's
StrongTrans.isoMk then constructs the inverse modification automatically, so
the v5.73 post-to-pre orientation is obtained without re-proving inverse
naturality by hand.
-/

namespace Generic

universe uB vB wB

variable {B : Type uB} [Bicategory.{wB, vB} B]

namespace UnitSelfInterchanger

variable (R : Pseudofunctor B B)
variable (eta : Pseudofunctor.StrongTrans (Pseudofunctor.id B) R)

/-- The eta/eta component in the forward pseudonaturality orientation. -/
def reverseComponentIso (X : B) :
    (prePath R eta).app X ≅
      (postPath R eta).app X :=
  eta.naturality (eta.app X)

@[simp] theorem reverseComponentIso_hom (X : B) :
    (reverseComponentIso R eta X).hom =
      (eta.naturality (eta.app X)).hom :=
  rfl

/-- Modification naturality in the forward pseudonaturality orientation. -/
def ReverseNaturality : Prop :=
  ∀ {X Y : B} (f : X ⟶ Y),
    (Pseudofunctor.id B).map f ◁
          (reverseComponentIso R eta Y).hom ≫
        ((postPath R eta).naturality f).hom =
      ((prePath R eta).naturality f).hom ≫
        (reverseComponentIso R eta X).hom ▷
          (Pseudofunctor.comp R R).map f

/-- The central eta/eta modification square.  The only non-structural input is
2-cell naturality of eta at eta.naturality(f).hom; the two composition laws
then expose the pre- and post-composed naturality factors. -/
theorem reverseNaturality : ReverseNaturality R eta := by
  intro X Y f
  have hY :=
    Pseudofunctor.StrongTrans.naturality_comp_hom
      eta f (eta.app Y)
  have hX :=
    Pseudofunctor.StrongTrans.naturality_comp_hom
      eta (eta.app X) (R.map f)
  let preIso :
      (Pseudofunctor.id B).map (f ≫ eta.app Y) ≫
          eta.app (R.obj Y) ≅
        (Pseudofunctor.id B).map f ≫ (prePath R eta).app Y :=
    Bicategory.whiskerRightIso
        ((Pseudofunctor.id B).mapComp f (eta.app Y))
        (eta.app (R.obj Y)) ≪≫
      (α_
        ((Pseudofunctor.id B).map f)
        ((Pseudofunctor.id B).map (eta.app Y))
        (eta.app (R.obj Y)))
  let postIso :
      (postPath R eta).app X ≫
          (Pseudofunctor.comp R R).map f ≅
        eta.app X ≫ R.map (eta.app X ≫ R.map f) :=
    (α_ (eta.app X) (R.map (eta.app X))
      (R.map (R.map f))) ≪≫
      Bicategory.whiskerLeftIso
        (eta.app X)
        (R.mapComp (eta.app X) (R.map f)).symm
  apply (cancel_epi preIso.hom).mp
  apply (cancel_mono postIso.hom).mp
  simp only [
    preIso, postIso, Iso.trans_hom,
    Bicategory.whiskerRightIso_hom,
    Bicategory.whiskerLeftIso_hom
  ]
  dsimp only [postPath, prePath]
  have hpost :=
    Pseudofunctor.StrongTrans.categoryStruct_comp_naturality_hom
      eta (UnitPostcomposition.strongTrans R eta) f
  change
    ((Pseudofunctor.StrongTrans.vcomp
      eta (UnitPostcomposition.strongTrans R eta)).naturality f).hom = _
      at hpost
  have hpre :=
    Pseudofunctor.StrongTrans.categoryStruct_comp_naturality_hom
      eta (UnitPrecomposition.strongTrans R eta) f
  change
    ((Pseudofunctor.StrongTrans.vcomp
      eta (UnitPrecomposition.strongTrans R eta)).naturality f).hom = _
      at hpre
  let leftFactor :=
    (α_ ((Pseudofunctor.id B).map f) (eta.app Y)
      (R.map (eta.app Y))).inv ≫
      (eta.naturality f).hom ▷ R.map (eta.app Y) ≫
        (α_ (eta.app X) (R.map f) (R.map (eta.app Y))).hom
  let rightFactor :=
    (α_ (eta.app X) (R.map (eta.app X))
      ((Pseudofunctor.comp R R).map f)).inv
  have hsplit :
      eta.app X ◁
          ((R.mapComp f (eta.app Y)).inv ≫
            (R.map₂ (eta.naturality f).hom ≫
              (R.mapComp (eta.app X) (R.map f)).hom)) =
        (eta.app X ◁ (R.mapComp f (eta.app Y)).inv) ≫
          (eta.app X ◁
            (R.map₂ (eta.naturality f).hom ≫
              (R.mapComp (eta.app X) (R.map f)).hom)) :=
    Bicategory.whiskerLeft_comp
      (eta.app X)
      (R.mapComp f (eta.app Y)).inv
      (R.map₂ (eta.naturality f).hom ≫
        (R.mapComp (eta.app X) (R.map f)).hom)
  have hpostRaw :
      ((Pseudofunctor.StrongTrans.vcomp
        eta (UnitPostcomposition.strongTrans R eta)).naturality f).hom =
        leftFactor ≫
          (eta.app X ◁
            ((R.mapComp f (eta.app Y)).inv ≫
              (R.map₂ (eta.naturality f).hom ≫
                (R.mapComp (eta.app X) (R.map f)).hom))) ≫
          rightFactor := by
    simpa only [leftFactor, rightFactor,
      UnitPostcomposition.strongTrans_app,
      UnitPostcomposition.strongTrans_naturality,
      UnitPostcomposition.naturalityIso_hom,
      Category.assoc] using hpost
  have hpostNorm :
      ((Pseudofunctor.StrongTrans.vcomp
        eta (UnitPostcomposition.strongTrans R eta)).naturality f).hom =
        leftFactor ≫
          (eta.app X ◁ (R.mapComp f (eta.app Y)).inv) ≫
          (eta.app X ◁ R.map₂ (eta.naturality f).hom) ≫
          (eta.app X ◁ (R.mapComp (eta.app X) (R.map f)).hom) ≫
          rightFactor := by
    calc
      _ = leftFactor ≫
            (eta.app X ◁
              ((R.mapComp f (eta.app Y)).inv ≫
                (R.map₂ (eta.naturality f).hom ≫
                  (R.mapComp (eta.app X) (R.map f)).hom))) ≫
            rightFactor := hpostRaw
      _ = leftFactor ≫
            ((eta.app X ◁ (R.mapComp f (eta.app Y)).inv) ≫
              (eta.app X ◁
                (R.map₂ (eta.naturality f).hom ≫
                  (R.mapComp (eta.app X) (R.map f)).hom))) ≫
            rightFactor :=
          congrArg (fun t => leftFactor ≫ t ≫ rightFactor) hsplit
      _ = _ := by
        simp only [Bicategory.whiskerLeft_comp, Category.assoc]
  have htail :
      (eta.app X ◁ (R.mapComp (eta.app X) (R.map f)).hom) ≫
        (α_ (eta.app X) (R.map (eta.app X))
          ((Pseudofunctor.comp R R).map f)).inv ≫
        (α_ (eta.app X) (R.map (eta.app X))
          (R.map (R.map f))).hom ≫
        (eta.app X ◁ (R.mapComp (eta.app X) (R.map f)).inv) =
      (eta.app X ◁ (R.mapComp (eta.app X) (R.map f)).hom) ≫
        (eta.app X ◁ (R.mapComp (eta.app X) (R.map f)).inv) := by
    change
      (eta.app X ◁ (R.mapComp (eta.app X) (R.map f)).hom) ≫
        (α_ (eta.app X) (R.map (eta.app X))
          (R.map (R.map f))).inv ≫
        (α_ (eta.app X) (R.map (eta.app X))
          (R.map (R.map f))).hom ≫
        (eta.app X ◁ (R.mapComp (eta.app X) (R.map f)).inv) =
      (eta.app X ◁ (R.mapComp (eta.app X) (R.map f)).hom) ≫
        (eta.app X ◁ (R.mapComp (eta.app X) (R.map f)).inv)
    let assocIso :=
      α_ (eta.app X) (R.map (eta.app X)) (R.map (R.map f))
    let first :=
      eta.app X ◁ (R.mapComp (eta.app X) (R.map f)).hom
    let last :=
      eta.app X ◁ (R.mapComp (eta.app X) (R.map f)).inv
    have hcancel := assocIso.inv_hom_id
    calc
      _ = first ≫ ((assocIso.inv ≫ assocIso.hom) ≫ last) := by
        simp only [first, last, assocIso, Category.assoc]
      _ = first ≫ ((𝟙 _) ≫ last) :=
        congrArg (fun middle => first ≫ (middle ≫ last)) hcancel
      _ = _ := by
        simp only [Category.id_comp]
        rfl
  rw [hpostNorm, hpre]
  simp only [
    leftFactor, rightFactor,
    reverseComponentIso_hom,
    UnitPrecomposition.strongTrans_naturality,
    UnitPrecomposition.strongTrans_app,
    Iso.symm_hom,
    Category.assoc
  ]
  calc
    _ = (eta.naturality (f ≫ eta.app Y)).hom ≫
          eta.app X ◁ R.map₂ (eta.naturality f).hom := by
        rw [hY]
        let lead :=
          ((Pseudofunctor.id B).mapComp f (eta.app Y)).hom ▷
              eta.app (R.obj Y) ≫
            (α_ ((Pseudofunctor.id B).map f)
              ((Pseudofunctor.id B).map (eta.app Y))
              (eta.app (R.obj Y))).hom ≫
              ((Pseudofunctor.id B).map f ◁
                (eta.naturality (eta.app Y)).hom) ≫
                (α_ ((Pseudofunctor.id B).map f)
                  (eta.app Y) (R.map (eta.app Y))).inv ≫
                  ((eta.naturality f).hom ▷ R.map (eta.app Y)) ≫
                    (α_ (eta.app X) (R.map f)
                      (R.map (eta.app Y))).hom ≫
                      (eta.app X ◁
                        (R.mapComp f (eta.app Y)).inv) ≫
                        (eta.app X ◁ R.map₂ (eta.naturality f).hom)
        have hlead :=
          congrArg (fun tail => lead ≫ tail) htail
        have htailRight :
            lead ≫
                ((eta.app X ◁
                    (R.mapComp (eta.app X) (R.map f)).hom) ≫
                  (eta.app X ◁
                    (R.mapComp (eta.app X) (R.map f)).inv)) =
              lead := by
          have hwhisker :
              (eta.app X ◁
                  (R.mapComp (eta.app X) (R.map f)).hom) ≫
                (eta.app X ◁
                  (R.mapComp (eta.app X) (R.map f)).inv) =
                𝟙 _ :=
            (Bicategory.whiskerLeftIso
              (eta.app X)
              (R.mapComp (eta.app X) (R.map f))).hom_inv_id
          have hc :=
            congrArg (fun middle => lead ≫ middle) hwhisker
          simpa only [Category.comp_id] using hc
        have htotal := hlead.trans htailRight
        simpa only [lead, Category.assoc] using htotal
    _ = (Pseudofunctor.id B).map₂ (eta.naturality f).hom ▷
          eta.app (R.obj Y) ≫
        (eta.naturality (eta.app X ≫ R.map f)).hom :=
      (eta.naturality_naturality (eta.naturality f).hom).symm
    _ = _ := by
      rw [hX]
      simp <;> bicategory

end UnitSelfInterchanger

end Generic

#print axioms Generic.UnitSelfInterchanger.reverseNaturality

end

end KUOS.DependentOriginationUnitSelfInterchangerNaturalityV5_74
