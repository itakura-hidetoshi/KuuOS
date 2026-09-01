import KUOS.DependentOriginationStandardTypeABoundaryPrismCellPushoutCriterionV1_65

namespace KUOS.DependentOriginationStandardTypeABoundaryPrismCellACompatibilityV1_66

open CategoryTheory
open Opposite
open Simplicial
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationScaledAnodyneAttachmentFactorizationV1_48
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeABoundaryPrismRelativeCellV1_61
open KUOS.DependentOriginationStandardTypeABoundaryPrismScaledCellsV1_62
open KUOS.DependentOriginationStandardTypeABoundaryPrismDimensionDichotomyV1_63
open KUOS.DependentOriginationStandardTypeABoundaryPrismStaircaseNormalFormV1_64
open KUOS.DependentOriginationStandardTypeABoundaryPrismCellPushoutCriterionV1_65

universe u

noncomputable section

/-!
# Type-(A) compatibility for every boundary-prism cell v1.66

Version v1.65 reduced the scaled cell problem to two local conditions.  The
first was target type-(A) compatibility

```text
standard type-(A) scaling at the cell index <= exact ambient cell scaling.
```

This file proves that condition for every rank cell, with no dimension split.
The proof uses the actual `unionProd` pairing rather than a presentation-level
shortcut.

For a type-(I) walk, let `p` be its pairing index and `i` the original horn
index.  Mathlib's `IsIndex` theorem gives

```text
fst(p)     = i,
fst(p + 1) = i + 1.
```

The first coordinate is also surjective by v1.63.  Hence the vertex immediately
before `p` maps either to `i - 1` or to `i`; there is no third possibility.
Therefore the distinguished type-(A) triangle centered at `p` maps either to

```text
(i-1, i, i+1)
```

(the original distinguished type-(A) triangle), or to

```text
(i, i, i+1)
```

(a degenerate triangle).  In either case it is thin.  Minimal thin triangles
are preserved by every simplicial map, so the complete type-(A) scaling is
preserved.

Consequences:

* `ACompatible` from v1.65 is unconditional for every boundary-prism cell;
* every attached cell of dimension at least four is exactly a pure type-(A)
  cobase change;
* any genuine post-A scaling residual is forced into dimensions two or three.

Thus the remaining type-(B) calculation is genuinely finite and low-dimensional.
-/

/-! ## A repeated first pair is minimally thin -/

/-- A standard-simplex 2-simplex whose first two vertices agree is the
`σ 0`-degeneracy of its `0`th face, hence belongs to the minimal scaling. -/
theorem minimalScaling_stdSimplex_thin_of_zero_eq_one
    {n : ℕ}
    (t : (Δ[n] : SSet.{u}).obj (op ⦋2⦌))
    (h01 : t 0 = t 1) :
    (minimalScaling (Δ[n] : SSet.{u})).thin t := by
  refine Or.inl ⟨(Δ[n] : SSet.{u}).δ (0 : Fin 3) t, ?_⟩
  apply SSet.stdSimplex.ext
  intro a
  fin_cases a <;>
    simp [SSet.stdSimplex.σ_apply, SSet.stdSimplex.δ_apply, h01]

/-! ## First-coordinate map of a core type-(I) walk -/

/-- The simplicial map represented by the first coordinate of one type-(I)
`unionProd` walk. -/
noncomputable def unionProdPairingCoreTypeOneFirstCoordinateMap
    {m : ℕ}
    (k : Fin (m + 1))
    (s : SSet.prodStdSimplex.pairingCore.Type₁.{u} k 1) :
    (Δ[s.d + 1] : SSet.{u}) ⟶ Δ[m + 1] :=
  SSet.yonedaEquiv.symm (s.x.cast s.hd).simplex.1

/-- Evaluation of the represented first-coordinate map is literal
precomposition of the top first-coordinate simplex. -/
@[simp]
theorem unionProdPairingCoreTypeOneFirstCoordinateMap_apply
    {m d : ℕ}
    (k : Fin (m + 1))
    (s : SSet.prodStdSimplex.pairingCore.Type₁.{u} k 1)
    (t : (Δ[s.d + 1] : SSet.{u}).obj (op ⦋d⦌))
    (a : Fin (d + 1)) :
    ((unionProdPairingCoreTypeOneFirstCoordinateMap k s).app (op ⦋d⦌) t) a =
      (s.x.cast s.hd).simplex.1 (t a) := by
  rfl

/-! ## The distinguished cell triangle maps to A-thin geometry -/

/-- The image of the cell's distinguished type-(A) triangle under the first
coordinate is either minimally thin or exactly the original distinguished
triangle.

