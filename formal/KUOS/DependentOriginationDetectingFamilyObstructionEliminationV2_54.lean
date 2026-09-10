import Mathlib.CategoryTheory.Generator.Basic
import KUOS.DependentOriginationSingleDetectorObstructionEliminationV2_53

namespace KUOS.DependentOriginationDetectingFamilyObstructionEliminationV2_54

open CategoryTheory
open CategoryTheory.Limits
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationStageIIIRouteCompletenessV2_33
open KUOS.DependentOriginationWeakCoherentTwoAxisObstructionV2_42
open KUOS.DependentOriginationPointwise2CellRigidityObstructionEliminationV2_47
open KUOS.DependentOriginationSeparatingFamilyObstructionEliminationV2_50
open KUOS.DependentOriginationSingleDetectorObstructionEliminationV2_53

universe u v uH vH

/-!
# Detecting-family obstruction elimination v2.54

v2.50 eliminates the local v2.42 E/R obstruction from a globally separating
or coseparating family whose relevant probe homs are subsingletons.  v2.53
specializes a different Mathlib mechanism to one detector or codetector object:
with equalizers a detector is a separator, and with coequalizers a codetector
is a coseparator.

The present file combines those two directions at the natural family level.
For fixed Cat 1-morphisms `F G : C ⟶ D`, a target object property `P` suffices
when

```text
P.IsDetecting
```

and every probe hom

```text
Q ⟶ G.obj Z      (P Q)
```

is a subsingleton, provided `D` has equalizers.  Mathlib upgrades
`P.IsDetecting` to `P.IsSeparating`, after which the exact v2.50 theorem
applies.  Dually, a codetecting family plus coequalizers gives a coseparating
family and the source-side criterion.

Thus:

```text
detecting target family + target-fiber equalizers
                 OR
codetecting source family + target-fiber coequalizers
  -> separating/coseparating family                  (Mathlib)
  -> v2.50 separating-family rigidity
  -> pointwise component-hom uniqueness              (v2.47)
  -> exact Cat 2-cell hom uniqueness                  (v2.46)
  -> stored modification naturality
  -> weak universality + coherent route completeness
  -> no local v2.42 E/R obstruction.
```

The singleton detector/codetector conditions of v2.53 embed into the family
conditions here by choosing the singleton object property.  Hence v2.53 is a
concrete special case of this structural route, while the equalizer and
coequalizer hypotheses are retained unchanged.

This file proves no existence theorem for detecting families, limits,
coherent universal data, strictification, or higher localizations, and no
final global dependent-origination theorem.  It does not weaken the limit
hypotheses used by Mathlib and does not identify this route with the v2.49
ordinary cancellation or v2.51 effective-epi-family routes.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- A globally detecting target family whose maps into every target component
of `G` are subsingletons.  Equalizers are an ambient hypothesis only when the
detecting family is upgraded to a separating family. -/
def CatHom₂DetectingTargetFamily
    {C D : Cat.{vH, uH}} (G : C ⟶ D) : Prop :=
  ∃ P : ObjectProperty D,
    P.IsDetecting ∧
      ∀ (Z : C) (Q : D), P Q → Subsingleton (Q ⟶ G.obj Z)

/-- Dually, a globally codetecting source family whose maps out of every
source component of `F` are subsingletons. -/
def CatHom₂CodetectingSourceFamily
    {C D : Cat.{vH, uH}} (F : C ⟶ D) : Prop :=
  ∃ P : ObjectProperty D,
    P.IsCodetecting ∧
      ∀ (Z : C) (Q : D), P Q → Subsingleton (F.obj Z ⟶ Q)

/-- In a category with equalizers, a detecting target family gives exactly the
v2.50 separating-target-family hypothesis. -/
theorem separatingTargetFamily_of_detectingTargetFamily
    {C D : Cat.{vH, uH}} [HasEqualizers D] (G : C ⟶ D)
    (hFamily : CatHom₂DetectingTargetFamily G) :
    CatHom₂SeparatingTargetFamily G := by
  rcases hFamily with ⟨P, hDetect, hSub⟩
  exact ⟨P, ObjectProperty.IsDetecting.isSeparating hDetect, hSub⟩

