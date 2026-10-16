import KUOS.WORLD.TomitaClosedGraphSpaceV0_57
import Mathlib.Analysis.Normed.Operator.LinearIsometry

/-!
Coordinate exchange preserves the closed Tomita graph.  On the complete graph
carrier this symmetry is a real-linear isometric involution.  Transported back
to the operator domain, it states that the closed Tomita operator preserves the
graph-space norm.
-/

namespace KUOS.WORLD

noncomputable section

variable {A B H : Type*}
variable [NormedAddCommGroup H] [InnerProductSpace Complex H]
variable {T : TomitaGraphCore A B H}

namespace TomitaRealLinearPMapRealization

variable (R : TomitaRealLinearPMapRealization T)

/-- Coordinate exchange as a real-linear endomorphism of the closed graph. -/
def closedGraphSwapLinearMap :
    R.closedGraphSpace →ₗ[Real] R.closedGraphSpace where
  toFun p :=
    ⟨((p : H × H).2, (p : H × H).1), by
      change ((p : H × H).2, (p : H × H).1) ∈ R.pmap.closure.graph
      exact R.mathlib_closure_graph_flip p.property⟩
  map_add' p q := by
    apply Subtype.ext
    rfl
  map_smul' c p := by
    apply Subtype.ext
    rfl

/-- Coordinate exchange is involutive on the closed graph. -/
theorem closedGraphSwapLinearMap_involutive :
    Function.Involutive R.closedGraphSwapLinearMap := by
  intro p
  apply Subtype.ext
  rfl

/-- Coordinate exchange as a real-linear automorphism of the closed graph. -/
def closedGraphSwapLinearEquiv :
    R.closedGraphSpace ≃ₗ[Real] R.closedGraphSpace :=
  LinearEquiv.ofInvolutive R.closedGraphSwapLinearMap
    R.closedGraphSwapLinearMap_involutive

/-- Coordinate exchange is an isometry for the product graph norm. -/
def closedGraphSwapLinearIsometryEquiv :
    R.closedGraphSpace ≃ₗᵢ[Real] R.closedGraphSpace :=
  ⟨R.closedGraphSwapLinearEquiv, by
    intro p
    change
      ‖((p : H × H).2, (p : H × H).1)‖ = ‖(p : H × H)‖
    rw [Prod.norm_def, Prod.norm_def, max_comm]⟩

@[simp]
theorem closedGraphSwapLinearIsometryEquiv_apply_apply
    (p : R.closedGraphSpace) :
    R.closedGraphSwapLinearIsometryEquiv
        (R.closedGraphSwapLinearIsometryEquiv p) = p :=
  R.closedGraphSwapLinearMap_involutive p

/-- Graph coordinate exchange represents the closed Tomita action on its domain. -/
theorem closedGraphSwap_closedDomainToGraph
    (x : R.pmap.closure.domain) :
    R.closedGraphSwapLinearIsometryEquiv (R.closedDomainToGraph x) =
      R.closedDomainToGraph (R.closedDomainLinearMap x) := by
  apply Subtype.ext
  apply Prod.ext
  · rfl
  · change (x : H) =
      R.pmap.closure
        ⟨R.pmap.closure x, R.mathlib_closure_map_mem_domain x⟩
    exact (R.mathlib_closure_map_map x).symm

/-- The closed Tomita operator preserves the graph-space norm. -/
theorem closedGraphNorm_map
    (x : R.pmap.closure.domain) :
    R.closedGraphNorm (R.closedDomainLinearMap x) =
      R.closedGraphNorm x := by
  unfold closedGraphNorm
  calc
    ‖R.closedDomainToGraph (R.closedDomainLinearMap x)‖ =
        ‖R.closedGraphSwapLinearIsometryEquiv (R.closedDomainToGraph x)‖ := by
          rw [R.closedGraphSwap_closedDomainToGraph x]
    _ = ‖R.closedDomainToGraph x‖ :=
      R.closedGraphSwapLinearIsometryEquiv.norm_map
        (R.closedDomainToGraph x)

end TomitaRealLinearPMapRealization
end
end KUOS.WORLD
