import KUOS.DependentOriginationStandardTypeABoundaryPrismCellwiseABClassificationV1_70

namespace KUOS.DependentOriginationStandardTypeABoundaryPrismScaledRankFiltrationV1_71

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Limits
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledAnodyneAttachmentFactorizationV1_48
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAScaledPushoutSourceEnrichmentV1_53
open KUOS.DependentOriginationStandardTypeAEndpointPrismPairingV1_60
open KUOS.DependentOriginationStandardTypeABoundaryPrismRelativeCellV1_61
open KUOS.DependentOriginationStandardTypeABoundaryPrismScaledCellsV1_62
open KUOS.DependentOriginationStandardTypeABoundaryPrismCellPushoutCriterionV1_65
open KUOS.DependentOriginationStandardTypeABoundaryPrismCellACompatibilityV1_66
open KUOS.DependentOriginationStandardTypeABoundaryPrismCellwiseABClassificationV1_70

universe u

noncomputable section

/-!
# Genuine scaled rank interface for the standard type-(A) boundary prism v1.71

Version v1.70 closed the local geometry of every ordinary Mathlib rank cell:
its exact ambient-scaled attachment is either pure type-(A), or a type-(A)
cobase change followed by exactly one q12/q23 type-(B) completion.

This file starts the global filtration without changing the ordinary carrier.
For every natural-number rank `j` we equip Mathlib's existing filtration
subcomplex with the scaling pulled back from the ambient standard type-(A)
cylinder.  Thus the filtration is now genuinely a diagram in `ScaledSSet`, not
merely an ordinary `SSet` filtration with an informal scaling annotation.

The second part isolates the exact two-phase factorization of every attached
cell:

```text
exact horn source
  -- A cobase change --> A-pushout target
  -- identity-underlying completion --> exact cell target.
```

The first arrow is the actual v1.65 pushout of a standard type-(A) generator.
The second arrow is scaled because v1.66 proves unconditional A-compatibility;
v1.70 classifies it exhaustively as trivial, q12, or q23.  Finally the exact
cell source and target map canonically into consecutive scaled rank stages.

This is the categorical interface needed for the next step: take coproducts of
all A phases at one rank, then coproducts of only the exceptional B phases, and
identify their composite with the ambient rank successor.  No canonical-KuuOS
family is identified with the standard A/B/C family here.
-/

/-! ## Ambient-pullback scaling on every ordinary rank stage -/

/-- The exact scaling on the `j`th ordinary Mathlib rank filtration stage,
pulled back from the standard type-(A) scaled cylinder. -/
def standardTypeABoundaryPrismRankStageScaling
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ) :
    ScaledSimplicialSet
      ((standardTypeABoundaryPrismRankFunction g).filtration j : SSet.{u}) :=
  pullbackScaling
    (scaledSimplexCylinder (standardTypeASimplexScaling g.i)).scaling
    ((standardTypeABoundaryPrismRankFunction g).filtration j).ι

/-- The `j`th genuine scaled rank stage. -/
def standardTypeABoundaryPrismRankStage
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ) : ScaledSSet.{u} :=
  ScaledSSet.of
    ((standardTypeABoundaryPrismRankFunction g).filtration j : SSet.{u})
    (standardTypeABoundaryPrismRankStageScaling g j)

/-- Every scaled rank stage maps canonically to the ambient scaled cylinder. -/
def standardTypeABoundaryPrismRankStageToCylinder
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ) :
    standardTypeABoundaryPrismRankStage g j ⟶
      scaledSimplexCylinder (standardTypeASimplexScaling g.i) where
  map := ((standardTypeABoundaryPrismRankFunction g).filtration j).ι
  scaled := pullbackScaling_map _ _

/-- Monotonicity of the ordinary rank filtration lifts canonically to a scaled
map between the ambient-pullback-scaled stages. -/
def standardTypeABoundaryPrismRankStageHom
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    {j k : ℕ}
    (h : j ≤ k) :
    standardTypeABoundaryPrismRankStage g j ⟶
      standardTypeABoundaryPrismRankStage g k where
  map := SSet.Subcomplex.homOfLE
    ((standardTypeABoundaryPrismRankFunction g).filtration_monotone h)
  scaled := by
    intro t ht
    change
      (scaledSimplexCylinder (standardTypeASimplexScaling g.i)).scaling.thin
        (((standardTypeABoundaryPrismRankFunction g).filtration k).ι.app
          (op ⦋2⦌)
          ((SSet.Subcomplex.homOfLE
            ((standardTypeABoundaryPrismRankFunction g).filtration_monotone h)).app
              (op ⦋2⦌) t))
    rw [← NatTrans.comp_app_apply]
    rw [SSet.Subcomplex.homOfLE_ι]
    exact ht

