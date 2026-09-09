import KUOS.DependentOriginationForwardFactorCoherenceSelectionV2_40
import KUOS.DependentOriginationStrongTransIsoTriangleTransportV2_35

namespace KUOS.DependentOriginationSplitToCoherentForwardExactV2_41

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationCoherentFactorForgetfulBridgeV2_20
open KUOS.DependentOriginationModificationTriangleNormalFormV2_22
open KUOS.DependentOriginationStrongTransIsoTriangleTransportV2_35
open KUOS.DependentOriginationWeakHigherLocalizationGapDecompositionV2_31
open KUOS.DependentOriginationRouteCompletenessInternalGapV2_34
open KUOS.DependentOriginationFixedChosenEssentialUniquenessReflectionV2_36
open KUOS.DependentOriginationFixedChosenSplitCarrierTransferV2_37
open KUOS.DependentOriginationCompletedCarrierTwoSidedUpgradeV2_39
open KUOS.DependentOriginationForwardFactorCoherenceSelectionV2_40

open scoped CategoryTheory.Pseudofunctor.StrongTrans

universe u v uH vH

/-!
# Split-to-coherent-forward exactness v2.41

The v2.40 layer proved a one-way local mechanism:

```text
coherent forward factor U.chosen -> C.chosen
        |
        v
fixed-side split comparison
        |
        v
route completeness.
```

It deliberately left open whether a fixed-side split must itself admit a coherent
forward presentation.  This file closes that converse **after Stage III completion
of the target carrier `C`**.

Let

```text
p : U.chosen -> C.chosen,
q : C.chosen -> U.chosen
```

be a v2.37 split comparison, so `p.hom ≫ q.hom ≅ 𝟙 U.chosen.lift`.  Independently,
the coherent universal datum `U` supplies a coherent backward factor

```text
q₀ : C.chosen -> U.chosen.
```

If `C` has Stage III essential uniqueness, then `q₀ ≫ p` and the identity factor
on `C.chosen` have isomorphic underlying StrongTrans, hence

```text
q₀.hom ≫ p.hom ≅ 𝟙 C.chosen.lift.
```

Thus `q₀` is a left inverse of `p`, while the original `q` is a right inverse.
Bicategorical associators and unitors give the standard uniqueness-of-inverse
isomorphism `q₀.hom ≅ q.hom`.  Transporting the fixed split along that isomorphism
yields

```text
p.hom ≫ q₀.hom ≅ 𝟙 U.chosen.lift.
```

Now `q₀` already carries a coherent comparison triangle.  Whiskering its inverse
triangle by `restrict(p)`, reassociating, applying the restricted fixed split, and
then the left unitor constructs the missing coherent triangle for `p` itself.
Therefore on a completed carrier:

```text
v2.37 split comparison
        <->
coherent forward factor
        <->
some weak forward factor with a modification triangle.
```

This upgrades the v2.40 sufficient criterion to an exact completion criterion and
turns its forward-modification-triangle obstruction into an exact failure normal
form for coherent route completeness.

No split is asserted for arbitrary completed carriers.  No strictification,
ordinary-localization substitution, new axiom, `sorry`, or `admit` is introduced.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- On a completed carrier, any fixed-side split comparison admits a coherent
forward presentation with the same underlying forward StrongTrans.

