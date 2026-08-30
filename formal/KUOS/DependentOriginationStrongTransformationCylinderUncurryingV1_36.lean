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

universe u u₁ u₂ v v₁ v₂ w w₁ w₂

/-!
# Strong-transformation cylinder uncurrying v1.36

A native strong transformation between strictly-unitary pseudofunctors gives a
normal cylinder over the walking interval.  We classify the two interval
objects with an indexed `Type`, rather than a proposition, so the classifier
may refine endpoint indices while constructing morphisms and isomorphisms.
-/

private inductive FinTwoView : Fin 2 → Type
  | zero : FinTwoView 0
  | one : FinTwoView 1

private def finTwoView (i : Fin 2) : FinTwoView i := by
  by_cases h : i = 0
  · subst i
    exact .zero
  · have h1 : i = 1 := by omega
    subst i
    exact .one

private def cylinderObj
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (P Q : StrictlyUnitaryPseudofunctor B C)
    (X : B × DuskinOrdinal 1) : C :=
  if X.2.as = (0 : Fin 2) then P.obj X.1 else Q.obj X.1

private def cylinderMap
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (P Q : StrictlyUnitaryPseudofunctor B C)
    (η : Pseudofunctor.StrongTrans P.toPseudofunctor Q.toPseudofunctor)
    {X Y : B × DuskinOrdinal 1}
    (f : X ⟶ Y) : cylinderObj P Q X ⟶ cylinderObj P Q Y := by
  rcases X with ⟨X, ⟨i⟩⟩
  rcases Y with ⟨Y, ⟨j⟩⟩
  cases finTwoView i <;> cases finTwoView j
  · simpa [cylinderObj] using P.map f.1
  · simpa [cylinderObj] using (P.map f.1 ≫ η.app Y)
  · have hle : (1 : Fin 2) ≤ 0 := by simpa using f.2.as.le
    omega
  · simpa [cylinderObj] using Q.map f.1

private def cylinderMap₂
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (P Q : StrictlyUnitaryPseudofunctor B C)
    (η : Pseudofunctor.StrongTrans P.toPseudofunctor Q.toPseudofunctor)
    {X Y : B × DuskinOrdinal 1}
    {f g : X ⟶ Y}
    (α : f ⟶ g) :
    cylinderMap P Q η f ⟶ cylinderMap P Q η g := by
  rcases X with ⟨X, ⟨i⟩⟩
  rcases Y with ⟨Y, ⟨j⟩⟩
  cases finTwoView i <;> cases finTwoView j
  · simpa [cylinderMap, cylinderObj, finTwoView] using P.map₂ α.1
  · simpa [cylinderMap, cylinderObj, finTwoView] using (P.map₂ α.1 ▷ η.app Y)
  · have hle : (1 : Fin 2) ≤ 0 := by simpa using f.2.as.le
    omega
  · simpa [cylinderMap, cylinderObj, finTwoView] using Q.map₂ α.1

