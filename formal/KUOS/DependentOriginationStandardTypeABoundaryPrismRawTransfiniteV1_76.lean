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
open KUOS.DependentOriginationScaledAnodyneAttachmentFactorizationV1_48
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardABCLeibnizCellularComparisonV1_59
open KUOS.DependentOriginationStandardTypeAEndpointPrismPairingV1_60
open KUOS.DependentOriginationStandardTypeABoundaryPrismRelativeCellV1_61
open KUOS.DependentOriginationStandardTypeABoundaryPrismScaledRankFiltrationV1_71
open KUOS.DependentOriginationStandardTypeABoundaryPrismRankwiseABCellularityV1_72
open KUOS.DependentOriginationStandardTypeABoundaryPrismRankwiseSimultaneousAPhaseV1_74
open KUOS.DependentOriginationStandardTypeABoundaryPrismRankwiseSimultaneousBPhaseV1_75

universe u w

noncomputable section


private theorem kuuos_morphism_property_of_heq
    {C : Type u} [Category C] (W : MorphismProperty C)
    {X Y X' Y' : C} {f : X ⟶ Y} {g : X' ⟶ Y'}
    (hx : X = X') (hy : Y = Y') (hfg : HEq f g)
    (hg : W g) : W f := by
  subst X'
  subst Y'
  have e : f = g := eq_of_heq hfg
  simpa [e] using hg

