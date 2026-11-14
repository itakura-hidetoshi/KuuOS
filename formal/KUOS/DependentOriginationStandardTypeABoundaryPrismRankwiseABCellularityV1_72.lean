import KUOS.DependentOriginationStandardTypeABoundaryPrismScaledRankFiltrationV1_71

namespace KUOS.DependentOriginationStandardTypeABoundaryPrismRankwiseABCellularityV1_72

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Limits
open HomotopicalAlgebra
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

Version v1.71 lifted the ordinary Mathlib rank filtration to genuine
ambient-pullback-scaled stages and factored every exact rank cell as

```text
exact horn -- A cobase change --> A-target -- completion --> exact cell.
```

Version v1.70 had already proved that the completion is exhaustively one of

```text
identity, q12, q23.
```

This file converts that geometric classification into the *same cellular
language* used by the v1.59 endpoint certificate.  The important point is that
we do not replace the Mathlib rank filtration and we do not identify the
canonical KuuOS arbitrary-scaling generator family with the standard A/B/C
family.

We isolate the unretracted cellular core

```text
transfiniteCompositions (pushouts (coproducts E_std))
```

and prove:

* every cellwise A phase is one raw standard cellular step;
* q12 and q23 are one raw standard cellular step because they are literal
  pushouts of the standard type-(B) generator;
* transport from a dependent three-cell carrier to the fixed `Delta[3]`
  preserves the completion arrow up to an explicit arrow isomorphism;
* therefore every exact rank cell is a finite transfinite composite of raw
  standard A/B steps;
* consequently the entire rank-indexed exact cell family lands in the v1.59
  `standardABCCellularClosure`.

After this theorem no local q12/q23 calculation is allowed to reappear in the
global rank assembly: the remaining frontier is purely the simultaneous
rank-successor pushout and its natural-number transfinite composition.
-/

/-! ## The raw and strong standard cellular classes -/

/-- One raw standard cellular step: a pushout of a coproduct of standard
A/B/C generators. -/
@[reducible] def standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u}) :=
  (MorphismProperty.coproducts.{u, u, u + 1}
    (standardScaledAnodyneGeneratorsABC :
      MorphismProperty (ScaledSSet.{u}))).pushouts

/-- The strong, unretracted standard cellular closure. -/
@[reducible] def standardABCStrongCellularClosure : MorphismProperty (ScaledSSet.{u}) :=
  MorphismProperty.transfiniteCompositions.{u, u, u + 1}
    (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u}))

/-- The strong cellular closure is contained in the v1.59 cellular closure by
the final retract operation. -/
theorem standardABCStrongCellularClosure_le_standardABCCellularClosure :
    (standardABCStrongCellularClosure : MorphismProperty (ScaledSSet.{u})) ≤
      standardABCCellularClosure := by
  intro X Y f hf
  exact MorphismProperty.le_retracts
    (MorphismProperty.transfiniteCompositions.{u, u, u + 1}
      (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u}))) f hf

/-! ## Every cellwise A phase is one raw standard cellular step -/

/-- The A phase of every exact boundary-prism cell is a pushout of one standard
type-(A) generator, hence already belongs to the raw standard cellular class. -/
theorem standardTypeABoundaryPrismCellAPushoutHom_mem_rawCellular
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j) :
    standardABCRawCellularStep
      (standardTypeABoundaryPrismCellAPushoutHom g j c) := by
  have hgen :
      (MorphismProperty.coproducts.{u, u, u + 1}
        (standardScaledAnodyneGeneratorsABC :
          MorphismProperty (ScaledSSet.{u})))
        (standardTypeAScaledHornGeneratorHom
          (standardTypeABoundaryPrismCellHornIndex g j c)) :=
    MorphismProperty.le_coproducts
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u})) _
      (standardTypeAGenerator_mem_ABC
        (standardTypeABoundaryPrismCellHornIndex g j c))
  rw [← standardTypeABoundaryPrismCellA_lowerMap_eq_generator g j c] at hgen
  exact
    (MorphismProperty.coproducts.{u, u, u + 1}
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u}))).pushouts_mk
      (standardTypeABoundaryPrismCellA_genericPushout g j c
        (standardTypeABoundaryPrismCellACompatible_all g j c)).flip
      hgen

