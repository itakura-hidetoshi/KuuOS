import KUOS.DependentOriginationStandardTypeABoundaryPrismRankwiseSimultaneousBPhaseV1_75
import Mathlib.CategoryTheory.Functor.OfSequence
import Mathlib.Data.Nat.Bits

namespace KUOS.DependentOriginationStandardTypeABoundaryPrismRawTransfiniteV1_76

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Limits
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardABCLeibnizCellularComparisonV1_59
open KUOS.DependentOriginationStandardTypeAEndpointPrismPairingV1_60
open KUOS.DependentOriginationStandardTypeABoundaryPrismRelativeCellV1_61
open KUOS.DependentOriginationStandardTypeABoundaryPrismScaledRankFiltrationV1_71
open KUOS.DependentOriginationStandardTypeABoundaryPrismRankwiseABCellularityV1_72
open KUOS.DependentOriginationStandardTypeABoundaryPrismRankwiseSimultaneousAPhaseV1_74
open KUOS.DependentOriginationStandardTypeABoundaryPrismRankwiseSimultaneousBPhaseV1_75

universe u

noncomputable section

set_option backward.isDefEq.respectTransparency false

/-!
# One raw transfinite A/B composition for the boundary prism v1.76

Versions v1.74 and v1.75 give the exact two-phase successor factorization

```text
R_j -- one raw A step --> A_j -- one raw B step --> R_(j+1).
```

This file flattens these two raw phases into the single sequence

```text
R_0, A_0, R_1, A_1, R_2, A_2, ...
```

and packages the boundary-prism inclusion itself as one natural-number
transfinite composition of raw standard A/B/C cellular steps. Equality
transport between the binary parity indexing and the geometric rank objects
is isolated in explicit canonical isomorphisms; cellularity is transported
through those isomorphisms using Mathlib's `RespectsIso` calculus.
-/

/-! ## The exact scaled rank diagram -/

@[reducible]
noncomputable def standardTypeABoundaryPrismScaledRankFunctor
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    ℕ ⥤ ScaledSSet.{u} where
  obj j := standardTypeABoundaryPrismRankStage g j
  map {j k} f := standardTypeABoundaryPrismRankStageHom g (leOfHom f)
  map_id j := by
    apply ScaledSSet.ScaledMap.ext
    rfl
  map_comp {i j k} f h := by
    apply ScaledSSet.ScaledMap.ext
    rfl

@[simp]
theorem standardTypeABoundaryPrismScaledRankFunctor_obj
    (g : StandardTypeAHornAttachmentGeneratorIndex) (j : ℕ) :
    (standardTypeABoundaryPrismScaledRankFunctor g).obj j =
      standardTypeABoundaryPrismRankStage g j := by
  rfl

@[simp]
theorem standardTypeABoundaryPrismScaledRankFunctor_map_succ
    (g : StandardTypeAHornAttachmentGeneratorIndex) (j : ℕ) :
    (standardTypeABoundaryPrismScaledRankFunctor g).map
        (homOfLE (Nat.le_add_right j 1)) =
      standardTypeABoundaryPrismRankStageHom g (Nat.le_succ j) := by
  apply ScaledSSet.ScaledMap.ext
  rfl

@[reducible]
noncomputable def standardTypeABoundaryPrismScaledRankCocone
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    Cocone (standardTypeABoundaryPrismScaledRankFunctor g) :=
  Cocone.mk
    (scaledSimplexCylinder (standardTypeASimplexScaling g.i))
    { app := fun j => standardTypeABoundaryPrismRankStageToCylinder g j
      naturality := by
        intro j k f
        change
          standardTypeABoundaryPrismRankStageHom g (leOfHom f) ≫
              standardTypeABoundaryPrismRankStageToCylinder g k =
            standardTypeABoundaryPrismRankStageToCylinder g j ≫ 𝟙 _
        exact
          (standardTypeABoundaryPrismRankStageHom_toCylinder g
            (leOfHom f)).trans (Category.comp_id _).symm }

/-! ## Finite-rank exhaustion of the cylinder -/

/-- Every simplex of the full prism carrier occurs in one finite rank stage. -/
theorem standardTypeABoundaryPrism_exists_rank_lift
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    {d : SimplexCategoryᵒᵖ}
    (t : (scaledSimplexCylinder
      (standardTypeASimplexScaling g.i)).carrier.obj d) :
    ∃ (j : ℕ)
      (x : (standardTypeABoundaryPrismRankStage g j).carrier.obj d),
      (standardTypeABoundaryPrismRankStageToCylinder g j).map.app d x = t := by
  have ht :
      t ∈
        (⨆ j : ℕ,
          (standardTypeABoundaryPrismRankFunction g).filtration j).obj d := by
    rw [standardTypeABoundaryPrism_iSup_filtration g]
    change t ∈ (Set.univ : Set _)
    exact Set.mem_univ t
  have ht' :
      t ∈
        ⋃ j : ℕ,
          ((standardTypeABoundaryPrismRankFunction g).filtration j).obj d := by
    simpa only [Subfunctor.iSup_obj] using ht
  rcases Set.mem_iUnion.mp ht' with ⟨j, hj⟩
  refine ⟨j, ⟨t, hj⟩, ?_⟩
  rfl

/-- Every thin triangle of the full cylinder lifts to a thin triangle in a
finite ambient-pullback-scaled rank stage. -/
theorem standardTypeABoundaryPrism_exists_thin_rank_lift
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (t : (scaledSimplexCylinder
      (standardTypeASimplexScaling g.i)).carrier.obj (op ⦋2⦌))
    (ht : (scaledSimplexCylinder
      (standardTypeASimplexScaling g.i)).scaling.thin t) :
    ∃ (j : ℕ)
      (x : (standardTypeABoundaryPrismRankStage g j).carrier.obj (op ⦋2⦌)),
      (standardTypeABoundaryPrismRankStage g j).scaling.thin x ∧
      (standardTypeABoundaryPrismRankStageToCylinder g j).map.app
        (op ⦋2⦌) x = t := by
  obtain ⟨j, x, hx⟩ := standardTypeABoundaryPrism_exists_rank_lift g t
  refine ⟨j, x, ?_, hx⟩
  change
    (scaledSimplexCylinder
      (standardTypeASimplexScaling g.i)).scaling.thin
      ((standardTypeABoundaryPrismRankStageToCylinder g j).map.app
        (op ⦋2⦌) x)
  rw [hx]
  exact ht

/-! ## Reuse the ordinary Mathlib relative-cell colimit underneath -/

@[simp]
theorem standardTypeABoundaryPrismRelativeCellComplex_F_obj
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ) :
    (standardTypeABoundaryPrismRelativeCellComplex g).F.obj j =
      ((standardTypeABoundaryPrismRankFunction g).filtration j : SSet.{u}) := by
  rfl

@[simp]
theorem standardTypeABoundaryPrismRelativeCellComplex_incl_app
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ) :
    (standardTypeABoundaryPrismRelativeCellComplex g).incl.app j =
      ((standardTypeABoundaryPrismRankFunction g).filtration j).ι := by
  rfl

