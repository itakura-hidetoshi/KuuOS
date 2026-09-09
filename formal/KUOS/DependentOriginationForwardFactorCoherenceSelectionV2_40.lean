import KUOS.DependentOriginationCompletedCarrierTwoSidedUpgradeV2_39
import KUOS.DependentOriginationModificationTriangleNormalFormV2_22

namespace KUOS.DependentOriginationForwardFactorCoherenceSelectionV2_40

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationCoherentFactorForgetfulBridgeV2_20
open KUOS.DependentOriginationFactorCoherenceLiftingV2_21
open KUOS.DependentOriginationModificationTriangleNormalFormV2_22
open KUOS.DependentOriginationWeakHigherLocalizationGapDecompositionV2_31
open KUOS.DependentOriginationRouteCompletenessInternalGapV2_34
open KUOS.DependentOriginationFixedChosenSplitCarrierTransferV2_37
open KUOS.DependentOriginationCompletedCarrierTwoSidedUpgradeV2_39

open scoped CategoryTheory.Pseudofunctor.StrongTrans

universe u v uH vH

/-!
# Forward-factor coherence selection v2.40

The v2.39 layer showed that, for a Stage III-completed weak carrier `C`, the
completed-carrier composite is automatic:

```text
C.chosen --q--> U.chosen --p--> C.chosen
q.hom ≫ p.hom ≅ 𝟙 C.chosen.lift.
```

The only remaining comparison obstruction is the fixed-side composite

```text
U.chosen --p--> C.chosen --q--> U.chosen
p.hom ≫ q.hom ≅ 𝟙 U.chosen.lift.
```

This file gives a local 2-categorical sufficient mechanism for producing that
fixed-side split.  It does **not** require the global v2.21 factor-coherence
lifting principle.  For one candidate `C`, it asks only for one coherent forward
factor

```text
p : U.chosen -> C.chosen.
```

A coherent backward factor `q : C.chosen -> U.chosen` already exists from the
coherent universal property `U.factor`.  Their coherent composite is therefore a
coherent endomorphism of `U.chosen`; coherent essential uniqueness in `U`
identifies its underlying StrongTrans with the coherent identity factor.  This
yields exactly

```text
p.hom ≫ q.hom ≅ 𝟙 U.chosen.lift.
```

By v2.22, existence of such a coherent forward factor is equivalent to existence
of an already-given v2.18 forward factor whose fixed StrongTrans admits the
single invertible modification triangle.  Thus the new sufficient condition is a
pure 2-cell coherence condition on one selected forward factor, not a new
1-cell, a carrier equality, a strictification, or an ordinary-localization
substitute.

The converse is deliberately not asserted: a noncoherent split comparison may
exist even when no selected forward factor is presently known to admit a
modification triangle.  Accordingly, the final obstruction theorem below is a
necessary obstruction for route failure, not an exact equivalence.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Coherent identity factor on a higher-localization factorization. -/
def coherentHigherLocalizationFactorMorphismId
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (H : HigherLocalizationFactorization (W := W) R) :
    CoherentHigherLocalizationFactorMorphism (W := W) H H where
  hom := 𝟙 H.lift
  comparison_triangle := by
    change (𝟙 _ ≫ H.comparison) ≅ H.comparison
    exact Bicategory.leftUnitor H.comparison

@[simp] theorem coherentHigherLocalizationFactorMorphismId_hom
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (H : HigherLocalizationFactorization (W := W) R) :
    (coherentHigherLocalizationFactorMorphismId (W := W) H).hom = 𝟙 H.lift := by
  rfl

/-- Vertical composition of coherent factor morphisms.

