import KUOS.WORLD.TomitaClosedInvolutionBridgeV0_57

/-!
The closed Tomita operator preserves its closed domain and is involutive there.
This file bundles that result as a real-linear automorphism of the closed
operator domain.
-/

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

/-- The closed Tomita operator as a real-linear automorphism of its domain. -/
def closedDomainLinearEquiv :
    R.pmap.closure.domain ≃ₗ[Real] R.pmap.closure.domain :=
  LinearEquiv.ofInvolutive R.closedDomainLinearMap
    R.closedDomainLinearMap_involutive

@[simp]
theorem closedDomainLinearEquiv_apply
    (x : R.pmap.closure.domain) :
    R.closedDomainLinearEquiv x = R.closedDomainLinearMap x :=
  rfl

/-- Applying the closed-domain Tomita automorphism twice is the identity. -/
@[simp]
theorem closedDomainLinearEquiv_apply_apply
    (x : R.pmap.closure.domain) :
    R.closedDomainLinearEquiv (R.closedDomainLinearEquiv x) = x :=
  R.closedDomainLinearMap_involutive x

/-- The closed-domain Tomita automorphism is bijective. -/
theorem closedDomainLinearEquiv_bijective :
    Function.Bijective R.closedDomainLinearEquiv :=
  R.closedDomainLinearEquiv.bijective

/-- The inverse of the closed-domain Tomita automorphism is itself. -/
@[simp]
theorem closedDomainLinearEquiv_symm_apply
    (x : R.pmap.closure.domain) :
    R.closedDomainLinearEquiv.symm x = R.closedDomainLinearEquiv x := by
  apply (R.closedDomainLinearEquiv.symm_apply_eq).2
  exact (R.closedDomainLinearEquiv_apply_apply x).symm

end TomitaRealLinearPMapRealization
end
end KUOS.WORLD
