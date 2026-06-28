import KUOS.WORLD.TomitaConjugateAdjointPMapV0_58
import Mathlib.Analysis.InnerProductSpace.Continuous

namespace KUOS.WORLD

noncomputable section

variable {A B H : Type*}
variable [NormedAddCommGroup H] [InnerProductSpace Complex H]
variable [IsScalarTower Real Complex H]
variable {T : TomitaGraphCore A B H}

namespace TomitaRealLinearPMapRealization

variable (R : TomitaRealLinearPMapRealization T)

def conjugateAdjointConstraint
    (x : R.pmap.closure.domain) : Set (H × H) :=
  {p | inner Complex (R.pmap.closure x) p.1 = inner Complex p.2 (x : H)}

omit [IsScalarTower Real Complex H] in
theorem conjugateAdjointConstraint_isClosed
    (x : R.pmap.closure.domain) :
    IsClosed (R.conjugateAdjointConstraint x) := by
  apply isClosed_eq
  · exact continuous_const.inner continuous_fst
  · exact continuous_snd.inner continuous_const

omit [IsScalarTower Real Complex H] in
theorem conjugateAdjointGraph_eq_iInter :
    R.conjugateAdjointGraph =
      ⋂ x : R.pmap.closure.domain, R.conjugateAdjointConstraint x := by
  ext p
  constructor
  · intro hp x
    exact hp x
  · intro hp x
    exact Set.mem_iInter.mp hp x

theorem conjugateAdjointGraph_isClosed :
    IsClosed R.conjugateAdjointGraph := by
  rw [R.conjugateAdjointGraph_eq_iInter]
  exact isClosed_iInter fun x => R.conjugateAdjointConstraint_isClosed x

theorem conjugateAdjointPMap_isClosed :
    R.conjugateAdjointPMap.IsClosed := by
  change IsClosed (R.conjugateAdjointPMap.graph : Set (H × H))
  rw [R.conjugateAdjointPMap_graph_eq]
  exact R.conjugateAdjointGraph_isClosed

end TomitaRealLinearPMapRealization
end
end KUOS.WORLD
