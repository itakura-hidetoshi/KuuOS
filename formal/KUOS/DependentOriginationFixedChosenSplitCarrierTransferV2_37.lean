import KUOS.DependentOriginationFixedChosenEssentialUniquenessReflectionV2_36

namespace KUOS.DependentOriginationFixedChosenSplitCarrierTransferV2_37

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationWeakHigherLocalizationGapDecompositionV2_31
open KUOS.DependentOriginationRouteCompletenessInternalGapV2_34
open KUOS.DependentOriginationFixedChosenEssentialUniquenessReflectionV2_36

open scoped CategoryTheory.Pseudofunctor.StrongTrans

universe u v uH vH

/-!
# Fixed-chosen split-carrier transfer v2.37

The v2.36 layer reduced coherent route completeness to one fixed-carrier Stage III
selection problem: essential uniqueness may be known on some completed weak
candidate `C`, while the coherent route is tied to the fixed carrier `U.chosen`.

This file supplies a genuinely categorical sufficient condition for transporting
that uniqueness.

For weak factor morphisms

```text
H --alpha--> K --p--> L,
```

objectwise comparison triangles compose, so `alpha` can be postcomposed with
`p` as another v2.18 factor morphism.  Hence, if a completed carrier `C.chosen`
is related to the fixed carrier `U.chosen` by factor morphisms

```text
U.chosen --p--> C.chosen --q--> U.chosen
```

whose underlying StrongTrans composite satisfies

```text
p.hom ≫ q.hom ≅ 𝟙 U.chosen.lift,
```

then essential uniqueness on `C.chosen` transports to `U.chosen`: postcompose
two factors into `U.chosen` with `p`, use uniqueness on `C.chosen`, whisker the
result by `q`, and cancel the split composite by associators and unitors.

Only this one-sided retract equation is required.  No equality of carriers,
strictification, ordinary localization, coherent lifting of arbitrary weak
factors, or new axiom is introduced.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Identity v2.18 factor morphism on one higher-localization factorization.

Its objectwise comparison triangle is the ordinary left-unitor natural
isomorphism. -/
def higherLocalizationFactorMorphismId
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (H : HigherLocalizationFactorization (W := W) R) :
    HigherLocalizationFactorMorphism (W := W) H H where
  hom := 𝟙 H.lift
  comparison_triangle X := by
    change
      (𝟭 _ ⋙ (H.comparison.app (.mk X)).toFunctor) ≅
        (H.comparison.app (.mk X)).toFunctor
    exact Functor.leftUnitor _

/-- Vertical composition of v2.18 factor morphisms.

The underlying StrongTrans are composed in the pseudofunctor bicategory.  At a
raw context object, the comparison triangle is obtained by reassociating the
three functors, whiskering the second triangle by the first factor component,
and then composing with the first triangle. -/
def higherLocalizationFactorMorphismComp
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K L : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K)
    (beta : HigherLocalizationFactorMorphism (W := W) K L) :
    HigherLocalizationFactorMorphism (W := W) H L where
  hom := alpha.hom ≫ beta.hom
  comparison_triangle X := by
    change
      ((alpha.hom.app (.mk ((higherPresentationUnitFunctor W).obj X))).toFunctor ⋙
          (beta.hom.app (.mk ((higherPresentationUnitFunctor W).obj X))).toFunctor) ⋙
            (L.comparison.app (.mk X)).toFunctor ≅
        (H.comparison.app (.mk X)).toFunctor
    exact
      Functor.associator _ _ _ ≪≫
        isoWhiskerLeft
          (alpha.hom.app (.mk ((higherPresentationUnitFunctor W).obj X))).toFunctor
          (beta.comparison_triangle X) ≪≫
        alpha.comparison_triangle X

@[simp] theorem higherLocalizationFactorMorphismComp_hom
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K L : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K)
    (beta : HigherLocalizationFactorMorphism (W := W) K L) :
    (higherLocalizationFactorMorphismComp (W := W) alpha beta).hom =
      alpha.hom ≫ beta.hom := by
  rfl

/-- A one-sided split comparison from the fixed coherent carrier to another weak
Stage II carrier.