/-- The scaled stage map is compatible with the common map to the cylinder. -/
theorem standardTypeABoundaryPrismRankStageHom_toCylinder
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    {j k : ℕ}
    (h : j ≤ k) :
    standardTypeABoundaryPrismRankStageHom g h ≫
        standardTypeABoundaryPrismRankStageToCylinder g k =
      standardTypeABoundaryPrismRankStageToCylinder g j := by
  apply ScaledSSet.ScaledMap.ext
  exact SSet.Subcomplex.homOfLE_ι
    ((standardTypeABoundaryPrismRankFunction g).filtration_monotone h)

/-- Rank zero is literally the already-defined scaled boundary prism. -/
theorem standardTypeABoundaryPrismRankStage_zero
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeABoundaryPrismRankStage g 0 =
      standardTypeABoundaryPrism g := by
  unfold standardTypeABoundaryPrismRankStage
  unfold standardTypeABoundaryPrismRankStageScaling
  rw [standardTypeABoundaryPrism_filtration_zero]
  rfl

/-! ## Every exact cell has a canonical A-then-completion factorization -/

/-- After the standard type-(A) cobase change, enrich the scaling by the
identity underlying simplicial map to the exact ambient cell scaling. -/
def standardTypeABoundaryPrismCellCompletionHom
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    standardTypeABoundaryPrismCellAPushoutTarget g j c ⟶
      standardTypeABoundaryPrismScaledCellTarget g j c where
  map := 𝟙 _
  scaled := by
    intro t ht
    exact
      standardTypeABoundaryPrismCellAPushoutScaling_le_cellScaling
        g j c
        (standardTypeABoundaryPrismCellACompatible_all g j c)
        t ht

/-- The exact scaled horn cell factors literally as its standard type-(A)
cobase-change map followed by the scaling-only completion. -/
theorem standardTypeABoundaryPrismScaledCellHom_factor_A_completion
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    standardTypeABoundaryPrismCellAPushoutHom g j c ≫
        standardTypeABoundaryPrismCellCompletionHom g j c =
      standardTypeABoundaryPrismScaledCellHom g j c := by
  apply ScaledSSet.ScaledMap.ext
  change c.horn.ι ≫ 𝟙 _ = c.horn.ι
  simp

/-- The completion phase is exhaustively either trivial, q12, or q23.  This is
the v1.70 local classification repackaged exactly in the form consumed by a
rank-successor construction. -/
theorem standardTypeABoundaryPrismCellCompletion_complete_classification
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    standardTypeABoundaryPrismCellAPushoutScaling g j c =
        standardTypeABoundaryPrismCellScaling g j c ∨
      StandardTypeABoundaryPrismCellQ12Factorization g j c ∨
      StandardTypeABoundaryPrismCellQ23Factorization g j c :=
  standardTypeABoundaryPrism_cell_complete_AB_classification g j c

/-- A convenient predicate selecting precisely the cells that require a
nontrivial type-(B) phase after their standard type-(A) attachment. -/
def standardTypeABoundaryPrismCellNeedsTypeB
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) : Prop :=
  StandardTypeABoundaryPrismCellQ12Factorization g j c ∨
    StandardTypeABoundaryPrismCellQ23Factorization g j c

/-- Every rank cell either finishes after the A phase or belongs to the exact
B-phase subfamily. -/
theorem standardTypeABoundaryPrismCell_pureA_or_needsTypeB
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    standardTypeABoundaryPrismCellAPushoutScaling g j c =
        standardTypeABoundaryPrismCellScaling g j c ∨
      standardTypeABoundaryPrismCellNeedsTypeB g j c := by
  rcases standardTypeABoundaryPrismCellCompletion_complete_classification
      g j c with hA | h12 | h23
  · exact Or.inl hA
  · exact Or.inr (Or.inl h12)
  · exact Or.inr (Or.inr h23)

/-! ## Exact cells map into the consecutive scaled rank stages -/

