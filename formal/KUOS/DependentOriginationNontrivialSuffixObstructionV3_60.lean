import KUOS.DependentOriginationInversePairSuffixPerturbationV3_59

namespace KUOS.DependentOriginationNontrivialSuffixObstructionV3_60

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationThreeRouteCorrectionCompatibilityGapV3_09
open KUOS.DependentOriginationQuotientGaugeIntersectionObstructionV3_11
open KUOS.DependentOriginationQuotientGaugeCoordinateKeyV3_14
open KUOS.DependentOriginationUnitorWitnessCorrelationV3_35
open KUOS.DependentOriginationAssociatorUnitorBoundaryReductionV3_36
open KUOS.DependentOriginationFiniteAssociatorScheduleV3_38
open KUOS.DependentOriginationFreshBoundaryCompatibilityV3_47
open KUOS.DependentOriginationGlobalCancellationFromSourceComplementsV3_52
open KUOS.DependentOriginationCompositeIdentityInversePairReductionV3_54
open KUOS.DependentOriginationInversePairBoundaryObstructionV3_55
open KUOS.DependentOriginationSourceComplementsGroupoidV3_57
open KUOS.DependentOriginationInversePairSuffixPerturbationV3_59

universe u v uH vH

set_option autoImplicit false

noncomputable section

/-!
# Nontrivial isolated suffix forces an inverse-pair obstruction v3.60

v3.59 constructs a fixed-gauge inverse-pair fresh-boundary obstruction after
perturbing one isolated suffix coordinate, but assumes the baseline gauge
already corrects the selected associator.

That assumption is unnecessary.

Fix a common-unitor gauge `Q` and one inverse-pair fresh-boundary task.  There
are only two cases:

1. `Q` already fails the selected associator.  Then v3.55 immediately
   recognizes `Q` itself as an
   `InversePairFreshBoundaryLeadingObstruction`.

2. `Q` corrects the selected associator.  If the isolated
   `gComp(f,g)` gauge fiber is nontrivial, Mathlib's `exists_ne` supplies an
   alternative value.  v3.59 changes exactly that coordinate, preserves all
   unitor corrections, and destroys the associator correction.

Hence one common unitor gauge plus one nontrivial isolated suffix fiber already
forces existence of a fixed-gauge inverse-pair fresh-boundary obstruction.

Under the v3.57 source-complement hypotheses, the faithfulness premise needed
by the v3.59 perturbation route is automatic.

This is a genuine strengthening of v3.59: no baseline associator-correction
hypothesis and no manually supplied alternative gauge value remain.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (R : RawHigherContextualSystem.{u, v, uH, vH}
  (Context := Context))
variable (D : PointwiseWAdjointEquivalenceData (W := W) R)

