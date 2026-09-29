import KUOS.DependentOriginationExactUniversalRealizationFullyFaithfulV4_77
import KUOS.DependentOriginationExactUniversalEquivalenceLegLiftabilityV4_73
import Mathlib.CategoryTheory.Bicategory.Adjunction.Basic

namespace KUOS.DependentOriginationExactUniversalSourceEquivalenceV4_78

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationExactPresentationComparisonV4_52
open KUOS.DependentOriginationExactUniversalTargetNaturalityV4_55
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMappingBicategoryV4_69
open KUOS.DependentOriginationExactUniversalEquivalenceLegLiftabilityV4_73
open KUOS.DependentOriginationExactUniversalRealizationFullyFaithfulV4_77

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Source adjoint equivalences from coherent raw inverse data v4.78

v4.73 supplies source lifts of both legs of a coherent raw equivalence.
v4.77 lifts every DO₂ isomorphism between existing source 1-cells.

First, a source endomorphism whose raw component is isomorphic to the identity
produces a coherent endocomparison of the chosen presentation. Essential
uniqueness compares its DO₂ component with the source identity. Local full
faithfulness then gives an isomorphism in the source hom category itself.

Apply this to both composites of a chosen pair of source 1-cells. Mathlib's
`Bicategory.Equivalence.mkOfAdjointifyCounit` supplies the triangle identities,
retaining both chosen 1-cells. Thus coherent raw equivalence gives an actual
source adjoint equivalence with exactly the prescribed raw forward/backward legs.

The source 2-isomorphisms are constructed, not assumed. Their raw components are
NOT asserted to equal the supplied raw unit/counit: essential uniqueness does
not prescribe the comparison modification, and adjointification adjusts the
counit. The theorem is about existence of a source adjoint equivalence with fixed
1-cell legs, not a lift of an entire prescribed adjunction, nor the final mapping
biequivalence or essential surjectivity on arbitrary DO₂ 1-cells.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))
variable {X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A}

/-- Close the raw identity comparison by whiskering the given raw isomorphism.
This changes only the triangle, not the localized StrongTrans. -/
def exactUniversalComparisonOfRawIdentity
    (h : ExactUniversalRawMorphism (W := W) A X X)
    (rawIso : h.raw ≅ 𝟙 X.raw) :
    ExactPresentationCoherentComparison (W := W) A X.presentation X.presentation where
  hom := h.lift.hom
  comparison_triangle := by
    change (restrictHigherLocalizedStrongTrans (W := W) h.lift.hom ≫
      X.presentation.comparison) ≅ X.presentation.comparison
    exact h.comparison_square ≪≫
      Bicategory.whiskerLeftIso X.presentation.comparison rawIso ≪≫
      Bicategory.rightUnitor X.presentation.comparison

/-- Essential uniqueness and v4.77 promote a raw identity isomorphism to
existence of a source identity isomorphism. No prescribed raw 2-cell is claimed. -/
theorem exactUniversalEndomorphism_iso_id_of_rawIso
    (h : ExactUniversalRawMorphism (W := W) A X X)
    (rawIso : h.raw ≅ 𝟙 X.raw) : Nonempty (h ≅ 𝟙 X) := by
  let alpha := exactUniversalComparisonOfRawIdentity (W := W) A h rawIso
  let beta := exactUniversalComparisonOfRawIdentity (W := W) A
    (ExactUniversalRawMorphism.id (W := W) A X) (Iso.refl (𝟙 X.raw))
  rcases X.universal.essential_unique X.presentation alpha beta with ⟨ell⟩
  have ell' : h.lift.hom ≅
      (ExactUniversalRawMorphism.id (W := W) A X).lift.hom := ell
  have liftIso : h.lift ≅ (ExactUniversalRawMorphism.id (W := W) A X).lift :=
    Bicategory.InducedBicategory.isoMk ell'
  exact ⟨exactUniversalSourceIsoOfLift (W := W) A
    (f := h) (g := ExactUniversalRawMorphism.id (W := W) A X) liftIso⟩

/-- A source unit exists for every chosen pair whose raw composite has a unit.
The raw component of this chosen unit need not be the supplied one. -/
def exactUniversalSourceUnitOfRawInverse
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    (g : ExactUniversalRawMorphism (W := W) A Y X)
    (rawUnit : 𝟙 X.raw ≅ f.raw ≫ g.raw) : 𝟙 X ≅ f ≫ g := by
  -- Pin the chosen source object and composite before eliminating `Nonempty`.
  have hfg : Nonempty (f ≫ g ≅ 𝟙 X) :=
    exactUniversalEndomorphism_iso_id_of_rawIso (W := W) A (X := X)
      (ExactUniversalRawMorphism.comp (W := W) A f g) rawUnit.symm
  exact (Classical.choice hfg).symm

