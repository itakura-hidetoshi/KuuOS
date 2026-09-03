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
    standardTypeABoundaryPrismRankStageHom g
      ((standardTypeABoundaryPrismRankFunction g).filtration_monotone.monotone
        (leOfHom f))
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
      t ∈
        (⊤ : ((Δ[g.n] : SSet.{u}) ⊗ Δ[1]).Subcomplex).obj d := by
    simp
  rw [← standardTypeABoundaryPrism_iSup_filtration g] at ht
  simp only [Subfunctor.iSup_obj, Set.mem_iUnion] at ht
  obtain ⟨j, hj⟩ := ht
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
  rw [hx]
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
    have h := congrArg ScaledSSet.ScaledMap.map (hm j)
    simpa [standardTypeABoundaryPrismScaledRankCocone,
      standardTypeABoundaryPrismRankStageToCylinder,
      standardTypeABoundaryPrismScaledRankDesc,
      standardTypeABoundaryPrismUnderlyingRankCocone] using h

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

/-- Successor map of the flattened filtration.  False parity is the raw A
phase; true parity is the raw B phase. -/
noncomputable def standardTypeABoundaryPrismAlternatingStep
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (n : ℕ) :
    standardTypeABoundaryPrismAlternatingObj g n ⟶
      standardTypeABoundaryPrismAlternatingObj g (n + 1) := by
  cases h : Nat.bodd n with
  | false =>
      simpa [standardTypeABoundaryPrismAlternatingObj,
        Nat.bodd_succ, Nat.div2_succ, h] using
        standardTypeABoundaryPrismRankStageToAPhase g (Nat.div2 n)
  | true =>
      simpa [standardTypeABoundaryPrismAlternatingObj,
        Nat.bodd_succ, Nat.div2_succ, h] using
        standardTypeABoundaryPrismRankAPhaseToSucc g (Nat.div2 n)

@[simp]
theorem standardTypeABoundaryPrismAlternatingStep_bit_false
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ) :
    standardTypeABoundaryPrismAlternatingStep g (Nat.bit false j) =
      standardTypeABoundaryPrismRankStageToAPhase g j := by
  simp [standardTypeABoundaryPrismAlternatingStep,
    standardTypeABoundaryPrismAlternatingObj,
    Nat.bodd_succ, Nat.div2_succ]

@[simp]
theorem standardTypeABoundaryPrismAlternatingStep_bit_true
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ) :
    standardTypeABoundaryPrismAlternatingStep g (Nat.bit true j) =
      standardTypeABoundaryPrismRankAPhaseToSucc g j := by
  simp [standardTypeABoundaryPrismAlternatingStep,
    standardTypeABoundaryPrismAlternatingObj,
    Nat.bodd_succ, Nat.div2_succ]

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
    standardABCRawCellularStep
      (standardTypeABoundaryPrismAlternatingStep g n) := by
  cases h : Nat.bodd n with
  | false =>
      simpa [standardTypeABoundaryPrismAlternatingStep,
        standardTypeABoundaryPrismAlternatingObj,
        Nat.bodd_succ, Nat.div2_succ, h] using
        standardTypeABoundaryPrismRankStageToAPhase_mem_rawCellular
          g (Nat.div2 n)
  | true =>
      simpa [standardTypeABoundaryPrismAlternatingStep,
        standardTypeABoundaryPrismAlternatingObj,
        Nat.bodd_succ, Nat.div2_succ, h] using
        standardTypeABoundaryPrismRankAPhaseToSucc_mem_rawCellular
          g (Nat.div2 n)

/-! ## A cocone of the alternating diagram to the full cylinder -/

/-- Canonical map from each flattened stage to the common full cylinder. -/
noncomputable def standardTypeABoundaryPrismAlternatingToCylinder
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (n : ℕ) :
    standardTypeABoundaryPrismAlternatingObj g n ⟶
      scaledSimplexCylinder (standardTypeASimplexScaling g.i) :=
  match h : Nat.bodd n with
  | false => standardTypeABoundaryPrismRankStageToCylinder g (Nat.div2 n)
  | true =>
      standardTypeABoundaryPrismRankAPhaseToSucc g (Nat.div2 n) ≫
        standardTypeABoundaryPrismRankStageToCylinder g (Nat.div2 n + 1)

