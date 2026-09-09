import KUOS.DependentOriginationPointwiseCoherenceEquationV2_30

namespace KUOS.DependentOriginationWeakHigherLocalizationGapDecompositionV2_31

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationWeakToStrictReductionV2_14
open KUOS.DependentOriginationHigherStrictificationPrincipleV2_15
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18

open scoped CategoryTheory.Pseudofunctor.StrongTrans

universe u v uH vH

/-!
# Weak higher localization universal-property gap decomposition v2.31

The v2.21--v2.30 layers analyze coherence of factor morphisms and comparison
triangles down to correction equations, rigidity, local extension, and explicit
arrowwise naturality equations.  This file moves one level upward and decomposes
the still-open implication

```text
IsHigherWAdmissible W R
  ->
HasWeakHigherLocalizationUniversalProperty W R
```

according to the three fields of the v2.18 universal-property structure.

For one raw higher system `R`, the completion problem has three stages:

1. existence of some higher localization factorization;
2. existence of a chosen factorization receiving a v2.18 factor morphism from
   every competing factorization;
3. essential uniqueness of all such factor morphisms into that same chosen
   factorization.

The second and third stages are packaged without requiring every arbitrary
factorization to be universal.  The completed candidate contains one chosen
factorization, its universal factor-existence property, and essential uniqueness
on that same chosen object.

The file then gives an exact admissible-domain failure normal form as the
disjunction of three explicit stage obstructions, and a global equivalence
between the original v2.18 universal principle and the conjunction of three
completion principles.

No completion principle is proved unconditionally.  In particular, no general
strictification, weak higher-localization existence, factor-existence completion,
essential-uniqueness completion, or coherence-equation solvability theorem is
asserted here.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Stage II local property for one chosen factorization `K`: every competing
factorization admits a v2.18 factor morphism into `K`.

This requires only the objectwise comparison triangles of v2.18.  No v2.19
modification-level coherence is added here. -/
def WeakUniversalFactorExistence
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (K : HigherLocalizationFactorization (W := W) R) : Prop :=
  ∀ H : HigherLocalizationFactorization (W := W) R,
    Nonempty (HigherLocalizationFactorMorphism (W := W) H K)

/-- Stage III local property for one chosen factorization `K`: any two v2.18
factor morphisms from the same competitor into `K` have isomorphic underlying
StrongTrans 1-cells. -/
def WeakUniversalEssentialUniqueness
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (K : HigherLocalizationFactorization (W := W) R) : Prop :=
  ∀ (H : HigherLocalizationFactorization (W := W) R)
    (alpha beta : HigherLocalizationFactorMorphism (W := W) H K),
    Nonempty (alpha.hom ≅ beta.hom)

/-- A Stage II universal candidate consists of one actual v2.10 factorization
plus the v2.18 factor-existence property for that same chosen factorization. -/
structure WeakHigherLocalizationUniversalCandidate
    (R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)) where
  /-- Chosen higher localization factorization. -/
  chosen : HigherLocalizationFactorization (W := W) R
  /-- Every competing factorization factors weakly into `chosen`. -/
  factor : WeakUniversalFactorExistence (W := W) chosen

/-- Stage III property attached to a fixed Stage II candidate. -/
def WeakHigherLocalizationUniversalCandidate.HasEssentialUniqueness
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (C : WeakHigherLocalizationUniversalCandidate (W := W) R) : Prop :=
  WeakUniversalEssentialUniqueness (W := W) C.chosen

/-- Existence of some Stage II universal candidate. -/
def HasWeakHigherLocalizationUniversalCandidate
    (R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)) : Prop :=
  Nonempty (WeakHigherLocalizationUniversalCandidate (W := W) R)

/-- Existence of one Stage II candidate for which Stage III essential uniqueness
also holds on the same chosen factorization. -/
def HasWeakHigherLocalizationUniversalCandidateWithUniqueness
    (R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)) : Prop :=
  ∃ C : WeakHigherLocalizationUniversalCandidate (W := W) R,
    C.HasEssentialUniqueness (W := W)

/-- Forget a v2.18 universal-property datum to its Stage II universal candidate. -/
def weakUniversalCandidateOfUniversalProperty
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : WeakHigherLocalizationUniversalProperty (W := W) R) :
    WeakHigherLocalizationUniversalCandidate (W := W) R where
  chosen := U.chosen
  factor := U.factor

