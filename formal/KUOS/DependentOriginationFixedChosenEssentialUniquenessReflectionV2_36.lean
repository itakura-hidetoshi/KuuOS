import KUOS.DependentOriginationStrongTransIsoTriangleTransportV2_35

namespace KUOS.DependentOriginationFixedChosenEssentialUniquenessReflectionV2_36

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationCoherentFactorForgetfulBridgeV2_20
open KUOS.DependentOriginationFactorCoherenceLiftingV2_21
open KUOS.DependentOriginationWeakHigherLocalizationGapDecompositionV2_31
open KUOS.DependentOriginationRouteCompletenessInternalGapV2_34
open KUOS.DependentOriginationStrongTransIsoTriangleTransportV2_35

open scoped CategoryTheory.Pseudofunctor.StrongTrans

universe u v uH vH

/-!
# Fixed-chosen essential-uniqueness reflection v2.36

The v2.35 layer closed StrongTrans-isomorphism transport for modification
triangles.  Hence, for a fixed coherent universal datum `U`, route completeness
is now equivalent to one remaining proposition:

```text
HasWeakHigherLocalizationUniversalProperty W R
  ->
WeakUniversalEssentialUniqueness W U.chosen.
```

This file identifies the exact mathematical content of that implication.

A coherent v2.19 datum already makes `U.chosen` a Stage II v2.31 weak universal
candidate: every competing factorization has a v2.18 factor into `U.chosen`, by
forgetting the coherent comparison triangle.  What is not automatic is Stage III
essential uniqueness for *all* v2.18 factor morphisms into that same fixed
carrier.

On the other hand, existence of a v2.18 universal property is equivalent to the
existence of some Stage II candidate carrying Stage III essential uniqueness.
Therefore fixed-chosen reflection is exactly a carrier-selection statement:

* whenever any completed Stage II candidate exists,
* its Stage III uniqueness must transfer to the fixed candidate determined by
  `U.chosen`.

The resulting obstruction is not a modification-transport defect and not a
coherent-lift defect.  It is the coexistence of

```text
some completed candidate C
+
U.chosen has no Stage III uniqueness.
```

This is an exact normal form.  No strictification, ordinary-localization
substitute, new axiom, or global uniqueness theorem is introduced.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- The fixed coherent carrier `U.chosen`, viewed only as a v2.31 Stage II weak
universal candidate.

The factor-existence field is unconditional: each coherent factor supplied by
`U.factor` forgets to a valid v2.18 factor morphism.  No Stage III uniqueness is
inserted here. -/
def fixedChosenWeakUniversalCandidate
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    WeakHigherLocalizationUniversalCandidate (W := W) R where
  chosen := U.chosen
  factor H := coherentWeakUniversalProperty_hasV2_18Factor W U H

/-- Stage III uniqueness for the fixed Stage II candidate is definitionally the
v2.34 fixed-chosen essential-uniqueness predicate. -/
@[simp] theorem fixedChosenWeakUniversalCandidate_hasEssentialUniqueness_iff
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    (fixedChosenWeakUniversalCandidate (W := W) U).HasEssentialUniqueness (W := W) ↔
      HigherFixedChosenEssentialUniqueness (W := W) U := by
  rfl

/-- Fixed-chosen uniqueness itself is sufficient for reflection, independently
of which weak universal datum witnesses the premise. -/
theorem fixedChosenReflection_of_fixedChosenEssentialUniqueness
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hUnique : HigherFixedChosenEssentialUniqueness (W := W) U) :
    HigherFixedChosenEssentialUniquenessReflection (W := W) U := by
  intro _
  exact hUnique

/-- Once a completed Stage II candidate exists, reflection is non-vacuous and
forces Stage III uniqueness on the fixed carrier `U.chosen`. -/
theorem fixedChosenEssentialUniqueness_of_reflection_and_completedCandidate
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hReflect : HigherFixedChosenEssentialUniquenessReflection (W := W) U)
    (hComplete :
      HasWeakHigherLocalizationUniversalCandidateWithUniqueness (W := W) R) :
    HigherFixedChosenEssentialUniqueness (W := W) U := by
  apply hReflect
  exact
    (hasWeakHigherLocalizationUniversalProperty_iff_candidateWithUniqueness
      (W := W) R).mpr hComplete

/-- In the non-vacuous regime where some completed weak candidate exists,
fixed-chosen reflection is exactly fixed-chosen Stage III uniqueness. -/
theorem fixedChosenReflection_iff_fixedChosenEssentialUniqueness_of_completedCandidate
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hComplete :
      HasWeakHigherLocalizationUniversalCandidateWithUniqueness (W := W) R) :
    HigherFixedChosenEssentialUniquenessReflection (W := W) U ↔
      HigherFixedChosenEssentialUniqueness (W := W) U := by
  constructor
  · intro hReflect
    exact fixedChosenEssentialUniqueness_of_reflection_and_completedCandidate
      (W := W) U hReflect hComplete
  · exact fixedChosenReflection_of_fixedChosenEssentialUniqueness (W := W) U

