import KUOS.DependentOriginationCoherentBiadjunctionNativeRightMateLaxTransV5_110
import Mathlib.CategoryTheory.Bicategory.Modification.Oplax

namespace KUOS.DependentOriginationCoherentBiadjunctionNativeRightMateTriangleModificationsV5_111

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationCoherentBiadjunctionMathlibAdjunctionBridgeV5_102
open KUOS.DependentOriginationCoherentBiadjunctionNativeRightMateLaxTransV5_110

set_option autoImplicit false
noncomputable section

/-!
# F15 / v5.111: Original objectwise adjunction triangles as native modifications

F14 constructs the original source/target right mates as genuine
`CategoryTheory.Oplax.LaxTrans` values, without asserting that their
naturality 2-cells are invertible.

The objectwise right legs are right adjoints of the *unchanged* original
source unit η and target counit ε.  The following generic construction
uses their **actual** unit/counit zigzag, normalized by the non-strict
bicategorical unitors, as a family of modification components.
The original right triangle makes that modification equal to the
identity modification.  Consequently its naturality is global, not
merely a collection of unrelated objectwise triangle equalities.

This is a precise first F15 modification-level boundary.  It does
not identify these objectwise adjunction triangles with the separate
v5.58 triangulators of the F/G biadjunction.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]

/-- Normalize the **original** right zigzag to an endomorphism of the
right adjoint, retaining both unitors of the non-strict bicategory. -/
def normalizedRightZigzag {a b : B} {l : a ⟶ b} {r : b ⟶ a}
    (adj : Bicategory.Adjunction l r) : r ⟶ r :=
  (ρ_ r).inv ≫ Bicategory.rightZigzag adj.unit adj.counit ≫ (λ_ r).hom

/-- The native right triangle identifies the actual normalized zigzag
with the identity, without a strictness or invertibility assumption
on a transformation's naturality squares. -/
theorem normalizedRightZigzag_eq_id {a b : B} {l : a ⟶ b} {r : b ⟶ a}
    (adj : Bicategory.Adjunction l r) :
    normalizedRightZigzag adj = 𝟙 r := by
  change (ρ_ r).inv ≫
      Bicategory.rightZigzag adj.unit adj.counit ≫ (λ_ r).hom = 𝟙 r
  rw [adj.right_triangle]
  simp only [Category.assoc, Iso.inv_hom_id_assoc,
    Category.id_comp, Iso.inv_hom_id]

variable {C : Type uC} [Bicategory.{wC, vC} C]
variable {F G : OplaxFunctor B C}

/-- A family of original adjunctions for the app-components of a lax
transformation yields a bona fide mathlib modification.  Naturality
uses the actual lax naturality of the transformation (even when its
squares are not invertible), and the exact adjunction triangles. -/
def rightZigzagModification (τ : Oplax.LaxTrans F G)
    (l : ∀ X : B, G.obj X ⟶ F.obj X)
    (adj : ∀ X : B, Bicategory.Adjunction (l X) (τ.app X)) :
    Oplax.LaxTrans.Modification τ τ where
  app X := normalizedRightZigzag (adj X)
  naturality {_ _} f := by
    simp only [normalizedRightZigzag_eq_id,
      Bicategory.id_whiskerRight, Bicategory.whiskerLeft_id,
      Category.id_comp, Category.comp_id]

/-- Modification-level right triangle, rather than only objectwise
equalities of two-morphisms. -/
theorem rightZigzagModification_eq_id (τ : Oplax.LaxTrans F G)
    (l : ∀ X : B, G.obj X ⟶ F.obj X)
    (adj : ∀ X : B, Bicategory.Adjunction (l X) (τ.app X)) :
    rightZigzagModification τ l adj =
      Oplax.LaxTrans.Modification.id τ := by
  apply Oplax.LaxTrans.Modification.ext
  funext X
  exact normalizedRightZigzag_eq_id (adj X)

end Generic

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- Native modification made from the right zigzags of the **original
source-unit** adjunctions, over the genuine F14 source lax right mate. -/
def actualLiftSourceRightMateTriangleModification :
    Oplax.LaxTrans.Modification
      (actualLiftSourceRightMateLaxTrans (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftSourceRightMateLaxTrans (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) :=
  Generic.rightZigzagModification
    (actualLiftSourceRightMateLaxTrans (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (fun X => (actualLiftSourceNativeAdjHom (W := W) A X).l)
    (fun X => (actualLiftSourceNativeAdjHom (W := W) A X).adj)

/-- The original source-unit right zigzag is exactly the identity
modification of F14's source lax transformation. -/
theorem actualLiftSourceRightMateTriangleModification_eq_id :
    actualLiftSourceRightMateTriangleModification (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel) =
    Oplax.LaxTrans.Modification.id
      (actualLiftSourceRightMateLaxTrans (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) := by
  exact Generic.rightZigzagModification_eq_id
    (actualLiftSourceRightMateLaxTrans (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (fun X => (actualLiftSourceNativeAdjHom (W := W) A X).l)
    (fun X => (actualLiftSourceNativeAdjHom (W := W) A X).adj)

/-- Target version, using the **original target-counit**
adjunctions and the non-strict target right mate of F14. -/
def actualLiftTargetRightMateTriangleModification :
    Oplax.LaxTrans.Modification
      (actualLiftTargetRightMateLaxTrans (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftTargetRightMateLaxTrans (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) :=
  Generic.rightZigzagModification
    (actualLiftTargetRightMateLaxTrans (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (fun Y => (actualLiftTargetNativeAdjHom (W := W) A Y).l)
    (fun Y => (actualLiftTargetNativeAdjHom (W := W) A Y).adj)

/-- The original target-counit right zigzag is exactly the identity
modification of F14's target lax transformation. -/
theorem actualLiftTargetRightMateTriangleModification_eq_id :
    actualLiftTargetRightMateTriangleModification (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel) =
    Oplax.LaxTrans.Modification.id
      (actualLiftTargetRightMateLaxTrans (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) := by
  exact Generic.rightZigzagModification_eq_id
    (actualLiftTargetRightMateLaxTrans (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
    (fun Y => (actualLiftTargetNativeAdjHom (W := W) A Y).l)
    (fun Y => (actualLiftTargetNativeAdjHom (W := W) A Y).adj)

#print axioms Generic.normalizedRightZigzag
#print axioms Generic.normalizedRightZigzag_eq_id
#print axioms Generic.rightZigzagModification
#print axioms Generic.rightZigzagModification_eq_id
#print axioms actualLiftSourceRightMateTriangleModification
#print axioms actualLiftSourceRightMateTriangleModification_eq_id
#print axioms actualLiftTargetRightMateTriangleModification
#print axioms actualLiftTargetRightMateTriangleModification_eq_id

end

end KUOS.DependentOriginationCoherentBiadjunctionNativeRightMateTriangleModificationsV5_111