private theorem kuuos_comp_eq_of_heq
    {C : Type u} [Category C]
    {A B D A' B' D' : C}
    {f : A ⟶ B} {g : B ⟶ D} {h : A ⟶ D}
    {f' : A' ⟶ B'} {g' : B' ⟶ D'} {h' : A' ⟶ D'}
    (ha : A = A') (hb : B = B') (hd : D = D')
    (hf : HEq f f') (hg : HEq g g') (hh : HEq h h')
    (heq : f' ≫ g' = h') : f ≫ g = h := by
  subst A'
  subst B'
  subst D'
  have ef : f = f' := eq_of_heq hf
  have eg : g = g' := eq_of_heq hg
  have eh : h = h' := eq_of_heq hh
  simpa [ef, eg, eh] using heq

private theorem kuuos_nat_transfinite_univ
    {C : Type u} [Category C] (W : MorphismProperty C)
    {X Y : C} (f : X ⟶ Y)
    (h : W.TransfiniteCompositionOfShape ℕ f) :
    (MorphismProperty.transfiniteCompositions.{w} W) f := by
  letI : SuccOrder (ULift.{w} ℕ) :=
    SuccOrder.ofOrderIso (ULift.orderIso : ULift.{w} ℕ ≃o ℕ).symm
  exact (MorphismProperty.transfiniteCompositionsOfShape_le_transfiniteCompositions
    (W := W) (ULift.{w} ℕ)) _
      (h.ofOrderIso (ULift.orderIso : ULift.{w} ℕ ≃o ℕ)).mem

private theorem kuuos_mp_heq {α β : Sort u} (h : α = β) (x : α) :
    h.mp x ≍ x := by
  cases h
  rfl

private theorem kuuos_mpr_heq {α β : Sort u} (h : α = β) (x : β) :
    h.mpr x ≍ x := by
  cases h
  rfl


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
    (scaledSimplexCylinder.{u} (standardTypeASimplexScaling g.i))
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
    (t : (scaledSimplexCylinder.{u}
      (standardTypeASimplexScaling g.i)).carrier.obj d) :
    ∃ (j : ℕ)
      (x : (standardTypeABoundaryPrismRankStage g j).carrier.obj d),
      (standardTypeABoundaryPrismRankStageToCylinder g j).map.app d x = t := by
  have hexists : ∃ (j : ℕ),
      t ∈ ((standardTypeABoundaryPrismRankFunction.{u} g).filtration j).obj d := by
    have ht :
        t ∈ (⊤ : (((Δ[g.n] : SSet.{u}) ⊗ Δ[1]).Subcomplex)).obj d := by
      change t ∈ (Set.univ : Set _)
      exact Set.mem_univ t
    rw [← standardTypeABoundaryPrism_iSup_filtration g] at ht
    rw [Subfunctor.iSup_obj] at ht
    exact Set.mem_iUnion.mp ht
  obtain ⟨j, hj⟩ := hexists
  refine ⟨j, ⟨t, hj⟩, ?_⟩
  rfl

/-- A thin triangle of the full cylinder lifts to a thin triangle in some
finite ambient-pullback-scaled rank stage. -/
theorem standardTypeABoundaryPrism_exists_thin_rank_lift
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (t : (scaledSimplexCylinder.{u}
      (standardTypeASimplexScaling g.i)).carrier.obj (op ⦋2⦌))
    (ht : (scaledSimplexCylinder.{u}
      (standardTypeASimplexScaling g.i)).scaling.thin t) :
    ∃ (j : ℕ)
      (x : (standardTypeABoundaryPrismRankStage g j).carrier.obj (op ⦋2⦌)),
      (standardTypeABoundaryPrismRankStage g j).scaling.thin x ∧
      (standardTypeABoundaryPrismRankStageToCylinder g j).map.app
        (op ⦋2⦌) x = t := by
  obtain ⟨j, x, hx⟩ := standardTypeABoundaryPrism_exists_rank_lift g t
  refine ⟨j, x, ?_, hx⟩
  change
    (scaledSimplexCylinder.{u}
      (standardTypeASimplexScaling g.i)).scaling.thin
      ((standardTypeABoundaryPrismRankStageToCylinder.{u} g j).map.app
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
    scaledSimplexCylinder.{u} (standardTypeASimplexScaling g.i) ⟶ s.pt where
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
    have h₁ := congrArg ScaledSSet.ScaledMap.map (hm j)
    change
      (standardTypeABoundaryPrismRelativeCellComplex g).incl.app j ≫ m.map =
        (s.ι.app j).map at h₁
    have h₂ := (standardTypeABoundaryPrismRelativeCellComplex g).isColimit.fac
      (standardTypeABoundaryPrismUnderlyingRankCocone g s) j
    exact h₁.trans h₂.symm

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
  cases n using Nat.bitCasesOn with
  | bit b j =>
      cases b with
      | false =>
          have hsucc : Nat.bit false j + 1 = Nat.bit true j := by
            simp [Nat.bit_val]
          simpa only [hsucc, standardTypeABoundaryPrismAlternatingObj,
            Nat.bodd_bit, Nat.div2_bit] using
              (standardTypeABoundaryPrismRankStageToAPhase.{u} g j)
      | true =>
          have hsucc : Nat.bit true j + 1 = Nat.bit false (j + 1) := by
            simp [Nat.bit_val]
            omega
          simpa only [hsucc, standardTypeABoundaryPrismAlternatingObj,
            Nat.bodd_bit, Nat.div2_bit] using
              (standardTypeABoundaryPrismRankAPhaseToSucc.{u} g j)

@[simp]
theorem standardTypeABoundaryPrismAlternatingStep_bit_false
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ) :
    HEq (standardTypeABoundaryPrismAlternatingStep g (Nat.bit false j))
      (standardTypeABoundaryPrismRankStageToAPhase g j) := by
  simp only [standardTypeABoundaryPrismAlternatingStep, Nat.bitCasesOn_bit]
  exact kuuos_mpr_heq _ _

@[simp]
theorem standardTypeABoundaryPrismAlternatingStep_bit_true
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ) :
    HEq (standardTypeABoundaryPrismAlternatingStep g (Nat.bit true j))
      (standardTypeABoundaryPrismRankAPhaseToSucc g j) := by
  simp only [standardTypeABoundaryPrismAlternatingStep, Nat.bitCasesOn_bit]
  exact kuuos_mpr_heq _ _

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
      (standardTypeABoundaryPrismAlternatingStep g n)  := by
  cases n using Nat.bitCasesOn with
  | bit b j =>
      cases b with
      | false =>
          have hi : Nat.bit false j + 1 = Nat.bit true j := by
            simp [Nat.bit_val]
          have hx :=
            standardTypeABoundaryPrismAlternatingObj_bit_false g j
          have hy :
              standardTypeABoundaryPrismAlternatingObj g (Nat.bit false j + 1) =
                standardTypeABoundaryPrismRankAPhase g j := by
            simpa only [hi] using
              (standardTypeABoundaryPrismAlternatingObj_bit_true g j)
          exact kuuos_morphism_property_of_heq
            standardABCRawCellularStep
            hx hy
            (standardTypeABoundaryPrismAlternatingStep_bit_false g j)
            (standardTypeABoundaryPrismRankStageToAPhase_mem_rawCellular g j)
      | true =>
          have hi : Nat.bit true j + 1 = Nat.bit false (j + 1) := by
            simp [Nat.bit_val]
            omega
          have hx :=
            standardTypeABoundaryPrismAlternatingObj_bit_true g j
          have hy :
              standardTypeABoundaryPrismAlternatingObj g (Nat.bit true j + 1) =
                standardTypeABoundaryPrismRankStage g (j + 1) := by
            simpa only [hi] using
              (standardTypeABoundaryPrismAlternatingObj_bit_false g (j + 1))
          exact kuuos_morphism_property_of_heq
            standardABCRawCellularStep
            hx hy
            (standardTypeABoundaryPrismAlternatingStep_bit_true g j)
            (standardTypeABoundaryPrismRankAPhaseToSucc_mem_rawCellular g j)

/-! ## A cocone of the alternating diagram to the full cylinder -/

/-- Canonical map from each flattened stage to the common full cylinder. -/
noncomputable def standardTypeABoundaryPrismAlternatingToCylinder
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (n : ℕ) :
    standardTypeABoundaryPrismAlternatingObj g n ⟶
      scaledSimplexCylinder.{u} (standardTypeASimplexScaling g.i) :=
by
  cases n using Nat.bitCasesOn with
  | bit b j =>
      cases b with
      | false =>
          simpa only [standardTypeABoundaryPrismAlternatingObj_bit_false] using
            (standardTypeABoundaryPrismRankStageToCylinder g j)
      | true =>
          simpa only [standardTypeABoundaryPrismAlternatingObj_bit_true] using
            (standardTypeABoundaryPrismRankAPhaseToSucc g j ≫
              standardTypeABoundaryPrismRankStageToCylinder g (j + 1))

@[simp]
theorem standardTypeABoundaryPrismAlternatingToCylinder_bit_false
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ) :
    HEq (standardTypeABoundaryPrismAlternatingToCylinder g (Nat.bit false j))
      (standardTypeABoundaryPrismRankStageToCylinder g j) := by
  simp [standardTypeABoundaryPrismAlternatingToCylinder]

@[simp]
theorem standardTypeABoundaryPrismAlternatingToCylinder_bit_true
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ) :
    HEq (standardTypeABoundaryPrismAlternatingToCylinder g (Nat.bit true j))
      (standardTypeABoundaryPrismRankAPhaseToSucc g j ≫
        standardTypeABoundaryPrismRankStageToCylinder g (j + 1)) := by
  simp [standardTypeABoundaryPrismAlternatingToCylinder]

/-- Consecutive alternating maps are compatible with the common cylinder map. -/
theorem standardTypeABoundaryPrismAlternatingStep_toCylinder
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (n : ℕ) :
    standardTypeABoundaryPrismAlternatingStep g n ≫
        standardTypeABoundaryPrismAlternatingToCylinder g (n + 1) =
      standardTypeABoundaryPrismAlternatingToCylinder g n  := by
  cases n using Nat.bitCasesOn with
  | bit b j =>
      cases b with
      | false =>
          have hi : Nat.bit false j + 1 = Nat.bit true j := by
            simp [Nat.bit_val]
          have hx :=
            standardTypeABoundaryPrismAlternatingObj_bit_false g j
          have hy :
              standardTypeABoundaryPrismAlternatingObj g (Nat.bit false j + 1) =
                standardTypeABoundaryPrismRankAPhase g j := by
            simpa only [hi] using
              (standardTypeABoundaryPrismAlternatingObj_bit_true g j)
          have hg : HEq
              (standardTypeABoundaryPrismAlternatingToCylinder g (Nat.bit false j + 1))
              (standardTypeABoundaryPrismRankAPhaseToSucc g j ≫
                standardTypeABoundaryPrismRankStageToCylinder g (j + 1)) := by
            simpa only [hi] using
              (standardTypeABoundaryPrismAlternatingToCylinder_bit_true g j)
          have hc :
              standardTypeABoundaryPrismRankStageToAPhase g j ≫
                  (standardTypeABoundaryPrismRankAPhaseToSucc g j ≫
                    standardTypeABoundaryPrismRankStageToCylinder g (j + 1)) =
                standardTypeABoundaryPrismRankStageToCylinder g j := by
            rw [← Category.assoc, standardTypeABoundaryPrismRankStep_factor_A_residual]
            exact standardTypeABoundaryPrismRankStageHom_toCylinder g (Nat.le_succ j)
          exact kuuos_comp_eq_of_heq hx hy rfl
            (standardTypeABoundaryPrismAlternatingStep_bit_false g j)
            hg
            (standardTypeABoundaryPrismAlternatingToCylinder_bit_false g j) hc
      | true =>
          have hi : Nat.bit true j + 1 = Nat.bit false (j + 1) := by
            simp [Nat.bit_val]
            omega
          have hx := standardTypeABoundaryPrismAlternatingObj_bit_true g j
          have hy :
              standardTypeABoundaryPrismAlternatingObj g (Nat.bit true j + 1) =
                standardTypeABoundaryPrismRankStage g (j + 1) := by
            simpa only [hi] using
              (standardTypeABoundaryPrismAlternatingObj_bit_false g (j + 1))
          have hg : HEq
              (standardTypeABoundaryPrismAlternatingToCylinder g (Nat.bit true j + 1))
              (standardTypeABoundaryPrismRankStageToCylinder g (j + 1)) := by
            simpa only [hi] using
              (standardTypeABoundaryPrismAlternatingToCylinder_bit_false g (j + 1))
          exact kuuos_comp_eq_of_heq hx hy rfl
            (standardTypeABoundaryPrismAlternatingStep_bit_true g j)
            hg
            (standardTypeABoundaryPrismAlternatingToCylinder_bit_true g j) rfl

/-- The full cylinder cocone on the single flattened A/B sequence. -/
noncomputable def standardTypeABoundaryPrismAlternatingCocone
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    Cocone (standardTypeABoundaryPrismAlternatingFunctor g) :=
  Cocone.mk
    (scaledSimplexCylinder.{u} (standardTypeASimplexScaling g.i))
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

private theorem kuuos_even_leg_heq
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeABoundaryPrismAlternatingFunctor g))
    (j : ℕ) :
    HEq (standardTypeABoundaryPrismAlternatingEvenLeg g s j)
      (s.ι.app (Nat.bit false j)) := by
  unfold standardTypeABoundaryPrismAlternatingEvenLeg
  simp only [id_eq]
  exact kuuos_mp_heq _ _

