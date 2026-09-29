import KUOS.DependentOriginationExactUniversalHomSectionV4_80
import KUOS.DependentOriginationPointwiseInverseCoherenceV4_82

namespace KUOS.DependentOriginationExactUniversalHomEquivalenceV4_83

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMappingHomCategoryV4_60
open KUOS.DependentOriginationExactUniversalAdjunctionLiftingV4_79
open KUOS.DependentOriginationExactUniversalHomSectionV4_80
open KUOS.DependentOriginationPointwiseInverseCoherenceV4_82

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Hom-category equivalence on the existing exact-universal sector v4.83

Instantiate v4.82 on X.presentation.comparison, using exactly its already
stored pointwise IsEquivalence field on LocallyDiscrete Context. The resulting
coherent retraction supplies v4.80's formerly explicit extra input.

For each existing pair X,Y and EVERY DO2 one-cell ell between their carriers,
construct a source one-cell with lift literally equal to ell. The construction
extends to a hom-category section whose composite with realization is equal
to the identity functor. The source-side unit is a natural isomorphism, so the
actual realization hom functor is an equivalence of categories.

No coherent inverse, liftability, or new admissibility hypothesis is supplied
by the caller. No field is added to ExactUniversalRawObject. This discharges P1
on this chosen exact-universal sector, not on the weakly admissible sector.
The new EssSurj/IsEquivalence instances are restricted to these existing objects.

This is a hom-category equivalence, NOT an isomorphism of categories or a
literal inverse on raw one-cells. The independently chosen source raw data of
P2, object coverage, cross-hom higher coherence and a final mapping biequivalence
remain separate. Our explicit source-unit iso retains both realized identity
components; no claim is made that Equivalence.mk leaves that unit unchanged.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- Adapt the stored Context-indexed field to the actual raw base bicategory.
This changes only the index wrapper; it adds no assumption and no opposite. -/
theorem exactUniversalComparisonPointwiseEquivalence
    (X : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
    (U : LocallyDiscrete Context) :
    (X.presentation.comparison.app U).toFunctor.IsEquivalence := by
  rcases U with ⟨U⟩
  exact X.presentation.comparison_isEquivalence U

/-- The v4.80 retraction data are now constructed from the existing presentation.
Both fields use the same pointwise witness and the same chosen inverse. -/
def exactUniversalComparisonRetraction
    (X : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A) :
    ExactUniversalComparisonRetraction (W := W) A X where
  retraction := pointwiseInverseStrongTrans X.presentation.comparison
    (exactUniversalComparisonPointwiseEquivalence (W := W) A X)
  retractIso := pointwiseInverseRetractionIso X.presentation.comparison
    (exactUniversalComparisonPointwiseEquivalence (W := W) A X)

/-- Lift any realized one-cell. Source objects are explicit: the carrier
projections alone must not be used to infer their chosen presentations. -/
def exactUniversalOneCellOfLift
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
    (ell : X.carrier ⟶ Y.carrier) : ExactUniversalRawMorphism (W := W) A X Y :=
  exactUniversalMorphismOfComparisonRetraction (W := W) A (X := X) (Y := Y)
    (exactUniversalComparisonRetraction (W := W) A X) ell

@[simp] theorem exactUniversalOneCellOfLift_lift
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
    (ell : X.carrier ⟶ Y.carrier) :
    (exactUniversalOneCellOfLift (W := W) A X Y ell).lift = ell := rfl

/-- Stronger than essential surjectivity: the chosen lift is exactly ell.
There is no uniqueness assertion about the source one-cell itself. -/
theorem exists_exactUniversalOneCell_of_lift
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
    (ell : X.carrier ⟶ Y.carrier) :
    ∃ f : ExactUniversalRawMorphism (W := W) A X Y, f.lift = ell :=
  ⟨exactUniversalOneCellOfLift (W := W) A X Y ell, rfl⟩

/-- P1 in its original essential-surjectivity form, with no extra input. -/
theorem exists_exactUniversalOneCell_iso_lift
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
    (ell : X.carrier ⟶ Y.carrier) :
    ∃ f : ExactUniversalRawMorphism (W := W) A X Y, Nonempty (f.lift ≅ ell) :=
  ⟨exactUniversalOneCellOfLift (W := W) A X Y ell, ⟨Iso.refl ell⟩⟩

/-- A section on each fixed hom category, using v4.77's compatible two-cell
preimages through v4.80. It constructs one-cells as well as two-cells. -/
def exactUniversalHomSection
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A) :
    (X.carrier ⟶ Y.carrier) ⥤ ExactUniversalRawMorphism (W := W) A X Y :=
  exactUniversalHomSectionOfRetraction (W := W) A (X := X) (Y := Y)
    (exactUniversalComparisonRetraction (W := W) A X)

