import KUOS.DependentOriginationClassificationCanonicalSectionV5_28
import KUOS.DependentOriginationExactUniversalAmbientRoundtripCounitV5_13
import KUOS.DependentOriginationExactUniversalSourceAmbientRoundtripUnitV5_14
import Mathlib

namespace KUOS.DependentOriginationClassificationUnitCounitCertificateV5_29

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalAmbientSectionPseudofunctorV5_12
open KUOS.DependentOriginationExactUniversalAmbientRoundtripCounitV5_13
open KUOS.DependentOriginationExactUniversalSourceAmbientRoundtripUnitV5_14
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactClassificationMorphismInterfaceV5_21
open KUOS.DependentOriginationExactClassificationBicategoryV5_23
open KUOS.DependentOriginationLocalizedClassificationRealizationV5_24
open KUOS.DependentOriginationClassificationWhiteheadBiequivalenceV5_27
open KUOS.DependentOriginationClassificationCanonicalSectionV5_28
open KUOS.DependentOriginationExactUniversalLabelledBiequivalenceV4_89

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory
open scoped Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Classification unit/counit biequivalence certificate v5.29

v5.27 supplies Whitehead-style local equivalence plus object coverage for the
full labelled classification realization.  v5.28 supplies an explicit
label-preserving canonical section pseudofunctor.

The remaining data needed for the same certificate level already achieved in
v5.15 are the two global StrongTrans roundtrip comparisons.

No new two-dimensional argument is needed.  The classification wrappers carry
only proposition-valued external label equality, while their mathematical
0/1/2-cell data project to the ambient exact-universal source and DO₂
bicategories.  Therefore:

* the target-side counit is v5.13's ambient counit wrapped with label equality
  `rfl`;
* the source-side unit is v5.14's source unit wrapped with label equality
  `rfl`;
* all StrongTrans naturality, identity, and composition laws reduce by
  classification 2-cell extensionality to the already proved v5.13/v5.14
  laws.

This theorem unit packages Whitehead data, the explicit quasi-inverse, unit,
and counit.  It still does not assert triangle modifications.
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

/-! ## Roundtrip pseudofunctors -/

/-- Target roundtrip: canonical classification section followed by strict
classification realization. -/
noncomputable def exactUniversalClassificationTargetRoundtrip
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP} :
    Pseudofunctor
      (Target (W := W) A WorldLabel PresentationLabel)
      (Target (W := W) A WorldLabel PresentationLabel) :=
  Pseudofunctor.comp
    (exactUniversalClassificationCanonicalSection (W := W) A)
    (exactUniversalClassificationRealization (W := W) A).toPseudofunctor

/-- Source roundtrip: strict classification realization followed by the
canonical classification section. -/
noncomputable def exactUniversalClassificationSourceRoundtrip
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP} :
    Pseudofunctor
      (Source (W := W) A WorldLabel PresentationLabel)
      (Source (W := W) A WorldLabel PresentationLabel) :=
  Pseudofunctor.comp
    (exactUniversalClassificationRealization (W := W) A).toPseudofunctor
    (exactUniversalClassificationCanonicalSection (W := W) A)

/-! ## Underlying roundtrip projections -/

@[simp] theorem exactUniversalClassificationTargetRoundtrip_obj_label
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (Z : Target (W := W) A WorldLabel PresentationLabel) :
    ((exactUniversalClassificationTargetRoundtrip
      (W := W) A).obj Z).label = Z.label :=
  rfl

@[simp] theorem exactUniversalClassificationTargetRoundtrip_obj_carrier
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (Z : Target (W := W) A WorldLabel PresentationLabel) :
    ((exactUniversalClassificationTargetRoundtrip
      (W := W) A).obj Z).carrier =
      (exactUniversalAmbientRoundtrip (W := W) A).obj Z.carrier :=
  rfl

@[simp] theorem exactUniversalClassificationTargetRoundtrip_map_underlying
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y : Target (W := W) A WorldLabel PresentationLabel}
    (f : X ⟶ Y) :
    ((exactUniversalClassificationTargetRoundtrip
      (W := W) A).map f).map =
      (exactUniversalAmbientRoundtrip (W := W) A).map f.map :=
  rfl

