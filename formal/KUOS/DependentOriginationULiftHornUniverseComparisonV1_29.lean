import KUOS.DependentOriginationCanonicalSameUniverseDuskinDescentV1_29

/-!
# Actual cross-universe comparison of standard simplices and horns

The Duskin source and target may live in independent SSet universes.
Before descending a lifted scaled horn filler, the represented simplex,
its finite face index and the horn subcomplex must be identified across
universes. This file proves the pointwise comparison and horn-membership
compatibility, without equating the ambient categories or changing any
original v1.29 admissibility predicate.
-/

namespace KUOS.DependentOriginationULiftHornUniverseComparisonV1_29

open CategoryTheory Simplicial Opposite

universe u v

/-- An n-simplex is its monotone vertex map, irrespective of the ambient
SSet universe. This is an equivalence between the actual two representables. -/
def simplexUniverseEquiv
    (n : ℕ) (d : SimplexCategoryᵒᵖ) :
    ((Δ[n] : SSet.{u}).obj d) ≃
      ((Δ[n] : SSet.{max u v}).obj d) :=
  (SSet.stdSimplex.objEquiv.{u}).trans
    (SSet.stdSimplex.objEquiv.{max u v}).symm

/-- The comparison preserves the *original* finite simplex morphism. -/
@[simp] theorem simplexUniverseEquiv_objEquiv
    (n : ℕ) (d : SimplexCategoryᵒᵖ)
    (x : (Δ[n] : SSet.{u}).obj d) :
    SSet.stdSimplex.objEquiv
      (simplexUniverseEquiv.{u, v} n d x) =
      SSet.stdSimplex.objEquiv x := by
  simp [simplexUniverseEquiv]

/-- Horn membership is the same statement about the vertex range before
and after changing the represented simplex universe. -/
theorem hornUniverseMem_iff
    (n : ℕ) (i : Fin (n + 1)) (d : SimplexCategoryᵒᵖ)
    (x : (Δ[n] : SSet.{u}).obj d) :
    x ∈ (SSet.horn.{u} n i).obj d ↔
      simplexUniverseEquiv.{u, v} n d x ∈
        (SSet.horn.{max u v} n i).obj d := by
  simp only [SSet.mem_horn_iff]
  have h :
      SSet.stdSimplex.asOrderHom
          (simplexUniverseEquiv.{u, v} n d x) =
        SSet.stdSimplex.asOrderHom x := by
    apply OrderHom.ext
    funext j
    simpa only [SSet.stdSimplex.objEquiv_toOrderHom_apply]
      using congrArg (fun f => f.toOrderHom j)
        (simplexUniverseEquiv_objEquiv (u := u) (v := v) n d x)
  rw [h]

#print axioms simplexUniverseEquiv
#print axioms simplexUniverseEquiv_objEquiv
#print axioms hornUniverseMem_iff

end KUOS.DependentOriginationULiftHornUniverseComparisonV1_29
