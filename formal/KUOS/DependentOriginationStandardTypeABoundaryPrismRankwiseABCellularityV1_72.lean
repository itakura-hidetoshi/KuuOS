import KUOS.DependentOriginationStandardTypeABoundaryPrismScaledRankFiltrationV1_71

namespace KUOS.DependentOriginationStandardTypeABoundaryPrismRankwiseABCellularityV1_72

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Limits
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationStandardTypeBScalingPushoutV1_56
open KUOS.DependentOriginationStandardTypeBThreeSimplexCompletionV1_57
open KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58
open KUOS.DependentOriginationStandardABCLeibnizCellularComparisonV1_59
open KUOS.DependentOriginationStandardTypeABoundaryPrismRelativeCellV1_61
open KUOS.DependentOriginationStandardTypeABoundaryPrismScaledCellsV1_62
open KUOS.DependentOriginationStandardTypeABoundaryPrismCellPushoutCriterionV1_65
open KUOS.DependentOriginationStandardTypeABoundaryPrismCellACompatibilityV1_66
open KUOS.DependentOriginationStandardTypeABoundaryPrismCellwiseABClassificationV1_70
open KUOS.DependentOriginationStandardTypeABoundaryPrismScaledRankFiltrationV1_71

universe u

noncomputable section

/-!
# Rankwise A/B cellularity of the standard type-(A) boundary prism v1.72

The local geometry established in v1.65--v1.71 is consumed here in the
morphism-property calculus.  Every exact rank cell is a standard type-(A)
cobase change followed either by no scaling completion, or by exactly one of
the q12/q23 type-(B) completions.  The two phases are placed in the raw
standard A/B/C cellular class and hence in its transfinite closure.
-/

/-- One raw standard cellular step: a pushout of a coproduct of standard
A/B/C generators. -/
def standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u}) :=
  (MorphismProperty.coproducts.{u}
    (standardScaledAnodyneGeneratorsABC :
      MorphismProperty (ScaledSSet.{u}))).pushouts

/-- The strong, unretracted standard cellular closure. -/
def standardABCStrongCellularClosure : MorphismProperty (ScaledSSet.{u}) :=
  MorphismProperty.transfiniteCompositions.{u}
    (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u}))

/-- The strong cellular closure is contained in the v1.59 cellular closure by
the final retract operation. -/
theorem standardABCStrongCellularClosure_le_standardABCCellularClosure :
    (standardABCStrongCellularClosure : MorphismProperty (ScaledSSet.{u})) ≤
      standardABCCellularClosure := by
  intro X Y f hf
  exact MorphismProperty.le_retracts
    (MorphismProperty.transfiniteCompositions.{u}
      (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u}))) f hf

/-! ## Cellwise A phase -/

/-- The A phase of every exact boundary-prism cell is a pushout of one standard
type-(A) generator. -/
theorem standardTypeABoundaryPrismCellAPushoutHom_mem_rawCellular
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    standardABCRawCellularStep
      (standardTypeABoundaryPrismCellAPushoutHom g j c) := by
  let P : MorphismProperty (ScaledSSet.{u}) :=
    MorphismProperty.coproducts.{u}
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u}))
  have hgen :
      P (standardTypeAScaledHornGeneratorHom
        (standardTypeABoundaryPrismCellHornIndex g j c)) :=
    MorphismProperty.le_coproducts
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u})) _
      (standardTypeAGenerator_mem_ABC
        (standardTypeABoundaryPrismCellHornIndex g j c))
  rw [← standardTypeABoundaryPrismCellA_lowerMap_eq_generator g j c] at hgen
  change P.pushouts (standardTypeABoundaryPrismCellAPushoutHom g j c)
  exact P.pushouts_mk
    (standardTypeABoundaryPrismCellA_genericPushout g j c
      (standardTypeABoundaryPrismCellACompatible_all g j c)).flip
    hgen

/-! ## Fixed B completions -/