private theorem kuuos_odd_leg_heq
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeABoundaryPrismAlternatingFunctor g))
    (j : ℕ) :
    HEq (standardTypeABoundaryPrismAlternatingOddLeg g s j)
      (s.ι.app (Nat.bit true j)) := by
  unfold standardTypeABoundaryPrismAlternatingOddLeg
  simp only [id_eq]
  exact kuuos_mp_heq _ _

private theorem kuuos_evenLeg_A_compat
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeABoundaryPrismAlternatingFunctor g))
    (j : ℕ) :
    standardTypeABoundaryPrismRankStageToAPhase g j ≫
        standardTypeABoundaryPrismAlternatingOddLeg g s j =
      standardTypeABoundaryPrismAlternatingEvenLeg g s j := by
  have hi : Nat.bit false j + 1 = Nat.bit true j := by
    simp [Nat.bit_val]
  have ha := (standardTypeABoundaryPrismAlternatingObj_bit_false g j).symm
  have hb :
      standardTypeABoundaryPrismRankAPhase g j =
        standardTypeABoundaryPrismAlternatingObj g (Nat.bit false j + 1) := by
    simpa only [hi] using
      (standardTypeABoundaryPrismAlternatingObj_bit_true g j).symm
  have hg : HEq
      (standardTypeABoundaryPrismAlternatingOddLeg g s j)
      (s.ι.app (Nat.bit false j + 1)) := by
    simpa only [hi] using (kuuos_odd_leg_heq g s j)
  have hw :
      standardTypeABoundaryPrismAlternatingStep g (Nat.bit false j) ≫
          s.ι.app (Nat.bit false j + 1) =
        s.ι.app (Nat.bit false j) := by
    simpa [standardTypeABoundaryPrismAlternatingFunctor] using
      (s.w (homOfLE (Nat.le_add_right (Nat.bit false j) 1)))
  exact kuuos_comp_eq_of_heq ha hb rfl
    (standardTypeABoundaryPrismAlternatingStep_bit_false g j).symm
    hg (kuuos_even_leg_heq g s j) hw

