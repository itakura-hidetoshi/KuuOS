import KUOS.DependentOriginationExactUniversalTargetDO2EquivalenceV4_56
import KUOS.DependentOriginationExactUniversalTargetNaturalityV4_55
import KUOS.DependentOriginationExactPresentationComparisonV4_52
import Mathlib

namespace KUOS.DependentOriginationExactUniversalMappingMorphismV4_57

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationForwardFactorCoherenceSelectionV2_40
open KUOS.DependentOriginationExactHigherPresentationSectorV4_50
open KUOS.DependentOriginationExactPresentationComparisonV4_52
open KUOS.DependentOriginationExactPresentationEssentialUniquenessV4_53
open KUOS.DependentOriginationExactUniversalTargetNaturalityV4_55
open KUOS.DependentOriginationExactUniversalTargetDO2EquivalenceV4_56

open scoped CategoryTheory.Pseudofunctor.StrongTrans

set_option autoImplicit false

noncomputable section

/-!
# Mapping-property 1-cell interface v4.57

The weak admissible sector is too large to carry a universal realization:
the octahedral counterexample is weakly W-admissible but has no exact
localization factorization.

Accordingly the positive mapping-property source must remember enough structure
to lie in the exact universal sector.

An object in this file consists of

* a raw Cat-valued higher contextual system R;
* an exact DO₂ presentation Q_R of R;
* a coherent universal-target witness for Q_R.

A 1-cell X --> Y consists of

* a raw StrongTrans eta : X.raw --> Y.raw;
* a DO₂ 1-cell F : Q_X --> Q_Y;
* an invertible modification filling the comparison square

    restrict(F) ≫ c_Y  ≅  c_X ≫ eta.

This is the natural comma-style morphism interface required before constructing
a realization pseudofunctor.  Identity and composition are proved below using
only bicategorical unitors, associators, and whiskering.

No final mapping-property equivalence is asserted yet.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- Positive raw objects equipped with a chosen exact coherent universal
presentation. -/
structure ExactUniversalRawObject where
  raw :
    RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)
  presentation :
    ExactHigherDependentOriginationPresentation
      (W := W) A raw
  universal :
    ExactPresentationCoherentUniversalTarget
      (W := W) A presentation

/-- The chosen object of DO₂ carried by an exact universal raw object. -/
abbrev ExactUniversalRawObject.carrier
    (X : ExactUniversalRawObject (W := W) A) :
    DependentOriginationCompletion2 (W := W) A :=
  X.presentation.carrier

/-- Every exact universal raw object is weakly W-admissible. -/
theorem ExactUniversalRawObject.isHigherWAdmissible
    (X : ExactUniversalRawObject (W := W) A) :
    IsHigherWAdmissible W X.raw :=
  exactPresentation_isHigherWAdmissible
    (W := W) A X.raw X.presentation

/-- A mapping-property 1-cell between exact universal raw objects.

The comparison square is an invertible modification in the raw pseudofunctor
bicategory. -/
structure ExactUniversalRawMorphism
    (X Y : ExactUniversalRawObject (W := W) A) where
  raw : X.raw ⟶ Y.raw
  lift : X.carrier ⟶ Y.carrier
  comparison_square :
    (restrictHigherLocalizedStrongTrans (W := W) lift.hom ≫
      Y.presentation.comparison) ≅
    (X.presentation.comparison ≫ raw)

/-- Identity mapping-property 1-cell. -/
noncomputable def ExactUniversalRawMorphism.id
    (X : ExactUniversalRawObject (W := W) A) :
    ExactUniversalRawMorphism (W := W) A X X where
  raw := 𝟙 X.raw
  lift := 𝟙 X.carrier
  comparison_square := by
    change
      (𝟙 _ ≫ X.presentation.comparison) ≅
        (X.presentation.comparison ≫ 𝟙 _)
    exact
      Bicategory.leftUnitor X.presentation.comparison ≪≫
        (Bicategory.rightUnitor X.presentation.comparison).symm

