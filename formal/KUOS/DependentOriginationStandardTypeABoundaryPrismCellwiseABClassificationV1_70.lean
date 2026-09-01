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
open KUOS.DependentOriginationStandardTypeAScaledPushoutSourceEnrichmentV1_53
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

Every ordinary Mathlib boundary-prism rank cell has exactly one of the local
scaled forms

```text
pure A,
A followed by the q12 type-(B) completion,
A followed by the q23 type-(B) completion.
```

The equal-dimensional branch is rigid by surjectivity of the paired first
coordinate. The only post-A residual occurs for `g.n = 2` in target dimension
three and is the finite q12/q23 table of v1.69.
-/

/-! ## Public first-coordinate rigidity for the union-product pairing -/

set_option backward.defeqAttrib.useBackward true
set_option backward.isDefEq.respectTransparency false

/-- Transport the public pairing together with its dependent type-(II) simplex
to the implementation-level pairing core. Keeping the pairing abstract in the
motive lets Lean transport the cell and regularity data together. -/
private lemma unionProdPairing_eq_core_firstCoordinate_data
    {m : ℕ}
    (k : Fin (m + 1))
    {P : (SSet.Subcomplex.unionProd.{u} Λ[m + 1, k.castSucc] ∂Δ[1]).Pairing}
    [P.IsRegular]
    (hP : P = (SSet.prodStdSimplex.pairingCore.{u} k 1).pairing)
    (z : P.II) :
    Function.Surjective
        (((P.p z).val.cast (P.isUniquelyCodimOneFace z).dim_eq).simplex.1) ∧
      ∃ l : Fin (z.val.dim + 1),
        l.castSucc = (P.isUniquelyCodimOneFace z).index rfl ∧
          ((P.p z).val.cast
            (P.isUniquelyCodimOneFace z).dim_eq).simplex.1 l.castSucc =
              k.castSucc ∧
          ((P.p z).val.cast
            (P.isUniquelyCodimOneFace z).dim_eq).simplex.1 l.succ =
              k.succ := by
  subst P
  let C := SSet.prodStdSimplex.pairingCore.{u} k 1
  obtain ⟨s, rfl⟩ := C.equivII.surjective z
  have hdim : (C.equivII s).val.dim = C.dim s := by
    rfl
  have htop :
      (C.pairing.p (C.equivII s)).val.cast
          (C.pairing.isUniquelyCodimOneFace (C.equivII s)).dim_eq =
        s.x.cast s.hd := by
    calc
      _ = (C.pairing.p (C.equivII s)).val :=
        (C.pairing.p (C.equivII s)).val.cast_eq_self
          (C.pairing.isUniquelyCodimOneFace (C.equivII s)).dim_eq
      _ = C.type₁ s := (C.type₁_pairing s).symm
      _ = s.x := by
        simpa [C] using SSet.prodStdSimplex.type₁_pairingCore k s
      _ = s.x.cast s.hd := (s.x.cast_eq_self s.hd).symm
  have hbottom :
      (C.equivII s).val.cast hdim = C.type₂ s := by
    calc
      _ = (C.equivII s).val :=
        (C.equivII s).val.cast_eq_self hdim
      _ = C.type₂ s := by rfl
  have htopSimplex :
      ((C.pairing.p (C.equivII s)).val.cast
          (C.pairing.isUniquelyCodimOneFace (C.equivII s)).dim_eq).simplex =
        (s.x.cast s.hd).simplex := by
    have hs := congrArg (fun q => q.toS) htop
    rw [SSet.S.ext_iff'] at hs
    rcases hs with ⟨_, hs⟩
    simpa using hs
  have hbottomSimplex :
      ((C.equivII s).val.cast hdim).simplex = (C.type₂ s).simplex := by
    have hs := congrArg (fun q => q.toS) hbottom
    rw [SSet.S.ext_iff'] at hs
    rcases hs with ⟨_, hs⟩
    simpa using hs
  have hidx :
      (C.pairing.isUniquelyCodimOneFace (C.equivII s)).index rfl =
        C.index s := by
    symm
    apply
      ((C.pairing.isUniquelyCodimOneFace (C.equivII s)).δ_eq_iff
        hdim (C.index s)).mp
    rw [htopSimplex, hbottomSimplex]
    simpa [C, SSet.prodStdSimplex.pairingCore] using
      (C.isUniquelyCodimOneFace s).δ_index rfl
  have hfirst :
      ((C.pairing.p (C.equivII s)).val.cast
          (C.pairing.isUniquelyCodimOneFace (C.equivII s)).dim_eq).simplex.1 =
        (s.x.cast s.hd).simplex.1 :=
    congrArg Prod.fst htopSimplex
  constructor
  · rw [hfirst]
    exact unionProdPairingCore_typeOne_fst_surjective k s
  · refine ⟨s.index, ?_, ?_, ?_⟩
    · simpa [C, SSet.prodStdSimplex.pairingCore] using hidx.symm
    · rw [hfirst]
      exact s.isIndex.simplex_fst_castSucc
    · rw [hfirst]
      exact s.isIndex.simplex_fst_succ

/-- Public-pairing form of the first-coordinate surjectivity theorem. -/
theorem unionProdPairing_typeTwo_fst_surjective
    {m : ℕ}
    (k : Fin (m + 1))
    (z : (SSet.prodStdSimplex.pairing.{u} k.castSucc 1).II) :
    Function.Surjective
      (((SSet.prodStdSimplex.pairing.{u} k.castSucc 1).p z).val.cast
        ((SSet.prodStdSimplex.pairing.{u} k.castSucc 1).isUniquelyCodimOneFace z).dim_eq).simplex.1 := by
  exact
    (unionProdPairing_eq_core_firstCoordinate_data
      k (P := SSet.prodStdSimplex.pairing.{u} k.castSucc 1)
      (SSet.prodStdSimplex.pairing_castSucc k 1) z).1

/-- The public pairing remembers the exact first-coordinate transition through
its missing face. -/
theorem unionProdPairing_typeTwo_index_transition
    {m : ℕ}
    (k : Fin (m + 1))
    (z : (SSet.prodStdSimplex.pairing.{u} k.castSucc 1).II) :
    ∃ l : Fin (z.val.dim + 1),
      l.castSucc =
          ((SSet.prodStdSimplex.pairing.{u} k.castSucc 1).isUniquelyCodimOneFace z).index rfl ∧
        (((SSet.prodStdSimplex.pairing.{u} k.castSucc 1).p z).val.cast
          ((SSet.prodStdSimplex.pairing.{u} k.castSucc 1).isUniquelyCodimOneFace z).dim_eq).simplex.1 l.castSucc =
            k.castSucc ∧
        (((SSet.prodStdSimplex.pairing.{u} k.castSucc 1).p z).val.cast
          ((SSet.prodStdSimplex.pairing.{u} k.castSucc 1).isUniquelyCodimOneFace z).dim_eq).simplex.1 l.succ =
            k.succ := by
  exact
    (unionProdPairing_eq_core_firstCoordinate_data
      k (P := SSet.prodStdSimplex.pairing.{u} k.castSucc 1)
      (SSet.prodStdSimplex.pairing_castSucc k 1) z).2

/-- The same surjectivity statement before a rank cell is introduced. -/
private theorem standardTypeABoundaryPrismPairing_fst_surjective
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (z : (standardTypeABoundaryPrismPairing.{u} g).II) :
    Function.Surjective
      (((standardTypeABoundaryPrismPairing g).p z).val.cast
        ((standardTypeABoundaryPrismPairing g).isUniquelyCodimOneFace z).dim_eq).simplex.1 := by
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
      change Function.Surjective
        (((SSet.prodStdSimplex.pairing.{u} k.castSucc 1).p z).val.cast
          ((SSet.prodStdSimplex.pairing.{u} k.castSucc 1).isUniquelyCodimOneFace z).dim_eq).simplex.1
      exact unionProdPairing_typeTwo_fst_surjective k z

/-- The corresponding adjacent-index transition before introducing a rank
cell. -/
private theorem standardTypeABoundaryPrismPairing_index_transition
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (z : (standardTypeABoundaryPrismPairing.{u} g).II) :
    ∃ l : Fin (z.val.dim + 1),
      l.castSucc =
          ((standardTypeABoundaryPrismPairing g).isUniquelyCodimOneFace z).index rfl ∧
        (((standardTypeABoundaryPrismPairing g).p z).val.cast
          ((standardTypeABoundaryPrismPairing g).isUniquelyCodimOneFace z).dim_eq).simplex.1 l.castSucc =
            g.i ∧
        (((standardTypeABoundaryPrismPairing g).p z).val.cast
          ((standardTypeABoundaryPrismPairing g).isUniquelyCodimOneFace z).dim_eq).simplex.1 l.succ =
          ⟨g.i.val + 1, by
            have h := g.inner_right
            change g.i.val < g.n at h
            omega⟩ := by
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
      change ∃ l : Fin (z.val.dim + 1),
        l.castSucc =
            ((SSet.prodStdSimplex.pairing.{u} k.castSucc 1).isUniquelyCodimOneFace z).index rfl ∧
          (((SSet.prodStdSimplex.pairing.{u} k.castSucc 1).p z).val.cast
            ((SSet.prodStdSimplex.pairing.{u} k.castSucc 1).isUniquelyCodimOneFace z).dim_eq).simplex.1 l.castSucc =
              k.castSucc ∧
          (((SSet.prodStdSimplex.pairing.{u} k.castSucc 1).p z).val.cast
            ((SSet.prodStdSimplex.pairing.{u} k.castSucc 1).isUniquelyCodimOneFace z).dim_eq).simplex.1 l.succ =
              k.succ
      exact unionProdPairing_typeTwo_index_transition k z

/-- The first coordinate of every actual KuuOS boundary-prism paired simplex
is surjective. -/
theorem standardTypeABoundaryPrismCellPaired_fst_surjective
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j) :
    Function.Surjective
      (standardTypeABoundaryPrismCellPairedNondegenerate g j c).1.1 := by
  change Function.Surjective
    (((standardTypeABoundaryPrismPairing g).p c.s).val.cast
      ((standardTypeABoundaryPrismPairing g).isUniquelyCodimOneFace c.s).dim_eq).simplex.1
  exact standardTypeABoundaryPrismPairing_fst_surjective g c.s

/-- Exact adjacent transition data for an actual KuuOS rank cell. -/
theorem standardTypeABoundaryPrismCellPaired_index_transition
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j) :
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
  change ∃ l : Fin (c.s.val.dim + 1),
    l.castSucc =
        ((standardTypeABoundaryPrismPairing g).isUniquelyCodimOneFace c.s).index rfl ∧
      (((standardTypeABoundaryPrismPairing g).p c.s).val.cast
        ((standardTypeABoundaryPrismPairing g).isUniquelyCodimOneFace c.s).dim_eq).simplex.1 l.castSucc =
          g.i ∧
      (((standardTypeABoundaryPrismPairing g).p c.s).val.cast
        ((standardTypeABoundaryPrismPairing g).isUniquelyCodimOneFace c.s).dim_eq).simplex.1 l.succ =
        ⟨g.i.val + 1, by
          have h := g.inner_right
          change g.i.val < g.n at h
          omega⟩
  exact standardTypeABoundaryPrismPairing_index_transition g c.s

