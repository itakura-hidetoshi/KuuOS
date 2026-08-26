import KUOS.DependentOriginationStandardTypeAEndpointPrismPairingV1_60
import Mathlib.AlgebraicTopology.SimplicialSet.AnodyneExtensions.UnionProd

namespace KUOS.DependentOriginationStandardTypeABoundaryPrismRelativeCellV1_61

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Limits
open HomotopicalAlgebra
open MonoidalCategory
open Opposite
open Simplicial
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationStandardTypeAEndpointPrismPairingV1_60

universe u

/-!
# Standard type-(A) boundary-prism relative-cell filtration v1.61

Version 1.60 factored the genuine endpoint Leibniz prism through

```text
A_boundary = (Lambda_i^n x Delta[1]) union (Delta[n] x boundary Delta[1]).
```

The ordinary inclusion `A_boundary -> Delta[n] x Delta[1]` is not a new
combinatorial problem.  At the pinned Mathlib revision it is exactly the
`unionProd` geometry handled by `SSet.prodStdSimplex.pairing`.  This file makes
that identification theorem-level and then consumes the complete pinned
pairing/rank/relative-cell-complex infrastructure in one pass:

* reuse the Mathlib pairing for the boundary prism;
* prove that the pairing is regular and inner from the type-(A) index bounds;
* take its canonical natural-number rank function;
* obtain the relative cell complex whose successor stages are pushouts of
  coproducts of horn inclusions;
* expose that every horn occurring in that filtration has an inner index;
* package every ordinary basic cell as the underlying map of a KuuOS standard
  type-(A) scaled horn generator.

Thus after this file there is no remaining ordinary prism-filtration problem.
The only residual issue for the endpoint theorem is scaled: compare the
pullback scaling on each attached simplex/horn with the standard type-(A)
scaling, with the known low-dimensional type-(B) completion exceptions.
-/

/-! ## Reuse the pinned Mathlib boundary-prism pairing -/

/-- The boundary prism carries Mathlib's canonical regular `unionProd`
pairing.  The impossible `n = 0` branch is eliminated by the inner-left bound
contained in the type-(A) generator index. -/
noncomputable def standardTypeABoundaryPrismPairing
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardTypeABoundaryPrismSubcomplex g).Pairing := by
  rcases g with ⟨n, i, h0, hn, endpoint⟩
  cases n with
  | zero =>
      have hi : i = 0 := Subsingleton.elim _ _
      subst i
      simp at h0
  | succ n =>
      exact SSet.prodStdSimplex.pairing i 1

/-- The reused pairing is regular, so its ancestrality relation is well
founded and admits the canonical natural-number rank. -/
instance standardTypeABoundaryPrismPairing_isRegular
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardTypeABoundaryPrismPairing g).IsRegular := by
  rcases g with ⟨n, i, h0, hn, endpoint⟩
  cases n with
  | zero =>
      have hi : i = 0 := Subsingleton.elim _ _
      subst i
      simp at h0
  | succ n =>
      simpa [standardTypeABoundaryPrismPairing,
        standardTypeABoundaryPrismSubcomplex] using
        (inferInstance : (SSet.prodStdSimplex.pairing i 1).IsRegular)

/-- Because the original type-(A) horn index is strictly between the two
endpoints, the Mathlib prism pairing uses only inner horns. -/
instance standardTypeABoundaryPrismPairing_isInner
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardTypeABoundaryPrismPairing g).IsInner := by
  rcases g with ⟨n, i, h0, hn, endpoint⟩
  cases n with
  | zero =>
      have hi : i = 0 := Subsingleton.elim _ _
      subst i
      simp at h0
  | succ n =>
      have hi0 : i ≠ 0 := ne_of_gt h0
      obtain ⟨j, rfl⟩ := Fin.eq_succ_of_ne_zero hi0
      have hj : j ≠ Fin.last n := by
        intro hj
        subst j
        simpa using hn
      obtain ⟨k, rfl⟩ := Fin.eq_castSucc_of_ne_last hj
      simpa [standardTypeABoundaryPrismPairing,
        standardTypeABoundaryPrismSubcomplex] using
        (inferInstance :
          (SSet.prodStdSimplex.pairing k.castSucc.succ 1).IsInner)

/-! ## Canonical rank and relative cell complex -/

/-- The canonical natural-number rank function supplied by regularity. -/
noncomputable def standardTypeABoundaryPrismRankFunction
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardTypeABoundaryPrismPairing g).RankFunction ℕ :=
  (standardTypeABoundaryPrismPairing g).rankFunction

/-- The complete ordinary boundary-prism filtration.  Mathlib's
`RankFunction.relativeCellComplex` proves that every successor stage is a
pushout of a coproduct of the rank's horn cells and that the colimit is the
whole prism. -/
noncomputable def standardTypeABoundaryPrismRelativeCellComplex
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    RelativeCellComplex
      (standardTypeABoundaryPrismRankFunction g).basicCell
      (standardTypeABoundaryPrismSubcomplex g).ι :=
  (standardTypeABoundaryPrismRankFunction g).relativeCellComplex

