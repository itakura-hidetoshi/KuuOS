import KUOS.DependentOriginationStandardTypeABoundaryPrismRankwiseSimultaneousBPhaseV1_75
import Mathlib.CategoryTheory.Functor.OfSequence
import Mathlib.Data.Nat.Bits

namespace KUOS.DependentOriginationStandardTypeABoundaryPrismRawTransfiniteV1_76

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Limits
open MonoidalCategory
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationStandardTypeAScaledPushoutSourceEnrichmentV1_53
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

Versions v1.74 and v1.75 established the exact two-phase successor
factorization

```text
R_j -- one raw A step --> A_j -- one raw B step --> R_(j+1).
```

The point of this file is to assemble those *raw* steps before applying the
transfinite-composition closure.  We deliberately do not first collapse each
pair to an already-transfinite morphism and then take another transfinite
composition: that would hide a flattening obligation.  Instead we use the
single natural-number sequence

```text
R_0, A_0, R_1, A_1, R_2, A_2, ...
```

and prove directly that every successor map is in
`pushouts (coproducts E_std)`.

There are two categorical ingredients.

1. The ambient-pullback-scaled rank diagram has the full scaled cylinder as
   its colimit.  Ordinary carrier universality comes from the Mathlib relative
   cell complex of v1.61; scaledness of the universal map follows because
   every thin triangle of the cylinder occurs in some finite rank stage.
2. The alternating sequence inserts `A_j` between consecutive rank stages.
   Its even subsequence is the rank diagram, and the two one-step cocone
   equations show that inserting the intermediate A-phases does not alter the
   colimit.

We encode parity with `Nat.bodd` and `Nat.div2`.  This makes successor
normalization exact: a false bit takes `R_j` to `A_j`, and a true bit takes
`A_j` to `R_(j+1)`.

The final output is

```text
standardTypeABoundaryPrismToCylinder g
  ∈ transfiniteCompositions (pushouts (coproducts E_std)).
```

Thus the complete boundary-prism part of the endpoint Leibniz map already
lies in the strong unretracted standard cellular closure.  No type-(C) cell is
used and no canonical arbitrary-scaling KuuOS family is identified with the
standard A/B/C family.
-/

/-! ## The exact scaled rank diagram -/

/-- The ambient-pullback-scaled rank stages as an honest natural-number
functor.  Its maps are the canonical scaled inclusions of v1.71. -/
noncomputable def standardTypeABoundaryPrismScaledRankFunctor
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    ℕ ⥤ ScaledSSet.{u} where
  obj j := standardTypeABoundaryPrismRankStage g j
  map {j k} f :=
    standardTypeABoundaryPrismRankStageHom g (leOfHom f)
  map_id j := by
    apply ScaledSSet.ScaledMap.ext
    rfl
  map_comp {i j k} f h := by
    apply ScaledSSet.ScaledMap.ext
    rfl

/-- The rank diagram maps to the full scaled cylinder by the common ambient
inclusions. -/
noncomputable def standardTypeABoundaryPrismScaledRankCocone
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    Cocone (standardTypeABoundaryPrismScaledRankFunctor g) :=
  Cocone.mk
    (scaledSimplexCylinder (standardTypeASimplexScaling g.i))
    { app := fun j => standardTypeABoundaryPrismRankStageToCylinder g j
      naturality := by
        intro j k f
        simpa [standardTypeABoundaryPrismScaledRankFunctor] using
          standardTypeABoundaryPrismRankStageHom_toCylinder g
            (leOfHom f) }

/-! ## Every cylinder simplex, and every thin cylinder triangle, occurs at a finite rank -/

/-- Every simplex of the full prism carrier already occurs in one finite rank
stage.  This is the elementwise form of v1.61's `iSup_filtration = top`. -/
theorem standardTypeABoundaryPrism_exists_rank_lift
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    {d : SimplexCategoryᵒᵖ}
    (t : (scaledSimplexCylinder
      (standardTypeASimplexScaling g.i)).carrier.obj d) :
    ∃ (j : ℕ)
      (x : (standardTypeABoundaryPrismRankStage g j).carrier.obj d),
      (standardTypeABoundaryPrismRankStageToCylinder g j).map.app d x = t := by
  have ht :
      t ∈ (⨆ j : ℕ,
        (standardTypeABoundaryPrismRankFunction g).filtration j).obj d := by
    rw [standardTypeABoundaryPrism_iSup_filtration g]
    exact Set.mem_univ t
  rw [Subfunctor.iSup_obj] at ht
  obtain ⟨j, hj⟩ := Set.mem_iUnion.mp ht
  refine ⟨j, ⟨t, hj⟩, ?_⟩
  rfl

