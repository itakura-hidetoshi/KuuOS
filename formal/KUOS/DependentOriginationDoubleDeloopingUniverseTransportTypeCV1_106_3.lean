import KUOS.DependentOriginationDoubleDeloopingUniverseTransportTypeABV1_106_2
import Mathlib.CategoryTheory.Limits.Preserves.FunctorCategory
import Mathlib.CategoryTheory.Limits.Shapes.Pullback.IsPullback.Basic

namespace KUOS.DependentOriginationDoubleDeloopingUniverseTransportTypeCV1_106_3

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Limits
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58
open KUOS.DependentOriginationDoubleDeloopingUniverseTransportV1_106_1
open KUOS.DependentOriginationDoubleDeloopingUniverseTransportTypeABV1_106_2

universe u

noncomputable section

/-!
# Universe transport for standard type-(C) generators v1.106.3

The type-(C) source and target are pushouts in simplicial sets.  We transport
the low-universe pushout squares through the pointwise universe lift, identify
the three span vertices with their native high-universe presentations, and use
pushout uniqueness to identify the lifted apex with the native apex.

The source and target scalings are minimal scaling enlarged by the single
`01n` triangle.  Once the carrier isomorphisms are fixed, scaled transport is
therefore reduced to minimal-scaling invariance and preservation of that one
distinguished triangle.  The resulting arrow isomorphism transports the
right-lifting property with Mathlib's arrow-isomorphism API.
-/

/-- Pointwise universe lift of simplicial sets preserves walking-span
colimits, because Type-level `ULift` preserves arbitrary colimits and
functor-category colimits are computed pointwise. -/
noncomputable instance ssetUlift_preservesWalkingSpan :
    PreservesColimitsOfShape WalkingSpan (SSet.uliftFunctor.{u, 0}) := by
  simpa only [SSet.uliftFunctor, SimplicialObject.whiskering] using
    (inferInstance :
      PreservesColimitsOfShape WalkingSpan
        ((Functor.whiskeringRight SimplexCategoryᵒᵖ (Type 0) (Type u)).obj
          CategoryTheory.uliftFunctor.{u, 0}))

/-! ## The collapsed edge face -/

/-- Degreewise identification of the lifted low-universe edge face with the
native high-universe edge face. -/
def standardTypeCEdgeFaceUliftObjEquiv
    (m : Nat) (J : SimplexCategoryᵒᵖ) :
    ((SSet.uliftFunctor.{u, 0}).obj
      (standardTypeCEdgeFace.{0} m : SSet.{0})).obj J ≃
      (standardTypeCEdgeFace.{u} m : SSet.{u}).obj J where
  toFun x :=
    ⟨(stdSimplexUliftIso.{u} (m + 3)).hom.app J
        (ULift.up x.down.1), by
      have hx := x.down.2
      change
        Finset.image
            (SSet.stdSimplex.objEquiv.{0} x.down.1).toOrderHom ⊤ ≤
          ({0, 1} : Finset (Fin (m + 4))) at hx
      change
        Finset.image
            (SSet.stdSimplex.objEquiv.{u}
              ((stdSimplexUliftIso.{u} (m + 3)).hom.app J
                (ULift.up x.down.1))).toOrderHom ⊤ ≤
          ({0, 1} : Finset (Fin (m + 4)))
      change
        Finset.image
            (SSet.stdSimplex.objEquiv.{0} x.down.1).toOrderHom ⊤ ≤
          ({0, 1} : Finset (Fin (m + 4)))
      exact hx⟩
  invFun x :=
    ULift.up
      ⟨((stdSimplexUliftIso.{u} (m + 3)).inv.app J x.1).down, by
        have hx := x.2
        change
          Finset.image
              (SSet.stdSimplex.objEquiv.{u} x.1).toOrderHom ⊤ ≤
            ({0, 1} : Finset (Fin (m + 4))) at hx
        change
          Finset.image
              (SSet.stdSimplex.objEquiv.{0}
                ((stdSimplexUliftIso.{u} (m + 3)).inv.app J x.1).down).toOrderHom ⊤ ≤
            ({0, 1} : Finset (Fin (m + 4)))
        change
          Finset.image
              (SSet.stdSimplex.objEquiv.{u} x.1).toOrderHom ⊤ ≤
            ({0, 1} : Finset (Fin (m + 4)))
        exact hx⟩
  left_inv x := by
    apply ULift.ext
    apply Subtype.ext
    change
      ((stdSimplexUliftObjEquiv.{u} (m + 3) J).symm
        ((stdSimplexUliftObjEquiv.{u} (m + 3) J)
          (ULift.up x.down.1))).down = x.down.1
    rw [Equiv.symm_apply_apply]
  right_inv x := by
    apply Subtype.ext
    change
      (stdSimplexUliftObjEquiv.{u} (m + 3) J)
        ((stdSimplexUliftObjEquiv.{u} (m + 3) J).symm x.1) = x.1
    rw [Equiv.apply_symm_apply]

