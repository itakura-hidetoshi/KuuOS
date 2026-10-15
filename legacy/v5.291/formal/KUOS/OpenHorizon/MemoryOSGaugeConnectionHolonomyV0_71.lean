import Mathlib
import KUOS.OpenHorizon.MemoryOSCollusionCorrelationWeightedCutV0_70

namespace KUOS.OpenHorizon.MemoryOSGaugeConnectionHolonomyV0_71

/-- Exact-rational additive gauge connection on three local memory charts. -/
structure GaugeConnection where
  ab : ℚ
  bc : ℚ
  ca : ℚ
deriving DecidableEq, Repr

/-- Local change of frame on the three charts. -/
structure GaugeParameter where
  ga : ℚ
  gb : ℚ
  gc : ℚ
deriving DecidableEq, Repr

/-- Local memory section represented in the chosen chart frames. -/
structure MemorySection where
  sa : ℚ
  sb : ℚ
  sc : ℚ
deriving DecidableEq, Repr

/-- Additive discrete gauge transformation Aᵢⱼ ↦ Aᵢⱼ + gⱼ - gᵢ. -/
def gaugeTransform (connection : GaugeConnection) (gauge : GaugeParameter) :
    GaugeConnection :=
  {
    ab := connection.ab + gauge.gb - gauge.ga
    bc := connection.bc + gauge.gc - gauge.gb
    ca := connection.ca + gauge.ga - gauge.gc
  }

/-- Local section transformation sᵢ ↦ sᵢ + gᵢ. -/
def sectionTransform (section : MemorySection) (gauge : GaugeParameter) :
    MemorySection :=
  {
    sa := section.sa + gauge.ga
    sb := section.sb + gauge.gb
    sc := section.sc + gauge.gc
  }

/-- Additive holonomy, equivalently the discrete curvature of the triangular atlas. -/
def holonomy (connection : GaugeConnection) : ℚ :=
  connection.ab + connection.bc + connection.ca

/-- Gauge-invariant squared curvature energy. -/
def curvatureEnergy (connection : GaugeConnection) : ℚ :=
  holonomy connection ^ 2

/-- A connection is flat exactly when its triangular holonomy vanishes. -/
def Flat (connection : GaugeConnection) : Prop :=
  holonomy connection = 0

/-- Gauge-covariant consistency residuals on the three overlaps. -/
def covariantAB (connection : GaugeConnection) (section : MemorySection) : ℚ :=
  section.sb - section.sa - connection.ab

def covariantBC (connection : GaugeConnection) (section : MemorySection) : ℚ :=
  section.sc - section.sb - connection.bc

def covariantCA (connection : GaugeConnection) (section : MemorySection) : ℚ :=
  section.sa - section.sc - connection.ca

/-- The triangular holonomy is unchanged by every local frame change. -/
theorem holonomy_gauge_invariant
    (connection : GaugeConnection)
    (gauge : GaugeParameter) :
    holonomy (gaugeTransform connection gauge) = holonomy connection := by
  unfold holonomy gaugeTransform
  ring

/-- Curvature energy is gauge invariant. -/
theorem curvature_energy_gauge_invariant
    (connection : GaugeConnection)
    (gauge : GaugeParameter) :
    curvatureEnergy (gaugeTransform connection gauge) = curvatureEnergy connection := by
  unfold curvatureEnergy
  rw [holonomy_gauge_invariant]

/-- Flatness is independent of the chosen local chart frames. -/
theorem flat_gauge_invariant
    (connection : GaugeConnection)
    (gauge : GaugeParameter) :
    Flat (gaugeTransform connection gauge) ↔ Flat connection := by
  unfold Flat
  rw [holonomy_gauge_invariant]

/-- Each overlap residual is gauge invariant when connection and section transform together. -/
theorem covariant_ab_gauge_invariant
    (connection : GaugeConnection)
    (section : MemorySection)
    (gauge : GaugeParameter) :
    covariantAB (gaugeTransform connection gauge) (sectionTransform section gauge) =
      covariantAB connection section := by
  unfold covariantAB gaugeTransform sectionTransform
  ring

