import KUOS.DependentOriginationFiveRouteFactorizationV2_98

namespace KUOS.DependentOriginationGeneratedCorrectionGaugeNormalFormV2_99

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFreePathEvaluatorV2_57
open KUOS.DependentOriginationCoherenceDefectsV2_65
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68
open KUOS.DependentOriginationCorrectionRealizationV2_74
open KUOS.DependentOriginationGeneratedHolonomyCorrectabilityV2_80
open KUOS.DependentOriginationCorrectedGeneratedRouteV2_97

universe u v uH vH s q uC vC

/-!
# Generated correction as gauge normal form v2.99

v2.97 turns correctability of a generated difference-loop holonomy into an
explicit corrected route equality.  v2.98 shows that only five generated route
families, rather than global path-independence, are needed for the Stage-I
factorization construction.

This layer identifies the exact algebra behind one corrected route.

For parallel isomorphisms

```text
eta, theta : X ≅ Y
```

the unique right correction carrying `eta` to `theta` is their automorphism
defect

```text
eta⁻¹ * theta.
```

Consequently, for generated localization routes `alpha` and `beta` with
common endpoints:

```text
difference-loop holonomy
  = parallel route defect
```

and the following conditions are equivalent:

```text
difference-loop holonomy is reachable by C
  ↔ an admissible right correction sends E(alpha) to E(beta)
  ↔ an admissible right correction makes the corrected route defect trivial.
```

Thus the v2.70--v2.95 correction semantics and the v2.65--v2.66 gauge
obstruction are not merely analogous at the single-route level: they are the
same automorphism equation.  What remains is the higher compatibility problem
of assembling the five route-family corrections into one pointwise-choice
gauge.
-/

/-- The automorphism defect is exactly the unique right correction carrying one
parallel isomorphism to the other. -/
theorem rightCorrection_eq_iff_eq_parallelIsoDefectIso
    {C : Type uC} [Category.{vC} C] {X Y : C}
    (eta theta : X ≅ Y) (c : Y ≅ Y) :
    eta ≪≫ c = theta ↔
      c = parallelIsoDefectIso eta theta := by
  constructor
  · intro h
    have h' := congrArg (fun e : X ≅ Y => eta.symm ≪≫ e) h
    simpa [parallelIsoDefectIso, Category.assoc] using h'
  · intro h
    rw [h]
    simp [parallelIsoDefectIso, Category.assoc]

/-- Equivalent defect-vanishing form of the same right-correction equation. -/
theorem rightCorrection_eq_iff_correctedDefect_trivial
    {C : Type uC} [Category.{vC} C] {X Y : C}
    (eta theta : X ≅ Y) (c : Y ≅ Y) :
    eta ≪≫ c = theta ↔
      parallelIsoDefectIso (eta ≪≫ c) theta = Iso.refl Y := by
  exact
    (parallelIsoDefectIso_eq_refl_iff (eta ≪≫ c) theta).symm

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- The holonomy of the generated difference loop is literally the v2.65
Iso-level defect of the two evaluated generated routes. -/
theorem generatedDifferenceHolonomy_eq_parallelIsoDefectIso
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p r : X ⟶ Y}
    (alpha beta : GeneratedLocalization2Cell W p r) :
    generatedHolonomy W R D
        (generatedLocalization2CellDifference W alpha beta) =
      parallelIsoDefectIso
        (generatedLocalization2CellEvaluationIso W R D alpha)
        (generatedLocalization2CellEvaluationIso W R D beta) := by
  rw [generatedLocalization2CellDifference_holonomy]
  rfl

/-- An admissible correction parameter acts as a right gauge on the evaluated
generated route. -/
def GeneratedRouteRightCorrection
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p r : X ⟶ Y}
    (alpha beta : GeneratedLocalization2Cell W p r)
    {State : Type s} {Param : Type q}
    (C : CorrectionRealization State Param
      ((freePathEvaluator W R D).map r ≅
        (freePathEvaluator W R D).map r))
    (x : State) : Prop :=
  ∃ c : Param,
    C.admissible x c ∧
      generatedLocalization2CellEvaluationIso W R D alpha ≪≫
          C.effect x c =
        generatedLocalization2CellEvaluationIso W R D beta

/-- The same condition expressed directly as triviality of the corrected route
defect. -/
def GeneratedRouteDefectRightTrivializable
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p r : X ⟶ Y}
    (alpha beta : GeneratedLocalization2Cell W p r)
    {State : Type s} {Param : Type q}
    (C : CorrectionRealization State Param
      ((freePathEvaluator W R D).map r ≅
        (freePathEvaluator W R D).map r))
    (x : State) : Prop :=
  ∃ c : Param,
    C.admissible x c ∧
      parallelIsoDefectIso
          (generatedLocalization2CellEvaluationIso W R D alpha ≪≫
            C.effect x c)
          (generatedLocalization2CellEvaluationIso W R D beta) =
        Iso.refl _

