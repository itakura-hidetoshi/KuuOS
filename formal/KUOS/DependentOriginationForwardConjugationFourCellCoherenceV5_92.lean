import KUOS.DependentOriginationForwardReverseContractionCancellationV5_91

namespace KUOS.DependentOriginationForwardConjugationFourCellCoherenceV5_92

open CategoryTheory
open scoped CategoryTheory.Bicategory
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePrelaxV5_46
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftTriangleComponentsV5_51

set_option autoImplicit false
set_option maxHeartbeats 600000
noncomputable section

/-!
# The genuine conjugation four-cell and the remaining F3 law (v5.92)

The original forward-swallowtail interchanger is constructed from the
fixed source unit, G.mapComp, and unit self-naturality.  In the actual
KuuOS implementation, G is the original conjugation pseudofunctor of
two chosen bicategorical equivalences.

We extract the four-cell before using the actual-lift wrappers, keeping
both *different* equivalences e and d, their original unit/counit,
and the non-strict identity comparison of the conjugation functor.

The intended theorem is a genuine bicategorical equation, rather than
another definition of the swallowtail proposition.  No arbitrary
coherence data are chosen.
-/

universe uB vB wB

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {a b x : B}

/-- The original four constituent 2-isomorphisms, with
  * e at the target object F(X);
  * d at the target object F(G(F(X))).

No assertion that these equivalences are equal is made. -/
def conjugationForwardFourCell
    (e : Bicategory.Equivalence a x)
    (d : Bicategory.Equivalence b a) :
    e.inv ≫ (Conjugation.homFunctor e e).obj (e.inv ≫ e.hom) ≅
      e.inv ≫ (d.inv ≫ (Conjugation.homFunctor d e).obj e.hom) :=
  Bicategory.whiskerLeftIso e.inv
      (Conjugation.compIso e d e e.inv e.hom) ≪≫
    (α_ e.inv
      ((Conjugation.homFunctor e d).obj e.inv)
      ((Conjugation.homFunctor d e).obj e.hom)).symm ≪≫
    Bicategory.whiskerRightIso
      (ConjugationUnit.naturalityIso e d e.inv).symm
      ((Conjugation.homFunctor d e).obj e.hom) ≪≫
    (α_ e.inv d.inv ((Conjugation.homFunctor d e).obj e.hom))

/-- Generic source-side coherence: four-cell followed by the genuine
reverse triangle contraction equals the mapped original forward counit
and original G.mapId comparison.  This is the remaining mathematical
content of F3, without strictifying the quasi-inverse. -/
theorem conjugationForwardFourCell_cancelled
    (e : Bicategory.Equivalence a x)
    (d : Bicategory.Equivalence b a) :
    (conjugationForwardFourCell e d).hom ≫
        e.inv ◁ (ConjugationTriangle.quasiInverseIso e d).hom =
      e.inv ◁
        ((Conjugation.homFunctor e e).map e.counit.hom ≫
          (Conjugation.idIso e).hom) := by
  let n := ConjugationUnit.naturalityIso e e (e.inv ≫ e.hom)
  let sigma := (conjugationForwardFourCell e d).hom
  let cG := (ConjugationTriangle.quasiInverseIso e d).hom
  let a0 := (Conjugation.homFunctor e e).map e.counit.hom ≫
    (Conjugation.idIso e).hom
  change sigma ≫ e.inv ◁ cG = e.inv ◁ a0
  -- This is the same right triangle used in v5.56, now solved for the
  -- original counit's right whiskering. No new triangle is assumed.
  have htriangle :
      (α_ e.inv e.hom e.inv).hom ≫ e.inv ◁ e.unit.inv =
        e.counit.hom ▷ e.inv ≫
          (λ_ e.inv).hom ≫ (ρ_ e.inv).inv := by
    have h := KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleModificationV5_56.BackwardTriangleCoherence.counit_right e
    have h' := congrArg
      (fun t => (α_ e.inv e.hom e.inv).hom ≫ t ≫ (ρ_ e.inv).inv) h
    simpa only [Category.assoc, Iso.hom_inv_id_assoc,
      Iso.inv_hom_id_assoc, Category.comp_id] using h'.symm
  -- The three coherence equations below were proved for the genuine
  -- conjugation functor and the original selected object equivalences.
  have hcomposition := ConjugationUnit.comp e d e e.inv e.hom
  have hnatural := ConjugationUnit.naturality e e e.counit.hom
  have hidentity := ConjugationUnit.id e
  have hpre :
      n.hom ≫ (sigma ≫ e.inv ◁ cG) =
        n.hom ≫ e.inv ◁ a0 := by
    calc
      _ = (α_ e.inv e.hom e.inv).hom ≫ e.inv ◁ e.unit.inv := by
        dsimp [n, sigma, cG, conjugationForwardFourCell,
          ConjugationTriangle.quasiInverseIso]
        simp only [Iso.trans_hom, Iso.symm_hom,
          Bicategory.whiskerLeftIso_hom,
          Bicategory.whiskerRightIso_hom,
          Bicategory.whiskerLeft_comp]
        repeat rw [← Category.assoc]
        rw [hcomposition]
        simp only [Category.assoc, Iso.hom_inv_id_assoc,
          Iso.inv_hom_id_assoc, Bicategory.whiskerLeft_comp,
          Bicategory.comp_whiskerRight,
          Bicategory.hom_inv_whiskerLeft,
          Bicategory.inv_hom_whiskerLeft,
          Bicategory.hom_inv_whiskerRight,
          Bicategory.inv_hom_whiskerRight,
          Category.id_comp, Category.comp_id]
        bicategory
      _ = (e.counit.hom ▷ e.inv) ≫
            (λ_ e.inv).hom ≫ (ρ_ e.inv).inv := htriangle
      _ = _ := by
        dsimp [n, a0]
        rw [Bicategory.whiskerLeft_comp]
        rw [← Category.assoc]
        rw [← hnatural]
        rw [Category.assoc]
        rw [hidentity]
        simp only [Category.assoc, Bicategory.id_whiskerRight,
          Category.id_comp]
  have hp := congrArg (fun t => n.inv ≫ t) hpre
  simpa only [← Category.assoc, Iso.inv_hom_id, Category.id_comp] using hp

#print axioms conjugationForwardFourCell
#print axioms conjugationForwardFourCell_cancelled

end

end KUOS.DependentOriginationForwardConjugationFourCellCoherenceV5_92