/-- A thin triangle of the full cylinder lifts to a thin triangle in some
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
      (((standardTypeABoundaryPrismRankFunction g).filtration j).ι.app
        (op ⦋2⦌) x)
  rw [← hx] at ht
  exact ht

/-! ## Reuse the ordinary Mathlib relative-cell colimit underneath -/

/-- The ordinary relative-cell-complex functor really is the rank filtration
functor.  We expose its objects for the scaled colimit proof below. -/
@[simp]
theorem standardTypeABoundaryPrismRelativeCellComplex_F_obj
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ) :
    (standardTypeABoundaryPrismRelativeCellComplex g).F.obj j =
      ((standardTypeABoundaryPrismRankFunction g).filtration j : SSet.{u}) := by
  rfl

/-- The colimit inclusion of the ordinary relative-cell complex is the literal
rank-subcomplex inclusion into the full prism. -/
@[simp]
theorem standardTypeABoundaryPrismRelativeCellComplex_incl_app
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ) :
    (standardTypeABoundaryPrismRelativeCellComplex g).incl.app j =
      ((standardTypeABoundaryPrismRankFunction g).filtration j).ι := by
  rfl

/-- Forget the scaling of an arbitrary cocone on the scaled rank diagram and
view its legs as a cocone on Mathlib's ordinary relative-cell-complex functor. -/
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
              (s.ι.app j).map
        simpa [standardTypeABoundaryPrismScaledRankFunctor,
          standardTypeABoundaryPrismRankStageHom] using h }

/-- Universal map out of the full scaled cylinder induced by a cocone on the
scaled rank stages. -/
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

/-- The full scaled cylinder is the colimit of the ambient-pullback-scaled rank
diagram.  Ordinary universality is exactly Mathlib's v1.61 relative-cell
complex; the only new statement is preservation of thin triangles by the
induced universal map. -/
noncomputable def standardTypeABoundaryPrismScaledRankCoconeIsColimit
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    IsColimit (standardTypeABoundaryPrismScaledRankCocone g) where
  desc s := standardTypeABoundaryPrismScaledRankDesc g s
  fac s j := by
    apply ScaledSSet.ScaledMap.ext
    simpa [standardTypeABoundaryPrismScaledRankCocone,
      standardTypeABoundaryPrismRankStageToCylinder,
      standardTypeABoundaryPrismScaledRankDesc,
      standardTypeABoundaryPrismUnderlyingRankCocone] using
        (standardTypeABoundaryPrismRelativeCellComplex g).isColimit.fac
          (standardTypeABoundaryPrismUnderlyingRankCocone g s) j
  uniq s m hm := by
    apply ScaledSSet.ScaledMap.ext
    apply (standardTypeABoundaryPrismRelativeCellComplex g).isColimit.hom_ext
    intro j
    have hleft :
        (standardTypeABoundaryPrismRelativeCellComplex g).incl.app j ≫ m.map =
          (s.ι.app j).map := by
      simpa [standardTypeABoundaryPrismScaledRankCocone,
        standardTypeABoundaryPrismRankStageToCylinder] using
        congrArg ScaledSSet.ScaledMap.map (hm j)
    have hright :=
      (standardTypeABoundaryPrismRelativeCellComplex g).isColimit.fac
        (standardTypeABoundaryPrismUnderlyingRankCocone g s) j
    exact hleft.trans hright.symm

/-! ## The alternating raw A/B sequence -/

/-- Object at position `n` in the flattened rank filtration.  Even positions
are rank stages and odd positions are the intermediate simultaneous A-phases. -/
def standardTypeABoundaryPrismAlternatingObj
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (n : ℕ) : ScaledSSet.{u} :=
  match Nat.bodd n with
  | false => standardTypeABoundaryPrismRankStage g (Nat.div2 n)
  | true => standardTypeABoundaryPrismRankAPhase g (Nat.div2 n)

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

/-! Type-correct canonical identifications of successor objects.
Arithmetic bit identities below are propositional, not definitional equalities. -/

