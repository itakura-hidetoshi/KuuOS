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

For strictly-unitary pseudofunctors `P Q : B -> C` and a native strong
transformation `η : P ==> Q`, this layer constructs the normal cylinder
`B × [1] -> C`.  The interval is normalized by cases on its actual `Fin 2`
object data.  This avoids proof-equality transports at the 0/1 boundary and
leaves the mixed composition laws exactly to the strong naturality of `η`.
-/

private def cylinderObj
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (P Q : StrictlyUnitaryPseudofunctor B C)
    (X : B × DuskinOrdinal 1) : C :=
  Fin.cases (P.obj X.1) (fun _ => Q.obj X.1) X.2.as

private def cylinderMap
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (P Q : StrictlyUnitaryPseudofunctor B C)
    (η : Pseudofunctor.StrongTrans P.toPseudofunctor Q.toPseudofunctor)
    {X Y : B × DuskinOrdinal 1}
    (f : X ⟶ Y) : cylinderObj P Q X ⟶ cylinderObj P Q Y := by
  rcases X with ⟨X, ⟨i⟩⟩
  rcases Y with ⟨Y, ⟨j⟩⟩
  cases i using Fin.cases
  · cases j using Fin.cases
    · exact P.map f.1
    · exact P.map f.1 ≫ η.app Y
  · cases j using Fin.cases
    · have hle := f.2.as.le
      simp at hle
    · exact Q.map f.1

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
  cases i using Fin.cases
  · cases j using Fin.cases
    · exact P.map₂ α.1
    · exact P.map₂ α.1 ▷ η.app Y
  · cases j using Fin.cases
    · have hle := f.2.as.le
      simp at hle
    · exact Q.map₂ α.1

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
  cases i using Fin.cases
  · cases j using Fin.cases
    · cases k using Fin.cases
      · exact P.mapComp f.1 g.1
      · exact
          whiskerRightIso (P.mapComp f.1 g.1) (η.app Z) ≪≫
            α_ (P.map f.1) (P.map g.1) (η.app Z)
    · cases k using Fin.cases
      · have hle := g.2.as.le
        simp at hle
      · exact
          whiskerRightIso (P.mapComp f.1 g.1) (η.app Z) ≪≫
            α_ (P.map f.1) (P.map g.1) (η.app Z) ≪≫
            whiskerLeftIso (P.map f.1) (η.naturality g.1) ≪≫
            (α_ (P.map f.1) (η.app Y) (Q.map g.1)).symm
  · cases j using Fin.cases
    · have hle := f.2.as.le
      simp at hle
    · cases k using Fin.cases
      · have hle := g.2.as.le
        simp at hle
      · exact Q.mapComp f.1 g.1

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
    fin_cases i
    · simpa [cylinderMap, cylinderObj] using P.map_id X
    · simpa [cylinderMap, cylinderObj] using Q.map_id X
  map₂ := cylinderMap₂ P Q η
  map₂_id := by
    intro X Y f
    rcases X with ⟨X, ⟨i⟩⟩
    rcases Y with ⟨Y, ⟨j⟩⟩
    fin_cases i <;> fin_cases j
    · simp [cylinderMap₂, cylinderMap, cylinderObj]
    · simp [cylinderMap₂, cylinderMap, cylinderObj]
    · have hle := f.2.as.le
      omega
    · simp [cylinderMap₂, cylinderMap, cylinderObj]
  map₂_comp := by
    intro X Y f g h α β
    rcases X with ⟨X, ⟨i⟩⟩
    rcases Y with ⟨Y, ⟨j⟩⟩
    fin_cases i <;> fin_cases j
    · simp [cylinderMap₂, cylinderMap, cylinderObj]
    · simp [cylinderMap₂, cylinderMap, cylinderObj, comp_whiskerRight]
    · have hle := f.2.as.le
      omega
    · simp [cylinderMap₂, cylinderMap, cylinderObj]
  mapComp := cylinderMapComp P Q η
  map₂_whisker_left := by
    intro X Y Z f g h β
    rcases X with ⟨X, ⟨i⟩⟩
    rcases Y with ⟨Y, ⟨j⟩⟩
    rcases Z with ⟨Z, ⟨k⟩⟩
    fin_cases i <;> fin_cases j <;> fin_cases k
    all_goals
      try
        have hf := f.2.as.le
        have hg := g.2.as.le
        omega
    · simpa [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj] using
        P.map₂_whisker_left f.1 β.1
    · simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj,
        P.map₂_whisker_left]
      bicategory
    · simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj,
        P.map₂_whisker_left]
      bicategory
    · simpa [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj] using
        Q.map₂_whisker_left f.1 β.1
  map₂_whisker_right := by
    intro X Y Z f g α h
    rcases X with ⟨X, ⟨i⟩⟩
    rcases Y with ⟨Y, ⟨j⟩⟩
    rcases Z with ⟨Z, ⟨k⟩⟩
    fin_cases i <;> fin_cases j <;> fin_cases k
    all_goals
      try
        have hf := f.2.as.le
        have hh := h.2.as.le
        omega
    · simpa [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj] using
        P.map₂_whisker_right α.1 h.1
    · simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj,
        P.map₂_whisker_right]
      bicategory
    · have hnat := η.naturality_naturality α.1
      simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj,
        P.map₂_whisker_right, hnat]
      bicategory
    · simpa [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj] using
        Q.map₂_whisker_right α.1 h.1
  map₂_left_unitor := by
    intro X Y f
    rcases X with ⟨X, ⟨i⟩⟩
    rcases Y with ⟨Y, ⟨j⟩⟩
    fin_cases i <;> fin_cases j
    · simpa [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj,
        P.map_id] using P.map₂_left_unitor f.1
    · simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj,
        P.map_id, P.map₂_left_unitor]
      bicategory
    · have hle := f.2.as.le
      omega
    · simpa [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj,
        Q.map_id] using Q.map₂_left_unitor f.1
  map₂_right_unitor := by
    intro X Y f
    rcases X with ⟨X, ⟨i⟩⟩
    rcases Y with ⟨Y, ⟨j⟩⟩
    fin_cases i <;> fin_cases j
    · simpa [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj,
        P.map_id] using P.map₂_right_unitor f.1
    · simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj,
        P.map_id, Q.map_id,
        P.map₂_right_unitor, Pseudofunctor.StrongTrans.naturality_id_hom]
      bicategory
    · have hle := f.2.as.le
      omega
    · simpa [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj,
        Q.map_id] using Q.map₂_right_unitor f.1
  map₂_associator := by
    intro A B C D f g h
    rcases A with ⟨A, ⟨i⟩⟩
    rcases B with ⟨B, ⟨j⟩⟩
    rcases C with ⟨C, ⟨k⟩⟩
    rcases D with ⟨D, ⟨l⟩⟩
    fin_cases i <;> fin_cases j <;> fin_cases k <;> fin_cases l
    all_goals
      try
        have hf := f.2.as.le
        have hg := g.2.as.le
        have hh := h.2.as.le
        omega
    · simpa [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj] using
        P.map₂_associator f.1 g.1 h.1
    · simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj,
        P.map₂_associator]
      bicategory
    · simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj,
        P.map₂_associator,
        Pseudofunctor.StrongTrans.naturality_comp_hom]
      bicategory
    · simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj,
        P.map₂_associator,
        Pseudofunctor.StrongTrans.naturality_comp_hom]
      bicategory
    · simpa [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj] using
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
    intro J σ
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
    intro J σ
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
    {B C : Type u}
    [Bicategory.{w, v} B] [Bicategory.{w, v} C]
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
-/

end KUOS.DependentOriginationStrongTransformationCylinderUncurryingV1_36