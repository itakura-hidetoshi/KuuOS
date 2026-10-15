import KUOS.DependentOriginationExactUniversalMappingUnitorsV4_66
import Mathlib

namespace KUOS.DependentOriginationExactUniversalMappingStructuralIsoV4_67

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMappingTwoCellV4_58
open KUOS.DependentOriginationExactUniversalMappingTwoCellVerticalV4_59
open KUOS.DependentOriginationExactUniversalMappingHomCategoryV4_60
open KUOS.DependentOriginationExactUniversalRestrictionWhiskeringV4_61
open KUOS.DependentOriginationExactUniversalMappingLeftWhiskerV4_62
open KUOS.DependentOriginationExactUniversalMappingRightWhiskerV4_63
open KUOS.DependentOriginationExactUniversalMappingHorizontalV4_64
open KUOS.DependentOriginationExactUniversalMappingAssociatorV4_65
open KUOS.DependentOriginationExactUniversalMappingUnitorsV4_66

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Structural inverse 2-cells and isomorphisms v4.67

v4.65 and v4.66 construct the compatible homs of the source associator and
unitors.  This file closes those structural cells under inverses and packages
them as isomorphisms in the v4.60 hom categories.

The key point is generic.  A compatible mapping-property 2-cell whose raw and
DO₂ projections are the homs of isomorphisms has a compatible inverse.  The
proof uses only:

* the stored comparison-square compatibility of the hom;
* functoriality of restriction under vertical composition from v4.59;
* bicategorical whiskering of inverse pairs.

Thus the inverse structural cells do not repeat the large dependent pasting
proofs from v4.65-v4.66.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-!
## DO₂ structural isomorphisms

These small constructor-level wrappers expose both hom and inverse without
forcing Lean to normalize the full induced bicategory instance.
-/

/-- DO₂ associator as an isomorphism in the induced hom category. -/
noncomputable def completion2AssociatorIso
    {F G H I : DependentOriginationCompletion2 (W := W) A}
    (f : F ⟶ G)
    (g : G ⟶ H)
    (h : H ⟶ I) :
    ((f ≫ g) ≫ h) ≅ (f ≫ (g ≫ h)) :=
  CategoryTheory.Bicategory.InducedBicategory.isoMk
    (Pseudofunctor.StrongTrans.associator f.hom g.hom h.hom)

@[simp] theorem completion2AssociatorIso_hom
    {F G H I : DependentOriginationCompletion2 (W := W) A}
    (f : F ⟶ G)
    (g : G ⟶ H)
    (h : H ⟶ I) :
    (completion2AssociatorIso (W := W) A f g h).hom =
      completion2AssociatorHom (W := W) A f g h :=
  rfl

@[simp] theorem completion2AssociatorIso_inv_hom
    {F G H I : DependentOriginationCompletion2 (W := W) A}
    (f : F ⟶ G)
    (g : G ⟶ H)
    (h : H ⟶ I) :
    (completion2AssociatorIso (W := W) A f g h).inv.hom =
      (Pseudofunctor.StrongTrans.associator
        f.hom g.hom h.hom).inv :=
  rfl

/-- DO₂ left unitor as an isomorphism in the induced hom category. -/
noncomputable def completion2LeftUnitorIso
    {F G : DependentOriginationCompletion2 (W := W) A}
    (f : F ⟶ G) :
    (𝟙 F ≫ f) ≅ f :=
  CategoryTheory.Bicategory.InducedBicategory.isoMk
    (Pseudofunctor.StrongTrans.leftUnitor f.hom)

@[simp] theorem completion2LeftUnitorIso_hom
    {F G : DependentOriginationCompletion2 (W := W) A}
    (f : F ⟶ G) :
    (completion2LeftUnitorIso (W := W) A f).hom =
      completion2LeftUnitorHom (W := W) A f :=
  rfl

@[simp] theorem completion2LeftUnitorIso_inv_hom
    {F G : DependentOriginationCompletion2 (W := W) A}
    (f : F ⟶ G) :
    (completion2LeftUnitorIso (W := W) A f).inv.hom =
      (Pseudofunctor.StrongTrans.leftUnitor f.hom).inv :=
  rfl

