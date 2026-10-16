import KUOS.WORLD.TomitaClosedDomainEquivV0_57
import Mathlib.Algebra.Module.LinearMap.Star

/-!
The closed Tomita domain is stable under complex scalars. This file upgrades
that domain to a complex submodule and bundles the closed Tomita involution as
a conjugate-linear automorphism.
-/

namespace KUOS.WORLD

noncomputable section

open scoped ComplexConjugate

variable {A B H : Type*}
variable [NormedAddCommGroup H] [InnerProductSpace Complex H]
variable {T : TomitaGraphCore A B H}

namespace TomitaRealLinearPMapRealization

variable (R : TomitaRealLinearPMapRealization T)

/-- The domain of the closed Tomita operator as a complex submodule. -/
def closedComplexDomain : Submodule Complex H where
  carrier := R.pmap.closure.domain
  zero_mem' := R.pmap.closure.domain.zero_mem
  add_mem' := fun hx hy => R.pmap.closure.domain.add_mem hx hy
  smul_mem' := by
    intro c x hx
    exact R.closure_complex_smul_mem c ⟨x, hx⟩

@[simp]
theorem mem_closedComplexDomain {x : H} :
    x ∈ R.closedComplexDomain ↔ x ∈ R.pmap.closure.domain :=
  Iff.rfl

/-- Forget the complex-submodule packaging of the closed domain. -/
def closedComplexToReal
    (x : R.closedComplexDomain) : R.pmap.closure.domain :=
  ⟨x, x.property⟩

@[simp]
theorem closedComplexToReal_coe
    (x : R.closedComplexDomain) :
    ((R.closedComplexToReal x : R.pmap.closure.domain) : H) = (x : H) :=
  rfl

/-- The closed Tomita operator as a conjugate-linear endomorphism of its complex domain. -/
def closedDomainStarLinearMap :
    R.closedComplexDomain →ₗ⋆[Complex] R.closedComplexDomain where
  toFun x :=
    ⟨R.pmap.closure (R.closedComplexToReal x),
      R.mathlib_closure_map_mem_domain (R.closedComplexToReal x)⟩
  map_add' x y := by
    apply Subtype.ext
    change
      R.pmap.closure (R.closedComplexToReal (x + y)) =
        R.pmap.closure (R.closedComplexToReal x) +
          R.pmap.closure (R.closedComplexToReal y)
    simpa only [closedComplexToReal] using
      R.pmap.closure.map_add (R.closedComplexToReal x)
        (R.closedComplexToReal y)
  map_smul' c x := by
    apply Subtype.ext
    change
      R.pmap.closure (R.closedComplexToReal (c • x)) =
        starRingEnd Complex c •
          R.pmap.closure (R.closedComplexToReal x)
    simpa only [closedComplexToReal, starRingEnd_apply] using
      R.mathlib_closure_map_complex_smul c (R.closedComplexToReal x)

@[simp]
theorem closedDomainStarLinearMap_coe
    (x : R.closedComplexDomain) :
    ((R.closedDomainStarLinearMap x : R.closedComplexDomain) : H) =
      R.pmap.closure (R.closedComplexToReal x) :=
  rfl

/-- The closed conjugate-linear Tomita endomorphism is involutive. -/
theorem closedDomainStarLinearMap_involutive :
    Function.Involutive R.closedDomainStarLinearMap := by
  intro x
  apply Subtype.ext
  change
    R.pmap.closure
        ⟨R.pmap.closure (R.closedComplexToReal x),
          R.mathlib_closure_map_mem_domain (R.closedComplexToReal x)⟩ =
      (x : H)
  exact R.mathlib_closure_map_map (R.closedComplexToReal x)

/-- The closed Tomita operator as a conjugate-linear automorphism of its complex domain. -/
def closedDomainStarLinearEquiv :
    R.closedComplexDomain ≃ₗ⋆[Complex] R.closedComplexDomain :=
  LinearEquiv.ofInvolutive R.closedDomainStarLinearMap
    R.closedDomainStarLinearMap_involutive

@[simp]
theorem closedDomainStarLinearEquiv_apply_apply
    (x : R.closedComplexDomain) :
    R.closedDomainStarLinearEquiv (R.closedDomainStarLinearEquiv x) = x :=
  R.closedDomainStarLinearMap_involutive x

end TomitaRealLinearPMapRealization
end
end KUOS.WORLD
