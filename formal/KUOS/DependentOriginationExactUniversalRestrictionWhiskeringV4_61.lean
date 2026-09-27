import KUOS.DependentOriginationExactUniversalMappingHomCategoryV4_60
import Mathlib

namespace KUOS.DependentOriginationExactUniversalRestrictionWhiskeringV4_61

open CategoryTheory
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationExactUniversalMappingTwoCellV4_58
open KUOS.DependentOriginationExactUniversalMappingTwoCellVerticalV4_59
open KUOS.DependentOriginationExactUniversalMappingHomCategoryV4_60

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Restriction preserves 2-cell whiskering v4.61

The source-bicategory construction will need to whisker compatible 2-cells by
mapping-property 1-cells.  The only new fact needed at the presentation-unit
boundary is that restriction of localized modifications commutes with the
native bicategorical left and right whiskering operations.

Pinned Mathlib's pseudofunctor bicategory defines these whiskerings
componentwise:

  (alpha ◁ Gamma).app X = alpha.app X ◁ Gamma.app X
  (Gamma ▷ beta).app X = Gamma.app X ▷ beta.app X.

Since KuuOS restriction is likewise componentwise evaluation at the image of
the presentation unit, both preservation laws are immediate by modification
extensionality.

No source-bicategory whiskering operation is installed yet in this file.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Restriction commutes with left whiskering of a localized modification. -/
@[simp] theorem restrictHigherLocalizedModification_whiskerLeft
    {F G H : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    (alpha : F ⟶ G)
    {beta gamma : G ⟶ H}
    (eta : beta ⟶ gamma) :
    restrictHigherLocalizedModification (W := W) (alpha ◁ eta) =
      restrictHigherLocalizedStrongTrans (W := W) alpha ◁
        restrictHigherLocalizedModification (W := W) eta := by
  apply Pseudofunctor.StrongTrans.homCategory.ext
  intro X
  rfl

/-- Restriction commutes with right whiskering of a localized modification. -/
@[simp] theorem restrictHigherLocalizedModification_whiskerRight
    {F G H : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    {alpha beta : F ⟶ G}
    (eta : alpha ⟶ beta)
    (gamma : G ⟶ H) :
    restrictHigherLocalizedModification (W := W) (eta ▷ gamma) =
      restrictHigherLocalizedModification (W := W) eta ▷
        restrictHigherLocalizedStrongTrans (W := W) gamma := by
  apply Pseudofunctor.StrongTrans.homCategory.ext
  intro X
  rfl

/-!
## Boundary after v4.61

Restriction of localized 2-cells is now functorial for

* identity and vertical composition (v4.59);
* left whiskering;
* right whiskering.

These are precisely the local operations needed to transport Mathlib's
bicategorical 2-cell calculus through the presentation-unit boundary.

The next theorem unit can therefore define left/right whiskering of compatible
mapping-property 2-cells themselves, using only the stored comparison-square
compatibility equations and bicategorical coherence.
-/

end

end KUOS.DependentOriginationExactUniversalRestrictionWhiskeringV4_61