/-- DO₂ right unitor as an isomorphism in the induced hom category. -/
noncomputable def completion2RightUnitorIso
    {F G : DependentOriginationCompletion2 (W := W) A}
    (f : F ⟶ G) :
    (f ≫ 𝟙 G) ≅ f :=
  CategoryTheory.Bicategory.InducedBicategory.isoMk
    (Pseudofunctor.StrongTrans.rightUnitor f.hom)

@[simp] theorem completion2RightUnitorIso_hom
    {F G : DependentOriginationCompletion2 (W := W) A}
    (f : F ⟶ G) :
    (completion2RightUnitorIso (W := W) A f).hom =
      completion2RightUnitorHom (W := W) A f :=
  rfl

@[simp] theorem completion2RightUnitorIso_inv_hom
    {F G : DependentOriginationCompletion2 (W := W) A}
    (f : F ⟶ G) :
    (completion2RightUnitorIso (W := W) A f).inv.hom =
      (Pseudofunctor.StrongTrans.rightUnitor f.hom).inv :=
  rfl

/-!
## Generic compatible inverse

The compatibility square for the inverse is obtained by inserting the raw
hom-inverse identity on the right and the restricted lift inverse-hom identity
on the left.  This avoids any dependent rewrite through a structural
StrongTrans.
-/

private theorem compatibleInverseCompatibility
    {X Y : ExactUniversalRawObject (W := W) A}
    {f g : ExactUniversalRawMorphism (W := W) A X Y}
    (eta : ExactUniversalRawMorphismTwoCell (W := W) A f g)
    (rawIso : f.raw ≅ g.raw)
    (liftIso : f.lift ≅ g.lift)
    (hraw : eta.raw = rawIso.hom)
    (hlift : eta.lift = liftIso.hom) :
    (restrictHigherLocalizedModification
        (W := W) liftIso.inv.hom ▷
      Y.presentation.comparison) ≫
        f.comparison_square.hom =
      g.comparison_square.hom ≫
        (X.presentation.comparison ◁ rawIso.inv) := by
  have hcompat :
      (restrictHigherLocalizedModification
          (W := W) liftIso.hom.hom ▷
        Y.presentation.comparison) ≫
          g.comparison_square.hom =
        f.comparison_square.hom ≫
          (X.presentation.comparison ◁ rawIso.hom) := by
    simpa only [hraw, hlift] using eta.compatibility

  have hlift_inv_hom :
      liftIso.inv.hom ≫ liftIso.hom.hom =
        𝟙 g.lift.hom := by
    have h :=
      congrArg
        (fun m : g.lift ⟶ g.lift => m.hom)
        liftIso.inv_hom_id
    change
      liftIso.inv.hom ≫ liftIso.hom.hom =
        𝟙 g.lift.hom at h
    exact h

  have hlift_whisker :
      (restrictHigherLocalizedModification
          (W := W) liftIso.inv.hom ▷
        Y.presentation.comparison) ≫
        (restrictHigherLocalizedModification
          (W := W) liftIso.hom.hom ▷
        Y.presentation.comparison) =
      𝟙
        (restrictHigherLocalizedStrongTrans
            (W := W) g.lift.hom ≫
          Y.presentation.comparison) := by
    rw [← Bicategory.comp_whiskerRight]
    rw [← restrictHigherLocalizedModification_comp]
    rw [hlift_inv_hom]
    rw [restrictHigherLocalizedModification_id]
    simp

  have hraw_whisker :
      (X.presentation.comparison ◁ rawIso.hom) ≫
        (X.presentation.comparison ◁ rawIso.inv) =
      𝟙 (X.presentation.comparison ≫ f.raw) :=
    Bicategory.whiskerLeft_hom_inv
      X.presentation.comparison rawIso

  calc
    (restrictHigherLocalizedModification
        (W := W) liftIso.inv.hom ▷
      Y.presentation.comparison) ≫
        f.comparison_square.hom =
      ((restrictHigherLocalizedModification
          (W := W) liftIso.inv.hom ▷
        Y.presentation.comparison) ≫
          f.comparison_square.hom) ≫
        𝟙 (X.presentation.comparison ≫ f.raw) := by
          simp
    _ =
      ((restrictHigherLocalizedModification
          (W := W) liftIso.inv.hom ▷
        Y.presentation.comparison) ≫
          f.comparison_square.hom) ≫
        ((X.presentation.comparison ◁ rawIso.hom) ≫
          (X.presentation.comparison ◁ rawIso.inv)) := by
            rw [hraw_whisker]
    _ =
      ((restrictHigherLocalizedModification
          (W := W) liftIso.inv.hom ▷
        Y.presentation.comparison) ≫
          (f.comparison_square.hom ≫
            (X.presentation.comparison ◁ rawIso.hom))) ≫
        (X.presentation.comparison ◁ rawIso.inv) := by
          simp only [Category.assoc]
    _ =
      ((restrictHigherLocalizedModification
          (W := W) liftIso.inv.hom ▷
        Y.presentation.comparison) ≫
          ((restrictHigherLocalizedModification
              (W := W) liftIso.hom.hom ▷
            Y.presentation.comparison) ≫
              g.comparison_square.hom)) ≫
        (X.presentation.comparison ◁ rawIso.inv) := by
          rw [← hcompat]
    _ =
      (((restrictHigherLocalizedModification
          (W := W) liftIso.inv.hom ▷
        Y.presentation.comparison) ≫
        (restrictHigherLocalizedModification
          (W := W) liftIso.hom.hom ▷
        Y.presentation.comparison)) ≫
          g.comparison_square.hom) ≫
        (X.presentation.comparison ◁ rawIso.inv) := by
          rw [← Category.assoc]
    _ =
      g.comparison_square.hom ≫
        (X.presentation.comparison ◁ rawIso.inv) := by
          rw [hlift_whisker]
          simp

