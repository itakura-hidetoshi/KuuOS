import KUOS.DependentOriginationCanonicalMinimalHornReverseCoreV1_109
import KUOS.DependentOriginationStandardTypeATwoSimplexThinReplacementV1_93
import KUOS.DependentOriginationStandardTypeAEndpointOppositeCellCertificateV1_77
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
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationStandardABCPositiveCanonicalResidualSplitV1_79
open KUOS.DependentOriginationCanonicalAttachmentScalingObstructionRetractV1_88
open KUOS.DependentOriginationStandardTypeATwoSimplexThinReplacementV1_93
open KUOS.DependentOriginationCanonicalMinimalHornReverseCoreV1_109
open KUOS.DependentOriginationStandardTypeAEndpointOppositeCellCertificateV1_77

universe u

noncomputable section

/-!
# The degree-two type-A horn as a dimension-raising canonical staircase retract v1.110

Version v1.109 removed all scaling decoration from one sufficient route to the
standard-to-canonical reverse comparison.  That uniform minimal-horn route is
stronger than necessary in the lowest type-(A) dimension.

For the unique type-(A) generator `n = 2, i = 1`, use instead the canonical
horn-cylinder attachment one dimension lower:

```text
n = 1, i = 1, endpoint = 0,
simplex scaling = minimal.
```

Its ordinary target is the square `Delta[1] x Delta[1]`, and its source is the
union of the bottom and right edges.  The monotone addition map

```text
(a,b) |-> a+b

Delta[1] x Delta[1] -> Delta[2]
```

sends those two edges onto `Lambda[2,1]`.  Conversely the lower-right
staircase triangle

```text
(0,0) < (1,0) < (1,1)
```

gives a simplicial section `Delta[2] -> Delta[1] x Delta[1]` and restricts to
the same horn-source union.  Thus the degree-two type-(A) arrow is an arrow
retract of this literal canonical attachment.

The scaled part is exactly why the dimension shift is useful.  Every
2-simplex of `Delta[1]` is minimally thin, so every 2-simplex of the canonical
square cylinder is thin.  Every 2-simplex of the degree-two type-(A) simplex
is also thin: a degenerate one is minimally thin, while the unique
nondegenerate triangle is the distinguished type-(A) triangle.  Hence both
staircase target maps are scaled.  The source maps are controlled by the
minimal scaling and the fact, proved in v1.93, that every 2-simplex of
`Lambda[2,1]` is minimally thin.

This closes the literal `n=2` type-(A) reverse generator unconditionally and
strictly shrinks the v1.109 frontier: future type-(A) geometry only needs
simplex dimensions at least three.  No same-dimensional contraction is used.
-/

/-! ## The square-to-triangle addition map and its staircase section -/

/-- Pointwise addition of the two `Delta[1]` coordinates. -/
def typeATwoSquareAdditionMap :
    ((Δ[1] : SSet.{u}) ⊗ Δ[1]) ⟶ (Δ[2] : SSet.{u}) where
  app := fun ⟨⟨d⟩⟩ => ↾fun z =>
    SSet.stdSimplex.objMk
      { toFun := fun j =>
          ⟨(z.1 j).val + (z.2 j).val, by omega⟩
        monotone' := by
          intro a b hab
          have h₁ := SSet.stdSimplex.monotone_apply z.1 hab
          have h₂ := SSet.stdSimplex.monotone_apply z.2 hab
          apply Fin.mk_le_mk.mpr
          omega }
  naturality := by
    intro d e f
    ext z j
    rfl

@[simp]
theorem typeATwoSquareAdditionMap_apply
    {d : Nat}
    (z : ((Δ[1] : SSet.{u}) ⊗ Δ[1]) _⦋d⦌)
    (j : Fin (d + 1)) :
    typeATwoSquareAdditionMap.app (op ⦋d⦌) z j =
      ⟨(z.1 j).val + (z.2 j).val, by omega⟩ :=
  rfl

/-- The lower-right staircase `Delta[2] -> Delta[1] x Delta[1]`.
Its coordinate maps are the two codegeneracies `[0,1,1]` and `[0,0,1]`. -/
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

/-- Addition retracts the lower-right staircase section. -/
theorem typeATwoLowerRightStaircaseSection_comp_addition :
    typeATwoLowerRightStaircaseSection ≫ typeATwoSquareAdditionMap =
      𝟙 (Δ[2] : SSet.{u}) := by
  ext d x
  apply SSet.stdSimplex.ext
  intro j
  change
    ⟨((SimplexCategory.σ (1 : Fin 2)).toOrderHom (x j)).val +
        ((SimplexCategory.σ (0 : Fin 2)).toOrderHom (x j)).val,
      by omega⟩ = x j
  fin_cases h : x j <;> rfl

