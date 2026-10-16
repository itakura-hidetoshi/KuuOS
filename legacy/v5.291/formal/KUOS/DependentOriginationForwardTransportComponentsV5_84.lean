import KUOS.DependentOriginationGlobalForwardSwallowtailInterchangerV5_83

namespace KUOS.DependentOriginationForwardTransportComponentsV5_84

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans

set_option autoImplicit false
noncomputable section

/-!
# Component semantics of native StrongTrans equality transports v5.84

The global forward-swallowtail comparison of v5.83 uses eqToIso
only to bridge *proved* whole-StrongTrans equalities. To identify its
component with the original four-cell v5.68 paste, those transports
must be shown to act on object components via their original equality
proofs, without postulating strictness or another chosen 2-cell.

This generic file proves exactly how eqToIso and vertical composition
in Mathlib's native StrongTrans hom category act on components.
At the pinned Mathlib revision, eqToIso is built from eqToHom, while
StrongTrans.homCategory uses Modification.id and Modification.vcomp.
Thus equality induction and definitional reduction expose the original
component identity and vertical paste without any extra coherence choice.
The actual-lift component identification is a separate, subsequent step.
-/

namespace Generic

universe uB vB wB uC vC wC

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable {F G : Pseudofunctor B C}

local instance sourceStrongTransCategory :
    Category (Pseudofunctor.StrongTrans F G) :=
  Pseudofunctor.StrongTrans.homCategory
    (B := B) (C := C) (F := F) (G := G)

/-- The underlying component of a native equality-transport modification
is the equality transport of the original component 1-morphisms. -/
theorem eqToIso_hom_app
    {eta theta : Pseudofunctor.StrongTrans F G}
    (h : eta = theta) (X : B) :
    (eqToIso h).hom.as.app X =
      eqToHom (congrArg
        (fun t : Pseudofunctor.StrongTrans F G => t.app X) h) := by
  cases h
  rfl

/-- The inverse equality-transport modification is likewise the
componentwise inverse equality transport, with no extra pseudofunctor
coherence cell. -/
theorem eqToIso_inv_app
    {eta theta : Pseudofunctor.StrongTrans F G}
    (h : eta = theta) (X : B) :
    (eqToIso h).inv.as.app X =
      eqToHom (congrArg
        (fun t : Pseudofunctor.StrongTrans F G => t.app X) h.symm) := by
  cases h
  rfl

/-- One may supply any proved component equality: proof irrelevance
guarantees that no change of mathematical 2-cell is introduced. -/
theorem eqToIso_hom_app_of_app_eq
    {eta theta : Pseudofunctor.StrongTrans F G}
    (h : eta = theta) (X : B)
    (happ : eta.app X = theta.app X) :
    (eqToIso h).hom.as.app X = eqToHom happ := by
  cases h
  cases happ
  rfl

/-- A composite of two modifications in the native StrongTrans hom
category has precisely the old vertical composition of 2-cells at X. -/
theorem isoTrans_hom_app
    {eta theta iota : Pseudofunctor.StrongTrans F G}
    (e : eta ≅ theta) (d : theta ≅ iota) (X : B) :
    (e ≪≫ d).hom.as.app X =
      e.hom.as.app X ≫ d.hom.as.app X :=
  rfl

end Generic

#print axioms Generic.eqToIso_hom_app
#print axioms Generic.eqToIso_inv_app
#print axioms Generic.eqToIso_hom_app_of_app_eq
#print axioms Generic.isoTrans_hom_app

end

end KUOS.DependentOriginationForwardTransportComponentsV5_84
