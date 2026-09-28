import KUOS.DependentOriginationExactUniversalMappingStructuralIsoV4_67
import Mathlib

namespace KUOS.DependentOriginationExactUniversalMappingCoherenceV4_68

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

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Pentagon and triangle coherence v4.68

v4.67 packages the compatible source associator and unitors as genuine
isomorphisms in the v4.60 hom categories.  The remaining structural obligation
before installing a source bicategory is coherence.

The proof is componentwise.  v4.60 extensionality reduces equality of source
2-cells to equality of their raw and DO₂ components.  Both projections are
definitionally the native Mathlib bicategorical associator/unitors, so the two
source coherence laws reduce to \`Bicategory.pentagon\` and
\`Bicategory.triangle\`.

No presentation-level compatibility square is reopened and no new hypothesis
on exact presentations is introduced.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- The exact universal mapping source satisfies the bicategory pentagon law.

This is the source-level lift of Mathlib's native pentagon through the raw and
DO₂ projections. -/
theorem ExactUniversalRawMorphismTwoCell.pentagon
    {V X Y Z T : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A V X)
    (g : ExactUniversalRawMorphism (W := W) A X Y)
    (h : ExactUniversalRawMorphism (W := W) A Y Z)
    (i : ExactUniversalRawMorphism (W := W) A Z T) :
    ExactUniversalRawMorphismTwoCell.vcomp
      (W := W) A
      (ExactUniversalRawMorphismTwoCell.vcomp
        (W := W) A
        (ExactUniversalRawMorphismTwoCell.whiskerRight
          (W := W) A
          (ExactUniversalRawMorphismTwoCell.associator
            (W := W) A f g h)
          i)
        (ExactUniversalRawMorphismTwoCell.associator
          (W := W) A f
          (ExactUniversalRawMorphism.comp (W := W) A g h)
          i))
      (ExactUniversalRawMorphismTwoCell.whiskerLeft
        (W := W) A f
        (ExactUniversalRawMorphismTwoCell.associator
          (W := W) A g h i)) =
    ExactUniversalRawMorphismTwoCell.vcomp
      (W := W) A
      (ExactUniversalRawMorphismTwoCell.associator
        (W := W) A
        (ExactUniversalRawMorphism.comp (W := W) A f g)
        h i)
      (ExactUniversalRawMorphismTwoCell.associator
        (W := W) A f g
        (ExactUniversalRawMorphism.comp (W := W) A h i)) := by
  apply ExactUniversalRawMorphismTwoCell.ext
  · simpa only [
      ExactUniversalRawMorphismTwoCell.vcomp_raw,
      ExactUniversalRawMorphismTwoCell.whiskerRight_raw,
      ExactUniversalRawMorphismTwoCell.whiskerLeft_raw,
      ExactUniversalRawMorphismTwoCell.associator_raw,
      ExactUniversalRawMorphism.comp_raw
    ] using!
      (Bicategory.pentagon f.raw g.raw h.raw i.raw)
  · simpa only [
      ExactUniversalRawMorphismTwoCell.vcomp_lift,
      ExactUniversalRawMorphismTwoCell.whiskerRight_lift,
      ExactUniversalRawMorphismTwoCell.whiskerLeft_lift,
      ExactUniversalRawMorphism.comp_lift
    ] using!
      (Bicategory.pentagon f.lift g.lift h.lift i.lift)

/-- The exact universal mapping source satisfies the bicategory triangle law.

Again, source extensionality leaves exactly the native raw and DO₂ triangle
equations. -/
theorem ExactUniversalRawMorphismTwoCell.triangle
    {X Y Z : ExactUniversalRawObject (W := W) A}
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    (g : ExactUniversalRawMorphism (W := W) A Y Z) :
    ExactUniversalRawMorphismTwoCell.vcomp
      (W := W) A
      (ExactUniversalRawMorphismTwoCell.associator
        (W := W) A f
        (ExactUniversalRawMorphism.id (W := W) A Y)
        g)
      (ExactUniversalRawMorphismTwoCell.whiskerLeft
        (W := W) A f
        (ExactUniversalRawMorphismTwoCell.leftUnitor
          (W := W) A g)) =
    ExactUniversalRawMorphismTwoCell.whiskerRight
      (W := W) A
      (ExactUniversalRawMorphismTwoCell.rightUnitor
        (W := W) A f)
      g := by
  apply ExactUniversalRawMorphismTwoCell.ext
  · simpa only [
      ExactUniversalRawMorphismTwoCell.vcomp_raw,
      ExactUniversalRawMorphismTwoCell.associator_raw,
      ExactUniversalRawMorphismTwoCell.whiskerLeft_raw,
      ExactUniversalRawMorphismTwoCell.leftUnitor_raw,
      ExactUniversalRawMorphismTwoCell.whiskerRight_raw,
      ExactUniversalRawMorphismTwoCell.rightUnitor_raw,
      ExactUniversalRawMorphism.id_raw
    ] using!
      (Bicategory.triangle f.raw g.raw)
  · simpa only [
      ExactUniversalRawMorphismTwoCell.vcomp_lift,
      ExactUniversalRawMorphismTwoCell.whiskerLeft_lift,
      ExactUniversalRawMorphismTwoCell.whiskerRight_lift,
      ExactUniversalRawMorphism.id_lift
    ] using!
      (Bicategory.triangle f.lift g.lift)

/-!
## Boundary after v4.68

The exact universal mapping source now has:

* hom categories;
* compatible left/right whiskering;
* horizontal composition and interchange;
* associator, left unitor, and right unitor isomorphisms;
* pentagon coherence;
* triangle coherence.

The next theorem unit can assemble these already-closed operations into a
genuine Mathlib \`Bicategory\` instance on the exact universal mapping source.
No weakly admissible system lacking exact presentation data is admitted by
this construction.
-/

end

end KUOS.DependentOriginationExactUniversalMappingCoherenceV4_68
