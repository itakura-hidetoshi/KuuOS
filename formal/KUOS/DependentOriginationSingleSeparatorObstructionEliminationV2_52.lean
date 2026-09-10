import KUOS.DependentOriginationCommonEffectiveEpiFamilyObstructionEliminationV2_51

namespace KUOS.DependentOriginationSingleSeparatorObstructionEliminationV2_52

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationStageIIIRouteCompletenessV2_33
open KUOS.DependentOriginationWeakCoherentTwoAxisObstructionV2_42
open KUOS.DependentOriginationPointwise2CellRigidityObstructionEliminationV2_47
open KUOS.DependentOriginationSeparatingFamilyObstructionEliminationV2_50

universe u v uH vH

/-!
# Single-separator obstruction elimination v2.52

v2.50 proves that a globally separating or coseparating family of target
objects, together with subsingleton probe homs, forces the exact component-hom
uniqueness isolated in v2.47.  The present file specializes that mechanism to
the standard singleton notions already provided by Mathlib:

```text
IsSeparator S
IsCoseparator S.
```

For fixed Cat 1-morphisms `F G : C ⟶ D`, a single separator object `S : D`
suffices if every hom

```text
S ⟶ G.obj Z
```

is a subsingleton.  Indeed, `IsSeparator S` is precisely the statement that
the singleton object property `{S}` is separating, so v2.50 applies.  Dually,
a single coseparator `S` with subsingleton homs

```text
F.obj Z ⟶ S
```

gives the source-side criterion.

Thus:

```text
single separator/coseparator object
  -> singleton separating/coseparating family          (v2.50)
  -> pointwise component-hom uniqueness                (v2.47)
  -> exact Cat 2-cell hom uniqueness                    (v2.46)
  -> stored modification naturality
  -> weak universality + coherent route completeness
  -> no local v2.42 E/R obstruction.
```

This is a concrete sufficient interface, not an existence theorem for a
separator.  It does not assert that every target category has such an object,
nor does it identify this route with the v2.49 ordinary epi detector or v2.51
effective-epi-family route.  No coherent universal-data existence,
strictification, general higher-localization existence principle, or final
global dependent-origination theorem is proved here.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- A single separator object whose homs into all target components of `G` are
subsingletons. -/
def CatHom₂SeparatorTargetObject
    {C D : Cat.{vH, uH}} (G : C ⟶ D) : Prop :=
  ∃ S : D, IsSeparator S ∧
    ∀ Z : C, Subsingleton (S ⟶ G.obj Z)

/-- Dually, a single coseparator object whose homs out of all source
components of `F` are subsingletons. -/
def CatHom₂CoseparatorSourceObject
    {C D : Cat.{vH, uH}} (F : C ⟶ D) : Prop :=
  ∃ S : D, IsCoseparator S ∧
    ∀ Z : C, Subsingleton (F.obj Z ⟶ S)

/-- Either singleton separator mechanism is available for the pair `F`, `G`. -/
def CatHom₂SingleSeparatorRigidity
    {C D : Cat.{vH, uH}} (F G : C ⟶ D) : Prop :=
  CatHom₂SeparatorTargetObject G ∨ CatHom₂CoseparatorSourceObject F

/-- A separator object gives exactly the separating target-family hypothesis
of v2.50 by taking the singleton object property. -/
theorem separatingTargetFamily_of_separatorTargetObject
    {C D : Cat.{vH, uH}} (G : C ⟶ D)
    (hObj : CatHom₂SeparatorTargetObject G) :
    CatHom₂SeparatingTargetFamily G := by
  rcases hObj with ⟨S, hSep, hSub⟩
  refine ⟨ObjectProperty.singleton S, hSep, ?_⟩
  intro Z Q hQ
  have hSQ : S = Q := (ObjectProperty.singleton_iff S Q).mp hQ
  subst Q
  exact hSub Z

