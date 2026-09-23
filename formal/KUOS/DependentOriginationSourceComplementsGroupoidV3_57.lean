import KUOS.DependentOriginationInversePairRepresentativeEquivalenceV3_56

namespace KUOS.DependentOriginationSourceComplementsGroupoidV3_57

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationAssociatorUnitorTriangleResidualV3_26
open KUOS.DependentOriginationAssociatorUnitorOneSidedSeparationV3_28
open KUOS.DependentOriginationWCompositeSplitSeparationV3_34
open KUOS.DependentOriginationFiniteAssociatorScheduleV3_38
open KUOS.DependentOriginationGlobalCancellationFromSourceComplementsV3_52
open KUOS.DependentOriginationInversePairRepresentativeEquivalenceV3_56

universe u v uH vH

set_option autoImplicit false

noncomputable section

/-!
# Source complements force a groupoid localization v3.57

v3.52 uses global left/right source-complement hypotheses only as a source of
epi/mono cancellation.  The pinned Mathlib API shows that the pair is actually
stronger.

For every source arrow `f`,

* a left W-composite complement gives `IsSplitEpi (W.Q.map f)`;
* a right W-composite complement gives `IsSplitMono (W.Q.map f)`.

A split epi is epi, and a split mono which is epi is an isomorphism.  Hence
every source generator of the localization is invertible under the two global
complement hypotheses.

Mathlib's exact localization induction principle
`Localization.Construction.morphismProperty_eq_top` then propagates the
`isomorphisms` morphism property from

* every source image `W.Q.map f`;
* every formal inverse `wInv w hw`;
* composition;

to every arrow of `W.Localization`.

Thus the v3.52 hypotheses do not merely provide cancellation: together they
force the ordinary localization category into its groupoid sector.

Combining with v3.56 gives a semantic consequence in the Cat-valued target:
every chosen quotient representative map is an equivalence of categories.
Consequently the v3.28 double-whiskering separation condition holds for every
pair of localization arrows.

This still does not eliminate the v3.55 inverse-pair leading gauge
obstruction.  Groupoidality of source 1-arrows and equivalence of target
representative functors remain one-categorical statements; nontrivial
automorphism-valued compositor/coherence data can survive them.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- The two source-complement directions make every source generator of the
localization an isomorphism. -/
theorem Q_map_isIso_of_sourceComplements
    (hLeft : HasLeftWCompositeComplements W)
    (hRight : HasRightWCompositeComplements W)
    {X Y : Context} (f : X ⟶ Y) :
    IsIso (W.Q.map f) := by
  rcases hLeft f with ⟨A, s, hs⟩
  rcases hRight f with ⟨B, r, hr⟩
  letI : IsSplitEpi (W.Q.map f) :=
    isSplitEpi_Q_map_of_W_comp W f s hs
  letI : IsSplitMono (W.Q.map f) :=
    isSplitMono_Q_map_of_W_comp W f r hr
  exact isIso_of_epi_of_isSplitMono (W.Q.map f)

/-- Under both global source-complement hypotheses, the isomorphism property
is top on the ordinary localization category. -/
theorem localization_isomorphisms_eq_top_of_sourceComplements
    (hLeft : HasLeftWCompositeComplements W)
    (hRight : HasRightWCompositeComplements W) :
    MorphismProperty.isomorphisms W.Localization = ⊤ := by
  apply Localization.Construction.morphismProperty_eq_top
  · intro X Y f
    rw [MorphismProperty.isomorphisms.iff]
    exact Q_map_isIso_of_sourceComplements W hLeft hRight f
  · intro X Y w hw
    rw [MorphismProperty.isomorphisms.iff]
    infer_instance

/-- Equivalent pointwise form: every localization arrow is an isomorphism. -/
theorem allLocalizationArrows_isIso_of_sourceComplements
    (hLeft : HasLeftWCompositeComplements W)
    (hRight : HasRightWCompositeComplements W) :
    ∀ {X Y : W.Localization} (f : X ⟶ Y), IsIso f := by
  have hTop :=
    localization_isomorphisms_eq_top_of_sourceComplements
      W hLeft hRight
  intro X Y f
  have hf : MorphismProperty.isomorphisms W.Localization f :=
    MorphismProperty.of_eq_top hTop f
  exact (MorphismProperty.isomorphisms.iff f).mp hf

variable (R : RawHigherContextualSystem.{u, v, uH, vH}
  (Context := Context))
variable (D : PointwiseWAdjointEquivalenceData (W := W) R)

/-- Once the source localization is forced into its groupoid sector, every
chosen quotient representative evaluation is an equivalence of categories. -/
theorem allQuotientRepresentativeMaps_isEquivalence_of_sourceComplements
    (hLeft : HasLeftWCompositeComplements W)
    (hRight : HasRightWCompositeComplements W) :
    ∀ {X Y : W.Localization} (f : X ⟶ Y),
      (quotientRepresentativeMap W R D f).toFunctor.IsEquivalence := by
  intro X Y f
  have hIso : IsIso f :=
    allLocalizationArrows_isIso_of_sourceComplements W hLeft hRight f
  letI : IsIso f := hIso
  exact quotientRepresentativeMap_isEquivalence_of_isIso W R D f

/-- Therefore every pair of localization arrows satisfies the exact v3.26/v3.28
double-whiskering separation predicate. -/
theorem all_middleIdentityWhiskerSeparating_of_sourceComplements
    (hLeft : HasLeftWCompositeComplements W)
    (hRight : HasRightWCompositeComplements W) :
    ∀ {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z),
      MiddleIdentityWhiskerSeparating W R D f g := by
  intro X Y Z f g
  exact
    middleIdentityWhiskerSeparating_of_isEquivalence_via_oneSided
      W R D f g
      (allQuotientRepresentativeMaps_isEquivalence_of_sourceComplements
        W R D hLeft hRight f)
      (allQuotientRepresentativeMaps_isEquivalence_of_sourceComplements
        W R D hLeft hRight g)

/-!
## Boundary after v3.57

The two v3.52 global source-complement hypotheses together imply

```text
MorphismProperty.isomorphisms W.Localization = ⊤.
```

Hence every localization arrow is invertible, every chosen quotient
representative evaluation is a category equivalence, and the v3.28
double-whiskering separation condition is globally automatic.

This significantly clarifies the remaining obstruction.  The final
fresh-boundary issue is not caused by

* missing epi/mono cancellation;
* missing splitness;
* noninvertible source localization arrows;
* non-equivalence of representative functors;
* failure of middle-identity whiskering separation.

What remains is genuinely the v3.55 two-dimensional leading gauge
compatibility equation on inverse-pair fresh-boundary tasks.

The next truth test should therefore target that equation itself, preferably
through an exact finite automorphism-valued cocycle model or a theorem showing
that the existing generated coherence algebra forces its vanishing in this
groupoid sector.  No such vanishing is asserted here.

No weak-admissibility derivation of source complements, schedule/seed/W/R/D
independence, comparison-gauge equations, Stage I, Stage II, or final
universality is claimed.  Protected validation-only PR #1558 remains
untouched.
-/

end

end KUOS.DependentOriginationSourceComplementsGroupoidV3_57