/-! ## Equal-dimensional cells: surjective endomorphism = identity -/

/-- Simplex-category morphism represented by the paired first coordinate. -/
noncomputable def standardTypeABoundaryPrismCellFirstCoordinateOrdinal
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j) :
    ⦋c.dim + 1⦌ ⟶ ⦋g.n⦌ :=
  SSet.stdSimplex.objEquiv
    (standardTypeABoundaryPrismCellPairedNondegenerate g j c).1.1

/-- The represented ordinal morphism is an epimorphism. -/
theorem standardTypeABoundaryPrismCellFirstCoordinateOrdinal_epi
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j) :
    Epi (standardTypeABoundaryPrismCellFirstCoordinateOrdinal g j c) := by
  rw [SimplexCategory.epi_iff_surjective]
  intro y
  obtain ⟨x, hx⟩ :=
    standardTypeABoundaryPrismCellPaired_fst_surjective g j c y
  exact ⟨x, by
    simpa [standardTypeABoundaryPrismCellFirstCoordinateOrdinal] using hx⟩

/-- In the equal-dimensional branch, transport the first-coordinate ordinal
back to the source ordinal. -/
noncomputable def standardTypeABoundaryPrismCellEqualFirstCoordinateEndomorphism
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
    (heq : c.dim + 1 = g.n) :
    ⦋c.dim + 1⦌ ⟶ ⦋c.dim + 1⦌ :=
  standardTypeABoundaryPrismCellFirstCoordinateOrdinal g j c ≫
    eqToHom (congrArg (fun n : ℕ => ⦋n⦌) heq.symm)

