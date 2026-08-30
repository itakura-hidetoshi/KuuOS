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

universe u u₁ u₂ u₃ v v₁ v₂ v₃ w w₁ w₂ w₃

/-!
# Strong-transformation cylinder uncurrying v1.36

A native strong transformation between strictly-unitary pseudofunctors gives a
normal cylinder over the walking interval. Endpoint classification is stored
in an ordinary `Type` whose constructors expose the endpoint equality directly.
This permits Type-valued elimination while leaving `subst` an actual equality.
-/

private inductive FinTwoCases (i : Fin 2) : Type where
  | zero (h : i = 0)
  | one (h : i = 1)

private def finTwoCases (i : Fin 2) : FinTwoCases i :=
  if h : i = 0 then .zero h else .one (by omega)

private abbrev cylinderObj
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
  rcases finTwoCases i with ⟨hi⟩ | ⟨hi⟩ <;> subst i <;>
    rcases finTwoCases j with ⟨hj⟩ | ⟨hj⟩ <;> subst j
  · exact P.map f.1
  · exact P.map f.1 ≫ η.app Y
  · have hle : (1 : Fin 2) ≤ 0 := by simpa using f.2.as.le
    omega
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
  rcases finTwoCases i with ⟨hi⟩ | ⟨hi⟩ <;> subst i <;>
    rcases finTwoCases j with ⟨hj⟩ | ⟨hj⟩ <;> subst j
  · exact P.map₂ α.1
  · exact P.map₂ α.1 ▷ η.app Y
  · have hle : (1 : Fin 2) ≤ 0 := by simpa using f.2.as.le
    omega
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
  rcases finTwoCases i with ⟨hi⟩ | ⟨hi⟩ <;> subst i <;>
    rcases finTwoCases j with ⟨hj⟩ | ⟨hj⟩ <;> subst j <;>
      rcases finTwoCases k with ⟨hk⟩ | ⟨hk⟩ <;> subst k
  · exact P.mapComp f.1 g.1
  · exact
      whiskerRightIso (P.mapComp f.1 g.1) (η.app Z) ≪≫
        α_ (P.map f.1) (P.map g.1) (η.app Z)
  · have hle : (1 : Fin 2) ≤ 0 := by simpa using g.2.as.le
    omega
  · exact
      whiskerRightIso (P.mapComp f.1 g.1) (η.app Z) ≪≫
        α_ (P.map f.1) (P.map g.1) (η.app Z) ≪≫
        whiskerLeftIso (P.map f.1) (η.naturality g.1) ≪≫
        (α_ (P.map f.1) (η.app Y) (Q.map g.1)).symm
  · have hle : (1 : Fin 2) ≤ 0 := by simpa using f.2.as.le
    omega
  · have hle : (1 : Fin 2) ≤ 0 := by simpa using f.2.as.le
    omega
  · have hle : (1 : Fin 2) ≤ 0 := by simpa using g.2.as.le
    omega
  · exact Q.mapComp f.1 g.1

/-- Exchange of two 2-cells, written in the fully associated form used by the cylinder core. -/
private theorem whiskerExchangeConjugation
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {A B C₀ C₁ D : C}
    {f g : A ⟶ B} (μ : f ⟶ g)
    (h : B ⟶ C₀) (k : C₀ ⟶ D)
    (i : B ⟶ C₁) (j : C₁ ⟶ D)
    (θ : h ≫ k ≅ i ≫ j) :
    μ ▷ h ▷ k =
      (α_ f h k).hom ≫ f ◁ θ.hom ≫ (α_ f i j).inv ≫
        μ ▷ i ▷ j ≫ (α_ g i j).hom ≫ g ◁ θ.inv ≫ (α_ g h k).inv := by
  rw [← cancel_epi (α_ f h k).inv,
    ← cancel_mono (α_ g h k).hom,
    ← cancel_mono (g ◁ θ.hom)]
  simpa [Category.assoc] using (Bicategory.whisker_exchange μ θ.hom).symm

