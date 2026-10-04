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
    X.toWeak (W := W) A |>.label = X.label :=
  rfl

@[simp] theorem ExactLiftableClassificationObject.toWeak_raw
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject
        (W := W) A WorldLabel PresentationLabel) :
    X.toWeak (W := W) A |>.raw = X.raw :=
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
    X.realize (W := W) A |>.label = X.label :=
  rfl

@[simp] theorem ExactUniversalClassificationObject.realize_carrier
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel) :
    X.realize (W := W) A |>.carrier = X.source.carrier :=
  rfl

/-! ## Explicit object/1-cell/2-cell levels -/

/-- Weak semantic 1-cell: a label-preserving StrongTrans between raw systems. -/
structure WeakSemanticClassificationOneCell
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      WeakSemanticClassificationObject
        (W := W) WorldLabel PresentationLabel) where
  label_eq : X.label = Y.label
  map : Pseudofunctor.StrongTrans X.raw Y.raw

/-- Weak semantic 2-cell: a native Mathlib modification. -/
structure WeakSemanticClassificationTwoCell
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      WeakSemanticClassificationObject
        (W := W) WorldLabel PresentationLabel}
    (f g : WeakSemanticClassificationOneCell (W := W) X Y) where
  cell :
    Pseudofunctor.StrongTrans.Modification f.map g.map

/-- Exact-universal 1-cell: labels are preserved and the actual map is the
validated v4.57 mapping-property 1-cell. -/
structure ExactUniversalClassificationOneCell
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel) where
  label_eq : X.label = Y.label
  map :
    ExactUniversalRawMorphism
      (W := W) A X.source Y.source

/-- Exact-universal 2-cell: exactly the validated v4.58 compatible 2-cell. -/
structure ExactUniversalClassificationTwoCell
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    (f g : ExactUniversalClassificationOneCell (W := W) A X Y) where
  cell :
    ExactUniversalRawMorphismTwoCell
      (W := W) A f.map g.map

/-- Localized 1-cell in the ambient DO₂ bicategory, again label-preserving. -/
structure LocalizedClassificationOneCell
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      LocalizedClassificationObject
        (W := W) A WorldLabel PresentationLabel) where
  label_eq : X.label = Y.label
  map : X.carrier ⟶ Y.carrier

/-- Localized 2-cell in the ambient DO₂ hom category. -/
structure LocalizedClassificationTwoCell
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      LocalizedClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    (f g : LocalizedClassificationOneCell (W := W) A X Y) where
  cell : f.map ⟶ g.map

/-- Realization preserves the external label and projects an exact-universal
1-cell to its DO₂ lift. -/
def ExactUniversalClassificationOneCell.realize
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    (f : ExactUniversalClassificationOneCell (W := W) A X Y) :
    LocalizedClassificationOneCell
      (W := W) A
      (X.realize (W := W) A)
      (Y.realize (W := W) A) where
  label_eq := f.label_eq
  map := f.map.lift

/-- Realization projects the exact-universal compatible 2-cell to its DO₂
2-cell without changing labels. -/
def ExactUniversalClassificationTwoCell.realize
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    {f g : ExactUniversalClassificationOneCell (W := W) A X Y}
    (eta : ExactUniversalClassificationTwoCell (W := W) A f g) :
    LocalizedClassificationTwoCell
      (W := W) A
      (f.realize (W := W) A)
      (g.realize (W := W) A) where
  cell := eta.cell.lift

@[simp] theorem ExactUniversalClassificationOneCell.realize_map
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    (f : ExactUniversalClassificationOneCell (W := W) A X Y) :
    (f.realize (W := W) A).map = f.map.lift :=
  rfl

@[simp] theorem ExactUniversalClassificationTwoCell.realize_cell
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactUniversalClassificationObject
        (W := W) A WorldLabel PresentationLabel}
    {f g : ExactUniversalClassificationOneCell (W := W) A X Y}
    (eta : ExactUniversalClassificationTwoCell (W := W) A f g) :
    (eta.realize (W := W) A).cell = eta.cell.lift :=
  rfl

/-! ## The covariant mapping side `Fun(DO₂, X)` -/

/-- Objects on the localized mapping side: covariant pseudofunctors from DO₂
into an arbitrary target bicategory. -/
abbrev LocalizedClassificationMappingObject
    (Target : Type uT)
    [Bicategory.{wT, vT} Target] :=
  Pseudofunctor
    (DependentOriginationCompletion2.{u, v, uH, uH, vH}
      (W := W) A)
    Target

