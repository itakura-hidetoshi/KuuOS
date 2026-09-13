import Mathlib.CategoryTheory.Bicategory.FunctorBicategory.Pseudo
import KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18

namespace KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19

open CategoryTheory
open KUOS.DependentOriginationHigherStackDescentV2_8
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

Universe bookkeeping follows the same four-level discipline as v2.18.  The
source category contributes `u` and `v`, while the target `Cat.{vH, uH}`
contributes `uH` and `vH`.  Consequently both
`HigherLocalizedDescentSystem` and `RawHigherContextualSystem` are instantiated
with universe application syntax `.{u, v, uH, vH}`; `uH` and `vH` are not
term-level named arguments.  The localized descent abbreviation itself lives in
the v2.8 namespace, so that namespace must also be in scope before applying
explicit universe parameters; otherwise Lean's auto-implicit mechanism may treat
an unresolved identifier as a local variable, producing misleading downstream
universe and field-notation errors.  In contrast, `W` is genuine localization
data and is retained as `(W := W)` exactly for declarations whose types depend on
the presentation localization.

There is a second, independent coherence issue at the StrongTrans level.  After
precomposition by the presentation pseudofunctor, the component and the
1-morphism naturality isomorphism are inherited from `alpha`, but the identity
and composition axioms are not definitionally the original axioms: the
`Pseudofunctor.comp` mapId and mapComp contain the image of the presentation
pseudofunctor's own mapId and mapComp constraints.  The restricted StrongTrans
therefore transports coherence in two stages.  Since `Cat` deliberately wraps
2-morphisms in `Cat.Hom₂`, generic bicategorical rewriting need not see a
composite 2-cell through whiskering even when the pretty-printer displays that
composite.  We therefore cross the wrapper boundary explicitly with
`Cat.Hom₂.ext`, transport the StrongTrans coherence laws to the underlying
natural transformations, and split the concrete presentation mapId or mapComp
composite there using ordinary functor-whiskering functoriality.  The inner
presentation constraint is then transported by `alpha.naturality_naturality`,
after which `alpha.naturality_id` or `alpha.naturality_comp` handles the outer
constraint.  This preserves the two-stage pseudonatural precomposition argument
without relying on rewrite matching through the `Cat.Hom₂` representation layer.

No existence of such coherent factor morphisms is proved here.  In particular,
this theorem unit does not identify ordinary 1-categorical localization with the
required bicategorical localization, does not strictify equivalences of categories
to isomorphisms, and does not assert the global weak localization principle.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Restrict a StrongTrans between localized Cat-valued pseudofunctors along the
canonical higher presentation unit.

This is pseudonatural precomposition by the presentation pseudofunctor.  The
localization functor is noncomputable, so the induced restricted transformation
is noncomputable as well. -/
noncomputable def restrictHigherLocalizedStrongTrans
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (alpha : F ⟶ G) :
    restrictHigherLocalizedSystem W F ⟶ restrictHigherLocalizedSystem W G where
  app X :=
    alpha.app ((higherPresentationUnitFunctor W).toPseudofunctor.obj X)
  naturality f :=
    alpha.naturality ((higherPresentationUnitFunctor W).toPseudofunctor.map f)
  naturality_naturality η := by
    simpa [restrictHigherLocalizedSystem] using
      alpha.naturality_naturality
        ((higherPresentationUnitFunctor W).toPseudofunctor.map₂ η)
  naturality_id a := by
    let P := (higherPresentationUnitFunctor W).toPseudofunctor
    have hnat := congrArg Cat.Hom₂.toNatTrans
      (alpha.naturality_naturality (P.mapId a).hom)
    have hid := congrArg Cat.Hom₂.toNatTrans
      (alpha.naturality_id (P.obj a))
    apply Cat.Hom₂.ext
    dsimp [P, restrictHigherLocalizedSystem, Pseudofunctor.comp] at hnat hid ⊢
    simp only [Cat.Hom.toNatTrans_comp, Cat.whiskerLeft_toNatTrans,
      Cat.whiskerRight_toNatTrans, Functor.whiskerLeft_comp,
      Functor.whiskerRight_comp] at hnat hid ⊢
    rw [← Category.assoc, ← hnat]
    rw [Category.assoc, hid]
    simp only [Category.assoc]
  naturality_comp {a b c} f g := by
    let P := (higherPresentationUnitFunctor W).toPseudofunctor
    have hnat := congrArg Cat.Hom₂.toNatTrans
      (alpha.naturality_naturality (P.mapComp f g).hom)
    have hcomp := congrArg Cat.Hom₂.toNatTrans
      (alpha.naturality_comp (P.map f) (P.map g))
    apply Cat.Hom₂.ext
    dsimp [P, restrictHigherLocalizedSystem, Pseudofunctor.comp] at hnat hcomp ⊢
    simp only [Cat.Hom.toNatTrans_comp, Cat.whiskerLeft_toNatTrans,
      Cat.whiskerRight_toNatTrans, Functor.whiskerLeft_comp,
      Functor.whiskerRight_comp] at hnat hcomp ⊢
    rw [← Category.assoc, ← hnat]
    rw [Category.assoc, hcomp]
    simp only [Category.assoc]

