import KUOS.DependentOriginationExactUniversalAdjunctionLiftingV4_79
import Mathlib.CategoryTheory.Equivalence

namespace KUOS.DependentOriginationExactUniversalHomSectionV4_80

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMappingTwoCellV4_58
open KUOS.DependentOriginationExactUniversalMappingHomCategoryV4_60
open KUOS.DependentOriginationExactUniversalRealizationFaithfulV4_76
open KUOS.DependentOriginationExactUniversalRealizationFullyFaithfulV4_77

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# A coherent-retraction reduction of one-cell lifting v4.80

This is a conditional P1 theorem, not a proof of unconditional P1.

For a chosen exact-universal object X, let c_X be its presentation comparison.
A single strong transformation d_X with an invertible modification

  c_X >> d_X ~= identity

suffices to lift EVERY DO2 one-cell ell out of X.carrier. The raw component is

  d_X >> (restrict(ell) >> c_Y),

and the DO2 component is exactly ell. No counit, triangle law, inverse for c_Y,
or assumption that the particular ell is already liftable is needed.

The v4.77 compatible two-cell preimage makes this assignment a functor section
of realization. Local faithfulness proves its laws and the naturality of its
source unit. The resulting native hom-category equivalence has this explicit
section as its inverse functor, not an unspecified objectwise choice.

The coherent retraction is explicit INPUT. The pointwise-equivalence field of
ExactUniversalRawObject has NOT yet been assembled into this global datum here.
We neither add that field to the source object nor assert a global instance that
produces it. The remaining unconditional P1 obligation is that assembly. P2's
independently prescribed raw data, object coverage, and cross-hom higher
coherence are not asserted. The exact/weak sector boundary is unchanged.
-/

universe u v uH vH uB vB wB

section BicategoricalRetraction

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {R S T : B}

/-- A one-sided coherent retraction constructs one-cell preimages by composition.
The three factors retain the actual unitors, comparison isomorphism and
associator; no strictness of the ambient bicategory is assumed. -/
def oneCellPreimageIsoOfRetraction
    (c : R ⟶ S) (d : S ⟶ R) (h : c ≫ d ≅ 𝟙 R) (k : R ⟶ T) :
    k ≅ c ≫ (d ≫ k) :=
  (Bicategory.leftUnitor k).symm ≪≫
    Bicategory.whiskerRightIso h.symm k ≪≫
      Bicategory.associator c d k

/-- For all ambient targets, essential surjectivity of precomposition on
one-cells is equivalent to a one-sided coherent retraction. Necessity is tested
at the original source and its identity. This is NOT a claim that the restricted
collection of exact-universal targets alone detects a retraction. -/
theorem exists_retraction_iff_allTargetOneCellLift (c : R ⟶ S) :
    (∃ d : S ⟶ R, Nonempty (c ≫ d ≅ 𝟙 R)) ↔
      ∀ (T : B) (k : R ⟶ T), ∃ r : S ⟶ T, Nonempty (k ≅ c ≫ r) := by
  constructor
  · rintro ⟨d, ⟨h⟩⟩ T k
    exact ⟨d ≫ k, ⟨oneCellPreimageIsoOfRetraction c d h k⟩⟩
  · intro hlift
    rcases hlift R (𝟙 R) with ⟨d, ⟨h⟩⟩
    exact ⟨d, ⟨h.symm⟩⟩

end BicategoricalRetraction

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- The raw restriction of the chosen DO2 carrier, with its actual variance. -/
abbrev exactUniversalRestrictedCarrier
    (X : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A) :=
  restrictHigherLocalizedSystem W (higherStackObjectVal (W := W) A X.carrier)

/-- Additional coherent data used by this reduction theorem, not a new field
or automatically inhabited class of exact-universal source objects. Only the
one-sided inverse modification needed for precomposition is required. -/
structure ExactUniversalComparisonRetraction
    (X : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A) where
  retraction : X.raw ⟶ exactUniversalRestrictedCarrier (W := W) A X
  retractIso : X.presentation.comparison ≫ retraction ≅
    𝟙 (exactUniversalRestrictedCarrier (W := W) A X)

variable {X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A}

