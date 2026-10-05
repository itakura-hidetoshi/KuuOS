import KUOS.DependentOriginationClassificationWhiteheadBiequivalenceV5_27
import KUOS.DependentOriginationExactUniversalAmbientSectionPseudofunctorV5_12
import KUOS.DependentOriginationExactClassificationBicategoryV5_23
import Mathlib

namespace KUOS.DependentOriginationClassificationCanonicalSectionV5_28

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMappingBicategoryV4_69
open KUOS.DependentOriginationExactUniversalAmbientCanonicalSourceV5_11
open KUOS.DependentOriginationExactUniversalAmbientSectionPseudofunctorV5_12
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactClassificationMorphismInterfaceV5_21
open KUOS.DependentOriginationExactClassificationHomFunctorV5_22
open KUOS.DependentOriginationExactClassificationBicategoryV5_23
open KUOS.DependentOriginationLocalizedClassificationRealizationV5_24
open KUOS.DependentOriginationClassificationWhiteheadBiequivalenceV5_27

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory
open scoped Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Label-preserving canonical classification section v5.28

v5.27 packages the classification realization as a Whitehead-style
biequivalence certificate.  The next higher-coherence step is to expose an
explicit quasi-inverse pseudofunctor.

The mathematical quasi-inverse already exists at the ambient level: v5.12
constructs

  exactUniversalAmbientCanonicalSectionPseudofunctor :
    DO₂ -> ExactUniversalRawObject.

A localized classification object contains two independent pieces of data:

* an external classification label;
* an ambient DO₂ carrier.

This file leaves the label literally unchanged and applies the v5.12 ambient
section only to the carrier.  The same lifting is performed on one-cells and
two-cells.  Identity/composition comparison isomorphisms and all pseudofunctor
coherence are inherited from v5.12 after forgetting the proposition-valued
label equality.

No new object choice, no arbitrary raw-system factorization, and no
ExactLiftabilityCriterion -> AmbientAlignedExactLiftabilityCriterion converse
is introduced.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable
  (A :
    RefinementAtlas.{u, max u v, uH}
      (LocalizedContext W))

abbrev Source
    (WorldLabel : Type uW)
    (PresentationLabel : Type uP) :=
  ExactUniversalClassificationObject
    (W := W) A WorldLabel PresentationLabel

abbrev Target
    (WorldLabel : Type uW)
    (PresentationLabel : Type uP) :=
  LocalizedClassificationObject
    (W := W) A WorldLabel PresentationLabel

/-! ## Object/cell wrappers -/

/-- Apply the ambient canonical section to the carrier and retain the external
classification label literally. -/
noncomputable def exactUniversalClassificationCanonicalSectionObj
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (Z : Target (W := W) A WorldLabel PresentationLabel) :
    Source (W := W) A WorldLabel PresentationLabel where
  label := Z.label
  source :=
    (exactUniversalAmbientCanonicalSectionPseudofunctor
      (W := W) A).obj Z.carrier

/-- Lift a localized classification one-cell through the ambient canonical
section, retaining its existing label equality. -/
noncomputable def exactUniversalClassificationCanonicalSectionMap
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y : Target (W := W) A WorldLabel PresentationLabel}
    (f : X ⟶ Y) :
    exactUniversalClassificationCanonicalSectionObj (W := W) A X ⟶
      exactUniversalClassificationCanonicalSectionObj (W := W) A Y where
  label_eq := f.label_eq
  map :=
    (exactUniversalAmbientCanonicalSectionPseudofunctor
      (W := W) A).map f.map

/-- Lift a localized classification two-cell through the ambient canonical
section. -/
noncomputable def exactUniversalClassificationCanonicalSectionMap₂
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y : Target (W := W) A WorldLabel PresentationLabel}
    {f g : X ⟶ Y}
    (eta : f ⟶ g) :
    exactUniversalClassificationCanonicalSectionMap (W := W) A f ⟶
      exactUniversalClassificationCanonicalSectionMap (W := W) A g where
  cell :=
    (exactUniversalAmbientCanonicalSectionPseudofunctor
      (W := W) A).map₂ eta.cell

