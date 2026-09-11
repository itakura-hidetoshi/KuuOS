import KUOS.DependentOriginationPointwiseEquivalenceTransportV2_17

namespace KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18

open CategoryTheory
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationHigherStrictificationPrincipleV2_15
open KUOS.DependentOriginationHigherLocalizationNecessityV2_16

open scoped CategoryTheory.Pseudofunctor.StrongTrans

universe u v uH vH

/-!
# Weak higher presentation-localization universal-property interface v2.18

The v2.17 layer identifies the strictifiable raw higher systems with the
pointwise-equivalence saturation of the strict Cat-valued sector.  What remains
open is whether every weakly `W`-admissible pseudofunctor belongs to that sector,
or whether one instead needs a genuinely bicategorical localization theorem.

This file takes the second route without asserting an existence theorem.

The key point is that the desired universal property must classify arrows in
`W` by **equivalences of categories**, not by literal isomorphisms in the
ordinary 1-category `Cat`.  We therefore introduce an explicit weak higher
localization universal-property datum whose chosen object is a genuine v2.10
higher localization factorization and whose comparison morphisms are StrongTrans.
Factor maps are required to commute with the raw comparison objectwise up to
natural isomorphism, and essential uniqueness is expressed by an invertible
modification between the underlying StrongTrans factors.

This is intentionally an interface theorem unit.  In particular:

* no existence of the universal-property datum is assumed or proved;
* ordinary `Localization.functorEquivalence` is not used as a substitute;
* no strictification of equivalences of categories to isomorphisms is asserted;
* the objectwise comparison triangle below is not advertised as the final fully
  coherent bicategorical comma-object formulation.

What is proved is the safe one-way implication requested by the higher spine:
if this stronger weak universal property exists, then the v2.10 factorization
exists, and hence the raw system is weakly `W`-admissible by v2.16.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- A morphism between two v2.10 higher-localization factorizations of the same
raw system.

The underlying 1-cell is a genuine StrongTrans between the localized lifts.  At
each raw context object, its composite with the target comparison is required to
agree with the source comparison up to a natural isomorphism of functors.

This records the universal-property triangle at the Cat-valued object level
without pretending that the triangle commutes definitionally. -/
structure HigherLocalizationFactorMorphism
    {R : RawHigherContextualSystem (Context := Context)}
    (H K : HigherLocalizationFactorization (W := W) R) where
  /-- Strong factor map between localized pseudofunctors. -/
  hom : H.lift ⟶ K.lift
  /-- Objectwise weak commutativity of the localization comparison triangle. -/
  comparison_triangle :
    ∀ X : Context,
      (hom.app (.mk ((higherPresentationUnitFunctor W).obj X))).toFunctor ⋙
          (K.comparison.app (.mk X)).toFunctor ≅
        (H.comparison.app (.mk X)).toFunctor

/-- A weak bicategorical localization universal-property datum for one raw
Cat-valued contextual system.

`chosen` supplies an actual v2.10 factorization.  Every other factorization has a
StrongTrans factor into it satisfying the objectwise comparison triangle, and
any two such factor maps are essentially unique up to an invertible modification
of their underlying StrongTrans.

Existence of this structure is deliberately *not* postulated. -/
structure WeakHigherLocalizationUniversalProperty
    (R : RawHigherContextualSystem (Context := Context)) where
  /-- Chosen weak higher localization factorization. -/
  chosen : HigherLocalizationFactorization (W := W) R
  /-- Every competing higher factorization admits a weakly comparison-preserving
  StrongTrans into the chosen factorization. -/
  factor :
    ∀ H : HigherLocalizationFactorization (W := W) R,
      Nonempty (HigherLocalizationFactorMorphism (W := W) H chosen)
  /-- Essential uniqueness of factor maps up to invertible modification of the
  underlying StrongTrans. -/
  essential_unique :
    ∀ (H : HigherLocalizationFactorization (W := W) R)
      (α β : HigherLocalizationFactorMorphism (W := W) H chosen),
      Nonempty (α.hom ≅ β.hom)