/-- Reassemble the v2.18 universal-property datum from one Stage II candidate
and Stage III essential uniqueness for the same chosen factorization. -/
def weakHigherLocalizationUniversalPropertyOfCandidateWithUniqueness
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (C : WeakHigherLocalizationUniversalCandidate (W := W) R)
    (hUnique : C.HasEssentialUniqueness (W := W)) :
    WeakHigherLocalizationUniversalProperty (W := W) R where
  chosen := C.chosen
  factor := C.factor
  essential_unique := hUnique

/-- Exact local characterization: the v2.18 universal property exists exactly
when there is one Stage II candidate carrying Stage III essential uniqueness. -/
theorem hasWeakHigherLocalizationUniversalProperty_iff_candidateWithUniqueness
    (R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)) :
    HasWeakHigherLocalizationUniversalProperty (W := W) R ↔
      HasWeakHigherLocalizationUniversalCandidateWithUniqueness (W := W) R := by
  constructor
  · rintro ⟨U⟩
    exact ⟨weakUniversalCandidateOfUniversalProperty (W := W) U, U.essential_unique⟩
  · rintro ⟨C, hUnique⟩
    exact
      ⟨weakHigherLocalizationUniversalPropertyOfCandidateWithUniqueness
        (W := W) C hUnique⟩

/-- A Stage II candidate contains, in particular, a genuine v2.10
factorization. -/
theorem hasHigherLocalizationFactorization_of_hasWeakUniversalCandidate
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (hC : HasWeakHigherLocalizationUniversalCandidate (W := W) R) :
    HasHigherLocalizationFactorization (W := W) R := by
  rcases hC with ⟨C⟩
  exact ⟨C.chosen⟩

/-- A completed candidate contains its Stage II candidate. -/
theorem hasWeakUniversalCandidate_of_candidateWithUniqueness
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (hC : HasWeakHigherLocalizationUniversalCandidateWithUniqueness (W := W) R) :
    HasWeakHigherLocalizationUniversalCandidate (W := W) R := by
  rcases hC with ⟨C, _⟩
  exact ⟨C⟩

/-- Stage I obstruction on the admissible domain: `R` is weakly `W`-admissible
but has no v2.10 higher localization factorization at all. -/
def HigherWeakLocalizationFactorizationExistenceObstruction
    (R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)) : Prop :=
  IsHigherWAdmissible W R ∧
    ¬ HasHigherLocalizationFactorization (W := W) R

/-- Stage II obstruction: a factorization exists, but no factorization can be
chosen that receives v2.18 factor morphisms from all competitors. -/
def HigherWeakUniversalFactorExistenceObstruction
    (R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)) : Prop :=
  IsHigherWAdmissible W R ∧
    HasHigherLocalizationFactorization (W := W) R ∧
      ¬ HasWeakHigherLocalizationUniversalCandidate (W := W) R

/-- Stage III obstruction: a Stage II universal candidate exists, but no such
candidate also satisfies v2.18 essential uniqueness. -/
def HigherWeakEssentialUniquenessObstruction
    (R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)) : Prop :=
  IsHigherWAdmissible W R ∧
    HasWeakHigherLocalizationUniversalCandidate (W := W) R ∧
      ¬ HasWeakHigherLocalizationUniversalCandidateWithUniqueness (W := W) R

/-- The complete local gap obstruction is the disjunction of the three exact
stage failures. -/
def HigherWeakLocalizationUniversalGapObstruction
    (R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)) : Prop :=
  HigherWeakLocalizationFactorizationExistenceObstruction (W := W) R ∨
    HigherWeakUniversalFactorExistenceObstruction (W := W) R ∨
      HigherWeakEssentialUniquenessObstruction (W := W) R

/-- Failure of factorization existence is stronger than failure of the strict
presentation route: if no factorization exists, then in particular no strict
presentation model can exist, because v2.14 would turn such a model into a
factorization.

The converse is deliberately not claimed.  Thus strictification failure is not
silently identified with Stage I failure. -/
theorem higherStrictificationObstruction_of_factorizationExistenceObstruction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (hObs : HigherWeakLocalizationFactorizationExistenceObstruction (W := W) R) :
    HigherStrictificationObstruction (W := W) R := by
  refine ⟨hObs.1, ?_⟩
  intro hStrict
  apply hObs.2
  exact hasHigherLocalizationFactorization_of_strictPresentationModel W hStrict