@[simp]
private theorem standardTypeABoundaryPrismAlternatingObj_bit_false_succ
    (g : StandardTypeAHornAttachmentGeneratorIndex) (j : ℕ) :
    standardTypeABoundaryPrismAlternatingObj g (Nat.bit false j + 1) =
      standardTypeABoundaryPrismRankAPhase g j := by
  have hbit : Nat.bit false j + 1 = Nat.bit true j := by
    simp [Nat.bit_val]
  rw [hbit, standardTypeABoundaryPrismAlternatingObj_bit_true]

@[simp]
private theorem standardTypeABoundaryPrismAlternatingObj_bit_true_succ
    (g : StandardTypeAHornAttachmentGeneratorIndex) (j : ℕ) :
    standardTypeABoundaryPrismAlternatingObj g (Nat.bit true j + 1) =
      standardTypeABoundaryPrismRankStage g (j + 1) := by
  have hbit : Nat.bit true j + 1 = Nat.bit false (j + 1) := by
    simp [Nat.bit_val, Nat.mul_add, Nat.add_assoc, Nat.add_comm, Nat.add_left_comm]
    omega
  rw [hbit, standardTypeABoundaryPrismAlternatingObj_bit_false]

/-- The canonical alternating successor, defined by the binary eliminator
instead of proof-relevant Bool.rec transports. -/
noncomputable def standardTypeABoundaryPrismAlternatingStep
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (n : ℕ) :
    standardTypeABoundaryPrismAlternatingObj g n ⟶
      standardTypeABoundaryPrismAlternatingObj g (n + 1) :=
  Nat.bitCasesOn
    (motive := fun k : ℕ =>
      standardTypeABoundaryPrismAlternatingObj g k ⟶
        standardTypeABoundaryPrismAlternatingObj g (k + 1))
    n (fun b j =>
      match b with
      | false =>
          (eqToHom (standardTypeABoundaryPrismAlternatingObj_bit_false g j) ≫
            standardTypeABoundaryPrismRankStageToAPhase g j) ≫
            eqToHom (standardTypeABoundaryPrismAlternatingObj_bit_false_succ g j).symm
      | true =>
          (eqToHom (standardTypeABoundaryPrismAlternatingObj_bit_true g j) ≫
            standardTypeABoundaryPrismRankAPhaseToSucc g j) ≫
            eqToHom (standardTypeABoundaryPrismAlternatingObj_bit_true_succ g j).symm)

/-- The literal A-phase map after the canonical, *proof-relevant object
identifications* of the even rank and next odd phase. -/
@[simp]
theorem standardTypeABoundaryPrismAlternatingStep_bit_false
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ) :
    standardTypeABoundaryPrismAlternatingStep g (Nat.bit false j) =
      (eqToHom (standardTypeABoundaryPrismAlternatingObj_bit_false g j) ≫
        standardTypeABoundaryPrismRankStageToAPhase g j) ≫
        eqToHom (standardTypeABoundaryPrismAlternatingObj_bit_false_succ g j).symm := by
  simp [standardTypeABoundaryPrismAlternatingStep, Nat.bit_val,
    Nat.bitCasesOn_bit0, Nat.bitCasesOn_bit1]

/-- The literal B-phase map after the canonical odd-phase / next even-rank
object identifications. -/
@[simp]
theorem standardTypeABoundaryPrismAlternatingStep_bit_true
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ) :
    standardTypeABoundaryPrismAlternatingStep g (Nat.bit true j) =
      (eqToHom (standardTypeABoundaryPrismAlternatingObj_bit_true g j) ≫
        standardTypeABoundaryPrismRankAPhaseToSucc g j) ≫
        eqToHom (standardTypeABoundaryPrismAlternatingObj_bit_true_succ g j).symm := by
  simp [standardTypeABoundaryPrismAlternatingStep, Nat.bit_val,
    Nat.bitCasesOn_bit0, Nat.bitCasesOn_bit1]

/-- The flattened natural-number diagram generated by the raw A/B successor
maps. -/
noncomputable def standardTypeABoundaryPrismAlternatingFunctor
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    ℕ ⥤ ScaledSSet.{u} :=
  Functor.ofSequence (standardTypeABoundaryPrismAlternatingStep g)