/-- Lift an arbitrary DO2 one-cell, with literal recovery of its DO2 component.
One coherent retraction of c_X works uniformly for every Y and every ell. -/
def exactUniversalMorphismOfComparisonRetraction
    (RX : ExactUniversalComparisonRetraction (W := W) A X)
    (ell : X.carrier ⟶ Y.carrier) :
    ExactUniversalRawMorphism (W := W) A X Y where
  raw := RX.retraction ≫
    (restrictHigherLocalizedStrongTrans (W := W) ell.hom ≫ Y.presentation.comparison)
  lift := ell
  comparison_square :=
    oneCellPreimageIsoOfRetraction X.presentation.comparison RX.retraction
      RX.retractIso
      (restrictHigherLocalizedStrongTrans (W := W) ell.hom ≫ Y.presentation.comparison)

@[simp] theorem exactUniversalMorphismOfComparisonRetraction_lift
    (RX : ExactUniversalComparisonRetraction (W := W) A X)
    (ell : X.carrier ⟶ Y.carrier) :
    (exactUniversalMorphismOfComparisonRetraction (W := W) A RX ell).lift = ell := rfl

/-- The result is stronger than essential surjectivity: no adjustment of ell
by an isomorphism is necessary. The retraction hypothesis remains explicit. -/
theorem exists_exactUniversalMorphism_of_comparisonRetraction
    (RX : ExactUniversalComparisonRetraction (W := W) A X)
    (ell : X.carrier ⟶ Y.carrier) :
    ∃ f : ExactUniversalRawMorphism (W := W) A X Y, f.lift = ell :=
  ⟨exactUniversalMorphismOfComparisonRetraction (W := W) A RX ell, rfl⟩

/-- The arbitrary-one-cell construction extends to a functor on each fixed
hom category. Its two-cell part reuses v4.77, rather than treating that theorem
as if it already provided one-cell preimages. -/
def exactUniversalHomSectionOfRetraction
    (RX : ExactUniversalComparisonRetraction (W := W) A X) :
    (X.carrier ⟶ Y.carrier) ⥤ ExactUniversalRawMorphism (W := W) A X Y where
  obj ell := exactUniversalMorphismOfComparisonRetraction (W := W) A RX ell
  map {ell₁ ell₂} eta :=
    exactUniversalCompletion2Preimage (W := W) A
      (f := exactUniversalMorphismOfComparisonRetraction (W := W) A RX ell₁)
      (g := exactUniversalMorphismOfComparisonRetraction (W := W) A RX ell₂) eta
  map_id ell := by
    apply exactUniversalCompletion2_map_injective (W := W) A
    rfl
  map_comp eta theta := by
    apply exactUniversalCompletion2_map_injective (W := W) A
    rfl

@[simp] theorem exactUniversalHomSection_obj_lift
    (RX : ExactUniversalComparisonRetraction (W := W) A X)
    (ell : X.carrier ⟶ Y.carrier) :
    ((exactUniversalHomSectionOfRetraction (W := W) A RX).obj ell).lift = ell := rfl

@[simp] theorem exactUniversalHomSection_map_lift
    (RX : ExactUniversalComparisonRetraction (W := W) A X)
    {ell₁ ell₂ : X.carrier ⟶ Y.carrier} (eta : ell₁ ⟶ ell₂) :
    ((exactUniversalHomSectionOfRetraction (W := W) A RX).map eta).lift = eta := rfl

/-- This is equality of functors, including their action on two-cells, not just
an objectwise or up-to-isomorphism section. -/
theorem exactUniversalHomSection_comp_realization
    (RX : ExactUniversalComparisonRetraction (W := W) A X) :
    exactUniversalHomSectionOfRetraction (W := W) A RX (Y := Y) ⋙
      exactUniversalCompletion2HomFunctor (W := W) A X Y =
        𝟭 (X.carrier ⟶ Y.carrier) := rfl

/-- Every old source one-cell is isomorphic to the chosen section over its lift.
No equality with an independently prescribed raw comparison is asserted. -/
def exactUniversalSourceIsoSectionOfRetraction
    (RX : ExactUniversalComparisonRetraction (W := W) A X)
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    f ≅ (exactUniversalHomSectionOfRetraction (W := W) A RX).obj f.lift :=
  exactUniversalSourceIsoOfLift (W := W) A
    (f := f)
    (g := exactUniversalMorphismOfComparisonRetraction (W := W) A RX f.lift)
    (Iso.refl f.lift)