/-- Exact admissible-domain failure normal form.  Once admissibility is fixed,
failure of the v2.18 universal property occurs exactly at one of the three
stages: no factorization, no universal candidate, or no essentially unique
universal candidate. -/
theorem not_hasWeakHigherLocalizationUniversalProperty_iff_gapObstruction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (hR : IsHigherWAdmissible W R) :
    (¬ HasWeakHigherLocalizationUniversalProperty (W := W) R) ↔
      HigherWeakLocalizationUniversalGapObstruction (W := W) R := by
  classical
  constructor
  · intro hNoUniversal
    have hNoComplete :
        ¬ HasWeakHigherLocalizationUniversalCandidateWithUniqueness (W := W) R := by
      intro hComplete
      exact hNoUniversal
        ((hasWeakHigherLocalizationUniversalProperty_iff_candidateWithUniqueness
          (W := W) R).mpr hComplete)
    by_cases hFactorization : HasHigherLocalizationFactorization (W := W) R
    · by_cases hCandidate : HasWeakHigherLocalizationUniversalCandidate (W := W) R
      · exact Or.inr (Or.inr ⟨hR, hCandidate, hNoComplete⟩)
      · exact Or.inr (Or.inl ⟨hR, hFactorization, hCandidate⟩)
    · exact Or.inl ⟨hR, hFactorization⟩
  · intro hGap hUniversal
    have hComplete :
        HasWeakHigherLocalizationUniversalCandidateWithUniqueness (W := W) R :=
      (hasWeakHigherLocalizationUniversalProperty_iff_candidateWithUniqueness
        (W := W) R).mp hUniversal
    have hCandidate :
        HasWeakHigherLocalizationUniversalCandidate (W := W) R :=
      hasWeakUniversalCandidate_of_candidateWithUniqueness (W := W) hComplete
    have hFactorization :
        HasHigherLocalizationFactorization (W := W) R :=
      hasHigherLocalizationFactorization_of_hasWeakUniversalCandidate
        (W := W) hCandidate
    rcases hGap with hStageI | hRest
    · exact hStageI.2 hFactorization
    · rcases hRest with hStageII | hStageIII
      · exact hStageII.2.2 hCandidate
      · exact hStageIII.2.2 hComplete

/-- Stage II global completion principle.  It does not claim that every
factorization is universal: given admissibility and Stage I existence, it asks
only for existence of some Stage II universal candidate. -/
def HigherWeakUniversalFactorExistenceCompletion : Prop :=
  ∀ R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH),
    IsHigherWAdmissible W R →
      HasHigherLocalizationFactorization (W := W) R →
        HasWeakHigherLocalizationUniversalCandidate (W := W) R

/-- Stage III global completion principle.  Given admissibility and existence of
some Stage II candidate, it asks for existence of a possibly selected candidate
that retains Stage II factor existence and also satisfies essential uniqueness.
The completed candidate itself keeps both properties on one chosen
factorization. -/
def HigherWeakEssentialUniquenessCompletion : Prop :=
  ∀ R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH),
    IsHigherWAdmissible W R →
      HasWeakHigherLocalizationUniversalCandidate (W := W) R →
        HasWeakHigherLocalizationUniversalCandidateWithUniqueness (W := W) R

/-- Package the three global completion obligations without asserting any of
them. -/
def HigherWeakLocalizationUniversalGapCompletion : Prop :=
  HigherWeakLocalizationExistence (W := W) (uH := uH) (vH := vH) ∧
    HigherWeakUniversalFactorExistenceCompletion (W := W) (uH := uH) (vH := vH) ∧
      HigherWeakEssentialUniquenessCompletion (W := W) (uH := uH) (vH := vH)

/-- The v2.18 universal principle implies Stage II completion. -/
theorem higherWeakUniversalFactorExistenceCompletion_of_universalPrinciple
    (hUniversal : HigherWeakLocalizationUniversalPrinciple
      (W := W) (uH := uH) (vH := vH)) :
    HigherWeakUniversalFactorExistenceCompletion
      (W := W) (uH := uH) (vH := vH) := by
  intro R hR _
  rcases hUniversal R hR with ⟨U⟩
  exact ⟨weakUniversalCandidateOfUniversalProperty (W := W) U⟩

/-- The v2.18 universal principle implies Stage III completion. -/
theorem higherWeakEssentialUniquenessCompletion_of_universalPrinciple
    (hUniversal : HigherWeakLocalizationUniversalPrinciple
      (W := W) (uH := uH) (vH := vH)) :
    HigherWeakEssentialUniquenessCompletion
      (W := W) (uH := uH) (vH := vH) := by
  intro R hR _
  rcases hUniversal R hR with ⟨U⟩
  exact ⟨weakUniversalCandidateOfUniversalProperty (W := W) U, U.essential_unique⟩

