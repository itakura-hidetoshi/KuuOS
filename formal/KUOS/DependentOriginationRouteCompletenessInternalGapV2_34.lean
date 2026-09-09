import KUOS.DependentOriginationStageIIIRouteCompletenessV2_33

namespace KUOS.DependentOriginationRouteCompletenessInternalGapV2_34

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationCoherentFactorForgetfulBridgeV2_20
open KUOS.DependentOriginationFactorCoherenceLiftingV2_21
open KUOS.DependentOriginationModificationTriangleNormalFormV2_22
open KUOS.DependentOriginationStoredTriangleCorrectionV2_26
open KUOS.DependentOriginationWeakHigherLocalizationGapDecompositionV2_31
open KUOS.DependentOriginationCoherentStageIIIGapCollapseV2_32
open KUOS.DependentOriginationStageIIIRouteCompletenessV2_33

open scoped CategoryTheory.Pseudofunctor.StrongTrans

universe u v uH vH

/-!
# Route-completeness internal gap v2.34

The v2.33 layer isolated `HigherCoherentRouteCompleteness U` as the exact extra
logical content needed to reflect a v2.26 correction obstruction back to Stage
III failure.  This file opens that route-completeness implication itself.

For a fixed coherent v2.19 universal datum `U`, the key mismatch is now visible:

* `U` already supplies, for every competing factorization `H`, at least one
  coherent factor `beta : H -> U.chosen`;
* forgetting coherence gives a v2.18 factor with a genuine modification
  triangle;
* an arbitrary v2.18 factor `alpha : H -> U.chosen` need not be that coherent
  factor;
* essential uniqueness can at best provide an isomorphism
  `alpha.hom ≅ beta.hom` of StrongTrans 1-cells;
* v2.21/v2.22 require a modification triangle on the *same* underlying
  StrongTrans `alpha.hom`.

Thus route completeness has two logically distinct internal failure modes:

1. **fixed-chosen reflection failure**: some weak universal property exists on
   the raw system, but essential uniqueness does not reflect to the fixed
   carrier `U.chosen`;
2. **iso-coherence transport residual**: fixed-chosen essential uniqueness does
   hold, but correction lifting for arbitrary factors into `U.chosen` still
   fails.

The first main theorem gives an exact disjunction normal form for failure of
route completeness.  The second layer isolates an explicit StrongTrans-iso
transport property: modification triangles can be transported from `beta` to
`alpha` whenever `alpha.hom ≅ beta.hom`.  Under that property the second
residual obstruction disappears, so route completeness becomes exactly
fixed-chosen essential-uniqueness reflection.

The iso-transport property is an explicit proposition, not an axiom and not an
unconditional theorem.  No claim is made that an arbitrary isomorphism of
StrongTrans automatically induces the required whiskered comparison triangle
without checking the relevant bicategorical coherence.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Essential uniqueness on the particular coherent carrier `U.chosen`. -/
def HigherFixedChosenEssentialUniqueness
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  WeakUniversalEssentialUniqueness (W := W) U.chosen

/-- Reflection of an arbitrary v2.18 weak universal property back to essential
uniqueness on the fixed coherent carrier `U.chosen`. -/
def HigherFixedChosenEssentialUniquenessReflection
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  HasWeakHigherLocalizationUniversalProperty (W := W) R ->
    HigherFixedChosenEssentialUniqueness (W := W) U

/-- First internal obstruction: weak universality exists somewhere, but does not
reflect to essential uniqueness on `U.chosen`. -/
def HigherFixedChosenEssentialUniquenessReflectionFailure
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  HasWeakHigherLocalizationUniversalProperty (W := W) R ∧
    ¬ HigherFixedChosenEssentialUniqueness (W := W) U

/-- Second internal obstruction: weak universality exists and fixed-chosen
essential uniqueness already holds, but the correction route still fails. -/
def HigherIsoCoherenceTransportResidualObstruction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  HasWeakHigherLocalizationUniversalProperty (W := W) R ∧
    HigherFixedChosenEssentialUniqueness (W := W) U ∧
      ¬ HigherStoredTriangleTargetCorrectionLifting (W := W) U