noncomputable def standardTypeABoundaryPrismUnderlyingRankCocone
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeABoundaryPrismScaledRankFunctor g)) :
    Cocone (standardTypeABoundaryPrismRelativeCellComplex g).F where
  pt := s.pt.carrier
  ι :=
    { app := fun j => (s.ι.app j).map
      naturality := by
        intro j k f
        have h := congrArg ScaledSSet.ScaledMap.map (s.ι.naturality f)
        change
          SSet.Subcomplex.homOfLE
              ((standardTypeABoundaryPrismRankFunction g).filtration_monotone
                (leOfHom f)) ≫
            (s.ι.app k).map =
              (s.ι.app j).map ≫ 𝟙 _ at h
        change
          SSet.Subcomplex.homOfLE
              ((standardTypeABoundaryPrismRankFunction g).filtration_monotone
                (leOfHom f)) ≫
            (s.ι.app k).map =
              (s.ι.app j).map
        exact h.trans (Category.comp_id _) }

noncomputable def standardTypeABoundaryPrismScaledRankDesc
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeABoundaryPrismScaledRankFunctor g)) :
    scaledSimplexCylinder (standardTypeASimplexScaling g.i) ⟶ s.pt where
  map :=
    (standardTypeABoundaryPrismRelativeCellComplex g).isColimit.desc
      (standardTypeABoundaryPrismUnderlyingRankCocone g s)
  scaled := by
    intro t ht
    obtain ⟨j, x, hxthin, hxt⟩ :=
      standardTypeABoundaryPrism_exists_thin_rank_lift g t ht
    have hs := (s.ι.app j).scaled x hxthin
    change
      s.pt.scaling.thin
        (((standardTypeABoundaryPrismRelativeCellComplex g).isColimit.desc
          (standardTypeABoundaryPrismUnderlyingRankCocone g s)).app
            (op ⦋2⦌) t)
    rw [← hxt]
    change
      s.pt.scaling.thin
        ((((standardTypeABoundaryPrismRelativeCellComplex g).incl.app j ≫
          (standardTypeABoundaryPrismRelativeCellComplex g).isColimit.desc
            (standardTypeABoundaryPrismUnderlyingRankCocone g s))).app
              (op ⦋2⦌) x)
    rw [(standardTypeABoundaryPrismRelativeCellComplex g).isColimit.fac]
    exact hs

noncomputable def standardTypeABoundaryPrismScaledRankCoconeIsColimit
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    IsColimit (standardTypeABoundaryPrismScaledRankCocone g) where
  desc s := standardTypeABoundaryPrismScaledRankDesc g s
  fac s j := by
    apply ScaledSSet.ScaledMap.ext
    change
      (standardTypeABoundaryPrismRelativeCellComplex g).incl.app j ≫
          (standardTypeABoundaryPrismRelativeCellComplex g).isColimit.desc
            (standardTypeABoundaryPrismUnderlyingRankCocone g s) =
        (standardTypeABoundaryPrismUnderlyingRankCocone g s).ι.app j
    exact
      (standardTypeABoundaryPrismRelativeCellComplex g).isColimit.fac
        (standardTypeABoundaryPrismUnderlyingRankCocone g s) j
  uniq s m hm := by
    apply ScaledSSet.ScaledMap.ext
    apply (standardTypeABoundaryPrismRelativeCellComplex g).isColimit.hom_ext
    intro j
    change
      (standardTypeABoundaryPrismRelativeCellComplex g).incl.app j ≫ m.map =
        (standardTypeABoundaryPrismRelativeCellComplex g).incl.app j ≫
          (standardTypeABoundaryPrismRelativeCellComplex g).isColimit.desc
            (standardTypeABoundaryPrismUnderlyingRankCocone g s)
    have hmj := congrArg ScaledSSet.ScaledMap.map (hm j)
    change
      (standardTypeABoundaryPrismRelativeCellComplex g).incl.app j ≫ m.map =
        (standardTypeABoundaryPrismUnderlyingRankCocone g s).ι.app j at hmj
    rw [hmj]
    exact
      ((standardTypeABoundaryPrismRelativeCellComplex g).isColimit.fac
        (standardTypeABoundaryPrismUnderlyingRankCocone g s) j).symm

/-! ## The alternating raw A/B sequence -/

/-- Morphisms in the alternating package are pinned to the quiver owned by the
category itself.  This avoids Lean 4.31 selecting the separate bare `Quiver`
instance when elaborating sequence and cocone APIs. -/
abbrev standardTypeABoundaryPrismScaledCatHom
    (X Y : ScaledSSet.{u}) :=
  @Quiver.Hom ScaledSSet
    (inferInstance : Category (ScaledSSet.{u})).toQuiver X Y

@[simp]
theorem standardTypeABoundaryPrism_bit_false_succ (j : ℕ) :
    Nat.bit false j + 1 = Nat.bit true j := by
  simp [Nat.bit]

@[simp]
theorem standardTypeABoundaryPrism_bit_true_succ (j : ℕ) :
    Nat.bit true j + 1 = Nat.bit false (j + 1) := by
  simp [Nat.bit, Nat.mul_succ, Nat.add_assoc]

def standardTypeABoundaryPrismAlternatingObj
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (n : ℕ) : ScaledSSet.{u} :=
  Nat.bitCasesOn n (fun b j =>
    match b with
    | false => standardTypeABoundaryPrismRankStage g j
    | true => standardTypeABoundaryPrismRankAPhase g j)

@[simp]
theorem standardTypeABoundaryPrismAlternatingObj_bit_false
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ) :
    standardTypeABoundaryPrismAlternatingObj g (Nat.bit false j) =
      standardTypeABoundaryPrismRankStage g j := by
  simp [standardTypeABoundaryPrismAlternatingObj]

@[simp]
theorem standardTypeABoundaryPrismAlternatingObj_bit_true
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ) :
    standardTypeABoundaryPrismAlternatingObj g (Nat.bit true j) =
      standardTypeABoundaryPrismRankAPhase g j := by
  simp [standardTypeABoundaryPrismAlternatingObj]

@[simp]
theorem standardTypeABoundaryPrismAlternatingObj_zero
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeABoundaryPrismAlternatingObj g 0 =
      standardTypeABoundaryPrismRankStage g 0 := by
  simpa using standardTypeABoundaryPrismAlternatingObj_bit_false g 0

/-- Canonical parity isomorphisms. -/
noncomputable def standardTypeABoundaryPrismAlternatingEvenIso
    (g : StandardTypeAHornAttachmentGeneratorIndex) (j : ℕ) :
    standardTypeABoundaryPrismAlternatingObj g (Nat.bit false j) ≅
      standardTypeABoundaryPrismRankStage g j :=
  eqToIso (standardTypeABoundaryPrismAlternatingObj_bit_false g j)

noncomputable def standardTypeABoundaryPrismAlternatingOddIso
    (g : StandardTypeAHornAttachmentGeneratorIndex) (j : ℕ) :
    standardTypeABoundaryPrismAlternatingObj g (Nat.bit true j) ≅
      standardTypeABoundaryPrismRankAPhase g j :=
  eqToIso (standardTypeABoundaryPrismAlternatingObj_bit_true g j)

