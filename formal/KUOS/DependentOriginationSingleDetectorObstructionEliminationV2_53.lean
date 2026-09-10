import Mathlib.CategoryTheory.Generator.Basic
import KUOS.DependentOriginationSingleSeparatorObstructionEliminationV2_52

namespace KUOS.DependentOriginationSingleDetectorObstructionEliminationV2_53

open CategoryTheory
open CategoryTheory.Limits
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationStageIIIRouteCompletenessV2_33
open KUOS.DependentOriginationWeakCoherentTwoAxisObstructionV2_42
open KUOS.DependentOriginationPointwise2CellRigidityObstructionEliminationV2_47
open KUOS.DependentOriginationSingleSeparatorObstructionEliminationV2_52

universe u v uH vH

/-!
# Single-detector obstruction elimination v2.53

v2.52 eliminates the local v2.42 E/R obstruction when each relevant stored
naturality square admits a single separator or coseparator object with the
corresponding probe homs subsingleton.

Mathlib provides a weaker-looking but standard route to those singleton
separation hypotheses.  A detector object only asks that its covariant Hom
functor reflect isomorphisms.  In a category with equalizers, Mathlib proves

```text
IsDetector S -> IsSeparator S.
```

Dually, in a category with coequalizers,

```text
IsCodetector S -> IsCoseparator S.
```

The present file transports these exact Mathlib theorems into the stored
higher-localization setting.  On the target-detector side we assume that every
raw target fiber has equalizers and that every stored naturality square admits
a detector `S` whose maps into the target components are subsingletons.  On the
dual side we assume coequalizers and a codetector receiving unique maps from
the source components.

Thus the route is

```text
single detector + target-fiber equalizers
  -> single separator                               (Mathlib)
  -> singleton separator rigidity                   (v2.52)
  -> pointwise component-hom uniqueness             (v2.47)
  -> exact Cat 2-cell hom uniqueness                (v2.46)
  -> stored modification naturality
  -> weak universality + coherent route completeness
  -> no local v2.42 E/R obstruction,
```

with the coequalizer/codetector route dual to it.

The equalizer/coequalizer hypotheses are essential to the bridge used here:
this file does not claim that a detector is a separator in an arbitrary
category.  It proves no existence theorem for detectors, limits, coherent
universal data, strictification, or higher localizations, and no final global
dependent-origination theorem.  No implication to or from the v2.49 ordinary
epi detector route or v2.51 effective-epi-family route is asserted.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- A single detector object whose homs into all target components of `G` are
subsingletons.  Equalizers are not included in this predicate; they are an
ambient structural hypothesis when the detector is converted to a separator. -/
def CatHom₂DetectorTargetObject
    {C D : Cat.{vH, uH}} (G : C ⟶ D) : Prop :=
  ∃ S : D, IsDetector S ∧
    ∀ Z : C, Subsingleton (S ⟶ G.obj Z)

/-- Dually, a single codetector receiving unique maps from all source
components of `F`. -/
def CatHom₂CodetectorSourceObject
    {C D : Cat.{vH, uH}} (F : C ⟶ D) : Prop :=
  ∃ S : D, IsCodetector S ∧
    ∀ Z : C, Subsingleton (F.obj Z ⟶ S)

/-- In a target category with equalizers, Mathlib upgrades a detector to a
separator, giving exactly the v2.52 target-object hypothesis. -/
theorem separatorTargetObject_of_detectorTargetObject
    {C D : Cat.{vH, uH}} [HasEqualizers D] (G : C ⟶ D)
    (hObj : CatHom₂DetectorTargetObject G) :
    CatHom₂SeparatorTargetObject G := by
  rcases hObj with ⟨S, hDetect, hSub⟩
  exact ⟨S, IsDetector.isSeparator hDetect, hSub⟩

/-- Dually, coequalizers upgrade a codetector to a coseparator. -/
theorem coseparatorSourceObject_of_codetectorSourceObject
    {C D : Cat.{vH, uH}} [HasCoequalizers D] (F : C ⟶ D)
    (hObj : CatHom₂CodetectorSourceObject F) :
    CatHom₂CoseparatorSourceObject F := by
  rcases hObj with ⟨S, hDetect, hSub⟩
  exact ⟨S, IsCodetector.isCoseparator hDetect, hSub⟩

