import KUOS.DependentOriginationCountableRankedEnumerationV3_44
import Mathlib.Data.List.FinRange

namespace KUOS.DependentOriginationLowerRankFinitenessV3_45

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationThreeRouteCorrectionCompatibilityGapV3_09
open KUOS.DependentOriginationQuotientGaugeIntersectionObstructionV3_11
open KUOS.DependentOriginationQuotientGaugeCoordinateKeyV3_14
open KUOS.DependentOriginationUnitorWitnessCorrelationV3_35
open KUOS.DependentOriginationAssociatorUnitorBoundaryReductionV3_36
open KUOS.DependentOriginationFreshAssociatorCompletionV3_37
open KUOS.DependentOriginationFiniteAssociatorScheduleV3_38
open KUOS.DependentOriginationCountableAssociatorStabilizationV3_39
open KUOS.DependentOriginationCollisionSectorPreservationV3_40
open KUOS.DependentOriginationAssociatorIncidenceDecompositionV3_41
open KUOS.DependentOriginationFreshInteriorGlobalCoverageV3_42
open KUOS.DependentOriginationFiniteRankedScheduleV3_43
open KUOS.DependentOriginationCountableRankedEnumerationV3_44

universe u v uH vH

set_option autoImplicit false

/-!
# Finite lower-rank sublevels are necessary for ranked countable schedules v3.45

v3.44 shows that an injective rank-monotone enumeration of the complete
fresh/interior sector automatically satisfies v3.39 forward noninterference.

This layer proves a converse structural constraint on any such enumeration.
Fix a task appearing at index i. Every fresh/interior task of strictly smaller
rank must appear at an index j < i. Otherwise equality of indices would give an
irreflexive rank inequality, while i < j would contradict rank monotonicity.

Hence all strictly lower-rank fresh/interior tasks are contained in the finite
prefix consisting of the first i enumerated tasks.

This makes lower-rank local finiteness a proved necessary condition for the
rank-monotone natural-number scheduling strategy, rather than merely a
convenient hypothesis suggested by examples.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- The first i actual tasks of one countable ranked enumeration. -/
def rankedEnumerationPrefix
    (E : CountableRankedFreshInteriorEnumeration W) (i : ℕ) :
    List (AssociatorTask W) :=
  List.ofFn (fun j : Fin i => E.tasks j)

/-- Explicit list-form lower-rank local finiteness for the fresh/interior
sector. The finite list may contain extra tasks; it must cover every strictly
lower-rank fresh/interior task. -/
def HasFiniteLowerRankFreshInteriorCovers
    (rank : AssociatorTask W → ℕ) : Prop :=
  ∀ a : AssociatorTask W,
    FreshInteriorAssociatorTask W a →
      ∃ lower : List (AssociatorTask W),
        ∀ b : AssociatorTask W,
          FreshInteriorAssociatorTask W b →
          rank b < rank a →
            b ∈ lower

/-- If b has lower rank than the task at enumeration index i, then b must have
already appeared at a strictly earlier index. -/
theorem lowerRank_task_occurs_before
    (E : CountableRankedFreshInteriorEnumeration W)
    {i : ℕ} {b : AssociatorTask W}
    (hb : FreshInteriorAssociatorTask W b)
    (hRank : E.rank b < E.rank (E.tasks i)) :
    ∃ j : ℕ, j < i ∧ b = E.tasks j := by
  rcases E.covers b hb with ⟨j, hj⟩
  rcases lt_trichotomy j i with hji | hEq | hij
  · exact ⟨j, hji, hj⟩
  · subst j
    have hSelf :
        E.rank (E.tasks i) < E.rank (E.tasks i) := by
      simpa [hj] using hRank
    exact False.elim (Nat.lt_irrefl _ hSelf)
  · have hMono :
        E.rank (E.tasks i) ≤ E.rank (E.tasks j) :=
      E.rank_monotone hij
    have hBack :
        E.rank (E.tasks j) < E.rank (E.tasks i) := by
      simpa [hj] using hRank
    exact False.elim ((Nat.not_lt_of_ge hMono) hBack)

