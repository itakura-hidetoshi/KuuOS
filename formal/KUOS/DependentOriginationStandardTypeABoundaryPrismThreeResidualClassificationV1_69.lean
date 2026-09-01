import KUOS.DependentOriginationStandardTypeBThreeSimplexMaximalCompletionV1_68

namespace KUOS.DependentOriginationStandardTypeABoundaryPrismThreeResidualClassificationV1_69

open CategoryTheory
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAScaledPushoutSourceEnrichmentV1_53
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

/-! # Complete fixed three-simplex A/B residual classification v1.69 -/

def standardTypeBSourceTriangle123 :
    (Δ[4] : SSet.{u}).obj (op ⦋2⦌) :=
  SSet.stdSimplex.triangle
    (1 : Fin 5) 2 3 (by decide) (by decide)

def standardTypeBSourceTriangle012 :
    (Δ[4] : SSet.{u}).obj (op ⦋2⦌) :=
  SSet.stdSimplex.triangle
    (0 : Fin 5) 1 2 (by decide) (by decide)

theorem standardTypeBSourceTriangle123_isSourceTriangle :
    IsStandardTypeBSourceTriangle standardTypeBSourceTriangle123 := by
  exact Or.inr (Or.inl ⟨rfl, rfl, rfl⟩)

theorem standardTypeBSourceTriangle012_isSourceTriangle :
    IsStandardTypeBSourceTriangle standardTypeBSourceTriangle012 := by
  exact Or.inr (Or.inr (Or.inr (Or.inr ⟨rfl, rfl, rfl⟩)))

theorem standardTypeBSourceTriangle123_source_thin :
    standardTypeBSourceScaling.thin standardTypeBSourceTriangle123 := by
  exact Or.inr standardTypeBSourceTriangle123_isSourceTriangle

theorem standardTypeBSourceTriangle012_source_thin :
    standardTypeBSourceScaling.thin standardTypeBSourceTriangle012 := by
  exact Or.inr standardTypeBSourceTriangle012_isSourceTriangle

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

theorem standardTypeBCollapse12_map_minimal
    {t : (Δ[4] : SSet.{u}).obj (op ⦋2⦌)}
    (ht : (minimalScaling (Δ[4] : SSet.{u})).thin t) :
    (minimalScaling (Δ[3] : SSet.{u})).thin
      (standardTypeBCollapse12.app (op ⦋2⦌) t) := by
  exact
    (minimalScaling_map
      (minimalScaling (Δ[3] : SSet.{u}))
      standardTypeBCollapse12) t ht

theorem standardTypeBCollapse23_map_minimal
    {t : (Δ[4] : SSet.{u}).obj (op ⦋2⦌)}
    (ht : (minimalScaling (Δ[4] : SSet.{u})).thin t) :
    (minimalScaling (Δ[3] : SSet.{u})).thin
      (standardTypeBCollapse23.app (op ⦋2⦌) t) := by
  exact
    (minimalScaling_map
      (minimalScaling (Δ[3] : SSet.{u}))
      standardTypeBCollapse23) t ht

theorem standardTypeBCollapse12_triangle_source123_minimal :
    (minimalScaling (Δ[3] : SSet.{u})).thin
      (standardTypeBCollapse12.app (op ⦋2⦌)
        standardTypeBSourceTriangle123) := by
  apply minimalScaling_stdSimplex_thin_of_zero_eq_one
  rfl

theorem standardTypeBCollapse12_triangle_source012_minimal :
    (minimalScaling (Δ[3] : SSet.{u})).thin
      (standardTypeBCollapse12.app (op ⦋2⦌)
        standardTypeBSourceTriangle012) := by
  apply minimalScaling_stdSimplex_thin_of_one_eq_two
  rfl

theorem standardTypeBCollapse23_triangle_source123_minimal :
    (minimalScaling (Δ[3] : SSet.{u})).thin
      (standardTypeBCollapse23.app (op ⦋2⦌)
        standardTypeBSourceTriangle123) := by
  apply minimalScaling_stdSimplex_thin_of_one_eq_two
  rfl

theorem standardTypeBCollapse23_triangle_source012 :
    standardTypeBCollapse23.app (op ⦋2⦌)
        standardTypeBSourceTriangle012 =
      standardTypeBThreeTriangle012 := by
  apply SSet.stdSimplex.ext
  intro j
  fin_cases j <;> rfl

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

def standardTypeAThreeHornSaturatedScaling
    (i : Fin 4) : ScaledSimplicialSet (Δ[3] : SSet.{u}) where
  thin := fun t =>
    (standardTypeASimplexScaling i).thin t ∨
      t ∈ (SSet.horn.{u} 3 i).obj (op ⦋2⦌)
  thin_sigma_zero := by
    intro x
    exact Or.inl ((standardTypeASimplexScaling i).thin_sigma_zero x)
  thin_sigma_one := by
    intro x
    exact Or.inl ((standardTypeASimplexScaling i).thin_sigma_one x)

theorem standardTypeBThreeTriangle012_eq_delta3 :
    standardTypeBThreeTriangle012 =
      (SSet.stdSimplex.objEquiv (m := op ⦋2⦌)).symm
        (SimplexCategory.δ (3 : Fin 4)) := by
  apply SSet.stdSimplex.ext
  intro j
  fin_cases j <;> rfl

theorem standardTypeBThreeTriangle013_eq_delta2 :
    standardTypeBThreeTriangle013 =
      (SSet.stdSimplex.objEquiv (m := op ⦋2⦌)).symm
        (SimplexCategory.δ (2 : Fin 4)) := by
  apply SSet.stdSimplex.ext
  intro j
  fin_cases j <;> rfl