/-! ## The two fixed B completions are also raw standard cellular steps -/

/-- The fixed q12 completion is literally a pushout of the standard type-(B)
generator. -/
theorem standardTypeBCollapse12CompletionHom_mem_rawCellular :
    standardABCRawCellularStep standardTypeBCollapse12CompletionHom.{u} := by
  have hB :
      (MorphismProperty.coproducts.{u, u, u + 1}
        (standardScaledAnodyneGeneratorsABC :
          MorphismProperty (ScaledSSet.{u}))) standardTypeBGeneratorHom :=
    MorphismProperty.le_coproducts
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u})) _
      standardTypeBGenerator_mem_ABC
  exact
    (MorphismProperty.coproducts.{u, u, u + 1}
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u}))).pushouts_mk
      standardTypeBCollapse12Completion_isPushout hB

/-- The fixed q23 completion is literally a pushout of the standard type-(B)
generator. -/
theorem standardTypeBCollapse23CompletionHom_mem_rawCellular :
    standardABCRawCellularStep standardTypeBCollapse23CompletionHom.{u} := by
  have hB :
      (MorphismProperty.coproducts.{u, u, u + 1}
        (standardScaledAnodyneGeneratorsABC :
          MorphismProperty (ScaledSSet.{u}))) standardTypeBGeneratorHom :=
    MorphismProperty.le_coproducts
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u})) _
      standardTypeBGenerator_mem_ABC
  exact
    (MorphismProperty.coproducts.{u, u, u + 1}
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u}))).pushouts_mk
      standardTypeBCollapse23Completion_isPushout hB

/-! ## Explicit carrier/scaling isomorphisms for the exceptional three-cells -/

/-- Equality of two scalings on a fixed carrier gives an isomorphism whose
underlying simplicial maps are literally identities.  Keeping this constructor
explicit avoids allowing equality transports to pollute the later arrow
comparison. -/
noncomputable def scalingEqualityIso
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

/-- Transport scalings across a free simplex dimension, before fixing a dependent cell. -/
private noncomputable def scalingTransportIsoToThree
    {n : ℕ} (h3 : n = 3)
    (s : ScaledSimplicialSet (Δ[n] : SSet.{u})) :
    ScaledSSet.of (Δ[n] : SSet.{u}) s ≅
      ScaledSSet.of (Δ[3] : SSet.{u})
        (Eq.mp
          (congrArg (fun d : ℕ => ScaledSimplicialSet (Δ[d] : SSet.{u})) h3) s) := by
  cases h3
  exact Iso.refl _

/-- In a freely varying dimension, transporting the simplex carrier to
dimension three has the same underlying inverse map for every scaling. -/
private theorem scalingTransportIsoToThree_inv_map_eq
    {n : ℕ} (h3 : n = 3)
    (s t : ScaledSimplicialSet (Δ[n] : SSet.{u})) :
    (scalingTransportIsoToThree h3 s).inv.map =
      (scalingTransportIsoToThree h3 t).inv.map := by
  cases h3
  rfl

/-- Transport a scaled map along a dimension equality without eliminating the cell. -/
private noncomputable def scalingHomTransportToThree
    {n : ℕ} (h3 : n = 3)
    {s t : ScaledSimplicialSet (Δ[n] : SSet.{u})}
    (f : ScaledSSet.of (Δ[n] : SSet.{u}) s ⟶
      ScaledSSet.of (Δ[n] : SSet.{u}) t) :
    ScaledSSet.of (Δ[3] : SSet.{u})
        (Eq.mp
          (congrArg (fun d : ℕ => ScaledSimplicialSet (Δ[d] : SSet.{u})) h3) s) ⟶
      ScaledSSet.of (Δ[3] : SSet.{u})
        (Eq.mp
          (congrArg (fun d : ℕ => ScaledSimplicialSet (Δ[d] : SSet.{u})) h3) t) := by
  cases h3
  exact f

