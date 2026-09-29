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
StrongTrans. A raw 1-cell is admitted exactly when it has a DO₂ lift between the
chosen exact carriers and an invertible presentation-comparison square.

Liftability is indexed by the chosen source objects, not just their raw systems.
Those indices are supplied explicitly below: a raw projection must not silently
select a different exact presentation of the same system.

The condition is equivalent to existence of a source 1-cell over the raw map and
is closed under identity and composition. No arbitrary weak admissibility
hypothesis is silently strengthened to exact liftability.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- A raw StrongTrans is liftable between the chosen exact-universal objects
when a DO₂ 1-cell fills their presentation square by an invertible modification. -/
def ExactUniversalRawMorphism.Liftable
    {X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A}
    (eta : X.raw ⟶ Y.raw) : Prop :=
  ∃ lift : X.carrier ⟶ Y.carrier,
    Nonempty
      ((restrictHigherLocalizedStrongTrans (W := W) lift.hom ≫
          Y.presentation.comparison) ≅
        (X.presentation.comparison ≫ eta))

/-- A raw morphism is obstructed exactly when no compatible lift exists. -/
def ExactUniversalRawMorphism.Obstructed
    {X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A}
    (eta : X.raw ⟶ Y.raw) : Prop :=
  ¬ ExactUniversalRawMorphism.Liftable (W := W) A (X := X) (Y := Y) eta

/-- Exact liftability is equivalent to existence of a source 1-cell over the
prescribed raw map, with the chosen presentations fixed. -/
theorem ExactUniversalRawMorphism.liftable_iff_exists_sourceMorphism
    {X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A}
    (eta : X.raw ⟶ Y.raw) :
    ExactUniversalRawMorphism.Liftable (W := W) A (X := X) (Y := Y) eta ↔
      ∃ f : ExactUniversalRawMorphism (W := W) A X Y,
        f.raw = eta := by
  constructor
  · rintro ⟨lift, ⟨comparison_square⟩⟩
    exact ⟨{
      raw := eta
      lift := lift
      comparison_square := comparison_square
    }, rfl⟩
  · rintro ⟨f, hraw⟩
    refine ⟨f.lift, ⟨?_⟩⟩
    rw [← hraw]
    exact f.comparison_square

/-- The obstruction is exactly nonexistence of a source 1-cell over the map. -/
theorem ExactUniversalRawMorphism.obstructed_iff_not_exists_sourceMorphism
    {X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A}
    (eta : X.raw ⟶ Y.raw) :
    ExactUniversalRawMorphism.Obstructed (W := W) A (X := X) (Y := Y) eta ↔
      ¬ ∃ f : ExactUniversalRawMorphism (W := W) A X Y,
        f.raw = eta := by
  unfold ExactUniversalRawMorphism.Obstructed
  exact not_congr (ExactUniversalRawMorphism.liftable_iff_exists_sourceMorphism
    (W := W) A (X := X) (Y := Y) eta)

/-- Every source 1-cell witnesses liftability of its own raw projection. -/
theorem ExactUniversalRawMorphism.liftable_raw
    {X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    ExactUniversalRawMorphism.Liftable (W := W) A (X := X) (Y := Y) f.raw :=
  ⟨f.lift, ⟨f.comparison_square⟩⟩

/-- Identity raw morphisms are liftable over the same chosen source object. -/
theorem ExactUniversalRawMorphism.liftable_id
    (X : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A) :
    ExactUniversalRawMorphism.Liftable (W := W) A (X := X) (Y := X) (𝟙 X.raw) :=
  ExactUniversalRawMorphism.liftable_raw (W := W) A
    (ExactUniversalRawMorphism.id (W := W) A X)

/-- Exact liftability is closed under composition of arbitrary raw morphisms. -/
theorem ExactUniversalRawMorphism.Liftable.comp
    {X Y Z : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A}
    {eta : X.raw ⟶ Y.raw}
    {theta : Y.raw ⟶ Z.raw}
    (heta : ExactUniversalRawMorphism.Liftable
      (W := W) A (X := X) (Y := Y) eta)
    (htheta : ExactUniversalRawMorphism.Liftable
      (W := W) A (X := Y) (Y := Z) theta) :
    ExactUniversalRawMorphism.Liftable
      (W := W) A (X := X) (Y := Z) (eta ≫ theta) := by
  rcases
      (ExactUniversalRawMorphism.liftable_iff_exists_sourceMorphism
        (W := W) A (X := X) (Y := Y) eta).1 heta with ⟨f, hf⟩
  rcases
      (ExactUniversalRawMorphism.liftable_iff_exists_sourceMorphism
        (W := W) A (X := Y) (Y := Z) theta).1 htheta with ⟨g, hg⟩
  apply
    (ExactUniversalRawMorphism.liftable_iff_exists_sourceMorphism
      (W := W) A (X := X) (Y := Z) (eta ≫ theta)).2
  refine ⟨ExactUniversalRawMorphism.comp (W := W) A f g, ?_⟩
  exact congrArg₂ (fun a b => a ≫ b) hf hg

/-- A realized source 1-cell cannot be obstructed at its raw projection. -/
theorem ExactUniversalRawMorphism.not_obstructed_raw
    {X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    ¬ ExactUniversalRawMorphism.Obstructed
      (W := W) A (X := X) (Y := Y) f.raw := by
  intro h
  exact h (ExactUniversalRawMorphism.liftable_raw (W := W) A f)

/-!
## Boundary after v4.72

A raw morphism is admitted by the generalized source exactly when it has a
compatible DO₂ lift between the chosen presentations. This morphism class is
stable under identity and composition.

The remaining question is to compare exact liftability with the intended
semantic admissibility predicate: prove the implication under explicit
hypotheses or exhibit the obstruction. This file does not assume that all
weakly admissible morphisms lift.
-/

end

end KUOS.DependentOriginationExactUniversalMorphismLiftabilityV4_72