/-- Existence of the v2.18 weak higher localization universal-property datum is
kept as an explicit proposition. -/
def HasWeakHigherLocalizationUniversalProperty
    (R : RawHigherContextualSystem (Context := Context)) : Prop :=
  Nonempty (WeakHigherLocalizationUniversalProperty (W := W) R)

/-- The genuine weak-localization existence principle that remains open: every
weakly `W`-admissible raw higher system admits the v2.18 universal-property
datum.

This is a proposition, not an axiom and not a theorem proved in this file. -/
def HigherWeakLocalizationUniversalPrinciple : Prop :=
  ∀ R : RawHigherContextualSystem (Context := Context),
    IsHigherWAdmissible W R →
      HasWeakHigherLocalizationUniversalProperty (W := W) R

/-- A v2.18 universal-property datum contains, in particular, the exact v2.10
higher localization factorization data. -/
def higherLocalizationFactorizationOfWeakUniversalProperty
    {R : RawHigherContextualSystem (Context := Context)}
    (U : WeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherLocalizationFactorization (W := W) R :=
  U.chosen

/-- Existence of the stronger v2.18 universal property implies existence of the
v2.10 higher localization factorization. -/
theorem hasHigherLocalizationFactorization_of_hasWeakHigherLocalizationUniversalProperty
    {R : RawHigherContextualSystem (Context := Context)}
    (hU : HasWeakHigherLocalizationUniversalProperty (W := W) R) :
    HasHigherLocalizationFactorization (W := W) R := by
  rcases hU with ⟨U⟩
  exact ⟨U.chosen⟩

/-- Consequently, existence of the v2.18 universal property forces the raw
system to satisfy the exact weak `W`-admissibility condition.  This direction is
unconditional and reuses the v2.16 necessity theorem. -/
theorem hasWeakHigherLocalizationUniversalProperty_isHigherWAdmissible
    {R : RawHigherContextualSystem (Context := Context)}
    (hU : HasWeakHigherLocalizationUniversalProperty (W := W) R) :
    IsHigherWAdmissible W R :=
  hasHigherLocalizationFactorization_isHigherWAdmissible W
    (hasHigherLocalizationFactorization_of_hasWeakHigherLocalizationUniversalProperty
      W hU)

/-- If the still-open v2.18 universal principle is supplied, then the weaker
v2.15 existence principle follows.  This is the formal one-way bridge from the
proposed genuine weak universal property to the already-established v2.10
factorization interface. -/
theorem higherWeakLocalizationExistence_of_universalPrinciple
    (hU : HigherWeakLocalizationUniversalPrinciple (W := W)) :
    HigherWeakLocalizationExistence (W := W) := by
  intro R hR
  exact
    hasHigherLocalizationFactorization_of_hasWeakHigherLocalizationUniversalProperty W
      (hU R hR)

/-- Under the explicitly supplied universal principle, weak `W`-admissibility is
characterized by existence of the v2.18 universal-property datum.  The reverse
direction remains unconditional. -/
theorem higherWAdmissible_iff_hasWeakHigherLocalizationUniversalProperty_of_universalPrinciple
    (hU : HigherWeakLocalizationUniversalPrinciple (W := W))
    (R : RawHigherContextualSystem (Context := Context)) :
    IsHigherWAdmissible W R ↔
      HasWeakHigherLocalizationUniversalProperty (W := W) R := by
  constructor
  · exact hU R
  · exact hasWeakHigherLocalizationUniversalProperty_isHigherWAdmissible W

/-!
The logical boundary after v2.18 is therefore:

```text
HasWeakHigherLocalizationUniversalProperty W R
        ↓                         proved, unconditional
HasHigherLocalizationFactorization W R
        ↓                         proved in v2.16
IsHigherWAdmissible W R

IsHigherWAdmissible W R
        ↓                         OPEN in general
HasWeakHigherLocalizationUniversalProperty W R.
```

Thus the genuine weak-localization route is now represented by a concrete
StrongTrans / modification-level target rather than by an informal appeal to
ordinary localization.  The next theorem unit may either strengthen the
comparison triangle from objectwise natural isomorphisms to a fully coherent
modification-level comma condition, or prove the universal principle on a
nontrivial sufficient subclass.  Neither step is silently assumed here.
-/

end KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
