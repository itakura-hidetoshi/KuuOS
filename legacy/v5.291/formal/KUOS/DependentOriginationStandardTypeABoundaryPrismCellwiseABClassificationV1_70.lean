import KUOS.DependentOriginationStandardTypeABoundaryPrismThreeResidualClassificationV1_69
import Mathlib.AlgebraicTopology.SimplexCategory.Basic

namespace KUOS.DependentOriginationStandardTypeABoundaryPrismCellwiseABClassificationV1_70

open CategoryTheory
open CategoryTheory.Category
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeBScalingPushoutV1_56
open KUOS.DependentOriginationStandardTypeBThreeSimplexCompletionV1_57
open KUOS.DependentOriginationStandardTypeABoundaryPrismRelativeCellV1_61
open KUOS.DependentOriginationStandardTypeABoundaryPrismScaledCellsV1_62
open KUOS.DependentOriginationStandardTypeABoundaryPrismDimensionDichotomyV1_63
open KUOS.DependentOriginationStandardTypeABoundaryPrismStaircaseNormalFormV1_64
open KUOS.DependentOriginationStandardTypeABoundaryPrismCellPushoutCriterionV1_65
open KUOS.DependentOriginationStandardTypeABoundaryPrismCellACompatibilityV1_66
open KUOS.DependentOriginationStandardTypeABoundaryPrismN2MaximalFrontierV1_67
open KUOS.DependentOriginationStandardTypeBThreeSimplexMaximalCompletionV1_68
open KUOS.DependentOriginationStandardTypeABoundaryPrismThreeResidualClassificationV1_69

universe u

noncomputable section

/-!
# Complete boundary-prism cellwise A/B classification v1.70

This file closes the local scaled geometry left open by v1.69.  It keeps the
ordinary Mathlib rank cell as the carrier and proves, for every such cell, that
its exact scaled attachment is one of exactly three forms:

```text
pure A,
A followed by the q12 type-(B) completion,
A followed by the q23 type-(B) completion.
```

The equal-dimensional branch is rigid because the paired first coordinate is
a surjective monotone endomorphism of the same finite ordinal.  We turn
surjectivity into `Epi`, use `SimplexCategory.eq_id_of_epi`, and recover the
identity first coordinate.  Hence the cell index is the original type-(A)
index and the exact cell scaling has no post-A residual.

For the only genuinely exceptional branch, `g.n = 2` and attached dimension
three, v1.67 says the exact cell target is maximal.  Therefore the actual horn
scaling is maximal, and the type-(A) cobase change has exactly the intrinsic
"standard A or already in the horn" scaling.  A single canonical transport to
`Delta[3]` identifies this scaling with the fixed horn-saturated table of
v1.69, giving literal q12/q23 base and completed-target equalities.

No canonical-KuuOS/standard-A-B-C family equality is asserted here.
-/

/-! ## Public first-coordinate rigidity for the union-product pairing -/

/-- Public-pairing form of the v1.63 first-coordinate surjectivity theorem. -/
theorem unionProdPairing_typeTwo_fst_surjective
    {m : ℕ}
    (k : Fin (m + 1))
    (z : (SSet.prodStdSimplex.pairing.{u} k.castSucc 1).II) :
    Function.Surjective
      (((SSet.prodStdSimplex.pairing.{u} k.castSucc 1).p z).val.cast
        ((SSet.prodStdSimplex.pairing.{u} k.castSucc 1)
          .isUniquelyCodimOneFace z).dim_eq).simplex.1 := by
  rw [SSet.prodStdSimplex.pairing_castSucc] at z ⊢
  obtain ⟨s, rfl⟩ :=
    (SSet.prodStdSimplex.pairingCore.{u} k 1).equivII.surjective z
  simpa [SSet.prodStdSimplex.pairingCore] using
    unionProdPairingCore_typeOne_fst_surjective k s

