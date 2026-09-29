import KUOS.DependentOriginationExactUniversalMappingHomCategoryV4_60
import Mathlib.CategoryTheory.Comma.Basic

namespace KUOS.DependentOriginationExactUniversalCompatibleIsoV4_75

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMappingTwoCellV4_58
open KUOS.DependentOriginationExactUniversalMappingTwoCellVerticalV4_59
open KUOS.DependentOriginationExactUniversalMappingHomCategoryV4_60

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Compatible source isomorphisms via Mathlib comma categories v4.75

For any two chosen exact-universal objects, their mapping hom category embeds
fully faithfully in a Mathlib comma category. The left functor restricts a DO₂
map and postcomposes the target comparison; the right functor precomposes a raw
map with the source comparison. A source 2-cell is exactly a comma morphism.

Mathlib `Comma.isoMk` therefore supplies inverse compatibility from forward
compatibility, without repeating the structural pasting proof from v4.67.
We classify source isomorphisms by compatible pairs of raw and DO₂ isomorphisms,
and prove that the two projections jointly detect invertible 2-cells.

This is local full faithfulness of the *comma embedding*, not of the DO₂
realization. A bare DO₂ isomorphism from v4.74 still need not satisfy the
prescribed comparison square. No source object equivalence is asserted here.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))

/-- The DO₂ side of the comparison square, functorial on modifications. -/
def exactUniversalLiftComparisonFunctor
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A) :
    (X.carrier ⟶ Y.carrier) ⥤
      (restrictHigherLocalizedSystem W
        (higherStackObjectVal (W := W) A X.carrier) ⟶ Y.raw) where
  obj f := restrictHigherLocalizedStrongTrans (W := W) f.hom ≫
    Y.presentation.comparison
  map eta := restrictHigherLocalizedModification (W := W) eta.hom ▷
    Y.presentation.comparison
  map_id f := by
    change (restrictHigherLocalizedModification (W := W) (𝟙 f.hom) ▷
      Y.presentation.comparison) = 𝟙 _
    rw [restrictHigherLocalizedModification_id]
    exact Bicategory.id_whiskerRight _ _
  map_comp eta theta := by
    change (restrictHigherLocalizedModification (W := W)
      (eta.hom ≫ theta.hom) ▷ Y.presentation.comparison) =
      (restrictHigherLocalizedModification (W := W) eta.hom ▷
        Y.presentation.comparison) ≫
      (restrictHigherLocalizedModification (W := W) theta.hom ▷
        Y.presentation.comparison)
    rw [restrictHigherLocalizedModification_comp, Bicategory.comp_whiskerRight]

/-- The raw side of the comparison square, functorial on modifications. -/
def exactUniversalRawComparisonFunctor
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A) :
    (X.raw ⟶ Y.raw) ⥤
      (restrictHigherLocalizedSystem W
        (higherStackObjectVal (W := W) A X.carrier) ⟶ Y.raw) where
  obj f := X.presentation.comparison ≫ f
  map eta := X.presentation.comparison ◁ eta
  map_id f := Bicategory.whiskerLeft_id _ f
  map_comp eta theta := Bicategory.whiskerLeft_comp _ eta theta

/-- The ambient Mathlib comma category of comparison squares. -/
abbrev ExactUniversalComparisonComma
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A) :=
  Comma (exactUniversalLiftComparisonFunctor (W := W) A X Y)
    (exactUniversalRawComparisonFunctor (W := W) A X Y)

/-- A source 1-cell is an invertible comparison square; its compatible 2-cells
are exactly the corresponding comma morphisms. -/
def exactUniversalComparisonCommaFunctor
    (X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A) :
    ExactUniversalRawMorphism (W := W) A X Y ⥤
      ExactUniversalComparisonComma (W := W) A X Y where
  obj f := { left := f.lift, right := f.raw, hom := f.comparison_square.hom }
  map eta := { left := eta.lift, right := eta.raw, w := eta.compatibility }
  map_id _ := by apply CommaMorphism.ext <;> rfl
  map_comp _ _ := by apply CommaMorphism.ext <;> rfl

variable {X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A}
variable {f g : ExactUniversalRawMorphism (W := W) A X Y}

/-- Recover the compatible source 2-cell from its comma square. -/
def exactUniversalTwoCellOfComma
    (eta : (exactUniversalComparisonCommaFunctor (W := W) A X Y).obj f ⟶
      (exactUniversalComparisonCommaFunctor (W := W) A X Y).obj g) :
    f ⟶ g where
  raw := eta.right
  lift := eta.left
  compatibility := eta.w