@[simp] theorem exactUniversalSourceIsoSection_hom_lift
    (RX : ExactUniversalComparisonRetraction (W := W) A X)
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    (exactUniversalSourceIsoSectionOfRetraction (W := W) A RX f).hom.lift =
      𝟙 f.lift := by
  exact (exactUniversalCompletion2HomFunctor (W := W) A X Y).map_preimage
    (X := f)
    (Y := exactUniversalMorphismOfComparisonRetraction (W := W) A RX f.lift)
    (𝟙 f.lift)

@[simp] theorem exactUniversalSourceIsoSection_inv_lift
    (RX : ExactUniversalComparisonRetraction (W := W) A X)
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    (exactUniversalSourceIsoSectionOfRetraction (W := W) A RX f).inv.lift =
      𝟙 f.lift := by
  exact (exactUniversalCompletion2HomFunctor (W := W) A X Y).map_preimage
    (X := exactUniversalMorphismOfComparisonRetraction (W := W) A RX f.lift)
    (Y := f) (𝟙 f.lift)

/-- Local naturality is proved by faithful realization, so the objectwise
source isomorphisms really form a natural isomorphism on this hom category. -/
def exactUniversalHomSectionUnitIso
    (RX : ExactUniversalComparisonRetraction (W := W) A X) :
    𝟭 (ExactUniversalRawMorphism (W := W) A X Y) ≅
      exactUniversalCompletion2HomFunctor (W := W) A X Y ⋙
        exactUniversalHomSectionOfRetraction (W := W) A RX :=
  NatIso.ofComponents
    (fun f => exactUniversalSourceIsoSectionOfRetraction (W := W) A RX f)
    (by
      intro f g eta
      apply exactUniversalCompletion2_map_injective (W := W) A
      change eta.lift ≫
          (exactUniversalSourceIsoSectionOfRetraction (W := W) A RX g).hom.lift =
        (exactUniversalSourceIsoSectionOfRetraction (W := W) A RX f).hom.lift ≫
          eta.lift
      rw [exactUniversalSourceIsoSection_hom_lift,
        exactUniversalSourceIsoSection_hom_lift]
      simp only [Category.comp_id, Category.id_comp])

/-- Conditional native hom-category equivalence with the explicit constructed
section as inverse. Mathlib supplies the adjointification required by its
Equivalence constructor; no extra triangle hypothesis is imposed. -/
def exactUniversalHomEquivalenceOfRetraction
    (RX : ExactUniversalComparisonRetraction (W := W) A X) :
    ExactUniversalRawMorphism (W := W) A X Y ≌ (X.carrier ⟶ Y.carrier) :=
  CategoryTheory.Equivalence.mk
    (exactUniversalCompletion2HomFunctor (W := W) A X Y)
    (exactUniversalHomSectionOfRetraction (W := W) A RX)
    (exactUniversalHomSectionUnitIso (W := W) A RX)
    (eqToIso (exactUniversalHomSection_comp_realization (W := W) A RX))

/-- The actual realization functor is essentially surjective under the stated
coherent retraction, not an unrelated replacement functor. -/
def exactUniversalCompletion2HomEssSurjOfRetraction
    (RX : ExactUniversalComparisonRetraction (W := W) A X) :
    (exactUniversalCompletion2HomFunctor (W := W) A X Y).EssSurj :=
  ⟨fun ell =>
    ⟨exactUniversalMorphismOfComparisonRetraction (W := W) A RX ell,
      ⟨Iso.refl ell⟩⟩⟩

/-- The native IsEquivalence interface retains the explicit retraction input.
It is deliberately not installed as an unconditional global instance. -/
def exactUniversalCompletion2HomIsEquivalenceOfRetraction
    (RX : ExactUniversalComparisonRetraction (W := W) A X) :
    (exactUniversalCompletion2HomFunctor (W := W) A X Y).IsEquivalence where
  essSurj := exactUniversalCompletion2HomEssSurjOfRetraction (W := W) A RX

/-! ## Regression checks for exact projection and both functors. -/

variable (RX : ExactUniversalComparisonRetraction (W := W) A X)

example (ell : X.carrier ⟶ Y.carrier) :
    (exactUniversalMorphismOfComparisonRetraction (W := W) A RX ell).lift = ell := rfl

example (ell : X.carrier ⟶ Y.carrier) :
    (exactUniversalMorphismOfComparisonRetraction (W := W) A RX ell).raw =
      RX.retraction ≫
        (restrictHigherLocalizedStrongTrans (W := W) ell.hom ≫
          Y.presentation.comparison) := rfl

