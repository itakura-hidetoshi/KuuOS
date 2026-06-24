import KUOS.WORLD.TomitaRealLinearPMapBridgeV0_57

/-!
Construction of the algebraic Tomita partial operator from a real-linear graph.

The representation-level core intentionally does not assume algebraic
operations on its representative type.  This bridge instead records that its
concrete graph in the Hilbert carrier is a real submodule, together with the
complex conjugate scalar action.  Mathlib's `Submodule.toLinearPMap` then
constructs the partial operator directly from that graph.
-/

namespace KUOS.WORLD

noncomputable section

variable {A B H : Type*}
variable [NormedAddCommGroup H] [InnerProductSpace Complex H]

/--
Real-submodule data for a representation-level algebraic Tomita graph.

The graph is real-linear because the Tomita map is conjugate-linear over
`Complex`.  The last field retains the full complex conjugate scalar law.
-/
structure TomitaRealGraphSubmoduleData
    (T : TomitaGraphCore A B H) where
  graphSubmodule : Submodule Real (H × H)
  graph_eq : (graphSubmodule : Set (H × H)) = T.graph
  complex_smul_mem :
    forall (c : Complex) {x y : H},
      (x, y) ∈ graphSubmodule ->
        (c • x, star c • y) ∈ graphSubmodule

namespace TomitaRealGraphSubmoduleData

variable {T : TomitaGraphCore A B H}
variable (D : TomitaRealGraphSubmoduleData T)

/-- A vertical vector in the algebraic graph must vanish. -/
theorem vertical_unique {y : H}
    (hy : (0, y) ∈ D.graphSubmodule) : y = 0 := by
  have hyT : T.graph (0, y) := by
    rwa [← D.graph_eq]
  have hzeroT : T.graph (0, 0) := by
    rw [← D.graph_eq]
    exact D.graphSubmodule.zero_mem
  exact T.graph_right_unique hyT hzeroT

/-- The real-linear algebraic Tomita partial operator constructed from its graph. -/
def pmap : LinearPMap (RingHom.id Real) H H :=
  D.graphSubmodule.toLinearPMap

/-- The graph of the constructed partial operator is exactly the input submodule. -/
theorem pmap_graph_eq_submodule :
    D.pmap.graph = D.graphSubmodule := by
  apply Submodule.toLinearPMap_graph_eq
  rintro ⟨x, y⟩ hxy hx
  simp only at hx
  subst x
  exact D.vertical_unique hxy

/-- The constructed partial operator has exactly the representation-level Tomita graph. -/
theorem pmap_graph_eq :
    (D.pmap.graph : Set (H × H)) = T.graph := by
  rw [D.pmap_graph_eq_submodule]
  exact D.graph_eq

/-- The domain of the constructed partial operator is the represented left domain. -/
theorem pmap_domain_eq :
    (D.pmap.domain : Set H) = T.domain := by
  ext x
  constructor
  · intro hx
    rw [LinearPMap.mem_domain_iff] at hx
    rcases hx with ⟨y, hxy⟩
    have hxyT : T.graph (x, y) := by
      rw [← D.pmap_graph_eq]
      exact hxy
    rcases hxyT with ⟨a, hxa, _⟩
    exact ⟨a, hxa.symm⟩
  · intro hx
    rcases hx with ⟨a, rfl⟩
    rw [LinearPMap.mem_domain_iff]
    refine ⟨T.leftVector (T.leftStar a), ?_⟩
    rw [D.pmap_graph_eq]
    exact ⟨a, rfl, rfl⟩

/-- Complex scalar multiplication preserves the constructed operator domain. -/
theorem complex_smul_mem_domain
    (c : Complex) {x : H} (hx : x ∈ D.pmap.domain) :
    c • x ∈ D.pmap.domain := by
  rw [LinearPMap.mem_domain_iff] at hx ⊢
  rcases hx with ⟨y, hxy⟩
  refine ⟨star c • y, ?_⟩
  rw [D.pmap_graph_eq_submodule] at hxy ⊢
  exact D.complex_smul_mem c hxy