private theorem scalingHomTransportToThree_map_id
    {n : ℕ} (h3 : n = 3)
    {s t : ScaledSimplicialSet (Δ[n] : SSet.{u})}
    (f : ScaledSSet.of (Δ[n] : SSet.{u}) s ⟶
      ScaledSSet.of (Δ[n] : SSet.{u}) t)
    (hf : f.map = 𝟙 _) :
    (scalingHomTransportToThree h3 f).map = 𝟙 _ := by
  cases h3
  exact hf

private noncomputable def scalingHomTransportArrowIsoToThree
    {n : ℕ} (h3 : n = 3)
    {s t : ScaledSimplicialSet (Δ[n] : SSet.{u})}
    (f : ScaledSSet.of (Δ[n] : SSet.{u}) s ⟶
      ScaledSSet.of (Δ[n] : SSet.{u}) t) :
    Arrow.mk f ≅ Arrow.mk (scalingHomTransportToThree h3 f) := by
  cases h3
  exact Iso.refl _

/-- Equal scalings plus equal underlying maps yield a genuine arrow isomorphism. -/
private noncomputable def scalingIdentityArrowIso
    {X : SSet.{u}}
    {s₁ s₂ t₁ t₂ : ScaledSimplicialSet X}
    (hs : s₁ = s₂) (ht : t₁ = t₂)
    (f : ScaledSSet.of X s₁ ⟶ ScaledSSet.of X t₁)
    (g : ScaledSSet.of X s₂ ⟶ ScaledSSet.of X t₂)
    (hf : f.map = 𝟙 X) (hg : g.map = 𝟙 X) :
    Arrow.mk f ≅ Arrow.mk g := by
  cases hs
  cases ht
  have hfg : f = g := by
    apply ScaledSSet.ScaledMap.ext
    exact hf.trans hg.symm
  cases hfg
  exact Iso.refl _

/-- One-shot isomorphism from a dependent actual three-cell carrier to the
fixed `Delta[3]` carrier carrying the v1.70 transported scaling. -/
noncomputable def standardTypeABoundaryPrismCellScalingIsoToThree
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
    (h3 : c.dim + 1 = 3)
    (s : ScaledSimplicialSet (Δ[c.dim + 1] : SSet.{u})) :
    ScaledSSet.of (Δ[c.dim + 1] : SSet.{u}) s ≅
      ScaledSSet.of (Δ[3] : SSet.{u})
        (standardTypeABoundaryPrismTransportScalingToThree g j c h3 s) :=
  scalingTransportIsoToThree h3 s

/-- Carrier transport to the fixed three-simplex is independent of the
scaling: source and target inverse maps have the same underlying simplicial map. -/
theorem standardTypeABoundaryPrismCellScalingIsoToThree_inv_map_eq
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
    (h3 : c.dim + 1 = 3)
    (s t : ScaledSimplicialSet (Δ[c.dim + 1] : SSet.{u})) :
    (standardTypeABoundaryPrismCellScalingIsoToThree g j c h3 s).inv.map =
      (standardTypeABoundaryPrismCellScalingIsoToThree g j c h3 t).inv.map :=
  scalingTransportIsoToThree_inv_map_eq h3 s t

/-- Transport the identity-underlying completion arrow itself to the fixed
three-simplex carrier. -/
noncomputable def standardTypeABoundaryPrismCellCompletionTransportToThree
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
    (h3 : c.dim + 1 = 3) :
    ScaledSSet.of (Δ[3] : SSet.{u})
        (standardTypeABoundaryPrismTransportScalingToThree g j c h3
          (standardTypeABoundaryPrismCellAPushoutScaling g j c)) ⟶
      ScaledSSet.of (Δ[3] : SSet.{u})
        (standardTypeABoundaryPrismTransportScalingToThree g j c h3
          (standardTypeABoundaryPrismCellScaling g j c)) :=
  scalingHomTransportToThree h3 (standardTypeABoundaryPrismCellCompletionHom g j c)

/-- The actual dependent completion arrow and its fixed-three-simplex transport
are isomorphic as arrows. -/
noncomputable def standardTypeABoundaryPrismCellCompletionArrowIsoToThree
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
    (h3 : c.dim + 1 = 3) :
    Arrow.mk (standardTypeABoundaryPrismCellCompletionHom g j c) ≅
      Arrow.mk
        (standardTypeABoundaryPrismCellCompletionTransportToThree g j c h3) :=
  scalingHomTransportArrowIsoToThree h3 (standardTypeABoundaryPrismCellCompletionHom g j c)

