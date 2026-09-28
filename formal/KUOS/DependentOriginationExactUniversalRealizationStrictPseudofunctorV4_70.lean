import KUOS.DependentOriginationExactUniversalMappingBicategoryV4_69
import Mathlib.CategoryTheory.Bicategory.Functor.StrictPseudofunctor
import Mathlib

namespace KUOS.DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMappingTwoCellV4_58
open KUOS.DependentOriginationExactUniversalMappingTwoCellVerticalV4_59
open KUOS.DependentOriginationExactUniversalMappingHomCategoryV4_60
open KUOS.DependentOriginationExactUniversalMappingLeftWhiskerV4_62
open KUOS.DependentOriginationExactUniversalMappingRightWhiskerV4_63
open KUOS.DependentOriginationExactUniversalMappingAssociatorV4_65
open KUOS.DependentOriginationExactUniversalMappingUnitorsV4_66
open KUOS.DependentOriginationExactUniversalMappingStructuralIsoV4_67
open KUOS.DependentOriginationExactUniversalMappingCoherenceV4_68
open KUOS.DependentOriginationExactUniversalMappingBicategoryV4_69

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Strict DO₂ realization pseudofunctor v4.70

The source bicategory of v4.69 was designed so that its chosen DO₂ realization
is already strict on identities and composition:

* source object X maps to X.carrier;
* source 1-cell f maps to f.lift;
* source 2-cell eta maps to eta.lift;
* the lift of source identity is definitionally the DO₂ identity;
* the lift of source composition is definitionally DO₂ composition.

Likewise the source whiskerings and structural cells were constructed with DO₂
projection equal to the native induced-bicategory operations.  Hence the
realization is not merely a pseudofunctor: it is a Mathlib
\`StrictPseudofunctor\`.

This packages the mapping-level coherence without adding any presentation
hypothesis or comparison coefficient.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- The strict realization core from the exact universal mapping source into
the chosen DO₂ carrier. -/
noncomputable def exactUniversalRealizationStrictCore :
    StrictPseudofunctorCore
      (ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
      (DependentOriginationCompletion2 (W := W) A) where
  obj X := X.carrier
  map f := f.lift
  map_id X := rfl
  map₂ eta := eta.lift
  map₂_id f := rfl
  map₂_comp eta theta := rfl
  map_comp f g := rfl

  map₂_whisker_left := by
    intro X Y Z f g g' eta
    simp only [eqToHom_refl, Category.id_comp, Category.comp_id]
    rfl

  map₂_whisker_right := by
    intro X Y Z f f' eta g
    simp only [eqToHom_refl, Category.id_comp, Category.comp_id]
    rfl

  map₂_left_unitor := by
    intro X Y f
    simp only [eqToHom_refl, Category.id_comp]
    rfl

  map₂_right_unitor := by
    intro X Y f
    simp only [eqToHom_refl, Category.id_comp]
    rfl

  map₂_associator := by
    intro X Y Z T f g h
    simp only [eqToHom_refl, Category.id_comp, Category.comp_id]
    rfl

/-- The DO₂ realization of the exact universal mapping source is a strict
pseudofunctor. -/
noncomputable def exactUniversalRealization :
    StrictPseudofunctor
      (ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
      (DependentOriginationCompletion2 (W := W) A) :=
  StrictPseudofunctor.mk'
    (exactUniversalRealizationStrictCore (W := W) A)

@[simp] theorem exactUniversalRealization_obj
    (X : ExactUniversalRawObject (W := W) A) :
    (exactUniversalRealization (W := W) A).obj X = X.carrier :=
  rfl

@[simp] theorem exactUniversalRealization_map
    {X Y : ExactUniversalRawObject (W := W) A}
    (f : X ⟶ Y) :
    (exactUniversalRealization (W := W) A).map f = f.lift :=
  rfl

@[simp] theorem exactUniversalRealization_map₂
    {X Y : ExactUniversalRawObject (W := W) A}
    {f g : X ⟶ Y}
    (eta : f ⟶ g) :
    (exactUniversalRealization (W := W) A).map₂ eta = eta.lift :=
  rfl

@[simp] theorem exactUniversalRealization_map_id
    (X : ExactUniversalRawObject (W := W) A) :
    (exactUniversalRealization (W := W) A).map (𝟙 X) =
      𝟙 X.carrier :=
  rfl

@[simp] theorem exactUniversalRealization_map_comp
    {X Y Z : ExactUniversalRawObject (W := W) A}
    (f : X ⟶ Y)
    (g : Y ⟶ Z) :
    (exactUniversalRealization (W := W) A).map (f ≫ g) =
      (exactUniversalRealization (W := W) A).map f ≫
        (exactUniversalRealization (W := W) A).map g :=
  rfl

/-!
## Boundary after v4.70

The exact universal mapping source now carries a genuine bicategory structure,
and its chosen exact presentation defines a strict pseudofunctor into DO₂.

The next universality layer can therefore be formulated at mapping level
without rebuilding object/1-cell/2-cell coherence.  The remaining mathematical
obligations are existence, coherent essential uniqueness, and naturality of
the relevant realization/factor maps, together with explicit variance and
authority hypotheses for the final dependent-origination classification
statement.
-/

end

end KUOS.DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70