/-- Rank zero starts at the boundary prism itself. -/
theorem standardTypeABoundaryPrism_filtration_zero
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardTypeABoundaryPrismRankFunction g).filtration 0 =
      standardTypeABoundaryPrismSubcomplex g := by
  simpa using (standardTypeABoundaryPrismRankFunction g).filtration_bot

/-- The rank filtration exhausts the whole simplicial prism. -/
theorem standardTypeABoundaryPrism_iSup_filtration
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (⨆ j : ℕ, (standardTypeABoundaryPrismRankFunction g).filtration j) = ⊤ := by
  exact (standardTypeABoundaryPrismRankFunction g).iSup_filtration

/-- Every successor rank square is literally the pushout square constructed by
pinned Mathlib: the left map is the coproduct of all horn inclusions of that
rank. -/
noncomputable def standardTypeABoundaryPrism_rankStep_isPushout
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ) :
    IsPushout
      ((standardTypeABoundaryPrismRankFunction g).t j)
      ((standardTypeABoundaryPrismRankFunction g).m j)
      (SSet.Subcomplex.homOfLE
        ((standardTypeABoundaryPrismRankFunction g).filtration_monotone
          (Order.le_succ j)))
      ((standardTypeABoundaryPrismRankFunction g).b j) :=
  (standardTypeABoundaryPrismRankFunction g).isPushout j

/-! ## Every ordinary attachment cell is an inner type-(A) horn -/

/-- The missing face index of every rank cell is nonzero. -/
theorem standardTypeABoundaryPrism_cell_index_ne_zero
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    c.index ≠ 0 := by
  change
    ((standardTypeABoundaryPrismPairing g).isUniquelyCodimOneFace c.s).index rfl ≠ 0
  exact SSet.Subcomplex.Pairing.IsInner.ne_zero c.s rfl

/-- The missing face index of every rank cell is not the last vertex. -/
theorem standardTypeABoundaryPrism_cell_index_ne_last
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    c.index ≠ Fin.last _ := by
  change
    ((standardTypeABoundaryPrismPairing g).isUniquelyCodimOneFace c.s).index rfl ≠
      Fin.last _
  exact SSet.Subcomplex.Pairing.IsInner.ne_last c.s rfl

/-- Hence every rank-cell horn index is strictly positive. -/
theorem standardTypeABoundaryPrism_cell_index_pos
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    0 < c.index := by
  exact lt_of_le_of_ne (Fin.zero_le _) 
    (standardTypeABoundaryPrism_cell_index_ne_zero g j c).symm

/-- And every rank-cell horn index is strictly below the last vertex. -/
theorem standardTypeABoundaryPrism_cell_index_lt_last
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    c.index < Fin.last (c.dim + 1) := by
  exact lt_of_le_of_ne (Fin.le_last _)
    (standardTypeABoundaryPrism_cell_index_ne_last g j c)

/-- Package the ordinary horn attached at a rank cell as exactly one KuuOS
standard type-(A) horn-generator index. -/
def standardTypeABoundaryPrismCellHornIndex
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    StandardTypeAHornGeneratorIndex where
  n := c.dim + 1
  i := c.index
  inner_left := standardTypeABoundaryPrism_cell_index_pos g j c
  inner_right := standardTypeABoundaryPrism_cell_index_lt_last g j c

/-- The Mathlib basic cell is definitionally the underlying simplicial map of
the corresponding KuuOS standard type-(A) scaled horn generator.  Thus all
ordinary cells in the relative-cell filtration have already been classified;
only their induced scalings remain to be compared. -/
theorem standardTypeABoundaryPrism_basicCell_eq_typeA_underlying
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    (standardTypeABoundaryPrismRankFunction g).basicCell j c =
      (standardTypeAScaledHornGeneratorHom
        (standardTypeABoundaryPrismCellHornIndex g j c)).map := by
  rfl

/-!
The ordinary endpoint-prism filtration is now complete:

```text
A_boundary
  -- rank 0 pushout of coproducts of inner horns -->
  -- rank 1 pushout of coproducts of inner horns -->
  -- ... -->
Delta[n] x Delta[1].
```

Every basic horn is literally the underlying map of a standard type-(A)
generator.  The next geometric unit therefore works entirely at the scaled
level.  It must identify the pullback scaling on each paired simplex/horn with
the standard type-(A) scaling, except for the low-dimensional switch cases
already represented by the v1.57 type-(B) three-simplex completions.  No
ordinary pairing, properness, regularity, rank, or filtration construction
remains to be supplied by hand.
-/

end KUOS.DependentOriginationStandardTypeABoundaryPrismRelativeCellV1_61
