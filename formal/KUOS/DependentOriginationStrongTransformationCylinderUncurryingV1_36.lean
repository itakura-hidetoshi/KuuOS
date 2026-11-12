import KUOS.DependentOriginationStrongTransformationDuskinCylinderV1_35
import Mathlib.Tactic
import KUOS.DependentOriginationMixedWhiskerPastingV1_36
import KUOS.DependentOriginationMixedLeftUnitorPastingV1_36
import KUOS.DependentOriginationMixedRightUnitorPastingV1_36

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
  have hx1 : X.as = (1 : Fin 2) := by
    apply Fin.ext
    change (X.as).val = 1
    have hlt : (X.as).val < 2 := (X.as).isLt
    have hval0 : (X.as).val ≠ 0 := by
      intro hv
      apply hX
      apply Fin.ext
      simpa using hv
    omega
  rw [hx1, hY] at hle
  exact (by decide : ¬ ((1 : Fin 2) ≤ (0 : Fin 2))) hle

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
  -- Fin.cases eliminates interval vertices in Type, unlike fin_cases,
  -- whose finite-enumeration membership elimination is restricted to Prop.
  rcases X with ⟨x, ⟨i⟩⟩
  rcases Y with ⟨y, ⟨j⟩⟩
  cases i using Fin.cases with
  | zero =>
      cases j using Fin.cases with
      | zero =>
          simpa [cylinderMap, cylinderObj] using P.map₂ α.1
      | succ j =>
          have hj : j = (0 : Fin 1) := Subsingleton.elim _ _
          subst j
          simpa [cylinderMap, cylinderObj] using (P.map₂ α.1 ▷ η.app y)
  | succ i =>
      have hi : i = (0 : Fin 1) := Subsingleton.elim _ _
      subst i
      cases j using Fin.cases with
      | zero =>
          exact False.elim
            ((by decide : ¬ ((1 : Fin 2) ≤ (0 : Fin 2))) f.2.as.le)
      | succ j =>
          have hj : j = (0 : Fin 1) := Subsingleton.elim _ _
          subst j
          simpa [cylinderMap, cylinderObj] using Q.map₂ α.1

private def cylinderMapComp
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (P Q : StrictlyUnitaryPseudofunctor B C)
    (η : Pseudofunctor.StrongTrans P.toPseudofunctor Q.toPseudofunctor)
    {X Y Z : B × DuskinOrdinal 1}
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    cylinderMap P Q η (f ≫ g) ≅
      cylinderMap P Q η f ≫ cylinderMap P Q η g := by
  -- Eliminate the actual interval vertices so the required isomorphism
  -- has the original 1-morphism endpoints, not proof-dependent casts.
  rcases X with ⟨x, ⟨i⟩⟩
  rcases Y with ⟨y, ⟨j⟩⟩
  rcases Z with ⟨z, ⟨k⟩⟩
  cases i using Fin.cases with
  | zero =>
      cases j using Fin.cases with
      | zero =>
          cases k using Fin.cases with
          | zero =>
              simpa [cylinderMap, cylinderObj] using P.mapComp f.1 g.1
          | succ k =>
              have hk : k = (0 : Fin 1) := Subsingleton.elim _ _
              subst k
              simpa [cylinderMap, cylinderObj] using
                (whiskerRightIso (P.mapComp f.1 g.1) (η.app z) ≪≫
                  α_ (P.map f.1) (P.map g.1) (η.app z))
      | succ j =>
          have hj : j = (0 : Fin 1) := Subsingleton.elim _ _
          subst j
          cases k using Fin.cases with
          | zero =>
              exact False.elim
                ((by decide : ¬ ((1 : Fin 2) ≤ (0 : Fin 2))) g.2.as.le)
          | succ k =>
              have hk : k = (0 : Fin 1) := Subsingleton.elim _ _
              subst k
              simpa [cylinderMap, cylinderObj] using
                (whiskerRightIso (P.mapComp f.1 g.1) (η.app z) ≪≫
                  α_ (P.map f.1) (P.map g.1) (η.app z) ≪≫
                  whiskerLeftIso (P.map f.1) (η.naturality g.1) ≪≫
                  (α_ (P.map f.1) (η.app y) (Q.map g.1)).symm)
  | succ i =>
      have hi : i = (0 : Fin 1) := Subsingleton.elim _ _
      subst i
      cases j using Fin.cases with
      | zero =>
          exact False.elim
            ((by decide : ¬ ((1 : Fin 2) ≤ (0 : Fin 2))) f.2.as.le)
      | succ j =>
          have hj : j = (0 : Fin 1) := Subsingleton.elim _ _
          subst j
          cases k using Fin.cases with
          | zero =>
              exact False.elim
                ((by decide : ¬ ((1 : Fin 2) ≤ (0 : Fin 2))) g.2.as.le)
          | succ k =>
              have hk : k = (0 : Fin 1) := Subsingleton.elim _ _
              subst k
              simpa [cylinderMap, cylinderObj] using Q.mapComp f.1 g.1

