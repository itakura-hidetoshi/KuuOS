import KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
import KUOS.DependentOriginationExactUniversalMappingTwoCellV4_58
import KUOS.DependentOriginationExactUniversalMappingBicategoryV4_69
import KUOS.DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70
import Mathlib

namespace KUOS.DependentOriginationExactClassificationMorphismInterfaceV5_21

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMappingTwoCellV4_58
open KUOS.DependentOriginationExactUniversalMappingBicategoryV4_69
open KUOS.DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Classification morphism and mapping-side interface v5.21

Canonical v5.17 intentionally stopped at the object-level compile boundary.
Before that reduction, its branch history already contained the mathematically
correct 1-cell / 2-cell and mapping-side interfaces.  v5.18-v5.20 have now
separated exact liftability, factor existence, and coherent uniqueness, so the
missing typed morphism layer can be restored as its own theorem unit.

This file does not assert a final classification equivalence.

It only fixes:

* weak semantic 1-cells and 2-cells;
* exact-universal 1-cells and 2-cells;
* localized DO₂ 1-cells and 2-cells;
* realization on exact-universal 1/2-cells;
* the covariant mapping object Pseudofunctor DO₂ Target;
* restriction to the exact-universal source by precomposition with the strict
  realization Source -> DO₂.

External labels remain explicit equality data on 1-cells.  No carrier
equivalence is allowed to erase them.
-/

universe u v uH vH uW uP uT vT wT

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-! ## Weak semantic morphism levels -/

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

/-! ## Exact-universal morphism levels -/

/-- Exact-universal 1-cell: external labels are preserved and the mathematical
map is exactly the validated v4.57 mapping-property 1-cell. -/
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

/-! ## Localized DO₂ morphism levels -/

/-- Localized 1-cell in the ambient DO₂ bicategory, retaining label equality. -/
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

/-! ## Realization on 1-cells and 2-cells -/

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

/-- Realization projects the compatible exact-universal 2-cell to its DO₂
2-cell, again without changing the label data. -/
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

/-! ## Covariant mapping side Fun(DO₂, Target) -/

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
    (F G :
      LocalizedClassificationMappingObject
        (W := W) A Target) :=
  Pseudofunctor.StrongTrans F G

/-- 2-cells on the localized mapping side are modifications. -/
abbrev LocalizedClassificationMappingTwoCell
    {Target : Type uT}
    [Bicategory.{wT, vT} Target]
    {F G :
      LocalizedClassificationMappingObject
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

/-- 1-cells on the exact-source mapping side. -/
abbrev ExactSourceClassificationMappingOneCell
    {Target : Type uT}
    [Bicategory.{wT, vT} Target]
    (F G :
      ExactSourceClassificationMappingObject
        (W := W) A Target) :=
  Pseudofunctor.StrongTrans F G

/-- 2-cells on the exact-source mapping side. -/
abbrev ExactSourceClassificationMappingTwoCell
    {Target : Type uT}
    [Bicategory.{wT, vT} Target]
    {F G :
      ExactSourceClassificationMappingObject
        (W := W) A Target}
    (alpha beta :
      ExactSourceClassificationMappingOneCell
        (W := W) A F G) :=
  Pseudofunctor.StrongTrans.Modification alpha beta

/-- Restriction of a localized mapping object along the strict exact-universal
realization.  This fixes the variance of the later mapping theorem:

  Source -> DO₂ -> Target.
-/
noncomputable def restrictLocalizedClassificationMapping
    {Target : Type uT}
    [Bicategory.{wT, vT} Target]
    (F :
      LocalizedClassificationMappingObject
        (W := W) A Target) :
    ExactSourceClassificationMappingObject
      (W := W) A Target :=
  Pseudofunctor.comp
    (exactUniversalRealization (W := W) A).toPseudofunctor
    F

@[simp] theorem restrictLocalizedClassificationMapping_obj
    {Target : Type uT}
    [Bicategory.{wT, vT} Target]
    (F :
      LocalizedClassificationMappingObject
        (W := W) A Target)
    (X :
      ExactUniversalRawObject.{u, v, uH, vH}
        (W := W) A) :
    (restrictLocalizedClassificationMapping
      (W := W) A F).obj X =
      F.obj X.carrier :=
  rfl

/-!
## Boundary after v5.21

The classification interface now again has explicit typed 0/1/2-cell levels
without overloading the object-level v5.17 module:

  weak semantic raw systems
      -- StrongTrans / Modification -->

  exact-universal source
      -- ExactUniversalRawMorphism / compatible two-cell -->

  ambient DO₂
      -- native bicategory 1/2-cells -->.

For every target bicategory Target the mapping-side variance is fixed as

  Pseudofunctor DO₂ Target,

and restriction is precomposition along

  Source --exactUniversalRealization--> DO₂.

This still does not assert the final classification equivalence.  The remaining
bridges include:

* ordinary v5.18 exact liftability versus the ambient-aligned v5.19 criterion;
* extending classification functoriality beyond the already exact-universal
  source morphism interface;
* proving the final mapping-side essential surjectivity/full faithfulness at
  the intended classification boundary.
-/

end

end KUOS.DependentOriginationExactClassificationMorphismInterfaceV5_21
