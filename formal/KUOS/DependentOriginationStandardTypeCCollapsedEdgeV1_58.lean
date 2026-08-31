import KUOS.DependentOriginationStandardTypeBThreeSimplexCompletionV1_57
import Mathlib.CategoryTheory.Limits.Shapes.Pullback.HasPullback

namespace KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Limits
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationExternalScaledAnodyneGeneratorComparisonV1_46
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationStandardTypeBScalingPushoutV1_56
open KUOS.DependentOriginationStandardTypeBThreeSimplexCompletionV1_57

universe u

noncomputable section

/-!
# Standard type-(C) collapsed-edge generators v1.58

The type-(A) and type-(B) pieces of the standard scaled-anodyne presentation
are now explicit in KuuOS.  This file adds the remaining standard type-(C)
family literally and then packages all three kinds of generators into one
morphism property.

For every `n > 2`, the standard type-(C) carrier is

```text
Lambda_0^n  ⨿_{Delta^{0,1}} Delta^0
       -->
Delta^n     ⨿_{Delta^{0,1}} Delta^0.
```

The edge `{0,1}` is collapsed to a point on both sides.  Both source and target
carry the minimal scaling together with the image of the triangle `01n` as a
single additional thin triangle.  We parameterize by `n = m + 3`, so every
allowed dimension occurs and no side condition is hidden in the generator
index.

The construction below proves:

* the edge face lies in the outer horn `Lambda_0^n`;
* both quotient carriers are genuine `SSet` pushouts;
* the induced map between those pushouts transports the distinguished `01n`
  triangle exactly;
* hence the induced carrier map is a morphism in `ScaledSSet`;
* the family indexed by `m : Nat` exhausts all standard type-(C) dimensions;
* type-(A), type-(B), and type-(C) form one explicit standard generator
  property;
* its `rlp.llp` and `rlp` are exposed as the standard generated left and right
  orthogonals;
* the two v1.57 three-simplex completion cells are automatically in that
  generated left class.

No equality with the stronger arbitrary-scaling KuuOS attachment family is
asserted here.  The purpose is to make the external standard A/B/C
presentation itself a concrete object for the subsequent comparison theorem.
-/

/-! ## The collapsed edge inside the outer horn -/

/-- In dimension `n = m + 3`, this is the edge face with vertices `{0,1}`. -/
def standardTypeCEdgeFace (m : Nat) :
    (Δ[m + 3] : SSet.{u}).Subcomplex :=
  SSet.stdSimplex.face ({0, 1} : Finset (Fin (m + 4)))

/-- The edge `{0,1}` lies in `Lambda_0^{m+3}`.  We factor it through the face
opposite vertex `2`, which is one of the faces present in that outer horn. -/
theorem standardTypeCEdgeFace_le_horn (m : Nat) :
    standardTypeCEdgeFace m ≤
      SSet.horn (m + 3) (0 : Fin (m + 4)) := by
  have hface :
      standardTypeCEdgeFace m ≤
        SSet.stdSimplex.face ({(2 : Fin (m + 4))}ᶜ) := by
    change
      SSet.stdSimplex.face ({0, 1} : Finset (Fin (m + 4))) ≤
        SSet.stdSimplex.face ({(2 : Fin (m + 4))}ᶜ)
    rw [SSet.stdSimplex.face_le_face_iff]
    intro j hj
    simp only [Finset.mem_insert, Finset.mem_singleton] at hj
    rcases hj with rfl | rfl
    · simp [Fin.ext_iff]
    · simp [Fin.ext_iff]
  exact hface.trans
    (SSet.face_le_horn
      (2 : Fin (m + 4)) (0 : Fin (m + 4)) (by simp [Fin.ext_iff]))

/-- Inclusion of the collapsed edge into the outer horn. -/
def standardTypeCEdgeToHorn (m : Nat) :
    (standardTypeCEdgeFace m : SSet.{u}) ⟶
      (SSet.horn (m + 3) (0 : Fin (m + 4)) : SSet.{u}) :=
  SSet.Subcomplex.homOfLE (standardTypeCEdgeFace_le_horn m)

/-- Inclusion of the collapsed edge into the full simplex. -/
def standardTypeCEdgeToSimplex (m : Nat) :
    (standardTypeCEdgeFace m : SSet.{u}) ⟶
      (Δ[m + 3] : SSet.{u}) :=
  (standardTypeCEdgeFace m).ι