/-- The public pairing also remembers the exact transition at its missing-face
index: there is a predecessor index `l` whose cast is the cell index, with
first coordinates `k` and `k+1` on the two adjacent vertices. -/
theorem unionProdPairing_typeTwo_index_transition
    {m : ℕ}
    (k : Fin (m + 1))
    (z : (SSet.prodStdSimplex.pairing.{u} k.castSucc 1).II) :
    ∃ l : Fin (z.val.dim + 1),
      l.castSucc =
          ((SSet.prodStdSimplex.pairing.{u} k.castSucc 1)
            .isUniquelyCodimOneFace z).index rfl ∧
        (((SSet.prodStdSimplex.pairing.{u} k.castSucc 1).p z).val.cast
          ((SSet.prodStdSimplex.pairing.{u} k.castSucc 1)
            .isUniquelyCodimOneFace z).dim_eq).simplex.1 l.castSucc =
            k.castSucc ∧
        (((SSet.prodStdSimplex.pairing.{u} k.castSucc 1).p z).val.cast
          ((SSet.prodStdSimplex.pairing.{u} k.castSucc 1)
            .isUniquelyCodimOneFace z).dim_eq).simplex.1 l.succ =
            k.succ := by
  rw [SSet.prodStdSimplex.pairing_castSucc] at z ⊢
  obtain ⟨s, rfl⟩ :=
    (SSet.prodStdSimplex.pairingCore.{u} k 1).equivII.surjective z
  refine ⟨s.index, ?_, ?_, ?_⟩
  · simp [SSet.prodStdSimplex.pairingCore]
  · simpa [SSet.prodStdSimplex.pairingCore] using
      s.isIndex.simplex_fst_castSucc
  · simpa [SSet.prodStdSimplex.pairingCore] using
      s.isIndex.simplex_fst_succ

/-- The first coordinate of every actual KuuOS boundary-prism paired simplex
is surjective. -/
theorem standardTypeABoundaryPrismCellPaired_fst_surjective
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    Function.Surjective
      (standardTypeABoundaryPrismCellPairedNondegenerate g j c).1.1 := by
  rcases g with ⟨n, i, h0, hn, endpoint⟩
  cases n with
  | zero =>
      have hi : i = 0 := Subsingleton.elim _ _
      subst i
      simp at h0
  | succ m =>
      have hilast : i ≠ Fin.last (m + 1) := ne_of_lt hn
      obtain ⟨k, rfl⟩ := Fin.eq_castSucc_of_ne_last hilast
      simpa [standardTypeABoundaryPrismCellPairedNondegenerate,
        standardTypeABoundaryPrismPairing] using
        unionProdPairing_typeTwo_fst_surjective k c.s

/-- Exact adjacent transition data for an actual KuuOS rank cell. -/
theorem standardTypeABoundaryPrismCellPaired_index_transition
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    ∃ l : Fin (c.dim + 1),
      l.castSucc = c.index ∧
        (standardTypeABoundaryPrismCellPairedNondegenerate g j c).1.1
            l.castSucc = g.i ∧
        (standardTypeABoundaryPrismCellPairedNondegenerate g j c).1.1
            l.succ =
          ⟨g.i.val + 1, by
            have h := g.inner_right
            change g.i.val < g.n at h
            omega⟩ := by
  rcases g with ⟨n, i, h0, hn, endpoint⟩
  cases n with
  | zero =>
      have hi : i = 0 := Subsingleton.elim _ _
      subst i
      simp at h0
  | succ m =>
      have hilast : i ≠ Fin.last (m + 1) := ne_of_lt hn
      obtain ⟨k, rfl⟩ := Fin.eq_castSucc_of_ne_last hilast
      simpa [standardTypeABoundaryPrismCellPairedNondegenerate,
        standardTypeABoundaryPrismPairing] using
        unionProdPairing_typeTwo_index_transition k c.s

/-! ## Equal-dimensional cells: surjective endomorphism = identity -/