The two arrows are genuine v2.18 factor morphisms, so their objectwise comparison
triangles are retained.  The only cancellation datum required is an isomorphism
of underlying StrongTrans

```text
forward.hom ≫ backward.hom ≅ 𝟙 U.chosen.lift.
```

Thus `U.chosen` is a retract of `C.chosen` at the localized-lift 1-cell level.
No inverse equation on `C.chosen` is assumed. -/
structure HigherFixedChosenSplitCarrierComparison
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (C : WeakHigherLocalizationUniversalCandidate (W := W) R) where
  forward : HigherLocalizationFactorMorphism (W := W) U.chosen C.chosen
  backward : HigherLocalizationFactorMorphism (W := W) C.chosen U.chosen
  fixed_retract : Nonempty (forward.hom ≫ backward.hom ≅ 𝟙 U.chosen.lift)

/-- A split carrier comparison transports Stage III essential uniqueness from a
completed weak candidate to the fixed coherent carrier.

The proof is the explicit cancellation chain

```text
alpha
  ≅ alpha ≫ 𝟙
  ≅ alpha ≫ (p ≫ q)
  ≅ (alpha ≫ p) ≫ q
  ≅ (beta  ≫ p) ≫ q
  ≅ beta  ≫ (p ≫ q)
  ≅ beta  ≫ 𝟙
  ≅ beta.
```

The middle isomorphism is uniqueness on `C.chosen`, after composing the two
v2.18 factors with `p`. -/
theorem fixedChosenEssentialUniqueness_of_splitCarrierComparison
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (C : WeakHigherLocalizationUniversalCandidate (W := W) R)
    (hUnique : C.HasEssentialUniqueness (W := W))
    (S : HigherFixedChosenSplitCarrierComparison (W := W) U C) :
    HigherFixedChosenEssentialUniqueness (W := W) U := by
  intro H alpha beta
  rcases hUnique H
      (higherLocalizationFactorMorphismComp (W := W) alpha S.forward)
      (higherLocalizationFactorMorphismComp (W := W) beta S.forward) with ⟨eC⟩
  change
    (alpha.hom ≫ S.forward.hom) ≅
      (beta.hom ≫ S.forward.hom) at eC
  rcases S.fixed_retract with ⟨eSplit⟩
  refine ⟨?_⟩
  exact
    (Bicategory.rightUnitor alpha.hom).symm ≪≫
      Bicategory.whiskerLeftIso alpha.hom eSplit.symm ≪≫
        (Bicategory.associator alpha.hom S.forward.hom S.backward.hom).symm ≪≫
          Bicategory.whiskerRightIso eC S.backward.hom ≪≫
            Bicategory.associator beta.hom S.forward.hom S.backward.hom ≪≫
              Bicategory.whiskerLeftIso beta.hom eSplit ≪≫
                Bicategory.rightUnitor beta.hom

/-- The fixed Stage II candidate has a canonical split comparison with itself.
This witness is used only to show that the split-completed-carrier predicate below
is exact once fixed essential uniqueness is already known. -/
def fixedChosenSelfSplitCarrierComparison
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherFixedChosenSplitCarrierComparison
      (W := W) U (fixedChosenWeakUniversalCandidate (W := W) U) where
  forward := higherLocalizationFactorMorphismId (W := W) U.chosen
  backward := higherLocalizationFactorMorphismId (W := W) U.chosen
  fixed_retract := by
    refine ⟨?_⟩
    exact Bicategory.leftUnitor (𝟙 U.chosen.lift)

/-- There exists a completed weak Stage II carrier equipped with a split comparison
back to the fixed coherent carrier. -/
def HasHigherFixedChosenSplitCompletedCarrier
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∃ C : WeakHigherLocalizationUniversalCandidate (W := W) R,
    C.HasEssentialUniqueness (W := W) ∧
      Nonempty (HigherFixedChosenSplitCarrierComparison (W := W) U C)

/-- Existence of a split completed carrier is exactly fixed-carrier Stage III
uniqueness.

