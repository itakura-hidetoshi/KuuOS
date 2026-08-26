import KUOS.DependentOriginationStandardTypeABoundaryPrismN2MaximalFrontierV1_67

namespace KUOS.DependentOriginationStandardTypeBThreeSimplexMaximalCompletionV1_68

open CategoryTheory
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeAScaledPushoutSourceEnrichmentV1_53
open KUOS.DependentOriginationStandardTypeBScalingPushoutV1_56
open KUOS.DependentOriginationStandardTypeBThreeSimplexCompletionV1_57
open KUOS.DependentOriginationStandardTypeABoundaryPrismCellACompatibilityV1_66
open KUOS.DependentOriginationStandardTypeABoundaryPrismN2MaximalFrontierV1_67

universe u

noncomputable section

/-!
# Maximal target of the q12/q23 type-(B) three-simplex completions v1.68

Version v1.67 proved that every boundary-prism cell over an original `n = 2`
type-(A) generator has maximal exact target scaling.  To identify the remaining
three-dimensional cells with the already constructed q12/q23 type-(B)
completion pushouts, one needs the converse local statement on the fixed
three-simplex: both q12 and q23 completions really produce the maximal scaling
on `Delta[3]`.

This file proves that statement directly and finitely.

Every 2-simplex of `Delta[3]` is either minimally thin because two adjacent
vertices agree, or is one of the four strictly increasing faces

```text
012, 013, 023, 123.
```

For q12 the source-generated base already contains `012`, `013`, and `123`,
and the type-(B) completion supplies `023`.  For q23 the base already contains
`012`, `023`, and `123`, and the completion supplies `013`.  Hence both
completed scalings are literally maximal.

No model-structure argument is used: this is only the finite standard-simplex
calculation sitting underneath the categorical pushout theorem of v1.57.
-/

/-! ## The two remaining nondegenerate three-simplex faces -/

/-- The face `012` of `Delta[3]`. -/
def standardTypeBThreeTriangle012 :
    (Δ[3] : SSet.{u}).obj (op ⦋2⦌) :=
  SSet.stdSimplex.triangle
    (0 : Fin 4) 1 2 (by decide) (by decide)

/-- The face `123` of `Delta[3]`. -/
def standardTypeBThreeTriangle123 :
    (Δ[3] : SSet.{u}).obj (op ⦋2⦌) :=
  SSet.stdSimplex.triangle
    (1 : Fin 4) 2 3 (by decide) (by decide)

/-! ## Source triangles whose collapse images are 012 and 123 -/

/-- The type-(B) source triangle `013` in `Delta[4]`. -/
def standardTypeBSourceTriangle013 :
    (Δ[4] : SSet.{u}).obj (op ⦋2⦌) :=
  SSet.stdSimplex.triangle
    (0 : Fin 5) 1 3 (by decide) (by decide)

/-- The type-(B) source triangle `134` in `Delta[4]`. -/
def standardTypeBSourceTriangle134 :
    (Δ[4] : SSet.{u}).obj (op ⦋2⦌) :=
  SSet.stdSimplex.triangle
    (1 : Fin 5) 3 4 (by decide) (by decide)

/-- `013` belongs to the five designated source-thin type-(B) triangles. -/
theorem standardTypeBSourceTriangle013_isSourceTriangle :
    IsStandardTypeBSourceTriangle standardTypeBSourceTriangle013 := by
  exact Or.inr (Or.inr (Or.inl ⟨rfl, rfl, rfl⟩))

/-- `134` belongs to the five designated source-thin type-(B) triangles. -/
theorem standardTypeBSourceTriangle134_isSourceTriangle :
    IsStandardTypeBSourceTriangle standardTypeBSourceTriangle134 := by
  exact Or.inr (Or.inr (Or.inr (Or.inl ⟨rfl, rfl, rfl⟩)))

/-- Hence `013` is thin in the source scaling of the type-(B) generator. -/
theorem standardTypeBSourceTriangle013_source_thin :
    standardTypeBSourceScaling.thin standardTypeBSourceTriangle013 := by
  exact Or.inr standardTypeBSourceTriangle013_isSourceTriangle

