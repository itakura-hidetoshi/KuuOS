import KUOS.DependentOriginationFiberwiseThinObstructionEliminationV2_45

namespace KUOS.DependentOriginationLocal2CellRigidityObstructionEliminationV2_46

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationFactorCoherenceLiftingV2_21
open KUOS.DependentOriginationModificationTriangleNormalFormV2_22
open KUOS.DependentOriginationStoredTriangleModificationNaturalityV2_23
open KUOS.DependentOriginationStoredTriangleCorrectionV2_26
open KUOS.DependentOriginationStageIIIRouteCompletenessV2_33
open KUOS.DependentOriginationWeakCoherentTwoAxisObstructionV2_42
open KUOS.DependentOriginationFiberwiseThinObstructionEliminationV2_45

universe u v uH vH

/-!
# Local 2-cell rigidity obstruction elimination v2.46

v2.45 kills the stored-triangle coherence obstruction by assuming every raw
fiber is thin.  That hypothesis is stronger than what the v2.23 naturality
square actually uses.

For a fixed v2.18 factor `alpha` and base arrow `f : X ⟶ Y`, both sides of the
stored modification-naturality equation are Cat 2-cells with the same source
and target.  It is therefore enough that this one Cat 2-cell hom type be a
subsingleton.  No thinness assumption is needed on any unrelated hom in the
raw fiber.

This file isolates that exact local rigidity condition and proves

```text
local naturality-hom subsingleton
  -> stored v2.18 triangle modification naturality
  -> factor modification triangle / factor coherence lifting
  -> weak universality on the same coherent chosen carrier
  -> coherent route completeness
  -> no local v2.42 E/R obstruction.
```

It also proves that v2.45 fiberwise thinness implies the new local condition,
so the v2.45 theorem factors through this strictly more targeted interface.

The condition below is not the v2.23 naturality equation restated: it is a
uniqueness property of the ambient 2-cell hom type in which that equation lives.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- For each base arrow, the precise Cat 2-cell hom type containing the two
sides of the stored v2.18 modification-naturality equation is a subsingleton.

This is local to the chosen factor morphism and to the single source/target pair
appearing in the v2.23 square; it does not require the whole raw target fiber to
be thin. -/
def StoredV2_18NaturalityHomSubsingleton
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K) : Prop :=
  ∀ {X Y : Context} (f : X ⟶ Y),
    Subsingleton
      (((restrictHigherLocalizedSystem W H.lift).map f.toLoc ≫
          (restrictHigherLocalizedStrongTrans (W := W) alpha.hom ≫
            K.comparison).app (.mk Y)) ⟶
        (H.comparison.app (.mk X) ≫ R.map f.toLoc))

/-- Local 2-cell uniqueness forces the stored v2.18 naturality equation. -/
theorem storedV2_18TriangleIsModificationNatural_of_local2CellRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K)
    (hRigid : StoredV2_18NaturalityHomSubsingleton (W := W) alpha) :
    StoredV2_18TriangleIsModificationNatural (W := W) alpha := by
  intro X Y f
  letI := hRigid f
  exact Subsingleton.elim _ _

/-- Fiberwise thinness from v2.45 implies the strictly more local v2.46
subsingleton condition. -/
theorem storedV2_18NaturalityHomSubsingleton_of_fiberwiseThin
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (hThin : HigherRawFiberwiseThin R)
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K) :
    StoredV2_18NaturalityHomSubsingleton (W := W) alpha := by
  intro X Y f
  letI : Quiver.IsThin (R.obj (.mk Y)) := hThin Y
  exact subsingleton_catHom₂_of_targetThin _ _

/-- Uniform local 2-cell rigidity for all v2.18 factors into one coherent chosen
carrier. -/
def HigherStoredV2_18NaturalityHomSubsingleton
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∀ (H : HigherLocalizationFactorization (W := W) R)
    (alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),
    StoredV2_18NaturalityHomSubsingleton (W := W) alpha