/-- The edge-face equivalences are natural in the simplex degree. -/
def standardTypeCEdgeFaceUliftIso (m : Nat) :
    (SSet.uliftFunctor.{u, 0}).obj
        (standardTypeCEdgeFace.{0} m : SSet.{0}) ≅
      (standardTypeCEdgeFace.{u} m : SSet.{u}) :=
  NatIso.ofComponents
    (fun J => Equiv.toIso (standardTypeCEdgeFaceUliftObjEquiv.{u} m J))
    (fun f => by
      ext x
      apply Subtype.ext
      rfl)

/-- The edge-face universe identification commutes with the map to the outer
horn. -/
theorem standardTypeCEdgeFaceUliftIso_hom_toHorn (m : Nat) :
    (SSet.uliftFunctor.{u, 0}).map
        (standardTypeCEdgeToHorn.{0} m) ≫
      (hornUliftIso.{u} (m + 3) (0 : Fin (m + 4))).hom =
    (standardTypeCEdgeFaceUliftIso.{u} m).hom ≫
      standardTypeCEdgeToHorn.{u} m := by
  apply SSet.hom_ext
  intro J
  apply ConcreteCategory.hom_ext
  intro x
  apply Subtype.ext
  rfl

/-- The edge-face universe identification commutes with the map to the full
simplex. -/
theorem standardTypeCEdgeFaceUliftIso_hom_toSimplex (m : Nat) :
    (SSet.uliftFunctor.{u, 0}).map
        (standardTypeCEdgeToSimplex.{0} m) ≫
      (stdSimplexUliftIso.{u} (m + 3)).hom =
    (standardTypeCEdgeFaceUliftIso.{u} m).hom ≫
      standardTypeCEdgeToSimplex.{u} m := by
  apply SSet.hom_ext
  intro J
  apply ConcreteCategory.hom_ext
  intro x
  rfl

/-- The edge-collapse map is compatible with the universe identifications of
the edge and the point. -/
theorem standardTypeCEdgeFaceUliftIso_hom_collapse (m : Nat) :
    (SSet.uliftFunctor.{u, 0}).map
        (standardTypeCEdgeCollapseToPoint.{0} m) ≫
      (stdSimplexUliftIso.{u} 0).hom =
    (standardTypeCEdgeFaceUliftIso.{u} m).hom ≫
      standardTypeCEdgeCollapseToPoint.{u} m := by
  apply SSet.hom_ext
  intro J
  apply ConcreteCategory.hom_ext
  intro x
  rfl

/-! ## Transport the source and target pushout carriers -/

/-- The universe lift sends the low-universe source pushout square to a
pushout square. -/
def standardTypeCSourceCarrierUlift_isPushout (m : Nat) :
    IsPushout
      ((SSet.uliftFunctor.{u, 0}).map
        (standardTypeCEdgeToHorn.{0} m))
      ((SSet.uliftFunctor.{u, 0}).map
        (standardTypeCEdgeCollapseToPoint.{0} m))
      ((SSet.uliftFunctor.{u, 0}).map
        (standardTypeCSourceInl.{0} m))
      ((SSet.uliftFunctor.{u, 0}).map
        (standardTypeCSourceInr.{0} m)) :=
  (standardTypeCSourceCarrier_isPushout.{0} m).map
    (SSet.uliftFunctor.{u, 0})

/-- The universe lift sends the low-universe target pushout square to a
pushout square. -/
def standardTypeCTargetCarrierUlift_isPushout (m : Nat) :
    IsPushout
      ((SSet.uliftFunctor.{u, 0}).map
        (standardTypeCEdgeToSimplex.{0} m))
      ((SSet.uliftFunctor.{u, 0}).map
        (standardTypeCEdgeCollapseToPoint.{0} m))
      ((SSet.uliftFunctor.{u, 0}).map
        (standardTypeCTargetInl.{0} m))
      ((SSet.uliftFunctor.{u, 0}).map
        (standardTypeCTargetInr.{0} m)) :=
  (standardTypeCTargetCarrier_isPushout.{0} m).map
    (SSet.uliftFunctor.{u, 0})

/-- Native high-universe horn leg into the lifted low source apex. -/
def standardTypeCSourceNativeUliftInl (m : Nat) :
    (SSet.horn (m + 3) (0 : Fin (m + 4)) : SSet.{u}) ⟶
      (SSet.uliftFunctor.{u, 0}).obj
        (standardTypeCSourceCarrier.{0} m) :=
  (hornUliftIso.{u} (m + 3) (0 : Fin (m + 4))).inv ≫
    (SSet.uliftFunctor.{u, 0}).map
      (standardTypeCSourceInl.{0} m)

