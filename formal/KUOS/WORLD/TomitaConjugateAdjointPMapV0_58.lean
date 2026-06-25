import KUOS.WORLD.TomitaConjugateAdjointGraphV0_58
import Mathlib.Analysis.InnerProductSpace.LinearPMap

/-!
The conjugate-adjoint relation of the closed Tomita operator is a real-linear,
single-valued graph.  Hence it canonically determines a partially defined
real-linear operator.  Its domain is exactly the relation domain, and the
operator obeys the expected conjugate scalar law.
-/

namespace KUOS.WORLD

noncomputable section

variable {A B H : Type*}
variable [NormedAddCommGroup H] [InnerProductSpace Complex H]
variable {T : TomitaGraphCore A B H}

namespace TomitaRealLinearPMapRealization

variable (R : TomitaRealLinearPMapRealization T)

/-- The conjugate-adjoint relation is closed under conjugate complex scaling. -/
theorem conjugateAdjointGraph_complex_smul
    (c : Complex) {y z : H}
    (hyz : R.conjugateAdjointGraph (y, z)) :
    R.conjugateAdjointGraph (c • y, star c • z) := by
  intro x
  change
    inner Complex (R.pmap.closure x) (c • y) =
      inner Complex (star c • z) (x : H)
  rw [inner_smul_right, inner_smul_left, star_star, hyz x]

/-- The conjugate-adjoint graph as a real submodule of the product carrier. -/
def conjugateAdjointGraphSubmodule : Submodule Real (H × H) where
  carrier := R.conjugateAdjointGraph
  zero_mem' := by
    intro x
    simp [conjugateAdjointGraph]
  add_mem' := by
    intro p q hp hq x
    change
      inner Complex (R.pmap.closure x) (p.1 + q.1) =
        inner Complex (p.2 + q.2) (x : H)
    rw [inner_add_right, inner_add_left, hp x, hq x]
  smul_mem' := by
    intro r p hp x
    change
      inner Complex (R.pmap.closure x) (r • p.1) =
        inner Complex (r • p.2) (x : H)
    rw [inner_smul_right_eq_smul, inner_smul_left_eq_smul, hp x]

/-- A vertical vector in the conjugate-adjoint graph must vanish. -/
theorem conjugateAdjointGraphSubmodule_vertical_unique {z : H}
    (hz : (0, z) ∈ R.conjugateAdjointGraphSubmodule) : z = 0 := by
  have hzero : (0, 0) ∈ R.conjugateAdjointGraphSubmodule :=
    R.conjugateAdjointGraphSubmodule.zero_mem
  exact R.conjugateAdjointGraph_right_unique hz hzero

/-- The partially defined conjugate adjoint of the closed Tomita operator. -/
def conjugateAdjointPMap : LinearPMap (RingHom.id Real) H H :=
  R.conjugateAdjointGraphSubmodule.toLinearPMap

/-- The graph of the constructed partial operator is the adjoint relation. -/
theorem conjugateAdjointPMap_graph_eq_submodule :
    R.conjugateAdjointPMap.graph = R.conjugateAdjointGraphSubmodule := by
  apply Submodule.toLinearPMap_graph_eq
  rintro ⟨y, z⟩ hyz hy
  simp only at hy
  subst y
  exact R.conjugateAdjointGraphSubmodule_vertical_unique hyz

/-- Set-level identification of the constructed graph with the adjoint relation. -/
theorem conjugateAdjointPMap_graph_eq :
    (R.conjugateAdjointPMap.graph : Set (H × H)) =
      R.conjugateAdjointGraph := by
  rw [R.conjugateAdjointPMap_graph_eq_submodule]
  rfl

/-- The partial-operator domain is exactly the conjugate-adjoint relation domain. -/
theorem conjugateAdjointPMap_domain_eq :
    (R.conjugateAdjointPMap.domain : Set H) =
      R.conjugateAdjointDomain := by
  ext y
  constructor
  · intro hy
    rcases (LinearPMap.mem_domain_iff (f := R.conjugateAdjointPMap)).mp hy with
      ⟨z, hyz⟩
    exact ⟨z, by
      rw [← R.conjugateAdjointPMap_graph_eq]
      exact hyz⟩
  · rintro ⟨z, hyz⟩
    apply (LinearPMap.mem_domain_iff (f := R.conjugateAdjointPMap)).mpr
    refine ⟨z, ?_⟩
    rw [R.conjugateAdjointPMap_graph_eq]
    exact hyz

/-- The conjugate-adjoint operator domain is closed under complex scalars. -/
theorem conjugateAdjointPMap_complex_smul_mem
    (c : Complex) {y : H}
    (hy : y ∈ R.conjugateAdjointPMap.domain) :
    c • y ∈ R.conjugateAdjointPMap.domain := by
  rcases (LinearPMap.mem_domain_iff (f := R.conjugateAdjointPMap)).mp hy with
    ⟨z, hyz⟩
  apply (LinearPMap.mem_domain_iff (f := R.conjugateAdjointPMap)).mpr
  refine ⟨star c • z, ?_⟩
  rw [R.conjugateAdjointPMap_graph_eq] at hyz ⊢
  exact R.conjugateAdjointGraph_complex_smul c hyz

/-- The constructed conjugate adjoint obeys the conjugate scalar law. -/
theorem conjugateAdjointPMap_map_complex_smul
    (c : Complex) (y : H)
    (hy : y ∈ R.conjugateAdjointPMap.domain) :
    R.conjugateAdjointPMap
        ⟨c • y, R.conjugateAdjointPMap_complex_smul_mem c hy⟩ =
      star c • R.conjugateAdjointPMap ⟨y, hy⟩ := by
  have hOriginal :
      (y, R.conjugateAdjointPMap ⟨y, hy⟩) ∈
        R.conjugateAdjointGraphSubmodule := by
    rw [← R.conjugateAdjointPMap_graph_eq_submodule]
    exact LinearPMap.mem_graph R.conjugateAdjointPMap ⟨y, hy⟩
  have hScaled :
      (c • y, star c • R.conjugateAdjointPMap ⟨y, hy⟩) ∈
        R.conjugateAdjointPMap.graph := by
    rw [R.conjugateAdjointPMap_graph_eq_submodule]
    exact R.conjugateAdjointGraph_complex_smul c hOriginal
  have hCanonical :
      (c • y,
          R.conjugateAdjointPMap
            ⟨c • y, R.conjugateAdjointPMap_complex_smul_mem c hy⟩) ∈
        R.conjugateAdjointPMap.graph :=
    LinearPMap.mem_graph R.conjugateAdjointPMap
      ⟨c • y, R.conjugateAdjointPMap_complex_smul_mem c hy⟩
  exact R.conjugateAdjointPMap.mem_graph_snd_inj
    hCanonical hScaled rfl

end TomitaRealLinearPMapRealization
end
end KUOS.WORLD