/-- The map which collapses the entire edge face to the unique vertex of
`Delta[0]`. -/
def standardTypeCEdgeCollapseToPoint (m : Nat) :
    (standardTypeCEdgeFace m : SSet.{u}) ⟶
      (Δ[0] : SSet.{u}) :=
  SSet.const (SSet.stdSimplex.obj₀Equiv.symm (0 : Fin 1))

@[simp, reassoc]
theorem standardTypeCEdgeToHorn_comp_hornInclusion (m : Nat) :
    standardTypeCEdgeToHorn m ≫
        (SSet.horn (m + 3) (0 : Fin (m + 4))).ι =
      standardTypeCEdgeToSimplex m := by
  rfl

/-! ## The two quotient carriers -/

/-- Source carrier `Lambda_0^n ⨿_{Delta^{0,1}} Delta^0`. -/
def standardTypeCSourceCarrier (m : Nat) : SSet.{u} :=
  pushout
    (standardTypeCEdgeToHorn m)
    (standardTypeCEdgeCollapseToPoint m)

/-- Target carrier `Delta^n ⨿_{Delta^{0,1}} Delta^0`. -/
def standardTypeCTargetCarrier (m : Nat) : SSet.{u} :=
  pushout
    (standardTypeCEdgeToSimplex m)
    (standardTypeCEdgeCollapseToPoint m)

/-- Canonical horn leg into the source quotient, with the ambient `SSet`
universe fixed explicitly for Lean 4.31. -/
def standardTypeCSourceInl (m : Nat) :
    (SSet.horn (m + 3) (0 : Fin (m + 4)) : SSet.{u}) ⟶
      standardTypeCSourceCarrier m :=
  pushout.inl
    (standardTypeCEdgeToHorn m)
    (standardTypeCEdgeCollapseToPoint m)

/-- Canonical point leg into the source quotient. -/
def standardTypeCSourceInr (m : Nat) :
    (Δ[0] : SSet.{u}) ⟶ standardTypeCSourceCarrier m :=
  pushout.inr
    (standardTypeCEdgeToHorn m)
    (standardTypeCEdgeCollapseToPoint m)

/-- Canonical simplex leg into the target quotient. -/
def standardTypeCTargetInl (m : Nat) :
    (Δ[m + 3] : SSet.{u}) ⟶ standardTypeCTargetCarrier m :=
  pushout.inl
    (standardTypeCEdgeToSimplex m)
    (standardTypeCEdgeCollapseToPoint m)

/-- Canonical point leg into the target quotient. -/
def standardTypeCTargetInr (m : Nat) :
    (Δ[0] : SSet.{u}) ⟶ standardTypeCTargetCarrier m :=
  pushout.inr
    (standardTypeCEdgeToSimplex m)
    (standardTypeCEdgeCollapseToPoint m)

/-- The source quotient is represented by the native `SSet` pushout. -/
def standardTypeCSourceCarrier_isPushout (m : Nat) :
    IsPushout
      (standardTypeCEdgeToHorn m)
      (standardTypeCEdgeCollapseToPoint m)
      (standardTypeCSourceInl m)
      (standardTypeCSourceInr m) := by
  simpa [standardTypeCSourceInl, standardTypeCSourceInr] using
    (pushoutIsPushout
      (standardTypeCEdgeToHorn m)
      (standardTypeCEdgeCollapseToPoint m))

/-- The target quotient is represented by the native `SSet` pushout. -/
def standardTypeCTargetCarrier_isPushout (m : Nat) :
    IsPushout
      (standardTypeCEdgeToSimplex m)
      (standardTypeCEdgeCollapseToPoint m)
      (standardTypeCTargetInl m)
      (standardTypeCTargetInr m) := by
  simpa [standardTypeCTargetInl, standardTypeCTargetInr] using
    (pushoutIsPushout
      (standardTypeCEdgeToSimplex m)
      (standardTypeCEdgeCollapseToPoint m))

/-- On the source quotient the edge inclusion agrees with the point collapse. -/
theorem standardTypeCSource_edge_collapsed (m : Nat) :
    standardTypeCEdgeToHorn m ≫ standardTypeCSourceInl m =
      standardTypeCEdgeCollapseToPoint m ≫ standardTypeCSourceInr m := by
  simpa [standardTypeCSourceInl, standardTypeCSourceInr] using
    (pushout.condition :
      standardTypeCEdgeToHorn m ≫
          pushout.inl
            (standardTypeCEdgeToHorn m)
            (standardTypeCEdgeCollapseToPoint m) =
        standardTypeCEdgeCollapseToPoint m ≫
          pushout.inr
            (standardTypeCEdgeToHorn m)
            (standardTypeCEdgeCollapseToPoint m))