/-- The fixed q12 completion is a raw standard cellular step. -/
theorem standardTypeBCollapse12CompletionHom_mem_rawCellular :
    standardABCRawCellularStep
      (standardTypeBCollapse12CompletionHom :
        ScaledSSet.{u} ⟶ ScaledSSet.{u}) := by
  let P : MorphismProperty (ScaledSSet.{u}) :=
    MorphismProperty.coproducts.{u}
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u}))
  have hB : P (standardTypeBGeneratorHom : ScaledSSet.{u} ⟶ ScaledSSet.{u}) :=
    MorphismProperty.le_coproducts
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u})) _
      standardTypeBGenerator_mem_ABC
  change P.pushouts
    (standardTypeBCollapse12CompletionHom : ScaledSSet.{u} ⟶ ScaledSSet.{u})
  exact P.pushouts_mk standardTypeBCollapse12Completion_isPushout hB

/-- The fixed q23 completion is a raw standard cellular step. -/
theorem standardTypeBCollapse23CompletionHom_mem_rawCellular :
    standardABCRawCellularStep
      (standardTypeBCollapse23CompletionHom :
        ScaledSSet.{u} ⟶ ScaledSSet.{u}) := by
  let P : MorphismProperty (ScaledSSet.{u}) :=
    MorphismProperty.coproducts.{u}
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u}))
  have hB : P (standardTypeBGeneratorHom : ScaledSSet.{u} ⟶ ScaledSSet.{u}) :=
    MorphismProperty.le_coproducts
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u})) _
      standardTypeBGenerator_mem_ABC
  change P.pushouts
    (standardTypeBCollapse23CompletionHom : ScaledSSet.{u} ⟶ ScaledSSet.{u})
  exact P.pushouts_mk standardTypeBCollapse23Completion_isPushout hB

/-! ## Equality and three-simplex transport -/

/-- Equality of scalings on a fixed carrier gives the canonical identity
isomorphism after equality elimination. -/
def scalingEqualityIso
    {X : SSet.{u}}
    (s t : ScaledSimplicialSet X)
    (h : s = t) :
    ScaledSSet.of X s ≅ ScaledSSet.of X t := by
  cases h
  exact Iso.refl _

@[simp]
theorem scalingEqualityIso_hom_map
    {X : SSet.{u}}
    (s t : ScaledSimplicialSet X)
    (h : s = t) :
    (scalingEqualityIso s t h).hom.map = 𝟙 X := by
  cases h
  rfl

@[simp]
theorem scalingEqualityIso_inv_map
    {X : SSet.{u}}
    (s t : ScaledSimplicialSet X)
    (h : s = t) :
    (scalingEqualityIso s t h).inv.map = 𝟙 X := by
  cases h
  rfl

/-- Canonical carrier/scaling isomorphism from an actual three-cell to the
fixed three-simplex used by the q12/q23 tables. -/
noncomputable def standardTypeABoundaryPrismCellScalingIsoToThree
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h3 : c.dim + 1 = 3)
    (s : ScaledSimplicialSet (Δ[c.dim + 1] : SSet.{u})) :
    ScaledSSet.of (Δ[c.dim + 1] : SSet.{u}) s ≅
      ScaledSSet.of (Δ[3] : SSet.{u})
        (standardTypeABoundaryPrismTransportScalingToThree g j c h3 s) := by
  cases h3
  exact Iso.refl _

/-- Transport the identity-underlying completion arrow itself to the fixed
three-simplex carrier. -/
noncomputable def standardTypeABoundaryPrismCellCompletionTransportToThree
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h3 : c.dim + 1 = 3) :
    ScaledSSet.of (Δ[3] : SSet.{u})
        (standardTypeABoundaryPrismTransportScalingToThree g j c h3
          (standardTypeABoundaryPrismCellAPushoutScaling g j c)) ⟶
      ScaledSSet.of (Δ[3] : SSet.{u})
        (standardTypeABoundaryPrismTransportScalingToThree g j c h3
          (standardTypeABoundaryPrismCellScaling g j c)) := by
  cases h3
  exact standardTypeABoundaryPrismCellCompletionHom g j c