/-- The actual pullback-scaled horn of a rank cell maps to the current scaled
rank stage.  Scaledness is exactly the statement that both structures are
restrictions of the same ambient cylinder scaling. -/
def standardTypeABoundaryPrismScaledCellSourceToRankStage
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    standardTypeABoundaryPrismScaledCellSource g j c ⟶
      standardTypeABoundaryPrismRankStage g j where
  map := c.mapHorn
  scaled := by
    intro t ht
    change
      (scaledSimplexCylinder (standardTypeASimplexScaling g.i)).scaling.thin
        (((standardTypeABoundaryPrismRankFunction g).filtration j).ι.app
          (op ⦋2⦌) (c.mapHorn.app (op ⦋2⦌) t))
    rw [← NatTrans.comp_app_apply]
    rw [c.mapHorn_ι]
    exact ht

/-- The exact target simplex of a rank cell maps to the next scaled rank stage. -/
def standardTypeABoundaryPrismScaledCellTargetToRankSucc
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    standardTypeABoundaryPrismScaledCellTarget g j c ⟶
      standardTypeABoundaryPrismRankStage g (j + 1) where
  map := c.mapToSucc
  scaled := by
    intro t ht
    have hmap := c.mapToSucc_ι
    rw [Order.succ_eq_add_one] at hmap
    have hcomp :=
      ConcreteCategory.congr_hom
        (congr_app hmap (op ⦋2⦌)) t
    change
      (scaledSimplexCylinder (standardTypeASimplexScaling g.i)).scaling.thin
        (c.map.app (op ⦋2⦌) t) at ht
    change
      (scaledSimplexCylinder (standardTypeASimplexScaling g.i)).scaling.thin
        ((c.mapToSucc ≫
          ((standardTypeABoundaryPrismRankFunction g).filtration (j + 1)).ι).app
            (op ⦋2⦌) t)
    exact hcomp.symm ▸ ht

/-- Pulling the next-stage scaling back along the cell target map recovers
exactly the cell scaling.  This is the key compatibility needed to assemble
rank cells without losing or inventing thin triangles. -/
theorem standardTypeABoundaryPrismRankSuccScaling_pullback_cell
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    pullbackScaling
        (standardTypeABoundaryPrismRankStageScaling g (j + 1))
        c.mapToSucc =
      standardTypeABoundaryPrismCellScaling g j c := by
  apply scaling_eq_of_le_antisymm
  · intro t ht
    have hmap := c.mapToSucc_ι
    rw [Order.succ_eq_add_one] at hmap
    have hcomp :=
      ConcreteCategory.congr_hom
        (congr_app hmap (op ⦋2⦌)) t
    change
      (scaledSimplexCylinder (standardTypeASimplexScaling g.i)).scaling.thin
        ((c.mapToSucc ≫
          ((standardTypeABoundaryPrismRankFunction g).filtration (j + 1)).ι).app
            (op ⦋2⦌) t) at ht
    change
      (scaledSimplexCylinder (standardTypeASimplexScaling g.i)).scaling.thin
        (c.map.app (op ⦋2⦌) t)
    exact hcomp ▸ ht
  · intro t ht
    have hmap := c.mapToSucc_ι
    rw [Order.succ_eq_add_one] at hmap
    have hcomp :=
      ConcreteCategory.congr_hom
        (congr_app hmap (op ⦋2⦌)) t
    change
      (scaledSimplexCylinder (standardTypeASimplexScaling g.i)).scaling.thin
        (c.map.app (op ⦋2⦌) t) at ht
    change
      (scaledSimplexCylinder (standardTypeASimplexScaling g.i)).scaling.thin
        ((c.mapToSucc ≫
          ((standardTypeABoundaryPrismRankFunction g).filtration (j + 1)).ι).app
            (op ⦋2⦌) t)
    exact hcomp.symm ▸ ht

/-!
At this point the ordinary rank filtration has a canonical scaled lift and
every exact rank cell has a literal two-phase factorization compatible with
that lift:

```text
rank stage j
   ^
   | exact horn scaling
   |
cell horn -- standard A pushout --> A-target -- completion --> exact cell
                                                          |
                                                          v
                                                   rank stage (j+1)

completion = identity  or  q12  or  q23.
```

The remaining construction is rankwise rather than cellwise: form the
coproduct of all A phases at rank `j`, then the coproduct of the selected B
completion phases, prove the composite pushout target equals
`standardTypeABoundaryPrismRankStage g (j+1)`, and consume the resulting
natural-number transfinite composition in `standardABCCellularClosure`.
-/

end

end KUOS.DependentOriginationStandardTypeABoundaryPrismScaledRankFiltrationV1_71
