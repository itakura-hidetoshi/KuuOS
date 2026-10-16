import KUOS.DependentOriginationStandardTypeABoundaryPrismScaledCellsV1_62
import Mathlib.AlgebraicTopology.SimplicialSet.AnodyneExtensions.PairingCore

namespace KUOS.DependentOriginationStandardTypeABoundaryPrismDimensionDichotomyV1_63

open CategoryTheory
open Opposite
open Simplicial
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAEndpointPrismPairingV1_60
open KUOS.DependentOriginationStandardTypeABoundaryPrismRelativeCellV1_61
open KUOS.DependentOriginationStandardTypeABoundaryPrismScaledCellsV1_62

universe u

/-!
# Dimension dichotomy for standard type-(A) boundary-prism cells v1.63

Version v1.62 isolated the scaled frontier of each cell in the Mathlib
`unionProd` relative-cell filtration.  To turn that local frontier into a
uniform cellular argument, one needs one further structural fact about the
actual paired simplices: an attached simplex can have only the original
simplex dimension or one dimension more.

For a type-(I) simplex in the pinned Mathlib `unionProd` pairing, the first
coordinate visits every vertex of the left standard simplex.  All vertices
except the omitted horn vertex are supplied by `pairingCore.mem_range_left`,
and the omitted vertex itself occurs at the distinguished pairing index.  Thus
the first coordinate is surjective.  Finite cardinality gives the lower bound
on the attached dimension.  The standard product-dimension theorem gives the
opposite upper bound:

```text
n <= attached dimension <= n + 1.
```

Hence every boundary-prism cell lies in exactly one of the two numerical
regimes

```text
attached dimension = n
attached dimension = n + 1.
```

This has two immediate consequences for the v1.62 scaled frontier.

* If the original type-(A) generator has dimension at least four, every cell
  is already in the high-dimensional regime where every triangle lies in the
  horn source.
* Any 2- or 3-dimensional cell can occur only for original generator dimension
  two or three.  Thus the q12/q23 type-(B) exceptional directions are genuinely
  low-dimensional and cannot propagate to higher dimensions.

The next unit uses the surjective first-coordinate map itself.  In the equal
case it is an endomorphism of a finite ordinal and hence the identity; in the
top-dimensional case Mathlib `SimplexCategory.eq_σ_of_epi` identifies it with
one degeneracy `σ_r`.  That is the staircase normal form needed before lifting
the cellwise A/B classification to scaled rank-successor pushouts.
-/

/-! ## The pinned union-product type-(I) simplex visits every left vertex -/

/-- For the non-last `unionProd` pairing core, the first coordinate of every
type-(I) simplex is surjective onto the left simplex vertices.

All vertices distinct from the omitted horn vertex come from Mathlib's
`mem_range_left`; the omitted vertex itself is exactly the left coordinate at
the distinguished pairing index. -/
theorem unionProdPairingCore_typeOne_fst_surjective
    {m : ℕ}
    (k : Fin (m + 1))
    (s : SSet.prodStdSimplex.pairingCore.Type₁.{u} k 1) :
    Function.Surjective (s.x.cast s.hd).simplex.1 := by
  intro a
  by_cases ha : a = k.castSucc
  · subst a
    exact ⟨s.index.castSucc, s.isIndex.simplex_fst_castSucc⟩
  · exact SSet.prodStdSimplex.pairingCore.mem_range_left
      s.x s.hd a ha

/-- Consequently a type-(II) simplex in the same pairing core has dimension
large enough that its paired type-(I) simplex has at least the left simplex
dimension. -/
theorem unionProdPairingCore_typeTwo_target_dim_ge_left
    {m : ℕ}
    (k : Fin (m + 1))
    (z : (SSet.prodStdSimplex.pairingCore.{u} k 1).pairing.II) :
    m + 1 ≤ z.val.dim + 1 := by
  obtain ⟨s, rfl⟩ :=
    (SSet.prodStdSimplex.pairingCore.{u} k 1).equivII.surjective z
  change m + 1 ≤ s.d + 1
  have hcard := Fintype.card_le_of_surjective _
    (unionProdPairingCore_typeOne_fst_surjective k s)
  simp only [Fintype.card_fin] at hcard
  omega

