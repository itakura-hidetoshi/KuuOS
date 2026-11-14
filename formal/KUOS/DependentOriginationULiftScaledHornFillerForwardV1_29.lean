import KUOS.DependentOriginationULiftHornInclusionNaturalityV1_29
import KUOS.DependentOriginationScaledAnodyneAttachmentFactorizationV1_48

/-!
# Cross-universe scaled horn and filler transport

The already-certified natural isomorphisms of representable simplices and
horns yield an actual commutative horn-inclusion square. This file preserves
the *particular* scalings chosen on a horn problem, by pulling their ULift
scalings back along the canonical comparison isomorphisms. We do not replace
the source horn scaling by an arbitrary minimal/maximal scaling.

The construction is forward-only. Arbitrary larger-universe horn problems
and arbitrary admissibility predicates have not been shown to arise in this
manner; no global fibrancy equivalence is asserted.
-/

namespace KUOS.DependentOriginationULiftScaledHornFillerForwardV1_29

open CategoryTheory Simplicial Opposite
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationScaledDuskinUniverseLiftBridgeV1_29
open KUOS.DependentOriginationScaledAnodyneAttachmentFactorizationV1_48
open KUOS.DependentOriginationULiftHornUniverseComparisonV1_29
open KUOS.DependentOriginationULiftHornInclusionNaturalityV1_29

universe u v

/-- On the larger representable horn, use precisely the lifted original
horn scaling transported along the inverse universe comparison. -/
@[reducible] def liftedHornScaling (n : ℕ) (i : Fin (n + 1))
    (s : ScaledSimplicialSet (SSet.horn.{u} n i : SSet.{u})) :
    ScaledSimplicialSet (SSet.horn.{max u v} n i : SSet.{max u v}) :=
  pullbackScaling (uliftScaling.{u, v} s)
    (hornUniverseIso.{u, v} n i).inv

/-- On the larger represented simplex, use exactly the original simplex
scaling transported through the natural universe isomorphism. -/
@[reducible] def liftedSimplexScaling (n : ℕ)
    (s : ScaledSimplicialSet (Δ[n] : SSet.{u})) :
    ScaledSimplicialSet (Δ[n] : SSet.{max u v}) :=
  pullbackScaling (uliftScaling.{u, v} s)
    (simplexUniverseIso.{u, v} n).inv

/-- The genuine horn inclusion remains scaled after universe lifting. -/
theorem liftedHornInclusion_scaled
    {X : SSet.{u}} {sX : ScaledSimplicialSet X}
    {n : ℕ} {i : Fin (n + 1)}
    (P : ScaledHornExtensionProblem X sX n i) :
    IsScaledMap
      (liftedHornScaling.{u, v} n i P.hornScaling)
      (liftedSimplexScaling.{u, v} n P.simplexScaling)
      (SSet.horn.{max u v} n i).ι := by
  intro t ht
  have hpoint := congrArg
    (fun f : (SSet.horn.{max u v} n i : SSet.{max u v}) ⟶
        (SSet.uliftFunctor.{v, u}).obj (Δ[n] : SSet.{u}) =>
      f.app (op ⦋2⦌) t)
    (hornUniverseIso_inv_inclusion.{u, v} n i)
  have hdown :
      (((simplexUniverseIso.{u, v} n).inv.app (op ⦋2⦌)
        ((SSet.horn.{max u v} n i).ι.app (op ⦋2⦌) t)).down) =
      ((SSet.horn.{u} n i).ι.app (op ⦋2⦌)
        (((hornUniverseIso.{u, v} n i).inv.app (op ⦋2⦌) t).down)) := by
    exact congrArg ULift.down hpoint
  change P.simplexScaling.thin
    (((simplexUniverseIso.{u, v} n).inv.app (op ⦋2⦌)
      ((SSet.horn.{max u v} n i).ι.app (op ⦋2⦌) t)).down)
  change P.hornScaling.thin
    (((hornUniverseIso.{u, v} n i).inv.app (op ⦋2⦌) t).down) at ht
  rw [hdown]
  exact P.inclusion_scaled _ ht

/-- Every original scaled horn problem has a correctly typed problem in the
larger universe; both scaling structures are transported, not erased. -/
noncomputable def liftScaledHornProblem
    {X : SSet.{u}} {sX : ScaledSimplicialSet X}
    {n : ℕ} {i : Fin (n + 1)}
    (P : ScaledHornExtensionProblem X sX n i) :
    ScaledHornExtensionProblem
      ((SSet.uliftFunctor.{v, u}).obj X) (uliftScaling.{u, v} sX) n i where
  hornScaling := liftedHornScaling.{u, v} n i P.hornScaling
  simplexScaling := liftedSimplexScaling.{u, v} n P.simplexScaling
  inclusion_scaled := liftedHornInclusion_scaled.{u, v} P
  hornMap := liftHornMap.{u, v} n i P.hornMap
  hornMap_scaled := by
    have h₁ :
        IsScaledMap (liftedHornScaling.{u, v} n i P.hornScaling)
          (uliftScaling.{u, v} P.hornScaling)
          (hornUniverseIso.{u, v} n i).inv :=
      pullbackScaling_map _ _
    exact h₁.comp (isScaledMap_ulift.{u, v} P.hornMap_scaled)

/-- A certified scaled filler transports to the larger universe while
preserving its extension equation and its nontrivial thin-triangle data. -/
noncomputable def liftScaledHornFiller
    {X : SSet.{u}} {sX : ScaledSimplicialSet X}
    {n : ℕ} {i : Fin (n + 1)}
    {P : ScaledHornExtensionProblem X sX n i}
    (Q : ScaledHornFiller P) :
    ScaledHornFiller (liftScaledHornProblem.{u, v} P) where
  simplexMap := liftSimplexMap.{u, v} n Q.simplexMap
  extends_horn := liftHornMap_extends.{u, v} n i
    P.hornMap Q.simplexMap Q.extends_horn
  simplexMap_scaled := by
    have h₁ :
        IsScaledMap (liftedSimplexScaling.{u, v} n P.simplexScaling)
          (uliftScaling.{u, v} P.simplexScaling)
          (simplexUniverseIso.{u, v} n).inv :=
      pullbackScaling_map _ _
    exact h₁.comp (isScaledMap_ulift.{u, v} Q.simplexMap_scaled)

/-- The forward implication of filler existence needs no further axiom.
Surjectivity on *all* higher-universe horns is a separate descent issue. -/
theorem liftScaledHornFiller_nonempty
    {X : SSet.{u}} {sX : ScaledSimplicialSet X}
    {n : ℕ} {i : Fin (n + 1)}
    {P : ScaledHornExtensionProblem X sX n i}
    (h : Nonempty (ScaledHornFiller P)) :
    Nonempty (ScaledHornFiller (liftScaledHornProblem.{u, v} P)) :=
  h.map liftScaledHornFiller

#print axioms liftedHornInclusion_scaled
#print axioms liftScaledHornProblem
#print axioms liftScaledHornFiller
#print axioms liftScaledHornFiller_nonempty

end KUOS.DependentOriginationULiftScaledHornFillerForwardV1_29
