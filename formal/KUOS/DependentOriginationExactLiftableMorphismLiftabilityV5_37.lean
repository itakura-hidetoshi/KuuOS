import KUOS.DependentOriginationExactLiftableCoherentUniversalizationV5_36
import KUOS.DependentOriginationExactClassificationMorphismInterfaceV5_21
import KUOS.DependentOriginationExactUniversalMorphismLiftabilityV4_72
import Mathlib

namespace KUOS.DependentOriginationExactLiftableMorphismLiftabilityV5_37

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMorphismLiftabilityV4_72
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactClassificationMorphismInterfaceV5_21
open KUOS.DependentOriginationExactLiftableCoherentUniversalizationV5_36

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Exact-liftable classification morphism liftability v5.37

v5.36 upgrades every exact-liftable classification object, under the aligned
atlas specialization, to a chosen coherent universal target over its own raw
system.

The remaining morphism boundary must not be collapsed incorrectly: v4.72
already proves that an arbitrary raw StrongTrans is admitted by the
exact-universal source exactly when it has a compatible DO2 lift and invertible
presentation-comparison square.

This file transports that precise boundary to the exact-liftable
classification layer.

For each exact-liftable object X we package the chosen v5.36 universal target
as an ExactUniversalClassificationObject whose raw system is definitionally
X.raw and whose label is X.label.

A label-preserving raw classification 1-cell f : X.raw -> Y.raw is then called
liftable exactly when v4.72's ExactUniversalRawMorphism.Liftable holds between
those chosen source objects.

The main theorem states:

  liftable f
    <->
  exists an ExactUniversalClassificationOneCell over the prescribed raw map.

The class is closed under identity and composition by the already-proved v4.72
closure theorems.

This does not assert that every raw StrongTrans is liftable.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable
  (A :
    RefinementAtlas.{u, max u v, uH}
      (LocalizedContext W))

/-! ## Canonical exact-universal source chosen from v5.36 -/

/-- Repackage a fixed-raw coherent universal classification object as the
underlying exact-universal raw source object. -/
def exactUniversalRawObjectOfFixedRaw
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {R :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)}
    (U :
      KUOS.DependentOriginationExactClassificationCoherentUniquenessV5_20.FixedRawExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)
        R) :
    ExactUniversalRawObject.{u, v, uH, vH}
      (W := W) A where
  raw := R
  presentation := U.presentation
  universal := U.universal

@[simp] theorem exactUniversalRawObjectOfFixedRaw_raw
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {R :
      RawHigherContextualSystem.{u, v, uH, vH}
        (Context := Context)}
    (U :
      KUOS.DependentOriginationExactClassificationCoherentUniquenessV5_20.FixedRawExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)
        R) :
    (exactUniversalRawObjectOfFixedRaw
      (W := W) A U).raw = R :=
  rfl

/-- The canonical exact-universal classification object attached to an
exact-liftable classification object by the v5.36 choice. -/
noncomputable def canonicalExactUniversalClassificationObjectOfExactLiftable
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel where
  label := X.label
  source :=
    exactUniversalRawObjectOfFixedRaw
      (W := W) A
      (KUOS.DependentOriginationExactLiftableCoherentUniversalizationV5_36.fixedRawExactUniversalTargetOfExactLiftable
        (W := W) A X)

@[simp] theorem canonicalExactUniversalClassificationObjectOfExactLiftable_label
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    (canonicalExactUniversalClassificationObjectOfExactLiftable
      (W := W) A X).label = X.label :=
  rfl

@[simp] theorem canonicalExactUniversalClassificationObjectOfExactLiftable_raw
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    (canonicalExactUniversalClassificationObjectOfExactLiftable
      (W := W) A X).source.raw = X.raw :=
  rfl

/-! ## Label-preserving raw 1-cells on the exact-liftable layer -/

/-- Raw classification 1-cell before asking whether it admits a compatible
exact-universal lift. -/
structure ExactLiftableClassificationRawOneCell
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) where
  label_eq : X.label = Y.label
  map : Pseudofunctor.StrongTrans X.raw Y.raw

/-- v4.72 liftability, evaluated on the canonical v5.36 source choices. -/
def exactLiftableClassificationRawOneCellLiftable
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f :
      ExactLiftableClassificationRawOneCell
        (W := W) A X Y) : Prop :=
  KUOS.DependentOriginationExactUniversalMorphismLiftabilityV4_72.ExactUniversalRawMorphism.Liftable
    (W := W) A
    (X :=
      (canonicalExactUniversalClassificationObjectOfExactLiftable
        (W := W) A X).source)
    (Y :=
      (canonicalExactUniversalClassificationObjectOfExactLiftable
        (W := W) A Y).source)
    f.map