The forward implication is the cancellation theorem above.  For the reverse
implication, choose the fixed Stage II candidate itself and its canonical identity
split comparison. -/
theorem hasSplitCompletedCarrier_iff_fixedChosenEssentialUniqueness
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HasHigherFixedChosenSplitCompletedCarrier (W := W) U ↔
      HigherFixedChosenEssentialUniqueness (W := W) U := by
  constructor
  · rintro ⟨C, hUnique, ⟨S⟩⟩
    exact
      fixedChosenEssentialUniqueness_of_splitCarrierComparison
        (W := W) U C hUnique S
  · intro hFixed
    refine
      ⟨fixedChosenWeakUniversalCandidate (W := W) U, ?_,
        ⟨fixedChosenSelfSplitCarrierComparison (W := W) U⟩⟩
    exact hFixed

/-- Split-carrier selection principle for one coherent datum: whenever any weak
Stage II candidate is completed through Stage III, one can select a completed
candidate carrying a one-sided split comparison to `U.chosen`. -/
def HigherFixedChosenSplitCarrierSelection
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  HasWeakHigherLocalizationUniversalCandidateWithUniqueness (W := W) R →
    HasHigherFixedChosenSplitCompletedCarrier (W := W) U

/-- The v2.36 fixed Stage III completion property is exactly split-carrier
selection.  The new formulation exposes an explicit categorical transport witness
rather than leaving carrier transfer opaque. -/
theorem stageIIICompletion_iff_splitCarrierSelection
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherFixedChosenStageIIICompletion (W := W) U ↔
      HigherFixedChosenSplitCarrierSelection (W := W) U := by
  constructor
  · intro hComplete hWeakComplete
    exact
      (hasSplitCompletedCarrier_iff_fixedChosenEssentialUniqueness (W := W) U).mpr
        (hComplete hWeakComplete)
  · intro hSplit hWeakComplete
    exact
      (hasSplitCompletedCarrier_iff_fixedChosenEssentialUniqueness (W := W) U).mp
        (hSplit hWeakComplete)

/-- Consequently, fixed-chosen reflection is exactly split-carrier selection. -/
theorem fixedChosenReflection_iff_splitCarrierSelection
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherFixedChosenEssentialUniquenessReflection (W := W) U ↔
      HigherFixedChosenSplitCarrierSelection (W := W) U :=
  (fixedChosenReflection_iff_stageIIICompletion (W := W) U).trans
    (stageIIICompletion_iff_splitCarrierSelection (W := W) U)

/-- Coherent route completeness is exactly split-carrier selection. -/
theorem routeCompleteness_iff_splitCarrierSelection
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherCoherentRouteCompleteness (W := W) U ↔
      HigherFixedChosenSplitCarrierSelection (W := W) U :=
  (routeCompleteness_iff_stageIIICompletion (W := W) U).trans
    (stageIIICompletion_iff_splitCarrierSelection (W := W) U)

/-- Failure of split-carrier selection in the non-vacuous regime. -/
def HigherFixedChosenSplitCarrierSelectionFailure
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  HasWeakHigherLocalizationUniversalCandidateWithUniqueness (W := W) R ∧
    ¬ HasHigherFixedChosenSplitCompletedCarrier (W := W) U

/-- The v2.36 carrier-mismatch obstruction is exactly failure to select a split
completed carrier. -/
theorem carrierMismatchObstruction_iff_splitCarrierSelectionFailure
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherFixedChosenCarrierMismatchObstruction (W := W) U ↔
      HigherFixedChosenSplitCarrierSelectionFailure (W := W) U := by
  constructor
  · rintro ⟨C, hUnique, hNoFixed⟩
    refine ⟨⟨C, hUnique⟩, ?_⟩
    intro hSplit
    exact hNoFixed
      ((hasSplitCompletedCarrier_iff_fixedChosenEssentialUniqueness (W := W) U).mp hSplit)
  · rintro ⟨hComplete, hNoSplit⟩
    rcases hComplete with ⟨C, hUnique⟩
    refine ⟨C, hUnique, ?_⟩
    intro hFixed
    apply hNoSplit
    exact
      (hasSplitCompletedCarrier_iff_fixedChosenEssentialUniqueness (W := W) U).mpr hFixed