/-- Hence `134` is thin in the source scaling of the type-(B) generator. -/
theorem standardTypeBSourceTriangle134_source_thin :
    standardTypeBSourceScaling.thin standardTypeBSourceTriangle134 := by
  exact Or.inr standardTypeBSourceTriangle134_isSourceTriangle

/-- Under q12, source-thin `013` becomes the three-simplex face `012`. -/
theorem standardTypeBCollapse12_triangle_source013 :
    standardTypeBCollapse12.app (op ⦋2⦌) standardTypeBSourceTriangle013 =
      standardTypeBThreeTriangle012 := by
  apply SSet.stdSimplex.ext
  intro j
  fin_cases j <;> rfl

/-- Under q23, source-thin `013` also becomes the three-simplex face `012`. -/
theorem standardTypeBCollapse23_triangle_source013 :
    standardTypeBCollapse23.app (op ⦋2⦌) standardTypeBSourceTriangle013 =
      standardTypeBThreeTriangle012 := by
  apply SSet.stdSimplex.ext
  intro j
  fin_cases j <;> rfl

/-- Under q12, source-thin `134` becomes the three-simplex face `123`. -/
theorem standardTypeBCollapse12_triangle_source134 :
    standardTypeBCollapse12.app (op ⦋2⦌) standardTypeBSourceTriangle134 =
      standardTypeBThreeTriangle123 := by
  apply SSet.stdSimplex.ext
  intro j
  fin_cases j <;> rfl

/-- Under q23, source-thin `134` also becomes the three-simplex face `123`. -/
theorem standardTypeBCollapse23_triangle_source134 :
    standardTypeBCollapse23.app (op ⦋2⦌) standardTypeBSourceTriangle134 =
      standardTypeBThreeTriangle123 := by
  apply SSet.stdSimplex.ext
  intro j
  fin_cases j <;> rfl

/-! ## Both source-generated bases contain the three common faces -/

/-- Every minimally thin triangle is already in the q12 base scaling. -/
theorem standardTypeBCollapse12Base_minimal_thin
    (t : (Δ[3] : SSet.{u}).obj (op ⦋2⦌))
    (ht : (minimalScaling (Δ[3] : SSet.{u})).thin t) :
    standardTypeBCollapse12BaseScaling.thin t := by
  exact Or.inl ht

/-- Every minimally thin triangle is already in the q23 base scaling. -/
theorem standardTypeBCollapse23Base_minimal_thin
    (t : (Δ[3] : SSet.{u}).obj (op ⦋2⦌))
    (ht : (minimalScaling (Δ[3] : SSet.{u})).thin t) :
    standardTypeBCollapse23BaseScaling.thin t := by
  exact Or.inl ht

/-- The q12 base contains `012`, as the image of source-thin `013`. -/
theorem standardTypeBCollapse12Base_triangle_012_thin :
    standardTypeBCollapse12BaseScaling.thin standardTypeBThreeTriangle012 := by
  exact Or.inr
    ⟨standardTypeBSourceTriangle013,
      standardTypeBSourceTriangle013_source_thin,
      standardTypeBCollapse12_triangle_source013⟩

/-- The q23 base contains `012`, as the image of source-thin `013`. -/
theorem standardTypeBCollapse23Base_triangle_012_thin :
    standardTypeBCollapse23BaseScaling.thin standardTypeBThreeTriangle012 := by
  exact Or.inr
    ⟨standardTypeBSourceTriangle013,
      standardTypeBSourceTriangle013_source_thin,
      standardTypeBCollapse23_triangle_source013⟩

/-- The q12 base contains `123`, as the image of source-thin `134`. -/
theorem standardTypeBCollapse12Base_triangle_123_thin :
    standardTypeBCollapse12BaseScaling.thin standardTypeBThreeTriangle123 := by
  exact Or.inr
    ⟨standardTypeBSourceTriangle134,
      standardTypeBSourceTriangle134_source_thin,
      standardTypeBCollapse12_triangle_source134⟩

/-- The q23 base contains `123`, as the image of source-thin `134`. -/
theorem standardTypeBCollapse23Base_triangle_123_thin :
    standardTypeBCollapse23BaseScaling.thin standardTypeBThreeTriangle123 := by
  exact Or.inr
    ⟨standardTypeBSourceTriangle134,
      standardTypeBSourceTriangle134_source_thin,
      standardTypeBCollapse23_triangle_source134⟩

