import Mathlib
import KUOS.GaugeInvariantDependentOriginationDenseDescentV0_1

namespace KUOS.GaugeInvariantDependentOriginationOrbitQuotientV0_1

open Set Topology
open KUOS.GaugeInvariantDependentOriginationDenseDescentV0_1

universe u v w z

variable {X : Type u} {Y : Type v} {Gauge : Type w}
variable {Local : ℕ → Type z}

/-- Two representatives are gauge-related when one is obtained from the other
by a gauge/frame action.  This is the raw representative relation whose quotient
forgets the choice of gauge representative without forgetting semantic content. -/
def GaugeRelated [Group Gauge] [MulAction Gauge X] (x y : X) : Prop :=
  ∃ g : Gauge, g • x = y

/-- Gauge-relatedness is an equivalence relation for every group action. -/
def gaugeOrbitSetoid (Gauge : Type w) (X : Type u)
    [Group Gauge] [MulAction Gauge X] : Setoid X where
  r := GaugeRelated
  iseqv := by
    constructor
    · intro x
      exact ⟨1, by simp⟩
    · intro x y hxy
      rcases hxy with ⟨g, hgy⟩
      refine ⟨g⁻¹, ?_⟩
      rw [← hgy]
      simp
    · intro x y z hxy hyz
      rcases hxy with ⟨g, hgy⟩
      rcases hyz with ⟨h, hhz⟩
      refine ⟨h * g, ?_⟩
      calc
        (h * g) • x = h • (g • x) := by rw [mul_smul]
        _ = h • y := by rw [hgy]
        _ = z := hhz

/-- The semantic carrier with gauge representatives identified. -/
def GaugeOrbit (Gauge : Type w) (X : Type u)
    [Group Gauge] [MulAction Gauge X] : Type u :=
  Quotient (gaugeOrbitSetoid Gauge X)

/-- Canonical projection from raw representatives to their gauge orbit. -/
def orbitProjection (Gauge : Type w) (X : Type u)
    [Group Gauge] [MulAction Gauge X] (x : X) : GaugeOrbit Gauge X :=
  Quotient.mk (gaugeOrbitSetoid Gauge X) x

/-- A gauge-invariant semantic map descends canonically to the gauge-orbit
quotient.  This is the precise factorization form of `no privileged gauge
representative` at the semantic layer. -/
def descendSemantic [Group Gauge] [MulAction Gauge X]
    (semantic : X → Y)
    (hInvariant : ∀ (g : Gauge) (x : X), semantic (g • x) = semantic x) :
    GaugeOrbit Gauge X → Y :=
  Quotient.lift semantic (by
    intro x y hxy
    rcases hxy with ⟨g, hgy⟩
    rw [← hgy]
    exact (hInvariant g x).symm)

@[simp] theorem descendSemantic_orbitProjection
    [Group Gauge] [MulAction Gauge X]
    (semantic : X → Y)
    (hInvariant : ∀ (g : Gauge) (x : X), semantic (g • x) = semantic x)
    (x : X) :
    descendSemantic semantic hInvariant (orbitProjection Gauge X x) = semantic x :=
  rfl

/-- The descended semantic map is the unique map on gauge orbits whose pullback
along the orbit projection is the original invariant semantics. -/
theorem descendSemantic_unique
    [Group Gauge] [MulAction Gauge X]
    (semantic : X → Y)
    (hInvariant : ∀ (g : Gauge) (x : X), semantic (g • x) = semantic x)
    (candidate : GaugeOrbit Gauge X → Y)
    (hcandidate : ∀ x : X,
      candidate (orbitProjection Gauge X x) = semantic x) :
    candidate = descendSemantic semantic hInvariant := by
  funext q
  refine Quotient.inductionOn q ?_
  intro x
  change candidate (orbitProjection Gauge X x) =
    descendSemantic semantic hInvariant (orbitProjection Gauge X x)
  calc
    candidate (orbitProjection Gauge X x) = semantic x := hcandidate x
    _ = descendSemantic semantic hInvariant (orbitProjection Gauge X x) := by rfl

/-- Gauge invariance is equivalent to factorization through the orbit quotient.
This converts the slogan `meaning is invariant` into an exact universal-property
statement. -/
theorem semantic_factors_through_orbit_iff
    [Group Gauge] [MulAction Gauge X]
    (semantic : X → Y) :
    (∃ orbitSemantic : GaugeOrbit Gauge X → Y,
      ∀ x : X, orbitSemantic (orbitProjection Gauge X x) = semantic x) ↔
    (∀ (g : Gauge) (x : X), semantic (g • x) = semantic x) := by
  constructor
  · rintro ⟨orbitSemantic, horbit⟩ g x
    have hq : orbitProjection Gauge X x =
        orbitProjection Gauge X (g • x) :=
      Quotient.sound ⟨g, rfl⟩
    calc
      semantic (g • x) = orbitSemantic (orbitProjection Gauge X (g • x)) :=
        (horbit (g • x)).symm
      _ = orbitSemantic (orbitProjection Gauge X x) := congrArg orbitSemantic hq.symm
      _ = semantic x := horbit x
  · intro hInvariant
    exact ⟨descendSemantic semantic hInvariant, by intro x; rfl⟩