/-- Native high-universe point leg into the lifted low source apex. -/
def standardTypeCSourceNativeUliftInr (m : Nat) :
    (Δ[0] : SSet.{u}) ⟶
      (SSet.uliftFunctor.{u, 0}).obj
        (standardTypeCSourceCarrier.{0} m) :=
  (stdSimplexUliftIso.{u} 0).inv ≫
    (SSet.uliftFunctor.{u, 0}).map
      (standardTypeCSourceInr.{0} m)

/-- Re-present the lifted low source square over the native high-universe
span. -/
def standardTypeCSourceNativeSpanUlift_isPushout (m : Nat) :
    IsPushout
      (standardTypeCEdgeToHorn.{u} m)
      (standardTypeCEdgeCollapseToPoint.{u} m)
      (standardTypeCSourceNativeUliftInl.{u} m)
      (standardTypeCSourceNativeUliftInr.{u} m) := by
  exact
    (standardTypeCSourceCarrierUlift_isPushout.{u} m).of_iso
      (standardTypeCEdgeFaceUliftIso.{u} m)
      (hornUliftIso.{u} (m + 3) (0 : Fin (m + 4)))
      (stdSimplexUliftIso.{u} 0)
      (Iso.refl _)
      (standardTypeCEdgeFaceUliftIso_hom_toHorn.{u} m)
      (standardTypeCEdgeFaceUliftIso_hom_collapse.{u} m)
      (by simp [standardTypeCSourceNativeUliftInl])
      (by simp [standardTypeCSourceNativeUliftInr])

/-- Native high-universe simplex leg into the lifted low target apex. -/
def standardTypeCTargetNativeUliftInl (m : Nat) :
    (Δ[m + 3] : SSet.{u}) ⟶
      (SSet.uliftFunctor.{u, 0}).obj
        (standardTypeCTargetCarrier.{0} m) :=
  (stdSimplexUliftIso.{u} (m + 3)).inv ≫
    (SSet.uliftFunctor.{u, 0}).map
      (standardTypeCTargetInl.{0} m)

/-- Native high-universe point leg into the lifted low target apex. -/
def standardTypeCTargetNativeUliftInr (m : Nat) :
    (Δ[0] : SSet.{u}) ⟶
      (SSet.uliftFunctor.{u, 0}).obj
        (standardTypeCTargetCarrier.{0} m) :=
  (stdSimplexUliftIso.{u} 0).inv ≫
    (SSet.uliftFunctor.{u, 0}).map
      (standardTypeCTargetInr.{0} m)

/-- Re-present the lifted low target square over the native high-universe
span. -/
def standardTypeCTargetNativeSpanUlift_isPushout (m : Nat) :
    IsPushout
      (standardTypeCEdgeToSimplex.{u} m)
      (standardTypeCEdgeCollapseToPoint.{u} m)
      (standardTypeCTargetNativeUliftInl.{u} m)
      (standardTypeCTargetNativeUliftInr.{u} m) := by
  exact
    (standardTypeCTargetCarrierUlift_isPushout.{u} m).of_iso
      (standardTypeCEdgeFaceUliftIso.{u} m)
      (stdSimplexUliftIso.{u} (m + 3))
      (stdSimplexUliftIso.{u} 0)
      (Iso.refl _)
      (standardTypeCEdgeFaceUliftIso_hom_toSimplex.{u} m)
      (standardTypeCEdgeFaceUliftIso_hom_collapse.{u} m)
      (by simp [standardTypeCTargetNativeUliftInl])
      (by simp [standardTypeCTargetNativeUliftInr])

/-- Canonical source-apex isomorphism obtained from uniqueness of the native
high-universe source pushout. -/
def standardTypeCSourceCarrierUliftIso (m : Nat) :
    (SSet.uliftFunctor.{u, 0}).obj
        (standardTypeCSourceCarrier.{0} m) ≅
      standardTypeCSourceCarrier.{u} m :=
  (standardTypeCSourceNativeSpanUlift_isPushout.{u} m).isoIsPushout
    _ _ (standardTypeCSourceCarrier_isPushout.{u} m)

/-- Canonical target-apex isomorphism obtained from uniqueness of the native
high-universe target pushout. -/
def standardTypeCTargetCarrierUliftIso (m : Nat) :
    (SSet.uliftFunctor.{u, 0}).obj
        (standardTypeCTargetCarrier.{0} m) ≅
      standardTypeCTargetCarrier.{u} m :=
  (standardTypeCTargetNativeSpanUlift_isPushout.{u} m).isoIsPushout
    _ _ (standardTypeCTargetCarrier_isPushout.{u} m)