/-- Obstruction spelling of failure of the canonical v5.36 source lift. -/
def exactLiftableClassificationRawOneCellObstructed
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f :
      ExactLiftableClassificationRawOneCell
        (W := W) A X Y) : Prop :=
  ¬ exactLiftableClassificationRawOneCellLiftable
      (W := W) A f

/-- Main v5.37 criterion.

A label-preserving raw 1-cell is liftable between the canonical v5.36 source
choices iff an exact-universal classification 1-cell exists whose prescribed
raw projection is exactly that raw map. -/
theorem exactLiftableClassificationRawOneCell_liftable_iff_exists_classificationOneCell
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f :
      ExactLiftableClassificationRawOneCell
        (W := W) A X Y) :
    exactLiftableClassificationRawOneCellLiftable
        (W := W) A f ↔
      ∃ g :
          KUOS.DependentOriginationExactClassificationMorphismInterfaceV5_21.ExactUniversalClassificationOneCell.{u, v, uH, vH, uW, uP}
            (W := W) A
            (canonicalExactUniversalClassificationObjectOfExactLiftable
              (W := W) A X)
            (canonicalExactUniversalClassificationObjectOfExactLiftable
              (W := W) A Y),
        g.map.raw = f.map := by
  constructor
  · intro hLift
    rcases
        (KUOS.DependentOriginationExactUniversalMorphismLiftabilityV4_72.ExactUniversalRawMorphism.liftable_iff_exists_sourceMorphism
          (W := W) A
          (X :=
            (canonicalExactUniversalClassificationObjectOfExactLiftable
              (W := W) A X).source)
          (Y :=
            (canonicalExactUniversalClassificationObjectOfExactLiftable
              (W := W) A Y).source)
          f.map).1 hLift with
      ⟨m, hm⟩
    exact
      ⟨{
        label_eq := f.label_eq
        map := m
      }, hm⟩
  · rintro ⟨g, hg⟩
    exact
      (KUOS.DependentOriginationExactUniversalMorphismLiftabilityV4_72.ExactUniversalRawMorphism.liftable_iff_exists_sourceMorphism
        (W := W) A
        (X :=
          (canonicalExactUniversalClassificationObjectOfExactLiftable
            (W := W) A X).source)
        (Y :=
          (canonicalExactUniversalClassificationObjectOfExactLiftable
            (W := W) A Y).source)
        f.map).2
        ⟨g.map, hg⟩

/-- The obstruction is exactly nonexistence of a classification 1-cell over the
prescribed raw map. -/
theorem exactLiftableClassificationRawOneCell_obstructed_iff_not_exists_classificationOneCell
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f :
      ExactLiftableClassificationRawOneCell
        (W := W) A X Y) :
    exactLiftableClassificationRawOneCellObstructed
        (W := W) A f ↔
      ¬ ∃ g :
          KUOS.DependentOriginationExactClassificationMorphismInterfaceV5_21.ExactUniversalClassificationOneCell.{u, v, uH, vH, uW, uP}
            (W := W) A
            (canonicalExactUniversalClassificationObjectOfExactLiftable
              (W := W) A X)
            (canonicalExactUniversalClassificationObjectOfExactLiftable
              (W := W) A Y),
        g.map.raw = f.map := by
  unfold exactLiftableClassificationRawOneCellObstructed
  exact
    not_congr
      (exactLiftableClassificationRawOneCell_liftable_iff_exists_classificationOneCell
        (W := W) A f)

/-! ## Closure under identity and composition -/

/-- Identity raw classification 1-cell. -/
noncomputable def exactLiftableClassificationRawOneCellId
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    ExactLiftableClassificationRawOneCell
      (W := W) A X X where
  label_eq := rfl
  map := 𝟙 X.raw

/-- Composition of raw classification 1-cells. -/
def exactLiftableClassificationRawOneCellComp
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y Z :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f :
      ExactLiftableClassificationRawOneCell
        (W := W) A X Y)
    (g :
      ExactLiftableClassificationRawOneCell
        (W := W) A Y Z) :
    ExactLiftableClassificationRawOneCell
      (W := W) A X Z where
  label_eq := f.label_eq.trans g.label_eq
  map := f.map ≫ g.map

