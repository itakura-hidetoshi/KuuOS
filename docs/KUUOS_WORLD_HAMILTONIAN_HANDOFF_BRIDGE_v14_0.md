# KuuOS v14.0 — Hamiltonian Handoff Bridge

## 1. 目的

この文書は、`itakura-hidetoshi/4d-mass-gap` の Hamiltonian 関連 Lean surface を、KuuOS v14.0 Causal WorldModel OS に proof-state input として接続する。

この bridge は、Hilbert-space handoff の次段として、operator / Hamiltonian layer が WORLD モデル内で追跡できるようにする。

接続対象は、Hamiltonian label、spectral witness link、operator normalization、vacuum-orthogonal closed Hamiltonian API、Rayleigh lower-bound API である。

ただし、WORLD モデル内の Hamiltonian 状態は、外部世界の事実認定でも、独立外部査読済みの物理的最終定理でもない。

## 2. Source surfaces

```text
repository: itakura-hidetoshi/4d-mass-gap
carrier branch: formal/real-hilbert-uniform-coercive-strong-limit
```

Hamiltonian label の最小 carrier は次である。

```text
MGAP4D.Hamiltonian.Basic
HamiltonianLabel
Hphys = { name := "H_phys" }
```

Hamiltonian label と spectral gap witness の接続は次である。

```text
MGAP4D.Hamiltonian.Physical
PhysicalGapRecord
physicalGap3320Record
physicalGap3320_value
```

operator-scale normalization の surface は次である。

```text
PhysicalHamiltonianOperatorNormalizationData
physicalHamiltonianOperatorNormalizationData
PhysicalHamiltonianOperatorNormalizationData.ready
physical_hamiltonian_operator_normalization_ready
physical_hamiltonian_operator_normalized_scale_def
physical_hamiltonian_operator_scale_reconstruction
physical_hamiltonian_operator_normalized_gap_eq_exact
physical_hamiltonian_operator_dimensional_gap_eq_reference_mul_exact
physical_hamiltonian_operator_internal_dimensional_gap_eq_exact
```

vacuum-orthogonal excitation sector の closed Hamiltonian API は次である。

```text
vacuumOrthogonalClosedRightHamiltonianLinearMap
vacuumOrthogonalClosedRightHamiltonian
vacuumOrthogonalClosedRightHamiltonian_isFormalAdjoint
FiniteVolumeVacuumGapTransfer.vacuumOrthogonalClosedRightHamiltonian_gap
FiniteVolumeVacuumGapTransfer.vacuumOrthogonalClosedRightHamiltonian_eq_zero_of_eigenvalue_lt_mass
```

## 3. WORLD variables

KuuOS WORLD モデルに追加する標準変数は次である。

```text
HamiltonianLabelAPI = present
HPhysLabel = H_phys
HamiltonianSpectralWitnessLink = present
HamiltonianOperatorNormalizationAPI = present
VacuumOrthogonalClosedHamiltonianAPI = conditional-present
HamiltonianRayleighLowerBoundAPI = conditional-present
HamiltonianSelfAdjointnessBoundary = conditional-on-formal-adjoint-input
HamiltonianSpectralGapBoundary = witness-surface-not-external-consensus
```

`HamiltonianLabelAPI` と `HPhysLabel` は、operator layer が Hamiltonian object を WORLD モデル上で参照するための名前付き entry point である。

`HamiltonianSpectralWitnessLink` は、Hamiltonian label と normalized spectral witness の接続を示す。

`HamiltonianOperatorNormalizationAPI` は、`H_norm = E0^{-1} * H_phys` と `H_phys = E0 * H_norm` の normalization boundary を追跡する。

`VacuumOrthogonalClosedHamiltonianAPI` と `HamiltonianRayleighLowerBoundAPI` は、OS excitation sector 上の closed Hamiltonian と Rayleigh lower bound を記録する。

これらは、必要な仮定と入力を消さない conditional-present state として扱う。

## 4. Protected boundaries

次の変数は protected variables として扱う。

```text
HamiltonianSelfAdjointnessBoundary
HamiltonianSpectralGapBoundary
PhysicalMassGapClaimBoundary
```

これらは通常の observation / intervention による上書きを拒否する。

## 5. Non-claim invariants

この bridge は、次の非同一性を保持する。

```text
Hamiltonian label != constructed external physical Hamiltonian acceptance
formal-adjoint / symmetric input != unconditional self-adjointness theorem
normalized spectral witness != dimensional physical gap without E0
WORLD-model Hamiltonian state != external mathematical consensus
WORLD-model state != Clay-style public final theorem acceptance
```

## 6. Operational mapping

Causal WorldModel OS v14.0 では、Hamiltonian bridge は次のように対応する。

```text
initialize:
  HamiltonianLabelAPI
  HPhysLabel
  HamiltonianSpectralWitnessLink
  HamiltonianOperatorNormalizationAPI
  VacuumOrthogonalClosedHamiltonianAPI
  HamiltonianRayleighLowerBoundAPI
  HamiltonianSelfAdjointnessBoundary
  HamiltonianSpectralGapBoundary
  PhysicalMassGapClaimBoundary

inspect:
  current Hamiltonian proof-state variables and boundary variables

counterfactual:
  downstream spectral/operator readiness scenarios without mutating persistent state

observe / intervene:
  licensed internal WORLD-model updates only
```

この mapping は KuuOS 側の内部 WORLD 状態を更新するだけであり、4d-mass-gap 側の Lean artifact を変更しない。

## 7. Normalization boundary

normalized Hamiltonian convention は次である。

```text
H_norm = E0^{-1} * H_phys
H_phys = E0 * H_norm
Delta_norm = exactGapValueReal
Delta_phys(E0) = E0 * Delta_norm
```

内部正規化では `E0 = 1` を使えるが、次元付きの物理解釈には外部 reference energy scale `E0` が必要である。

## 8. Non-claim

この bridge は Hamiltonian 関連 surface を KuuOS WORLD model に接続する。

この bridge は、独立外部査読済みの物理的 self-adjoint Hamiltonian、次元付き Hamiltonian spectral gap、または Clay Millennium 問題の公的最終受理を主張しない。