/-- Dually, coequalizers upgrade a codetecting source family to the v2.50
coseparating-family hypothesis. -/
theorem coseparatingSourceFamily_of_codetectingSourceFamily
    {C D : Cat.{vH, uH}} [HasCoequalizers D] (F : C ⟶ D)
    (hFamily : CatHom₂CodetectingSourceFamily F) :
    CatHom₂CoseparatingSourceFamily F := by
  rcases hFamily with ⟨P, hDetect, hSub⟩
  exact ⟨P, ObjectProperty.IsCodetecting.isCoseparating hDetect, hSub⟩

/-- A detecting target family plus equalizers forces the exact v2.47
componentwise hom-subsingleton criterion. -/
theorem catHom₂PointwiseSubsingleton_of_detectingTargetFamily
    {C D : Cat.{vH, uH}} [HasEqualizers D] (F G : C ⟶ D)
    (hFamily : CatHom₂DetectingTargetFamily G) :
    CatHom₂PointwiseSubsingleton F G :=
  catHom₂PointwiseSubsingleton_of_separatingTargetFamily
    F G (separatingTargetFamily_of_detectingTargetFamily G hFamily)

/-- A codetecting source family plus coequalizers gives the dual v2.47
criterion. -/
theorem catHom₂PointwiseSubsingleton_of_codetectingSourceFamily
    {C D : Cat.{vH, uH}} [HasCoequalizers D] (F G : C ⟶ D)
    (hFamily : CatHom₂CodetectingSourceFamily F) :
    CatHom₂PointwiseSubsingleton F G :=
  catHom₂PointwiseSubsingleton_of_coseparatingSourceFamily
    F G (coseparatingSourceFamily_of_codetectingSourceFamily F hFamily)

/-- A v2.53 singleton detector is a detecting family by taking the singleton
object property.  No equalizer hypothesis is needed for this embedding. -/
theorem detectingTargetFamily_of_detectorTargetObject
    {C D : Cat.{vH, uH}} (G : C ⟶ D)
    (hObj : CatHom₂DetectorTargetObject G) :
    CatHom₂DetectingTargetFamily G := by
  rcases hObj with ⟨S, hDetect, hSub⟩
  refine ⟨ObjectProperty.singleton S, hDetect, ?_⟩
  intro Z Q hQ
  have hSQ : S = Q := (ObjectProperty.singleton_iff S Q).mp hQ
  subst Q
  exact hSub Z

/-- Dually, a v2.53 singleton codetector is a codetecting family. -/
theorem codetectingSourceFamily_of_codetectorSourceObject
    {C D : Cat.{vH, uH}} (F : C ⟶ D)
    (hObj : CatHom₂CodetectorSourceObject F) :
    CatHom₂CodetectingSourceFamily F := by
  rcases hObj with ⟨S, hDetect, hSub⟩
  refine ⟨ObjectProperty.singleton S, hDetect, ?_⟩
  intro Z Q hQ
  have hSQ : S = Q := (ObjectProperty.singleton_iff S Q).mp hQ
  subst Q
  exact hSub Z

/-- For every raw base arrow, the target Cat 1-morphism in the exact stored
naturality square admits a detecting family with subsingleton probe homs. -/
def StoredV2_18NaturalityDetectingTargetFamily
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K) : Prop :=
  ∀ {X Y : Context} (f : X ⟶ Y),
    CatHom₂DetectingTargetFamily
      (H.comparison.app (.mk X) ≫ R.map f.toLoc)

/-- Dually, every exact stored source Cat 1-morphism admits a codetecting
family with subsingleton outgoing probe homs. -/
def StoredV2_18NaturalityCodetectingSourceFamily
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K) : Prop :=
  ∀ {X Y : Context} (f : X ⟶ Y),
    CatHom₂CodetectingSourceFamily
      ((restrictHigherLocalizedSystem W H.lift).map f.toLoc ≫
        (restrictHigherLocalizedStrongTrans (W := W) alpha.hom ≫
          K.comparison).app (.mk Y))