/-- A target detector plus equalizers forces the exact v2.47 component-hom
subsingleton criterion. -/
theorem catHom₂PointwiseSubsingleton_of_detectorTargetObject
    {C D : Cat.{vH, uH}} [HasEqualizers D] (F G : C ⟶ D)
    (hObj : CatHom₂DetectorTargetObject G) :
    CatHom₂PointwiseSubsingleton F G :=
  catHom₂PointwiseSubsingleton_of_singleSeparatorRigidity
    F G (Or.inl (separatorTargetObject_of_detectorTargetObject G hObj))

/-- A source codetector plus coequalizers gives the dual v2.47 criterion. -/
theorem catHom₂PointwiseSubsingleton_of_codetectorSourceObject
    {C D : Cat.{vH, uH}} [HasCoequalizers D] (F G : C ⟶ D)
    (hObj : CatHom₂CodetectorSourceObject F) :
    CatHom₂PointwiseSubsingleton F G :=
  catHom₂PointwiseSubsingleton_of_singleSeparatorRigidity
    F G (Or.inr (coseparatorSourceObject_of_codetectorSourceObject F hObj))

/-- Every raw target fiber has equalizers. -/
def HigherRawFiberHasEqualizers
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)) : Prop :=
  ∀ X : Context, HasEqualizers (R.obj (.mk X))

/-- Every raw target fiber has coequalizers. -/
def HigherRawFiberHasCoequalizers
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)) : Prop :=
  ∀ X : Context, HasCoequalizers (R.obj (.mk X))

/-- For every raw base arrow, the target Cat 1-morphism in the stored
naturality square admits a detector with unique probe maps into every target
component. -/
def StoredV2_18NaturalityDetectorTargetObject
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K) : Prop :=
  ∀ {X Y : Context} (f : X ⟶ Y),
    CatHom₂DetectorTargetObject
      (H.comparison.app (.mk X) ≫ R.map f.toLoc)

/-- Dually, for every raw base arrow the source Cat 1-morphism in the stored
naturality square admits a codetector receiving unique maps from every source
component. -/
def StoredV2_18NaturalityCodetectorSourceObject
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K) : Prop :=
  ∀ {X Y : Context} (f : X ⟶ Y),
    CatHom₂CodetectorSourceObject
      ((restrictHigherLocalizedSystem W H.lift).map f.toLoc ≫
        (restrictHigherLocalizedStrongTrans (W := W) alpha.hom ≫
          K.comparison).app (.mk Y))

/-- Fiberwise equalizers plus a detector on every stored target side give the
v2.52 stored singleton-separator rigidity condition. -/
theorem storedV2_18NaturalitySingleSeparatorRigidity_of_detectorTargetObject
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K)
    (hEq : HigherRawFiberHasEqualizers R)
    (hDetect : StoredV2_18NaturalityDetectorTargetObject
      (W := W) alpha) :
    StoredV2_18NaturalitySingleSeparatorRigidity (W := W) alpha := by
  intro X Y f
  letI : HasEqualizers (R.obj (.mk Y)) := hEq Y
  exact Or.inl
    (separatorTargetObject_of_detectorTargetObject _ (hDetect f))

/-- Fiberwise coequalizers plus stored source codetectors give the dual v2.52
criterion. -/
theorem storedV2_18NaturalitySingleSeparatorRigidity_of_codetectorSourceObject
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K)
    (hCoeq : HigherRawFiberHasCoequalizers R)
    (hDetect : StoredV2_18NaturalityCodetectorSourceObject
      (W := W) alpha) :
    StoredV2_18NaturalitySingleSeparatorRigidity (W := W) alpha := by
  intro X Y f
  letI : HasCoequalizers (R.obj (.mk Y)) := hCoeq Y
  exact Or.inr
    (coseparatorSourceObject_of_codetectorSourceObject _ (hDetect f))

/-- Uniform stored target-detector rigidity for every factor into one coherent
chosen carrier. -/
def HigherStoredV2_18NaturalityDetectorTargetObject
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∀ (H : HigherLocalizationFactorization (W := W) R)
    (alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),
    StoredV2_18NaturalityDetectorTargetObject (W := W) alpha

/-- Uniform stored source-codetector rigidity for every factor into the same
chosen carrier. -/
def HigherStoredV2_18NaturalityCodetectorSourceObject
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∀ (H : HigherLocalizationFactorization (W := W) R)
    (alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),
    StoredV2_18NaturalityCodetectorSourceObject (W := W) alpha