/-! ## Every triangle of Delta[3] is minimal or one of its four faces -/

/-- Finite classification of 2-simplices of `Delta[3]` in the exact form
needed by the two completion scalings. -/
theorem standardTypeBThree_triangle_minimal_or_four_faces
    (t : (Δ[3] : SSet.{u}).obj (op ⦋2⦌)) :
    (minimalScaling (Δ[3] : SSet.{u})).thin t ∨
      t = standardTypeBThreeTriangle012 ∨
      t = standardTypeBThreeTriangle013 ∨
      t = standardTypeBThreeTriangle023 ∨
      t = standardTypeBThreeTriangle123 := by
  by_cases h01 : t 0 = t 1
  · exact Or.inl
      (minimalScaling_stdSimplex_thin_of_zero_eq_one t h01)
  by_cases h12 : t 1 = t 2
  · exact Or.inl
      (minimalScaling_stdSimplex_thin_of_one_eq_two t h12)
  have h01le : t 0 ≤ t 1 :=
    SSet.stdSimplex.monotone_apply t (by decide)
  have h12le : t 1 ≤ t 2 :=
    SSet.stdSimplex.monotone_apply t (by decide)
  have h01lt : t 0 < t 1 := lt_of_le_of_ne h01le h01
  have h12lt : t 1 < t 2 := lt_of_le_of_ne h12le h12
  have hb0 := (t 0).isLt
  have hb1 := (t 1).isLt
  have hb2 := (t 2).isLt
  have hvals :
      ((t 0).val = 0 ∧ (t 1).val = 1 ∧ (t 2).val = 2) ∨
      ((t 0).val = 0 ∧ (t 1).val = 1 ∧ (t 2).val = 3) ∨
      ((t 0).val = 0 ∧ (t 1).val = 2 ∧ (t 2).val = 3) ∨
      ((t 0).val = 1 ∧ (t 1).val = 2 ∧ (t 2).val = 3) := by
    omega
  rcases hvals with h012 | h013 | h023 | h123
  · right
    left
    apply SSet.stdSimplex.ext
    intro a
    fin_cases a
    · apply Fin.ext
      change (t 0).val = 0
      exact h012.1
    · apply Fin.ext
      change (t 1).val = 1
      exact h012.2.1
    · apply Fin.ext
      change (t 2).val = 2
      exact h012.2.2
  · right
    right
    left
    apply SSet.stdSimplex.ext
    intro a
    fin_cases a
    · apply Fin.ext
      change (t 0).val = 0
      exact h013.1
    · apply Fin.ext
      change (t 1).val = 1
      exact h013.2.1
    · apply Fin.ext
      change (t 2).val = 3
      exact h013.2.2
  · right
    right
    right
    left
    apply SSet.stdSimplex.ext
    intro a
    fin_cases a
    · apply Fin.ext
      change (t 0).val = 0
      exact h023.1
    · apply Fin.ext
      change (t 1).val = 2
      exact h023.2.1
    · apply Fin.ext
      change (t 2).val = 3
      exact h023.2.2
  · right
    right
    right
    right
    apply SSet.stdSimplex.ext
    intro a
    fin_cases a
    · apply Fin.ext
      change (t 0).val = 1
      exact h123.1
    · apply Fin.ext
      change (t 1).val = 2
      exact h123.2.1
    · apply Fin.ext
      change (t 2).val = 3
      exact h123.2.2

/-! ## Completion adds the unique missing nondegenerate face -/

/-- Any q12-base-thin triangle remains thin after the type-(B) completion. -/
theorem standardTypeBCollapse12Completed_of_base
    {t : (Δ[3] : SSet.{u}).obj (op ⦋2⦌)}
    (ht : standardTypeBCollapse12BaseScaling.thin t) :
    standardTypeBCollapse12CompletedScaling.thin t := by
  exact Or.inl ht

/-- Any q23-base-thin triangle remains thin after the type-(B) completion. -/
theorem standardTypeBCollapse23Completed_of_base
    {t : (Δ[3] : SSet.{u}).obj (op ⦋2⦌)}
    (ht : standardTypeBCollapse23BaseScaling.thin t) :
    standardTypeBCollapse23CompletedScaling.thin t := by
  exact Or.inl ht