/-- The arithmetic successor transport followed by the odd parity iso. -/
noncomputable def standardTypeABoundaryPrismAlternatingFalseSuccIso
    (g : StandardTypeAHornAttachmentGeneratorIndex) (j : ℕ) :
    standardTypeABoundaryPrismAlternatingObj g (Nat.bit false j + 1) ≅
      standardTypeABoundaryPrismRankAPhase g j :=
  eqToIso
      (congrArg (standardTypeABoundaryPrismAlternatingObj g)
        (standardTypeABoundaryPrism_bit_false_succ j)) ≪≫
    standardTypeABoundaryPrismAlternatingOddIso g j

/-- The arithmetic successor transport followed by the next even parity iso. -/
noncomputable def standardTypeABoundaryPrismAlternatingTrueSuccIso
    (g : StandardTypeAHornAttachmentGeneratorIndex) (j : ℕ) :
    standardTypeABoundaryPrismAlternatingObj g (Nat.bit true j + 1) ≅
      standardTypeABoundaryPrismRankStage g (j + 1) :=
  eqToIso
      (congrArg (standardTypeABoundaryPrismAlternatingObj g)
        (standardTypeABoundaryPrism_bit_true_succ j)) ≪≫
    standardTypeABoundaryPrismAlternatingEvenIso g (j + 1)

local instance standardTypeABoundaryPrismRawStep_respectsIso :
    (standardABCRawCellularStep :
      MorphismProperty (ScaledSSet.{u})).RespectsIso := by
  unfold standardABCRawCellularStep
  infer_instance

/-- The two geometric raw phases with all parity transport made explicit. -/
noncomputable def standardTypeABoundaryPrismAlternatingStep
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (n : ℕ) :
    standardTypeABoundaryPrismScaledCatHom
      (standardTypeABoundaryPrismAlternatingObj g n)
      (standardTypeABoundaryPrismAlternatingObj g (n + 1)) :=
  Nat.bitCasesOn
    (motive := fun n =>
      standardTypeABoundaryPrismScaledCatHom
        (standardTypeABoundaryPrismAlternatingObj g n)
        (standardTypeABoundaryPrismAlternatingObj g (n + 1)))
    n (fun b j =>
      match b with
      | false =>
          ((standardTypeABoundaryPrismAlternatingEvenIso g j).hom ≫
            standardTypeABoundaryPrismRankStageToAPhase g j) ≫
              (standardTypeABoundaryPrismAlternatingFalseSuccIso g j).inv
      | true =>
          ((standardTypeABoundaryPrismAlternatingOddIso g j).hom ≫
            standardTypeABoundaryPrismRankAPhaseToSucc g j) ≫
              (standardTypeABoundaryPrismAlternatingTrueSuccIso g j).inv)

@[simp]
theorem standardTypeABoundaryPrismAlternatingStep_bit_false
    (g : StandardTypeAHornAttachmentGeneratorIndex) (j : ℕ) :
    standardTypeABoundaryPrismAlternatingStep g (Nat.bit false j) =
      ((standardTypeABoundaryPrismAlternatingEvenIso g j).hom ≫
        standardTypeABoundaryPrismRankStageToAPhase g j) ≫
          (standardTypeABoundaryPrismAlternatingFalseSuccIso g j).inv := by
  simp [standardTypeABoundaryPrismAlternatingStep]

@[simp]
theorem standardTypeABoundaryPrismAlternatingStep_bit_true
    (g : StandardTypeAHornAttachmentGeneratorIndex) (j : ℕ) :
    standardTypeABoundaryPrismAlternatingStep g (Nat.bit true j) =
      ((standardTypeABoundaryPrismAlternatingOddIso g j).hom ≫
        standardTypeABoundaryPrismRankAPhaseToSucc g j) ≫
          (standardTypeABoundaryPrismAlternatingTrueSuccIso g j).inv := by
  simp [standardTypeABoundaryPrismAlternatingStep]

/-- Every flattened successor is raw cellular; only source/target isomorphisms
are added to the literal v1.74/v1.75 raw A/B maps. -/
theorem standardTypeABoundaryPrismAlternatingStep_mem_rawCellular
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (n : ℕ) :
    standardABCRawCellularStep
      (standardTypeABoundaryPrismAlternatingStep g n) := by
  cases n using Nat.bitCasesOn with
  | bit b j =>
      cases b with
      | false =>
          rw [standardTypeABoundaryPrismAlternatingStep_bit_false]
          apply MorphismProperty.RespectsIso.postcomp
          apply MorphismProperty.RespectsIso.precomp
          exact standardTypeABoundaryPrismRankStageToAPhase_mem_rawCellular g j
      | true =>
          rw [standardTypeABoundaryPrismAlternatingStep_bit_true]
          apply MorphismProperty.RespectsIso.postcomp
          apply MorphismProperty.RespectsIso.precomp
          exact standardTypeABoundaryPrismRankAPhaseToSucc_mem_rawCellular g j

@[reducible]
noncomputable def standardTypeABoundaryPrismAlternatingFunctor
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    ℕ ⥤ ScaledSSet.{u} :=
  Functor.ofSequence (standardTypeABoundaryPrismAlternatingStep g)

@[simp]
theorem standardTypeABoundaryPrismAlternatingFunctor_obj
    (g : StandardTypeAHornAttachmentGeneratorIndex) (n : ℕ) :
    (standardTypeABoundaryPrismAlternatingFunctor g).obj n =
      standardTypeABoundaryPrismAlternatingObj g n := by
  rfl

@[simp]
theorem standardTypeABoundaryPrismAlternatingFunctor_map_succ
    (g : StandardTypeAHornAttachmentGeneratorIndex) (n : ℕ) :
    (standardTypeABoundaryPrismAlternatingFunctor g).map
        (homOfLE (Nat.le_add_right n 1)) =
      standardTypeABoundaryPrismAlternatingStep g n := by
  unfold standardTypeABoundaryPrismAlternatingFunctor
  exact Functor.ofSequence_map_homOfLE_succ
    (standardTypeABoundaryPrismAlternatingStep g) n

/-! ## A cocone of the alternating diagram to the full cylinder -/

noncomputable def standardTypeABoundaryPrismAlternatingToCylinder
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (n : ℕ) :
    standardTypeABoundaryPrismScaledCatHom
      (standardTypeABoundaryPrismAlternatingObj g n)
      (scaledSimplexCylinder (standardTypeASimplexScaling g.i)) :=
  Nat.bitCasesOn
    (motive := fun n =>
      standardTypeABoundaryPrismScaledCatHom
        (standardTypeABoundaryPrismAlternatingObj g n)
        (scaledSimplexCylinder (standardTypeASimplexScaling g.i)))
    n (fun b j =>
      match b with
      | false =>
          (standardTypeABoundaryPrismAlternatingEvenIso g j).hom ≫
            standardTypeABoundaryPrismRankStageToCylinder g j
      | true =>
          ((standardTypeABoundaryPrismAlternatingOddIso g j).hom ≫
            standardTypeABoundaryPrismRankAPhaseToSucc g j) ≫
              standardTypeABoundaryPrismRankStageToCylinder g (j + 1))

@[simp]
theorem standardTypeABoundaryPrismAlternatingToCylinder_bit_false
    (g : StandardTypeAHornAttachmentGeneratorIndex) (j : ℕ) :
    standardTypeABoundaryPrismAlternatingToCylinder g (Nat.bit false j) =
      (standardTypeABoundaryPrismAlternatingEvenIso g j).hom ≫
        standardTypeABoundaryPrismRankStageToCylinder g j := by
  simp [standardTypeABoundaryPrismAlternatingToCylinder]

