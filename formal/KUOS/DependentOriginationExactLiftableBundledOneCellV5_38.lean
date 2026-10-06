import KUOS.DependentOriginationExactLiftableMorphismLiftabilityV5_37
import KUOS.DependentOriginationExactClassificationHomFunctorV5_22
import Mathlib

namespace KUOS.DependentOriginationExactLiftableBundledOneCellV5_38

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactClassificationMorphismInterfaceV5_21
open KUOS.DependentOriginationExactClassificationHomFunctorV5_22
open KUOS.DependentOriginationExactLiftableMorphismLiftabilityV5_37

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Bundled exact-liftable classification one-cells v5.38

v5.37 gives the precise morphism boundary for exact-liftable classification
objects: a label-preserving raw StrongTrans is admitted exactly when it satisfies
v4.72 liftability for the canonical exact-universal representatives chosen from
v5.36.

This file bundles the raw one-cell together with that liftability proof.

The bundled one-cells are closed under identity and composition.  Each bundled
one-cell also has a chosen exact-universal classification lift, and the raw
projection of that chosen lift is exactly the bundled raw map.

This is intentionally only the one-cell layer.  A bicategory on exact-liftable
objects still requires a deliberate 2-cell interface and coherence relating
chosen lifts of composites to composites of chosen lifts.  Those data are not
silently inferred from noncomputable choice.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable
  (A :
    RefinementAtlas.{u, max u v, uH}
      (LocalizedContext W))

/-- A morphism in the exact-liftable classification layer is a label-preserving
raw StrongTrans together with proof that it is admitted by the v4.72
exact-universal liftability criterion for the canonical v5.36 representatives. -/
structure ExactLiftableClassificationOneCell
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) where
  raw :
    KUOS.DependentOriginationExactLiftableMorphismLiftabilityV5_37.ExactLiftableClassificationRawOneCell
      (W := W) A X Y
  liftable :
    KUOS.DependentOriginationExactLiftableMorphismLiftabilityV5_37.exactLiftableClassificationRawOneCellLiftable
      (W := W) A raw

/-- The external label equality stored by a bundled exact-liftable one-cell. -/
abbrev ExactLiftableClassificationOneCell.label_eq
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f : ExactLiftableClassificationOneCell (W := W) A X Y) :
    X.label = Y.label :=
  f.raw.label_eq

/-- The underlying raw StrongTrans. -/
abbrev ExactLiftableClassificationOneCell.map
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f : ExactLiftableClassificationOneCell (W := W) A X Y) :
    Pseudofunctor.StrongTrans X.raw Y.raw :=
  f.raw.map

/-- Identity bundled one-cell. -/
noncomputable def exactLiftableClassificationOneCellId
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    ExactLiftableClassificationOneCell
      (W := W) A X X where
  raw :=
    KUOS.DependentOriginationExactLiftableMorphismLiftabilityV5_37.exactLiftableClassificationRawOneCellId
      (W := W) A X
  liftable :=
    KUOS.DependentOriginationExactLiftableMorphismLiftabilityV5_37.exactLiftableClassificationRawOneCell_id_liftable
      (W := W) A X

/-- Composition of bundled one-cells. -/
noncomputable def exactLiftableClassificationOneCellComp
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y Z :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f :
      ExactLiftableClassificationOneCell
        (W := W) A X Y)
    (g :
      ExactLiftableClassificationOneCell
        (W := W) A Y Z) :
    ExactLiftableClassificationOneCell
      (W := W) A X Z where
  raw :=
    KUOS.DependentOriginationExactLiftableMorphismLiftabilityV5_37.exactLiftableClassificationRawOneCellComp
      (W := W) A f.raw g.raw
  liftable :=
    KUOS.DependentOriginationExactLiftableMorphismLiftabilityV5_37.exactLiftableClassificationRawOneCell_liftable_comp
      (W := W) A f.raw g.raw f.liftable g.liftable

@[simp] theorem exactLiftableClassificationOneCellId_map
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    (exactLiftableClassificationOneCellId
      (W := W) A X).map =
      𝟙 X.raw :=
  rfl

@[simp] theorem exactLiftableClassificationOneCellComp_map
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y Z :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f :
      ExactLiftableClassificationOneCell
        (W := W) A X Y)
    (g :
      ExactLiftableClassificationOneCell
        (W := W) A Y Z) :
    (exactLiftableClassificationOneCellComp
      (W := W) A f g).map =
      Pseudofunctor.StrongTrans.vcomp f.map g.map :=
  rfl

@[simp] theorem exactLiftableClassificationOneCellComp_label_eq
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y Z :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f :
      ExactLiftableClassificationOneCell
        (W := W) A X Y)
    (g :
      ExactLiftableClassificationOneCell
        (W := W) A Y Z) :
    (exactLiftableClassificationOneCellComp
      (W := W) A f g).label_eq =
      f.label_eq.trans g.label_eq := by
  apply Subsingleton.elim

/-! ## Canonical exact-universal lift -/