private def cylinderMapComp
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (P Q : StrictlyUnitaryPseudofunctor B C)
    (η : Pseudofunctor.StrongTrans P.toPseudofunctor Q.toPseudofunctor)
    {X Y Z : B × DuskinOrdinal 1}
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    cylinderMap P Q η (f ≫ g) ≅
      cylinderMap P Q η f ≫ cylinderMap P Q η g := by
  rcases X with ⟨X, ⟨i⟩⟩
  rcases Y with ⟨Y, ⟨j⟩⟩
  rcases Z with ⟨Z, ⟨k⟩⟩
  cases finTwoView i <;> cases finTwoView j <;> cases finTwoView k
  · simpa [cylinderMap, cylinderObj, finTwoView] using P.mapComp f.1 g.1
  · simpa [cylinderMap, cylinderObj, finTwoView] using
      (whiskerRightIso (P.mapComp f.1 g.1) (η.app Z) ≪≫
        α_ (P.map f.1) (P.map g.1) (η.app Z))
  · have hle : (1 : Fin 2) ≤ 0 := by simpa using g.2.as.le
    omega
  · simpa [cylinderMap, cylinderObj, finTwoView] using
      (whiskerRightIso (P.mapComp f.1 g.1) (η.app Z) ≪≫
        α_ (P.map f.1) (P.map g.1) (η.app Z) ≪≫
        whiskerLeftIso (P.map f.1) (η.naturality g.1) ≪≫
        (α_ (P.map f.1) (η.app Y) (Q.map g.1)).symm)
  · have hle : (1 : Fin 2) ≤ 0 := by simpa using f.2.as.le
    omega
  · have hle : (1 : Fin 2) ≤ 0 := by simpa using f.2.as.le
    omega
  · have hle : (1 : Fin 2) ≤ 0 := by simpa using g.2.as.le
    omega
  · simpa [cylinderMap, cylinderObj, finTwoView] using Q.mapComp f.1 g.1

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
    rcases X with ⟨X, ⟨i⟩⟩
    cases finTwoView i
    · simpa [cylinderMap, cylinderObj, finTwoView] using P.map_id X
    · simpa [cylinderMap, cylinderObj, finTwoView] using Q.map_id X
  map₂ := cylinderMap₂ P Q η
  map₂_id := by
    intro X Y f
    rcases X with ⟨X, ⟨i⟩⟩
    rcases Y with ⟨Y, ⟨j⟩⟩
    cases finTwoView i <;> cases finTwoView j
    · simpa [cylinderMap₂, cylinderMap, cylinderObj, finTwoView] using P.map₂_id f.1
    · simp [cylinderMap₂, cylinderMap, cylinderObj, finTwoView]
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using f.2.as.le
      omega
    · simpa [cylinderMap₂, cylinderMap, cylinderObj, finTwoView] using Q.map₂_id f.1
  map₂_comp := by
    intro X Y f g h α β
    rcases X with ⟨X, ⟨i⟩⟩
    rcases Y with ⟨Y, ⟨j⟩⟩
    cases finTwoView i <;> cases finTwoView j
    · simpa [cylinderMap₂, cylinderMap, cylinderObj, finTwoView] using P.map₂_comp α.1 β.1
    · simp [cylinderMap₂, cylinderMap, cylinderObj, finTwoView]
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using f.2.as.le
      omega
    · simpa [cylinderMap₂, cylinderMap, cylinderObj, finTwoView] using Q.map₂_comp α.1 β.1
  mapComp := cylinderMapComp P Q η
  map₂_whisker_left := by
    intro X Y Z f g h β
    rcases X with ⟨X, ⟨i⟩⟩
    rcases Y with ⟨Y, ⟨j⟩⟩
    rcases Z with ⟨Z, ⟨k⟩⟩
    cases finTwoView i <;> cases finTwoView j <;> cases finTwoView k
    · simpa [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj, finTwoView] using
        P.map₂_whisker_left f.1 β.1
    · simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj, finTwoView]
      bicategory
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using g.2.as.le
      omega
    · simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj, finTwoView]
      bicategory
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using f.2.as.le
      omega
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using f.2.as.le
      omega
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using g.2.as.le
      omega
    · simpa [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj, finTwoView] using
        Q.map₂_whisker_left f.1 β.1
  map₂_whisker_right := by
    intro X Y Z f g α h
    rcases X with ⟨X, ⟨i⟩⟩
    rcases Y with ⟨Y, ⟨j⟩⟩
    rcases Z with ⟨Z, ⟨k⟩⟩
    cases finTwoView i <;> cases finTwoView j <;> cases finTwoView k
    · simpa [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj, finTwoView] using
        P.map₂_whisker_right α.1 h.1
    · simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj, finTwoView]
      bicategory
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using h.2.as.le
      omega
    · have hnat := η.naturality_naturality α.1
      simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj, finTwoView, hnat]
      bicategory
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using f.2.as.le
      omega
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using f.2.as.le
      omega
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using h.2.as.le
      omega
    · simpa [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj, finTwoView] using
        Q.map₂_whisker_right α.1 h.1
  map₂_left_unitor := by
    intro X Y f
    rcases X with ⟨X, ⟨i⟩⟩
    rcases Y with ⟨Y, ⟨j⟩⟩
    cases finTwoView i <;> cases finTwoView j
    · simpa [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj, finTwoView,
        P.map_id] using P.map₂_left_unitor f.1
    · simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj, finTwoView]
      bicategory
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using f.2.as.le
      omega
    · simpa [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj, finTwoView,
        Q.map_id] using Q.map₂_left_unitor f.1
  map₂_right_unitor := by
    intro X Y f
    rcases X with ⟨X, ⟨i⟩⟩
    rcases Y with ⟨Y, ⟨j⟩⟩
    cases finTwoView i <;> cases finTwoView j
    · simpa [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj, finTwoView,
        P.map_id] using P.map₂_right_unitor f.1
    · simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj, finTwoView]
      bicategory
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using f.2.as.le
      omega
    · simpa [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj, finTwoView,
        Q.map_id] using Q.map₂_right_unitor f.1
  map₂_associator := by
    intro A B C D f g h
    rcases A with ⟨A, ⟨i⟩⟩
    rcases B with ⟨B, ⟨j⟩⟩
    rcases C with ⟨C, ⟨k⟩⟩
    rcases D with ⟨D, ⟨l⟩⟩
    cases finTwoView i <;> cases finTwoView j <;> cases finTwoView k <;> cases finTwoView l
    · simpa [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj, finTwoView] using
        P.map₂_associator f.1 g.1 h.1
    · simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj, finTwoView]
      bicategory
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using h.2.as.le
      omega
    · simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj, finTwoView]
      bicategory
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using g.2.as.le
      omega
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using g.2.as.le
      omega
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using h.2.as.le
      omega
    · simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj, finTwoView]
      bicategory
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using f.2.as.le
      omega
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using f.2.as.le
      omega
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using f.2.as.le
      omega
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using f.2.as.le
      omega
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using g.2.as.le
      omega
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using g.2.as.le
      omega
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using h.2.as.le
      omega
    · simpa [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj, finTwoView] using
        Q.map₂_associator f.1 g.1 h.1

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