/-- Simplex-category morphism represented by the paired first coordinate. -/
noncomputable def standardTypeABoundaryPrismCellFirstCoordinateOrdinal
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    ⦋c.dim + 1⦌ ⟶ ⦋g.n⦌ :=
  SSet.stdSimplex.objEquiv
    (standardTypeABoundaryPrismCellPairedNondegenerate g j c).1.1

/-- The represented ordinal morphism is an epimorphism. -/
theorem standardTypeABoundaryPrismCellFirstCoordinateOrdinal_epi
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    Epi (standardTypeABoundaryPrismCellFirstCoordinateOrdinal g j c) := by
  rw [SimplexCategory.epi_iff_surjective]
  simpa [standardTypeABoundaryPrismCellFirstCoordinateOrdinal] using
    standardTypeABoundaryPrismCellPaired_fst_surjective g j c

/-- In the equal-dimensional branch, transport the first-coordinate ordinal
back to the source ordinal. -/
noncomputable def standardTypeABoundaryPrismCellEqualFirstCoordinateEndomorphism
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (heq : c.dim + 1 = g.n) :
    ⦋c.dim + 1⦌ ⟶ ⦋c.dim + 1⦌ :=
  standardTypeABoundaryPrismCellFirstCoordinateOrdinal g j c ≫
    eqToHom (congrArg (fun n : ℕ => ⦋n⦌) heq.symm)

/-- The equal-dimensional paired first coordinate is the identity after the
canonical ordinal transport.  This is the exact `surjective -> Epi -> id`
rigidity step. -/
theorem standardTypeABoundaryPrismCellEqualFirstCoordinateEndomorphism_eq_id
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (heq : c.dim + 1 = g.n) :
    standardTypeABoundaryPrismCellEqualFirstCoordinateEndomorphism g j c heq =
      𝟙 _ := by
  let θ := standardTypeABoundaryPrismCellFirstCoordinateOrdinal g j c
  haveI hθ : Epi θ :=
    standardTypeABoundaryPrismCellFirstCoordinateOrdinal_epi g j c
  haveI : Epi
      (standardTypeABoundaryPrismCellEqualFirstCoordinateEndomorphism
        g j c heq) := by
    dsimp [standardTypeABoundaryPrismCellEqualFirstCoordinateEndomorphism]
    infer_instance
  exact SimplexCategory.eq_id_of_epi _

/-- Canonical transport of the original generator index to the equal-dimensional
cell's vertex ordinal. -/
noncomputable def standardTypeABoundaryPrismEqualGeneratorIndex
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (heq : c.dim + 1 = g.n) : Fin (c.dim + 2) :=
  Fin.cast (by omega) g.i

/-- Pairing rigidity forces the actual cell horn index to be exactly the
transported original type-(A) index. -/
theorem standardTypeABoundaryPrism_cell_index_eq_generatorIndex_of_equal
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (heq : c.dim + 1 = g.n) :
    c.index = standardTypeABoundaryPrismEqualGeneratorIndex g j c heq := by
  rcases standardTypeABoundaryPrismCellPaired_index_transition g j c with
    ⟨l, hl, hfst, _⟩
  have hid :=
    standardTypeABoundaryPrismCellEqualFirstCoordinateEndomorphism_eq_id
      g j c heq
  have happ := SimplexCategory.congr_toOrderHom_apply hid l.castSucc
  rw [hl] at hfst
  rw [hfst] at happ
  apply Fin.ext
  simpa [standardTypeABoundaryPrismCellEqualFirstCoordinateEndomorphism,
    standardTypeABoundaryPrismCellFirstCoordinateOrdinal,
    standardTypeABoundaryPrismEqualGeneratorIndex] using happ.symm

