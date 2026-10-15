import KUOS.DependentOriginationStandardTypeABoundaryPrismRelativeCellV1_61
import KUOS.DependentOriginationStandardTypeBThreeSimplexCompletionV1_57

namespace KUOS.DependentOriginationStandardTypeABoundaryPrismScaledCellsV1_62

open CategoryTheory
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledHornAttachmentLiftingV1_40
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeBThreeSimplexCompletionV1_57
open KUOS.DependentOriginationStandardTypeAEndpointPrismPairingV1_60
open KUOS.DependentOriginationStandardTypeABoundaryPrismRelativeCellV1_61

universe u

/-!
# Scaled cells of the standard type-(A) boundary prism v1.62

Version v1.61 solved the ordinary combinatorics of

```text
A_boundary = (Lambda_i^n x Delta[1]) union (Delta[n] x boundary Delta[1])
```

by a regular inner pairing and its natural-number relative-cell filtration.
Every ordinary basic cell was identified literally with the underlying map of
one standard type-(A) inner horn generator.

The remaining issue is entirely scaled.  This file isolates that issue without
changing the canonical KuuOS carrier.

For every relative cell we pull the cylinder scaling back along the cell map,
and then pull it back once more to the cell horn.  This gives the exact scaling
carried by that cell in the ambient standard type-(A) cylinder.

The key dimension observation is then formalized.  If the attached simplex has
dimension at least four, its inner horn already contains every 2-simplex, so
there is no triangle outside the horn on which an additional scaling condition
could appear.  Consequently every possible scaling-only frontier is forced
into dimensions two and three.

In dimension two there is a unique inner index.  In dimension three there are
exactly two inner indices.  Their missing faces are exactly

```text
index 1 : 023,
index 2 : 013,
```

which are precisely the two triangles supplied by the q12/q23 standard
type-(B) three-simplex completions of v1.57.  Thus the endpoint-prism frontier
has only type-(A) cells plus these two type-(B) completion directions; no
outer-horn/type-(C) index occurs.

This file deliberately stops one categorical step before the final cellular
certificate: the next unit identifies the scaled successor pushout at each
rank with these A/B generators and packages the transfinite composite as
`StandardABCTypeAEndpointLeibnizCellularCertificate`.
-/

/-! ## Exact pullback scalings carried by a relative cell -/

/-- The exact scaling on the simplex attached by a boundary-prism rank cell:
pull back the ambient type-(A) cylinder scaling along the Mathlib cell map. -/
def standardTypeABoundaryPrismCellScaling
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    ScaledSimplicialSet (Δ[c.dim + 1] : SSet.{u}) :=
  pullbackScaling
    (simplexCylinderScaling (standardTypeASimplexScaling g.i))
    c.map

/-- The corresponding horn scaling is the pullback of the exact cell scaling. -/
def standardTypeABoundaryPrismCellHornScaling
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    ScaledSimplicialSet (c.horn : SSet.{u}) :=
  pullbackScaling (standardTypeABoundaryPrismCellScaling g j c) c.horn.ι

/-- The scaled source object of one relative cell. -/
def standardTypeABoundaryPrismScaledCellSource
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) : ScaledSSet.{u} :=
  ScaledSSet.of (c.horn : SSet.{u})
    (standardTypeABoundaryPrismCellHornScaling g j c)

/-- The scaled target object of one relative cell. -/
def standardTypeABoundaryPrismScaledCellTarget
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) : ScaledSSet.{u} :=
  ScaledSSet.of (Δ[c.dim + 1] : SSet.{u})
    (standardTypeABoundaryPrismCellScaling g j c)

/-- The ordinary basic horn cell with its exact ambient pullback scalings. -/
def standardTypeABoundaryPrismScaledCellHom
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    standardTypeABoundaryPrismScaledCellSource g j c ⟶
      standardTypeABoundaryPrismScaledCellTarget g j c where
  map := c.horn.ι
  scaled := pullbackScaling_map _ _

