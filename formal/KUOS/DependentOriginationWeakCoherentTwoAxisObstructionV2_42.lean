import KUOS.DependentOriginationSplitToCoherentForwardExactV2_41
import KUOS.DependentOriginationCoherentStageIIIGapCollapseV2_32

namespace KUOS.DependentOriginationWeakCoherentTwoAxisObstructionV2_42

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationWeakHigherLocalizationGapDecompositionV2_31
open KUOS.DependentOriginationCoherentStageIIIGapCollapseV2_32
open KUOS.DependentOriginationStageIIIRouteCompletenessV2_33
open KUOS.DependentOriginationForwardFactorCoherenceSelectionV2_40
open KUOS.DependentOriginationSplitToCoherentForwardExactV2_41

universe u v uH vH

/-!
# Weak/coherent two-axis obstruction v2.42

The v2.41 layer closes the internal fixed-carrier reflection gap for an already
supplied coherent universal datum `U`.  In particular, coherent route failure is
now exactly the existence of a Stage III-completed weak carrier on which every
forward v2.18 factor fails the modification-triangle test.

There is, however, a logically different failure mode that route completeness
cannot detect: the raw system may have no Stage III-completed weak carrier at all.
For a coherent datum `U`, v2.32 already identifies that failure exactly with the
Stage III essential-uniqueness obstruction.

This file separates those two axes:

```text
Axis E  (existence)
  no completed weak carrier exists
  = HigherWeakEssentialUniquenessObstruction

Axis R  (route)
  a completed weak carrier exists, but the fixed coherent route fails
  = HigherFixedChosenForwardModificationTriangleObstruction.
```

The axes are locally mutually exclusive.  Indeed, Axis R itself contains a
completed carrier, while Axis E asserts that no completed carrier exists.
Moreover, Axis E makes route completeness vacuously true because the premise of
`HigherCoherentRouteCompleteness` is the existence of a weak universal property.
Conversely, Axis R implies that a weak universal property really exists and that
only the chosen coherent route fails.

Thus one coherent datum has exactly three logical states:

1. weak-universality existence obstruction;
2. fixed coherent route obstruction;
3. weak/coherent alignment: weak universality exists and the route is complete.

The file also globalizes this decomposition.  Relative to the still-explicit
coherent universal principle, the conjunction

```text
HigherWeakLocalizationUniversalPrinciple
  +
HigherCoherentRouteCompletenessPrinciple
```

is equivalent to absence of the two global obstruction classes.

No global existence or route-completeness principle is proved here.  The point
is to make the remaining open content disjoint and exact rather than to hide it
inside one implication.  No strictification, ordinary-localization substitute,
new axiom, `sorry`, or `admit` is introduced.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Local aligned state for one coherent datum: a v2.18 weak universal property
exists somewhere on the raw system and the fixed coherent datum reflects that
universality through its chosen route. -/
def HigherWeakCoherentAlignment
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  HasWeakHigherLocalizationUniversalProperty (W := W) R ∧
    HigherCoherentRouteCompleteness (W := W) U

/-- Exact local two-axis obstruction for one coherent datum. -/
def HigherWeakCoherentTwoAxisObstruction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  HigherWeakEssentialUniquenessObstruction (W := W) R ∨
    HigherFixedChosenForwardModificationTriangleObstruction (W := W) U

/-- A fixed-route obstruction already contains a Stage III-completed candidate,
so it implies existence of the v2.18 weak universal property. -/
theorem hasWeakHigherLocalizationUniversalProperty_of_forwardModificationTriangleObstruction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hObs : HigherFixedChosenForwardModificationTriangleObstruction (W := W) U) :
    HasWeakHigherLocalizationUniversalProperty (W := W) R := by
  rcases hObs with ⟨C, hUnique, _⟩
  exact
    (hasWeakHigherLocalizationUniversalProperty_iff_candidateWithUniqueness
      (W := W) R).mpr ⟨C, hUnique⟩

/-- In the Stage III existence-obstructed state, route completeness is vacuous:
its premise, existence of a weak universal property, is false. -/
theorem routeCompleteness_of_essentialUniquenessObstruction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hObs : HigherWeakEssentialUniquenessObstruction (W := W) R) :
    HigherCoherentRouteCompleteness (W := W) U := by
  intro hUniversal
  exact False.elim
    (((not_hasWeakHigherLocalizationUniversalProperty_iff_essentialUniquenessObstruction_of_coherent
      (W := W) U).mpr hObs) hUniversal)

