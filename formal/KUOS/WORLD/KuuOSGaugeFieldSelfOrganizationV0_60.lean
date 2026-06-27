import Mathlib

/-!
# KuuOS gauge-field self-organization v0.60

Context-local OS states are sections, transport is a connection, local
implementation changes are gauge transformations, and plaquette holonomy
changes only by conjugation.
-/

namespace KUOS.WORLD.KuuOSGaugeFieldSelfOrganizationV0_60

variable {X G V R : Type*} [Group G] [MulAction G V]

abbrev GaugeConnection (X G : Type*) := X → X → G
abbrev GaugeField (X V : Type*) := X → V

def gaugeTransformConnection
    (h : X → G)
    (A : GaugeConnection X G) : GaugeConnection X G :=
  fun x y => h y * A x y * (h x)⁻¹

def gaugeTransformField
    (h : X → G)
    (φ : GaugeField X V) : GaugeField X V :=
  fun x => h x • φ x

def plaquetteHolonomy
    (A : GaugeConnection X G)
    (x₀ x₁ x₂ x₃ : X) : G :=
  A x₃ x₀ * A x₂ x₃ * A x₁ x₂ * A x₀ x₁

theorem gaugeTransform_transport_covariant
    (h : X → G)
    (A : GaugeConnection X G)
    (φ : GaugeField X V)
    (x y : X) :
    gaugeTransformConnection h A x y • gaugeTransformField h φ x =
      h y • (A x y • φ x) := by
  simp [gaugeTransformConnection, gaugeTransformField, smul_smul, mul_assoc]

theorem gaugeTransform_plaquetteHolonomy
    (h : X → G)
    (A : GaugeConnection X G)
    (x₀ x₁ x₂ x₃ : X) :
    plaquetteHolonomy (gaugeTransformConnection h A) x₀ x₁ x₂ x₃ =
      h x₀ * plaquetteHolonomy A x₀ x₁ x₂ x₃ * (h x₀)⁻¹ := by
  simp only [gaugeTransformConnection, plaquetteHolonomy]
  group

def IsClassFunction (W : G → R) : Prop :=
  ∀ g u, W (g * u * g⁻¹) = W u

theorem wilson_observable_gauge_invariant
    (W : G → R)
    (hW : IsClassFunction W)
    (h : X → G)
    (A : GaugeConnection X G)
    (x₀ x₁ x₂ x₃ : X) :
    W (plaquetteHolonomy (gaugeTransformConnection h A) x₀ x₁ x₂ x₃) =
      W (plaquetteHolonomy A x₀ x₁ x₂ x₃) := by
  rw [gaugeTransform_plaquetteHolonomy]
  exact hW (h x₀) (plaquetteHolonomy A x₀ x₁ x₂ x₃)

def IsConstitutionalInvariant
    (G : Type*) [SMul G V]
    (P : V → Prop) : Prop :=
  ∀ (g : G) v, P (g • v) ↔ P v

theorem constitutional_state_preserved
    (P : V → Prop)
    (hP : IsConstitutionalInvariant G P)
    (g : G)
    (v : V)
    (hv : P v) :
    P (g • v) := by
  exact (hP g v).2 hv

structure ImprovementCandidate where
  sourceAction : ℝ
  candidateAction : ℝ
  chartDomainPreserved : Prop
  fieldIdentityPreserved : Prop
  connectionPreserved : Prop
  plaquetteDomainPreserved : Prop
  protectedStatePreserved : Prop
  ownershipPreserved : Prop
  authorityPreserved : Prop
  rollbackBound : Prop

structure ImprovementCandidate.Admissible (c : ImprovementCandidate) : Prop where
  actionNonincreasing : c.candidateAction ≤ c.sourceAction
  chartDomainPreserved : c.chartDomainPreserved
  fieldIdentityPreserved : c.fieldIdentityPreserved
  connectionPreserved : c.connectionPreserved
  plaquetteDomainPreserved : c.plaquetteDomainPreserved
  protectedStatePreserved : c.protectedStatePreserved
  ownershipPreserved : c.ownershipPreserved
  authorityPreserved : c.authorityPreserved
  rollbackBound : c.rollbackBound

theorem admissible_candidate_preserves_authority
    (c : ImprovementCandidate)
    (hc : c.Admissible) :
    c.authorityPreserved :=
  hc.authorityPreserved

theorem gauge_self_organization_boundary
    (c : ImprovementCandidate)
    (hc : c.Admissible) :
    c.candidateAction ≤ c.sourceAction ∧
      c.chartDomainPreserved ∧
      c.fieldIdentityPreserved ∧
      c.connectionPreserved ∧
      c.plaquetteDomainPreserved ∧
      c.protectedStatePreserved ∧
      c.ownershipPreserved ∧
      c.authorityPreserved ∧
      c.rollbackBound := by
  exact ⟨hc.actionNonincreasing,
    hc.chartDomainPreserved,
    hc.fieldIdentityPreserved,
    hc.connectionPreserved,
    hc.plaquetteDomainPreserved,
    hc.protectedStatePreserved,
    hc.ownershipPreserved,
    hc.authorityPreserved,
    hc.rollbackBound⟩

end KUOS.WORLD.KuuOSGaugeFieldSelfOrganizationV0_60
