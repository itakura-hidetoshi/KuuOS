import KUOS.DependentOriginationCoherentBiadjunctionSwallowtailModificationExchangeV5_112
import Mathlib.CategoryTheory.Bicategory.Adjunction.Adj

namespace KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactLiftableActualLiftSourceUnitV5_50
open KUOS.DependentOriginationExactLiftableActualLiftTargetCounitV5_49
open KUOS.DependentOriginationCoherentBiadjunctionMathlibAdjunctionBridgeV5_102
open KUOS.DependentOriginationCoherentBiadjunctionNativeRightMateLaxTransV5_110
open KUOS.DependentOriginationCoherentBiadjunctionNativeRightMateTriangleModificationsV5_111
open KUOS.DependentOriginationCoherentBiadjunctionSwallowtailModificationExchangeV5_112

set_option autoImplicit false
noncomputable section

/-!
# F16 / v5.113: arbitrary modification conjugation and its exact naturality boundary

The previous certified case concerned the original normalized η/ε
adjunction triangles. Here an arbitrary (possibly noninvertible)
modification Γ : σ ⇒ θ between pseudonatural transformations is
transported objectwise by the *same* chosen adjunctions:
  Γ_X : σ_X ⟶ θ_X  |-->  conjugateEquiv(θ_X ⊣ θ_X^R, σ_X ⊣ σ_X^R)(Γ_X)
                               : θ_X^R ⟶ σ_X^R.

The direction reverses. The original right mates are lax, not strong.

In particular, an objectwise conjugate family is NOT silently declared
to be a global lax modification. The genuine lax modification naturality
equation is retained as an explicit proposition `Compatible`, and
`compatible_iff_exists` proves it is the exact existence obstruction.
When this equation holds, we construct an ACTUAL mathlib
`Oplax.LaxTrans.Modification`. Identity and vertical composition
preserve this transport, contravariantly, using mathlib's native
`Bicategory.conjugateEquiv_id/comp`.

Finally the original v5.111 source/target unit/counit triangles give
certified compatible examples; the constructed arbitrary-modification
transport reduces to the unchanged v5.111 right-mate modifications.

This does NOT assume the compatibility equation automatically for every
arbitrary modification; the unrestricted preservation theorem remains
an explicit separate mathematical obligation.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable {F G : Pseudofunctor B C}
variable {σ θ ι : Pseudofunctor.StrongTrans F G}

/-- A right-mate lax transformation bundled with exactly the original
objectwise adjunctions and mate equations for the strong naturality.
No invertibility of the resulting lax naturality is asserted. -/
structure RightMateLaxData (σ : Pseudofunctor.StrongTrans F G) where
  right : Oplax.LaxTrans G.toOplax F.toOplax
  adj (X : B) : Bicategory.Adjunction (σ.app X) (right.app X)
  naturality_eq_mate {X Y : B} (f : X ⟶ Y) :
    right.naturality f =
      Bicategory.mateEquiv (adj X) (adj Y) ((σ.naturality f).hom)

/-- Conjugate an arbitrary (not necessarily invertible) modification
component across the chosen pointwise adjunctions. The direction
reversal is forced by the genuine mathlib `conjugateEquiv` type. -/
def conjugateComponent (dσ : RightMateLaxData σ)
    (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ) (X : B) :
    dθ.right.app X ⟶ dσ.right.app X :=
  Bicategory.conjugateEquiv (dθ.adj X) (dσ.adj X) (Γ.app X)

/-- Exact compatibility condition for transporting Γ to a modification
of the right mate lax transformations. It is NOT an extra axiom; this is
the missing global naturality equation with the original non-strict F/G. -/
def Compatible (dσ : RightMateLaxData σ)
    (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ) : Prop :=
  ∀ {X Y : B} (f : X ⟶ Y),
    conjugateComponent dσ dθ Γ X ▷ F.map f ≫ dσ.right.naturality f =
      dθ.right.naturality f ≫ G.map f ◁ conjugateComponent dσ dθ Γ Y