/-- Choose the v5.37 exact-universal classification 1-cell associated to the
bundled liftable one-cell. -/
noncomputable def exactUniversalClassificationOneCellOfExactLiftableOneCell
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f :
      ExactLiftableClassificationOneCell
        (W := W) A X Y) :
    KUOS.DependentOriginationExactClassificationMorphismInterfaceV5_21.ExactUniversalClassificationOneCell
      (W := W) A
      (KUOS.DependentOriginationExactLiftableMorphismLiftabilityV5_37.canonicalExactUniversalClassificationObjectOfExactLiftable
        (W := W) A X)
      (KUOS.DependentOriginationExactLiftableMorphismLiftabilityV5_37.canonicalExactUniversalClassificationObjectOfExactLiftable
        (W := W) A Y) :=
  KUOS.DependentOriginationExactLiftableMorphismLiftabilityV5_37.classificationOneCellOfLiftableRawOneCell
    (W := W) A f.raw f.liftable

/-- The chosen exact-universal lift has exactly the prescribed raw
StrongTrans. -/
@[simp] theorem exactUniversalClassificationOneCellOfExactLiftableOneCell_raw
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f :
      ExactLiftableClassificationOneCell
        (W := W) A X Y) :
    (exactUniversalClassificationOneCellOfExactLiftableOneCell
      (W := W) A f).map.raw =
      f.map :=
  KUOS.DependentOriginationExactLiftableMorphismLiftabilityV5_37.classificationOneCellOfLiftableRawOneCell_raw
    (W := W) A f.raw f.liftable

/-- The chosen lift of the bundled identity projects to the raw identity. -/
@[simp] theorem exactUniversalClassificationOneCellOfExactLiftableOneCell_id_raw
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) :
    (exactUniversalClassificationOneCellOfExactLiftableOneCell
      (W := W) A
      (exactLiftableClassificationOneCellId
        (W := W) A X)).map.raw =
      𝟙 X.raw := by
  exact
    exactUniversalClassificationOneCellOfExactLiftableOneCell_raw
      (W := W) A
      (exactLiftableClassificationOneCellId
        (W := W) A X)

/-- The chosen lift of a bundled composite projects to the vertical composite
of the original raw StrongTranses. -/
@[simp] theorem exactUniversalClassificationOneCellOfExactLiftableOneCell_comp_raw
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y Z :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f :
      ExactLiftableClassificationOneCell
        (W := W) A X Y)
    (g :
      ExactLiftableClassificationOneCell
        (W := W) A Y Z) :
    (exactUniversalClassificationOneCellOfExactLiftableOneCell
      (W := W) A
      (exactLiftableClassificationOneCellComp
        (W := W) A f g)).map.raw =
      Pseudofunctor.StrongTrans.vcomp f.map g.map := by
  exact
    exactUniversalClassificationOneCellOfExactLiftableOneCell_raw
      (W := W) A
      (exactLiftableClassificationOneCellComp
        (W := W) A f g)

/-! ## Existence equivalence with the bundled interface -/

/-- A v5.37 raw one-cell is liftable precisely when it can be bundled as a
v5.38 exact-liftable classification one-cell with that exact raw datum. -/
theorem rawOneCellLiftable_iff_exists_bundledOneCell
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y :
      ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel}
    (f :
      KUOS.DependentOriginationExactLiftableMorphismLiftabilityV5_37.ExactLiftableClassificationRawOneCell
        (W := W) A X Y) :
    KUOS.DependentOriginationExactLiftableMorphismLiftabilityV5_37.exactLiftableClassificationRawOneCellLiftable
        (W := W) A f ↔
      ∃ g :
          ExactLiftableClassificationOneCell
            (W := W) A X Y,
        g.raw = f := by
  constructor
  · intro h
    exact ⟨{ raw := f, liftable := h }, rfl⟩
  · rintro ⟨g, rfl⟩
    exact g.liftable

/-!
## Boundary after v5.38

Closed:

* liftability is now part of the exact-liftable classification morphism type;
* bundled morphisms are closed under identity and composition;
* every bundled morphism has a chosen exact-universal classification lift;
* that chosen lift preserves the prescribed raw StrongTrans exactly.

Still open deliberately:

* chosen lifts are noncomputable choices; v5.38 does not assert that the chosen
  lift of a composite is definitionally equal to the composite of the chosen
  lifts;
* a 2-cell interface between bundled exact-liftable morphisms is not yet
  packaged;
* therefore no bicategory instance is installed here.

The next theorem unit can define 2-cells by comparison through the canonical
exact-universal representatives and then address identity/composition coherence
of the chosen lift.
-/

#print axioms exactLiftableClassificationOneCellId
#print axioms exactLiftableClassificationOneCellComp
#print axioms exactUniversalClassificationOneCellOfExactLiftableOneCell
#print axioms exactUniversalClassificationOneCellOfExactLiftableOneCell_raw
#print axioms rawOneCellLiftable_iff_exists_bundledOneCell

end

end KUOS.DependentOriginationExactLiftableBundledOneCellV5_38