/-- Every successor of the flattened diagram is literally one raw standard
cellular step. -/
theorem standardTypeABoundaryPrismAlternatingStep_mem_rawCellular
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (n : ℕ) :
    standardABCRawCellularStep.{u}
      (standardTypeABoundaryPrismAlternatingStep.{u} g n) := by
  cases n using Nat.bitCasesOn with
  | bit b j =>
      cases b with
      | false =>
          change standardABCRawCellularStep
            (standardTypeABoundaryPrismAlternatingStep g (Nat.bit false j))
          rw [standardTypeABoundaryPrismAlternatingStep_bit_false]
          have hpost :
              standardABCRawCellularStep
                (standardTypeABoundaryPrismRankStageToAPhase g j ≫
                  eqToHom (standardTypeABoundaryPrismAlternatingObj_bit_false_succ g j).symm) :=
            MorphismProperty.RespectsIso.postcomp
              (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u}))
              (eqToHom (standardTypeABoundaryPrismAlternatingObj_bit_false_succ g j).symm)
              _ (standardTypeABoundaryPrismRankStageToAPhase_mem_rawCellular g j)
          have hpre :
              standardABCRawCellularStep
                (eqToHom (standardTypeABoundaryPrismAlternatingObj_bit_false g j) ≫
                  (standardTypeABoundaryPrismRankStageToAPhase g j ≫
                    eqToHom (standardTypeABoundaryPrismAlternatingObj_bit_false_succ g j).symm)) :=
            MorphismProperty.RespectsIso.precomp
              (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u}))
              (eqToHom (standardTypeABoundaryPrismAlternatingObj_bit_false g j))
              _ hpost
          simpa only [Category.assoc] using hpre
      | true =>
          change standardABCRawCellularStep
            (standardTypeABoundaryPrismAlternatingStep g (Nat.bit true j))
          rw [standardTypeABoundaryPrismAlternatingStep_bit_true]
          have hpost :
              standardABCRawCellularStep
                (standardTypeABoundaryPrismRankAPhaseToSucc g j ≫
                  eqToHom (standardTypeABoundaryPrismAlternatingObj_bit_true_succ g j).symm) :=
            MorphismProperty.RespectsIso.postcomp
              (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u}))
              (eqToHom (standardTypeABoundaryPrismAlternatingObj_bit_true_succ g j).symm)
              _ (standardTypeABoundaryPrismRankAPhaseToSucc_mem_rawCellular g j)
          have hpre :
              standardABCRawCellularStep
                (eqToHom (standardTypeABoundaryPrismAlternatingObj_bit_true g j) ≫
                  (standardTypeABoundaryPrismRankAPhaseToSucc g j ≫
                    eqToHom (standardTypeABoundaryPrismAlternatingObj_bit_true_succ g j).symm)) :=
            MorphismProperty.RespectsIso.precomp
              (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u}))
              (eqToHom (standardTypeABoundaryPrismAlternatingObj_bit_true g j))
              _ hpost
          simpa only [Category.assoc] using hpre


/-! ## A cocone of the alternating diagram to the full cylinder -/

/-- Canonical map from each flattened stage to the common full cylinder. -/
noncomputable def standardTypeABoundaryPrismAlternatingToCylinder
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (n : ℕ) :
    standardTypeABoundaryPrismAlternatingObj g n ⟶
      scaledSimplexCylinder (standardTypeASimplexScaling g.i) :=
  Nat.bitCasesOn
    (motive := fun k : ℕ =>
      standardTypeABoundaryPrismAlternatingObj g k ⟶
        scaledSimplexCylinder (standardTypeASimplexScaling g.i))
    n (fun b j =>
      match b with
      | false =>
          eqToHom (standardTypeABoundaryPrismAlternatingObj_bit_false g j) ≫
            standardTypeABoundaryPrismRankStageToCylinder g j
      | true =>
          eqToHom (standardTypeABoundaryPrismAlternatingObj_bit_true g j) ≫
            (standardTypeABoundaryPrismRankAPhaseToSucc g j ≫
              standardTypeABoundaryPrismRankStageToCylinder g (j + 1)))


@[simp]
theorem standardTypeABoundaryPrismAlternatingToCylinder_bit_false
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ) :
    standardTypeABoundaryPrismAlternatingToCylinder g (Nat.bit false j) =
      eqToHom (standardTypeABoundaryPrismAlternatingObj_bit_false g j) ≫
        standardTypeABoundaryPrismRankStageToCylinder g j := by
  simp [standardTypeABoundaryPrismAlternatingToCylinder, Nat.bit_val,
    Nat.bitCasesOn_bit0, Nat.bitCasesOn_bit1]

