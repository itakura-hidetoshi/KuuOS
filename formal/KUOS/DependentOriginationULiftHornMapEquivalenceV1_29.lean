import KUOS.DependentOriginationULiftScaledHornFillerForwardV1_29
import Mathlib.CategoryTheory.Whiskering

/-!
# Fully faithful descent of the underlying horn and simplex maps

The pinned Type-valued ULift functor is fully faithful. Post-composing
simplicial objects with it remains fully faithful. The certified
hornUniverseIso / simplexUniverseIso identify lifted representables with
the actual representables in the larger universe. These facts give genuine
two-sided equivalences of *all underlying* horn and simplex maps.

This does not silently identify a chosen admissibility predicate or a
nontransported scaling, so an unconditional scaled-fibrancy equivalence
is not asserted by this module.
-/

namespace KUOS.DependentOriginationULiftHornMapEquivalenceV1_29

open CategoryTheory Simplicial Opposite
open KUOS.DependentOriginationULiftHornUniverseComparisonV1_29
open KUOS.DependentOriginationULiftHornInclusionNaturalityV1_29

universe u v

/-- Fixed-mathlib full faithfulness of the actual simplicial-set ULift
functor, using the fully faithful Type ULift functor and whiskering. -/
noncomputable def fullyFaithfulSSetULift :
    (SSet.uliftFunctor.{v, u}).FullyFaithful :=
  CategoryTheory.fullyFaithfulULiftFunctor.{v, u}.whiskeringRight SimplexCategoryᵒᵖ

/-- Every map from a lower-universe representable horn corresponds
bijectively to a map from the actual higher-universe horn into ULift X. -/
noncomputable def hornMapUniverseEquiv
    {X : SSet.{u}} (n : ℕ) (i : Fin (n + 1)) :
    ((SSet.horn.{u} n i : SSet.{u}) ⟶ X) ≃
      ((SSet.horn.{max u v} n i : SSet.{max u v}) ⟶
        (SSet.uliftFunctor.{v, u}).obj X) := by
  let E :
      ((SSet.horn.{u} n i : SSet.{u}) ⟶ X) ≃
        ((SSet.uliftFunctor.{v, u}).obj
            (SSet.horn.{u} n i : SSet.{u}) ⟶
          (SSet.uliftFunctor.{v, u}).obj X) :=
    fullyFaithfulSSetULift.{u, v}.homEquiv
  exact E.trans
    { toFun := fun f => (hornUniverseIso.{u, v} n i).inv ≫ f
      invFun := fun f => (hornUniverseIso.{u, v} n i).hom ≫ f
      left_inv := by intro f; simp [Category.assoc]
      right_inv := by intro f; simp [Category.assoc] }

/-- The identical equivalence for simplex maps is natural in the target
and uses the certified standard-simplex universe isomorphism. -/
noncomputable def simplexMapUniverseEquiv
    {X : SSet.{u}} (n : ℕ) :
    ((Δ[n] : SSet.{u}) ⟶ X) ≃
      ((Δ[n] : SSet.{max u v}) ⟶
        (SSet.uliftFunctor.{v, u}).obj X) := by
  let E :
      ((Δ[n] : SSet.{u}) ⟶ X) ≃
        ((SSet.uliftFunctor.{v, u}).obj (Δ[n] : SSet.{u}) ⟶
          (SSet.uliftFunctor.{v, u}).obj X) :=
    fullyFaithfulSSetULift.{u, v}.homEquiv
  exact E.trans
    { toFun := fun f => (simplexUniverseIso.{u, v} n).inv ≫ f
      invFun := fun f => (simplexUniverseIso.{u, v} n).hom ≫ f
      left_inv := by intro f; simp [Category.assoc]
      right_inv := by intro f; simp [Category.assoc] }

/-- The inverse to hornMapUniverseEquiv is the canonical unlift map.
This is defined for every higher-universe horn map into a lifted target. -/
noncomputable def unliftHornMap
    {X : SSet.{u}} (n : ℕ) (i : Fin (n + 1))
    (f : (SSet.horn.{max u v} n i : SSet.{max u v}) ⟶
        (SSet.uliftFunctor.{v, u}).obj X) :
    (SSet.horn.{u} n i : SSet.{u}) ⟶ X :=
  (hornMapUniverseEquiv.{u, v} (X := X) n i).symm f

/-- The inverse to simplexMapUniverseEquiv is also available for any
map with lifted target; a filler can therefore be considered on the
original simplex domain at the level of underlying simplicial maps. -/
noncomputable def unliftSimplexMap
    {X : SSet.{u}} (n : ℕ)
    (f : (Δ[n] : SSet.{max u v}) ⟶
        (SSet.uliftFunctor.{v, u}).obj X) :
    (Δ[n] : SSet.{u}) ⟶ X :=
  (simplexMapUniverseEquiv.{u, v} (X := X) n).symm f

theorem unliftHornMap_equiv_lift
    {X : SSet.{u}} (n : ℕ) (i : Fin (n + 1))
    (f : (SSet.horn.{u} n i : SSet.{u}) ⟶ X) :
    unliftHornMap.{u, v} n i
      (hornMapUniverseEquiv.{u, v} n i f) = f :=
  (hornMapUniverseEquiv.{u, v} (X := X) n i).left_inv f

theorem unliftSimplexMap_equiv_lift
    {X : SSet.{u}} (n : ℕ)
    (f : (Δ[n] : SSet.{u}) ⟶ X) :
    unliftSimplexMap.{u, v} n
      (simplexMapUniverseEquiv.{u, v} n f) = f :=
  (simplexMapUniverseEquiv.{u, v} (X := X) n).left_inv f

#print axioms fullyFaithfulSSetULift
#print axioms hornMapUniverseEquiv
#print axioms simplexMapUniverseEquiv
#print axioms unliftHornMap_equiv_lift
#print axioms unliftSimplexMap_equiv_lift

end KUOS.DependentOriginationULiftHornMapEquivalenceV1_29
