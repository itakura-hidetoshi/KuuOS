import Mathlib.CategoryTheory.Generator.Basic
import KUOS.DependentOriginationCommonCancellationDetectorObstructionEliminationV2_49

namespace KUOS.DependentOriginationSeparatingFamilyObstructionEliminationV2_50

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationStageIIIRouteCompletenessV2_33
open KUOS.DependentOriginationWeakCoherentTwoAxisObstructionV2_42
open KUOS.DependentOriginationPointwise2CellRigidityObstructionEliminationV2_47

universe u v uH vH

/-!
# Separating-family obstruction elimination v2.50

v2.47 reduces the target-side stored-triangle coherence problem to uniqueness
of the component morphisms

```text
F.obj Z ⟶ G.obj Z
```

for the exact pair of Cat 1-morphisms occurring in each v2.23 naturality
square.  v2.48 obtains that uniqueness from thinness of the image-envelope
subcategory, while v2.49 obtains it from one common epi or mono cancellation
detector.

This file gives a third structural route using the standard Mathlib notions
`ObjectProperty.IsSeparating` and `ObjectProperty.IsCoseparating`.

If `P` is a globally separating family in the target category and every probe
hom

```text
Q ⟶ G.obj Z      (P Q)
```

is a subsingleton, then any two maps `F.obj Z ⟶ G.obj Z` become equal after
precomposition with every `P`-probe.  Global separation therefore makes the
maps themselves equal.  Dually, a globally coseparating family whose probe
homs

```text
F.obj Z ⟶ Q      (P Q)
```

are subsingletons gives equality by postcomposition.

Thus:

```text
global separating target probes
             OR
global coseparating source probes
  -> pointwise component-hom uniqueness                (v2.47)
  -> exact Cat 2-cell hom uniqueness                    (v2.46)
  -> stored modification naturality
  -> weak universality + coherent route completeness
  -> no local v2.42 E/R obstruction.
```

The separating/coseparating hypothesis is global in the ambient target
category.  We deliberately do not replace it by a relative predicate tailored
only to the single pair `F.obj Z`, `G.obj Z`, because such a predicate could
collapse into a repackaging of the desired pointwise equality itself.

This route is only sufficient.  No implication to or from the v2.48
image-envelope route or the v2.49 common-cancellation route is asserted.  No
existence of a separating family, coherent universal data, strictification, or
final global dependent-origination theorem is proved here.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- A globally separating family whose maps into every target component are
subsingletons.  Such probes distinguish all parallel morphisms in `D`, while
the subsingleton condition makes every probe unable to distinguish two maps
into `G.obj Z` because their composites are forced equal. -/
def CatHom₂SeparatingTargetFamily
    {C D : Cat.{vH, uH}} (G : C ⟶ D) : Prop :=
  ∃ P : ObjectProperty D,
    P.IsSeparating ∧
      ∀ (Z : C) (Q : D), P Q → Subsingleton (Q ⟶ G.obj Z)

/-- Dually, a globally coseparating family whose maps out of every source
component are subsingletons. -/
def CatHom₂CoseparatingSourceFamily
    {C D : Cat.{vH, uH}} (F : C ⟶ D) : Prop :=
  ∃ P : ObjectProperty D,
    P.IsCoseparating ∧
      ∀ (Z : C) (Q : D), P Q → Subsingleton (F.obj Z ⟶ Q)

/-- Either standard global probe-family mechanism is available for the pair
`F`, `G`. -/
def CatHom₂SeparatingFamilyRigidity
    {C D : Cat.{vH, uH}} (F G : C ⟶ D) : Prop :=
  CatHom₂SeparatingTargetFamily G ∨ CatHom₂CoseparatingSourceFamily F

/-- A separating target family forces uniqueness of all corresponding
component morphisms. -/
theorem catHom₂PointwiseSubsingleton_of_separatingTargetFamily
    {C D : Cat.{vH, uH}} (F G : C ⟶ D)
    (hFamily : CatHom₂SeparatingTargetFamily G) :
    CatHom₂PointwiseSubsingleton F G := by
  rcases hFamily with ⟨P, hSep, hSub⟩
  intro Z
  constructor
  intro f g
  apply hSep f g
  intro Q hQ k
  exact (hSub Z Q hQ).elim _ _

/-- A coseparating source family gives the dual componentwise uniqueness
criterion. -/
theorem catHom₂PointwiseSubsingleton_of_coseparatingSourceFamily
    {C D : Cat.{vH, uH}} (F G : C ⟶ D)
    (hFamily : CatHom₂CoseparatingSourceFamily F) :
    CatHom₂PointwiseSubsingleton F G := by
  rcases hFamily with ⟨P, hCosep, hSub⟩
  intro Z
  constructor
  intro f g
  apply hCosep f g
  intro Q hQ k
  exact (hSub Z Q hQ).elim _ _