/-- Forgetting scaling recovers exactly the v1.61 basic cell. -/
theorem standardTypeABoundaryPrismScaledCellHom_map
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    (standardTypeABoundaryPrismScaledCellHom g j c).map =
      (standardTypeABoundaryPrismRankFunction g).basicCell j c := by
  rfl

/-- The attached scaled simplex maps canonically back into the ambient
standard type-(A) cylinder. -/
def standardTypeABoundaryPrismScaledCellToCylinder
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    standardTypeABoundaryPrismScaledCellTarget g j c ⟶
      scaledSimplexCylinder (standardTypeASimplexScaling g.i) where
  map := c.map
  scaled := pullbackScaling_map _ _

/-! ## Innerness forces attached dimension at least two -/

/-- Every attached cell has simplex dimension at least two.  This is the
numerical content of the fact that its horn index is genuinely inner. -/
theorem standardTypeABoundaryPrism_cell_target_dim_ge_two
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    2 ≤ c.dim + 1 := by
  have h0 := standardTypeABoundaryPrism_cell_index_pos g j c
  have hlast := standardTypeABoundaryPrism_cell_index_lt_last g j c
  change 0 < c.index.val at h0
  change c.index.val < c.dim + 1 at hlast
  omega

/-- Repackage the v1.61 inner-index result as a direct exclusion of all
outer-horn/type-(C) indices. -/
theorem standardTypeABoundaryPrism_cell_no_outer_index
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    c.index ≠ 0 ∧ c.index ≠ Fin.last (c.dim + 1) :=
  ⟨standardTypeABoundaryPrism_cell_index_ne_zero g j c,
    standardTypeABoundaryPrism_cell_index_ne_last g j c⟩

/-! ## In dimension at least four the horn already contains every triangle -/

/-- Once the attached simplex has dimension at least four, its inner horn is
already all of the simplex in degree two. -/
theorem standardTypeABoundaryPrism_cell_horn_obj_two_eq_univ_of_four_le
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h4 : 4 ≤ c.dim + 1) :
    c.horn.obj (op ⦋2⦌) = Set.univ := by
  change
    (SSet.horn (c.dim + 1) c.index).obj (op ⦋2⦌) = Set.univ
  exact SSet.horn_obj_eq_univ c.index 2 (by omega)

/-- Hence every 2-simplex of a cell of dimension at least four is already in
the horn source. -/
theorem standardTypeABoundaryPrism_cell_triangle_mem_horn_of_four_le
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h4 : 4 ≤ c.dim + 1)
    (t : (Δ[c.dim + 1] : SSet.{u}).obj (op ⦋2⦌)) :
    t ∈ c.horn.obj (op ⦋2⦌) := by
  rw [standardTypeABoundaryPrism_cell_horn_obj_two_eq_univ_of_four_le
    g j c h4]
  exact Set.mem_univ t

/-- A triangle outside the cell horn can therefore occur only when the attached
simplex has dimension at most three. -/
theorem standardTypeABoundaryPrism_cell_target_dim_le_three_of_triangle_notMem_horn
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    {t : (Δ[c.dim + 1] : SSet.{u}).obj (op ⦋2⦌)}
    (ht : t ∉ c.horn.obj (op ⦋2⦌)) :
    c.dim + 1 ≤ 3 := by
  by_contra! h
  have h4 : 4 ≤ c.dim + 1 := by omega
  exact ht
    (standardTypeABoundaryPrism_cell_triangle_mem_horn_of_four_le
      g j c h4 t)

/-- Combining innerness with the preceding upper bound leaves exactly dimensions
two and three for any triangle outside the horn. -/
theorem standardTypeABoundaryPrism_cell_target_dim_eq_two_or_three_of_triangle_notMem_horn
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    {t : (Δ[c.dim + 1] : SSet.{u}).obj (op ⦋2⦌)}
    (ht : t ∉ c.horn.obj (op ⦋2⦌)) :
    c.dim + 1 = 2 ∨ c.dim + 1 = 3 := by
  have hlo := standardTypeABoundaryPrism_cell_target_dim_ge_two g j c
  have hhi :=
    standardTypeABoundaryPrism_cell_target_dim_le_three_of_triangle_notMem_horn
      g j c ht
  omega