private theorem kuuos_oddLeg_B_compat
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeABoundaryPrismAlternatingFunctor g))
    (j : ℕ) :
    standardTypeABoundaryPrismRankAPhaseToSucc g j ≫
        standardTypeABoundaryPrismAlternatingEvenLeg g s (j + 1) =
      standardTypeABoundaryPrismAlternatingOddLeg g s j := by
  have hi : Nat.bit true j + 1 = Nat.bit false (j + 1) := by
    simp [Nat.bit_val]
    omega
  have ha := (standardTypeABoundaryPrismAlternatingObj_bit_true g j).symm
  have hb :
      standardTypeABoundaryPrismRankStage g (j + 1) =
        standardTypeABoundaryPrismAlternatingObj g (Nat.bit true j + 1) := by
    simpa only [hi] using
      (standardTypeABoundaryPrismAlternatingObj_bit_false g (j + 1)).symm
  have hg : HEq
      (standardTypeABoundaryPrismAlternatingEvenLeg g s (j + 1))
      (s.ι.app (Nat.bit true j + 1)) := by
    simpa only [hi] using (kuuos_even_leg_heq g s (j + 1))
  have hw :
      standardTypeABoundaryPrismAlternatingStep g (Nat.bit true j) ≫
          s.ι.app (Nat.bit true j + 1) =
        s.ι.app (Nat.bit true j) := by
    simpa [standardTypeABoundaryPrismAlternatingFunctor] using
      (s.w (homOfLE (Nat.le_add_right (Nat.bit true j) 1)))
  exact kuuos_comp_eq_of_heq ha hb rfl
    (standardTypeABoundaryPrismAlternatingStep_bit_true g j).symm
    hg (kuuos_odd_leg_heq g s j) hw