/-- On every triangle, the equal-dimensional first-coordinate map is exactly
canonical finite-ordinal transport. -/
theorem standardTypeABoundaryPrismCellFirstCoordinateMap_apply_of_equal
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (heq : c.dim + 1 = g.n)
    (t : (Δ[c.dim + 1] : SSet.{u}).obj (op ⦋2⦌))
    (a : Fin 3) :
    ((standardTypeABoundaryPrismCellFirstCoordinateMap g j c)
      .app (op ⦋2⦌) t) a =
      Fin.cast (by omega) (t a) := by
  have hid :=
    standardTypeABoundaryPrismCellEqualFirstCoordinateEndomorphism_eq_id
      g j c heq
  have hθ :
      standardTypeABoundaryPrismCellFirstCoordinateOrdinal g j c ≫
          eqToHom (congrArg (fun n : ℕ => ⦋n⦌) heq.symm) =
        𝟙 _ := by
    simpa [standardTypeABoundaryPrismCellEqualFirstCoordinateEndomorphism]
      using hid
  have hpoint := SimplexCategory.congr_toOrderHom_apply hθ (t a)
  simpa [standardTypeABoundaryPrismCellFirstCoordinateOrdinal,
    standardTypeABoundaryPrismCellFirstCoordinateMap] using hpoint

/-- Equal-dimensional cells have exact target scaling equal to their own
standard type-(A) scaling. -/
theorem standardTypeABoundaryPrismCellScaling_eq_standardTypeA_of_equal
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (heq : c.dim + 1 = g.n) :
    standardTypeABoundaryPrismCellScaling g j c =
      standardTypeASimplexScaling c.index := by
  apply scaling_eq_of_le_antisymm
  · intro t ht
    change
      (standardTypeASimplexScaling g.i).thin
        ((standardTypeABoundaryPrismCellFirstCoordinateMap g j c)
          .app (op ⦋2⦌) t) at ht
    rw [standardTypeABoundaryPrism_cell_index_eq_generatorIndex_of_equal
      g j c heq]
    rcases ht with hmin | hdist
    · left
      rcases hmin with ⟨x, hx⟩ | ⟨x, hx⟩
      · left
        refine ⟨(Δ[c.dim + 1] : SSet.{u}).δ (0 : Fin 3) t, ?_⟩
        apply SSet.stdSimplex.ext
        intro a
        fin_cases a <;>
          simp [SSet.stdSimplex.σ_apply, SSet.stdSimplex.δ_apply]
      · right
        refine ⟨(Δ[c.dim + 1] : SSet.{u}).δ (2 : Fin 3) t, ?_⟩
        apply SSet.stdSimplex.ext
        intro a
        fin_cases a <;>
          simp [SSet.stdSimplex.σ_apply, SSet.stdSimplex.δ_apply]
    · right
      refine ⟨?_, ?_, ?_⟩
      · apply Fin.ext
        have h := hdist.1
        simpa [standardTypeABoundaryPrismEqualGeneratorIndex] using h
      · have h := hdist.2.1
        change
          (((standardTypeABoundaryPrismCellFirstCoordinateMap g j c)
            .app (op ⦋2⦌) t) 0).val + 1 = g.i.val at h
        rw [standardTypeABoundaryPrismCellFirstCoordinateMap_apply_of_equal
          g j c heq t 0] at h
        simpa [standardTypeABoundaryPrismEqualGeneratorIndex] using h
      · have h := hdist.2.2
        change
          g.i.val + 1 =
            (((standardTypeABoundaryPrismCellFirstCoordinateMap g j c)
              .app (op ⦋2⦌) t) 2).val at h
        rw [standardTypeABoundaryPrismCellFirstCoordinateMap_apply_of_equal
          g j c heq t 2] at h
        simpa [standardTypeABoundaryPrismEqualGeneratorIndex] using h
  · exact standardTypeABoundaryPrismCellACompatible_all g j c

