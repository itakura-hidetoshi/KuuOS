import KUOS.DependentOriginationActualLiftUnitSelfGlobalInterchangerV5_75

namespace KUOS.DependentOriginationSourceCounitMultiplicationGlobalInterchangerV5_76

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionV5_59.Generic
open KUOS.DependentOriginationBiadjunctionTriangulatorHorizontalPastesV5_64.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationUnitSelfInterchangerBoundaryV5_73.Generic.UnitSelfInterchanger
open KUOS.DependentOriginationActualLiftUnitSelfGlobalInterchangerV5_75.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationUnitSelfNaturalityCoreV5_67.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationStrongTransModificationPrecompositionV5_61
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleCounitV5_54

set_option autoImplicit false

noncomputable section

/-!
# Source counit multiplication and global eta/eta whiskering v5.76

Let R = F ; G and let eta : Id => R, eps : G ; F => Id be the
unchanged unit and counit of an incoherent biadjunction.

The v5.68 four-cell swallowtail comparison contains the middle step
  (eta.naturality (eta_X)).inv ▷ G.map (eps_(F X)).
v5.75 proves the eta/eta comparison is globally natural. To transport that
proof through the counit, the right whisker must itself be a *native*
StrongTrans (R ; R) => R; a mere family of components would not suffice.

We construct this factor by precomposing v5.60's non-strict counit
factor with F, then using the v5.54 proved TripleComparison on the
source mapId/mapComp. No strictification or new F/G/eta/eps data occur.

Whiskering the v5.75 invertible modification on the right now gives a
global invertible modification with the exact middle component of v5.68.
The two surrounding associators and leading mapComp still have to be
pasted at modification level to discharge v5.70. The v5.65 swallowtail
equality remains a separate, unproved obligation.
-/

namespace Generic

universe uB vB wB uC vC wC

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]

namespace IncoherentBiadjunctionDatum

variable (D : IncoherentBiadjunctionDatum B C)

/-- The counit factor before reassociating the fourfold source
F ; (G ; (F ; G)) into (F ; G) ; (F ; G). -/
private def sourceCounitRaw :
    Pseudofunctor.StrongTrans
      (Pseudofunctor.comp D.base.whitehead.forward
        (Pseudofunctor.comp D.base.quasiInverse (sourceRoundtrip D)))
      (sourceRoundtrip D) :=
  StrongTransPrecomposition.strongTrans
    D.base.whitehead.forward
    (KUOS.DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionHorizontalWhiskeringV5_60.Generic.IncoherentBiadjunctionDatum.quasiInverseCounitFactor D)

/-- Native multiplication (F ; G) ; (F ; G) => F ; G induced by the
*existing* counit eps. The source's actual mapId and mapComp are kept,
rather than silently identifying the two pseudofunctor bracketings. -/
def sourceCounitMultiplication :
    Pseudofunctor.StrongTrans
      (Pseudofunctor.comp (sourceRoundtrip D) (sourceRoundtrip D))
      (sourceRoundtrip D) where
  app X := (sourceCounitRaw D).app X
  naturality f := (sourceCounitRaw D).naturality f
  naturality_naturality theta :=
    (sourceCounitRaw D).naturality_naturality theta
  naturality_id X := by
    rw [TripleComparison.mapId_hom
      D.base.whitehead.forward D.base.quasiInverse (sourceRoundtrip D) X]
    exact (sourceCounitRaw D).naturality_id X
  naturality_comp f g := by
    rw [TripleComparison.mapComp_hom
      D.base.whitehead.forward D.base.quasiInverse (sourceRoundtrip D) f g]
    exact (sourceCounitRaw D).naturality_comp f g

@[simp] theorem sourceCounitMultiplication_app (X : B) :
    (sourceCounitMultiplication D).app X =
      D.base.quasiInverse.map
        (D.base.counit.app (D.base.whitehead.forward.obj X)) :=
  rfl

local instance sourceUnitSelfHomCategory :
    Category
      (Pseudofunctor.StrongTrans
        (Pseudofunctor.id B)
        (Pseudofunctor.comp (sourceRoundtrip D) (sourceRoundtrip D))) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := B) (C := B)
    (F := Pseudofunctor.id B)
    (G := Pseudofunctor.comp (sourceRoundtrip D) (sourceRoundtrip D))

local instance sourceCounitWhiskeredHomCategory :
    Category
      (Pseudofunctor.StrongTrans
        (Pseudofunctor.id B)
        (sourceRoundtrip D)) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := B) (C := B)
    (F := Pseudofunctor.id B)
    (G := sourceRoundtrip D)

/-- The globally natural eta/eta interchanger, right-whiskered by the
original counit multiplication; this is the exact central step of v5.68,
but at the level of native invertible modifications. -/
def unitSelfCounitWhiskeredComparisonIso :
    @CategoryTheory.Iso
      (Pseudofunctor.StrongTrans (Pseudofunctor.id B) (sourceRoundtrip D))
      (Pseudofunctor.StrongTrans.homCategory
        (B := B) (C := B)
        (F := Pseudofunctor.id B) (G := sourceRoundtrip D))
      (Pseudofunctor.StrongTrans.vcomp
        (postPath (sourceRoundtrip D) D.base.unit)
        (sourceCounitMultiplication D))
      (Pseudofunctor.StrongTrans.vcomp
        (prePath (sourceRoundtrip D) D.base.unit)
        (sourceCounitMultiplication D)) :=
  Bicategory.whiskerRightIso (B := Pseudofunctor B B)
    (unitSelfGlobalComparisonIso D)
    (sourceCounitMultiplication D)

/-- The component of the global whiskering is the very same inverse
eta/eta core, right-whiskered by G(eps_(F X)), as in the third cell
of the original four-step v5.68 paste. -/
@[simp] theorem unitSelfCounitWhiskeredComparisonIso_hom_app (X : B) :
    (unitSelfCounitWhiskeredComparisonIso D).hom.as.app X =
      (Bicategory.whiskerRightIso
        (unitSelfNaturalityIso D X).symm
        (D.base.quasiInverse.map
          (D.base.counit.app (D.base.whitehead.forward.obj X)))).hom := by
  simp only [unitSelfCounitWhiskeredComparisonIso,
    Bicategory.whiskerRightIso_hom,
    Pseudofunctor.StrongTrans.whiskerRight_as_app,
    unitSelfGlobalComparisonIso_hom_app,
    sourceCounitMultiplication_app,
    Iso.symm_hom]
  rfl

end IncoherentBiadjunctionDatum
end Generic

#print axioms Generic.IncoherentBiadjunctionDatum.sourceCounitMultiplication
#print axioms Generic.IncoherentBiadjunctionDatum.sourceCounitMultiplication_app
#print axioms Generic.IncoherentBiadjunctionDatum.unitSelfCounitWhiskeredComparisonIso
#print axioms Generic.IncoherentBiadjunctionDatum.unitSelfCounitWhiskeredComparisonIso_hom_app

end

end KUOS.DependentOriginationSourceCounitMultiplicationGlobalInterchangerV5_76