/-- Surjective equal-dimensional ordinal endomorphisms are identities. -/
theorem standardTypeABoundaryPrismCellEqualFirstCoordinateEndomorphism_eq_id
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
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
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
    (heq : c.dim + 1 = g.n) : Fin (c.dim + 2) :=
  Fin.cast (by omega) g.i

/-- Pairing rigidity forces the cell horn index to be the transported original
A-index. -/
theorem standardTypeABoundaryPrism_cell_index_eq_generatorIndex_of_equal
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
    (heq : c.dim + 1 = g.n) :
    c.index = standardTypeABoundaryPrismEqualGeneratorIndex g j c heq := by
  rcases standardTypeABoundaryPrismCellPaired_index_transition g j c with
    ⟨l, hl, hfst, _⟩
  have hid :=
    standardTypeABoundaryPrismCellEqualFirstCoordinateEndomorphism_eq_id
      g j c heq
  have happ := SimplexCategory.congr_toOrderHom_apply hid l.castSucc
  have happ' :
      Fin.cast (by omega)
          ((standardTypeABoundaryPrismCellPairedNondegenerate g j c).1.1
            l.castSucc) =
        l.castSucc := by
    simpa [standardTypeABoundaryPrismCellEqualFirstCoordinateEndomorphism,
      standardTypeABoundaryPrismCellFirstCoordinateOrdinal] using happ
  rw [hl] at hfst
  rw [hl, hfst] at happ'
  simpa [standardTypeABoundaryPrismEqualGeneratorIndex] using happ'.symm