/-- The two consecutive raw cocone equations collapse to the exact rank-stage
successor equation on the even subsequence. -/
theorem standardTypeABoundaryPrismAlternatingEvenLeg_succ
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeABoundaryPrismAlternatingFunctor g))
    (j : ℕ) :
    standardTypeABoundaryPrismRankStageHom g (Nat.le_succ j) ≫
        standardTypeABoundaryPrismAlternatingEvenLeg g s (j + 1) =
      standardTypeABoundaryPrismAlternatingEvenLeg g s j  := by
  rw [← standardTypeABoundaryPrismRankStep_factor_A_residual g j]
  rw [Category.assoc, kuuos_oddLeg_B_compat g s j,
    kuuos_evenLeg_A_compat g s j]

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
      standardTypeABoundaryPrismAlternatingOddLeg g s j  := by
  exact kuuos_oddLeg_B_compat g s j

/-! ## Inserting the A-phases does not change the colimit -/

/-- Universal map induced by an alternating cocone, obtained from its even
rank-subcocone and the scaled rank colimit theorem. -/
noncomputable def standardTypeABoundaryPrismAlternatingDesc
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeABoundaryPrismAlternatingFunctor g)) :
    scaledSimplexCylinder.{u} (standardTypeASimplexScaling g.i) ⟶ s.pt :=
  (standardTypeABoundaryPrismScaledRankCoconeIsColimit g).desc
    (standardTypeABoundaryPrismRankCoconeOfAlternatingCocone g s)

