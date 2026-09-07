import KUOS.DependentOriginationCanonicalMinimalHornReverseCoreV1_109
import KUOS.DependentOriginationStandardTypeATwoSimplexThinReplacementV1_93
import KUOS.DependentOriginationStandardTypeAEndpointOppositeCellCertificateV1_77
import KUOS.DependentOriginationPresentationIndependentSeparationTypeBReverseV1_107
import Mathlib.AlgebraicTopology.SimplicialSet.ProdStdSimplexOne
import Mathlib.CategoryTheory.MorphismProperty.Retract

namespace KUOS.DependentOriginationCanonicalTypeATwoStaircaseRetractV1_110

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Limits
open MonoidalCategory
open CartesianMonoidalCategory
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledHornAttachmentLiftingV1_40
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42
open KUOS.DependentOriginationExternalScaledAnodyneGeneratorComparisonV1_46
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationStandardTypeAScaledPushoutSourceEnrichmentV1_53
open KUOS.DependentOriginationStandardTypeBScalingPushoutV1_56
open KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58
open KUOS.DependentOriginationStandardABCPositiveCanonicalResidualSplitV1_79
open KUOS.DependentOriginationGeneratedPresentationPosetalReflectionV1_83
open KUOS.DependentOriginationGeneratedPresentationOrderReflectionV1_84
open KUOS.DependentOriginationCanonicalAttachmentScalingObstructionRetractV1_88
open KUOS.DependentOriginationCanonicalFibrancyAtomicTwoSimplexAuditV1_91
open KUOS.DependentOriginationStandardTypeATwoSimplexThinReplacementV1_93
open KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106
open KUOS.DependentOriginationPresentationIndependentSeparationTypeBReverseV1_107
open KUOS.DependentOriginationCanonicalMinimalHornReverseCoreV1_109
open KUOS.DependentOriginationStandardTypeAEndpointOppositeCellCertificateV1_77

universe u

noncomputable section

/-! The degree-two standard type-(A) horn is an arrow retract of the literal
canonical `n = 1, i = 1, endpoint = 0` minimal horn-cylinder attachment. -/

/-- Pointwise addition on `Delta[1] x Delta[1]`. -/
def typeATwoSquareAdditionMap :
    ((Δ[1] : SSet.{u}) ⊗ Δ[1]) ⟶ (Δ[2] : SSet.{u}) where
  app := fun ⟨⟨d⟩⟩ => ↾fun z =>
    SSet.stdSimplex.objMk
      { toFun := fun j =>
          ⟨(z.1 j).val + (z.2 j).val, by
            show (z.1 j).val + (z.2 j).val < 3
            have h1 : (z.1 j).val < 2 := (z.1 j).isLt
            have h2 : (z.2 j).val < 2 := (z.2 j).isLt
            omega⟩
        monotone' := by
          intro a b hab
          apply Fin.mk_le_mk.mpr
          exact Nat.add_le_add
            (Fin.mk_le_mk.mp (SSet.stdSimplex.monotone_apply z.1 hab))
            (Fin.mk_le_mk.mp (SSet.stdSimplex.monotone_apply z.2 hab)) }
  naturality := by
    intro d e f
    rfl

@[simp]
theorem typeATwoSquareAdditionMap_apply
    {d : Nat}
    (z : ((Δ[1] : SSet.{u}) ⊗ Δ[1]) _⦋d⦌)
    (j : Fin (d + 1)) :
    typeATwoSquareAdditionMap.app (op ⦋d⦌) z j =
      ⟨(z.1 j).val + (z.2 j).val, by
        show (z.1 j).val + (z.2 j).val < 3
        have h1 : (z.1 j).val < 2 := (z.1 j).isLt
        have h2 : (z.2 j).val < 2 := (z.2 j).isLt
        omega⟩ :=
  rfl

