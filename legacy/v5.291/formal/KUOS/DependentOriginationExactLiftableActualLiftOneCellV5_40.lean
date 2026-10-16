import KUOS.DependentOriginationExactLiftableBundledOneCellV5_38
import KUOS.DependentOriginationExactClassificationHomFunctorV5_22
import Mathlib

namespace KUOS.DependentOriginationExactLiftableActualLiftOneCellV5_40

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactClassificationMorphismInterfaceV5_21
open KUOS.DependentOriginationExactClassificationHomFunctorV5_22
open KUOS.DependentOriginationExactLiftableMorphismLiftabilityV5_37
open KUOS.DependentOriginationExactLiftableBundledOneCellV5_38

open scoped CategoryTheory.Pseudofunctor.StrongTrans

set_option autoImplicit false

noncomputable section

/-!
# Actual-lift exact-liftable classification one-cells v5.40

v5.38 stores a label-preserving raw StrongTrans together with the proposition
that it is liftable.  v5.37 then chooses an exact-universal classification
lift noncomputably.  This is sufficient for local hom categories, but the
choice is not definitionally compatible with identity or composition.

The present theorem unit changes the presentation of the one-cell data.  A
v5.40 one-cell stores:

* the prescribed label-preserving raw one-cell;
* an actual v5.21 exact-universal classification one-cell between the canonical
  v5.36 representatives;
* an equality saying that the actual lift projects to exactly the prescribed
  raw StrongTrans.

The v5.38 liftability proof is therefore derivable data rather than an
independent choice.  Identities and composites use the already-validated v5.22
identity and composition on the stored actual lifts themselves.  Consequently
the projection to exact-universal classification one-cells preserves identity
and composition by construction.

This does not yet install the global exact-liftable bicategory.  It removes the
specific choice-coherence obstruction that prevented doing so in v5.39.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable
  (A :
    RefinementAtlas.{u, max u v, uH}
      (LocalizedContext W))

/-- The canonical exact-universal classification representative of an
exact-liftable classification object. -/
abbrev CanonicalExactUniversalObject
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :=
  canonicalExactUniversalClassificationObjectOfExactLiftable
    (W := W) A X

/-- A one-cell carrying an actual exact-universal classification lift.

The liftability proposition of v5.38 is intentionally not stored: it follows
from `actualLift` and `raw_eq` by the v5.37 exact criterion. -/
structure ExactLiftableClassificationActualOneCell
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) where
  raw :
    ExactLiftableClassificationRawOneCell
      (W := W) A X Y
  actualLift :
    ExactUniversalClassificationOneCell
      (W := W) A
      (CanonicalExactUniversalObject (W := W) A X)
      (CanonicalExactUniversalObject (W := W) A Y)
  raw_eq :
    actualLift.map.raw = raw.map

/-- External label equality of an actual-lift one-cell. -/
abbrev ExactLiftableClassificationActualOneCell.label_eq
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f :
      ExactLiftableClassificationActualOneCell
        (W := W) A X Y) :
    X.label = Y.label :=
  f.raw.label_eq

/-- Prescribed raw StrongTrans of an actual-lift one-cell. -/
abbrev ExactLiftableClassificationActualOneCell.map
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f :
      ExactLiftableClassificationActualOneCell
        (W := W) A X Y) :
    Pseudofunctor.StrongTrans X.raw Y.raw :=
  f.raw.map

/-- The stored actual lift proves the v5.37 liftability criterion. -/
theorem ExactLiftableClassificationActualOneCell.liftable
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f :
      ExactLiftableClassificationActualOneCell
        (W := W) A X Y) :
    exactLiftableClassificationRawOneCellLiftable
      (W := W) A f.raw :=
  (exactLiftableClassificationRawOneCell_liftable_iff_exists_classificationOneCell
    (W := W) A f.raw).2
    ⟨f.actualLift, f.raw_eq⟩

/-- Forget the selected actual lift, recovering the v5.38 bundled admissible
one-cell. -/
noncomputable def ExactLiftableClassificationActualOneCell.toBundled
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f :
      ExactLiftableClassificationActualOneCell
        (W := W) A X Y) :
    ExactLiftableClassificationOneCell
      (W := W) A X Y where
  raw := f.raw
  liftable := f.liftable (W := W) A

@[simp] theorem ExactLiftableClassificationActualOneCell.toBundled_raw
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f :
      ExactLiftableClassificationActualOneCell
        (W := W) A X Y) :
    (f.toBundled (W := W) A).raw = f.raw :=
  rfl

@[simp] theorem ExactLiftableClassificationActualOneCell.actualLift_raw
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f :
      ExactLiftableClassificationActualOneCell
        (W := W) A X Y) :
    f.actualLift.map.raw = f.map :=
  f.raw_eq

/-- Every v5.38 bundled admissible one-cell has a canonical v5.40 refinement,
using the already-chosen v5.38 exact-universal classification lift. -/
noncomputable def actualOneCellOfBundled
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f :
      ExactLiftableClassificationOneCell
        (W := W) A X Y) :
    ExactLiftableClassificationActualOneCell
      (W := W) A X Y where
  raw := f.raw
  actualLift :=
    exactUniversalClassificationOneCellOfExactLiftableOneCell
      (W := W) A f
  raw_eq :=
    exactUniversalClassificationOneCellOfExactLiftableOneCell_raw
      (W := W) A f

