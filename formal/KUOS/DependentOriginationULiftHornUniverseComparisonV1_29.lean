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
      using congrArg (fun (f : d.unop ⟶ ⦋n⦌) => f.toOrderHom j)
        (simplexUniverseEquiv_objEquiv.{u, v} n d x)
  rw [h]


/-! ## Functorial comparison, not merely objectwise membership -/

/-- The universe comparison respects each simplex operator by the Yoneda
description of standard simplices. -/
theorem simplexUniverseEquiv_natural
    (n : ℕ) {d e : SimplexCategoryᵒᵖ} (f : d ⟶ e)
    (x : (Δ[n] : SSet.{u}).obj d) :
    simplexUniverseEquiv.{u, v} n e ((Δ[n] : SSet.{u}).map f x) =
      (Δ[n] : SSet.{max u v}).map f
        (simplexUniverseEquiv.{u, v} n d x) := by
  obtain ⟨a, rfl⟩ := (SSet.stdSimplex.objEquiv.{u}).symm.surjective x
  rfl

/-- The actual pointwise horn equivalence, retaining the horn proof
associated to every simplex. -/
def hornUniverseEquiv
    (n : ℕ) (i : Fin (n + 1)) (d : SimplexCategoryᵒᵖ) :
    ((Λ[n, i] : SSet.{u}).obj d) ≃
      ((Λ[n, i] : SSet.{max u v}).obj d) :=
  (simplexUniverseEquiv.{u, v} n d).subtypeEquiv
    (fun x => hornUniverseMem_iff.{u, v} n i d x)

/-- Horn comparison is natural in every simplicial operator. -/
theorem hornUniverseEquiv_natural
    (n : ℕ) (i : Fin (n + 1))
    {d e : SimplexCategoryᵒᵖ} (f : d ⟶ e)
    (x : (Λ[n, i] : SSet.{u}).obj d) :
    hornUniverseEquiv.{u, v} n i e ((Λ[n, i] : SSet.{u}).map f x) =
      (Λ[n, i] : SSet.{max u v}).map f
        (hornUniverseEquiv.{u, v} n i d x) := by
  apply Subtype.ext
  exact simplexUniverseEquiv_natural.{u, v} n f x.val

#print axioms simplexUniverseEquiv_natural
#print axioms hornUniverseEquiv
#print axioms hornUniverseEquiv_natural

#print axioms simplexUniverseEquiv
#print axioms simplexUniverseEquiv_objEquiv
#print axioms hornUniverseMem_iff

end KUOS.DependentOriginationULiftHornUniverseComparisonV1_29