/-- Fiberwise equalizers plus stored target detecting families give the exact
v2.50 stored separating-family rigidity condition. -/
theorem storedV2_18NaturalitySeparatingFamilyRigidity_of_detectingTargetFamily
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K)
    (hEq : HigherRawFiberHasEqualizers R)
    (hDetect : StoredV2_18NaturalityDetectingTargetFamily
      (W := W) alpha) :
    StoredV2_18NaturalitySeparatingFamilyRigidity (W := W) alpha := by
  intro X Y f
  letI : HasEqualizers (R.obj (.mk Y)) := hEq Y
  exact Or.inl
    (separatingTargetFamily_of_detectingTargetFamily _ (hDetect f))

/-- Fiberwise coequalizers plus stored source codetecting families give the
dual v2.50 criterion. -/
theorem storedV2_18NaturalitySeparatingFamilyRigidity_of_codetectingSourceFamily
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K)
    (hCoeq : HigherRawFiberHasCoequalizers R)
    (hDetect : StoredV2_18NaturalityCodetectingSourceFamily
      (W := W) alpha) :
    StoredV2_18NaturalitySeparatingFamilyRigidity (W := W) alpha := by
  intro X Y f
  letI : HasCoequalizers (R.obj (.mk Y)) := hCoeq Y
  exact Or.inr
    (coseparatingSourceFamily_of_codetectingSourceFamily _ (hDetect f))

/-- The v2.53 stored singleton target-detector condition embeds into the
family-level condition. -/
theorem storedV2_18NaturalityDetectingTargetFamily_of_detectorTargetObject
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K)
    (hObj : StoredV2_18NaturalityDetectorTargetObject (W := W) alpha) :
    StoredV2_18NaturalityDetectingTargetFamily (W := W) alpha := by
  intro X Y f
  exact detectingTargetFamily_of_detectorTargetObject _ (hObj f)

/-- The v2.53 stored singleton source-codetector condition embeds dually. -/
theorem storedV2_18NaturalityCodetectingSourceFamily_of_codetectorSourceObject
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K)
    (hObj : StoredV2_18NaturalityCodetectorSourceObject (W := W) alpha) :
    StoredV2_18NaturalityCodetectingSourceFamily (W := W) alpha := by
  intro X Y f
  exact codetectingSourceFamily_of_codetectorSourceObject _ (hObj f)

/-- Uniform target detecting-family rigidity for every factor into one
coherent chosen carrier. -/
def HigherStoredV2_18NaturalityDetectingTargetFamily
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∀ (H : HigherLocalizationFactorization (W := W) R)
    (alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),
    StoredV2_18NaturalityDetectingTargetFamily (W := W) alpha

/-- Uniform source codetecting-family rigidity on the same chosen carrier. -/
def HigherStoredV2_18NaturalityCodetectingSourceFamily
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∀ (H : HigherLocalizationFactorization (W := W) R)
    (alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),
    StoredV2_18NaturalityCodetectingSourceFamily (W := W) alpha

/-- The two family-level detector/limit routes.  The Mathlib limit hypotheses
are kept exactly as in v2.53. -/
def HigherStoredV2_18NaturalityDetectingFamilyLimitRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  (HigherRawFiberHasEqualizers R ∧
      HigherStoredV2_18NaturalityDetectingTargetFamily (W := W) U) ∨
    (HigherRawFiberHasCoequalizers R ∧
      HigherStoredV2_18NaturalityCodetectingSourceFamily (W := W) U)

/-- Either detecting-family/limit route gives the uniform v2.50
separating-family criterion on the exact same chosen carrier. -/
theorem higherStoredV2_18NaturalitySeparatingFamilyRigidity_of_detectingFamilyLimitRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hDetect : HigherStoredV2_18NaturalityDetectingFamilyLimitRigidity
      (W := W) U) :
    HigherStoredV2_18NaturalitySeparatingFamilyRigidity (W := W) U := by
  rcases hDetect with ⟨hEq, hTarget⟩ | ⟨hCoeq, hSource⟩
  · intro H alpha
    exact storedV2_18NaturalitySeparatingFamilyRigidity_of_detectingTargetFamily
      (W := W) alpha hEq (hTarget H alpha)
  · intro H alpha
    exact storedV2_18NaturalitySeparatingFamilyRigidity_of_codetectingSourceFamily
      (W := W) alpha hCoeq (hSource H alpha)

