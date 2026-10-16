import KUOS.DependentOriginationStandardTypeBThreeSimplexMaximalCompletionV1_68

namespace KUOS.DependentOriginationStandardTypeABoundaryPrismThreeResidualClassificationV1_69

open CategoryTheory
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeBScalingPushoutV1_56
open KUOS.DependentOriginationStandardTypeBThreeSimplexCompletionV1_57
open KUOS.DependentOriginationStandardTypeABoundaryPrismRelativeCellV1_61
open KUOS.DependentOriginationStandardTypeABoundaryPrismScaledCellsV1_62
open KUOS.DependentOriginationStandardTypeABoundaryPrismStaircaseNormalFormV1_64
open KUOS.DependentOriginationStandardTypeABoundaryPrismCellPushoutCriterionV1_65
open KUOS.DependentOriginationStandardTypeABoundaryPrismCellACompatibilityV1_66
open KUOS.DependentOriginationStandardTypeABoundaryPrismN2MaximalFrontierV1_67
open KUOS.DependentOriginationStandardTypeBThreeSimplexMaximalCompletionV1_68

universe u

noncomputable section

/-!
# Complete fixed three-simplex A/B residual classification v1.69

The preceding units reduced every possible post-A boundary-prism scaling
residual to attached dimension three, and v1.68 proved that both standard
q12/q23 type-(B) completions have maximal target scaling on `Δ[3]`.

This file closes the remaining fixed three-simplex geometry in one finite unit.
It does not yet assemble the global scaled rank filtration.  Instead it proves
exactly what that filtration will consume at every exceptional three-cell.

First we strengthen v1.68 from one-sided base membership to exact base
characterizations:

```text
q12 base = minimal + 012 + 013 + 123,
q23 base = minimal + 012 + 023 + 123.
```

Next we define the intrinsic scaling obtained from a standard type-(A)
three-simplex after saturating by every triangle already lying in its inner
horn.  This is precisely the finite scaling pattern that a type-(A) cobase
change has when the incoming horn scaling is maximal.  We prove literally

```text
index 1 horn-saturated A scaling = q12 base,
index 2 horn-saturated A scaling = q23 base.
```

Together with v1.68 this gives the complete fixed A/B table

```text
index 1 : A-saturated base = q12 base  --> q12 completion = maximal,
index 2 : A-saturated base = q23 base  --> q23 completion = maximal.
```

Finally we attach this table to every actual three-dimensional boundary-prism
cell via the already formalized fixed cell index and missing-face theorems.  In
the original-generator `n = 2` branch the actual target is maximal by v1.67,
so the only remaining categorical work is to identify the actual A-pushout
transport with this now-rigid fixed table and insert the corresponding B
completion into each rank successor.
-/

/-! ## The two remaining designated type-(B) source triangles -/

/-- The source triangle `123` in `Δ[4]`. -/
def standardTypeBSourceTriangle123 :
    (Δ[4] : SSet.{u}).obj (op ⦋2⦌) :=
  SSet.stdSimplex.triangle
    (1 : Fin 5) 2 3 (by decide) (by decide)

/-- The source triangle `012` in `Δ[4]`. -/
def standardTypeBSourceTriangle012 :
    (Δ[4] : SSet.{u}).obj (op ⦋2⦌) :=
  SSet.stdSimplex.triangle
    (0 : Fin 5) 1 2 (by decide) (by decide)

/-- `123` is one of the five designated source-thin type-(B) triangles. -/
theorem standardTypeBSourceTriangle123_isSourceTriangle :
    IsStandardTypeBSourceTriangle standardTypeBSourceTriangle123 := by
  exact Or.inr (Or.inl ⟨rfl, rfl, rfl⟩)

/-- `012` is one of the five designated source-thin type-(B) triangles. -/
theorem standardTypeBSourceTriangle012_isSourceTriangle :
    IsStandardTypeBSourceTriangle standardTypeBSourceTriangle012 := by
  exact Or.inr (Or.inr (Or.inr (Or.inr ⟨rfl, rfl, rfl⟩)))

