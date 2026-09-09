import KUOS.DependentOriginationWeakToStrictReductionV2_14

namespace KUOS.DependentOriginationHigherStrictificationPrincipleV2_15

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationStrictHigherLocalizationV2_11
open KUOS.DependentOriginationWeakToStrictReductionV2_14

universe u v uH vH

/-!
# Higher strictification principle and obstruction v2.15

The v2.14 layer proves a precise sufficient reduction:

```text
HasHigherStrictPresentationModel W R
        ⇒
HasHigherLocalizationFactorization W R.
```

The genuinely unresolved step is not hidden here.  It is the passage from the
weak presentation-invariance condition

```text
IsHigherWAdmissible W R
```

(where arrows in `W` are sent only to equivalences of categories) to existence
of a strict presentation model whose underlying ordinary Cat-valued functor
sends `W` to actual isomorphisms in the 1-category `Cat`.

This file names that missing statement as an explicit *principle* rather than
asserting it.  It then proves that the principle is sufficient to discharge the
full weak higher-localization existence obligation.  It also names the exact
objectwise obstruction: a weakly admissible raw system for which no strict
presentation model exists.

No theorem in this file proves that the strictification principle holds.  Thus
no bicategorical localization or pseudofunctor strictification result is being
smuggled in through ordinary localization.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- The full weak higher-localization existence obligation.

This is the theorem one ultimately wants at the presentation-localization layer:
every raw higher system which sends `W` to equivalences of categories admits the
v2.10 higher localization factorization.  It is defined as a proposition here;
its proof is not assumed. -/
def HigherWeakLocalizationExistence : Prop :=
  ∀ R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH),
    IsHigherWAdmissible W R → HasHigherLocalizationFactorization (W := W) R

/-- The explicit strictification principle isolated by v2.14.

It says that every weakly `W`-admissible raw higher system has a strict
presentation model in the exact sense of v2.14.  This proposition is *not*
proved globally in the present development. -/
def HigherStrictificationPrinciple : Prop :=
  ∀ R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH),
    IsHigherWAdmissible W R → HasHigherStrictPresentationModel (W := W) R

/-- The exact objectwise obstruction to the v2.14 strictification route:
weak `W`-admissibility together with failure of existence of a strict
presentation model. -/
def HigherStrictificationObstruction
    (R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)) : Prop :=
  IsHigherWAdmissible W R ∧ ¬ HasHigherStrictPresentationModel (W := W) R

/-- If the strictification principle is supplied, the full weak
higher-localization existence obligation follows from v2.14. -/
theorem weakLocalizationExistence_of_strictificationPrinciple
    (hstrict : HigherStrictificationPrinciple (W := W) (uH := uH) (vH := vH)) :
    HigherWeakLocalizationExistence (W := W) (uH := uH) (vH := vH) := by
  intro R hR
  exact
    hasHigherLocalizationFactorization_of_strictPresentationModel W
      (hstrict R hR)

/-- A global strictification principle rules out every objectwise
strictification obstruction. -/
theorem no_strictificationObstruction_of_principle
    (hstrict : HigherStrictificationPrinciple (W := W) (uH := uH) (vH := vH))
    (R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)) :
    ¬ HigherStrictificationObstruction (W := W) R := by
  intro hobs
  exact hobs.2 (hstrict R hobs.1)

/-- Conversely at the level of explicit evidence, weak admissibility plus a
proof that no strict presentation model exists is precisely an obstruction. -/
theorem strictificationObstruction_of_failure
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (hR : IsHigherWAdmissible W R)
    (hfail : ¬ HasHigherStrictPresentationModel (W := W) R) :
    HigherStrictificationObstruction (W := W) R :=
  ⟨hR, hfail⟩

/-- The already-strict Cat-valued sector cannot exhibit the v2.15 obstruction,
because v2.14 provides its strict presentation model tautologically. -/
theorem strictSector_has_no_strictificationObstruction
    (G : Context ⥤ Cat.{vH, uH})
    (hG : W.IsInvertedBy G) :
    ¬ HigherStrictificationObstruction (W := W)
      (strictRawHigherSystem (uH := uH) (vH := vH) G) := by
  intro hobs
  exact hobs.2 (strictSector_hasHigherStrictPresentationModel W G hG)

/-- The strict sector also satisfies the weak admissibility condition, so it lies
inside the intended domain of the weak theorem rather than merely beside it. -/
theorem strictSector_isHigherWAdmissible
    (G : Context ⥤ Cat.{vH, uH})
    (hG : W.IsInvertedBy G) :
    IsHigherWAdmissible W
      (strictRawHigherSystem (uH := uH) (vH := vH) G) :=
  strictRawHigherSystem_isHigherWAdmissible W G hG

/-!
The formal dependency after v2.15 is therefore:

```text
IsHigherWAdmissible W R
        ↓
[UNRESOLVED: HigherStrictificationPrinciple]
        ↓
HasHigherStrictPresentationModel W R
        ↓  (v2.14, proved)
HasHigherLocalizationFactorization W R.
```

Equivalently, the strictification route can fail only at an explicitly named
objectwise obstruction

```text
IsHigherWAdmissible W R
∧
¬ HasHigherStrictPresentationModel W R.
```

This is a boundary theorem, not a solution of the boundary.  Future work must
either prove `HigherStrictificationPrinciple` under justified hypotheses or
construct a genuine bicategorical localization theorem that bypasses it.
-/

end KUOS.DependentOriginationHigherStrictificationPrincipleV2_15