@[simp]
theorem standardTypeABoundaryPrismAlternatingToCylinder_bit_true
    (g : StandardTypeAHornAttachmentGeneratorIndex) (j : ℕ) :
    standardTypeABoundaryPrismAlternatingToCylinder g (Nat.bit true j) =
      ((standardTypeABoundaryPrismAlternatingOddIso g j).hom ≫
        standardTypeABoundaryPrismRankAPhaseToSucc g j) ≫
          standardTypeABoundaryPrismRankStageToCylinder g (j + 1) := by
  simp [standardTypeABoundaryPrismAlternatingToCylinder]

/-- Equality of sequence indices transports the cylinder leg canonically. -/
theorem standardTypeABoundaryPrismAlternatingToCylinder_transport
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    {n m : ℕ} (h : n = m) :
    (eqToIso
      (congrArg (standardTypeABoundaryPrismAlternatingObj g) h)).inv ≫
        standardTypeABoundaryPrismAlternatingToCylinder g n =
      standardTypeABoundaryPrismAlternatingToCylinder g m := by
  subst m
  simp

/-- The target transport after an A phase cancels against the odd parity
identification before mapping to the cylinder. -/
theorem standardTypeABoundaryPrismAlternatingFalseSucc_toCylinder
    (g : StandardTypeAHornAttachmentGeneratorIndex) (j : ℕ) :
    (standardTypeABoundaryPrismAlternatingFalseSuccIso g j).inv ≫
        standardTypeABoundaryPrismAlternatingToCylinder g
          (Nat.bit false j + 1) =
      standardTypeABoundaryPrismRankAPhaseToSucc g j ≫
        standardTypeABoundaryPrismRankStageToCylinder g (j + 1) := by
  unfold standardTypeABoundaryPrismAlternatingFalseSuccIso
  rw [Iso.trans_inv, Category.assoc,
    standardTypeABoundaryPrismAlternatingToCylinder_transport g
      (standardTypeABoundaryPrism_bit_false_succ j),
    standardTypeABoundaryPrismAlternatingToCylinder_bit_true]
  simp [Category.assoc]

/-- The target transport after a B phase cancels against the next even parity
identification. -/
theorem standardTypeABoundaryPrismAlternatingTrueSucc_toCylinder
    (g : StandardTypeAHornAttachmentGeneratorIndex) (j : ℕ) :
    (standardTypeABoundaryPrismAlternatingTrueSuccIso g j).inv ≫
        standardTypeABoundaryPrismAlternatingToCylinder g
          (Nat.bit true j + 1) =
      standardTypeABoundaryPrismRankStageToCylinder g (j + 1) := by
  unfold standardTypeABoundaryPrismAlternatingTrueSuccIso
  rw [Iso.trans_inv, Category.assoc,
    standardTypeABoundaryPrismAlternatingToCylinder_transport g
      (standardTypeABoundaryPrism_bit_true_succ j),
    standardTypeABoundaryPrismAlternatingToCylinder_bit_false]
  simp

/-- Consecutive alternating maps are compatible with the common cylinder map. -/
theorem standardTypeABoundaryPrismAlternatingStep_toCylinder
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (n : ℕ) :
    standardTypeABoundaryPrismAlternatingStep g n ≫
        standardTypeABoundaryPrismAlternatingToCylinder g (n + 1) =
      standardTypeABoundaryPrismAlternatingToCylinder g n := by
  cases n using Nat.bitCasesOn with
  | bit b j =>
      cases b with
      | false =>
          rw [standardTypeABoundaryPrismAlternatingStep_bit_false,
            standardTypeABoundaryPrismAlternatingToCylinder_bit_false]
          calc
            (((standardTypeABoundaryPrismAlternatingEvenIso g j).hom ≫
                standardTypeABoundaryPrismRankStageToAPhase g j) ≫
              (standardTypeABoundaryPrismAlternatingFalseSuccIso g j).inv) ≫
                standardTypeABoundaryPrismAlternatingToCylinder g
                  (Nat.bit false j + 1) =
              (standardTypeABoundaryPrismAlternatingEvenIso g j).hom ≫
                ((standardTypeABoundaryPrismRankStageToAPhase g j ≫
                    standardTypeABoundaryPrismRankAPhaseToSucc g j) ≫
                  standardTypeABoundaryPrismRankStageToCylinder g (j + 1)) := by
                    simp only [Category.assoc,
                      standardTypeABoundaryPrismAlternatingFalseSucc_toCylinder]
            _ = (standardTypeABoundaryPrismAlternatingEvenIso g j).hom ≫
                  (standardTypeABoundaryPrismRankStageHom g (Nat.le_succ j) ≫
                    standardTypeABoundaryPrismRankStageToCylinder g (j + 1)) := by
                      rw [standardTypeABoundaryPrismRankStep_factor_A_residual]
            _ = (standardTypeABoundaryPrismAlternatingEvenIso g j).hom ≫
                  standardTypeABoundaryPrismRankStageToCylinder g j := by
                    rw [standardTypeABoundaryPrismRankStageHom_toCylinder]
      | true =>
          rw [standardTypeABoundaryPrismAlternatingStep_bit_true,
            standardTypeABoundaryPrismAlternatingToCylinder_bit_true]
          simp only [Category.assoc,
            standardTypeABoundaryPrismAlternatingTrueSucc_toCylinder]

/-- Successor naturality is kept as a named theorem so the alternating cocone
stores only an opaque theorem reference rather than a large anonymous proof. -/
theorem standardTypeABoundaryPrismAlternatingToCylinder_succ_naturality
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (n : ℕ) :
    (standardTypeABoundaryPrismAlternatingFunctor g).map
          (homOfLE (Nat.le_add_right n 1)) ≫
        standardTypeABoundaryPrismAlternatingToCylinder g (n + 1) =
      standardTypeABoundaryPrismAlternatingToCylinder g n ≫
        ((Functor.const ℕ).obj
          (scaledSimplexCylinder (standardTypeASimplexScaling g.i))).map
            (homOfLE (Nat.le_add_right n 1)) := by
  rw [standardTypeABoundaryPrismAlternatingFunctor_map_succ,
    Functor.const_obj_map, Category.comp_id]
  exact standardTypeABoundaryPrismAlternatingStep_toCylinder g n

@[reducible]
noncomputable def standardTypeABoundaryPrismAlternatingCocone
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    Cocone (standardTypeABoundaryPrismAlternatingFunctor g) :=
  Cocone.mk
    (scaledSimplexCylinder (standardTypeASimplexScaling g.i))
    (NatTrans.ofSequence
      (F := standardTypeABoundaryPrismAlternatingFunctor g)
      (G := (Functor.const ℕ).obj
        (scaledSimplexCylinder (standardTypeASimplexScaling g.i)))
      (standardTypeABoundaryPrismAlternatingToCylinder g)
      (standardTypeABoundaryPrismAlternatingToCylinder_succ_naturality g))

@[simp]
theorem standardTypeABoundaryPrismAlternatingCocone_ι_app
    (g : StandardTypeAHornAttachmentGeneratorIndex) (n : ℕ) :
    (standardTypeABoundaryPrismAlternatingCocone g).ι.app n =
      standardTypeABoundaryPrismAlternatingToCylinder g n := by
  rfl