The comparison triangle is obtained by reassociating, whiskering the second
coherent triangle by the restricted first factor, and then composing with the
first coherent triangle. -/
def coherentHigherLocalizationFactorMorphismComp
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K L : HigherLocalizationFactorization (W := W) R}
    (alpha : CoherentHigherLocalizationFactorMorphism (W := W) H K)
    (beta : CoherentHigherLocalizationFactorMorphism (W := W) K L) :
    CoherentHigherLocalizationFactorMorphism (W := W) H L where
  hom := alpha.hom ≫ beta.hom
  comparison_triangle := by
    change
      ((restrictHigherLocalizedStrongTrans (W := W) alpha.hom ≫
          restrictHigherLocalizedStrongTrans (W := W) beta.hom) ≫
        L.comparison) ≅ H.comparison
    exact
      Bicategory.associator
          (restrictHigherLocalizedStrongTrans (W := W) alpha.hom)
          (restrictHigherLocalizedStrongTrans (W := W) beta.hom)
          L.comparison ≪≫
        Bicategory.whiskerLeftIso
          (restrictHigherLocalizedStrongTrans (W := W) alpha.hom)
          beta.comparison_triangle ≪≫
        alpha.comparison_triangle

@[simp] theorem coherentHigherLocalizationFactorMorphismComp_hom
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K L : HigherLocalizationFactorization (W := W) R}
    (alpha : CoherentHigherLocalizationFactorMorphism (W := W) H K)
    (beta : CoherentHigherLocalizationFactorMorphism (W := W) K L) :
    (coherentHigherLocalizationFactorMorphismComp (W := W) alpha beta).hom =
      alpha.hom ≫ beta.hom := by
  rfl

/-- Local forward-coherence condition for one Stage II carrier.

Only existence of one coherent factor from the fixed carrier to `C.chosen` is
required.  The backward coherent factor is supplied automatically by `U.factor`.
-/
def HasHigherFixedChosenCoherentForwardFactor
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (C : WeakHigherLocalizationUniversalCandidate (W := W) R) : Prop :=
  Nonempty
    (CoherentHigherLocalizationFactorMorphism (W := W) U.chosen C.chosen)

/-- v2.22 normal form for the local forward-coherence condition: a coherent
forward factor exists exactly when some existing v2.18 forward factor carries an
invertible modification triangle on its already-fixed StrongTrans. -/
theorem hasCoherentForwardFactor_iff_exists_forwardModificationTriangle
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (C : WeakHigherLocalizationUniversalCandidate (W := W) R) :
    HasHigherFixedChosenCoherentForwardFactor (W := W) U C ↔
      ∃ alpha : HigherLocalizationFactorMorphism (W := W) U.chosen C.chosen,
        HasFactorModificationTriangle (W := W) alpha := by
  constructor
  · rintro ⟨coherent⟩
    let alpha : HigherLocalizationFactorMorphism (W := W) U.chosen C.chosen :=
      coherentHigherLocalizationFactorMorphismToV2_18 (W := W) coherent
    have hLift : Nonempty (CoherentLiftOfV2_18Factor (W := W) alpha) := by
      exact ⟨{
        coherent := coherent
        hom_eq := rfl
      }⟩
    exact
      ⟨alpha,
        (coherentLiftOfV2_18Factor_iff_hasFactorModificationTriangle
          (W := W) alpha).mp hLift⟩
  · rintro ⟨alpha, hTriangle⟩
    rcases
        (coherentLiftOfV2_18Factor_iff_hasFactorModificationTriangle
          (W := W) alpha).mpr hTriangle with ⟨lift⟩
    exact ⟨lift.coherent⟩

/-- One coherent forward factor is sufficient to construct the exact v2.37
fixed-side split comparison.

