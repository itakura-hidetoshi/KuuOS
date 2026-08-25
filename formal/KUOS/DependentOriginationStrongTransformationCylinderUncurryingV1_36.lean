import KUOS.DependentOriginationStrongTransformationDuskinCylinderV1_35
import Mathlib.Tactic

namespace KUOS.DependentOriginationStrongTransformationCylinderUncurryingV1_36

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Bicategory
open CategoryTheory.Prod
open Simplicial
open Opposite
open scoped Bicategory
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27
open KUOS.DependentOriginationCoherentNormalizedScaledModelEquivalenceV1_32
open KUOS.DependentOriginationGlobalDuskinPrismHomotopyV1_34
open KUOS.DependentOriginationStrongTransformationDuskinCylinderV1_35

universe u₁ u₂ v₁ v₂ w₁ w₂

/-!
# Strong-transformation cylinder uncurrying v1.36

This layer closes the bicategorical construction isolated in v1.35.

For strictly-unitary pseudofunctors `P Q : B -> C` and a native strong
transformation `η : P ==> Q`, we construct the normal pseudofunctorial
cylinder

`B × [1] -> C`.

On a horizontal arrow `f : X -> Y` the cylinder uses

* `P(f)` on the `0` end,
* `Q(f)` on the `1` end,
* `P(f) ; η_Y` across `0 -> 1`.

The two mixed composition laws are exactly the pseudofunctor composition
constraint of `P` and the strong naturality isomorphism of `η`.  The strong
transformation identity, composition, and 2-cell naturality laws close the
unit, associativity, and map₂ coherence equations.  Converting the resulting
strictly-unitary pseudofunctor to a strictly-unitary lax functor gives the
cylinder required by v1.35, hence one global Duskin prism and all hornwise
homotopies.
-/

private def cylinderObj
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (P Q : StrictlyUnitaryPseudofunctor B C)
    (X : B × DuskinOrdinal 1) : C :=
  if X.2.as = (0 : Fin 2) then P.obj X.1 else Q.obj X.1

private theorem noIntervalHomOneZero
    {X Y : DuskinOrdinal 1}
    (f : X ⟶ Y)
    (hX : X.as ≠ (0 : Fin 2))
    (hY : Y.as = (0 : Fin 2)) : False := by
  have hle := f.as.le
  have hx1 : X.as = (1 : Fin 2) := by omega
  rw [hx1, hY] at hle
  omega

private def cylinderMap
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (P Q : StrictlyUnitaryPseudofunctor B C)
    (η : Pseudofunctor.StrongTrans P.toPseudofunctor Q.toPseudofunctor)
    {X Y : B × DuskinOrdinal 1}
    (f : X ⟶ Y) : cylinderObj P Q X ⟶ cylinderObj P Q Y := by
  by_cases hX : X.2.as = (0 : Fin 2)
  · by_cases hY : Y.2.as = (0 : Fin 2)
    · simpa [cylinderObj, hX, hY] using P.map f.1
    · simpa [cylinderObj, hX, hY] using (P.map f.1 ≫ η.app Y.1)
  · by_cases hY : Y.2.as = (0 : Fin 2)
    · exact False.elim (noIntervalHomOneZero f.2 hX hY)
    · simpa [cylinderObj, hX, hY] using Q.map f.1

private def cylinderMap₂
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (P Q : StrictlyUnitaryPseudofunctor B C)
    (η : Pseudofunctor.StrongTrans P.toPseudofunctor Q.toPseudofunctor)
    {X Y : B × DuskinOrdinal 1}
    {f g : X ⟶ Y}
    (α : f ⟶ g) :
    cylinderMap P Q η f ⟶ cylinderMap P Q η g := by
  by_cases hX : X.2.as = (0 : Fin 2)
  · by_cases hY : Y.2.as = (0 : Fin 2)
    · simpa [cylinderMap, cylinderObj, hX, hY] using P.map₂ α.1
    · simpa [cylinderMap, cylinderObj, hX, hY] using
        (P.map₂ α.1 ▷ η.app Y.1)
  · by_cases hY : Y.2.as = (0 : Fin 2)
    · exact False.elim (noIntervalHomOneZero f.2 hX hY)
    · simpa [cylinderMap, cylinderObj, hX, hY] using Q.map₂ α.1