/-- Hence `123` is source-thin. -/
theorem standardTypeBSourceTriangle123_source_thin :
    standardTypeBSourceScaling.thin standardTypeBSourceTriangle123 := by
  exact Or.inr standardTypeBSourceTriangle123_isSourceTriangle

/-- Hence `012` is source-thin. -/
theorem standardTypeBSourceTriangle012_source_thin :
    standardTypeBSourceScaling.thin standardTypeBSourceTriangle012 := by
  exact Or.inr standardTypeBSourceTriangle012_isSourceTriangle

/-- A specified standard-vertex triangle is literally the corresponding
`stdSimplex.triangle`. -/
theorem isStandardVertexTriangle_eq_triangle
    {n : ℕ}
    {a b c : Fin (n + 1)}
    (hab : a ≤ b)
    (hbc : b ≤ c)
    {t : (Δ[n] : SSet.{u}).obj (op ⦋2⦌)}
    (ht : IsStandardVertexTriangle a b c t) :
    t = SSet.stdSimplex.triangle a b c hab hbc := by
  apply SSet.stdSimplex.ext
  intro j
  fin_cases j
  · exact ht.1
  · exact ht.2.1
  · exact ht.2.2

/-- Exhaustive form of source thinness: a source-thin triangle is either
minimal or literally one of the five designated nondegenerate source faces. -/
theorem standardTypeBSourceScaling_thin_cases
    {t : (Δ[4] : SSet.{u}).obj (op ⦋2⦌)}
    (ht : standardTypeBSourceScaling.thin t) :
    (minimalScaling (Δ[4] : SSet.{u})).thin t ∨
      t = standardTypeBTriangle024 ∨
      t = standardTypeBSourceTriangle123 ∨
      t = standardTypeBSourceTriangle013 ∨
      t = standardTypeBSourceTriangle134 ∨
      t = standardTypeBSourceTriangle012 := by
  rcases ht with hmin | hsrc
  · exact Or.inl hmin
  rcases hsrc with h024 | h123 | h013 | h134 | h012
  · exact Or.inr (Or.inl
      (isStandardVertexTriangle_eq_triangle
        (by decide) (by decide) h024))
  · exact Or.inr (Or.inr (Or.inl
      (isStandardVertexTriangle_eq_triangle
        (by decide) (by decide) h123)))
  · exact Or.inr (Or.inr (Or.inr (Or.inl
      (isStandardVertexTriangle_eq_triangle
        (by decide) (by decide) h013))))
  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inl
      (isStandardVertexTriangle_eq_triangle
        (by decide) (by decide) h134)))))
  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr
      (isStandardVertexTriangle_eq_triangle
        (by decide) (by decide) h012)))))

/-! ## Collapse images of the remaining source faces -/

/-- Minimal thinness is preserved by q12. -/
theorem standardTypeBCollapse12_map_minimal
    {t : (Δ[4] : SSet.{u}).obj (op ⦋2⦌)}
    (ht : (minimalScaling (Δ[4] : SSet.{u})).thin t) :
    (minimalScaling (Δ[3] : SSet.{u})).thin
      (standardTypeBCollapse12.app (op ⦋2⦌) t) := by
  exact
    (minimalScaling_map
      (minimalScaling (Δ[3] : SSet.{u}))
      standardTypeBCollapse12) t ht

/-- Minimal thinness is preserved by q23. -/
theorem standardTypeBCollapse23_map_minimal
    {t : (Δ[4] : SSet.{u}).obj (op ⦋2⦌)}
    (ht : (minimalScaling (Δ[4] : SSet.{u})).thin t) :
    (minimalScaling (Δ[3] : SSet.{u})).thin
      (standardTypeBCollapse23.app (op ⦋2⦌) t) := by
  exact
    (minimalScaling_map
      (minimalScaling (Δ[3] : SSet.{u}))
      standardTypeBCollapse23) t ht