The backward coherent factor comes from `U.factor C.chosen`.  Coherent
composition gives a coherent endomorphism of `U.chosen`; `U.essential_unique`
compares it with the coherent identity factor and produces the required
StrongTrans isomorphism. -/
theorem hasSplitCarrierComparison_of_coherentForwardFactor
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (C : WeakHigherLocalizationUniversalCandidate (W := W) R)
    (hForward : HasHigherFixedChosenCoherentForwardFactor (W := W) U C) :
    Nonempty (HigherFixedChosenSplitCarrierComparison (W := W) U C) := by
  rcases hForward with ⟨forwardCoherent⟩
  rcases U.factor C.chosen with ⟨backwardCoherent⟩
  let composite : CoherentHigherLocalizationFactorMorphism (W := W) U.chosen U.chosen :=
    coherentHigherLocalizationFactorMorphismComp
      (W := W) forwardCoherent backwardCoherent
  let identity : CoherentHigherLocalizationFactorMorphism (W := W) U.chosen U.chosen :=
    coherentHigherLocalizationFactorMorphismId (W := W) U.chosen
  rcases U.essential_unique U.chosen composite identity with ⟨e⟩
  change
    (forwardCoherent.hom ≫ backwardCoherent.hom) ≅
      𝟙 U.chosen.lift at e
  refine ⟨{
    forward := coherentHigherLocalizationFactorMorphismToV2_18
      (W := W) forwardCoherent
    backward := coherentHigherLocalizationFactorMorphismToV2_18
      (W := W) backwardCoherent
    fixed_retract := ?_
  }⟩
  exact ⟨e⟩

/-- If `C` is Stage III-completed, the coherent-forward mechanism upgrades via
v2.39 to an actual Mathlib bicategorical adjoint equivalence of the localized
lifts. -/
theorem hasAdjointEquivalence_of_coherentForwardFactor
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (C : WeakHigherLocalizationUniversalCandidate (W := W) R)
    (hUnique : C.HasEssentialUniqueness (W := W))
    (hForward : HasHigherFixedChosenCoherentForwardFactor (W := W) U C) :
    Nonempty (Bicategory.Equivalence U.chosen.lift C.chosen.lift) := by
  rcases hasSplitCarrierComparison_of_coherentForwardFactor
      (W := W) U C hForward with ⟨split⟩
  exact
    hasAdjointEquivalence_of_splitCompletedCarrier
      (W := W) U C hUnique split

/-- Completion condition: every Stage III-completed weak carrier admits at least
one coherent forward factor from the fixed coherent carrier. -/
def HigherFixedChosenCoherentForwardFactorCompletion
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∀ C : WeakHigherLocalizationUniversalCandidate (W := W) R,
    C.HasEssentialUniqueness (W := W) →
      HasHigherFixedChosenCoherentForwardFactor (W := W) U C

/-- Pure modification-triangle normal form of the preceding completion
condition. -/
def HigherFixedChosenForwardModificationTriangleCompletion
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∀ C : WeakHigherLocalizationUniversalCandidate (W := W) R,
    C.HasEssentialUniqueness (W := W) →
      ∃ alpha : HigherLocalizationFactorMorphism (W := W) U.chosen C.chosen,
        HasFactorModificationTriangle (W := W) alpha

/-- The coherent-forward completion condition is exactly its v2.22 pure
modification-triangle normal form. -/
theorem coherentForwardFactorCompletion_iff_forwardModificationTriangleCompletion
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherFixedChosenCoherentForwardFactorCompletion (W := W) U ↔
      HigherFixedChosenForwardModificationTriangleCompletion (W := W) U := by
  constructor
  · intro h C hUnique
    exact
      (hasCoherentForwardFactor_iff_exists_forwardModificationTriangle
        (W := W) U C).mp (h C hUnique)
  · intro h C hUnique
    exact
      (hasCoherentForwardFactor_iff_exists_forwardModificationTriangle
        (W := W) U C).mpr (h C hUnique)

/-- Coherent-forward completion implies the v2.37 split-comparison completion. -/
theorem splitCarrierComparisonCompletion_of_coherentForwardFactorCompletion
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hForward : HigherFixedChosenCoherentForwardFactorCompletion (W := W) U) :
    HigherFixedChosenSplitCarrierComparisonCompletion (W := W) U := by
  intro C hUnique
  exact
    hasSplitCarrierComparison_of_coherentForwardFactor
      (W := W) U C (hForward C hUnique)

/-- Hence local coherent-forward selection on every completed carrier is
sufficient for coherent route completeness. -/
theorem routeCompleteness_of_coherentForwardFactorCompletion
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hForward : HigherFixedChosenCoherentForwardFactorCompletion (W := W) U) :
    HigherCoherentRouteCompleteness (W := W) U :=
  routeCompleteness_of_splitCarrierComparisonCompletion
    (W := W) U
    (splitCarrierComparisonCompletion_of_coherentForwardFactorCompletion
      (W := W) U hForward)

