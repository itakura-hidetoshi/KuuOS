import KUOS.DependentOriginationExactUniversalMappingAssociatorV4_65
import Mathlib

namespace KUOS.DependentOriginationExactUniversalMappingUnitorsV4_66

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

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Compatible source unitors v4.66

v4.65 constructs the compatible associator.  This file constructs the two
compatible unitor homs.

As with the associator, the induced DO₂ bicategory is never expanded inside a
large dependent goal.  Its unitors are exposed through small
`InducedBicategory.mkHom₂` wrappers, restriction is proved only in the ambient
pseudofunctor bicategory, and the comparison-square identities are discharged
by pure bicategory lemmas.

The result is the structural hom-level data

  lambda_f : id ; f ==> f
  rho_f    : f ; id ==> f

with raw and DO₂ components equal to the native Mathlib unitors.
-/

universe u v uH vH uB vB wB

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- Hom of the left unitor in DO₂, exposed through the induced-bicategory
constructor to avoid elaborating the whole induced bicategory instance in
restriction statements. -/
noncomputable def completion2LeftUnitorHom
    {F G : DependentOriginationCompletion2 (W := W) A}
    (f : F ⟶ G) :
    (𝟙 F ≫ f) ⟶ f :=
  CategoryTheory.Bicategory.InducedBicategory.mkHom₂
    (Pseudofunctor.StrongTrans.leftUnitor f.hom).hom

@[simp] theorem completion2LeftUnitorHom_hom
    {F G : DependentOriginationCompletion2 (W := W) A}
    (f : F ⟶ G) :
    (completion2LeftUnitorHom (W := W) A f).hom =
      (Pseudofunctor.StrongTrans.leftUnitor f.hom).hom :=
  rfl

/-- Hom of the right unitor in DO₂, exposed at the same constructor boundary. -/
noncomputable def completion2RightUnitorHom
    {F G : DependentOriginationCompletion2 (W := W) A}
    (f : F ⟶ G) :
    (f ≫ 𝟙 G) ⟶ f :=
  CategoryTheory.Bicategory.InducedBicategory.mkHom₂
    (Pseudofunctor.StrongTrans.rightUnitor f.hom).hom

@[simp] theorem completion2RightUnitorHom_hom
    {F G : DependentOriginationCompletion2 (W := W) A}
    (f : F ⟶ G) :
    (completion2RightUnitorHom (W := W) A f).hom =
      (Pseudofunctor.StrongTrans.rightUnitor f.hom).hom :=
  rfl

/-- Restriction of the ambient StrongTrans left unitor, evaluated at one
raw context object.

As in v4.65, we intentionally avoid a global equality between composed
StrongTrans types.  The component equality is definitional and keeps
definitional-equality checking shallow. -/
@[simp] theorem restrictHigherLocalizedModification_strongTransLeftUnitor_app
    {F G : HigherLocalizedDescentSystem (W := W)}
    (f : F ⟶ G)
    (X : Context) :
    (restrictHigherLocalizedModification
      (W := W) (Pseudofunctor.StrongTrans.leftUnitor f).hom).as.app
        (LocallyDiscrete.mk X) =
      (Bicategory.leftUnitor
        ((restrictHigherLocalizedStrongTrans (W := W) f).app
          (LocallyDiscrete.mk X))).hom := by
  rfl

/-- Restriction of the ambient StrongTrans right unitor, evaluated at one raw
context object. -/
@[simp] theorem restrictHigherLocalizedModification_strongTransRightUnitor_app
    {F G : HigherLocalizedDescentSystem (W := W)}
    (f : F ⟶ G)
    (X : Context) :
    (restrictHigherLocalizedModification
      (W := W) (Pseudofunctor.StrongTrans.rightUnitor f).hom).as.app
        (LocallyDiscrete.mk X) =
      (Bicategory.rightUnitor
        ((restrictHigherLocalizedStrongTrans (W := W) f).app
          (LocallyDiscrete.mk X))).hom := by
  rfl


/-- Underlying StrongTrans of the DO₂ identity lift.