theorem standardTypeBThreeTriangle023_eq_delta1 :
    standardTypeBThreeTriangle023 =
      (SSet.stdSimplex.objEquiv (m := op ⦋2⦌)).symm
        (SimplexCategory.δ (1 : Fin 4)) := by
  apply SSet.stdSimplex.ext
  intro j
  fin_cases j <;> rfl

theorem standardTypeBThreeTriangle123_eq_delta0 :
    standardTypeBThreeTriangle123 =
      (SSet.stdSimplex.objEquiv (m := op ⦋2⦌)).symm
        (SimplexCategory.δ (0 : Fin 4)) := by
  apply SSet.stdSimplex.ext
  intro j
  fin_cases j <;> rfl

theorem standardTypeBThreeTriangle012_mem_horn_one :
    standardTypeBThreeTriangle012 ∈
      (SSet.horn.{u} 3 (1 : Fin 4)).obj (op ⦋2⦌) := by
  rw [standardTypeBThreeTriangle012_eq_delta3,
    SSet.objEquiv_symm_δ_mem_horn_iff]
  decide

theorem standardTypeBThreeTriangle013_mem_horn_one :
    standardTypeBThreeTriangle013 ∈
      (SSet.horn.{u} 3 (1 : Fin 4)).obj (op ⦋2⦌) := by
  rw [standardTypeBThreeTriangle013_eq_delta2,
    SSet.objEquiv_symm_δ_mem_horn_iff]
  decide

theorem standardTypeBThreeTriangle123_mem_horn_one :
    standardTypeBThreeTriangle123 ∈
      (SSet.horn.{u} 3 (1 : Fin 4)).obj (op ⦋2⦌) := by
  rw [standardTypeBThreeTriangle123_eq_delta0,
    SSet.objEquiv_symm_δ_mem_horn_iff]
  decide

theorem standardTypeBThreeTriangle023_notMem_horn_one :
    standardTypeBThreeTriangle023 ∉
      (SSet.horn.{u} 3 (1 : Fin 4)).obj (op ⦋2⦌) := by
  rw [standardTypeBThreeTriangle023_eq_delta1,
    SSet.objEquiv_symm_δ_notMem_horn_iff]

theorem standardTypeBThreeTriangle012_mem_horn_two :
    standardTypeBThreeTriangle012 ∈
      (SSet.horn.{u} 3 (2 : Fin 4)).obj (op ⦋2⦌) := by
  rw [standardTypeBThreeTriangle012_eq_delta3,
    SSet.objEquiv_symm_δ_mem_horn_iff]
  decide

theorem standardTypeBThreeTriangle023_mem_horn_two :
    standardTypeBThreeTriangle023 ∈
      (SSet.horn.{u} 3 (2 : Fin 4)).obj (op ⦋2⦌) := by
  rw [standardTypeBThreeTriangle023_eq_delta1,
    SSet.objEquiv_symm_δ_mem_horn_iff]
  decide

theorem standardTypeBThreeTriangle123_mem_horn_two :
    standardTypeBThreeTriangle123 ∈
      (SSet.horn.{u} 3 (2 : Fin 4)).obj (op ⦋2⦌) := by
  rw [standardTypeBThreeTriangle123_eq_delta0,
    SSet.objEquiv_symm_δ_mem_horn_iff]
  decide

theorem standardTypeBThreeTriangle013_notMem_horn_two :
    standardTypeBThreeTriangle013 ∉
      (SSet.horn.{u} 3 (2 : Fin 4)).obj (op ⦋2⦌) := by
  rw [standardTypeBThreeTriangle013_eq_delta2,
    SSet.objEquiv_symm_δ_notMem_horn_iff]

theorem standardTypeAThree_index_one_triangle_012_thin :
    (standardTypeASimplexScaling (1 : Fin 4)).thin
      standardTypeBThreeTriangle012 := by
  exact Or.inr ⟨rfl, rfl, rfl⟩

theorem standardTypeAThree_index_two_triangle_123_thin :
    (standardTypeASimplexScaling (2 : Fin 4)).thin
      standardTypeBThreeTriangle123 := by
  exact Or.inr ⟨rfl, rfl, rfl⟩

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

structure StandardTypeAThreeResidualTable.{u} : Prop where
  index_one_base :
    standardTypeAThreeHornSaturatedScaling.{u} (1 : Fin 4) =
      standardTypeBCollapse12BaseScaling.{u}
  index_one_completed :
    standardTypeBCollapse12CompletedScaling =
      ScaledSimplicialSet.maximal (Δ[3] : SSet.{u})
  index_two_base :
    standardTypeAThreeHornSaturatedScaling.{u} (2 : Fin 4) =
      standardTypeBCollapse23BaseScaling.{u}
  index_two_completed :
    standardTypeBCollapse23CompletedScaling =
      ScaledSimplicialSet.maximal (Δ[3] : SSet.{u})

def standardTypeAThreeResidualTable : StandardTypeAThreeResidualTable.{u} where
  index_one_base := standardTypeAThreeHornSaturatedScaling_one_eq_q12Base
  index_one_completed := standardTypeBCollapse12CompletedScaling_eq_maximal
  index_two_base := standardTypeAThreeHornSaturatedScaling_two_eq_q23Base
  index_two_completed := standardTypeBCollapse23CompletedScaling_eq_maximal

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

end

end KUOS.DependentOriginationStandardTypeABoundaryPrismThreeResidualClassificationV1_69