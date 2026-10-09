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
  dsimp [conjugationForwardFourCell, ConjugationTriangle.quasiInverseIso,
    ConjugationUnit.naturalityIso, Conjugation.compIso,
    Conjugation.homFunctor, Conjugation.idIso]
  bicategory

#print axioms conjugationForwardFourCell
#print axioms conjugationForwardFourCell_cancelled

end

end KUOS.DependentOriginationForwardConjugationFourCellCoherenceV5_92
