import KUOS.DependentOriginationExactUniversalRealizationFullyFaithfulV4_77
import KUOS.DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70
import Mathlib.CategoryTheory.Bicategory.Adjunction.Basic

namespace KUOS.DependentOriginationExactUniversalAdjunctionLiftingV4_79

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackCarrierV2_9
open KUOS.DependentOriginationExactUniversalMappingMorphismV4_57
open KUOS.DependentOriginationExactUniversalMappingHomCategoryV4_60
open KUOS.DependentOriginationExactUniversalMappingBicategoryV4_69
open KUOS.DependentOriginationExactUniversalRealizationStrictPseudofunctorV4_70
open KUOS.DependentOriginationExactUniversalRealizationFaithfulV4_76
open KUOS.DependentOriginationExactUniversalRealizationFullyFaithfulV4_77

open scoped CategoryTheory.Pseudofunctor.StrongTrans
open scoped CategoryTheory.Bicategory

set_option autoImplicit false

noncomputable section

/-!
# Exact lifting of adjunction data along DO₂ realization v4.79

Fix already chosen source 1-cells f : X ⟶ Y and g : Y ⟶ X. Strict realization
preserves both zigzags, including their associators and unitors. Local
faithfulness therefore reflects each triangle identity; local fullness supplies
the unique compatible unit and counit over any prescribed DO₂ components.

This gives an Equiv between native Mathlib `Bicategory.Adjunction` structures on
the fixed source legs and on their DO₂ realizations. Neither unit nor counit is
assumed invertible. Both components are recovered exactly, not merely up to iso.

For invertible prescribed DO₂ data that already satisfy the triangle, the same
reflection constructs a source adjoint equivalence without adjointification:
neither prescribed DO₂ component is adjusted. This is stronger data control
than v4.78, which constructs an equivalence from raw inverse data by adjusting
a chosen source counit.

The two source legs remain inputs. No arbitrary DO₂ 1-cell is lifted here, and
no final mapping biequivalence or equality with prescribed raw unit/counit data
is asserted. The theorem concerns the existing exact-universal sector; it does
not turn weak admissibility into exact presentability.
-/

universe u v uH vH

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas (LocalizedContext W))
variable {X Y : ExactUniversalRawObject.{u, v, uH, vH} (W := W) A}
variable (f : X ⟶ Y) (g : Y ⟶ X)

/-- The left zigzag preserves all structural cells under the strict projection. -/
@[simp] theorem exactUniversal_leftZigzag_lift
    (eta : 𝟙 X ⟶ f ≫ g) (eps : g ≫ f ⟶ 𝟙 Y) :
    (Bicategory.leftZigzag eta eps).lift =
      Bicategory.leftZigzag eta.lift eps.lift := rfl

/-- The right zigzag also retains its inverse associator and unitors. -/
@[simp] theorem exactUniversal_rightZigzag_lift
    (eta : 𝟙 X ⟶ f ≫ g) (eps : g ≫ f ⟶ 𝟙 Y) :
    (Bicategory.rightZigzag eta eps).lift =
      Bicategory.rightZigzag eta.lift eps.lift := rfl

/-- The left triangle is true in the source exactly when its realization is. -/
theorem exactUniversal_leftTriangle_iff_lift
    (eta : 𝟙 X ⟶ f ≫ g) (eps : g ≫ f ⟶ 𝟙 Y) :
    (Bicategory.leftZigzag eta eps = (λ_ f).hom ≫ (ρ_ f).inv) ↔
      (Bicategory.leftZigzag eta.lift eps.lift =
        (λ_ f.lift).hom ≫ (ρ_ f.lift).inv) :=
  exactUniversalTwoCell_eq_iff_lift_eq (W := W) A (X := X) (Y := Y)
    (Bicategory.leftZigzag eta eps) ((λ_ f).hom ≫ (ρ_ f).inv)

/-- The right triangle is reflected independently of the left triangle. -/
theorem exactUniversal_rightTriangle_iff_lift
    (eta : 𝟙 X ⟶ f ≫ g) (eps : g ≫ f ⟶ 𝟙 Y) :
    (Bicategory.rightZigzag eta eps = (ρ_ g).hom ≫ (λ_ g).inv) ↔
      (Bicategory.rightZigzag eta.lift eps.lift =
        (ρ_ g.lift).hom ≫ (λ_ g.lift).inv) :=
  exactUniversalTwoCell_eq_iff_lift_eq (W := W) A (X := Y) (Y := X)
    (Bicategory.rightZigzag eta eps) ((ρ_ g).hom ≫ (λ_ g).inv)

