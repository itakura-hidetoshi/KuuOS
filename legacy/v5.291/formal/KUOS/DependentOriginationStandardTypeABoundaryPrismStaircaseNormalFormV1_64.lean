import KUOS.DependentOriginationStandardTypeABoundaryPrismDimensionDichotomyV1_63
import Mathlib.AlgebraicTopology.SimplicialSet.ProdStdSimplexOne

namespace KUOS.DependentOriginationStandardTypeABoundaryPrismStaircaseNormalFormV1_64

open CategoryTheory
open MonoidalCategory
open Opposite
open Simplicial
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeABoundaryPrismRelativeCellV1_61
open KUOS.DependentOriginationStandardTypeABoundaryPrismScaledCellsV1_62
open KUOS.DependentOriginationStandardTypeABoundaryPrismDimensionDichotomyV1_63

universe u

noncomputable section

/-!
# Staircase normal form for standard type-(A) boundary-prism cells v1.64

Version v1.63 proved the numerical dichotomy

```text
attached dimension = n  or  attached dimension = n + 1
```

for every cell in the regular `unionProd` filtration of the boundary prism.
This file rigidifies the second branch completely.  The paired type-(I)
simplex is a nondegenerate simplex of `Delta[n] x Delta[1]`.  In top dimension
`n+1`, pinned Mathlib provides the canonical equivalence

```text
Fin (n+1) ~= nondegenerate (n+1)-simplices of Delta[n] x Delta[1].
```

Thus every top cell has a unique staircase index `r`.  Its two coordinates are
literally

```text
first  coordinate = sigma_r : [n+1] -> [n]
second coordinate = the interval switch at r.
```

Combining this exact normal form with v1.63 also isolates the low-dimensional
frontier:

* a 2-dimensional cell necessarily comes from `n = 2` and is in the equal
  dimension branch;
* a 3-dimensional cell either comes from `n = 3` in the equal branch, or from
  `n = 2` in the top staircase branch.

Consequently the q12/q23 type-(B) frontier of v1.62 can only occur in the
`n = 2` top-staircase branch.  No type-(C) geometry is introduced here.
-/

/-! ## The paired nondegenerate simplex carried by a rank cell -/

/-- The type-(I) simplex paired with a rank cell, cast to the cell's attached
simplex dimension.  This is the same nondegenerate simplex used implicitly in
the v1.63 upper-dimension bound, now exposed as a reusable object. -/
def standardTypeABoundaryPrismCellPairedNondegenerate
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    ((Δ[g.n] : SSet.{u}) ⊗ Δ[1]).nonDegenerate (c.dim + 1) := by
  let P := standardTypeABoundaryPrismPairing g
  let x :=
    (P.p c.s).val.cast (P.isUniquelyCodimOneFace c.s).dim_eq
  exact ⟨x.simplex, x.nonDegenerate⟩

/-- Transport the paired simplex into the fixed top dimension `g.n + 1`. -/
def standardTypeABoundaryPrismCellPairedTop
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (htop : c.dim + 1 = g.n + 1) :
    ((Δ[g.n] : SSet.{u}) ⊗ Δ[1]).nonDegenerate (g.n + 1) :=
  Eq.mp
    (congrArg
      (fun d : ℕ => ((Δ[g.n] : SSet.{u}) ⊗ Δ[1]).nonDegenerate d)
      htop)
    (standardTypeABoundaryPrismCellPairedNondegenerate g j c)

/-! ## Every top cell is exactly one pinned Mathlib staircase -/

/-- A top-dimensional paired simplex is exactly one member of Mathlib's
canonical staircase enumeration. -/
theorem standardTypeABoundaryPrism_cell_top_exists_staircase
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (htop : c.dim + 1 = g.n + 1) :
    ∃ r : Fin (g.n + 1),
      SSet.prodStdSimplex.nonDegenerateEquiv₁ r =
        standardTypeABoundaryPrismCellPairedTop g j c htop := by
  exact
    (SSet.prodStdSimplex.nonDegenerateEquiv₁
      (p := g.n)).surjective
      (standardTypeABoundaryPrismCellPairedTop g j c htop)

/-- In top dimension the first coordinate is literally the unique degeneracy
`σ_r` associated with the staircase index. -/
theorem standardTypeABoundaryPrism_cell_top_fst_eq_sigma
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (htop : c.dim + 1 = g.n + 1) :
    ∃ r : Fin (g.n + 1),
      (standardTypeABoundaryPrismCellPairedTop g j c htop).1.1 =
        (SSet.stdSimplex.objEquiv (m := op ⦋g.n + 1⦌)).symm
          (SimplexCategory.σ r) := by
  obtain ⟨r, hr⟩ :=
    standardTypeABoundaryPrism_cell_top_exists_staircase g j c htop
  refine ⟨r, ?_⟩
  rw [← hr]
  exact SSet.prodStdSimplex.nonDegenerateEquiv₁_fst r

/-- In top dimension the second coordinate is literally the canonical interval
switch belonging to the same staircase index `r`. -/
theorem standardTypeABoundaryPrism_cell_top_snd_eq_intervalSwitch
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (htop : c.dim + 1 = g.n + 1) :
    ∃ r : Fin (g.n + 1),
      (standardTypeABoundaryPrismCellPairedTop g j c htop).1.2 =
        SSet.stdSimplex.objMk₁ r.succ.castSucc := by
  obtain ⟨r, hr⟩ :=
    standardTypeABoundaryPrism_cell_top_exists_staircase g j c htop
  refine ⟨r, ?_⟩
  rw [← hr]
  exact SSet.prodStdSimplex.nonDegenerateEquiv₁_snd r