@[simp]
theorem standardTypeABoundaryPrismAlternatingToCylinder_bit_false
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ) :
    standardTypeABoundaryPrismAlternatingToCylinder g (Nat.bit false j) =
      standardTypeABoundaryPrismRankStageToCylinder g j := by
  simp [standardTypeABoundaryPrismAlternatingToCylinder]

@[simp]
theorem standardTypeABoundaryPrismAlternatingToCylinder_bit_true
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ) :
    standardTypeABoundaryPrismAlternatingToCylinder g (Nat.bit true j) =
      standardTypeABoundaryPrismRankAPhaseToSucc g j ≫
        standardTypeABoundaryPrismRankStageToCylinder g (j + 1) := by
  simp [standardTypeABoundaryPrismAlternatingToCylinder]

/-- Consecutive alternating maps are compatible with the common cylinder map. -/
theorem standardTypeABoundaryPrismAlternatingStep_toCylinder
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (n : ℕ) :
    standardTypeABoundaryPrismAlternatingStep g n ≫
        standardTypeABoundaryPrismAlternatingToCylinder g (n + 1) =
      standardTypeABoundaryPrismAlternatingToCylinder g n := by
  cases h : Nat.bodd n with
  | false =>
      have hc :=
        standardTypeABoundaryPrismRankStageHom_toCylinder g
          (Nat.le_succ (Nat.div2 n))
      simpa [standardTypeABoundaryPrismAlternatingStep,
        standardTypeABoundaryPrismAlternatingToCylinder,
        standardTypeABoundaryPrismAlternatingObj,
        Nat.bodd_succ, Nat.div2_succ, h, ← Category.assoc,
        standardTypeABoundaryPrismRankStep_factor_A_residual] using hc
  | true =>
      simp [standardTypeABoundaryPrismAlternatingStep,
        standardTypeABoundaryPrismAlternatingToCylinder,
        standardTypeABoundaryPrismAlternatingObj,
        Nat.bodd_succ, Nat.div2_succ, h]

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
    standardTypeABoundaryPrismRankStage g j ⟶ s.pt := by
  simpa [standardTypeABoundaryPrismAlternatingFunctor,
    standardTypeABoundaryPrismAlternatingObj] using
    s.ι.app (Nat.bit false j)

