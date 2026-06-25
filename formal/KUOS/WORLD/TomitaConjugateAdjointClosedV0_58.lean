import KUOS.WORLD.TomitaConjugateAdjointPMapV0_58
import Mathlib.Analysis.InnerProductSpace.Continuous

/-!
The conjugate-adjoint graph is an intersection of closed inner-product
constraints. Hence the partially defined conjugate adjoint is a closed
real-linear operator. No density statement about its domain is used here.
-/

namespace KUOS.WORLD

noncomputable section

variable {A B H : Type*}
variable [NormedAddCommGroup H] [InnerProductSpace Complex H]
variable [IsScalarTower Real Complex H]
variable {T : TomitaGraphCore A B H}

namespace TomitaRealLinearPMapRealization

variable (R : TomitaRealLinearPMapRealization T)

/-- The closed constraint corresponding to one vector in the Tomita domain. -/
def conjugateAdjointConstraint
    (x : R.pmap.closure.domain) : Set (H × H) :=
  {p | inner Complex (R.pmap.closure x) p.1 = inner Complex p.2 (x : H)}

/-- Each defining inner-product constraint is closed. -/
theorem conjugateAdjointConstraint_isClosed
    (x : R.pmap.closure.domain) :
    IsClosed (R.conjugateAdjointConstraint x) := by
  apply isClosed_eq
  · exact continuous_const.inner continuous_fst
  · exact continuous_snd.inner continuous_const

/-- The conjugate-adjoint graph is the intersection of all pairing constraints. -/
theorem conjugateAdjointGraph_eq_iInter :
    R.conjugateAdjointGraph =
      ⋂ x : R.pmap.closure.domain, R.conjugateAdjointConstraint x := by
  ext p
  simp only [conjugateAdjointGraph, conjugateAdjointConstraint,
    Set.mem_iInter, Set.mem_setOf_eq]

/-- The conjugate-adjoint graph is closed in the product Hilbert carrier. -/
theorem conjugateAdjointGraph_isClosed :
    IsClosed R.conjugateAdjointGraph := by
  rw [R.conjugateAdjointGraph_eq_iInter]
  exact isClosed_iInter fun x => R.conjugateAdjointConstraint_isClosed x

/-- The constructed conjugate-adjoint partial operator is closed. -/
theorem conjugateAdjointPMap_isClosed :
    R.conjugateAdjointPMap.IsClosed := by
  change IsClosed (R.conjugateAdjointPMap.graph : Set (H × H))
  rw [R.conjugateAdjointPMap_graph_eq]
  exact R.conjugateAdjointGraph_isClosed

end TomitaRealLinearPMapRealization
end
end KUOS.WORLD