/-- v2.80/v2.97 reachability is exactly existence of an admissible right gauge
carrying the first generated-route evaluation to the second. -/
theorem generatedRouteCorrectionReachable_iff_rightCorrection
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p r : X ⟶ Y}
    (alpha beta : GeneratedLocalization2Cell W p r)
    {State : Type s} {Param : Type q}
    (C : CorrectionRealization State Param
      ((freePathEvaluator W R D).map r ≅
        (freePathEvaluator W R D).map r))
    (x : State) :
    GeneratedRouteCorrectionReachable W R D alpha beta C x ↔
      GeneratedRouteRightCorrection W R D alpha beta C x := by
  change
    C.CorrectableAt x
        (generatedHolonomy W R D
          (generatedLocalization2CellDifference W alpha beta)) ↔
      _
  constructor
  · rintro ⟨c, hc, heffect⟩
    refine ⟨c, hc, ?_⟩
    rw [heffect, generatedLocalization2CellDifference_holonomy]
    simp [Category.assoc]
  · rintro ⟨c, hc, hcorr⟩
    refine ⟨c, hc, ?_⟩
    rw [generatedLocalization2CellDifference_holonomy]
    have h' :=
      congrArg
        (fun e =>
          (generatedLocalization2CellEvaluationIso W R D alpha).symm ≪≫ e)
        hcorr
    simpa [Category.assoc] using h'

/-- An admissible right correction is equivalent to triviality of the corrected
parallel-route defect. -/
theorem generatedRouteRightCorrection_iff_defectRightTrivializable
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p r : X ⟶ Y}
    (alpha beta : GeneratedLocalization2Cell W p r)
    {State : Type s} {Param : Type q}
    (C : CorrectionRealization State Param
      ((freePathEvaluator W R D).map r ≅
        (freePathEvaluator W R D).map r))
    (x : State) :
    GeneratedRouteRightCorrection W R D alpha beta C x ↔
      GeneratedRouteDefectRightTrivializable W R D alpha beta C x := by
  constructor
  · rintro ⟨c, hc, hcorr⟩
    refine ⟨c, hc, ?_⟩
    exact
      (parallelIsoDefectIso_eq_refl_iff
        (generatedLocalization2CellEvaluationIso W R D alpha ≪≫
          C.effect x c)
        (generatedLocalization2CellEvaluationIso W R D beta)).2 hcorr
  · rintro ⟨c, hc, htriv⟩
    refine ⟨c, hc, ?_⟩
    exact
      (parallelIsoDefectIso_eq_refl_iff
        (generatedLocalization2CellEvaluationIso W R D alpha ≪≫
          C.effect x c)
        (generatedLocalization2CellEvaluationIso W R D beta)).1 htriv

/-- Main v2.99 normal form: generated-holonomy correctability is exactly
one-sided gauge trivializability of the corresponding evaluated route defect. -/
theorem generatedRouteCorrectionReachable_iff_defectRightTrivializable
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p r : X ⟶ Y}
    (alpha beta : GeneratedLocalization2Cell W p r)
    {State : Type s} {Param : Type q}
    (C : CorrectionRealization State Param
      ((freePathEvaluator W R D).map r ≅
        (freePathEvaluator W R D).map r))
    (x : State) :
    GeneratedRouteCorrectionReachable W R D alpha beta C x ↔
      GeneratedRouteDefectRightTrivializable W R D alpha beta C x := by
  rw [generatedRouteCorrectionReachable_iff_rightCorrection W R D alpha beta C x]
  exact
    generatedRouteRightCorrection_iff_defectRightTrivializable
      W R D alpha beta C x

/-- Whenever a parameter repairs the route, its effect is forced to equal the
parallel route defect.  Thus no extra defect value is hidden in the correction
presentation. -/
theorem correctionEffect_eq_parallelIsoDefectIso_of_rightCorrection
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : LocalizationPaths W} {p r : X ⟶ Y}
    (alpha beta : GeneratedLocalization2Cell W p r)
    {State : Type s} {Param : Type q}
    (C : CorrectionRealization State Param
      ((freePathEvaluator W R D).map r ≅
        (freePathEvaluator W R D).map r))
    (x : State) (c : Param)
    (hcorr :
      generatedLocalization2CellEvaluationIso W R D alpha ≪≫
          C.effect x c =
        generatedLocalization2CellEvaluationIso W R D beta) :
    C.effect x c =
      parallelIsoDefectIso
        (generatedLocalization2CellEvaluationIso W R D alpha)
        (generatedLocalization2CellEvaluationIso W R D beta) :=
  (rightCorrection_eq_iff_eq_parallelIsoDefectIso
    (generatedLocalization2CellEvaluationIso W R D alpha)
    (generatedLocalization2CellEvaluationIso W R D beta)
    (C.effect x c)).1 hcorr

/-!
## Boundary fixed by v2.99

At the level of one generated route comparison, the correction and gauge
languages now coincide exactly:

```text
GeneratedRouteCorrectionReachable
        ↔
admissible right gauge sends E(alpha) to E(beta)
        ↔
corrected parallel-route defect = identity.
```

Together with v2.98, the remaining Stage-I bridge is now sharply localized:

```text
five route-family right corrections
        +
compatibility saying they arise from one PointwiseChoiceGauge
        ?
        v
FiveGeneratedCoherenceRouteEqualities on the adjusted choice
        v
HigherLocalizationFactorization.
```

The unresolved content is therefore a higher compatibility / coboundary
equation, not ordinary reachability and not global holonomy vanishing.
-/

end KUOS.DependentOriginationGeneratedCorrectionGaugeNormalFormV2_99