/-- Carrier-level transfer condition for Stage III uniqueness.

Every Stage II candidate that already has essential uniqueness transfers that
property to the fixed coherent carrier `U.chosen`.  The conclusion concerns all
v2.18 factors into `U.chosen`; it does not require coherent lifts of those
factors. -/
def HigherFixedChosenCarrierUniquenessTransfer
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∀ C : WeakHigherLocalizationUniversalCandidate (W := W) R,
    C.HasEssentialUniqueness (W := W) ->
      HigherFixedChosenEssentialUniqueness (W := W) U

/-- Fixed-chosen reflection is exactly carrier-level transfer of Stage III
uniqueness from completed weak candidates to `U.chosen`. -/
theorem fixedChosenReflection_iff_carrierUniquenessTransfer
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherFixedChosenEssentialUniquenessReflection (W := W) U ↔
      HigherFixedChosenCarrierUniquenessTransfer (W := W) U := by
  constructor
  · intro hReflect C hUnique
    apply hReflect
    exact
      ⟨weakHigherLocalizationUniversalPropertyOfCandidateWithUniqueness
        (W := W) C hUnique⟩
  · intro hTransfer hUniversal
    rcases hUniversal with ⟨V⟩
    exact
      hTransfer
        (weakUniversalCandidateOfUniversalProperty (W := W) V)
        V.essential_unique

/-- Exact carrier-selection obstruction: some weak Stage II carrier is already
complete through Stage III, while the coherent fixed carrier `U.chosen` is not. -/
def HigherFixedChosenCarrierMismatchObstruction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∃ C : WeakHigherLocalizationUniversalCandidate (W := W) R,
    C.HasEssentialUniqueness (W := W) ∧
      ¬ HigherFixedChosenEssentialUniqueness (W := W) U

/-- The v2.34 reflection failure is exactly the fixed-carrier mismatch
obstruction. -/
theorem reflectionFailure_iff_carrierMismatchObstruction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherFixedChosenEssentialUniquenessReflectionFailure (W := W) U ↔
      HigherFixedChosenCarrierMismatchObstruction (W := W) U := by
  constructor
  · rintro ⟨hUniversal, hNoUnique⟩
    rcases hUniversal with ⟨V⟩
    exact
      ⟨weakUniversalCandidateOfUniversalProperty (W := W) V,
        V.essential_unique,
        hNoUnique⟩
  · rintro ⟨C, hUnique, hNoUnique⟩
    refine ⟨?_, hNoUnique⟩
    exact
      ⟨weakHigherLocalizationUniversalPropertyOfCandidateWithUniqueness
        (W := W) C hUnique⟩

/-- Carrier transfer is equivalently absence of the explicit mismatch
obstruction.  Classical logic is used only for the final double-negation step. -/
theorem carrierUniquenessTransfer_iff_no_mismatchObstruction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherFixedChosenCarrierUniquenessTransfer (W := W) U ↔
      ¬ HigherFixedChosenCarrierMismatchObstruction (W := W) U := by
  classical
  constructor
  · intro hTransfer hMismatch
    rcases hMismatch with ⟨C, hUnique, hNoFixed⟩
    exact hNoFixed (hTransfer C hUnique)
  · intro hNoMismatch C hUnique
    by_contra hNoFixed
    exact hNoMismatch ⟨C, hUnique, hNoFixed⟩

/-- Candidate-completion normal form: if some Stage II candidate can be completed
through Stage III, then the *fixed* Stage II candidate selected by the coherent
datum must also complete through Stage III. -/
def HigherFixedChosenStageIIICompletion
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  HasWeakHigherLocalizationUniversalCandidateWithUniqueness (W := W) R ->
    HigherFixedChosenEssentialUniqueness (W := W) U

/-- Quantifying transfer over completed candidates is equivalent to the compact
existential candidate-completion form. -/
theorem carrierUniquenessTransfer_iff_stageIIICompletion
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherFixedChosenCarrierUniquenessTransfer (W := W) U ↔
      HigherFixedChosenStageIIICompletion (W := W) U := by
  constructor
  · intro hTransfer hComplete
    rcases hComplete with ⟨C, hUnique⟩
    exact hTransfer C hUnique
  · intro hComplete C hUnique
    exact hComplete ⟨C, hUnique⟩

/-- The exact v2.36 closure theorem: fixed-chosen reflection is neither more nor
less than fixed-carrier Stage III completion. -/
theorem fixedChosenReflection_iff_stageIIICompletion
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherFixedChosenEssentialUniquenessReflection (W := W) U ↔
      HigherFixedChosenStageIIICompletion (W := W) U :=
  (fixedChosenReflection_iff_carrierUniquenessTransfer (W := W) U).trans
    (carrierUniquenessTransfer_iff_stageIIICompletion (W := W) U)