private def strongCylinderCore
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (P Q : StrictlyUnitaryPseudofunctor B C)
    (η : Pseudofunctor.StrongTrans P.toPseudofunctor Q.toPseudofunctor) :
    StrictlyUnitaryPseudofunctorCore (B × DuskinOrdinal 1) C where
  obj := cylinderObj P Q
  map := cylinderMap P Q η
  map_id := by
    -- Eliminate the interval vertex before unfolding the dependent object map:
    -- a symbolic if/transport leaves a cast that simp cannot identify with id.
    rintro ⟨x, ⟨i⟩⟩
    cases i using Fin.cases with
    | zero =>
        simpa [cylinderMap, cylinderObj] using P.map_id x
    | succ i =>
        have hi : i = (0 : Fin 1) := Subsingleton.elim _ _
        subst i
        simpa [cylinderMap, cylinderObj] using Q.map_id x
  map₂ := cylinderMap₂ P Q η
  map₂_id := by
    -- Reduce at literal endpoints before applying the original functor law.
    -- change uses definitional equality without simplifying its proof to True.
    rintro ⟨x, ⟨i⟩⟩ ⟨y, ⟨j⟩⟩ f
    cases i using Fin.cases with
    | zero =>
        cases j using Fin.cases with
        | zero =>
            change P.map₂ (𝟙 f.1) = 𝟙 (P.map f.1)
            exact P.map₂_id f.1
        | succ j =>
            have hj : j = (0 : Fin 1) := Subsingleton.elim _ _
            subst j
            change P.map₂ (𝟙 f.1) ▷ η.app y = 𝟙 (P.map f.1 ≫ η.app y)
            simp only [P.map₂_id, id_whiskerRight]
    | succ i =>
        have hi : i = (0 : Fin 1) := Subsingleton.elim _ _
        subst i
        cases j using Fin.cases with
        | zero =>
            exact False.elim
              ((by decide : ¬ ((1 : Fin 2) ≤ (0 : Fin 2))) f.2.as.le)
        | succ j =>
            have hj : j = (0 : Fin 1) := Subsingleton.elim _ _
            subst j
            change Q.map₂ (𝟙 f.1) = 𝟙 (Q.map f.1)
            exact Q.map₂_id f.1
  map₂_comp := by
    -- First reduce the dependent interval eliminators at actual vertices.
    -- The mixed case is exactly functoriality followed by right whiskering.
    rintro ⟨x, ⟨i⟩⟩ ⟨y, ⟨j⟩⟩ f g h α β
    cases i using Fin.cases with
    | zero =>
        cases j using Fin.cases with
        | zero =>
            change P.map₂ (α.1 ≫ β.1) = P.map₂ α.1 ≫ P.map₂ β.1
            exact P.map₂_comp α.1 β.1
        | succ j =>
            have hj : j = (0 : Fin 1) := Subsingleton.elim _ _
            subst j
            change P.map₂ (α.1 ≫ β.1) ▷ η.app y =
              (P.map₂ α.1 ▷ η.app y) ≫ (P.map₂ β.1 ▷ η.app y)
            simp only [P.map₂_comp, comp_whiskerRight]
    | succ i =>
        have hi : i = (0 : Fin 1) := Subsingleton.elim _ _
        subst i
        cases j using Fin.cases with
        | zero =>
            exact False.elim
              ((by decide : ¬ ((1 : Fin 2) ≤ (0 : Fin 2))) f.2.as.le)
        | succ j =>
            have hj : j = (0 : Fin 1) := Subsingleton.elim _ _
            subst j
            change Q.map₂ (α.1 ≫ β.1) = Q.map₂ α.1 ≫ Q.map₂ β.1
            exact Q.map₂_comp α.1 β.1
  mapComp := cylinderMapComp P Q η
  map₂_whisker_left := by
    -- Eliminate the actual interval vertices before simplifying dependent maps.
    -- An if-case hypothesis alone does not reduce the Fin.cases motives.
    rintro ⟨x, ⟨i⟩⟩ ⟨y, ⟨j⟩⟩ ⟨z, ⟨k⟩⟩ f g h β
    cases i using Fin.cases with
    | zero =>
        cases j using Fin.cases with
        | zero =>
            cases k using Fin.cases with
            | zero =>
                change P.map₂ (f.1 ◁ β.1) =
                  (P.mapComp f.1 g.1).hom ≫
                    P.map f.1 ◁ P.map₂ β.1 ≫ (P.mapComp f.1 h.1).inv
                exact P.map₂_whisker_left f.1 β.1
            | succ k =>
                have hk : k = (0 : Fin 1) := Subsingleton.elim _ _
                subst k
                change P.map₂ (f.1 ◁ β.1) ▷ η.app z =
                  (whiskerRightIso (P.mapComp f.1 g.1) (η.app z) ≪≫
                    α_ (P.map f.1) (P.map g.1) (η.app z)).hom ≫
                    P.map f.1 ◁ (P.map₂ β.1 ▷ η.app z) ≫
                  (whiskerRightIso (P.mapComp f.1 h.1) (η.app z) ≪≫
                    α_ (P.map f.1) (P.map h.1) (η.app z)).inv
                -- Do not rewrite beneath a dependent whisker using rw:
                -- transport the exact two-cell equality and then normalize.
                calc
                  P.map₂ (f.1 ◁ β.1) ▷ η.app z =
                      ((P.mapComp f.1 g.1).hom ≫
                        P.map f.1 ◁ P.map₂ β.1 ≫
                        (P.mapComp f.1 h.1).inv) ▷ η.app z := by
                        exact congrArg (fun θ => θ ▷ η.app z)
                          (P.map₂_whisker_left f.1 β.1)
                  _ = _ := by
                    -- Normalize composite Iso.hom/Iso.inv constructors first:
                    -- the pinned coherence tactic only handles atomic isomorphisms.
                    dsimp
                    bicategory
        | succ j =>
            have hj : j = (0 : Fin 1) := Subsingleton.elim _ _
            subst j
            cases k using Fin.cases with
            | zero =>
                exact False.elim
                  ((by decide : ¬ ((1 : Fin 2) ≤ (0 : Fin 2))) g.2.as.le)
            | succ k =>
                have hk : k = (0 : Fin 1) := Subsingleton.elim _ _
                subst k
                have hnat := η.naturality_naturality β.1
                change P.map₂ (f.1 ◁ β.1) ▷ η.app z =
                  (whiskerRightIso (P.mapComp f.1 g.1) (η.app z) ≪≫
                    α_ (P.map f.1) (P.map g.1) (η.app z) ≪≫
                    whiskerLeftIso (P.map f.1) (η.naturality g.1) ≪≫
                    (α_ (P.map f.1) (η.app y) (Q.map g.1)).symm).hom ≫
                    (P.map f.1 ≫ η.app y) ◁ Q.map₂ β.1 ≫
                  (whiskerRightIso (P.mapComp f.1 h.1) (η.app z) ≪≫
                    α_ (P.map f.1) (P.map h.1) (η.app z) ≪≫
                    whiskerLeftIso (P.map f.1) (η.naturality h.1) ≪≫
                    (α_ (P.map f.1) (η.app y) (Q.map h.1)).symm).inv
                have hstep :
                    P.map₂ β.1 ▷ η.app z =
                      (η.naturality g.1).hom ≫
                        (η.app y ◁ Q.map₂ β.1) ≫
                        (η.naturality h.1).inv := by
                  have hh := congrArg
                    (fun θ => θ ≫ (η.naturality h.1).inv) hnat
                  calc
                    P.map₂ β.1 ▷ η.app z =
                      (P.map₂ β.1 ▷ η.app z) ≫
                        (η.naturality h.1).hom ≫
                        (η.naturality h.1).inv := by
                          simp [Category.assoc]
                    _ = _ := by
                      -- Beta-reduce congrArg's function application without
                      -- simplifying the original naturality witness to True.
                      simpa only [Category.assoc] using hh
                calc
                  P.map₂ (f.1 ◁ β.1) ▷ η.app z =
                      ((P.mapComp f.1 g.1).hom ≫
                        P.map f.1 ◁ P.map₂ β.1 ≫
                        (P.mapComp f.1 h.1).inv) ▷ η.app z := by
                          exact congrArg (fun θ => θ ▷ η.app z)
                            (P.map₂_whisker_left f.1 β.1)
                  _ = _ := by
                    dsimp
                    simp [hstep] <;> bicategory
    | succ i =>
        have hi : i = (0 : Fin 1) := Subsingleton.elim _ _
        subst i
        cases j using Fin.cases with
        | zero =>
            exact False.elim
              ((by decide : ¬ ((1 : Fin 2) ≤ (0 : Fin 2))) f.2.as.le)
        | succ j =>
            have hj : j = (0 : Fin 1) := Subsingleton.elim _ _
            subst j
            cases k using Fin.cases with
            | zero =>
                exact False.elim
                  ((by decide : ¬ ((1 : Fin 2) ≤ (0 : Fin 2))) g.2.as.le)
            | succ k =>
                have hk : k = (0 : Fin 1) := Subsingleton.elim _ _
                subst k
                change Q.map₂ (f.1 ◁ β.1) =
                  (Q.mapComp f.1 g.1).hom ≫
                    Q.map f.1 ◁ Q.map₂ β.1 ≫ (Q.mapComp f.1 h.1).inv
                exact Q.map₂_whisker_left f.1 β.1
  map₂_whisker_right := by
    -- The interval vertices must be eliminated before the dependent
    -- cylinderMap₂ motive reduces to the original pseudofunctor law.
    rintro ⟨x, ⟨i⟩⟩ ⟨y, ⟨j⟩⟩ ⟨z, ⟨k⟩⟩ f g α h
    cases i using Fin.cases with
    | zero =>
        cases j using Fin.cases with
        | zero =>
            cases k using Fin.cases with
            | zero =>
                change P.map₂ (α.1 ▷ h.1) =
                  (P.mapComp f.1 h.1).hom ≫
                    P.map₂ α.1 ▷ P.map h.1 ≫ (P.mapComp g.1 h.1).inv
                exact P.map₂_whisker_right α.1 h.1
            | succ k =>
                have hk : k = (0 : Fin 1) := Subsingleton.elim _ _
                subst k
                change P.map₂ (α.1 ▷ h.1) ▷ η.app z =
                  (whiskerRightIso (P.mapComp f.1 h.1) (η.app z) ≪≫
                    α_ (P.map f.1) (P.map h.1) (η.app z)).hom ≫
                    (P.map₂ α.1 ▷ (P.map h.1 ≫ η.app z)) ≫
                  (whiskerRightIso (P.mapComp g.1 h.1) (η.app z) ≪≫
                    α_ (P.map g.1) (P.map h.1) (η.app z)).inv
                calc
                  P.map₂ (α.1 ▷ h.1) ▷ η.app z =
                      ((P.mapComp f.1 h.1).hom ≫
                        P.map₂ α.1 ▷ P.map h.1 ≫
                        (P.mapComp g.1 h.1).inv) ▷ η.app z := by
                        exact congrArg (fun θ => θ ▷ η.app z)
                          (P.map₂_whisker_right α.1 h.1)
                  _ = _ := by
                    dsimp
                    bicategory
        | succ j =>
            have hj : j = (0 : Fin 1) := Subsingleton.elim _ _
            subst j
            cases k using Fin.cases with
            | zero =>
                exact False.elim
                  ((by decide : ¬ ((1 : Fin 2) ≤ (0 : Fin 2))) h.2.as.le)
            | succ k =>
                have hk : k = (0 : Fin 1) := Subsingleton.elim _ _
                subst k
                change P.map₂ (α.1 ▷ h.1) ▷ η.app z =
                  (whiskerRightIso (P.mapComp f.1 h.1) (η.app z) ≪≫
                    α_ (P.map f.1) (P.map h.1) (η.app z) ≪≫
                    whiskerLeftIso (P.map f.1) (η.naturality h.1) ≪≫
                    (α_ (P.map f.1) (η.app y) (Q.map h.1)).symm).hom ≫
                    ((P.map₂ α.1 ▷ η.app y) ▷ Q.map h.1) ≫
                  (whiskerRightIso (P.mapComp g.1 h.1) (η.app z) ≪≫
                    α_ (P.map g.1) (P.map h.1) (η.app z) ≪≫
                    whiskerLeftIso (P.map g.1) (η.naturality h.1) ≪≫
                    (α_ (P.map g.1) (η.app y) (Q.map h.1)).symm).inv
                calc
                  P.map₂ (α.1 ▷ h.1) ▷ η.app z =
                      ((P.mapComp f.1 h.1).hom ≫
                        P.map₂ α.1 ▷ P.map h.1 ≫
                        (P.mapComp g.1 h.1).inv) ▷ η.app z := by
                        exact congrArg (fun θ => θ ▷ η.app z)
                          (P.map₂_whisker_right α.1 h.1)
                  _ = _ :=
                    KUOS.DependentOriginationMixedWhiskerPastingV1_36.mixedRightWhiskerPasting
                      (P.map₂ α.1) (P.map h.1) (η.app z) (η.app y) (Q.map h.1)
                      (η.naturality h.1) (P.mapComp f.1 h.1) (P.mapComp g.1 h.1)
    | succ i =>
        have hi : i = (0 : Fin 1) := Subsingleton.elim _ _
        subst i
        cases j using Fin.cases with
        | zero =>
            exact False.elim
              ((by decide : ¬ ((1 : Fin 2) ≤ (0 : Fin 2))) f.2.as.le)
        | succ j =>
            have hj : j = (0 : Fin 1) := Subsingleton.elim _ _
            subst j
            cases k using Fin.cases with
            | zero =>
                exact False.elim
                  ((by decide : ¬ ((1 : Fin 2) ≤ (0 : Fin 2))) h.2.as.le)
            | succ k =>
                have hk : k = (0 : Fin 1) := Subsingleton.elim _ _
                subst k
                change Q.map₂ (α.1 ▷ h.1) =
                  (Q.mapComp f.1 h.1).hom ≫
                    Q.map₂ α.1 ▷ Q.map h.1 ≫ (Q.mapComp g.1 h.1).inv
                exact Q.map₂_whisker_right α.1 h.1
  map₂_left_unitor := by
    -- Dependent interval eliminators must be computed at literal vertices.
    -- The endpoint cases are the original strictly-unitary unitor law;
    -- the mixed case still requires genuine bicategorical coherence.
    rintro ⟨x, ⟨i⟩⟩ ⟨y, ⟨j⟩⟩ f
    cases i using Fin.cases with
    | zero =>
        cases j using Fin.cases with
        | zero =>
            change P.map₂ (λ_ f.1).hom =
              (P.mapComp (𝟙 x) f.1).hom ≫
                eqToHom (by rw [P.map_id x]) ≫ (λ_ (P.map f.1)).hom
            simpa only [P.mapId_eq_eqToIso, eqToIso.hom,
              Bicategory.eqToHom_whiskerRight] using
              P.map₂_left_unitor f.1
        | succ j =>
            have hj : j = (0 : Fin 1) := Subsingleton.elim _ _
            subst j
            change P.map₂ (λ_ f.1).hom ▷ η.app y =
              (whiskerRightIso (P.mapComp (𝟙 x) f.1) (η.app y) ≪≫
                α_ (P.map (𝟙 x)) (P.map f.1) (η.app y)).hom ≫
                  eqToHom (by rw [P.map_id x]) ≫
                    (λ_ (P.map f.1 ≫ η.app y)).hom
            calc
              P.map₂ (λ_ f.1).hom ▷ η.app y =
                  ((P.mapComp (𝟙 x) f.1).hom ≫
                    eqToHom (by rw [P.map_id x]) ≫
                      (λ_ (P.map f.1)).hom) ▷ η.app y := by
                        apply congrArg (fun θ => θ ▷ η.app y)
                        simpa only [P.mapId_eq_eqToIso, eqToIso.hom,
                          Bicategory.eqToHom_whiskerRight] using
                          P.map₂_left_unitor f.1
              _ = _ :=
                KUOS.DependentOriginationMixedLeftUnitorPastingV1_36.mixedLeftUnitorPasting
                  (P.map_id x) (P.map f.1) (η.app y) (P.mapComp (𝟙 x) f.1)
    | succ i =>
        have hi : i = (0 : Fin 1) := Subsingleton.elim _ _
        subst i
        cases j using Fin.cases with
        | zero =>
            exact False.elim
              ((by decide : ¬ ((1 : Fin 2) ≤ (0 : Fin 2))) f.2.as.le)
        | succ j =>
            have hj : j = (0 : Fin 1) := Subsingleton.elim _ _
            subst j
            change Q.map₂ (λ_ f.1).hom =
              (Q.mapComp (𝟙 x) f.1).hom ≫
                eqToHom (by rw [Q.map_id x]) ≫ (λ_ (Q.map f.1)).hom
            simpa only [Q.mapId_eq_eqToIso, eqToIso.hom,
              Bicategory.eqToHom_whiskerRight] using
              Q.map₂_left_unitor f.1
  map₂_right_unitor := by
    -- Normalize the actual Fin vertices first, not a propositional
    -- by_cases: the dependent cylinderMap₂ eliminator reduces only then.
    rintro ⟨x, ⟨i⟩⟩ ⟨y, ⟨j⟩⟩ f
    cases i using Fin.cases with
    | zero =>
        cases j using Fin.cases with
        | zero =>
            change P.map₂ (ρ_ f.1).hom =
              (P.mapComp f.1 (𝟙 y)).hom ≫
                eqToHom (by rw [P.map_id y]) ≫ (ρ_ (P.map f.1)).hom
            simpa only [P.mapId_eq_eqToIso, eqToIso.hom,
              Bicategory.whiskerLeft_eqToHom] using
              P.map₂_right_unitor f.1
        | succ j =>
            have hj : j = (0 : Fin 1) := Subsingleton.elim _ _
            subst j
            change P.map₂ (ρ_ f.1).hom ▷ η.app y =
              (whiskerRightIso (P.mapComp f.1 (𝟙 y)) (η.app y) ≪≫
                α_ (P.map f.1) (P.map (𝟙 y)) (η.app y) ≪≫
                whiskerLeftIso (P.map f.1) (η.naturality (𝟙 y)) ≪≫
                (α_ (P.map f.1) (η.app y) (Q.map (𝟙 y))).symm).hom ≫
                  eqToHom (by rw [Q.map_id y]) ≫
                    (ρ_ (P.map f.1 ≫ η.app y)).hom
            have hnat : (η.naturality (𝟙 y)).hom =
                (eqToHom (P.map_id y) ▷ η.app y) ≫
                  (λ_ (η.app y)).hom ≫ (ρ_ (η.app y)).inv ≫
                    (η.app y ◁ eqToHom (Q.map_id y).symm) := by
              simpa only [P.mapId_eq_eqToIso, Q.mapId_eq_eqToIso,
                eqToIso.hom, eqToIso.inv] using
                (Pseudofunctor.StrongTrans.naturality_id_hom η y)
            calc
              P.map₂ (ρ_ f.1).hom ▷ η.app y =
                  ((P.mapComp f.1 (𝟙 y)).hom ≫
                    eqToHom (by rw [P.map_id y]) ≫
                      (ρ_ (P.map f.1)).hom) ▷ η.app y := by
                    apply congrArg (fun θ => θ ▷ η.app y)
                    simpa only [P.mapId_eq_eqToIso, eqToIso.hom,
                      Bicategory.whiskerLeft_eqToHom] using
                      P.map₂_right_unitor f.1
              _ = _ :=
                KUOS.DependentOriginationMixedRightUnitorPastingV1_36.mixedRightUnitorPasting
                  (P.map f.1) (η.app y) (P.map_id y) (Q.map_id y)
                  (P.mapComp f.1 (𝟙 y)) (η.naturality (𝟙 y)) hnat
    | succ i =>
        have hi : i = (0 : Fin 1) := Subsingleton.elim _ _
        subst i
        cases j using Fin.cases with
        | zero =>
            exact False.elim
              ((by decide : ¬ ((1 : Fin 2) ≤ (0 : Fin 2))) f.2.as.le)
        | succ j =>
            have hj : j = (0 : Fin 1) := Subsingleton.elim _ _
            subst j
            change Q.map₂ (ρ_ f.1).hom =
              (Q.mapComp f.1 (𝟙 y)).hom ≫
                eqToHom (by rw [Q.map_id y]) ≫ (ρ_ (Q.map f.1)).hom
            simpa only [Q.mapId_eq_eqToIso, eqToIso.hom,
              Bicategory.whiskerLeft_eqToHom] using
              Q.map₂_right_unitor f.1
  map₂_associator := by
    -- Fin.cases reduces the dependent interval motives before applying
    -- either native associator law. A by_cases on a proposition does not.
    rintro ⟨a, ⟨i⟩⟩ ⟨b, ⟨j⟩⟩ ⟨c, ⟨k⟩⟩ ⟨d, ⟨l⟩⟩ f g h
    cases i using Fin.cases with
    | zero =>
        cases j using Fin.cases with
        | zero =>
            cases k using Fin.cases with
            | zero =>
                cases l using Fin.cases with
                | zero =>
                    change P.map₂ (α_ f.1 g.1 h.1).hom =
                      (P.mapComp (f.1 ≫ g.1) h.1).hom ≫
                        (P.mapComp f.1 g.1).hom ▷ P.map h.1 ≫
                        (α_ (P.map f.1) (P.map g.1) (P.map h.1)).hom ≫
                        P.map f.1 ◁ (P.mapComp g.1 h.1).inv ≫
                        (P.mapComp f.1 (g.1 ≫ h.1)).inv
                    exact P.map₂_associator f.1 g.1 h.1
                | succ l =>
                    have hl : l = (0 : Fin 1) := Subsingleton.elim _ _
                    subst l
                    change P.map₂ (α_ f.1 g.1 h.1).hom ▷ η.app d =
                      (whiskerRightIso (P.mapComp (f.1 ≫ g.1) h.1) (η.app d) ≪≫
                        α_ (P.map (f.1 ≫ g.1)) (P.map h.1) (η.app d)).hom ≫
                        (P.mapComp f.1 g.1).hom ▷ (P.map h.1 ≫ η.app d) ≫
                        (α_ (P.map f.1) (P.map g.1) (P.map h.1 ≫ η.app d)).hom ≫
                        P.map f.1 ◁
                          (whiskerRightIso (P.mapComp g.1 h.1) (η.app d) ≪≫
                            α_ (P.map g.1) (P.map h.1) (η.app d)).inv ≫
                        (whiskerRightIso (P.mapComp f.1 (g.1 ≫ h.1)) (η.app d) ≪≫
                          α_ (P.map f.1) (P.map (g.1 ≫ h.1)) (η.app d)).inv
                    calc
                      P.map₂ (α_ f.1 g.1 h.1).hom ▷ η.app d =
                          ((P.mapComp (f.1 ≫ g.1) h.1).hom ≫
                            (P.mapComp f.1 g.1).hom ▷ P.map h.1 ≫
                            (α_ (P.map f.1) (P.map g.1) (P.map h.1)).hom ≫
                            P.map f.1 ◁ (P.mapComp g.1 h.1).inv ≫
                            (P.mapComp f.1 (g.1 ≫ h.1)).inv) ▷ η.app d := by
                        exact congrArg (fun θ => θ ▷ η.app d)
                          (P.map₂_associator f.1 g.1 h.1)
                      _ = _ := by
                        dsimp only [Iso.trans, Iso.symm, whiskerRightIso]
                        bicategory
            | succ k =>
                have hk : k = (0 : Fin 1) := Subsingleton.elim _ _
                subst k
                cases l using Fin.cases with
                | zero =>
                    exact False.elim
                      ((by decide : ¬ ((1 : Fin 2) ≤ (0 : Fin 2))) h.2.as.le)
                | succ l =>
                    have hl : l = (0 : Fin 1) := Subsingleton.elim _ _
                    subst l
                    change P.map₂ (α_ f.1 g.1 h.1).hom ▷ η.app d =
                      (whiskerRightIso (P.mapComp (f.1 ≫ g.1) h.1) (η.app d) ≪≫
                        α_ (P.map (f.1 ≫ g.1)) (P.map h.1) (η.app d) ≪≫
                        whiskerLeftIso (P.map (f.1 ≫ g.1)) (η.naturality h.1) ≪≫
                        (α_ (P.map (f.1 ≫ g.1)) (η.app c) (Q.map h.1)).symm).hom ≫
                      (whiskerRightIso (P.mapComp f.1 g.1) (η.app c) ≪≫
                        α_ (P.map f.1) (P.map g.1) (η.app c)).hom ▷ Q.map h.1 ≫
                      (α_ (P.map f.1) (P.map g.1 ≫ η.app c) (Q.map h.1)).hom ≫
                      P.map f.1 ◁
                        (whiskerRightIso (P.mapComp g.1 h.1) (η.app d) ≪≫
                          α_ (P.map g.1) (P.map h.1) (η.app d) ≪≫
                          whiskerLeftIso (P.map g.1) (η.naturality h.1) ≪≫
                          (α_ (P.map g.1) (η.app c) (Q.map h.1)).symm).inv ≫
                      (whiskerRightIso (P.mapComp f.1 (g.1 ≫ h.1)) (η.app d) ≪≫
                        α_ (P.map f.1) (P.map (g.1 ≫ h.1)) (η.app d)).inv
                    calc
                      P.map₂ (α_ f.1 g.1 h.1).hom ▷ η.app d =
                          ((P.mapComp (f.1 ≫ g.1) h.1).hom ≫
                            (P.mapComp f.1 g.1).hom ▷ P.map h.1 ≫
                            (α_ (P.map f.1) (P.map g.1) (P.map h.1)).hom ≫
                            P.map f.1 ◁ (P.mapComp g.1 h.1).inv ≫
                            (P.mapComp f.1 (g.1 ≫ h.1)).inv) ▷ η.app d := by
                        exact congrArg (fun θ => θ ▷ η.app d)
                          (P.map₂_associator f.1 g.1 h.1)
                      _ = _ := by
                        dsimp only [Iso.trans, Iso.symm, whiskerRightIso, whiskerLeftIso]
                        -- Expand the outer composite's right whiskering first:
                        -- the reassociation lemma's left side is otherwise
                        -- buried under a still-unexpanded composition.
                        simp only [Bicategory.comp_whiskerRight]
                        rw [KUOS.DependentOriginationMixedWhiskerPastingV1_36.reassociatedRightWhisker
                          (P.mapComp f.1 g.1).hom (P.map h.1) (η.app d)
                          (η.app c) (Q.map h.1) (η.naturality h.1)]
                        bicategory
        | succ j =>
            have hj : j = (0 : Fin 1) := Subsingleton.elim _ _
            subst j
            cases k using Fin.cases with
            | zero =>
                exact False.elim
                  ((by decide : ¬ ((1 : Fin 2) ≤ (0 : Fin 2))) g.2.as.le)
            | succ k =>
                have hk : k = (0 : Fin 1) := Subsingleton.elim _ _
                subst k
                cases l using Fin.cases with
                | zero =>
                    exact False.elim
                      ((by decide : ¬ ((1 : Fin 2) ≤ (0 : Fin 2))) h.2.as.le)
                | succ l =>
                    have hl : l = (0 : Fin 1) := Subsingleton.elim _ _
                    subst l
                    change P.map₂ (α_ f.1 g.1 h.1).hom ▷ η.app d =
                      (whiskerRightIso (P.mapComp (f.1 ≫ g.1) h.1) (η.app d) ≪≫
                        α_ (P.map (f.1 ≫ g.1)) (P.map h.1) (η.app d) ≪≫
                        whiskerLeftIso (P.map (f.1 ≫ g.1)) (η.naturality h.1) ≪≫
                        (α_ (P.map (f.1 ≫ g.1)) (η.app c) (Q.map h.1)).symm).hom ≫
                      (whiskerRightIso (P.mapComp f.1 g.1) (η.app c) ≪≫
                        α_ (P.map f.1) (P.map g.1) (η.app c) ≪≫
                        whiskerLeftIso (P.map f.1) (η.naturality g.1) ≪≫
                        (α_ (P.map f.1) (η.app b) (Q.map g.1)).symm).hom ▷ Q.map h.1 ≫
                      (α_ (P.map f.1 ≫ η.app b) (Q.map g.1) (Q.map h.1)).hom ≫
                      (P.map f.1 ≫ η.app b) ◁ (Q.mapComp g.1 h.1).inv ≫
                      (whiskerRightIso (P.mapComp f.1 (g.1 ≫ h.1)) (η.app d) ≪≫
                        α_ (P.map f.1) (P.map (g.1 ≫ h.1)) (η.app d) ≪≫
                        whiskerLeftIso (P.map f.1) (η.naturality (g.1 ≫ h.1)) ≪≫
                        (α_ (P.map f.1) (η.app b) (Q.map (g.1 ≫ h.1))).symm).inv
                    calc
                      P.map₂ (α_ f.1 g.1 h.1).hom ▷ η.app d =
                          ((P.mapComp (f.1 ≫ g.1) h.1).hom ≫
                            (P.mapComp f.1 g.1).hom ▷ P.map h.1 ≫
                            (α_ (P.map f.1) (P.map g.1) (P.map h.1)).hom ≫
                            P.map f.1 ◁ (P.mapComp g.1 h.1).inv ≫
                            (P.mapComp f.1 (g.1 ≫ h.1)).inv) ▷ η.app d := by
                        exact congrArg (fun θ => θ ▷ η.app d)
                          (P.map₂_associator f.1 g.1 h.1)
                      _ = _ := by
                        dsimp only [Iso.trans, Iso.symm, whiskerRightIso, whiskerLeftIso]
                        -- The naturality square must be aligned with the
                        -- pseudofunctor comparison before applying coherence.
                        simp only [Bicategory.comp_whiskerRight]
                        rw [KUOS.DependentOriginationMixedWhiskerPastingV1_36.reassociatedRightWhisker
                          (P.mapComp f.1 g.1).hom (P.map h.1) (η.app d)
                          (η.app c) (Q.map h.1) (η.naturality h.1)]
                        rw [Pseudofunctor.StrongTrans.naturality_comp_inv η g.1 h.1]
                        -- Normalize the actual string diagram first.
                        -- The pure normal-form tactic cannot evaluate a
                        -- nested, nonstructural Iso.hom; the ordinary tactic
                        -- leaves a typed residual to simplify instead.
                        bicategory
                        all_goals
                          dsimp only [Iso.trans, Iso.symm, Iso.refl,
                            whiskerRightIso, whiskerLeftIso]
                          simp only [Category.assoc,
                            Bicategory.whiskerLeft_hom_inv_whiskerRight,
                            Bicategory.whiskerLeft_whiskerLeft_inv_hom,
                            Bicategory.whiskerLeft_hom_inv,
                            Bicategory.hom_inv_whiskerRight,
                            Bicategory.whiskerLeft_inv_hom,
                            Bicategory.inv_hom_whiskerRight,
                            Category.comp_id, Category.id_comp]
                          bicategory
    | succ i =>
        have hi : i = (0 : Fin 1) := Subsingleton.elim _ _
        subst i
        cases j using Fin.cases with
        | zero =>
            exact False.elim
              ((by decide : ¬ ((1 : Fin 2) ≤ (0 : Fin 2))) f.2.as.le)
        | succ j =>
            have hj : j = (0 : Fin 1) := Subsingleton.elim _ _
            subst j
            cases k using Fin.cases with
            | zero =>
                exact False.elim
                  ((by decide : ¬ ((1 : Fin 2) ≤ (0 : Fin 2))) g.2.as.le)
            | succ k =>
                have hk : k = (0 : Fin 1) := Subsingleton.elim _ _
                subst k
                cases l using Fin.cases with
                | zero =>
                    exact False.elim
                      ((by decide : ¬ ((1 : Fin 2) ≤ (0 : Fin 2))) h.2.as.le)
                | succ l =>
                    have hl : l = (0 : Fin 1) := Subsingleton.elim _ _
                    subst l
                    change Q.map₂ (α_ f.1 g.1 h.1).hom =
                      (Q.mapComp (f.1 ≫ g.1) h.1).hom ≫
                        (Q.mapComp f.1 g.1).hom ▷ Q.map h.1 ≫
                        (α_ (Q.map f.1) (Q.map g.1) (Q.map h.1)).hom ≫
                        Q.map f.1 ◁ (Q.mapComp g.1 h.1).inv ≫
                        (Q.mapComp f.1 (g.1 ≫ h.1)).inv
                    exact Q.map₂_associator f.1 g.1 h.1