/-- The lower-right staircase section. -/
def typeATwoLowerRightStaircaseSection :
    (Δ[2] : SSet.{u}) ⟶ (Δ[1] : SSet.{u}) ⊗ Δ[1] :=
  CartesianMonoidalCategory.lift
    (SSet.stdSimplex.map (SimplexCategory.σ (1 : Fin 2)))
    (SSet.stdSimplex.map (SimplexCategory.σ (0 : Fin 2)))

@[simp]
theorem typeATwoLowerRightStaircaseSection_fst_apply
    {d : Nat}
    (x : (Δ[2] : SSet.{u}) _⦋d⦌)
    (j : Fin (d + 1)) :
    (typeATwoLowerRightStaircaseSection.app (op ⦋d⦌) x).1 j =
      (SimplexCategory.σ (1 : Fin 2)).toOrderHom (x j) :=
  rfl

@[simp]
theorem typeATwoLowerRightStaircaseSection_snd_apply
    {d : Nat}
    (x : (Δ[2] : SSet.{u}) _⦋d⦌)
    (j : Fin (d + 1)) :
    (typeATwoLowerRightStaircaseSection.app (op ⦋d⦌) x).2 j =
      (SimplexCategory.σ (0 : Fin 2)).toOrderHom (x j) :=
  rfl

private theorem sigma_one_eq_zero_iff (a : Fin 3) :
    (SimplexCategory.σ (1 : Fin 2)).toOrderHom a = 0 ↔ a = 0 := by
  fin_cases a <;> decide

private theorem sigma_zero_eq_zero_iff (a : Fin 3) :
    (SimplexCategory.σ (0 : Fin 2)).toOrderHom a = 0 ↔ a ≠ 2 := by
  fin_cases a <;> decide

private theorem sigma_sum_eq (a : Fin 3) :
    ((SimplexCategory.σ (1 : Fin 2)).toOrderHom a).val +
        ((SimplexCategory.σ (0 : Fin 2)).toOrderHom a).val = a.val := by
  fin_cases a <;> decide

/-- Addition retracts the staircase section. -/
theorem typeATwoLowerRightStaircaseSection_comp_addition :
    typeATwoLowerRightStaircaseSection ≫ typeATwoSquareAdditionMap =
      𝟙 (Δ[2] : SSet.{u}) := by
  ext d x
  apply SSet.stdSimplex.ext
  intro j
  apply Fin.ext
  change
    ((SimplexCategory.σ (1 : Fin 2)).toOrderHom
          (SSet.stdSimplex.asOrderHom x j)).val +
        ((SimplexCategory.σ (0 : Fin 2)).toOrderHom
          (SSet.stdSimplex.asOrderHom x j)).val =
      (SSet.stdSimplex.asOrderHom x j).val
  exact sigma_sum_eq (SSet.stdSimplex.asOrderHom x j)

/-- Restrict the staircase section to `Lambda[2,1]`. -/
def typeATwoHornIntoCanonicalAttachmentMap :
    (Λ[2, (1 : Fin 3)] : SSet.{u}) ⟶
      (hornCylinderAttachment 1 (1 : Fin 2) 0 : SSet.{u}) :=
  SSet.Subcomplex.lift
    ((Λ[2, (1 : Fin 3)].ι :
        (Λ[2, (1 : Fin 3)] : SSet.{u}) ⟶ (Δ[2] : SSet.{u})) ≫
      typeATwoLowerRightStaircaseSection)
    (by
      rintro ⟨⟨d⟩⟩ y ⟨x, rfl⟩
      change
        typeATwoLowerRightStaircaseSection.app (op ⦋d⦌) x.val ∈
          ((SSet.horn 1 (1 : Fin 2)).unionProd
            (intervalEndpoint (0 : Fin 2))).obj (op ⦋d⦌)
      apply
        (SSet.Subcomplex.mem_unionProd_iff
          (SSet.horn 1 (1 : Fin 2))
          (intervalEndpoint (0 : Fin 2))
          (typeATwoLowerRightStaircaseSection.app (op ⦋d⦌) x.val)).2
      rcases
          (SSet.mem_horn_iff_notMem_range x.val (1 : Fin 3)).1 x.property with
        ⟨missing, hmissing_ne, hmissing⟩
      fin_cases missing
      · right
        rw [SSet.mem_horn_iff_notMem_range]
        refine ⟨0, by decide, ?_⟩
        rintro ⟨k, hk⟩
        apply hmissing
        refine ⟨k, ?_⟩
        exact
          (sigma_one_eq_zero_iff (x.val k)).1
            (by simpa using hk)
      · exact (hmissing_ne rfl).elim
      · left
        rw [intervalEndpoint_zero_eq_face_one,
          SSet.stdSimplex.mem_face_iff]
        intro k
        have hk_ne : x.val k ≠ (2 : Fin 3) := by
          intro hk
          exact hmissing ⟨k, hk⟩
        have hzero :
            (SimplexCategory.σ (0 : Fin 2)).toOrderHom (x.val k) = 0 :=
          (sigma_zero_eq_zero_iff (x.val k)).2 hk_ne
        rw [typeATwoLowerRightStaircaseSection_snd_apply, hzero]
        simp)

