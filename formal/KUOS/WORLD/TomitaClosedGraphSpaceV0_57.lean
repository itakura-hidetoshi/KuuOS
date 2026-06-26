import KUOS.WORLD.TomitaClosedInverseV0_57
import Mathlib.Topology.Algebra.Module.ClosedSubmodule

/-!
The inherited norm on the domain of an unbounded operator need not be complete.
The correct complete analytic carrier is its closed graph inside the product
Hilbert space.  This file identifies the closed Tomita domain with that graph
as a real vector space and records completeness of the graph carrier.
-/

namespace KUOS.WORLD

noncomputable section

variable {A B H : Type*}
variable [NormedAddCommGroup H] [InnerProductSpace Complex H]
variable {T : TomitaGraphCore A B H}

namespace TomitaRealLinearPMapRealization

variable (R : TomitaRealLinearPMapRealization T)

/-- The graph of the closed Tomita operator, used as its graph-norm carrier. -/
def closedGraphSpace : Submodule Real (H × H) :=
  R.pmap.closure.graph

/-- The closed Tomita graph is a closed subset of the product Hilbert space. -/
theorem closedGraphSpace_isClosed :
    IsClosed (R.closedGraphSpace : Set (H × H)) := by
  change IsClosed (R.pmap.closure.graph : Set (H × H))
  exact R.mathlib_closure_isClosed

/-- Insert a closed-domain vector into the closed graph. -/
def closedDomainToGraph :
    R.pmap.closure.domain →ₗ[Real] R.closedGraphSpace where
  toFun x :=
    ⟨((x : H), R.pmap.closure x), LinearPMap.mem_graph R.pmap.closure x⟩
  map_add' x y := by
    apply Subtype.ext
    ext <;> simp [LinearPMap.map_add]
  map_smul' c x := by
    apply Subtype.ext
    ext <;> simp [LinearPMap.map_smul]

/-- Project a point of the closed graph to the closed operator domain. -/
def closedGraphToDomain :
    R.closedGraphSpace →ₗ[Real] R.pmap.closure.domain where
  toFun p :=
    ⟨(p : H × H).1, LinearPMap.mem_domain_of_mem_graph p.property⟩
  map_add' p q := by
    apply Subtype.ext
    rfl
  map_smul' c p := by
    apply Subtype.ext
    rfl

@[simp]
theorem closedGraphToDomain_closedDomainToGraph
    (x : R.pmap.closure.domain) :
    R.closedGraphToDomain (R.closedDomainToGraph x) = x := by
  apply Subtype.ext
  rfl

@[simp]
theorem closedDomainToGraph_closedGraphToDomain
    (p : R.closedGraphSpace) :
    R.closedDomainToGraph (R.closedGraphToDomain p) = p := by
  apply Subtype.ext
  apply Prod.ext
  · rfl
  · exact R.pmap.closure.mem_graph_snd_inj
      (LinearPMap.mem_graph R.pmap.closure (R.closedGraphToDomain p))
      p.property rfl

/-- The closed domain and the closed graph are real-linearly equivalent. -/
def closedDomainGraphLinearEquiv :
    R.pmap.closure.domain ≃ₗ[Real] R.closedGraphSpace :=
  { R.closedDomainToGraph with
    invFun := R.closedGraphToDomain
    left_inv := R.closedGraphToDomain_closedDomainToGraph
    right_inv := R.closedDomainToGraph_closedGraphToDomain }

@[simp]
theorem closedDomainGraphLinearEquiv_apply
    (x : R.pmap.closure.domain) :
    R.closedDomainGraphLinearEquiv x = R.closedDomainToGraph x :=
  rfl

/-- The graph-space norm is the product norm of a vector and its Tomita image. -/
def closedGraphNorm (x : R.pmap.closure.domain) : Real :=
  ‖R.closedDomainToGraph x‖

@[simp]
theorem closedGraphNorm_eq
    (x : R.pmap.closure.domain) :
    R.closedGraphNorm x = ‖((x : H), R.pmap.closure x)‖ :=
  rfl

/-- A closed Tomita graph over a complete Hilbert carrier is complete. -/
noncomputable instance closedGraphSpaceComplete
    [CompleteSpace H] : CompleteSpace R.closedGraphSpace := by
  letI : IsClosed (R.closedGraphSpace : Set (H × H)) :=
    R.closedGraphSpace_isClosed
  infer_instance

end TomitaRealLinearPMapRealization
end
end KUOS.WORLD