/-- The two structurally valid singleton-detector routes.  One chooses either
fiberwise equalizers together with uniform target detectors, or fiberwise
coequalizers together with uniform source codetectors. -/
def HigherStoredV2_18NaturalitySingleDetectorLimitRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  (HigherRawFiberHasEqualizers R ∧
      HigherStoredV2_18NaturalityDetectorTargetObject (W := W) U) ∨
    (HigherRawFiberHasCoequalizers R ∧
      HigherStoredV2_18NaturalityCodetectorSourceObject (W := W) U)

/-- Either detector/limit route gives the uniform v2.52 singleton-separator
criterion on the same chosen carrier. -/
theorem higherStoredV2_18NaturalitySingleSeparatorRigidity_of_singleDetectorLimitRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hDetect : HigherStoredV2_18NaturalitySingleDetectorLimitRigidity
      (W := W) U) :
    HigherStoredV2_18NaturalitySingleSeparatorRigidity (W := W) U := by
  rcases hDetect with ⟨hEq, hTarget⟩ | ⟨hCoeq, hSource⟩
  · intro H alpha
    exact storedV2_18NaturalitySingleSeparatorRigidity_of_detectorTargetObject
      (W := W) alpha hEq (hTarget H alpha)
  · intro H alpha
    exact storedV2_18NaturalitySingleSeparatorRigidity_of_codetectorSourceObject
      (W := W) alpha hCoeq (hSource H alpha)

/-- The detector/limit route therefore supplies the uniform v2.47 pointwise
component-hom criterion. -/
theorem higherStoredV2_18NaturalityComponentHomSubsingleton_of_singleDetectorLimitRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hDetect : HigherStoredV2_18NaturalitySingleDetectorLimitRigidity
      (W := W) U) :
    HigherStoredV2_18NaturalityComponentHomSubsingleton (W := W) U :=
  higherStoredV2_18NaturalityComponentHomSubsingleton_of_singleSeparatorRigidity
    (W := W) U
      (higherStoredV2_18NaturalitySingleSeparatorRigidity_of_singleDetectorLimitRigidity
        (W := W) U hDetect)

/-- Coherent universal data plus the detector/limit rigidity hypothesis give
the v2.18 weak universal property on the same chosen carrier. -/
theorem hasWeakHigherLocalizationUniversalProperty_of_singleDetectorLimitRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hDetect : HigherStoredV2_18NaturalitySingleDetectorLimitRigidity
      (W := W) U) :
    HasWeakHigherLocalizationUniversalProperty (W := W) R :=
  hasWeakHigherLocalizationUniversalProperty_of_singleSeparatorRigidity
    (W := W) U
      (higherStoredV2_18NaturalitySingleSeparatorRigidity_of_singleDetectorLimitRigidity
        (W := W) U hDetect)

/-- The coherent Stage III route obstruction disappears under the same
single-detector/limit condition. -/
theorem higherCoherentRouteCompleteness_of_singleDetectorLimitRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hDetect : HigherStoredV2_18NaturalitySingleDetectorLimitRigidity
      (W := W) U) :
    HigherCoherentRouteCompleteness (W := W) U :=
  higherCoherentRouteCompleteness_of_singleSeparatorRigidity
    (W := W) U
      (higherStoredV2_18NaturalitySingleSeparatorRigidity_of_singleDetectorLimitRigidity
        (W := W) U hDetect)

/-- Detector/limit rigidity gives the aligned state in the v2.42 local
classification. -/
theorem higherWeakCoherentAlignment_of_singleDetectorLimitRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hDetect : HigherStoredV2_18NaturalitySingleDetectorLimitRigidity
      (W := W) U) :
    HigherWeakCoherentAlignment (W := W) U :=
  higherWeakCoherentAlignment_of_singleSeparatorRigidity
    (W := W) U
      (higherStoredV2_18NaturalitySingleSeparatorRigidity_of_singleDetectorLimitRigidity
        (W := W) U hDetect)

/-- Exact local E/R obstruction elimination from a single detector plus
fiberwise equalizers, or dually a single codetector plus fiberwise
coequalizers. -/
theorem no_twoAxisObstruction_of_singleDetectorLimitRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hDetect : HigherStoredV2_18NaturalitySingleDetectorLimitRigidity
      (W := W) U) :
    ¬ HigherWeakCoherentTwoAxisObstruction (W := W) U :=
  no_twoAxisObstruction_of_singleSeparatorRigidity
    (W := W) U
      (higherStoredV2_18NaturalitySingleSeparatorRigidity_of_singleDetectorLimitRigidity
        (W := W) U hDetect)

end KUOS.DependentOriginationSingleDetectorObstructionEliminationV2_53