/-- Under q12 the source face `123` becomes degenerate (`112`). -/
theorem standardTypeBCollapse12_triangle_source123_minimal :
    (minimalScaling (Δ[3] : SSet.{u})).thin
      (standardTypeBCollapse12.app (op ⦋2⦌)
        standardTypeBSourceTriangle123) := by
  apply minimalScaling_stdSimplex_thin_of_zero_eq_one
  rfl

/-- Under q12 the source face `012` becomes degenerate (`011`). -/
theorem standardTypeBCollapse12_triangle_source012_minimal :
    (minimalScaling (Δ[3] : SSet.{u})).thin
      (standardTypeBCollapse12.app (op ⦋2⦌)
        standardTypeBSourceTriangle012) := by
  apply minimalScaling_stdSimplex_thin_of_one_eq_two
  rfl

/-- Under q23 the source face `123` becomes degenerate (`122`). -/
theorem standardTypeBCollapse23_triangle_source123_minimal :
    (minimalScaling (Δ[3] : SSet.{u})).thin
      (standardTypeBCollapse23.app (op ⦋2⦌)
        standardTypeBSourceTriangle123) := by
  apply minimalScaling_stdSimplex_thin_of_one_eq_two
  rfl

/-- Under q23 the source face `012` stays `012`. -/
theorem standardTypeBCollapse23_triangle_source012 :
    standardTypeBCollapse23.app (op ⦋2⦌)
        standardTypeBSourceTriangle012 =
      standardTypeBThreeTriangle012 := by
  apply SSet.stdSimplex.ext
  intro j
  fin_cases j <;> rfl

/-! ## Exact source-generated q12/q23 base scalings -/

/-- Exact finite characterization of the q12 source-generated base. -/
theorem standardTypeBCollapse12Base_thin_iff
    (t : (Δ[3] : SSet.{u}).obj (op ⦋2⦌)) :
    standardTypeBCollapse12BaseScaling.thin t ↔
      (minimalScaling (Δ[3] : SSet.{u})).thin t ∨
        t = standardTypeBThreeTriangle012 ∨
        t = standardTypeBThreeTriangle013 ∨
        t = standardTypeBThreeTriangle123 := by
  constructor
  · intro ht
    change
      (minimalScaling (Δ[3] : SSet.{u})).thin t ∨
        ∃ x : (Δ[4] : SSet.{u}).obj (op ⦋2⦌),
          standardTypeBSourceScaling.thin x ∧
            standardTypeBCollapse12.app (op ⦋2⦌) x = t at ht
    rcases ht with hmin | ⟨x, hx, hxt⟩
    · exact Or.inl hmin
    rcases standardTypeBSourceScaling_thin_cases hx with
        hmin | h024 | h123 | h013 | h134 | h012
    · left
      rw [← hxt]
      exact standardTypeBCollapse12_map_minimal hmin
    · subst x
      right
      right
      left
      exact hxt.symm.trans standardTypeBCollapse12_triangle_024
    · subst x
      left
      rw [← hxt]
      exact standardTypeBCollapse12_triangle_source123_minimal
    · subst x
      right
      left
      exact hxt.symm.trans standardTypeBCollapse12_triangle_source013
    · subst x
      right
      right
      right
      exact hxt.symm.trans standardTypeBCollapse12_triangle_source134
    · subst x
      left
      rw [← hxt]
      exact standardTypeBCollapse12_triangle_source012_minimal
  · intro ht
    rcases ht with hmin | h012 | h013 | h123
    · exact standardTypeBCollapse12Base_minimal_thin t hmin
    · subst t
      exact standardTypeBCollapse12Base_triangle_012_thin
    · subst t
      exact standardTypeBCollapse12Base_triangle_013_thin
    · subst t
      exact standardTypeBCollapse12Base_triangle_123_thin