/-- Therefore every equal-dimensional cell is a pure type-(A) cobase change. -/
theorem standardTypeABoundaryPrismCellAPushoutScaling_eq_cellScaling_of_equal
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (heq : c.dim + 1 = g.n) :
    standardTypeABoundaryPrismCellAPushoutScaling g j c =
      standardTypeABoundaryPrismCellScaling g j c := by
  apply standardTypeABoundaryPrismCellAPushoutScaling_eq_cellScaling
    g j c (standardTypeABoundaryPrismCellACompatible_all g j c)
  intro t ht _
  rw [standardTypeABoundaryPrismCellScaling_eq_standardTypeA_of_equal
    g j c heq] at ht
  exact ht

/-! ## Actual `n = 2`, `N = 3` A-pushouts and canonical transport -/

/-- Intrinsic A-plus-horn saturation on an actual dependent cell carrier. -/
def standardTypeABoundaryPrismCellHornSaturatedAScaling
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    ScaledSimplicialSet (Δ[c.dim + 1] : SSet.{u}) where
  thin := fun t =>
    (standardTypeASimplexScaling c.index).thin t ∨
      t ∈ c.horn.obj (op ⦋2⦌)
  thin_sigma_zero := by
    intro x
    exact Or.inl ((standardTypeASimplexScaling c.index).thin_sigma_zero x)
  thin_sigma_one := by
    intro x
    exact Or.inl ((standardTypeASimplexScaling c.index).thin_sigma_one x)

/-- If the exact target is maximal, then the actual type-(A) cobase-change
scaling is exactly A plus all triangles already in the horn. -/
theorem standardTypeABoundaryPrismCellAPushoutScaling_eq_hornSaturated_of_cell_maximal
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (hmax : standardTypeABoundaryPrismCellScaling g j c =
      ScaledSimplicialSet.maximal (Δ[c.dim + 1] : SSet.{u})) :
    standardTypeABoundaryPrismCellAPushoutScaling g j c =
      standardTypeABoundaryPrismCellHornSaturatedAScaling g j c := by
  apply scaling_eq_of_le_antisymm
  · intro t ht
    change
      (standardTypeASimplexScaling c.index).thin t ∨
        ∃ x : (c.horn : SSet.{u}).obj (op ⦋2⦌),
          (standardTypeABoundaryPrismCellHornScaling g j c).thin x ∧
            c.horn.ι.app (op ⦋2⦌) x = t at ht
    rcases ht with hA | ⟨x, _, rfl⟩
    · exact Or.inl hA
    · exact Or.inr x.2
  · intro t ht
    rcases ht with hA | hhorn
    · exact Or.inl hA
    · right
      let x : (c.horn : SSet.{u}).obj (op ⦋2⦌) := ⟨t, hhorn⟩
      refine ⟨x, ?_, rfl⟩
      change
        (standardTypeABoundaryPrismCellScaling g j c).thin
          (c.horn.ι.app (op ⦋2⦌) x)
      rw [hmax]
      exact ScaledSimplicialSet.maximal_thin _ _

/-- Canonical one-shot transport of any actual three-cell scaling to the fixed
`Delta[3]` carrier. -/
noncomputable def standardTypeABoundaryPrismTransportScalingToThree
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h3 : c.dim + 1 = 3)
    (s : ScaledSimplicialSet (Δ[c.dim + 1] : SSet.{u})) :
    ScaledSimplicialSet (Δ[3] : SSet.{u}) :=
  Eq.mp
    (congrArg (fun n : ℕ => ScaledSimplicialSet (Δ[n] : SSet.{u})) h3)
    s

/-- Transport commutes with maximal scaling. -/
theorem standardTypeABoundaryPrismTransportScalingToThree_maximal
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h3 : c.dim + 1 = 3) :
    standardTypeABoundaryPrismTransportScalingToThree g j c h3
        (ScaledSimplicialSet.maximal (Δ[c.dim + 1] : SSet.{u})) =
      ScaledSimplicialSet.maximal (Δ[3] : SSet.{u}) := by
  subst_vars
  rfl

