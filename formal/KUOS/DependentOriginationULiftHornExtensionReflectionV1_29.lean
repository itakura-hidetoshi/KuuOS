import KUOS.DependentOriginationULiftHornMapEquivalenceV1_29

/-!
# Cross-universe reflection of the exact horn-extension equation

The previously certified fully faithful equivalences of horn and simplex
maps have the same forward component as the explicit KuuOS ULift transports.
Here their reverse components are proved to reflect the horn-extension
equation. This is a necessary descent condition for returning a lifted filler
to its original unlifted target. The scaling and admissibility predicates
remain separate obligations, not silently inferred from the hom-equivalences.
-/

namespace KUOS.DependentOriginationULiftHornExtensionReflectionV1_29

open CategoryTheory Simplicial
open KUOS.DependentOriginationULiftHornUniverseComparisonV1_29
open KUOS.DependentOriginationULiftHornInclusionNaturalityV1_29
open KUOS.DependentOriginationULiftHornMapEquivalenceV1_29

universe u v

/-- The canonical forward horn-map equivalence is the already proved
simplicial map lift, not a different universe identification. -/
theorem hornMapUniverseEquiv_apply {X : SSet.{u}}
    (n : ℕ) (i : Fin (n + 1))
    (f : (SSet.horn.{u} n i : SSet.{u}) ⟶ X) :
    hornMapUniverseEquiv.{u, v} n i f = liftHornMap.{u, v} n i f := rfl

/-- Likewise for the canonical simplex-map equivalence. -/
theorem simplexMapUniverseEquiv_apply {X : SSet.{u}}
    (n : ℕ) (f : (Δ[n] : SSet.{u}) ⟶ X) :
    simplexMapUniverseEquiv.{u, v} n f = liftSimplexMap.{u, v} n f := rfl

/-- Every higher-universe horn map into a lifted target is the lift of its
unique original-universe map. -/
theorem lift_unliftHornMap {X : SSet.{u}}
    (n : ℕ) (i : Fin (n + 1))
    (f : (SSet.horn.{max u v} n i : SSet.{max u v}) ⟶
      (SSet.uliftFunctor.{v, u}).obj X) :
    liftHornMap.{u, v} n i (unliftHornMap.{u, v} n i f) = f := by
  rw [← hornMapUniverseEquiv_apply]
  exact (hornMapUniverseEquiv.{u, v} (X := X) n i).apply_symm_apply f

/-- Every higher-universe simplex map into a lifted target is the lift of
its unique original-universe map. -/
theorem lift_unliftSimplexMap {X : SSet.{u}}
    (n : ℕ)
    (g : (Δ[n] : SSet.{max u v}) ⟶
      (SSet.uliftFunctor.{v, u}).obj X) :
    liftSimplexMap.{u, v} n (unliftSimplexMap.{u, v} n g) = g := by
  rw [← simplexMapUniverseEquiv_apply]
  exact (simplexMapUniverseEquiv.{u, v} (X := X) n).apply_symm_apply g

/-- Reflection of the *actual horn inclusion* extension equation across
independent universe levels. No thinness or admissibility is erased. -/
theorem unliftHornMap_extends {X : SSet.{u}}
    (n : ℕ) (i : Fin (n + 1))
    (f : (SSet.horn.{max u v} n i : SSet.{max u v}) ⟶
      (SSet.uliftFunctor.{v, u}).obj X)
    (g : (Δ[n] : SSet.{max u v}) ⟶
      (SSet.uliftFunctor.{v, u}).obj X)
    (h : f = (SSet.horn.{max u v} n i).ι ≫ g) :
    unliftHornMap.{u, v} n i f =
      (SSet.horn.{u} n i).ι ≫ unliftSimplexMap.{u, v} n g := by
  apply (hornMapUniverseEquiv.{u, v} (X := X) n i).injective
  change liftHornMap.{u, v} n i (unliftHornMap.{u, v} n i f) =
    liftHornMap.{u, v} n i
      ((SSet.horn.{u} n i).ι ≫ unliftSimplexMap.{u, v} n g)
  rw [lift_unliftHornMap]
  rw [liftHornMap_extends.{u, v} n i
    ((SSet.horn.{u} n i).ι ≫ unliftSimplexMap.{u, v} n g)
    (unliftSimplexMap.{u, v} n g) rfl]
  rw [lift_unliftSimplexMap]
  exact h

#print axioms hornMapUniverseEquiv_apply
#print axioms simplexMapUniverseEquiv_apply
#print axioms lift_unliftHornMap
#print axioms lift_unliftSimplexMap
#print axioms unliftHornMap_extends

end KUOS.DependentOriginationULiftHornExtensionReflectionV1_29