/-- Every lower-rank fresh/interior task belongs to the finite prefix before i. -/
theorem lowerRank_task_mem_rankedEnumerationPrefix
    (E : CountableRankedFreshInteriorEnumeration W)
    {i : ℕ} {b : AssociatorTask W}
    (hb : FreshInteriorAssociatorTask W b)
    (hRank : E.rank b < E.rank (E.tasks i)) :
    b ∈ rankedEnumerationPrefix W E i := by
  rcases lowerRank_task_occurs_before W E hb hRank with ⟨j, hji, hj⟩
  simp only [rankedEnumerationPrefix, List.mem_ofFn]
  exact ⟨⟨j, hji⟩, hj.symm⟩

/-- The prefix is duplicate-free because the ranked enumeration itself is
injective. This is stronger than needed merely to witness finiteness. -/
theorem rankedEnumerationPrefix_nodup
    (E : CountableRankedFreshInteriorEnumeration W) (i : ℕ) :
    (rankedEnumerationPrefix W E i).Nodup := by
  apply List.nodup_ofFn.mpr
  intro j k hEq
  apply Fin.ext
  exact E.injective hEq

/-- Any ranked countable enumeration forces finite lower-rank covers for the
entire fresh/interior sector. -/
theorem rankedEnumeration_hasFiniteLowerRankFreshInteriorCovers
    (E : CountableRankedFreshInteriorEnumeration W) :
    HasFiniteLowerRankFreshInteriorCovers W E.rank := by
  intro a ha
  rcases E.covers a ha with ⟨i, hi⟩
  refine ⟨rankedEnumerationPrefix W E i, ?_⟩
  intro b hb hRank
  apply lowerRank_task_mem_rankedEnumerationPrefix W E hb
  simpa [hi] using hRank

/-- A more explicit witness: each fresh/interior task has a duplicate-free
finite prefix covering all lower-rank fresh/interior tasks. -/
theorem exists_nodup_lowerRank_prefix_cover
    (E : CountableRankedFreshInteriorEnumeration W)
    (a : AssociatorTask W)
    (ha : FreshInteriorAssociatorTask W a) :
    ∃ (i : ℕ) (lower : List (AssociatorTask W)),
      a = E.tasks i ∧
      lower = rankedEnumerationPrefix W E i ∧
      lower.Nodup ∧
      ∀ b : AssociatorTask W,
        FreshInteriorAssociatorTask W b →
        E.rank b < E.rank a →
          b ∈ lower := by
  rcases E.covers a ha with ⟨i, hi⟩
  refine ⟨i, rankedEnumerationPrefix W E i, hi, rfl,
    rankedEnumerationPrefix_nodup W E i, ?_⟩
  intro b hb hRank
  apply lowerRank_task_mem_rankedEnumerationPrefix W E hb
  simpa [hi] using hRank

/-!
## Boundary after v3.45

Finite lower-rank coverage is now a theorem-level necessary condition for the
specific rank-monotone ℕ-enumeration strategy used by v3.44. It is not yet a
sufficiency theorem.

In particular, finite lower-rank covers alone do not provide:

* countability of the fresh/interior sector;
* a chosen injective enumeration;
* a rank-monotone ordering within equal-rank fibres; or
* existence of the dependency rank itself.

The next constructive question is whether countability plus an explicit rank
whose lower sublevels have suitable finite covers is enough to build the
v3.44 ranked enumeration, with finite and genuinely infinite cases separated
as in v3.42-v3.43.

The v3.41 residual sector is unchanged. No residual-sector vanishing, schedule
independence, comparison-gauge equations, general Stage I, Stage II, or final
DO universality is asserted.

Protected validation-only #1558 is untouched.
-/

end KUOS.DependentOriginationLowerRankFinitenessV3_45