/-- The transported actual horn-saturated scaling is literally the fixed v1.69
horn-saturated scaling at the transported cell index. -/
theorem standardTypeABoundaryPrismTransportScalingToThree_hornSaturated
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h3 : c.dim + 1 = 3) :
    standardTypeABoundaryPrismTransportScalingToThree g j c h3
        (standardTypeABoundaryPrismCellHornSaturatedAScaling g j c) =
      standardTypeAThreeHornSaturatedScaling
        (standardTypeABoundaryPrismCellIndex3 g j c h3) := by
  subst_vars
  simp [standardTypeABoundaryPrismTransportScalingToThree,
    standardTypeABoundaryPrismCellHornSaturatedAScaling,
    standardTypeAThreeHornSaturatedScaling,
    standardTypeABoundaryPrismCellIndex3]

/-- In the exceptional `n = 2`, `N = 3` branch the transported A-pushout is
exactly the fixed horn-saturated A scaling. -/
theorem standardTypeABoundaryPrism_generator_two_target_three_APushout_transport
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (hn2 : g.n = 2)
    (h3 : c.dim + 1 = 3) :
    standardTypeABoundaryPrismTransportScalingToThree g j c h3
        (standardTypeABoundaryPrismCellAPushoutScaling g j c) =
      standardTypeAThreeHornSaturatedScaling
        (standardTypeABoundaryPrismCellIndex3 g j c h3) := by
  rw [standardTypeABoundaryPrismCellAPushoutScaling_eq_hornSaturated_of_cell_maximal
    g j c
    (standardTypeABoundaryPrismCellScaling_eq_maximal_of_generator_two_target_three
      g j c hn2 h3)]
  exact standardTypeABoundaryPrismTransportScalingToThree_hornSaturated
    g j c h3

/-- Exact q12 factorization of an actual exceptional cell with fixed index 1. -/
structure StandardTypeABoundaryPrismCellQ12Factorization
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) : Prop where
  generator_two : g.n = 2
  target_three : c.dim + 1 = 3
  index_one :
    standardTypeABoundaryPrismCellIndex3 g j c target_three = (1 : Fin 4)
  A_base :
    standardTypeABoundaryPrismTransportScalingToThree g j c target_three
        (standardTypeABoundaryPrismCellAPushoutScaling g j c) =
      standardTypeBCollapse12BaseScaling
  completed_target :
    standardTypeABoundaryPrismTransportScalingToThree g j c target_three
        (standardTypeABoundaryPrismCellScaling g j c) =
      standardTypeBCollapse12CompletedScaling

/-- Exact q23 factorization of an actual exceptional cell with fixed index 2. -/
structure StandardTypeABoundaryPrismCellQ23Factorization
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) : Prop where
  generator_two : g.n = 2
  target_three : c.dim + 1 = 3
  index_two :
    standardTypeABoundaryPrismCellIndex3 g j c target_three = (2 : Fin 4)
  A_base :
    standardTypeABoundaryPrismTransportScalingToThree g j c target_three
        (standardTypeABoundaryPrismCellAPushoutScaling g j c) =
      standardTypeBCollapse23BaseScaling
  completed_target :
    standardTypeABoundaryPrismTransportScalingToThree g j c target_three
        (standardTypeABoundaryPrismCellScaling g j c) =
      standardTypeBCollapse23CompletedScaling

/-- Index 1 gives literal A;q12 base/completed equality. -/
theorem standardTypeABoundaryPrismCellQ12Factorization_of_index_one
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (hn2 : g.n = 2)
    (h3 : c.dim + 1 = 3)
    (hidx : standardTypeABoundaryPrismCellIndex3 g j c h3 = (1 : Fin 4)) :
    StandardTypeABoundaryPrismCellQ12Factorization g j c := by
  refine ⟨hn2, h3, ?_, ?_, ?_⟩
  · simpa using hidx
  · rw [standardTypeABoundaryPrism_generator_two_target_three_APushout_transport
      g j c hn2 h3,
    hidx,
    standardTypeAThreeHornSaturatedScaling_one_eq_q12Base]
  · calc
      standardTypeABoundaryPrismTransportScalingToThree g j c h3
          (standardTypeABoundaryPrismCellScaling g j c) =
          ScaledSimplicialSet.maximal (Δ[3] : SSet.{u}) := by
            rw [standardTypeABoundaryPrismCellScaling_eq_maximal_of_generator_two_target_three
              g j c hn2 h3]
            exact standardTypeABoundaryPrismTransportScalingToThree_maximal
              g j c h3
      _ = standardTypeBCollapse12CompletedScaling :=
        standardTypeBCollapse12CompletedScaling_eq_maximal.symm