@[reassoc (attr := simp)]
theorem typeATwoHornIntoCanonicalAttachmentMap_ι :
    typeATwoHornIntoCanonicalAttachmentMap ≫
        (hornCylinderAttachment 1 (1 : Fin 2) 0).ι =
      (Λ[2, (1 : Fin 3)].ι :
          (Λ[2, (1 : Fin 3)] : SSet.{u}) ⟶ (Δ[2] : SSet.{u})) ≫
        typeATwoLowerRightStaircaseSection := by
  exact SSet.Subcomplex.lift_ι _ _

/-- Addition sends the canonical bottom-plus-right source into `Lambda[2,1]`. -/
def typeATwoCanonicalAttachmentToHornMap :
    (hornCylinderAttachment 1 (1 : Fin 2) 0 : SSet.{u}) ⟶
      (Λ[2, (1 : Fin 3)] : SSet.{u}) :=
  SSet.Subcomplex.lift
    ((hornCylinderAttachment 1 (1 : Fin 2) 0).ι ≫
      typeATwoSquareAdditionMap)
    (by
      rintro ⟨⟨d⟩⟩ y ⟨z, rfl⟩
      change
        typeATwoSquareAdditionMap.app (op ⦋d⦌) z.val ∈
          (SSet.horn 2 (1 : Fin 3)).obj (op ⦋d⦌)
      rw [SSet.mem_horn_iff_notMem_range]
      have hzprop_union :
          z.val ∈
            ((SSet.horn 1 (1 : Fin 2)).unionProd
              (intervalEndpoint (0 : Fin 2))).obj (op ⦋d⦌) := by
        exact z.property
      have hzprop :
          z.val.2 ∈ (intervalEndpoint (0 : Fin 2)).obj (op ⦋d⦌) ∨
            z.val.1 ∈ (SSet.horn 1 (1 : Fin 2)).obj (op ⦋d⦌) :=
        (SSet.Subcomplex.mem_unionProd_iff
          (SSet.horn 1 (1 : Fin 2))
          (intervalEndpoint (0 : Fin 2)) z.val).1 hzprop_union
      rcases hzprop with hendpoint | hhorn
      · refine ⟨2, by decide, ?_⟩
        rintro ⟨k, hk⟩
        rw [intervalEndpoint_zero_eq_face_one,
          SSet.stdSimplex.mem_face_iff] at hendpoint
        have hs_ne_one : z.val.2 k ≠ (1 : Fin 2) := by
          simpa using hendpoint k
        have hs_zero : z.val.2 k = (0 : Fin 2) := by
          apply Fin.ext
          change (z.val.2 k).val = 0
          have hlt : (z.val.2 k).val < 2 := (z.val.2 k).isLt
          have hne_one_val : (z.val.2 k).val ≠ 1 := by
            intro hv
            apply hs_ne_one
            apply Fin.ext
            exact hv
          omega
        rw [typeATwoSquareAdditionMap_apply] at hk
        have hkval := congrArg Fin.val hk
        change (z.val.1 k).val + (z.val.2 k).val = 2 at hkval
        have hfst : (z.val.1 k).val < 2 := (z.val.1 k).isLt
        rw [hs_zero] at hkval
        omega
      · have hzero : (0 : Fin 2) ∉ Set.range z.val.1 := by
          rcases
              (SSet.mem_horn_iff_notMem_range z.val.1 (1 : Fin 2)).1 hhorn with
            ⟨missing, hmissing_ne, hmissing⟩
          fin_cases missing
          · exact hmissing
          · exact (hmissing_ne rfl).elim
        refine ⟨0, by decide, ?_⟩
        rintro ⟨k, hk⟩
        apply hzero
        refine ⟨k, ?_⟩
        apply Fin.ext
        rw [typeATwoSquareAdditionMap_apply] at hk
        have hkval := congrArg Fin.val hk
        change (z.val.1 k).val + (z.val.2 k).val = 0 at hkval
        have hfst : (z.val.1 k).val < 2 := (z.val.1 k).isLt
        have hsnd : (z.val.2 k).val < 2 := (z.val.2 k).isLt
        omega)