/-- Project an arbitrary source adjunction, not only an adjoint equivalence. -/
def exactUniversalAdjunctionToLift (adj : Bicategory.Adjunction f g) :
    Bicategory.Adjunction f.lift g.lift where
  unit := adj.unit.lift
  counit := adj.counit.lift
  left_triangle :=
    (exactUniversal_leftTriangle_iff_lift (W := W) A f g adj.unit adj.counit).1
      adj.left_triangle
  right_triangle :=
    (exactUniversal_rightTriangle_iff_lift (W := W) A f g adj.unit adj.counit).1
      adj.right_triangle

/-- Lift the specified DO₂ unit and counit, then reflect both triangle laws.
Chosen object indices and source constructors are explicit at each preimage. -/
def exactUniversalAdjunctionOfLift (adj : Bicategory.Adjunction f.lift g.lift) :
    Bicategory.Adjunction f g where
  unit := exactUniversalCompletion2Preimage (W := W) A (X := X) (Y := X)
    (f := ExactUniversalRawMorphism.id (W := W) A X)
    (g := ExactUniversalRawMorphism.comp (W := W) A f g) adj.unit
  counit := exactUniversalCompletion2Preimage (W := W) A (X := Y) (Y := Y)
    (f := ExactUniversalRawMorphism.comp (W := W) A g f)
    (g := ExactUniversalRawMorphism.id (W := W) A Y) adj.counit
  left_triangle := by
    apply (exactUniversal_leftTriangle_iff_lift (W := W) A f g _ _).2
    exact adj.left_triangle
  right_triangle := by
    apply (exactUniversal_rightTriangle_iff_lift (W := W) A f g _ _).2
    exact adj.right_triangle

/-- Exact classification of adjunction structures on fixed source legs.
The inverse laws use only 2-cell faithfulness and Mathlib adjunction extensionality. -/
def exactUniversalAdjunctionEquivLift :
    Bicategory.Adjunction f g ≃ Bicategory.Adjunction f.lift g.lift where
  toFun := exactUniversalAdjunctionToLift (W := W) A f g
  invFun := exactUniversalAdjunctionOfLift (W := W) A f g
  left_inv _ := by
    apply Bicategory.Adjunction.ext
    · apply exactUniversalCompletion2_map_injective (W := W) A (X := X) (Y := X)
      rfl
    · apply exactUniversalCompletion2_map_injective (W := W) A (X := Y) (Y := Y)
      rfl
  right_inv _ := by
    apply Bicategory.Adjunction.ext <;> rfl

/-- A prescribed realized adjunction has one and only one compatible source
adjunction. This is uniqueness with both 1-cell legs fixed. -/
theorem existsUnique_exactUniversalAdjunction_of_lift
    (adj : Bicategory.Adjunction f.lift g.lift) :
    ∃! a : Bicategory.Adjunction f g,
      a.unit.lift = adj.unit ∧ a.counit.lift = adj.counit := by
  refine ⟨exactUniversalAdjunctionOfLift (W := W) A f g adj, ⟨rfl, rfl⟩, ?_⟩
  intro a ha
  apply Bicategory.Adjunction.ext
  · apply exactUniversalCompletion2_map_injective (W := W) A (X := X) (Y := X)
    exact ha.1
  · apply exactUniversalCompletion2_map_injective (W := W) A (X := Y) (Y := Y)
    exact ha.2

/-- Existence of an adjunction on the chosen pair is detected by realization. -/
theorem exactUniversalAdjunction_nonempty_iff_lift :
    Nonempty (Bicategory.Adjunction f g) ↔
      Nonempty (Bicategory.Adjunction f.lift g.lift) := by
  constructor
  · rintro ⟨adj⟩
    exact ⟨exactUniversalAdjunctionToLift (W := W) A f g adj⟩
  · rintro ⟨adj⟩
    exact ⟨exactUniversalAdjunctionOfLift (W := W) A f g adj⟩

