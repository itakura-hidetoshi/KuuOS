import KUOS.DependentOriginationExactUniversalMappingRightWhiskerV4_63
import Mathlib

namespace KUOS.DependentOriginationExactUniversalMappingHorizontalV4_64

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMappingTwoCellV4_58
open KUOS.DependentOriginationExactUniversalMappingTwoCellVerticalV4_59
open KUOS.DependentOriginationExactUniversalMappingHomCategoryV4_60
open KUOS.DependentOriginationExactUniversalRestrictionWhiskeringV4_61
open KUOS.DependentOriginationExactUniversalMappingLeftWhiskerV4_62
open KUOS.DependentOriginationExactUniversalMappingRightWhiskerV4_63

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Horizontal composition and interchange v4.64

v4.62 and v4.63 provide compatible left and right whiskering.  The next step
toward a genuine bicategory is to internalize horizontal composition of
mapping-property 2-cells and prove its interchange law with vertical
composition.

For

  eta   : f ==> g,     f,g : X --> Y
  theta : h ==> i,     h,i : Y --> Z,

there are two canonical pastings from f;h to g;i:

  (eta ▷ h) ; (g ◁ theta)

and

  (f ◁ theta) ; (eta ▷ i).

Mathlib's bicategorical whisker exchange identifies them.  Because v4.62-v4.63
already proved that both whiskerings preserve the exact-presentation
compatibility equation, the source-level equality now follows componentwise,
without reopening any dependent comparison-square proof.

The same pure exchange law proves the full horizontal/vertical interchange
identity.  This is the functoriality datum needed before the source associator
and unitors are installed.
-/