/-- Identity belongs to the liftable raw morphism class. -/
theorem exactLiftableClassificationRawOneCell_id_liftable
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    exactLiftableClassificationRawOneCellLiftable
      (W := W) A
      (exactLiftableClassificationRawOneCellId
        (W := W) A X) := by
  change
    KUOS.DependentOriginationExactUniversalMorphismLiftabilityV4_72.ExactUniversalRawMorphism.Liftable
      (W := W) A
      (X :=
        (canonicalExactUniversalClassificationObjectOfExactLiftable
          (W := W) A X).source)
      (Y :=
        (canonicalExactUniversalClassificationObjectOfExactLiftable
          (W := W) A X).source)
      (𝟙
        (canonicalExactUniversalClassificationObjectOfExactLiftable
          (W := W) A X).source.raw)
  exact
    KUOS.DependentOriginationExactUniversalMorphismLiftabilityV4_72.ExactUniversalRawMorphism.liftable_id
      (W := W) A
      (canonicalExactUniversalClassificationObjectOfExactLiftable
        (W := W) A X).source

/-- Liftability is closed under composition on the exact-liftable
classification layer. -/
theorem exactLiftableClassificationRawOneCell_liftable_comp
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y Z :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f :
      ExactLiftableClassificationRawOneCell
        (W := W) A X Y)
    (g :
      ExactLiftableClassificationRawOneCell
        (W := W) A Y Z)
    (hf :
      exactLiftableClassificationRawOneCellLiftable
        (W := W) A f)
    (hg :
      exactLiftableClassificationRawOneCellLiftable
        (W := W) A g) :
    exactLiftableClassificationRawOneCellLiftable
      (W := W) A
      (exactLiftableClassificationRawOneCellComp
        (W := W) A f g) := by
  exact
    KUOS.DependentOriginationExactUniversalMorphismLiftabilityV4_72.ExactUniversalRawMorphism.Liftable.comp
      (W := W) A hf hg

/-! ## Chosen classification lift -/

/-- Noncomputably choose the exact-universal classification 1-cell associated
to a liftable raw classification 1-cell. -/
noncomputable def classificationOneCellOfLiftableRawOneCell
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f :
      ExactLiftableClassificationRawOneCell
        (W := W) A X Y)
    (hLift :
      exactLiftableClassificationRawOneCellLiftable
        (W := W) A f) :
    KUOS.DependentOriginationExactClassificationMorphismInterfaceV5_21.ExactUniversalClassificationOneCell.{u, v, uH, vH, uW, uP}
      (W := W) A
      (canonicalExactUniversalClassificationObjectOfExactLiftable
        (W := W) A X)
      (canonicalExactUniversalClassificationObjectOfExactLiftable
        (W := W) A Y) :=
  Classical.choose
    ((exactLiftableClassificationRawOneCell_liftable_iff_exists_classificationOneCell
      (W := W) A f).1 hLift)

@[simp] theorem classificationOneCellOfLiftableRawOneCell_raw
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f :
      ExactLiftableClassificationRawOneCell
        (W := W) A X Y)
    (hLift :
      exactLiftableClassificationRawOneCellLiftable
        (W := W) A f) :
    (classificationOneCellOfLiftableRawOneCell
      (W := W) A f hLift).map.raw = f.map :=
  Classical.choose_spec
    ((exactLiftableClassificationRawOneCell_liftable_iff_exists_classificationOneCell
      (W := W) A f).1 hLift)

/-!
## Boundary after v5.37

Closed:

* exact-liftable objects have canonical chosen exact-universal classification
  representatives over their own raw systems;
* a label-preserving raw StrongTrans is admitted precisely when v4.72's
  compatible-lift criterion holds for those chosen representatives;
* the criterion is equivalent to existence of a v5.21 exact-universal
  classification 1-cell over the prescribed raw map;
* the admitted class is closed under identity and composition.

Still deliberately open:

* not every raw StrongTrans is asserted liftable;
* no semantic hypothesis weaker than v4.72 liftability has yet been proved
  sufficient;
* a bicategory of exact-liftable objects with only liftable raw 1-cells has not
  yet been packaged;
* the final mapping-side classification equivalence still requires the intended
  boundary category/bicategory and its functorial comparison.
-/

#print axioms exactUniversalRawObjectOfFixedRaw
#print axioms canonicalExactUniversalClassificationObjectOfExactLiftable
#print axioms exactLiftableClassificationRawOneCell_liftable_iff_exists_classificationOneCell
#print axioms exactLiftableClassificationRawOneCell_id_liftable
#print axioms exactLiftableClassificationRawOneCell_liftable_comp
#print axioms classificationOneCellOfLiftableRawOneCell

end

end KUOS.DependentOriginationExactLiftableMorphismLiftabilityV5_37