private def cylinderMapComp
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (P Q : StrictlyUnitaryPseudofunctor B C)
    (η : Pseudofunctor.StrongTrans P.toPseudofunctor Q.toPseudofunctor)
    {X Y Z : B × DuskinOrdinal 1}
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    cylinderMap P Q η (f ≫ g) ≅
      cylinderMap P Q η f ≫ cylinderMap P Q η g := by
  by_cases hX : X.2.as = (0 : Fin 2)
  · by_cases hY : Y.2.as = (0 : Fin 2)
    · by_cases hZ : Z.2.as = (0 : Fin 2)
      · simpa [cylinderMap, cylinderObj, hX, hY, hZ] using P.mapComp f.1 g.1
      · simpa [cylinderMap, cylinderObj, hX, hY, hZ] using
          (whiskerRightIso (P.mapComp f.1 g.1) (η.app Z.1) ≪≫
            α_ (P.map f.1) (P.map g.1) (η.app Z.1))
    · by_cases hZ : Z.2.as = (0 : Fin 2)
      · exact False.elim (noIntervalHomOneZero g.2 hY hZ)
      · simpa [cylinderMap, cylinderObj, hX, hY, hZ] using
          (whiskerRightIso (P.mapComp f.1 g.1) (η.app Z.1) ≪≫
            α_ (P.map f.1) (P.map g.1) (η.app Z.1) ≪≫
            whiskerLeftIso (P.map f.1) (η.naturality g.1) ≪≫
            (α_ (P.map f.1) (η.app Y.1) (Q.map g.1)).symm)
  · by_cases hY : Y.2.as = (0 : Fin 2)
    · exact False.elim (noIntervalHomOneZero f.2 hX hY)
    · by_cases hZ : Z.2.as = (0 : Fin 2)
      · exact False.elim (noIntervalHomOneZero g.2 hY hZ)
      · simpa [cylinderMap, cylinderObj, hX, hY, hZ] using Q.mapComp f.1 g.1

