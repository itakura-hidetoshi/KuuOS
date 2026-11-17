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
          G.forward.toStrictlyUnitaryLaxFunctor)

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
          F.forward.toStrictlyUnitaryLaxFunctor)


/-!
## Global pairwise-lifted homotopy from the original typed cylinder

The B/B normal-lax cylinder can be evaluated on B/D simplices without
identifying the B/B and B/D SSet universes. Its endpoint equations are
transported by ULift.up on the actual ambient B/D carrier.
-/

/-- Evaluate a certified B/B cylinder in the independent B/D ULift universe.
This proves the homotopy on the actual pairwise carrier, not by a cast of the
B/B homotopy, and does not assert unlifted scaled-horn descent. -/
noncomputable def ambientNormalLaxCylinderHomotopy
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {D : Type u₂} [Bicategory.{w₂, v₂} D]
    {P Q : StrictlyUnitaryLaxFunctor B B}
    (H : NormalLaxDuskinCylinder P Q) :
    SSet.Homotopy
      (ambientNormalLaxEndo (D := D) P)
      (ambientNormalLaxEndo (D := D) Q) where
  h :=
    { app := fun idx => TypeCat.ofHom fun x =>
        ULift.up ((normalLaxPair x.1.down (intervalNormalLax x.2)).comp H.cylinder)
      naturality := by
        intro idx idx' f
        ext x
        change
          ULift.up ((normalLaxPair ((duskinReindex f).comp x.1.down)
              (intervalNormalLax (Δ[1].map f x.2))).comp H.cylinder) =
          ULift.up ((duskinReindex f).comp
              ((normalLaxPair x.1.down (intervalNormalLax x.2)).comp H.cylinder))
        apply congrArg ULift.up
        rw [intervalNormalLax_reindex]
        rw [← normalLaxPair_precomp]
        exact StrictlyUnitaryLaxFunctor.comp_assoc
          (duskinReindex f)
          (normalLaxPair x.1.down (intervalNormalLax x.2))
          H.cylinder }
  h₀ := by
    ext idx σ
    change
      ULift.up ((normalLaxPair σ.down
        (intervalNormalLax ((SSet.ι₀.app idx σ).2))).comp H.cylinder) =
      ULift.up (σ.down.comp P)
    exact congrArg ULift.up (H.endpoint_zero σ.down)
  h₁ := by
    ext idx σ
    change
      ULift.up ((normalLaxPair σ.down
        (intervalNormalLax ((SSet.ι₁.app idx σ).2))).comp H.cylinder) =
      ULift.up (σ.down.comp Q)
    exact congrArg ULift.up (H.endpoint_one σ.down)
  rel := by
    ext idx x
    rcases x with ⟨⟨σ, hσ⟩, t⟩
    exact False.elim hσ

/-- The B/B source cylinder induces a genuine B/C round-trip homotopy. -/
noncomputable def sourceRoundTrip_pairwise_prism
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (F : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (G : StrictlyUnitaryBicategoricalModelEquivalence C B)
    (H : NormalLaxDuskinCylinder
      (sourceRoundTripNormalLax F G) (StrictlyUnitaryLaxFunctor.id B)) :
    SSet.Homotopy
      (normalizedDuskinNerveMap F ≫ normalizedDuskinNerveMap G)
      (𝟙 (normalizedDuskinSource B C)) := by
  rw [sourceRoundTrip_pairwise_map F G, ← ambientNormalLaxEndo_id B C]
  exact ambientNormalLaxCylinderHomotopy (D := C) H

/-- The C/C target cylinder induces a genuine C/B round-trip homotopy. -/
noncomputable def targetRoundTrip_pairwise_prism
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (F : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (G : StrictlyUnitaryBicategoricalModelEquivalence C B)
    (H : NormalLaxDuskinCylinder
      (targetRoundTripNormalLax F G) (StrictlyUnitaryLaxFunctor.id C)) :
    SSet.Homotopy
      (normalizedDuskinNerveMap G ≫ normalizedDuskinNerveMap F)
      (𝟙 (normalizedDuskinTarget B C)) := by
  change SSet.Homotopy
    (normalizedDuskinNerveMap G ≫ normalizedDuskinNerveMap F)
    (𝟙 (normalizedDuskinSource C B))
  rw [targetRoundTrip_pairwise_map F G, ← ambientNormalLaxEndo_id C B]
  exact ambientNormalLaxCylinderHomotopy (D := B) H

#print axioms ambientNormalLaxEndo_id
#print axioms sourceRoundTrip_pairwise_map
#print axioms targetRoundTrip_pairwise_map
#print axioms ambientNormalLaxCylinderHomotopy
#print axioms sourceRoundTrip_pairwise_prism
#print axioms targetRoundTrip_pairwise_prism

end KUOS.DependentOriginationPairwiseNormalLaxRoundTripBridgeV1_36
