import KUOS.DependentOriginationUnitSelfInterchangerNaturalityV5_74
import KUOS.DependentOriginationForwardSwallowtailModificationObstructionV5_70

namespace KUOS.DependentOriginationActualLiftUnitSelfGlobalInterchangerV5_75

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationExactLiftableActualLiftIncoherentBiadjunctionV5_59.Generic
open KUOS.DependentOriginationBiadjunctionTriangulatorHorizontalPastesV5_64.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationUnitSelfNaturalityCoreV5_67.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationUnitSelfInterchangerBoundaryV5_73.Generic.UnitSelfInterchanger
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationForwardSwallowtailPredicateV5_65
open KUOS.DependentOriginationUnitSelfNaturalityCoreV5_67
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6

set_option autoImplicit false

noncomputable section

/-!
# Actual-lift global unit self-interchanger v5.75

The v5.74 naturality theorem packages the eta/eta comparison as a genuine
invertible modification for every pseudofunctor R and unit eta : Id ==> R.
Here we specialize that proof to the unchanged actual-lift biadjunction
datum, retaining its native, possibly non-strict, source roundtrip.

The middle component is definitionally the inverse v5.67 self-naturality
core appearing in the four-cell v5.68 swallowtail paste. This is a typed
global bridge, not yet naturality of the complete v5.68 four-cell paste,
nor the v5.65 swallowtail equation.
-/

namespace Generic

universe uB vB wB uC vC wC

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]

namespace IncoherentBiadjunctionDatum

variable (D : IncoherentBiadjunctionDatum B C)

/-- The v5.73 exact naturality proposition instantiated on the native
source roundtrip of an arbitrary stored biadjunction datum. -/
theorem unitSelfGlobalNaturality :
    KUOS.DependentOriginationUnitSelfInterchangerBoundaryV5_73.Generic.UnitSelfInterchanger.Naturality
      (sourceRoundtrip D) D.base.unit :=
  KUOS.DependentOriginationUnitSelfInterchangerNaturalityV5_74.Generic.UnitSelfInterchanger.naturality
    (sourceRoundtrip D) D.base.unit

/-- A true global invertible modification between the two eta/eta paths,
with no additional coherence assumption on the stored biadjunction. -/
def unitSelfGlobalComparisonIso :
    @CategoryTheory.Iso
      (Pseudofunctor.StrongTrans
        (Pseudofunctor.id B)
        (Pseudofunctor.comp (sourceRoundtrip D) (sourceRoundtrip D)))
      (Pseudofunctor.StrongTrans.homCategory
        (B := B) (C := B)
        (F := Pseudofunctor.id B)
        (G := Pseudofunctor.comp (sourceRoundtrip D) (sourceRoundtrip D)))
      (postPath (sourceRoundtrip D) D.base.unit)
      (prePath (sourceRoundtrip D) D.base.unit) :=
  KUOS.DependentOriginationUnitSelfInterchangerNaturalityV5_74.Generic.UnitSelfInterchanger.comparisonIso
    (sourceRoundtrip D) D.base.unit

/-! Mathlib scopes the StrongTrans hom-category instance.  The universe
of its 2-cells is not an output parameter, so pin the exact category before
elaborating Iso projections in the following component theorems. -/
local instance unitSelfGlobalHomCategory :
    Category
      (Pseudofunctor.StrongTrans
        (Pseudofunctor.id B)
        (Pseudofunctor.comp (sourceRoundtrip D) (sourceRoundtrip D))) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := B) (C := B)
    (F := Pseudofunctor.id B)
    (G := Pseudofunctor.comp (sourceRoundtrip D) (sourceRoundtrip D))

/-- The global modification's component is literally the v5.67 core,
reversed in the direction used by the forward swallowtail. -/
@[simp] theorem unitSelfGlobalComparisonIso_hom_app (X : B) :
    (unitSelfGlobalComparisonIso D).hom.as.app X =
      (unitSelfNaturalityIso D X).inv :=
  rfl

@[simp] theorem unitSelfGlobalComparisonIso_inv_app (X : B) :
    (unitSelfGlobalComparisonIso D).inv.as.app X =
      (unitSelfNaturalityIso D X).hom :=
  rfl

end IncoherentBiadjunctionDatum

end Generic

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- Specialization to the exact unchanged actual-lift F, G and source unit. -/
def actualLiftUnitSelfGlobalComparisonIso :=
  Generic.IncoherentBiadjunctionDatum.unitSelfGlobalComparisonIso
    (actualLiftForwardSwallowtailDatum
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))

/-! The six universe levels of ActualLiftSource are explicit here, as
in v5.70.  A hom-category instance inferred only from the abbreviated
comparison may leave the 2-morphism universe underconstrained. -/
local instance actualLiftUnitSelfHomCategory :
    Category
      (Pseudofunctor.StrongTrans
        (Pseudofunctor.id
          (ActualLiftSource.{u, v, uH, vH, uW, uP}
            (W := W) A WorldLabel PresentationLabel))
        (Pseudofunctor.comp
          (sourceRoundtrip
            (actualLiftForwardSwallowtailDatum
              (W := W) A
              (WorldLabel := WorldLabel)
              (PresentationLabel := PresentationLabel)))
          (sourceRoundtrip
            (actualLiftForwardSwallowtailDatum
              (W := W) A
              (WorldLabel := WorldLabel)
              (PresentationLabel := PresentationLabel))))) :=
  Pseudofunctor.StrongTrans.homCategory
    (B :=
      ActualLiftSource.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)
    (C :=
      ActualLiftSource.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)
    (F := Pseudofunctor.id _)
    (G := _)

/-- The same component used by the v5.68 four-cell paste, now supplied by
a globally natural modification instead of only pointwise isomorphisms. -/
@[simp] theorem actualLiftUnitSelfGlobalComparisonIso_hom_app
    (X :
      ActualLiftSource.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    (actualLiftUnitSelfGlobalComparisonIso
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).hom.as.app X =
      (actualLiftUnitSelfNaturalityIso
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)
        X).inv :=
  rfl

#print axioms Generic.IncoherentBiadjunctionDatum.unitSelfGlobalNaturality
#print axioms Generic.IncoherentBiadjunctionDatum.unitSelfGlobalComparisonIso
#print axioms Generic.IncoherentBiadjunctionDatum.unitSelfGlobalComparisonIso_hom_app
#print axioms actualLiftUnitSelfGlobalComparisonIso
#print axioms actualLiftUnitSelfGlobalComparisonIso_hom_app

end

end KUOS.DependentOriginationActualLiftUnitSelfGlobalInterchangerV5_75