/-! ## Restrict an alternating cocone to its even rank stages -/

noncomputable def standardTypeABoundaryPrismAlternatingEvenLeg
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeABoundaryPrismAlternatingFunctor g))
    (j : ℕ) :
    standardTypeABoundaryPrismScaledCatHom
      (standardTypeABoundaryPrismRankStage g j) s.pt :=
  (standardTypeABoundaryPrismAlternatingEvenIso g j).inv ≫
    s.ι.app (Nat.bit false j)

noncomputable def standardTypeABoundaryPrismAlternatingOddLeg
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeABoundaryPrismAlternatingFunctor g))
    (j : ℕ) :
    standardTypeABoundaryPrismScaledCatHom
      (standardTypeABoundaryPrismRankAPhase g j) s.pt :=
  (standardTypeABoundaryPrismAlternatingOddIso g j).inv ≫
    s.ι.app (Nat.bit true j)

/-- Successor naturality for an arbitrary cocone on the flattened sequence. -/
theorem standardTypeABoundaryPrismAlternatingCocone_step
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeABoundaryPrismAlternatingFunctor g))
    (n : ℕ) :
    standardTypeABoundaryPrismAlternatingStep g n ≫ s.ι.app (n + 1) =
      s.ι.app n := by
  have h := s.w (homOfLE (Nat.le_add_right n 1))
  simpa only [standardTypeABoundaryPrismAlternatingFunctor_map_succ,
    Functor.const_obj_map, Category.comp_id] using h

/-- Equality of sequence indices transports every cocone leg canonically. -/
theorem standardTypeABoundaryPrismAlternatingCocone_transport
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeABoundaryPrismAlternatingFunctor g))
    {n m : ℕ} (h : n = m) :
    (eqToIso
      (congrArg (standardTypeABoundaryPrismAlternatingObj g) h)).inv ≫
        s.ι.app n =
      s.ι.app m := by
  subst m
  simp

/-- The two descriptions of the post-A stage leg agree after arithmetic
normalization of the binary index. -/
theorem standardTypeABoundaryPrismAlternatingFalseSucc_leg
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeABoundaryPrismAlternatingFunctor g))
    (j : ℕ) :
    (standardTypeABoundaryPrismAlternatingFalseSuccIso g j).inv ≫
        s.ι.app (Nat.bit false j + 1) =
      (standardTypeABoundaryPrismAlternatingOddIso g j).inv ≫
        s.ι.app (Nat.bit true j) := by
  unfold standardTypeABoundaryPrismAlternatingFalseSuccIso
  rw [Iso.trans_inv, Category.assoc,
    standardTypeABoundaryPrismAlternatingCocone_transport g s
      (standardTypeABoundaryPrism_bit_false_succ j)]

/-- Likewise the post-B leg is the next even rank leg. -/
theorem standardTypeABoundaryPrismAlternatingTrueSucc_leg
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeABoundaryPrismAlternatingFunctor g))
    (j : ℕ) :
    (standardTypeABoundaryPrismAlternatingTrueSuccIso g j).inv ≫
        s.ι.app (Nat.bit true j + 1) =
      (standardTypeABoundaryPrismAlternatingEvenIso g (j + 1)).inv ≫
        s.ι.app (Nat.bit false (j + 1)) := by
  unfold standardTypeABoundaryPrismAlternatingTrueSuccIso
  rw [Iso.trans_inv, Category.assoc,
    standardTypeABoundaryPrismAlternatingCocone_transport g s
      (standardTypeABoundaryPrism_bit_true_succ j)]

/-- The A-step cocone equation after removing the canonical parity isos. -/
theorem standardTypeABoundaryPrismAlternatingA_leg_eq
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeABoundaryPrismAlternatingFunctor g))
    (j : ℕ) :
    standardTypeABoundaryPrismRankStageToAPhase g j ≫
        standardTypeABoundaryPrismAlternatingOddLeg g s j =
      standardTypeABoundaryPrismAlternatingEvenLeg g s j := by
  have h0 :=
    standardTypeABoundaryPrismAlternatingCocone_step g s (Nat.bit false j)
  rw [standardTypeABoundaryPrismAlternatingStep_bit_false] at h0
  have h1 :
      (((standardTypeABoundaryPrismAlternatingEvenIso g j).hom ≫
          standardTypeABoundaryPrismRankStageToAPhase g j) ≫
        (standardTypeABoundaryPrismAlternatingOddIso g j).inv) ≫
          s.ι.app (Nat.bit true j) =
        s.ι.app (Nat.bit false j) := by
    calc
      (((standardTypeABoundaryPrismAlternatingEvenIso g j).hom ≫
          standardTypeABoundaryPrismRankStageToAPhase g j) ≫
        (standardTypeABoundaryPrismAlternatingOddIso g j).inv) ≫
          s.ι.app (Nat.bit true j) =
        ((standardTypeABoundaryPrismAlternatingEvenIso g j).hom ≫
          standardTypeABoundaryPrismRankStageToAPhase g j) ≫
            ((standardTypeABoundaryPrismAlternatingOddIso g j).inv ≫
              s.ι.app (Nat.bit true j)) := by simp only [Category.assoc]
      _ = ((standardTypeABoundaryPrismAlternatingEvenIso g j).hom ≫
          standardTypeABoundaryPrismRankStageToAPhase g j) ≫
            ((standardTypeABoundaryPrismAlternatingFalseSuccIso g j).inv ≫
              s.ι.app (Nat.bit false j + 1)) := by
                exact congrArg
                  (fun q =>
                    ((standardTypeABoundaryPrismAlternatingEvenIso g j).hom ≫
                      standardTypeABoundaryPrismRankStageToAPhase g j) ≫ q)
                  (standardTypeABoundaryPrismAlternatingFalseSucc_leg g s j).symm
      _ = (((standardTypeABoundaryPrismAlternatingEvenIso g j).hom ≫
          standardTypeABoundaryPrismRankStageToAPhase g j) ≫
            (standardTypeABoundaryPrismAlternatingFalseSuccIso g j).inv) ≫
              s.ι.app (Nat.bit false j + 1) := by simp only [Category.assoc]
      _ = s.ι.app (Nat.bit false j) := h0
  change
    standardTypeABoundaryPrismRankStageToAPhase g j ≫
        ((standardTypeABoundaryPrismAlternatingOddIso g j).inv ≫
          s.ι.app (Nat.bit true j)) =
      (standardTypeABoundaryPrismAlternatingEvenIso g j).inv ≫
        s.ι.app (Nat.bit false j)
  calc
    standardTypeABoundaryPrismRankStageToAPhase g j ≫
        ((standardTypeABoundaryPrismAlternatingOddIso g j).inv ≫
          s.ι.app (Nat.bit true j)) =
      (standardTypeABoundaryPrismAlternatingEvenIso g j).inv ≫
        ((((standardTypeABoundaryPrismAlternatingEvenIso g j).hom ≫
            standardTypeABoundaryPrismRankStageToAPhase g j) ≫
          (standardTypeABoundaryPrismAlternatingOddIso g j).inv) ≫
            s.ι.app (Nat.bit true j)) := by simp [Category.assoc]
    _ = (standardTypeABoundaryPrismAlternatingEvenIso g j).inv ≫
          s.ι.app (Nat.bit false j) :=
      congrArg
        (fun q => (standardTypeABoundaryPrismAlternatingEvenIso g j).inv ≫ q)
        h1

