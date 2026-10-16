import KUOS.DependentOriginationExactUniversalMappingHorizontalV4_64
import Mathlib

namespace KUOS.DependentOriginationExactUniversalMappingAssociatorV4_65

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

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Compatible source associator v4.65

v4.64 closes horizontal composition and interchange.  The next structural
obligation is the associator for mapping-property 1-cells.

The proof is split into three layers:

1. a pure bicategorical composite-square operation;
2. its associativity/pentagon compatibility, with no KuuOS dependent wrappers;
3. the exact universal mapping associator, whose raw and DO₂ components are the
   native Mathlib associators.

This is the same elaboration boundary that made v4.62-v4.63 stable: structural
bicategory algebra is proved before dependent presentation data is introduced.
-/

universe u v uH vH uB vB wB

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- The pure comparison square obtained by horizontally composing two
comparison squares.  This is exactly the pasting used by
`ExactUniversalRawMorphism.comp`, stripped of all dependent wrappers. -/
private def compositeSquare
    {B : Type uB} [Bicategory.{wB, vB} B]
    {P Q R X₀ Y₀ Z₀ : B}
    (rf : P ⟶ Q)
    (rg : Q ⟶ R)
    (cR : R ⟶ Z₀)
    (cQ : Q ⟶ Y₀)
    (cP : P ⟶ X₀)
    (fraw : X₀ ⟶ Y₀)
    (graw : Y₀ ⟶ Z₀)
    (fsq : rf ≫ cQ ⟶ cP ≫ fraw)
    (gsq : rg ≫ cR ⟶ cQ ≫ graw) :
    (rf ≫ rg) ≫ cR ⟶ cP ≫ (fraw ≫ graw) :=
  (Bicategory.associator rf rg cR).hom ≫
    (rf ◁ gsq) ≫
    (Bicategory.associator rf cQ graw).inv ≫
    (fsq ▷ graw) ≫
    (Bicategory.associator cP fraw graw).hom

/-- Pure associativity law for composite comparison squares.

The left side first reassociates the three lifted 1-cells and then uses the
right-associated comparison pasting.  The right side uses the left-associated
pasting and finally reassociates the three raw 1-cells.  Bicategorical
pentagon/naturality coherence identifies the two. -/
private theorem compositeSquare_associator
    {B : Type uB} [Bicategory.{wB, vB} B]
    {P Q R S X₀ Y₀ Z₀ T₀ : B}
    (rf : P ⟶ Q)
    (rg : Q ⟶ R)
    (rh : R ⟶ S)
    (cS : S ⟶ T₀)
    (cR : R ⟶ Z₀)
    (cQ : Q ⟶ Y₀)
    (cP : P ⟶ X₀)
    (fraw : X₀ ⟶ Y₀)
    (graw : Y₀ ⟶ Z₀)
    (hraw : Z₀ ⟶ T₀)
    (fsq : rf ≫ cQ ⟶ cP ≫ fraw)
    (gsq : rg ≫ cR ⟶ cQ ≫ graw)
    (hsq : rh ≫ cS ⟶ cR ≫ hraw) :
    ((Bicategory.associator rf rg rh).hom ▷ cS) ≫
        compositeSquare
          rf (rg ≫ rh)
          cS cQ cP
          fraw (graw ≫ hraw)
          fsq
          (compositeSquare
            rg rh cS cR cQ
            graw hraw gsq hsq) =
      compositeSquare
          (rf ≫ rg) rh
          cS cR cP
          (fraw ≫ graw) hraw
          (compositeSquare
            rf rg cR cQ cP
            fraw graw fsq gsq)
          hsq ≫
        (cP ◁ (Bicategory.associator fraw graw hraw).hom) := by
  simp [compositeSquare]

/-- The DO₂ associator hom, exposed directly through the induced-bicategory
constructor.

Keeping this small constructor-level API avoids asking Lean to weak-head
normalize the full induced bicategory associator while elaborating a restriction
statement. -/
noncomputable def completion2AssociatorHom
    {F G H I : DependentOriginationCompletion2 (W := W) A}
    (f : F ⟶ G)
    (g : G ⟶ H)
    (h : H ⟶ I) :
    ((f ≫ g) ≫ h) ⟶ (f ≫ (g ≫ h)) :=
  CategoryTheory.Bicategory.InducedBicategory.mkHom₂
    (Pseudofunctor.StrongTrans.associator f.hom g.hom h.hom).hom