/-- Evaluation of the cell first-coordinate map is literal precomposition of
the paired first-coordinate simplex. -/
@[simp]
theorem standardTypeABoundaryPrismCellFirstCoordinateMap_apply
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
    {d : ℕ}
    (t : (Δ[c.dim + 1] : SSet.{u}).obj (op ⦋d⦌))
    (a : Fin (d + 1)) :
    ((standardTypeABoundaryPrismCellFirstCoordinateMap g j c).app
      (op ⦋d⦌) t) a =
      (standardTypeABoundaryPrismCellPairedNondegenerate g j c).1.1 (t a) := by
  change
    ((SSet.yonedaEquiv.symm
      (standardTypeABoundaryPrismCellPairedNondegenerate g j c).1.1).app
      (op ⦋d⦌) t) a = _
  rfl

/-- On every triangle, the equal-dimensional first-coordinate map is canonical
finite-ordinal transport. -/
theorem standardTypeABoundaryPrismCellFirstCoordinateMap_apply_of_equal
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
    (heq : c.dim + 1 = g.n)
    (t : (Δ[c.dim + 1] : SSet.{u}).obj (op ⦋2⦌))
    (a : Fin 3) :
    ((standardTypeABoundaryPrismCellFirstCoordinateMap g j c).app
      (op ⦋2⦌) t) a =
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
  have hpoint' :
      Fin.cast (by omega)
          ((standardTypeABoundaryPrismCellPairedNondegenerate g j c).1.1
            (t a)) =
        t a := by
    simpa [standardTypeABoundaryPrismCellFirstCoordinateOrdinal] using hpoint
  rw [standardTypeABoundaryPrismCellFirstCoordinateMap_apply]
  apply Fin.ext
  simpa using congrArg Fin.val hpoint'

