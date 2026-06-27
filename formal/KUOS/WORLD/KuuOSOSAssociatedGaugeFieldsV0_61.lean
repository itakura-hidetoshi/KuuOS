import KUOS.WORLD.KuuOSGaugeFieldSelfOrganizationV0_60

/-!
# KuuOS OS-associated gauge fields v0.61

ObserveOS, VerifyOS, and MemoryOS are treated as local associated fields.
Their covariant residuals split into invariant semantic channels, while the
closed Observe-Verify-Memory transport defines memory holonomy.
-/

namespace KUOS.WORLD.KuuOSOSAssociatedGaugeFieldsV0_61

open KUOS.WORLD.KuuOSGaugeFieldSelfOrganizationV0_60

inductive OSRole where
  | observe
  | verify
  | memory
  deriving DecidableEq, Repr

variable {X G V R : Type*} [Group G] [AddGroup V] [DistribMulAction G V]

def covariantResidual
    (A : GaugeConnection X G)
    (φ : GaugeField X V)
    (x y : X) : V :=
  A x y • φ x - φ y

theorem gaugeTransform_covariantResidual
    (h : X → G)
    (A : GaugeConnection X G)
    (φ : GaugeField X V)
    (x y : X) :
    covariantResidual (gaugeTransformConnection h A)
        (gaugeTransformField h φ) x y =
      h y • covariantResidual A φ x y := by
  simp only [covariantResidual]
  rw [gaugeTransform_transport_covariant]
  change h y • (A x y • φ x) - h y • φ y =
    h y • (A x y • φ x - φ y)
  exact (smul_sub (h y) (A x y • φ x) (φ y)).symm

def IsGaugeInvariantChannel (E : V → R) : Prop :=
  ∀ g v, E (g • v) = E v

theorem channelCurvature_gauge_invariant
    (E : V → R)
    (hE : IsGaugeInvariantChannel E)
    (h : X → G)
    (A : GaugeConnection X G)
    (φ : GaugeField X V)
    (x y : X) :
    E (covariantResidual (gaugeTransformConnection h A)
        (gaugeTransformField h φ) x y) =
      E (covariantResidual A φ x y) := by
  rw [gaugeTransform_covariantResidual]
  exact hE (h y) (covariantResidual A φ x y)

structure OSChannelObservables (V R : Type*) where
  epistemic : V → R
  verification : V → R
  memory : V → R

structure OSChannelObservables.Invariant
    (channels : OSChannelObservables V R) : Prop where
  epistemic : IsGaugeInvariantChannel channels.epistemic
  verification : IsGaugeInvariantChannel channels.verification
  memory : IsGaugeInvariantChannel channels.memory

def splitOSCurvature
    (channels : OSChannelObservables V R)
    (A : GaugeConnection X G)
    (observe verify memory : GaugeField X V)
    (xObserve xVerify xMemory : X) : R × R × R :=
  (channels.epistemic (covariantResidual A observe xObserve xVerify),
    channels.verification (covariantResidual A verify xVerify xMemory),
    channels.memory (covariantResidual A memory xMemory xObserve))

theorem splitOSCurvature_gauge_invariant
    (channels : OSChannelObservables V R)
    (hchannels : channels.Invariant)
    (h : X → G)
    (A : GaugeConnection X G)
    (observe verify memory : GaugeField X V)
    (xObserve xVerify xMemory : X) :
    splitOSCurvature channels (gaugeTransformConnection h A)
        (gaugeTransformField h observe)
        (gaugeTransformField h verify)
        (gaugeTransformField h memory)
        xObserve xVerify xMemory =
      splitOSCurvature channels A observe verify memory
        xObserve xVerify xMemory := by
  simp only [splitOSCurvature]
  apply Prod.ext
  · exact channelCurvature_gauge_invariant
      channels.epistemic hchannels.epistemic h A observe xObserve xVerify
  · apply Prod.ext
    · exact channelCurvature_gauge_invariant
        channels.verification hchannels.verification h A verify xVerify xMemory
    · exact channelCurvature_gauge_invariant
        channels.memory hchannels.memory h A memory xMemory xObserve

def memoryTriangleHolonomy
    (A : GaugeConnection X G)
    (xObserve xVerify xMemory : X) : G :=
  A xMemory xObserve * A xVerify xMemory * A xObserve xVerify

theorem gaugeTransform_memoryTriangleHolonomy
    (h : X → G)
    (A : GaugeConnection X G)
    (xObserve xVerify xMemory : X) :
    memoryTriangleHolonomy (gaugeTransformConnection h A)
        xObserve xVerify xMemory =
      h xObserve * memoryTriangleHolonomy A xObserve xVerify xMemory *
        (h xObserve)⁻¹ := by
  simp only [memoryTriangleHolonomy, gaugeTransformConnection]
  group

theorem memoryHolonomyObservable_gauge_invariant
    (W : G → R)
    (hW : IsClassFunction W)
    (h : X → G)
    (A : GaugeConnection X G)
    (xObserve xVerify xMemory : X) :
    W (memoryTriangleHolonomy (gaugeTransformConnection h A)
        xObserve xVerify xMemory) =
      W (memoryTriangleHolonomy A xObserve xVerify xMemory) := by
  rw [gaugeTransform_memoryTriangleHolonomy]
  exact hW (h xObserve) (memoryTriangleHolonomy A xObserve xVerify xMemory)

end KUOS.WORLD.KuuOSOSAssociatedGaugeFieldsV0_61