@[simp]
theorem standardTypeABoundaryPrismAlternatingToCylinder_bit_true
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ) :
    standardTypeABoundaryPrismAlternatingToCylinder g (Nat.bit true j) =
      eqToHom (standardTypeABoundaryPrismAlternatingObj_bit_true g j) ≫
        (standardTypeABoundaryPrismRankAPhaseToSucc g j ≫
          standardTypeABoundaryPrismRankStageToCylinder g (j + 1)) := by
  simp [standardTypeABoundaryPrismAlternatingToCylinder, Nat.bit_val,
    Nat.bitCasesOn_bit0, Nat.bitCasesOn_bit1]

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
          have hbit : Nat.bit false j + 1 = Nat.bit true j := by
            simp [Nat.bit_val]
          have hc :
              standardTypeABoundaryPrismRankStageToAPhase g j ≫
                  (standardTypeABoundaryPrismRankAPhaseToSucc g j ≫
                    standardTypeABoundaryPrismRankStageToCylinder g (j + 1)) =
                standardTypeABoundaryPrismRankStageToCylinder g j := by
            rw [← Category.assoc, standardTypeABoundaryPrismRankStep_factor_A_residual]
            exact standardTypeABoundaryPrismRankStageHom_toCylinder g (Nat.le_succ j)
          have hc' :=
            congrArg (fun f :
              standardTypeABoundaryPrismRankStage g j ⟶
                scaledSimplexCylinder (standardTypeASimplexScaling g.i) =>
              eqToHom (standardTypeABoundaryPrismAlternatingObj_bit_false g j) ≫ f) hc
          simpa [standardTypeABoundaryPrismAlternatingStep_bit_false,
            standardTypeABoundaryPrismAlternatingToCylinder_bit_false,
            standardTypeABoundaryPrismAlternatingToCylinder_bit_true,
            hbit, Category.assoc] using hc'
      | true =>
          have hbit : Nat.bit true j + 1 = Nat.bit false (j + 1) := by
            simp [Nat.bit_val, Nat.mul_add, Nat.add_assoc, Nat.add_comm, Nat.add_left_comm]
            omega
          simp [standardTypeABoundaryPrismAlternatingStep_bit_true,
            standardTypeABoundaryPrismAlternatingToCylinder_bit_false,
            standardTypeABoundaryPrismAlternatingToCylinder_bit_true,
            hbit, Category.assoc]


/-- The full cylinder cocone on the single flattened A/B sequence. -/
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

/-! ## Restrict any alternating cocone to its even rank stages -/

/-- Even leg of an arbitrary cocone on the alternating diagram. -/
noncomputable def standardTypeABoundaryPrismAlternatingEvenLeg
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeABoundaryPrismAlternatingFunctor g))
    (j : ℕ) :
    standardTypeABoundaryPrismRankStage g j ⟶ s.pt :=
  eqToHom (standardTypeABoundaryPrismAlternatingObj_bit_false g j).symm ≫
    s.ι.app (Nat.bit false j)

/-- Odd A-phase leg of an arbitrary cocone on the alternating diagram. -/
noncomputable def standardTypeABoundaryPrismAlternatingOddLeg
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeABoundaryPrismAlternatingFunctor g))
    (j : ℕ) :
    standardTypeABoundaryPrismRankAPhase g j ⟶ s.pt :=
  eqToHom (standardTypeABoundaryPrismAlternatingObj_bit_true g j).symm ≫
    s.ι.app (Nat.bit true j)