/-- No information about 2-cells is lost by the comma encoding. -/
def exactUniversalTwoCellEquivComma :
    (f ⟶ g) ≃
      ((exactUniversalComparisonCommaFunctor (W := W) A X Y).obj f ⟶
        (exactUniversalComparisonCommaFunctor (W := W) A X Y).obj g) where
  toFun := (exactUniversalComparisonCommaFunctor (W := W) A X Y).map
  invFun := exactUniversalTwoCellOfComma (W := W) A
  left_inv _ := rfl
  right_inv _ := rfl

instance exactUniversalComparisonCommaFunctor_faithful :
    (exactUniversalComparisonCommaFunctor (W := W) A X Y).Faithful where
  map_injective {f g} eta theta h :=
    (exactUniversalTwoCellEquivComma (W := W) A (f := f) (g := g)).injective h

instance exactUniversalComparisonCommaFunctor_full :
    (exactUniversalComparisonCommaFunctor (W := W) A X Y).Full where
  map_surjective {f g} eta :=
    (exactUniversalTwoCellEquivComma (W := W) A (f := f) (g := g)).surjective eta

/-- Forward compatibility is sufficient: Mathlib constructs and verifies the
inverse square. Both component isomorphisms remain exactly as prescribed. -/
def exactUniversalSourceIsoOfCompatibleComponents
    (rawIso : f.raw ≅ g.raw) (liftIso : f.lift ≅ g.lift)
    (h : (restrictHigherLocalizedModification (W := W) liftIso.hom.hom ▷
        Y.presentation.comparison) ≫ g.comparison_square.hom =
      f.comparison_square.hom ≫ (X.presentation.comparison ◁ rawIso.hom)) :
    f ≅ g := by
  let e : (exactUniversalComparisonCommaFunctor (W := W) A X Y).obj f ≅
      (exactUniversalComparisonCommaFunctor (W := W) A X Y).obj g :=
    Comma.isoMk liftIso rawIso h
  refine
    { hom := exactUniversalTwoCellOfComma (W := W) A e.hom
      inv := exactUniversalTwoCellOfComma (W := W) A e.inv
      hom_inv_id := ?_
      inv_hom_id := ?_ }
  · apply ExactUniversalRawMorphismTwoCell.ext
    · change rawIso.hom ≫ rawIso.inv = 𝟙 f.raw
      exact rawIso.hom_inv_id
    · change liftIso.hom ≫ liftIso.inv = 𝟙 f.lift
      exact liftIso.hom_inv_id
  · apply ExactUniversalRawMorphismTwoCell.ext
    · change rawIso.inv ≫ rawIso.hom = 𝟙 g.raw
      exact rawIso.inv_hom_id
    · change liftIso.inv ≫ liftIso.hom = 𝟙 g.lift
      exact liftIso.inv_hom_id

/-- Component isomorphisms together with the exact, prescribed square. -/
structure ExactUniversalCompatibleComponentIso
    (f g : ExactUniversalRawMorphism (W := W) A X Y) where
  raw : f.raw ≅ g.raw
  lift : f.lift ≅ g.lift
  compatibility :
    (restrictHigherLocalizedModification (W := W) lift.hom.hom ▷
      Y.presentation.comparison) ≫ g.comparison_square.hom =
      f.comparison_square.hom ≫ (X.presentation.comparison ◁ raw.hom)

/-- Forget a source isomorphism to its compatible component isomorphisms. -/
def exactUniversalCompatibleComponentIsoOfSource (e : f ≅ g) :
    ExactUniversalCompatibleComponentIso (W := W) A f g where
  raw := (exactUniversalRawHomFunctor (W := W) A X Y).mapIso e
  lift := (exactUniversalCompletion2HomFunctor (W := W) A X Y).mapIso e
  compatibility := e.hom.compatibility

/-- Reassemble a compatible pair using Mathlib's inverse-square theorem. -/
def exactUniversalSourceIsoOfCompatible
    (e : ExactUniversalCompatibleComponentIso (W := W) A f g) : f ≅ g :=
  exactUniversalSourceIsoOfCompatibleComponents (W := W) A
    e.raw e.lift e.compatibility