@[simp] theorem completion2AssociatorHom_hom
    {F G H I : DependentOriginationCompletion2 (W := W) A}
    (f : F ⟶ G)
    (g : G ⟶ H)
    (h : H ⟶ I) :
    (completion2AssociatorHom (W := W) A f g h).hom =
      (Pseudofunctor.StrongTrans.associator f.hom g.hom h.hom).hom :=
  rfl

/-- Restriction of the ambient StrongTrans associator, evaluated at one raw
context object.

The global equality between the restricted associator and the associator of
the three separately restricted StrongTrans is intentionally not stated:
although mathematically immediate, its source and target force Lean to compare
large composed StrongTrans types before componentwise reduction.  At one object
the equality is definitional and cheap. -/
@[simp] theorem restrictHigherLocalizedModification_strongTransAssociator_app
    {F G H I : HigherLocalizedDescentSystem (W := W)}
    (f : F ⟶ G)
    (g : G ⟶ H)
    (h : H ⟶ I)
    (X : Context) :
    (restrictHigherLocalizedModification
      (W := W) (Pseudofunctor.StrongTrans.associator f g h).hom).as.app (LocallyDiscrete.mk X) =
      (Bicategory.associator
        ((restrictHigherLocalizedStrongTrans (W := W) f).app (LocallyDiscrete.mk X))
        ((restrictHigherLocalizedStrongTrans (W := W) g).app (LocallyDiscrete.mk X))
        ((restrictHigherLocalizedStrongTrans (W := W) h).app (LocallyDiscrete.mk X))).hom := by
  rfl

/-- Componentwise expansion of the v4.57 composite comparison square.