/-- Correction lifting on `U` already forces essential uniqueness on the same
fixed chosen carrier.  The proof passes through the exact v2.26 -> v2.22 ->
v2.21 route and then reads the `essential_unique` field of the reconstructed
v2.18 universal datum. -/
theorem fixedChosenEssentialUniqueness_of_correctionLifting
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hCorrection : HigherStoredTriangleTargetCorrectionLifting (W := W) U) :
    HigherFixedChosenEssentialUniqueness (W := W) U := by
  have hTriangle : HigherFactorModificationTriangleLifting (W := W) U :=
    (higherStoredTriangleCorrectionLifting_iff_modificationTriangleLifting
      (W := W) U).mp hCorrection
  have hFactor : HigherFactorCoherenceLifting (W := W) U :=
    (higherFactorCoherenceLifting_iff_modificationTriangleLifting
      (W := W) U).mpr hTriangle
  exact (weakHigherLocalizationUniversalPropertyOfCoherent W U hFactor).essential_unique

/-- Route completeness therefore always implies fixed-chosen essential-
uniqueness reflection. -/
theorem fixedChosenReflection_of_routeCompleteness
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hRoute : HigherCoherentRouteCompleteness (W := W) U) :
    HigherFixedChosenEssentialUniquenessReflection (W := W) U := by
  intro hUniversal
  exact fixedChosenEssentialUniqueness_of_correctionLifting
    (W := W) U (hRoute hUniversal)

/-- Exact internal failure decomposition of v2.33 route completeness. -/
theorem not_routeCompleteness_iff_reflectionFailure_or_transportResidual
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    (¬ HigherCoherentRouteCompleteness (W := W) U) ↔
      HigherFixedChosenEssentialUniquenessReflectionFailure (W := W) U ∨
        HigherIsoCoherenceTransportResidualObstruction (W := W) U := by
  classical
  constructor
  · intro hNoRoute
    have hUniversal : HasWeakHigherLocalizationUniversalProperty (W := W) R := by
      by_contra hNoUniversal
      apply hNoRoute
      intro hUniversal
      exact False.elim (hNoUniversal hUniversal)
    have hNoCorrection :
        ¬ HigherStoredTriangleTargetCorrectionLifting (W := W) U := by
      intro hCorrection
      exact hNoRoute (fun _ => hCorrection)
    by_cases hUnique : HigherFixedChosenEssentialUniqueness (W := W) U
    · exact Or.inr ⟨hUniversal, hUnique, hNoCorrection⟩
    · exact Or.inl ⟨hUniversal, hUnique⟩
  · intro hObstruction hRoute
    rcases hObstruction with hReflection | hResidual
    · exact hReflection.2
        (fixedChosenReflection_of_routeCompleteness
          (W := W) U hRoute hReflection.1)
    · exact hResidual.2.2 (hRoute hResidual.1)

/-- Fixed-chosen reflection is exactly absence of its explicit first-stage
obstruction. -/
theorem fixedChosenReflection_iff_no_reflectionFailure
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherFixedChosenEssentialUniquenessReflection (W := W) U ↔
      ¬ HigherFixedChosenEssentialUniquenessReflectionFailure (W := W) U := by
  classical
  constructor
  · intro hReflect hFailure
    exact hFailure.2 (hReflect hFailure.1)
  · intro hNoFailure hUniversal
    by_contra hNoUnique
    exact hNoFailure ⟨hUniversal, hNoUnique⟩

/-- Explicit transport property for the remaining 2-cell problem.

For two v2.18 factors with the same source and target, an isomorphism of their
underlying StrongTrans 1-cells is required to transport a modification triangle
from the second factor to the first.  This proposition precisely exposes the
bicategorical whiskering/coherence step; it is not asserted unconditionally. -/
def HigherFactorModificationTriangleIsoTransport
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∀ (H : HigherLocalizationFactorization (W := W) R)
    (alpha beta : HigherLocalizationFactorMorphism (W := W) H U.chosen),
    Nonempty (alpha.hom ≅ beta.hom) ->
      HasFactorModificationTriangle (W := W) beta ->
        HasFactorModificationTriangle (W := W) alpha

/-- The coherent factor supplied by `U` gives a v2.18 factor whose modification
triangle is already available. -/
theorem hasTriangle_for_forgottenCoherentFactor
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H : HigherLocalizationFactorization (W := W) R}
    {K : HigherLocalizationFactorization (W := W) R}
    (beta : CoherentHigherLocalizationFactorMorphism (W := W) H K) :
    HasFactorModificationTriangle
      (W := W) (coherentHigherLocalizationFactorMorphismToV2_18 (W := W) beta) := by
  refine ⟨?_⟩
  simpa only [coherentHigherLocalizationFactorMorphismToV2_18_hom] using
    beta.comparison_triangle