theorem covariant_bc_gauge_invariant
    (connection : GaugeConnection)
    (section : MemorySection)
    (gauge : GaugeParameter) :
    covariantBC (gaugeTransform connection gauge) (sectionTransform section gauge) =
      covariantBC connection section := by
  unfold covariantBC gaugeTransform sectionTransform
  ring

theorem covariant_ca_gauge_invariant
    (connection : GaugeConnection)
    (section : MemorySection)
    (gauge : GaugeParameter) :
    covariantCA (gaugeTransform connection gauge) (sectionTransform section gauge) =
      covariantCA connection section := by
  unfold covariantCA gaugeTransform sectionTransform
  ring

/-- Curvature energy is nonnegative. -/
theorem curvature_energy_nonnegative (connection : GaugeConnection) :
    0 ≤ curvatureEnergy connection := by
  unfold curvatureEnergy
  exact sq_nonneg (holonomy connection)

/-- Zero curvature energy is equivalent to flatness. -/
theorem curvature_energy_eq_zero_iff_flat (connection : GaugeConnection) :
    curvatureEnergy connection = 0 ↔ Flat connection := by
  unfold curvatureEnergy Flat
  constructor
  · intro h
    nlinarith [sq_nonneg (holonomy connection)]
  · intro h
    simp [h]

/-- Gauge fixing along the a-b-c spanning tree. -/
def treeGauge (connection : GaugeConnection) : GaugeParameter :=
  {
    ga := 0
    gb := -connection.ab
    gc := -(connection.ab + connection.bc)
  }

/-- Tree gauge removes both tree-edge potentials. -/
theorem tree_gauge_ab_zero (connection : GaugeConnection) :
    (gaugeTransform connection (treeGauge connection)).ab = 0 := by
  unfold gaugeTransform treeGauge
  ring

theorem tree_gauge_bc_zero (connection : GaugeConnection) :
    (gaugeTransform connection (treeGauge connection)).bc = 0 := by
  unfold gaugeTransform treeGauge
  ring

/-- The only residual after tree gauge fixing is the gauge-invariant holonomy. -/
theorem tree_gauge_ca_eq_holonomy (connection : GaugeConnection) :
    (gaugeTransform connection (treeGauge connection)).ca = holonomy connection := by
  unfold gaugeTransform treeGauge holonomy
  ring

/-- Difference between indirect and direct transport from chart a to chart c. -/
def indirectToC (connection : GaugeConnection) : ℚ :=
  connection.ab + connection.bc

def directToC (connection : GaugeConnection) : ℚ :=
  -connection.ca

theorem path_transport_difference_eq_holonomy (connection : GaugeConnection) :
    indirectToC connection - directToC connection = holonomy connection := by
  unfold indirectToC directToC holonomy
  ring

/-- Path dependence is itself gauge invariant. -/
theorem path_transport_difference_gauge_invariant
    (connection : GaugeConnection)
    (gauge : GaugeParameter) :
    indirectToC (gaugeTransform connection gauge) -
        directToC (gaugeTransform connection gauge) =
      indirectToC connection - directToC connection := by
  calc
    indirectToC (gaugeTransform connection gauge) -
        directToC (gaugeTransform connection gauge) =
      holonomy (gaugeTransform connection gauge) :=
        path_transport_difference_eq_holonomy _
    _ = holonomy connection := holonomy_gauge_invariant _ _
    _ = indirectToC connection - directToC connection :=
      (path_transport_difference_eq_holonomy connection).symm

/-- Gauge-invariant curvature threshold, used only as an advisory inconsistency flag. -/
def CurvatureFlag (threshold : ℚ) (connection : GaugeConnection) : Prop :=
  threshold ≤ |holonomy connection|

theorem curvature_flag_gauge_invariant
    (threshold : ℚ)
    (connection : GaugeConnection)
    (gauge : GaugeParameter) :
    CurvatureFlag threshold (gaugeTransform connection gauge) ↔
      CurvatureFlag threshold connection := by
  unfold CurvatureFlag
  rw [holonomy_gauge_invariant]