/-- Source-apex identification on the horn leg. -/
theorem standardTypeCSourceCarrierUliftIso_hom_inl (m : Nat) :
    (SSet.uliftFunctor.{u, 0}).map
        (standardTypeCSourceInl.{0} m) ≫
      (standardTypeCSourceCarrierUliftIso.{u} m).hom =
    (hornUliftIso.{u} (m + 3) (0 : Fin (m + 4))).hom ≫
      standardTypeCSourceInl.{u} m := by
  have h :=
    IsPushout.inl_isoIsPushout_hom
      (SSet.horn (m + 3) (0 : Fin (m + 4)) : SSet.{u})
      (Δ[0] : SSet.{u})
      (standardTypeCSourceNativeSpanUlift_isPushout.{u} m)
      (standardTypeCSourceCarrier_isPushout.{u} m)
  rw [← cancel_epi
    (hornUliftIso.{u} (m + 3) (0 : Fin (m + 4))).inv]
  change
    standardTypeCSourceNativeUliftInl.{u} m ≫
      (standardTypeCSourceCarrierUliftIso.{u} m).hom =
    standardTypeCSourceInl.{u} m
  exact h

/-- Source-apex identification on the point leg. -/
theorem standardTypeCSourceCarrierUliftIso_hom_inr (m : Nat) :
    (SSet.uliftFunctor.{u, 0}).map
        (standardTypeCSourceInr.{0} m) ≫
      (standardTypeCSourceCarrierUliftIso.{u} m).hom =
    (stdSimplexUliftIso.{u} 0).hom ≫
      standardTypeCSourceInr.{u} m := by
  have h :=
    IsPushout.inr_isoIsPushout_hom
      (SSet.horn (m + 3) (0 : Fin (m + 4)) : SSet.{u})
      (Δ[0] : SSet.{u})
      (standardTypeCSourceNativeSpanUlift_isPushout.{u} m)
      (standardTypeCSourceCarrier_isPushout.{u} m)
  rw [← cancel_epi (stdSimplexUliftIso.{u} 0).inv]
  change
    standardTypeCSourceNativeUliftInr.{u} m ≫
      (standardTypeCSourceCarrierUliftIso.{u} m).hom =
    standardTypeCSourceInr.{u} m
  exact h

/-- Target-apex identification on the simplex leg. -/
theorem standardTypeCTargetCarrierUliftIso_hom_inl (m : Nat) :
    (SSet.uliftFunctor.{u, 0}).map
        (standardTypeCTargetInl.{0} m) ≫
      (standardTypeCTargetCarrierUliftIso.{u} m).hom =
    (stdSimplexUliftIso.{u} (m + 3)).hom ≫
      standardTypeCTargetInl.{u} m := by
  have h :=
    IsPushout.inl_isoIsPushout_hom
      (Δ[m + 3] : SSet.{u})
      (Δ[0] : SSet.{u})
      (standardTypeCTargetNativeSpanUlift_isPushout.{u} m)
      (standardTypeCTargetCarrier_isPushout.{u} m)
  rw [← cancel_epi (stdSimplexUliftIso.{u} (m + 3)).inv]
  change
    standardTypeCTargetNativeUliftInl.{u} m ≫
      (standardTypeCTargetCarrierUliftIso.{u} m).hom =
    standardTypeCTargetInl.{u} m
  exact h

/-- Target-apex identification on the point leg. -/
theorem standardTypeCTargetCarrierUliftIso_hom_inr (m : Nat) :
    (SSet.uliftFunctor.{u, 0}).map
        (standardTypeCTargetInr.{0} m) ≫
      (standardTypeCTargetCarrierUliftIso.{u} m).hom =
    (stdSimplexUliftIso.{u} 0).hom ≫
      standardTypeCTargetInr.{u} m := by
  have h :=
    IsPushout.inr_isoIsPushout_hom
      (Δ[m + 3] : SSet.{u})
      (Δ[0] : SSet.{u})
      (standardTypeCTargetNativeSpanUlift_isPushout.{u} m)
      (standardTypeCTargetCarrier_isPushout.{u} m)
  rw [← cancel_epi (stdSimplexUliftIso.{u} 0).inv]
  change
    standardTypeCTargetNativeUliftInr.{u} m ≫
      (standardTypeCTargetCarrierUliftIso.{u} m).hom =
    standardTypeCTargetInr.{u} m
  exact h

/-! ## Distinguished triangle transport -/

/-- Pointwise `ULift` on a simplicial morphism acts by `ULift.up` on each
simplex. -/
@[simp]
theorem ssetUlift_map_app_up
    {X Y : SSet.{0}}
    (f : X ⟶ Y)
    (J : SimplexCategoryᵒᵖ)
    (x : X.obj J) :
    ((SSet.uliftFunctor.{u, 0}).map f).app J (ULift.up x) =
      ULift.up (f.app J x) := by
  rfl

/-- The canonical simplex universe isomorphism carries the low `01n` triangle
to the native high one. -/
@[simp]
theorem stdSimplexUliftIso_hom_standardTypeCTriangle01n (m : Nat) :
    (stdSimplexUliftIso.{u} (m + 3)).hom.app (op ⦋2⦌)
        (ULift.up (standardTypeCTriangle01n.{0} m)) =
      standardTypeCTriangle01n.{u} m := by
  ext j
  fin_cases j <;> rfl