/-! ## The two source restrictions -/

/-- Restrict the lower-right staircase to `Lambda[2,1]`.  The horn condition
says either vertex `0` or vertex `2` is absent.  In the first case the first
staircase coordinate is the right vertex of `Delta[1]`; in the second case the
second coordinate is the bottom endpoint. -/
def typeATwoHornIntoCanonicalAttachmentMap :
    (Λ[2, (1 : Fin 3)] : SSet.{u}) ⟶
      (hornCylinderAttachment 1 (1 : Fin 2) 0 : SSet.{u}) :=
  SSet.Subcomplex.lift
    ((Λ[2, (1 : Fin 3)].ι :
        (Λ[2, (1 : Fin 3)] : SSet.{u}) ⟶ (Δ[2] : SSet.{u})) ≫
      typeATwoLowerRightStaircaseSection)
    (by
      rintro d y ⟨x, rfl⟩
      rw [SSet.Subcomplex.mem_unionProd_iff]
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

/-- Addition sends the canonical bottom-plus-right source into
`Lambda[2,1]`: on the bottom edge the value `2` is absent, while on the right
edge the value `0` is absent. -/
def typeATwoCanonicalAttachmentToHornMap :
    (hornCylinderAttachment 1 (1 : Fin 2) 0 : SSet.{u}) ⟶
      (Λ[2, (1 : Fin 3)] : SSet.{u}) :=
  SSet.Subcomplex.lift
    ((hornCylinderAttachment 1 (1 : Fin 2) 0).ι ≫
      typeATwoSquareAdditionMap)
    (by
      rintro d y ⟨z, rfl⟩
      rw [SSet.mem_horn_iff_notMem_range]
      rw [SSet.Subcomplex.mem_unionProd_iff] at z.property
      rcases z.property with hendpoint | hhorn
      · refine ⟨2, by decide, ?_⟩
        rintro ⟨k, hk⟩
        rw [intervalEndpoint_zero_eq_face_one,
          SSet.stdSimplex.mem_face_iff] at hendpoint
        have hs_mem := hendpoint k
        have hs_zero : z.val.2 k = (0 : Fin 2) := by
          fin_cases h : z.val.2 k <;> simp_all
        have hkval := congrArg Fin.val hk
        simp [typeATwoSquareAdditionMap_apply, hs_zero] at hkval
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
        have hkval := congrArg Fin.val hk
        simp [typeATwoSquareAdditionMap_apply] at hkval
        omega)

@[reassoc (attr := simp)]
theorem typeATwoCanonicalAttachmentToHornMap_ι :
    typeATwoCanonicalAttachmentToHornMap ≫
        (Λ[2, (1 : Fin 3)].ι :
          (Λ[2, (1 : Fin 3)] : SSet.{u}) ⟶ (Δ[2] : SSet.{u})) =
      (hornCylinderAttachment 1 (1 : Fin 2) 0).ι ≫
        typeATwoSquareAdditionMap := by
  exact SSet.Subcomplex.lift_ι _ _

/-! ## Thinness in the two target dimensions -/

/-- Every 2-simplex of `Delta[1]` is minimally thin. -/
theorem stdOne_every_two_simplex_minimally_thin
    (t : (Δ[1] : SSet.{u}) _⦋2⦌) :
    (minimalScaling (Δ[1] : SSet.{u})).thin t := by
  have hdeg :
      t ∈ (Δ[1] : SSet.{u}).degenerate 2 := by
    rw [SSet.degenerate_eq_univ_of_hasDimensionLT
      (Δ[1] : SSet.{u}) 2 2]
    simp
  rw [SSet.degenerate_eq_iUnion_range_σ] at hdeg
  simp only [Set.mem_iUnion, Set.mem_range] at hdeg
  rcases hdeg with ⟨i, x, rfl⟩
  fin_cases i
  · exact Or.inl ⟨x, rfl⟩
  · exact Or.inr ⟨x, rfl⟩

/-- Every 2-simplex of the degree-two standard type-(A) simplex is thin.
The unique nondegenerate 2-simplex is the identity triangle and is the
standard distinguished triangle. -/
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
      simpa [identityTwoSimplex] using hj
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

/-! ## Upgrade the four staircase maps to scaled maps -/

/-- The literal canonical `n=1` attachment used by the retract. -/
def typeATwoStaircaseCanonicalIndex :
    ScaledHornAttachmentGeneratorIndex.{u} where
  n := 1
  i := 1
  endpoint := 0
  simplexScaling := minimalScaling (Δ[1] : SSet.{u})

/-- Horn source section into the minimally scaled canonical attachment. -/
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

/-- Retraction from the minimally scaled canonical source to the type-(A)
horn. -/
def typeATwoCanonicalSourceToSource :
    minimallyScaledHornCylinderAttachment 1 (1 : Fin 2) 0 ⟶
      standardTypeAScaledHorn standardTypeATwoSimplexIndex where
  map := typeATwoCanonicalAttachmentToHornMap
  scaled := minimalScaling_map _ _

/-- Target staircase section into the canonical square cylinder. -/
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
    typeATwoSourceToCanonicalSource ≫ typeATwoCanonicalSourceToSource =
      𝟙 (standardTypeAScaledHorn standardTypeATwoSimplexIndex) := by
  apply ScaledSSet.ScaledMap.ext
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

/-! ## Arrow retract and unconditional canonical membership -/

/-- The staircase sections define a morphism from the degree-two type-(A)
arrow into the literal canonical `n=1` attachment arrow. -/
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

/-- Addition defines the reverse arrow morphism. -/
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

/-- The degree-two type-(A) generator is an arrow retract of a literal
canonical attachment one simplex dimension lower. -/
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

/-- The unique degree-two standard type-(A) generator is therefore
canonical-generated unconditionally. -/
theorem standardTypeATwoGenerator_mem_canonicalGenerated :
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
      (standardTypeAScaledHornGeneratorHom standardTypeATwoSimplexIndex) := by
  exact MorphismProperty.of_retract
    (P := canonicalGeneratedScaledAnodyne)
    standardTypeATwoGenerator_retractArrow
    (scaledHornAttachmentGenerators_le_generated _
      (scaledHornAttachmentGenerator_mem typeATwoStaircaseCanonicalIndex))

/-! ## Remove dimension two from the remaining type-(A) frontier -/

/-- The degree-two inner index is unique. -/
theorem standardTypeAHornGeneratorIndex_eq_two
    (g : StandardTypeAHornGeneratorIndex)
    (hn : g.n = 2) :
    g = standardTypeATwoSimplexIndex := by
  rcases g with ⟨n, i, hleft, hright⟩
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

/-- After closing dimension two, a sufficient reverse core only needs the
literal type-(A) generators in dimensions at least three and the same minimal
outer horns for type-(C) as v1.109. -/
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

/-- The refined post-two core gives the complete generatorwise reverse
comparison. -/
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

/-- Hence this strictly smaller core suffices for the full standard-to-canonical
left-class inclusion. -/
theorem standardGenerated_le_canonicalGenerated
    (K : StandardABCCanonicalPostTwoReverseCore.{u}) :
    standardGeneratedScaledAnodyneABC ≤
      (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u})) :=
  K.toGeneratorwiseReverse.standardGenerated_le_canonicalGenerated

