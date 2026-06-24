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

@[simp]
theorem closedDomainLinearMap_coe
    (x : R.pmap.closure.domain) :
    ((R.closedDomainLinearMap x : R.pmap.closure.domain) : H) =
      R.pmap.closure x :=
  rfl

/-- The closed-domain endomorphism is involutive. -/
theorem closedDomainLinearMap_involutive :
    Function.Involutive R.closedDomainLinearMap := by
  intro x
  apply Subtype.ext
  change
    R.pmap.closure
        ⟨R.pmap.closure x, R.mathlib_closure_map_mem_domain x⟩ =
      (x : H)
  exact R.mathlib_closure_map_map x

end TomitaRealLinearPMapRealization
end
end KUOS.WORLD
