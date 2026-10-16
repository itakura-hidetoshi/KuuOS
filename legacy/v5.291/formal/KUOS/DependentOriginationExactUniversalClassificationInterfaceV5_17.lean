import KUOS.DependentOriginationExactHigherAdmissibleV4_50
import KUOS.DependentOriginationExactUniversalAmbientTriangleCoherenceV5_16

namespace KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationExactHigherPresentationSectorV4_50
open KUOS.DependentOriginationExactHigherAdmissibleV4_50
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMappingTwoCellV4_58
open KUOS.DependentOriginationExactUniversalMappingBicategoryV4_69
open KUOS.DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70
open KUOS.DependentOriginationExactUniversalAmbientTriangleCoherenceV5_16
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationAdmissibleNonfactorizationV4_01

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Exact-universal classification interface v5.17

This file fixes the domain/codomain types for the later mapping/classification
theorem without asserting that theorem yet.

The interface deliberately separates four levels.

1. A weak semantic object stores only a raw higher contextual system together
   with `IsHigherWAdmissible`.
2. An exact-liftable object stores an actual exact DO₂ presentation-existence
   witness.
3. An exact-universal object stores the stronger chosen exact presentation and
   coherent universal-target data used by the v4.57-v5.16 source bicategory.
4. A localized object stores an object of the ambient DO₂ completion.

External world and presentation labels are carried separately from the
mathematical presentation.  They are never erased merely because realized
carriers agree.

For an arbitrary target bicategory `X`, the localized mapping side is the
native Mathlib type

  `Pseudofunctor DO₂ X`

with StrongTrans as 1-cells and Modifications as 2-cells.  Its restriction to
the exact-universal source is precomposition with the strict realization
pseudofunctor.

No equivalence between weak semantic objects and localized mappings is asserted
here.  In particular there is no map from weak admissibility to exact
liftability; the established countermodel is restated below as the formal
boundary that v5.18 must respect.
-/

universe u v uH vH uW uP uT vT wT

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-! ## External labels retained by the classification interface -/

/-- External conventional labels retained independently of carrier equivalence.

`world` records the world/context binding and `presentation` records the
externally meaningful presentation name.  These are not identified with the
internal exact-presentation structure stored in the exact-universal source. -/
structure ClassificationLabel
    (WorldLabel : Type uW)
    (PresentationLabel : Type uP) where
  world : WorldLabel
  presentation : PresentationLabel

/-! ## Weak semantic versus exact-liftable objects -/

/-- Weak semantic classification object.

This is intentionally only the semantic `W`-admissibility layer. -/
structure WeakSemanticClassificationObject
    (WorldLabel : Type uW)
    (PresentationLabel : Type uP) where
  label : ClassificationLabel WorldLabel PresentationLabel
  raw :
    RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)
  admissible : IsHigherWAdmissible W raw

/-- Exact-liftable classification object.

Exact liftability is represented by existence of a genuine carrier-first
exact presentation.  It is strictly stronger data than weak semantic
admissibility and is kept as a separate type. -/
structure ExactLiftableClassificationObject
    (WorldLabel : Type uW)
    (PresentationLabel : Type uP) where
  label : ClassificationLabel WorldLabel PresentationLabel
  raw :
    RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context)
  exact :
    HasExactHigherDependentOriginationPresentation
      (W := W) A raw

/-- Forget exact liftability to weak semantic admissibility while retaining all
external labels. -/
def ExactLiftableClassificationObject.toWeak
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject
        (W := W) A WorldLabel PresentationLabel) :
    WeakSemanticClassificationObject
      (W := W) WorldLabel PresentationLabel where
  label := X.label
  raw := X.raw
  admissible :=
    exactPresentation_isHigherWAdmissible
      (W := W) A X.raw X.exact

@[simp] theorem ExactLiftableClassificationObject.toWeak_label
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject
        (W := W) A WorldLabel PresentationLabel) :
    (X.toWeak (W := W) A).label = X.label :=
  rfl

@[simp] theorem ExactLiftableClassificationObject.toWeak_raw
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject
        (W := W) A WorldLabel PresentationLabel) :
    (X.toWeak (W := W) A).raw = X.raw :=
  rfl

/-! ## Exact-universal source and localized carrier objects -/

/-- Labelled exact-universal source object.

The internal source object retains its actual exact presentation and coherent
universal-target witness; the external label remains separate. -/
structure ExactUniversalClassificationObject
    (WorldLabel : Type uW)
    (PresentationLabel : Type uP) where
  label : ClassificationLabel WorldLabel PresentationLabel
  source :
    ExactUniversalRawObject.{u, v, uH, vH}
      (W := W) A

/-- Labelled localized DO₂ object. -/
structure LocalizedClassificationObject
    (WorldLabel : Type uW)
    (PresentationLabel : Type uP) where
  label : ClassificationLabel WorldLabel PresentationLabel
  carrier :
    DependentOriginationCompletion2.{u, v, uH, uH, vH}
      (W := W) A

/-- Every exact-universal source object determines an exact-liftable object. -/
def ExactUniversalClassificationObject.toExactLiftable
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel) :
    ExactLiftableClassificationObject
      (W := W) A WorldLabel PresentationLabel where
  label := X.label
  raw := X.source.raw
  exact := ⟨X.source.presentation⟩

/-- Every exact-universal source object therefore determines a weak semantic
object, but no converse is supplied. -/
def ExactUniversalClassificationObject.toWeak
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel) :
    WeakSemanticClassificationObject
      (W := W) WorldLabel PresentationLabel :=
  (X.toExactLiftable (W := W) A).toWeak (W := W) A

/-- Strict realization of a labelled exact-universal source object into DO₂,
preserving the external labels literally. -/
def ExactUniversalClassificationObject.realize
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel) :
    LocalizedClassificationObject
      (W := W) A WorldLabel PresentationLabel where
  label := X.label
  carrier := X.source.carrier

@[simp] theorem ExactUniversalClassificationObject.realize_label
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel) :
    (X.realize (W := W) A).label = X.label :=
  rfl

@[simp] theorem ExactUniversalClassificationObject.realize_carrier
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel) :
    (X.realize (W := W) A).carrier = X.source.carrier :=
  rfl

/-!
## Compile probe boundary

This commit intentionally stops after the object-level classification boundary.
It is used to separate import/cache cost from the later morphism/mapping-side
elaboration cost.  The full v5.17 draft remains in branch history.
-/

end

end KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