@[simp] theorem exactUniversalClassificationCanonicalSectionObj_label
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (Z : Target (W := W) A WorldLabel PresentationLabel) :
    (exactUniversalClassificationCanonicalSectionObj
      (W := W) A Z).label = Z.label :=
  rfl

@[simp] theorem exactUniversalClassificationCanonicalSectionObj_source
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (Z : Target (W := W) A WorldLabel PresentationLabel) :
    (exactUniversalClassificationCanonicalSectionObj
      (W := W) A Z).source =
      (exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).obj Z.carrier :=
  rfl

@[simp] theorem exactUniversalClassificationCanonicalSectionMap_map
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y : Target (W := W) A WorldLabel PresentationLabel}
    (f : X ⟶ Y) :
    (exactUniversalClassificationCanonicalSectionMap
      (W := W) A f).map =
      (exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).map f.map :=
  rfl

@[simp] theorem exactUniversalClassificationCanonicalSectionMap₂_cell
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y : Target (W := W) A WorldLabel PresentationLabel}
    {f g : X ⟶ Y}
    (eta : f ⟶ g) :
    (exactUniversalClassificationCanonicalSectionMap₂
      (W := W) A eta).cell =
      (exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).map₂ eta.cell :=
  rfl

/-! ## Structural comparison isomorphisms -/

/-- Identity comparison inherited from the ambient canonical section. -/
noncomputable def exactUniversalClassificationCanonicalSectionMapId
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (Z : Target (W := W) A WorldLabel PresentationLabel) :
    exactUniversalClassificationCanonicalSectionMap
        (W := W) A (𝟙 Z) ≅
      𝟙 (exactUniversalClassificationCanonicalSectionObj
        (W := W) A Z) :=
  ExactUniversalClassificationTwoCell.isoOfUnderlying
    (W := W) A
    ((exactUniversalAmbientCanonicalSectionPseudofunctor
      (W := W) A).mapId Z.carrier)

/-- Composition comparison inherited from the ambient canonical section. -/
noncomputable def exactUniversalClassificationCanonicalSectionMapComp
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y Z : Target (W := W) A WorldLabel PresentationLabel}
    (f : X ⟶ Y)
    (g : Y ⟶ Z) :
    exactUniversalClassificationCanonicalSectionMap
        (W := W) A (f ≫ g) ≅
      exactUniversalClassificationCanonicalSectionMap (W := W) A f ≫
        exactUniversalClassificationCanonicalSectionMap (W := W) A g :=
  ExactUniversalClassificationTwoCell.isoOfUnderlying
    (W := W) A
    ((exactUniversalAmbientCanonicalSectionPseudofunctor
      (W := W) A).mapComp f.map g.map)

/-! ## Global pseudofunctor -/

/-- Label-preserving explicit quasi-inverse candidate for classification
realization, obtained by lifting the v5.12 ambient canonical section. -/
noncomputable def exactUniversalClassificationCanonicalSection
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP} :
    Pseudofunctor
      (Target (W := W) A WorldLabel PresentationLabel)
      (Source (W := W) A WorldLabel PresentationLabel) where
  obj Z :=
    exactUniversalClassificationCanonicalSectionObj (W := W) A Z
  map f :=
    exactUniversalClassificationCanonicalSectionMap (W := W) A f
  map₂ eta :=
    exactUniversalClassificationCanonicalSectionMap₂ (W := W) A eta
  map₂_id f := by
    apply ExactUniversalClassificationTwoCell.ext
    exact
      (exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).map₂_id f.map
  map₂_comp eta theta := by
    apply ExactUniversalClassificationTwoCell.ext
    exact
      (exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).map₂_comp eta.cell theta.cell
  mapId Z :=
    exactUniversalClassificationCanonicalSectionMapId
      (W := W) A Z
  mapComp f g :=
    exactUniversalClassificationCanonicalSectionMapComp
      (W := W) A f g
  map₂_whisker_left {X Y Z} f {g h} eta := by
    apply ExactUniversalClassificationTwoCell.ext
    exact
      (exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).map₂_whisker_left f.map eta.cell
  map₂_whisker_right {X Y Z} {f g} eta h := by
    apply ExactUniversalClassificationTwoCell.ext
    exact
      (exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).map₂_whisker_right eta.cell h.map
  map₂_associator {X Y Z T} f g h := by
    apply ExactUniversalClassificationTwoCell.ext
    exact
      (exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).map₂_associator f.map g.map h.map
  map₂_left_unitor {X Y} f := by
    apply ExactUniversalClassificationTwoCell.ext
    exact
      (exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).map₂_left_unitor f.map
  map₂_right_unitor {X Y} f := by
    apply ExactUniversalClassificationTwoCell.ext
    exact
      (exactUniversalAmbientCanonicalSectionPseudofunctor
        (W := W) A).map₂_right_unitor f.map

