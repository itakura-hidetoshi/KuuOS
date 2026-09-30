import KUOS.DependentOriginationExactUniversalGlobalCounitStrongTransV4_88
import KUOS.DependentOriginationBiequivalencePresentationInvariantV1_26

namespace KUOS.DependentOriginationExactUniversalLabelledBiequivalenceV4_89

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationPresentationIndependentInvariantV1_25
open KUOS.DependentOriginationBiequivalencePresentationInvariantV1_26
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalHomEquivalenceV4_83
open KUOS.DependentOriginationExactUniversalSectionPseudofunctorV4_84
open KUOS.DependentOriginationExactUniversalLabelledRealizationV4_85
open KUOS.DependentOriginationExactUniversalGlobalUnitStrongTransV4_87
open KUOS.DependentOriginationExactUniversalGlobalCounitStrongTransV4_88

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory
open scoped Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Whitehead biequivalence certificate on the object-labelled sector v4.89

v4.83 proved a category equivalence from every source hom category to the
corresponding DO₂ hom category. v4.84 assembled the chosen inverses into a
section pseudofunctor, v4.85 constructed the converse label-preserving strict
realization, and v4.87/v4.88 constructed global StrongTrans unit/counit data.

The realized sector is an induced bicategory: its hom objects are one-field
wrappers around the underlying DO₂ one-cells and two-cells. We first package
this wrapper/forgetful pair as an ordinary category equivalence. Composing it
with v4.83 gives, for each pair of labelled objects, an equivalence whose
forward functor is exactly the hom functor of the labelled realization.

Because the realized sector has exactly the same object labels as the source,
object essential surjectivity inside this sector is reflexive. Hence the
existing v1.26 Whitehead-style BicategoricalModelEquivalence applies directly.

Finally we retain the chosen v4.84 section together with the actual v4.87 unit
and v4.88 counit in one certificate. This is a biequivalence certificate for
the object-labelled realized sector, not for all ambient DO₂ objects. The
pinned Mathlib version does not provide a bundled tricategorical
pseudofunctor-biequivalence structure with triangle modifications; no such
stronger packaging is asserted here.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

abbrev Source :=
  ExactUniversalRawObject.{u, v, uH, vH} (W := W) A

abbrev Realized :=
  ExactUniversalRealizedSector.{u, v, uH, vH} (W := W) A

/-- Forget the induced-bicategory wrapper on one fixed realized hom category. -/
def exactUniversalRealizedHomForget
    (X Y : Realized (W := W) A) :
    (X ⟶ Y) ⥤ (X.carrier ⟶ Y.carrier) where
  obj f := f.hom
  map eta := eta.hom
  map_id _ := rfl
  map_comp _ _ := rfl

/-- Rewrap an underlying DO₂ hom as a morphism of the induced realized sector. -/
def exactUniversalRealizedHomWrap
    (X Y : Realized (W := W) A) :
    (X.carrier ⟶ Y.carrier) ⥤ (X ⟶ Y) where
  obj f := Bicategory.InducedBicategory.mkHom (X := X) (Y := Y) f
  map eta := Bicategory.InducedBicategory.mkHom₂ eta
  map_id _ := rfl
  map_comp _ _ := rfl

/-- Forgetting and then rewrapping is naturally isomorphic to identity on the
realized hom category. -/
def exactUniversalRealizedHomWrapperUnitIso
    (X Y : Realized (W := W) A) :
    𝟭 (X ⟶ Y) ≅
      exactUniversalRealizedHomForget (W := W) A X Y ⋙
        exactUniversalRealizedHomWrap (W := W) A X Y :=
  NatIso.ofComponents
    (fun f => Bicategory.InducedBicategory.isoMk (Iso.refl f.hom))

/-- Rewrapping and then forgetting is literally identity on the underlying
DO₂ hom category. -/
def exactUniversalRealizedHomWrapperCounitIso
    (X Y : Realized (W := W) A) :
    exactUniversalRealizedHomWrap (W := W) A X Y ⋙
        exactUniversalRealizedHomForget (W := W) A X Y ≅
      𝟭 (X.carrier ⟶ Y.carrier) :=
  NatIso.ofComponents (fun f => Iso.refl f)

/-- The induced realized hom category is equivalent to the corresponding
underlying DO₂ hom category. -/
def exactUniversalRealizedHomWrapperEquivalence
    (X Y : Realized (W := W) A) :
    (X ⟶ Y) ≌ (X.carrier ⟶ Y.carrier) :=
  CategoryTheory.Equivalence.mk
    (exactUniversalRealizedHomForget (W := W) A X Y)
    (exactUniversalRealizedHomWrap (W := W) A X Y)
    (exactUniversalRealizedHomWrapperUnitIso (W := W) A X Y)
    (exactUniversalRealizedHomWrapperCounitIso (W := W) A X Y)

/-- Local equivalence from source morphisms directly to the object-labelled
realized hom category. It is v4.83 followed by rewrapping. -/
def exactUniversalLabelledHomEquivalence
    (X Y : Source (W := W) A) :
    (X ⟶ Y) ≌
      ((exactUniversalLabelledRealization (W := W) A).obj X ⟶
        (exactUniversalLabelledRealization (W := W) A).obj Y) :=
  (exactUniversalHomEquivalence (W := W) A X Y).trans
    (exactUniversalRealizedHomWrapperEquivalence
      (W := W) A
      ((exactUniversalLabelledRealization (W := W) A).obj X)
      ((exactUniversalLabelledRealization (W := W) A).obj Y)).symm