Surjectivity is used only once: it supplies the vertex immediately below the
original horn index somewhere before the pairing index.  Monotonicity then
forces the predecessor of the pairing index to map to either that vertex or
the horn index itself. -/
theorem unionProdPairingCore_typeOne_distinguished_firstCoordinate_thin
    {m : ℕ}
    (k : Fin (m + 1))
    (hk0 : 0 < k.castSucc)
    (s : SSet.prodStdSimplex.pairingCore.Type₁.{u} k 1)
    (t : (Δ[s.d + 1] : SSet.{u}).obj (op ⦋2⦌))
    (ht : IsStandardTypeADistinguishedTriangle s.index.castSucc t) :
    let y :=
      (unionProdPairingCoreTypeOneFirstCoordinateMap k s).app (op ⦋2⦌) t
    (minimalScaling (Δ[m + 1] : SSet.{u})).thin y ∨
      IsStandardTypeADistinguishedTriangle k.castSucc y := by
  have hkpos : 0 < k.val := by
    simpa using hk0
  let km1 : Fin (m + 2) := ⟨k.val - 1, by omega⟩
  obtain ⟨q, hq⟩ :=
    unionProdPairingCore_typeOne_fst_surjective k s km1
  have hq_lt : q < s.index.castSucc := by
    by_contra hnot
    have hpq : s.index.castSucc ≤ q := le_of_not_gt hnot
    have hmono :=
      SSet.stdSimplex.monotone_apply (s.x.cast s.hd).simplex.1 hpq
    change
      (s.x.cast s.hd).simplex.1 s.index.castSucc ≤
        (s.x.cast s.hd).simplex.1 q at hmono
    rw [s.isIndex.simplex_fst_castSucc, hq] at hmono
    change k.val ≤ km1.val at hmono
    dsimp [km1] at hmono
    omega
  have ht0val : (t 0).val + 1 = s.index.val := by
    simpa using ht.2.1
  have hqval : q.val < s.index.val := by
    change q.val < s.index.val at hq_lt
    exact hq_lt
  have hq_le_t0 : q ≤ t 0 := by
    change q.val ≤ (t 0).val
    omega
  have ht0_le_index : t 0 ≤ s.index.castSucc := by
    change (t 0).val ≤ s.index.val
    omega
  have hlower :=
    SSet.stdSimplex.monotone_apply (s.x.cast s.hd).simplex.1 hq_le_t0
  change
    (s.x.cast s.hd).simplex.1 q ≤
      (s.x.cast s.hd).simplex.1 (t 0) at hlower
  rw [hq] at hlower
  have hupper :=
    SSet.stdSimplex.monotone_apply (s.x.cast s.hd).simplex.1 ht0_le_index
  change
    (s.x.cast s.hd).simplex.1 (t 0) ≤
      (s.x.cast s.hd).simplex.1 s.index.castSucc at hupper
  rw [s.isIndex.simplex_fst_castSucc] at hupper
  have hpred_or_eq :
      (s.x.cast s.hd).simplex.1 (t 0) = km1 ∨
        (s.x.cast s.hd).simplex.1 (t 0) = k.castSucc := by
    by_cases heq : (s.x.cast s.hd).simplex.1 (t 0) = k.castSucc
    · exact Or.inr heq
    · left
      apply Fin.ext
      change km1.val ≤ ((s.x.cast s.hd).simplex.1 (t 0)).val at hlower
      change ((s.x.cast s.hd).simplex.1 (t 0)).val ≤ k.val at hupper
      have hne : ((s.x.cast s.hd).simplex.1 (t 0)).val ≠ k.val := by
        intro hval
        apply heq
        apply Fin.ext
        exact hval
      let r : ℕ := ((s.x.cast s.hd).simplex.1 (t 0)).val
      have hlower' : k.val - 1 ≤ r := by
        simpa [r, km1] using hlower
      have hupper' : r ≤ k.val := by
        simpa [r] using hupper
      have hne' : r ≠ k.val := by
        simpa [r] using hne
      have hr : r = k.val - 1 := by
        omega
      simpa [r, km1] using hr
  have ht2 : t 2 = s.index.succ := by
    apply Fin.ext
    change (t 2).val = s.index.val + 1
    have h := ht.2.2
    change s.index.val + 1 = (t 2).val at h
    exact h.symm
  let y :=
    (unionProdPairingCoreTypeOneFirstCoordinateMap k s).app (op ⦋2⦌) t
  have hy1 : y 1 = k.castSucc := by
    dsimp [y]
    rw [unionProdPairingCoreTypeOneFirstCoordinateMap_apply, ht.1]
    exact s.isIndex.simplex_fst_castSucc
  have hy2 : y 2 = k.succ := by
    dsimp [y]
    rw [unionProdPairingCoreTypeOneFirstCoordinateMap_apply, ht2]
    exact s.isIndex.simplex_fst_succ
  rcases hpred_or_eq with hpred | heq
  · exact Or.inr ⟨hy1, by
      dsimp [y]
      rw [unionProdPairingCoreTypeOneFirstCoordinateMap_apply, hpred]
      dsimp [km1]
      omega, by
      rw [hy2]
      rfl⟩
  · apply Or.inl
    apply minimalScaling_stdSimplex_thin_of_zero_eq_one y
    have hy0 : y 0 = k.castSucc := by
      dsimp [y]
      rw [unionProdPairingCoreTypeOneFirstCoordinateMap_apply, heq]
    exact hy0.trans hy1.symm

