import KUOS.DependentOriginationStandardTypeABoundaryPrismCellACompatibilityV1_66

namespace KUOS.DependentOriginationStandardTypeABoundaryPrismN2MaximalFrontierV1_67

open CategoryTheory
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAScaledPushoutSourceEnrichmentV1_53
open KUOS.DependentOriginationStandardTypeBThreeSimplexCompletionV1_57
open KUOS.DependentOriginationStandardTypeABoundaryPrismRelativeCellV1_61
open KUOS.DependentOriginationStandardTypeABoundaryPrismScaledCellsV1_62
open KUOS.DependentOriginationStandardTypeABoundaryPrismDimensionDichotomyV1_63
open KUOS.DependentOriginationStandardTypeABoundaryPrismStaircaseNormalFormV1_64
open KUOS.DependentOriginationStandardTypeABoundaryPrismCellPushoutCriterionV1_65
open KUOS.DependentOriginationStandardTypeABoundaryPrismCellACompatibilityV1_66

universe u

noncomputable section

/-!
# The `n = 2` maximal-scaling frontier for boundary-prism cells v1.67

Version v1.66 proved type-(A) compatibility for every cell and reduced every
possible post-A scaling residual to attached dimension two or three.  This file
removes the two-dimensional branch completely and isolates the remaining
three-dimensional type-(B) problem.

The key elementary observation is that the standard type-(A) scaling on
`Delta[2]` at its unique inner index `1` is already maximal.  Indeed every
2-simplex of `Delta[2]` either has a repeated adjacent vertex and is minimally
thin, or is the unique strictly increasing triangle `012`, which is precisely
the distinguished type-(A) triangle.

Consequently:

* every original type-(A) generator with `n = 2` has maximal simplex scaling;
* every exact boundary-prism cell over such a generator has maximal pullback
  scaling, in every attached dimension;
* every attached 2-cell is a pure type-(A) cobase change, because its own
  standard type-(A) scaling is maximal as well;
* therefore the global post-A frontier shrinks from `N = 2 or 3` to `N = 3`;
* in the remaining `n = 2`, `N = 3` branch the actual cell target is maximal,
  while v1.62 already identifies the unique missing horn face with `023` or
  `013` and the corresponding q12/q23 type-(B) completion makes it thin.

The next unit identifies the A-pushout scaling itself with the exact q12/q23
base scaling, and the maximal actual target with the corresponding completed
scaling.  That will give the literal `A ; B` cell factorization needed for the
scaled rank filtration.
-/

/-! ## Minimal thinness from the second adjacent repetition -/

/-- A standard-simplex 2-simplex whose last two vertices agree is the
`σ 1`-degeneracy of its last face, hence is minimally thin. -/
theorem minimalScaling_stdSimplex_thin_of_one_eq_two
    {n : ℕ}
    (t : (Δ[n] : SSet.{u}).obj (op ⦋2⦌))
    (h12 : t 1 = t 2) :
    (minimalScaling (Δ[n] : SSet.{u})).thin t := by
  refine Or.inr ⟨(Δ[n] : SSet.{u}).δ (2 : Fin 3) t, ?_⟩
  apply SSet.stdSimplex.ext
  intro a
  fin_cases a
  · rfl
  ·
    simp only [SSet.stdSimplex.σ_apply, SSet.stdSimplex.δ_apply]
    simpa [Fin.succAbove, Fin.predAbove] using h12
  ·
    simp only [SSet.stdSimplex.σ_apply, SSet.stdSimplex.δ_apply]
    simpa [Fin.succAbove, Fin.predAbove] using h12

/-! ## The unique inner type-(A) scaling on `Delta[2]` is maximal -/

/-- In simplex dimension two, an inner index necessarily has value one and its
standard type-(A) scaling is maximal.  The statement is written with an
arbitrary natural `n` plus the equality `n = 2`, so it can be reused directly
for dependent cell dimensions. -/
theorem standardTypeASimplexScaling_eq_maximal_of_dim_two
    {n : ℕ}
    (i : Fin (n + 1))
    (hn : n = 2)
    (hi : i.val = 1) :
    standardTypeASimplexScaling i =
      ScaledSimplicialSet.maximal (Δ[n] : SSet.{u}) := by
  subst n
  have hii : i = (1 : Fin 3) := by
    apply Fin.ext
    exact hi
  subst i
  apply scaling_eq_of_le_antisymm
  · intro t _
    exact ScaledSimplicialSet.maximal_thin _ t
  · intro t _
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
    have hv0 : (t 0).val = 0 := by omega
    have hv1 : (t 1).val = 1 := by omega
    have hv2 : (t 2).val = 2 := by omega
    exact Or.inr ⟨by
      apply Fin.ext
      exact hv1, by
      change (t 0).val + 1 = 1
      omega, by
      change 1 + 1 = (t 2).val
      omega⟩

