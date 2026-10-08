import KUOS.DependentOriginationForwardSwallowtailNativeBoundaryV5_79

namespace KUOS.DependentOriginationForwardMiddleFactorNaturalityV5_80

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftBiadjunctionTriangulatorsV5_58
open KUOS.DependentOriginationExactLiftableActualLiftForwardTriangleModificationV5_52
open KUOS.DependentOriginationActualLiftForwardMapCompGlobalV5_78
open KUOS.DependentOriginationForwardSwallowtailNativeBoundaryV5_79
open KUOS.DependentOriginationStrongTransModificationPostcompositionV5_62
open KUOS.DependentOriginationUnitPostcompositionNativeSourceV5_72.Generic

set_option autoImplicit false
noncomputable section

/-!
# Source middle-factor naturality, preserving the native strict projection v5.80

The v5.79 middle StrongTrans paths agree objectwise. The remaining global
comparison must retain the *actual* non-strict quasi-inverse G compositor.

The forward pseudofunctor F, unlike G, is already a strict pseudofunctor in
v5.42. This gives a concrete, mathematically meaningful cancellation:
the compositor of R = F ; G is precisely the compositor of G on F-mapped
1-morphisms. This is a stated equality of isomorphisms, including both
hom and inv, not an assertion that G is strict.

The factor comparisons below use only the old projected source unit
(v5.52), old restricted target counit (v5.52), native unit
postcomposition (v5.72), and old counit multiplication (v5.76).
They are the small-scale inputs for the v5.79 MiddleNaturalityAgreement,
not a replacement for that yet-unproved global proposition.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- The original F preserves composition strictly: the hom part of
its compositor is literally the identity on the canonical lifted 1-cell. -/
@[simp] theorem strictForward_mapComp_hom
    {X Y Z :
      sourceV578 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)}
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    ((forwardV578 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).mapComp f g).hom =
      𝟙 (((forwardV578 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)).map f) ≫
        ((forwardV578 (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel)).map g)) :=
  rfl

/-- The native R = F ; G compositor is the old G compositor, including
both directions, because *only F* is strict. No strictification of G. -/
theorem roundtrip_mapComp_eq_quasiInverse_mapComp
    {X Y Z :
      sourceV578 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)}
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    (roundtripV578 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).mapComp f g =
    (quasiInverseV578 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).mapComp
      ((forwardV578 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)).map f)
      ((forwardV578 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)).map g) := by
  apply Iso.ext
  change
    (quasiInverseV578 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).map₂
      (((forwardV578 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)).mapComp f g).hom) ≫
      ((quasiInverseV578 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)).mapComp
        ((forwardV578 (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel)).map f)
        ((forwardV578 (W := W) A
          (WorldLabel := WorldLabel)
          (PresentationLabel := PresentationLabel)).map g)).hom = _
  rw [strictForward_mapComp_hom (W := W) A f g,
    PrelaxFunctor.map₂_id, Category.id_comp]

/-- The full native source roundtrip now has a named compositor equality
which can be used in either hom or inv orientations in later proofs. -/
@[simp] theorem roundtrip_mapComp_hom
    {X Y Z :
      sourceV578 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)}
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    ((roundtripV578 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).mapComp f g).hom =
    ((quasiInverseV578 (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).mapComp
      ((forwardV578 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)).map f)
      ((forwardV578 (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)).map g)).hom := by
  rw [roundtrip_mapComp_eq_quasiInverse_mapComp (W := W) A f g]

#print axioms strictForward_mapComp_hom
#print axioms roundtrip_mapComp_eq_quasiInverse_mapComp
#print axioms roundtrip_mapComp_hom

end

end KUOS.DependentOriginationForwardMiddleFactorNaturalityV5_80
