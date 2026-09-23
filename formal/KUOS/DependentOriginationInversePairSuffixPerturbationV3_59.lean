import KUOS.DependentOriginationGroupoidHolonomySeparationV3_58

namespace KUOS.DependentOriginationInversePairSuffixPerturbationV3_59

open CategoryTheory
open CategoryTheory.Bicategory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationCoherenceDefectsV2_65
open KUOS.DependentOriginationGeneratedPointwiseChoiceV2_68
open KUOS.DependentOriginationFiveGeneratedCorrectionCoboundaryV3_00
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationQuotientDefectOrbitV3_06
open KUOS.DependentOriginationThreeRouteCorrectionCompatibilityGapV3_09
open KUOS.DependentOriginationQuotientGaugeIntersectionObstructionV3_11
open KUOS.DependentOriginationQuotientGaugeCoordinateFootprintV3_12
open KUOS.DependentOriginationQuotientGaugeCoordinateKeyV3_14
open KUOS.DependentOriginationAssociatorThreeOfFourRigidityV3_23
open KUOS.DependentOriginationAssociatorUnitorOneSidedSeparationV3_28
open KUOS.DependentOriginationUnitorWitnessCorrelationV3_35
open KUOS.DependentOriginationAssociatorUnitorBoundaryReductionV3_36
open KUOS.DependentOriginationFreshAssociatorCompletionV3_37
open KUOS.DependentOriginationFiniteAssociatorScheduleV3_38
open KUOS.DependentOriginationFreshBoundaryCompatibilityV3_47
open KUOS.DependentOriginationGlobalCancellationFromSourceComplementsV3_52
open KUOS.DependentOriginationCompositeIdentityInversePairReductionV3_54
open KUOS.DependentOriginationInversePairBoundaryObstructionV3_55
open KUOS.DependentOriginationSourceComplementsGroupoidV3_57
open KUOS.DependentOriginationGroupoidHolonomySeparationV3_58

universe u v uH vH

set_option autoImplicit false

noncomputable section

/-!
# Inverse-pair interior-suffix perturbation v3.59

v3.58 shows that groupoid source geometry and equivalence of all quotient
representative functors do not, by themselves, force generated holonomy to
vanish.  The remaining v3.55 question is more local and sharper: can one
produce a *fixed quotient gauge* that still corrects every unitor while failing
one inverse-pair fresh-boundary associator?

This module gives a direct construction under an explicit and minimal local
nontriviality hypothesis.

The key new rigidity theorem is the suffix analogue of v3.23.  Suppose two
gauges both correct the same associator.  If their leading coordinate,
`gComp(g,h)`, and `gComp(f,g≫h)` agree, then equality of the remaining
`gComp(f,g)` coordinate follows as soon as the representative of `h` is
faithful.  The proof cancels the common invertible prefix and suffix in the
actual v2.65 associator equation, then cancels right whiskering using Mathlib's
faithful-whiskering functor.

Under v3.57 source complements that faithfulness premise is automatic, because
every quotient representative is an equivalence of categories.

We then perturb only the `gComp(f,g)` coordinate.  If that coordinate is
outside the whole unitor-visible boundary and isolated from the other three
associator footprint keys, footprint locality preserves every unitor
correction.  If the new value is genuinely different, the suffix rigidity
theorem forbids the perturbed gauge from correcting the associator.

For an inverse-pair fresh-boundary task this constructs exactly the v3.55
`InversePairFreshBoundaryLeadingObstruction` at a fixed gauge.

No universal existence of a nontrivial perturbation value is asserted.  The
result isolates the final algebraic input needed for a concrete counterexample:
one interior composition-gauge fiber with at least two values.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (R : RawHigherContextualSystem.{u, v, uH, vH}
  (Context := Context))
variable (D : PointwiseWAdjointEquivalenceData (W := W) R)

/-- The `gComp(f,g)` coordinate is isolated from the other three associator
coordinates and from every unitor footprint. -/
def AssociatorFGInteriorIsolated
    {X Y Z T : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T) : Prop :=
  (QuotientGaugeCoordinate.composition f g ≠
      .composition (f ≫ g) h) ∧
    (QuotientGaugeCoordinate.composition f g ≠
      .composition g h) ∧
    (QuotientGaugeCoordinate.composition f g ≠
      .composition f (g ≫ h)) ∧
    ¬ UnitorVisibleCoordinate W (.composition f g)

