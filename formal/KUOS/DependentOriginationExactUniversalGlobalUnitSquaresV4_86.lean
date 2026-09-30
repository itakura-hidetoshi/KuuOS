import KUOS.DependentOriginationExactUniversalLabelledRealizationV4_85
import KUOS.DependentOriginationExactUniversalMappingStructuralIsoV4_67

namespace KUOS.DependentOriginationExactUniversalGlobalUnitSquaresV4_86

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMappingTwoCellVerticalV4_59
open KUOS.DependentOriginationExactUniversalMappingHomCategoryV4_60
open KUOS.DependentOriginationExactUniversalMappingStructuralIsoV4_67
open KUOS.DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70
open KUOS.DependentOriginationExactUniversalRealizationFaithfulV4_76
open KUOS.DependentOriginationExactUniversalRealizationFullyFaithfulV4_77
open KUOS.DependentOriginationExactUniversalHomEquivalenceV4_83
open KUOS.DependentOriginationExactUniversalSectionPseudofunctorV4_84
open KUOS.DependentOriginationExactUniversalLabelledRealizationV4_85

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Global source-roundtrip unit squares v4.86

v4.83 constructed a natural isomorphism on every fixed source hom category.
v4.84 assembled the inverse hom sections into a pseudofunctor, and v4.85
constructed the converse label-preserving strict realization.

This file moves one level higher.  We first form the ACTUAL Mathlib composite
pseudofunctor

  source --labelled realization--> realized sector --section--> source.

Its action on objects is the identity, while its one- and two-cell maps are the
already verified v4.83 section applied to the realized components.

For each source one-cell f we then turn the v4.83 hom-unit component

  f ~= section(f.lift)

into the exact pseudonaturality-shaped square

  f >> 1 ~= 1 >> roundtrip(f)

by adjoining the native right and left unitors.  The resulting isomorphism is
not an independently chosen replacement: its middle factor is literally the
existing hom-unit component.

Both directions are checked under DO2 realization.  The middle hom-unit
disappears to identity, leaving precisely

  rho(f.lift) ; lambda(f.lift)^-1

and its inverse.  These are the canonical naturality cells for an identity-
component strong transformation.  This prepares, but does not yet assert, the
global StrongTrans coherence laws.

No object coverage of all DO2, final biequivalence, or independently prescribed
raw component is asserted here.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

abbrev Source :=
  ExactUniversalRawObject.{u, v, uH, vH} (W := W) A

/-- The actual composite of the strict labelled realization and the v4.84
section pseudofunctor. -/
def exactUniversalSourceRoundtrip :
    Pseudofunctor (Source (W := W) A) (Source (W := W) A) :=
  Pseudofunctor.comp
    (exactUniversalLabelledRealization (W := W) A).toPseudofunctor
    (exactUniversalSectionPseudofunctor (W := W) A)

@[simp] theorem exactUniversalSourceRoundtrip_obj
    (X : Source (W := W) A) :
    (exactUniversalSourceRoundtrip (W := W) A).obj X = X := rfl

@[simp] theorem exactUniversalSourceRoundtrip_map
    {X Y : Source (W := W) A} (f : X ⟶ Y) :
    (exactUniversalSourceRoundtrip (W := W) A).map f =
      exactUniversalOneCellOfLift (W := W) A X Y f.lift := rfl

@[simp] theorem exactUniversalSourceRoundtrip_map₂
    {X Y : Source (W := W) A} {f g : X ⟶ Y} (eta : f ⟶ g) :
    (exactUniversalSourceRoundtrip (W := W) A).map₂ eta =
      (exactUniversalHomSection (W := W) A X Y).map eta.lift := rfl

/-- The existing v4.83 source-side hom-unit component, retyped as an isomorphism
from f to the actual global composite's image of f. -/
def exactUniversalSourceRoundtripCoreIso
    {X Y : Source (W := W) A} (f : X ⟶ Y) :
    f ≅ (exactUniversalSourceRoundtrip (W := W) A).map f := by
  change f ≅ (exactUniversalHomSection (W := W) A X Y).obj f.lift
  exact (exactUniversalHomUnitIso (W := W) A X Y).app f

@[simp] theorem exactUniversalSourceRoundtripCoreIso_hom_lift
    {X Y : Source (W := W) A} (f : X ⟶ Y) :
    (exactUniversalSourceRoundtripCoreIso (W := W) A f).hom.lift =
      𝟙 f.lift :=
  exactUniversalHomUnitIso_hom_lift (W := W) A f

@[simp] theorem exactUniversalSourceRoundtripCoreIso_inv_lift
    {X Y : Source (W := W) A} (f : X ⟶ Y) :
    (exactUniversalSourceRoundtripCoreIso (W := W) A f).inv.lift =
      𝟙 f.lift :=
  exactUniversalHomUnitIso_inv_lift (W := W) A f

/-- Source left-unitor inverse realizes to the native DO2 left-unitor inverse. -/
@[simp] theorem exactUniversalRealization_source_leftUnitor_inv_lift
    {X Y : Source (W := W) A} (f : X ⟶ Y) :
    (λ_ f).inv.lift = (λ_ f.lift).inv := by
  apply Bicategory.InducedBicategory.hom₂_ext
  rfl

/-- Source right-unitor inverse realizes to the native DO2 right-unitor inverse. -/
@[simp] theorem exactUniversalRealization_source_rightUnitor_inv_lift
    {X Y : Source (W := W) A} (f : X ⟶ Y) :
    (ρ_ f).inv.lift = (ρ_ f.lift).inv := by
  apply Bicategory.InducedBicategory.hom₂_ext
  rfl