@[reassoc (attr := simp)]
theorem typeATwoCanonicalAttachmentToHornMap_ι :
    typeATwoCanonicalAttachmentToHornMap ≫
        (Λ[2, (1 : Fin 3)].ι :
          (Λ[2, (1 : Fin 3)] : SSet.{u}) ⟶ (Δ[2] : SSet.{u})) =
      (hornCylinderAttachment 1 (1 : Fin 2) 0).ι ≫
        typeATwoSquareAdditionMap := by
  exact SSet.Subcomplex.lift_ι _ _

/-- Every 2-simplex of `Delta[1]` is minimally thin. -/
theorem stdOne_every_two_simplex_minimally_thin
    (t : (Δ[1] : SSet.{u}) _⦋2⦌) :
    (minimalScaling (Δ[1] : SSet.{u})).thin t := by
  have hdeg : t ∈ (Δ[1] : SSet.{u}).degenerate 2 := by
    rw [SSet.degenerate_eq_univ_of_hasDimensionLT
      (Δ[1] : SSet.{u}) 2 2]
    simp
  rw [SSet.degenerate_eq_iUnion_range_σ] at hdeg
  simp only [Set.mem_iUnion, Set.mem_range] at hdeg
  rcases hdeg with ⟨i, x, rfl⟩
  fin_cases i
  · exact Or.inl ⟨x, rfl⟩
  · exact Or.inr ⟨x, rfl⟩

/-- Every 2-simplex of the degree-two standard type-(A) target is thin. -/
theorem standardTypeATwo_every_two_simplex_thin
    (t : (Δ[2] : SSet.{u}) _⦋2⦌) :
    (standardTypeASimplexScaling (1 : Fin 3)).thin t := by
  by_cases hnd : t ∈ (Δ[2] : SSet.{u}).nonDegenerate 2
  · have hstrict :=
      (SSet.stdSimplex.mem_nonDegenerate_iff_strictMono t).1 hnd
    have hord : SSet.stdSimplex.asOrderHom t = OrderHom.id :=
      OrderHom.eq_id_of_injective _ hstrict.injective
    have ht : t = identityTwoSimplex := by
      apply SSet.stdSimplex.ext
      intro j
      have hj := DFunLike.congr_fun hord j
      change t j =
        (SSet.stdSimplex.objEquiv.symm (𝟙 ⦋2⦌) :
          (Δ[2] : SSet.{u}) _⦋2⦌) j
      rw [SSet.stdSimplex.objEquiv_symm_apply]
      exact hj
    rw [ht]
    exact identityTwoSimplex_standardTypeA_thin
  · have hdeg : t ∈ (Δ[2] : SSet.{u}).degenerate 2 := by
      rwa [SSet.mem_degenerate_iff_notMem_nonDegenerate]
    rw [SSet.degenerate_eq_iUnion_range_σ] at hdeg
    simp only [Set.mem_iUnion, Set.mem_range] at hdeg
    rcases hdeg with ⟨i, x, rfl⟩
    fin_cases i
    · exact Or.inl (Or.inl ⟨x, rfl⟩)
    · exact Or.inl (Or.inr ⟨x, rfl⟩)