/-- Generic inverse of a compatible 2-cell whose two projections are the homs
of isomorphisms. -/
private noncomputable def compatibleInverse
    {X Y : ExactUniversalRawObject (W := W) A}
    {f g : ExactUniversalRawMorphism (W := W) A X Y}
    (eta : ExactUniversalRawMorphismTwoCell (W := W) A f g)
    (rawIso : f.raw ≅ g.raw)
    (liftIso : f.lift ≅ g.lift)
    (hraw : eta.raw = rawIso.hom)
    (hlift : eta.lift = liftIso.hom) :
    ExactUniversalRawMorphismTwoCell (W := W) A g f where
  raw := rawIso.inv
  lift := liftIso.inv
  compatibility :=
    compatibleInverseCompatibility
      (W := W) A eta rawIso liftIso hraw hlift

/-- The generic compatible inverse is a right inverse of the original
compatible 2-cell.  After v4.60 extensionality the two goals are exactly the
native inverse laws of the supplied raw and DO₂ isomorphisms. -/
private theorem compatibleInverse_hom_inv
    {X Y : ExactUniversalRawObject (W := W) A}
    {f g : ExactUniversalRawMorphism (W := W) A X Y}
    (eta : ExactUniversalRawMorphismTwoCell (W := W) A f g)
    (rawIso : f.raw ≅ g.raw)
    (liftIso : f.lift ≅ g.lift)
    (hraw : eta.raw = rawIso.hom)
    (hlift : eta.lift = liftIso.hom) :
    eta ≫
        compatibleInverse
          (W := W) A eta rawIso liftIso hraw hlift =
      𝟙 f := by
  apply ExactUniversalRawMorphismTwoCell.ext
  · change eta.raw ≫ rawIso.inv = 𝟙 f.raw
    rw [hraw]
    exact rawIso.hom_inv_id
  · change eta.lift ≫ liftIso.inv = 𝟙 f.lift
    rw [hlift]
    exact liftIso.hom_inv_id