/-- The two consecutive raw cocone equations collapse to the exact rank-stage
successor equation on the even subsequence. -/
theorem standardTypeABoundaryPrismAlternatingEvenLeg_succ
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeABoundaryPrismAlternatingFunctor g))
    (j : ℕ) :
    standardTypeABoundaryPrismRankStageHom g (Nat.le_succ j) ≫
        standardTypeABoundaryPrismAlternatingEvenLeg g s (j + 1) =
      standardTypeABoundaryPrismAlternatingEvenLeg g s j := by
  have hA0 :=
    s.w (homOfLE (Nat.le_add_right (Nat.bit false j) 1))
  have hB0 :=
    s.w (homOfLE (Nat.le_add_right (Nat.bit true j) 1))
  have hbitA : Nat.bit false j + 1 = Nat.bit true j := by
    simp [Nat.bit_val]
  have hbitB : Nat.bit true j + 1 = Nat.bit false (j + 1) := by
    simp [Nat.bit_val, Nat.mul_add, Nat.add_assoc, Nat.add_comm, Nat.add_left_comm]
    omega
  have hA :
      standardTypeABoundaryPrismRankStageToAPhase g j ≫
          standardTypeABoundaryPrismAlternatingOddLeg g s j =
        standardTypeABoundaryPrismAlternatingEvenLeg g s j := by
    have ha :
        standardTypeABoundaryPrismAlternatingStep g (Nat.bit false j) ≫
            s.ι.app (Nat.bit true j) = s.ι.app (Nat.bit false j) := by
      simpa [standardTypeABoundaryPrismAlternatingFunctor, hbitA] using hA0
    have hat :=
      congrArg (fun f :
        standardTypeABoundaryPrismAlternatingObj g (Nat.bit false j) ⟶ s.pt =>
        eqToHom (standardTypeABoundaryPrismAlternatingObj_bit_false g j).symm ≫ f) ha
    simpa [standardTypeABoundaryPrismAlternatingEvenLeg,
      standardTypeABoundaryPrismAlternatingOddLeg,
      standardTypeABoundaryPrismAlternatingStep_bit_false,
      hbitA, Category.assoc] using hat
  have hB :
      standardTypeABoundaryPrismRankAPhaseToSucc g j ≫
          standardTypeABoundaryPrismAlternatingEvenLeg g s (j + 1) =
        standardTypeABoundaryPrismAlternatingOddLeg g s j := by
    have hb :
        standardTypeABoundaryPrismAlternatingStep g (Nat.bit true j) ≫
            s.ι.app (Nat.bit false (j + 1)) = s.ι.app (Nat.bit true j) := by
      simpa [standardTypeABoundaryPrismAlternatingFunctor, hbitB] using hB0
    have hbt :=
      congrArg (fun f :
        standardTypeABoundaryPrismAlternatingObj g (Nat.bit true j) ⟶ s.pt =>
        eqToHom (standardTypeABoundaryPrismAlternatingObj_bit_true g j).symm ≫ f) hb
    simpa [standardTypeABoundaryPrismAlternatingEvenLeg,
      standardTypeABoundaryPrismAlternatingOddLeg,
      standardTypeABoundaryPrismAlternatingStep_bit_true,
      hbitB, Category.assoc] using hbt
  rw [← standardTypeABoundaryPrismRankStep_factor_A_residual g j]
  rw [Category.assoc, hB, hA]

/-- The even legs of an alternating cocone form a cocone on the exact scaled
rank diagram. -/
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

/-- The odd cocone equation is the B-step followed by the next even leg. -/
theorem standardTypeABoundaryPrismAlternatingOddLeg_eq
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeABoundaryPrismAlternatingFunctor g))
    (j : ℕ) :
    standardTypeABoundaryPrismRankAPhaseToSucc g j ≫
        standardTypeABoundaryPrismAlternatingEvenLeg g s (j + 1) =
      standardTypeABoundaryPrismAlternatingOddLeg g s j := by
  have h := s.w (homOfLE (Nat.le_add_right (Nat.bit true j) 1))
  have hbit : Nat.bit true j + 1 = Nat.bit false (j + 1) := by
    simp [Nat.bit_val, Nat.mul_add, Nat.add_assoc, Nat.add_comm, Nat.add_left_comm]
    omega
  have hb :
      standardTypeABoundaryPrismAlternatingStep g (Nat.bit true j) ≫
          s.ι.app (Nat.bit false (j + 1)) = s.ι.app (Nat.bit true j) := by
    simpa [standardTypeABoundaryPrismAlternatingFunctor, hbit] using h
  have hbt :=
    congrArg (fun f :
      standardTypeABoundaryPrismAlternatingObj g (Nat.bit true j) ⟶ s.pt =>
      eqToHom (standardTypeABoundaryPrismAlternatingObj_bit_true g j).symm ≫ f) hb
  simpa [standardTypeABoundaryPrismAlternatingEvenLeg,
    standardTypeABoundaryPrismAlternatingOddLeg,
    standardTypeABoundaryPrismAlternatingStep_bit_true,
    hbit, Category.assoc] using hbt

/-! ## Inserting the A-phases does not change the colimit -/