/-! ## Exact carrier recovery -/

@[simp] theorem exactUniversalClassificationCanonicalSection_obj_label
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (Z : Target (W := W) A WorldLabel PresentationLabel) :
    (exactUniversalClassificationCanonicalSection
      (W := W) A).obj Z |>.label = Z.label :=
  rfl

@[simp] theorem exactUniversalClassificationCanonicalSection_obj_realize_carrier
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (Z : Target (W := W) A WorldLabel PresentationLabel) :
    ((exactUniversalClassificationRealization
      (W := W) A).obj
        ((exactUniversalClassificationCanonicalSection
          (W := W) A).obj Z)).carrier =
      Z.carrier := by
  exact
    exactUniversalAmbientCanonicalSectionPseudofunctor_obj_realization
      (W := W) A Z.carrier

@[simp] theorem exactUniversalClassificationCanonicalSection_map_realize_underlying
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y : Target (W := W) A WorldLabel PresentationLabel}
    (f : X ⟶ Y) :
    ((exactUniversalClassificationRealization
      (W := W) A).map
        ((exactUniversalClassificationCanonicalSection
          (W := W) A).map f)).map =
      f.map := by
  exact
    exactUniversalAmbientCanonicalSectionPseudofunctor_map_lift
      (W := W) A f.map

@[simp] theorem exactUniversalClassificationCanonicalSection_map₂_realize_underlying
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y : Target (W := W) A WorldLabel PresentationLabel}
    {f g : X ⟶ Y}
    (eta : f ⟶ g) :
    ((exactUniversalClassificationRealization
      (W := W) A).map₂
        ((exactUniversalClassificationCanonicalSection
          (W := W) A).map₂ eta)).cell =
      eta.cell := by
  exact
    exactUniversalAmbientCanonicalSectionPseudofunctor_map₂_lift
      (W := W) A eta.cell

/-!
## Boundary after v5.28

The classification Whitehead certificate now has an explicit label-preserving
quasi-inverse candidate.  The next theorem unit can form the two roundtrip
pseudofunctors and lift the existing ambient counit/source unit to native
classification StrongTrans data.

No claim about arbitrary raw/exact-liftable systems or the v5.19
universe-alignment converse is introduced.
-/

/-! ## Regression checks -/

section Regression

variable
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}

example :
    Pseudofunctor
      (Target (W := W) A WorldLabel PresentationLabel)
      (Source (W := W) A WorldLabel PresentationLabel) :=
  exactUniversalClassificationCanonicalSection
    (W := W) A

example
    (Z : Target (W := W) A WorldLabel PresentationLabel) :
    ((exactUniversalClassificationCanonicalSection
      (W := W) A).obj Z).label = Z.label :=
  rfl

end Regression

#print axioms exactUniversalClassificationCanonicalSection
#print axioms exactUniversalClassificationCanonicalSection_obj_realize_carrier
#print axioms exactUniversalClassificationCanonicalSection_map_realize_underlying
#print axioms exactUniversalClassificationCanonicalSection_map₂_realize_underlying

end

end KUOS.DependentOriginationClassificationCanonicalSectionV5_28