/-- The dependent completion arrow and its fixed-three-simplex transport are
isomorphic as arrows. -/
noncomputable def standardTypeABoundaryPrismCellCompletionArrowIsoToThree
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h3 : c.dim + 1 = 3) :
    Arrow.mk (standardTypeABoundaryPrismCellCompletionHom g j c) ≅
      Arrow.mk
        (standardTypeABoundaryPrismCellCompletionTransportToThree g j c h3) := by
  cases h3
  exact Iso.refl _

/-! ## Exceptional q12/q23 cells -/

noncomputable def standardTypeABoundaryPrismCellQ12SourceIso
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h : StandardTypeABoundaryPrismCellQ12Factorization g j c) :
    standardTypeABoundaryPrismCellAPushoutTarget g j c ≅
      ScaledSSet.of (Δ[3] : SSet.{u}) standardTypeBCollapse12BaseScaling :=
  standardTypeABoundaryPrismCellScalingIsoToThree g j c h.target_three
      (standardTypeABoundaryPrismCellAPushoutScaling g j c) ≪≫
    scalingEqualityIso _ _ h.A_base

noncomputable def standardTypeABoundaryPrismCellQ12TargetIso
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h : StandardTypeABoundaryPrismCellQ12Factorization g j c) :
    standardTypeABoundaryPrismScaledCellTarget g j c ≅
      ScaledSSet.of (Δ[3] : SSet.{u}) standardTypeBCollapse12CompletedScaling :=
  standardTypeABoundaryPrismCellScalingIsoToThree g j c h.target_three
      (standardTypeABoundaryPrismCellScaling g j c) ≪≫
    scalingEqualityIso _ _ h.completed_target

noncomputable def standardTypeABoundaryPrismCellQ12CompletionArrowIso
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h : StandardTypeABoundaryPrismCellQ12Factorization g j c) :
    Arrow.mk (standardTypeABoundaryPrismCellCompletionHom g j c) ≅
      Arrow.mk standardTypeBCollapse12CompletionHom := by
  refine Arrow.isoMk
    (standardTypeABoundaryPrismCellQ12SourceIso g j c h)
    (standardTypeABoundaryPrismCellQ12TargetIso g j c h) ?_
  apply ScaledSSet.ScaledMap.ext
  cases h.target_three
  simp [standardTypeABoundaryPrismCellQ12SourceIso,
    standardTypeABoundaryPrismCellQ12TargetIso,
    standardTypeABoundaryPrismCellScalingIsoToThree,
    standardTypeABoundaryPrismCellCompletionHom,
    standardTypeBCollapse12CompletionHom,
    standardTypeBPushoutEnrichment,
    scalingEnrichmentPushoutTargetEnrichment,
    scalingEqualityIso]

noncomputable def standardTypeABoundaryPrismCellQ23SourceIso
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h : StandardTypeABoundaryPrismCellQ23Factorization g j c) :
    standardTypeABoundaryPrismCellAPushoutTarget g j c ≅
      ScaledSSet.of (Δ[3] : SSet.{u}) standardTypeBCollapse23BaseScaling :=
  standardTypeABoundaryPrismCellScalingIsoToThree g j c h.target_three
      (standardTypeABoundaryPrismCellAPushoutScaling g j c) ≪≫
    scalingEqualityIso _ _ h.A_base

noncomputable def standardTypeABoundaryPrismCellQ23TargetIso
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h : StandardTypeABoundaryPrismCellQ23Factorization g j c) :
    standardTypeABoundaryPrismScaledCellTarget g j c ≅
      ScaledSSet.of (Δ[3] : SSet.{u}) standardTypeBCollapse23CompletedScaling :=
  standardTypeABoundaryPrismCellScalingIsoToThree g j c h.target_three
      (standardTypeABoundaryPrismCellScaling g j c) ≪≫
    scalingEqualityIso _ _ h.completed_target

