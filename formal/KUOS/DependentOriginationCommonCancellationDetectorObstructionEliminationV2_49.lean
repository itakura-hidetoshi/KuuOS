import KUOS.DependentOriginationImageEnvelopeThinObstructionEliminationV2_48

namespace KUOS.DependentOriginationCommonCancellationDetectorObstructionEliminationV2_49

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationStageIIIRouteCompletenessV2_33
open KUOS.DependentOriginationWeakCoherentTwoAxisObstructionV2_42
open KUOS.DependentOriginationPointwise2CellRigidityObstructionEliminationV2_47

universe u v uH vH

/-!
# Common cancellation-detector obstruction elimination v2.49

v2.47 shows that the target-side stored-triangle obstruction disappears once
each corresponding component hom set in the exact v2.23 naturality square is a
subsingleton.  v2.48 gives one structural route to that condition by requiring
the full subcategory spanned by the two relevant functor images to be thin.

The present file gives a different route which does not require that image
envelope, or even any nontrivial full subcategory of the target, to be thin.

For Cat 1-morphisms `F G : C ⟶ D`, suppose there is one object `Q : D` and,
for every `Z : C`, an epimorphism

```text
Q ⟶ F.obj Z
```

such that each detector hom `Q ⟶ G.obj Z` is a subsingleton.  Then two maps
`F.obj Z ⟶ G.obj Z` agree after precomposition with the epi, hence agree by
cancellation.  Dually, one common target `Q` equipped with monomorphisms

```text
G.obj Z ⟶ Q
```

and subsingleton detector homs `F.obj Z ⟶ Q` gives the same conclusion by
postcomposition and mono cancellation.

Thus we obtain the genuinely non-thin route

```text
common epi detector OR common mono detector
  -> pointwise component-hom uniqueness                (v2.47)
  -> exact Cat 2-cell hom uniqueness                    (v2.46)
  -> stored modification naturality
  -> weak universality + coherent route completeness
  -> no local v2.42 E/R obstruction.
```

The detector object is common to all components of a fixed naturality square.
This prevents the criterion from degenerating into a tautological choice of
`Q = F.obj Z` or `Q = G.obj Z` separately for every `Z`.

This is a parallel sufficient route to v2.48, not an implication from or to
image-envelope thinness.  No coherent universal-data existence, strictification,
or final global dependent-origination theorem is asserted here.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- A single source object detects all corresponding component homs by epi
precomposition.  The same `Q` must work for every source object `Z`. -/
def CatHom₂CommonEpiDetector
    {C D : Cat.{vH, uH}} (F G : C ⟶ D) : Prop :=
  ∃ (Q : D) (e : ∀ Z : C, Q ⟶ F.obj Z),
    (∀ Z : C, Epi (e Z)) ∧
      ∀ Z : C, Subsingleton (Q ⟶ G.obj Z)

/-- A single target object detects all corresponding component homs by mono
postcomposition.  The same `Q` must work for every source object `Z`. -/
def CatHom₂CommonMonoDetector
    {C D : Cat.{vH, uH}} (F G : C ⟶ D) : Prop :=
  ∃ (Q : D) (m : ∀ Z : C, G.obj Z ⟶ Q),
    (∀ Z : C, Mono (m Z)) ∧
      ∀ Z : C, Subsingleton (F.obj Z ⟶ Q)

/-- Either of the two common cancellation mechanisms is available. -/
def CatHom₂CommonCancellationDetector
    {C D : Cat.{vH, uH}} (F G : C ⟶ D) : Prop :=
  CatHom₂CommonEpiDetector F G ∨ CatHom₂CommonMonoDetector F G

/-- A common epi detector forces the corresponding component homs to be
subsingletons. -/
theorem catHom₂PointwiseSubsingleton_of_commonEpiDetector
    {C D : Cat.{vH, uH}} (F G : C ⟶ D)
    (hDetect : CatHom₂CommonEpiDetector F G) :
    CatHom₂PointwiseSubsingleton F G := by
  rcases hDetect with ⟨Q, e, hepi, hsub⟩
  intro Z
  letI : Epi (e Z) := hepi Z
  constructor
  intro f g
  apply (cancel_epi (e Z)).1
  exact (hsub Z).elim _ _

/-- Dually, a common mono detector forces the corresponding component homs to
be subsingletons. -/
theorem catHom₂PointwiseSubsingleton_of_commonMonoDetector
    {C D : Cat.{vH, uH}} (F G : C ⟶ D)
    (hDetect : CatHom₂CommonMonoDetector F G) :
    CatHom₂PointwiseSubsingleton F G := by
  rcases hDetect with ⟨Q, m, hmono, hsub⟩
  intro Z
  letI : Mono (m Z) := hmono Z
  constructor
  intro f g
  apply (cancel_mono (m Z)).1
  exact (hsub Z).elim _ _