/-- The distinguished index of every original type-(A) generator of dimension
two has value one. -/
theorem standardTypeAHornAttachmentGenerator_index_val_eq_one_of_dim_two
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (hn : g.n = 2) :
    g.i.val = 1 := by
  have h0 := g.inner_left
  have hlast := g.inner_right
  change 0 < g.i.val at h0
  change g.i.val < g.n at hlast
  omega

/-- Hence the original simplex scaling of an `n = 2` type-(A) generator is
maximal. -/
theorem standardTypeAHornAttachmentGenerator_scaling_eq_maximal_of_dim_two
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (hn : g.n = 2) :
    standardTypeASimplexScaling g.i =
      ScaledSimplicialSet.maximal (Δ[g.n] : SSet.{u}) :=
  standardTypeASimplexScaling_eq_maximal_of_dim_two
    g.i hn
    (standardTypeAHornAttachmentGenerator_index_val_eq_one_of_dim_two g hn)

/-! ## Every cell over an `n = 2` generator has maximal actual scaling -/

/-- Pulling the maximal `Delta[2]` scaling through the simplex-cylinder first
coordinate makes every exact rank-cell target maximally scaled. -/
theorem standardTypeABoundaryPrismCellScaling_eq_maximal_of_generator_dim_two
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (hn : g.n = 2) :
    standardTypeABoundaryPrismCellScaling g j c =
      ScaledSimplicialSet.maximal (Δ[c.dim + 1] : SSet.{u}) := by
  apply scaling_eq_of_le_antisymm
  · intro t _
    exact ScaledSimplicialSet.maximal_thin _ t
  · intro t _
    change
      (standardTypeASimplexScaling g.i).thin
        ((c.map.app (op ⦋2⦌) t).1)
    rw [standardTypeAHornAttachmentGenerator_scaling_eq_maximal_of_dim_two
      g hn]
    exact ScaledSimplicialSet.maximal_thin _ _

/-! ## Attached 2-cells have no post-A residual -/

/-- In attached dimension two the cell index is the unique inner index, so the
cell's own standard type-(A) target scaling is maximal.  Therefore the
outside-A condition of v1.65 is automatic. -/
theorem standardTypeABoundaryPrismCellOutsideACompatible_of_target_dim_two
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h2 : c.dim + 1 = 2) :
    standardTypeABoundaryPrismCellOutsideACompatible g j c := by
  have hidx :=
    standardTypeABoundaryPrism_cell_index_val_eq_one_of_target_dim_two
      g j c h2
  intro t _ _
  have hmax :
      standardTypeASimplexScaling c.index =
        ScaledSimplicialSet.maximal Δ[c.dim + 1] :=
    standardTypeASimplexScaling_eq_maximal_of_dim_two c.index h2 hidx
  rw [hmax]
  exact ScaledSimplicialSet.maximal_thin _ t

/-- Hence every attached 2-cell is exactly the pure type-(A) cobase change,
with no type-(B) scaling completion. -/
theorem standardTypeABoundaryPrismCellAPushoutScaling_eq_cellScaling_of_target_dim_two
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h2 : c.dim + 1 = 2) :
    standardTypeABoundaryPrismCellAPushoutScaling g j c =
      standardTypeABoundaryPrismCellScaling g j c :=
  standardTypeABoundaryPrismCellAPushoutScaling_eq_cellScaling
    g j c
    (standardTypeABoundaryPrismCellACompatible_all g j c)
    (standardTypeABoundaryPrismCellOutsideACompatible_of_target_dim_two
      g j c h2)