/-- Uncurrying a native strong transformation into a strictly-unitary pseudofunctor cylinder. -/
def strongTransformationCylinder
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (P Q : StrictlyUnitaryPseudofunctor B C)
    (η : Pseudofunctor.StrongTrans P.toPseudofunctor Q.toPseudofunctor)
    : StrictlyUnitaryPseudofunctor (B × DuskinOrdinal 1) C :=
  StrictlyUnitaryPseudofunctor.mk' (strongCylinderCore P Q η)

/-- The corresponding normal-lax cylinder. -/
def strongTransformationNormalLaxCylinder
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (P Q : StrictlyUnitaryPseudofunctor B C)
    (η : Pseudofunctor.StrongTrans P.toPseudofunctor Q.toPseudofunctor) :
    StrictlyUnitaryLaxFunctor (B × DuskinOrdinal 1) C :=
  (strongTransformationCylinder P Q η).toStrictlyUnitaryLaxFunctor

/-! ## Fully typed constant-interval endpoint functors -/

/-- The ordinary thin-category functor taking every vertex to the selected
endpoint. Its hom component is the unique identity in that thin category. -/
private def constantIntervalFunctor (n : Nat) (i : Fin 2) :
    Fin (n + 1) ⥤ Fin 2 where
  obj := fun _ => i
  map := fun _ => 𝟙 i
  map_id := by intro _; rfl
  map_comp := by intros; simp