example (ell : X.carrier ⟶ Y.carrier) :
    ∃ f : ExactUniversalRawMorphism (W := W) A X Y, f.lift = ell :=
  exists_exactUniversalMorphism_of_comparisonRetraction (W := W) A RX ell

example (ell : X.carrier ⟶ Y.carrier) :
    ∃ f : ExactUniversalRawMorphism (W := W) A X Y, Nonempty (f.lift ≅ ell) :=
  ⟨exactUniversalMorphismOfComparisonRetraction (W := W) A RX ell, ⟨Iso.refl ell⟩⟩

example {ell₁ ell₂ : X.carrier ⟶ Y.carrier} (eta : ell₁ ⟶ ell₂) :
    ((exactUniversalHomSectionOfRetraction (W := W) A RX).map eta).lift = eta := rfl

example (ell : X.carrier ⟶ Y.carrier) :
    (exactUniversalHomSectionOfRetraction (W := W) A RX).map (𝟙 ell) =
      𝟙 ((exactUniversalHomSectionOfRetraction (W := W) A RX).obj ell) :=
  (exactUniversalHomSectionOfRetraction (W := W) A RX).map_id ell

example {ell₁ ell₂ ell₃ : X.carrier ⟶ Y.carrier}
    (eta : ell₁ ⟶ ell₂) (theta : ell₂ ⟶ ell₃) :
    (exactUniversalHomSectionOfRetraction (W := W) A RX).map (eta ≫ theta) =
      (exactUniversalHomSectionOfRetraction (W := W) A RX).map eta ≫
        (exactUniversalHomSectionOfRetraction (W := W) A RX).map theta :=
  (exactUniversalHomSectionOfRetraction (W := W) A RX).map_comp eta theta

example :
    exactUniversalHomSectionOfRetraction (W := W) A RX (Y := Y) ⋙
      exactUniversalCompletion2HomFunctor (W := W) A X Y =
        𝟭 (X.carrier ⟶ Y.carrier) :=
  exactUniversalHomSection_comp_realization (W := W) A RX

example :
    (exactUniversalHomEquivalenceOfRetraction (W := W) A RX (Y := Y)).functor =
      exactUniversalCompletion2HomFunctor (W := W) A X Y := rfl

example :
    (exactUniversalHomEquivalenceOfRetraction (W := W) A RX (Y := Y)).inverse =
      exactUniversalHomSectionOfRetraction (W := W) A RX := rfl

example (f : ExactUniversalRawMorphism (W := W) A X Y) :
    (exactUniversalSourceIsoSectionOfRetraction (W := W) A RX f).hom.lift = 𝟙 f.lift :=
  exactUniversalSourceIsoSection_hom_lift (W := W) A RX f

example (f : ExactUniversalRawMorphism (W := W) A X Y) :
    (exactUniversalSourceIsoSectionOfRetraction (W := W) A RX f).inv.lift = 𝟙 f.lift :=
  exactUniversalSourceIsoSection_inv_lift (W := W) A RX f

example (f : ExactUniversalRawMorphism (W := W) A X Y) :
    (exactUniversalCompletion2HomFunctor (W := W) A X Y).mapIso
      (exactUniversalSourceIsoSectionOfRetraction (W := W) A RX f) =
        Iso.refl f.lift := by
  apply Iso.ext
  exact exactUniversalSourceIsoSection_hom_lift (W := W) A RX f

example : (exactUniversalCompletion2HomFunctor (W := W) A X Y).EssSurj :=
  exactUniversalCompletion2HomEssSurjOfRetraction (W := W) A RX

example : (exactUniversalCompletion2HomFunctor (W := W) A X Y).IsEquivalence :=
  exactUniversalCompletion2HomIsEquivalenceOfRetraction (W := W) A RX

#print axioms exists_retraction_iff_allTargetOneCellLift
#print axioms exactUniversalMorphismOfComparisonRetraction
#print axioms exactUniversalHomSectionOfRetraction
#print axioms exactUniversalHomSection_comp_realization
#print axioms exactUniversalHomSectionUnitIso
#print axioms exactUniversalHomEquivalenceOfRetraction
#print axioms exactUniversalCompletion2HomIsEquivalenceOfRetraction

end

end KUOS.DependentOriginationExactUniversalHomSectionV4_80