/-- Invariant semantics admit a unique orbit-level representative. -/
theorem existsUnique_orbitSemantic_of_invariant
    [Group Gauge] [MulAction Gauge X]
    (semantic : X → Y)
    (hInvariant : ∀ (g : Gauge) (x : X), semantic (g • x) = semantic x) :
    ∃! orbitSemantic : GaugeOrbit Gauge X → Y,
      ∀ x : X, orbitSemantic (orbitProjection Gauge X x) = semantic x := by
  refine ⟨descendSemantic semantic hInvariant, ?_, ?_⟩
  · intro x
    rfl
  · intro candidate hcandidate
    exact descendSemantic_unique semantic hInvariant candidate hcandidate

/-- Dense local dependent-origination descent not only generates global gauge
invariance; it therefore generates a unique semantic map on the gauge-orbit
quotient.  Global semantic extension existence is still an explicit input via
`semantic : ContinuousMap X Y`. -/
theorem dense_descent_existsUnique_orbitSemantic
    [Group Gauge] [MulAction Gauge X]
    [TopologicalSpace X] [TopologicalSpace Y] [T2Space Y]
    (realize : (n : ℕ) → Local n → X)
    (localAction : (n : ℕ) → Gauge → Local n → Local n)
    (semantic : ContinuousMap X Y)
    (hDense : Dense (realizationImageUnion realize))
    (hActionContinuous : ∀ g : Gauge, Continuous (fun x : X => g • x))
    (hEquivariant : ∀ (n : ℕ) (g : Gauge) (u : Local n),
      g • realize n u = realize n (localAction n g u))
    (hLocalInvariant : ∀ (n : ℕ) (g : Gauge) (u : Local n),
      semantic (realize n (localAction n g u)) = semantic (realize n u)) :
    ∃! orbitSemantic : GaugeOrbit Gauge X → Y,
      ∀ x : X, orbitSemantic (orbitProjection Gauge X x) = semantic x := by
  have hInvariant : ∀ (g : Gauge) (x : X), semantic (g • x) = semantic x :=
    semantic_invariant_of_dense_local_realization
      realize (fun g x => g • x) localAction semantic hDense
      hActionContinuous hEquivariant hLocalInvariant
  exact existsUnique_orbitSemantic_of_invariant semantic hInvariant

/-- Exact local readout plus dense descent yields both cross-scale compatibility
and a unique orbit-level global semantic map.  This packages dependent
origination as local compatibility + gauge quotient factorization without
promoting the quotient itself to an ultimate ontology. -/
theorem dense_descent_orbitSemantic_and_crossScaleCompatibility
    [Group Gauge] [MulAction Gauge X]
    [TopologicalSpace X] [TopologicalSpace Y] [T2Space Y]
    (realize : (n : ℕ) → Local n → X)
    (target : (n : ℕ) → Local n → Y)
    (localAction : (n : ℕ) → Gauge → Local n → Local n)
    (semantic : ContinuousMap X Y)
    (hDense : Dense (realizationImageUnion realize))
    (hActionContinuous : ∀ g : Gauge, Continuous (fun x : X => g • x))
    (hEquivariant : ∀ (n : ℕ) (g : Gauge) (u : Local n),
      g • realize n u = realize n (localAction n g u))
    (hreadout : ∀ (n : ℕ) (u : Local n),
      semantic (realize n u) = target n u)
    (hTargetInvariant : ∀ (n : ℕ) (g : Gauge) (u : Local n),
      target n (localAction n g u) = target n u) :
    (∃! orbitSemantic : GaugeOrbit Gauge X → Y,
      ∀ x : X, orbitSemantic (orbitProjection Gauge X x) = semantic x) ∧
      CrossScaleCompatible realize target := by
  have hpair := dense_descent_invariance_and_compatibility
    realize target (fun g x => g • x) localAction semantic hDense
    hActionContinuous hEquivariant hreadout hTargetInvariant
  constructor
  · exact existsUnique_orbitSemantic_of_invariant semantic hpair.1
  · exact hpair.2

end KUOS.GaugeInvariantDependentOriginationOrbitQuotientV0_1