@[simp] theorem exactUniversalHomSection_obj_lift_exact
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
    (ell : X.carrier ⟶ Y.carrier) :
    ((exactUniversalHomSection (W := W) A X Y).obj ell).lift = ell := rfl

@[simp] theorem exactUniversalHomSection_map_lift_exact
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
    {ell₁ ell₂ : X.carrier ⟶ Y.carrier} (eta : ell₁ ⟶ ell₂) :
    ((exactUniversalHomSection (W := W) A X Y).map eta).lift = eta := rfl

/-- Literal equality of the composite hom functor, including its two-cell map. -/
theorem exactUniversalHomSection_realization
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A) :
    exactUniversalHomSection (W := W) A X Y ⋙
      exactUniversalCompletion2HomFunctor (W := W) A X Y =
        𝟭 (X.carrier ⟶ Y.carrier) :=
  exactUniversalHomSection_comp_realization (W := W) A (X := X) (Y := Y)
    (exactUniversalComparisonRetraction (W := W) A X)

/-- The source-side round trip is naturally isomorphic to identity; it need
not be literally equal to an independently prescribed raw transformation. -/
def exactUniversalHomUnitIso
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A) :
    𝟭 (ExactUniversalRawMorphism (W := W) A X Y) ≅
      exactUniversalCompletion2HomFunctor (W := W) A X Y ⋙
        exactUniversalHomSection (W := W) A X Y :=
  exactUniversalHomSectionUnitIso (W := W) A (X := X) (Y := Y)
    (exactUniversalComparisonRetraction (W := W) A X)

variable {X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A}

@[simp] theorem exactUniversalHomUnitIso_hom_lift
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    ((exactUniversalHomUnitIso (W := W) A X Y).hom.app f).lift = 𝟙 f.lift :=
  exactUniversalSourceIsoSection_hom_lift (W := W) A
    (exactUniversalComparisonRetraction (W := W) A X) f

@[simp] theorem exactUniversalHomUnitIso_inv_lift
    (f : ExactUniversalRawMorphism (W := W) A X Y) :
    ((exactUniversalHomUnitIso (W := W) A X Y).inv.app f).lift = 𝟙 f.lift :=
  exactUniversalSourceIsoSection_inv_lift (W := W) A
    (exactUniversalComparisonRetraction (W := W) A X) f

/-- The actual realization hom functor is the forward functor of this
Mathlib equivalence, and the explicitly constructed section is its inverse. -/
def exactUniversalHomEquivalence
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A) :
    ExactUniversalRawMorphism (W := W) A X Y ≌ (X.carrier ⟶ Y.carrier) :=
  exactUniversalHomEquivalenceOfRetraction (W := W) A (X := X) (Y := Y)
    (exactUniversalComparisonRetraction (W := W) A X)

@[simp] theorem exactUniversalHomEquivalence_functor
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A) :
    (exactUniversalHomEquivalence (W := W) A X Y).functor =
      exactUniversalCompletion2HomFunctor (W := W) A X Y := rfl

@[simp] theorem exactUniversalHomEquivalence_inverse
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A) :
    (exactUniversalHomEquivalence (W := W) A X Y).inverse =
      exactUniversalHomSection (W := W) A X Y := rfl