/-- Therefore the entire standard type-(A) scaling at the pairing index is
preserved by the first-coordinate map of every type-(I) walk. -/
theorem unionProdPairingCore_typeOne_firstCoordinate_scaled
    {m : ℕ}
    (k : Fin (m + 1))
    (hk0 : 0 < k.castSucc)
    (s : SSet.prodStdSimplex.pairingCore.Type₁.{u} k 1) :
    IsScaledMap
      (standardTypeASimplexScaling s.index.castSucc)
      (standardTypeASimplexScaling k.castSucc)
      (unionProdPairingCoreTypeOneFirstCoordinateMap k s) := by
  intro t ht
  rcases ht with ht | ht
  · exact
      (minimalScaling_map
        (standardTypeASimplexScaling k.castSucc)
        (unionProdPairingCoreTypeOneFirstCoordinateMap k s)) t ht
  · rcases
      unionProdPairingCore_typeOne_distinguished_firstCoordinate_thin
        k hk0 s t ht with hmin | hA
    · exact Or.inl hmin
    · exact Or.inr hA

/-! ## Public pairing form -/

/-- Public `pairing k.castSucc 1` form of the preceding theorem.  Its source
index is exactly the unique codimension-one face index of the paired type-(I)
simplex, so this is the form consumed by rank cells. -/
theorem unionProdPairing_typeTwo_firstCoordinate_scaled
    {m : ℕ}
    (k : Fin (m + 1))
    (hk0 : 0 < k.castSucc)
    (z : (SSet.prodStdSimplex.pairing.{u} k.castSucc 1).II) :
    IsScaledMap
      (standardTypeASimplexScaling
        (((SSet.prodStdSimplex.pairing.{u} k.castSucc 1).isUniquelyCodimOneFace z).index rfl))
      (standardTypeASimplexScaling k.castSucc)
      (SSet.yonedaEquiv.symm
        (((SSet.prodStdSimplex.pairing.{u} k.castSucc 1).p z).val.cast
          ((SSet.prodStdSimplex.pairing.{u} k.castSucc 1).isUniquelyCodimOneFace z).dim_eq).simplex.1) := by
  simp only [SSet.prodStdSimplex.pairing_castSucc] at z ⊢
  obtain ⟨s, rfl⟩ :=
    (SSet.prodStdSimplex.pairingCore.{u} k 1).equivII.surjective z
  simpa [SSet.prodStdSimplex.pairingCore,
    unionProdPairingCoreTypeOneFirstCoordinateMap] using
    unionProdPairingCore_typeOne_firstCoordinate_scaled k hk0 s

/-! ## Every KuuOS boundary-prism cell is A-compatible -/

/-- First-coordinate simplicial map of the paired type-(I) simplex carried by
a rank cell. -/
noncomputable def standardTypeABoundaryPrismCellFirstCoordinateMap
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    (Δ[c.dim + 1] : SSet.{u}) ⟶ Δ[g.n] :=
  SSet.yonedaEquiv.symm
    (standardTypeABoundaryPrismCellPairedNondegenerate g j c).1.1

/-- The first-coordinate cell map preserves the cell's own standard type-(A)
scaling into the original generator's standard type-(A) scaling. -/
theorem standardTypeABoundaryPrismCellFirstCoordinate_scaled
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    IsScaledMap
      (standardTypeASimplexScaling c.index)
      (standardTypeASimplexScaling g.i)
      (standardTypeABoundaryPrismCellFirstCoordinateMap g j c) := by
  rcases g with ⟨n, i, h0, hn, endpoint⟩
  cases n with
  | zero =>
      have hi : i = 0 := by
        apply Fin.ext
        omega
      subst i
      simp at h0
  | succ m =>
      have hilast : i ≠ Fin.last (m + 1) := ne_of_lt hn
      obtain ⟨k, rfl⟩ := Fin.eq_castSucc_of_ne_last hilast
      change
        IsScaledMap
          (standardTypeASimplexScaling
            (((SSet.prodStdSimplex.pairing.{u} k.castSucc 1).isUniquelyCodimOneFace c.s).index rfl))
          (standardTypeASimplexScaling k.castSucc)
          (SSet.yonedaEquiv.symm
            (((SSet.prodStdSimplex.pairing.{u} k.castSucc 1).p c.s).val.cast
              ((SSet.prodStdSimplex.pairing.{u} k.castSucc 1).isUniquelyCodimOneFace c.s).dim_eq).simplex.1)
      exact unionProdPairing_typeTwo_firstCoordinate_scaled k h0 c.s