/-- The exact route-completeness failure normal form can therefore be stated as
split-carrier selection failure. -/
theorem not_routeCompleteness_iff_splitCarrierSelectionFailure
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    (¬ HigherCoherentRouteCompleteness (W := W) U) ↔
      HigherFixedChosenSplitCarrierSelectionFailure (W := W) U :=
  (not_routeCompleteness_iff_carrierMismatchObstruction (W := W) U).trans
    (carrierMismatchObstruction_iff_splitCarrierSelectionFailure (W := W) U)

/-- A direct sufficient condition: if every completed weak candidate admits a
split comparison to the fixed carrier, then carrier uniqueness transfer follows. -/
def HigherFixedChosenSplitCarrierComparisonCompletion
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∀ C : WeakHigherLocalizationUniversalCandidate (W := W) R,
    C.HasEssentialUniqueness (W := W) →
      Nonempty (HigherFixedChosenSplitCarrierComparison (W := W) U C)

/-- The explicit split-comparison completion condition is sufficient for the
v2.36 carrier-transfer property. -/
theorem carrierUniquenessTransfer_of_splitCarrierComparisonCompletion
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hSplit : HigherFixedChosenSplitCarrierComparisonCompletion (W := W) U) :
    HigherFixedChosenCarrierUniquenessTransfer (W := W) U := by
  intro C hUnique
  rcases hSplit C hUnique with ⟨S⟩
  exact
    fixedChosenEssentialUniqueness_of_splitCarrierComparison
      (W := W) U C hUnique S

/-- Hence the explicit split-comparison completion condition is sufficient for
coherent route completeness. -/
theorem routeCompleteness_of_splitCarrierComparisonCompletion
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hSplit : HigherFixedChosenSplitCarrierComparisonCompletion (W := W) U) :
    HigherCoherentRouteCompleteness (W := W) U :=
  (routeCompleteness_iff_carrierUniquenessTransfer (W := W) U).mpr
    (carrierUniquenessTransfer_of_splitCarrierComparisonCompletion
      (W := W) U hSplit)

/-- Global split-carrier comparison completion principle.  This remains an
explicit proposition, not a theorem asserted for arbitrary coherent universal
data. -/
def HigherFixedChosenSplitCarrierComparisonCompletionPrinciple : Prop :=
  ∀ (R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH))
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R),
    HigherFixedChosenSplitCarrierComparisonCompletion (W := W) U

/-- The global split-comparison principle implies the global fixed-chosen
reflection principle. -/
theorem fixedChosenReflectionPrinciple_of_splitCarrierComparisonCompletionPrinciple
    (hSplit : HigherFixedChosenSplitCarrierComparisonCompletionPrinciple
      (W := W) (uH := uH) (vH := vH)) :
    HigherFixedChosenEssentialUniquenessReflectionPrinciple
      (W := W) (uH := uH) (vH := vH) := by
  intro R U
  exact
    (fixedChosenReflection_iff_carrierUniquenessTransfer (W := W) U).mpr
      (carrierUniquenessTransfer_of_splitCarrierComparisonCompletion
        (W := W) U (hSplit R U))

/-!
## Boundary after v2.37

The remaining carrier ambiguity now has an explicit sufficient transport
mechanism:

```text
completed weak carrier C.chosen
        |
        | p : U.chosen -> C.chosen
        | q : C.chosen -> U.chosen
        | p.hom >> q.hom ≅ id
        v
fixed U.chosen inherits Stage III uniqueness
        |
        v
coherent route completeness.
```

Thus mutual Stage II factor existence alone is still not enough: the additional
content is the one-sided StrongTrans retract needed for cancellation.  Conversely,
once fixed Stage III uniqueness is known, the fixed candidate itself gives the
canonical identity split witness, so split-carrier *selection* is an exact normal
form for v2.36 Stage III completion.

What remains open is to derive such split comparisons from weaker intrinsic data
on arbitrary completed carriers (for example an actual equivalence, adjoint
equivalence, conservativity/fully-faithfulness condition, or another justified
bicategorical universal property).  No such derivation is assumed here.
-/

end KUOS.DependentOriginationFixedChosenSplitCarrierTransferV2_37