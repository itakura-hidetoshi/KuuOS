import KUOS.WORLD.TomitaRealLinearPMapBridgeV0_57

/-!
The conjugate-linear scalar law of the algebraic Tomita map survives graph
closure.  Consequently the Mathlib closure of its real-linear realization is
complex conjugate-linear on its closed domain.
-/

namespace KUOS.WORLD

noncomputable section

open Filter Topology

variable {A B H : Type*}
variable [NormedAddCommGroup H] [InnerProductSpace Complex H]
variable {T : TomitaGraphCore A B H}

namespace TomitaRealLinearPMapRealization

variable (R : TomitaRealLinearPMapRealization T)

/-- The algebraic Tomita graph is stable under conjugate scalar multiplication. -/
theorem algebraic_graph_complex_smul
    (c : Complex) {x y : H}
    (hxy : T.graph (x, y)) :
    T.graph (c • x, star c • y) := by
  rw [← TomitaRealLinearPMapRealization.graph_eq R] at hxy ⊢
  rw [LinearPMap.mem_graph_iff] at hxy ⊢
  rcases hxy with ⟨u, hux, huy⟩
  let v : R.pmap.domain :=
    ⟨c • (u : H), R.complex_smul_mem c u.property⟩
  refine ⟨v, ?_, ?_⟩
  · change c • (u : H) = c • x
    rw [hux]
  · change R.pmap v = star c • y
    dsimp [v]
    rw [R.map_complex_smul c (u : H) u.property, huy]

/-- The closed Tomita graph is stable under conjugate scalar multiplication. -/
theorem closure_graph_complex_smul
    (c : Complex) {x y : H}
    (hxy : (closure T.graph) (x, y)) :
    (closure T.graph) (c • x, star c • y) := by
  obtain ⟨p, hp, hpLim⟩ := mem_closure_iff_seq_limit.mp hxy
  refine mem_closure_iff_seq_limit.mpr ?_
  refine ⟨(fun n => (c • (p n).1, star c • (p n).2)), ?_, ?_⟩
  · intro n
    exact R.algebraic_graph_complex_smul c (hp n)
  · have hfst : Tendsto (fun n => (p n).1) atTop (nhds x) :=
      (continuous_fst.tendsto (x, y)).comp hpLim
    have hsnd : Tendsto (fun n => (p n).2) atTop (nhds y) :=
      (continuous_snd.tendsto (x, y)).comp hpLim
    have hc : Tendsto (fun n => c • (p n).1) atTop (nhds (c • x)) :=
      tendsto_const_nhds.smul hfst
    have hstar :
        Tendsto (fun n => star c • (p n).2) atTop (nhds (star c • y)) :=
      tendsto_const_nhds.smul hsnd
    exact hc.prod_mk hstar

/-- The set-theoretic closed graph equals the graph of Mathlib's closure. -/
theorem set_graph_closure_eq_mathlib_closure_graph :
    closure T.graph = (R.pmap.closure.graph : Set (H × H)) := by
  ext p
  change p ∈ closure T.graph ↔ p ∈ R.pmap.closure.graph
  rw [← TomitaRealLinearPMapRealization.graph_eq R]
  rw [← Submodule.topologicalClosure_coe]
  rw [(R.pmap_isClosable).graph_closure_eq_closure_graph]

/-- The domain of the closed Tomita operator is stable under complex scalars. -/
theorem closure_complex_smul_mem
    (c : Complex) (x : R.pmap.closure.domain) :
    c • (x : H) ∈ R.pmap.closure.domain := by
  rw [LinearPMap.mem_domain_iff]
  refine ⟨star c • R.pmap.closure x, ?_⟩
  rw [← R.set_graph_closure_eq_mathlib_closure_graph]
  exact R.closure_graph_complex_smul c
    (R.mathlib_closure_graph_mem_set_closure x)

/-- Mathlib's closed Tomita operator is conjugate-linear on its domain. -/
theorem mathlib_closure_map_complex_smul
    (c : Complex) (x : R.pmap.closure.domain) :
    R.pmap.closure
        ⟨c • (x : H), R.closure_complex_smul_mem c x⟩ =
      star c • R.pmap.closure x := by
  have hActual :
      (c • (x : H),
          R.pmap.closure ⟨c • (x : H), R.closure_complex_smul_mem c x⟩) ∈
        R.pmap.closure.graph :=
    LinearPMap.mem_graph R.pmap.closure
      ⟨c • (x : H), R.closure_complex_smul_mem c x⟩
  have hScaled :
      (c • (x : H), star c • R.pmap.closure x) ∈
        R.pmap.closure.graph := by
    rw [← R.set_graph_closure_eq_mathlib_closure_graph]
    exact R.closure_graph_complex_smul c
      (R.mathlib_closure_graph_mem_set_closure x)
  exact R.pmap.closure.mem_graph_snd_inj hActual hScaled rfl

end TomitaRealLinearPMapRealization
end
end KUOS.WORLD