/-- The same lower bound for Mathlib's public `pairing k.castSucc 1` rather
than its implementation-level pairing core. -/
theorem unionProdPairing_typeTwo_target_dim_ge_left
    {m : ℕ}
    (k : Fin (m + 1))
    (z : (SSet.prodStdSimplex.pairing.{u} k.castSucc 1).II) :
    m + 1 ≤ z.val.dim + 1 := by
  have z' :
      (SSet.prodStdSimplex.pairingCore.{u} k 1).pairing.II := by
    simpa only [SSet.prodStdSimplex.pairing_castSucc] using z
  have h := unionProdPairingCore_typeTwo_target_dim_ge_left k z'
  simpa only [SSet.prodStdSimplex.pairing_castSucc] using h

/-! ## Lower and upper dimension bounds for every KuuOS boundary-prism cell -/

/-- Every standard type-(A) generator has simplex dimension at least two,
because its distinguished horn index is strictly between the two endpoints. -/
theorem standardTypeAHornAttachmentGenerator_dim_ge_two
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    2 ≤ g.n := by
  have h0 := g.inner_left
  have hn := g.inner_right
  change 0 < g.i.val at h0
  change g.i.val < g.n at hn
  omega

/-- The paired type-(I) simplex visits every original simplex vertex, so an
attached boundary-prism cell has dimension at least `g.n`. -/
theorem standardTypeABoundaryPrism_cell_target_dim_ge_generator_dim
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    g.n ≤ c.dim + 1 := by
  rcases g with ⟨n, i, h0, hn, endpoint⟩
  cases n with
  | zero =>
      have hi : i = 0 := Subsingleton.elim _ _
      subst i
      simp at h0
  | succ m =>
      have hilast : i ≠ Fin.last (m + 1) := ne_of_lt hn
      obtain ⟨k, rfl⟩ := Fin.eq_castSucc_of_ne_last hilast
      change m + 1 ≤ c.s.val.dim + 1
      exact unionProdPairing_typeTwo_target_dim_ge_left k c.s

/-- The paired type-(I) simplex is nondegenerate in
`Delta[g.n] x Delta[1]`, whose dimension is at most `g.n + 1`.  This gives the
matching upper bound on every attached cell. -/
theorem standardTypeABoundaryPrism_cell_target_dim_le_generator_succ
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    c.dim + 1 ≤ g.n + 1 := by
  let P := standardTypeABoundaryPrismPairing g
  let x :=
    (P.p c.s).val.cast (P.isUniquelyCodimOneFace c.s).dim_eq
  let z :
      ((Δ[g.n] : SSet.{u}) ⊗ Δ[1]).nonDegenerate (c.dim + 1) :=
    ⟨x.simplex, x.nonDegenerate⟩
  simpa [z] using
    (SSet.dim_le_of_nonDegenerate z (g.n + 1))

/-- Exact dimension dichotomy: every attached simplex is either of the same
dimension as the original type-(A) simplex, or one dimension higher. -/
theorem standardTypeABoundaryPrism_cell_target_dim_eq_generator_or_succ
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    c.dim + 1 = g.n ∨ c.dim + 1 = g.n + 1 := by
  have hlo :=
    standardTypeABoundaryPrism_cell_target_dim_ge_generator_dim g j c
  have hhi :=
    standardTypeABoundaryPrism_cell_target_dim_le_generator_succ g j c
  omega

/-! ## Consequences for the scaled A/B frontier -/