@[simp] theorem exactUniversalClassificationTargetRoundtrip_map₂_underlying
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y : Target (W := W) A WorldLabel PresentationLabel}
    {f g : X ⟶ Y}
    (eta : f ⟶ g) :
    ((exactUniversalClassificationTargetRoundtrip
      (W := W) A).map₂ eta).cell =
      (exactUniversalAmbientRoundtrip (W := W) A).map₂ eta.cell :=
  rfl

@[simp] theorem exactUniversalClassificationSourceRoundtrip_obj_label
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X : Source (W := W) A WorldLabel PresentationLabel) :
    ((exactUniversalClassificationSourceRoundtrip
      (W := W) A).obj X).label = X.label :=
  rfl

@[simp] theorem exactUniversalClassificationSourceRoundtrip_obj_source
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X : Source (W := W) A WorldLabel PresentationLabel) :
    ((exactUniversalClassificationSourceRoundtrip
      (W := W) A).obj X).source =
      (exactUniversalSourceAmbientRoundtrip (W := W) A).obj X.source :=
  rfl

@[simp] theorem exactUniversalClassificationSourceRoundtrip_map_underlying
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y : Source (W := W) A WorldLabel PresentationLabel}
    (f : X ⟶ Y) :
    ((exactUniversalClassificationSourceRoundtrip
      (W := W) A).map f).map =
      (exactUniversalSourceAmbientRoundtrip (W := W) A).map f.map :=
  rfl

@[simp] theorem exactUniversalClassificationSourceRoundtrip_map₂_underlying
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y : Source (W := W) A WorldLabel PresentationLabel}
    {f g : X ⟶ Y}
    (eta : f ⟶ g) :
    ((exactUniversalClassificationSourceRoundtrip
      (W := W) A).map₂ eta).cell =
      (exactUniversalSourceAmbientRoundtrip (W := W) A).map₂ eta.cell :=
  rfl

/-! ## Target-side counit -/

/-- Counit component obtained by wrapping the v5.13 ambient counit component. -/
noncomputable def exactUniversalClassificationTargetRoundtripCounitApp
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (Z : Target (W := W) A WorldLabel PresentationLabel) :
    (exactUniversalClassificationTargetRoundtrip (W := W) A).obj Z ⟶ Z where
  label_eq := rfl
  map :=
    (exactUniversalAmbientRoundtripCounit (W := W) A).app Z.carrier

/-- Counit naturality isomorphism obtained by wrapping v5.13. -/
noncomputable def exactUniversalClassificationTargetRoundtripCounitNaturalityIso
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y : Target (W := W) A WorldLabel PresentationLabel}
    (f : X ⟶ Y) :
    (exactUniversalClassificationTargetRoundtrip (W := W) A).map f ≫
        exactUniversalClassificationTargetRoundtripCounitApp (W := W) A Y ≅
      exactUniversalClassificationTargetRoundtripCounitApp (W := W) A X ≫ f := by
  apply LocalizedClassificationTwoCell.isoOfUnderlying (W := W) A
  exact
    (exactUniversalAmbientRoundtripCounit (W := W) A).naturality f.map

/-- Native target-side StrongTrans counit. -/
noncomputable def exactUniversalClassificationTargetRoundtripCounit
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP} :
    Pseudofunctor.StrongTrans
      (exactUniversalClassificationTargetRoundtrip
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel))
      (Pseudofunctor.id
        (Target (W := W) A WorldLabel PresentationLabel)) where
  app Z :=
    exactUniversalClassificationTargetRoundtripCounitApp (W := W) A Z
  naturality f :=
    exactUniversalClassificationTargetRoundtripCounitNaturalityIso
      (W := W) A f
  naturality_naturality {a b} {f g} eta := by
    apply LocalizedClassificationTwoCell.ext
    exact
      (exactUniversalAmbientRoundtripCounit
        (W := W) A).naturality_naturality eta.cell
  naturality_id X := by
    apply LocalizedClassificationTwoCell.ext
    exact
      (exactUniversalAmbientRoundtripCounit
        (W := W) A).naturality_id X.carrier
  naturality_comp {a b c} f g := by
    apply LocalizedClassificationTwoCell.ext
    exact
      (exactUniversalAmbientRoundtripCounit
        (W := W) A).naturality_comp f.map g.map