/-- On the target quotient the edge inclusion agrees with the point collapse. -/
theorem standardTypeCTarget_edge_collapsed (m : Nat) :
    standardTypeCEdgeToSimplex m ≫ standardTypeCTargetInl m =
      standardTypeCEdgeCollapseToPoint m ≫ standardTypeCTargetInr m := by
  simpa [standardTypeCTargetInl, standardTypeCTargetInr] using
    (pushout.condition :
      standardTypeCEdgeToSimplex m ≫
          pushout.inl
            (standardTypeCEdgeToSimplex m)
            (standardTypeCEdgeCollapseToPoint m) =
        standardTypeCEdgeCollapseToPoint m ≫
          pushout.inr
            (standardTypeCEdgeToSimplex m)
            (standardTypeCEdgeCollapseToPoint m))

/-- The induced map from the collapsed outer horn to the collapsed simplex. -/
def standardTypeCCarrierMap (m : Nat) :
    standardTypeCSourceCarrier m ⟶ standardTypeCTargetCarrier m :=
  pushout.map
    (standardTypeCEdgeToHorn m)
    (standardTypeCEdgeCollapseToPoint m)
    (standardTypeCEdgeToSimplex m)
    (standardTypeCEdgeCollapseToPoint m)
    (SSet.horn (m + 3) (0 : Fin (m + 4))).ι
    (𝟙 (Δ[0] : SSet.{u}))
    (𝟙 (standardTypeCEdgeFace m : SSet.{u}))
    (by simp [standardTypeCEdgeToHorn_comp_hornInclusion])
    (by simp)

/-- The induced carrier map is the horn inclusion on the horn leg. -/
@[reassoc]
theorem standardTypeCCarrierMap_inl_horn (m : Nat) :
    standardTypeCSourceInl m ≫ standardTypeCCarrierMap m =
      (SSet.horn (m + 3) (0 : Fin (m + 4))).ι ≫
        standardTypeCTargetInl m := by
  simp [standardTypeCSourceInl, standardTypeCTargetInl,
    standardTypeCCarrierMap]

/-- The induced carrier map is the identity on the collapsed point leg. -/
@[reassoc]
theorem standardTypeCCarrierMap_inr_point (m : Nat) :
    standardTypeCSourceInr m ≫ standardTypeCCarrierMap m =
      standardTypeCTargetInr m := by
  simp [standardTypeCSourceInr, standardTypeCTargetInr,
    standardTypeCCarrierMap]

/-! ## The distinguished `01n` triangle -/

/-- The triangle with vertices `0,1,n` in `Delta[n]`, where `n = m + 3`. -/
def standardTypeCTriangle01n (m : Nat) :
    (Δ[m + 3] : SSet.{u}).obj (op ⦋2⦌) :=
  SSet.stdSimplex.triangle
    (0 : Fin (m + 4))
    (1 : Fin (m + 4))
    (Fin.last (m + 3))
    (by omega)
    (by omega)

/-- The triangle `01n` belongs to the outer horn `Lambda_0^n`: it lies in the
face opposite vertex `2`. -/
def standardTypeCTriangle01nInHorn (m : Nat) :
    (SSet.horn (m + 3) (0 : Fin (m + 4)) : SSet.{u}).obj (op ⦋2⦌) :=
  ⟨standardTypeCTriangle01n m, by
    have ht :
        standardTypeCTriangle01n m ∈
          (SSet.stdSimplex.face ({(2 : Fin (m + 4))}ᶜ)).obj (op ⦋2⦌) := by
      rw [SSet.stdSimplex.mem_face_iff]
      intro j
      fin_cases j <;>
        simp [standardTypeCTriangle01n, Fin.ext_iff] <;> omega
    exact
      (SSet.face_le_horn
        (2 : Fin (m + 4)) (0 : Fin (m + 4))
        (by simp [Fin.ext_iff])) _ ht⟩

/-- Distinguished source triangle: the image of `01n` in the collapsed horn. -/
def standardTypeCSourceDistinguishedTriangle (m : Nat) :
    (standardTypeCSourceCarrier m).obj (op ⦋2⦌) :=
  (standardTypeCSourceInl m).app (op ⦋2⦌)
    (standardTypeCTriangle01nInHorn m)