private theorem kuuos_rank_fac
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (s : Cocone (standardTypeABoundaryPrismAlternatingFunctor g))
    (j : ℕ) :
    standardTypeABoundaryPrismRankStageToCylinder g j ≫
        standardTypeABoundaryPrismAlternatingDesc g s =
      standardTypeABoundaryPrismAlternatingEvenLeg g s j := by
  simpa [standardTypeABoundaryPrismScaledRankCocone,
    standardTypeABoundaryPrismAlternatingDesc,
    standardTypeABoundaryPrismRankCoconeOfAlternatingCocone] using
      (standardTypeABoundaryPrismScaledRankCoconeIsColimit g).fac
        (standardTypeABoundaryPrismRankCoconeOfAlternatingCocone g s) j

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
            have hraw :
                standardTypeABoundaryPrismAlternatingToCylinder g (Nat.bit false j) ≫
                    standardTypeABoundaryPrismAlternatingDesc g s =
                  s.ι.app (Nat.bit false j) := by
              exact kuuos_comp_eq_of_heq
                (standardTypeABoundaryPrismAlternatingObj_bit_false g j)
                rfl rfl
                (standardTypeABoundaryPrismAlternatingToCylinder_bit_false g j)
                (HEq.refl _)
                (kuuos_even_leg_heq g s j).symm
                (kuuos_rank_fac g s j)
            simpa [standardTypeABoundaryPrismAlternatingCocone,
              standardTypeABoundaryPrismAlternatingFunctor] using hraw
        | true =>
            have hcomp :
                (standardTypeABoundaryPrismRankAPhaseToSucc g j ≫
                  standardTypeABoundaryPrismRankStageToCylinder g (j + 1)) ≫
                    standardTypeABoundaryPrismAlternatingDesc g s =
                  standardTypeABoundaryPrismAlternatingOddLeg g s j := by
              rw [Category.assoc, kuuos_rank_fac g s (j + 1),
                kuuos_oddLeg_B_compat g s j]
            have hraw :
                standardTypeABoundaryPrismAlternatingToCylinder g (Nat.bit true j) ≫
                    standardTypeABoundaryPrismAlternatingDesc g s =
                  s.ι.app (Nat.bit true j) := by
              exact kuuos_comp_eq_of_heq
                (standardTypeABoundaryPrismAlternatingObj_bit_true g j)
                rfl rfl
                (standardTypeABoundaryPrismAlternatingToCylinder_bit_true g j)
                (HEq.refl _)
                (kuuos_odd_leg_heq g s j).symm hcomp
            simpa [standardTypeABoundaryPrismAlternatingCocone,
              standardTypeABoundaryPrismAlternatingFunctor] using hraw
  uniq s m hm := by
    apply (standardTypeABoundaryPrismScaledRankCoconeIsColimit g).hom_ext
    intro j
    have hraw :
        standardTypeABoundaryPrismAlternatingToCylinder g (Nat.bit false j) ≫ m =
          s.ι.app (Nat.bit false j) := by
      simpa [standardTypeABoundaryPrismAlternatingCocone,
        standardTypeABoundaryPrismAlternatingFunctor] using
          (hm (Nat.bit false j))
    have heven :
        standardTypeABoundaryPrismRankStageToCylinder g j ≫ m =
          standardTypeABoundaryPrismAlternatingEvenLeg g s j := by
      exact kuuos_comp_eq_of_heq
        (standardTypeABoundaryPrismAlternatingObj_bit_false g j).symm
        rfl rfl
        (standardTypeABoundaryPrismAlternatingToCylinder_bit_false g j).symm
        (HEq.refl _)
        (kuuos_even_leg_heq g s j) hraw
    exact heven.trans (kuuos_rank_fac g s j).symm

private def bpObj (g : StandardTypeAHornAttachmentGeneratorIndex)
    (K : (((Δ[g.n] : SSet.{u}) ⊗ Δ[1]).Subcomplex)) : ScaledSSet.{u} :=
  ScaledSSet.of (K : SSet.{u})
    (pullbackScaling
      (scaledSimplexCylinder (standardTypeASimplexScaling g.i)).scaling K.ι)

private def bpIncl (g : StandardTypeAHornAttachmentGeneratorIndex)
    (K : (((Δ[g.n] : SSet.{u}) ⊗ Δ[1]).Subcomplex)) :
    bpObj g K ⟶ scaledSimplexCylinder (standardTypeASimplexScaling g.i) where
  map := K.ι
  scaled := pullbackScaling_map _ _

