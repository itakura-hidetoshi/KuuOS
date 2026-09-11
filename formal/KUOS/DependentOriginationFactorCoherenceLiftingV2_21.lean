import KUOS.DependentOriginationCoherentFactorForgetfulBridgeV2_20

namespace KUOS.DependentOriginationFactorCoherenceLiftingV2_21

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationCoherentFactorForgetfulBridgeV2_20

open scoped CategoryTheory.Pseudofunctor.StrongTrans

universe u v uH vH

/-!
# Factor-coherence lifting obstruction v2.21

The v2.20 layer proves that every coherent v2.19 factor morphism forgets to a
valid v2.18 factor morphism.  The remaining mismatch between the two universal
properties is therefore entirely in the opposite direction: v2.18 essential
uniqueness quantifies over arbitrary objectwise factor morphisms, while v2.19
essential uniqueness only quantifies over factor morphisms carrying a coherent
modification-level triangle.

This file isolates exactly the additional hypothesis needed to bridge that gap.
An arbitrary v2.18 factor morphism is required to admit a coherent refinement
with the **same underlying StrongTrans**.  Under that lifting hypothesis, the
v2.19 essential-uniqueness theorem applies to arbitrary v2.18 factor maps, and
the full v2.18 universal-property datum follows.

No such lifting theorem is asserted unconditionally.  In particular, this file
introduces neither a new axiom nor a strictification principle, and it does not
replace equivalence-valued higher localization by ordinary 1-categorical
localization.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- A coherent refinement of one v2.18 factor morphism.

The coherent factor has a modification-level comparison triangle, while
`hom_eq` states that no new factor 1-cell is introduced: its underlying
StrongTrans is exactly the StrongTrans of the original v2.18 factor morphism. -/
structure CoherentLiftOfV2_18Factor
    {R : RawHigherContextualSystem (Context := Context)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K) where
  /-- The coherent refinement. -/
  coherent : CoherentHigherLocalizationFactorMorphism (W := W) H K
  /-- Coherence is added without changing the underlying StrongTrans. -/
  hom_eq : coherent.hom = alpha.hom

/-- Every v2.18 factor map into the chosen coherent universal factorization can
be equipped with a modification-level comparison triangle without changing its
underlying StrongTrans.

This is the precise lifting condition missing after v2.20. -/
def HigherFactorCoherenceLifting
    {R : RawHigherContextualSystem (Context := Context)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∀ (H : HigherLocalizationFactorization (W := W) R)
    (alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),
    Nonempty (CoherentLiftOfV2_18Factor (W := W) alpha)

/-- Failure of factor-coherence lifting is exhibited by one v2.18 factor morphism
that admits no coherent refinement with the same underlying StrongTrans. -/
def HigherFactorCoherenceObstruction
    {R : RawHigherContextualSystem (Context := Context)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∃ (H : HigherLocalizationFactorization (W := W) R)
    (alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),
    ¬ Nonempty (CoherentLiftOfV2_18Factor (W := W) alpha)

/-- The lifting condition is exactly absence of the explicit factor-coherence
obstruction. -/
theorem higherFactorCoherenceLifting_iff_no_obstruction
    {R : RawHigherContextualSystem (Context := Context)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherFactorCoherenceLifting (W := W) U ↔
      ¬ HigherFactorCoherenceObstruction (W := W) U := by
  constructor
  · intro hLift hObs
    rcases hObs with ⟨H, alpha, hNoLift⟩
    exact hNoLift (hLift H alpha)
  · intro hNoObs H alpha
    classical
    by_contra hNoLift
    exact hNoObs ⟨H, alpha, hNoLift⟩

/-- Under factor-coherence lifting, a coherent v2.19 universal-property datum
for `R` yields the full v2.18 universal-property datum for the same chosen
factorization.

The factor-existence field is obtained by the v2.20 forgetful bridge.  For
essential uniqueness, arbitrary v2.18 factors are coherently refined, compared
using v2.19 essential uniqueness, and then transported back along the equalities
of underlying StrongTrans. -/
def weakHigherLocalizationUniversalPropertyOfCoherent
    {R : RawHigherContextualSystem (Context := Context)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hLift : HigherFactorCoherenceLifting (W := W) U) :
    WeakHigherLocalizationUniversalProperty (W := W) R where
  chosen := U.chosen
  factor H := coherentWeakUniversalProperty_hasV2_18Factor W U H
  essential_unique H alpha beta := by
    rcases hLift H alpha with ⟨alphaLift⟩
    rcases hLift H beta with ⟨betaLift⟩
    rcases U.essential_unique H alphaLift.coherent betaLift.coherent with ⟨e⟩
    exact ⟨by simpa only [alphaLift.hom_eq, betaLift.hom_eq] using e⟩

/-- Package the exact additional data needed to descend from the coherent v2.19
universal property to the v2.18 universal property. -/
def HasCoherentWeakHigherLocalizationUniversalPropertyWithFactorLifting
    (R : RawHigherContextualSystem (Context := Context)) : Prop :=
  ∃ U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R,
    HigherFactorCoherenceLifting (W := W) U

/-- Coherent universal data together with factor-coherence lifting imply
existence of the v2.18 weak higher localization universal-property datum. -/
theorem hasWeakHigherLocalizationUniversalProperty_of_coherent_with_factorLifting
    {R : RawHigherContextualSystem (Context := Context)}
    (h : HasCoherentWeakHigherLocalizationUniversalPropertyWithFactorLifting
      (W := W) R) :
    HasWeakHigherLocalizationUniversalProperty (W := W) R := by
  rcases h with ⟨U, hLift⟩
  exact ⟨weakHigherLocalizationUniversalPropertyOfCoherent W U hLift⟩

/-- Global factor-coherence lifting principle for coherent universal-property
data.  This remains an explicit proposition rather than an axiom. -/
def HigherFactorCoherenceLiftingPrinciple : Prop :=
  ∀ (R : RawHigherContextualSystem (Context := Context))
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R),
    HigherFactorCoherenceLifting (W := W) U

/-- The coherent v2.19 universal principle plus the explicit factor-coherence
lifting principle imply the v2.18 weak universal principle.

This theorem closes only the logical mismatch between the two interfaces.  It
does not prove either premise. -/
theorem higherWeakLocalizationUniversalPrinciple_of_coherent_and_factorCoherenceLifting
    (hCoherent : CoherentHigherWeakLocalizationUniversalPrinciple (W := W))
    (hLift : HigherFactorCoherenceLiftingPrinciple (W := W)) :
    HigherWeakLocalizationUniversalPrinciple (W := W) := by
  intro R hR
  rcases hCoherent R hR with ⟨U⟩
  exact ⟨weakHigherLocalizationUniversalPropertyOfCoherent W U (hLift R U)⟩

/-!
The boundary after v2.21 is therefore explicit:

```text
CoherentWeakHigherLocalizationUniversalProperty W R
        +
HigherFactorCoherenceLifting W U
        |
        v                         proved here
WeakHigherLocalizationUniversalProperty W R

HigherFactorCoherenceLifting W U
        <->
no explicit v2.18 factor lacks a coherent refinement.
```

The unresolved mathematical content is now localized to the coherence-lifting
problem itself (and, separately, existence of coherent universal data).  Neither
is hidden behind ordinary localization or an unproved strictification step.
-/

end KUOS.DependentOriginationFactorCoherenceLiftingV2_21
