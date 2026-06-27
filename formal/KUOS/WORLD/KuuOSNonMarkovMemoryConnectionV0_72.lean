import Mathlib
import KUOS.WORLD.KuuOSNoncommutativeLeibnizConnectionV0_71

/-!
# KuuOS non-Markov memory connections v0.72

A read-only history is represented by a left module `H`.  A finite memory
kernel is an `A`-linear map from history into the current fiber.  Adding the
history term to a directional Leibniz connection preserves the pathwise
Leibniz law when the scalar acts on the current section and its history
simultaneously.
-/

namespace KUOS.WORLD.KuuOSNonMarkovMemoryConnectionV0_72

open KUOS.WORLD.KuuOSNoncommutativeLeibnizConnectionV0_71

variable {A M H : Type*}
variable [Ring A]
variable [AddCommGroup M] [Module A M]
variable [AddCommGroup H] [Module A H]

structure HistoricalConnection (δ : AlgebraDerivation A) where
  base : DirectionalConnection (M := M) δ
  memoryKernel : H →ₗ[A] M


def HistoricalConnection.apply
    {δ : AlgebraDerivation A}
    (connection : HistoricalConnection (M := M) (H := H) δ)
    (current : M)
    (history : H) : M :=
  connection.base current + connection.memoryKernel history


theorem historical_connection_satisfies_pathwise_leibniz
    (δ : AlgebraDerivation A)
    (connection : HistoricalConnection (M := M) (H := H) δ)
    (a : A)
    (current : M)
    (history : H) :
    connection.apply (a • current) (a • history) =
      δ a • current + a • connection.apply current history := by
  change
    connection.base (a • current) + connection.memoryKernel (a • history) =
      δ a • current +
        a • (connection.base current + connection.memoryKernel history)
  rw [connection.base.leibniz a current]
  rw [connection.memoryKernel.map_smul a history, smul_add]
  abel


def deformMemoryKernel
    {δ : AlgebraDerivation A}
    (connection : HistoricalConnection (M := M) (H := H) δ)
    (deltaKernel : H →ₗ[A] M) : HistoricalConnection (M := M) (H := H) δ where
  base := connection.base
  memoryKernel := connection.memoryKernel + deltaKernel


theorem memory_kernel_deformation_preserves_pathwise_leibniz
    (δ : AlgebraDerivation A)
    (connection : HistoricalConnection (M := M) (H := H) δ)
    (deltaKernel : H →ₗ[A] M)
    (a : A)
    (current : M)
    (history : H) :
    (deformMemoryKernel connection deltaKernel).apply
        (a • current) (a • history) =
      δ a • current +
        a • (deformMemoryKernel connection deltaKernel).apply current history := by
  exact historical_connection_satisfies_pathwise_leibniz
    δ (deformMemoryKernel connection deltaKernel) a current history


def memoryKernelDifference
    {δ : AlgebraDerivation A}
    (first second : HistoricalConnection (M := M) (H := H) δ) : H →ₗ[A] M :=
  first.memoryKernel - second.memoryKernel


theorem memory_kernel_difference_is_history_linear
    (δ : AlgebraDerivation A)
    (first second : HistoricalConnection (M := M) (H := H) δ)
    (a : A)
    (history : H) :
    memoryKernelDifference first second (a • history) =
      a • memoryKernelDifference first second history := by
  exact map_smul (memoryKernelDifference first second) a history


def PreservesHistoryFiltration
    (kernel : H →ₗ[A] M)
    (historyFiltration : ℕ → Submodule A H)
    (stateFiltration : ℕ → Submodule A M) : Prop :=
  ∀ p history, history ∈ historyFiltration p →
    kernel history ∈ stateFiltration p


theorem sum_memory_kernels_preserves_filtration
    (source deltaKernel : H →ₗ[A] M)
    (historyFiltration : ℕ → Submodule A H)
    (stateFiltration : ℕ → Submodule A M)
    (hSource : PreservesHistoryFiltration source historyFiltration stateFiltration)
    (hDelta : PreservesHistoryFiltration deltaKernel historyFiltration stateFiltration) :
    PreservesHistoryFiltration (source + deltaKernel)
      historyFiltration stateFiltration := by
  intro p history hHistory
  exact (stateFiltration p).add_mem
    (hSource p history hHistory)
    (hDelta p history hHistory)


def gaugeTransformMemoryKernel
    (stateGauge : M ≃ₗ[A] M)
    (historyGauge : H ≃ₗ[A] H)
    (kernel : H →ₗ[A] M) : H →ₗ[A] M :=
  stateGauge.toLinearMap.comp
    (kernel.comp historyGauge.symm.toLinearMap)


theorem gauge_transform_preserves_memory_kernel_linearity
    (stateGauge : M ≃ₗ[A] M)
    (historyGauge : H ≃ₗ[A] H)
    (kernel : H →ₗ[A] M)
    (a : A)
    (history : H) :
    gaugeTransformMemoryKernel stateGauge historyGauge kernel (a • history) =
      a • gaugeTransformMemoryKernel stateGauge historyGauge kernel history := by
  exact map_smul
    (gaugeTransformMemoryKernel stateGauge historyGauge kernel) a history


theorem rollback_memory_kernel_recovers_source
    (source deltaKernel : H →ₗ[A] M) :
    (source + deltaKernel) - deltaKernel = source := by
  ext history
  simp


structure HistoryCandidateReceipt where
  sourceHistoryUnchanged : Prop
  sourceKernelUnchanged : Prop
  candidateOnly : Prop
  liveEffectDenied : Prop
  stateWriteDenied : Prop
  authorityWideningDenied : Prop
  rollbackExact : Prop


structure HistoryCandidateReceipt.Valid
    (receipt : HistoryCandidateReceipt) : Prop where
  sourceHistoryUnchanged : receipt.sourceHistoryUnchanged
  sourceKernelUnchanged : receipt.sourceKernelUnchanged
  candidateOnly : receipt.candidateOnly
  liveEffectDenied : receipt.liveEffectDenied
  stateWriteDenied : receipt.stateWriteDenied
  authorityWideningDenied : receipt.authorityWideningDenied
  rollbackExact : receipt.rollbackExact


theorem valid_history_candidate_preserves_read_only_sources
    (receipt : HistoryCandidateReceipt)
    (h : receipt.Valid) :
    receipt.sourceHistoryUnchanged ∧
      receipt.sourceKernelUnchanged ∧
      receipt.candidateOnly ∧
      receipt.liveEffectDenied ∧
      receipt.stateWriteDenied ∧
      receipt.authorityWideningDenied ∧
      receipt.rollbackExact := by
  exact ⟨h.sourceHistoryUnchanged, h.sourceKernelUnchanged,
    h.candidateOnly, h.liveEffectDenied, h.stateWriteDenied,
    h.authorityWideningDenied, h.rollbackExact⟩

end KUOS.WORLD.KuuOSNonMarkovMemoryConnectionV0_72