/-- The literal canonical lower-dimensional attachment index. -/
def typeATwoStaircaseCanonicalIndex :
    ScaledHornAttachmentGeneratorIndex.{u} where
  n := 1
  i := 1
  endpoint := 0
  simplexScaling := minimalScaling (Δ[1] : SSet.{u})

/-- Horn source section into the canonical attachment source. -/
def typeATwoSourceToCanonicalSource :
    standardTypeAScaledHorn standardTypeATwoSimplexIndex ⟶
      minimallyScaledHornCylinderAttachment 1 (1 : Fin 2) 0 where
  map := typeATwoHornIntoCanonicalAttachmentMap
  scaled := by
    intro t _
    exact
      (minimalScaling_map
        (minimalScaling (hornCylinderAttachment 1 (1 : Fin 2) 0 : SSet.{u}))
        typeATwoHornIntoCanonicalAttachmentMap) t
        (standardTypeATwoHorn_every_two_simplex_minimally_thin t)

/-- Source retraction by addition. -/
def typeATwoCanonicalSourceToSource :
    minimallyScaledHornCylinderAttachment 1 (1 : Fin 2) 0 ⟶
      standardTypeAScaledHorn standardTypeATwoSimplexIndex where
  map := typeATwoCanonicalAttachmentToHornMap
  scaled := minimalScaling_map _ _

/-- Target staircase section. -/
def typeATwoTargetToCanonicalTarget :
    standardTypeAScaledSimplex standardTypeATwoSimplexIndex ⟶
      scaledSimplexCylinder (minimalScaling (Δ[1] : SSet.{u})) where
  map := typeATwoLowerRightStaircaseSection
  scaled := by
    intro t _
    change
      (minimalScaling (Δ[1] : SSet.{u})).thin
        ((typeATwoLowerRightStaircaseSection.app (op ⦋2⦌) t).1)
    exact stdOne_every_two_simplex_minimally_thin _

/-- Target retraction by coordinate addition. -/
def typeATwoCanonicalTargetToTarget :
    scaledSimplexCylinder (minimalScaling (Δ[1] : SSet.{u})) ⟶
      standardTypeAScaledSimplex standardTypeATwoSimplexIndex where
  map := typeATwoSquareAdditionMap
  scaled := by
    intro t _
    exact standardTypeATwo_every_two_simplex_thin _

/-- The target section/retraction pair is split. -/
theorem typeATwoTarget_retract :
    typeATwoTargetToCanonicalTarget ≫ typeATwoCanonicalTargetToTarget =
      𝟙 (standardTypeAScaledSimplex standardTypeATwoSimplexIndex) := by
  apply ScaledSSet.ScaledMap.ext
  exact typeATwoLowerRightStaircaseSection_comp_addition

/-- The source section/retraction pair is split. -/
theorem typeATwoSource_retract :
    typeATwoSourceToCanonicalSource.{u} ≫
        typeATwoCanonicalSourceToSource.{u} =
      𝟙 (standardTypeAScaledHorn standardTypeATwoSimplexIndex : ScaledSSet.{u}) := by
  have hmap :
      typeATwoHornIntoCanonicalAttachmentMap.{u} ≫
          typeATwoCanonicalAttachmentToHornMap.{u} =
        𝟙 (Λ[2, (1 : Fin 3)] : SSet.{u}) := by
    apply (cancel_mono
      (Λ[2, (1 : Fin 3)].ι :
        (Λ[2, (1 : Fin 3)] : SSet.{u}) ⟶ (Δ[2] : SSet.{u}))).1
    rw [Category.assoc,
      typeATwoCanonicalAttachmentToHornMap_ι,
      ← Category.assoc,
      typeATwoHornIntoCanonicalAttachmentMap_ι,
      Category.assoc,
      typeATwoLowerRightStaircaseSection_comp_addition]
    simp
  apply ScaledSSet.ScaledMap.ext
  dsimp [typeATwoSourceToCanonicalSource,
    typeATwoCanonicalSourceToSource]
  exact hmap

