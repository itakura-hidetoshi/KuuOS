import KUOS.DependentOriginationStrongTransformationDuskinCylinderV1_35

namespace KUOS.DependentOriginationPairwiseNormalLaxRoundTripBridgeV1_36

open CategoryTheory
open CategoryTheory.Category
open Simplicial
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27
open KUOS.DependentOriginationScaledDuskinHornTransportV1_29
open KUOS.DependentOriginationStrongTransformationDuskinCylinderV1_35

universe u₁ u₂ v₁ v₂ w₁ w₂

/-!
A typed bridge between the B/B cylinder carrier and the B/C pairwise
ULift carrier used by the global Duskin round-trip statement.

This proves compatibility of the two *maps*, not a transport of homotopies,
not an identification of differing universe levels, and not unlifted
scaled-horn descent. Those remain independent proof obligations.
-/

/-- Self-transport of a Duskin nerve on the actual pairwise B/D ULift carrier. -/
def ambientNormalLaxEndo
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {D : Type u₂} [Bicategory.{w₂, v₂} D]
    (P : StrictlyUnitaryLaxFunctor B B) :
    normalizedDuskinSource B D ⟶ normalizedDuskinSource B D where
  app idx := TypeCat.ofHom fun σ => ULift.up (σ.down.comp P)
  naturality := by
    intro idx idx' f
    ext σ
    change
      ULift.up (((duskinReindex f).comp σ.down).comp P) =
        ULift.up ((duskinReindex f).comp (σ.down.comp P))
    exact congrArg ULift.up
      (StrictlyUnitaryLaxFunctor.comp_assoc (duskinReindex f) σ.down P)

/-- Self-transport by the identity remains identity in any ambient universe. -/
@[simp] theorem ambientNormalLaxEndo_id
    (B : Type u₁) [Bicategory.{w₁, v₁} B]
    (D : Type u₂) [Bicategory.{w₂, v₂} D] :
    ambientNormalLaxEndo (D := D) (StrictlyUnitaryLaxFunctor.id B) =
      𝟙 (normalizedDuskinSource B D) := by
  ext idx σ
  change ULift.up (σ.down.comp (StrictlyUnitaryLaxFunctor.id B)) = σ
  rw [StrictlyUnitaryLaxFunctor.comp_id]
  cases σ
  rfl

/-- The genuine B/C lifted source round-trip equals its ambient self-map. -/
theorem sourceRoundTrip_pairwise_map
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (F : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (G : StrictlyUnitaryBicategoricalModelEquivalence C B) :
    (normalizedDuskinNerveMap F ≫ normalizedDuskinNerveMap G) =
      ambientNormalLaxEndo (D := C) (sourceRoundTripNormalLax F G) := by
  ext idx σ
  cases σ with
  | up σ =>
      change
        ULift.up ((σ.comp F.forward.toStrictlyUnitaryLaxFunctor).comp
          G.forward.toStrictlyUnitaryLaxFunctor) =
          ULift.up (σ.comp
            (F.forward.toStrictlyUnitaryLaxFunctor.comp
              G.forward.toStrictlyUnitaryLaxFunctor))
      exact congrArg ULift.up
        (StrictlyUnitaryLaxFunctor.comp_assoc σ
          F.forward.toStrictlyUnitaryLaxFunctor
          G.forward.toStrictlyUnitaryLaxFunctor).symm

/-- The genuine C/B lifted target round-trip equals its ambient self-map. -/
theorem targetRoundTrip_pairwise_map
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (F : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (G : StrictlyUnitaryBicategoricalModelEquivalence C B) :
    (normalizedDuskinNerveMap G ≫ normalizedDuskinNerveMap F) =
      ambientNormalLaxEndo (D := B) (targetRoundTripNormalLax F G) := by
  ext idx σ
  cases σ with
  | up σ =>
      change
        ULift.up ((σ.comp G.forward.toStrictlyUnitaryLaxFunctor).comp
          F.forward.toStrictlyUnitaryLaxFunctor) =
          ULift.up (σ.comp
            (G.forward.toStrictlyUnitaryLaxFunctor.comp
              F.forward.toStrictlyUnitaryLaxFunctor))
      exact congrArg ULift.up
        (StrictlyUnitaryLaxFunctor.comp_assoc σ
          G.forward.toStrictlyUnitaryLaxFunctor
          F.forward.toStrictlyUnitaryLaxFunctor).symm

#print axioms ambientNormalLaxEndo_id
#print axioms sourceRoundTrip_pairwise_map
#print axioms targetRoundTrip_pairwise_map

end KUOS.DependentOriginationPairwiseNormalLaxRoundTripBridgeV1_36
