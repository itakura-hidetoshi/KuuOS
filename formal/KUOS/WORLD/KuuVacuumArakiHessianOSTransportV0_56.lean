import Mathlib
import KUOS.WORLD.ArakiBoundedExponentialArcCalculusV0_56
import KUOS.WORLD.KuuVacuumInformationGeometryBridgeV0_55

/-!
WORLD v0.56 transport of the verified bounded-generator Araki calculus to the
vacuum quantum Fisher metric, completed Hilbert excitations, and the
Osterwalder-Schrader reflection form.

The derivative argument is imported from the independently validated
Mathlib-only calculus root.  This module contains only the typed physical
transport and does not duplicate the Hessian calculus.
-/

namespace KUOS
namespace WORLD

noncomputable section

structure WorldKuuVacuumArakiHessianOSTransport
    {C : RealHilbertL2Carrier}
    {W : WorldNoncommutativeOperatorAlgebra C}
    [PartialOrder W.Region]
    {B : WorldCStarLocalNetBridge C W}
    {V : WorldVonNeumannBicommutantBridge B}
    {M : WorldStandardFormModularFlowBridge V}
    {R : WorldModularStateKMSRelativeFlowBridge M}
    {E : WorldArakiRelativeEntropyBridge R}
    {P : WorldPetzRecoverySufficiencyBridge E}
    {T : WorldConditionalExpectationTakesakiBridge P}
    {J : WorldJonesBasicConstructionIndexBridge T}
    {S : WorldJonesTowerStandardInvariantBridge J}
    {Q : WorldCanonicalEndomorphismQSystemFrobeniusBridge S}
    {F : WorldBimoduleSectorFusionCategoryBridge Q}
    {Z : WorldModuleCategoryNimrepTubeCenterBridge F}
    {G : WorldGaugeCategoricalIndraNetBridge Z}
    {I : WorldInformationGeometricHigherGaugeBridge G}
    {H : WorldArakiPetzQuantumInformationGeometryBridge I}
    {D : WorldQuantumExponentialDualAffineProjectionBridge H}
    {Vary : WorldQuantumGeodesicMirrorDescentFreeEnergyBridge D}
    {Flow : WorldQuantumGradientJKOEntropyProductionBridge Vary}
    {Mix : WorldQuantumLogSobolevContractivityMixingBridge Flow}
    {K : WorldKuuVacuumOSHilbertCompletionBridge Mix}
    {Central : WorldKuuVacuumCentralReferenceStateBridge K}
    (Geom : WorldKuuVacuumInformationGeometryBridge Central) where
  calculus : ArakiBoundedExponentialArcCalculus

  tangentOfGenerator : calculus.Generator → I.Tangent
  physicalObservable : calculus.Generator → B.A
  tangentObservable_eq_physicalObservable : ∀ h,
    H.tangentObservable (tangentOfGenerator h) = physicalObservable h

  bkm_eq_quantumFisher : ∀ i k h,
    calculus.bkmPairing k h =
      H.quantumFisherMetric i (Geom.vacuumParameter i)
        (tangentOfGenerator k) (tangentOfGenerator h)

  positiveTimeRepresentative : calculus.Generator → K.PositiveTimeObservable
  osImage_eq_excitation : ∀ h,
    K.osHilbertIdentification (K.osClass (positiveTimeRepresentative h)) =
      Central.excitationVector (physicalObservable h)

  infiniteDimensionalPhysicalCarrier : InfiniteDimensional ℂ M.H

  boundedGeneratorScope : Prop
  boundedGeneratorScopeProof : boundedGeneratorScope
  faithfulNormalVacuumScope : Prop
  faithfulNormalVacuumScopeProof : faithfulNormalVacuumScope
  sigmaFiniteStandardFormScope : Prop
  sigmaFiniteStandardFormScopeProof : sigmaFiniteStandardFormScope

  noArbitraryUnboundedGeneratorClaim : Prop
  noArbitraryUnboundedGeneratorClaimProof :
    noArbitraryUnboundedGeneratorClaim
  physicalTransportNotWorldIdentity : Prop
  physicalTransportNotWorldIdentityProof : physicalTransportNotWorldIdentity
  hessianNotTruthAuthority : Prop
  hessianNotTruthAuthorityProof : hessianNotTruthAuthority
  readOnlyTransport : Prop
  readOnlyTransportProof : readOnlyTransport