@[simp] theorem exactUniversalClassificationTargetRoundtripCounit_app_underlying
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (Z : Target (W := W) A WorldLabel PresentationLabel) :
    ((exactUniversalClassificationTargetRoundtripCounit
      (W := W) A).app Z).map =
      (exactUniversalAmbientRoundtripCounit (W := W) A).app Z.carrier :=
  rfl

/-! ## Source-side unit -/

/-- Unit component obtained by wrapping the v5.14 source unit component. -/
noncomputable def exactUniversalClassificationSourceRoundtripUnitApp
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X : Source (W := W) A WorldLabel PresentationLabel) :
    X ⟶ (exactUniversalClassificationSourceRoundtrip (W := W) A).obj X where
  label_eq := rfl
  map :=
    (exactUniversalSourceAmbientRoundtripUnit (W := W) A).app X.source

/-- Unit naturality isomorphism obtained by wrapping v5.14. -/
noncomputable def exactUniversalClassificationSourceRoundtripUnitNaturalityIso
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    {X Y : Source (W := W) A WorldLabel PresentationLabel}
    (f : X ⟶ Y) :
    f ≫ exactUniversalClassificationSourceRoundtripUnitApp (W := W) A Y ≅
      exactUniversalClassificationSourceRoundtripUnitApp (W := W) A X ≫
        (exactUniversalClassificationSourceRoundtrip (W := W) A).map f := by
  apply ExactUniversalClassificationTwoCell.isoOfUnderlying (W := W) A
  exact
    (exactUniversalSourceAmbientRoundtripUnit (W := W) A).naturality f.map

/-- Native source-side StrongTrans unit. -/
noncomputable def exactUniversalClassificationSourceRoundtripUnit
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP} :
    Pseudofunctor.StrongTrans
      (Pseudofunctor.id
        (Source (W := W) A WorldLabel PresentationLabel))
      (exactUniversalClassificationSourceRoundtrip
        (W := W) A
        (WorldLabel := WorldLabel)
        (PresentationLabel := PresentationLabel)) where
  app X :=
    exactUniversalClassificationSourceRoundtripUnitApp (W := W) A X
  naturality f :=
    exactUniversalClassificationSourceRoundtripUnitNaturalityIso
      (W := W) A f
  naturality_naturality {a b} {f g} eta := by
    apply ExactUniversalClassificationTwoCell.ext
    exact
      (exactUniversalSourceAmbientRoundtripUnit
        (W := W) A).naturality_naturality eta.cell
  naturality_id X := by
    apply ExactUniversalClassificationTwoCell.ext
    exact
      (exactUniversalSourceAmbientRoundtripUnit
        (W := W) A).naturality_id X.source
  naturality_comp {a b c} f g := by
    apply ExactUniversalClassificationTwoCell.ext
    exact
      (exactUniversalSourceAmbientRoundtripUnit
        (W := W) A).naturality_comp f.map g.map

@[simp] theorem exactUniversalClassificationSourceRoundtripUnit_app_underlying
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}
    (X : Source (W := W) A WorldLabel PresentationLabel) :
    ((exactUniversalClassificationSourceRoundtripUnit
      (W := W) A).app X).map =
      (exactUniversalSourceAmbientRoundtripUnit (W := W) A).app X.source :=
  rfl

/-! ## Complete current classification certificate -/

/-- Classification analogue of the v5.15 ambient biequivalence certificate:
Whitehead data, explicit quasi-inverse, and global unit/counit StrongTrans. -/
structure ExactUniversalClassificationBiequivalenceCertificate
    (WorldLabel : Type uW)
    (PresentationLabel : Type uP) where
  whitehead :
    WhiteheadBiequivalenceData
      (Source (W := W) A WorldLabel PresentationLabel)
      (Target (W := W) A WorldLabel PresentationLabel)
  quasiInverse :
    Pseudofunctor
      (Target (W := W) A WorldLabel PresentationLabel)
      (Source (W := W) A WorldLabel PresentationLabel)
  unit :
    Pseudofunctor.StrongTrans
      (Pseudofunctor.id
        (Source (W := W) A WorldLabel PresentationLabel))
      (Pseudofunctor.comp whitehead.forward quasiInverse)
  counit :
    Pseudofunctor.StrongTrans
      (Pseudofunctor.comp quasiInverse whitehead.forward)
      (Pseudofunctor.id
        (Target (W := W) A WorldLabel PresentationLabel))