/-- 1-cells on the localized mapping side are StrongTrans. -/
abbrev LocalizedClassificationMappingOneCell
    {Target : Type uT}
    [Bicategory.{wT, vT} Target]
    (F G : LocalizedClassificationMappingObject
      (W := W) A Target) :=
  Pseudofunctor.StrongTrans F G

/-- 2-cells on the localized mapping side are modifications. -/
abbrev LocalizedClassificationMappingTwoCell
    {Target : Type uT}
    [Bicategory.{wT, vT} Target]
    {F G : LocalizedClassificationMappingObject
      (W := W) A Target}
    (alpha beta :
      LocalizedClassificationMappingOneCell
        (W := W) A F G) :=
  Pseudofunctor.StrongTrans.Modification alpha beta

/-- Mapping objects on the exact-universal source side. -/
abbrev ExactSourceClassificationMappingObject
    (Target : Type uT)
    [Bicategory.{wT, vT} Target] :=
  Pseudofunctor
    (ExactUniversalRawObject.{u, v, uH, vH}
      (W := W) A)
    Target

/-- Restriction of a localized mapping object along the strict exact-universal
realization.  This fixes the variance of the later mapping theorem:
`Source -> DO₂ -> Target`. -/
noncomputable def restrictLocalizedClassificationMapping
    {Target : Type uT}
    [Bicategory.{wT, vT} Target]
    (F : LocalizedClassificationMappingObject
      (W := W) A Target) :
    ExactSourceClassificationMappingObject
      (W := W) A Target :=
  Pseudofunctor.comp
    (exactUniversalRealization (W := W) A).toPseudofunctor
    F

@[simp] theorem restrictLocalizedClassificationMapping_obj
    {Target : Type uT}
    [Bicategory.{wT, vT} Target]
    (F : LocalizedClassificationMappingObject
      (W := W) A Target)
    (X : ExactUniversalRawObject.{u, v, uH, vH}
      (W := W) A) :
    (restrictLocalizedClassificationMapping
      (W := W) A F).obj X =
      F.obj X.carrier :=
  rfl

/-! ## Formal weak/exact obstruction boundary -/

/-- The known countermodel prevents replacing weak semantic admissibility by
exact liftability in the classification interface. -/
theorem weakAdmissibility_not_exactLiftability_counterexample
    (A :
      RefinementAtlas
        (LocalizedContext
          KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69.allMorphisms)) :
    IsHigherWAdmissible
        KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69.allMorphisms
        KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69.counterSystem
      ∧
    ¬ HasExactHigherDependentOriginationPresentation
        (W :=
          KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69.allMorphisms)
        A
        KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69.counterSystem := by
  exact
    ⟨KUOS.DependentOriginationAdmissibleNonfactorizationV4_01.counterSystem_admissible,
      KUOS.DependentOriginationExactHigherPresentationSectorV4_50
        .counterSystem_no_exactHigherDependentOriginationPresentation A⟩

/-!
## Boundary after v5.17

The final classification problem now has a typed interface:

* weak semantic objects are separate from exact-liftable objects;
* exact-universal source objects retain their chosen presentation/universal data;
* world and external presentation labels are explicit and preserved by 1-cells;
* raw/source/localized 1-cell and 2-cell levels are explicit;
* `Fun(DO₂, X)` is represented by native covariant Mathlib pseudofunctors,
  StrongTrans, and Modifications;
* restriction to the exact source has the explicit direction
  `Source -> DO₂ -> Target`;
* the weak-to-exact converse is formally blocked by the existing countermodel.

What remains for v5.18 is a mathematically correct criterion deciding when a
weak semantic object belongs to the exact-liftable sector.  Only after that
criterion, factor existence, and coherent uniqueness are separated should a
v5.19+ classification equivalence be stated.
-/

#print axioms ExactLiftableClassificationObject.toWeak
#print axioms ExactUniversalClassificationObject.toExactLiftable
#print axioms ExactUniversalClassificationObject.toWeak
#print axioms ExactUniversalClassificationObject.realize
#print axioms ExactUniversalClassificationOneCell.realize
#print axioms ExactUniversalClassificationTwoCell.realize
#print axioms restrictLocalizedClassificationMapping
#print axioms weakAdmissibility_not_exactLiftability_counterexample

end

end KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