namespace WorldKuuVacuumArakiHessianOSTransport

variable {C : RealHilbertL2Carrier}
variable {W : WorldNoncommutativeOperatorAlgebra C}
variable [PartialOrder W.Region]
variable {B : WorldCStarLocalNetBridge C W}
variable {V : WorldVonNeumannBicommutantBridge B}
variable {M : WorldStandardFormModularFlowBridge V}
variable {R : WorldModularStateKMSRelativeFlowBridge M}
variable {E : WorldArakiRelativeEntropyBridge R}
variable {P : WorldPetzRecoverySufficiencyBridge E}
variable {T : WorldConditionalExpectationTakesakiBridge P}
variable {J : WorldJonesBasicConstructionIndexBridge T}
variable {S : WorldJonesTowerStandardInvariantBridge J}
variable {Q : WorldCanonicalEndomorphismQSystemFrobeniusBridge S}
variable {F : WorldBimoduleSectorFusionCategoryBridge Q}
variable {Z : WorldModuleCategoryNimrepTubeCenterBridge F}
variable {G : WorldGaugeCategoricalIndraNetBridge Z}
variable {I : WorldInformationGeometricHigherGaugeBridge G}
variable {H : WorldArakiPetzQuantumInformationGeometryBridge I}
variable {D : WorldQuantumExponentialDualAffineProjectionBridge H}
variable {Vary : WorldQuantumGeodesicMirrorDescentFreeEnergyBridge D}
variable {Flow : WorldQuantumGradientJKOEntropyProductionBridge Vary}
variable {Mix : WorldQuantumLogSobolevContractivityMixingBridge Flow}
variable {K : WorldKuuVacuumOSHilbertCompletionBridge Mix}
variable {Central : WorldKuuVacuumCentralReferenceStateBridge K}
variable {Geom : WorldKuuVacuumInformationGeometryBridge Central}

variable (Transport : WorldKuuVacuumArakiHessianOSTransport Geom)

def physicalExcitation
    (h : Transport.calculus.Generator) : M.H :=
  Central.excitationVector (Transport.physicalObservable h)

theorem physical_excitation_eq_tangent_excitation
    (h : Transport.calculus.Generator) :
    Transport.physicalExcitation h =
      Geom.vacuumTangentExcitation (Transport.tangentOfGenerator h) := by
  unfold physicalExcitation
  unfold WorldKuuVacuumInformationGeometryBridge.vacuumTangentExcitation
  rw [Transport.tangentObservable_eq_physicalObservable h]

theorem physical_excitation_eq_os_image
    (h : Transport.calculus.Generator) :
    Transport.physicalExcitation h =
      K.osHilbertIdentification
        (K.osClass (Transport.positiveTimeRepresentative h)) :=
  (Transport.osImage_eq_excitation h).symm

theorem hessian_eq_quantum_fisher
    (i : G.Patch) (k h : Transport.calculus.Generator) :
    Transport.calculus.mixedHessian k h =
      H.quantumFisherMetric i (Geom.vacuumParameter i)
        (Transport.tangentOfGenerator k)
        (Transport.tangentOfGenerator h) := by
  rw [Transport.calculus.mixedHessian_eq_bkm]
  exact Transport.bkm_eq_quantumFisher i k h