/-- Composition of mapping-property 1-cells.

The comparison square is obtained by reassociating, whiskering the second
square by the restricted first lift, reassociating back, whiskering the first
square by the second raw map, and then applying the final associator. -/
noncomputable def ExactUniversalRawMorphism.comp
    {X Y Z : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    (g : ExactUniversalRawMorphism (W := W) A Y Z) :
    ExactUniversalRawMorphism (W := W) A X Z where
  raw := f.raw ≫ g.raw
  lift := f.lift ≫ g.lift
  comparison_square := by
    change
      ((restrictHigherLocalizedStrongTrans (W := W) f.lift.hom ≫
          restrictHigherLocalizedStrongTrans (W := W) g.lift.hom) ≫
        Z.presentation.comparison) ≅
      (X.presentation.comparison ≫ (f.raw ≫ g.raw))
    exact
      Bicategory.associator
          (restrictHigherLocalizedStrongTrans (W := W) f.lift.hom)
          (restrictHigherLocalizedStrongTrans (W := W) g.lift.hom)
          Z.presentation.comparison ≪≫
        Bicategory.whiskerLeftIso
          (restrictHigherLocalizedStrongTrans (W := W) f.lift.hom)
          g.comparison_square ≪≫
        (Bicategory.associator
          (restrictHigherLocalizedStrongTrans (W := W) f.lift.hom)
          Y.presentation.comparison
          g.raw).symm ≪≫
        Bicategory.whiskerRightIso
          f.comparison_square g.raw ≪≫
        Bicategory.associator
          X.presentation.comparison f.raw g.raw

@[simp] theorem ExactUniversalRawMorphism.id_raw
    (X : ExactUniversalRawObject (W := W) A) :
    (ExactUniversalRawMorphism.id (W := W) A X).raw =
      𝟙 X.raw :=
  rfl

@[simp] theorem ExactUniversalRawMorphism.id_lift
    (X : ExactUniversalRawObject (W := W) A) :
    (ExactUniversalRawMorphism.id (W := W) A X).lift =
      𝟙 X.carrier :=
  rfl

@[simp] theorem ExactUniversalRawMorphism.comp_raw
    {X Y Z : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    (g : ExactUniversalRawMorphism (W := W) A Y Z) :
    (ExactUniversalRawMorphism.comp (W := W) A f g).raw =
      f.raw ≫ g.raw :=
  rfl

@[simp] theorem ExactUniversalRawMorphism.comp_lift
    {X Y Z : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    (g : ExactUniversalRawMorphism (W := W) A Y Z) :
    (ExactUniversalRawMorphism.comp (W := W) A f g).lift =
      f.lift ≫ g.lift :=
  rfl

/-- Forget the raw comparison data and retain the realized DO₂ 1-cell. -/
abbrev ExactUniversalRawMorphism.toCompletion2Hom
    {X Y : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    X.carrier ⟶ Y.carrier :=
  f.lift

@[simp] theorem ExactUniversalRawMorphism.toCompletion2Hom_id
    (X : ExactUniversalRawObject (W := W) A) :
    (ExactUniversalRawMorphism.id (W := W) A X).toCompletion2Hom =
      𝟙 X.carrier :=
  rfl

@[simp] theorem ExactUniversalRawMorphism.toCompletion2Hom_comp
    {X Y Z : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    (g : ExactUniversalRawMorphism (W := W) A Y Z) :
    (ExactUniversalRawMorphism.comp (W := W) A f g).toCompletion2Hom =
      f.toCompletion2Hom ≫ g.toCompletion2Hom :=
  rfl

/-!
## Boundary after v4.57

The positive universal sector now has an explicit mapping-property 1-cell
interface, with identity and composition, and a composition-preserving
projection to DO₂ 1-cells.

The next layer must add 2-cells between these morphisms and verify their
vertical/horizontal compositions.  After that, the object/1-cell/2-cell data can
be assembled into the source bicategory and the realization pseudofunctor.
-/

end

end KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
