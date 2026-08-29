import Mathlib.CategoryTheory.Bicategory.Adjunction.Basic
import KUOS.DependentOriginationNativeInfinityTwoScaledV1_19

namespace KUOS.DependentOriginationCompleteSegalInfinityTwoV1_20

open CategoryTheory
open Simplicial
open scoped Bicategory
open KUOS.DependentOriginationInfinityTwoYonedaV1_18
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19

universe u v w

/-!
# Complete-Segal / univalent infinity-two certificate v1.20

For a complete Segal model, completeness is not the assertion that equivalent
objects are definitionally equal.  Homotopically, the identity/path space of
objects must agree with the space of equivalences.  At the present 2-truncated
bicategorical level, the exact analogue is an equivalence of types

```text
(X = Y) ≃ (X ≌ Y),
```

where `X ≌ Y` is Mathlib's native `Bicategory.Equivalence`, i.e. an adjoint
equivalence with invertible unit/counit and triangle coherence.

This file packages that condition together with the already proved strict
Segal mapping nerves.  It is intentionally a stronger class than
`InfinityTwoCategory`: arbitrary bicategories need not be univalent/complete.
-/

/--
Object-level Rezk/univalence witness for a bicategory.

The forward direction identifies equality/path of objects with an adjoint
bicategorical equivalence; the inverse direction says every adjoint equivalence
is represented by such an object path in this complete presentation.
-/
structure ObjectUnivalence
    (B : Type u) [Bicategory.{w, v} B] where
  pathEquiv : forall X Y : B, (X = Y) ≃ (X ≌ Y)

/-- Equality always gives a canonical bicategorical adjoint equivalence. -/
def equalityToEquivalence
    {B : Type u} [Bicategory.{w, v} B]
    {X Y : B} (h : X = Y) : X ≌ Y := by
  subst Y
  exact Bicategory.Equivalence.id X

/--
A native complete-Segal `(infinity,2)` certificate for the current
2-truncated/quasicategory-enriched model.

* `InfinityTwoCategory` gives native mapping quasicategories;
* `mapping_strict_segal` gives the Segal condition on every mapping object;
* `object_univalence` is the Rezk-completeness analogue at object level.

The ambient Mathlib `Bicategory` still carries weak composition, associators,
unitors, pentagon, and triangle.
-/
class CompleteSegalInfinityTwoCategory
    (B : Type u) [Bicategory.{w, v} B]
    extends LocallyScaledInfinityTwoCategory B where
  mapping_strict_segal :
    forall X Y : B, SSet.IsStrictSegal (mappingNerve X Y)
  object_univalence : ObjectUnivalence B

/--
Any bicategory equipped with genuine object-univalence data upgrades to the
native complete-Segal class.  The Segal and quasicategory obligations are
proved from the hom-category nerves; only completeness is extra data.
-/
def completeSegalOfObjectUnivalence
    {B : Type u} [Bicategory.{w, v} B]
    (h : ObjectUnivalence B) :
    CompleteSegalInfinityTwoCategory B where
  mapping_quasicategory := by
    intro X Y
    exact mappingNerve_quasicategory X Y
  mapping_scaling := by
    intro X Y
    exact ScaledSimplicialSet.maximal (mappingNerve X Y)
  mapping_strict_segal := by
    intro X Y
    exact (mappingNerveStrictSegal X Y).isStrictSegal
  object_univalence := h

/-- Completeness recovers an object path from every bicategorical equivalence. -/
def pathOfEquivalence
    {B : Type u} [Bicategory.{w, v} B]
    [CompleteSegalInfinityTwoCategory B]
    {X Y : B} (e : X ≌ Y) : X = Y :=
  ((CompleteSegalInfinityTwoCategory.object_univalence
    (B := B)).pathEquiv X Y).symm e

/-- The recovered path and the supplied equivalence are inverse under univalence. -/
theorem pathEquiv_apply_symm_apply
    {B : Type u} [Bicategory.{w, v} B]
    [CompleteSegalInfinityTwoCategory B]
    {X Y : B} (e : X ≌ Y) :
    (CompleteSegalInfinityTwoCategory.object_univalence
      (B := B)).pathEquiv X Y
        (pathOfEquivalence e) = e := by
  exact Equiv.apply_symm_apply _ e

/-- Conversely, an object path is recovered after passing to its complete equivalence image. -/
theorem pathEquiv_symm_apply_apply
    {B : Type u} [Bicategory.{w, v} B]
    [CompleteSegalInfinityTwoCategory B]
    {X Y : B} (h : X = Y) :
    ((CompleteSegalInfinityTwoCategory.object_univalence
      (B := B)).pathEquiv X Y).symm
        ((CompleteSegalInfinityTwoCategory.object_univalence
          (B := B)).pathEquiv X Y h) = h := by
  let e : (X = Y) ≃ (X ≌ Y) :=
    (CompleteSegalInfinityTwoCategory.object_univalence
      (B := B)).pathEquiv X Y
  change e.symm (e h) = h
  exact e.symm_apply_apply h

/-- The complete-Segal class still provides all mapping inner-horn fillers. -/
theorem completeSegal_mapping_innerHornFilling
    {B : Type u} [Bicategory.{w, v} B]
    [CompleteSegalInfinityTwoCategory B]
    (X Y : B)
    {n : Nat} {i : Fin (n + 1)}
    (h0 : 0 < i) (hn : i < Fin.last n)
    (sigma0 : (Λ[n, i] : SSet) ⟶ mappingNerve X Y) :
    exists sigma : Δ[n] ⟶ mappingNerve X Y,
      sigma0 = Λ[n, i].ι ≫ sigma := by
  exact mapping_innerHornFilling X Y h0 hn sigma0

/-- Completeness is genuinely extra: expose the exact additional witness required. -/
def objectUnivalenceOfCompleteSegal
    {B : Type u} [Bicategory.{w, v} B]
    [CompleteSegalInfinityTwoCategory B] :
    ObjectUnivalence B :=
  CompleteSegalInfinityTwoCategory.object_univalence (B := B)

/-!
The exact logical boundary is now formal:

```text
Bicategory B
  -> InfinityTwoCategory B                 -- automatic
  -> LocallyScaledInfinityTwoCategory B   -- automatic via maximal local scale

Bicategory B + ObjectUnivalence B
  -> CompleteSegalInfinityTwoCategory B.  -- proved
```

The final implication is not stated without `ObjectUnivalence`: Rezk
completeness is additional global information, not a consequence of the
bicategory axioms alone.
-/

end KUOS.DependentOriginationCompleteSegalInfinityTwoV1_20