/-- A coseparator object gives the dual v2.50 source-family hypothesis. -/
theorem coseparatingSourceFamily_of_coseparatorSourceObject
    {C D : Cat.{vH, uH}} (F : C ⟶ D)
    (hObj : CatHom₂CoseparatorSourceObject F) :
    CatHom₂CoseparatingSourceFamily F := by
  rcases hObj with ⟨S, hCosep, hSub⟩
  refine ⟨ObjectProperty.singleton S, hCosep, ?_⟩
  intro Z Q hQ
  have hSQ : S = Q := (ObjectProperty.singleton_iff S Q).mp hQ
  subst Q
  exact hSub Z

/-- Singleton separator rigidity is a concrete specialization of the v2.50
separating-family rigidity criterion. -/
theorem separatingFamilyRigidity_of_singleSeparatorRigidity
    {C D : Cat.{vH, uH}} (F G : C ⟶ D)
    (hSingle : CatHom₂SingleSeparatorRigidity F G) :
    CatHom₂SeparatingFamilyRigidity F G := by
  rcases hSingle with hTarget | hSource
  · exact Or.inl (separatingTargetFamily_of_separatorTargetObject G hTarget)
  · exact Or.inr (coseparatingSourceFamily_of_coseparatorSourceObject F hSource)

/-- Hence a single separator or coseparator object forces the exact v2.47
componentwise hom-subsingleton criterion. -/
theorem catHom₂PointwiseSubsingleton_of_singleSeparatorRigidity
    {C D : Cat.{vH, uH}} (F G : C ⟶ D)
    (hSingle : CatHom₂SingleSeparatorRigidity F G) :
    CatHom₂PointwiseSubsingleton F G :=
  catHom₂PointwiseSubsingleton_of_separatingFamilyRigidity
    F G (separatingFamilyRigidity_of_singleSeparatorRigidity F G hSingle)

/-- For every raw base arrow, the exact Cat 1-morphism pair occurring in the
v2.23 stored-triangle naturality square admits a singleton separator or
coseparator rigidity witness. -/
def StoredV2_18NaturalitySingleSeparatorRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K) : Prop :=
  ∀ {X Y : Context} (f : X ⟶ Y),
    CatHom₂SingleSeparatorRigidity
      ((restrictHigherLocalizedSystem W H.lift).map f.toLoc ≫
        (restrictHigherLocalizedStrongTrans (W := W) alpha.hom ≫
          K.comparison).app (.mk Y))
      (H.comparison.app (.mk X) ≫ R.map f.toLoc)

/-- The singleton criterion supplies the exact stored v2.50 separating-family
rigidity hypothesis. -/
theorem storedV2_18NaturalitySeparatingFamilyRigidity_of_singleSeparatorRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K)
    (hSingle : StoredV2_18NaturalitySingleSeparatorRigidity
      (W := W) alpha) :
    StoredV2_18NaturalitySeparatingFamilyRigidity (W := W) alpha := by
  intro X Y f
  exact separatingFamilyRigidity_of_singleSeparatorRigidity
    _ _ (hSingle f)

/-- The same singleton criterion therefore gives the stored v2.47 component
hom-subsingleton condition. -/
theorem storedV2_18NaturalityComponentHomSubsingleton_of_singleSeparatorRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K)
    (hSingle : StoredV2_18NaturalitySingleSeparatorRigidity
      (W := W) alpha) :
    StoredV2_18NaturalityComponentHomSubsingleton (W := W) alpha :=
  storedV2_18NaturalityComponentHomSubsingleton_of_separatingFamilyRigidity
    (W := W) alpha
      (storedV2_18NaturalitySeparatingFamilyRigidity_of_singleSeparatorRigidity
        (W := W) alpha hSingle)

/-- Uniform singleton separator rigidity for every v2.18 factor into one
coherent chosen carrier. -/
def HigherStoredV2_18NaturalitySingleSeparatorRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∀ (H : HigherLocalizationFactorization (W := W) R)
    (alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),
    StoredV2_18NaturalitySingleSeparatorRigidity (W := W) alpha

