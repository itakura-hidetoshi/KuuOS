import KUOS.DependentOriginationCanonicalFiveLawCounterexampleV3_70
import KUOS.DependentOriginationPointwiseEquivalenceTransportV2_17

namespace KUOS.DependentOriginationFactorizationNecessityBoundaryV3_71

open CategoryTheory
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseEquivalenceTransportV2_17
open KUOS.DependentOriginationCoherentComparisonFactorizationV2_60
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationArbitraryTransportComparisonV3_69
open KUOS.DependentOriginationCanonicalFiveLawCounterexampleV3_70

set_option autoImplicit false

noncomputable section

universe u v uH vH

/-!
# Factorization necessity boundary v3.71

v3.70 proves that the concrete octahedral C2 system is weakly admissible while
its canonical five-law package is empty.  It is tempting to bridge this
immediately to nonexistence of the larger v2.10
`HigherLocalizationFactorization` interface by asserting that every
factorization normalizes to the canonical five-law package.

This file separates the genuinely proved structural reduction from that still
unproved normalization statement.

For any factorization `H`:

* its localized lift `H.lift`, when restricted back to the raw base, has a
  tautological factorization with identity comparison;
* the original comparison of `H` is exactly a pointwise-equivalence strong
  comparison from that literal restriction to the raw system.

Thus an arbitrary factorization decomposes as

```text
restrict(H.lift)
  -- pointwise-equivalence comparison --> R.
```

What is not automatic is transport of the canonical five-law normal form across
that pointwise equivalence.

For the concrete countermodel, because v3.70 already proves that the canonical
five-law package is empty, the proposed normalization bridge is logically
equivalent to nonexistence of arbitrary higher-localization factorization.
Hence proving the bridge as an intermediate lemma would be circular: the next
mathematical task must attack arbitrary factorization data directly, or prove a
genuinely independent presentation-invariance theorem strong enough to transport
the obstruction.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Any localized higher system tautologically factors its own restriction.
The localized carrier is unchanged and the comparison is the identity strong
transformation. -/
noncomputable def restrictionHigherLocalizationFactorization
    (F : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)) :
    HigherLocalizationFactorization (W := W)
      (restrictHigherLocalizedSystem W F) where
  lift := F
  comparison := 𝟙 _
  comparison_isEquivalence := by
    intro X
    change (𝟭 ((restrictHigherLocalizedSystem W F).obj (.mk X))).IsEquivalence
    infer_instance

/-- Every arbitrary factorization supplies a directed pointwise-equivalence
comparison from the literal restriction of its localized lift back to the raw
system. -/
noncomputable def factorizationRestrictionPointwiseEquivalence
    {R : RawHigherContextualSystem.{u, v, uH, vH} (Context := Context)}
    (H : HigherLocalizationFactorization (W := W) R) :
    HigherPointwiseEquivalenceComparison
      (restrictHigherLocalizedSystem W H.lift) R where
  comparison := H.comparison
  comparison_isEquivalence := H.comparison_isEquivalence

/-- The tautological factorization of the restriction has exactly the same
localized lift. -/
@[simp] theorem restrictionHigherLocalizationFactorization_lift
    (F : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)) :
    (restrictionHigherLocalizationFactorization W F).lift = F := by
  rfl

/-- The pointwise-equivalence comparison extracted from a factorization is
literally its stored comparison. -/
@[simp] theorem factorizationRestrictionPointwiseEquivalence_comparison
    {R : RawHigherContextualSystem.{u, v, uH, vH} (Context := Context)}
    (H : HigherLocalizationFactorization (W := W) R) :
    (factorizationRestrictionPointwiseEquivalence W H).comparison =
      H.comparison := by
  rfl

/-! ## Concrete countermodel boundary -/

/-- Proposed canonical-normalization bridge for the concrete countermodel:
existence of any abstract higher-localization factorization would force
existence of the canonical five-law package. -/
def CounterCanonicalFiveLawNecessity : Prop :=
  HasHigherLocalizationFactorization
      (W := allMorphisms) counterSystem ->
    HasCoherentGeneralWFactorizationData
      allMorphisms counterSystem counterD

/-- Pointwise version of the same proposed bridge: every individual abstract
factorization normalizes to the canonical five-law package. -/
def CounterEveryFactorizationCanonicalNormalizes : Prop :=
  ∀ H : HigherLocalizationFactorization
      (W := allMorphisms) counterSystem,
    HasCoherentGeneralWFactorizationData
      allMorphisms counterSystem counterD

/-- The existence-shaped and pointwise-shaped normalization principles are
logically equivalent. -/
theorem counterEveryFactorizationCanonicalNormalizes_iff_necessity :
    CounterEveryFactorizationCanonicalNormalizes ↔
      CounterCanonicalFiveLawNecessity := by
  constructor
  · intro hNorm hExists
    rcases hExists with ⟨H⟩
    exact hNorm H
  · intro hNec H
    exact hNec ⟨H⟩

/-- Because v3.70 already proves that the canonical five-law package is empty,
the proposed necessity bridge is equivalent to complete nonexistence of an
abstract higher-localization factorization for the countermodel.

This theorem is the exact anti-circularity boundary for the next stage. -/
theorem counterCanonicalFiveLawNecessity_iff_noHigherLocalizationFactorization :
    CounterCanonicalFiveLawNecessity ↔
      ¬ HasHigherLocalizationFactorization
          (W := allMorphisms) counterSystem := by
  constructor
  · intro hNec hFactor
    exact
      counterD_not_hasCoherentGeneralWFactorizationData
        (hNec hFactor)
  · intro hNo hFactor
    exact (hNo hFactor).elim

/-- Equivalently, saying that every abstract factorization admits canonical
five-law normalization is already exactly as strong as saying that no abstract
factorization exists. -/
theorem counterEveryFactorizationCanonicalNormalizes_iff_noHigherLocalizationFactorization :
    CounterEveryFactorizationCanonicalNormalizes ↔
      ¬ HasHigherLocalizationFactorization
          (W := allMorphisms) counterSystem := by
  rw [counterEveryFactorizationCanonicalNormalizes_iff_necessity,
    counterCanonicalFiveLawNecessity_iff_noHigherLocalizationFactorization]

/-!
## Boundary after v3.71

The structural decomposition

```text
arbitrary H : HigherLocalizationFactorization W R

H.lift
  -> tautological factorization of restrict(H.lift)

H.comparison
  -> pointwise-equivalence comparison
     restrict(H.lift) --> R
```

is unconditional.

For the concrete C2 countermodel, however,

```text
every factorization canonically normalizes to five-law data
  <-> no arbitrary higher-localization factorization exists.
```

Therefore canonical-normalization is not a weaker bridge that can simply be
assumed or proved by repackaging v3.69.  The next truth test must instead
analyze the StrongTrans comparison and the arbitrary localized compositor of an
arbitrary factorization directly, or establish an independent
presentation-invariance theorem for the parity obstruction.

No nonfactorization theorem is claimed in v3.71.
-/

end

end KUOS.DependentOriginationFactorizationNecessityBoundaryV3_71