/-- No extra hypothesis: the instance is restricted to the chosen
exact-universal objects whose comparisons are already pointwise equivalences. -/
instance exactUniversalCompletion2HomFunctor_essSurj
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A) :
    (exactUniversalCompletion2HomFunctor (W := W) A X Y).EssSurj :=
  exactUniversalCompletion2HomEssSurjOfRetraction (W := W) A (X := X) (Y := Y)
    (exactUniversalComparisonRetraction (W := W) A X)

/-- Native equivalence interface for the existing realization hom functor. -/
instance exactUniversalCompletion2HomFunctor_isEquivalence
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A) :
    (exactUniversalCompletion2HomFunctor (W := W) A X Y).IsEquivalence :=
  exactUniversalCompletion2HomIsEquivalenceOfRetraction (W := W) A (X := X) (Y := Y)
    (exactUniversalComparisonRetraction (W := W) A X)

/-! ## Regression checks: no extra retraction, liftability or coherence assumptions. -/

example (U : Context) :
    (X.presentation.comparison.app (.mk U)).toFunctor.IsEquivalence :=
  exactUniversalComparisonPointwiseEquivalence (W := W) A X (.mk U)

example : X.presentation.comparison ≫
    (exactUniversalComparisonRetraction (W := W) A X).retraction ≅
      𝟙 (exactUniversalRestrictedCarrier (W := W) A X) :=
  (exactUniversalComparisonRetraction (W := W) A X).retractIso

example (ell : X.carrier ⟶ Y.carrier) :
    (exactUniversalOneCellOfLift (W := W) A X Y ell).lift = ell := rfl

example (ell : X.carrier ⟶ Y.carrier) :
    (exactUniversalOneCellOfLift (W := W) A X Y ell).raw =
      (exactUniversalComparisonRetraction (W := W) A X).retraction ≫
        (restrictHigherLocalizedStrongTrans (W := W) ell.hom ≫
          Y.presentation.comparison) := rfl

example (ell : X.carrier ⟶ Y.carrier) :
    ∃ f : ExactUniversalRawMorphism (W := W) A X Y, f.lift = ell :=
  exists_exactUniversalOneCell_of_lift (W := W) A X Y ell

example (ell : X.carrier ⟶ Y.carrier) :
    ∃ f : ExactUniversalRawMorphism (W := W) A X Y, Nonempty (f.lift ≅ ell) :=
  exists_exactUniversalOneCell_iso_lift (W := W) A X Y ell

example (ell : X.carrier ⟶ Y.carrier) :
    ((exactUniversalHomSection (W := W) A X Y).obj ell).lift = ell := rfl

example {ell₁ ell₂ : X.carrier ⟶ Y.carrier} (eta : ell₁ ⟶ ell₂) :
    ((exactUniversalHomSection (W := W) A X Y).map eta).lift = eta := rfl

example (ell : X.carrier ⟶ Y.carrier) :
    (exactUniversalHomSection (W := W) A X Y).map (𝟙 ell) =
      𝟙 ((exactUniversalHomSection (W := W) A X Y).obj ell) :=
  (exactUniversalHomSection (W := W) A X Y).map_id ell

example {ell₁ ell₂ ell₃ : X.carrier ⟶ Y.carrier}
    (eta : ell₁ ⟶ ell₂) (theta : ell₂ ⟶ ell₃) :
    (exactUniversalHomSection (W := W) A X Y).map (eta ≫ theta) =
      (exactUniversalHomSection (W := W) A X Y).map eta ≫
        (exactUniversalHomSection (W := W) A X Y).map theta :=
  (exactUniversalHomSection (W := W) A X Y).map_comp eta theta

example : exactUniversalHomSection (W := W) A X Y ⋙
    exactUniversalCompletion2HomFunctor (W := W) A X Y =
      𝟭 (X.carrier ⟶ Y.carrier) :=
  exactUniversalHomSection_realization (W := W) A X Y

example : (X ⟶ Y) ≌ (X.carrier ⟶ Y.carrier) :=
  exactUniversalHomEquivalence (W := W) A X Y