private def strongCylinderCore
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (P Q : StrictlyUnitaryPseudofunctor B C)
    (η : Pseudofunctor.StrongTrans P.toPseudofunctor Q.toPseudofunctor) :
    StrictlyUnitaryPseudofunctorCore (B × DuskinOrdinal 1) C where
  obj := cylinderObj P Q
  map := cylinderMap P Q η
  map_id := by
    intro X
    by_cases hX : X.2.as = (0 : Fin 2)
    · simpa [cylinderMap, cylinderObj, hX, P.map_id]
    · simpa [cylinderMap, cylinderObj, hX, Q.map_id]
  map₂ := cylinderMap₂ P Q η
  map₂_id := by
    intro X Y f
    by_cases hX : X.2.as = (0 : Fin 2)
    · by_cases hY : Y.2.as = (0 : Fin 2)
      · simp [cylinderMap₂, cylinderMap, cylinderObj, hX, hY]
      · simp [cylinderMap₂, cylinderMap, cylinderObj, hX, hY]
    · by_cases hY : Y.2.as = (0 : Fin 2)
      · exact False.elim (noIntervalHomOneZero f.2 hX hY)
      · simp [cylinderMap₂, cylinderMap, cylinderObj, hX, hY]
  map₂_comp := by
    intro X Y f g h α β
    by_cases hX : X.2.as = (0 : Fin 2)
    · by_cases hY : Y.2.as = (0 : Fin 2)
      · simp [cylinderMap₂, cylinderMap, cylinderObj, hX, hY]
      · simp [cylinderMap₂, cylinderMap, cylinderObj, hX, hY,
          comp_whiskerRight]
    · by_cases hY : Y.2.as = (0 : Fin 2)
      · exact False.elim (noIntervalHomOneZero f.2 hX hY)
      · simp [cylinderMap₂, cylinderMap, cylinderObj, hX, hY]
  mapComp := cylinderMapComp P Q η
  map₂_whisker_left := by
    intro X Y Z f g h β
    by_cases hX : X.2.as = (0 : Fin 2)
    · by_cases hY : Y.2.as = (0 : Fin 2)
      · by_cases hZ : Z.2.as = (0 : Fin 2)
        · simpa [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj,
            hX, hY, hZ] using P.map₂_whisker_left f.1 β.1
        · simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj,
            hX, hY, hZ, P.map₂_whisker_left]
          bicategory
      · by_cases hZ : Z.2.as = (0 : Fin 2)
        · exact False.elim (noIntervalHomOneZero g.2 hY hZ)
        · simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj,
            hX, hY, hZ, P.map₂_whisker_left]
          bicategory
    · by_cases hY : Y.2.as = (0 : Fin 2)
      · exact False.elim (noIntervalHomOneZero f.2 hX hY)
      · by_cases hZ : Z.2.as = (0 : Fin 2)
        · exact False.elim (noIntervalHomOneZero g.2 hY hZ)
        · simpa [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj,
            hX, hY, hZ] using Q.map₂_whisker_left f.1 β.1
  map₂_whisker_right := by
    intro X Y Z f g α h
    by_cases hX : X.2.as = (0 : Fin 2)
    · by_cases hY : Y.2.as = (0 : Fin 2)
      · by_cases hZ : Z.2.as = (0 : Fin 2)
        · simpa [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj,
            hX, hY, hZ] using P.map₂_whisker_right α.1 h.1
        · simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj,
            hX, hY, hZ, P.map₂_whisker_right]
          bicategory
      · by_cases hZ : Z.2.as = (0 : Fin 2)
        · exact False.elim (noIntervalHomOneZero h.2 hY hZ)
        · have hnat := η.naturality_naturality α.1
          simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj,
            hX, hY, hZ, P.map₂_whisker_right, hnat]
          bicategory
    · by_cases hY : Y.2.as = (0 : Fin 2)
      · exact False.elim (noIntervalHomOneZero f.2 hX hY)
      · by_cases hZ : Z.2.as = (0 : Fin 2)
        · exact False.elim (noIntervalHomOneZero h.2 hY hZ)
        · simpa [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj,
            hX, hY, hZ] using Q.map₂_whisker_right α.1 h.1
  map₂_left_unitor := by
    intro X Y f
    by_cases hX : X.2.as = (0 : Fin 2)
    · by_cases hY : Y.2.as = (0 : Fin 2)
      · simpa [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj,
          hX, hY, P.map_id] using P.map₂_left_unitor f.1
      · simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj,
          hX, hY, P.map_id, P.map₂_left_unitor]
        bicategory
    · by_cases hY : Y.2.as = (0 : Fin 2)
      · exact False.elim (noIntervalHomOneZero f.2 hX hY)
      · simpa [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj,
          hX, hY, Q.map_id] using Q.map₂_left_unitor f.1
  map₂_right_unitor := by
    intro X Y f
    by_cases hX : X.2.as = (0 : Fin 2)
    · by_cases hY : Y.2.as = (0 : Fin 2)
      · simpa [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj,
          hX, hY, P.map_id] using P.map₂_right_unitor f.1
      · simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj,
          hX, hY, P.map_id, Q.map_id,
          P.map₂_right_unitor, Pseudofunctor.StrongTrans.naturality_id_hom]
        bicategory
    · by_cases hY : Y.2.as = (0 : Fin 2)
      · exact False.elim (noIntervalHomOneZero f.2 hX hY)
      · simpa [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj,
          hX, hY, Q.map_id] using Q.map₂_right_unitor f.1
  map₂_associator := by
    intro A B C D f g h
    by_cases hA : A.2.as = (0 : Fin 2)
    · by_cases hB : B.2.as = (0 : Fin 2)
      · by_cases hC : C.2.as = (0 : Fin 2)
        · by_cases hD : D.2.as = (0 : Fin 2)
          · simpa [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj,
              hA, hB, hC, hD] using P.map₂_associator f.1 g.1 h.1
          · simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj,
              hA, hB, hC, hD, P.map₂_associator]
            bicategory
        · by_cases hD : D.2.as = (0 : Fin 2)
          · exact False.elim (noIntervalHomOneZero h.2 hC hD)
          · simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj,
              hA, hB, hC, hD,
              P.map₂_associator,
              Pseudofunctor.StrongTrans.naturality_comp_hom]
            bicategory
      · by_cases hC : C.2.as = (0 : Fin 2)
        · exact False.elim (noIntervalHomOneZero g.2 hB hC)
        · by_cases hD : D.2.as = (0 : Fin 2)
          · exact False.elim (noIntervalHomOneZero h.2 hC hD)
          · simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj,
              hA, hB, hC, hD,
              P.map₂_associator,
              Pseudofunctor.StrongTrans.naturality_comp_hom]
            bicategory
    · by_cases hB : B.2.as = (0 : Fin 2)
      · exact False.elim (noIntervalHomOneZero f.2 hA hB)
      · by_cases hC : C.2.as = (0 : Fin 2)
        · exact False.elim (noIntervalHomOneZero g.2 hB hC)
        · by_cases hD : D.2.as = (0 : Fin 2)
          · exact False.elim (noIntervalHomOneZero h.2 hC hD)
          · simpa [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj,
              hA, hB, hC, hD] using Q.map₂_associator f.1 g.1 h.1