/-- Index 2 gives literal A;q23 base/completed equality. -/
theorem standardTypeABoundaryPrismCellQ23Factorization_of_index_two
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (hn2 : g.n = 2)
    (h3 : c.dim + 1 = 3)
    (hidx : standardTypeABoundaryPrismCellIndex3 g j c h3 = (2 : Fin 4)) :
    StandardTypeABoundaryPrismCellQ23Factorization g j c := by
  refine ⟨hn2, h3, ?_, ?_, ?_⟩
  · simpa using hidx
  · rw [standardTypeABoundaryPrism_generator_two_target_three_APushout_transport
      g j c hn2 h3,
    hidx,
    standardTypeAThreeHornSaturatedScaling_two_eq_q23Base]
  · calc
      standardTypeABoundaryPrismTransportScalingToThree g j c h3
          (standardTypeABoundaryPrismCellScaling g j c) =
          ScaledSimplicialSet.maximal (Δ[3] : SSet.{u}) := by
            rw [standardTypeABoundaryPrismCellScaling_eq_maximal_of_generator_two_target_three
              g j c hn2 h3]
            exact standardTypeABoundaryPrismTransportScalingToThree_maximal
              g j c h3
      _ = standardTypeBCollapse23CompletedScaling :=
        standardTypeBCollapse23CompletedScaling_eq_maximal.symm

/-! ## Exhaustive cellwise classification -/

/-- Every boundary-prism rank cell is pure A, exact A;q12, or exact A;q23.
There is no unclassified local scaling geometry. -/
theorem standardTypeABoundaryPrism_cell_complete_AB_classification
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    standardTypeABoundaryPrismCellAPushoutScaling g j c =
        standardTypeABoundaryPrismCellScaling g j c ∨
      StandardTypeABoundaryPrismCellQ12Factorization g j c ∨
      StandardTypeABoundaryPrismCellQ23Factorization g j c := by
  rcases standardTypeABoundaryPrismCell_pureA_or_target_dim_three g j c with
    hpure | h3
  · exact Or.inl hpure
  · rcases standardTypeABoundaryPrism_cell_dim_three_origin_normalForm
      g j c h3 with hequal | htop
    · left
      exact standardTypeABoundaryPrismCellAPushoutScaling_eq_cellScaling_of_equal
        g j c hequal.2
    · right
      rcases htop with ⟨hn2, _htop, _r, _hr⟩
      rcases standardTypeABoundaryPrismCellIndex3_eq_one_or_two g j c h3 with
        hidx | hidx
      · exact Or.inl
          (standardTypeABoundaryPrismCellQ12Factorization_of_index_one
            g j c hn2 h3 hidx)
      · exact Or.inr
          (standardTypeABoundaryPrismCellQ23Factorization_of_index_two
            g j c hn2 h3 hidx)

/-!
The exhaustive local exit criterion is now theorem-level:

```text
every boundary-prism rank cell
  = pure A
  or A ; q12
  or A ; q23.
```

The only remaining display refinement is to identify the three `n=2` top
staircases as `q23, q23, q12`; it does not change the exhaustive factorization
above.  Once that finite display theorem is attached, the next mathematical
unit may build the genuine scaled rank filtration without reopening local
geometry.
-/

end

end KUOS.DependentOriginationStandardTypeABoundaryPrismCellwiseABClassificationV1_70
