import KUOS.DependentOriginationLocal2CellRigidityObstructionEliminationV2_46

namespace KUOS.DependentOriginationPointwise2CellRigidityObstructionEliminationV2_47

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationStageIIIRouteCompletenessV2_33
open KUOS.DependentOriginationWeakCoherentTwoAxisObstructionV2_42
open KUOS.DependentOriginationFiberwiseThinObstructionEliminationV2_45
open KUOS.DependentOriginationLocal2CellRigidityObstructionEliminationV2_46

universe u v uH vH

/-!
# Pointwise 2-cell rigidity obstruction elimination v2.47

v2.46 isolates the exact Cat 2-cell hom type in which each stored v2.18
modification-naturality equation lives and assumes that whole hom type is a
subsingleton.  This file resolves that condition one categorical level lower.

A Cat 2-cell is a wrapped natural transformation.  Two such 2-cells are equal
once their underlying natural transformations have equal components.  Hence it
is enough that, for every object of the source fiber, the single component hom
set between the two functors occurring in the naturality square is a
subsingleton.

The structural route is therefore

```text
pointwise component-hom uniqueness
  -> Cat 2-cell hom uniqueness (v2.46 hypothesis)
  -> stored v2.18 triangle modification naturality
  -> factor coherence lifting
  -> weak universality + coherent route completeness
  -> no local v2.42 E/R obstruction.
```

This does not assume that the whole target fiber is thin.  Unrelated object
pairs may have many morphisms.  It also does not restate the naturality
equation itself: the hypothesis is only uniqueness of the component morphism
sets in which possible natural transformations would be evaluated.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Pointwise uniqueness criterion for Cat 2-cells between two fixed Cat
1-morphisms.  Only the hom sets between corresponding object images are
required to be subsingletons. -/
def CatHom₂PointwiseSubsingleton
    {C D : Cat.{vH, uH}} (F G : C ⟶ D) : Prop :=
  ∀ Z : C, Subsingleton (F.obj Z ⟶ G.obj Z)

/-- Pointwise component-hom uniqueness implies uniqueness of the whole Cat
2-cell.  `Cat.Hom₂.ext` unwraps Cat 2-cells and `NatTrans.ext` reduces equality
to equality of components. -/
theorem subsingleton_catHom₂_of_pointwise
    {C D : Cat.{vH, uH}} (F G : C ⟶ D)
    (hPoint : CatHom₂PointwiseSubsingleton F G) :
    Subsingleton (F ⟶ G) := by
  constructor
  intro η θ
  apply Cat.Hom₂.ext
  apply NatTrans.ext
  funext Z
  exact Subsingleton.elim _ _

/-- For every raw base arrow, each component hom set of the exact v2.23
stored-triangle naturality square is a subsingleton.

Unlike v2.45, this does not require all hom sets in the target raw fiber to be
subsingletons.  Unlike v2.46, it does not assume uniqueness of whole natural
transformations directly. -/
def StoredV2_18NaturalityComponentHomSubsingleton
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K) : Prop :=
  ∀ {X Y : Context} (f : X ⟶ Y),
    CatHom₂PointwiseSubsingleton
      ((restrictHigherLocalizedSystem W H.lift).map f.toLoc ≫
        (restrictHigherLocalizedStrongTrans (W := W) alpha.hom ≫
          K.comparison).app (.mk Y))
      (H.comparison.app (.mk X) ≫ R.map f.toLoc)

/-- Pointwise component uniqueness supplies the exact local Cat 2-cell
subsingleton hypothesis isolated in v2.46. -/
theorem storedV2_18NaturalityHomSubsingleton_of_pointwise
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K)
    (hPoint : StoredV2_18NaturalityComponentHomSubsingleton
      (W := W) alpha) :
    StoredV2_18NaturalityHomSubsingleton (W := W) alpha := by
  intro X Y f
  exact subsingleton_catHom₂_of_pointwise _ _ (hPoint f)

