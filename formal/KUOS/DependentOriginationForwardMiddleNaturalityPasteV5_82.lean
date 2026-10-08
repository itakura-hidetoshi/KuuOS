import KUOS.DependentOriginationForwardMiddleUnitCounitFactorsV5_81

namespace KUOS.DependentOriginationForwardMiddleNaturalityPasteV5_82

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationActualLiftForwardMapCompGlobalV5_78
open KUOS.DependentOriginationForwardSwallowtailNativeBoundaryV5_79
open KUOS.DependentOriginationForwardMiddleUnitCounitFactorsV5_81
open KUOS.DependentOriginationSourceCounitMultiplicationGlobalInterchangerV5_76.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationReassociatedSourceCounitInterchangerV5_77.Generic.IncoherentBiadjunctionDatum

set_option autoImplicit false
noncomputable section

/-!
# Reassemble the exact middle naturality paste v5.82

v5.81 compares the unit and counit factor naturalities separately.
Their two vertical composites are genuine StrongTrans R => R, with the same
native source and target pseudofunctors, unlike the individual factors.
Use the pinned mathlib StrongTrans composition naturality and the v5.79
extensionality theorem on this *small* boundary, then left compose with eta
without unfolding the complete actual-lift record.

This aims to close the exact v5.79 MiddleNaturalityAgreement, not the
unrelated v5.65 swallowtail equation. No added F/G/eta/eps data, axioms
or strictification.
-/

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- The separately G-postcomposed old v5.52 unit/counit factors. -/
abbrev mappedMiddleV582 :=
  Pseudofunctor.StrongTrans.vcomp
    (mappedProjectedUnitV581 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))
    (mappedRestrictedCounitV581 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))

/-- The v5.72 post-unit and v5.76 counit multiplication factorization. -/
abbrev nativeMiddleV582 :=
  Pseudofunctor.StrongTrans.vcomp
    (nativeRoundtripUnitV581 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel))
    (sourceCounitMultiplication
      (actualLiftDatumV579 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)))

/-- The two native middle factor composites have exactly the same
object component, without changing either pseudofunctor's coherence. -/
@[simp] theorem middleFactors_app (X :
    sourceV578 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)) :
    (mappedMiddleV582 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).app X =
    (nativeMiddleV582 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).app X :=
  rfl

/-- The two middle naturality 2-cells agree because the original
unit and counit factor naturalities agree. -/
theorem middleFactors_naturality_hom
    {X Y : sourceV578 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)}
    (f : X ⟶ Y) :
    ((mappedMiddleV582 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).naturality f).hom =
    ((nativeMiddleV582 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).naturality f).hom := by
  have hMapped :=
    Pseudofunctor.StrongTrans.categoryStruct_comp_naturality_hom
      (mappedProjectedUnitV581 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
      (mappedRestrictedCounitV581 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)) f
  change
    ((Pseudofunctor.StrongTrans.vcomp
      (mappedProjectedUnitV581 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
      (mappedRestrictedCounitV581 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))).naturality f).hom = _ at hMapped
  have hNative :=
    Pseudofunctor.StrongTrans.categoryStruct_comp_naturality_hom
      (nativeRoundtripUnitV581 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
      (sourceCounitMultiplication
        (actualLiftDatumV579 (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel))) f
  change
    ((Pseudofunctor.StrongTrans.vcomp
      (nativeRoundtripUnitV581 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
      (sourceCounitMultiplication
        (actualLiftDatumV579 (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel)))).naturality f).hom = _ at hNative
  rw [hMapped, hNative]
  simp only [mappedProjectedUnit_naturality_hom,
    mappedRestrictedCounit_naturality_hom, mappedProjectedUnit_app]

/-- Equality of the two native R => R middle transformations, using
both the original app-fields and original 2-isomorphism naturality. -/
theorem middleFactors_eq :
    mappedMiddleV582 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) =
    nativeMiddleV582 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) := by
  apply KUOS.DependentOriginationForwardSwallowtailNativeBoundaryV5_79.Generic.strongTrans_eq_of_app_and_naturality
  · intro X
    exact middleFactors_app (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) X
  · intro X Y f
    exact heq_of_eq (middleFactors_naturality_hom (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) f)

/-- The original v5.79 middle boundary is the unit vertically composed
with these two equal R => R factors. -/
theorem middleStrongTrans_eq :
    targetMapCompPathV578 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) =
    sourcePostCounitPath
      (actualLiftDatumV579 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)) := by
  change
    Pseudofunctor.StrongTrans.vcomp
      (unitV578 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
      (mappedMiddleV582 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)) =
    Pseudofunctor.StrongTrans.vcomp
      (unitV578 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
      (nativeMiddleV582 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
  rw [middleFactors_eq (W := W) A]

/-- Discharge the exact v5.79 naturality predicate from the unchanged
natural transformations, without selecting any additional coherence cell. -/
theorem actualLiftMiddleNaturalityAgreement :
    MiddleNaturalityAgreement (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel) := by
  intro X Y f
  rw [middleStrongTrans_eq (W := W) A
    (WorldLabel := WorldLabel)
    (PresentationLabel := PresentationLabel)]

#print axioms middleFactors_app
#print axioms middleFactors_naturality_hom
#print axioms middleFactors_eq
#print axioms middleStrongTrans_eq
#print axioms actualLiftMiddleNaturalityAgreement

end

end KUOS.DependentOriginationForwardMiddleNaturalityPasteV5_82
