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
transfinite composition of raw standard A/B/C cellular steps.  Equality
transport between the binary parity indexing and the geometric rank objects
is isolated in explicit canonical isomorphisms; cellularity is transported
through those isomorphisms using Mathlib's `RespectsIso` calculus.
-/

/-! ## The exact scaled rank diagram -/

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

/-- Every simplex of the full prism carrier occurs in one finite rank stage.
The proof works directly in the supremum of the rank subcomplexes, avoiding
any universe-sensitive type annotation for the top subcomplex. -/
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
    simp
  simp only [Subfunctor.iSup_obj, Set.mem_iUnion] at ht
  obtain ⟨j, hj⟩ := ht
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

/-- Canonical parity isomorphisms.  Every equality transport in the flattened
sequence is routed through these named isomorphisms. -/
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

noncomputable def standardTypeABoundaryPrismAlternatingFalseSuccIso
    (g : StandardTypeAHornAttachmentGeneratorIndex) (j : ℕ) :
    standardTypeABoundaryPrismAlternatingObj g (Nat.bit false j + 1) ≅
      standardTypeABoundaryPrismRankAPhase g j :=
  eqToIso (by
    rw [standardTypeABoundaryPrism_bit_false_succ]
    exact standardTypeABoundaryPrismAlternatingObj_bit_true g j)

noncomputable def standardTypeABoundaryPrismAlternatingTrueSuccIso
    (g : StandardTypeAHornAttachmentGeneratorIndex) (j : ℕ) :
    standardTypeABoundaryPrismAlternatingObj g (Nat.bit true j + 1) ≅
      standardTypeABoundaryPrismRankStage g (j + 1) :=
  eqToIso (by
    rw [standardTypeABoundaryPrism_bit_true_succ]
    exact standardTypeABoundaryPrismAlternatingObj_bit_false g (j + 1))

local instance standardTypeABoundaryPrismRawStep_respectsIso :
    (standardABCRawCellularStep :
      MorphismProperty (ScaledSSet.{u})).RespectsIso := by
  unfold standardABCRawCellularStep
  infer_instance

/-- The two geometric raw phases with all parity transport made explicit. -/
noncomputable def standardTypeABoundaryPrismAlternatingStep
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (n : ℕ) :
    standardTypeABoundaryPrismAlternatingObj g n ⟶
      standardTypeABoundaryPrismAlternatingObj g (n + 1) :=
  Nat.bitCasesOn
    (motive := fun n =>
      standardTypeABoundaryPrismAlternatingObj g n ⟶
        standardTypeABoundaryPrismAlternatingObj g (n + 1))
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

noncomputable def standardTypeABoundaryPrismAlternatingFunctor
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    ℕ ⥤ ScaledSSet.{u} :=
  Functor.ofSequence (standardTypeABoundaryPrismAlternatingStep g)

/-! ## A cocone of the alternating diagram to the full cylinder -/

noncomputable def standardTypeABoundaryPrismAlternatingToCylinder
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (n : ℕ) :
    standardTypeABoundaryPrismAlternatingObj g n ⟶
      scaledSimplexCylinder (standardTypeASimplexScaling g.i) :=
  Nat.bitCasesOn
    (motive := fun n =>
      standardTypeABoundaryPrismAlternatingObj g n ⟶
        scaledSimplexCylinder (standardTypeASimplexScaling g.i))
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

/-- The target transport after an A phase cancels against the odd parity
identification before mapping to the cylinder. -/
theorem standardTypeABoundaryPrismAlternatingFalseSucc_toCylinder
    (g : StandardTypeAHornAttachmentGeneratorIndex) (j : ℕ) :
    (standardTypeABoundaryPrismAlternatingFalseSuccIso g j).inv ≫
        standardTypeABoundaryPrismAlternatingToCylinder g
          (Nat.bit false j + 1) =
      standardTypeABoundaryPrismRankAPhaseToSucc g j ≫
        standardTypeABoundaryPrismRankStageToCylinder g (j + 1) := by
  rw [standardTypeABoundaryPrism_bit_false_succ]
  simp [standardTypeABoundaryPrismAlternatingFalseSuccIso,
    standardTypeABoundaryPrismAlternatingOddIso,
    standardTypeABoundaryPrismAlternatingToCylinder, Category.assoc]