/-- Uniform local 2-cell rigidity implies uniform stored-triangle modification
naturality. -/
theorem higherStoredV2_18TriangleModificationNaturality_of_local2CellRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hRigid : HigherStoredV2_18NaturalityHomSubsingleton (W := W) U) :
    HigherStoredV2_18TriangleModificationNaturality (W := W) U := by
  intro H alpha
  exact storedV2_18TriangleIsModificationNatural_of_local2CellRigidity
    (W := W) alpha (hRigid H alpha)

/-- The v2.45 fiberwise-thin route factors through the local v2.46 rigidity
interface. -/
theorem higherStoredV2_18NaturalityHomSubsingleton_of_fiberwiseThin
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (hThin : HigherRawFiberwiseThin R)
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherStoredV2_18NaturalityHomSubsingleton (W := W) U := by
  intro H alpha
  exact storedV2_18NaturalityHomSubsingleton_of_fiberwiseThin
    (W := W) hThin alpha

/-- Local 2-cell rigidity makes factor-coherence lifting automatic. -/
theorem higherFactorCoherenceLifting_of_local2CellRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hRigid : HigherStoredV2_18NaturalityHomSubsingleton (W := W) U) :
    HigherFactorCoherenceLifting (W := W) U :=
  higherFactorCoherenceLifting_of_storedTriangleNaturality
    W U
      (higherStoredV2_18TriangleModificationNaturality_of_local2CellRigidity
        (W := W) U hRigid)

/-- Hence coherent universal data plus local 2-cell rigidity give the full v2.18
weak universal property on the same chosen carrier. -/
theorem hasWeakHigherLocalizationUniversalProperty_of_local2CellRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hRigid : HigherStoredV2_18NaturalityHomSubsingleton (W := W) U) :
    HasWeakHigherLocalizationUniversalProperty (W := W) R := by
  exact ⟨weakHigherLocalizationUniversalPropertyOfCoherent
    W U (higherFactorCoherenceLifting_of_local2CellRigidity
      (W := W) U hRigid)⟩

/-- The Stage III route obstruction also disappears under the same local
2-cell-rigidity hypothesis. -/
theorem higherCoherentRouteCompleteness_of_local2CellRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hRigid : HigherStoredV2_18NaturalityHomSubsingleton (W := W) U) :
    HigherCoherentRouteCompleteness (W := W) U := by
  intro _hUniversal
  apply
    (higherStoredTriangleCorrectionLifting_iff_modificationTriangleLifting
      (W := W) U).mpr
  exact
    higherFactorModificationTriangleLifting_of_storedTriangleNaturality
      W U
        (higherStoredV2_18TriangleModificationNaturality_of_local2CellRigidity
          (W := W) U hRigid)

/-- Local 2-cell rigidity gives the aligned state in the v2.42 classification. -/
theorem higherWeakCoherentAlignment_of_local2CellRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hRigid : HigherStoredV2_18NaturalityHomSubsingleton (W := W) U) :
    HigherWeakCoherentAlignment (W := W) U :=
  ⟨hasWeakHigherLocalizationUniversalProperty_of_local2CellRigidity
      (W := W) U hRigid,
    higherCoherentRouteCompleteness_of_local2CellRigidity
      (W := W) U hRigid⟩

/-- Exact local E/R obstruction elimination under the minimal ambient 2-cell
uniqueness condition used by the v2.23 stored naturality square. -/
theorem no_twoAxisObstruction_of_local2CellRigidity
    {R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hRigid : HigherStoredV2_18NaturalityHomSubsingleton (W := W) U) :
    ¬ HigherWeakCoherentTwoAxisObstruction (W := W) U :=
  (higherWeakCoherentAlignment_iff_no_twoAxisObstruction
    (W := W) U).mp
      (higherWeakCoherentAlignment_of_local2CellRigidity
        (W := W) U hRigid)

end KUOS.DependentOriginationLocal2CellRigidityObstructionEliminationV2_46