/-- A nontrivial isolated suffix fiber forces some fixed-gauge inverse-pair
fresh-boundary obstruction, without assuming the baseline gauge already
corrects the selected associator. -/
theorem exists_inversePairFreshBoundaryObstruction_of_nontrivial_isolated_fg
    {X Y T : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ X) (h : X ⟶ T)
    (hfg : f ≫ g = 𝟙 X)
    (hgf : g ≫ f = 𝟙 Y)
    (Q : GeneratedQuotientGaugeParameters W R D)
    [Nontrivial (QuotientGaugeCoordinateFiber W R D (.composition f g))]
    (hBoundary :
      FreshBoundaryAssociatorTask W
        ({ X := X, Y := Y, Z := X, T := T,
           f := f, g := g, h := h } : AssociatorTask W))
    (hIsolated : AssociatorFGInteriorIsolated W f g h)
    (hUnit : ∀ A (s : UnitorRouteAt W A),
      Q ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s))
    (hFaith :
      (quotientRepresentativeMap W R D h).toFunctor.Faithful) :
    ∃ Q' : GeneratedQuotientGaugeParameters W R D,
      (∀ A (s : UnitorRouteAt W A),
        Q' ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s)) ∧
      InversePairFreshBoundaryLeadingObstruction W R D Q'
        ({ X := X, Y := Y, Z := X, T := T,
           f := f, g := g, h := h } : AssociatorTask W) := by
  let a : AssociatorTask W :=
    { X := X, Y := Y, Z := X, T := T,
      f := f, g := g, h := h }
  have hInverse : IsCompositeInversePairAssociatorTask W a := by
    exact ⟨X, Y, T, f, g, h, hfg, hgf, rfl⟩
  have hBoundaryA : FreshBoundaryAssociatorTask W a := by
    simpa [a] using hBoundary
  by_cases hCorrect :
      Q ∈ quotientRouteCorrectionLocus W R D (.associator f g h)
  · obtain ⟨value, hDifferent⟩ :=
      exists_ne (Q.mapCompGauge f g)
    exact
      exists_inversePairFreshBoundaryObstruction_of_isolated_fg_perturbation
        W R D f g h hfg hgf Q value hBoundary hIsolated hDifferent
        hUnit hCorrect hFaith
  · have hNotCorrectA :
        Q ∉ quotientRouteCorrectionLocus W R D (associatorTaskRoute W a) := by
      simpa [a] using hCorrect
    have hObstruction :
        InversePairFreshBoundaryLeadingObstruction W R D Q a :=
      (inversePairFreshBoundaryLeadingObstruction_iff_not_corrected
        W R D Q a hBoundaryA hInverse).2 hNotCorrectA
    refine ⟨Q, hUnit, ?_⟩
    simpa [a] using hObstruction

/-- Under both v3.57 source-complement hypotheses, representative faithfulness
is automatic, so nontriviality plus isolation is the only remaining local
algebraic input beyond the common-unitor gauge and inverse-pair boundary task. -/
theorem exists_inversePairFreshBoundaryObstruction_of_nontrivial_isolated_fg_of_sourceComplements
    {X Y T : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ X) (h : X ⟶ T)
    (hfg : f ≫ g = 𝟙 X)
    (hgf : g ≫ f = 𝟙 Y)
    (Q : GeneratedQuotientGaugeParameters W R D)
    [Nontrivial (QuotientGaugeCoordinateFiber W R D (.composition f g))]
    (hBoundary :
      FreshBoundaryAssociatorTask W
        ({ X := X, Y := Y, Z := X, T := T,
           f := f, g := g, h := h } : AssociatorTask W))
    (hIsolated : AssociatorFGInteriorIsolated W f g h)
    (hUnit : ∀ A (s : UnitorRouteAt W A),
      Q ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s))
    (hLeft : HasLeftWCompositeComplements W)
    (hRight : HasRightWCompositeComplements W) :
    ∃ Q' : GeneratedQuotientGaugeParameters W R D,
      (∀ A (s : UnitorRouteAt W A),
        Q' ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s)) ∧
      InversePairFreshBoundaryLeadingObstruction W R D Q'
        ({ X := X, Y := Y, Z := X, T := T,
           f := f, g := g, h := h } : AssociatorTask W) := by
  have hEqv :
      (quotientRepresentativeMap W R D h).toFunctor.IsEquivalence :=
    allQuotientRepresentativeMaps_isEquivalence_of_sourceComplements
      W R D hLeft hRight h
  letI :
      (quotientRepresentativeMap W R D h).toFunctor.IsEquivalence := hEqv
  have hFaith :
      (quotientRepresentativeMap W R D h).toFunctor.Faithful := inferInstance
  exact
    exists_inversePairFreshBoundaryObstruction_of_nontrivial_isolated_fg
      W R D f g h hfg hgf Q hBoundary hIsolated hUnit hFaith

/-!
## Boundary after v3.60

The selected inverse-pair fresh-boundary obstruction now needs no baseline
associator-correction witness.

The exact sufficient mechanism is

```text
common unitor gauge
+ inverse-pair fresh-boundary task
+ isolated gComp(f,g)
+ Nontrivial gauge fiber at gComp(f,g)
+ Faithful representative(h)
------------------------------------------------
some fixed gauge preserves all unitors
and fails that associator
------------------------------------------------
InversePairFreshBoundaryLeadingObstruction.
```

Under v3.57 source complements, the final faithfulness line is automatic.

Thus the remaining local algebraic question has become sharply concrete:
is the dependent quotient-gauge fiber at an isolated inverse-pair suffix
actually nontrivial?

The next theorem unit should attack that fiber nontriviality directly.  The
v2.69 C2 countermodel supplies a concrete nontrivial automorphism in the target
fiber, but it still has to be transported into the exact dependent
`QuotientGaugeCoordinateFiber` used here.  That transport must be proved, not
inferred from generated-holonomy nontriviality.

No universal obstruction existence, no failure of all correction mechanisms,
no weak-admissibility derivation of source complements, and no final Stage I/II
universality claim is made here.  Protected validation-only PR #1558 is
untouched.
-/

end

end KUOS.DependentOriginationNontrivialSuffixObstructionV3_60