/-- Exact finite characterization of the q23 source-generated base. -/
theorem standardTypeBCollapse23Base_thin_iff
    (t : (Δ[3] : SSet.{u}).obj (op ⦋2⦌)) :
    standardTypeBCollapse23BaseScaling.thin t ↔
      (minimalScaling (Δ[3] : SSet.{u})).thin t ∨
        t = standardTypeBThreeTriangle012 ∨
        t = standardTypeBThreeTriangle023 ∨
        t = standardTypeBThreeTriangle123 := by
  constructor
  · intro ht
    change
      (minimalScaling (Δ[3] : SSet.{u})).thin t ∨
        ∃ x : (Δ[4] : SSet.{u}).obj (op ⦋2⦌),
          standardTypeBSourceScaling.thin x ∧
            standardTypeBCollapse23.app (op ⦋2⦌) x = t at ht
    rcases ht with hmin | ⟨x, hx, hxt⟩
    · exact Or.inl hmin
    rcases standardTypeBSourceScaling_thin_cases hx with
        hmin | h024 | h123 | h013 | h134 | h012
    · left
      rw [← hxt]
      exact standardTypeBCollapse23_map_minimal hmin
    · subst x
      right
      right
      left
      exact hxt.symm.trans standardTypeBCollapse23_triangle_024
    · subst x
      left
      rw [← hxt]
      exact standardTypeBCollapse23_triangle_source123_minimal
    · subst x
      right
      left
      exact hxt.symm.trans standardTypeBCollapse23_triangle_source013
    · subst x
      right
      right
      right
      exact hxt.symm.trans standardTypeBCollapse23_triangle_source134
    · subst x
      right
      left
      exact hxt.symm.trans standardTypeBCollapse23_triangle_source012
  · intro ht
    rcases ht with hmin | h012 | h023 | h123
    · exact standardTypeBCollapse23Base_minimal_thin t hmin
    · subst t
      exact standardTypeBCollapse23Base_triangle_012_thin
    · subst t
      exact standardTypeBCollapse23Base_triangle_023_thin
    · subst t
      exact standardTypeBCollapse23Base_triangle_123_thin

/-! ## The intrinsic horn-saturated type-(A) three-simplex scaling -/

/-- On a fixed `Δ[3]`, saturate the standard type-(A) target scaling by every
triangle already lying in the corresponding inner horn.  When the incoming
horn scaling is maximal, this is exactly the finite thin-triangle predicate
produced by the type-(A) cobase change. -/
def standardTypeAThreeHornSaturatedScaling
    (i : Fin 4) : ScaledSimplicialSet (Δ[3] : SSet.{u}) where
  thin := fun t =>
    (standardTypeASimplexScaling i).thin t ∨
      t ∈ (Λ[3, i] : SSet.{u}).obj (op ⦋2⦌)
  thin_sigma_zero := by
    intro x
    exact Or.inl ((standardTypeASimplexScaling i).thin_sigma_zero x)
  thin_sigma_one := by
    intro x
    exact Or.inl ((standardTypeASimplexScaling i).thin_sigma_one x)

/-- The four named faces are the four standard cofaces. -/
theorem standardTypeBThreeTriangle012_eq_delta3 :
    standardTypeBThreeTriangle012 =
      (SSet.stdSimplex.objEquiv (m := op ⦋2⦌)).symm
        (SimplexCategory.δ (3 : Fin 4)) := by
  apply SSet.stdSimplex.ext
  intro j
  fin_cases j <;> rfl

/-- `013` is coface `δ₂`. -/
theorem standardTypeBThreeTriangle013_eq_delta2 :
    standardTypeBThreeTriangle013 =
      (SSet.stdSimplex.objEquiv (m := op ⦋2⦌)).symm
        (SimplexCategory.δ (2 : Fin 4)) := by
  apply SSet.stdSimplex.ext
  intro j
  fin_cases j <;> rfl