/-- The v1.65 target type-(A) compatibility condition is therefore automatic
for every rank cell. -/
theorem standardTypeABoundaryPrismCellACompatible_all
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    standardTypeABoundaryPrismCellACompatible g j c := by
  intro t ht
  change
    (standardTypeASimplexScaling g.i).thin
      ((standardTypeABoundaryPrismCellFirstCoordinateMap g j c).app
        (op ⦋2⦌) t)
  exact standardTypeABoundaryPrismCellFirstCoordinate_scaled g j c t ht

/-! ## High-dimensional cells are now unconditionally pure type-(A) -/

/-- In attached dimension at least four, the exact cell scaling is the
standard type-(A) cobase-change scaling with no hypotheses left. -/
theorem standardTypeABoundaryPrismCellAPushoutScaling_eq_cellScaling_of_four_le_all
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h4 : 4 ≤ c.dim + 1) :
    standardTypeABoundaryPrismCellAPushoutScaling g j c =
      standardTypeABoundaryPrismCellScaling g j c :=
  standardTypeABoundaryPrismCellAPushoutScaling_eq_cellScaling_of_four_le
    g j c (standardTypeABoundaryPrismCellACompatible_all g j c) h4

/-- Object-level form: every high-dimensional exact target is literally the
pure type-(A) cobase-change target. -/
theorem standardTypeABoundaryPrismCellAPushoutTarget_eq_cellTarget_of_four_le_all
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h4 : 4 ≤ c.dim + 1) :
    standardTypeABoundaryPrismCellAPushoutTarget g j c =
      standardTypeABoundaryPrismScaledCellTarget g j c :=
  standardTypeABoundaryPrismCellAPushoutTarget_eq_cellTarget_of_four_le
    g j c (standardTypeABoundaryPrismCellACompatible_all g j c) h4

/-- Every cell is either already a pure type-(A) cobase change or lies in the
finite low-dimensional frontier `N = 2` or `N = 3`. -/
theorem standardTypeABoundaryPrismCell_pureA_or_lowDim
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    standardTypeABoundaryPrismCellAPushoutScaling g j c =
        standardTypeABoundaryPrismCellScaling g j c ∨
      c.dim + 1 = 2 ∨ c.dim + 1 = 3 := by
  by_cases h4 : 4 ≤ c.dim + 1
  · exact Or.inl
      (standardTypeABoundaryPrismCellAPushoutScaling_eq_cellScaling_of_four_le_all
        g j c h4)
  · right
    have h2 := standardTypeABoundaryPrism_cell_target_dim_ge_two g j c
    omega

/-- Equivalently, failure of the outside-A condition can only occur in
attached dimension two or three.  The type-(A) target compatibility itself is
never the source of the residual. -/
theorem standardTypeABoundaryPrismCell_notOutsideACompatible_lowDim
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h : ¬ standardTypeABoundaryPrismCellOutsideACompatible g j c) :
    c.dim + 1 = 2 ∨ c.dim + 1 = 3 := by
  by_contra hlow
  have h2 := standardTypeABoundaryPrism_cell_target_dim_ge_two g j c
  have h4 : 4 ≤ c.dim + 1 := by omega
  exact h
    (standardTypeABoundaryPrismCellOutsideACompatible_of_four_le g j c h4)

/-!
The local scaled geometry has now separated completely:

```text
all cells:
  standard A at cell index --> exact ambient cell scaling

N >= 4:
  standard A cobase change = exact cell

N = 2 or 3:
  only possible remaining issue = scaling-only residual after A.
```

The next unit is therefore finite.  In the `n = 2` top-staircase branch it
computes the three staircase positions explicitly: the first two produce the
`q23` base/completion and the last produces the `q12` base/completion.  Equal
2-cells and equal 3-cells have no residual.  After that classification the
scaled rank filtration can be assembled in `ScaledSSet` and fed to the v1.59
A/B/C cellular certificate without any type-(C) cell.
-/

end

end KUOS.DependentOriginationStandardTypeABoundaryPrismCellACompatibilityV1_66