/-- The existence and route obstruction axes cannot occur simultaneously on the
same raw system/coherent datum. -/
theorem essentialUniquenessObstruction_disjoint_forwardModificationTriangleObstruction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    ¬ (HigherWeakEssentialUniquenessObstruction (W := W) R ∧
      HigherFixedChosenForwardModificationTriangleObstruction (W := W) U) := by
  rintro ⟨hExistenceObs, hRouteObs⟩
  have hUniversal : HasWeakHigherLocalizationUniversalProperty (W := W) R :=
    hasWeakHigherLocalizationUniversalProperty_of_forwardModificationTriangleObstruction
      (W := W) U hRouteObs
  exact
    ((not_hasWeakHigherLocalizationUniversalProperty_iff_essentialUniquenessObstruction_of_coherent
      (W := W) U).mpr hExistenceObs) hUniversal

/-- Exact local success normal form: weak/coherent alignment is equivalent to
absence of both obstruction axes. -/
theorem higherWeakCoherentAlignment_iff_no_twoAxisObstruction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherWeakCoherentAlignment (W := W) U ↔
      ¬ HigherWeakCoherentTwoAxisObstruction (W := W) U := by
  classical
  constructor
  · rintro ⟨hUniversal, hRoute⟩ hObs
    rcases hObs with hExistenceObs | hRouteObs
    · exact
        ((not_hasWeakHigherLocalizationUniversalProperty_iff_essentialUniquenessObstruction_of_coherent
          (W := W) U).mpr hExistenceObs) hUniversal
    · exact
        ((not_routeCompleteness_iff_forwardModificationTriangleObstruction
          (W := W) U).mpr hRouteObs) hRoute
  · intro hNoObs
    have hUniversal : HasWeakHigherLocalizationUniversalProperty (W := W) R := by
      by_contra hNoUniversal
      apply hNoObs
      exact Or.inl
        ((not_hasWeakHigherLocalizationUniversalProperty_iff_essentialUniquenessObstruction_of_coherent
          (W := W) U).mp hNoUniversal)
    have hRoute : HigherCoherentRouteCompleteness (W := W) U := by
      by_contra hNoRoute
      apply hNoObs
      exact Or.inr
        ((not_routeCompleteness_iff_forwardModificationTriangleObstruction
          (W := W) U).mp hNoRoute)
    exact ⟨hUniversal, hRoute⟩

/-- Exact local failure normal form. -/
theorem not_higherWeakCoherentAlignment_iff_twoAxisObstruction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    (¬ HigherWeakCoherentAlignment (W := W) U) ↔
      HigherWeakCoherentTwoAxisObstruction (W := W) U := by
  classical
  constructor
  · intro hNoAlignment
    by_contra hNoObs
    exact hNoAlignment
      ((higherWeakCoherentAlignment_iff_no_twoAxisObstruction
        (W := W) U).mpr hNoObs)
  · intro hObs hAlignment
    exact
      ((higherWeakCoherentAlignment_iff_no_twoAxisObstruction
        (W := W) U).mp hAlignment) hObs

/-- Because the two axes are disjoint, the local obstruction is an exclusive
dichotomy rather than a merely inclusive disjunction. -/
theorem twoAxisObstruction_iff_exclusiveDichotomy
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherWeakCoherentTwoAxisObstruction (W := W) U ↔
      (HigherWeakEssentialUniquenessObstruction (W := W) R ∧
        ¬ HigherFixedChosenForwardModificationTriangleObstruction (W := W) U) ∨
      (¬ HigherWeakEssentialUniquenessObstruction (W := W) R ∧
        HigherFixedChosenForwardModificationTriangleObstruction (W := W) U) := by
  constructor
  · intro hObs
    rcases hObs with hExistenceObs | hRouteObs
    · exact Or.inl
        ⟨hExistenceObs, fun hRouteObs =>
          (essentialUniquenessObstruction_disjoint_forwardModificationTriangleObstruction
            (W := W) U) ⟨hExistenceObs, hRouteObs⟩⟩
    · exact Or.inr
        ⟨(fun hExistenceObs =>
          (essentialUniquenessObstruction_disjoint_forwardModificationTriangleObstruction
            (W := W) U) ⟨hExistenceObs, hRouteObs⟩), hRouteObs⟩
  · rintro (⟨hExistenceObs, _⟩ | ⟨_, hRouteObs⟩)
    · exact Or.inl hExistenceObs
    · exact Or.inr hRouteObs