/-- A source counit exists for every chosen pair whose raw composite has a
counit. Mathlib will subsequently adjust this counit for the triangle law. -/
def exactUniversalSourceCounitOfRawInverse
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    (g : ExactUniversalRawMorphism (W := W) A Y X)
    (rawCounit : g.raw ≫ f.raw ≅ 𝟙 Y.raw) : g ≫ f ≅ 𝟙 Y := by
  -- The endomorphism lemma's object parameter is now the target object `Y`.
  have hgf : Nonempty (g ≫ f ≅ 𝟙 Y) :=
    exactUniversalEndomorphism_iso_id_of_rawIso (W := W) A (X := Y)
      (ExactUniversalRawMorphism.comp (W := W) A g f) rawCounit
  exact Classical.choice hgf

/-- Adjointify the constructed source unit/counit using Mathlib. Both chosen
source 1-cells are retained exactly; no source inverse laws are assumed. -/
def exactUniversalSourceEquivalenceOfRawInverse
    (f : ExactUniversalRawMorphism (W := W) A X Y)
    (g : ExactUniversalRawMorphism (W := W) A Y X)
    (rawUnit : 𝟙 X.raw ≅ f.raw ≫ g.raw)
    (rawCounit : g.raw ≫ f.raw ≅ 𝟙 Y.raw) : Bicategory.Equivalence X Y :=
  Bicategory.Equivalence.mkOfAdjointifyCounit
    (exactUniversalSourceUnitOfRawInverse (W := W) A f g rawUnit)
    (exactUniversalSourceCounitOfRawInverse (W := W) A f g rawCounit)

/-- Coherent raw equivalence lifts to an actual source adjoint equivalence,
with the raw forward and backward legs preserved exactly. -/
theorem exists_exactUniversalSourceEquivalence_of_rawCoherentEquivalence
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
    (E : HigherRawSystemCoherentEquivalence X.raw Y.raw) :
    ∃ e : Bicategory.Equivalence X Y,
      e.hom.raw = E.forward.comparison ∧ e.inv.raw = E.backward.comparison := by
  rcases exists_exactUniversalRawMorphism_forward_of_rawCoherentEquivalence
    (W := W) A X Y E with ⟨f, hf⟩
  rcases exists_exactUniversalRawMorphism_backward_of_rawCoherentEquivalence
    (W := W) A X Y E with ⟨g, hg⟩
  have hfg : f.raw ≫ g.raw = E.forward.comparison ≫ E.backward.comparison :=
    congrArg₂ (fun (a : X.raw ⟶ Y.raw) (b : Y.raw ⟶ X.raw) => a ≫ b) hf hg
  have hgf : g.raw ≫ f.raw = E.backward.comparison ≫ E.forward.comparison :=
    congrArg₂ (fun (b : Y.raw ⟶ X.raw) (a : X.raw ⟶ Y.raw) => b ≫ a) hg hf
  let rawUnit : 𝟙 X.raw ≅ f.raw ≫ g.raw := E.unit ≪≫ (eqToIso hfg).symm
  let rawCounit : g.raw ≫ f.raw ≅ 𝟙 Y.raw := eqToIso hgf ≪≫ E.counit
  refine ⟨exactUniversalSourceEquivalenceOfRawInverse
    (W := W) A f g rawUnit rawCounit, ?_, ?_⟩
  · exact hf
  · exact hg

/-- Source objects, not merely their realized carriers, are adjoint equivalent
under coherent raw equivalence. -/
theorem exactUniversalRawObject_equivalent_of_rawCoherentEquivalence
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A)
    (E : HigherRawSystemCoherentEquivalence X.raw Y.raw) :
    Nonempty (Bicategory.Equivalence X Y) := by
  rcases exists_exactUniversalSourceEquivalence_of_rawCoherentEquivalence
    (W := W) A X Y E with ⟨e, _, _⟩
  exact ⟨e⟩

/-! ## Regression checks: source-level inverse data and native triangle laws. -/