set_option backward.defeqAttrib.useBackward true in
set_option backward.isDefEq.respectTransparency false in
set_option maxHeartbeats 1000000 in
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
    rcases finTwoCases i with ⟨hi⟩ | ⟨hi⟩ <;> subst i
    · exact P.map_id X
    · exact Q.map_id X
  map₂ := cylinderMap₂ P Q η
  map₂_id := by
    intro X Y f
    rcases X with ⟨X, ⟨i⟩⟩
    rcases Y with ⟨Y, ⟨j⟩⟩
    rcases finTwoCases i with ⟨hi⟩ | ⟨hi⟩ <;> subst i <;>
      rcases finTwoCases j with ⟨hj⟩ | ⟨hj⟩ <;> subst j
    · exact P.map₂_id f.1
    · change P.map₂ (𝟙 f.1) ▷ η.app Y = 𝟙 (P.map f.1 ≫ η.app Y)
      rw [P.map₂_id]
      simp
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using f.2.as.le
      omega
    · exact Q.map₂_id f.1
  map₂_comp := by
    intro X Y f g h α β
    rcases X with ⟨X, ⟨i⟩⟩
    rcases Y with ⟨Y, ⟨j⟩⟩
    rcases finTwoCases i with ⟨hi⟩ | ⟨hi⟩ <;> subst i <;>
      rcases finTwoCases j with ⟨hj⟩ | ⟨hj⟩ <;> subst j
    · exact P.map₂_comp α.1 β.1
    · change P.map₂ (α.1 ≫ β.1) ▷ η.app Y =
        (P.map₂ α.1 ▷ η.app Y) ≫ (P.map₂ β.1 ▷ η.app Y)
      rw [P.map₂_comp]
      simp
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using f.2.as.le
      omega
    · exact Q.map₂_comp α.1 β.1
  mapComp := cylinderMapComp P Q η
  map₂_whisker_left := by
    intro X Y Z f g h β
    rcases X with ⟨X, ⟨i⟩⟩
    rcases Y with ⟨Y, ⟨j⟩⟩
    rcases Z with ⟨Z, ⟨k⟩⟩
    rcases finTwoCases i with ⟨hi⟩ | ⟨hi⟩ <;> subst i <;>
      rcases finTwoCases j with ⟨hj⟩ | ⟨hj⟩ <;> subst j <;>
        rcases finTwoCases k with ⟨hk⟩ | ⟨hk⟩ <;> subst k
    · exact P.map₂_whisker_left f.1 β.1
    · simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj, finTwoCases,
        P.map₂_whisker_left] <;> bicategory
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using g.2.as.le
      omega
    · have hnat :
          P.map₂ β.1 ▷ η.app Z =
            (η.naturality g.1).hom ≫ η.app Y ◁ Q.map₂ β.1 ≫
              (η.naturality h.1).inv := by
        rw [← cancel_mono (η.naturality h.1).hom]
        simpa [Category.assoc] using η.naturality_naturality β.1
      simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj, finTwoCases,
        P.map₂_whisker_left, hnat] <;> bicategory
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using f.2.as.le
      omega
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using f.2.as.le
      omega
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using g.2.as.le
      omega
    · exact Q.map₂_whisker_left f.1 β.1
  map₂_whisker_right := by
    intro X Y Z f g α h
    rcases X with ⟨X, ⟨i⟩⟩
    rcases Y with ⟨Y, ⟨j⟩⟩
    rcases Z with ⟨Z, ⟨k⟩⟩
    rcases finTwoCases i with ⟨hi⟩ | ⟨hi⟩ <;> subst i <;>
      rcases finTwoCases j with ⟨hj⟩ | ⟨hj⟩ <;> subst j <;>
        rcases finTwoCases k with ⟨hk⟩ | ⟨hk⟩ <;> subst k
    · exact P.map₂_whisker_right α.1 h.1
    · simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj, finTwoCases,
        P.map₂_whisker_right] <;> bicategory
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using h.2.as.le
      omega
    · have hconj := whiskerExchangeConjugation (μ := P.map₂ α.1)
        (P.map h.1) (η.app Z) (η.app Y) (Q.map h.1) (η.naturality h.1)
      simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj, finTwoCases,
        P.map₂_whisker_right]
      rw [hconj]
      bicategory
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using f.2.as.le
      omega
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using f.2.as.le
      omega
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using h.2.as.le
      omega
    · exact Q.map₂_whisker_right α.1 h.1
  map₂_left_unitor := by
    intro X Y f
    rcases X with ⟨X, ⟨i⟩⟩
    rcases Y with ⟨Y, ⟨j⟩⟩
    rcases finTwoCases i with ⟨hi⟩ | ⟨hi⟩ <;> subst i <;>
      rcases finTwoCases j with ⟨hj⟩ | ⟨hj⟩ <;> subst j
    · simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj, finTwoCases,
        P.map₂_left_unitor, P.mapId_eq_eqToIso] <;> bicategory
    · simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj, finTwoCases,
        P.map₂_left_unitor, P.mapId_eq_eqToIso]
      rw [P.map_id X]
      bicategory
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using f.2.as.le
      omega
    · simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj, finTwoCases,
        Q.map₂_left_unitor, Q.mapId_eq_eqToIso] <;> bicategory
  map₂_right_unitor := by
    intro X Y f
    rcases X with ⟨X, ⟨i⟩⟩
    rcases Y with ⟨Y, ⟨j⟩⟩
    rcases finTwoCases i with ⟨hi⟩ | ⟨hi⟩ <;> subst i <;>
      rcases finTwoCases j with ⟨hj⟩ | ⟨hj⟩ <;> subst j
    · simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj, finTwoCases,
        P.map₂_right_unitor, P.mapId_eq_eqToIso] <;> bicategory
    · simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj, finTwoCases,
        P.map₂_right_unitor, P.mapId_eq_eqToIso, Q.mapId_eq_eqToIso,
        Pseudofunctor.StrongTrans.naturality_id_hom]
      rw [P.map_id Y, Q.map_id Y]
      bicategory
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using f.2.as.le
      omega
    · simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj, finTwoCases,
        Q.map₂_right_unitor, Q.mapId_eq_eqToIso] <;> bicategory
  map₂_associator := by
    intro A B C D f g h
    rcases A with ⟨A, ⟨i⟩⟩
    rcases B with ⟨B, ⟨j⟩⟩
    rcases C with ⟨C, ⟨k⟩⟩
    rcases D with ⟨D, ⟨l⟩⟩
    rcases finTwoCases i with ⟨hi⟩ | ⟨hi⟩ <;> subst i <;>
      rcases finTwoCases j with ⟨hj⟩ | ⟨hj⟩ <;> subst j <;>
        rcases finTwoCases k with ⟨hk⟩ | ⟨hk⟩ <;> subst k <;>
          rcases finTwoCases l with ⟨hl⟩ | ⟨hl⟩ <;> subst l
    · simpa [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj, finTwoCases] using
        P.map₂_associator f.1 g.1 h.1
    · simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj, finTwoCases,
        P.map₂_associator] <;> bicategory
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using h.2.as.le
      omega
    · have hconj := whiskerExchangeConjugation (μ := (P.mapComp f.1 g.1).hom)
        (P.map h.1) (η.app D) (η.app C) (Q.map h.1) (η.naturality h.1)
      simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj, finTwoCases,
        P.map₂_associator]
      rw [hconj]
      bicategory
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using g.2.as.le
      omega
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using g.2.as.le
      omega
    · have hle : (1 : Fin 2) ≤ 0 := by simpa using h.2.as.le
      omega
    · have hconj := whiskerExchangeConjugation (μ := (P.mapComp f.1 g.1).hom)
        (P.map h.1) (η.app D) (η.app C) (Q.map h.1) (η.naturality h.1)
      simp [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj, finTwoCases,
        P.map₂_associator, Pseudofunctor.StrongTrans.naturality_comp_inv]
      rw [hconj]
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
    · simpa [cylinderMapComp, cylinderMap₂, cylinderMap, cylinderObj, finTwoCases] using
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