noncomputable def standardTypeABoundaryPrismCellQ23CompletionArrowIso
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h : StandardTypeABoundaryPrismCellQ23Factorization g j c) :
    Arrow.mk (standardTypeABoundaryPrismCellCompletionHom g j c) ≅
      Arrow.mk standardTypeBCollapse23CompletionHom := by
  refine Arrow.isoMk
    (standardTypeABoundaryPrismCellQ23SourceIso g j c h)
    (standardTypeABoundaryPrismCellQ23TargetIso g j c h) ?_
  apply ScaledSSet.ScaledMap.ext
  cases h.target_three
  simp [standardTypeABoundaryPrismCellQ23SourceIso,
    standardTypeABoundaryPrismCellQ23TargetIso,
    standardTypeABoundaryPrismCellScalingIsoToThree,
    standardTypeABoundaryPrismCellCompletionHom,
    standardTypeBCollapse23CompletionHom,
    standardTypeBPushoutEnrichment,
    scalingEnrichmentPushoutTargetEnrichment,
    scalingEqualityIso]

/-- Every q12 exceptional completion is a raw standard cellular step. -/
theorem standardTypeABoundaryPrismCellCompletionHom_mem_rawCellular_of_q12
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h : StandardTypeABoundaryPrismCellQ12Factorization g j c) :
    standardABCRawCellularStep
      (standardTypeABoundaryPrismCellCompletionHom g j c) := by
  change
    (MorphismProperty.coproducts.{u}
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u}))).pushouts
      (standardTypeABoundaryPrismCellCompletionHom g j c)
  exact
    (((MorphismProperty.coproducts.{u}
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u}))).pushouts).arrow_mk_iso_iff
      (standardTypeABoundaryPrismCellQ12CompletionArrowIso g j c h)).2
      standardTypeBCollapse12CompletionHom_mem_rawCellular

/-- Every q23 exceptional completion is a raw standard cellular step. -/
theorem standardTypeABoundaryPrismCellCompletionHom_mem_rawCellular_of_q23
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h : StandardTypeABoundaryPrismCellQ23Factorization g j c) :
    standardABCRawCellularStep
      (standardTypeABoundaryPrismCellCompletionHom g j c) := by
  change
    (MorphismProperty.coproducts.{u}
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u}))).pushouts
      (standardTypeABoundaryPrismCellCompletionHom g j c)
  exact
    (((MorphismProperty.coproducts.{u}
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u}))).pushouts).arrow_mk_iso_iff
      (standardTypeABoundaryPrismCellQ23CompletionArrowIso g j c h)).2
      standardTypeBCollapse23CompletionHom_mem_rawCellular

/-! ## Exact-cell cellularity -/

noncomputable def standardTypeABoundaryPrismCellPureAArrowIso
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h : standardTypeABoundaryPrismCellAPushoutScaling g j c =
      standardTypeABoundaryPrismCellScaling g j c) :
    Arrow.mk (standardTypeABoundaryPrismCellAPushoutHom g j c) ≅
      Arrow.mk (standardTypeABoundaryPrismScaledCellHom g j c) := by
  refine Arrow.isoMk (Iso.refl _) (scalingEqualityIso _ _ h) ?_
  apply ScaledSSet.ScaledMap.ext
  simp [standardTypeABoundaryPrismCellAPushoutHom_map,
    standardTypeABoundaryPrismScaledCellHom_map,
    scalingEqualityIso]