/-- Universal map induced by an alternating cocone, obtained from its even
rank-subcocone and the scaled rank colimit theorem. -/
noncomputable def standardTypeABoundaryPrismAlternatingDesc
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeABoundaryPrismAlternatingFunctor g)) :
    scaledSimplexCylinder (standardTypeASimplexScaling g.i) ⟶ s.pt :=
  (standardTypeABoundaryPrismScaledRankCoconeIsColimit g).desc
    (standardTypeABoundaryPrismRankCoconeOfAlternatingCocone g s)

/-- The flattened A/B cocone still has the full scaled cylinder as its colimit. -/
noncomputable def standardTypeABoundaryPrismAlternatingCoconeIsColimit
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    IsColimit (standardTypeABoundaryPrismAlternatingCocone g) where
  desc s := standardTypeABoundaryPrismAlternatingDesc g s
  fac s n := by
    cases n using Nat.bitCasesOn with
    | bit b j =>
        cases b with
        | false =>
            have hr :
                standardTypeABoundaryPrismRankStageToCylinder g j ≫
                    standardTypeABoundaryPrismAlternatingDesc g s =
                  standardTypeABoundaryPrismAlternatingEvenLeg g s j := by
              simpa [standardTypeABoundaryPrismScaledRankCocone,
                standardTypeABoundaryPrismAlternatingDesc,
                standardTypeABoundaryPrismRankCoconeOfAlternatingCocone] using
                  (standardTypeABoundaryPrismScaledRankCoconeIsColimit g).fac
                    (standardTypeABoundaryPrismRankCoconeOfAlternatingCocone g s) j
            have hrt :=
              congrArg (fun f : standardTypeABoundaryPrismRankStage g j ⟶ s.pt =>
                eqToHom (standardTypeABoundaryPrismAlternatingObj_bit_false g j) ≫ f) hr
            simpa [standardTypeABoundaryPrismAlternatingCocone,
              standardTypeABoundaryPrismAlternatingToCylinder_bit_false,
              standardTypeABoundaryPrismAlternatingEvenLeg,
              Category.assoc] using hrt
        | true =>
            have hr :
                standardTypeABoundaryPrismRankStageToCylinder g (j + 1) ≫
                    standardTypeABoundaryPrismAlternatingDesc g s =
                  standardTypeABoundaryPrismAlternatingEvenLeg g s (j + 1) := by
              simpa [standardTypeABoundaryPrismScaledRankCocone,
                standardTypeABoundaryPrismAlternatingDesc,
                standardTypeABoundaryPrismRankCoconeOfAlternatingCocone] using
                  (standardTypeABoundaryPrismScaledRankCoconeIsColimit g).fac
                    (standardTypeABoundaryPrismRankCoconeOfAlternatingCocone g s) (j + 1)
            have hb := standardTypeABoundaryPrismAlternatingOddLeg_eq g s j
            have hodd :
                (standardTypeABoundaryPrismRankAPhaseToSucc g j ≫
                  standardTypeABoundaryPrismRankStageToCylinder g (j + 1)) ≫
                    standardTypeABoundaryPrismAlternatingDesc g s =
                  standardTypeABoundaryPrismAlternatingOddLeg g s j := by
              rw [Category.assoc, hr]
              exact hb
            have hoddt :=
              congrArg (fun f : standardTypeABoundaryPrismRankAPhase g j ⟶ s.pt =>
                eqToHom (standardTypeABoundaryPrismAlternatingObj_bit_true g j) ≫ f) hodd
            simpa [standardTypeABoundaryPrismAlternatingCocone,
              standardTypeABoundaryPrismAlternatingToCylinder_bit_true,
              standardTypeABoundaryPrismAlternatingOddLeg,
              Category.assoc] using hoddt
  uniq s m hm := by
    apply (standardTypeABoundaryPrismScaledRankCoconeIsColimit g).hom_ext
    intro j
    have heven := hm (Nat.bit false j)
    have hevent :=
      congrArg (fun f :
        standardTypeABoundaryPrismAlternatingObj g (Nat.bit false j) ⟶ s.pt =>
        eqToHom (standardTypeABoundaryPrismAlternatingObj_bit_false g j).symm ≫ f) heven
    have hleft :
        standardTypeABoundaryPrismRankStageToCylinder g j ≫ m =
          standardTypeABoundaryPrismAlternatingEvenLeg g s j := by
      simpa [standardTypeABoundaryPrismAlternatingCocone,
        standardTypeABoundaryPrismAlternatingToCylinder_bit_false,
        standardTypeABoundaryPrismAlternatingEvenLeg,
        Category.assoc] using hevent
    have hright :
        standardTypeABoundaryPrismRankStageToCylinder g j ≫
            standardTypeABoundaryPrismAlternatingDesc g s =
          standardTypeABoundaryPrismAlternatingEvenLeg g s j := by
      simpa [standardTypeABoundaryPrismScaledRankCocone,
        standardTypeABoundaryPrismAlternatingDesc,
        standardTypeABoundaryPrismRankCoconeOfAlternatingCocone] using
          (standardTypeABoundaryPrismScaledRankCoconeIsColimit g).fac
            (standardTypeABoundaryPrismRankCoconeOfAlternatingCocone g s) j
    simpa [standardTypeABoundaryPrismScaledRankCocone] using
      hleft.trans hright.symm