universe u v uH vH uB vB wB

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- Pure bicategorical horizontal/vertical interchange in the orientation used
by the exact universal mapping source. -/
private theorem horizontalInterchange
    {B : Type uB} [Bicategory.{wB, vB} B]
    {X₀ Y₀ Z₀ : B}
    {f g j : X₀ ⟶ Y₀}
    {h i k : Y₀ ⟶ Z₀}
    (eta : f ⟶ g)
    (eta' : g ⟶ j)
    (theta : h ⟶ i)
    (theta' : i ⟶ k) :
    (((eta ≫ eta') ▷ h) ≫
        (j ◁ (theta ≫ theta'))) =
      (((eta ▷ h) ≫ (g ◁ theta)) ≫
        ((eta' ▷ i) ≫ (j ◁ theta'))) := by
  rw [
    Bicategory.comp_whiskerRight,
    Bicategory.whiskerLeft_comp
  ]
  simp only [Category.assoc]
  rw [Bicategory.whisker_exchange_assoc]

/-- Pure identity law for the chosen horizontal-composition presentation. -/
private theorem horizontalIdentity
    {B : Type uB} [Bicategory.{wB, vB} B]
    {X₀ Y₀ Z₀ : B}
    (f : X₀ ⟶ Y₀)
    (h : Y₀ ⟶ Z₀) :
    ((𝟙 f) ▷ h) ≫ (f ◁ (𝟙 h)) =
      𝟙 (f ≫ h) := by
  rw [
    Bicategory.id_whiskerRight,
    Bicategory.whiskerLeft_id,
    Category.id_comp
  ]

/-- Horizontal composition of compatible mapping-property 2-cells.

We choose the right-then-left whiskering presentation.  v4.64 proves below
that the left-then-right presentation is equal to it. -/
noncomputable def ExactUniversalRawMorphismTwoCell.hcomp
    {X Y Z : ExactUniversalRawObject (W := W) A}
    {f g : ExactUniversalRawMorphism (W := W) A X Y}
    {h i : ExactUniversalRawMorphism (W := W) A Y Z}
    (eta : ExactUniversalRawMorphismTwoCell (W := W) A f g)
    (theta : ExactUniversalRawMorphismTwoCell (W := W) A h i) :
    ExactUniversalRawMorphismTwoCell
      (W := W) A
      (ExactUniversalRawMorphism.comp (W := W) A f h)
      (ExactUniversalRawMorphism.comp (W := W) A g i) :=
  ExactUniversalRawMorphismTwoCell.vcomp
    (W := W) A
    (ExactUniversalRawMorphismTwoCell.whiskerRight
      (W := W) A eta h)
    (ExactUniversalRawMorphismTwoCell.whiskerLeft
      (W := W) A g theta)

@[simp] theorem ExactUniversalRawMorphismTwoCell.hcomp_raw
    {X Y Z : ExactUniversalRawObject (W := W) A}
    {f g : ExactUniversalRawMorphism (W := W) A X Y}
    {h i : ExactUniversalRawMorphism (W := W) A Y Z}
    (eta : ExactUniversalRawMorphismTwoCell (W := W) A f g)
    (theta : ExactUniversalRawMorphismTwoCell (W := W) A h i) :
    (ExactUniversalRawMorphismTwoCell.hcomp
      (W := W) A eta theta).raw =
      (eta.raw ▷ h.raw) ≫ (g.raw ◁ theta.raw) :=
  rfl

@[simp] theorem ExactUniversalRawMorphismTwoCell.hcomp_lift
    {X Y Z : ExactUniversalRawObject (W := W) A}
    {f g : ExactUniversalRawMorphism (W := W) A X Y}
    {h i : ExactUniversalRawMorphism (W := W) A Y Z}
    (eta : ExactUniversalRawMorphismTwoCell (W := W) A f g)
    (theta : ExactUniversalRawMorphismTwoCell (W := W) A h i) :
    (ExactUniversalRawMorphismTwoCell.hcomp
      (W := W) A eta theta).lift =
      (eta.lift ▷ h.lift) ≫ (g.lift ◁ theta.lift) :=
  rfl

/-- The two canonical whiskering presentations of horizontal composition agree
inside the exact universal mapping source. -/
theorem ExactUniversalRawMorphismTwoCell.hcomp_eq_exchange
    {X Y Z : ExactUniversalRawObject (W := W) A}
    {f g : ExactUniversalRawMorphism (W := W) A X Y}
    {h i : ExactUniversalRawMorphism (W := W) A Y Z}
    (eta : ExactUniversalRawMorphismTwoCell (W := W) A f g)
    (theta : ExactUniversalRawMorphismTwoCell (W := W) A h i) :
    ExactUniversalRawMorphismTwoCell.hcomp
        (W := W) A eta theta =
      ExactUniversalRawMorphismTwoCell.vcomp
        (W := W) A
        (ExactUniversalRawMorphismTwoCell.whiskerLeft
          (W := W) A f theta)
        (ExactUniversalRawMorphismTwoCell.whiskerRight
          (W := W) A eta i) := by
  apply ExactUniversalRawMorphismTwoCell.ext
  · simpa using
      (Bicategory.whisker_exchange eta.raw theta.raw).symm
  · simpa using
      (Bicategory.whisker_exchange eta.lift theta.lift).symm

/-- Horizontal composition preserves identity 2-cells. -/
@[simp] theorem ExactUniversalRawMorphismTwoCell.hcomp_id
    {X Y Z : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    (h : ExactUniversalRawMorphism (W := W) A Y Z) :
    ExactUniversalRawMorphismTwoCell.hcomp
        (W := W) A
        (ExactUniversalRawMorphismTwoCell.id (W := W) A f)
        (ExactUniversalRawMorphismTwoCell.id (W := W) A h) =
      ExactUniversalRawMorphismTwoCell.id
        (W := W) A
        (ExactUniversalRawMorphism.comp (W := W) A f h) := by
  apply ExactUniversalRawMorphismTwoCell.ext
  · simpa using horizontalIdentity f.raw h.raw
  · simpa using horizontalIdentity f.lift h.lift

/-- Full interchange: horizontal composition carries vertical composites to the
vertical composite of horizontal composites. -/
theorem ExactUniversalRawMorphismTwoCell.hcomp_vcomp
    {X Y Z : ExactUniversalRawObject (W := W) A}
    {f g j : ExactUniversalRawMorphism (W := W) A X Y}
    {h i k : ExactUniversalRawMorphism (W := W) A Y Z}
    (eta : ExactUniversalRawMorphismTwoCell (W := W) A f g)
    (eta' : ExactUniversalRawMorphismTwoCell (W := W) A g j)
    (theta : ExactUniversalRawMorphismTwoCell (W := W) A h i)
    (theta' : ExactUniversalRawMorphismTwoCell (W := W) A i k) :
    ExactUniversalRawMorphismTwoCell.hcomp
        (W := W) A
        (ExactUniversalRawMorphismTwoCell.vcomp
          (W := W) A eta eta')
        (ExactUniversalRawMorphismTwoCell.vcomp
          (W := W) A theta theta') =
      ExactUniversalRawMorphismTwoCell.vcomp
        (W := W) A
        (ExactUniversalRawMorphismTwoCell.hcomp
          (W := W) A eta theta)
        (ExactUniversalRawMorphismTwoCell.hcomp
          (W := W) A eta' theta') := by
  apply ExactUniversalRawMorphismTwoCell.ext
  · simpa using
      horizontalInterchange
        eta.raw eta'.raw theta.raw theta'.raw
  · simpa using
      horizontalInterchange
        eta.lift eta'.lift theta.lift theta'.lift

/-!
## Boundary after v4.64

The positive universal mapping source now has:

* hom categories;
* compatible left and right whiskering;
* horizontal composition of compatible 2-cells;
* equality of the two whiskering pastings;
* identity preservation;
* full horizontal/vertical interchange.

Thus horizontal 2-cell calculus is functorial.  The next obstruction is
structural rather than local: construct compatible source associator and unitor
2-cells for `ExactUniversalRawMorphism.comp`, prove their coherence, and then
package the mapping-property source as a bicategory whose raw and DO₂
projections recover the native bicategorical structure.
-/

end

end KUOS.DependentOriginationExactUniversalMappingHorizontalV4_64