The proof uses the coherent backward factor supplied by `U.factor`, Stage III
uniqueness on `C` to make it a left inverse of the split forward factor, and the
original split backward factor as a right inverse. -/
theorem hasCoherentForwardFactor_of_splitCompletedCarrier
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (C : WeakHigherLocalizationUniversalCandidate (W := W) R)
    (hUnique : C.HasEssentialUniqueness (W := W))
    (S : HigherFixedChosenSplitCarrierComparison (W := W) U C) :
    HasHigherFixedChosenCoherentForwardFactor (W := W) U C := by
  rcases U.factor C.chosen with ⟨backwardCoherent⟩
  let backwardWeak : HigherLocalizationFactorMorphism (W := W) C.chosen U.chosen :=
    coherentHigherLocalizationFactorMorphismToV2_18 (W := W) backwardCoherent
  rcases hUnique C.chosen
      (higherLocalizationFactorMorphismComp (W := W) backwardWeak S.forward)
      (higherLocalizationFactorMorphismId (W := W) C.chosen) with ⟨eCompleted⟩
  change
    (backwardCoherent.hom ≫ S.forward.hom) ≅
      𝟙 C.chosen.lift at eCompleted
  rcases S.fixed_retract with ⟨eFixed⟩
  have eBackward : backwardCoherent.hom ≅ S.backward.hom :=
    (Bicategory.rightUnitor backwardCoherent.hom).symm ≪≫
      Bicategory.whiskerLeftIso backwardCoherent.hom eFixed.symm ≪≫
        (Bicategory.associator
          backwardCoherent.hom S.forward.hom S.backward.hom).symm ≪≫
          Bicategory.whiskerRightIso eCompleted S.backward.hom ≪≫
            Bicategory.leftUnitor S.backward.hom
  have eFixedCoherent :
      S.forward.hom ≫ backwardCoherent.hom ≅ 𝟙 U.chosen.lift :=
    Bicategory.whiskerLeftIso S.forward.hom eBackward ≪≫ eFixed
  let eRestricted :=
    restrictHigherLocalizedStrongTransIso (W := W) eFixedCoherent
  change
    (restrictHigherLocalizedStrongTrans (W := W) S.forward.hom ≫
        restrictHigherLocalizedStrongTrans (W := W) backwardCoherent.hom) ≅
      𝟙 (restrictHigherLocalizedSystem W U.chosen.lift) at eRestricted
  let forwardCoherent :
      CoherentHigherLocalizationFactorMorphism (W := W) U.chosen C.chosen := {
    hom := S.forward.hom
    comparison_triangle :=
      Bicategory.whiskerLeftIso
          (restrictHigherLocalizedStrongTrans (W := W) S.forward.hom)
          backwardCoherent.comparison_triangle.symm ≪≫
        (Bicategory.associator
          (restrictHigherLocalizedStrongTrans (W := W) S.forward.hom)
          (restrictHigherLocalizedStrongTrans (W := W) backwardCoherent.hom)
          U.chosen.comparison).symm ≪≫
        Bicategory.whiskerRightIso eRestricted U.chosen.comparison ≪≫
        Bicategory.leftUnitor U.chosen.comparison
  }
  exact ⟨forwardCoherent⟩

/-- Exact local characterization on a Stage III-completed carrier: fixed-side
split comparison and coherent-forward existence are equivalent. -/
theorem nonempty_splitCarrierComparison_iff_coherentForwardFactor_of_completed
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (C : WeakHigherLocalizationUniversalCandidate (W := W) R)
    (hUnique : C.HasEssentialUniqueness (W := W)) :
    Nonempty (HigherFixedChosenSplitCarrierComparison (W := W) U C) ↔
      HasHigherFixedChosenCoherentForwardFactor (W := W) U C := by
  constructor
  · rintro ⟨S⟩
    exact
      hasCoherentForwardFactor_of_splitCompletedCarrier
        (W := W) U C hUnique S
  · intro hForward
    exact
      hasSplitCarrierComparison_of_coherentForwardFactor
        (W := W) U C hForward

/-- Hence the split-comparison completion condition of v2.37 and the local
coherent-forward completion condition of v2.40 are exactly equivalent. -/
theorem splitCarrierComparisonCompletion_iff_coherentForwardFactorCompletion
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherFixedChosenSplitCarrierComparisonCompletion (W := W) U ↔
      HigherFixedChosenCoherentForwardFactorCompletion (W := W) U := by
  constructor
  · intro hSplit C hUnique
    exact
      (nonempty_splitCarrierComparison_iff_coherentForwardFactor_of_completed
        (W := W) U C hUnique).mp (hSplit C hUnique)
  · intro hForward C hUnique
    exact
      (nonempty_splitCarrierComparison_iff_coherentForwardFactor_of_completed
        (W := W) U C hUnique).mpr (hForward C hUnique)

/-- Route completeness forces a split comparison with **every** Stage III-completed
weak carrier, not merely the existence of one selected split completed carrier.