/-- The complete zero-end interval normal-lax functor, including hom and
2-morphism data, is the lift of a *constant* thin-category functor.
Unlike pointwise equalities of `.as`, this identifies the entire
dependent structure before composing with the cylinder. -/
private theorem intervalNormalLax_zero_eq_constant
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {idx : SimplexCategoryᵒᵖ} (σ : (duskinNerve B).obj idx) :
    intervalNormalLax ((SSet.ι₀.app idx σ).2) =
      locallyDiscreteNormalLax (constantIntervalFunctor idx.unop.len 0) := by
  unfold intervalNormalLax
  apply congrArg locallyDiscreteNormalLax
  apply CategoryTheory.Functor.ext
  case h_obj =>
    intro X
    rfl
  case h_map =>
    intro X Y f
    first
    | rfl
    | simp [constantIntervalFunctor, SSet.ι₀_app_snd_apply,
        SSet.ι₁_app_snd_apply]

/-- The complete one-end interval normal-lax functor is also constant.
This is independent of the zero-endpoint and exposes the symmetric typing
needed for the two sides of the eventual endpoint equality. -/
private theorem intervalNormalLax_one_eq_constant
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {idx : SimplexCategoryᵒᵖ} (σ : (duskinNerve B).obj idx) :
    intervalNormalLax ((SSet.ι₁.app idx σ).2) =
      locallyDiscreteNormalLax (constantIntervalFunctor idx.unop.len 1) := by
  unfold intervalNormalLax
  apply congrArg locallyDiscreteNormalLax
  apply CategoryTheory.Functor.ext
  case h_obj =>
    intro X
    rfl
  case h_map =>
    intro X Y f
    first
    | rfl
    | simp [constantIntervalFunctor, SSet.ι₀_app_snd_apply,
        SSet.ι₁_app_snd_apply]

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
    intro _idx σ
    have hIntervalZero (X : DuskinOrdinal _idx.unop.len) :
        ((intervalNormalLax ((SSet.ι₀.app _idx σ).2)).obj X).as =
          (0 : Fin 2) := by
      rfl
    -- Transporting only the scalar .as equation leaves a dependent
    -- Fin.cases motive; identify the actual locally-discrete object.
    have hIntervalZeroObj (X : DuskinOrdinal _idx.unop.len) :
        (intervalNormalLax ((SSet.ι₀.app _idx σ).2)).obj X =
          (⟨(0 : Fin 2)⟩ : DuskinOrdinal 1) := by
      apply LocallyDiscrete.ext
      exact hIntervalZero X
    -- Explicitly identify the complete object map before transporting
    -- the dependent hom/map₂/mapId/mapComp fields.
    have hObj :
        ((normalLaxPair σ
            (intervalNormalLax ((SSet.ι₀.app _idx σ).2))).comp
          (strongTransformationNormalLaxCylinder P Q η)).obj =
          (σ.comp P.toStrictlyUnitaryLaxFunctor).obj := by
      funext X
      rfl
    apply StrictlyUnitaryLaxFunctor.ext
    · exact hObj
    -- First discharge the dependent map field pointwise, using the
    -- heterogeneous function extensionality supported by the pinned API.
    case map =>
      -- The heterogeneously quantified map has three arguments:
      -- source object, target object, then the underlying 1-morphism.
      -- hfunext introduces an HEq proof at each argument.
      apply Function.hfunext rfl
      intro X X' hX
      cases hX
      apply Function.hfunext rfl
      intro Y Y' hY
      cases hY
      apply Function.hfunext rfl
      intro f f' hf
      cases hf
      simp [normalLaxPair, hIntervalZero,
        strongTransformationNormalLaxCylinder,
        strongTransformationCylinder, strongCylinderCore,
        cylinderObj, cylinderMap]
      all_goals
        have hx0 := hIntervalZero X
        have hy0 := hIntervalZero Y
        split_ifs
        all_goals first | contradiction | simp_all
    -- The 2-cell map is a heterogeneously indexed five-argument function;
    -- eliminate every genuine binder before reducing the endpoint.
    case map₂ =>
      apply Function.hfunext rfl
      intro X X' hX
      cases hX
      apply Function.hfunext rfl
      intro Y Y' hY
      cases hY
      apply Function.hfunext rfl
      intro f f' hf
      cases hf
      apply Function.hfunext rfl
      intro g g' hg
      cases hg
      apply Function.hfunext rfl
      intro θ θ' hθ
      cases hθ
      -- Rewrite the entire interval normal-lax functor before attempting
      -- to reduce the dependent Fin.cases motive. The typed Functor.ext
      -- witnesses replace both its object and morphism components.
      rw [intervalNormalLax_zero_eq_constant σ]
      simp [normalLaxPair, constantIntervalFunctor,
        locallyDiscreteNormalLax,
        strongTransformationNormalLaxCylinder,
        strongTransformationCylinder, strongCylinderCore,
        cylinderObj, cylinderMap, cylinderMap₂]
      -- Remaining goals are retained and checked independently below.
      all_goals
        first
        | simp [normalLaxPair, hIntervalZero,
            strongTransformationNormalLaxCylinder,
            strongTransformationCylinder, strongCylinderCore,
            cylinderObj, cylinderMap, cylinderMap₂]
        | skip
      all_goals
        have hx0 := hIntervalZero X
        have hy0 := hIntervalZero Y
        split_ifs
        all_goals first | contradiction | simp_all
    all_goals
      · rw! (castMode := .all) [hObj]
        simp only [heq_iff_eq]
        ext
        simp [normalLaxPair, hIntervalZero, SSet.ι₀_app_snd_apply,
          strongTransformationNormalLaxCylinder,
          strongTransformationCylinder, strongCylinderCore,
          cylinderObj, cylinderMap, cylinderMap₂, cylinderMapComp]
  endpoint_one := by
    intro _idx σ
    have hIntervalOne (X : DuskinOrdinal _idx.unop.len) :
        ((intervalNormalLax ((SSet.ι₁.app _idx σ).2)).obj X).as =
          (1 : Fin 2) := by
      rfl
    have hObj :
        ((normalLaxPair σ
            (intervalNormalLax ((SSet.ι₁.app _idx σ).2))).comp
          (strongTransformationNormalLaxCylinder P Q η)).obj =
          (σ.comp Q.toStrictlyUnitaryLaxFunctor).obj := by
      funext X
      rfl
    apply StrictlyUnitaryLaxFunctor.ext
    · exact hObj
    -- First discharge the dependent map field pointwise, using the
    -- heterogeneous function extensionality supported by the pinned API.
    case map =>
      -- The heterogeneously quantified map has three arguments:
      -- source object, target object, then the underlying 1-morphism.
      -- hfunext introduces an HEq proof at each argument.
      apply Function.hfunext rfl
      intro X X' hX
      cases hX
      apply Function.hfunext rfl
      intro Y Y' hY
      cases hY
      apply Function.hfunext rfl
      intro f f' hf
      cases hf
      simp [normalLaxPair, hIntervalOne,
        strongTransformationNormalLaxCylinder,
        strongTransformationCylinder, strongCylinderCore,
        cylinderObj, cylinderMap]
      all_goals
        have hx0 := hIntervalOne X
        have hy0 := hIntervalOne Y
        split_ifs
        all_goals first | contradiction | simp_all
    all_goals
      · rw! (castMode := .all) [hObj]
        simp only [heq_iff_eq]
        ext
        simp [normalLaxPair, hIntervalOne, SSet.ι₁_app_snd_apply,
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