/-- Arrow morphism from the degree-two standard generator into the canonical attachment. -/
def typeATwoToCanonicalAttachmentArrow :
    Arrow.mk
        (standardTypeAScaledHornGeneratorHom standardTypeATwoSimplexIndex) ⟶
      Arrow.mk (scaledHornAttachmentGeneratorHom typeATwoStaircaseCanonicalIndex) :=
  Arrow.homMk
    typeATwoSourceToCanonicalSource
    typeATwoTargetToCanonicalTarget
    (by
      apply ScaledSSet.ScaledMap.ext
      change
        (Λ[2, (1 : Fin 3)].ι :
            (Λ[2, (1 : Fin 3)] : SSet.{u}) ⟶ (Δ[2] : SSet.{u})) ≫
          typeATwoLowerRightStaircaseSection =
        typeATwoHornIntoCanonicalAttachmentMap ≫
          (hornCylinderAttachment 1 (1 : Fin 2) 0).ι
      exact typeATwoHornIntoCanonicalAttachmentMap_ι.symm)

/-- Reverse arrow morphism by addition. -/
def canonicalAttachmentToTypeATwoArrow :
    Arrow.mk (scaledHornAttachmentGeneratorHom typeATwoStaircaseCanonicalIndex) ⟶
      Arrow.mk
        (standardTypeAScaledHornGeneratorHom standardTypeATwoSimplexIndex) :=
  Arrow.homMk
    typeATwoCanonicalSourceToSource
    typeATwoCanonicalTargetToTarget
    (by
      apply ScaledSSet.ScaledMap.ext
      change
        (hornCylinderAttachment 1 (1 : Fin 2) 0).ι ≫
            typeATwoSquareAdditionMap =
          typeATwoCanonicalAttachmentToHornMap ≫
            (Λ[2, (1 : Fin 3)].ι :
              (Λ[2, (1 : Fin 3)] : SSet.{u}) ⟶ (Δ[2] : SSet.{u}))
      exact typeATwoCanonicalAttachmentToHornMap_ι.symm)

/-- The degree-two standard type-(A) generator is an arrow retract. -/
def standardTypeATwoGenerator_retractArrow :
    RetractArrow
      (standardTypeAScaledHornGeneratorHom standardTypeATwoSimplexIndex)
      (scaledHornAttachmentGeneratorHom typeATwoStaircaseCanonicalIndex) where
  i := typeATwoToCanonicalAttachmentArrow
  r := canonicalAttachmentToTypeATwoArrow
  retract := by
    apply Arrow.hom_ext
    · exact typeATwoSource_retract
    · exact typeATwoTarget_retract

/-- The degree-two standard type-(A) generator is canonical-generated. -/
theorem standardTypeATwoGenerator_mem_canonicalGenerated :
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
      (standardTypeAScaledHornGeneratorHom standardTypeATwoSimplexIndex) := by
  exact MorphismProperty.of_retract
    (P := canonicalGeneratedScaledAnodyne)
    standardTypeATwoGenerator_retractArrow
    (scaledHornAttachmentGenerators_le_generated _
      (scaledHornAttachmentGenerator_mem typeATwoStaircaseCanonicalIndex))

/-- The degree-two inner type-(A) index is unique. -/
theorem standardTypeAHornGeneratorIndex_eq_two
    (g : StandardTypeAHornGeneratorIndex)
    (hn : g.n = 2) :
    g = standardTypeATwoSimplexIndex := by
  rcases g with ⟨n, i, hleft, hright⟩
  change n = 2 at hn
  subst n
  have hi : i = (1 : Fin 3) := by
    apply Fin.ext
    change i.val = 1
    change 0 < i.val at hleft
    change i.val < 2 at hright
    omega
  subst i
  rfl