/-- Pure modification-triangle selection is therefore also sufficient for route
completeness. -/
theorem routeCompleteness_of_forwardModificationTriangleCompletion
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hTriangle : HigherFixedChosenForwardModificationTriangleCompletion (W := W) U) :
    HigherCoherentRouteCompleteness (W := W) U :=
  routeCompleteness_of_coherentForwardFactorCompletion
    (W := W) U
    ((coherentForwardFactorCompletion_iff_forwardModificationTriangleCompletion
      (W := W) U).mpr hTriangle)

/-- Explicit failure of the local forward modification-triangle selection
criterion: some Stage III-completed carrier admits no forward v2.18 factor whose
already-fixed StrongTrans carries the required invertible modification triangle.
-/
def HigherFixedChosenForwardModificationTriangleObstruction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∃ C : WeakHigherLocalizationUniversalCandidate (W := W) R,
    C.HasEssentialUniqueness (W := W) ∧
      ∀ alpha : HigherLocalizationFactorMorphism (W := W) U.chosen C.chosen,
        ¬ HasFactorModificationTriangle (W := W) alpha

/-- The forward modification-triangle completion condition is exactly absence of
the explicit local selection obstruction. -/
theorem forwardModificationTriangleCompletion_iff_no_obstruction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherFixedChosenForwardModificationTriangleCompletion (W := W) U ↔
      ¬ HigherFixedChosenForwardModificationTriangleObstruction (W := W) U := by
  classical
  constructor
  · intro hComplete hObs
    rcases hObs with ⟨C, hUnique, hAllFail⟩
    rcases hComplete C hUnique with ⟨alpha, hTriangle⟩
    exact hAllFail alpha hTriangle
  · intro hNoObs C hUnique
    by_contra hNoTriangle
    apply hNoObs
    refine ⟨C, hUnique, ?_⟩
    intro alpha hTriangle
    exact hNoTriangle ⟨alpha, hTriangle⟩

/-- Therefore failure of coherent route completeness forces an explicit local
2-cell obstruction on at least one completed carrier.

Only this direction is asserted.  The reverse implication is not generally
available from the current spine, because a split comparison might conceivably
exist through factor maps not carrying the selected coherent-forward triangle. -/
theorem forwardModificationTriangleObstruction_of_not_routeCompleteness
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hFail : ¬ HigherCoherentRouteCompleteness (W := W) U) :
    HigherFixedChosenForwardModificationTriangleObstruction (W := W) U := by
  classical
  by_contra hNoObs
  apply hFail
  exact
    routeCompleteness_of_forwardModificationTriangleCompletion
      (W := W) U
      ((forwardModificationTriangleCompletion_iff_no_obstruction
        (W := W) U).mpr hNoObs)

/-!
## Boundary after v2.40

The fixed-side route now has a strictly local sufficient mechanism:

```text
one coherent forward factor p : U.chosen -> C.chosen
        +
coherent backward factor q : C.chosen -> U.chosen   (automatic from U.factor)
        |
        | coherent composition + U.essential_unique
        v
p.hom ≫ q.hom ≅ 𝟙 U.chosen.lift
        |
        v
v2.37 split comparison
        |
        | if C has Stage III uniqueness, v2.39
        v
actual bicategorical adjoint equivalence
        |
        v
coherent route completeness.
```

And v2.22 identifies the forward-coherence premise with a pure 2-cell statement:

```text
exists coherent forward factor
        <->
exists weak forward factor with an invertible modification triangle.
```

Thus route failure necessarily exposes a completed carrier on which every
forward weak factor fails that modification-triangle test.  This is a necessary
obstruction only; proving the converse would require an additional theorem that
turns every fixed-side split into such a coherent-forward presentation, which is
not assumed here.
-/

end KUOS.DependentOriginationForwardFactorCoherenceSelectionV2_40