/-- The horn universe isomorphism carries the low `01n` horn triangle to the
native high one. -/
@[simp]
theorem hornUliftIso_hom_standardTypeCTriangle01nInHorn (m : Nat) :
    (hornUliftIso.{u} (m + 3) (0 : Fin (m + 4))).hom.app (op ⦋2⦌)
        (ULift.up (standardTypeCTriangle01nInHorn.{0} m)) =
      standardTypeCTriangle01nInHorn.{u} m := by
  apply Subtype.ext
  exact stdSimplexUliftIso_hom_standardTypeCTriangle01n.{u} m

/-- The source-apex isomorphism sends the lifted distinguished source triangle
to the native distinguished source triangle. -/
theorem standardTypeCSourceCarrierUliftIso_hom_distinguished (m : Nat) :
    (standardTypeCSourceCarrierUliftIso.{u} m).hom.app (op ⦋2⦌)
        (ULift.up (standardTypeCSourceDistinguishedTriangle.{0} m)) =
      standardTypeCSourceDistinguishedTriangle.{u} m := by
  have h := congrArg
    (fun k :
        (SSet.uliftFunctor.{u, 0}).obj
            (SSet.horn (m + 3) (0 : Fin (m + 4)) : SSet.{0}) ⟶
          standardTypeCSourceCarrier.{u} m =>
      k.app (op ⦋2⦌)
        (ULift.up (standardTypeCTriangle01nInHorn.{0} m)))
    (standardTypeCSourceCarrierUliftIso_hom_inl.{u} m)
  simpa [standardTypeCSourceDistinguishedTriangle] using h

/-- The target-apex isomorphism sends the lifted distinguished target triangle
to the native distinguished target triangle. -/
theorem standardTypeCTargetCarrierUliftIso_hom_distinguished (m : Nat) :
    (standardTypeCTargetCarrierUliftIso.{u} m).hom.app (op ⦋2⦌)
        (ULift.up (standardTypeCTargetDistinguishedTriangle.{0} m)) =
      standardTypeCTargetDistinguishedTriangle.{u} m := by
  have h := congrArg
    (fun k :
        (SSet.uliftFunctor.{u, 0}).obj (Δ[m + 3] : SSet.{0}) ⟶
          standardTypeCTargetCarrier.{u} m =>
      k.app (op ⦋2⦌)
        (ULift.up (standardTypeCTriangle01n.{0} m)))
    (standardTypeCTargetCarrierUliftIso_hom_inl.{u} m)
  simpa [standardTypeCTargetDistinguishedTriangle] using h

/-! ## Minimal-plus-one-triangle scaling transport -/

/-- A carrier isomorphism from a lifted low object transports the scaling
obtained by adjoining one distinguished triangle. -/
theorem minimalPlusTriangleScaling_ulift_iso_iff
    {X : SSet.{0}} {Y : SSet.{u}}
    (e : (SSet.uliftFunctor.{u, 0}).obj X ≅ Y)
    (t0 : X.obj (op ⦋2⦌))
    (t1 : Y.obj (op ⦋2⦌))
    (hdist : e.hom.app (op ⦋2⦌)
        (ULift.up t0 :
          ((SSet.uliftFunctor.{u, 0}).obj X).obj (op ⦋2⦌)) = t1)
    (t : ((SSet.uliftFunctor.{u, 0}).obj X).obj (op ⦋2⦌)) :
    (uliftScaling (minimalPlusTriangleScaling t0)).thin t ↔
      (minimalPlusTriangleScaling t1).thin
        (e.hom.app (op ⦋2⦌) t) := by
  change
    ((minimalScaling X).thin t.down ∨ t.down = t0) ↔
      ((minimalScaling Y).thin (e.hom.app (op ⦋2⦌) t) ∨
        e.hom.app (op ⦋2⦌) t = t1)
  constructor
  · intro ht
    rcases ht with hmin | heq
    · have hLift :
          (minimalScaling
            ((SSet.uliftFunctor.{u, 0}).obj X)).thin t :=
        (uliftScaling_minimal_iff t).1 hmin
      exact Or.inl ((minimalScaling_iso_iff e t).1 hLift)
    · have ht0 :
          t = (ULift.up t0 :
            ((SSet.uliftFunctor.{u, 0}).obj X).obj (op ⦋2⦌)) := by
        apply ULift.ext
        exact heq
      rw [ht0]
      exact Or.inr hdist
  · intro ht
    rcases ht with hmin | heq
    · have hLift :
          (minimalScaling
            ((SSet.uliftFunctor.{u, 0}).obj X)).thin t :=
        (minimalScaling_iso_iff e t).2 hmin
      exact Or.inl ((uliftScaling_minimal_iff t).2 hLift)
    · have heq' :
          e.hom.app (op ⦋2⦌) t =
            e.hom.app (op ⦋2⦌)
              (ULift.up t0 :
                ((SSet.uliftFunctor.{u, 0}).obj X).obj (op ⦋2⦌)) := by
        rw [heq, hdist]
      have ht0 :
          t = (ULift.up t0 :
            ((SSet.uliftFunctor.{u, 0}).obj X).obj (op ⦋2⦌)) :=
        (e.app (op ⦋2⦌)).toEquiv.injective heq'
      exact Or.inr (congrArg ULift.down ht0)