/-- Complete local three-state classification for one coherent datum. -/
theorem coherentDatum_stateTrichotomy
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherWeakEssentialUniquenessObstruction (W := W) R ∨
      HigherFixedChosenForwardModificationTriangleObstruction (W := W) U ∨
        HigherWeakCoherentAlignment (W := W) U := by
  classical
  by_cases hExistenceObs : HigherWeakEssentialUniquenessObstruction (W := W) R
  · exact Or.inl hExistenceObs
  · by_cases hRouteObs :
      HigherFixedChosenForwardModificationTriangleObstruction (W := W) U
    · exact Or.inr (Or.inl hRouteObs)
    · exact Or.inr (Or.inr
        ((higherWeakCoherentAlignment_iff_no_twoAxisObstruction
          (W := W) U).mpr (by
            intro hObs
            rcases hObs with hE | hR
            · exact hExistenceObs hE
            · exact hRouteObs hR)))

/-- Global alignment over every coherent datum that actually exists.  This does
not itself assert that coherent data exist for every admissible raw system. -/
def HigherWeakCoherentAlignmentPrinciple : Prop :=
  ∀ (R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH))
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R),
    HigherWeakCoherentAlignment (W := W) U

/-- Global witness of the weak-universality existence axis, restricted to raw
systems that carry an actual coherent datum. -/
def HigherGlobalWeakStageIIIExistenceObstruction : Prop :=
  ∃ (R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH))
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R),
    HigherWeakEssentialUniquenessObstruction (W := W) R

/-- Global witness of the fixed coherent route axis. -/
def HigherGlobalFixedRouteObstruction : Prop :=
  ∃ (R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH))
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R),
    HigherFixedChosenForwardModificationTriangleObstruction (W := W) U

/-- The two global obstruction classes.  They may coexist globally on different
raw systems even though they are mutually exclusive for one fixed `R,U`. -/
def HigherGlobalWeakCoherentTwoAxisObstruction : Prop :=
  HigherGlobalWeakStageIIIExistenceObstruction
      (W := W) (uH := uH) (vH := vH) ∨
    HigherGlobalFixedRouteObstruction
      (W := W) (uH := uH) (vH := vH)

/-- Relative to a coherent universal principle, global weak/coherent alignment is
exactly the conjunction of the v2.18 weak universal principle and the v2.33
route-completeness principle. -/
theorem higherWeakCoherentAlignmentPrinciple_iff_universal_and_route_of_coherent
    (hCoherent : CoherentHigherWeakLocalizationUniversalPrinciple
      (W := W) (uH := uH) (vH := vH)) :
    HigherWeakCoherentAlignmentPrinciple
        (W := W) (uH := uH) (vH := vH) ↔
      (HigherWeakLocalizationUniversalPrinciple
          (W := W) (uH := uH) (vH := vH) ∧
        HigherCoherentRouteCompletenessPrinciple
          (W := W) (uH := uH) (vH := vH)) := by
  constructor
  · intro hAlignment
    constructor
    · intro R hR
      rcases hCoherent R hR with ⟨U⟩
      exact (hAlignment R U).1
    · intro R U
      exact (hAlignment R U).2
  · rintro ⟨hUniversal, hRoute⟩ R U
    have hR : IsHigherWAdmissible W R :=
      hasCoherentWeakHigherLocalizationUniversalProperty_isHigherWAdmissible W ⟨U⟩
    exact ⟨hUniversal R hR, hRoute R U⟩