/-- The target transport after a B phase cancels against the next even parity
identification. -/
theorem standardTypeABoundaryPrismAlternatingTrueSucc_toCylinder
    (g : StandardTypeAHornAttachmentGeneratorIndex) (j : ℕ) :
    (standardTypeABoundaryPrismAlternatingTrueSuccIso g j).inv ≫
        standardTypeABoundaryPrismAlternatingToCylinder g
          (Nat.bit true j + 1) =
      standardTypeABoundaryPrismRankStageToCylinder g (j + 1) := by
  rw [standardTypeABoundaryPrism_bit_true_succ]
  simp [standardTypeABoundaryPrismAlternatingTrueSuccIso,
    standardTypeABoundaryPrismAlternatingEvenIso,
    standardTypeABoundaryPrismAlternatingToCylinder, Category.assoc]

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
          simp only [Category.assoc,
            standardTypeABoundaryPrismAlternatingFalseSucc_toCylinder]
          rw [standardTypeABoundaryPrismRankStep_factor_A_residual]
          rw [standardTypeABoundaryPrismRankStageHom_toCylinder]
      | true =>
          rw [standardTypeABoundaryPrismAlternatingStep_bit_true,
            standardTypeABoundaryPrismAlternatingToCylinder_bit_true]
          simp only [Category.assoc,
            standardTypeABoundaryPrismAlternatingTrueSucc_toCylinder]

noncomputable def standardTypeABoundaryPrismAlternatingCocone
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    Cocone (standardTypeABoundaryPrismAlternatingFunctor g) :=
  Cocone.mk
    (scaledSimplexCylinder (standardTypeASimplexScaling g.i))
    (NatTrans.ofSequence
      (standardTypeABoundaryPrismAlternatingToCylinder g)
      (fun n => by
        simpa [standardTypeABoundaryPrismAlternatingFunctor] using
          standardTypeABoundaryPrismAlternatingStep_toCylinder g n))

/-! ## Restrict an alternating cocone to its even rank stages -/

noncomputable def standardTypeABoundaryPrismAlternatingEvenLeg
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeABoundaryPrismAlternatingFunctor g))
    (j : ℕ) :
    standardTypeABoundaryPrismRankStage g j ⟶ s.pt :=
  (standardTypeABoundaryPrismAlternatingEvenIso g j).inv ≫
    s.ι.app (Nat.bit false j)

noncomputable def standardTypeABoundaryPrismAlternatingOddLeg
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeABoundaryPrismAlternatingFunctor g))
    (j : ℕ) :
    standardTypeABoundaryPrismRankAPhase g j ⟶ s.pt :=
  (standardTypeABoundaryPrismAlternatingOddIso g j).inv ≫
    s.ι.app (Nat.bit true j)

/-- The A-step cocone equation after removing the canonical parity isos. -/
theorem standardTypeABoundaryPrismAlternatingA_leg_eq
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeABoundaryPrismAlternatingFunctor g))
    (j : ℕ) :
    standardTypeABoundaryPrismRankStageToAPhase g j ≫
        standardTypeABoundaryPrismAlternatingOddLeg g s j =
      standardTypeABoundaryPrismAlternatingEvenLeg g s j := by
  have h0 := s.w (homOfLE (Nat.le_add_right (Nat.bit false j) 1))
  have h1 :
      (((standardTypeABoundaryPrismAlternatingEvenIso g j).hom ≫
          standardTypeABoundaryPrismRankStageToAPhase g j) ≫
        (standardTypeABoundaryPrismAlternatingOddIso g j).inv) ≫
          s.ι.app (Nat.bit true j) =
        s.ι.app (Nat.bit false j) := by
    simpa [standardTypeABoundaryPrismAlternatingFunctor,
      standardTypeABoundaryPrismAlternatingStep,
      standardTypeABoundaryPrismAlternatingFalseSuccIso,
      standardTypeABoundaryPrismAlternatingOddIso,
      standardTypeABoundaryPrism_bit_false_succ,
      Category.comp_id] using h0
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
          s.ι.app (Nat.bit false j) := by rw [h1]