/-! ## One raw transfinite composition from the boundary prism to the cylinder -/

/-- The complete boundary-prism inclusion is a single natural-number
transfinite composition whose every successor is a raw standard A/B cellular
step. -/
noncomputable def standardTypeABoundaryPrismRawTransfiniteComposition
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    MorphismProperty.TransfiniteCompositionOfShape
      (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u}))
      ℕ (standardTypeABoundaryPrismToCylinder g) where
  F := standardTypeABoundaryPrismAlternatingFunctor g
  isoBot := eqToIso (by
    simp [standardTypeABoundaryPrismAlternatingFunctor,
      standardTypeABoundaryPrismAlternatingObj,
      standardTypeABoundaryPrismRankStage_zero])
  incl := (standardTypeABoundaryPrismAlternatingCocone g).ι
  isColimit := standardTypeABoundaryPrismAlternatingCoconeIsColimit g
  fac := by
    apply ScaledSSet.ScaledMap.ext
    simp [standardTypeABoundaryPrismAlternatingCocone,
      standardTypeABoundaryPrismAlternatingToCylinder,
      standardTypeABoundaryPrismAlternatingFunctor,
      standardTypeABoundaryPrismAlternatingObj,
      Nat.bitCasesOn, Nat.bitCasesOn_bit0,
      standardTypeABoundaryPrismRankStage_zero,
      standardTypeABoundaryPrismRankStageToCylinder,
      standardTypeABoundaryPrismToCylinder]
  map_mem j _ := by
    simpa [standardTypeABoundaryPrismAlternatingFunctor] using
      standardTypeABoundaryPrismAlternatingStep_mem_rawCellular g j

/-- Strong unretracted cellularity of the entire boundary-prism inclusion. -/
theorem standardTypeABoundaryPrismToCylinder_mem_strongCellular
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardABCStrongCellularClosure.{u}
      (standardTypeABoundaryPrismToCylinder.{u} g) := by
  simpa only [standardABCStrongCellularClosure] using
    (MorphismProperty.transfiniteCompositionsOfShape_le_transfiniteCompositions
      (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u})) _ _
      ((standardTypeABoundaryPrismRawTransfiniteComposition g).ofOrderIso
        (orderIsoShrink.{u} ℕ).symm).mem)

/-- Consequently the full boundary-prism inclusion lies in the exact v1.59
standard A/B/C cellular closure. -/
theorem standardTypeABoundaryPrismToCylinder_mem_cellular
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardABCCellularClosure
      (standardTypeABoundaryPrismToCylinder g) :=
  standardABCStrongCellularClosure_le_standardABCCellularClosure _
    (standardTypeABoundaryPrismToCylinder_mem_strongCellular g)

/-!
The boundary-prism part of the standard endpoint Leibniz problem is now
finished in exactly the cellular language required by v1.59:

```text
A_boundary
  -- R_0 -> A_0 -> R_1 -> A_1 -> ... -->
Delta[n] x Delta[1]
```

is one raw transfinite composition of pushouts of coproducts of literal
standard A/B generators.

The only remaining geometric map in the endpoint factorization is

```text
A_epsilon -> A_boundary,
```

the single missing opposite-endpoint copy of the same type-(A) horn identified
in v1.60.  Once that map is put in the raw standard class, composition with the
theorem above and
`standardTypeAEndpointLeibniz_factor_boundaryPrism` produces the v1.59
`StandardABCTypeAEndpointLeibnizCellularCertificate`.
-/

end

end KUOS.DependentOriginationStandardTypeABoundaryPrismRawTransfiniteV1_76