/-! ## Exceptional completion arrows are fixed q12/q23 up to arrow isomorphism -/

/-- Source-object identification for a q12 exceptional cell. -/
noncomputable def standardTypeABoundaryPrismCellQ12SourceIso
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
    (h : StandardTypeABoundaryPrismCellQ12Factorization g j c) :
    standardTypeABoundaryPrismCellAPushoutTarget g j c ≅
      ScaledSSet.of (Δ[3] : SSet.{u}) standardTypeBCollapse12BaseScaling :=
  standardTypeABoundaryPrismCellScalingIsoToThree g j c h.target_three
      (standardTypeABoundaryPrismCellAPushoutScaling g j c) ≪≫
    scalingEqualityIso _ _ h.A_base

/-- Target-object identification for a q12 exceptional cell. -/
noncomputable def standardTypeABoundaryPrismCellQ12TargetIso
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
    (h : StandardTypeABoundaryPrismCellQ12Factorization g j c) :
    standardTypeABoundaryPrismScaledCellTarget g j c ≅
      ScaledSSet.of (Δ[3] : SSet.{u}) standardTypeBCollapse12CompletedScaling :=
  standardTypeABoundaryPrismCellScalingIsoToThree g j c h.target_three
      (standardTypeABoundaryPrismCellScaling g j c) ≪≫
    scalingEqualityIso _ _ h.completed_target

/-- The actual q12 exceptional completion is arrow-isomorphic to the fixed
v1.57 q12 completion pushout. -/
noncomputable def standardTypeABoundaryPrismCellQ12CompletionArrowIso
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
    (h : StandardTypeABoundaryPrismCellQ12Factorization g j c) :
    Arrow.mk (standardTypeABoundaryPrismCellCompletionHom g j c) ≅
      Arrow.mk standardTypeBCollapse12CompletionHom := 
  (standardTypeABoundaryPrismCellCompletionArrowIsoToThree g j c h.target_three) ≪≫
    (scalingIdentityArrowIso h.A_base h.completed_target
      (standardTypeABoundaryPrismCellCompletionTransportToThree g j c h.target_three)
      standardTypeBCollapse12CompletionHom
      (scalingHomTransportToThree_map_id h.target_three
        (standardTypeABoundaryPrismCellCompletionHom g j c) rfl)
      rfl)

/-- Source-object identification for a q23 exceptional cell. -/
noncomputable def standardTypeABoundaryPrismCellQ23SourceIso
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
    (h : StandardTypeABoundaryPrismCellQ23Factorization g j c) :
    standardTypeABoundaryPrismCellAPushoutTarget g j c ≅
      ScaledSSet.of (Δ[3] : SSet.{u}) standardTypeBCollapse23BaseScaling :=
  standardTypeABoundaryPrismCellScalingIsoToThree g j c h.target_three
      (standardTypeABoundaryPrismCellAPushoutScaling g j c) ≪≫
    scalingEqualityIso _ _ h.A_base

/-- Target-object identification for a q23 exceptional cell. -/
noncomputable def standardTypeABoundaryPrismCellQ23TargetIso
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
    (h : StandardTypeABoundaryPrismCellQ23Factorization g j c) :
    standardTypeABoundaryPrismScaledCellTarget g j c ≅
      ScaledSSet.of (Δ[3] : SSet.{u}) standardTypeBCollapse23CompletedScaling :=
  standardTypeABoundaryPrismCellScalingIsoToThree g j c h.target_three
      (standardTypeABoundaryPrismCellScaling g j c) ≪≫
    scalingEqualityIso _ _ h.completed_target

/-- The actual q23 exceptional completion is arrow-isomorphic to the fixed
v1.57 q23 completion pushout. -/
noncomputable def standardTypeABoundaryPrismCellQ23CompletionArrowIso
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
    (h : StandardTypeABoundaryPrismCellQ23Factorization g j c) :
    Arrow.mk (standardTypeABoundaryPrismCellCompletionHom g j c) ≅
      Arrow.mk standardTypeBCollapse23CompletionHom := 
  (standardTypeABoundaryPrismCellCompletionArrowIsoToThree g j c h.target_three) ≪≫
    (scalingIdentityArrowIso h.A_base h.completed_target
      (standardTypeABoundaryPrismCellCompletionTransportToThree g j c h.target_three)
      standardTypeBCollapse23CompletionHom
      (scalingHomTransportToThree_map_id h.target_three
        (standardTypeABoundaryPrismCellCompletionHom g j c) rfl)
      rfl)

