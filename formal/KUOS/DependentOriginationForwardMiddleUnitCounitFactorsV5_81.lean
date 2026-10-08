import KUOS.DependentOriginationForwardMiddleFactorNaturalityV5_80

namespace KUOS.DependentOriginationForwardMiddleUnitCounitFactorsV5_81

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationExactLiftableActualLiftForwardTriangleModificationV5_52
open KUOS.DependentOriginationActualLiftForwardMapCompGlobalV5_78
open KUOS.DependentOriginationForwardSwallowtailNativeBoundaryV5_79
open KUOS.DependentOriginationForwardMiddleFactorNaturalityV5_80
open KUOS.DependentOriginationStrongTransModificationPostcompositionV5_62
open KUOS.DependentOriginationUnitPostcompositionNativeSourceV5_72.Generic
open KUOS.DependentOriginationSourceCounitMultiplicationGlobalInterchangerV5_76.Generic.IncoherentBiadjunctionDatum

set_option autoImplicit false
noncomputable section

/-!
# Compare original unit/counit factors at the native middle boundary v5.81

The v5.79 middle paths have matching objectwise 1-cells, but their global
2-cell naturalities were assembled using two different source presentations.

This file reduces that comparison at the two primitive factors:

* the non-strict G-postcomposition of the old v5.52 projected unit versus
  the native source-roundtrip unit postcomposition of v5.72;
* the non-strict G-postcomposition of the old v5.52 restricted counit versus
  the source counit multiplication of v5.76.

The first step uses the proved v5.80 compositor of R = F ; G. No G
strictness, replacement unit/counit, new coherence assumption or sorry.
-/

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- The existing v5.52 source-unit factor, postcomposed with the
unchanged, possibly non-strict quasi-inverse G. -/
abbrev mappedProjectedUnitV581 :=
  StrongTransPostcomposition.strongTrans
    (quasiInverseV578 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))
    (projectedUnitV578 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))

/-- The same source-unit factor represented via the native roundtrip. -/
abbrev nativeRoundtripUnitV581 :=
  UnitPostcomposition.strongTrans
    (roundtripV578 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))
    (unitV578 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))

/-- Agreement of the unit-factor components before comparing naturality. -/
@[simp] theorem mappedProjectedUnit_app (X :
    sourceV578 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) :
    (mappedProjectedUnitV581 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).app X =
    (nativeRoundtripUnitV581 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).app X :=
  rfl

/-- The old G-postcomposed unit's naturality is the native R-unit
naturality. The strictness used here belongs to F alone. -/
theorem mappedProjectedUnit_naturality_hom
    {X Y : sourceV578 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)}
    (f : X ⟶ Y) :
    ((mappedProjectedUnitV581 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).naturality f).hom =
    ((nativeRoundtripUnitV581 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).naturality f).hom := by
  simp only [mappedProjectedUnitV581, nativeRoundtripUnitV581,
    StrongTransPostcomposition.strongTrans_naturality,
    UnitPostcomposition.strongTrans_naturality,
    StrongTransPostcomposition.naturalityIso_hom,
    UnitPostcomposition.naturalityIso_hom,
    actualLiftProjectedSourceUnit_naturality,
    roundtrip_mapComp_eq_quasiInverse_mapComp,
    PrelaxFunctor.map₂Iso_hom]
  all_goals rfl

/-- The original v5.52 target-counit factor, postcomposed with G. -/
abbrev mappedRestrictedCounitV581 :=
  StrongTransPostcomposition.strongTrans
    (quasiInverseV578 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))
    (restrictedCounitV578 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))

/-- The counit factor's naturality is literally the old counit
naturality evaluated at F.map f, preserving the v5.60 comparison. -/
theorem mappedRestrictedCounit_naturality_hom
    {X Y : sourceV578 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)}
    (f : X ⟶ Y) :
    ((mappedRestrictedCounitV581 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).naturality f).hom =
    ((sourceCounitMultiplication
      (actualLiftDatumV579 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))).naturality f).hom := by
  rfl

#print axioms mappedProjectedUnit_app
#print axioms mappedProjectedUnit_naturality_hom
#print axioms mappedRestrictedCounit_naturality_hom

end

end KUOS.DependentOriginationForwardMiddleUnitCounitFactorsV5_81