@[simp] theorem actualOneCellOfBundled_raw
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f :
      ExactLiftableClassificationOneCell
        (W := W) A X Y) :
    (actualOneCellOfBundled (W := W) A f).raw = f.raw :=
  rfl

@[simp] theorem actualOneCellOfBundled_actualLift
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f :
      ExactLiftableClassificationOneCell
        (W := W) A X Y) :
    (actualOneCellOfBundled (W := W) A f).actualLift =
      exactUniversalClassificationOneCellOfExactLiftableOneCell
        (W := W) A f :=
  rfl

/-- Identity with its actual classification lift stored as data. -/
noncomputable def exactLiftableClassificationActualOneCellId
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    ExactLiftableClassificationActualOneCell
      (W := W) A X X where
  raw :=
    exactLiftableClassificationRawOneCellId
      (W := W) A X
  actualLift :=
    ExactUniversalClassificationOneCell.id
      (W := W) A
      (CanonicalExactUniversalObject (W := W) A X)
  raw_eq := by
    rw [
      ExactUniversalClassificationOneCell.id_map,
      ExactUniversalRawMorphism.id_raw
    ]
    rfl

/-- Composition with the actual exact-universal lifts composed directly. -/
noncomputable def exactLiftableClassificationActualOneCellComp
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y Z :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f :
      ExactLiftableClassificationActualOneCell
        (W := W) A X Y)
    (g :
      ExactLiftableClassificationActualOneCell
        (W := W) A Y Z) :
    ExactLiftableClassificationActualOneCell
      (W := W) A X Z where
  raw :=
    exactLiftableClassificationRawOneCellComp
      (W := W) A f.raw g.raw
  actualLift :=
    ExactUniversalClassificationOneCell.comp
      (W := W) A f.actualLift g.actualLift
  raw_eq := by
    rw [
      ExactUniversalClassificationOneCell.comp_map,
      ExactUniversalRawMorphism.comp_raw,
      f.raw_eq,
      g.raw_eq
    ]
    rfl

@[simp] theorem exactLiftableClassificationActualOneCellId_map
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    (exactLiftableClassificationActualOneCellId
      (W := W) A X).map =
      𝟙 X.raw :=
  rfl

@[simp] theorem exactLiftableClassificationActualOneCellComp_map
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y Z :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f :
      ExactLiftableClassificationActualOneCell
        (W := W) A X Y)
    (g :
      ExactLiftableClassificationActualOneCell
        (W := W) A Y Z) :
    (exactLiftableClassificationActualOneCellComp
      (W := W) A f g).map =
      Pseudofunctor.StrongTrans.vcomp f.map g.map :=
  rfl

@[simp] theorem exactLiftableClassificationActualOneCellId_actualLift
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    (exactLiftableClassificationActualOneCellId
      (W := W) A X).actualLift =
      ExactUniversalClassificationOneCell.id
        (W := W) A
        (CanonicalExactUniversalObject (W := W) A X) :=
  rfl

@[simp] theorem exactLiftableClassificationActualOneCellComp_actualLift
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y Z :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f :
      ExactLiftableClassificationActualOneCell
        (W := W) A X Y)
    (g :
      ExactLiftableClassificationActualOneCell
        (W := W) A Y Z) :
    (exactLiftableClassificationActualOneCellComp
      (W := W) A f g).actualLift =
      ExactUniversalClassificationOneCell.comp
        (W := W) A f.actualLift g.actualLift :=
  rfl

/-- The v5.37 liftability criterion is equivalent to existence of an actual-lift
one-cell carrying exactly the prescribed raw datum. -/
theorem rawOneCellLiftable_iff_exists_actualOneCell
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
          ExactLiftableClassificationActualOneCell
            (W := W) A X Y,
        g.raw = f := by
  constructor
  · intro h
    let bundled :
        ExactLiftableClassificationOneCell
          (W := W) A X Y :=
      { raw := f
        liftable := h }
    exact
      ⟨actualOneCellOfBundled (W := W) A bundled, rfl⟩
  · rintro ⟨g, hg⟩
    rw [← hg]
    exact g.liftable (W := W) A

/-!
## Boundary after v5.40

Closed:

* an admissible raw morphism can be presented together with an actual
  exact-universal classification lift;
* the old v5.38 bundled interface is recovered by forgetting the selected lift;
* every v5.38 bundled one-cell has a canonical v5.40 refinement;
* liftability is exactly existence of such an actual-lift presentation;
* identity and composition are defined using the stored v5.22 actual lifts;
* therefore the actual-lift projection preserves identity and composition
  definitionally.

In particular, the v5.39 obstruction

  chosenLift (f ; g) versus chosenLift f ; chosenLift g

is no longer a coherence problem for this refined presentation: the composite
stores the latter as its actual lift by construction.

Still open:

* install 2-cells using the stored actual lifts;
* reuse v5.23 whiskering, associator, unitors, pentagon, and triangle;
* package the resulting global exact-liftable classification bicategory.
-/

#print axioms ExactLiftableClassificationActualOneCell.liftable
#print axioms ExactLiftableClassificationActualOneCell.toBundled
#print axioms actualOneCellOfBundled
#print axioms exactLiftableClassificationActualOneCellId
#print axioms exactLiftableClassificationActualOneCellComp
#print axioms rawOneCellLiftable_iff_exists_actualOneCell

end

end KUOS.DependentOriginationExactLiftableActualLiftOneCellV5_40