/-- Under a coherent universal principle, failure of the global v2.18 weak
universal principle is exactly a global Stage III existence witness. -/
theorem not_higherWeakLocalizationUniversalPrinciple_iff_globalWeakStageIIIExistenceObstruction_of_coherent
    (hCoherent : CoherentHigherWeakLocalizationUniversalPrinciple
      (W := W) (uH := uH) (vH := vH)) :
    (¬ HigherWeakLocalizationUniversalPrinciple
        (W := W) (uH := uH) (vH := vH)) ↔
      HigherGlobalWeakStageIIIExistenceObstruction
        (W := W) (uH := uH) (vH := vH) := by
  classical
  constructor
  · intro hNoUniversalPrinciple
    by_contra hNoGlobalObs
    apply hNoUniversalPrinciple
    intro R hR
    rcases hCoherent R hR with ⟨U⟩
    by_contra hNoUniversal
    apply hNoGlobalObs
    exact ⟨R, U,
      (not_hasWeakHigherLocalizationUniversalProperty_iff_essentialUniquenessObstruction_of_coherent
        (W := W) U).mp hNoUniversal⟩
  · rintro ⟨R, U, hExistenceObs⟩ hUniversalPrinciple
    have hR : IsHigherWAdmissible W R :=
      hasCoherentWeakHigherLocalizationUniversalProperty_isHigherWAdmissible W ⟨U⟩
    have hUniversal : HasWeakHigherLocalizationUniversalProperty (W := W) R :=
      hUniversalPrinciple R hR
    exact
      ((not_hasWeakHigherLocalizationUniversalProperty_iff_essentialUniquenessObstruction_of_coherent
        (W := W) U).mpr hExistenceObs) hUniversal

/-- Failure of the global route-completeness principle is exactly a global
forward-modification-triangle obstruction witness. -/
theorem not_higherCoherentRouteCompletenessPrinciple_iff_globalFixedRouteObstruction :
    (¬ HigherCoherentRouteCompletenessPrinciple
        (W := W) (uH := uH) (vH := vH)) ↔
      HigherGlobalFixedRouteObstruction
        (W := W) (uH := uH) (vH := vH) := by
  classical
  constructor
  · intro hNoRoutePrinciple
    by_contra hNoGlobalObs
    apply hNoRoutePrinciple
    intro R U
    by_contra hNoRoute
    apply hNoGlobalObs
    exact ⟨R, U,
      (not_routeCompleteness_iff_forwardModificationTriangleObstruction
        (W := W) U).mp hNoRoute⟩
  · rintro ⟨R, U, hRouteObs⟩ hRoutePrinciple
    exact
      ((not_routeCompleteness_iff_forwardModificationTriangleObstruction
        (W := W) U).mpr hRouteObs) (hRoutePrinciple R U)

/-- Global alignment is exactly absence of both global obstruction classes. -/
theorem higherWeakCoherentAlignmentPrinciple_iff_no_globalTwoAxisObstruction :
    HigherWeakCoherentAlignmentPrinciple
        (W := W) (uH := uH) (vH := vH) ↔
      ¬ HigherGlobalWeakCoherentTwoAxisObstruction
        (W := W) (uH := uH) (vH := vH) := by
  constructor
  · intro hAlignment hGlobalObs
    rcases hGlobalObs with hExistenceGlobal | hRouteGlobal
    · rcases hExistenceGlobal with ⟨R, U, hExistenceObs⟩
      exact
        ((higherWeakCoherentAlignment_iff_no_twoAxisObstruction
          (W := W) U).mp (hAlignment R U)) (Or.inl hExistenceObs)
    · rcases hRouteGlobal with ⟨R, U, hRouteObs⟩
      exact
        ((higherWeakCoherentAlignment_iff_no_twoAxisObstruction
          (W := W) U).mp (hAlignment R U)) (Or.inr hRouteObs)
  · intro hNoGlobalObs R U
    apply
      (higherWeakCoherentAlignment_iff_no_twoAxisObstruction
        (W := W) U).mpr
    intro hLocalObs
    rcases hLocalObs with hExistenceObs | hRouteObs
    · exact hNoGlobalObs (Or.inl ⟨R, U, hExistenceObs⟩)
    · exact hNoGlobalObs (Or.inr ⟨R, U, hRouteObs⟩)

/-- Main global v2.42 normal form.  Relative to coherent existence, simultaneous
weak universality and fixed-route completeness are exactly absence of the two
remaining global obstruction classes. -/
theorem weakUniversal_and_routePrinciples_iff_no_globalTwoAxisObstruction_of_coherent
    (hCoherent : CoherentHigherWeakLocalizationUniversalPrinciple
      (W := W) (uH := uH) (vH := vH)) :
    (HigherWeakLocalizationUniversalPrinciple
        (W := W) (uH := uH) (vH := vH) ∧
      HigherCoherentRouteCompletenessPrinciple
        (W := W) (uH := uH) (vH := vH)) ↔
      ¬ HigherGlobalWeakCoherentTwoAxisObstruction
        (W := W) (uH := uH) (vH := vH) :=
  (higherWeakCoherentAlignmentPrinciple_iff_universal_and_route_of_coherent
    (W := W) hCoherent).symm.trans
    (higherWeakCoherentAlignmentPrinciple_iff_no_globalTwoAxisObstruction
      (W := W) (uH := uH) (vH := vH))