/-- `023` is coface `δ₁`. -/
theorem standardTypeBThreeTriangle023_eq_delta1 :
    standardTypeBThreeTriangle023 =
      (SSet.stdSimplex.objEquiv (m := op ⦋2⦌)).symm
        (SimplexCategory.δ (1 : Fin 4)) := by
  apply SSet.stdSimplex.ext
  intro j
  fin_cases j <;> rfl

/-- `123` is coface `δ₀`. -/
theorem standardTypeBThreeTriangle123_eq_delta0 :
    standardTypeBThreeTriangle123 =
      (SSet.stdSimplex.objEquiv (m := op ⦋2⦌)).symm
        (SimplexCategory.δ (0 : Fin 4)) := by
  apply SSet.stdSimplex.ext
  intro j
  fin_cases j <;> rfl

/-- A named coface belongs to an inner 3-horn exactly when it is not the
missing coface. -/
theorem standardTypeBThreeTriangle012_mem_horn_one :
    standardTypeBThreeTriangle012 ∈
      (Λ[3, (1 : Fin 4)] : SSet.{u}).obj (op ⦋2⦌) := by
  rw [standardTypeBThreeTriangle012_eq_delta3,
    SSet.objEquiv_symm_δ_mem_horn_iff]
  decide

/-- `013` belongs to horn 1. -/
theorem standardTypeBThreeTriangle013_mem_horn_one :
    standardTypeBThreeTriangle013 ∈
      (Λ[3, (1 : Fin 4)] : SSet.{u}).obj (op ⦋2⦌) := by
  rw [standardTypeBThreeTriangle013_eq_delta2,
    SSet.objEquiv_symm_δ_mem_horn_iff]
  decide

/-- `123` belongs to horn 1. -/
theorem standardTypeBThreeTriangle123_mem_horn_one :
    standardTypeBThreeTriangle123 ∈
      (Λ[3, (1 : Fin 4)] : SSet.{u}).obj (op ⦋2⦌) := by
  rw [standardTypeBThreeTriangle123_eq_delta0,
    SSet.objEquiv_symm_δ_mem_horn_iff]
  decide

/-- The missing face `023` does not belong to horn 1. -/
theorem standardTypeBThreeTriangle023_notMem_horn_one :
    standardTypeBThreeTriangle023 ∉
      (Λ[3, (1 : Fin 4)] : SSet.{u}).obj (op ⦋2⦌) := by
  rw [standardTypeBThreeTriangle023_eq_delta1,
    SSet.objEquiv_symm_δ_notMem_horn_iff]

/-- `012` belongs to horn 2. -/
theorem standardTypeBThreeTriangle012_mem_horn_two :
    standardTypeBThreeTriangle012 ∈
      (Λ[3, (2 : Fin 4)] : SSet.{u}).obj (op ⦋2⦌) := by
  rw [standardTypeBThreeTriangle012_eq_delta3,
    SSet.objEquiv_symm_δ_mem_horn_iff]
  decide

/-- `023` belongs to horn 2. -/
theorem standardTypeBThreeTriangle023_mem_horn_two :
    standardTypeBThreeTriangle023 ∈
      (Λ[3, (2 : Fin 4)] : SSet.{u}).obj (op ⦋2⦌) := by
  rw [standardTypeBThreeTriangle023_eq_delta1,
    SSet.objEquiv_symm_δ_mem_horn_iff]
  decide

/-- `123` belongs to horn 2. -/
theorem standardTypeBThreeTriangle123_mem_horn_two :
    standardTypeBThreeTriangle123 ∈
      (Λ[3, (2 : Fin 4)] : SSet.{u}).obj (op ⦋2⦌) := by
  rw [standardTypeBThreeTriangle123_eq_delta0,
    SSet.objEquiv_symm_δ_mem_horn_iff]
  decide

