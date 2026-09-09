import KUOS.DependentOriginationWeakHigherLocalizationGapDecompositionV2_31

namespace KUOS.DependentOriginationCoherentStageIIIGapCollapseV2_32

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationCoherentFactorForgetfulBridgeV2_20
open KUOS.DependentOriginationFactorCoherenceLiftingV2_21
open KUOS.DependentOriginationModificationTriangleNormalFormV2_22
open KUOS.DependentOriginationStoredTriangleCorrectionV2_26
open KUOS.DependentOriginationWeakHigherLocalizationGapDecompositionV2_31

open scoped CategoryTheory.Pseudofunctor.StrongTrans

universe u v uH vH

/-!
# Coherent Stage-III gap collapse v2.32

The v2.31 layer decomposes the still-open v2.18 weak universal principle into
three stages:

1. higher-localization factorization existence;
2. existence of one factor-universal candidate;
3. essential uniqueness for such a candidate.

The earlier coherent v2.19 interface is already stronger than the first two
stages at the level of supplied data.  A coherent universal datum contains a
factorization, and v2.20 forgets every coherent factor map to a v2.18 factor
map.  Therefore, once one coherent v2.19 universal datum `U` for a raw system is
explicitly supplied, the v2.31 Stage I and Stage II obstructions cannot occur.
The entire v2.31 local gap then collapses exactly to Stage III.

This file proves that collapse and connects the surviving Stage III obstruction
to the previously isolated coherence route:

```text
Stage III essential-uniqueness obstruction
        |
        v
factor-coherence lifting obstruction          (v2.21)
        |
        v
modification-triangle obstruction              (v2.22)
        |
        v
stored-triangle correction obstruction         (v2.26).
```

Only the displayed downward implications are claimed.  Their converses are not
valid from the current interfaces: failure of a particular coherent lifting or
correction route does not by itself exclude some other v2.18 universal
candidate.  Likewise no arrowwise equation obstruction from v2.30 is inferred
without the additional rigidity/extension hypotheses used there.

Globally, under an explicitly assumed coherent v2.19 universal principle, the
v2.31 three-stage completion package is equivalent to Stage III completion
alone.  Consequently the v2.18 weak universal principle is equivalent to Stage
III completion relative to that coherent premise.

No coherent universal principle, correction-solvability principle, or weak
higher-localization theorem is asserted unconditionally.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Forget only enough coherent v2.19 structure to obtain the v2.31 Stage II
candidate on the same chosen factorization. -/
def weakUniversalCandidateOfCoherentUniversalProperty
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    WeakHigherLocalizationUniversalCandidate (W := W) R where
  chosen := U.chosen
  factor H := coherentWeakUniversalProperty_hasV2_18Factor W U H

/-- A supplied coherent universal datum therefore gives a v2.31 Stage II
candidate. -/
theorem hasWeakUniversalCandidate_of_coherentUniversalProperty
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HasWeakHigherLocalizationUniversalCandidate (W := W) R :=
  ⟨weakUniversalCandidateOfCoherentUniversalProperty (W := W) U⟩

/-- Stage I obstruction is impossible once a coherent universal datum is
supplied, because that datum already contains its chosen v2.10 factorization. -/
theorem not_factorizationExistenceObstruction_of_coherentUniversalProperty
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    ¬ HigherWeakLocalizationFactorizationExistenceObstruction (W := W) R := by
  intro hObs
  exact hObs.2 ⟨U.chosen⟩

/-- Stage II obstruction is likewise impossible: v2.20 forgets coherent factor
maps into `U.chosen` to v2.18 factor maps, producing a Stage II candidate. -/
theorem not_universalFactorExistenceObstruction_of_coherentUniversalProperty
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    ¬ HigherWeakUniversalFactorExistenceObstruction (W := W) R := by
  intro hObs
  exact hObs.2.2
    (hasWeakUniversalCandidate_of_coherentUniversalProperty (W := W) U)