/-- Factor-coherence lifting remains a sufficient condition for the v2.36
carrier-transfer property, but is deliberately not claimed necessary.  Under
lifting, v2.21 already constructs a v2.18 universal datum on the same chosen
carrier, whose essential-uniqueness field is exactly the required conclusion. -/
theorem carrierUniquenessTransfer_of_factorCoherenceLifting
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hLift : HigherFactorCoherenceLifting (W := W) U) :
    HigherFixedChosenCarrierUniquenessTransfer (W := W) U := by
  intro _ _
  exact (weakHigherLocalizationUniversalPropertyOfCoherent W U hLift).essential_unique

/-- Consequently, factor-coherence lifting is sufficient for fixed-chosen
reflection, without being built into the reflection criterion itself. -/
theorem fixedChosenReflection_of_factorCoherenceLifting
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hLift : HigherFactorCoherenceLifting (W := W) U) :
    HigherFixedChosenEssentialUniquenessReflection (W := W) U :=
  (fixedChosenReflection_iff_carrierUniquenessTransfer (W := W) U).mpr
    (carrierUniquenessTransfer_of_factorCoherenceLifting (W := W) U hLift)

/-- Combining v2.35 with the v2.36 carrier normal form removes the last internal
presentation ambiguity in route completeness: route completeness is exactly
Stage III uniqueness transfer to the fixed coherent carrier. -/
theorem routeCompleteness_iff_carrierUniquenessTransfer
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherCoherentRouteCompleteness (W := W) U ↔
      HigherFixedChosenCarrierUniquenessTransfer (W := W) U :=
  (routeCompleteness_iff_fixedChosenReflection (W := W) U).trans
    (fixedChosenReflection_iff_carrierUniquenessTransfer (W := W) U)

/-- Equivalent route-completeness normal form using the compact fixed Stage III
completion predicate. -/
theorem routeCompleteness_iff_stageIIICompletion
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherCoherentRouteCompleteness (W := W) U ↔
      HigherFixedChosenStageIIICompletion (W := W) U :=
  (routeCompleteness_iff_fixedChosenReflection (W := W) U).trans
    (fixedChosenReflection_iff_stageIIICompletion (W := W) U)

/-- The sole remaining route-completeness obstruction is therefore exactly the
coexistence of a completed weak carrier and failure of Stage III uniqueness on
`U.chosen`. -/
theorem not_routeCompleteness_iff_carrierMismatchObstruction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    (¬ HigherCoherentRouteCompleteness (W := W) U) ↔
      HigherFixedChosenCarrierMismatchObstruction (W := W) U :=
  (not_routeCompleteness_iff_reflectionFailure (W := W) U).trans
    (reflectionFailure_iff_carrierMismatchObstruction (W := W) U)

/-- Global fixed-carrier Stage III completion principle.  It is an explicit
proposition, not a theorem asserted for arbitrary coherent universal data. -/
def HigherFixedChosenStageIIICompletionPrinciple : Prop :=
  ∀ (R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH))
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R),
    HigherFixedChosenStageIIICompletion (W := W) U

/-- Globally, the v2.34 fixed-chosen reflection principle is exactly the v2.36
fixed-carrier Stage III completion principle. -/
theorem fixedChosenReflectionPrinciple_iff_stageIIICompletionPrinciple :
    HigherFixedChosenEssentialUniquenessReflectionPrinciple
        (W := W) (uH := uH) (vH := vH) ↔
      HigherFixedChosenStageIIICompletionPrinciple
        (W := W) (uH := uH) (vH := vH) := by
  constructor
  · intro hReflect R U
    exact
      (fixedChosenReflection_iff_stageIIICompletion (W := W) U).mp
        (hReflect R U)
  · intro hComplete R U
    exact
      (fixedChosenReflection_iff_stageIIICompletion (W := W) U).mpr
        (hComplete R U)

/-!
## Boundary after v2.36

The route-completeness frontier has now been reduced to a fixed-carrier Stage III
selection problem:

```text
some weak Stage II candidate C has Stage III uniqueness
                         |
                         |  v2.36 transfer condition
                         v
fixed coherent candidate U.chosen has Stage III uniqueness
                         |
                         |  v2.35 iso-triangle transport
                         v
coherent route completeness.
```

The exact obstruction is

```text
∃ completed candidate C,
  ¬ WeakUniversalEssentialUniqueness W U.chosen.
```

This file does **not** prove that the obstruction is absent in general.  In
particular, it does not derive uniqueness on `U.chosen` merely from uniqueness on
some other chosen carrier, does not silently identify weak and coherent factor
morphisms, and does not reintroduce StrongTrans-iso triangle transport as a
hypothesis.

A next theorem unit may seek a genuinely mathematical sufficient condition for
carrier transfer (for example a suitable retract/equivalence/conservativity
property between chosen weak carriers), or construct an explicit obstruction
model.  The general reflection principle remains open.
-/

end KUOS.DependentOriginationFixedChosenEssentialUniquenessReflectionV2_36
