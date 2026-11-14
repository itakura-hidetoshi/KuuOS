import KUOS.DependentOriginationULiftHornUniverseComparisonV1_29

/-!
# Canonical cross-universe horn inclusion square

The ordinary representable and horn comparison isomorphisms already constructed
in v1.29 are compatible with the *actual* horn inclusions. This missing square
is required before lifted horn problems and their fillers can be transported
between independent universe levels. No scaled family or fibrancy is assumed.
-/

namespace KUOS.DependentOriginationULiftHornInclusionNaturalityV1_29

open CategoryTheory Simplicial
open KUOS.DependentOriginationULiftHornUniverseComparisonV1_29

universe u v

/-- The horn inclusion is carried by the exact universe-comparison isomorphisms,
rather than by a non-type-correct identification of the two horn domains. -/
theorem hornUniverseIso_inclusion_commutes (n : ℕ) (i : Fin (n + 1)) :
    (SSet.uliftFunctor.{v, u}).map (SSet.horn.{u} n i).ι ≫
      (simplexUniverseIso.{u, v} n).hom =
    (hornUniverseIso.{u, v} n i).hom ≫ (SSet.horn.{max u v} n i).ι := by
  apply SSet.hom_ext
  intro d
  ext x
  rfl

/-- The equivalent square in the direction used to lift a horn problem. -/
theorem hornUniverseIso_inv_inclusion (n : ℕ) (i : Fin (n + 1)) :
    (SSet.horn.{max u v} n i).ι ≫ (simplexUniverseIso.{u, v} n).inv =
      (hornUniverseIso.{u, v} n i).inv ≫
        (SSet.uliftFunctor.{v, u}).map (SSet.horn.{u} n i).ι := by
  have h := hornUniverseIso_inclusion_commutes.{u, v} n i
  calc
    (SSet.horn.{max u v} n i).ι ≫ (simplexUniverseIso.{u, v} n).inv =
      (hornUniverseIso.{u, v} n i).inv ≫
        ((hornUniverseIso.{u, v} n i).hom ≫
          (SSet.horn.{max u v} n i).ι) ≫
        (simplexUniverseIso.{u, v} n).inv := by simp [Category.assoc]
    _ = (hornUniverseIso.{u, v} n i).inv ≫
          ((SSet.uliftFunctor.{v, u}).map (SSet.horn.{u} n i).ι ≫
            (simplexUniverseIso.{u, v} n).hom) ≫
          (simplexUniverseIso.{u, v} n).inv := by rw [h]
    _ = (hornUniverseIso.{u, v} n i).inv ≫
          (SSet.uliftFunctor.{v, u}).map (SSet.horn.{u} n i).ι := by
        simp [Category.assoc]

/-- A horn map in the original universe gives a *typed* horn map in the larger
universe after transporting the domain along its canonical natural isomorphism. -/
noncomputable def liftHornMap {X : SSet.{u}}
    (n : ℕ) (i : Fin (n + 1))
    (f : (SSet.horn.{u} n i : SSet.{u}) ⟶ X) :
    (SSet.horn.{max u v} n i : SSet.{max u v}) ⟶
      (SSet.uliftFunctor.{v, u}).obj X :=
  (hornUniverseIso.{u, v} n i).inv ≫ (SSet.uliftFunctor.{v, u}).map f

/-- A simplex map lifts using the analogous isomorphism for representables. -/
noncomputable def liftSimplexMap {X : SSet.{u}}
    (n : ℕ) (f : (Δ[n] : SSet.{u}) ⟶ X) :
    (Δ[n] : SSet.{max u v}) ⟶ (SSet.uliftFunctor.{v, u}).obj X :=
  (simplexUniverseIso.{u, v} n).inv ≫ (SSet.uliftFunctor.{v, u}).map f

/-- Actual horn extensions commute with universe lifting, including the
distinguished face index. This is a concrete compatibility witness, not a
claim of general scaled-fibrancy descent. -/
theorem liftHornMap_extends {X : SSet.{u}}
    (n : ℕ) (i : Fin (n + 1))
    (f : (SSet.horn.{u} n i : SSet.{u}) ⟶ X)
    (g : (Δ[n] : SSet.{u}) ⟶ X)
    (h : f = (SSet.horn.{u} n i).ι ≫ g) :
    liftHornMap.{u, v} n i f =
      (SSet.horn.{max u v} n i).ι ≫ liftSimplexMap.{u, v} n g := by
  subst f
  unfold liftHornMap liftSimplexMap
  rw [Functor.map_comp]
  calc
    (hornUniverseIso.{u, v} n i).inv ≫
      ((SSet.uliftFunctor.{v, u}).map (SSet.horn.{u} n i).ι ≫
        (SSet.uliftFunctor.{v, u}).map g) =
      ((hornUniverseIso.{u, v} n i).inv ≫
        (SSet.uliftFunctor.{v, u}).map (SSet.horn.{u} n i).ι) ≫
          (SSet.uliftFunctor.{v, u}).map g := by simp [Category.assoc]
    _ = ((SSet.horn.{max u v} n i).ι ≫
          (simplexUniverseIso.{u, v} n).inv) ≫
            (SSet.uliftFunctor.{v, u}).map g := by
          rw [hornUniverseIso_inv_inclusion]
    _ = (SSet.horn.{max u v} n i).ι ≫
          ((simplexUniverseIso.{u, v} n).inv ≫
            (SSet.uliftFunctor.{v, u}).map g) := by simp [Category.assoc]

#print axioms hornUniverseIso_inclusion_commutes
#print axioms hornUniverseIso_inv_inclusion
#print axioms liftHornMap_extends

end KUOS.DependentOriginationULiftHornInclusionNaturalityV1_29