/-- The v2.53 uniform singleton-detector condition is a special case of the
v2.54 detecting-family condition, with the same equalizer/coequalizer branch. -/
theorem higherStoredV2_18NaturalityDetectingFamilyLimitRigidity_of_singleDetectorLimitRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hSingle : HigherStoredV2_18NaturalitySingleDetectorLimitRigidity
      (W := W) U) :
    HigherStoredV2_18NaturalityDetectingFamilyLimitRigidity (W := W) U := by
  rcases hSingle with ⟨hEq, hTarget⟩ | ⟨hCoeq, hSource⟩
  · exact Or.inl ⟨hEq, fun H alpha =>
      storedV2_18NaturalityDetectingTargetFamily_of_detectorTargetObject
        (W := W) alpha (hTarget H alpha)⟩
  · exact Or.inr ⟨hCoeq, fun H alpha =>
      storedV2_18NaturalityCodetectingSourceFamily_of_codetectorSourceObject
        (W := W) alpha (hSource H alpha)⟩

/-- Detecting-family rigidity therefore supplies the uniform v2.47 pointwise
component-hom criterion. -/
theorem higherStoredV2_18NaturalityComponentHomSubsingleton_of_detectingFamilyLimitRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hDetect : HigherStoredV2_18NaturalityDetectingFamilyLimitRigidity
      (W := W) U) :
    HigherStoredV2_18NaturalityComponentHomSubsingleton (W := W) U :=
  higherStoredV2_18NaturalityComponentHomSubsingleton_of_separatingFamilyRigidity
    (W := W) U
      (higherStoredV2_18NaturalitySeparatingFamilyRigidity_of_detectingFamilyLimitRigidity
        (W := W) U hDetect)

/-- Coherent universal data plus detecting-family rigidity give the v2.18 weak
universal property on the same chosen carrier. -/
theorem hasWeakHigherLocalizationUniversalProperty_of_detectingFamilyLimitRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hDetect : HigherStoredV2_18NaturalityDetectingFamilyLimitRigidity
      (W := W) U) :
    HasWeakHigherLocalizationUniversalProperty (W := W) R :=
  hasWeakHigherLocalizationUniversalProperty_of_separatingFamilyRigidity
    (W := W) U
      (higherStoredV2_18NaturalitySeparatingFamilyRigidity_of_detectingFamilyLimitRigidity
        (W := W) U hDetect)

/-- The coherent Stage III route obstruction disappears under the same
family-level detector/limit condition. -/
theorem higherCoherentRouteCompleteness_of_detectingFamilyLimitRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hDetect : HigherStoredV2_18NaturalityDetectingFamilyLimitRigidity
      (W := W) U) :
    HigherCoherentRouteCompleteness (W := W) U :=
  higherCoherentRouteCompleteness_of_separatingFamilyRigidity
    (W := W) U
      (higherStoredV2_18NaturalitySeparatingFamilyRigidity_of_detectingFamilyLimitRigidity
        (W := W) U hDetect)

/-- Detecting-family rigidity gives the aligned state in the v2.42 local
classification. -/
theorem higherWeakCoherentAlignment_of_detectingFamilyLimitRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hDetect : HigherStoredV2_18NaturalityDetectingFamilyLimitRigidity
      (W := W) U) :
    HigherWeakCoherentAlignment (W := W) U :=
  higherWeakCoherentAlignment_of_separatingFamilyRigidity
    (W := W) U
      (higherStoredV2_18NaturalitySeparatingFamilyRigidity_of_detectingFamilyLimitRigidity
        (W := W) U hDetect)

/-- Exact local E/R obstruction elimination under the family-level
detector/limit rigidity condition. -/
theorem no_twoAxisObstruction_of_detectingFamilyLimitRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hDetect : HigherStoredV2_18NaturalityDetectingFamilyLimitRigidity
      (W := W) U) :
    ¬ HigherWeakCoherentTwoAxisObstruction (W := W) U :=
  no_twoAxisObstruction_of_separatingFamilyRigidity
    (W := W) U
      (higherStoredV2_18NaturalitySeparatingFamilyRigidity_of_detectingFamilyLimitRigidity
        (W := W) U hDetect)

end KUOS.DependentOriginationDetectingFamilyObstructionEliminationV2_54