/-- The B-step cocone equation after removing the canonical parity isos. -/
theorem standardTypeABoundaryPrismAlternatingOddLeg_eq
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeABoundaryPrismAlternatingFunctor g))
    (j : ℕ) :
    standardTypeABoundaryPrismRankAPhaseToSucc g j ≫
        standardTypeABoundaryPrismAlternatingEvenLeg g s (j + 1) =
      standardTypeABoundaryPrismAlternatingOddLeg g s j := by
  have h0 := s.w (homOfLE (Nat.le_add_right (Nat.bit true j) 1))
  have h1 :
      (((standardTypeABoundaryPrismAlternatingOddIso g j).hom ≫
          standardTypeABoundaryPrismRankAPhaseToSucc g j) ≫
        (standardTypeABoundaryPrismAlternatingEvenIso g (j + 1)).inv) ≫
          s.ι.app (Nat.bit false (j + 1)) =
        s.ι.app (Nat.bit true j) := by
    simpa [standardTypeABoundaryPrismAlternatingFunctor,
      standardTypeABoundaryPrismAlternatingStep,
      standardTypeABoundaryPrismAlternatingTrueSuccIso,
      standardTypeABoundaryPrismAlternatingEvenIso,
      standardTypeABoundaryPrism_bit_true_succ,
      Category.comp_id] using h0
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
          s.ι.app (Nat.bit true j) := by rw [h1]

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

noncomputable def standardTypeABoundaryPrismRankCoconeOfAlternatingCocone
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeABoundaryPrismAlternatingFunctor g)) :
    Cocone (standardTypeABoundaryPrismScaledRankFunctor g) :=
  Cocone.mk s.pt
    (NatTrans.ofSequence
      (standardTypeABoundaryPrismAlternatingEvenLeg g s)
      (fun j => by
        simpa [standardTypeABoundaryPrismScaledRankFunctor] using
          standardTypeABoundaryPrismAlternatingEvenLeg_succ g s j))

/-! ## Inserting the A-phases does not change the colimit -/