/-! ## Low-dimensional inner indices -/

/-- In an attached 2-simplex the only possible inner horn index is `1`. -/
theorem standardTypeABoundaryPrism_cell_index_val_eq_one_of_target_dim_two
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h2 : c.dim + 1 = 2) :
    c.index.val = 1 := by
  have h0 := standardTypeABoundaryPrism_cell_index_pos g j c
  have hlast := standardTypeABoundaryPrism_cell_index_lt_last g j c
  change 0 < c.index.val at h0
  change c.index.val < c.dim + 1 at hlast
  omega

/-- In an attached 3-simplex the inner horn index is exactly `1` or `2`. -/
theorem standardTypeABoundaryPrism_cell_index_val_eq_one_or_two_of_target_dim_three
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h3 : c.dim + 1 = 3) :
    c.index.val = 1 ∨ c.index.val = 2 := by
  have h0 := standardTypeABoundaryPrism_cell_index_pos g j c
  have hlast := standardTypeABoundaryPrism_cell_index_lt_last g j c
  change 0 < c.index.val at h0
  change c.index.val < c.dim + 1 at hlast
  omega

/-- Cast a 3-dimensional cell index to the fixed carrier `Fin 4`. -/
noncomputable def standardTypeABoundaryPrismCellIndex3
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h3 : c.dim + 1 = 3) : Fin 4 :=
  Fin.cast (by omega) c.index

/-- The fixed `Fin 4` form of a 3-dimensional cell index is `1` or `2`. -/
theorem standardTypeABoundaryPrismCellIndex3_eq_one_or_two
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h3 : c.dim + 1 = 3) :
    standardTypeABoundaryPrismCellIndex3 g j c h3 = (1 : Fin 4) ∨
      standardTypeABoundaryPrismCellIndex3 g j c h3 = (2 : Fin 4) := by
  rcases
      standardTypeABoundaryPrism_cell_index_val_eq_one_or_two_of_target_dim_three
        g j c h3 with h | h
  · left
    apply Fin.ext
    simpa [standardTypeABoundaryPrismCellIndex3] using h
  · right
    apply Fin.ext
    simpa [standardTypeABoundaryPrismCellIndex3] using h

/-! ## The two 3-simplex missing faces are exactly the type-(B) frontier -/

/-- The unique face missing from a 3-dimensional relative-cell horn, transported
to the fixed standard `Delta[3]`. -/
noncomputable def standardTypeABoundaryPrismCellMissingFace3
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h3 : c.dim + 1 = 3) :
    (Δ[3] : SSet.{u}).obj (op ⦋2⦌) :=
  SSet.stdSimplex.objEquiv.symm
    (SimplexCategory.δ
      (standardTypeABoundaryPrismCellIndex3 g j c h3))

/-- Missing index `1` means the missing 2-face is exactly `023`, the triangle
forced by the q12 type-(B) completion. -/
theorem standardTypeABoundaryPrismCellMissingFace3_eq_023_of_index_one
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h3 : c.dim + 1 = 3)
    (hidx : standardTypeABoundaryPrismCellIndex3 g j c h3 = (1 : Fin 4)) :
    standardTypeABoundaryPrismCellMissingFace3 g j c h3 =
      standardTypeBThreeTriangle023 := by
  unfold standardTypeABoundaryPrismCellMissingFace3
  rw [hidx]
  apply SSet.stdSimplex.ext
  intro k
  fin_cases k <;> rfl

/-- Missing index `2` means the missing 2-face is exactly `013`, the triangle
forced by the q23 type-(B) completion. -/
theorem standardTypeABoundaryPrismCellMissingFace3_eq_013_of_index_two
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h3 : c.dim + 1 = 3)
    (hidx : standardTypeABoundaryPrismCellIndex3 g j c h3 = (2 : Fin 4)) :
    standardTypeABoundaryPrismCellMissingFace3 g j c h3 =
      standardTypeBThreeTriangle013 := by
  unfold standardTypeABoundaryPrismCellMissingFace3
  rw [hidx]
  apply SSet.stdSimplex.ext
  intro k
  fin_cases k <;> rfl