/-- Odd A-phase leg of an arbitrary cocone on the alternating diagram. -/
noncomputable def standardTypeABoundaryPrismAlternatingOddLeg
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeABoundaryPrismAlternatingFunctor g))
    (j : ℕ) :
    standardTypeABoundaryPrismRankAPhase g j ⟶ s.pt := by
  simpa [standardTypeABoundaryPrismAlternatingFunctor,
    standardTypeABoundaryPrismAlternatingObj] using
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
  have hA :
      standardTypeABoundaryPrismRankStageToAPhase g j ≫
          standardTypeABoundaryPrismAlternatingOddLeg g s j =
        standardTypeABoundaryPrismAlternatingEvenLeg g s j := by
    simpa [standardTypeABoundaryPrismAlternatingEvenLeg,
      standardTypeABoundaryPrismAlternatingOddLeg,
      standardTypeABoundaryPrismAlternatingFunctor,
      standardTypeABoundaryPrismAlternatingObj,
      standardTypeABoundaryPrismAlternatingStep,
      Nat.bit_val, Nat.mul_succ, Nat.add_assoc] using hA0
  have hB :
      standardTypeABoundaryPrismRankAPhaseToSucc g j ≫
          standardTypeABoundaryPrismAlternatingEvenLeg g s (j + 1) =
        standardTypeABoundaryPrismAlternatingOddLeg g s j := by
    simpa [standardTypeABoundaryPrismAlternatingEvenLeg,
      standardTypeABoundaryPrismAlternatingOddLeg,
      standardTypeABoundaryPrismAlternatingFunctor,
      standardTypeABoundaryPrismAlternatingObj,
      standardTypeABoundaryPrismAlternatingStep,
      Nat.bit_val, Nat.mul_succ, Nat.add_assoc] using hB0
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
  simpa [standardTypeABoundaryPrismAlternatingEvenLeg,
    standardTypeABoundaryPrismAlternatingOddLeg,
    standardTypeABoundaryPrismAlternatingFunctor,
    standardTypeABoundaryPrismAlternatingObj,
    standardTypeABoundaryPrismAlternatingStep,
    Nat.bit_val, Nat.mul_succ, Nat.add_assoc] using h

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
            simpa [standardTypeABoundaryPrismAlternatingCocone,
              standardTypeABoundaryPrismAlternatingToCylinder,
              standardTypeABoundaryPrismAlternatingDesc,
              standardTypeABoundaryPrismRankCoconeOfAlternatingCocone,
              standardTypeABoundaryPrismAlternatingEvenLeg,
              standardTypeABoundaryPrismAlternatingFunctor,
              standardTypeABoundaryPrismAlternatingObj] using
                (standardTypeABoundaryPrismScaledRankCoconeIsColimit g).fac
                  (standardTypeABoundaryPrismRankCoconeOfAlternatingCocone g s) j
        | true =>
            have hr :=
              (standardTypeABoundaryPrismScaledRankCoconeIsColimit g).fac
                (standardTypeABoundaryPrismRankCoconeOfAlternatingCocone g s) (j + 1)
            have hb := standardTypeABoundaryPrismAlternatingOddLeg_eq g s j
            change
              (standardTypeABoundaryPrismRankAPhaseToSucc g j ≫
                standardTypeABoundaryPrismRankStageToCylinder g (j + 1)) ≫
                  standardTypeABoundaryPrismAlternatingDesc g s =
                s.ι.app (Nat.bit true j)
            rw [Category.assoc, hr]
            simpa [standardTypeABoundaryPrismAlternatingEvenLeg,
              standardTypeABoundaryPrismAlternatingOddLeg,
              standardTypeABoundaryPrismAlternatingFunctor,
              standardTypeABoundaryPrismAlternatingObj] using hb
  uniq s m hm := by
    apply (standardTypeABoundaryPrismScaledRankCoconeIsColimit g).hom_ext
    intro j
    have heven := hm (Nat.bit false j)
    have hdesc :=
      (standardTypeABoundaryPrismScaledRankCoconeIsColimit g).fac
        (standardTypeABoundaryPrismRankCoconeOfAlternatingCocone g s) j
    calc
      (standardTypeABoundaryPrismScaledRankCocone g).ι.app j ≫ m =
          standardTypeABoundaryPrismAlternatingEvenLeg g s j := by
            simpa [standardTypeABoundaryPrismScaledRankCocone,
              standardTypeABoundaryPrismAlternatingCocone,
              standardTypeABoundaryPrismAlternatingToCylinder,
              standardTypeABoundaryPrismAlternatingEvenLeg,
              standardTypeABoundaryPrismAlternatingFunctor,
              standardTypeABoundaryPrismAlternatingObj] using heven
      _ = (standardTypeABoundaryPrismScaledRankCocone g).ι.app j ≫
          standardTypeABoundaryPrismAlternatingDesc g s := by
            simpa [standardTypeABoundaryPrismAlternatingDesc,
              standardTypeABoundaryPrismRankCoconeOfAlternatingCocone] using hdesc.symm

/-! ## One raw transfinite composition from the boundary prism to the cylinder -/

/-- The complete boundary-prism inclusion is a single natural-number
transfinite composition whose every successor is a raw standard A/B cellular
step. -/
noncomputable def standardTypeABoundaryPrismRawTransfiniteComposition
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u})).
      TransfiniteCompositionOfShape ℕ
        (standardTypeABoundaryPrismToCylinder g) where
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
      standardTypeABoundaryPrismRankStage_zero,
      standardTypeABoundaryPrismRankStageToCylinder,
      standardTypeABoundaryPrismToCylinder]
  map_mem j _ := by
    simpa [standardTypeABoundaryPrismAlternatingFunctor] using
      standardTypeABoundaryPrismAlternatingStep_mem_rawCellular g j

/-- Strong unretracted cellularity of the entire boundary-prism inclusion. -/
theorem standardTypeABoundaryPrismToCylinder_mem_strongCellular
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardABCStrongCellularClosure
      (standardTypeABoundaryPrismToCylinder g) := by
  change
    (MorphismProperty.transfiniteCompositions.{u}
      (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u})))
        (standardTypeABoundaryPrismToCylinder g)
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