noncomputable def standardTypeABoundaryPrismAlternatingDesc
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeABoundaryPrismAlternatingFunctor g)) :
    scaledSimplexCylinder (standardTypeASimplexScaling g.i) ⟶ s.pt :=
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
            rw [standardTypeABoundaryPrismAlternatingToCylinder_bit_false]
            change
              ((standardTypeABoundaryPrismAlternatingEvenIso g j).hom ≫
                standardTypeABoundaryPrismRankStageToCylinder g j) ≫
                  standardTypeABoundaryPrismAlternatingDesc g s =
                (standardTypeABoundaryPrismAlternatingCocone g).ι.app
                  (Nat.bit false j)
            rw [Category.assoc, hr']
            simp [standardTypeABoundaryPrismAlternatingEvenLeg,
              standardTypeABoundaryPrismAlternatingCocone,
              standardTypeABoundaryPrismAlternatingFunctor]
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
            rw [standardTypeABoundaryPrismAlternatingToCylinder_bit_true]
            change
              (((standardTypeABoundaryPrismAlternatingOddIso g j).hom ≫
                  standardTypeABoundaryPrismRankAPhaseToSucc g j) ≫
                standardTypeABoundaryPrismRankStageToCylinder g (j + 1)) ≫
                  standardTypeABoundaryPrismAlternatingDesc g s =
                (standardTypeABoundaryPrismAlternatingCocone g).ι.app
                  (Nat.bit true j)
            rw [Category.assoc, hr',
              standardTypeABoundaryPrismAlternatingOddLeg_eq g s j]
            simp [standardTypeABoundaryPrismAlternatingOddLeg,
              standardTypeABoundaryPrismAlternatingCocone,
              standardTypeABoundaryPrismAlternatingFunctor]
  uniq s m hm := by
    apply (standardTypeABoundaryPrismScaledRankCoconeIsColimit g).hom_ext
    intro j
    have heven := hm (Nat.bit false j)
    have hdesc :=
      (standardTypeABoundaryPrismScaledRankCoconeIsColimit g).fac
        (standardTypeABoundaryPrismRankCoconeOfAlternatingCocone g s) j
    have heven' :
        standardTypeABoundaryPrismRankStageToCylinder g j ≫ m =
          standardTypeABoundaryPrismAlternatingEvenLeg g s j := by
      rw [standardTypeABoundaryPrismAlternatingToCylinder_bit_false] at heven
      change
        ((standardTypeABoundaryPrismAlternatingEvenIso g j).hom ≫
            standardTypeABoundaryPrismRankStageToCylinder g j) ≫ m =
          (standardTypeABoundaryPrismAlternatingCocone g).ι.app
            (Nat.bit false j) at heven
      change
        standardTypeABoundaryPrismRankStageToCylinder g j ≫ m =
          (standardTypeABoundaryPrismAlternatingEvenIso g j).inv ≫
            (standardTypeABoundaryPrismAlternatingCocone g).ι.app
              (Nat.bit false j)
      calc
        standardTypeABoundaryPrismRankStageToCylinder g j ≫ m =
          (standardTypeABoundaryPrismAlternatingEvenIso g j).inv ≫
            (((standardTypeABoundaryPrismAlternatingEvenIso g j).hom ≫
              standardTypeABoundaryPrismRankStageToCylinder g j) ≫ m) := by
                simp [Category.assoc]
        _ = (standardTypeABoundaryPrismAlternatingEvenIso g j).inv ≫
              (standardTypeABoundaryPrismAlternatingCocone g).ι.app
                (Nat.bit false j) := by rw [heven]
    have hdesc' :
        standardTypeABoundaryPrismRankStageToCylinder g j ≫
            standardTypeABoundaryPrismAlternatingDesc g s =
          standardTypeABoundaryPrismAlternatingEvenLeg g s j := by
      simpa [standardTypeABoundaryPrismScaledRankCocone,
        standardTypeABoundaryPrismAlternatingDesc,
        standardTypeABoundaryPrismRankCoconeOfAlternatingCocone] using hdesc
    exact heven'.trans hdesc'.symm

/-! ## One raw transfinite composition from the boundary prism to the cylinder -/

noncomputable def standardTypeABoundaryPrismAlternatingBotIso
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardTypeABoundaryPrismAlternatingFunctor g).obj 0 ≅
      standardTypeABoundaryPrism g := by
  change standardTypeABoundaryPrismAlternatingObj g 0 ≅
    standardTypeABoundaryPrism g
  exact
    standardTypeABoundaryPrismAlternatingEvenIso g 0 ≪≫
      eqToIso (standardTypeABoundaryPrismRankStage_zero g)

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
    apply ScaledSSet.ScaledMap.ext
    simp [standardTypeABoundaryPrismAlternatingBotIso,
      standardTypeABoundaryPrismAlternatingCocone,
      standardTypeABoundaryPrismAlternatingToCylinder,
      standardTypeABoundaryPrismAlternatingFunctor,
      standardTypeABoundaryPrismAlternatingEvenIso,
      standardTypeABoundaryPrismAlternatingObj,
      standardTypeABoundaryPrismRankStage_zero,
      standardTypeABoundaryPrismRankStageToCylinder,
      standardTypeABoundaryPrismToCylinder]
  map_mem j _ := by
    change
      standardABCRawCellularStep
        ((standardTypeABoundaryPrismAlternatingFunctor g).map
          (homOfLE (Order.le_succ j)))
    rw [standardTypeABoundaryPrismAlternatingFunctor,
      Functor.ofSequence_map_homOfLE_succ]
    exact standardTypeABoundaryPrismAlternatingStep_mem_rawCellular g j

/-- Strong unretracted cellularity of the entire boundary-prism inclusion. -/
theorem standardTypeABoundaryPrismToCylinder_mem_strongCellular
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardABCStrongCellularClosure
      (standardTypeABoundaryPrismToCylinder g) := by
  unfold standardABCStrongCellularClosure
  exact
    (MorphismProperty.transfiniteCompositionsOfShape_le_transfiniteCompositions
      (W := (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u}))) ℕ)
      _
      (standardTypeABoundaryPrismRawTransfiniteComposition g).mem

/-- Consequently the full boundary-prism inclusion lies in the exact v1.59
standard A/B/C cellular closure. -/
theorem standardTypeABoundaryPrismToCylinder_mem_cellular
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardABCCellularClosure
      (standardTypeABoundaryPrismToCylinder g) :=
  standardABCStrongCellularClosure_le_standardABCCellularClosure _
    (standardTypeABoundaryPrismToCylinder_mem_strongCellular g)

/-!
The boundary-prism component is now represented by one raw transfinite
composition of literal standard A/B generators.  The remaining geometric map
for the endpoint factorization is the missing opposite-endpoint type-(A) cell
handled by v1.77.
-/

end

end KUOS.DependentOriginationStandardTypeABoundaryPrismRawTransfiniteV1_76