/-- The generic compatible inverse is also a left inverse. -/
private theorem compatibleInverse_inv_hom
    {X Y : ExactUniversalRawObject (W := W) A}
    {f g : ExactUniversalRawMorphism (W := W) A X Y}
    (eta : ExactUniversalRawMorphismTwoCell (W := W) A f g)
    (rawIso : f.raw ≅ g.raw)
    (liftIso : f.lift ≅ g.lift)
    (hraw : eta.raw = rawIso.hom)
    (hlift : eta.lift = liftIso.hom) :
    compatibleInverse
          (W := W) A eta rawIso liftIso hraw hlift ≫
        eta =
      𝟙 g := by
  apply ExactUniversalRawMorphismTwoCell.ext
  · change rawIso.inv ≫ eta.raw = 𝟙 g.raw
    rw [hraw]
    exact rawIso.inv_hom_id
  · change liftIso.inv ≫ eta.lift = 𝟙 g.lift
    rw [hlift]
    exact liftIso.inv_hom_id

/-!
## Structural inverse cells
-/

/-- Compatible inverse associator in the mapping-property source. -/
noncomputable def ExactUniversalRawMorphismTwoCell.associatorInv
    {X Y Z T : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    (g : ExactUniversalRawMorphism (W := W) A Y Z)
    (h : ExactUniversalRawMorphism (W := W) A Z T) :
    ExactUniversalRawMorphismTwoCell
      (W := W) A
      (ExactUniversalRawMorphism.comp
        (W := W) A f
        (ExactUniversalRawMorphism.comp (W := W) A g h))
      (ExactUniversalRawMorphism.comp
        (W := W) A
        (ExactUniversalRawMorphism.comp (W := W) A f g)
        h) :=
  compatibleInverse
    (W := W) A
    (ExactUniversalRawMorphismTwoCell.associator (W := W) A f g h)
    (Pseudofunctor.StrongTrans.associator f.raw g.raw h.raw)
    (completion2AssociatorIso (W := W) A f.lift g.lift h.lift)
    rfl
    rfl

/-- Compatible inverse left unitor in the mapping-property source. -/
noncomputable def ExactUniversalRawMorphismTwoCell.leftUnitorInv
    {X Y : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    ExactUniversalRawMorphismTwoCell
      (W := W) A
      f
      (ExactUniversalRawMorphism.comp
        (W := W) A
        (ExactUniversalRawMorphism.id (W := W) A X)
        f) :=
  compatibleInverse
    (W := W) A
    (ExactUniversalRawMorphismTwoCell.leftUnitor (W := W) A f)
    (Pseudofunctor.StrongTrans.leftUnitor f.raw)
    (completion2LeftUnitorIso (W := W) A f.lift)
    rfl
    rfl

/-- Compatible inverse right unitor in the mapping-property source. -/
noncomputable def ExactUniversalRawMorphismTwoCell.rightUnitorInv
    {X Y : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    ExactUniversalRawMorphismTwoCell
      (W := W) A
      f
      (ExactUniversalRawMorphism.comp
        (W := W) A f
        (ExactUniversalRawMorphism.id (W := W) A Y)) :=
  compatibleInverse
    (W := W) A
    (ExactUniversalRawMorphismTwoCell.rightUnitor (W := W) A f)
    (Pseudofunctor.StrongTrans.rightUnitor f.raw)
    (completion2RightUnitorIso (W := W) A f.lift)
    rfl
    rfl

@[simp] theorem ExactUniversalRawMorphismTwoCell.associatorInv_raw
    {X Y Z T : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    (g : ExactUniversalRawMorphism (W := W) A Y Z)
    (h : ExactUniversalRawMorphism (W := W) A Z T) :
    (ExactUniversalRawMorphismTwoCell.associatorInv
      (W := W) A f g h).raw =
      (Pseudofunctor.StrongTrans.associator f.raw g.raw h.raw).inv :=
  rfl

@[simp] theorem ExactUniversalRawMorphismTwoCell.associatorInv_lift_hom
    {X Y Z T : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    (g : ExactUniversalRawMorphism (W := W) A Y Z)
    (h : ExactUniversalRawMorphism (W := W) A Z T) :
    (ExactUniversalRawMorphismTwoCell.associatorInv
      (W := W) A f g h).lift.hom =
      (Pseudofunctor.StrongTrans.associator
        f.lift.hom g.lift.hom h.lift.hom).inv :=
  rfl

@[simp] theorem ExactUniversalRawMorphismTwoCell.leftUnitorInv_raw
    {X Y : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    (ExactUniversalRawMorphismTwoCell.leftUnitorInv
      (W := W) A f).raw =
      (Pseudofunctor.StrongTrans.leftUnitor f.raw).inv :=
  rfl

@[simp] theorem ExactUniversalRawMorphismTwoCell.leftUnitorInv_lift_hom
    {X Y : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    (ExactUniversalRawMorphismTwoCell.leftUnitorInv
      (W := W) A f).lift.hom =
      (Pseudofunctor.StrongTrans.leftUnitor f.lift.hom).inv :=
  rfl

@[simp] theorem ExactUniversalRawMorphismTwoCell.rightUnitorInv_raw
    {X Y : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    (ExactUniversalRawMorphismTwoCell.rightUnitorInv
      (W := W) A f).raw =
      (Pseudofunctor.StrongTrans.rightUnitor f.raw).inv :=
  rfl

@[simp] theorem ExactUniversalRawMorphismTwoCell.rightUnitorInv_lift_hom
    {X Y : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    (ExactUniversalRawMorphismTwoCell.rightUnitorInv
      (W := W) A f).lift.hom =
      (Pseudofunctor.StrongTrans.rightUnitor f.lift.hom).inv :=
  rfl

/-!
## Inverse laws and Iso packaging

The v4.60 extensionality principle reduces the source inverse laws to the raw
and DO₂ hom categories.  Both are exactly the native Mathlib structural
isomorphisms.
-/

@[simp] theorem ExactUniversalRawMorphismTwoCell.associator_hom_inv
    {X Y Z T : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    (g : ExactUniversalRawMorphism (W := W) A Y Z)
    (h : ExactUniversalRawMorphism (W := W) A Z T) :
    ExactUniversalRawMorphismTwoCell.associator (W := W) A f g h ≫
      ExactUniversalRawMorphismTwoCell.associatorInv (W := W) A f g h =
    𝟙
      (ExactUniversalRawMorphism.comp
        (W := W) A
        (ExactUniversalRawMorphism.comp (W := W) A f g)
        h) :=
  compatibleInverse_hom_inv
    (W := W) A
    (ExactUniversalRawMorphismTwoCell.associator (W := W) A f g h)
    (Pseudofunctor.StrongTrans.associator f.raw g.raw h.raw)
    (completion2AssociatorIso (W := W) A f.lift g.lift h.lift)
    rfl
    rfl

@[simp] theorem ExactUniversalRawMorphismTwoCell.associator_inv_hom
    {X Y Z T : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    (g : ExactUniversalRawMorphism (W := W) A Y Z)
    (h : ExactUniversalRawMorphism (W := W) A Z T) :
    ExactUniversalRawMorphismTwoCell.associatorInv (W := W) A f g h ≫
      ExactUniversalRawMorphismTwoCell.associator (W := W) A f g h =
    𝟙
      (ExactUniversalRawMorphism.comp
        (W := W) A f
        (ExactUniversalRawMorphism.comp (W := W) A g h)) :=
  compatibleInverse_inv_hom
    (W := W) A
    (ExactUniversalRawMorphismTwoCell.associator (W := W) A f g h)
    (Pseudofunctor.StrongTrans.associator f.raw g.raw h.raw)
    (completion2AssociatorIso (W := W) A f.lift g.lift h.lift)
    rfl
    rfl

@[simp] theorem ExactUniversalRawMorphismTwoCell.leftUnitor_hom_inv
    {X Y : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    ExactUniversalRawMorphismTwoCell.leftUnitor (W := W) A f ≫
      ExactUniversalRawMorphismTwoCell.leftUnitorInv (W := W) A f =
    𝟙
      (ExactUniversalRawMorphism.comp
        (W := W) A
        (ExactUniversalRawMorphism.id (W := W) A X)
        f) :=
  compatibleInverse_hom_inv
    (W := W) A
    (ExactUniversalRawMorphismTwoCell.leftUnitor (W := W) A f)
    (Pseudofunctor.StrongTrans.leftUnitor f.raw)
    (completion2LeftUnitorIso (W := W) A f.lift)
    rfl
    rfl

@[simp] theorem ExactUniversalRawMorphismTwoCell.leftUnitor_inv_hom
    {X Y : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    ExactUniversalRawMorphismTwoCell.leftUnitorInv (W := W) A f ≫
      ExactUniversalRawMorphismTwoCell.leftUnitor (W := W) A f =
    𝟙 f :=
  compatibleInverse_inv_hom
    (W := W) A
    (ExactUniversalRawMorphismTwoCell.leftUnitor (W := W) A f)
    (Pseudofunctor.StrongTrans.leftUnitor f.raw)
    (completion2LeftUnitorIso (W := W) A f.lift)
    rfl
    rfl

@[simp] theorem ExactUniversalRawMorphismTwoCell.rightUnitor_hom_inv
    {X Y : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    ExactUniversalRawMorphismTwoCell.rightUnitor (W := W) A f ≫
      ExactUniversalRawMorphismTwoCell.rightUnitorInv (W := W) A f =
    𝟙
      (ExactUniversalRawMorphism.comp
        (W := W) A f
        (ExactUniversalRawMorphism.id (W := W) A Y)) :=
  compatibleInverse_hom_inv
    (W := W) A
    (ExactUniversalRawMorphismTwoCell.rightUnitor (W := W) A f)
    (Pseudofunctor.StrongTrans.rightUnitor f.raw)
    (completion2RightUnitorIso (W := W) A f.lift)
    rfl
    rfl

@[simp] theorem ExactUniversalRawMorphismTwoCell.rightUnitor_inv_hom
    {X Y : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    ExactUniversalRawMorphismTwoCell.rightUnitorInv (W := W) A f ≫
      ExactUniversalRawMorphismTwoCell.rightUnitor (W := W) A f =
    𝟙 f :=
  compatibleInverse_inv_hom
    (W := W) A
    (ExactUniversalRawMorphismTwoCell.rightUnitor (W := W) A f)
    (Pseudofunctor.StrongTrans.rightUnitor f.raw)
    (completion2RightUnitorIso (W := W) A f.lift)
    rfl
    rfl

/-- Source associator packaged as an isomorphism in the v4.60 hom category. -/
noncomputable def ExactUniversalRawMorphismTwoCell.associatorIso
    {X Y Z T : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    (g : ExactUniversalRawMorphism (W := W) A Y Z)
    (h : ExactUniversalRawMorphism (W := W) A Z T) :
    ExactUniversalRawMorphism.comp
        (W := W) A
        (ExactUniversalRawMorphism.comp (W := W) A f g)
        h ≅
      ExactUniversalRawMorphism.comp
        (W := W) A f
        (ExactUniversalRawMorphism.comp (W := W) A g h) where
  hom := ExactUniversalRawMorphismTwoCell.associator (W := W) A f g h
  inv := ExactUniversalRawMorphismTwoCell.associatorInv (W := W) A f g h
  hom_inv_id :=
    ExactUniversalRawMorphismTwoCell.associator_hom_inv (W := W) A f g h
  inv_hom_id :=
    ExactUniversalRawMorphismTwoCell.associator_inv_hom (W := W) A f g h

/-- Source left unitor packaged as an isomorphism in the v4.60 hom category. -/
noncomputable def ExactUniversalRawMorphismTwoCell.leftUnitorIso
    {X Y : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    ExactUniversalRawMorphism.comp
        (W := W) A
        (ExactUniversalRawMorphism.id (W := W) A X)
        f ≅ f where
  hom := ExactUniversalRawMorphismTwoCell.leftUnitor (W := W) A f
  inv := ExactUniversalRawMorphismTwoCell.leftUnitorInv (W := W) A f
  hom_inv_id :=
    ExactUniversalRawMorphismTwoCell.leftUnitor_hom_inv (W := W) A f
  inv_hom_id :=
    ExactUniversalRawMorphismTwoCell.leftUnitor_inv_hom (W := W) A f

/-- Source right unitor packaged as an isomorphism in the v4.60 hom category. -/
noncomputable def ExactUniversalRawMorphismTwoCell.rightUnitorIso
    {X Y : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    ExactUniversalRawMorphism.comp
        (W := W) A f
        (ExactUniversalRawMorphism.id (W := W) A Y) ≅ f where
  hom := ExactUniversalRawMorphismTwoCell.rightUnitor (W := W) A f
  inv := ExactUniversalRawMorphismTwoCell.rightUnitorInv (W := W) A f
  hom_inv_id :=
    ExactUniversalRawMorphismTwoCell.rightUnitor_hom_inv (W := W) A f
  inv_hom_id :=
    ExactUniversalRawMorphismTwoCell.rightUnitor_inv_hom (W := W) A f

@[simp] theorem ExactUniversalRawMorphismTwoCell.associatorIso_hom
    {X Y Z T : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    (g : ExactUniversalRawMorphism (W := W) A Y Z)
    (h : ExactUniversalRawMorphism (W := W) A Z T) :
    (ExactUniversalRawMorphismTwoCell.associatorIso
      (W := W) A f g h).hom =
      ExactUniversalRawMorphismTwoCell.associator (W := W) A f g h :=
  rfl

@[simp] theorem ExactUniversalRawMorphismTwoCell.associatorIso_inv
    {X Y Z T : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    (g : ExactUniversalRawMorphism (W := W) A Y Z)
    (h : ExactUniversalRawMorphism (W := W) A Z T) :
    (ExactUniversalRawMorphismTwoCell.associatorIso
      (W := W) A f g h).inv =
      ExactUniversalRawMorphismTwoCell.associatorInv (W := W) A f g h :=
  rfl

@[simp] theorem ExactUniversalRawMorphismTwoCell.leftUnitorIso_hom
    {X Y : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    (ExactUniversalRawMorphismTwoCell.leftUnitorIso
      (W := W) A f).hom =
      ExactUniversalRawMorphismTwoCell.leftUnitor (W := W) A f :=
  rfl

@[simp] theorem ExactUniversalRawMorphismTwoCell.leftUnitorIso_inv
    {X Y : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    (ExactUniversalRawMorphismTwoCell.leftUnitorIso
      (W := W) A f).inv =
      ExactUniversalRawMorphismTwoCell.leftUnitorInv (W := W) A f :=
  rfl

@[simp] theorem ExactUniversalRawMorphismTwoCell.rightUnitorIso_hom
    {X Y : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    (ExactUniversalRawMorphismTwoCell.rightUnitorIso
      (W := W) A f).hom =
      ExactUniversalRawMorphismTwoCell.rightUnitor (W := W) A f :=
  rfl

@[simp] theorem ExactUniversalRawMorphismTwoCell.rightUnitorIso_inv
    {X Y : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    (ExactUniversalRawMorphismTwoCell.rightUnitorIso
      (W := W) A f).inv =
      ExactUniversalRawMorphismTwoCell.rightUnitorInv (W := W) A f :=
  rfl

/-!
## Boundary after v4.67

The mapping-property source now has associator, left unitor, and right unitor as
genuine isomorphisms in its hom categories.  Their raw and DO₂ projections are
exactly Mathlib's native bicategorical structural isomorphisms.

The next theorem unit can prove pentagon and triangle componentwise through
v4.60 extensionality.  Only after those coherence laws are closed should these
data be assembled into a source `Bicategory` instance.
-/

end

end KUOS.DependentOriginationExactUniversalMappingStructuralIsoV4_67