/-- The missing face `013` does not belong to horn 2. -/
theorem standardTypeBThreeTriangle013_notMem_horn_two :
    standardTypeBThreeTriangle013 ∉
      (Λ[3, (2 : Fin 4)] : SSet.{u}).obj (op ⦋2⦌) := by
  rw [standardTypeBThreeTriangle013_eq_delta2,
    SSet.objEquiv_symm_δ_notMem_horn_iff]

/-- The type-(A) distinguished face at index 1 is exactly `012`. -/
theorem standardTypeAThree_index_one_triangle_012_thin :
    (standardTypeASimplexScaling (1 : Fin 4)).thin
      standardTypeBThreeTriangle012 := by
  exact Or.inr ⟨rfl, rfl, rfl⟩

/-- The type-(A) distinguished face at index 2 is exactly `123`. -/
theorem standardTypeAThree_index_two_triangle_123_thin :
    (standardTypeASimplexScaling (2 : Fin 4)).thin
      standardTypeBThreeTriangle123 := by
  exact Or.inr ⟨rfl, rfl, rfl⟩

/-- Horn-saturated type-(A) scaling at index 1 is exactly the q12 base. -/
theorem standardTypeAThreeHornSaturatedScaling_one_eq_q12Base :
    standardTypeAThreeHornSaturatedScaling (1 : Fin 4) =
      standardTypeBCollapse12BaseScaling := by
  apply scaling_eq_of_le_antisymm
  · intro t ht
    rcases ht with hA | hhorn
    · rcases hA with hmin | hdist
      · exact standardTypeBCollapse12Base_minimal_thin t hmin
      · have ht012 : t = standardTypeBThreeTriangle012 := by
          apply SSet.stdSimplex.ext
          intro a
          fin_cases a
          · apply Fin.ext
            change (t 0).val = 0
            have h := hdist.2.1
            change (t 0).val + 1 = 1 at h
            omega
          · exact hdist.1
          · apply Fin.ext
            change (t 2).val = 2
            have h := hdist.2.2
            change 1 + 1 = (t 2).val at h
            omega
        subst t
        exact standardTypeBCollapse12Base_triangle_012_thin
    · rcases standardTypeBThree_triangle_minimal_or_four_faces t with
          hmin | h012 | h013 | h023 | h123
      · exact standardTypeBCollapse12Base_minimal_thin t hmin
      · subst t
        exact standardTypeBCollapse12Base_triangle_012_thin
      · subst t
        exact standardTypeBCollapse12Base_triangle_013_thin
      · subst t
        exact (standardTypeBThreeTriangle023_notMem_horn_one hhorn).elim
      · subst t
        exact standardTypeBCollapse12Base_triangle_123_thin
  · intro t ht
    rw [standardTypeBCollapse12Base_thin_iff t] at ht
    rcases ht with hmin | h012 | h013 | h123
    · exact Or.inl (Or.inl hmin)
    · subst t
      exact Or.inl standardTypeAThree_index_one_triangle_012_thin
    · subst t
      exact Or.inr standardTypeBThreeTriangle013_mem_horn_one
    · subst t
      exact Or.inr standardTypeBThreeTriangle123_mem_horn_one

