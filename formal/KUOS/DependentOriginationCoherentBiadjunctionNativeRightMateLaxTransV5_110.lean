import KUOS.DependentOriginationCoherentBiadjunctionSourceCompositorCorrectedMatesV5_109

namespace KUOS.DependentOriginationCoherentBiadjunctionNativeRightMateLaxTransV5_110

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftOneCellV5_40
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePrelaxV5_46
open KUOS.DependentOriginationExactLiftableActualLiftQuasiInversePseudofunctorV5_48
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationCoherentBiadjunctionMathlibAdjunctionBridgeV5_102
open KUOS.DependentOriginationCoherentBiadjunctionNativeMatesV5_104
open KUOS.DependentOriginationCoherentBiadjunctionNativeMatesCompositionV5_105
open KUOS.DependentOriginationCoherentBiadjunctionTargetCompositorCorrectedMatesV5_106
open KUOS.DependentOriginationCoherentBiadjunctionNativeMatesIdentityV5_107
open KUOS.DependentOriginationCoherentBiadjunctionNativeMatesTwoCellNaturalityV5_108
open KUOS.DependentOriginationCoherentBiadjunctionSourceCompositorCorrectedMatesV5_109

set_option autoImplicit false
noncomputable section

/-!
# F14 / v5.110: Native mathlib lax transformations of ORIGINAL right mates

The original actual-lift source η : Id_L ⇒ R_L and target
ε : R_E ⇒ Id_E are strong transformations. Their original
objectwise right adjoints need NOT themselves carry a strong
transformation: bicategorical mates of invertible 2-cells are not
automatically invertible.

The certified correct target is instead `Oplax.LaxTrans`:
  source: R_L.toOplax ⇒ Id_L.toOplax, components r_X,
  target: Id_E.toOplax ⇒ R_E.toOplax, components r_X.

F11 supplies the exact (non-strict) mapId condition, F12 the
arbitrary-2-cell naturality condition, and F10/F13 the native
mapComp condition, with all original comparison cells intact.
This creates new coherent structures, not new axioms, functors,
objectwise adjunctions, eta/epsilon, or strictifications.
-/

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- The original source unit's chosen right adjoints and native mates
form a genuine mathlib lax natural transformation R_L ⇒ Id_L.
Every required coherence field is discharged by the previous Lean
theorems on the exact original η, not by redefining its components. -/
def actualLiftSourceRightMateLaxTrans :
    Oplax.LaxTrans
      (actualLiftSourceRoundtrip (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).toOplax
      (Pseudofunctor.id
        (ActualLiftSource.{u, v, uH, vH, uW, uP}
          (W := W) A WorldLabel PresentationLabel)).toOplax where
  app X := (actualLiftSourceNativeAdjHom (W := W) A X).r
  naturality {_ _} f := actualLiftSourceUnitRightMate (W := W) A f
  naturality_naturality {X Y} {f g} θ := by
    exact (actualLiftSourceUnitRightMate_naturality₂_explicit (W := W) A θ).symm
  naturality_id X := by
    simpa only [Bicategory.whiskerLeft_id, Category.id_comp] using
      (actualLiftSourceUnitRightMate_id_mapId (W := W) A X)
  naturality_comp {X Y Z} f g := by
    have h := actualLiftSourceUnitRightCorrectedVComp_eq_vcomp (W := W) A f g
    simpa only [actualLiftSourceUnitRightCorrectedVComp,
      actualLiftSourceUnitRightMapCompWhisker, actualLiftSourceUnitMateVComp,
      Bicategory.rightAdjointSquare.vcomp, Bicategory.whiskerLeft_id,
      Category.id_comp] using h

/-- The original target counit's chosen right adjoints and native
mates form a mathlib lax natural transformation Id_E ⇒ R_E.
In particular, this retains the genuine non-strict R_E.mapComp
on the LEFT of the native right-mate vertical paste. -/
def actualLiftTargetRightMateLaxTrans :
    Oplax.LaxTrans
      (Pseudofunctor.id
        (ActualLiftTarget.{u, v, uH, vH, uW, uP}
          (W := W) A WorldLabel PresentationLabel)).toOplax
      (actualLiftTargetRoundtrip (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)).toOplax where
  app X := (actualLiftTargetNativeAdjHom (W := W) A X).r
  naturality {_ _} f := actualLiftTargetCounitRightMate (W := W) A f
  naturality_naturality {X Y} {f g} θ := by
    exact (actualLiftTargetCounitRightMate_naturality₂_explicit (W := W) A θ).symm
  naturality_id X := by
    simpa only [Bicategory.id_whiskerRight, Category.comp_id] using
      (actualLiftTargetCounitRightMate_id_mapId (W := W) A X)
  naturality_comp {X Y Z} f g := by
    let eX := actualLiftTargetNativeAdjHom (W := W) A X
    let eZ := actualLiftTargetNativeAdjHom (W := W) A Z
    let eps := actualLiftTargetRoundtripCounit (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
    have hRight :
        actualLiftTargetCounitRightMate (W := W) A (f ≫ g) ≫
            𝟙 (f ≫ g) ▷ eZ.r =
          actualLiftTargetCounitRightCorrectedVComp (W := W) A f g := by
      calc
        _ = (Bicategory.mateEquiv eX.adj eZ.adj)
            ((eps.naturality (f ≫ g)).hom ≫ eps.app X ◁ 𝟙 (f ≫ g)) := by
          exact (KUOS.DependentOriginationCoherentBiadjunctionNativeMatesIdentityV5_107.Generic.mateEquiv_postcompose
            eX.adj eZ.adj
            ((eps.naturality (f ≫ g)).hom) (𝟙 (f ≫ g))).symm
        _ = _ := actualLiftTargetCounitMateComp_correctedRight (W := W) A f g
    simpa only [actualLiftTargetCounitRightCorrectedVComp,
      actualLiftTargetCounitRightMapCompWhisker, actualLiftTargetCounitMateVComp,
      Bicategory.rightAdjointSquare.vcomp] using hRight

#print axioms actualLiftSourceRightMateLaxTrans
#print axioms actualLiftTargetRightMateLaxTrans

end

end KUOS.DependentOriginationCoherentBiadjunctionNativeRightMateLaxTransV5_110