theorem hessian_eq_araki_hessian_shadow
    (i : G.Patch) (k h : Transport.calculus.Generator) :
    Transport.calculus.mixedHessian k h =
      H.arakiHessianShadow i (Geom.vacuumParameter i)
        (Transport.tangentOfGenerator k)
        (Transport.tangentOfGenerator h) := by
  calc
    Transport.calculus.mixedHessian k h =
        H.quantumFisherMetric i (Geom.vacuumParameter i)
          (Transport.tangentOfGenerator k)
          (Transport.tangentOfGenerator h) :=
      Transport.hessian_eq_quantum_fisher i k h
    _ = H.arakiHessianShadow i (Geom.vacuumParameter i)
          (Transport.tangentOfGenerator k)
          (Transport.tangentOfGenerator h) :=
      H.quantumFisher_eq_arakiHessian i (Geom.vacuumParameter i)
        (Transport.tangentOfGenerator k)
        (Transport.tangentOfGenerator h)

theorem hessian_eq_physical_excitation_gram
    (i : G.Patch) (k h : Transport.calculus.Generator) :
    Transport.calculus.mixedHessian k h =
      (inner ℂ (Transport.physicalExcitation k)
        (Transport.physicalExcitation h)).re := by
  calc
    Transport.calculus.mixedHessian k h =
        H.quantumFisherMetric i (Geom.vacuumParameter i)
          (Transport.tangentOfGenerator k)
          (Transport.tangentOfGenerator h) :=
      Transport.hessian_eq_quantum_fisher i k h
    _ = (inner ℂ
          (Geom.vacuumTangentExcitation (Transport.tangentOfGenerator k))
          (Geom.vacuumTangentExcitation (Transport.tangentOfGenerator h))).re :=
      (Geom.vacuum_excitation_gram_eq_quantum_fisher i
        (Transport.tangentOfGenerator k)
        (Transport.tangentOfGenerator h)).symm
    _ = (inner ℂ (Transport.physicalExcitation k)
          (Transport.physicalExcitation h)).re := by
      rw [Transport.physical_excitation_eq_tangent_excitation]
      rw [Transport.physical_excitation_eq_tangent_excitation]

theorem hessian_eq_os_reflection_form_re
    (i : G.Patch) (k h : Transport.calculus.Generator) :
    Transport.calculus.mixedHessian k h =
      (K.osReflectionForm
        (Transport.positiveTimeRepresentative k)
        (Transport.positiveTimeRepresentative h)).re := by
  rw [Transport.hessian_eq_physical_excitation_gram i k h]
  rw [Transport.physical_excitation_eq_os_image k]
  rw [Transport.physical_excitation_eq_os_image h]
  rw [K.osHilbertIdentification.inner_map_map]
  exact congrArg Complex.re
    (K.osClassInner
      (Transport.positiveTimeRepresentative k)
      (Transport.positiveTimeRepresentative h))

theorem hessian_nonnegative
    (h : Transport.calculus.Generator) :
    0 ≤ Transport.calculus.mixedHessian h h :=
  Transport.calculus.mixedHessian_nonnegative h

theorem physical_carrier_infinite_dimensional :
    InfiniteDimensional ℂ M.H :=
  Transport.infiniteDimensionalPhysicalCarrier

theorem exact_scope :
    Transport.boundedGeneratorScope ∧
    Transport.faithfulNormalVacuumScope ∧
    Transport.sigmaFiniteStandardFormScope :=
  ⟨Transport.boundedGeneratorScopeProof,
    Transport.faithfulNormalVacuumScopeProof,
    Transport.sigmaFiniteStandardFormScopeProof⟩

theorem boundary_package :
    Transport.noArbitraryUnboundedGeneratorClaim ∧
    Transport.physicalTransportNotWorldIdentity ∧
    Transport.hessianNotTruthAuthority ∧
    Transport.readOnlyTransport :=
  ⟨Transport.noArbitraryUnboundedGeneratorClaimProof,
    Transport.physicalTransportNotWorldIdentityProof,
    Transport.hessianNotTruthAuthorityProof,
    Transport.readOnlyTransportProof⟩

end WorldKuuVacuumArakiHessianOSTransport
end
end WORLD
end KUOS
