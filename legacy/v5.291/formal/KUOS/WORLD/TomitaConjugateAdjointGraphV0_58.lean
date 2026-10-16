import KUOS.WORLD.TomitaClosedComplexDomainV0_57

/-!
The first adjoint layer for the closed Tomita operator.

For a densely defined conjugate-linear operator `S`, its conjugate adjoint
relation is characterized by

  inner (S x) y = inner z x

for every `x` in the domain of `S`.  This module defines that relation for the
closed v0.57 Tomita operator and proves that the adjoint value `z` is unique.
It does not assert existence or density of the adjoint domain.
-/

namespace KUOS.WORLD

noncomputable section

variable {A B H : Type*}
variable [NormedAddCommGroup H] [InnerProductSpace Complex H]
variable {T : TomitaGraphCore A B H}

namespace TomitaRealLinearPMapRealization

variable (R : TomitaRealLinearPMapRealization T)

/-- The inclusion of the closed Tomita domain into the Hilbert carrier. -/
def closedDomainInclusion : R.pmap.closure.domain -> H :=
  fun x => (x : H)

/-- The closed Tomita domain inclusion has dense range. -/
theorem closedDomainInclusion_denseRange :
    DenseRange R.closedDomainInclusion := by
  change Dense (Set.range R.closedDomainInclusion)
  have hrange :
      Set.range R.closedDomainInclusion = (R.pmap.closure.domain : Set H) := by
    ext x
    constructor
    · rintro ⟨y, rfl⟩
      exact y.property
    · intro hx
      exact ⟨⟨x, hx⟩, rfl⟩
  rw [hrange]
  exact R.mathlib_closure_dense_domain

/--
The conjugate-adjoint graph relation of the closed Tomita operator.

A pair `(y,z)` belongs to this relation when
`inner (S x) y = inner z x` for every `x` in the closed Tomita domain.
-/
def conjugateAdjointGraph : Set (H × H) :=
  fun p => forall x : R.pmap.closure.domain,
    inner Complex (R.pmap.closure x) p.1 = inner Complex p.2 (x : H)

/-- A conjugate-adjoint graph point satisfies its defining pairing. -/
theorem conjugateAdjointGraph_pairing {y z : H}
    (hyz : R.conjugateAdjointGraph (y, z))
    (x : R.pmap.closure.domain) :
    inner Complex (R.pmap.closure x) y = inner Complex z (x : H) :=
  hyz x

/-- Density of the closed Tomita domain makes the adjoint value unique. -/
theorem conjugateAdjointGraph_right_unique {y z1 z2 : H}
    (h1 : R.conjugateAdjointGraph (y, z1))
    (h2 : R.conjugateAdjointGraph (y, z2)) :
    z1 = z2 := by
  apply sub_eq_zero.mp
  apply R.closedDomainInclusion_denseRange.eq_zero_of_inner_left Complex
  intro x
  rw [inner_sub_left]
  apply sub_eq_zero.mpr
  exact (h1 x).symm.trans (h2 x)

/-- The domain of the conjugate adjoint relation. -/
def conjugateAdjointDomain : Set H :=
  fun y => Exists fun z => R.conjugateAdjointGraph (y, z)

/-- The unique conjugate-adjoint value selected on its domain. -/
def conjugateAdjointValue
    (y : H) (hy : R.conjugateAdjointDomain y) : H :=
  Classical.choose hy

/-- The selected value belongs to the conjugate-adjoint graph. -/
theorem conjugateAdjointValue_mem_graph
    (y : H) (hy : R.conjugateAdjointDomain y) :
    R.conjugateAdjointGraph (y, R.conjugateAdjointValue y hy) :=
  Classical.choose_spec hy

/-- Every conjugate-adjoint graph value equals the selected value. -/
theorem conjugateAdjointValue_unique
    (y z : H) (hy : R.conjugateAdjointDomain y)
    (hyz : R.conjugateAdjointGraph (y, z)) :
    z = R.conjugateAdjointValue y hy := by
  exact R.conjugateAdjointGraph_right_unique hyz
    (R.conjugateAdjointValue_mem_graph y hy)

end TomitaRealLinearPMapRealization
end
end KUOS.WORLD