/-- The forward functor of the local equivalence is exactly the hom functor of
the labelled realization, not merely isomorphic to it. -/
theorem exactUniversalLabelledHomEquivalence_functor
    (X Y : Source (W := W) A) :
    (exactUniversalLabelledHomEquivalence (W := W) A X Y).functor =
      (exactUniversalLabelledRealization (W := W) A).toPseudofunctor
        |>.toPrelaxFunctor.mapFunctor X Y := by
  apply CategoryTheory.Functor.hext
  · intro f
    rfl
  · intro f g eta
    exact heq_of_eq rfl

/-- Whitehead-style biequivalence data from the exact-universal source to its
object-labelled realized sector. Object essential surjectivity is reflexive
because the labels are retained exactly. -/
def exactUniversalLabelledBicategoricalModelEquivalence :
    BicategoricalModelEquivalence
      (Source (W := W) A)
      (Realized (W := W) A) where
  forward :=
    (exactUniversalLabelledRealization (W := W) A).toPseudofunctor
  homEquiv X Y :=
    exactUniversalLabelledHomEquivalence (W := W) A X Y
  homEquiv_functor X Y :=
    exactUniversalLabelledHomEquivalence_functor (W := W) A X Y
  object_essentially_surjective := by
    intro Z
    refine ⟨Z, ?_⟩
    change Nonempty (Z ≌ Z)
    exact ⟨Bicategory.Equivalence.id Z⟩

/-- Package the Whitehead local/object certificate together with the chosen
global quasi-inverse and the already verified StrongTrans unit/counit. -/
structure ExactUniversalLabelledBiequivalenceCertificate where
  whitehead :
    BicategoricalModelEquivalence
      (Source (W := W) A)
      (Realized (W := W) A)
  section :
    Pseudofunctor
      (Realized (W := W) A)
      (Source (W := W) A)
  unit :
    Pseudofunctor.StrongTrans
      (Pseudofunctor.id (Source (W := W) A))
      (Pseudofunctor.comp whitehead.forward section)
  counit :
    Pseudofunctor.StrongTrans
      (Pseudofunctor.comp section whitehead.forward)
      (Pseudofunctor.id (Realized (W := W) A))

/-- The complete current object-labelled biequivalence certificate. -/
def exactUniversalLabelledBiequivalenceCertificate :
    ExactUniversalLabelledBiequivalenceCertificate (W := W) A where
  whitehead :=
    exactUniversalLabelledBicategoricalModelEquivalence (W := W) A
  section :=
    exactUniversalSectionPseudofunctor (W := W) A
  unit := by
    change
      Pseudofunctor.StrongTrans
        (Pseudofunctor.id (Source (W := W) A))
        (exactUniversalSourceRoundtrip (W := W) A)
    exact exactUniversalSourceRoundtripUnit (W := W) A
  counit := by
    change
      Pseudofunctor.StrongTrans
        (exactUniversalRealizedRoundtrip (W := W) A)
        (Pseudofunctor.id (Realized (W := W) A))
    exact exactUniversalRealizedRoundtripCounit (W := W) A

@[simp] theorem exactUniversalLabelledBiequivalenceCertificate_forward :
    (exactUniversalLabelledBiequivalenceCertificate
      (W := W) A).whitehead.forward =
      (exactUniversalLabelledRealization (W := W) A).toPseudofunctor := rfl

@[simp] theorem exactUniversalLabelledBiequivalenceCertificate_section :
    (exactUniversalLabelledBiequivalenceCertificate
      (W := W) A).section =
      exactUniversalSectionPseudofunctor (W := W) A := rfl

/-- Object coverage is deliberately only coverage of the object-labelled
realized sector. -/
theorem exactUniversalLabelledObjectEssentialSurjectivity
    (Z : Realized (W := W) A) :
    ∃ X : Source (W := W) A,
      IntrinsicObjectEquivalent
        ((exactUniversalLabelledRealization (W := W) A).obj X) Z :=
  (exactUniversalLabelledBicategoricalModelEquivalence
    (W := W) A).object_essentially_surjective Z

/-! ## Regression checks -/

variable {X Y : Source (W := W) A}

example :
    BicategoricalModelEquivalence
      (Source (W := W) A)
      (Realized (W := W) A) :=
  exactUniversalLabelledBicategoricalModelEquivalence (W := W) A

example :
    (X ⟶ Y) ≌
      ((exactUniversalLabelledRealization (W := W) A).obj X ⟶
        (exactUniversalLabelledRealization (W := W) A).obj Y) :=
  exactUniversalLabelledHomEquivalence (W := W) A X Y

example :
    Pseudofunctor.StrongTrans
      (Pseudofunctor.id (Source (W := W) A))
      (exactUniversalSourceRoundtrip (W := W) A) :=
  (exactUniversalLabelledBiequivalenceCertificate
    (W := W) A).unit

example :
    Pseudofunctor.StrongTrans
      (exactUniversalRealizedRoundtrip (W := W) A)
      (Pseudofunctor.id (Realized (W := W) A)) :=
  (exactUniversalLabelledBiequivalenceCertificate
    (W := W) A).counit

#print axioms exactUniversalRealizedHomWrapperEquivalence
#print axioms exactUniversalLabelledHomEquivalence
#print axioms exactUniversalLabelledHomEquivalence_functor
#print axioms exactUniversalLabelledBicategoricalModelEquivalence
#print axioms exactUniversalLabelledBiequivalenceCertificate
#print axioms exactUniversalLabelledObjectEssentialSurjectivity

end

end KUOS.DependentOriginationExactUniversalLabelledBiequivalenceV4_89