/-- Equal-dimensional cells have exact target scaling equal to their own
standard type-(A) scaling. -/
theorem standardTypeABoundaryPrismCellScaling_eq_standardTypeA_of_equal
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
    (heq : c.dim + 1 = g.n) :
    standardTypeABoundaryPrismCellScaling g j c =
      standardTypeASimplexScaling c.index := by
  apply scaling_eq_of_le_antisymm
  · intro t ht
    change
      (standardTypeASimplexScaling g.i).thin
        ((standardTypeABoundaryPrismCellFirstCoordinateMap g j c).app
          (op ⦋2⦌) t) at ht
    rw [standardTypeABoundaryPrism_cell_index_eq_generatorIndex_of_equal
      g j c heq]
    rcases ht with hmin | hdist
    · left
      rcases hmin with ⟨x, hx⟩ | ⟨x, hx⟩
      · have himg :
            ((standardTypeABoundaryPrismCellFirstCoordinateMap g j c).app
              (op ⦋2⦌) t) 0 =
            ((standardTypeABoundaryPrismCellFirstCoordinateMap g j c).app
              (op ⦋2⦌) t) 1 := by
          rw [← hx]
          simp [SSet.stdSimplex.σ_apply, Fin.predAbove]
        rw [standardTypeABoundaryPrismCellFirstCoordinateMap_apply_of_equal
          g j c heq t 0,
          standardTypeABoundaryPrismCellFirstCoordinateMap_apply_of_equal
            g j c heq t 1] at himg
        apply minimalScaling_stdSimplex_thin_of_zero_eq_one t
        apply Fin.ext
        simpa using congrArg Fin.val himg
      · have himg :
            ((standardTypeABoundaryPrismCellFirstCoordinateMap g j c).app
              (op ⦋2⦌) t) 1 =
            ((standardTypeABoundaryPrismCellFirstCoordinateMap g j c).app
              (op ⦋2⦌) t) 2 := by
          rw [← hx]
          simp [SSet.stdSimplex.σ_apply, Fin.predAbove]
        rw [standardTypeABoundaryPrismCellFirstCoordinateMap_apply_of_equal
          g j c heq t 1,
          standardTypeABoundaryPrismCellFirstCoordinateMap_apply_of_equal
            g j c heq t 2] at himg
        apply minimalScaling_stdSimplex_thin_of_one_eq_two t
        apply Fin.ext
        simpa using congrArg Fin.val himg
    · right
      refine ⟨?_, ?_, ?_⟩
      · have h := hdist.1
        rw [standardTypeABoundaryPrismCellFirstCoordinateMap_apply_of_equal
          g j c heq t 1] at h
        apply Fin.ext
        simpa [standardTypeABoundaryPrismEqualGeneratorIndex] using
          congrArg Fin.val h
      · have h := hdist.2.1
        change
          (((standardTypeABoundaryPrismCellFirstCoordinateMap g j c).app
            (op ⦋2⦌) t) 0).val + 1 = g.i.val at h
        rw [standardTypeABoundaryPrismCellFirstCoordinateMap_apply_of_equal
          g j c heq t 0] at h
        simpa [standardTypeABoundaryPrismEqualGeneratorIndex] using h
      · have h := hdist.2.2
        change
          g.i.val + 1 =
            (((standardTypeABoundaryPrismCellFirstCoordinateMap g j c).app
              (op ⦋2⦌) t) 2).val at h
        rw [standardTypeABoundaryPrismCellFirstCoordinateMap_apply_of_equal
          g j c heq t 2] at h
        simpa [standardTypeABoundaryPrismEqualGeneratorIndex] using h
  · exact standardTypeABoundaryPrismCellACompatible_all g j c

/-- Therefore every equal-dimensional cell is a pure type-(A) cobase change. -/
theorem standardTypeABoundaryPrismCellAPushoutScaling_eq_cellScaling_of_equal
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
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

/-- Dimension-parametric A-plus-horn saturation. -/
private def standardTypeAHornSaturatedScaling
    {d : ℕ}
    (i : Fin (d + 1)) :
    ScaledSimplicialSet (Δ[d] : SSet.{u}) where
  thin := fun t =>
    (standardTypeASimplexScaling i).thin t ∨
      t ∈ (SSet.horn.{u} d i).obj (op ⦋2⦌)
  thin_sigma_zero := by
    intro x
    exact Or.inl ((standardTypeASimplexScaling i).thin_sigma_zero x)
  thin_sigma_one := by
    intro x
    exact Or.inl ((standardTypeASimplexScaling i).thin_sigma_one x)

