import Mathlib
import KUOS.WORLD.RealHilbertL2SelfAdjointProofReceiptBridgeV0_28

/-!
Kū–Indra WORLD noncommutative operator-algebra module v0.29.

The global WORLD observable algebra is represented faithfully on the real Hilbert
carrier. Its genuinely noncommutative directions generate a nontrivial commutator
submodule. Relations between local observable algebras are not reduced to object
attributes: they are encoded as bimodules through commuting left and right
operator representations.
-/

namespace KUOS
namespace WORLD

structure FaithfulNoncommutativeOperatorAlgebra
    (C : RealHilbertL2Carrier) where
  A : Type
  [ring : Ring A]
  [algebra : Algebra ℝ A]
  representation : A →ₐ[ℝ] Module.End ℝ C.H
  faithful : Function.Injective representation
  noncommutingWitness : ∃ a b : A, a * b ≠ b * a

attribute [instance] FaithfulNoncommutativeOperatorAlgebra.ring
attribute [instance] FaithfulNoncommutativeOperatorAlgebra.algebra

namespace FaithfulNoncommutativeOperatorAlgebra

variable {C : RealHilbertL2Carrier}
variable (N : FaithfulNoncommutativeOperatorAlgebra C)

def commutatorSet : Set N.A :=
  {c | ∃ a b : N.A, c = a * b - b * a}

def commutatorSubmodule : Submodule ℝ N.A :=
  Submodule.span ℝ N.commutatorSet

theorem commutator_mem (a b : N.A) :
    a * b - b * a ∈ N.commutatorSubmodule := by
  apply Submodule.subset_span
  exact ⟨a, b, rfl⟩

theorem commutatorSubmodule_ne_bot :
    N.commutatorSubmodule ≠ ⊥ := by
  rcases N.noncommutingWitness with ⟨a, b, hab⟩
  intro hbot
  have hmem : a * b - b * a ∈ N.commutatorSubmodule :=
    N.commutator_mem a b
  rw [hbot] at hmem
  have hzero : a * b - b * a = 0 := by
    simpa using hmem
  exact hab (sub_eq_zero.mp hzero)

theorem representation_mul_apply (a b : N.A) (x : C.H) :
    N.representation (a * b) x =
      N.representation a (N.representation b x) := by
  calc
    N.representation (a * b) x =
        (N.representation a * N.representation b) x := by
          rw [map_mul]
    _ = N.representation a (N.representation b x) := rfl

theorem representation_commutator_apply (a b : N.A) (x : C.H) :
    N.representation (a * b - b * a) x =
      N.representation a (N.representation b x) -
        N.representation b (N.representation a x) := by
  calc
    N.representation (a * b - b * a) x =
        (N.representation (a * b) - N.representation (b * a)) x := by
          rw [map_sub]
    _ = N.representation (a * b) x - N.representation (b * a) x := rfl
    _ = N.representation a (N.representation b x) -
        N.representation b (N.representation a x) := by
          rw [N.representation_mul_apply, N.representation_mul_apply]

theorem represented_noncommuting :
    ∃ a b : N.A,
      N.representation a * N.representation b ≠
        N.representation b * N.representation a := by
  rcases N.noncommutingWitness with ⟨a, b, hab⟩
  refine ⟨a, b, ?_⟩
  intro h
  apply hab
  apply N.faithful
  calc
    N.representation (a * b) =
        N.representation a * N.representation b := by
          rw [map_mul]
    _ = N.representation b * N.representation a := h
    _ = N.representation (b * a) := by
          rw [map_mul]

def representedCommutatorSubmodule :
    Submodule ℝ (Module.End ℝ C.H) :=
  N.commutatorSubmodule.map N.representation.toLinearMap

theorem representedCommutatorSubmodule_ne_bot :
    N.representedCommutatorSubmodule ≠ ⊥ := by
  rcases N.noncommutingWitness with ⟨a, b, hab⟩
  let c : N.A := a * b - b * a
  have hc_mem : c ∈ N.commutatorSubmodule := by
    exact N.commutator_mem a b
  have hrepr_mem : N.representation c ∈ N.representedCommutatorSubmodule := by
    exact ⟨c, hc_mem, rfl⟩
  intro hbot
  rw [hbot] at hrepr_mem
  have hrepr_zero : N.representation c = 0 := by
    simpa using hrepr_mem
  have hc_zero : c = 0 := by
    apply N.faithful
    simpa using hrepr_zero
  exact hab (sub_eq_zero.mp hc_zero)

end FaithfulNoncommutativeOperatorAlgebra