/-- Main local collapse theorem: with one coherent v2.19 universal datum in
hand, the full v2.31 three-way gap obstruction is exactly the Stage III
essential-uniqueness obstruction. -/
theorem gapObstruction_iff_essentialUniquenessObstruction_of_coherentUniversalProperty
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherWeakLocalizationUniversalGapObstruction (W := W) R ↔
      HigherWeakEssentialUniquenessObstruction (W := W) R := by
  constructor
  · intro hGap
    rcases hGap with hStageI | hRest
    · exact False.elim
        ((not_factorizationExistenceObstruction_of_coherentUniversalProperty
          (W := W) U) hStageI)
    · rcases hRest with hStageII | hStageIII
      · exact False.elim
          ((not_universalFactorExistenceObstruction_of_coherentUniversalProperty
            (W := W) U) hStageII)
      · exact hStageIII
  · intro hStageIII
    exact Or.inr (Or.inr hStageIII)

/-- Equivalently, once coherent universal data exist locally, failure of the
v2.18 weak universal property is exactly Stage III failure.  Admissibility need
not be supplied separately: it follows from the coherent datum itself. -/
theorem not_hasWeakHigherLocalizationUniversalProperty_iff_essentialUniquenessObstruction_of_coherent
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    (¬ HasWeakHigherLocalizationUniversalProperty (W := W) R) ↔
      HigherWeakEssentialUniquenessObstruction (W := W) R := by
  have hR : IsHigherWAdmissible W R :=
    hasCoherentWeakHigherLocalizationUniversalProperty_isHigherWAdmissible W ⟨U⟩
  exact
    (not_hasWeakHigherLocalizationUniversalProperty_iff_gapObstruction
      (W := W) hR).trans
      (gapObstruction_iff_essentialUniquenessObstruction_of_coherentUniversalProperty
        (W := W) U)

/-- Stage III failure forces the v2.21 factor-coherence route to fail for every
explicit coherent universal datum `U` on the same raw system.  If lifting held,
v2.21 would construct a v2.18 universal property and hence a completed v2.31
candidate, contradicting Stage III obstruction. -/
theorem higherFactorCoherenceObstruction_of_essentialUniquenessObstruction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hStageIII : HigherWeakEssentialUniquenessObstruction (W := W) R) :
    HigherFactorCoherenceObstruction (W := W) U := by
  classical
  by_contra hNoObstruction
  have hLift : HigherFactorCoherenceLifting (W := W) U :=
    (higherFactorCoherenceLifting_iff_no_obstruction (W := W) U).mpr
      hNoObstruction
  have hUniversal : HasWeakHigherLocalizationUniversalProperty (W := W) R :=
    ⟨weakHigherLocalizationUniversalPropertyOfCoherent W U hLift⟩
  have hComplete :
      HasWeakHigherLocalizationUniversalCandidateWithUniqueness (W := W) R :=
    (hasWeakHigherLocalizationUniversalProperty_iff_candidateWithUniqueness
      (W := W) R).mp hUniversal
  exact hStageIII.2.2 hComplete

/-- The same Stage III failure therefore forces the exact v2.22 pure
modification-triangle obstruction. -/
theorem higherFactorModificationTriangleObstruction_of_essentialUniquenessObstruction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hStageIII : HigherWeakEssentialUniquenessObstruction (W := W) R) :
    HigherFactorModificationTriangleObstruction (W := W) U :=
  (higherFactorCoherenceObstruction_iff_modificationTriangleObstruction
    (W := W) U).mp
    (higherFactorCoherenceObstruction_of_essentialUniquenessObstruction
      (W := W) U hStageIII)