/-- The B-step cocone equation after removing the canonical parity isos. -/
theorem standardTypeABoundaryPrismAlternatingOddLeg_eq
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeABoundaryPrismAlternatingFunctor g))
    (j : ℕ) :
    standardTypeABoundaryPrismRankAPhaseToSucc g j ≫
        standardTypeABoundaryPrismAlternatingEvenLeg g s (j + 1) =
      standardTypeABoundaryPrismAlternatingOddLeg g s j := by
  have h0 :=
    standardTypeABoundaryPrismAlternatingCocone_step g s (Nat.bit true j)
  rw [standardTypeABoundaryPrismAlternatingStep_bit_true] at h0
  have h1 :
      (((standardTypeABoundaryPrismAlternatingOddIso g j).hom ≫
          standardTypeABoundaryPrismRankAPhaseToSucc g j) ≫
        (standardTypeABoundaryPrismAlternatingEvenIso g (j + 1)).inv) ≫
          s.ι.app (Nat.bit false (j + 1)) =
        s.ι.app (Nat.bit true j) := by
    calc
      (((standardTypeABoundaryPrismAlternatingOddIso g j).hom ≫
          standardTypeABoundaryPrismRankAPhaseToSucc g j) ≫
        (standardTypeABoundaryPrismAlternatingEvenIso g (j + 1)).inv) ≫
          s.ι.app (Nat.bit false (j + 1)) =
        ((standardTypeABoundaryPrismAlternatingOddIso g j).hom ≫
          standardTypeABoundaryPrismRankAPhaseToSucc g j) ≫
            ((standardTypeABoundaryPrismAlternatingEvenIso g (j + 1)).inv ≫
              s.ι.app (Nat.bit false (j + 1))) := by simp only [Category.assoc]
      _ = ((standardTypeABoundaryPrismAlternatingOddIso g j).hom ≫
          standardTypeABoundaryPrismRankAPhaseToSucc g j) ≫
            ((standardTypeABoundaryPrismAlternatingTrueSuccIso g j).inv ≫
              s.ι.app (Nat.bit true j + 1)) := by
                exact congrArg
                  (fun q =>
                    ((standardTypeABoundaryPrismAlternatingOddIso g j).hom ≫
                      standardTypeABoundaryPrismRankAPhaseToSucc g j) ≫ q)
                  (standardTypeABoundaryPrismAlternatingTrueSucc_leg g s j).symm
      _ = (((standardTypeABoundaryPrismAlternatingOddIso g j).hom ≫
          standardTypeABoundaryPrismRankAPhaseToSucc g j) ≫
            (standardTypeABoundaryPrismAlternatingTrueSuccIso g j).inv) ≫
              s.ι.app (Nat.bit true j + 1) := by simp only [Category.assoc]
      _ = s.ι.app (Nat.bit true j) := h0
  change
    standardTypeABoundaryPrismRankAPhaseToSucc g j ≫
        ((standardTypeABoundaryPrismAlternatingEvenIso g (j + 1)).inv ≫
          s.ι.app (Nat.bit false (j + 1))) =
      (standardTypeABoundaryPrismAlternatingOddIso g j).inv ≫
        s.ι.app (Nat.bit true j)
  calc
    standardTypeABoundaryPrismRankAPhaseToSucc g j ≫
        ((standardTypeABoundaryPrismAlternatingEvenIso g (j + 1)).inv ≫
          s.ι.app (Nat.bit false (j + 1))) =
      (standardTypeABoundaryPrismAlternatingOddIso g j).inv ≫
        ((((standardTypeABoundaryPrismAlternatingOddIso g j).hom ≫
            standardTypeABoundaryPrismRankAPhaseToSucc g j) ≫
          (standardTypeABoundaryPrismAlternatingEvenIso g (j + 1)).inv) ≫
            s.ι.app (Nat.bit false (j + 1))) := by simp [Category.assoc]
    _ = (standardTypeABoundaryPrismAlternatingOddIso g j).inv ≫
          s.ι.app (Nat.bit true j) :=
      congrArg
        (fun q => (standardTypeABoundaryPrismAlternatingOddIso g j).inv ≫ q)
        h1

/-- The two raw equations recover the exact rank successor equation. -/
theorem standardTypeABoundaryPrismAlternatingEvenLeg_succ
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeABoundaryPrismAlternatingFunctor g))
    (j : ℕ) :
    standardTypeABoundaryPrismRankStageHom g (Nat.le_succ j) ≫
        standardTypeABoundaryPrismAlternatingEvenLeg g s (j + 1) =
      standardTypeABoundaryPrismAlternatingEvenLeg g s j := by
  rw [← standardTypeABoundaryPrismRankStep_factor_A_residual g j]
  rw [Category.assoc,
    standardTypeABoundaryPrismAlternatingOddLeg_eq g s j,
    standardTypeABoundaryPrismAlternatingA_leg_eq g s j]

/-- The rank subsequence inherits its successor equation as a named naturality
law, keeping the reconstructed rank cocone kernel-small. -/
theorem standardTypeABoundaryPrismAlternatingEvenLeg_succ_naturality
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeABoundaryPrismAlternatingFunctor g))
    (j : ℕ) :
    (standardTypeABoundaryPrismScaledRankFunctor g).map
          (homOfLE (Nat.le_add_right j 1)) ≫
        standardTypeABoundaryPrismAlternatingEvenLeg g s (j + 1) =
      standardTypeABoundaryPrismAlternatingEvenLeg g s j ≫
        ((Functor.const ℕ).obj s.pt).map
          (homOfLE (Nat.le_add_right j 1)) := by
  rw [standardTypeABoundaryPrismScaledRankFunctor_map_succ,
    Functor.const_obj_map, Category.comp_id]
  exact standardTypeABoundaryPrismAlternatingEvenLeg_succ g s j

@[reducible]
noncomputable def standardTypeABoundaryPrismRankCoconeOfAlternatingCocone
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeABoundaryPrismAlternatingFunctor g)) :
    Cocone (standardTypeABoundaryPrismScaledRankFunctor g) :=
  Cocone.mk s.pt
    (NatTrans.ofSequence
      (F := standardTypeABoundaryPrismScaledRankFunctor g)
      (G := (Functor.const ℕ).obj s.pt)
      (standardTypeABoundaryPrismAlternatingEvenLeg g s)
      (standardTypeABoundaryPrismAlternatingEvenLeg_succ_naturality g s))

/-! ## Inserting the A-phases does not change the colimit -/

@[reducible]
noncomputable def standardTypeABoundaryPrismAlternatingDesc
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeABoundaryPrismAlternatingFunctor g)) :
    standardTypeABoundaryPrismScaledCatHom
      (scaledSimplexCylinder (standardTypeASimplexScaling g.i)) s.pt :=
  (standardTypeABoundaryPrismScaledRankCoconeIsColimit g).desc
    (standardTypeABoundaryPrismRankCoconeOfAlternatingCocone g s)