/-- When and only when the typed naturality obstruction is discharged,
the conjugated arbitrary components become an actual mathlib lax
modification, contravariantly from θ^R to σ^R. -/
def toRightModification (dσ : RightMateLaxData σ)
    (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    (h : Compatible dσ dθ Γ) :
    Oplax.LaxTrans.Modification dθ.right dσ.right where
  app X := conjugateComponent dσ dθ Γ X
  naturality {_ _} f := h f

/-- Exact existence criterion for transport to the RIGHT, keeping
both transformation structures and every chosen adjunction fixed. -/
theorem compatible_iff_exists (dσ : RightMateLaxData σ)
    (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ) :
    Compatible dσ dθ Γ ↔
      ∃ (m : Oplax.LaxTrans.Modification dθ.right dσ.right),
        ∀ X : B, m.app X = conjugateComponent dσ dθ Γ X := by
  constructor
  · intro h
    exact ⟨toRightModification dσ dθ Γ h, fun _ => rfl⟩
  · rintro ⟨m, hm⟩ X Y f
    simpa only [hm X, hm Y] using m.naturality f

/-- The transported right modification is uniquely determined by its
conjugated components; no arbitrary modification is re-selected. -/
theorem toRightModification_unique (dσ : RightMateLaxData σ)
    (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    (h : Compatible dσ dθ Γ)
    (m : Oplax.LaxTrans.Modification dθ.right dσ.right)
    (hm : ∀ X : B, m.app X = conjugateComponent dσ dθ Γ X) :
    m = toRightModification dσ dθ Γ h := by
  apply Oplax.LaxTrans.Modification.ext
  funext X
  exact hm X

/-- Any right-mate lax datum transports the identity modification.
This is a true global naturality statement, not merely componentwise. -/
theorem compatible_id (dσ : RightMateLaxData σ) :
    Compatible dσ dσ (Pseudofunctor.StrongTrans.Modification.id σ) := by
  intro X Y f
  change
    Bicategory.conjugateEquiv (dσ.adj X) (dσ.adj X) (𝟙 _) ▷ F.map f ≫
      dσ.right.naturality f =
    dσ.right.naturality f ≫
      G.map f ◁ Bicategory.conjugateEquiv (dσ.adj Y) (dσ.adj Y) (𝟙 _)
  simpa only [Bicategory.conjugateEquiv_id] using
    (Oplax.LaxTrans.Modification.id dσ.right).naturality f

/-- The identity modification is sent to the identity right-mate lax
modification, without assuming it is strong. -/
theorem toRightModification_id (dσ : RightMateLaxData σ) :
    toRightModification dσ dσ
      (Pseudofunctor.StrongTrans.Modification.id σ)
      (compatible_id dσ) =
    Oplax.LaxTrans.Modification.id dσ.right := by
  apply Oplax.LaxTrans.Modification.ext
  funext X
  change Bicategory.conjugateEquiv (dσ.adj X) (dσ.adj X) (𝟙 _) = 𝟙 _
  exact Bicategory.conjugateEquiv_id (dσ.adj X)

/-- Arbitrary vertical composition reverses under the original
conjugate-mate equivalences; no inverse of Γ or deltaMod is needed. -/
theorem conjugateComponent_vcomp
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (dι : RightMateLaxData ι)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    (deltaMod : Pseudofunctor.StrongTrans.Modification θ ι)
    (X : B) :
    conjugateComponent dσ dι
      (Pseudofunctor.StrongTrans.Modification.vcomp Γ deltaMod) X =
    conjugateComponent dθ dι deltaMod X ≫ conjugateComponent dσ dθ Γ X := by
  change
    Bicategory.conjugateEquiv (dι.adj X) (dσ.adj X)
        (Γ.app X ≫ deltaMod.app X) =
      Bicategory.conjugateEquiv (dι.adj X) (dθ.adj X) (deltaMod.app X) ≫
        Bicategory.conjugateEquiv (dθ.adj X) (dσ.adj X) (Γ.app X)
  exact (Bicategory.conjugateEquiv_comp
    (dι.adj X) (dθ.adj X) (dσ.adj X) (deltaMod.app X) (Γ.app X)).symm

/-- Natural arbitrary modifications are closed under the original
vertical paste. The corresponding right modifications compose in the
REVERSE order. -/
theorem compatible_vcomp
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (dι : RightMateLaxData ι)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    (deltaMod : Pseudofunctor.StrongTrans.Modification θ ι)
    (hΓ : Compatible dσ dθ Γ) (hdeltaMod : Compatible dθ dι deltaMod) :
    Compatible dσ dι
      (Pseudofunctor.StrongTrans.Modification.vcomp Γ deltaMod) := by
  let m : Oplax.LaxTrans.Modification dι.right dσ.right :=
    Oplax.LaxTrans.Modification.vcomp
      (toRightModification dθ dι deltaMod hdeltaMod)
      (toRightModification dσ dθ Γ hΓ)
  have hm (X : B) :
      m.app X =
        conjugateComponent dσ dι
          (Pseudofunctor.StrongTrans.Modification.vcomp Γ deltaMod) X := by
    change conjugateComponent dθ dι deltaMod X ≫
      conjugateComponent dσ dθ Γ X = _
    exact (conjugateComponent_vcomp dσ dθ dι Γ deltaMod X).symm
  intro X Y f
  simpa only [hm X, hm Y] using m.naturality f

/-- Full equality of actual right lax modifications (not only of
objectwise 2-cells): contravariant vertical functoriality. -/
theorem toRightModification_vcomp
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (dι : RightMateLaxData ι)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    (deltaMod : Pseudofunctor.StrongTrans.Modification θ ι)
    (hΓ : Compatible dσ dθ Γ) (hdeltaMod : Compatible dθ dι deltaMod) :
    toRightModification dσ dι
      (Pseudofunctor.StrongTrans.Modification.vcomp Γ deltaMod)
      (compatible_vcomp dσ dθ dι Γ deltaMod hΓ hdeltaMod) =
    Oplax.LaxTrans.Modification.vcomp
      (toRightModification dθ dι deltaMod hdeltaMod)
      (toRightModification dσ dθ Γ hΓ) := by
  apply Oplax.LaxTrans.Modification.ext
  funext X
  exact conjugateComponent_vcomp dσ dθ dι Γ deltaMod X

end Generic

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- The original v5.110 source lax right mate, its unchanged v5.50
unit, and its original v5.102 chosen native adjunctions. -/
def actualLiftSourceRightMateData :
    Generic.RightMateLaxData
      (actualLiftSourceRoundtripUnit (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) where
  right := actualLiftSourceRightMateLaxTrans (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
  adj X := (actualLiftSourceNativeAdjHom (W := W) A X).adj
  naturality_eq_mate {_ _} _ := rfl

/-- The same unchanged v5.49 counit, original target adjunctions, and
v5.110 target lax right mate, including its non-strict compositor. -/
def actualLiftTargetRightMateData :
    Generic.RightMateLaxData
      (actualLiftTargetRoundtripCounit (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) where
  right := actualLiftTargetRightMateLaxTrans (W := W) A
    (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)
  adj Y := (actualLiftTargetNativeAdjHom (W := W) A Y).adj
  naturality_eq_mate {_ _} _ := rfl

/-- The original source-unit triangle is an ACTUAL zero-obstruction
example of arbitrary modification mate transport. -/
theorem actualLiftSourceTriangle_compatible :
    Generic.Compatible
      (actualLiftSourceRightMateData (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftSourceRightMateData (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftSourceUnitLeftTriangleModification (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) := by
  rw [actualLiftSourceUnitLeftTriangleModification_eq_id]
  exact Generic.compatible_id
    (actualLiftSourceRightMateData (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))

/-- The original target-counit triangle is likewise compatible. -/
theorem actualLiftTargetTriangle_compatible :
    Generic.Compatible
      (actualLiftTargetRightMateData (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftTargetRightMateData (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftTargetCounitLeftTriangleModification (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) := by
  rw [actualLiftTargetCounitLeftTriangleModification_eq_id]
  exact Generic.compatible_id
    (actualLiftTargetRightMateData (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))

/-- The new GENERIC transport, specialized to the original source-unit
left triangle, recovers the ORIGINAL v5.111 source right triangle
modification as a full global mathlib modification. -/
theorem actualLiftSourceTriangle_transport_eq_original :
    Generic.toRightModification
      (actualLiftSourceRightMateData (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftSourceRightMateData (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftSourceUnitLeftTriangleModification (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftSourceTriangle_compatible (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) =
    actualLiftSourceRightMateTriangleModification (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel) := by
  apply Oplax.LaxTrans.Modification.ext
  funext X
  exact actualLiftSourceTriangle_conjugate_eq_rightMate (W := W) A X

/-- The same lossless generic-to-original recovery for the target counit. -/
theorem actualLiftTargetTriangle_transport_eq_original :
    Generic.toRightModification
      (actualLiftTargetRightMateData (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftTargetRightMateData (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftTargetCounitLeftTriangleModification (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))
      (actualLiftTargetTriangle_compatible (W := W) A
        (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel)) =
    actualLiftTargetRightMateTriangleModification (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel) := by
  apply Oplax.LaxTrans.Modification.ext
  funext Y
  exact actualLiftTargetTriangle_conjugate_eq_rightMate (W := W) A Y

#print axioms Generic.RightMateLaxData
#print axioms Generic.conjugateComponent
#print axioms Generic.Compatible
#print axioms Generic.toRightModification
#print axioms Generic.compatible_iff_exists
#print axioms Generic.toRightModification_unique
#print axioms Generic.compatible_id
#print axioms Generic.toRightModification_id
#print axioms Generic.conjugateComponent_vcomp
#print axioms Generic.compatible_vcomp
#print axioms Generic.toRightModification_vcomp
#print axioms actualLiftSourceRightMateData
#print axioms actualLiftTargetRightMateData
#print axioms actualLiftSourceTriangle_compatible
#print axioms actualLiftTargetTriangle_compatible
#print axioms actualLiftSourceTriangle_transport_eq_original
#print axioms actualLiftTargetTriangle_transport_eq_original

end

end KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113
