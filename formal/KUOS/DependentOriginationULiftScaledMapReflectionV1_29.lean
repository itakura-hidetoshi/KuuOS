import KUOS.DependentOriginationULiftScalingRoundTripV1_29

/-!
# Reflection of scaled maps along canonical cross-universe ULift isomorphisms

The scaling on a higher-universe horn or simplex is the *exact* pullback
of the lifted original scaling along the canonical representable isomorphism.
The corresponding lifted simplicial map is scaled if and only if its original
map is scaled. The nontrivial reverse implication is proved here by evaluating
at ULift.up of an arbitrary thin two-simplex, using the iso inverse law.

This does not assert that an independently chosen target family is
admissible; it is the local typed reflection needed for inverse fillers.
-/

namespace KUOS.DependentOriginationULiftScaledMapReflectionV1_29

open CategoryTheory Simplicial Opposite
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationScaledDuskinUniverseLiftBridgeV1_29
open KUOS.DependentOriginationScaledAnodyneAttachmentFactorizationV1_48
open KUOS.DependentOriginationULiftHornUniverseComparisonV1_29
open KUOS.DependentOriginationULiftHornInclusionNaturalityV1_29
open KUOS.DependentOriginationULiftHornMapEquivalenceV1_29
open KUOS.DependentOriginationULiftHornExtensionReflectionV1_29
open KUOS.DependentOriginationULiftScaledHornFillerForwardV1_29

universe u v

/-- A map scaled after conjugating its domain by a genuine ULift isomorphism
was already scaled before the lift. This works for *any* simplicial domain. -/
theorem scaledMap_reflected_by_ulift_iso
    {A X : SSet.{u}}
    {Y : SSet.{max u v}}
    (e : ((SSet.uliftFunctor.{v, u}).obj A) ≅ Y)
    (sA : ScaledSimplicialSet A)
    (sX : ScaledSimplicialSet X)
    (f : A ⟶ X)
    (h : IsScaledMap
      (pullbackScaling (uliftScaling.{u, v} sA) e.inv)
      (uliftScaling.{u, v} sX)
      (e.inv ≫ (SSet.uliftFunctor.{v, u}).map f)) :
    IsScaledMap sA sX f := by
  intro t ht
  have htHigh :
      (pullbackScaling (uliftScaling.{u, v} sA) e.inv).thin
        (e.hom.app (op ⦋2⦌) (ULift.up t)) := by
    change sA.thin
      ((e.inv.app (op ⦋2⦌)
        (e.hom.app (op ⦋2⦌) (ULift.up t))).down)
    have hIso := congrArg
      (fun g : (SSet.uliftFunctor.{v, u}).obj A ⟶
        (SSet.uliftFunctor.{v, u}).obj A =>
        g.app (op ⦋2⦌) (ULift.up t)) e.hom_inv_id
    change e.inv.app (op ⦋2⦌)
      (e.hom.app (op ⦋2⦌) (ULift.up t)) = ULift.up t at hIso
    rw [hIso]
    exact ht
  have hTarget := h _ htHigh
  change sX.thin
    (((e.inv ≫ (SSet.uliftFunctor.{v, u}).map f).app (op ⦋2⦌)
      (e.hom.app (op ⦋2⦌) (ULift.up t))).down) at hTarget
  have heq :
      (e.inv ≫ (SSet.uliftFunctor.{v, u}).map f).app (op ⦋2⦌)
        (e.hom.app (op ⦋2⦌) (ULift.up t)) =
      ULift.up (f.app (op ⦋2⦌) t) := by
    change
      (e.hom ≫ (e.inv ≫ (SSet.uliftFunctor.{v, u}).map f)).app (op ⦋2⦌)
        (ULift.up t) = _
    rw [← Category.assoc, e.hom_inv_id, Category.id_comp]
    rfl
  rw [heq] at hTarget
  exact hTarget

/-- The scaledness of a lifted horn map reflects to its original map. -/
theorem scaledHornMap_reflect
    {X : SSet.{u}} (sX : ScaledSimplicialSet X)
    (n : ℕ) (i : Fin (n + 1))
    (s : ScaledSimplicialSet (SSet.horn.{u} n i : SSet.{u}))
    (f : (SSet.horn.{u} n i : SSet.{u}) ⟶ X)
    (hf : IsScaledMap
      (liftedHornScaling.{u, v} n i s) (uliftScaling.{u, v} sX)
      (liftHornMap.{u, v} n i f)) :
    IsScaledMap s sX f :=
  scaledMap_reflected_by_ulift_iso (hornUniverseIso.{u, v} n i) s sX f hf

/-- The corresponding reflection theorem for simplex maps. -/
theorem scaledSimplexMap_reflect
    {X : SSet.{u}} (sX : ScaledSimplicialSet X)
    (n : ℕ) (s : ScaledSimplicialSet (Δ[n] : SSet.{u}))
    (f : (Δ[n] : SSet.{u}) ⟶ X)
    (hf : IsScaledMap
      (liftedSimplexScaling.{u, v} n s) (uliftScaling.{u, v} sX)
      (liftSimplexMap.{u, v} n f)) :
    IsScaledMap s sX f :=
  scaledMap_reflected_by_ulift_iso (simplexUniverseIso.{u, v} n) s sX f hf

/-- An arbitrary higher-universe horn map into ULift X that preserves the
canonical lifted scaling descends to a scaled map on the original horn. -/
theorem unliftHornMap_scaled
    {X : SSet.{u}} (sX : ScaledSimplicialSet X)
    (n : ℕ) (i : Fin (n + 1))
    (s : ScaledSimplicialSet (SSet.horn.{u} n i : SSet.{u}))
    (g : (SSet.horn.{max u v} n i : SSet.{max u v}) ⟶
      (SSet.uliftFunctor.{v, u}).obj X)
    (hg : IsScaledMap
      (liftedHornScaling.{u, v} n i s) (uliftScaling.{u, v} sX) g) :
    IsScaledMap s sX (unliftHornMap.{u, v} n i g) := by
  apply scaledHornMap_reflect sX n i s
  rw [lift_unliftHornMap.{u, v} n i g]
  exact hg

/-- The same construction for an arbitrary simplex map. -/
theorem unliftSimplexMap_scaled
    {X : SSet.{u}} (sX : ScaledSimplicialSet X)
    (n : ℕ) (s : ScaledSimplicialSet (Δ[n] : SSet.{u}))
    (g : (Δ[n] : SSet.{max u v}) ⟶
      (SSet.uliftFunctor.{v, u}).obj X)
    (hg : IsScaledMap
      (liftedSimplexScaling.{u, v} n s) (uliftScaling.{u, v} sX) g) :
    IsScaledMap s sX (unliftSimplexMap.{u, v} n g) := by
  apply scaledSimplexMap_reflect sX n s
  rw [lift_unliftSimplexMap.{u, v} n g]
  exact hg

#print axioms scaledMap_reflected_by_ulift_iso
#print axioms scaledHornMap_reflect
#print axioms scaledSimplexMap_reflect
#print axioms unliftHornMap_scaled
#print axioms unliftSimplexMap_scaled

end KUOS.DependentOriginationULiftScaledMapReflectionV1_29
