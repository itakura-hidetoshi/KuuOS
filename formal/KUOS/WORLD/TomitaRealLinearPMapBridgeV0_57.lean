import KUOS.WORLD.TomitaGraphCoreV0_57
import Mathlib.Analysis.InnerProductSpace.LinearPMap

/-!
A Mathlib bridge from the representation-level Tomita graph kernel to a
partially defined real-linear operator.

The algebraic Tomita map is conjugate-linear over `Complex`, hence linear over
`Real`. This file packages a real-linear `LinearPMap` realization whose graph
is the algebraic graph, proves Mathlib closability from the graph criterion,
and identifies its Mathlib closure with the single-valued closed graph value.
-/

namespace KUOS.WORLD

noncomputable section

open Topology

variable {A B H : Type*}
variable [NormedAddCommGroup H] [InnerProductSpace Complex H]

/--
A real-linear partial-operator realization of a representation-level Tomita
core. The final two fields retain the conjugate-linear scalar law on the
algebraic domain.
-/
structure TomitaRealLinearPMapRealization
    (T : TomitaGraphCore A B H) where
  pmap : LinearPMap (RingHom.id Real) H H
  graph_eq : (pmap.graph : Set (H × H)) = T.graph
  domain_eq : (pmap.domain : Set H) = T.domain
  complex_smul_mem :
    forall (c : Complex) {x : H}, x ∈ pmap.domain -> c • x ∈ pmap.domain
  map_complex_smul :
    forall (c : Complex) (x : H) (hx : x ∈ pmap.domain),
      pmap ⟨c • x, complex_smul_mem c hx⟩ =
        star c • pmap ⟨x, hx⟩

namespace TomitaRealLinearPMapRealization

variable {T : TomitaGraphCore A B H}
variable (R : TomitaRealLinearPMapRealization T)

/-- The realized real-linear partial operator has dense domain. -/
theorem dense_domain : Dense (R.pmap.domain : Set H) := by
  rw [R.domain_eq]
  exact T.domain_dense

/-- The realized algebraic graph is closed under subtraction. -/
theorem algebraic_graph_sub {p q : H × H}
    (hp : T.graph p) (hq : T.graph q) :
    T.graph (p - q) := by
  rw [← R.graph_eq] at hp hq ⊢
  exact R.pmap.graph.sub_mem hp hq

/--
The graph-level closability theorem produces Mathlib's standard
`LinearPMap.IsClosable` witness.
-/
theorem pmap_isClosable : R.pmap.IsClosable := by
  let g := R.pmap.graph.topologicalClosure
  have hg : forall (x : H × H), x ∈ g -> x.1 = 0 -> x.2 = 0 := by
    intro x hx hx0
    have hxSet : x ∈ closure (R.pmap.graph : Set (H × H)) := by
      simpa only [Submodule.topologicalClosure_coe] using hx
    have hVertical : (closure T.graph) (0, x.2) := by
      rw [← R.graph_eq]
      simpa [hx0] using hxSet
    exact T.graph_closable x.2 hVertical
  refine ⟨g.toLinearPMap, ?_⟩
  exact (Submodule.toLinearPMap_graph_eq g hg).symm

/-- The graph closure is the graph of Mathlib's closure operator. -/
theorem graph_closure_eq_mathlib_closure :
    R.pmap.graph.topologicalClosure = R.pmap.closure.graph :=
  (pmap_isClosable R).graph_closure_eq_closure_graph

/-- Mathlib's closure operator is closed. -/
theorem mathlib_closure_isClosed : R.pmap.closure.IsClosed :=
  (pmap_isClosable R).closure_isClosed

/-- The algebraic operator is contained in its Mathlib closure. -/
theorem le_mathlib_closure : R.pmap ≤ R.pmap.closure :=
  LinearPMap.le_closure R.pmap

/-- The Mathlib closure remains densely defined. -/
theorem mathlib_closure_dense_domain :
    Dense (R.pmap.closure.domain : Set H) := by
  apply (dense_domain R).mono
  exact (LinearPMap.le_closure R.pmap).1

/-- A point of the Mathlib closure graph lies in the set-theoretic graph closure. -/
theorem mathlib_closure_graph_mem_set_closure
    (x : R.pmap.closure.domain) :
    (closure T.graph) ((x : H), R.pmap.closure x) := by
  have hxGraph :
      ((x : H), R.pmap.closure x) ∈ R.pmap.closure.graph :=
    LinearPMap.mem_graph R.pmap.closure x
  have hxTopological :
      ((x : H), R.pmap.closure x) ∈ R.pmap.graph.topologicalClosure := by
    rw [(pmap_isClosable R).graph_closure_eq_closure_graph]
    exact hxGraph
  have hxSet :
      ((x : H), R.pmap.closure x) ∈
        closure (R.pmap.graph : Set (H × H)) := by
    simpa only [Submodule.topologicalClosure_coe] using hxTopological
  rwa [R.graph_eq] at hxSet

/-- Every point in the Mathlib closure domain belongs to the graph-level closed domain. -/
def graphClosedDomainOfMathlib
    (x : R.pmap.closure.domain) : T.closedDomain (x : H) :=
  ⟨R.pmap.closure x, mathlib_closure_graph_mem_set_closure R x⟩

/--
The value of Mathlib's closure agrees with the unique value selected from the
set-theoretic closed graph.
-/
theorem mathlib_closure_apply_eq_closedValue
    (x : R.pmap.closure.domain) :
    R.pmap.closure x =
      T.closedValue (x : H) (graphClosedDomainOfMathlib R x) := by
  exact T.closedValue_unique (algebraic_graph_sub R)
    (x : H) (R.pmap.closure x) (graphClosedDomainOfMathlib R x)
    (mathlib_closure_graph_mem_set_closure R x)

/-- The conjugate-linear scalar law on the algebraic domain. -/
theorem map_complex_smul_apply
    (c : Complex) (x : H) (hx : x ∈ R.pmap.domain) :
    R.pmap ⟨c • x, R.complex_smul_mem c hx⟩ =
      star c • R.pmap ⟨x, hx⟩ :=
  R.map_complex_smul c x hx

end TomitaRealLinearPMapRealization
end
end KUOS.WORLD