/-- Every exact boundary-prism rank cell lies in the strong unretracted
standard A/B cellular closure. -/
theorem standardTypeABoundaryPrismScaledCellHom_mem_strongCellular
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    standardABCStrongCellularClosure
      (standardTypeABoundaryPrismScaledCellHom g j c) := by
  have hAraw := standardTypeABoundaryPrismCellAPushoutHom_mem_rawCellular g j c
  have hA :
      standardABCStrongCellularClosure
        (standardTypeABoundaryPrismCellAPushoutHom g j c) :=
    MorphismProperty.le_transfiniteCompositions.{u}
      (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u})) _ hAraw
  rcases standardTypeABoundaryPrismCellCompletion_complete_classification
      g j c with hpure | h12 | h23
  · exact
      ((standardABCStrongCellularClosure :
        MorphismProperty (ScaledSSet.{u})).arrow_mk_iso_iff
        (standardTypeABoundaryPrismCellPureAArrowIso g j c hpure)).1 hA
  · have hBraw :=
      standardTypeABoundaryPrismCellCompletionHom_mem_rawCellular_of_q12
        g j c h12
    have hB :
        standardABCStrongCellularClosure
          (standardTypeABoundaryPrismCellCompletionHom g j c) :=
      MorphismProperty.le_transfiniteCompositions.{u}
        (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u})) _ hBraw
    have hcomp :=
      (standardABCStrongCellularClosure : MorphismProperty (ScaledSSet.{u})).comp_mem
        (standardTypeABoundaryPrismCellAPushoutHom g j c)
        (standardTypeABoundaryPrismCellCompletionHom g j c) hA hB
    simpa only [standardTypeABoundaryPrismScaledCellHom_factor_A_completion]
      using hcomp
  · have hBraw :=
      standardTypeABoundaryPrismCellCompletionHom_mem_rawCellular_of_q23
        g j c h23
    have hB :
        standardABCStrongCellularClosure
          (standardTypeABoundaryPrismCellCompletionHom g j c) :=
      MorphismProperty.le_transfiniteCompositions.{u}
        (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u})) _ hBraw
    have hcomp :=
      (standardABCStrongCellularClosure : MorphismProperty (ScaledSSet.{u})).comp_mem
        (standardTypeABoundaryPrismCellAPushoutHom g j c)
        (standardTypeABoundaryPrismCellCompletionHom g j c) hA hB
    simpa only [standardTypeABoundaryPrismScaledCellHom_factor_A_completion]
      using hcomp

/-- Hence every exact boundary-prism rank cell lies in the precise v1.59
standard A/B/C cellular closure. -/
theorem standardTypeABoundaryPrismScaledCellHom_mem_cellular
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    standardABCCellularClosure
      (standardTypeABoundaryPrismScaledCellHom g j c) :=
  standardABCStrongCellularClosure_le_standardABCCellularClosure _
    (standardTypeABoundaryPrismScaledCellHom_mem_strongCellular g j c)

/-- Global index of all exact cells of the natural-number rank filtration. -/
def StandardTypeABoundaryPrismRankCellIndex
    (g : StandardTypeAHornAttachmentGeneratorIndex) : Type u :=
  Σ j : ℕ, (standardTypeABoundaryPrismRankFunction g).Cell j

/-- The complete family of exact pullback-scaled cells occurring anywhere in
the boundary-prism rank filtration. -/
def standardTypeABoundaryPrismExactScaledCellGenerators
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    MorphismProperty (ScaledSSet.{u}) :=
  MorphismProperty.ofHoms
    (fun γ : StandardTypeABoundaryPrismRankCellIndex g =>
      standardTypeABoundaryPrismScaledCellHom g γ.1 γ.2)

/-- Every exact cell in the entire Mathlib rank filtration is standard
A/B/C-cellular. -/
theorem standardTypeABoundaryPrismExactScaledCellGenerators_le_cellular
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardTypeABoundaryPrismExactScaledCellGenerators g :
      MorphismProperty (ScaledSSet.{u})) ≤ standardABCCellularClosure := by
  intro X Y f hf
  cases hf with
  | mk γ =>
      exact standardTypeABoundaryPrismScaledCellHom_mem_cellular
        g γ.1 γ.2

end

end KUOS.DependentOriginationStandardTypeABoundaryPrismRankwiseABCellularityV1_72