/-- If the original type-(A) simplex has dimension at least four, every
attached cell also has dimension at least four.  Therefore v1.62 implies that
every 2-simplex of every attached cell already lies in its horn source. -/
theorem standardTypeABoundaryPrism_cell_triangle_mem_horn_of_generator_four_le
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h4 : 4 ≤ g.n)
    (t : (Δ[c.dim + 1] : SSet.{u}).obj (op ⦋2⦌)) :
    t ∈ c.horn.obj (op ⦋2⦌) := by
  have h4c : 4 ≤ c.dim + 1 :=
    h4.trans
      (standardTypeABoundaryPrism_cell_target_dim_ge_generator_dim g j c)
  exact standardTypeABoundaryPrism_cell_triangle_mem_horn_of_four_le
    g j c h4c t

/-- A 2-dimensional attached cell forces the original generator itself to have
dimension two. -/
theorem standardTypeABoundaryPrism_generator_dim_eq_two_of_cell_target_dim_two
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h2 : c.dim + 1 = 2) :
    g.n = 2 := by
  have hlo := standardTypeAHornAttachmentGenerator_dim_ge_two g
  have hcell :=
    standardTypeABoundaryPrism_cell_target_dim_ge_generator_dim g j c
  omega

/-- A 3-dimensional attached cell can arise only from an original generator of
dimension two or three. -/
theorem standardTypeABoundaryPrism_generator_dim_eq_two_or_three_of_cell_target_dim_three
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h3 : c.dim + 1 = 3) :
    g.n = 2 ∨ g.n = 3 := by
  have hlo := standardTypeAHornAttachmentGenerator_dim_ge_two g
  have hcell :=
    standardTypeABoundaryPrism_cell_target_dim_ge_generator_dim g j c
  omega

/-- Refined finite frontier combining the new global dimension dichotomy with
the v1.62 low-dimensional classification. -/
theorem standardTypeABoundaryPrism_cell_scaled_frontier_refined
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    (c.dim + 1 = g.n ∨ c.dim + 1 = g.n + 1) ∧
      (4 ≤ g.n →
        ∀ t : (Δ[c.dim + 1] : SSet.{u}).obj (op ⦋2⦌),
          t ∈ c.horn.obj (op ⦋2⦌)) ∧
      (c.dim + 1 = 2 → g.n = 2) ∧
      (c.dim + 1 = 3 → g.n = 2 ∨ g.n = 3) := by
  refine ⟨standardTypeABoundaryPrism_cell_target_dim_eq_generator_or_succ g j c,
    ?_, ?_, ?_⟩
  · intro h4 t
    exact standardTypeABoundaryPrism_cell_triangle_mem_horn_of_generator_four_le
      g j c h4 t
  · exact standardTypeABoundaryPrism_generator_dim_eq_two_of_cell_target_dim_two
      g j c
  · exact
      standardTypeABoundaryPrism_generator_dim_eq_two_or_three_of_cell_target_dim_three
        g j c

/-!
The numerical shape of the boundary-prism pairing is now rigid:

```text
original generator dimension n >= 2
                 |
                 v
paired type-(I) first coordinate is surjective
                 |
                 v
      n <= attached dimension <= n + 1
                 |
                 v
       attached dimension = n or n+1

n >= 4  -> every attached triangle is already in the horn
N = 2   -> n = 2
N = 3   -> n = 2 or n = 3.
```

Thus the exceptional q12/q23 type-(B) directions isolated in v1.62 are now
proved to be genuinely low-dimensional phenomena.  The next unit keeps the
surjective first-coordinate map rather than only its cardinality: equal
dimension gives the identity ordinal map, and top dimension gives one
Mathlib degeneracy `σ_r`.  That staircase normal form is the final geometric
input needed to classify the exact scaled successor-cell morphisms before the
relative-cell transfinite-composition certificate is assembled.
-/

end KUOS.DependentOriginationStandardTypeABoundaryPrismDimensionDichotomyV1_63