/-- Bounded gauge-invariant penalty derived from absolute holonomy. -/
def curvaturePenalty (connection : GaugeConnection) : ℚ :=
  |holonomy connection| / 7

def gaugeAdjustedConfidence (base : ℚ) (connection : GaugeConnection) : ℚ :=
  base - curvaturePenalty connection

theorem curvature_penalty_gauge_invariant
    (connection : GaugeConnection)
    (gauge : GaugeParameter) :
    curvaturePenalty (gaugeTransform connection gauge) = curvaturePenalty connection := by
  unfold curvaturePenalty
  rw [holonomy_gauge_invariant]

theorem gauge_adjusted_confidence_gauge_invariant
    (base : ℚ)
    (connection : GaugeConnection)
    (gauge : GaugeParameter) :
    gaugeAdjustedConfidence base (gaugeTransform connection gauge) =
      gaugeAdjustedConfidence base connection := by
  unfold gaugeAdjustedConfidence
  rw [curvature_penalty_gauge_invariant]

theorem gauge_adjusted_confidence_mem_unit_interval
    (base : ℚ)
    (connection : GaugeConnection)
    (hbase0 : 0 ≤ base)
    (hbase1 : base ≤ 1)
    (hpen0 : 0 ≤ curvaturePenalty connection)
    (hpen : curvaturePenalty connection ≤ base) :
    gaugeAdjustedConfidence base connection ∈ Set.Icc (0 : ℚ) 1 := by
  unfold gaugeAdjustedConfidence
  constructor <;> linarith

/-- Canonical flat and curved memory-atlas profiles. -/
def flatConnection : GaugeConnection :=
  { ab := 1 / 3, bc := 1 / 4, ca := -7 / 12 }

def curvedConnection : GaugeConnection :=
  { ab := 1 / 2, bc := 1 / 3, ca := -1 / 4 }

def canonicalGauge : GaugeParameter :=
  { ga := 1 / 5, gb := -1 / 10, gc := 2 / 15 }

theorem flat_connection_holonomy : holonomy flatConnection = 0 := by
  norm_num [holonomy, flatConnection]

theorem curved_connection_holonomy : holonomy curvedConnection = 7 / 12 := by
  norm_num [holonomy, curvedConnection]

theorem canonical_gauge_preserves_curved_holonomy :
    holonomy (gaugeTransform curvedConnection canonicalGauge) = 7 / 12 := by
  rw [holonomy_gauge_invariant]
  exact curved_connection_holonomy

theorem flat_connection_not_flagged :
    ¬ CurvatureFlag (1 / 2) flatConnection := by
  norm_num [CurvatureFlag, holonomy, flatConnection]

theorem curved_connection_flagged :
    CurvatureFlag (1 / 2) curvedConnection := by
  norm_num [CurvatureFlag, holonomy, curvedConnection]

theorem canonical_curvature_penalty :
    curvaturePenalty curvedConnection = 1 / 12 := by
  norm_num [curvaturePenalty, holonomy, curvedConnection, abs_of_nonneg]

theorem canonical_gauge_adjusted_confidence :
    gaugeAdjustedConfidence (3 / 4) curvedConnection = 2 / 3 := by
  norm_num [gaugeAdjustedConfidence, curvaturePenalty, holonomy, curvedConnection, abs_of_nonneg]

structure GaugeConnectionHolonomyCertificate where
  sourceMemoryOSV070Bound : Bool
  localGaugeFramesExact : Bool
  connectionTransformationExact : Bool
  holonomyGaugeInvariantExact : Bool
  covariantResidualExact : Bool
  curvatureEnergyExact : Bool
  treeGaugeFixingExact : Bool
  pathDependenceHolonomyExact : Bool
  gaugeAdjustedConfidenceExact : Bool
  nonAbelianHolonomyClaimed : Bool
  gaugeFlagUsedAsCandidateRanking : Bool
  executionPermission : Bool
  persistentWorldStateMutated : Bool
  truthAuthorityGranted : Bool

end KUOS.OpenHorizon.MemoryOSGaugeConnectionHolonomyV0_71