noncomputable def standardTypeABoundaryPrismAlternatingCoconeIsColimit
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    IsColimit (standardTypeABoundaryPrismAlternatingCocone g) where
  desc s := standardTypeABoundaryPrismAlternatingDesc g s
  fac s n := by
    cases n using Nat.bitCasesOn with
    | bit b j =>
        cases b with
        | false =>
            have hr :=
              (standardTypeABoundaryPrismScaledRankCoconeIsColimit g).fac
                (standardTypeABoundaryPrismRankCoconeOfAlternatingCocone g s) j
            have hr' :
                standardTypeABoundaryPrismRankStageToCylinder g j ≫
                    standardTypeABoundaryPrismAlternatingDesc g s =
                  standardTypeABoundaryPrismAlternatingEvenLeg g s j := by
              simpa [standardTypeABoundaryPrismScaledRankCocone,
                standardTypeABoundaryPrismAlternatingDesc,
                standardTypeABoundaryPrismRankCoconeOfAlternatingCocone] using hr
            change
              standardTypeABoundaryPrismAlternatingToCylinder g
                    (Nat.bit false j) ≫
                  standardTypeABoundaryPrismAlternatingDesc g s =
                s.ι.app (Nat.bit false j)
            rw [standardTypeABoundaryPrismAlternatingToCylinder_bit_false]
            calc
              ((standardTypeABoundaryPrismAlternatingEvenIso g j).hom ≫
                  standardTypeABoundaryPrismRankStageToCylinder g j) ≫
                    standardTypeABoundaryPrismAlternatingDesc g s =
                (standardTypeABoundaryPrismAlternatingEvenIso g j).hom ≫
                  (standardTypeABoundaryPrismRankStageToCylinder g j ≫
                    standardTypeABoundaryPrismAlternatingDesc g s) := by
                      simp only [Category.assoc]
              _ = (standardTypeABoundaryPrismAlternatingEvenIso g j).hom ≫
                    standardTypeABoundaryPrismAlternatingEvenLeg g s j := by
                      rw [hr']
              _ = s.ι.app (Nat.bit false j) := by
                    simp [standardTypeABoundaryPrismAlternatingEvenLeg]
        | true =>
            have hr :=
              (standardTypeABoundaryPrismScaledRankCoconeIsColimit g).fac
                (standardTypeABoundaryPrismRankCoconeOfAlternatingCocone g s) (j + 1)
            have hr' :
                standardTypeABoundaryPrismRankStageToCylinder g (j + 1) ≫
                    standardTypeABoundaryPrismAlternatingDesc g s =
                  standardTypeABoundaryPrismAlternatingEvenLeg g s (j + 1) := by
              simpa [standardTypeABoundaryPrismScaledRankCocone,
                standardTypeABoundaryPrismAlternatingDesc,
                standardTypeABoundaryPrismRankCoconeOfAlternatingCocone] using hr
            change
              standardTypeABoundaryPrismAlternatingToCylinder g
                    (Nat.bit true j) ≫
                  standardTypeABoundaryPrismAlternatingDesc g s =
                s.ι.app (Nat.bit true j)
            rw [standardTypeABoundaryPrismAlternatingToCylinder_bit_true]
            calc
              (((standardTypeABoundaryPrismAlternatingOddIso g j).hom ≫
                  standardTypeABoundaryPrismRankAPhaseToSucc g j) ≫
                standardTypeABoundaryPrismRankStageToCylinder g (j + 1)) ≫
                  standardTypeABoundaryPrismAlternatingDesc g s =
                ((standardTypeABoundaryPrismAlternatingOddIso g j).hom ≫
                  standardTypeABoundaryPrismRankAPhaseToSucc g j) ≫
                    (standardTypeABoundaryPrismRankStageToCylinder g (j + 1) ≫
                      standardTypeABoundaryPrismAlternatingDesc g s) := by
                        simp only [Category.assoc]
              _ = ((standardTypeABoundaryPrismAlternatingOddIso g j).hom ≫
                    standardTypeABoundaryPrismRankAPhaseToSucc g j) ≫
                      standardTypeABoundaryPrismAlternatingEvenLeg g s (j + 1) := by
                        rw [hr']
              _ = (standardTypeABoundaryPrismAlternatingOddIso g j).hom ≫
                    (standardTypeABoundaryPrismRankAPhaseToSucc g j ≫
                      standardTypeABoundaryPrismAlternatingEvenLeg g s (j + 1)) := by
                        simp only [Category.assoc]
              _ = (standardTypeABoundaryPrismAlternatingOddIso g j).hom ≫
                    standardTypeABoundaryPrismAlternatingOddLeg g s j := by
                      rw [standardTypeABoundaryPrismAlternatingOddLeg_eq]
              _ = s.ι.app (Nat.bit true j) := by
                    simp [standardTypeABoundaryPrismAlternatingOddLeg]
  uniq s m hm := by
    apply (standardTypeABoundaryPrismScaledRankCoconeIsColimit g).hom_ext
    intro j
    have heven := hm (Nat.bit false j)
    change
      standardTypeABoundaryPrismAlternatingToCylinder g (Nat.bit false j) ≫ m =
        s.ι.app (Nat.bit false j) at heven
    rw [standardTypeABoundaryPrismAlternatingToCylinder_bit_false] at heven
    have hdesc :=
      (standardTypeABoundaryPrismScaledRankCoconeIsColimit g).fac
        (standardTypeABoundaryPrismRankCoconeOfAlternatingCocone g s) j
    have heven' :
        standardTypeABoundaryPrismRankStageToCylinder g j ≫ m =
          standardTypeABoundaryPrismAlternatingEvenLeg g s j := by
      have h :=
        congrArg
          (fun q => (standardTypeABoundaryPrismAlternatingEvenIso g j).inv ≫ q)
          heven
      simpa [standardTypeABoundaryPrismAlternatingEvenLeg,
        Category.assoc] using h
    have hdesc' :
        standardTypeABoundaryPrismRankStageToCylinder g j ≫
            standardTypeABoundaryPrismAlternatingDesc g s =
          standardTypeABoundaryPrismAlternatingEvenLeg g s j := by
      simpa [standardTypeABoundaryPrismScaledRankCocone,
        standardTypeABoundaryPrismAlternatingDesc,
        standardTypeABoundaryPrismRankCoconeOfAlternatingCocone] using hdesc
    exact heven'.trans hdesc'.symm

/-! ## An explicit rank-zero scaled isomorphism -/

noncomputable def standardTypeABoundaryPrismRankStageZeroToBoundary
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeABoundaryPrismRankStage g 0 ⟶
      standardTypeABoundaryPrism g := by
  let hle :
      (standardTypeABoundaryPrismRankFunction g).filtration 0 ≤
        standardTypeABoundaryPrismSubcomplex g := by
    rw [standardTypeABoundaryPrism_filtration_zero]
  refine
    { map := SSet.Subcomplex.homOfLE hle
      scaled := ?_ }
  intro t ht
  change
    (scaledSimplexCylinder
      (standardTypeASimplexScaling g.i)).scaling.thin
      (((standardTypeABoundaryPrismRankFunction g).filtration 0).ι.app
        (op ⦋2⦌) t) at ht
  change
    (scaledSimplexCylinder
      (standardTypeASimplexScaling g.i)).scaling.thin
      ((standardTypeABoundaryPrismSubcomplex g).ι.app (op ⦋2⦌)
        ((SSet.Subcomplex.homOfLE hle).app (op ⦋2⦌) t))
  rw [← NatTrans.comp_app_apply]
  rw [SSet.Subcomplex.homOfLE_ι]
  exact ht

noncomputable def standardTypeABoundaryPrismBoundaryToRankStageZero
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeABoundaryPrism g ⟶
      standardTypeABoundaryPrismRankStage g 0 := by
  let hle :
      standardTypeABoundaryPrismSubcomplex g ≤
        (standardTypeABoundaryPrismRankFunction g).filtration 0 := by
    rw [standardTypeABoundaryPrism_filtration_zero]
  refine
    { map := SSet.Subcomplex.homOfLE hle
      scaled := ?_ }
  intro t ht
  change
    (scaledSimplexCylinder
      (standardTypeASimplexScaling g.i)).scaling.thin
      ((standardTypeABoundaryPrismSubcomplex g).ι.app (op ⦋2⦌) t) at ht
  change
    (scaledSimplexCylinder
      (standardTypeASimplexScaling g.i)).scaling.thin
      (((standardTypeABoundaryPrismRankFunction g).filtration 0).ι.app
        (op ⦋2⦌)
        ((SSet.Subcomplex.homOfLE hle).app (op ⦋2⦌) t))
  rw [← NatTrans.comp_app_apply]
  rw [SSet.Subcomplex.homOfLE_ι]
  exact ht

noncomputable def standardTypeABoundaryPrismRankStageZeroIso
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeABoundaryPrismRankStage g 0 ≅
      standardTypeABoundaryPrism g where
  hom := standardTypeABoundaryPrismRankStageZeroToBoundary g
  inv := standardTypeABoundaryPrismBoundaryToRankStageZero g
  hom_inv_id := by
    apply ScaledSSet.ScaledMap.ext
    ext d x
    rfl
  inv_hom_id := by
    apply ScaledSSet.ScaledMap.ext
    ext d x
    rfl

/-- The explicit inverse rank-zero identification followed by the ambient leg
is the original boundary-prism inclusion. -/
theorem standardTypeABoundaryPrismRankStageZeroIso_inv_toCylinder
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardTypeABoundaryPrismRankStageZeroIso g).inv ≫
        standardTypeABoundaryPrismRankStageToCylinder g 0 =
      standardTypeABoundaryPrismToCylinder g := by
  apply ScaledSSet.ScaledMap.ext
  ext d x
  rfl

/-! ## One raw transfinite composition from the boundary prism to the cylinder -/

noncomputable def standardTypeABoundaryPrismAlternatingBotIso
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardTypeABoundaryPrismAlternatingFunctor g).obj 0 ≅
      standardTypeABoundaryPrism g := by
  change standardTypeABoundaryPrismAlternatingObj g 0 ≅
    standardTypeABoundaryPrism g
  exact
    standardTypeABoundaryPrismAlternatingEvenIso g 0 ≪≫
      standardTypeABoundaryPrismRankStageZeroIso g