/-- Intrinsic A-plus-horn saturation on an actual dependent cell carrier. -/
def standardTypeABoundaryPrismCellHornSaturatedAScaling
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j) :
    ScaledSimplicialSet (Δ[c.dim + 1] : SSet.{u}) :=
  standardTypeAHornSaturatedScaling c.index

/-- If the exact target is maximal, then the actual type-(A) cobase-change
scaling is exactly A plus all triangles already in the horn. -/
theorem standardTypeABoundaryPrismCellAPushoutScaling_eq_hornSaturated_of_cell_maximal
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
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
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
    (h3 : c.dim + 1 = 3)
    (s : ScaledSimplicialSet (Δ[c.dim + 1] : SSet.{u})) :
    ScaledSimplicialSet (Δ[3] : SSet.{u}) :=
  Eq.mp
    (congrArg (fun n : ℕ => ScaledSimplicialSet (Δ[n] : SSet.{u})) h3)
    s

private theorem transportScalingToThree_maximal_aux
    {d : ℕ}
    (h3 : d = 3) :
    Eq.mp
        (congrArg (fun n : ℕ => ScaledSimplicialSet (Δ[n] : SSet.{u})) h3)
        (ScaledSimplicialSet.maximal (Δ[d] : SSet.{u})) =
      ScaledSimplicialSet.maximal (Δ[3] : SSet.{u}) := by
  subst d
  rfl

private theorem transportScalingToThree_hornSaturated_aux
    {d : ℕ}
    (i : Fin (d + 1))
    (h3 : d = 3) :
    Eq.mp
        (congrArg (fun n : ℕ => ScaledSimplicialSet (Δ[n] : SSet.{u})) h3)
        (standardTypeAHornSaturatedScaling i) =
      standardTypeAThreeHornSaturatedScaling (Fin.cast (by omega) i) := by
  subst d
  apply scaling_eq_of_le_antisymm
  · intro t ht
    simpa [standardTypeAHornSaturatedScaling,
      standardTypeAThreeHornSaturatedScaling] using ht
  · intro t ht
    simpa [standardTypeAHornSaturatedScaling,
      standardTypeAThreeHornSaturatedScaling] using ht

/-- Transport commutes with maximal scaling. -/
theorem standardTypeABoundaryPrismTransportScalingToThree_maximal
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
    (h3 : c.dim + 1 = 3) :
    standardTypeABoundaryPrismTransportScalingToThree g j c h3
        (ScaledSimplicialSet.maximal (Δ[c.dim + 1] : SSet.{u})) =
      ScaledSimplicialSet.maximal (Δ[3] : SSet.{u}) := by
  exact transportScalingToThree_maximal_aux h3

/-- The transported actual horn-saturated scaling is literally the fixed v1.69
horn-saturated scaling at the transported cell index. -/
theorem standardTypeABoundaryPrismTransportScalingToThree_hornSaturated
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
    (h3 : c.dim + 1 = 3) :
    standardTypeABoundaryPrismTransportScalingToThree g j c h3
        (standardTypeABoundaryPrismCellHornSaturatedAScaling g j c) =
      standardTypeAThreeHornSaturatedScaling
        (standardTypeABoundaryPrismCellIndex3 g j c h3) := by
  simpa [standardTypeABoundaryPrismTransportScalingToThree,
    standardTypeABoundaryPrismCellHornSaturatedAScaling,
    standardTypeABoundaryPrismCellIndex3] using
    (transportScalingToThree_hornSaturated_aux (i := c.index) h3)

/-- In the exceptional `n = 2`, `N = 3` branch the transported A-pushout is
exactly the fixed horn-saturated A scaling. -/
theorem standardTypeABoundaryPrism_generator_two_target_three_APushout_transport
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
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
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j) : Prop where
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
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j) : Prop where
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
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
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
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
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

/-- Every boundary-prism rank cell is pure A, exact A;q12, or exact A;q23. -/
theorem standardTypeABoundaryPrism_cell_complete_AB_classification
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j) :
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

end

end KUOS.DependentOriginationStandardTypeABoundaryPrismCellwiseABClassificationV1_70
