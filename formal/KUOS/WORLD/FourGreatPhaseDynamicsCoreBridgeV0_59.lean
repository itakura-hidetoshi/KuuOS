import KUOS.WORLD.FourGreatPhaseDynamicsCoreV0_59
import KUOS.WORLD.FourGreatPhaseDynamicsV0_59

/-!
Typed realization of the Mathlib-only four-great core by the WORLD v0.59
Araki-Hessian and physical-Hilbert transport layer.
-/

namespace KUOS
namespace WORLD

noncomputable section

namespace WorldFourGreatPhaseDynamics

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
variable {Transport : WorldKuuVacuumArakiHessianOSTransport Geom}

variable (Dyn : WorldFourGreatPhaseDynamics Transport)

def analyticCore (i : G.Patch) :
    WorldFourGreatAnalyticCore Transport.calculus.Generator where
  earth := Dyn.earthStiffness
  water := Dyn.waterCorrelation
  fire := Dyn.fireLoss
  air := Dyn.airActivity
  earth_nonnegative := Dyn.earth_nonnegative
  water_nonnegative := Dyn.water_nonnegative i
  fire_nonnegative := Dyn.fire_nonnegative
  air_nonnegative := Dyn.air_nonnegative
  earth_eq_water := Dyn.earth_eq_water i
  air_zero := Dyn.air_zero_activity
  effectiveFireRequiresCoarseGraining :=
    Dyn.effectiveFireRequiresCoarseGraining
  effectiveFireRequiresCoarseGrainingProof :=
    Dyn.effectiveFireRequiresCoarseGrainingProof
  osContractionIsNotPhysicalFire :=
    Dyn.osContractionIsNotPhysicalFire
  osContractionIsNotPhysicalFireProof :=
    Dyn.osContractionIsNotPhysicalFireProof
  diagnosticIsNotOntology :=
    Dyn.fourGreatDiagnosticIsNotOntology
  diagnosticIsNotOntologyProof :=
    Dyn.fourGreatDiagnosticIsNotOntologyProof
  readOnlyDiagnostic := Dyn.readOnlyDiagnostic
  readOnlyDiagnosticProof := Dyn.readOnlyDiagnosticProof

theorem analyticCore_earth_eq_water
    (i : G.Patch) (h : Transport.calculus.Generator) :
    (Dyn.analyticCore i).earth h = (Dyn.analyticCore i).water h :=
  (Dyn.analyticCore i).earth_eq_water h

theorem analyticCore_total_nonnegative
    (i : G.Patch) (t : ℝ) (h : Transport.calculus.Generator) :
    0 ≤
      ((Dyn.analyticCore i).diagnostic t h).earth +
      ((Dyn.analyticCore i).diagnostic t h).water +
      ((Dyn.analyticCore i).diagnostic t h).fire +
      ((Dyn.analyticCore i).diagnostic t h).air :=
  (Dyn.analyticCore i).diagnostic_total_nonnegative t h

end WorldFourGreatPhaseDynamics
end
end WORLD
end KUOS