private theorem bpInclCongr (g : StandardTypeAHornAttachmentGeneratorIndex)
    {K L : (((Δ[g.n] : SSet.{u}) ⊗ Δ[1]).Subcomplex)} (h : K = L) :
    eqToHom (congrArg (bpObj g) h).symm ≫ bpIncl g K = bpIncl g L := by
  cases h
  simp

private theorem v176_rank0_comp (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (eqToHom (standardTypeABoundaryPrismRankStage_zero g).symm :
         standardTypeABoundaryPrism g ⟶ standardTypeABoundaryPrismRankStage g 0) ≫
       standardTypeABoundaryPrismRankStageToCylinder g 0 =
      standardTypeABoundaryPrismToCylinder g := by
  change (eqToHom (congrArg (bpObj g)
      (standardTypeABoundaryPrism_filtration_zero g)).symm) ≫
       bpIncl g ((standardTypeABoundaryPrismRankFunction g).filtration 0) =
      bpIncl g (standardTypeABoundaryPrismSubcomplex g)
  exact bpInclCongr g (standardTypeABoundaryPrism_filtration_zero g)


private theorem v176_alt_zero (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeABoundaryPrismAlternatingObj g 0 =
      standardTypeABoundaryPrismRankStage g 0 := by
  simpa only [show (Nat.bit false 0 : ℕ) = 0 by rfl] using
    standardTypeABoundaryPrismAlternatingObj_bit_false g 0

private theorem v176_toCyl_zero_heq (g : StandardTypeAHornAttachmentGeneratorIndex) :
    HEq (standardTypeABoundaryPrismAlternatingToCylinder g 0)
      (standardTypeABoundaryPrismRankStageToCylinder g 0) := by
  simpa only [show (Nat.bit false 0 : ℕ) = 0 by rfl] using
    standardTypeABoundaryPrismAlternatingToCylinder_bit_false g 0

private theorem v176_comp_of_heq
    {C : Type u} [Category C] {X Y Z : C} (h : X = Y)
    {f : X ⟶ Z} {g : Y ⟶ Z} (hf : HEq f g) :
    eqToHom h.symm ≫ f = g := by
  cases h
  simpa using eq_of_heq hf


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
  isoBot := eqToIso
    ((v176_alt_zero g).trans (standardTypeABoundaryPrismRankStage_zero g))
  incl := (standardTypeABoundaryPrismAlternatingCocone g).ι
  isColimit := standardTypeABoundaryPrismAlternatingCoconeIsColimit g

  fac := by
    change (eqToHom ((v176_alt_zero g).trans
        (standardTypeABoundaryPrismRankStage_zero g)).symm) ≫
          standardTypeABoundaryPrismAlternatingToCylinder g 0 =
        standardTypeABoundaryPrismToCylinder g
    calc
      _ = (eqToHom (standardTypeABoundaryPrismRankStage_zero g).symm) ≫
          ((eqToHom (v176_alt_zero g).symm) ≫
            standardTypeABoundaryPrismAlternatingToCylinder g 0) := by
          simp only [← Category.assoc]
          congr 1
      _ = (eqToHom (standardTypeABoundaryPrismRankStage_zero g).symm) ≫
            standardTypeABoundaryPrismRankStageToCylinder g 0 := by
          rw [v176_comp_of_heq (v176_alt_zero g) (v176_toCyl_zero_heq g)]
      _ = standardTypeABoundaryPrismToCylinder g := v176_rank0_comp g
  map_mem j _ := by
    simpa [standardTypeABoundaryPrismAlternatingFunctor] using
      standardTypeABoundaryPrismAlternatingStep_mem_rawCellular g j

/-- Strong unretracted cellularity of the entire boundary-prism inclusion. -/
theorem standardTypeABoundaryPrismToCylinder_mem_strongCellular
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardABCStrongCellularClosure
      (standardTypeABoundaryPrismToCylinder g)  := by
  exact kuuos_nat_transfinite_univ
    standardABCRawCellularStep
    (standardTypeABoundaryPrismToCylinder g)
    (standardTypeABoundaryPrismRawTransfiniteComposition g)

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