/-- The three stage-completion obligations reconstruct the full v2.18 universal
principle by following the dependency chain on each admissible raw system. -/
theorem higherWeakLocalizationUniversalPrinciple_of_gapCompletion
    (hGap : HigherWeakLocalizationUniversalGapCompletion
      (W := W) (uH := uH) (vH := vH)) :
    HigherWeakLocalizationUniversalPrinciple
      (W := W) (uH := uH) (vH := vH) := by
  intro R hR
  have hFactorization : HasHigherLocalizationFactorization (W := W) R :=
    hGap.1 R hR
  have hCandidate : HasWeakHigherLocalizationUniversalCandidate (W := W) R :=
    hGap.2.1 R hR hFactorization
  have hComplete :
      HasWeakHigherLocalizationUniversalCandidateWithUniqueness (W := W) R :=
    hGap.2.2 R hR hCandidate
  exact
    (hasWeakHigherLocalizationUniversalProperty_iff_candidateWithUniqueness
      (W := W) R).mpr hComplete

/-- Main global decomposition theorem.  The open v2.18 implication is exactly
equivalent to the conjunction of:

1. Stage I higher factorization existence;
2. Stage II universal factor-existence completion;
3. Stage III essential-uniqueness completion.

This is an equivalence of propositions, not a proof that either side holds. -/
theorem higherWeakLocalizationUniversalPrinciple_iff_gapCompletion :
    HigherWeakLocalizationUniversalPrinciple
        (W := W) (uH := uH) (vH := vH) ↔
      HigherWeakLocalizationUniversalGapCompletion
        (W := W) (uH := uH) (vH := vH) := by
  constructor
  · intro hUniversal
    exact
      ⟨higherWeakLocalizationExistence_of_universalPrinciple W hUniversal,
        higherWeakUniversalFactorExistenceCompletion_of_universalPrinciple
          (W := W) hUniversal,
        higherWeakEssentialUniquenessCompletion_of_universalPrinciple
          (W := W) hUniversal⟩
  · exact higherWeakLocalizationUniversalPrinciple_of_gapCompletion (W := W)

/-- Equivalent obstruction-free global normal form: the universal principle
holds exactly when every admissible raw system has no Stage I/II/III gap
obstruction. -/
theorem higherWeakLocalizationUniversalPrinciple_iff_no_gapObstruction :
    HigherWeakLocalizationUniversalPrinciple
        (W := W) (uH := uH) (vH := vH) ↔
      ∀ R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH),
        IsHigherWAdmissible W R →
          ¬ HigherWeakLocalizationUniversalGapObstruction (W := W) R := by
  classical
  constructor
  · intro hUniversal R hR hGap
    have hNoUniversal :
        ¬ HasWeakHigherLocalizationUniversalProperty (W := W) R :=
      (not_hasWeakHigherLocalizationUniversalProperty_iff_gapObstruction
        (W := W) hR).mpr hGap
    exact hNoUniversal (hUniversal R hR)
  · intro hNoGap R hR
    by_contra hNoUniversal
    exact
      hNoGap R hR
        ((not_hasWeakHigherLocalizationUniversalProperty_iff_gapObstruction
          (W := W) hR).mp hNoUniversal)

/-!
The v2.31 boundary is therefore:

```text
IsHigherWAdmissible W R
        |
        | Stage I: HigherWeakLocalizationExistence              OPEN
        v
some HigherLocalizationFactorization
        |
        | Stage II: HigherWeakUniversalFactorExistenceCompletion OPEN
        v
some WeakHigherLocalizationUniversalCandidate
        |
        | Stage III: HigherWeakEssentialUniquenessCompletion     OPEN
        v
HasWeakHigherLocalizationUniversalProperty W R.
```

On the admissible domain, failure of the final line is exactly the disjunction
of the three explicit stage obstructions.  Globally, the original v2.18
universal principle is exactly equivalent both to the three-stage completion
package and to absence of the local gap obstruction for every admissible raw
system.

The lower v2.21--v2.30 coherence/correction/rigidity/arrow-equation analysis is
not collapsed into any one of these stages.  It remains a finer analysis of
specific routes into factor coherence and uniqueness, while v2.31 records the
full logical gap of the v2.18 universal property itself.
-/

end KUOS.DependentOriginationWeakHigherLocalizationGapDecompositionV2_31