/-- At quotient level, the refined core places standard below canonical. -/
theorem standardPresentation_le_canonicalPresentation
    (K : StandardABCCanonicalPostTwoReverseCore.{u}) :
    standardABCPresentation ≤ canonicalKuuOSPresentation :=
  (standardABC_le_canonicalKuuOS_iff_generatorwiseReverse).2
    K.toGeneratorwiseReverse

/-- Combined with the already unconditional opposite-order obstruction, this
refined core is sufficient for the desired strict presentation order. -/
theorem presentation_strictOrderCertificate
    (K : StandardABCCanonicalPostTwoReverseCore.{u}) :
    standardABCPresentation ≤ canonicalKuuOSPresentation ∧
      ¬ canonicalKuuOSPresentation ≤ standardABCPresentation :=
  ⟨K.standardPresentation_le_canonicalPresentation,
    natDoubleDelooping_not_canonicalKuuOS_le_standardABC⟩

end StandardABCCanonicalPostTwoReverseCore

/-!
The reverse frontier has now genuinely moved:

```text
canonical n=1 minimal attachment
       |
       |  lower-right staircase / coordinate addition
       v
standard type-A n=2 generator
       |
       |  arrow retract
       v
canonicalGenerated
```

Therefore the type-(A) part of the remaining standard-to-canonical problem
starts only in dimension three.  The old mixed-thin obstruction applied to a
same-dimensional cylinder contraction; it does not apply to this
one-dimension-lower staircase retract because the `Delta[1]` cylinder is
already thin in every degree-two simplex.

The next unit can ask whether the same dimension-raising staircase mechanism
extends to `n >= 3`, or whether those dimensions require the local prism/cell
filtration isolated in v1.109.  In either case dimension two is no longer part
of the residual comparison.
-/

end KUOS.DependentOriginationCanonicalTypeATwoStaircaseRetractV1_110