/-- Uncurrying a native strong transformation into a strictly-unitary pseudofunctor cylinder. -/
def strongTransformationCylinder
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (P Q : StrictlyUnitaryPseudofunctor B C)
    (η : Pseudofunctor.StrongTrans P.toPseudofunctor Q.toPseudofunctor) :
    StrictlyUnitaryPseudofunctor (B × DuskinOrdinal 1) C :=
  StrictlyUnitaryPseudofunctor.mk' (strongCylinderCore P Q η)

/-- The corresponding normal-lax cylinder. -/
def strongTransformationNormalLaxCylinder
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (P Q : StrictlyUnitaryPseudofunctor B C)
    (η : Pseudofunctor.StrongTrans P.toPseudofunctor Q.toPseudofunctor) :
    StrictlyUnitaryLaxFunctor (B × DuskinOrdinal 1) C :=
  (strongTransformationCylinder P Q η).toStrictlyUnitaryLaxFunctor

/-! ## Endpoint identification -/

@[simp] theorem strongTransformationNormalLaxCylinder_zero_obj
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (P Q : StrictlyUnitaryPseudofunctor B C)
    (η : Pseudofunctor.StrongTrans P.toPseudofunctor Q.toPseudofunctor)
    (X : B) :
    (strongTransformationNormalLaxCylinder P Q η).obj
      (X, LocallyDiscrete.mk (0 : Fin 2)) = P.obj X := rfl

@[simp] theorem strongTransformationNormalLaxCylinder_one_obj
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (P Q : StrictlyUnitaryPseudofunctor B C)
    (η : Pseudofunctor.StrongTrans P.toPseudofunctor Q.toPseudofunctor)
    (X : B) :
    (strongTransformationNormalLaxCylinder P Q η).obj
      (X, LocallyDiscrete.mk (1 : Fin 2)) = Q.obj X := rfl