/-- Lifted low-universe type-(C) source and native high-universe source are
isomorphic as scaled simplicial sets. -/
def standardTypeCSourceUliftIso (m : Nat) :
    scaledUliftObj.{u} (standardTypeCSource.{0} m) ≅
      standardTypeCSource.{u} m := by
  refine scaledIsoOfCarrierIso
    (standardTypeCSourceCarrierUliftIso.{u} m) ?_ ?_
  · intro t ht
    change
      (uliftScaling
        (minimalPlusTriangleScaling
          (standardTypeCSourceDistinguishedTriangle.{0} m))).thin t at ht
    change
      (minimalPlusTriangleScaling
        (standardTypeCSourceDistinguishedTriangle.{u} m)).thin
          ((standardTypeCSourceCarrierUliftIso.{u} m).hom.app
            (op ⦋2⦌) t)
    exact
      (minimalPlusTriangleScaling_ulift_iso_iff
        (standardTypeCSourceCarrierUliftIso.{u} m)
        (standardTypeCSourceDistinguishedTriangle.{0} m)
        (standardTypeCSourceDistinguishedTriangle.{u} m)
        (standardTypeCSourceCarrierUliftIso_hom_distinguished.{u} m)
        t).1 ht
  · intro t ht
    change
      (minimalPlusTriangleScaling
        (standardTypeCSourceDistinguishedTriangle.{u} m)).thin t at ht
    change
      (uliftScaling
        (minimalPlusTriangleScaling
          (standardTypeCSourceDistinguishedTriangle.{0} m))).thin
            ((standardTypeCSourceCarrierUliftIso.{u} m).inv.app
              (op ⦋2⦌) t)
    apply
      (minimalPlusTriangleScaling_ulift_iso_iff
        (standardTypeCSourceCarrierUliftIso.{u} m)
        (standardTypeCSourceDistinguishedTriangle.{0} m)
        (standardTypeCSourceDistinguishedTriangle.{u} m)
        (standardTypeCSourceCarrierUliftIso_hom_distinguished.{u} m)
        ((standardTypeCSourceCarrierUliftIso.{u} m).inv.app
          (op ⦋2⦌) t)).2
    simpa using ht

/-- Lifted low-universe type-(C) target and native high-universe target are
isomorphic as scaled simplicial sets. -/
def standardTypeCTargetUliftIso (m : Nat) :
    scaledUliftObj.{u} (standardTypeCTarget.{0} m) ≅
      standardTypeCTarget.{u} m := by
  refine scaledIsoOfCarrierIso
    (standardTypeCTargetCarrierUliftIso.{u} m) ?_ ?_
  · intro t ht
    change
      (uliftScaling
        (minimalPlusTriangleScaling
          (standardTypeCTargetDistinguishedTriangle.{0} m))).thin t at ht
    change
      (minimalPlusTriangleScaling
        (standardTypeCTargetDistinguishedTriangle.{u} m)).thin
          ((standardTypeCTargetCarrierUliftIso.{u} m).hom.app
            (op ⦋2⦌) t)
    exact
      (minimalPlusTriangleScaling_ulift_iso_iff
        (standardTypeCTargetCarrierUliftIso.{u} m)
        (standardTypeCTargetDistinguishedTriangle.{0} m)
        (standardTypeCTargetDistinguishedTriangle.{u} m)
        (standardTypeCTargetCarrierUliftIso_hom_distinguished.{u} m)
        t).1 ht
  · intro t ht
    change
      (minimalPlusTriangleScaling
        (standardTypeCTargetDistinguishedTriangle.{u} m)).thin t at ht
    change
      (uliftScaling
        (minimalPlusTriangleScaling
          (standardTypeCTargetDistinguishedTriangle.{0} m))).thin
            ((standardTypeCTargetCarrierUliftIso.{u} m).inv.app
              (op ⦋2⦌) t)
    apply
      (minimalPlusTriangleScaling_ulift_iso_iff
        (standardTypeCTargetCarrierUliftIso.{u} m)
        (standardTypeCTargetDistinguishedTriangle.{0} m)
        (standardTypeCTargetDistinguishedTriangle.{u} m)
        (standardTypeCTargetCarrierUliftIso_hom_distinguished.{u} m)
        ((standardTypeCTargetCarrierUliftIso.{u} m).inv.app
          (op ⦋2⦌) t)).2
    simpa using ht

