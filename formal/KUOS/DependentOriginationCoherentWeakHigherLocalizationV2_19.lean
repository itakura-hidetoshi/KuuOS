import Mathlib.CategoryTheory.Bicategory.FunctorBicategory.Pseudo
import KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18

namespace KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationHigherStrictificationPrincipleV2_15
open KUOS.DependentOriginationHigherLocalizationNecessityV2_16
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18

open scoped CategoryTheory.Pseudofunctor.StrongTrans

universe u v uH vH

/-!
# Coherent weak higher presentation localization v2.19

The v2.18 interface isolates a genuine weak higher localization universal-property
candidate.  Its factor maps are StrongTrans, and essential uniqueness is already
expressed by invertible modifications, but the comparison triangle is only stored
objectwise as a natural isomorphism of functors.

This file tightens that interface by one categorical level without asserting the
still-open existence theorem.

The first step is to construct the actual restriction of a StrongTrans along the
presentation unit

```text
Context --Q--> HigherLocalizedSite(W)^op.
```

The resulting StrongTrans lives between the restricted pseudofunctors used in
v2.10.  A coherent factor morphism can therefore require the whole triangle

```text
restrict(H.lift) --restrict(alpha)--> restrict(K.lift)
       |                                  |
 H.comparison                         K.comparison
       |                                  |
       +---------------> R <--------------+
```

to commute up to an invertible **modification**, rather than merely objectwise
up to unrelated natural isomorphisms.

No existence of such coherent factor morphisms is proved here.  In particular,
this theorem unit does not identify ordinary 1-categorical localization with the
required bicategorical localization, does not strictify equivalences of categories
to isomorphisms, and does not assert the global weak localization principle.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Restrict a StrongTrans between localized Cat-valued pseudofunctors along the
canonical higher presentation unit.

Because pseudofunctor composition is definitionally objectwise on objects and
1-morphisms, the component and pseudonaturality isomorphism are inherited from
`alpha`; the remaining coherence obligations are discharged by the bicategorical
coherence tactic built into the `StrongTrans` structure defaults. -/
def restrictHigherLocalizedStrongTrans
    {F G : HigherLocalizedDescentSystem (W := W)}
    (alpha : F ⟶ G) :
    restrictHigherLocalizedSystem W F ⟶ restrictHigherLocalizedSystem W G where
  app X :=
    alpha.app ((higherPresentationUnitFunctor W).toPseudofunctor.obj X)
  naturality f :=
    alpha.naturality ((higherPresentationUnitFunctor W).toPseudofunctor.map f)

/-- On a raw context object, restriction of a StrongTrans has exactly the
component of the original StrongTrans at the image of the presentation unit. -/
@[simp] theorem restrictHigherLocalizedStrongTrans_app
    {F G : HigherLocalizedDescentSystem (W := W)}
    (alpha : F ⟶ G) (X : Context) :
    (restrictHigherLocalizedStrongTrans (W := W) alpha).app (.mk X) =
      alpha.app (.mk ((higherPresentationUnitFunctor W).obj X)) := by
  rfl

/-- A factor morphism whose comparison triangle is coherent at the StrongTrans
level.

The field `comparison_triangle` is an isomorphism in the hom-category of
StrongTrans, hence an invertible modification.  This is strictly stronger data
than the objectwise natural-isomorphism triangle used in v2.18. -/
structure CoherentHigherLocalizationFactorMorphism
    {R : RawHigherContextualSystem (Context := Context)}
    (H K : HigherLocalizationFactorization (W := W) R) where
  /-- Strong factor map between localized lifts. -/
  hom : H.lift ⟶ K.lift
  /-- Fully pseudonatural comparison triangle, encoded as an invertible
  modification between StrongTrans. -/
  comparison_triangle :
    (restrictHigherLocalizedStrongTrans (W := W) hom ≫ K.comparison) ≅ H.comparison

/-- Coherent weak higher localization universal-property datum for one raw
Cat-valued contextual system.

