import KUOS.DependentOriginationSourceCounitMultiplicationGlobalInterchangerV5_76

namespace KUOS.DependentOriginationReassociatedSourceCounitInterchangerV5_77

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionV5_59.Generic
open KUOS.DependentOriginationBiadjunctionTriangulatorHorizontalPastesV5_64.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationUnitPostcompositionNativeSourceV5_72.Generic
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInverseTriangleUnitV5_53
open KUOS.DependentOriginationActualLiftUnitSelfGlobalInterchangerV5_75.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationUnitSelfNaturalityCoreV5_67.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationSourceCounitMultiplicationGlobalInterchangerV5_76.Generic.IncoherentBiadjunctionDatum

set_option autoImplicit false

noncomputable section

/-!
# Reassociated source-counit interchanger v5.77

Let R = F ; G, eta : Id_B => R and eps : G ; F => Id_C be the unchanged
incoherent-biadjunction data, and m : R ; R => R the genuine native
counit multiplication from v5.76.

v5.76 provides an invertible modification
  (eta ; post(eta)) ; m  ==  (eta ; pre(eta)) ; m.
Pasting the two *native functor-bicategory associators* on either side
globalizes precisely the last three cells of the v5.68 four-cell paste:
  inverse associator; eta/eta interchanger whiskered by G(eps_FX);
  forward associator.

This is a theorem-bearing structural step, not merely componentwise data.
The leading G.mapComp modification and the exact v5.70 endpoint transport
remain to be proved separately. No swallowtail equation is assumed.
-/

namespace Generic

universe uB vB wB uC vC wC

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]

namespace IncoherentBiadjunctionDatum

variable (D : IncoherentBiadjunctionDatum B C)

/-- The right-associated eta/post-unit/counit path, in the native
StrongTrans hom-category from Id_B to R. -/
def sourcePostCounitPath :
    Pseudofunctor.StrongTrans (Pseudofunctor.id B) (sourceRoundtrip D) :=
  Pseudofunctor.StrongTrans.vcomp D.base.unit
    (Pseudofunctor.StrongTrans.vcomp
      (UnitPostcomposition.strongTrans (sourceRoundtrip D) D.base.unit)
      (sourceCounitMultiplication D))

/-- The right-associated eta/pre-unit/counit path with the same endpoints. -/
def sourcePreCounitPath :
    Pseudofunctor.StrongTrans (Pseudofunctor.id B) (sourceRoundtrip D) :=
  Pseudofunctor.StrongTrans.vcomp D.base.unit
    (Pseudofunctor.StrongTrans.vcomp
      (UnitPrecomposition.strongTrans (sourceRoundtrip D) D.base.unit)
      (sourceCounitMultiplication D))

@[simp] theorem sourcePostCounitPath_app (X : B) :
    (sourcePostCounitPath D).app X =
      D.base.unit.app X ≫
        ((sourceRoundtrip D).map (D.base.unit.app X) ≫
          D.base.quasiInverse.map
            (D.base.counit.app (D.base.whitehead.forward.obj X))) :=
  rfl

@[simp] theorem sourcePreCounitPath_app (X : B) :
    (sourcePreCounitPath D).app X =
      D.base.unit.app X ≫
        (D.base.unit.app ((sourceRoundtrip D).obj X) ≫
          D.base.quasiInverse.map
            (D.base.counit.app (D.base.whitehead.forward.obj X))) :=
  rfl

local instance sourceCounitPathHomCategory :
    Category
      (Pseudofunctor.StrongTrans (Pseudofunctor.id B) (sourceRoundtrip D)) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := B) (C := B)
    (F := Pseudofunctor.id B)
    (G := sourceRoundtrip D)

/-- Globally natural associator / central whiskering / associator paste.
These are the final three stages of the original four-stage construction. -/
def sourceCounitReassociatedInterchangerIso :
    @CategoryTheory.Iso
      (Pseudofunctor.StrongTrans (Pseudofunctor.id B) (sourceRoundtrip D))
      (Pseudofunctor.StrongTrans.homCategory
        (B := B) (C := B)
        (F := Pseudofunctor.id B) (G := sourceRoundtrip D))
      (sourcePostCounitPath D)
      (sourcePreCounitPath D) :=
  (α_
      D.base.unit
      (UnitPostcomposition.strongTrans (sourceRoundtrip D) D.base.unit)
      (sourceCounitMultiplication D)).symm ≪≫
    unitSelfCounitWhiskeredComparisonIso D ≪≫
    (α_
      D.base.unit
      (UnitPrecomposition.strongTrans (sourceRoundtrip D) D.base.unit)
      (sourceCounitMultiplication D))

/-- Exact three-stage pointwise paste in the v5.68 orientation. -/
def sourceCounitReassociatedComponentIso (X : B) :
    (sourcePostCounitPath D).app X ≅
      (sourcePreCounitPath D).app X :=
  (α_
      (D.base.unit.app X)
      ((sourceRoundtrip D).map (D.base.unit.app X))
      (D.base.quasiInverse.map
        (D.base.counit.app (D.base.whitehead.forward.obj X)))).symm ≪≫
    Bicategory.whiskerRightIso
      (unitSelfNaturalityIso D X).symm
      (D.base.quasiInverse.map
        (D.base.counit.app (D.base.whitehead.forward.obj X))) ≪≫
    (α_
      (D.base.unit.app X)
      (D.base.unit.app ((sourceRoundtrip D).obj X))
      (D.base.quasiInverse.map
        (D.base.counit.app (D.base.whitehead.forward.obj X))))

/-- The global modification has literally the v5.68 central three-cell
paste as its component: there is no new 2-cell choice. -/
@[simp] theorem sourceCounitReassociatedInterchangerIso_hom_app (X : B) :
    (sourceCounitReassociatedInterchangerIso D).hom.as.app X =
      (sourceCounitReassociatedComponentIso D X).hom := by
  simp only [sourceCounitReassociatedInterchangerIso,
    sourceCounitReassociatedComponentIso,
    Iso.trans_hom, Iso.symm_hom,
    Pseudofunctor.StrongTrans.associator_inv_as_app,
    Pseudofunctor.StrongTrans.associator_hom_as_app,
    unitSelfCounitWhiskeredComparisonIso_hom_app]
  rfl

end IncoherentBiadjunctionDatum
end Generic

#print axioms Generic.IncoherentBiadjunctionDatum.sourcePostCounitPath
#print axioms Generic.IncoherentBiadjunctionDatum.sourcePreCounitPath
#print axioms Generic.IncoherentBiadjunctionDatum.sourceCounitReassociatedInterchangerIso
#print axioms Generic.IncoherentBiadjunctionDatum.sourceCounitReassociatedComponentIso
#print axioms Generic.IncoherentBiadjunctionDatum.sourceCounitReassociatedInterchangerIso_hom_app

end

end KUOS.DependentOriginationReassociatedSourceCounitInterchangerV5_77