/-- Horn-saturated type-(A) scaling at index 2 is exactly the q23 base. -/
theorem standardTypeAThreeHornSaturatedScaling_two_eq_q23Base :
    standardTypeAThreeHornSaturatedScaling (2 : Fin 4) =
      standardTypeBCollapse23BaseScaling := by
  apply scaling_eq_of_le_antisymm
  · intro t ht
    rcases ht with hA | hhorn
    · rcases hA with hmin | hdist
      · exact standardTypeBCollapse23Base_minimal_thin t hmin
      · have ht123 : t = standardTypeBThreeTriangle123 := by
          apply SSet.stdSimplex.ext
          intro a
          fin_cases a
          · apply Fin.ext
            change (t 0).val = 1
            have h := hdist.2.1
            change (t 0).val + 1 = 2 at h
            omega
          · exact hdist.1
          · apply Fin.ext
            change (t 2).val = 3
            have h := hdist.2.2
            change 2 + 1 = (t 2).val at h
            omega
        subst t
        exact standardTypeBCollapse23Base_triangle_123_thin
    · rcases standardTypeBThree_triangle_minimal_or_four_faces t with
          hmin | h012 | h013 | h023 | h123
      · exact standardTypeBCollapse23Base_minimal_thin t hmin
      · subst t
        exact standardTypeBCollapse23Base_triangle_012_thin
      · subst t
        exact (standardTypeBThreeTriangle013_notMem_horn_two hhorn).elim
      · subst t
        exact standardTypeBCollapse23Base_triangle_023_thin
      · subst t
        exact standardTypeBCollapse23Base_triangle_123_thin
  · intro t ht
    rw [standardTypeBCollapse23Base_thin_iff t] at ht
    rcases ht with hmin | h012 | h023 | h123
    · exact Or.inl (Or.inl hmin)
    · subst t
      exact Or.inr standardTypeBThreeTriangle012_mem_horn_two
    · subst t
      exact Or.inr standardTypeBThreeTriangle023_mem_horn_two
    · subst t
      exact Or.inl standardTypeAThree_index_two_triangle_123_thin

/-! ## Complete fixed A/B table -/

/-- The entire exceptional three-simplex residual table. -/
structure StandardTypeAThreeResidualTable : Prop where
  index_one_base :
    standardTypeAThreeHornSaturatedScaling (1 : Fin 4) =
      standardTypeBCollapse12BaseScaling
  index_one_completed :
    standardTypeBCollapse12CompletedScaling =
      ScaledSimplicialSet.maximal (Δ[3] : SSet.{u})
  index_two_base :
    standardTypeAThreeHornSaturatedScaling (2 : Fin 4) =
      standardTypeBCollapse23BaseScaling
  index_two_completed :
    standardTypeBCollapse23CompletedScaling =
      ScaledSimplicialSet.maximal (Δ[3] : SSet.{u})

/-- Canonical certificate of the complete fixed A/B residual table. -/
def standardTypeAThreeResidualTable : StandardTypeAThreeResidualTable.{u} where
  index_one_base := standardTypeAThreeHornSaturatedScaling_one_eq_q12Base
  index_one_completed := standardTypeBCollapse12CompletedScaling_eq_maximal
  index_two_base := standardTypeAThreeHornSaturatedScaling_two_eq_q23Base
  index_two_completed := standardTypeBCollapse23CompletedScaling_eq_maximal

/-! ## Attach the fixed table to actual three-dimensional prism cells -/

/-- Every actual attached three-cell has one of the two fixed inner indices,
and its missing face and normalized A/B residual table are exactly q12 or q23. -/
theorem standardTypeABoundaryPrism_cell_target_dim_three_residual_table
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h3 : c.dim + 1 = 3) :
    (standardTypeABoundaryPrismCellIndex3 g j c h3 = (1 : Fin 4) ∧
        standardTypeABoundaryPrismCellMissingFace3 g j c h3 =
          standardTypeBThreeTriangle023 ∧
        standardTypeAThreeHornSaturatedScaling (1 : Fin 4) =
          standardTypeBCollapse12BaseScaling ∧
        standardTypeBCollapse12CompletedScaling =
          ScaledSimplicialSet.maximal (Δ[3] : SSet.{u})) ∨
      (standardTypeABoundaryPrismCellIndex3 g j c h3 = (2 : Fin 4) ∧
        standardTypeABoundaryPrismCellMissingFace3 g j c h3 =
          standardTypeBThreeTriangle013 ∧
        standardTypeAThreeHornSaturatedScaling (2 : Fin 4) =
          standardTypeBCollapse23BaseScaling ∧
        standardTypeBCollapse23CompletedScaling =
          ScaledSimplicialSet.maximal (Δ[3] : SSet.{u})) := by
  rcases standardTypeABoundaryPrismCellIndex3_eq_one_or_two g j c h3 with
      hidx | hidx
  · left
    exact ⟨hidx,
      standardTypeABoundaryPrismCellMissingFace3_eq_023_of_index_one
        g j c h3 hidx,
      standardTypeAThreeHornSaturatedScaling_one_eq_q12Base,
      standardTypeBCollapse12CompletedScaling_eq_maximal⟩
  · right
    exact ⟨hidx,
      standardTypeABoundaryPrismCellMissingFace3_eq_013_of_index_two
        g j c h3 hidx,
      standardTypeAThreeHornSaturatedScaling_two_eq_q23Base,
      standardTypeBCollapse23CompletedScaling_eq_maximal⟩