/-- Suffix rigidity for the `gComp(f,g)` coordinate.

Unlike v3.23's leading-coordinate rigidity, this direction must cancel right
whiskering by the representative of `h`.  Faithfulness is exactly the needed
and sufficient one-sided semantic hypothesis. -/
theorem associator_mapComp_f_g_eq_of_corrected_of_other_three_eq_of_faithful
    {X Y Z T : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T)
    (Q Q' : GeneratedQuotientGaugeParameters W R D)
    (hQ :
      Q ∈ quotientRouteCorrectionLocus W R D (.associator f g h))
    (hQ' :
      Q' ∈ quotientRouteCorrectionLocus W R D (.associator f g h))
    (hLead :
      Q.mapCompGauge (f ≫ g) h = Q'.mapCompGauge (f ≫ g) h)
    (hGH :
      Q.mapCompGauge g h = Q'.mapCompGauge g h)
    (hFGH :
      Q.mapCompGauge f (g ≫ h) = Q'.mapCompGauge f (g ≫ h))
    (hFaith :
      (quotientRepresentativeMap W R D h).toFunctor.Faithful) :
    Q.mapCompGauge f g = Q'.mapCompGauge f g := by
  change
    quotientAssociatorDefect W R D
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q)
      f g h = Iso.refl _ at hQ
  change
    quotientAssociatorDefect W R D
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q')
      f g h = Iso.refl _ at hQ'
  have hEqQ :=
    (quotientAssociatorDefect_eq_refl_iff W R D
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q)
      f g h).1 hQ
  have hEqQ' :=
    (quotientAssociatorDefect_eq_refl_iff W R D
      (quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q')
      f g h).1 hQ'

  let F := quotientRepresentativeMap W R D f
  let H := quotientRepresentativeMap W R D h
  let S := quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q
  let S' := quotientGaugeAdjustedGeneratedPointwiseChoice W R D Q'

  have hAdjustedLead :
      S.mapComp (f ≫ g) h = S'.mapComp (f ≫ g) h := by
    dsimp [S, S']
    simpa [quotientGaugeAdjustedGeneratedPointwiseChoice,
      gaugeAdjustedGeneratedPointwiseChoice,
      canonicalPointwiseGaugeOfQuotientGauge,
      extendGeneratedQuotientGaugeParameters] using
      congrArg
        (fun q => generatedCompositionMapIso W R D (f ≫ g) h ≪≫ q)
        hLead
  have hAdjustedGH :
      S.mapComp g h = S'.mapComp g h := by
    dsimp [S, S']
    simpa [quotientGaugeAdjustedGeneratedPointwiseChoice,
      gaugeAdjustedGeneratedPointwiseChoice,
      canonicalPointwiseGaugeOfQuotientGauge,
      extendGeneratedQuotientGaugeParameters] using
      congrArg
        (fun q => generatedCompositionMapIso W R D g h ≪≫ q)
        hGH
  have hAdjustedFGH :
      S.mapComp f (g ≫ h) = S'.mapComp f (g ≫ h) := by
    dsimp [S, S']
    simpa [quotientGaugeAdjustedGeneratedPointwiseChoice,
      gaugeAdjustedGeneratedPointwiseChoice,
      canonicalPointwiseGaugeOfQuotientGauge,
      extendGeneratedQuotientGaugeParameters] using
      congrArg
        (fun q => generatedCompositionMapIso W R D f (g ≫ h) ≪≫ q)
        hFGH
  have hAdjustedLeadHom := congrArg Iso.hom hAdjustedLead
  have hAdjustedGHInv := congrArg Iso.inv hAdjustedGH
  have hAdjustedFGHInv := congrArg Iso.inv hAdjustedFGH

  have hComposite :
      (S.mapComp (f ≫ g) h).hom ≫
          ((S.mapComp f g).hom ▷ H) ≫
          (α_
            (quotientRepresentativeMap W R D f)
            (quotientRepresentativeMap W R D g)
            H).hom ≫
          (F ◁ (S.mapComp g h).inv) ≫
          (S.mapComp f (g ≫ h)).inv =
        (S.mapComp (f ≫ g) h).hom ≫
          ((S'.mapComp f g).hom ▷ H) ≫
          (α_
            (quotientRepresentativeMap W R D f)
            (quotientRepresentativeMap W R D g)
            H).hom ≫
          (F ◁ (S.mapComp g h).inv) ≫
          (S.mapComp f (g ≫ h)).inv := by
    calc
      (S.mapComp (f ≫ g) h).hom ≫
          ((S.mapComp f g).hom ▷ H) ≫
          (α_
            (quotientRepresentativeMap W R D f)
            (quotientRepresentativeMap W R D g)
            H).hom ≫
          (F ◁ (S.mapComp g h).inv) ≫
          (S.mapComp f (g ≫ h)).inv =
        eqToHom (by simp) := by
          simpa [S, F, H] using hEqQ
      _ =
        (S'.mapComp (f ≫ g) h).hom ≫
          ((S'.mapComp f g).hom ▷ H) ≫
          (α_
            (quotientRepresentativeMap W R D f)
            (quotientRepresentativeMap W R D g)
            H).hom ≫
          (F ◁ (S'.mapComp g h).inv) ≫
          (S'.mapComp f (g ≫ h)).inv := by
          simpa [S', F, H] using hEqQ'.symm
      _ =
        (S.mapComp (f ≫ g) h).hom ≫
          ((S'.mapComp f g).hom ▷ H) ≫
          (α_
            (quotientRepresentativeMap W R D f)
            (quotientRepresentativeMap W R D g)
            H).hom ≫
          (F ◁ (S.mapComp g h).inv) ≫
          (S.mapComp f (g ≫ h)).inv := by
          rw [← hAdjustedLeadHom, ← hAdjustedGHInv, ← hAdjustedFGHInv]

  have hWhisk :
      (S.mapComp f g).hom ▷ H =
        (S'.mapComp f g).hom ▷ H := by
    apply (cancel_epi (S.mapComp (f ≫ g) h).hom).1
    apply
      (cancel_mono
        ((α_
            (quotientRepresentativeMap W R D f)
            (quotientRepresentativeMap W R D g)
            H).hom ≫
          (F ◁ (S.mapComp g h).inv) ≫
          (S.mapComp f (g ≫ h)).inv)).1
    simpa only [Category.assoc] using hComposite

  letI : H.toFunctor.Faithful := by
    simpa [H] using hFaith
  have hAdjustedFGHom :
      (S.mapComp f g).hom = (S'.mapComp f g).hom := by
    apply Cat.Hom₂.ext
    have hNat :
        Functor.whiskerRight (S.mapComp f g).hom.toNatTrans H.toFunctor =
          Functor.whiskerRight (S'.mapComp f g).hom.toNatTrans H.toFunctor := by
      simpa [H] using congrArg (fun k => k.toNatTrans) hWhisk
    exact
      ((Functor.whiskeringRight
        (R.obj (.mk X.as.obj))
        (R.obj (.mk Z.as.obj))
        (R.obj (.mk T.as.obj))).obj H.toFunctor).map_injective hNat

  have hGaugeHom :
      (Q.mapCompGauge f g).hom = (Q'.mapCompGauge f g).hom := by
    apply (cancel_epi (generatedCompositionMapIso W R D f g).hom).1
    simpa [S, S',
      quotientGaugeAdjustedGeneratedPointwiseChoice,
      gaugeAdjustedGeneratedPointwiseChoice,
      canonicalPointwiseGaugeOfQuotientGauge,
      extendGeneratedQuotientGaugeParameters,
      Iso.trans_hom] using hAdjustedFGHom
  apply Iso.ext
  exact hGaugeHom

/-- Updating one coordinate outside the entire unitor-visible boundary preserves
all unitor corrections. -/
theorem fgGaugeUpdate_preserves_all_unitors
    {X Y Z : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z)
    (Q : GeneratedQuotientGaugeParameters W R D)
    (value : QuotientGaugeCoordinateFiber W R D (.composition f g))
    (hInvisible :
      ¬ UnitorVisibleCoordinate W (.composition f g))
    (hUnit : ∀ A (s : UnitorRouteAt W A),
      Q ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s)) :
    ∀ A (s : UnitorRouteAt W A),
      quotientGaugeUpdate W R D Q (.composition f g) value ∈
        quotientRouteCorrectionLocus W R D (unitorRouteState W s) := by
  intro A s
  have hNotMem :
      ¬ RouteFootprintContains W (unitorRouteState W s) (.composition f g) := by
    intro hMem
    exact hInvisible
      (unitorVisibleCoordinate_of_mem W s (.composition f g) hMem)
  exact
    (quotientGaugeUpdate_mem_locus_iff_of_not_mem
      W R D Q (.composition f g) value (unitorRouteState W s) hNotMem).2
      (hUnit A s)

/-- An isolated nontrivial `gComp(f,g)` perturbation destroys associator
correction whenever right whiskering by the representative of `h` is
faithful. -/
theorem associator_not_corrected_after_isolated_fg_perturbation
    {X Y Z T : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T)
    (Q : GeneratedQuotientGaugeParameters W R D)
    (value : QuotientGaugeCoordinateFiber W R D (.composition f g))
    (hIsolated : AssociatorFGInteriorIsolated W f g h)
    (hDifferent : value ≠ Q.mapCompGauge f g)
    (hCorrect :
      Q ∈ quotientRouteCorrectionLocus W R D (.associator f g h))
    (hFaith :
      (quotientRepresentativeMap W R D h).toFunctor.Faithful) :
    quotientGaugeUpdate W R D Q (.composition f g) value ∉
      quotientRouteCorrectionLocus W R D (.associator f g h) := by
  intro hUpdated
  let Q' := quotientGaugeUpdate W R D Q (.composition f g) value
  have hLead :
      Q.mapCompGauge (f ≫ g) h = Q'.mapCompGauge (f ≫ g) h := by
    symm
    dsimp [Q']
    exact
      quotientGaugeUpdate_value_of_ne
        W R D Q (.composition f g) value
        (.composition (f ≫ g) h) hIsolated.1.symm
  have hGH :
      Q.mapCompGauge g h = Q'.mapCompGauge g h := by
    symm
    dsimp [Q']
    exact
      quotientGaugeUpdate_value_of_ne
        W R D Q (.composition f g) value
        (.composition g h) hIsolated.2.1.symm
  have hFGH :
      Q.mapCompGauge f (g ≫ h) = Q'.mapCompGauge f (g ≫ h) := by
    symm
    dsimp [Q']
    exact
      quotientGaugeUpdate_value_of_ne
        W R D Q (.composition f g) value
        (.composition f (g ≫ h)) hIsolated.2.2.1.symm
  have hUpdated' :
      Q' ∈ quotientRouteCorrectionLocus W R D (.associator f g h) := by
    simpa [Q'] using hUpdated
  have hFG :
      Q.mapCompGauge f g = Q'.mapCompGauge f g :=
    associator_mapComp_f_g_eq_of_corrected_of_other_three_eq_of_faithful
      W R D f g h Q Q' hCorrect hUpdated' hLead hGH hFGH hFaith
  have hSelf : Q'.mapCompGauge f g = value := by
    dsimp [Q']
    exact
      quotientGaugeUpdate_value_self
        W R D Q (.composition f g) value
  exact hDifferent (hSelf.symm.trans hFG.symm)

/-- Exact fixed-gauge inverse-pair fresh-boundary obstruction construction.

Starting from one gauge correcting all unitors and the selected associator,
perturb one isolated interior suffix coordinate.  The new gauge still corrects
all unitors but fails this inverse-pair fresh-boundary associator. -/
theorem exists_inversePairFreshBoundaryObstruction_of_isolated_fg_perturbation
    {X Y T : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ X) (h : X ⟶ T)
    (hfg : f ≫ g = 𝟙 X)
    (hgf : g ≫ f = 𝟙 Y)
    (Q : GeneratedQuotientGaugeParameters W R D)
    (value : QuotientGaugeCoordinateFiber W R D (.composition f g))
    (hBoundary :
      FreshBoundaryAssociatorTask W
        ({ X := X, Y := Y, Z := X, T := T,
           f := f, g := g, h := h } : AssociatorTask W))
    (hIsolated : AssociatorFGInteriorIsolated W f g h)
    (hDifferent : value ≠ Q.mapCompGauge f g)
    (hUnit : ∀ A (s : UnitorRouteAt W A),
      Q ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s))
    (hCorrect :
      Q ∈ quotientRouteCorrectionLocus W R D (.associator f g h))
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
  let Q' := quotientGaugeUpdate W R D Q (.composition f g) value
  have hUnit' :
      ∀ A (s : UnitorRouteAt W A),
        Q' ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s) := by
    dsimp [Q']
    exact
      fgGaugeUpdate_preserves_all_unitors
        W R D f g Q value hIsolated.2.2.2 hUnit
  have hNotCorrect :
      Q' ∉ quotientRouteCorrectionLocus W R D (associatorTaskRoute W a) := by
    change Q' ∉ quotientRouteCorrectionLocus W R D (.associator f g h)
    dsimp [Q']
    exact
      associator_not_corrected_after_isolated_fg_perturbation
        W R D f g h Q value hIsolated hDifferent hCorrect hFaith
  have hInverse : IsCompositeInversePairAssociatorTask W a := by
    exact ⟨X, Y, T, f, g, h, hfg, hgf, rfl⟩
  have hBoundaryA : FreshBoundaryAssociatorTask W a := by
    simpa [a] using hBoundary
  have hObstruction :
      InversePairFreshBoundaryLeadingObstruction W R D Q' a :=
    (inversePairFreshBoundaryLeadingObstruction_iff_not_corrected
      W R D Q' a hBoundaryA hInverse).2 hNotCorrect
  refine ⟨Q', hUnit', ?_⟩
  simpa [a] using hObstruction

/-- Under the v3.57 source-complement geometry the faithfulness premise of the
preceding construction is automatic. -/
theorem exists_inversePairFreshBoundaryObstruction_of_sourceComplements
    {X Y T : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ X) (h : X ⟶ T)
    (hfg : f ≫ g = 𝟙 X)
    (hgf : g ≫ f = 𝟙 Y)
    (Q : GeneratedQuotientGaugeParameters W R D)
    (value : QuotientGaugeCoordinateFiber W R D (.composition f g))
    (hBoundary :
      FreshBoundaryAssociatorTask W
        ({ X := X, Y := Y, Z := X, T := T,
           f := f, g := g, h := h } : AssociatorTask W))
    (hIsolated : AssociatorFGInteriorIsolated W f g h)
    (hDifferent : value ≠ Q.mapCompGauge f g)
    (hUnit : ∀ A (s : UnitorRouteAt W A),
      Q ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s))
    (hCorrect :
      Q ∈ quotientRouteCorrectionLocus W R D (.associator f g h))
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
    exists_inversePairFreshBoundaryObstruction_of_isolated_fg_perturbation
      W R D f g h hfg hgf Q value hBoundary hIsolated hDifferent
      hUnit hCorrect hFaith

/-!
## Boundary after v3.59

The inverse-pair fresh-boundary residual is now known to be constructible at a
fixed gauge whenever one specific interior suffix coordinate admits a
nontrivial perturbation.

The mechanism is exact:

```text
baseline gauge corrects all unitors + selected associator
isolated gComp(f,g) is outside the unitor boundary
alternative value at that gauge fiber
representative(h) faithful
---------------------------------------------------------
perturbed gauge still corrects every unitor
perturbed gauge fails the selected associator
---------------------------------------------------------
InversePairFreshBoundaryLeadingObstruction
```

Under v3.57 source complements, representative faithfulness is automatic.

Thus groupoidality does not by itself force the fresh-boundary residual to
vanish.  What can still prevent this construction is now sharply algebraic:
the relevant interior gauge fiber may be subsingleton, or the selected suffix
coordinate may fail the isolation condition.

The next truth test should therefore determine whether the actual generated
gauge fibers in a concrete KuuOS model admit such a nontrivial isolated value.
The existing v2.69 C2 automorphism carrier is a natural candidate, but the
dependent quotient-gauge fiber identification must be proved rather than
assumed.

No universal obstruction existence, no failure of correctability, no
schedule/seed/W/R/D independence, and no final Stage I/II universality claim is
made here.  Protected validation-only PR #1558 is untouched.
-/

end

end KUOS.DependentOriginationInversePairSuffixPerturbationV3_59