/-- On a raw context object, restriction of a StrongTrans has exactly the
component of the original StrongTrans at the image of the presentation unit. -/
@[simp] theorem restrictHigherLocalizedStrongTrans_app
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
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
    {R : RawHigherContextualSystem.{u, v, uH, vH} (Context := Context)}
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
    (R : RawHigherContextualSystem.{u, v, uH, vH} (Context := Context)) where
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
    (R : RawHigherContextualSystem.{u, v, uH, vH} (Context := Context)) : Prop :=
  Nonempty (CoherentWeakHigherLocalizationUniversalProperty (W := W) R)

/-- The global coherent weak-localization principle that remains open in general.
It is deliberately a proposition rather than an axiom or theorem of this file. -/
def CoherentHigherWeakLocalizationUniversalPrinciple : Prop :=
  ∀ R : RawHigherContextualSystem.{u, v, uH, vH} (Context := Context),
    IsHigherWAdmissible W R →
      HasCoherentWeakHigherLocalizationUniversalProperty (W := W) R

/-- A coherent universal-property datum contains a v2.10 higher localization
factorization. -/
def higherLocalizationFactorizationOfCoherentWeakUniversalProperty
    {R : RawHigherContextualSystem.{u, v, uH, vH} (Context := Context)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherLocalizationFactorization (W := W) R :=
  U.chosen

/-- Existence of the coherent v2.19 universal property implies existence of the
v2.10 higher localization factorization. -/
theorem hasHigherLocalizationFactorization_of_hasCoherentWeakHigherLocalizationUniversalProperty
    {R : RawHigherContextualSystem.{u, v, uH, vH} (Context := Context)}
    (hU : HasCoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HasHigherLocalizationFactorization (W := W) R := by
  rcases hU with ⟨U⟩
  exact ⟨U.chosen⟩

/-- Consequently, coherent weak higher-localization universal data force the exact
weak `W`-admissibility predicate from v2.10. -/
theorem hasCoherentWeakHigherLocalizationUniversalProperty_isHigherWAdmissible
    {R : RawHigherContextualSystem.{u, v, uH, vH} (Context := Context)}
    (hU : HasCoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    IsHigherWAdmissible W R :=
  hasHigherLocalizationFactorization_isHigherWAdmissible W
    (hasHigherLocalizationFactorization_of_hasCoherentWeakHigherLocalizationUniversalProperty
      W hU)

/-- Supplying the still-open coherent universal principle is enough to recover the
weaker v2.15 higher localization existence principle. -/
theorem higherWeakLocalizationExistence_of_coherentUniversalPrinciple
    (hU : CoherentHigherWeakLocalizationUniversalPrinciple.{u, v, uH, vH}
      (W := W)) :
    HigherWeakLocalizationExistence.{u, v, uH, vH} (W := W) := by
  intro R hR
  exact
    hasHigherLocalizationFactorization_of_hasCoherentWeakHigherLocalizationUniversalProperty W
      (hU R hR)

/-- Under an explicitly supplied coherent universal principle, weak
`W`-admissibility is characterized by existence of coherent universal data. -/
theorem higherWAdmissible_iff_hasCoherentWeakHigherLocalizationUniversalProperty_of_principle
    (hU : CoherentHigherWeakLocalizationUniversalPrinciple.{u, v, uH, vH}
      (W := W))
    (R : RawHigherContextualSystem.{u, v, uH, vH} (Context := Context)) :
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