/-- Every q12 exceptional completion is itself one raw standard cellular step. -/
theorem standardTypeABoundaryPrismCellCompletionHom_mem_rawCellular_of_q12
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
    (h : StandardTypeABoundaryPrismCellQ12Factorization g j c) :
    standardABCRawCellularStep
      (standardTypeABoundaryPrismCellCompletionHom g j c) := by
  exact
    ((standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u})).arrow_mk_iso_iff
      (standardTypeABoundaryPrismCellQ12CompletionArrowIso g j c h)).2
      standardTypeBCollapse12CompletionHom_mem_rawCellular

/-- Every q23 exceptional completion is itself one raw standard cellular step. -/
theorem standardTypeABoundaryPrismCellCompletionHom_mem_rawCellular_of_q23
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
    (h : StandardTypeABoundaryPrismCellQ23Factorization g j c) :
    standardABCRawCellularStep
      (standardTypeABoundaryPrismCellCompletionHom g j c) := by
  exact
    ((standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u})).arrow_mk_iso_iff
      (standardTypeABoundaryPrismCellQ23CompletionArrowIso g j c h)).2
      standardTypeBCollapse23CompletionHom_mem_rawCellular

/-! ## Pure A cells and complete exact-cell cellularity -/

/-- If no B completion is needed, the A-pushout arrow and the exact cell arrow
are isomorphic by the identity on the source and the scaling-equality
isomorphism on the target. -/
noncomputable def standardTypeABoundaryPrismCellPureAArrowIso
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j)
    (h : standardTypeABoundaryPrismCellAPushoutScaling g j c =
      standardTypeABoundaryPrismCellScaling g j c) :
    Arrow.mk (standardTypeABoundaryPrismCellAPushoutHom g j c) ≅
      Arrow.mk (standardTypeABoundaryPrismScaledCellHom g j c) := by
  refine Arrow.isoMk (Iso.refl _)
    (scalingEqualityIso _ _ h) ?_
  apply ScaledSSet.ScaledMap.ext
  simp [standardTypeABoundaryPrismCellAPushoutHom_map,
    standardTypeABoundaryPrismScaledCellHom_map]
  change c.horn.ι = c.horn.ι ≫ 𝟙 _
  simp only [Category.comp_id]

/-- A two-step raw A/B composite is a genuine finite transfinite composition.
No instance asserting that all transfinite composites are multiplicative is needed. -/
private theorem standardABCStrongCellularClosure_comp_of_raw
    {X Y Z : ScaledSSet.{u}} (f : X ⟶ Y) (g : Y ⟶ Z)
    (hf : standardABCRawCellularStep f)
    (hg : standardABCRawCellularStep g) :
    standardABCStrongCellularClosure (f ≫ g) := by
  exact MorphismProperty.transfiniteCompositionsOfShape_le_transfiniteCompositions
    (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u})) _ _
    ((MorphismProperty.TransfiniteCompositionOfShape.ofComp f g hf hg).ofOrderIso
      (orderIsoShrink.{u} (Fin 3)).symm).mem