/-- v2.45 fiberwise thinness implies the still more local pointwise condition.
Thus the target-side route now factors as fiberwise thin -> pointwise rigidity
-> whole 2-cell rigidity. -/
theorem storedV2_18NaturalityComponentHomSubsingleton_of_fiberwiseThin
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (hThin : HigherRawFiberwiseThin R)
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K) :
    StoredV2_18NaturalityComponentHomSubsingleton (W := W) alpha := by
  intro X Y f Z
  letI : Quiver.IsThin (R.obj (.mk Y)) := hThin Y
  infer_instance

/-- Uniform pointwise component-hom rigidity for every v2.18 factor into one
coherent chosen carrier. -/
def HigherStoredV2_18NaturalityComponentHomSubsingleton
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∀ (H : HigherLocalizationFactorization (W := W) R)
    (alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),
    StoredV2_18NaturalityComponentHomSubsingleton (W := W) alpha

/-- Uniform pointwise rigidity implies the uniform v2.46 local 2-cell rigidity
criterion. -/
theorem higherStoredV2_18NaturalityHomSubsingleton_of_pointwise
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hPoint : HigherStoredV2_18NaturalityComponentHomSubsingleton
      (W := W) U) :
    HigherStoredV2_18NaturalityHomSubsingleton (W := W) U := by
  intro H alpha
  exact storedV2_18NaturalityHomSubsingleton_of_pointwise
    (W := W) alpha (hPoint H alpha)

/-- The v2.45 fiberwise-thin route factors through the v2.47 pointwise
criterion. -/
theorem higherStoredV2_18NaturalityComponentHomSubsingleton_of_fiberwiseThin
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (hThin : HigherRawFiberwiseThin R)
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherStoredV2_18NaturalityComponentHomSubsingleton (W := W) U := by
  intro H alpha
  exact storedV2_18NaturalityComponentHomSubsingleton_of_fiberwiseThin
    (W := W) hThin alpha

/-- Coherent universal data plus uniform pointwise rigidity give the v2.18 weak
universal property on the same chosen carrier. -/
theorem hasWeakHigherLocalizationUniversalProperty_of_pointwise2CellRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hPoint : HigherStoredV2_18NaturalityComponentHomSubsingleton
      (W := W) U) :
    HasWeakHigherLocalizationUniversalProperty (W := W) R :=
  hasWeakHigherLocalizationUniversalProperty_of_local2CellRigidity
    (W := W) U
      (higherStoredV2_18NaturalityHomSubsingleton_of_pointwise
        (W := W) U hPoint)

/-- The coherent Stage III route obstruction disappears under the same
pointwise condition. -/
theorem higherCoherentRouteCompleteness_of_pointwise2CellRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hPoint : HigherStoredV2_18NaturalityComponentHomSubsingleton
      (W := W) U) :
    HigherCoherentRouteCompleteness (W := W) U :=
  higherCoherentRouteCompleteness_of_local2CellRigidity
    (W := W) U
      (higherStoredV2_18NaturalityHomSubsingleton_of_pointwise
        (W := W) U hPoint)

/-- Pointwise component-hom rigidity gives the positive aligned state of the
v2.42 classification. -/
theorem higherWeakCoherentAlignment_of_pointwise2CellRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hPoint : HigherStoredV2_18NaturalityComponentHomSubsingleton
      (W := W) U) :
    HigherWeakCoherentAlignment (W := W) U :=
  ⟨hasWeakHigherLocalizationUniversalProperty_of_pointwise2CellRigidity
      (W := W) U hPoint,
    higherCoherentRouteCompleteness_of_pointwise2CellRigidity
      (W := W) U hPoint⟩

/-- Exact local E/R obstruction elimination under pointwise component-hom
uniqueness. -/
theorem no_twoAxisObstruction_of_pointwise2CellRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hPoint : HigherStoredV2_18NaturalityComponentHomSubsingleton
      (W := W) U) :
    ¬ HigherWeakCoherentTwoAxisObstruction (W := W) U :=
  (higherWeakCoherentAlignment_iff_no_twoAxisObstruction
    (W := W) U).mp
      (higherWeakCoherentAlignment_of_pointwise2CellRigidity
        (W := W) U hPoint)

end KUOS.DependentOriginationPointwise2CellRigidityObstructionEliminationV2_47