structure OperatorBimodule
    (A B : Type)
    [Ring A] [Algebra ℝ A]
    [Ring B] [Algebra ℝ B] where
  E : Type
  [addCommGroup : AddCommGroup E]
  [moduleReal : Module ℝ E]
  leftRepresentation : A →ₐ[ℝ] Module.End ℝ E
  rightRepresentation : Bᵐᵒᵖ →ₐ[ℝ] Module.End ℝ E
  mixedCommute : ∀ (a : A) (b : Bᵐᵒᵖ) (x : E),
    leftRepresentation a (rightRepresentation b x) =
      rightRepresentation b (leftRepresentation a x)

attribute [instance] OperatorBimodule.addCommGroup
attribute [instance] OperatorBimodule.moduleReal

namespace OperatorBimodule

variable {A B : Type}
variable [Ring A] [Algebra ℝ A]
variable [Ring B] [Algebra ℝ B]
variable (E : OperatorBimodule A B)

theorem left_mul_apply (a₁ a₂ : A) (x : E.E) :
    E.leftRepresentation (a₁ * a₂) x =
      E.leftRepresentation a₁ (E.leftRepresentation a₂ x) := by
  calc
    E.leftRepresentation (a₁ * a₂) x =
        (E.leftRepresentation a₁ * E.leftRepresentation a₂) x := by
          rw [map_mul]
    _ = E.leftRepresentation a₁ (E.leftRepresentation a₂ x) := rfl

theorem right_mul_apply (b₁ b₂ : Bᵐᵒᵖ) (x : E.E) :
    E.rightRepresentation (b₁ * b₂) x =
      E.rightRepresentation b₁ (E.rightRepresentation b₂ x) := by
  calc
    E.rightRepresentation (b₁ * b₂) x =
        (E.rightRepresentation b₁ * E.rightRepresentation b₂) x := by
          rw [map_mul]
    _ = E.rightRepresentation b₁ (E.rightRepresentation b₂ x) := rfl

theorem left_right_commute (a : A) (b : Bᵐᵒᵖ) (x : E.E) :
    E.leftRepresentation a (E.rightRepresentation b x) =
      E.rightRepresentation b (E.leftRepresentation a x) :=
  E.mixedCommute a b x

end OperatorBimodule

structure WorldNoncommutativeOperatorAlgebra
    (C : RealHilbertL2Carrier) where
  global : FaithfulNoncommutativeOperatorAlgebra C
  Region : Type
  localObservable : Region → Subalgebra ℝ global.A
  relation : ∀ i j : Region,
    OperatorBimodule (localObservable i) (localObservable j)
  background : Subalgebra ℝ global.A
  action : Subalgebra ℝ global.A
  worldNotIdentifiedWithOperatorCarrier : Prop
  worldNotIdentifiedProof : worldNotIdentifiedWithOperatorCarrier
  relationNotReducedToObjectAttribute : Prop
  relationNotReducedProof : relationNotReducedToObjectAttribute
  multiWorldNoncollapsePreserved : Prop
  multiWorldNoncollapseProof : multiWorldNoncollapsePreserved
  twoTruthsGapPreserved : Prop
  twoTruthsGapProof : twoTruthsGapPreserved

namespace WorldNoncommutativeOperatorAlgebra

variable {C : RealHilbertL2Carrier}
variable (W : WorldNoncommutativeOperatorAlgebra C)

theorem global_commutator_submodule_nontrivial :
    W.global.commutatorSubmodule ≠ ⊥ :=
  W.global.commutatorSubmodule_ne_bot

theorem global_represented_commutator_submodule_nontrivial :
    W.global.representedCommutatorSubmodule ≠ ⊥ :=
  W.global.representedCommutatorSubmodule_ne_bot

theorem relation_actions_commute
    (i j : W.Region)
    (a : W.localObservable i)
    (b : (W.localObservable j)ᵐᵒᵖ)
    (x : (W.relation i j).E) :
    (W.relation i j).leftRepresentation a
        ((W.relation i j).rightRepresentation b x) =
      (W.relation i j).rightRepresentation b
        ((W.relation i j).leftRepresentation a x) :=
  (W.relation i j).mixedCommute a b x

theorem representation_boundary_preserved :
    W.worldNotIdentifiedWithOperatorCarrier ∧
    W.relationNotReducedToObjectAttribute ∧
    W.multiWorldNoncollapsePreserved ∧
    W.twoTruthsGapPreserved :=
  ⟨W.worldNotIdentifiedProof, W.relationNotReducedProof,
    W.multiWorldNoncollapseProof, W.twoTruthsGapProof⟩

end WorldNoncommutativeOperatorAlgebra
end WORLD
end KUOS