set_option backward.defeqAttrib.useBackward true in
set_option backward.isDefEq.respectTransparency false in
private theorem pseudofunctor_comp_to_lax
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {D : Type u₃} [Bicategory.{w₃, v₃} D]
    (P : StrictlyUnitaryPseudofunctor B C)
    (Q : StrictlyUnitaryPseudofunctor C D) :
    (P.comp Q).toStrictlyUnitaryLaxFunctor =
      P.toStrictlyUnitaryLaxFunctor.comp Q.toStrictlyUnitaryLaxFunctor := by
  apply StrictlyUnitaryLaxFunctor.ext
  case obj => rfl
  case map => rw [heq_iff_eq]; rfl
  case map₂ => rw [heq_iff_eq]; rfl
  case mapId =>
    rw [heq_iff_eq]
    funext X
    rw [((P.comp Q).toStrictlyUnitaryLaxFunctor).mapId_eq_eqToHom,
      (P.toStrictlyUnitaryLaxFunctor.comp Q.toStrictlyUnitaryLaxFunctor).mapId_eq_eqToHom]
  case mapComp => rw [heq_iff_eq]; rfl

set_option backward.defeqAttrib.useBackward true in
set_option backward.isDefEq.respectTransparency false in
private theorem pseudofunctor_id_to_lax
    (B : Type u₁) [Bicategory.{w₁, v₁} B] :
    (StrictlyUnitaryPseudofunctor.id B).toStrictlyUnitaryLaxFunctor =
      StrictlyUnitaryLaxFunctor.id B := by
  apply StrictlyUnitaryLaxFunctor.ext
  case obj => rfl
  case map => rw [heq_iff_eq]; rfl
  case map₂ => rw [heq_iff_eq]; rfl
  case mapId =>
    rw [heq_iff_eq]
    funext X
    rw [((StrictlyUnitaryPseudofunctor.id B).toStrictlyUnitaryLaxFunctor).mapId_eq_eqToHom,
      (StrictlyUnitaryLaxFunctor.id B).mapId_eq_eqToHom]
  case mapComp => rw [heq_iff_eq]; rfl

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
  simpa [P, Q, sourceRoundTripNormalLax, pseudofunctor_comp_to_lax,
    pseudofunctor_id_to_lax] using
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
  simpa [P, Q, targetRoundTripNormalLax, pseudofunctor_comp_to_lax,
    pseudofunctor_id_to_lax] using
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