/-- Distinguished target triangle: the image of `01n` in the collapsed full
simplex. -/
def standardTypeCTargetDistinguishedTriangle (m : Nat) :
    (standardTypeCTargetCarrier m).obj (op ⦋2⦌) :=
  (standardTypeCTargetInl m).app (op ⦋2⦌)
    (standardTypeCTriangle01n m)

/-- The quotient carrier map sends the distinguished source triangle exactly
to the distinguished target triangle. -/
theorem standardTypeCCarrierMap_distinguishedTriangle (m : Nat) :
    (standardTypeCCarrierMap m).app (op ⦋2⦌)
        (standardTypeCSourceDistinguishedTriangle m) =
      standardTypeCTargetDistinguishedTriangle m := by
  have h := congrArg
    (fun k :
        (SSet.horn (m + 3) (0 : Fin (m + 4)) : SSet.{u}) ⟶
          standardTypeCTargetCarrier m =>
      k.app (op ⦋2⦌) (standardTypeCTriangle01nInHorn m))
    (standardTypeCCarrierMap_inl_horn m)
  simpa [standardTypeCSourceDistinguishedTriangle,
    standardTypeCTargetDistinguishedTriangle,
    standardTypeCTriangle01nInHorn] using h

/-! ## Scaling by one distinguished triangle -/

/-- Minimal scaling enlarged by one specified thin triangle. -/
def minimalPlusTriangleScaling
    {X : SSet.{u}}
    (t0 : X.obj (op ⦋2⦌)) : ScaledSimplicialSet X where
  thin := fun t => (minimalScaling X).thin t ∨ t = t0
  thin_sigma_zero := by
    intro x
    exact Or.inl ((minimalScaling X).thin_sigma_zero x)
  thin_sigma_one := by
    intro x
    exact Or.inl ((minimalScaling X).thin_sigma_one x)

/-- Source scaling of the standard type-(C) generator. -/
def standardTypeCSourceScaling (m : Nat) :
    ScaledSimplicialSet (standardTypeCSourceCarrier m) :=
  minimalPlusTriangleScaling (standardTypeCSourceDistinguishedTriangle m)

/-- Target scaling of the standard type-(C) generator. -/
def standardTypeCTargetScaling (m : Nat) :
    ScaledSimplicialSet (standardTypeCTargetCarrier m) :=
  minimalPlusTriangleScaling (standardTypeCTargetDistinguishedTriangle m)

/-- The standard type-(C) source object. -/
def standardTypeCSource (m : Nat) : ScaledSSet.{u} :=
  ScaledSSet.of (standardTypeCSourceCarrier m) (standardTypeCSourceScaling m)

/-- The standard type-(C) target object. -/
def standardTypeCTarget (m : Nat) : ScaledSSet.{u} :=
  ScaledSSet.of (standardTypeCTargetCarrier m) (standardTypeCTargetScaling m)

/-- The standard type-(C) collapsed-edge generator. -/
def standardTypeCGeneratorHom (m : Nat) :
    standardTypeCSource m ⟶ standardTypeCTarget m where
  map := standardTypeCCarrierMap m
  scaled := by
    intro t ht
    rcases ht with ht | ht
    · exact Or.inl
        ((minimalScaling_map
          (standardTypeCTargetScaling m)
          (standardTypeCCarrierMap m)) t ht)
    · subst t
      exact Or.inr (standardTypeCCarrierMap_distinguishedTriangle m)

/-- The distinguished target triangle is thin by construction. -/
theorem standardTypeCTarget_distinguished_thin (m : Nat) :
    (standardTypeCTargetScaling m).thin
      (standardTypeCTargetDistinguishedTriangle m) := by
  exact Or.inr rfl

/-- The distinguished source triangle is thin by construction. -/
theorem standardTypeCSource_distinguished_thin (m : Nat) :
    (standardTypeCSourceScaling m).thin
      (standardTypeCSourceDistinguishedTriangle m) := by
  exact Or.inr rfl

/-! ## The complete type-(C) generator family -/

/-- Standard type-(C) generators in every allowed dimension `n > 2`. -/
def standardTypeCScaledAnodyneGenerators :
    MorphismProperty (ScaledSSet.{u}) :=
  MorphismProperty.ofHoms (fun m : Nat => standardTypeCGeneratorHom m)

/-- Every type-(C) collapsed-edge map belongs to the type-(C) generator family. -/
theorem standardTypeCGenerator_mem (m : Nat) :
    (standardTypeCScaledAnodyneGenerators :
      MorphismProperty (ScaledSSet.{u}))
      (standardTypeCGeneratorHom m) :=
  MorphismProperty.ofHoms.mk m

