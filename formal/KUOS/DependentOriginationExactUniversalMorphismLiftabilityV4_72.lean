import KUOS.DependentOriginationExactUniversalRealizationRawEquivalenceV4_71
import Mathlib

namespace KUOS.DependentOriginationExactUniversalMorphismLiftabilityV4_72

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMappingBicategoryV4_69
open KUOS.DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70
open KUOS.DependentOriginationExactUniversalRealizationRawEquivalenceV4_71

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Exact liftability boundary for arbitrary raw morphisms v4.72

The exact-universal mapping source intentionally does not contain every raw
StrongTrans.  A raw 1-cell is admitted exactly when it has

1. a DO₂ lift between the chosen exact carriers, and
2. an invertible modification filling the presentation comparison square.

This file exposes that condition as a proposition on arbitrary raw 1-cells and
proves that it is equivalent to existence of a source 1-cell lying over the
raw map.

The predicate contains the genuine obstruction rather than hiding it in a
choice of representative.  It is closed under identity and composition,
because the v4.57 source identity and composition already construct the
required compatible lifts.

Thus exact liftability is the precise composition-stable morphism boundary of
the generalized dependent-origination source.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- A raw StrongTrans between exact-universal source objects is liftable when
there exists a DO₂ 1-cell whose restriction fills the stored comparison square
up to an invertible modification. -/
def ExactUniversalRawMorphism.Liftable
    {X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A}
    (eta : X.raw ⟶ Y.raw) : Prop :=
  ∃ lift : X.carrier ⟶ Y.carrier,
    Nonempty
      ((restrictHigherLocalizedStrongTrans (W := W) lift.hom ≫
          Y.presentation.comparison) ≅
        (X.presentation.comparison ≫ eta))

/-- A raw morphism is obstructed precisely when the exact liftability witness
does not exist. -/
def ExactUniversalRawMorphism.Obstructed
    {X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A}
    (eta : X.raw ⟶ Y.raw) : Prop :=
  ¬ ExactUniversalRawMorphism.Liftable (W := W) A eta

/-- Exact liftability is equivalent to the existence of an actual mapping-
property source 1-cell whose raw projection is the prescribed map. -/
theorem ExactUniversalRawMorphism.liftable_iff_exists_sourceMorphism
    {X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A}
    (eta : X.raw ⟶ Y.raw) :
    ExactUniversalRawMorphism.Liftable (W := W) A eta ↔
      ∃ f : ExactUniversalRawMorphism (W := W) A X Y,
        f.raw = eta := by
  constructor
  · rintro ⟨lift, ⟨comparison_square⟩⟩
    refine ⟨{
      raw := eta
      lift := lift
      comparison_square := comparison_square
    }, rfl⟩
  · rintro ⟨f, hraw⟩
    refine ⟨f.lift, ⟨?_⟩⟩
    rw [← hraw]
    exact f.comparison_square

/-- The obstruction proposition is exactly nonexistence of a source 1-cell
over the prescribed raw morphism. -/
theorem ExactUniversalRawMorphism.obstructed_iff_not_exists_sourceMorphism
    {X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A}
    (eta : X.raw ⟶ Y.raw) :
    ExactUniversalRawMorphism.Obstructed (W := W) A eta ↔
      ¬ ∃ f : ExactUniversalRawMorphism (W := W) A X Y,
        f.raw = eta := by
  unfold ExactUniversalRawMorphism.Obstructed
  rw [ExactUniversalRawMorphism.liftable_iff_exists_sourceMorphism
    (W := W) A eta]

/-- Every source 1-cell witnesses liftability of its own raw projection. -/
theorem ExactUniversalRawMorphism.liftable_raw
    {X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    ExactUniversalRawMorphism.Liftable (W := W) A f.raw := by
  exact
    (ExactUniversalRawMorphism.liftable_iff_exists_sourceMorphism
      (W := W) A f.raw).2 ⟨f, rfl⟩

/-- Identity raw morphisms are liftable. -/
theorem ExactUniversalRawMorphism.liftable_id
    (X : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A) :
    ExactUniversalRawMorphism.Liftable (W := W) A (𝟙 X.raw) := by
  exact
    (ExactUniversalRawMorphism.liftable_iff_exists_sourceMorphism
      (W := W) A (𝟙 X.raw)).2
      ⟨ExactUniversalRawMorphism.id (W := W) A X, rfl⟩

/-- Exact liftability is closed under composition of arbitrary raw morphisms. -/
theorem ExactUniversalRawMorphism.Liftable.comp
    {X Y Z : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A}
    {eta : X.raw ⟶ Y.raw}
    {theta : Y.raw ⟶ Z.raw}
    (heta : ExactUniversalRawMorphism.Liftable (W := W) A eta)
    (htheta : ExactUniversalRawMorphism.Liftable (W := W) A theta) :
    ExactUniversalRawMorphism.Liftable (W := W) A (eta ≫ theta) := by
  rcases
      (ExactUniversalRawMorphism.liftable_iff_exists_sourceMorphism
        (W := W) A eta).1 heta with
    ⟨f, hf⟩
  rcases
      (ExactUniversalRawMorphism.liftable_iff_exists_sourceMorphism
        (W := W) A theta).1 htheta with
    ⟨g, hg⟩
  apply
    (ExactUniversalRawMorphism.liftable_iff_exists_sourceMorphism
      (W := W) A (eta ≫ theta)).2
  refine
    ⟨ExactUniversalRawMorphism.comp (W := W) A f g, ?_⟩
  simpa only [ExactUniversalRawMorphism.comp_raw, hf, hg]

/-- A realized source 1-cell can never be obstructed at its raw projection. -/
theorem ExactUniversalRawMorphism.not_obstructed_raw
    {X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    ¬ ExactUniversalRawMorphism.Obstructed (W := W) A f.raw := by
  intro h
  exact h (ExactUniversalRawMorphism.liftable_raw (W := W) A f)

/-!
## Boundary after v4.72

The arbitrary-morphism frontier is now exact:

  raw morphism eta
      is admitted by the generalized source
  iff
      eta has a compatible DO₂ lift.

The condition is stable under identity and composition, hence it is a genuine
morphism class rather than a one-off witness.

The next mathematical question is no longer structural coherence.  It is to
compare this exact liftability class with whichever semantic admissibility
predicate is intended for the final dependent-origination theorem:

* prove admissibility implies Liftable under explicit hypotheses; or
* exhibit the obstruction preventing such an implication.

That theorem, rather than a blanket assumption that all weakly admissible maps
lift, is the correct remaining generalization boundary.
-/

end

end KUOS.DependentOriginationExactUniversalMorphismLiftabilityV4_72