/-- Fixed-chosen essential uniqueness plus iso-transport is sufficient to solve
all correction equations into the same coherent carrier `U.chosen`. -/
theorem correctionLifting_of_fixedChosenUniqueness_and_isoTransport
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hUnique : HigherFixedChosenEssentialUniqueness (W := W) U)
    (hTransport : HigherFactorModificationTriangleIsoTransport (W := W) U) :
    HigherStoredTriangleTargetCorrectionLifting (W := W) U := by
  apply
    (higherStoredTriangleCorrectionLifting_iff_modificationTriangleLifting
      (W := W) U).mpr
  intro H alpha
  rcases U.factor H with ⟨betaCoherent⟩
  let beta : HigherLocalizationFactorMorphism (W := W) H U.chosen :=
    coherentHigherLocalizationFactorMorphismToV2_18 (W := W) betaCoherent
  have hIso : Nonempty (alpha.hom ≅ beta.hom) := hUnique H alpha beta
  have hBetaTriangle : HasFactorModificationTriangle (W := W) beta := by
    dsimp [beta]
    exact hasTriangle_for_forgottenCoherentFactor (W := W) betaCoherent
  exact hTransport H alpha beta hIso hBetaTriangle

/-- Under iso-transport, the second residual obstruction is impossible. -/
theorem not_transportResidual_of_isoTransport
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hTransport : HigherFactorModificationTriangleIsoTransport (W := W) U) :
    ¬ HigherIsoCoherenceTransportResidualObstruction (W := W) U := by
  rintro ⟨_, hUnique, hNoCorrection⟩
  exact hNoCorrection
    (correctionLifting_of_fixedChosenUniqueness_and_isoTransport
      (W := W) U hUnique hTransport)

/-- Main local closure theorem: once StrongTrans-isomorphic factor maps support
triangle transport, route completeness is exactly reflection of essential
uniqueness to the fixed coherent carrier. -/
theorem routeCompleteness_iff_fixedChosenReflection_of_isoTransport
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hTransport : HigherFactorModificationTriangleIsoTransport (W := W) U) :
    HigherCoherentRouteCompleteness (W := W) U ↔
      HigherFixedChosenEssentialUniquenessReflection (W := W) U := by
  constructor
  · exact fixedChosenReflection_of_routeCompleteness (W := W) U
  · intro hReflect hUniversal
    exact correctionLifting_of_fixedChosenUniqueness_and_isoTransport
      (W := W) U (hReflect hUniversal) hTransport

/-- Equivalently, under iso-transport, failure of route completeness is exactly
fixed-chosen reflection failure. -/
theorem not_routeCompleteness_iff_reflectionFailure_of_isoTransport
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hTransport : HigherFactorModificationTriangleIsoTransport (W := W) U) :
    (¬ HigherCoherentRouteCompleteness (W := W) U) ↔
      HigherFixedChosenEssentialUniquenessReflectionFailure (W := W) U := by
  rw [routeCompleteness_iff_fixedChosenReflection_of_isoTransport
    (W := W) U hTransport]
  exact not_congr
    (fixedChosenReflection_iff_no_reflectionFailure (W := W) U)

/-- Obstruction-free normal form of the same local closure. -/
theorem routeCompleteness_iff_no_reflectionFailure_of_isoTransport
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hTransport : HigherFactorModificationTriangleIsoTransport (W := W) U) :
    HigherCoherentRouteCompleteness (W := W) U ↔
      ¬ HigherFixedChosenEssentialUniquenessReflectionFailure (W := W) U := by
  exact
    (routeCompleteness_iff_fixedChosenReflection_of_isoTransport
      (W := W) U hTransport).trans
      (fixedChosenReflection_iff_no_reflectionFailure (W := W) U)

/-- Global StrongTrans-iso triangle-transport principle. -/
def HigherFactorModificationTriangleIsoTransportPrinciple : Prop :=
  ∀ (R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH))
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R),
    HigherFactorModificationTriangleIsoTransport (W := W) U

/-- Global fixed-chosen essential-uniqueness reflection principle. -/
def HigherFixedChosenEssentialUniquenessReflectionPrinciple : Prop :=
  ∀ (R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH))
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R),
    HigherFixedChosenEssentialUniquenessReflection (W := W) U