/-- The dimension of the `m`-th type-(C) generator is strictly greater than
`2`. -/
theorem standardTypeC_dimension_gt_two (m : Nat) :
    2 < m + 3 := by
  omega

/-- Conversely every natural dimension `n > 2` is uniquely represented at the
level needed here as `m + 3` for some `m`.  Thus the family above does not omit
any standard type-(C) dimension. -/
theorem exists_standardTypeC_index_of_dimension_gt_two
    (n : Nat) (hn : 2 < n) :
    ∃ m : Nat, n = m + 3 := by
  refine ⟨n - 3, ?_⟩
  omega

/-! ## Package the standard A/B/C generator presentation -/

/-- Explicit standard scaled-anodyne generator family consisting of:

* type-(A) inner scaled horns;
* the type-(B) four-simplex scaling enrichment;
* type-(C) collapsed outer horns in all dimensions `n > 2`.
-/
def standardScaledAnodyneGeneratorsABC :
    MorphismProperty (ScaledSSet.{u}) :=
  (standardTypeAScaledHornGenerators ⊔
      standardTypeBScaledAnodyneGenerators) ⊔
    standardTypeCScaledAnodyneGenerators

/-- Type-(A) generators are contained in the explicit A/B/C presentation. -/
theorem standardTypeAGenerators_le_ABC :
    (standardTypeAScaledHornGenerators :
      MorphismProperty (ScaledSSet.{u})) ≤
      standardScaledAnodyneGeneratorsABC := by
  intro X Y f hf
  exact Or.inl (Or.inl hf)

/-- Type-(B) is contained in the explicit A/B/C presentation. -/
theorem standardTypeBGenerators_le_ABC :
    (standardTypeBScaledAnodyneGenerators :
      MorphismProperty (ScaledSSet.{u})) ≤
      standardScaledAnodyneGeneratorsABC := by
  intro X Y f hf
  exact Or.inl (Or.inr hf)

/-- Type-(C) generators are contained in the explicit A/B/C presentation. -/
theorem standardTypeCGenerators_le_ABC :
    (standardTypeCScaledAnodyneGenerators :
      MorphismProperty (ScaledSSet.{u})) ≤
      standardScaledAnodyneGeneratorsABC := by
  intro X Y f hf
  exact Or.inr hf

/-- Every concrete type-(A) horn is a member of the A/B/C presentation. -/
theorem standardTypeAGenerator_mem_ABC
    (g : StandardTypeAHornGeneratorIndex) :
    standardScaledAnodyneGeneratorsABC
      (standardTypeAScaledHornGeneratorHom g) :=
  standardTypeAGenerators_le_ABC _
    (standardTypeAScaledHornGenerator_mem g)

/-- The concrete type-(B) generator is a member of the A/B/C presentation. -/
theorem standardTypeBGenerator_mem_ABC :
    standardScaledAnodyneGeneratorsABC standardTypeBGeneratorHom :=
  standardTypeBGenerators_le_ABC _ standardTypeBGenerator_mem

/-- Every concrete type-(C) map is a member of the A/B/C presentation. -/
theorem standardTypeCGenerator_mem_ABC (m : Nat) :
    standardScaledAnodyneGeneratorsABC (standardTypeCGeneratorHom m) :=
  standardTypeCGenerators_le_ABC _ (standardTypeCGenerator_mem m)

/-- Left orthogonal closure generated by the explicit standard A/B/C family. -/
def standardGeneratedScaledAnodyneABC :
    MorphismProperty (ScaledSSet.{u}) :=
  (standardScaledAnodyneGeneratorsABC :
    MorphismProperty (ScaledSSet.{u})).rlp.llp

/-- Right orthogonal class of the explicit standard A/B/C family. -/
def standardGeneratedScaledFibrationABC :
    MorphismProperty (ScaledSSet.{u}) :=
  (standardScaledAnodyneGeneratorsABC :
    MorphismProperty (ScaledSSet.{u})).rlp

/-- The standard generators lie in their own orthogonal left closure. -/
theorem standardScaledAnodyneGeneratorsABC_le_generated :
    (standardScaledAnodyneGeneratorsABC :
      MorphismProperty (ScaledSSet.{u})) ≤
      standardGeneratedScaledAnodyneABC := by
  exact MorphismProperty.le_llp_rlp _