This exposes exactly the projection needed by the component comparison-square
normal forms, without unfolding the induced bicategory instance inside a large
goal. -/
@[simp] theorem ExactUniversalRawMorphism.id_lift_hom
    (X : ExactUniversalRawObject (W := W) A) :
    (ExactUniversalRawMorphism.id (W := W) A X).lift.hom =
      𝟙 (higherStackObjectVal (W := W) A X.carrier) :=
  rfl

/-- Restriction of an identity StrongTrans is pointwise the identity. -/
@[simp] theorem restrictHigherLocalizedStrongTrans_id_app
    {F : HigherLocalizedDescentSystem (W := W)}
    (U : Context) :
    (restrictHigherLocalizedStrongTrans (W := W) (𝟙 F)).app
        (LocallyDiscrete.mk U) =
      𝟙 ((restrictHigherLocalizedSystem W F).obj (LocallyDiscrete.mk U)) :=
  rfl

/-- The hom of the v4.57 identity comparison square. -/
@[simp, reassoc] theorem ExactUniversalRawMorphism.id_comparison_square_hom
    (X : ExactUniversalRawObject (W := W) A) :
    (ExactUniversalRawMorphism.id
      (W := W) A X).comparison_square.hom =
      (Pseudofunctor.StrongTrans.leftUnitor
        X.presentation.comparison).hom ≫
        (Pseudofunctor.StrongTrans.rightUnitor
          X.presentation.comparison).inv :=
  rfl

/-- Componentwise form of the identity comparison square. -/
@[simp] theorem ExactUniversalRawMorphism.id_comparison_square_hom_app
    (X : ExactUniversalRawObject (W := W) A)
    (U : Context) :
    (ExactUniversalRawMorphism.id
      (W := W) A X).comparison_square.hom.as.app
        (LocallyDiscrete.mk U) =
      (Bicategory.leftUnitor
        (X.presentation.comparison.app (LocallyDiscrete.mk U))).hom ≫
      (Bicategory.rightUnitor
        (X.presentation.comparison.app (LocallyDiscrete.mk U))).inv := by
  have h :=
    congrArg
      (fun m => m.as.app (LocallyDiscrete.mk U))
      (ExactUniversalRawMorphism.id_comparison_square_hom
        (W := W) A X)
  simpa only [
    Pseudofunctor.StrongTrans.homCategory_comp_as_app,
    Pseudofunctor.StrongTrans.leftUnitor_hom_as_app,
    Pseudofunctor.StrongTrans.rightUnitor_inv_as_app
  ] using h


/-- Pure comparison-square law underlying the source left unitor. -/
private theorem leftUnitorCompositeSquare
    {B : Type uB} [Bicategory.{wB, vB} B]
    {P Q X₀ Y₀ : B}
    (rf : P ⟶ Q)
    (cQ : Q ⟶ Y₀)
    (cP : P ⟶ X₀)
    (fraw : X₀ ⟶ Y₀)
    (fsq : rf ≫ cQ ⟶ cP ≫ fraw) :
    ((Bicategory.leftUnitor rf).hom ▷ cQ) ≫
        fsq =
      (Bicategory.associator (𝟙 P) rf cQ).hom ≫
        ((𝟙 P) ◁ fsq) ≫
        (Bicategory.associator (𝟙 P) cP fraw).inv ≫
        (((Bicategory.leftUnitor cP).hom ≫
            (Bicategory.rightUnitor cP).inv) ▷ fraw) ≫
        (Bicategory.associator cP (𝟙 X₀) fraw).hom ≫
        (cP ◁ (Bicategory.leftUnitor fraw).hom) := by
  simp

/-- Pure comparison-square law underlying the source right unitor. -/
private theorem rightUnitorCompositeSquare
    {B : Type uB} [Bicategory.{wB, vB} B]
    {P Q X₀ Y₀ : B}
    (rf : P ⟶ Q)
    (cQ : Q ⟶ Y₀)
    (cP : P ⟶ X₀)
    (fraw : X₀ ⟶ Y₀)
    (fsq : rf ≫ cQ ⟶ cP ≫ fraw) :
    ((Bicategory.rightUnitor rf).hom ▷ cQ) ≫
        fsq =
      (Bicategory.associator rf (𝟙 Q) cQ).hom ≫
        (rf ◁
          ((Bicategory.leftUnitor cQ).hom ≫
            (Bicategory.rightUnitor cQ).inv)) ≫
        (Bicategory.associator rf cQ (𝟙 Y₀)).inv ≫
        (fsq ▷ (𝟙 Y₀)) ≫
        (Bicategory.associator cP fraw (𝟙 Y₀)).hom ≫
        (cP ◁ (Bicategory.rightUnitor fraw).hom) := by
  simp