private theorem normalLaxDuskinNerveMap_forward_eq_normalized
    {B C : Type u}
    [Bicategory.{w, v} B] [Bicategory.{w, v} C]
    (E : StrictlyUnitaryBicategoricalModelEquivalence B C) :
    normalLaxDuskinNerveMap E.forward.toStrictlyUnitaryLaxFunctor =
      normalizedDuskinNerveMap E := by
  ext J σ
  rfl

noncomputable def globalDuskinRoundTripPrismRealization
    {B C : Type u}
    [Bicategory.{w, v} B] [Bicategory.{w, v} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    (K : NormalizedCoherentQuasiInverse F G) :
    GlobalDuskinRoundTripPrismRealization K where
  sourcePrism := by
    rw [← normalLaxDuskinNerveMap_forward_eq_normalized F,
      ← normalLaxDuskinNerveMap_forward_eq_normalized G,
      ← normalLaxDuskinNerveMap_comp]
    exact (strongQuasiInverseNormalLaxCylinder K).sourcePrism
  targetPrism := by
    rw [← normalLaxDuskinNerveMap_forward_eq_normalized G,
      ← normalLaxDuskinNerveMap_forward_eq_normalized F,
      ← normalLaxDuskinNerveMap_comp]
    exact (strongQuasiInverseNormalLaxCylinder K).targetPrism

end KUOS.DependentOriginationStrongTransformationCylinderUncurryingV1_36