-- Check each choice boundary without assuming the other raw inverse cell.
example (f : ExactUniversalRawMorphism (W := W) A X Y)
    (g : ExactUniversalRawMorphism (W := W) A Y X)
    (rawUnit : 𝟙 X.raw ≅ f.raw ≫ g.raw) : Nonempty (𝟙 X ≅ f ≫ g) :=
  ⟨exactUniversalSourceUnitOfRawInverse (W := W) A f g rawUnit⟩

example (f : ExactUniversalRawMorphism (W := W) A X Y)
    (g : ExactUniversalRawMorphism (W := W) A Y X)
    (rawCounit : g.raw ≫ f.raw ≅ 𝟙 Y.raw) : Nonempty (g ≫ f ≅ 𝟙 Y) :=
  ⟨exactUniversalSourceCounitOfRawInverse (W := W) A f g rawCounit⟩

example (h : ExactUniversalRawMorphism (W := W) A X X)
    (rawIso : h.raw ≅ 𝟙 X.raw) : Nonempty (h ≅ 𝟙 X) :=
  exactUniversalEndomorphism_iso_id_of_rawIso (W := W) A h rawIso

example (f : ExactUniversalRawMorphism (W := W) A X Y)
    (g : ExactUniversalRawMorphism (W := W) A Y X)
    (rawUnit : 𝟙 X.raw ≅ f.raw ≫ g.raw)
    (rawCounit : g.raw ≫ f.raw ≅ 𝟙 Y.raw) :
    (exactUniversalSourceEquivalenceOfRawInverse
      (W := W) A f g rawUnit rawCounit).hom = f := rfl

example (f : ExactUniversalRawMorphism (W := W) A X Y)
    (g : ExactUniversalRawMorphism (W := W) A Y X)
    (rawUnit : 𝟙 X.raw ≅ f.raw ≫ g.raw)
    (rawCounit : g.raw ≫ f.raw ≅ 𝟙 Y.raw) :
    (exactUniversalSourceEquivalenceOfRawInverse
      (W := W) A f g rawUnit rawCounit).inv = g := rfl

example (f : ExactUniversalRawMorphism (W := W) A X Y)
    (g : ExactUniversalRawMorphism (W := W) A Y X)
    (rawUnit : 𝟙 X.raw ≅ f.raw ≫ g.raw)
    (rawCounit : g.raw ≫ f.raw ≅ 𝟙 Y.raw) :
    let e := exactUniversalSourceEquivalenceOfRawInverse
      (W := W) A f g rawUnit rawCounit
    Bicategory.leftZigzagIso e.unit e.counit =
      Bicategory.leftUnitor e.hom ≪≫ (Bicategory.rightUnitor e.hom).symm :=
  (exactUniversalSourceEquivalenceOfRawInverse
    (W := W) A f g rawUnit rawCounit).left_triangle

example (f : ExactUniversalRawMorphism (W := W) A X Y)
    (g : ExactUniversalRawMorphism (W := W) A Y X)
    (rawUnit : 𝟙 X.raw ≅ f.raw ≫ g.raw)
    (rawCounit : g.raw ≫ f.raw ≅ 𝟙 Y.raw) :
    let e := exactUniversalSourceEquivalenceOfRawInverse
      (W := W) A f g rawUnit rawCounit
    Bicategory.rightZigzagIso e.unit e.counit =
      Bicategory.rightUnitor e.inv ≪≫ (Bicategory.leftUnitor e.inv).symm :=
  (exactUniversalSourceEquivalenceOfRawInverse
    (W := W) A f g rawUnit rawCounit).right_triangle

example (E : HigherRawSystemCoherentEquivalence X.raw Y.raw) :
    ∃ e : Bicategory.Equivalence X Y,
      e.hom.raw = E.forward.comparison ∧ e.inv.raw = E.backward.comparison :=
  exists_exactUniversalSourceEquivalence_of_rawCoherentEquivalence (W := W) A X Y E

example (E : HigherRawSystemCoherentEquivalence X.raw Y.raw) :
    Nonempty (Bicategory.Equivalence X Y) :=
  exactUniversalRawObject_equivalent_of_rawCoherentEquivalence (W := W) A X Y E

#print axioms exactUniversalEndomorphism_iso_id_of_rawIso
#print axioms exactUniversalSourceUnitOfRawInverse
#print axioms exactUniversalSourceCounitOfRawInverse
#print axioms exactUniversalSourceEquivalenceOfRawInverse
#print axioms exists_exactUniversalSourceEquivalence_of_rawCoherentEquivalence
#print axioms exactUniversalRawObject_equivalent_of_rawCoherentEquivalence

end

end KUOS.DependentOriginationExactUniversalSourceEquivalenceV4_78