This uses the v2.36 carrier-uniqueness transfer normal form: route completeness
first gives Stage III uniqueness on the fixed carrier.  Applying that uniqueness
to the composite of any automatic mutual factor pair from v2.39 and the identity
factor yields the fixed-side split. -/
theorem splitCarrierComparisonCompletion_of_routeCompleteness
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hRoute : HigherCoherentRouteCompleteness (W := W) U) :
    HigherFixedChosenSplitCarrierComparisonCompletion (W := W) U := by
  have hTransfer : HigherFixedChosenCarrierUniquenessTransfer (W := W) U :=
    (routeCompleteness_iff_carrierUniquenessTransfer (W := W) U).mp hRoute
  intro C hUnique
  have hFixed : HigherFixedChosenEssentialUniqueness (W := W) U :=
    hTransfer C hUnique
  rcases hasMutualFactorComparison (W := W) U C with ⟨M⟩
  rcases hFixed U.chosen
      (higherLocalizationFactorMorphismComp (W := W) M.forward M.backward)
      (higherLocalizationFactorMorphismId (W := W) U.chosen) with ⟨e⟩
  change
    (M.forward.hom ≫ M.backward.hom) ≅
      𝟙 U.chosen.lift at e
  exact ⟨{
    forward := M.forward
    backward := M.backward
    fixed_retract := ⟨e⟩
  }⟩

/-- The all-completed-carriers split condition is therefore not merely sufficient:
it is exactly coherent route completeness. -/
theorem routeCompleteness_iff_splitCarrierComparisonCompletion
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherCoherentRouteCompleteness (W := W) U ↔
      HigherFixedChosenSplitCarrierComparisonCompletion (W := W) U := by
  constructor
  · exact splitCarrierComparisonCompletion_of_routeCompleteness (W := W) U
  · exact routeCompleteness_of_splitCarrierComparisonCompletion (W := W) U

/-- Combining the preceding exactness with v2.41 split-to-coherent transport,
coherent route completeness is exactly local coherent-forward completion on every
Stage III-completed carrier. -/
theorem routeCompleteness_iff_coherentForwardFactorCompletion
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherCoherentRouteCompleteness (W := W) U ↔
      HigherFixedChosenCoherentForwardFactorCompletion (W := W) U :=
  (routeCompleteness_iff_splitCarrierComparisonCompletion (W := W) U).trans
    (splitCarrierComparisonCompletion_iff_coherentForwardFactorCompletion
      (W := W) U)

/-- By the v2.22 normal form used in v2.40, route completeness is also exactly the
existence, for every completed carrier, of some weak forward factor whose fixed
StrongTrans admits an invertible modification triangle. -/
theorem routeCompleteness_iff_forwardModificationTriangleCompletion
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherCoherentRouteCompleteness (W := W) U ↔
      HigherFixedChosenForwardModificationTriangleCompletion (W := W) U :=
  (routeCompleteness_iff_coherentForwardFactorCompletion (W := W) U).trans
    (coherentForwardFactorCompletion_iff_forwardModificationTriangleCompletion
      (W := W) U)

/-- The v2.40 local forward-modification-triangle obstruction is now an exact
failure normal form for coherent route completeness. -/
theorem not_routeCompleteness_iff_forwardModificationTriangleObstruction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    (¬ HigherCoherentRouteCompleteness (W := W) U) ↔
      HigherFixedChosenForwardModificationTriangleObstruction (W := W) U := by
  constructor
  · exact
      forwardModificationTriangleObstruction_of_not_routeCompleteness
        (W := W) U
  · intro hObs hRoute
    have hCompletion :
        HigherFixedChosenForwardModificationTriangleCompletion (W := W) U :=
      (routeCompleteness_iff_forwardModificationTriangleCompletion
        (W := W) U).mp hRoute
    exact
      ((forwardModificationTriangleCompletion_iff_no_obstruction
        (W := W) U).mp hCompletion) hObs

/-!
## Boundary after v2.41

For a Stage III-completed carrier, the fixed-side comparison gap now has the exact
local normal form

```text
split comparison
    <->
coherent forward factor
    <->
weak forward factor + invertible modification triangle.
```

Globally for one coherent datum `U`:

```text
coherent route completeness
    <->
all completed carriers admit a split comparison
    <->
all completed carriers admit a coherent forward factor
    <->
all completed carriers admit some forward modification triangle.
```

Therefore route failure is exactly the existence of a Stage III-completed carrier
for which every forward v2.18 factor fails the modification-triangle test.

This does not solve the global weak higher-localization existence principle or the
global coherent universal principle.  It closes the **internal fixed-carrier
reflection gap conditional on the coherent datum `U` and the existence of a
completed weak carrier** by reducing it to the explicit v2.22 two-cell condition.
-/

end KUOS.DependentOriginationSplitToCoherentForwardExactV2_41
