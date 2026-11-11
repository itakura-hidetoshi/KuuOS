import KUOS.DependentOriginationScaledDuskinHornTransportV1_29

namespace KUOS.DependentOriginationNormalLaxUniverseLiftV1_35

open CategoryTheory
open Simplicial
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27
open KUOS.DependentOriginationScaledDuskinHornTransportV1_29

universe u₁ u₂ v₁ v₂ w₁ w₂

/-!
# Universe-safe Duskin map from a normal-lax functor

The unlifted nerves of bicategories at independent universe levels do not
form a morphism in one SSet universe. We retain both original nerves through
their canonical ULift carriers, as in the established v1.27/v1.29 route.

This does not assert descent of scaled horns to an unlifted carrier.
-/

/-- A strictly unitary normal-lax functor induces a map on the genuine
pairwise-lifted Duskin carriers, without identifying independent universes. -/
def liftedNormalLaxDuskinNerveMap
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (P : StrictlyUnitaryLaxFunctor B C) :
    normalizedDuskinSource B C ⟶ normalizedDuskinTarget B C where
  app idx := TypeCat.ofHom fun σ => ULift.up (σ.down.comp P)
  naturality := by
    intro idx idx' f
    ext σ
    change
      ULift.up (((duskinReindex f).comp σ.down).comp P) =
        ULift.up ((duskinReindex f).comp (σ.down.comp P))
    exact congrArg ULift.up
      (StrictlyUnitaryLaxFunctor.comp_assoc (duskinReindex f) σ.down P)

/-- The lifted normal-lax transport acts on a simplex exactly by
normal-lax postcomposition, followed by the actual ULift constructor. -/
@[simp] theorem liftedNormalLaxDuskinNerveMap_app
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (P : StrictlyUnitaryLaxFunctor B C)
    (idx : SimplexCategoryᵒᵖ)
    (σ : (normalizedDuskinSource B C).obj idx) :
    (liftedNormalLaxDuskinNerveMap P).app idx σ =
      ULift.up (σ.down.comp P) := rfl

/-- The new universe-safe normal-lax map agrees with the already established
v1.27 normalized model-equivalence map on its actual lifted carrier. -/
theorem liftedNormalLaxDuskinNerveMap_eq_normalized
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : StrictlyUnitaryBicategoricalModelEquivalence B C) :
    liftedNormalLaxDuskinNerveMap E.forward.toStrictlyUnitaryLaxFunctor =
      normalizedDuskinNerveMap E := rfl

end KUOS.DependentOriginationNormalLaxUniverseLiftV1_35