/-! ## The type-(C) generator arrow -/

/-- Mapped low source-leg equation for the induced type-(C) carrier map. -/
theorem standardTypeCCarrierMap_ulift_inl_horn (m : Nat) :
    (SSet.uliftFunctor.{u, 0}).map
        (standardTypeCSourceInl.{0} m) ≫
      (SSet.uliftFunctor.{u, 0}).map
        (standardTypeCCarrierMap.{0} m) =
    (SSet.uliftFunctor.{u, 0}).map
        ((SSet.horn.{0} (m + 3) (0 : Fin (m + 4))).ι) ≫
      (SSet.uliftFunctor.{u, 0}).map
        (standardTypeCTargetInl.{0} m) := by
  simpa only [(SSet.uliftFunctor.{u, 0}).map_comp] using
    congrArg
      (fun k => (SSet.uliftFunctor.{u, 0}).map k)
      (standardTypeCCarrierMap_inl_horn.{0} m)

/-- Mapped low point-leg equation for the induced type-(C) carrier map. -/
theorem standardTypeCCarrierMap_ulift_inr_point (m : Nat) :
    (SSet.uliftFunctor.{u, 0}).map
        (standardTypeCSourceInr.{0} m) ≫
      (SSet.uliftFunctor.{u, 0}).map
        (standardTypeCCarrierMap.{0} m) =
    (SSet.uliftFunctor.{u, 0}).map
      (standardTypeCTargetInr.{0} m) := by
  simpa only [(SSet.uliftFunctor.{u, 0}).map_comp] using
    congrArg
      (fun k => (SSet.uliftFunctor.{u, 0}).map k)
      (standardTypeCCarrierMap_inr_point.{0} m)

/-- The source and target pushout identifications intertwine the low lifted and
native high type-(C) carrier maps. -/
theorem standardTypeCCarrierMap_ulift_commutes (m : Nat) :
    (SSet.uliftFunctor.{u, 0}).map
        (standardTypeCCarrierMap.{0} m) ≫
      (standardTypeCTargetCarrierUliftIso.{u} m).hom =
    (standardTypeCSourceCarrierUliftIso.{u} m).hom ≫
      standardTypeCCarrierMap.{u} m := by
  apply (standardTypeCSourceCarrierUlift_isPushout.{u} m).hom_ext
  · calc
      (SSet.uliftFunctor.{u, 0}).map
            (standardTypeCSourceInl.{0} m) ≫
          ((SSet.uliftFunctor.{u, 0}).map
              (standardTypeCCarrierMap.{0} m) ≫
            (standardTypeCTargetCarrierUliftIso.{u} m).hom) =
        ((SSet.uliftFunctor.{u, 0}).map
              (standardTypeCSourceInl.{0} m) ≫
            (SSet.uliftFunctor.{u, 0}).map
              (standardTypeCCarrierMap.{0} m)) ≫
          (standardTypeCTargetCarrierUliftIso.{u} m).hom := by
            exact (Category.assoc _ _ _).symm
      _ =
        ((SSet.uliftFunctor.{u, 0}).map
              ((SSet.horn.{0} (m + 3) (0 : Fin (m + 4))).ι) ≫
            (SSet.uliftFunctor.{u, 0}).map
              (standardTypeCTargetInl.{0} m)) ≫
          (standardTypeCTargetCarrierUliftIso.{u} m).hom := by
            rw [standardTypeCCarrierMap_ulift_inl_horn.{u} m]
      _ =
        (SSet.uliftFunctor.{u, 0}).map
              ((SSet.horn.{0} (m + 3) (0 : Fin (m + 4))).ι) ≫
          ((stdSimplexUliftIso.{u} (m + 3)).hom ≫
            standardTypeCTargetInl.{u} m) := by
            rw [Category.assoc,
              standardTypeCTargetCarrierUliftIso_hom_inl.{u} m]
      _ =
        ((hornUliftIso.{u} (m + 3) (0 : Fin (m + 4))).hom ≫
            (SSet.horn.{u} (m + 3) (0 : Fin (m + 4))).ι) ≫
          standardTypeCTargetInl.{u} m := by
            rw [← Category.assoc, ← hornUliftIso_hom_ι.{u}]
      _ =
        (hornUliftIso.{u} (m + 3) (0 : Fin (m + 4))).hom ≫
          (standardTypeCSourceInl.{u} m ≫
            standardTypeCCarrierMap.{u} m) := by
            simp only [standardTypeCCarrierMap_inl_horn, Category.assoc]
      _ =
        ((SSet.uliftFunctor.{u, 0}).map
              (standardTypeCSourceInl.{0} m) ≫
            (standardTypeCSourceCarrierUliftIso.{u} m).hom) ≫
          standardTypeCCarrierMap.{u} m := by
            simp only [standardTypeCSourceCarrierUliftIso_hom_inl, Category.assoc]
      _ =
        (SSet.uliftFunctor.{u, 0}).map
            (standardTypeCSourceInl.{0} m) ≫
          ((standardTypeCSourceCarrierUliftIso.{u} m).hom ≫
            standardTypeCCarrierMap.{u} m) := by
            exact Category.assoc _ _ _
  · calc
      (SSet.uliftFunctor.{u, 0}).map
            (standardTypeCSourceInr.{0} m) ≫
          ((SSet.uliftFunctor.{u, 0}).map
              (standardTypeCCarrierMap.{0} m) ≫
            (standardTypeCTargetCarrierUliftIso.{u} m).hom) =
        ((SSet.uliftFunctor.{u, 0}).map
              (standardTypeCSourceInr.{0} m) ≫
            (SSet.uliftFunctor.{u, 0}).map
              (standardTypeCCarrierMap.{0} m)) ≫
          (standardTypeCTargetCarrierUliftIso.{u} m).hom := by
            exact (Category.assoc _ _ _).symm
      _ =
        (SSet.uliftFunctor.{u, 0}).map
              (standardTypeCTargetInr.{0} m) ≫
          (standardTypeCTargetCarrierUliftIso.{u} m).hom := by
            rw [standardTypeCCarrierMap_ulift_inr_point.{u} m]
      _ =
        (stdSimplexUliftIso.{u} 0).hom ≫
          standardTypeCTargetInr.{u} m :=
            standardTypeCTargetCarrierUliftIso_hom_inr.{u} m
      _ =
        (stdSimplexUliftIso.{u} 0).hom ≫
          (standardTypeCSourceInr.{u} m ≫
            standardTypeCCarrierMap.{u} m) := by
            rw [standardTypeCCarrierMap_inr_point.{u} m]
      _ =
        ((SSet.uliftFunctor.{u, 0}).map
              (standardTypeCSourceInr.{0} m) ≫
            (standardTypeCSourceCarrierUliftIso.{u} m).hom) ≫
          standardTypeCCarrierMap.{u} m := by
            simp only [standardTypeCSourceCarrierUliftIso_hom_inr, Category.assoc]
      _ =
        (SSet.uliftFunctor.{u, 0}).map
            (standardTypeCSourceInr.{0} m) ≫
          ((standardTypeCSourceCarrierUliftIso.{u} m).hom ≫
            standardTypeCCarrierMap.{u} m) := by
            exact Category.assoc _ _ _