/-- The pseudonaturality-shaped isomorphism for the prospective global unit.
The central factor is exactly the v4.83 hom-unit component. -/
def exactUniversalSourceRoundtripNaturalityIso
    {X Y : Source (W := W) A} (f : X ⟶ Y) :
    f ≫ 𝟙 Y ≅
      𝟙 X ≫ (exactUniversalSourceRoundtrip (W := W) A).map f :=
  (ρ_ f) ≪≫
    exactUniversalSourceRoundtripCoreIso (W := W) A f ≪≫
      (λ_ ((exactUniversalSourceRoundtrip (W := W) A).map f)).symm

/-- The forward naturality cell realizes to the canonical right-unitor followed
by inverse left-unitor. -/
@[simp] theorem exactUniversalSourceRoundtripNaturalityIso_hom_lift
    {X Y : Source (W := W) A} (f : X ⟶ Y) :
    (exactUniversalSourceRoundtripNaturalityIso (W := W) A f).hom.lift =
      (ρ_ f.lift).hom ≫ (λ_ f.lift).inv := by
  change
    (ρ_ f).hom.lift ≫
        (exactUniversalSourceRoundtripCoreIso (W := W) A f).hom.lift ≫
          (λ_ ((exactUniversalSourceRoundtrip (W := W) A).map f)).inv.lift =
      (ρ_ f.lift).hom ≫ (λ_ f.lift).inv
  rw [exactUniversalRealization_source_rightUnitor_lift,
    exactUniversalSourceRoundtripCoreIso_hom_lift,
    exactUniversalRealization_source_leftUnitor_inv_lift]
  simpa only [Category.id_comp, Category.comp_id]

/-- The inverse naturality cell realizes to the inverse canonical unitor path. -/
@[simp] theorem exactUniversalSourceRoundtripNaturalityIso_inv_lift
    {X Y : Source (W := W) A} (f : X ⟶ Y) :
    (exactUniversalSourceRoundtripNaturalityIso (W := W) A f).inv.lift =
      (λ_ f.lift).hom ≫ (ρ_ f.lift).inv := by
  simp only [exactUniversalSourceRoundtripNaturalityIso, Iso.trans_inv, Iso.symm_inv,
    ExactUniversalRawMorphismTwoCell.vcomp_lift]
  rw [exactUniversalRealization_source_leftUnitor_lift,
    exactUniversalSourceRoundtripCoreIso_inv_lift,
    exactUniversalRealization_source_rightUnitor_inv_lift]
  simpa only [exactUniversalSourceRoundtrip_map,
    exactUniversalOneCellOfLift_lift, Category.id_comp, Category.comp_id]

/-- As a complete realized isomorphism, the prospective unit naturality square
is exactly the canonical DO2 unitor comparison. -/
theorem exactUniversalSourceRoundtripNaturalityIso_realization
    {X Y : Source (W := W) A} (f : X ⟶ Y) :
    (exactUniversalCompletion2HomFunctor (W := W) A X Y).mapIso
      (exactUniversalSourceRoundtripNaturalityIso (W := W) A f) =
        (ρ_ f.lift) ≪≫ (λ_ f.lift).symm := by
  apply Iso.ext
  exact exactUniversalSourceRoundtripNaturalityIso_hom_lift
    (W := W) A f

/-! ## Regression checks -/

variable {X Y : Source (W := W) A}

example :
    Pseudofunctor (Source (W := W) A) (Source (W := W) A) :=
  exactUniversalSourceRoundtrip (W := W) A

example (f : X ⟶ Y) :
    (exactUniversalSourceRoundtrip (W := W) A).map f =
      exactUniversalOneCellOfLift (W := W) A X Y f.lift := rfl

example {f g : X ⟶ Y} (eta : f ⟶ g) :
    (exactUniversalSourceRoundtrip (W := W) A).map₂ eta =
      (exactUniversalHomSection (W := W) A X Y).map eta.lift := rfl

example (f : X ⟶ Y) :
    f ≅ (exactUniversalSourceRoundtrip (W := W) A).map f :=
  exactUniversalSourceRoundtripCoreIso (W := W) A f

example (f : X ⟶ Y) :
    f ≫ 𝟙 Y ≅
      𝟙 X ≫ (exactUniversalSourceRoundtrip (W := W) A).map f :=
  exactUniversalSourceRoundtripNaturalityIso (W := W) A f

example (f : X ⟶ Y) :
    (exactUniversalSourceRoundtripNaturalityIso (W := W) A f).hom.lift =
      (ρ_ f.lift).hom ≫ (λ_ f.lift).inv :=
  exactUniversalSourceRoundtripNaturalityIso_hom_lift (W := W) A f

example (f : X ⟶ Y) :
    (exactUniversalCompletion2HomFunctor (W := W) A X Y).mapIso
      (exactUniversalSourceRoundtripNaturalityIso (W := W) A f) =
        (ρ_ f.lift) ≪≫ (λ_ f.lift).symm :=
  exactUniversalSourceRoundtripNaturalityIso_realization (W := W) A f

#print axioms exactUniversalSourceRoundtrip
#print axioms exactUniversalSourceRoundtripCoreIso
#print axioms exactUniversalSourceRoundtripNaturalityIso
#print axioms exactUniversalSourceRoundtripNaturalityIso_hom_lift
#print axioms exactUniversalSourceRoundtripNaturalityIso_inv_lift
#print axioms exactUniversalSourceRoundtripNaturalityIso_realization

end

end KUOS.DependentOriginationExactUniversalGlobalUnitSquaresV4_86
