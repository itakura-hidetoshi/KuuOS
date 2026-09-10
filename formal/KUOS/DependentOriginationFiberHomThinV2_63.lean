import Mathlib.CategoryTheory.Thin
import KUOS.DependentOriginationFiberFunctorTwoThinV2_62

namespace KUOS.DependentOriginationFiberHomThinV2_63

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationCoherentComparisonFactorizationV2_60
open KUOS.DependentOriginationFiberFunctorTwoThinV2_62

universe u v uH vH

/-!
# Fiber-hom thin sufficient sector v2.63

Version 2.62 proves that weak `W`-admissibility yields a genuine higher
localization factorization whenever the relevant Cat-valued functor hom-categories
are 2-thin.  This file derives that hypothesis from a simpler and more intrinsic
condition on the fibers themselves.

A raw higher contextual system is *fiber-hom thin* when every image fiber category
has at most one morphism between any fixed pair of objects.  Mathlib already proves
that if a target category is thin, then every functor category into that target is
thin.  Hence for any two context objects `X,Y`, the functor category

```text
R.obj X ⥤ R.obj Y
```

is thin as soon as the target fiber `R.obj Y` is thin.  Passing through the small
wrapper `Cat.Hom₂` therefore gives exactly `IsFiberFunctorTwoThin R` from v2.62.

This produces a practically useful sufficient theorem for preorder/poset-like
fibers while keeping the unrestricted general-`W` boundary unchanged.  No
2-dimensional coherence is manufactured by choice: it is forced uniquely by
thinness of the target fibers.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Every fiber category in the image of `R` is thin: for any two objects in a
fixed fiber there is at most one morphism between them. -/
def IsFiberHomThin
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)) : Prop :=
  ∀ X : Context, Quiver.IsThin (R.obj (.mk X))

/-- Fiber-hom thinness implies the v2.62 fiber-functor 2-thinness condition.

For fixed `X,Y`, Mathlib's `CategoryTheory.functor_thin` instance makes the
functor category `R.obj X ⥤ R.obj Y` thin from thinness of the target `R.obj Y`.
A 2-cell in `Cat` is a wrapper around a natural transformation, so
`Cat.Hom₂.ext` transports that uniqueness to the Cat hom-category. -/
theorem isFiberFunctorTwoThin_of_fiberHomThin
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (hthin : IsFiberHomThin R) :
    IsFiberFunctorTwoThin R := by
  intro X Y F G η θ
  letI : Quiver.IsThin (R.obj (.mk Y)) := hthin Y
  apply Cat.Hom₂.ext
  exact Subsingleton.elim _ _

/-- Consequently, pointwise adjoint-equivalence data together with thin image
fibers already supplies the complete five-law coherent general-`W` package. -/
theorem hasCoherentGeneralWFactorizationData_of_fiberHomThin
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hthin : IsFiberHomThin R) :
    HasCoherentGeneralWFactorizationData W R D :=
  hasCoherentGeneralWFactorizationData_of_fiberFunctorTwoThin
    W R D (isFiberFunctorTwoThin_of_fiberHomThin R hthin)

/-- Fiber-hom thinness and pointwise adjoint-equivalence data therefore yield an
actual v2.10 higher-localization factorization. -/
theorem hasHigherLocalizationFactorization_of_fiberHomThin
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hthin : IsFiberHomThin R) :
    HasHigherLocalizationFactorization (W := W) R :=
  hasHigherLocalizationFactorization_of_fiberFunctorTwoThin
    W R D (isFiberFunctorTwoThin_of_fiberHomThin R hthin)

/-- Main v2.63 theorem: weak `W`-admissibility plus thin image fibers is enough
for the genuine general-`W` higher-localization factorization.

Weak admissibility supplies the pointwise adjoint equivalences by v2.56; fiber
thinness implies functor 2-thinness by the theorem above; v2.62 then closes all
five coherence laws and constructs the factorization. -/
theorem hasHigherLocalizationFactorization_of_admissible_and_fiberHomThin
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (hR : IsHigherWAdmissible W R)
    (hthin : IsFiberHomThin R) :
    HasHigherLocalizationFactorization (W := W) R :=
  hasHigherLocalizationFactorization_of_admissible_and_fiberFunctorTwoThin
    W hR (isFiberFunctorTwoThin_of_fiberHomThin R hthin)

/-!
## Boundary fixed by v2.63

The sufficient chain is now

```text
IsFiberHomThin R
      ↓  Mathlib functor_thin + Cat.Hom₂.ext
IsFiberFunctorTwoThin R
      ↓  v2.62
all five quotient/comparison coherence equations are forced
      ↓
HigherLocalizationFactorization W R.
```

Together with weak admissibility:

```text
IsHigherWAdmissible W R
+ IsFiberHomThin R
        ↓
HasHigherLocalizationFactorization W R.
```

This is stronger in usability than v2.62 because the hypothesis is internal to
each fiber category rather than quantified over all functors between fibers.
It applies in particular whenever the image fibers are thin categories, such as
categories arising from preorder-like semantics.

The unrestricted theorem without a thinness hypothesis remains open.  Removing
thinness still requires a genuine construction of coherent relation transports
(or an equivalent strictification/bicategorical localization theorem).  No
`Classical.choice` coherence principle, new axiom, `sorry`, or `admit` is used.
-/

end KUOS.DependentOriginationFiberHomThinV2_63
