import KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
import KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
import Mathlib.CategoryTheory.Bicategory.Modification.Pseudo
import Mathlib

namespace KUOS.DependentOriginationExactUniversalMappingTwoCellV4_58

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Mapping-property 2-cell interface v4.58

v4.57 defines the positive universal source objects and their mapping-property
1-cells.  The next layer requires 2-cells.

The first missing API is restriction of an arbitrary modification between
localized StrongTrans along the presentation unit.  Earlier v2.35 provides the
invertible-iso version; here we define the general noninvertible version needed
for a source bicategory.

For mapping-property 1-cells f,g : X --> Y, a 2-cell consists of

* a raw modification f.raw --> g.raw;
* a DO₂ modification f.lift --> g.lift;
* the compatibility equation saying these two modifications agree after
  conjugation by the stored comparison squares.

This file only fixes the correct 2-cell type.  Vertical and horizontal
composition are intentionally deferred to the next theorem unit so that their
coherence laws are checked against this exact interface rather than bundled
prematurely.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- Restrict an arbitrary modification between localized StrongTrans along the
higher presentation unit. -/
noncomputable def restrictHigherLocalizedModification
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    {alpha beta : F ⟶ G}
    (Gamma : alpha ⟶ beta) :
    restrictHigherLocalizedStrongTrans (W := W) alpha ⟶
      restrictHigherLocalizedStrongTrans (W := W) beta := by
  refine ⟨{
    app := fun X =>
      Gamma.as.app
        ((higherPresentationUnitFunctor W).toPseudofunctor.obj X)
    naturality := ?_
  }⟩
  intro X Y f
  simpa [restrictHigherLocalizedStrongTrans] using
    Gamma.as.naturality
      ((higherPresentationUnitFunctor W).toPseudofunctor.map f)

@[simp] theorem restrictHigherLocalizedModification_app
    {F G : HigherLocalizedDescentSystem.{u, v, uH, vH} (W := W)}
    {alpha beta : F ⟶ G}
    (Gamma : alpha ⟶ beta)
    (X : Context) :
    (restrictHigherLocalizedModification (W := W) Gamma).as.app (.mk X) =
      Gamma.as.app (.mk ((higherPresentationUnitFunctor W).obj X)) :=
  rfl

/-- A 2-cell between mapping-property 1-cells.

The compatibility equation is the modification-level square

  restrict(lift₂) ▷ c_Y ; square_g
      =
  square_f ; c_X ◁ raw₂.

Thus the raw and realized 2-cells represent the same change of mapping-property
1-cell through the exact presentation comparisons. -/
structure ExactUniversalRawMorphismTwoCell
    {X Y : ExactUniversalRawObject (W := W) A}
    (f g : ExactUniversalRawMorphism (W := W) A X Y) where
  raw : f.raw ⟶ g.raw
  lift : f.lift ⟶ g.lift
  compatibility :
    (restrictHigherLocalizedModification (W := W) lift.hom ▷
        Y.presentation.comparison) ≫
      g.comparison_square.hom =
    f.comparison_square.hom ≫
      (X.presentation.comparison ◁ raw)

/-- Forget a mapping-property 2-cell to its raw modification. -/
abbrev ExactUniversalRawMorphismTwoCell.toRawModification
    {X Y : ExactUniversalRawObject (W := W) A}
    {f g : ExactUniversalRawMorphism (W := W) A X Y}
    (eta : ExactUniversalRawMorphismTwoCell (W := W) A f g) :
    f.raw ⟶ g.raw :=
  eta.raw

/-- Forget a mapping-property 2-cell to its DO₂ modification. -/
abbrev ExactUniversalRawMorphismTwoCell.toCompletion2Modification
    {X Y : ExactUniversalRawObject (W := W) A}
    {f g : ExactUniversalRawMorphism (W := W) A X Y}
    (eta : ExactUniversalRawMorphismTwoCell (W := W) A f g) :
    f.lift ⟶ g.lift :=
  eta.lift

/-!
## Boundary after v4.58

The mapping-property source now has:

* positive universal objects;
* composable mapping-property 1-cells;
* a precise compatible 2-cell type.

The next theorem unit must prove identity and vertical composition for these
2-cells, then horizontal composition.  Only after those laws are closed should
the data be installed as a bicategory and projected to DO₂ by a pseudofunctor.
-/

end

end KUOS.DependentOriginationExactUniversalMappingTwoCellV4_58
