import Mathlib.CategoryTheory.Discrete.Basic
import KUOS.DependentOriginationDiscreteBaseObstructionEliminationV2_43

namespace KUOS.DependentOriginationIsDiscreteBaseObstructionEliminationV2_44

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationFactorCoherenceLiftingV2_21
open KUOS.DependentOriginationModificationTriangleNormalFormV2_22
open KUOS.DependentOriginationStoredTriangleModificationNaturalityV2_23
open KUOS.DependentOriginationStoredTriangleCorrectionV2_26
open KUOS.DependentOriginationStageIIIRouteCompletenessV2_33
open KUOS.DependentOriginationWeakCoherentTwoAxisObstructionV2_42

universe u v uH vH

/-!
# Abstract discrete-base obstruction elimination v2.44

The v2.43 theorem was proved for the concrete Mathlib presentation `Discrete I`.
The proof, however, uses only the presentation-invariant categorical content of
discreteness:

* every morphism identifies its source and target;
* every hom type is a subsingleton.

Mathlib packages exactly these two facts as `CategoryTheory.IsDiscrete`.
This file removes the concrete `Discrete I` presentation and proves the same
obstruction elimination for an arbitrary category carrying an `IsDiscrete`
instance.

For a base arrow `f : X ⟶ Y`, `IsDiscrete.eq_of_hom f` first identifies
`X = Y`.  After that transport, the subsingleton hom instance identifies `f`
with `𝟙 X`.  The v2.18 stored objectwise triangle is therefore automatically
modification-natural by the ordinary StrongTrans identity coherence law.

Thus the structural implication is

```text
IsDiscrete Context
  -> every stored v2.18 triangle is modification-natural
  -> factor modification-triangle lifting
  -> factor-coherence lifting
  -> weak universality on the coherent chosen carrier
  -> coherent route completeness
  -> no local v2.42 E/R obstruction.
```

This is not a strictification theorem and does not say that an arbitrary context
is equivalent to a discrete one.  It only shows that the obstruction-killing
mechanism of v2.43 depends on the categorical `IsDiscrete` structure rather than
on the concrete wrapper `Discrete I`.  Coherent universal-data existence remains
an explicit premise globally.
-/

variable {Context : Type u} [Category.{v} Context] [IsDiscrete Context]
variable (W : MorphismProperty Context)

/-- On any Mathlib-discrete category, every stored v2.18 comparison triangle is
already modification-natural. -/
theorem storedV2_18TriangleIsModificationNatural_of_isDiscrete
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K) :
    StoredV2_18TriangleIsModificationNatural (W := W) alpha := by
  intro X Y f
  obtain rfl := IsDiscrete.eq_of_hom f
  have hf : f = 𝟙 X := Subsingleton.elim _ _
  rw [hf]
  simp

/-- Uniform stored-triangle modification naturality on an abstract discrete
base. -/
theorem higherStoredV2_18TriangleModificationNaturality_of_isDiscrete
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherStoredV2_18TriangleModificationNaturality (W := W) U := by
  intro H alpha
  exact storedV2_18TriangleIsModificationNatural_of_isDiscrete (W := W) alpha

/-- Factor-coherence lifting is automatic for coherent universal data whenever
the base category is `IsDiscrete`. -/
theorem higherFactorCoherenceLifting_of_isDiscrete
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherFactorCoherenceLifting (W := W) U :=
  higherFactorCoherenceLifting_of_storedTriangleNaturality
    W U
      (higherStoredV2_18TriangleModificationNaturality_of_isDiscrete
        (W := W) U)

/-- Coherent universal data on an abstract discrete base already determine a
full v2.18 weak universal property on the same chosen factorization. -/
theorem hasWeakHigherLocalizationUniversalProperty_of_isDiscrete_coherent
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HasWeakHigherLocalizationUniversalProperty (W := W) R := by
  exact ⟨weakHigherLocalizationUniversalPropertyOfCoherent
    W U (higherFactorCoherenceLifting_of_isDiscrete (W := W) U)⟩

/-- The same abstract discreteness kills the route obstruction: correction
lifting is automatic, independently of the supplied weak-universal witness. -/
theorem higherCoherentRouteCompleteness_of_isDiscrete
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherCoherentRouteCompleteness (W := W) U := by
  intro _hUniversal
  apply
    (higherStoredTriangleCorrectionLifting_iff_modificationTriangleLifting
      (W := W) U).mpr
  exact
    higherFactorModificationTriangleLifting_of_storedTriangleNaturality
      W U
        (higherStoredV2_18TriangleModificationNaturality_of_isDiscrete
          (W := W) U)

/-- Local alignment on every `IsDiscrete` base. -/
theorem higherWeakCoherentAlignment_of_isDiscrete
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherWeakCoherentAlignment (W := W) U :=
  ⟨hasWeakHigherLocalizationUniversalProperty_of_isDiscrete_coherent
      (W := W) U,
    higherCoherentRouteCompleteness_of_isDiscrete (W := W) U⟩

/-- Exact local v2.42 two-axis obstruction elimination on an arbitrary
`IsDiscrete` base category. -/
theorem no_twoAxisObstruction_of_isDiscrete
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    ¬ HigherWeakCoherentTwoAxisObstruction (W := W) U :=
  (higherWeakCoherentAlignment_iff_no_twoAxisObstruction
    (W := W) U).mp
      (higherWeakCoherentAlignment_of_isDiscrete (W := W) U)

/-- Global consequence: on any abstract discrete base, coherent universal-data
existence is the only remaining premise needed for both weak universality and
route completeness. -/
theorem universal_and_route_of_isDiscrete_coherentPrinciple
    (hCoherent : CoherentHigherWeakLocalizationUniversalPrinciple
      (W := W) (uH := uH) (vH := vH)) :
    HigherWeakLocalizationUniversalPrinciple
        (W := W) (uH := uH) (vH := vH) ∧
      HigherCoherentRouteCompletenessPrinciple
        (W := W) (uH := uH) (vH := vH) := by
  apply
    (higherWeakCoherentAlignmentPrinciple_iff_universal_and_route_of_coherent
      (W := W) hCoherent).mp
  intro R U
  exact higherWeakCoherentAlignment_of_isDiscrete (W := W) U

end KUOS.DependentOriginationIsDiscreteBaseObstructionEliminationV2_44