/-- The lifted low-universe type-(C) generator is isomorphic, as an arrow, to
the native high-universe type-(C) generator. -/
def standardTypeCGeneratorUliftArrowIso (m : Nat) :
    Arrow.mk
        ((scaledUliftFunctor.{u}).map
          (standardTypeCGeneratorHom.{0} m)) ≅
      Arrow.mk (standardTypeCGeneratorHom.{u} m) :=
  Arrow.isoMk'
    ((scaledUliftFunctor.{u}).map
      (standardTypeCGeneratorHom.{0} m))
    (standardTypeCGeneratorHom.{u} m)
    (standardTypeCSourceUliftIso.{u} m)
    (standardTypeCTargetUliftIso.{u} m)
    (by
      apply ScaledSSet.ScaledMap.ext
      exact (standardTypeCCarrierMap_ulift_commutes.{u} m).symm)

/-- Any low-universe lifting property against a type-(C) generator transports
to the native type-(C) generator in an arbitrary universe. -/
theorem hasLiftingProperty_standardTypeC_ulift
    (m : Nat)
    {P Q : ScaledSSet.{0}}
    (p : P ⟶ Q)
    (h : HasLiftingProperty
      (standardTypeCGeneratorHom.{0} m) p) :
    HasLiftingProperty
      (standardTypeCGeneratorHom.{u} m)
      ((scaledUliftFunctor.{u}).map p) := by
  have hmap :
      HasLiftingProperty
        ((scaledUliftFunctor.{u}).map
          (standardTypeCGeneratorHom.{0} m))
        ((scaledUliftFunctor.{u}).map p) :=
    hasLiftingProperty_map_of_full_faithful
      (scaledUliftFunctor.{u}) h
  letI :
      HasLiftingProperty
        ((scaledUliftFunctor.{u}).map
          (standardTypeCGeneratorHom.{0} m))
        ((scaledUliftFunctor.{u}).map p) := hmap
  exact HasLiftingProperty.of_arrow_iso_left
    (standardTypeCGeneratorUliftArrowIso.{u} m)
    ((scaledUliftFunctor.{u}).map p)

end

end KUOS.DependentOriginationDoubleDeloopingUniverseTransportTypeCV1_106_3