/-- The constructed operator obeys the complex conjugate scalar law. -/
theorem map_complex_smul
    (c : Complex) (x : H) (hx : x ∈ D.pmap.domain) :
    D.pmap ⟨c • x, D.complex_smul_mem_domain c hx⟩ =
      star c • D.pmap ⟨x, hx⟩ := by
  have hOriginal :
      ((x : H), D.pmap ⟨x, hx⟩) ∈ D.graphSubmodule := by
    rw [← D.pmap_graph_eq_submodule]
    exact LinearPMap.mem_graph D.pmap ⟨x, hx⟩
  have hScaled :
      (c • x, star c • D.pmap ⟨x, hx⟩) ∈ D.pmap.graph := by
    rw [D.pmap_graph_eq_submodule]
    exact D.complex_smul_mem c hOriginal
  have hCanonical :
      (c • x, D.pmap ⟨c • x, D.complex_smul_mem_domain c hx⟩) ∈ D.pmap.graph :=
    LinearPMap.mem_graph D.pmap
      ⟨c • x, D.complex_smul_mem_domain c hx⟩
  exact D.pmap.mem_graph_snd_inj hCanonical hScaled rfl

/-- The graph data canonically realizes the real-linear Tomita partial operator. -/
def realization : TomitaRealLinearPMapRealization T where
  pmap := D.pmap
  graph_eq := D.pmap_graph_eq
  domain_eq := D.pmap_domain_eq
  complex_smul_mem := fun c _ hx => D.complex_smul_mem_domain c hx
  map_complex_smul := fun c x hx => D.map_complex_smul c x hx

/-- The algebraic Tomita operator maps its domain back into its domain. -/
theorem map_mem_domain (x : D.pmap.domain) :
    D.pmap x ∈ D.pmap.domain := by
  rw [LinearPMap.mem_domain_iff]
  refine ⟨(x : H), ?_⟩
  have hxGraph : T.graph ((x : H), D.pmap x) := by
    rw [← D.pmap_graph_eq]
    exact LinearPMap.mem_graph D.pmap x
  have hFlip : T.graph (D.pmap x, (x : H)) := T.graph_flip hxGraph
  rw [D.pmap_graph_eq]
  exact hFlip

/-- On its algebraic domain, the constructed Tomita operator is involutive. -/
theorem map_map (x : D.pmap.domain) :
    D.pmap ⟨D.pmap x, D.map_mem_domain x⟩ = (x : H) := by
  have hCanonical :
      (D.pmap x, D.pmap ⟨D.pmap x, D.map_mem_domain x⟩) ∈ D.pmap.graph :=
    LinearPMap.mem_graph D.pmap ⟨D.pmap x, D.map_mem_domain x⟩
  have hxGraph : T.graph ((x : H), D.pmap x) := by
    rw [← D.pmap_graph_eq]
    exact LinearPMap.mem_graph D.pmap x
  have hFlip : (D.pmap x, (x : H)) ∈ D.pmap.graph := by
    rw [D.pmap_graph_eq]
    exact T.graph_flip hxGraph
  exact D.pmap.mem_graph_snd_inj hCanonical hFlip rfl

/-- The constructed real-linear partial operator is densely defined. -/
theorem pmap_dense_domain : Dense (D.pmap.domain : Set H) := by
  rw [D.pmap_domain_eq]
  exact T.domain_dense

/-- The constructed real-linear partial operator is closable in Mathlib. -/
theorem pmap_isClosable : D.pmap.IsClosable :=
  TomitaRealLinearPMapRealization.pmap_isClosable D.realization

/-- Its Mathlib closure is a closed densely defined real-linear operator. -/
theorem closure_isClosed : D.pmap.closure.IsClosed :=
  TomitaRealLinearPMapRealization.mathlib_closure_isClosed D.realization

/-- The Mathlib closure remains densely defined. -/
theorem closure_dense_domain :
    Dense (D.pmap.closure.domain : Set H) :=
  TomitaRealLinearPMapRealization.mathlib_closure_dense_domain D.realization

end TomitaRealGraphSubmoduleData
end
end KUOS.WORLD