/-- Lift an already coherent pair of DO₂ isomorphisms without adjusting its
counit. Mathlib's native Equivalence carries the reflected left triangle and
provides the right triangle. The supplied source legs are retained exactly. -/
def exactUniversalEquivalenceOfLiftTriangle
    (unitIso : 𝟙 X.carrier ≅ f.lift ≫ g.lift)
    (counitIso : g.lift ≫ f.lift ≅ 𝟙 Y.carrier)
    (hleft : Bicategory.leftZigzagIso unitIso counitIso =
      (λ_ f.lift) ≪≫ (ρ_ f.lift).symm) : Bicategory.Equivalence X Y := by
  let eta : 𝟙 X ≅ f ≫ g :=
    exactUniversalSourceIsoOfLift (W := W) A (X := X) (Y := X)
      (f := ExactUniversalRawMorphism.id (W := W) A X)
      (g := ExactUniversalRawMorphism.comp (W := W) A f g) unitIso
  let eps : g ≫ f ≅ 𝟙 Y :=
    exactUniversalSourceIsoOfLift (W := W) A (X := Y) (Y := Y)
      (f := ExactUniversalRawMorphism.comp (W := W) A g f)
      (g := ExactUniversalRawMorphism.id (W := W) A Y) counitIso
  -- `map_preimage` also needs source hom-category objects: its `X` and `Y`
  -- are source 1-cells, not the outer bicategory objects or their DO₂ images.
  have heta : eta.hom.lift = unitIso.hom :=
    (exactUniversalCompletion2HomFunctor (W := W) A X X).map_preimage
      (X := ExactUniversalRawMorphism.id (W := W) A X)
      (Y := ExactUniversalRawMorphism.comp (W := W) A f g) unitIso.hom
  have heps : eps.hom.lift = counitIso.hom :=
    (exactUniversalCompletion2HomFunctor (W := W) A Y Y).map_preimage
      (X := ExactUniversalRawMorphism.comp (W := W) A g f)
      (Y := ExactUniversalRawMorphism.id (W := W) A Y) counitIso.hom
  refine { hom := f, inv := g, unit := eta, counit := eps, left_triangle := ?_ }
  apply Iso.ext
  apply (exactUniversal_leftTriangle_iff_lift (W := W) A f g eta.hom eps.hom).2
  exact (congrArg₂
    (fun (u : 𝟙 X.carrier ⟶ f.lift ≫ g.lift)
      (v : g.lift ≫ f.lift ⟶ 𝟙 Y.carrier) => Bicategory.leftZigzag u v)
    heta heps).trans (congrArg Iso.hom hleft)

/-- The lifted equivalence recovers the prescribed DO₂ unit. -/
theorem exactUniversalEquivalenceOfLiftTriangle_unit_lift
    (unitIso : 𝟙 X.carrier ≅ f.lift ≫ g.lift)
    (counitIso : g.lift ≫ f.lift ≅ 𝟙 Y.carrier)
    (hleft : Bicategory.leftZigzagIso unitIso counitIso =
      (λ_ f.lift) ≪≫ (ρ_ f.lift).symm) :
    (exactUniversalEquivalenceOfLiftTriangle
      (W := W) A f g unitIso counitIso hleft).unit.hom.lift = unitIso.hom :=
  (exactUniversalCompletion2HomFunctor (W := W) A X X).map_preimage
    (X := ExactUniversalRawMorphism.id (W := W) A X)
    (Y := ExactUniversalRawMorphism.comp (W := W) A f g) unitIso.hom

/-- In contrast with adjointification, the prescribed DO₂ counit is unchanged. -/
theorem exactUniversalEquivalenceOfLiftTriangle_counit_lift
    (unitIso : 𝟙 X.carrier ≅ f.lift ≫ g.lift)
    (counitIso : g.lift ≫ f.lift ≅ 𝟙 Y.carrier)
    (hleft : Bicategory.leftZigzagIso unitIso counitIso =
      (λ_ f.lift) ≪≫ (ρ_ f.lift).symm) :
    (exactUniversalEquivalenceOfLiftTriangle
      (W := W) A f g unitIso counitIso hleft).counit.hom.lift = counitIso.hom :=
  (exactUniversalCompletion2HomFunctor (W := W) A Y Y).map_preimage
    (X := ExactUniversalRawMorphism.comp (W := W) A g f)
    (Y := ExactUniversalRawMorphism.id (W := W) A Y) counitIso.hom

/-! ## Regression checks: fixed legs and prescribed adjunction data. -/

example (adj : Bicategory.Adjunction f.lift g.lift) :
    (exactUniversalAdjunctionOfLift (W := W) A f g adj).unit.lift = adj.unit := rfl

example (adj : Bicategory.Adjunction f.lift g.lift) :
    (exactUniversalAdjunctionOfLift (W := W) A f g adj).counit.lift = adj.counit := rfl

example (adj : Bicategory.Adjunction f g) :
    (exactUniversalAdjunctionEquivLift (W := W) A f g).symm
      ((exactUniversalAdjunctionEquivLift (W := W) A f g) adj) = adj :=
  (exactUniversalAdjunctionEquivLift (W := W) A f g).symm_apply_apply adj