/-- Uniform singleton rigidity gives the uniform v2.50 separating-family
criterion on the same chosen carrier. -/
theorem higherStoredV2_18NaturalitySeparatingFamilyRigidity_of_singleSeparatorRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hSingle : HigherStoredV2_18NaturalitySingleSeparatorRigidity
      (W := W) U) :
    HigherStoredV2_18NaturalitySeparatingFamilyRigidity (W := W) U := by
  intro H alpha
  exact
    storedV2_18NaturalitySeparatingFamilyRigidity_of_singleSeparatorRigidity
      (W := W) alpha (hSingle H alpha)

/-- Uniform singleton rigidity implies the uniform v2.47 pointwise criterion. -/
theorem higherStoredV2_18NaturalityComponentHomSubsingleton_of_singleSeparatorRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hSingle : HigherStoredV2_18NaturalitySingleSeparatorRigidity
      (W := W) U) :
    HigherStoredV2_18NaturalityComponentHomSubsingleton (W := W) U :=
  higherStoredV2_18NaturalityComponentHomSubsingleton_of_separatingFamilyRigidity
    (W := W) U
      (higherStoredV2_18NaturalitySeparatingFamilyRigidity_of_singleSeparatorRigidity
        (W := W) U hSingle)

/-- Coherent universal data plus uniform singleton separator rigidity give the
v2.18 weak universal property on the same chosen carrier. -/
theorem hasWeakHigherLocalizationUniversalProperty_of_singleSeparatorRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hSingle : HigherStoredV2_18NaturalitySingleSeparatorRigidity
      (W := W) U) :
    HasWeakHigherLocalizationUniversalProperty (W := W) R :=
  hasWeakHigherLocalizationUniversalProperty_of_separatingFamilyRigidity
    (W := W) U
      (higherStoredV2_18NaturalitySeparatingFamilyRigidity_of_singleSeparatorRigidity
        (W := W) U hSingle)

/-- The coherent Stage III route obstruction disappears under the same
singleton separator rigidity condition. -/
theorem higherCoherentRouteCompleteness_of_singleSeparatorRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hSingle : HigherStoredV2_18NaturalitySingleSeparatorRigidity
      (W := W) U) :
    HigherCoherentRouteCompleteness (W := W) U :=
  higherCoherentRouteCompleteness_of_separatingFamilyRigidity
    (W := W) U
      (higherStoredV2_18NaturalitySeparatingFamilyRigidity_of_singleSeparatorRigidity
        (W := W) U hSingle)

/-- Singleton separator rigidity gives the aligned state in the v2.42 local
classification. -/
theorem higherWeakCoherentAlignment_of_singleSeparatorRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hSingle : HigherStoredV2_18NaturalitySingleSeparatorRigidity
      (W := W) U) :
    HigherWeakCoherentAlignment (W := W) U :=
  higherWeakCoherentAlignment_of_separatingFamilyRigidity
    (W := W) U
      (higherStoredV2_18NaturalitySeparatingFamilyRigidity_of_singleSeparatorRigidity
        (W := W) U hSingle)

/-- Exact local E/R obstruction elimination under a single separator or
coseparator object. -/
theorem no_twoAxisObstruction_of_singleSeparatorRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hSingle : HigherStoredV2_18NaturalitySingleSeparatorRigidity
      (W := W) U) :
    ¬ HigherWeakCoherentTwoAxisObstruction (W := W) U :=
  no_twoAxisObstruction_of_separatingFamilyRigidity
    (W := W) U
      (higherStoredV2_18NaturalitySeparatingFamilyRigidity_of_singleSeparatorRigidity
        (W := W) U hSingle)

end KUOS.DependentOriginationSingleSeparatorObstructionEliminationV2_52
