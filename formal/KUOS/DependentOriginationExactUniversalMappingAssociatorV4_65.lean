import KUOS.DependentOriginationExactUniversalMappingHorizontalV4_64
import Mathlib

namespace KUOS.DependentOriginationExactUniversalMappingAssociatorV4_65

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

/-- Restriction of the DO₂ associator is the associator of the restricted
underlying strong transformations. -/
@[simp] theorem restrictHigherLocalizedModification_completion2Associator
    {F G H I : DependentOriginationCompletion2 (W := W) A}
    (f : F ⟶ G)
    (g : G ⟶ H)
    (h : H ⟶ I) :
    restrictHigherLocalizedModification
        (W := W) ((Bicategory.associator f g h).hom).hom =
      (Bicategory.associator
        (restrictHigherLocalizedStrongTrans (W := W) f.hom)
        (restrictHigherLocalizedStrongTrans (W := W) g.hom)
        (restrictHigherLocalizedStrongTrans (W := W) h.hom)).hom := by
  apply Pseudofunctor.StrongTrans.homCategory.ext
  intro X
  rfl

/-- The v4.57 comparison square is exactly the pure `compositeSquare`
construction. -/
private theorem compComparisonSquare_eq_compositeSquare
    {X Y Z : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    (g : ExactUniversalRawMorphism (W := W) A Y Z) :
    (ExactUniversalRawMorphism.comp
      (W := W) A f g).comparison_square.hom =
      compositeSquare
        (restrictHigherLocalizedStrongTrans (W := W) f.lift.hom)
        (restrictHigherLocalizedStrongTrans (W := W) g.lift.hom)
        Z.presentation.comparison
        Y.presentation.comparison
        X.presentation.comparison
        f.raw
        g.raw
        f.comparison_square.hom
        g.comparison_square.hom := by
  simpa [compositeSquare] using
    ExactUniversalRawMorphism.comp_comparison_square_hom
      (W := W) A f g

/-- Compatibility equation for the source associator. -/
private theorem associatorCompatibility
    {X Y Z T : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    (g : ExactUniversalRawMorphism (W := W) A Y Z)
    (h : ExactUniversalRawMorphism (W := W) A Z T) :
    (restrictHigherLocalizedModification
        (W := W)
        ((Bicategory.associator f.lift g.lift h.lift).hom).hom ▷
      T.presentation.comparison) ≫
        (ExactUniversalRawMorphism.comp
          (W := W) A f
          (ExactUniversalRawMorphism.comp (W := W) A g h)).comparison_square.hom =
      (ExactUniversalRawMorphism.comp
        (W := W) A
        (ExactUniversalRawMorphism.comp (W := W) A f g)
        h).comparison_square.hom ≫
        (X.presentation.comparison ◁
          (Bicategory.associator f.raw g.raw h.raw).hom) := by
  rw [restrictHigherLocalizedModification_completion2Associator]
  rw [
    compComparisonSquare_eq_compositeSquare
      (W := W) A f
      (ExactUniversalRawMorphism.comp (W := W) A g h),
    compComparisonSquare_eq_compositeSquare
      (W := W) A
      (ExactUniversalRawMorphism.comp (W := W) A f g) h,
    compComparisonSquare_eq_compositeSquare
      (W := W) A g h,
    compComparisonSquare_eq_compositeSquare
      (W := W) A f g
  ]
  simpa using
    compositeSquare_associator
      (rf := restrictHigherLocalizedStrongTrans (W := W) f.lift.hom)
      (rg := restrictHigherLocalizedStrongTrans (W := W) g.lift.hom)
      (rh := restrictHigherLocalizedStrongTrans (W := W) h.lift.hom)
      (cS := T.presentation.comparison)
      (cR := Z.presentation.comparison)
      (cQ := Y.presentation.comparison)
      (cP := X.presentation.comparison)
      (fraw := f.raw)
      (graw := g.raw)
      (hraw := h.raw)
      (fsq := f.comparison_square.hom)
      (gsq := g.comparison_square.hom)
      (hsq := h.comparison_square.hom)

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
  raw := (Bicategory.associator f.raw g.raw h.raw).hom
  lift := (Bicategory.associator f.lift g.lift h.lift).hom
  compatibility :=
    associatorCompatibility (W := W) A f g h

@[simp] theorem ExactUniversalRawMorphismTwoCell.associator_raw
    {X Y Z T : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    (g : ExactUniversalRawMorphism (W := W) A Y Z)
    (h : ExactUniversalRawMorphism (W := W) A Z T) :
    (ExactUniversalRawMorphismTwoCell.associator
      (W := W) A f g h).raw =
      (Bicategory.associator f.raw g.raw h.raw).hom :=
  rfl

@[simp] theorem ExactUniversalRawMorphismTwoCell.associator_lift
    {X Y Z T : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    (g : ExactUniversalRawMorphism (W := W) A Y Z)
    (h : ExactUniversalRawMorphism (W := W) A Z T) :
    (ExactUniversalRawMorphismTwoCell.associator
      (W := W) A f g h).lift =
      (Bicategory.associator f.lift g.lift h.lift).hom :=
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