/-- Either global separating-family mechanism implies the exact pointwise
criterion isolated in v2.47. -/
theorem catHom₂PointwiseSubsingleton_of_separatingFamilyRigidity
    {C D : Cat.{vH, uH}} (F G : C ⟶ D)
    (hFamily : CatHom₂SeparatingFamilyRigidity F G) :
    CatHom₂PointwiseSubsingleton F G := by
  rcases hFamily with hTarget | hSource
  · exact catHom₂PointwiseSubsingleton_of_separatingTargetFamily F G hTarget
  · exact catHom₂PointwiseSubsingleton_of_coseparatingSourceFamily F G hSource

/-- For every raw base arrow, the exact pair of Cat 1-morphisms occurring in
the v2.23 stored-triangle naturality square admits one of the two standard
global separating-family rigidity mechanisms. -/
def StoredV2_18NaturalitySeparatingFamilyRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K) : Prop :=
  ∀ {X Y : Context} (f : X ⟶ Y),
    CatHom₂SeparatingFamilyRigidity
      ((restrictHigherLocalizedSystem W H.lift).map f.toLoc ≫
        (restrictHigherLocalizedStrongTrans (W := W) alpha.hom ≫
          K.comparison).app (.mk Y))
      (H.comparison.app (.mk X) ≫ R.map f.toLoc)

/-- Separating-family rigidity supplies the exact v2.47 component-hom
subsingleton condition for a stored naturality square. -/
theorem storedV2_18NaturalityComponentHomSubsingleton_of_separatingFamilyRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K)
    (hFamily : StoredV2_18NaturalitySeparatingFamilyRigidity
      (W := W) alpha) :
    StoredV2_18NaturalityComponentHomSubsingleton (W := W) alpha := by
  intro X Y f
  exact catHom₂PointwiseSubsingleton_of_separatingFamilyRigidity
    _ _ (hFamily f)

/-- Uniform separating-family rigidity for every v2.18 factor into one
coherent chosen carrier. -/
def HigherStoredV2_18NaturalitySeparatingFamilyRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∀ (H : HigherLocalizationFactorization (W := W) R)
    (alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),
    StoredV2_18NaturalitySeparatingFamilyRigidity (W := W) alpha

/-- Uniform separating-family rigidity implies the uniform v2.47 pointwise
criterion. -/
theorem higherStoredV2_18NaturalityComponentHomSubsingleton_of_separatingFamilyRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hFamily : HigherStoredV2_18NaturalitySeparatingFamilyRigidity
      (W := W) U) :
    HigherStoredV2_18NaturalityComponentHomSubsingleton (W := W) U := by
  intro H alpha
  exact
    storedV2_18NaturalityComponentHomSubsingleton_of_separatingFamilyRigidity
      (W := W) alpha (hFamily H alpha)

/-- Coherent universal data plus uniform separating-family rigidity give the
v2.18 weak universal property on the same chosen carrier. -/
theorem hasWeakHigherLocalizationUniversalProperty_of_separatingFamilyRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hFamily : HigherStoredV2_18NaturalitySeparatingFamilyRigidity
      (W := W) U) :
    HasWeakHigherLocalizationUniversalProperty (W := W) R :=
  hasWeakHigherLocalizationUniversalProperty_of_pointwise2CellRigidity
    (W := W) U
      (higherStoredV2_18NaturalityComponentHomSubsingleton_of_separatingFamilyRigidity
        (W := W) U hFamily)

/-- The coherent Stage III route obstruction disappears under the same
separating-family rigidity condition. -/
theorem higherCoherentRouteCompleteness_of_separatingFamilyRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hFamily : HigherStoredV2_18NaturalitySeparatingFamilyRigidity
      (W := W) U) :
    HigherCoherentRouteCompleteness (W := W) U :=
  higherCoherentRouteCompleteness_of_pointwise2CellRigidity
    (W := W) U
      (higherStoredV2_18NaturalityComponentHomSubsingleton_of_separatingFamilyRigidity
        (W := W) U hFamily)

/-- Separating-family rigidity gives the aligned state in the v2.42 local
classification. -/
theorem higherWeakCoherentAlignment_of_separatingFamilyRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hFamily : HigherStoredV2_18NaturalitySeparatingFamilyRigidity
      (W := W) U) :
    HigherWeakCoherentAlignment (W := W) U :=
  ⟨hasWeakHigherLocalizationUniversalProperty_of_separatingFamilyRigidity
      (W := W) U hFamily,
    higherCoherentRouteCompleteness_of_separatingFamilyRigidity
      (W := W) U hFamily⟩

/-- Exact local E/R obstruction elimination under standard global separating
or coseparating probe-family rigidity. -/
theorem no_twoAxisObstruction_of_separatingFamilyRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hFamily : HigherStoredV2_18NaturalitySeparatingFamilyRigidity
      (W := W) U) :
    ¬ HigherWeakCoherentTwoAxisObstruction (W := W) U :=
  (higherWeakCoherentAlignment_iff_no_twoAxisObstruction
    (W := W) U).mp
      (higherWeakCoherentAlignment_of_separatingFamilyRigidity
        (W := W) U hFamily)

end KUOS.DependentOriginationSeparatingFamilyObstructionEliminationV2_50