example : (exactUniversalHomEquivalence (W := W) A X Y).functor =
    exactUniversalCompletion2HomFunctor (W := W) A X Y := rfl

example : (exactUniversalHomEquivalence (W := W) A X Y).inverse =
    exactUniversalHomSection (W := W) A X Y := rfl

example (f : ExactUniversalRawMorphism (W := W) A X Y) :
    ((exactUniversalHomUnitIso (W := W) A X Y).hom.app f).lift = 𝟙 f.lift :=
  exactUniversalHomUnitIso_hom_lift (W := W) A f

example (f : ExactUniversalRawMorphism (W := W) A X Y) :
    ((exactUniversalHomUnitIso (W := W) A X Y).inv.app f).lift = 𝟙 f.lift :=
  exactUniversalHomUnitIso_inv_lift (W := W) A f

example {f g : ExactUniversalRawMorphism (W := W) A X Y} (eta : f ⟶ g) :
    eta ≫ (exactUniversalHomUnitIso (W := W) A X Y).hom.app g =
      (exactUniversalHomUnitIso (W := W) A X Y).hom.app f ≫
        (exactUniversalHomSection (W := W) A X Y).map eta.lift :=
  (exactUniversalHomUnitIso (W := W) A X Y).hom.naturality eta

example {f g : ExactUniversalRawMorphism (W := W) A X Y} (eta : f ⟶ g) :
    (exactUniversalHomSection (W := W) A X Y).map eta.lift ≫
        (exactUniversalHomUnitIso (W := W) A X Y).inv.app g =
      (exactUniversalHomUnitIso (W := W) A X Y).inv.app f ≫ eta :=
  (exactUniversalHomUnitIso (W := W) A X Y).inv.naturality eta

example (f : ExactUniversalRawMorphism (W := W) A X Y) :
    (exactUniversalCompletion2HomFunctor (W := W) A X Y).mapIso
      ((exactUniversalHomUnitIso (W := W) A X Y).app f) = Iso.refl f.lift := by
  apply Iso.ext
  exact exactUniversalHomUnitIso_hom_lift (W := W) A f

example : (exactUniversalCompletion2HomFunctor (W := W) A X Y).EssSurj :=
  inferInstance

example : (exactUniversalCompletion2HomFunctor (W := W) A X Y).IsEquivalence :=
  inferInstance

example : Nonempty ((X ⟶ Y) ≌ (X.carrier ⟶ Y.carrier)) :=
  ⟨(exactUniversalCompletion2HomFunctor (W := W) A X Y).asEquivalence⟩

-- v4.79 applies to the now-constructed legs of ANY realized adjunction.
-- The legs are fixed by our section; their raw components are not prescribed independently.
example (ell : X.carrier ⟶ Y.carrier) (k : Y.carrier ⟶ X.carrier)
    (adj : Bicategory.Adjunction ell k) :
    ∃! a : Bicategory.Adjunction
        (exactUniversalOneCellOfLift (W := W) A X Y ell)
        (exactUniversalOneCellOfLift (W := W) A Y X k),
      a.unit.lift = adj.unit ∧ a.counit.lift = adj.counit :=
  existsUnique_exactUniversalAdjunction_of_lift (W := W) A
    (exactUniversalOneCellOfLift (W := W) A X Y ell)
    (exactUniversalOneCellOfLift (W := W) A Y X k) adj

#print axioms exactUniversalComparisonRetraction
#print axioms exactUniversalOneCellOfLift
#print axioms exists_exactUniversalOneCell_of_lift
#print axioms exists_exactUniversalOneCell_iso_lift
#print axioms exactUniversalHomSection
#print axioms exactUniversalHomSection_realization
#print axioms exactUniversalHomUnitIso
#print axioms exactUniversalHomEquivalence
#print axioms exactUniversalCompletion2HomFunctor_isEquivalence

end

end KUOS.DependentOriginationExactUniversalHomEquivalenceV4_83