/-- Exhaustive geometric classification of the 3-simplex missing face. -/
theorem standardTypeABoundaryPrismCellMissingFace3_eq_typeB_frontier
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h3 : c.dim + 1 = 3) :
    standardTypeABoundaryPrismCellMissingFace3 g j c h3 =
        standardTypeBThreeTriangle023 ∨
      standardTypeABoundaryPrismCellMissingFace3 g j c h3 =
        standardTypeBThreeTriangle013 := by
  rcases standardTypeABoundaryPrismCellIndex3_eq_one_or_two g j c h3 with h | h
  · exact Or.inl
      (standardTypeABoundaryPrismCellMissingFace3_eq_023_of_index_one
        g j c h3 h)
  · exact Or.inr
      (standardTypeABoundaryPrismCellMissingFace3_eq_013_of_index_two
        g j c h3 h)

/-- Whichever 3-simplex inner index occurs, its unique missing face is made thin
by one of the two existing standard type-(B) completion pushouts. -/
theorem standardTypeABoundaryPrismCellMissingFace3_typeB_completed_thin
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h3 : c.dim + 1 = 3) :
    standardTypeBCollapse12CompletedScaling.thin
        (standardTypeABoundaryPrismCellMissingFace3 g j c h3) ∨
      standardTypeBCollapse23CompletedScaling.thin
        (standardTypeABoundaryPrismCellMissingFace3 g j c h3) := by
  rcases
      standardTypeABoundaryPrismCellMissingFace3_eq_typeB_frontier
        g j c h3 with h | h
  · left
    rw [h]
    exact standardTypeBCollapse12Completed_triangle_023_thin
  · right
    rw [h]
    exact standardTypeBCollapse23Completed_triangle_013_thin

/-! ## Exhaustive scaled frontier -/

/-- Every boundary-prism cell lies in exactly the dimensional regimes relevant
to the standard A/B proof: high-dimensional cells have no triangle outside the
horn; dimension two has the unique inner type-(A) index; dimension three has
one of the two q12/q23 type-(B) frontier indices.  In all cases the index is
inner, so no type-(C) outer-horn cell is required by this prism filtration. -/
theorem standardTypeABoundaryPrism_cell_scaled_frontier
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    4 ≤ c.dim + 1 ∨
      c.dim + 1 = 2 ∨
        ∃ h3 : c.dim + 1 = 3,
          standardTypeABoundaryPrismCellIndex3 g j c h3 = (1 : Fin 4) ∨
            standardTypeABoundaryPrismCellIndex3 g j c h3 = (2 : Fin 4) := by
  by_cases h4 : 4 ≤ c.dim + 1
  · exact Or.inl h4
  · have hlo := standardTypeABoundaryPrism_cell_target_dim_ge_two g j c
    have hhi : c.dim + 1 ≤ 3 := by omega
    have hcases : c.dim + 1 = 2 ∨ c.dim + 1 = 3 := by omega
    rcases hcases with h2 | h3
    · exact Or.inr (Or.inl h2)
    · exact Or.inr (Or.inr
        ⟨h3, standardTypeABoundaryPrismCellIndex3_eq_one_or_two g j c h3⟩)

/-!
The scaled frontier is therefore finite and explicit:

```text
ordinary v1.61 inner horn cells
  + exact ambient pullback scaling
  -> dimension >= 4 : every triangle already lies in the horn
  -> dimension = 2  : unique inner type-(A) index 1
  -> dimension = 3  : index 1 / index 2
                       missing 023 / missing 013
                       q12 type-B / q23 type-B completion
  -> no outer index, hence no type-(C) cell in this prism.
```

The next categorical unit lifts this classification from individual cells to
the rank-successor pushout squares, composes the scaled rank filtration, adds
the opposite-endpoint type-(A) factor from v1.60, and exits through the v1.59
`StandardABCTypeAEndpointLeibnizCellularCertificate`.
-/

end KUOS.DependentOriginationStandardTypeABoundaryPrismScaledCellsV1_62