/-- Every 2-simplex of `Delta[3]` is thin after the q12 completion. -/
theorem standardTypeBCollapse12Completed_thin_all
    (t : (Δ[3] : SSet.{u}).obj (op ⦋2⦌)) :
    standardTypeBCollapse12CompletedScaling.thin t := by
  rcases standardTypeBThree_triangle_minimal_or_four_faces t with
      hmin | h012 | h013 | h023 | h123
  · exact standardTypeBCollapse12Completed_of_base
      (standardTypeBCollapse12Base_minimal_thin t hmin)
  · subst t
    exact standardTypeBCollapse12Completed_of_base
      standardTypeBCollapse12Base_triangle_012_thin
  · subst t
    exact standardTypeBCollapse12Completed_of_base
      standardTypeBCollapse12Base_triangle_013_thin
  · subst t
    exact standardTypeBCollapse12Completed_triangle_023_thin
  · subst t
    exact standardTypeBCollapse12Completed_of_base
      standardTypeBCollapse12Base_triangle_123_thin

/-- Every 2-simplex of `Delta[3]` is thin after the q23 completion. -/
theorem standardTypeBCollapse23Completed_thin_all
    (t : (Δ[3] : SSet.{u}).obj (op ⦋2⦌)) :
    standardTypeBCollapse23CompletedScaling.thin t := by
  rcases standardTypeBThree_triangle_minimal_or_four_faces t with
      hmin | h012 | h013 | h023 | h123
  · exact standardTypeBCollapse23Completed_of_base
      (standardTypeBCollapse23Base_minimal_thin t hmin)
  · subst t
    exact standardTypeBCollapse23Completed_of_base
      standardTypeBCollapse23Base_triangle_012_thin
  · subst t
    exact standardTypeBCollapse23Completed_triangle_013_thin
  · subst t
    exact standardTypeBCollapse23Completed_of_base
      standardTypeBCollapse23Base_triangle_023_thin
  · subst t
    exact standardTypeBCollapse23Completed_of_base
      standardTypeBCollapse23Base_triangle_123_thin

/-! ## Exact maximal-scaling identifications -/

/-- The q12 completion is literally the maximal scaling on `Delta[3]`. -/
theorem standardTypeBCollapse12CompletedScaling_eq_maximal :
    standardTypeBCollapse12CompletedScaling =
      ScaledSimplicialSet.maximal (Δ[3] : SSet.{u}) := by
  apply scaling_eq_of_le_antisymm
  · intro t _
    exact ScaledSimplicialSet.maximal_thin _ t
  · intro t _
    exact standardTypeBCollapse12Completed_thin_all t

/-- The q23 completion is literally the maximal scaling on `Delta[3]`. -/
theorem standardTypeBCollapse23CompletedScaling_eq_maximal :
    standardTypeBCollapse23CompletedScaling =
      ScaledSimplicialSet.maximal (Δ[3] : SSet.{u}) := by
  apply scaling_eq_of_le_antisymm
  · intro t _
    exact ScaledSimplicialSet.maximal_thin _ t
  · intro t _
    exact standardTypeBCollapse23Completed_thin_all t

/-- Consequently the two completion targets carry exactly the same scaling. -/
theorem standardTypeBCollapse12CompletedScaling_eq_collapse23 :
    standardTypeBCollapse12CompletedScaling =
      standardTypeBCollapse23CompletedScaling := by
  rw [standardTypeBCollapse12CompletedScaling_eq_maximal,
    standardTypeBCollapse23CompletedScaling_eq_maximal]

/-!
The fixed three-simplex type-(B) geometry is now exact:

```text
q12 base : minimal + 012 + 013 + 123
q12 completion adds 023
q12 completed = maximal Delta[3]

q23 base : minimal + 012 + 023 + 123
q23 completion adds 013
q23 completed = maximal Delta[3].
```

Combined with v1.67, every `n = 2`, attached-dimension-three boundary-prism
cell and either standard type-(B) completed target now have the same maximal
three-simplex scaling.  The next unit identifies the A-pushout *base* scaling
with q12 or q23 according to the cell index, proves the equal-dimensional
`n = 3` branch pure type-(A), and then records the staircase order
`q23 / q23 / q12` before assembling the scaled rank filtration.
-/

end

end KUOS.DependentOriginationStandardTypeBThreeSimplexMaximalCompletionV1_68