/-- In the v2.26 normal form, Stage III failure forces failure of the stored
triangle target-correction equation for at least one v2.18 factor into
`U.chosen`. -/
theorem higherStoredTriangleCorrectionObstruction_of_essentialUniquenessObstruction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hStageIII : HigherWeakEssentialUniquenessObstruction (W := W) R) :
    HigherStoredTriangleTargetCorrectionObstruction (W := W) U :=
  (higherStoredTriangleCorrectionObstruction_iff_modificationTriangleObstruction
    (W := W) U).mpr
    (higherFactorModificationTriangleObstruction_of_essentialUniquenessObstruction
      (W := W) U hStageIII)

/-- Because the local v2.31 gap has collapsed to Stage III, any surviving gap in
the presence of coherent universal data forces a v2.26 correction obstruction. -/
theorem higherStoredTriangleCorrectionObstruction_of_gapObstruction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hGap : HigherWeakLocalizationUniversalGapObstruction (W := W) R) :
    HigherStoredTriangleTargetCorrectionObstruction (W := W) U :=
  higherStoredTriangleCorrectionObstruction_of_essentialUniquenessObstruction
    (W := W) U
    ((gapObstruction_iff_essentialUniquenessObstruction_of_coherentUniversalProperty
      (W := W) U).mp hGap)

/-- Therefore local failure of the v2.18 universal property, under a supplied
coherent universal datum, forces a correction obstruction for that datum. -/
theorem higherStoredTriangleCorrectionObstruction_of_not_hasWeakUniversalProperty
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hNoUniversal : ¬ HasWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherStoredTriangleTargetCorrectionObstruction (W := W) U :=
  higherStoredTriangleCorrectionObstruction_of_essentialUniquenessObstruction
    (W := W) U
    ((not_hasWeakHigherLocalizationUniversalProperty_iff_essentialUniquenessObstruction_of_coherent
      (W := W) U).mp hNoUniversal)

/-- Absence of the v2.26 correction obstruction on one coherent universal datum
is sufficient to recover the v2.18 universal property through the exact
v2.26 -> v2.22 -> v2.21 transport chain. -/
theorem hasWeakHigherLocalizationUniversalProperty_of_no_storedTriangleCorrectionObstruction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hNoCorrection :
      ¬ HigherStoredTriangleTargetCorrectionObstruction (W := W) U) :
    HasWeakHigherLocalizationUniversalProperty (W := W) R := by
  have hCorrectionLifting :
      HigherStoredTriangleTargetCorrectionLifting (W := W) U :=
    (higherStoredTriangleCorrectionLifting_iff_no_obstruction
      (W := W) U).mpr hNoCorrection
  have hTriangleLifting : HigherFactorModificationTriangleLifting (W := W) U :=
    (higherStoredTriangleCorrectionLifting_iff_modificationTriangleLifting
      (W := W) U).mp hCorrectionLifting
  have hFactorLifting : HigherFactorCoherenceLifting (W := W) U :=
    (higherFactorCoherenceLifting_iff_modificationTriangleLifting
      (W := W) U).mpr hTriangleLifting
  exact ⟨weakHigherLocalizationUniversalPropertyOfCoherent W U hFactorLifting⟩

/-- Under coherent universal data, absence of the correction obstruction also
rules out the whole v2.31 gap obstruction. -/
theorem not_gapObstruction_of_no_storedTriangleCorrectionObstruction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hNoCorrection :
      ¬ HigherStoredTriangleTargetCorrectionObstruction (W := W) U) :
    ¬ HigherWeakLocalizationUniversalGapObstruction (W := W) R := by
  intro hGap
  exact hNoCorrection
    (higherStoredTriangleCorrectionObstruction_of_gapObstruction
      (W := W) U hGap)

/-- A global coherent v2.19 universal principle automatically supplies v2.31
Stage II completion: on every admissible raw system choose the coherent
universal datum and forget its coherent factor maps. -/
theorem higherWeakUniversalFactorExistenceCompletion_of_coherentUniversalPrinciple
    (hCoherent : CoherentHigherWeakLocalizationUniversalPrinciple
      (W := W) (uH := uH) (vH := vH)) :
    HigherWeakUniversalFactorExistenceCompletion
      (W := W) (uH := uH) (vH := vH) := by
  intro R hR _
  rcases hCoherent R hR with ⟨U⟩
  exact
    hasWeakUniversalCandidate_of_coherentUniversalProperty (W := W) U