/-- Every exact boundary-prism rank cell lies in the strong unretracted
standard A/B cellular closure.  The proof uses exactly the exhaustive local
trichotomy and no additional geometric case. -/
theorem standardTypeABoundaryPrismScaledCellHom_mem_strongCellular
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j) :
    standardABCStrongCellularClosure
      (standardTypeABoundaryPrismScaledCellHom g j c) := by
  have hAraw := standardTypeABoundaryPrismCellAPushoutHom_mem_rawCellular g j c
  rcases standardTypeABoundaryPrismCellCompletion_complete_classification
      g j c with hpure | h12 | h23
  · have hpureRaw :
        standardABCRawCellularStep
          (standardTypeABoundaryPrismScaledCellHom g j c) :=
      ((standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u})).arrow_mk_iso_iff
        (standardTypeABoundaryPrismCellPureAArrowIso g j c hpure)).1 hAraw
    exact MorphismProperty.le_transfiniteCompositions
      (standardABCRawCellularStep : MorphismProperty (ScaledSSet.{u})) _ hpureRaw
  · have hBraw :=
      standardTypeABoundaryPrismCellCompletionHom_mem_rawCellular_of_q12
        g j c h12
    have hcomp :=
      standardABCStrongCellularClosure_comp_of_raw
        (standardTypeABoundaryPrismCellAPushoutHom g j c)
        (standardTypeABoundaryPrismCellCompletionHom g j c) hAraw hBraw
    simpa only [standardTypeABoundaryPrismScaledCellHom_factor_A_completion]
      using hcomp
  · have hBraw :=
      standardTypeABoundaryPrismCellCompletionHom_mem_rawCellular_of_q23
        g j c h23
    have hcomp :=
      standardABCStrongCellularClosure_comp_of_raw
        (standardTypeABoundaryPrismCellAPushoutHom g j c)
        (standardTypeABoundaryPrismCellCompletionHom g j c) hAraw hBraw
    simpa only [standardTypeABoundaryPrismScaledCellHom_factor_A_completion]
      using hcomp

/-- Hence every exact boundary-prism rank cell lies in the precise v1.59
standard A/B/C cellular closure. -/
theorem standardTypeABoundaryPrismScaledCellHom_mem_cellular
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction.{u} g).Cell j) :
    standardABCCellularClosure
      (standardTypeABoundaryPrismScaledCellHom g j c) :=
  standardABCStrongCellularClosure_le_standardABCCellularClosure _
    (standardTypeABoundaryPrismScaledCellHom_mem_strongCellular g j c)

/-! ## Package every rank cell as one global indexed family -/

/-- Global index of all exact cells of the natural-number rank filtration. -/
def StandardTypeABoundaryPrismRankCellIndex
    (g : StandardTypeAHornAttachmentGeneratorIndex) : Type u :=
  Σ j : ℕ, (standardTypeABoundaryPrismRankFunction.{u} g).Cell j

/-- The complete family of exact pullback-scaled cells occurring anywhere in
the boundary-prism rank filtration. -/
def standardTypeABoundaryPrismExactScaledCellGenerators
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    MorphismProperty (ScaledSSet.{u}) :=
  MorphismProperty.ofHoms
    (fun γ : StandardTypeABoundaryPrismRankCellIndex g =>
      standardTypeABoundaryPrismScaledCellHom g γ.1 γ.2)

/-- Every exact cell in the entire Mathlib rank filtration is standard
A/B/C-cellular.  This is the global local-to-cellular exit theorem: subsequent
rank assembly can consume one uniform theorem and never reopen the q12/q23
classification. -/
theorem standardTypeABoundaryPrismExactScaledCellGenerators_le_cellular
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (standardTypeABoundaryPrismExactScaledCellGenerators g :
      MorphismProperty (ScaledSSet.{u})) ≤ standardABCCellularClosure := by
  intro X Y f hf
  cases hf with
  | mk γ =>
      exact standardTypeABoundaryPrismScaledCellHom_mem_cellular
        g γ.1 γ.2

/-!
The local scaled geometry is now fully consumed by the cellular calculus:

```text
all rank cells
  = pure A  or  A;q12  or  A;q23
  -> each A phase is pushout(coproduct(E_std))
  -> each q12/q23 phase is pushout(coproduct(E_std))
  -> each exact cell is a finite transfinite composite of raw A/B steps
  -> every exact cell belongs to standardABCCellularClosure.
```

The next and only remaining endpoint-prism task is genuinely rankwise:
construct the simultaneous scaled successor square at every natural-number
rank, using the already fixed ordinary Mathlib rank pushout and the exact
ambient pullback scalings of v1.71, then take the natural-number transfinite
composition and feed it into
`StandardABCTypeAEndpointLeibnizCellularCertificate`.
-/

end

end KUOS.DependentOriginationStandardTypeABoundaryPrismRankwiseABCellularityV1_72