/-- Corresponding exact global failure normal form. -/
theorem not_weakUniversal_and_routePrinciples_iff_globalTwoAxisObstruction_of_coherent
    (hCoherent : CoherentHigherWeakLocalizationUniversalPrinciple
      (W := W) (uH := uH) (vH := vH)) :
    (¬ (HigherWeakLocalizationUniversalPrinciple
          (W := W) (uH := uH) (vH := vH) ∧
        HigherCoherentRouteCompletenessPrinciple
          (W := W) (uH := uH) (vH := vH))) ↔
      HigherGlobalWeakCoherentTwoAxisObstruction
        (W := W) (uH := uH) (vH := vH) := by
  classical
  constructor
  · intro hFail
    by_contra hNoGlobalObs
    exact hFail
      ((weakUniversal_and_routePrinciples_iff_no_globalTwoAxisObstruction_of_coherent
        (W := W) hCoherent).mpr hNoGlobalObs)
  · intro hGlobalObs hSuccess
    exact
      ((weakUniversal_and_routePrinciples_iff_no_globalTwoAxisObstruction_of_coherent
        (W := W) hCoherent).mp hSuccess) hGlobalObs

/-- The concrete global two-axis obstruction is equivalently the disjunction of
failure of the two abstract global principles. -/
theorem globalTwoAxisObstruction_iff_notUniversal_or_notRoute_of_coherent
    (hCoherent : CoherentHigherWeakLocalizationUniversalPrinciple
      (W := W) (uH := uH) (vH := vH)) :
    HigherGlobalWeakCoherentTwoAxisObstruction
        (W := W) (uH := uH) (vH := vH) ↔
      ((¬ HigherWeakLocalizationUniversalPrinciple
          (W := W) (uH := uH) (vH := vH)) ∨
        (¬ HigherCoherentRouteCompletenessPrinciple
          (W := W) (uH := uH) (vH := vH))) := by
  constructor
  · intro hGlobalObs
    rcases hGlobalObs with hExistenceObs | hRouteObs
    · exact Or.inl
        ((not_higherWeakLocalizationUniversalPrinciple_iff_globalWeakStageIIIExistenceObstruction_of_coherent
          (W := W) hCoherent).mpr hExistenceObs)
    · exact Or.inr
        ((not_higherCoherentRouteCompletenessPrinciple_iff_globalFixedRouteObstruction
          (W := W) (uH := uH) (vH := vH)).mpr hRouteObs)
  · rintro (hNoUniversal | hNoRoute)
    · exact Or.inl
        ((not_higherWeakLocalizationUniversalPrinciple_iff_globalWeakStageIIIExistenceObstruction_of_coherent
          (W := W) hCoherent).mp hNoUniversal)
    · exact Or.inr
        ((not_higherCoherentRouteCompletenessPrinciple_iff_globalFixedRouteObstruction
          (W := W) (uH := uH) (vH := vH)).mp hNoRoute)

/-!
## Boundary after v2.42

For one coherent datum `U`, there are now exactly three states:

```text
E: Stage III existence obstruction
   -> no weak universal property
   -> route completeness holds vacuously

R: forward modification-triangle obstruction
   -> a weak universal property exists
   -> route completeness fails

A: no E and no R
   -> weak universal property exists
   -> route completeness holds.
```

The `E` and `R` states are mutually exclusive for one raw system/coherent datum.
They may both occur globally on different raw systems.

Relative to a coherent universal principle, the remaining global problem is
therefore exactly the elimination of two concrete obstruction classes:

```text
HigherGlobalWeakStageIIIExistenceObstruction
HigherGlobalFixedRouteObstruction.
```

The first is the genuinely existential Stage III problem.  The second is the
fixed-carrier two-cell route problem normalized in v2.41.  Neither is silently
assumed away here.
-/

end KUOS.DependentOriginationWeakCoherentTwoAxisObstructionV2_42