The chosen factorization and existence of factors parallel v2.18, but every factor
now carries a modification-level comparison triangle.  Essential uniqueness is
again expressed by an invertible modification between the underlying StrongTrans
factor maps. -/
structure CoherentWeakHigherLocalizationUniversalProperty
    (R : RawHigherContextualSystem (Context := Context)) where
  /-- Chosen weak higher localization factorization. -/
  chosen : HigherLocalizationFactorization (W := W) R
  /-- Every competing factorization admits a coherently comparison-preserving
  StrongTrans into the chosen factorization. -/
  factor :
    ∀ H : HigherLocalizationFactorization (W := W) R,
      Nonempty (CoherentHigherLocalizationFactorMorphism (W := W) H chosen)
  /-- Essential uniqueness of coherent factor maps up to invertible modification
  of their underlying StrongTrans. -/
  essential_unique :
    ∀ (H : HigherLocalizationFactorization (W := W) R)
      (alpha beta : CoherentHigherLocalizationFactorMorphism (W := W) H chosen),
      Nonempty (alpha.hom ≅ beta.hom)

/-- Existence of the coherent v2.19 universal-property datum remains an explicit
proposition. -/
def HasCoherentWeakHigherLocalizationUniversalProperty
    (R : RawHigherContextualSystem (Context := Context)) : Prop :=
  Nonempty (CoherentWeakHigherLocalizationUniversalProperty (W := W) R)

/-- The global coherent weak-localization principle that remains open in general.
It is deliberately a proposition rather than an axiom or theorem of this file. -/
def CoherentHigherWeakLocalizationUniversalPrinciple : Prop :=
  ∀ R : RawHigherContextualSystem (Context := Context),
    IsHigherWAdmissible W R →
      HasCoherentWeakHigherLocalizationUniversalProperty (W := W) R

/-- A coherent universal-property datum contains a v2.10 higher localization
factorization. -/
def higherLocalizationFactorizationOfCoherentWeakUniversalProperty
    {R : RawHigherContextualSystem (Context := Context)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherLocalizationFactorization (W := W) R :=
  U.chosen

/-- Existence of the coherent v2.19 universal property implies existence of the
v2.10 higher localization factorization. -/
theorem hasHigherLocalizationFactorization_of_hasCoherentWeakHigherLocalizationUniversalProperty
    {R : RawHigherContextualSystem (Context := Context)}
    (hU : HasCoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HasHigherLocalizationFactorization (W := W) R := by
  rcases hU with ⟨U⟩
  exact ⟨U.chosen⟩

/-- Consequently, coherent weak higher-localization universal data force the exact
weak `W`-admissibility predicate from v2.10. -/
theorem hasCoherentWeakHigherLocalizationUniversalProperty_isHigherWAdmissible
    {R : RawHigherContextualSystem (Context := Context)}
    (hU : HasCoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    IsHigherWAdmissible W R :=
  hasHigherLocalizationFactorization_isHigherWAdmissible W
    (hasHigherLocalizationFactorization_of_hasCoherentWeakHigherLocalizationUniversalProperty
      W hU)

/-- Supplying the still-open coherent universal principle is enough to recover the
weaker v2.15 higher localization existence principle. -/
theorem higherWeakLocalizationExistence_of_coherentUniversalPrinciple
    (hU : CoherentHigherWeakLocalizationUniversalPrinciple (W := W)) :
    HigherWeakLocalizationExistence (W := W) := by
  intro R hR
  exact
    hasHigherLocalizationFactorization_of_hasCoherentWeakHigherLocalizationUniversalProperty W
      (hU R hR)

/-- Under an explicitly supplied coherent universal principle, weak
`W`-admissibility is characterized by existence of coherent universal data. -/
theorem higherWAdmissible_iff_hasCoherentWeakHigherLocalizationUniversalProperty_of_principle
    (hU : CoherentHigherWeakLocalizationUniversalPrinciple (W := W))
    (R : RawHigherContextualSystem (Context := Context)) :
    IsHigherWAdmissible W R ↔
      HasCoherentWeakHigherLocalizationUniversalProperty (W := W) R := by
  constructor
  · exact hU R
  · exact hasCoherentWeakHigherLocalizationUniversalProperty_isHigherWAdmissible W

/-!
The logical boundary after v2.19 is therefore

```text
HasCoherentWeakHigherLocalizationUniversalProperty W R
        ↓                                  proved, unconditional
HasHigherLocalizationFactorization W R
        ↓                                  proved in v2.16
IsHigherWAdmissible W R

IsHigherWAdmissible W R
        ↓                                  OPEN in general
HasCoherentWeakHigherLocalizationUniversalProperty W R.
```

Unlike v2.18, the comparison triangle is now represented at the modification level.
What remains genuinely open is existence of this coherent universal datum for every
weakly `W`-admissible raw pseudofunctor, or a mathematically justified sufficient
subclass on which that existence can be proved.
-/

end KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