/-- The v1.35 cylinder interface is automatic for a native strong transformation. -/
noncomputable def strongTransformationDuskinCylinder
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (P Q : StrictlyUnitaryPseudofunctor B C)
    (η : Pseudofunctor.StrongTrans P.toPseudofunctor Q.toPseudofunctor) :
    NormalLaxDuskinCylinder
      P.toStrictlyUnitaryLaxFunctor Q.toStrictlyUnitaryLaxFunctor where
  cylinder := strongTransformationNormalLaxCylinder P Q η
  endpoint_zero := by
    intro Δ σ
    apply StrictlyUnitaryLaxFunctor.ext
    · rfl
    all_goals
      · rw [heq_iff_eq]
        ext
        simp [normalLaxPair, intervalNormalLax,
          strongTransformationNormalLaxCylinder,
          strongTransformationCylinder, strongCylinderCore,
          cylinderObj, cylinderMap, cylinderMap₂, cylinderMapComp]
  endpoint_one := by
    intro Δ σ
    apply StrictlyUnitaryLaxFunctor.ext
    · rfl
    all_goals
      · rw [heq_iff_eq]
        ext
        simp [normalLaxPair, intervalNormalLax,
          strongTransformationNormalLaxCylinder,
          strongTransformationCylinder, strongCylinderCore,
          cylinderObj, cylinderMap, cylinderMap₂, cylinderMapComp]

/-! ## Quasi-inverse specialization -/

/-- The source strong counit now has its canonical normal-lax cylinder. -/
noncomputable def sourceStrongCylinder
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    (K : NormalizedCoherentQuasiInverse F G) :
    NormalLaxDuskinCylinder
      (sourceRoundTripNormalLax F G)
      (StrictlyUnitaryLaxFunctor.id B) := by
  let P := F.forward.comp G.forward
  have hP : P.toStrictlyUnitaryLaxFunctor = sourceRoundTripNormalLax F G := rfl
  let Q := StrictlyUnitaryPseudofunctor.id B
  have hQ : Q.toStrictlyUnitaryLaxFunctor = StrictlyUnitaryLaxFunctor.id B := rfl
  simpa [P, Q, hP, hQ] using
    strongTransformationDuskinCylinder P Q (sourcePseudoStrong K)

/-- The target strong counit has its canonical normal-lax cylinder. -/
noncomputable def targetStrongCylinder
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    (K : NormalizedCoherentQuasiInverse F G) :
    NormalLaxDuskinCylinder
      (targetRoundTripNormalLax F G)
      (StrictlyUnitaryLaxFunctor.id C) := by
  let P := G.forward.comp F.forward
  have hP : P.toStrictlyUnitaryLaxFunctor = targetRoundTripNormalLax F G := rfl
  let Q := StrictlyUnitaryPseudofunctor.id C
  have hQ : Q.toStrictlyUnitaryLaxFunctor = StrictlyUnitaryLaxFunctor.id C := rfl
  simpa [P, Q, hP, hQ] using
    strongTransformationDuskinCylinder P Q (targetPseudoStrong K)

/-- The v1.35 remaining cylinder certificate is now theorem-level automatic. -/
noncomputable def strongQuasiInverseNormalLaxCylinder
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    (K : NormalizedCoherentQuasiInverse F G) :
    StrongQuasiInverseNormalLaxCylinder K where
  sourceCylinder := sourceStrongCylinder K
  targetCylinder := targetStrongCylinder K
  source_realizes_component := by intro X; rfl
  target_realizes_component := by intro X; rfl

/-- Native coherent quasi-inverses therefore automatically produce the global Duskin prisms. -/
noncomputable def globalDuskinRoundTripPrismRealization
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    (K : NormalizedCoherentQuasiInverse F G) :
    GlobalDuskinRoundTripPrismRealization K where
  sourcePrism := by
    simpa [normalLaxDuskinNerveMap_comp] using
      (strongQuasiInverseNormalLaxCylinder K).sourcePrism
  targetPrism := by
    simpa [normalLaxDuskinNerveMap_comp] using
      (strongQuasiInverseNormalLaxCylinder K).targetPrism

/-!
The prism side is now closed without hornwise choices:

`Pseudofunctor.StrongTrans`
  -> canonical strictly-unitary pseudofunctor cylinder
  -> canonical normal-lax cylinder
  -> canonical native `SSet.Homotopy`
  -> global Duskin round-trip prism
  -> every hornwise round-trip homotopy.

The only independent extra ingredient still retained from v1.33 is the
homotopy-to-strict horn rectification property.  It is deliberately not
manufactured from the prism, so no fibrancy assumption is used circularly.
-/

end KUOS.DependentOriginationStrongTransformationCylinderUncurryingV1_36
