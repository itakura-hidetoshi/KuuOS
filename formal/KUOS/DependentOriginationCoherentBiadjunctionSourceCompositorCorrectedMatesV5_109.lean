import KUOS.DependentOriginationCoherentBiadjunctionNativeMatesTwoCellNaturalityV5_108

namespace KUOS.DependentOriginationCoherentBiadjunctionSourceCompositorCorrectedMatesV5_109

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftOneCellV5_40
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePrelaxV5_46
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationCoherentBiadjunctionMathlibAdjunctionBridgeV5_102
open KUOS.DependentOriginationCoherentBiadjunctionNativeMatesV5_104
open KUOS.DependentOriginationCoherentBiadjunctionNativeMatesCompositionV5_105
open KUOS.DependentOriginationCoherentBiadjunctionNativeMatesIdentityV5_107.Generic

set_option autoImplicit false
noncomputable section

/-!
# F13 / v5.109: source compositor-corrected native right-mate composition

F9 proves the source naturality_comp equality only after retaining the
original non-strict source compositor on the LEFT-adjoint side.
F10 exposes the corresponding correction on the RIGHT for the TARGET.
F11 gives the generic mateEquiv_postcompose law needed to do the same
for the original SOURCE unit without reselecting its adjunction.

Here the original source mapComp cell acts AFTER the mate of (f ≫ g),
by right whiskering with the unchanged chosen right-adjoint leg at Z.
This is a typed pasting equality, not a strictification of R_L.

The symm mate equivalence also returns the original left-adjoint
vertical paste, so the corrected right-side equation loses no data.
-/

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}
variable {X Y Z : ActualLiftSource.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel}

/-- Right whiskering of the ORIGINAL, non-strict R_L.mapComp
2-cell by the ORIGINAL right-adjoint leg of the unit at Z. -/
def actualLiftSourceUnitRightMapCompWhisker
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    (((actualLiftSourceRoundtrip (W := W) A).map (f ≫ g)) ≫
      (actualLiftSourceNativeAdjHom (W := W) A Z).r) ⟶
      ((((actualLiftSourceRoundtrip (W := W) A).map f) ≫
        ((actualLiftSourceRoundtrip (W := W) A).map g)) ≫
          (actualLiftSourceNativeAdjHom (W := W) A Z).r) :=
  ((actualLiftSourceRoundtrip (W := W) A).mapComp f g).hom ▷
    (actualLiftSourceNativeAdjHom (W := W) A Z).r

/-- The source's completely typed compositor-corrected RIGHT pasting.
Unlike the target correction (F10), the source comparison follows
the unmodified right mate of the composite. -/
def actualLiftSourceUnitRightCorrectedVComp
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    (actualLiftSourceNativeAdjHom (W := W) A X).r ≫ (f ≫ g) ⟶
      ((((actualLiftSourceRoundtrip (W := W) A).map f) ≫
        ((actualLiftSourceRoundtrip (W := W) A).map g)) ≫
          (actualLiftSourceNativeAdjHom (W := W) A Z).r) :=
  actualLiftSourceUnitRightMate (W := W) A (f ≫ g) ≫
    actualLiftSourceUnitRightMapCompWhisker (W := W) A f g

/-- F13: the mate of the unchanged composite source naturality,
followed by the ORIGINAL R_L.mapComp right whisker, is exactly
the vertical paste of the two unchanged source right mates. -/
theorem actualLiftSourceUnitRightCorrectedVComp_eq_vcomp
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    actualLiftSourceUnitRightCorrectedVComp (W := W) A f g =
      actualLiftSourceUnitMateVComp (W := W) A f g := by
  calc
    _ =
        (Bicategory.mateEquiv
          (actualLiftSourceNativeAdjHom (W := W) A X).adj
          (actualLiftSourceNativeAdjHom (W := W) A Z).adj)
            (((actualLiftSourceRoundtripUnit (W := W) A).naturality (f ≫ g)).hom) ≫
          ((actualLiftSourceRoundtrip (W := W) A).mapComp f g).hom ▷
            (actualLiftSourceNativeAdjHom (W := W) A Z).r := rfl
    _ =
        (Bicategory.mateEquiv
          (actualLiftSourceNativeAdjHom (W := W) A X).adj
          (actualLiftSourceNativeAdjHom (W := W) A Z).adj)
          (((actualLiftSourceRoundtripUnit (W := W) A).naturality (f ≫ g)).hom ≫
            (actualLiftSourceRoundtripUnit (W := W) A).app X ◁
              ((actualLiftSourceRoundtrip (W := W) A).mapComp f g).hom) := by
      exact (Generic.mateEquiv_postcompose
        (actualLiftSourceNativeAdjHom (W := W) A X).adj
        (actualLiftSourceNativeAdjHom (W := W) A Z).adj
        ((actualLiftSourceRoundtripUnit (W := W) A).naturality (f ≫ g)).hom
        ((actualLiftSourceRoundtrip (W := W) A).mapComp f g).hom).symm
    _ = _ := actualLiftSourceUnitMateComp_native (W := W) A f g

/-- Unmating the original compositor-corrected right-side source
pasting recovers the LEFT vertical mate paste from v5.105 exactly. -/
theorem actualLiftSourceUnitRightCorrectedVComp_unmate
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    (Bicategory.mateEquiv
      (actualLiftSourceNativeAdjHom (W := W) A X).adj
      (actualLiftSourceNativeAdjHom (W := W) A Z).adj).symm
        (actualLiftSourceUnitRightCorrectedVComp (W := W) A f g) =
      Bicategory.leftAdjointSquare.vcomp
        ((actualLiftSourceRoundtripUnit (W := W) A).naturality f).hom
        ((actualLiftSourceRoundtripUnit (W := W) A).naturality g).hom := by
  rw [actualLiftSourceUnitRightCorrectedVComp_eq_vcomp]
  rw [← actualLiftSourceUnitMateVComp_eq]
  exact Equiv.symm_apply_apply _ _

#print axioms actualLiftSourceUnitRightMapCompWhisker
#print axioms actualLiftSourceUnitRightCorrectedVComp
#print axioms actualLiftSourceUnitRightCorrectedVComp_eq_vcomp
#print axioms actualLiftSourceUnitRightCorrectedVComp_unmate

end

end KUOS.DependentOriginationCoherentBiadjunctionSourceCompositorCorrectedMatesV5_109