/-- Under a coherent universal principle, the v2.31 three-stage completion
package is exactly Stage III completion alone.  Stage I follows from v2.19 and
Stage II from the preceding theorem. -/
theorem higherWeakLocalizationUniversalGapCompletion_iff_essentialUniquenessCompletion_of_coherent
    (hCoherent : CoherentHigherWeakLocalizationUniversalPrinciple
      (W := W) (uH := uH) (vH := vH)) :
    HigherWeakLocalizationUniversalGapCompletion
        (W := W) (uH := uH) (vH := vH) ↔
      HigherWeakEssentialUniquenessCompletion
        (W := W) (uH := uH) (vH := vH) := by
  constructor
  · intro hGap
    exact hGap.2.2
  · intro hStageIII
    exact
      ⟨higherWeakLocalizationExistence_of_coherentUniversalPrinciple W hCoherent,
        higherWeakUniversalFactorExistenceCompletion_of_coherentUniversalPrinciple
          (W := W) hCoherent,
        hStageIII⟩

/-- Main global collapse theorem: relative to an explicitly supplied coherent
v2.19 universal principle, the v2.18 weak universal principle is equivalent to
Stage III essential-uniqueness completion. -/
theorem higherWeakLocalizationUniversalPrinciple_iff_essentialUniquenessCompletion_of_coherent
    (hCoherent : CoherentHigherWeakLocalizationUniversalPrinciple
      (W := W) (uH := uH) (vH := vH)) :
    HigherWeakLocalizationUniversalPrinciple
        (W := W) (uH := uH) (vH := vH) ↔
      HigherWeakEssentialUniquenessCompletion
        (W := W) (uH := uH) (vH := vH) := by
  rw [higherWeakLocalizationUniversalPrinciple_iff_gapCompletion (W := W)]
  exact
    higherWeakLocalizationUniversalGapCompletion_iff_essentialUniquenessCompletion_of_coherent
      (W := W) hCoherent

/-- Global correction solvability is a sufficient Stage III completion route
under the coherent universal premise.  This is not stated as a converse. -/
theorem higherWeakEssentialUniquenessCompletion_of_coherent_and_corrections
    (hCoherent : CoherentHigherWeakLocalizationUniversalPrinciple
      (W := W) (uH := uH) (vH := vH))
    (hCorrections : HigherStoredTriangleTargetCorrectionPrinciple
      (W := W) (uH := uH) (vH := vH)) :
    HigherWeakEssentialUniquenessCompletion
      (W := W) (uH := uH) (vH := vH) :=
  higherWeakEssentialUniquenessCompletion_of_universalPrinciple
    (W := W)
    (higherWeakLocalizationUniversalPrinciple_of_coherent_and_corrections
      W hCoherent hCorrections)

/-!
The v2.32 frontier is therefore:

```text
CoherentWeakHigherLocalizationUniversalProperty W R
        |
        +--> Stage I obstruction impossible
        |
        +--> Stage II obstruction impossible
        |
        v
v2.31 gap obstruction
        <->
Stage III essential-uniqueness obstruction
        |
        v
v2.21 factor-coherence obstruction
        <->
v2.22 modification-triangle obstruction
        <->
v2.26 stored-triangle correction obstruction.
```

The first equivalence is new at the v2.31 system-gap level.  The lower
obstruction equivalences remain those already proved in v2.21--v2.26; this file
only transports the surviving Stage III failure into that established route.
No converse from correction failure to Stage III failure is claimed, because a
particular coherent route may fail even when another v2.18 universal candidate
exists.  No v2.30 arrowwise equation obstruction is inferred without its own
additional extension/rigidity hypotheses.
-/

end KUOS.DependentOriginationCoherentStageIIIGapCollapseV2_32