/-- In the only genuinely exceptional origin branch (`g.n = 2`, attached
dimension three), the actual target is maximal and the fixed residual table is
q12 or q23 according to the actual cell index. -/
theorem standardTypeABoundaryPrism_generator_two_target_three_complete_local_table
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (hn2 : g.n = 2)
    (h3 : c.dim + 1 = 3) :
    standardTypeABoundaryPrismCellScaling g j c =
        ScaledSimplicialSet.maximal (Δ[c.dim + 1] : SSet.{u}) ∧
      ((standardTypeABoundaryPrismCellIndex3 g j c h3 = (1 : Fin 4) ∧
          standardTypeABoundaryPrismCellMissingFace3 g j c h3 =
            standardTypeBThreeTriangle023 ∧
          standardTypeAThreeHornSaturatedScaling (1 : Fin 4) =
            standardTypeBCollapse12BaseScaling ∧
          standardTypeBCollapse12CompletedScaling =
            ScaledSimplicialSet.maximal (Δ[3] : SSet.{u})) ∨
        (standardTypeABoundaryPrismCellIndex3 g j c h3 = (2 : Fin 4) ∧
          standardTypeABoundaryPrismCellMissingFace3 g j c h3 =
            standardTypeBThreeTriangle013 ∧
          standardTypeAThreeHornSaturatedScaling (2 : Fin 4) =
            standardTypeBCollapse23BaseScaling ∧
          standardTypeBCollapse23CompletedScaling =
            ScaledSimplicialSet.maximal (Δ[3] : SSet.{u}))) := by
  exact ⟨
    standardTypeABoundaryPrismCellScaling_eq_maximal_of_generator_two_target_three
      g j c hn2 h3,
    standardTypeABoundaryPrism_cell_target_dim_three_residual_table
      g j c h3⟩

/-!
The fixed low-dimensional geometry needed by the scaled rank filtration is now
rigid and finite:

```text
attached N >= 4 : pure A                        (v1.66)
attached N = 2  : pure A                        (v1.67)
attached N = 3  : fixed index is 1 or 2

fixed index 1:
  missing face = 023
  horn-saturated A scaling = q12 base
  q12 completion = maximal Delta[3]

fixed index 2:
  missing face = 013
  horn-saturated A scaling = q23 base
  q23 completion = maximal Delta[3]

and for original n = 2, N = 3:
  actual target scaling = maximal.
```

Thus no additional low-dimensional scaling pattern remains to be discovered.
The next categorical unit only has to transport the actual A-pushout of an
`n = 2`, `N = 3` cell to the corresponding fixed horn-saturated scaling above,
and prove equal-dimensional `n = 3`, `N = 3` cells are pure A by first-coordinate
rigidity.  After those transport statements, every rank cell is literally A or
A followed by one q12/q23 B-completion, which is the exact local input for the
scaled transfinite rank filtration and the v1.59 cellular certificate.
-/

end

end KUOS.DependentOriginationStandardTypeABoundaryPrismThreeResidualClassificationV1_69