example (adj : Bicategory.Adjunction f.lift g.lift) :
    (exactUniversalAdjunctionEquivLift (W := W) A f g)
      ((exactUniversalAdjunctionEquivLift (W := W) A f g).symm adj) = adj :=
  (exactUniversalAdjunctionEquivLift (W := W) A f g).apply_symm_apply adj

example (adj : Bicategory.Adjunction f.lift g.lift) :
    ∃! a : Bicategory.Adjunction f g,
      a.unit.lift = adj.unit ∧ a.counit.lift = adj.counit :=
  existsUnique_exactUniversalAdjunction_of_lift (W := W) A f g adj

example : Nonempty (Bicategory.Adjunction f g) ↔
    Nonempty (Bicategory.Adjunction f.lift g.lift) :=
  exactUniversalAdjunction_nonempty_iff_lift (W := W) A f g

variable (unitIso : 𝟙 X.carrier ≅ f.lift ≫ g.lift)
variable (counitIso : g.lift ≫ f.lift ≅ 𝟙 Y.carrier)
variable (hleft : Bicategory.leftZigzagIso unitIso counitIso =
  (λ_ f.lift) ≪≫ (ρ_ f.lift).symm)

example : (exactUniversalEquivalenceOfLiftTriangle
    (W := W) A f g unitIso counitIso hleft).hom = f := rfl

example : (exactUniversalEquivalenceOfLiftTriangle
    (W := W) A f g unitIso counitIso hleft).inv = g := rfl

example : (exactUniversalEquivalenceOfLiftTriangle
    (W := W) A f g unitIso counitIso hleft).unit.hom.lift = unitIso.hom :=
  exactUniversalEquivalenceOfLiftTriangle_unit_lift
    (W := W) A f g unitIso counitIso hleft

example : (exactUniversalEquivalenceOfLiftTriangle
    (W := W) A f g unitIso counitIso hleft).counit.hom.lift = counitIso.hom :=
  exactUniversalEquivalenceOfLiftTriangle_counit_lift
    (W := W) A f g unitIso counitIso hleft

example :
    let e := exactUniversalEquivalenceOfLiftTriangle
      (W := W) A f g unitIso counitIso hleft
    Bicategory.rightZigzagIso e.unit e.counit = (ρ_ e.inv) ≪≫ (λ_ e.inv).symm :=
  (exactUniversalEquivalenceOfLiftTriangle
    (W := W) A f g unitIso counitIso hleft).right_triangle

-- Equality of the complete realized isomorphisms, including their inverses.
example : (exactUniversalCompletion2HomFunctor (W := W) A X X).mapIso
    (exactUniversalEquivalenceOfLiftTriangle
      (W := W) A f g unitIso counitIso hleft).unit = unitIso := by
  apply Iso.ext
  exact exactUniversalEquivalenceOfLiftTriangle_unit_lift
    (W := W) A f g unitIso counitIso hleft

example : (exactUniversalCompletion2HomFunctor (W := W) A Y Y).mapIso
    (exactUniversalEquivalenceOfLiftTriangle
      (W := W) A f g unitIso counitIso hleft).counit = counitIso := by
  apply Iso.ext
  exact exactUniversalEquivalenceOfLiftTriangle_counit_lift
    (W := W) A f g unitIso counitIso hleft

-- Check inverse preimages too: their source hom-category endpoints are reversed.
example : (exactUniversalEquivalenceOfLiftTriangle
    (W := W) A f g unitIso counitIso hleft).unit.inv.lift = unitIso.inv :=
  (exactUniversalCompletion2HomFunctor (W := W) A X X).map_preimage
    (X := ExactUniversalRawMorphism.comp (W := W) A f g)
    (Y := ExactUniversalRawMorphism.id (W := W) A X) unitIso.inv

example : (exactUniversalEquivalenceOfLiftTriangle
    (W := W) A f g unitIso counitIso hleft).counit.inv.lift = counitIso.inv :=
  (exactUniversalCompletion2HomFunctor (W := W) A Y Y).map_preimage
    (X := ExactUniversalRawMorphism.id (W := W) A Y)
    (Y := ExactUniversalRawMorphism.comp (W := W) A g f) counitIso.inv

#print axioms exactUniversal_leftTriangle_iff_lift
#print axioms exactUniversal_rightTriangle_iff_lift
#print axioms exactUniversalAdjunctionEquivLift
#print axioms existsUnique_exactUniversalAdjunction_of_lift
#print axioms exactUniversalEquivalenceOfLiftTriangle
#print axioms exactUniversalEquivalenceOfLiftTriangle_unit_lift
#print axioms exactUniversalEquivalenceOfLiftTriangle_counit_lift

end

end KUOS.DependentOriginationExactUniversalAdjunctionLiftingV4_79