/-- Object-level version of the preceding exact equality. -/
theorem standardTypeABoundaryPrismCellAPushoutTarget_eq_cellTarget_of_target_dim_two
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h2 : c.dim + 1 = 2) :
    standardTypeABoundaryPrismCellAPushoutTarget g j c =
      standardTypeABoundaryPrismScaledCellTarget g j c :=
  standardTypeABoundaryPrismCellAPushoutTarget_eq_cellTarget
    g j c
    (standardTypeABoundaryPrismCellACompatible_all g j c)
    (standardTypeABoundaryPrismCellOutsideACompatible_of_target_dim_two
      g j c h2)

/-! ## The entire unresolved frontier is now dimension three -/

/-- Combining v1.66 high-dimensional purity with the new two-dimensional
result leaves only attached dimension three as a possible post-A residual. -/
theorem standardTypeABoundaryPrismCell_pureA_or_target_dim_three
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    standardTypeABoundaryPrismCellAPushoutScaling g j c =
        standardTypeABoundaryPrismCellScaling g j c ∨
      c.dim + 1 = 3 := by
  rcases standardTypeABoundaryPrismCell_pureA_or_lowDim g j c with
    hpure | h2 | h3
  · exact Or.inl hpure
  · exact Or.inl
      (standardTypeABoundaryPrismCellAPushoutScaling_eq_cellScaling_of_target_dim_two
        g j c h2)
  · exact Or.inr h3

/-! ## The remaining `n = 2`, `N = 3` target is maximal and type-(B)-shaped -/

/-- A three-dimensional cell over an original two-simplex has maximal actual
scaling.  This is the target scaling which the q12/q23 completion must recover. -/
theorem standardTypeABoundaryPrismCellScaling_eq_maximal_of_generator_two_target_three
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (hn2 : g.n = 2)
    (_h3 : c.dim + 1 = 3) :
    standardTypeABoundaryPrismCellScaling g j c =
      ScaledSimplicialSet.maximal (Δ[c.dim + 1] : SSet.{u}) :=
  standardTypeABoundaryPrismCellScaling_eq_maximal_of_generator_dim_two
    g j c hn2

/-- The remaining `n = 2`, `N = 3` branch has exactly the v1.62 type-(B)
missing-face frontier, and that face is thin after one of the two existing
q12/q23 completion pushouts. -/
theorem standardTypeABoundaryPrismCell_generator_two_target_three_typeB_frontier
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (hn2 : g.n = 2)
    (h3 : c.dim + 1 = 3) :
    standardTypeABoundaryPrismCellScaling g j c =
        ScaledSimplicialSet.maximal (Δ[c.dim + 1] : SSet.{u}) ∧
      (standardTypeABoundaryPrismCellMissingFace3 g j c h3 =
          standardTypeBThreeTriangle023 ∨
        standardTypeABoundaryPrismCellMissingFace3 g j c h3 =
          standardTypeBThreeTriangle013) ∧
      (standardTypeBCollapse12CompletedScaling.thin
          (standardTypeABoundaryPrismCellMissingFace3 g j c h3) ∨
        standardTypeBCollapse23CompletedScaling.thin
          (standardTypeABoundaryPrismCellMissingFace3 g j c h3)) := by
  refine ⟨
    standardTypeABoundaryPrismCellScaling_eq_maximal_of_generator_two_target_three
      g j c hn2 h3,
    standardTypeABoundaryPrismCellMissingFace3_eq_typeB_frontier
      g j c h3,
    standardTypeABoundaryPrismCellMissingFace3_typeB_completed_thin
      g j c h3⟩

/-!
The scaled cell frontier is now reduced to one finite three-simplex problem:

```text
N >= 4 : pure A                      (v1.66)
N = 2  : pure A                      (this file)
N = 3  : only remaining frontier

and if the original generator has n = 2:
  actual cell scaling = maximal Delta[3]
  missing face = 023 or 013
  q12 or q23 completion makes that face thin.
```

The next unit proves the stronger literal identifications

```text
cell index 1 : A-pushout scaling = q12 base scaling
               actual scaling   = q12 completed scaling
cell index 2 : A-pushout scaling = q23 base scaling
               actual scaling   = q23 completed scaling,
```

and relates the three staircase positions to `q23 / q23 / q12`.  That is the
last local input before assembling the scaled rank filtration and the v1.59
A/B/C cellular certificate.
-/

end

end KUOS.DependentOriginationStandardTypeABoundaryPrismN2MaximalFrontierV1_67