/-- Exact local classification of source isomorphisms by compatible raw and
DO₂ isomorphisms. Unlike mere existence of a DO₂ isomorphism, this retains the
comparison equation and both prescribed components. -/
def exactUniversalSourceIsoEquivCompatibleComponents :
    (f ≅ g) ≃ ExactUniversalCompatibleComponentIso (W := W) A f g where
  toFun := exactUniversalCompatibleComponentIsoOfSource (W := W) A
  invFun := exactUniversalSourceIsoOfCompatible (W := W) A
  left_inv e := by
    apply Iso.ext
    apply ExactUniversalRawMorphismTwoCell.ext <;> rfl
  right_inv e := by
    cases e
    rfl

/-- Source invertibility is exactly joint raw/DO₂ invertibility for an already
compatible 2-cell. Neither projection is asserted to detect it on its own. -/
theorem exactUniversalTwoCell_isIso_iff (eta : f ⟶ g) :
    IsIso eta ↔ IsIso eta.raw ∧ IsIso eta.lift := by
  constructor
  · intro h
    letI := h
    exact ⟨(exactUniversalRawHomFunctor (W := W) A X Y).map_isIso eta,
      (exactUniversalCompletion2HomFunctor (W := W) A X Y).map_isIso eta⟩
  · rintro ⟨hraw, hlift⟩
    letI := hraw
    letI := hlift
    let e : f ≅ g := exactUniversalSourceIsoOfCompatibleComponents (W := W) A
      (asIso eta.raw) (asIso eta.lift) eta.compatibility
    have he : e.hom = eta := by
      apply ExactUniversalRawMorphismTwoCell.ext <;> rfl
    rw [← he]
    infer_instance

/-- Exact existence criterion, with the missing compatibility made explicit. -/
theorem exactUniversalSourceIso_nonempty_iff :
    Nonempty (f ≅ g) ↔
      ∃ rawIso : f.raw ≅ g.raw, ∃ liftIso : f.lift ≅ g.lift,
        (restrictHigherLocalizedModification (W := W) liftIso.hom.hom ▷
          Y.presentation.comparison) ≫ g.comparison_square.hom =
          f.comparison_square.hom ≫ (X.presentation.comparison ◁ rawIso.hom) := by
  constructor
  · rintro ⟨e⟩
    let c := exactUniversalCompatibleComponentIsoOfSource (W := W) A e
    exact ⟨c.raw, c.lift, c.compatibility⟩
  · rintro ⟨rawIso, liftIso, h⟩
    exact ⟨exactUniversalSourceIsoOfCompatibleComponents
      (W := W) A rawIso liftIso h⟩

/-- With both component isomorphisms fixed, the source isomorphism is unique.
This is not uniqueness of the DO₂ isomorphism furnished by v4.74. -/
theorem existsUnique_exactUniversalSourceIso_of_compatible
    (rawIso : f.raw ≅ g.raw) (liftIso : f.lift ≅ g.lift)
    (h : (restrictHigherLocalizedModification (W := W) liftIso.hom.hom ▷
        Y.presentation.comparison) ≫ g.comparison_square.hom =
      f.comparison_square.hom ≫ (X.presentation.comparison ◁ rawIso.hom)) :
    ∃! e : f ≅ g, e.hom.raw = rawIso.hom ∧ e.hom.lift = liftIso.hom := by
  refine ⟨exactUniversalSourceIsoOfCompatibleComponents
    (W := W) A rawIso liftIso h, ⟨rfl, rfl⟩, ?_⟩
  intro e he
  apply Iso.ext
  apply ExactUniversalRawMorphismTwoCell.ext
  · exact he.1
  · exact he.2

/-! ## Regression checks: arbitrary presentations, not only equivalence legs. -/

example (e : f ≅ g) :
    (exactUniversalSourceIsoEquivCompatibleComponents (W := W) A).symm
      ((exactUniversalSourceIsoEquivCompatibleComponents (W := W) A) e) = e :=
  (exactUniversalSourceIsoEquivCompatibleComponents (W := W) A).symm_apply_apply e

example (eta : f ⟶ g) [IsIso eta.raw] [IsIso eta.lift] : IsIso eta :=
  (exactUniversalTwoCell_isIso_iff (W := W) A eta).2 ⟨inferInstance, inferInstance⟩

example (f : ExactUniversalRawMorphism (W := W) A X Y) :
    IsIso (𝟙 f : f ⟶ f) :=
  (exactUniversalTwoCell_isIso_iff (W := W) A (𝟙 f)).2
    ⟨inferInstance, inferInstance⟩

#print axioms exactUniversalSourceIsoEquivCompatibleComponents
#print axioms exactUniversalTwoCell_isIso_iff

end

end KUOS.DependentOriginationExactUniversalCompatibleIsoV4_75