/-- Every degree-two type-(A) generator is canonical-generated. -/
theorem standardTypeA_mem_canonicalGenerated_of_dim_two
    (g : StandardTypeAHornGeneratorIndex)
    (hn : g.n = 2) :
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
      (standardTypeAScaledHornGeneratorHom g) := by
  rw [standardTypeAHornGeneratorIndex_eq_two g hn]
  exact standardTypeATwoGenerator_mem_canonicalGenerated

/-- After degree two, only type-A dimensions at least three and the v1.109
minimal type-C outer horns remain in this sufficient reverse core. -/
structure StandardABCCanonicalPostTwoReverseCore : Prop where
  typeA_ge_three :
    ∀ g : StandardTypeAHornGeneratorIndex,
      3 ≤ g.n →
        (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
          (standardTypeAScaledHornGeneratorHom g)
  typeC :
    ∀ m : Nat,
      (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
        (minimalHornInclusionHom (0 : Fin (m + 4)))

namespace StandardABCCanonicalPostTwoReverseCore

/-- The post-two core supplies the complete generatorwise reverse certificate. -/
def toGeneratorwiseReverse
    (K : StandardABCCanonicalPostTwoReverseCore.{u}) :
    StandardABCCanonicalGeneratorwiseReverseComparison.{u} where
  typeA_mem := by
    intro g
    have hge2 : 2 ≤ g.n := by
      have hleft := g.inner_left
      have hright := g.inner_right
      change 0 < g.i.val at hleft
      change g.i.val < g.n at hright
      omega
    by_cases htwo : g.n = 2
    · exact standardTypeA_mem_canonicalGenerated_of_dim_two g htwo
    · exact K.typeA_ge_three g (by omega)
  typeB_mem := standardTypeBGenerator_mem_canonicalGenerated
  typeC_mem := by
    intro m
    exact standardTypeC_mem_canonicalGenerated_of_minimalHorn m (K.typeC m)

/-- Generic generated-left inclusion remains universe-polymorphic. -/
theorem standardGenerated_le_canonicalGenerated
    (K : StandardABCCanonicalPostTwoReverseCore.{u}) :
    (KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58.standardGeneratedScaledAnodyneABC :
        MorphismProperty (ScaledSSet.{u})) ≤
      (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u})) :=
  K.toGeneratorwiseReverse.standardGenerated_le_canonicalGenerated

/-- Generic quotient-presentation inclusion remains universe-polymorphic. -/
theorem standardPresentation_le_canonicalPresentation
    (K : StandardABCCanonicalPostTwoReverseCore.{u}) :
    KUOS.DependentOriginationGeneratedPresentationQuotientInvariantV1_81.standardABCPresentation.{u} ≤
      KUOS.DependentOriginationGeneratedPresentationQuotientInvariantV1_81.canonicalKuuOSPresentation.{u} :=
  (standardABC_le_canonicalKuuOS_iff_generatorwiseReverse).2
    K.toGeneratorwiseReverse

/-- The v1.107 strictness witness is concrete universe zero. -/
theorem presentation_strictOrderCertificate
    (K : StandardABCCanonicalPostTwoReverseCore.{0}) :
    KUOS.DependentOriginationGeneratedPresentationQuotientInvariantV1_81.standardABCPresentation.{0} ≤
        KUOS.DependentOriginationGeneratedPresentationQuotientInvariantV1_81.canonicalKuuOSPresentation.{0} ∧
      ¬ KUOS.DependentOriginationGeneratedPresentationQuotientInvariantV1_81.canonicalKuuOSPresentation.{0} ≤
        KUOS.DependentOriginationGeneratedPresentationQuotientInvariantV1_81.standardABCPresentation.{0} :=
  ⟨K.standardPresentation_le_canonicalPresentation,
    natDoubleDelooping_not_canonicalKuuOS_le_standardABC⟩

end StandardABCCanonicalPostTwoReverseCore

end

end KUOS.DependentOriginationCanonicalTypeATwoStaircaseRetractV1_110