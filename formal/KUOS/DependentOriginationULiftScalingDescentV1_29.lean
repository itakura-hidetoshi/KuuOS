import KUOS.DependentOriginationULiftHornExtensionReflectionV1_29
import KUOS.DependentOriginationULiftScaledHornFillerForwardV1_29

/-!
# Reverse transport of the exact horn and simplex scaling predicates

This file constructs genuine scalings on the original lower-universe
horn and simplex by transporting the thin-two-simplex predicates of
the higher-universe representables through the certified natural
universe comparison equivalences. The two simplicial degeneracies
are handled using the proved naturality of the same equivalences.

This does not replace an arbitrary scaling with a maximal or minimal one.
The scaling and admissibility conditions for general fibrancy descent
remain distinct from the mere existence of these transported scalings.
-/

namespace KUOS.DependentOriginationULiftScalingDescentV1_29

open CategoryTheory Simplicial Opposite
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationULiftHornUniverseComparisonV1_29
open KUOS.DependentOriginationULiftHornInclusionNaturalityV1_29
open KUOS.DependentOriginationULiftScaledHornFillerForwardV1_29

universe u v

/-- Recover a scaling on the original represented horn from an arbitrary
higher-universe horn scaling, preserving its actual thinness predicate. -/
@[reducible] def unliftHornScaling (n : ℕ) (i : Fin (n + 1))
    (s : ScaledSimplicialSet (SSet.horn.{max u v} n i : SSet.{max u v})) :
    ScaledSimplicialSet (SSet.horn.{u} n i : SSet.{u}) where
  thin := fun t => s.thin (hornUniverseEquiv.{u, v} n i (op ⦋2⦌) t)
  thin_sigma_zero := by
    intro t
    change s.thin
      (hornUniverseEquiv.{u, v} n i (op ⦋2⦌)
        ((SSet.horn.{u} n i : SSet.{u}).σ 0 t))
    rw [show hornUniverseEquiv.{u, v} n i (op ⦋2⦌)
        ((SSet.horn.{u} n i : SSet.{u}).σ 0 t) =
        (SSet.horn.{max u v} n i : SSet.{max u v}).σ 0
          (hornUniverseEquiv.{u, v} n i (op ⦋1⦌) t) from
      hornUniverseEquiv_natural.{u, v} n i ((SimplexCategory.σ 0).op) t]
    exact s.thin_sigma_zero _
  thin_sigma_one := by
    intro t
    change s.thin
      (hornUniverseEquiv.{u, v} n i (op ⦋2⦌)
        ((SSet.horn.{u} n i : SSet.{u}).σ 1 t))
    rw [show hornUniverseEquiv.{u, v} n i (op ⦋2⦌)
        ((SSet.horn.{u} n i : SSet.{u}).σ 1 t) =
        (SSet.horn.{max u v} n i : SSet.{max u v}).σ 1
          (hornUniverseEquiv.{u, v} n i (op ⦋1⦌) t) from
      hornUniverseEquiv_natural.{u, v} n i ((SimplexCategory.σ 1).op) t]
    exact s.thin_sigma_one _

/-- The same exact inverse predicate transport for standard simplices. -/
@[reducible] def unliftSimplexScaling (n : ℕ)
    (s : ScaledSimplicialSet (Δ[n] : SSet.{max u v})) :
    ScaledSimplicialSet (Δ[n] : SSet.{u}) where
  thin := fun t => s.thin (simplexUniverseEquiv.{u, v} n (op ⦋2⦌) t)
  thin_sigma_zero := by
    intro t
    change s.thin
      (simplexUniverseEquiv.{u, v} n (op ⦋2⦌)
        ((Δ[n] : SSet.{u}).σ 0 t))
    rw [show simplexUniverseEquiv.{u, v} n (op ⦋2⦌)
        ((Δ[n] : SSet.{u}).σ 0 t) =
        (Δ[n] : SSet.{max u v}).σ 0
          (simplexUniverseEquiv.{u, v} n (op ⦋1⦌) t) from
      simplexUniverseEquiv_natural.{u, v} n ((SimplexCategory.σ 0).op) t]
    exact s.thin_sigma_zero _
  thin_sigma_one := by
    intro t
    change s.thin
      (simplexUniverseEquiv.{u, v} n (op ⦋2⦌)
        ((Δ[n] : SSet.{u}).σ 1 t))
    rw [show simplexUniverseEquiv.{u, v} n (op ⦋2⦌)
        ((Δ[n] : SSet.{u}).σ 1 t) =
        (Δ[n] : SSet.{max u v}).σ 1
          (simplexUniverseEquiv.{u, v} n (op ⦋1⦌) t) from
      simplexUniverseEquiv_natural.{u, v} n ((SimplexCategory.σ 1).op) t]
    exact s.thin_sigma_one _

/-- The inverse horn scaling is precisely evaluation at the true
universe-comparison simplex: no coarse replacement is made. -/
theorem unliftHornScaling_thin_iff (n : ℕ) (i : Fin (n + 1))
    (s : ScaledSimplicialSet (SSet.horn.{max u v} n i : SSet.{max u v}))
    (t : (SSet.horn.{u} n i : SSet.{u}).obj (op ⦋2⦌)) :
    (unliftHornScaling.{u, v} n i s).thin t ↔
      s.thin (hornUniverseEquiv.{u, v} n i (op ⦋2⦌) t) := Iff.rfl

theorem unliftSimplexScaling_thin_iff (n : ℕ)
    (s : ScaledSimplicialSet (Δ[n] : SSet.{max u v}))
    (t : (Δ[n] : SSet.{u}).obj (op ⦋2⦌)) :
    (unliftSimplexScaling.{u, v} n s).thin t ↔
      s.thin (simplexUniverseEquiv.{u, v} n (op ⦋2⦌) t) := Iff.rfl

#print axioms unliftHornScaling
#print axioms unliftSimplexScaling
#print axioms unliftHornScaling_thin_iff
#print axioms unliftSimplexScaling_thin_iff

end KUOS.DependentOriginationULiftScalingDescentV1_29