/-- Globally, under the explicit iso-transport principle, v2.33 route
completeness is exactly fixed-chosen essential-uniqueness reflection. -/
theorem routeCompletenessPrinciple_iff_fixedChosenReflectionPrinciple_of_isoTransport
    (hTransport : HigherFactorModificationTriangleIsoTransportPrinciple
      (W := W) (uH := uH) (vH := vH)) :
    HigherCoherentRouteCompletenessPrinciple
        (W := W) (uH := uH) (vH := vH) ↔
      HigherFixedChosenEssentialUniquenessReflectionPrinciple
        (W := W) (uH := uH) (vH := vH) := by
  constructor
  · intro hRoute R U
    exact fixedChosenReflection_of_routeCompleteness (W := W) U (hRoute R U)
  · intro hReflect R U
    exact
      (routeCompleteness_iff_fixedChosenReflection_of_isoTransport
        (W := W) U (hTransport R U)).mpr (hReflect R U)

/-- Combining v2.33 with the new internal decomposition: coherent universal
existence, iso-transport, and fixed-chosen reflection are sufficient to identify
the full v2.18 universal principle with global correction solvability. -/
theorem higherWeakLocalizationUniversalPrinciple_iff_storedCorrection_of_coherent_isoTransport_fixedReflection
    (hCoherent : CoherentHigherWeakLocalizationUniversalPrinciple
      (W := W) (uH := uH) (vH := vH))
    (hTransport : HigherFactorModificationTriangleIsoTransportPrinciple
      (W := W) (uH := uH) (vH := vH))
    (hReflect : HigherFixedChosenEssentialUniquenessReflectionPrinciple
      (W := W) (uH := uH) (vH := vH)) :
    HigherWeakLocalizationUniversalPrinciple
        (W := W) (uH := uH) (vH := vH) ↔
      HigherStoredTriangleTargetCorrectionPrinciple
        (W := W) (uH := uH) (vH := vH) := by
  have hRoute : HigherCoherentRouteCompletenessPrinciple
      (W := W) (uH := uH) (vH := vH) :=
    (routeCompletenessPrinciple_iff_fixedChosenReflectionPrinciple_of_isoTransport
      (W := W) hTransport).mpr hReflect
  exact
    higherWeakLocalizationUniversalPrinciple_iff_storedTriangleCorrectionPrinciple_of_coherent_and_routeCompleteness
      (W := W) hCoherent hRoute

/-- The corresponding Stage III completion normal form. -/
theorem higherWeakEssentialUniquenessCompletion_iff_storedCorrection_of_coherent_isoTransport_fixedReflection
    (hCoherent : CoherentHigherWeakLocalizationUniversalPrinciple
      (W := W) (uH := uH) (vH := vH))
    (hTransport : HigherFactorModificationTriangleIsoTransportPrinciple
      (W := W) (uH := uH) (vH := vH))
    (hReflect : HigherFixedChosenEssentialUniquenessReflectionPrinciple
      (W := W) (uH := uH) (vH := vH)) :
    HigherWeakEssentialUniquenessCompletion
        (W := W) (uH := uH) (vH := vH) ↔
      HigherStoredTriangleTargetCorrectionPrinciple
        (W := W) (uH := uH) (vH := vH) := by
  have hRoute : HigherCoherentRouteCompletenessPrinciple
      (W := W) (uH := uH) (vH := vH) :=
    (routeCompletenessPrinciple_iff_fixedChosenReflectionPrinciple_of_isoTransport
      (W := W) hTransport).mpr hReflect
  exact
    higherWeakEssentialUniquenessCompletion_iff_storedTriangleCorrectionPrinciple_of_coherent_and_routeCompleteness
      (W := W) hCoherent hRoute

/-!
The v2.34 frontier is therefore:

```text
weak v2.18 universality exists somewhere
        |
        | fixed-chosen reflection
        v
essential uniqueness on U.chosen
        |
        | StrongTrans-iso triangle transport
        v
correction lifting for every alpha : H -> U.chosen
        |
        v
v2.33 route completeness.
```

Failure of route completeness is exactly the disjunction of fixed-chosen
reflection failure and the residual failure after fixed-chosen uniqueness has
already been obtained.  Under the explicit iso-transport property the residual
vanishes and only the carrier-reflection problem remains.

Neither fixed-chosen reflection nor StrongTrans-iso triangle transport is proved
unconditionally here.  In particular, this file does not collapse arbitrary
presentation carriers or silently replace genuine modification coherence by
objectwise natural-isomorphism data.
-/

end KUOS.DependentOriginationRouteCompletenessInternalGapV2_34
