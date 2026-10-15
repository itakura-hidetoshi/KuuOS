import KUOS.WORLD.TomitaClosedComplexDomainV0_57

/-!
The closed Tomita operator is injective and its graph is invariant under
coordinate exchange.  Mathlib's `LinearPMap.inverse` therefore agrees with the
closed Tomita operator itself.
-/

namespace KUOS.WORLD

noncomputable section

open Topology

variable {A B H : Type*}
variable [NormedAddCommGroup H] [InnerProductSpace Complex H]
variable {T : TomitaGraphCore A B H}

namespace TomitaRealLinearPMapRealization

variable (R : TomitaRealLinearPMapRealization T)

/-- Coordinate exchange preserves the Mathlib graph of the closed Tomita operator. -/
theorem mathlib_closure_graph_flip {x y : H}
    (hxy : (x, y) ∈ R.pmap.closure.graph) :
    (y, x) ∈ R.pmap.closure.graph := by
  have hSet : (closure T.graph) (x, y) := by
    rw [R.set_graph_closure_eq_mathlib_closure_graph]
    exact hxy
  have hFlipSet : (closure T.graph) (y, x) :=
    T.closure_graph_flip hSet
  rw [R.set_graph_closure_eq_mathlib_closure_graph] at hFlipSet
  exact hFlipSet

/-- The closed Tomita operator has trivial kernel. -/
theorem mathlib_closure_ker_eq_bot :
    LinearMap.ker R.pmap.closure.toFun = ⊥ := by
  rw [LinearMap.ker_eq_bot']
  intro x hx
  apply R.mathlib_closure_injective
  simpa using hx

/-- Swapping coordinates leaves the closed Tomita graph unchanged. -/
theorem mathlib_closure_graph_prodComm :
    R.pmap.closure.graph.map
        (LinearEquiv.prodComm Real H H : (H × H) →ₗ[Real] (H × H)) =
      R.pmap.closure.graph := by
  ext p
  rw [Submodule.mem_map]
  constructor
  · rintro ⟨q, hq, hqp⟩
    have hflip : (q.2, q.1) ∈ R.pmap.closure.graph :=
      R.mathlib_closure_graph_flip hq
    have hp : (q.2, q.1) = p := by
      simpa only [LinearEquiv.coe_coe, LinearEquiv.prodComm_apply] using hqp
    rwa [hp] at hflip
  · intro hp
    refine ⟨(p.2, p.1), R.mathlib_closure_graph_flip hp, ?_⟩
    simp

/-- The graph of the inverse closed Tomita operator is the original graph. -/
theorem mathlib_closure_inverse_graph :
    R.pmap.closure.inverse.graph = R.pmap.closure.graph := by
  rw [LinearPMap.inverse_graph R.mathlib_closure_ker_eq_bot]
  exact R.mathlib_closure_graph_prodComm

/-- The closed Tomita operator is equal to its Mathlib inverse. -/
theorem mathlib_closure_inverse_eq :
    R.pmap.closure.inverse = R.pmap.closure :=
  LinearPMap.eq_of_eq_graph R.mathlib_closure_inverse_graph

@[simp]
theorem mathlib_closure_inverse_domain :
    R.pmap.closure.inverse.domain = R.pmap.closure.domain := by
  rw [R.mathlib_closure_inverse_eq]

end TomitaRealLinearPMapRealization
end
end KUOS.WORLD
