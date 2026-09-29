import KUOS.DependentOriginationExactUniversalMappingCoherenceV4_68
import Mathlib

namespace KUOS.DependentOriginationExactUniversalMappingBicategoryV4_69

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMappingTwoCellV4_58
open KUOS.DependentOriginationExactUniversalMappingTwoCellVerticalV4_59
open KUOS.DependentOriginationExactUniversalMappingHomCategoryV4_60
open KUOS.DependentOriginationExactUniversalMappingLeftWhiskerV4_62
open KUOS.DependentOriginationExactUniversalMappingRightWhiskerV4_63
open KUOS.DependentOriginationExactUniversalMappingHorizontalV4_64
open KUOS.DependentOriginationExactUniversalMappingAssociatorV4_65
open KUOS.DependentOriginationExactUniversalMappingUnitorsV4_66
open KUOS.DependentOriginationExactUniversalMappingStructuralIsoV4_67
open KUOS.DependentOriginationExactUniversalMappingCoherenceV4_68

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Exact universal mapping source bicategory v4.69

v4.57--v4.67 construct the exact-universal mapping objects, 1-cells, compatible
2-cells, hom categories, whiskering, horizontal composition, associator and
unitors as source isomorphisms.  v4.68 proves pentagon and triangle.

This file assembles those already-closed operations into a genuine Mathlib
\`Bicategory\` instance.  Every remaining whiskering axiom is proved
componentwise using v4.60 extensionality.  The raw and DO₂ projections then
reduce to the corresponding native Mathlib bicategory law.

No new presentation-level data or weak-admissibility assumption is added.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- The exact universal mapping-property source is a genuine bicategory. -/
noncomputable instance ExactUniversalRawObject.bicategory :
    Bicategory
      (ExactUniversalRawObject.{u, v, uH, vH} (W := W) A) where
  Hom X Y :=
    ExactUniversalRawMorphism (W := W) A X Y
  id X :=
    ExactUniversalRawMorphism.id (W := W) A X
  comp f g :=
    ExactUniversalRawMorphism.comp (W := W) A f g
  homCategory X Y :=
    ExactUniversalRawMorphism.homCategory (W := W) A X Y
  whiskerLeft {_ _ _} f {_ _} eta :=
    ExactUniversalRawMorphismTwoCell.whiskerLeft (W := W) A f eta
  whiskerRight {_ _ _} {_ _} eta h :=
    ExactUniversalRawMorphismTwoCell.whiskerRight (W := W) A eta h
  associator f g h :=
    ExactUniversalRawMorphismTwoCell.associatorIso (W := W) A f g h
  leftUnitor f :=
    ExactUniversalRawMorphismTwoCell.leftUnitorIso (W := W) A f
  rightUnitor f :=
    ExactUniversalRawMorphismTwoCell.rightUnitorIso (W := W) A f

  whiskerLeft_id := by
    intro X Y Z f g
    apply ExactUniversalRawMorphismTwoCell.ext
    · simp only [
        ExactUniversalRawMorphismTwoCell.whiskerLeft_raw,
        ExactUniversalRawMorphismTwoCell.id_raw,
        ExactUniversalRawMorphism.comp_raw
      ]
      exact (Bicategory.whiskerLeft_id f.raw g.raw)
    · simp only [
        ExactUniversalRawMorphismTwoCell.whiskerLeft_lift,
        ExactUniversalRawMorphismTwoCell.id_lift,
        ExactUniversalRawMorphism.comp_lift
      ]
      exact (Bicategory.whiskerLeft_id f.lift g.lift)

  whiskerLeft_comp := by
    intro X Y Z f g h i eta theta
    apply ExactUniversalRawMorphismTwoCell.ext
    · simp only [
        ExactUniversalRawMorphismTwoCell.whiskerLeft_raw,
        ExactUniversalRawMorphismTwoCell.vcomp_raw,
        ExactUniversalRawMorphism.comp_raw
      ]
      exact (Bicategory.whiskerLeft_comp f.raw eta.raw theta.raw)
    · simp only [
        ExactUniversalRawMorphismTwoCell.whiskerLeft_lift,
        ExactUniversalRawMorphismTwoCell.vcomp_lift,
        ExactUniversalRawMorphism.comp_lift
      ]
      exact (Bicategory.whiskerLeft_comp f.lift eta.lift theta.lift)

  id_whiskerLeft := by
    intro X Y f g eta
    apply ExactUniversalRawMorphismTwoCell.ext
    · simp only [
        ExactUniversalRawMorphismTwoCell.whiskerLeft_raw,
        ExactUniversalRawMorphismTwoCell.vcomp_raw,
        ExactUniversalRawMorphism.id_raw,
        ExactUniversalRawMorphism.comp_raw,
        ExactUniversalRawMorphismTwoCell.leftUnitorIso_hom,
        ExactUniversalRawMorphismTwoCell.leftUnitorIso_inv,
        ExactUniversalRawMorphismTwoCell.leftUnitor_raw,
        ExactUniversalRawMorphismTwoCell.leftUnitorInv_raw
      ]
      exact (Bicategory.id_whiskerLeft eta.raw)
    · simp only [
        ExactUniversalRawMorphismTwoCell.whiskerLeft_lift,
        ExactUniversalRawMorphismTwoCell.vcomp_lift,
        ExactUniversalRawMorphism.id_lift,
        ExactUniversalRawMorphism.comp_lift,
        ExactUniversalRawMorphismTwoCell.leftUnitorIso_hom,
        ExactUniversalRawMorphismTwoCell.leftUnitorIso_inv
      ]
      exact (Bicategory.id_whiskerLeft eta.lift)

  comp_whiskerLeft := by
    intro X Y Z T f g h h' eta
    apply ExactUniversalRawMorphismTwoCell.ext
    · simp only [
        ExactUniversalRawMorphismTwoCell.whiskerLeft_raw,
        ExactUniversalRawMorphismTwoCell.vcomp_raw,
        ExactUniversalRawMorphism.comp_raw,
        ExactUniversalRawMorphismTwoCell.associatorIso_hom,
        ExactUniversalRawMorphismTwoCell.associatorIso_inv,
        ExactUniversalRawMorphismTwoCell.associator_raw,
        ExactUniversalRawMorphismTwoCell.associatorInv_raw
      ]
      exact (Bicategory.comp_whiskerLeft f.raw g.raw eta.raw)
    · simp only [
        ExactUniversalRawMorphismTwoCell.whiskerLeft_lift,
        ExactUniversalRawMorphismTwoCell.vcomp_lift,
        ExactUniversalRawMorphism.comp_lift,
        ExactUniversalRawMorphismTwoCell.associatorIso_hom,
        ExactUniversalRawMorphismTwoCell.associatorIso_inv
      ]
      exact (Bicategory.comp_whiskerLeft f.lift g.lift eta.lift)

  id_whiskerRight := by
    intro X Y Z f g
    apply ExactUniversalRawMorphismTwoCell.ext
    · simp only [
        ExactUniversalRawMorphismTwoCell.whiskerRight_raw,
        ExactUniversalRawMorphismTwoCell.id_raw,
        ExactUniversalRawMorphism.comp_raw
      ]
      exact (Bicategory.id_whiskerRight f.raw g.raw)
    · simp only [
        ExactUniversalRawMorphismTwoCell.whiskerRight_lift,
        ExactUniversalRawMorphismTwoCell.id_lift,
        ExactUniversalRawMorphism.comp_lift
      ]
      exact (Bicategory.id_whiskerRight f.lift g.lift)

  comp_whiskerRight := by
    intro X Y Z f g h eta theta i
    apply ExactUniversalRawMorphismTwoCell.ext
    · simp only [
        ExactUniversalRawMorphismTwoCell.whiskerRight_raw,
        ExactUniversalRawMorphismTwoCell.vcomp_raw,
        ExactUniversalRawMorphism.comp_raw
      ]
      exact (Bicategory.comp_whiskerRight eta.raw theta.raw i.raw)
    · simp only [
        ExactUniversalRawMorphismTwoCell.whiskerRight_lift,
        ExactUniversalRawMorphismTwoCell.vcomp_lift,
        ExactUniversalRawMorphism.comp_lift
      ]
      exact (Bicategory.comp_whiskerRight eta.lift theta.lift i.lift)

  whiskerRight_id := by
    intro X Y f g eta
    apply ExactUniversalRawMorphismTwoCell.ext
    · simp only [
        ExactUniversalRawMorphismTwoCell.whiskerRight_raw,
        ExactUniversalRawMorphismTwoCell.vcomp_raw,
        ExactUniversalRawMorphism.id_raw,
        ExactUniversalRawMorphism.comp_raw,
        ExactUniversalRawMorphismTwoCell.rightUnitorIso_hom,
        ExactUniversalRawMorphismTwoCell.rightUnitorIso_inv,
        ExactUniversalRawMorphismTwoCell.rightUnitor_raw,
        ExactUniversalRawMorphismTwoCell.rightUnitorInv_raw
      ]
      exact (Bicategory.whiskerRight_id eta.raw)
    · simp only [
        ExactUniversalRawMorphismTwoCell.whiskerRight_lift,
        ExactUniversalRawMorphismTwoCell.vcomp_lift,
        ExactUniversalRawMorphism.id_lift,
        ExactUniversalRawMorphism.comp_lift,
        ExactUniversalRawMorphismTwoCell.rightUnitorIso_hom,
        ExactUniversalRawMorphismTwoCell.rightUnitorIso_inv
      ]
      exact (Bicategory.whiskerRight_id eta.lift)

  whiskerRight_comp := by
    intro X Y Z T f f' eta g h
    apply ExactUniversalRawMorphismTwoCell.ext
    · simp only [
        ExactUniversalRawMorphismTwoCell.whiskerRight_raw,
        ExactUniversalRawMorphismTwoCell.vcomp_raw,
        ExactUniversalRawMorphism.comp_raw,
        ExactUniversalRawMorphismTwoCell.associatorIso_hom,
        ExactUniversalRawMorphismTwoCell.associatorIso_inv,
        ExactUniversalRawMorphismTwoCell.associator_raw,
        ExactUniversalRawMorphismTwoCell.associatorInv_raw
      ]
      exact (Bicategory.whiskerRight_comp eta.raw g.raw h.raw)
    · simp only [
        ExactUniversalRawMorphismTwoCell.whiskerRight_lift,
        ExactUniversalRawMorphismTwoCell.vcomp_lift,
        ExactUniversalRawMorphism.comp_lift,
        ExactUniversalRawMorphismTwoCell.associatorIso_hom,
        ExactUniversalRawMorphismTwoCell.associatorIso_inv
      ]
      exact (Bicategory.whiskerRight_comp eta.lift g.lift h.lift)

  whisker_assoc := by
    intro X Y Z T f g g' eta h
    apply ExactUniversalRawMorphismTwoCell.ext
    · simp only [
        ExactUniversalRawMorphismTwoCell.whiskerLeft_raw,
        ExactUniversalRawMorphismTwoCell.whiskerRight_raw,
        ExactUniversalRawMorphismTwoCell.vcomp_raw,
        ExactUniversalRawMorphism.comp_raw,
        ExactUniversalRawMorphismTwoCell.associatorIso_hom,
        ExactUniversalRawMorphismTwoCell.associatorIso_inv,
        ExactUniversalRawMorphismTwoCell.associator_raw,
        ExactUniversalRawMorphismTwoCell.associatorInv_raw
      ]
      exact (Bicategory.whisker_assoc f.raw eta.raw h.raw)
    · simp only [
        ExactUniversalRawMorphismTwoCell.whiskerLeft_lift,
        ExactUniversalRawMorphismTwoCell.whiskerRight_lift,
        ExactUniversalRawMorphismTwoCell.vcomp_lift,
        ExactUniversalRawMorphism.comp_lift,
        ExactUniversalRawMorphismTwoCell.associatorIso_hom,
        ExactUniversalRawMorphismTwoCell.associatorIso_inv
      ]
      exact (Bicategory.whisker_assoc f.lift eta.lift h.lift)

  whisker_exchange := by
    intro X Y Z f g h i eta theta
    exact
      (ExactUniversalRawMorphismTwoCell.hcomp_eq_exchange
        (W := W) A eta theta).symm

  pentagon := by
    intro X Y Z T U f g h i
    exact
      ExactUniversalRawMorphismTwoCell.pentagon
        (W := W) A f g h i

  triangle := by
    intro X Y Z f g
    exact
      ExactUniversalRawMorphismTwoCell.triangle
        (W := W) A f g

/-!
## Boundary after v4.69

The exact universal mapping source is now an actual Mathlib bicategory, not
merely a collection of separately verified coherence operations.

The next layer may therefore promote the realized DO₂ projection

  object |-> chosen exact DO₂ carrier
  1-cell |-> chosen lift
  2-cell |-> compatible lift modification

to a pseudofunctor.  Its object/1-cell/2-cell action has already been
formalized; the remaining work is to package identity/composition comparison
isomorphisms and prove the pseudofunctor coherence against this source
bicategory.
-/

end

end KUOS.DependentOriginationExactUniversalMappingBicategoryV4_69