/-- Assemble the current full classification biequivalence certificate. -/
noncomputable def exactUniversalClassificationBiequivalenceCertificate
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP} :
    ExactUniversalClassificationBiequivalenceCertificate
      (W := W) A WorldLabel PresentationLabel where
  whitehead :=
    exactUniversalClassificationWhiteheadBiequivalence
      (W := W) A
  quasiInverse :=
    exactUniversalClassificationCanonicalSection
      (W := W) A
  unit := by
    change
      Pseudofunctor.StrongTrans
        (Pseudofunctor.id
          (Source (W := W) A WorldLabel PresentationLabel))
        (exactUniversalClassificationSourceRoundtrip
          (W := W) A)
    exact
      exactUniversalClassificationSourceRoundtripUnit
        (W := W) A
  counit := by
    change
      Pseudofunctor.StrongTrans
        (exactUniversalClassificationTargetRoundtrip
          (W := W) A)
        (Pseudofunctor.id
          (Target (W := W) A WorldLabel PresentationLabel))
    exact
      exactUniversalClassificationTargetRoundtripCounit
        (W := W) A

@[simp] theorem exactUniversalClassificationBiequivalenceCertificate_forward
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP} :
    (exactUniversalClassificationBiequivalenceCertificate
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).whitehead.forward =
      (exactUniversalClassificationRealization
        (W := W) A).toPseudofunctor :=
  rfl

@[simp] theorem exactUniversalClassificationBiequivalenceCertificate_quasiInverse
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP} :
    (exactUniversalClassificationBiequivalenceCertificate
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).quasiInverse =
      exactUniversalClassificationCanonicalSection
        (W := W) A :=
  rfl

theorem exactUniversalClassificationBiequivalenceCertificate_unit
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP} :
    (exactUniversalClassificationBiequivalenceCertificate
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).unit =
      exactUniversalClassificationSourceRoundtripUnit
        (W := W) A :=
  rfl

theorem exactUniversalClassificationBiequivalenceCertificate_counit
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP} :
    (exactUniversalClassificationBiequivalenceCertificate
      (W := W) A
      (WorldLabel := WorldLabel)
      (PresentationLabel := PresentationLabel)).counit =
      exactUniversalClassificationTargetRoundtripCounit
        (W := W) A :=
  rfl

/-!
## Boundary after v5.29

The full labelled classification realization now has the same certificate level
as the ambient v5.15 theorem:

* Whitehead local hom equivalence;
* object essential surjectivity;
* explicit label-preserving quasi-inverse pseudofunctor;
* global source unit StrongTrans;
* global target counit StrongTrans.

The next theorem unit is triangle coherence / modifications.  No triangle
modification is asserted here, and no statement about arbitrary weak semantic
or merely exact-liftable raw systems is added.
-/

/-! ## Regression checks -/

section Regression

variable
    {WorldLabel : Type uW}
    {PresentationLabel : Type uP}

example :
    ExactUniversalClassificationBiequivalenceCertificate
      (W := W) A WorldLabel PresentationLabel :=
  exactUniversalClassificationBiequivalenceCertificate
    (W := W) A

example :
    Pseudofunctor.StrongTrans
      (Pseudofunctor.id
        (Source (W := W) A WorldLabel PresentationLabel))
      (exactUniversalClassificationSourceRoundtrip
        (W := W) A) :=
  exactUniversalClassificationSourceRoundtripUnit
    (W := W) A

example :
    Pseudofunctor.StrongTrans
      (exactUniversalClassificationTargetRoundtrip
        (W := W) A)
      (Pseudofunctor.id
        (Target (W := W) A WorldLabel PresentationLabel)) :=
  exactUniversalClassificationTargetRoundtripCounit
    (W := W) A

end Regression

#print axioms exactUniversalClassificationTargetRoundtripCounit
#print axioms exactUniversalClassificationSourceRoundtripUnit
#print axioms exactUniversalClassificationBiequivalenceCertificate

end

end KUOS.DependentOriginationClassificationUnitCounitCertificateV5_29