/-- Component normal form for composing the mapping-property identity on the
left.  Identity wrappers are eliminated here, before entering the dependent
compatibility goal. -/
@[simp] theorem ExactUniversalRawMorphism.comp_id_left_comparison_square_hom_app
    {X Y : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    (U : Context) :
    (ExactUniversalRawMorphism.comp
      (W := W) A
      (ExactUniversalRawMorphism.id (W := W) A X)
      f).comparison_square.hom.as.app (LocallyDiscrete.mk U) =
      (Bicategory.associator
        (𝟙 ((restrictHigherLocalizedSystem W
          (higherStackObjectVal (W := W) A X.carrier)).obj
            (LocallyDiscrete.mk U)))
        ((restrictHigherLocalizedStrongTrans (W := W) f.lift.hom).app
          (LocallyDiscrete.mk U))
        (Y.presentation.comparison.app (LocallyDiscrete.mk U))).hom ≫
      (𝟙 ((restrictHigherLocalizedSystem W
          (higherStackObjectVal (W := W) A X.carrier)).obj
            (LocallyDiscrete.mk U)) ◁
        f.comparison_square.hom.as.app (LocallyDiscrete.mk U)) ≫
      (Bicategory.associator
        (𝟙 ((restrictHigherLocalizedSystem W
          (higherStackObjectVal (W := W) A X.carrier)).obj
            (LocallyDiscrete.mk U)))
        (X.presentation.comparison.app (LocallyDiscrete.mk U))
        (f.raw.app (LocallyDiscrete.mk U))).inv ≫
      (((Bicategory.leftUnitor
          (X.presentation.comparison.app (LocallyDiscrete.mk U))).hom ≫
        (Bicategory.rightUnitor
          (X.presentation.comparison.app (LocallyDiscrete.mk U))).inv) ▷
        f.raw.app (LocallyDiscrete.mk U)) ≫
      (Bicategory.associator
        (X.presentation.comparison.app (LocallyDiscrete.mk U))
        (𝟙 (X.raw.obj (LocallyDiscrete.mk U)))
        (f.raw.app (LocallyDiscrete.mk U))).hom := by
  rw [ExactUniversalRawMorphism.comp_comparison_square_hom_app]
  simp only [
    ExactUniversalRawMorphism.id_comparison_square_hom_app,
    ExactUniversalRawMorphism.id_raw,
    ExactUniversalRawMorphism.id_lift_hom,
    restrictHigherLocalizedStrongTrans_id_app,
    Pseudofunctor.StrongTrans.categoryStruct_id_app
  ]

/-- Component normal form for composing the mapping-property identity on the
right. -/
@[simp] theorem ExactUniversalRawMorphism.comp_id_right_comparison_square_hom_app
    {X Y : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    (U : Context) :
    (ExactUniversalRawMorphism.comp
      (W := W) A f
      (ExactUniversalRawMorphism.id (W := W) A Y)).comparison_square.hom.as.app
        (LocallyDiscrete.mk U) =
      (Bicategory.associator
        ((restrictHigherLocalizedStrongTrans (W := W) f.lift.hom).app
          (LocallyDiscrete.mk U))
        (𝟙 ((restrictHigherLocalizedSystem W
          (higherStackObjectVal (W := W) A Y.carrier)).obj
            (LocallyDiscrete.mk U)))
        (Y.presentation.comparison.app (LocallyDiscrete.mk U))).hom ≫
      ((restrictHigherLocalizedStrongTrans (W := W) f.lift.hom).app
          (LocallyDiscrete.mk U) ◁
        ((Bicategory.leftUnitor
          (Y.presentation.comparison.app (LocallyDiscrete.mk U))).hom ≫
        (Bicategory.rightUnitor
          (Y.presentation.comparison.app (LocallyDiscrete.mk U))).inv)) ≫
      (Bicategory.associator
        ((restrictHigherLocalizedStrongTrans (W := W) f.lift.hom).app
          (LocallyDiscrete.mk U))
        (Y.presentation.comparison.app (LocallyDiscrete.mk U))
        (𝟙 (Y.raw.obj (LocallyDiscrete.mk U)))).inv ≫
      (f.comparison_square.hom.as.app (LocallyDiscrete.mk U) ▷
        𝟙 (Y.raw.obj (LocallyDiscrete.mk U))) ≫
      (Bicategory.associator
        (X.presentation.comparison.app (LocallyDiscrete.mk U))
        (f.raw.app (LocallyDiscrete.mk U))
        (𝟙 (Y.raw.obj (LocallyDiscrete.mk U)))).hom := by
  rw [ExactUniversalRawMorphism.comp_comparison_square_hom_app]
  simp only [
    ExactUniversalRawMorphism.id_comparison_square_hom_app,
    ExactUniversalRawMorphism.id_raw,
    ExactUniversalRawMorphism.id_lift_hom,
    restrictHigherLocalizedStrongTrans_id_app,
    Pseudofunctor.StrongTrans.categoryStruct_id_app
  ]

/-- Exact component of the raw StrongTrans left unitor. -/
@[simp] theorem ExactUniversalRawMorphism.raw_leftUnitor_hom_app
    {X Y : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    (U : Context) :
    (Pseudofunctor.StrongTrans.leftUnitor f.raw).hom.as.app
        (LocallyDiscrete.mk U) =
      (Bicategory.leftUnitor (f.raw.app (LocallyDiscrete.mk U))).hom :=
  rfl

/-- Exact component of the raw StrongTrans right unitor. -/
@[simp] theorem ExactUniversalRawMorphism.raw_rightUnitor_hom_app
    {X Y : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    (U : Context) :
    (Pseudofunctor.StrongTrans.rightUnitor f.raw).hom.as.app
        (LocallyDiscrete.mk U) =
      (Bicategory.rightUnitor (f.raw.app (LocallyDiscrete.mk U))).hom :=
  rfl

/-- Compatibility equation for the source left unitor. -/
private theorem leftUnitorCompatibility
    {X Y : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    (restrictHigherLocalizedModification
        (W := W)
        (completion2LeftUnitorHom (W := W) A f.lift).hom ▷
      Y.presentation.comparison) ≫
        f.comparison_square.hom =
      (ExactUniversalRawMorphism.comp
        (W := W) A
        (ExactUniversalRawMorphism.id (W := W) A X)
        f).comparison_square.hom ≫
        (X.presentation.comparison ◁
          (Pseudofunctor.StrongTrans.leftUnitor f.raw).hom) := by
  rw [completion2LeftUnitorHom_hom]
  apply Pseudofunctor.StrongTrans.homCategory.ext
  rintro ⟨U⟩
  simp only [
    Pseudofunctor.StrongTrans.homCategory_comp_as_app,
    Pseudofunctor.StrongTrans.whiskerLeft_as_app,
    Pseudofunctor.StrongTrans.whiskerRight_as_app,
    restrictHigherLocalizedModification_strongTransLeftUnitor_app,
    ExactUniversalRawMorphism.comp_id_left_comparison_square_hom_app,
    ExactUniversalRawMorphism.raw_leftUnitor_hom_app
  ]
  exact
    leftUnitorCompositeSquare
      (rf :=
        (restrictHigherLocalizedStrongTrans (W := W) f.lift.hom).app
          (LocallyDiscrete.mk U))
      (cQ := Y.presentation.comparison.app (LocallyDiscrete.mk U))
      (cP := X.presentation.comparison.app (LocallyDiscrete.mk U))
      (fraw := f.raw.app (LocallyDiscrete.mk U))
      (fsq := f.comparison_square.hom.as.app (LocallyDiscrete.mk U))

/-- Compatibility equation for the source right unitor. -/
private theorem rightUnitorCompatibility
    {X Y : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    (restrictHigherLocalizedModification
        (W := W)
        (completion2RightUnitorHom (W := W) A f.lift).hom ▷
      Y.presentation.comparison) ≫
        f.comparison_square.hom =
      (ExactUniversalRawMorphism.comp
        (W := W) A f
        (ExactUniversalRawMorphism.id (W := W) A Y)).comparison_square.hom ≫
        (X.presentation.comparison ◁
          (Pseudofunctor.StrongTrans.rightUnitor f.raw).hom) := by
  rw [completion2RightUnitorHom_hom]
  apply Pseudofunctor.StrongTrans.homCategory.ext
  rintro ⟨U⟩
  simp only [
    Pseudofunctor.StrongTrans.homCategory_comp_as_app,
    Pseudofunctor.StrongTrans.whiskerLeft_as_app,
    Pseudofunctor.StrongTrans.whiskerRight_as_app,
    restrictHigherLocalizedModification_strongTransRightUnitor_app,
    ExactUniversalRawMorphism.comp_id_right_comparison_square_hom_app,
    ExactUniversalRawMorphism.raw_rightUnitor_hom_app
  ]
  exact
    rightUnitorCompositeSquare
      (rf :=
        (restrictHigherLocalizedStrongTrans (W := W) f.lift.hom).app
          (LocallyDiscrete.mk U))
      (cQ := Y.presentation.comparison.app (LocallyDiscrete.mk U))
      (cP := X.presentation.comparison.app (LocallyDiscrete.mk U))
      (fraw := f.raw.app (LocallyDiscrete.mk U))
      (fsq := f.comparison_square.hom.as.app (LocallyDiscrete.mk U))

/-- Compatible left unitor hom in the mapping-property source. -/
noncomputable def ExactUniversalRawMorphismTwoCell.leftUnitor
    {X Y : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    ExactUniversalRawMorphismTwoCell
      (W := W) A
      (ExactUniversalRawMorphism.comp
        (W := W) A
        (ExactUniversalRawMorphism.id (W := W) A X)
        f)
      f where
  raw := (Pseudofunctor.StrongTrans.leftUnitor f.raw).hom
  lift := completion2LeftUnitorHom (W := W) A f.lift
  compatibility :=
    leftUnitorCompatibility (W := W) A f

/-- Compatible right unitor hom in the mapping-property source. -/
noncomputable def ExactUniversalRawMorphismTwoCell.rightUnitor
    {X Y : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    ExactUniversalRawMorphismTwoCell
      (W := W) A
      (ExactUniversalRawMorphism.comp
        (W := W) A f
        (ExactUniversalRawMorphism.id (W := W) A Y))
      f where
  raw := (Pseudofunctor.StrongTrans.rightUnitor f.raw).hom
  lift := completion2RightUnitorHom (W := W) A f.lift
  compatibility :=
    rightUnitorCompatibility (W := W) A f

@[simp] theorem ExactUniversalRawMorphismTwoCell.leftUnitor_raw
    {X Y : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    (ExactUniversalRawMorphismTwoCell.leftUnitor
      (W := W) A f).raw =
      (Pseudofunctor.StrongTrans.leftUnitor f.raw).hom :=
  rfl

@[simp] theorem ExactUniversalRawMorphismTwoCell.leftUnitor_lift_hom
    {X Y : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    (ExactUniversalRawMorphismTwoCell.leftUnitor
      (W := W) A f).lift.hom =
      (Pseudofunctor.StrongTrans.leftUnitor f.lift.hom).hom :=
  rfl

@[simp] theorem ExactUniversalRawMorphismTwoCell.rightUnitor_raw
    {X Y : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    (ExactUniversalRawMorphismTwoCell.rightUnitor
      (W := W) A f).raw =
      (Pseudofunctor.StrongTrans.rightUnitor f.raw).hom :=
  rfl

@[simp] theorem ExactUniversalRawMorphismTwoCell.rightUnitor_lift_hom
    {X Y : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    (ExactUniversalRawMorphismTwoCell.rightUnitor
      (W := W) A f).lift.hom =
      (Pseudofunctor.StrongTrans.rightUnitor f.lift.hom).hom :=
  rfl

/-!
## Boundary after v4.66

The mapping-property source now has compatible hom-level associator and both
unitors, with raw and DO₂ underlying components given by Mathlib's native
bicategorical structure.

The next theorem unit should internalize the inverse structural 2-cells and
package associator/left-unitor/right-unitor as isomorphisms.  Their inverse laws,
pentagon, and triangle then reduce componentwise through v4.60 extensionality.
-/

end

end KUOS.DependentOriginationExactUniversalMappingUnitorsV4_66