/-- Every type-(A) generator belongs to the standard generated left class. -/
theorem standardTypeAGenerator_mem_standardGenerated
    (g : StandardTypeAHornGeneratorIndex) :
    standardGeneratedScaledAnodyneABC
      (standardTypeAScaledHornGeneratorHom g) :=
  standardScaledAnodyneGeneratorsABC_le_generated _
    (standardTypeAGenerator_mem_ABC g)

/-- Type-(B) belongs to the standard generated left class. -/
theorem standardTypeBGenerator_mem_standardGenerated :
    standardGeneratedScaledAnodyneABC standardTypeBGeneratorHom :=
  standardScaledAnodyneGeneratorsABC_le_generated _
    standardTypeBGenerator_mem_ABC

/-- Every type-(C) generator belongs to the standard generated left class. -/
theorem standardTypeCGenerator_mem_standardGenerated (m : Nat) :
    standardGeneratedScaledAnodyneABC (standardTypeCGeneratorHom m) :=
  standardScaledAnodyneGeneratorsABC_le_generated _
    (standardTypeCGenerator_mem_ABC m)

/-- The v1.57 `q12` three-simplex completion belongs automatically to the
standard generated left class because it is a pushout of type-(B). -/
theorem standardTypeBCollapse12Completion_mem_standardGenerated :
    standardGeneratedScaledAnodyneABC
      standardTypeBCollapse12CompletionHom := by
  change
    (standardScaledAnodyneGeneratorsABC :
      MorphismProperty (ScaledSSet.{u})).rlp.llp
      standardTypeBCollapse12CompletionHom
  exact standardTypeBCollapse12Completion_mem_llp
    (standardScaledAnodyneGeneratorsABC :
      MorphismProperty (ScaledSSet.{u})).rlp
    standardTypeBGenerator_mem_standardGenerated

/-- The v1.57 `q23` three-simplex completion belongs automatically to the
standard generated left class because it is a pushout of type-(B). -/
theorem standardTypeBCollapse23Completion_mem_standardGenerated :
    standardGeneratedScaledAnodyneABC
      standardTypeBCollapse23CompletionHom := by
  change
    (standardScaledAnodyneGeneratorsABC :
      MorphismProperty (ScaledSSet.{u})).rlp.llp
      standardTypeBCollapse23CompletionHom
  exact standardTypeBCollapse23Completion_mem_llp
    (standardScaledAnodyneGeneratorsABC :
      MorphismProperty (ScaledSSet.{u})).rlp
    standardTypeBGenerator_mem_standardGenerated

/-- Both low-dimensional completion cells are simultaneously available in the
standard generated left class. -/
def standardTypeBThreeSimplexCompletionStable_standardGenerated :
    StandardTypeBThreeSimplexCompletionStable
      standardGeneratedScaledAnodyneABC where
  collapse12_mem := standardTypeBCollapse12Completion_mem_standardGenerated
  collapse23_mem := standardTypeBCollapse23Completion_mem_standardGenerated

/-- The generic external-generation notation of v1.46 specializes literally
to the standard A/B/C left class. -/
theorem standardGeneratedScaledAnodyneABC_eq_external :
    standardGeneratedScaledAnodyneABC =
      externalGeneratedScaledAnodyne standardScaledAnodyneGeneratorsABC := by
  rfl

/-- Likewise the standard A/B/C right class is literally the v1.46 external
right class for this concrete generator family. -/
theorem standardGeneratedScaledFibrationABC_eq_external :
    standardGeneratedScaledFibrationABC =
      externalGeneratedScaledFibration standardScaledAnodyneGeneratorsABC := by
  rfl

/-!
The standard comparison side is now a concrete formal object:

```text
type A inner scaled horns
        +
type B four-simplex scaling enrichment
        +
type C collapsed outer horns (all n > 2)
        |
        v
standardScaledAnodyneGeneratorsABC
        |
        +--> rlp     = standardGeneratedScaledFibrationABC
        |
        +--> rlp.llp = standardGeneratedScaledAnodyneABC
```

The two exceptional three-simplex completion cells required by the type-(B)
calculus already lie in this generated left class.

The next comparison unit can therefore formulate the endpoint
pushout-product theorem directly for `standardGeneratedScaledAnodyneABC`, and
use the explicit A/B/C cells rather than an abstract external family `E`.
That is the remaining bridge needed to feed the v1.50/v1.55 type-(A) Leibniz
attachments into the standard generated class before returning to the full
v1.48 canonical-attachment comparison.
-/

end

end KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58