@[simp]
theorem standardTypeABoundaryPrismAlternatingToCylinder_zero
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeABoundaryPrismAlternatingToCylinder g 0 =
      (standardTypeABoundaryPrismAlternatingEvenIso g 0).hom ≫
        standardTypeABoundaryPrismRankStageToCylinder g 0 := by
  simpa [Nat.bit] using
    standardTypeABoundaryPrismAlternatingToCylinder_bit_false g 0

/-- The complete boundary-prism inclusion is a single natural-number
transfinite composition whose every successor is a raw standard A/B cellular
step. -/
noncomputable def standardTypeABoundaryPrismRawTransfiniteComposition
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    MorphismProperty.TransfiniteCompositionOfShape
      (C := ScaledSSet.{u})
      (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u}))
      ℕ (standardTypeABoundaryPrismToCylinder g) where
  F := standardTypeABoundaryPrismAlternatingFunctor g
  isoBot := standardTypeABoundaryPrismAlternatingBotIso g
  incl := (standardTypeABoundaryPrismAlternatingCocone g).ι
  isColimit := standardTypeABoundaryPrismAlternatingCoconeIsColimit g
  fac := by
    change
      (standardTypeABoundaryPrismAlternatingBotIso g).inv ≫
          standardTypeABoundaryPrismAlternatingToCylinder g 0 =
        standardTypeABoundaryPrismToCylinder g
    rw [standardTypeABoundaryPrismAlternatingToCylinder_zero]
    dsimp [standardTypeABoundaryPrismAlternatingBotIso]
    calc
      (((standardTypeABoundaryPrismRankStageZeroIso g).inv ≫
          (standardTypeABoundaryPrismAlternatingEvenIso g 0).inv) ≫
        (standardTypeABoundaryPrismAlternatingEvenIso g 0).hom) ≫
          standardTypeABoundaryPrismRankStageToCylinder g 0 =
        (standardTypeABoundaryPrismRankStageZeroIso g).inv ≫
          (((standardTypeABoundaryPrismAlternatingEvenIso g 0).inv ≫
              (standardTypeABoundaryPrismAlternatingEvenIso g 0).hom) ≫
            standardTypeABoundaryPrismRankStageToCylinder g 0) := by
              simp only [Category.assoc]
      _ = (standardTypeABoundaryPrismRankStageZeroIso g).inv ≫
            standardTypeABoundaryPrismRankStageToCylinder g 0 := by simp
      _ = standardTypeABoundaryPrismToCylinder g :=
        standardTypeABoundaryPrismRankStageZeroIso_inv_toCylinder g
  map_mem j _ := by
    have hhom :
        (homOfLE (Order.le_succ j) : j ⟶ j + 1) =
          homOfLE (Nat.le_add_right j 1) :=
      Subsingleton.elim _ _
    rw [hhom, standardTypeABoundaryPrismAlternatingFunctor_map_succ]
    exact standardTypeABoundaryPrismAlternatingStep_mem_rawCellular g j

/-- Strong unretracted cellularity of the entire boundary-prism inclusion. -/
theorem standardTypeABoundaryPrismToCylinder_mem_strongCellular
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardABCStrongCellularClosure : MorphismProperty (ScaledSSet.{u}))
      (standardTypeABoundaryPrismToCylinder g) := by
  unfold standardABCStrongCellularClosure
  have h :=
    (standardTypeABoundaryPrismRawTransfiniteComposition g).ofOrderIso
      (orderIsoShrink.{u} ℕ).symm
  exact
    (MorphismProperty.transfiniteCompositionsOfShape_le_transfiniteCompositions
      (W := (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u})))
      (Shrink.{u} ℕ)) _ h.mem

/-- Consequently the full boundary-prism inclusion lies in the exact v1.59
standard A/B/C cellular closure. -/
theorem standardTypeABoundaryPrismToCylinder_mem_cellular
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardABCCellularClosure : MorphismProperty (ScaledSSet.{u}))
      (standardTypeABoundaryPrismToCylinder g) :=
  standardABCStrongCellularClosure_le_standardABCCellularClosure _
    (standardTypeABoundaryPrismToCylinder_mem_strongCellular g)

/-!
The boundary-prism component is now represented by one raw transfinite
composition of literal standard A/B generators. The remaining geometric map
for the endpoint factorization is the missing opposite-endpoint type-(A) cell
handled by v1.77.
-/

end

end KUOS.DependentOriginationStandardTypeABoundaryPrismRawTransfiniteV1_76