@[simp] theorem strongTransformationNormalLaxCylinder_zero_obj
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (P Q : StrictlyUnitaryPseudofunctor B C)
    (η : Pseudofunctor.StrongTrans P.toPseudofunctor Q.toPseudofunctor)
    (X : B) :
    (strongTransformationNormalLaxCylinder P Q η).obj
      (X, LocallyDiscrete.mk (0 : Fin 2)) = P.obj X := by
  rfl

@[simp] theorem strongTransformationNormalLaxCylinder_one_obj
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (P Q : StrictlyUnitaryPseudofunctor B C)
    (η : Pseudofunctor.StrongTrans P.toPseudofunctor Q.toPseudofunctor)
    (X : B) :
    (strongTransformationNormalLaxCylinder P Q η).obj
      (X, LocallyDiscrete.mk (1 : Fin 2)) = Q.obj X := by
  rfl

set_option backward.defeqAttrib.useBackward true in
set_option backward.isDefEq.respectTransparency false in
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
    intro J σ
    apply StrictlyUnitaryLaxFunctor.ext
    case obj => rfl
    case map =>
      rw [heq_iff_eq]
      rfl
    case map₂ =>
      rw [heq_iff_eq]
      rfl
    case mapId =>
      rw [heq_iff_eq]
      funext X
      rw [((normalLaxPair σ (intervalNormalLax ((SSet.ι₀.app J σ).2))).comp
            (strongTransformationNormalLaxCylinder P Q η)).mapId_eq_eqToHom,
          (σ.comp P.toStrictlyUnitaryLaxFunctor).mapId_eq_eqToHom]
    case mapComp =>
      rw [heq_iff_eq]
      rfl
  endpoint_one := by
    intro J σ
    apply StrictlyUnitaryLaxFunctor.ext
    case obj => rfl
    case map =>
      rw [heq_iff_eq]
      rfl
    case map₂ =>
      rw [heq_iff_eq]
      rfl
    case mapId =>
      rw [heq_iff_eq]
      funext X
      rw [((normalLaxPair σ (intervalNormalLax ((SSet.ι₁.app J σ).2))).comp
            (strongTransformationNormalLaxCylinder P Q η)).mapId_eq_eqToHom,
          (σ.comp Q.toStrictlyUnitaryLaxFunctor).mapId_eq_eqToHom]
    case mapComp =>
      rw [heq_iff_eq]
      rfl

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
  let Q := StrictlyUnitaryPseudofunctor.id B
  simpa [P, Q, sourceRoundTripNormalLax] using
    strongTransformationDuskinCylinder P Q (sourcePseudoStrong K)

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
  let Q := StrictlyUnitaryPseudofunctor.id C
  simpa [P, Q, targetRoundTripNormalLax] using
    strongTransformationDuskinCylinder P Q (targetPseudoStrong K)

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

noncomputable def globalDuskinRoundTripPrismRealization
    {B C : Type u}
    [Bicategory.{w, v} B] [Bicategory.{w, v} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    (K : NormalizedCoherentQuasiInverse F G) :
    GlobalDuskinRoundTripPrismRealization K where
  sourcePrism := by
    rw [← normalLaxDuskinNerveMap_comp]
    exact (strongQuasiInverseNormalLaxCylinder K).sourcePrism
  targetPrism := by
    rw [← normalLaxDuskinNerveMap_comp]
    exact (strongQuasiInverseNormalLaxCylinder K).targetPrism

end KUOS.DependentOriginationStrongTransformationCylinderUncurryingV1_36