/-- Either common cancellation detector is sufficient for the v2.47 pointwise
rigidity condition. -/
theorem catHom₂PointwiseSubsingleton_of_commonCancellationDetector
    {C D : Cat.{vH, uH}} (F G : C ⟶ D)
    (hDetect : CatHom₂CommonCancellationDetector F G) :
    CatHom₂PointwiseSubsingleton F G := by
  rcases hDetect with hEpi | hMono
  · exact catHom₂PointwiseSubsingleton_of_commonEpiDetector F G hEpi
  · exact catHom₂PointwiseSubsingleton_of_commonMonoDetector F G hMono

/-- For every raw base arrow, the exact pair of Cat 1-morphisms occurring in
the v2.23 stored-triangle naturality square admits a common epi or mono
detector. -/
def StoredV2_18NaturalityCommonCancellationDetector
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K) : Prop :=
  ∀ {X Y : Context} (f : X ⟶ Y),
    CatHom₂CommonCancellationDetector
      ((restrictHigherLocalizedSystem W H.lift).map f.toLoc ≫
        (restrictHigherLocalizedStrongTrans (W := W) alpha.hom ≫
          K.comparison).app (.mk Y))
      (H.comparison.app (.mk X) ≫ R.map f.toLoc)

/-- Common cancellation detection implies the exact pointwise component-hom
rigidity criterion isolated in v2.47. -/
theorem storedV2_18NaturalityComponentHomSubsingleton_of_commonCancellationDetector
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K)
    (hDetect : StoredV2_18NaturalityCommonCancellationDetector
      (W := W) alpha) :
    StoredV2_18NaturalityComponentHomSubsingleton (W := W) alpha := by
  intro X Y f
  exact catHom₂PointwiseSubsingleton_of_commonCancellationDetector
    _ _ (hDetect f)

/-- Uniform common cancellation detection for all v2.18 factors into one
coherent chosen carrier. -/
def HigherStoredV2_18NaturalityCommonCancellationDetector
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∀ (H : HigherLocalizationFactorization (W := W) R)
    (alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),
    StoredV2_18NaturalityCommonCancellationDetector (W := W) alpha

/-- Uniform common cancellation detection implies uniform v2.47 pointwise
rigidity. -/
theorem higherStoredV2_18NaturalityComponentHomSubsingleton_of_commonCancellationDetector
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hDetect : HigherStoredV2_18NaturalityCommonCancellationDetector
      (W := W) U) :
    HigherStoredV2_18NaturalityComponentHomSubsingleton (W := W) U := by
  intro H alpha
  exact
    storedV2_18NaturalityComponentHomSubsingleton_of_commonCancellationDetector
      (W := W) alpha (hDetect H alpha)

/-- Coherent universal data plus common cancellation detection give the v2.18
weak universal property on the same chosen carrier. -/
theorem hasWeakHigherLocalizationUniversalProperty_of_commonCancellationDetector
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hDetect : HigherStoredV2_18NaturalityCommonCancellationDetector
      (W := W) U) :
    HasWeakHigherLocalizationUniversalProperty (W := W) R :=
  hasWeakHigherLocalizationUniversalProperty_of_pointwise2CellRigidity
    (W := W) U
      (higherStoredV2_18NaturalityComponentHomSubsingleton_of_commonCancellationDetector
        (W := W) U hDetect)

/-- The coherent Stage III route obstruction disappears under the same common
cancellation-detection condition. -/
theorem higherCoherentRouteCompleteness_of_commonCancellationDetector
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hDetect : HigherStoredV2_18NaturalityCommonCancellationDetector
      (W := W) U) :
    HigherCoherentRouteCompleteness (W := W) U :=
  higherCoherentRouteCompleteness_of_pointwise2CellRigidity
    (W := W) U
      (higherStoredV2_18NaturalityComponentHomSubsingleton_of_commonCancellationDetector
        (W := W) U hDetect)

/-- Common cancellation detection gives the aligned state in the v2.42 local
classification. -/
theorem higherWeakCoherentAlignment_of_commonCancellationDetector
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hDetect : HigherStoredV2_18NaturalityCommonCancellationDetector
      (W := W) U) :
    HigherWeakCoherentAlignment (W := W) U :=
  ⟨hasWeakHigherLocalizationUniversalProperty_of_commonCancellationDetector
      (W := W) U hDetect,
    higherCoherentRouteCompleteness_of_commonCancellationDetector
      (W := W) U hDetect⟩

/-- Exact local E/R obstruction elimination under a common epi/mono
cancellation detector. -/
theorem no_twoAxisObstruction_of_commonCancellationDetector
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hDetect : HigherStoredV2_18NaturalityCommonCancellationDetector
      (W := W) U) :
    ¬ HigherWeakCoherentTwoAxisObstruction (W := W) U :=
  (higherWeakCoherentAlignment_iff_no_twoAxisObstruction
    (W := W) U).mp
      (higherWeakCoherentAlignment_of_commonCancellationDetector
        (W := W) U hDetect)

end KUOS.DependentOriginationCommonCancellationDetectorObstructionEliminationV2_49
