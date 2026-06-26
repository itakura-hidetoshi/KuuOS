import KUOS.WORLD.TomitaClosedConjugateLinearBridgeV0_57

/-!
The algebraic Tomita graph is invariant under coordinate flip. This symmetry
survives topological closure, so the closed Tomita operator maps its domain to
itself and squares to the identity on that closed domain.
-/

namespace KUOS.WORLD

noncomputable section

open Filter Topology

variable {A B H : Type*}
variable [NormedAddCommGroup H] [InnerProductSpace Complex H]

namespace TomitaGraphCore

variable (T : TomitaGraphCore A B H)

/-- Coordinate-flip invariance of the algebraic graph survives closure. -/
theorem closure_graph_flip {x y : H}
    (hxy : (closure T.graph) (x, y)) :
    (closure T.graph) (y, x) := by
  obtain ⟨p, hp, hpLim⟩ := mem_closure_iff_seq_limit.mp hxy
  refine mem_closure_iff_seq_limit.mpr ?_
  refine ⟨(fun n => ((p n).2, (p n).1)), ?_, ?_⟩
  · intro n
    exact T.graph_flip (hp n)
  · have hfst : Tendsto (fun n => (p n).1) atTop (nhds x) :=
      (continuous_fst.tendsto (x, y)).comp hpLim
    have hsnd : Tendsto (fun n => (p n).2) atTop (nhds y) :=
      (continuous_snd.tendsto (x, y)).comp hpLim
    simpa only [nhds_prod_eq] using hsnd.prodMk hfst

end TomitaGraphCore

namespace TomitaRealLinearPMapRealization

variable {T : TomitaGraphCore A B H}
variable (R : TomitaRealLinearPMapRealization T)

/-- The closed Tomita operator maps its closed domain back into itself. -/
theorem mathlib_closure_map_mem_domain
    (x : R.pmap.closure.domain) :
    R.pmap.closure x ∈ R.pmap.closure.domain := by
  have hFlipSet :
      (closure T.graph) (R.pmap.closure x, (x : H)) :=
    T.closure_graph_flip (R.mathlib_closure_graph_mem_set_closure x)
  have hFlip :
      (R.pmap.closure x, (x : H)) ∈ R.pmap.closure.graph := by
    change
      (R.pmap.closure x, (x : H)) ∈
        (R.pmap.closure.graph : Set (H × H))
    rw [← R.set_graph_closure_eq_mathlib_closure_graph]
    exact hFlipSet
  exact LinearPMap.mem_domain_of_mem_graph hFlip

/-- The closed Tomita operator is involutive on its closed domain. -/
theorem mathlib_closure_map_map
    (x : R.pmap.closure.domain) :
    R.pmap.closure
        ⟨R.pmap.closure x, R.mathlib_closure_map_mem_domain x⟩ =
      (x : H) := by
  have hCanonical :
      (R.pmap.closure x,
          R.pmap.closure
            ⟨R.pmap.closure x, R.mathlib_closure_map_mem_domain x⟩) ∈
        R.pmap.closure.graph :=
    LinearPMap.mem_graph R.pmap.closure
      ⟨R.pmap.closure x, R.mathlib_closure_map_mem_domain x⟩
  have hFlipSet :
      (closure T.graph) (R.pmap.closure x, (x : H)) :=
    T.closure_graph_flip (R.mathlib_closure_graph_mem_set_closure x)
  have hFlip :
      (R.pmap.closure x, (x : H)) ∈ R.pmap.closure.graph := by
    change
      (R.pmap.closure x, (x : H)) ∈
        (R.pmap.closure.graph : Set (H × H))
    rw [← R.set_graph_closure_eq_mathlib_closure_graph]
    exact hFlipSet
  exact R.pmap.closure.mem_graph_snd_inj hCanonical hFlip rfl

/-- The closed Tomita operator is injective on its closed domain. -/
theorem mathlib_closure_injective :
    Function.Injective R.pmap.closure := by
  intro x y hxy
  let sx : R.pmap.closure.domain :=
    ⟨R.pmap.closure x, R.mathlib_closure_map_mem_domain x⟩
  let sy : R.pmap.closure.domain :=
    ⟨R.pmap.closure y, R.mathlib_closure_map_mem_domain y⟩
  have hsxy : sx = sy := by
    apply Subtype.ext
    exact hxy
  have hsecond : R.pmap.closure sx = R.pmap.closure sy :=
    congrArg R.pmap.closure hsxy
  apply Subtype.ext
  exact (R.mathlib_closure_map_map x).symm.trans
    (hsecond.trans (R.mathlib_closure_map_map y))

end TomitaRealLinearPMapRealization
end
end KUOS.WORLD