/-- Package both coordinate normal forms with one common staircase index. -/
theorem standardTypeABoundaryPrism_cell_top_coordinate_normalForm
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (htop : c.dim + 1 = g.n + 1) :
    ∃ r : Fin (g.n + 1),
      (standardTypeABoundaryPrismCellPairedTop g j c htop).1.1 =
          (SSet.stdSimplex.objEquiv (m := op ⦋g.n + 1⦌)).symm
            (SimplexCategory.σ r) ∧
        (standardTypeABoundaryPrismCellPairedTop g j c htop).1.2 =
          SSet.stdSimplex.objMk₁ r.succ.castSucc := by
  obtain ⟨r, hr⟩ :=
    standardTypeABoundaryPrism_cell_top_exists_staircase g j c htop
  refine ⟨r, ?_, ?_⟩
  · rw [← hr]
    exact SSet.prodStdSimplex.nonDegenerateEquiv₁_fst r
  · rw [← hr]
    exact SSet.prodStdSimplex.nonDegenerateEquiv₁_snd r

/-! ## Refine the v1.63 dimension dichotomy by the exact top normal form -/

/-- Every rank cell is either equal-dimensional with the original simplex, or
is an explicitly enumerated top staircase. -/
theorem standardTypeABoundaryPrism_cell_equal_or_top_staircase
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    c.dim + 1 = g.n ∨
      ∃ htop : c.dim + 1 = g.n + 1,
        ∃ r : Fin (g.n + 1),
          SSet.prodStdSimplex.nonDegenerateEquiv₁ r =
            standardTypeABoundaryPrismCellPairedTop g j c htop := by
  rcases
      standardTypeABoundaryPrism_cell_target_dim_eq_generator_or_succ
        g j c with heq | htop
  · exact Or.inl heq
  · exact Or.inr
      ⟨htop, standardTypeABoundaryPrism_cell_top_exists_staircase g j c htop⟩

/-! ## The low-dimensional frontier is now localized exactly -/

/-- A 2-dimensional cell is necessarily an equal-dimensional cell for the
unique possible generator dimension `n = 2`. -/
theorem standardTypeABoundaryPrism_cell_dim_two_is_generator_two_equal
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h2 : c.dim + 1 = 2) :
    g.n = 2 ∧ c.dim + 1 = g.n := by
  have hn :=
    standardTypeABoundaryPrism_generator_dim_eq_two_of_cell_target_dim_two
      g j c h2
  exact ⟨hn, by omega⟩

/-- A 3-dimensional cell has exactly two origins: either an equal-dimensional
`n = 3` cell, or a top staircase over `n = 2`.  The latter is therefore the
only branch in which the v1.62 q12/q23 three-simplex completion frontier can
occur. -/
theorem standardTypeABoundaryPrism_cell_dim_three_origin_normalForm
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h3 : c.dim + 1 = 3) :
    (g.n = 3 ∧ c.dim + 1 = g.n) ∨
      ∃ hn2 : g.n = 2,
        ∃ htop : c.dim + 1 = g.n + 1,
          ∃ r : Fin (g.n + 1),
            SSet.prodStdSimplex.nonDegenerateEquiv₁ r =
              standardTypeABoundaryPrismCellPairedTop g j c htop := by
  rcases
      standardTypeABoundaryPrism_generator_dim_eq_two_or_three_of_cell_target_dim_three
        g j c h3 with hn2 | hn3
  · right
    have htop : c.dim + 1 = g.n + 1 := by omega
    exact ⟨hn2, htop,
      standardTypeABoundaryPrism_cell_top_exists_staircase g j c htop⟩
  · left
    exact ⟨hn3, by omega⟩

/-- If a 3-dimensional cell comes from `n = 2`, its paired simplex has the
full top-staircase coordinate normal form, with one common index controlling
both the simplex degeneracy and the interval switch. -/
theorem standardTypeABoundaryPrism_cell_dim_three_generator_two_coordinate_normalForm
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h3 : c.dim + 1 = 3)
    (hn2 : g.n = 2) :
    ∃ htop : c.dim + 1 = g.n + 1,
      ∃ r : Fin (g.n + 1),
        (standardTypeABoundaryPrismCellPairedTop g j c htop).1.1 =
            (SSet.stdSimplex.objEquiv (m := op ⦋g.n + 1⦌)).symm
              (SimplexCategory.σ r) ∧
          (standardTypeABoundaryPrismCellPairedTop g j c htop).1.2 =
            SSet.stdSimplex.objMk₁ r.succ.castSucc := by
  have htop : c.dim + 1 = g.n + 1 := by omega
  exact ⟨htop,
    standardTypeABoundaryPrism_cell_top_coordinate_normalForm g j c htop⟩

/-!
The cell geometry is now normalized before any scaled pushout bookkeeping:

```text
cell dimension N
  |
  +-- N = n      : equal-dimensional branch
  |
  +-- N = n + 1  : unique staircase r
                    fst = sigma_r
                    snd = interval switch at r

N = 2 : necessarily n = 2, equal branch
N = 3 : either n = 3, equal branch
        or n = 2, top staircase branch.
```

Hence the only possible genuinely three-dimensional scaling-completion branch
is `n = 2` top staircase.  The next categorical unit uses this normal form to
identify the equal branches with pure standard type-(A) cells and the `n = 2`
top branch with the existing q12/q23 type-(B) completion cells.  Those
cellwise memberships can then be fed into the relative-cell rank pushouts and
finally into the v1.59 endpoint Leibniz cellular certificate.
-/

end

end KUOS.DependentOriginationStandardTypeABoundaryPrismStaircaseNormalFormV1_64
