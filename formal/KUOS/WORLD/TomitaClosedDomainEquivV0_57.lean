import KUOS.WORLD.TomitaClosedInvolutionBridgeV0_57

namespace KUOS.WORLD

noncomputable section

variable {A B H : Type*}
variable [NormedAddCommGroup H] [InnerProductSpace Complex H]
variable {T : TomitaGraphCore A B H}

namespace TomitaRealLinearPMapRealization

variable (R : TomitaRealLinearPMapRealization T)

/-- The closed Tomita operator as a real-linear endomorphism of its own domain. -/
def closedDomainLinearMap :
    R.pmap.closure.domain →ₗ[Real] R.pmap.closure.domain :=
  LinearMap.codRestrict R.pmap.closure.domain R.pmap.closure.toFun
    (fun x => R.mathlib_closure_map_mem_domain x)

end TomitaRealLinearPMapRealization
end
end KUOS.WORLD