The global expansion already exists in v4.62.  This component API is the form
needed for structural coherence proofs: it eliminates the StrongTrans wrapper
before bicategorical associativity is invoked. -/
@[simp] theorem ExactUniversalRawMorphism.comp_comparison_square_hom_app
    {X Y Z : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    (g : ExactUniversalRawMorphism (W := W) A Y Z)
    (U : Context) :
    (ExactUniversalRawMorphism.comp
      (W := W) A f g).comparison_square.hom.as.app (LocallyDiscrete.mk U) =
      (Bicategory.associator
        ((restrictHigherLocalizedStrongTrans (W := W) f.lift.hom).app (LocallyDiscrete.mk U))
        ((restrictHigherLocalizedStrongTrans (W := W) g.lift.hom).app (LocallyDiscrete.mk U))
        (Z.presentation.comparison.app (LocallyDiscrete.mk U))).hom ≫
      ((restrictHigherLocalizedStrongTrans (W := W) f.lift.hom).app (LocallyDiscrete.mk U) ◁
        g.comparison_square.hom.as.app (LocallyDiscrete.mk U)) ≫
      (Bicategory.associator
        ((restrictHigherLocalizedStrongTrans (W := W) f.lift.hom).app (LocallyDiscrete.mk U))
        (Y.presentation.comparison.app (LocallyDiscrete.mk U))
        (g.raw.app (LocallyDiscrete.mk U))).inv ≫
      (f.comparison_square.hom.as.app (LocallyDiscrete.mk U) ▷ g.raw.app (LocallyDiscrete.mk U)) ≫
      (Bicategory.associator
        (X.presentation.comparison.app (LocallyDiscrete.mk U))
        (f.raw.app (LocallyDiscrete.mk U))
        (g.raw.app (LocallyDiscrete.mk U))).hom := by
  have hcomp :=
    congrArg
      (fun m => m.as.app (LocallyDiscrete.mk U))
      (ExactUniversalRawMorphism.comp_comparison_square_hom
        (W := W) A f g)
  simpa only [
    Pseudofunctor.StrongTrans.homCategory_comp_as_app,
    Pseudofunctor.StrongTrans.whiskerLeft_as_app,
    Pseudofunctor.StrongTrans.whiskerRight_as_app,
    Pseudofunctor.StrongTrans.associator_hom_as_app
  ] using hcomp

/-- Compatibility equation for the source associator. -/
private theorem associatorCompatibility
    {X Y Z T : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    (g : ExactUniversalRawMorphism (W := W) A Y Z)
    (h : ExactUniversalRawMorphism (W := W) A Z T) :
    (restrictHigherLocalizedModification
        (W := W)
        (completion2AssociatorHom
          (W := W) A f.lift g.lift h.lift).hom ▷
      T.presentation.comparison) ≫
        (ExactUniversalRawMorphism.comp
          (W := W) A f
          (ExactUniversalRawMorphism.comp (W := W) A g h)).comparison_square.hom =
      (ExactUniversalRawMorphism.comp
        (W := W) A
        (ExactUniversalRawMorphism.comp (W := W) A f g)
        h).comparison_square.hom ≫
        (X.presentation.comparison ◁
          (Pseudofunctor.StrongTrans.associator f.raw g.raw h.raw).hom) := by
  rw [completion2AssociatorHom_hom]
  apply Pseudofunctor.StrongTrans.homCategory.ext
  rintro ⟨U⟩
  simp only [
    Pseudofunctor.StrongTrans.homCategory_comp_as_app,
    Pseudofunctor.StrongTrans.whiskerLeft_as_app,
    Pseudofunctor.StrongTrans.whiskerRight_as_app,
    restrictHigherLocalizedModification_strongTransAssociator_app,
    ExactUniversalRawMorphism.comp_comparison_square_hom_app,
    ExactUniversalRawMorphism.comp_raw,
    ExactUniversalRawMorphism.comp_lift,
    CategoryTheory.Bicategory.InducedBicategory.bicategory_comp_hom,
    Pseudofunctor.StrongTrans.comp_app
  ]
  simpa only [compositeSquare] using
    compositeSquare_associator
      (rf :=
        (restrictHigherLocalizedStrongTrans (W := W) f.lift.hom).app (LocallyDiscrete.mk U))
      (rg :=
        (restrictHigherLocalizedStrongTrans (W := W) g.lift.hom).app (LocallyDiscrete.mk U))
      (rh :=
        (restrictHigherLocalizedStrongTrans (W := W) h.lift.hom).app (LocallyDiscrete.mk U))
      (cS := T.presentation.comparison.app (LocallyDiscrete.mk U))
      (cR := Z.presentation.comparison.app (LocallyDiscrete.mk U))
      (cQ := Y.presentation.comparison.app (LocallyDiscrete.mk U))
      (cP := X.presentation.comparison.app (LocallyDiscrete.mk U))
      (fraw := f.raw.app (LocallyDiscrete.mk U))
      (graw := g.raw.app (LocallyDiscrete.mk U))
      (hraw := h.raw.app (LocallyDiscrete.mk U))
      (fsq := f.comparison_square.hom.as.app (LocallyDiscrete.mk U))
      (gsq := g.comparison_square.hom.as.app (LocallyDiscrete.mk U))
      (hsq := h.comparison_square.hom.as.app (LocallyDiscrete.mk U))

/-- The compatible associator 2-cell for mapping-property 1-cell composition. -/
noncomputable def ExactUniversalRawMorphismTwoCell.associator
    {X Y Z T : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    (g : ExactUniversalRawMorphism (W := W) A Y Z)
    (h : ExactUniversalRawMorphism (W := W) A Z T) :
    ExactUniversalRawMorphismTwoCell
      (W := W) A
      (ExactUniversalRawMorphism.comp
        (W := W) A
        (ExactUniversalRawMorphism.comp (W := W) A f g)
        h)
      (ExactUniversalRawMorphism.comp
        (W := W) A f
        (ExactUniversalRawMorphism.comp (W := W) A g h)) where
  raw := (Pseudofunctor.StrongTrans.associator f.raw g.raw h.raw).hom
  lift := completion2AssociatorHom (W := W) A f.lift g.lift h.lift
  compatibility :=
    associatorCompatibility (W := W) A f g h

@[simp] theorem ExactUniversalRawMorphismTwoCell.associator_raw
    {X Y Z T : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    (g : ExactUniversalRawMorphism (W := W) A Y Z)
    (h : ExactUniversalRawMorphism (W := W) A Z T) :
    (ExactUniversalRawMorphismTwoCell.associator
      (W := W) A f g h).raw =
      (Pseudofunctor.StrongTrans.associator f.raw g.raw h.raw).hom :=
  rfl

@[simp] theorem ExactUniversalRawMorphismTwoCell.associator_lift_hom
    {X Y Z T : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    (g : ExactUniversalRawMorphism (W := W) A Y Z)
    (h : ExactUniversalRawMorphism (W := W) A Z T) :
    (ExactUniversalRawMorphismTwoCell.associator
      (W := W) A f g h).lift.hom =
      (Pseudofunctor.StrongTrans.associator
        f.lift.hom g.lift.hom h.lift.hom).hom :=
  rfl

/-!
## Boundary after v4.65

The mapping-property source now contains a compatible associator whose raw and
DO₂ projections are the native Mathlib associators.

The next structural units are the compatible left and right unitors.  Once
their inverse 2-cells are also internalized, the pentagon and triangle laws can
be proved componentwise by the v4.60 extensionality principle, completing the
data needed for the source bicategory instance.
-/

end

end KUOS.DependentOriginationExactUniversalMappingAssociatorV4_65
