import Mathlib
import KUOS.OpenHorizon.MemoryOSGaugeConnectionHolonomyV0_71

namespace KUOS.OpenHorizon.MemoryOSNonAbelianWilsonLoopV0_72

/-- Matrix-free non-Abelian connection on three local memory charts. -/
structure NonAbelianConnection (G : Type*) [Group G] where
  ab : G
  bc : G
  ca : G

/-- Independent local frame choices on the three charts. -/
structure GaugeFrame (G : Type*) [Group G] where
  ga : G
  gb : G
  gc : G

/-- Link transformation Uᵢⱼ ↦ gᵢ⁻¹ Uᵢⱼ gⱼ. -/
def gaugeTransform {G : Type*} [Group G]
    (connection : NonAbelianConnection G) (frame : GaugeFrame G) :
    NonAbelianConnection G :=
  {
    ab := frame.ga⁻¹ * connection.ab * frame.gb
    bc := frame.gb⁻¹ * connection.bc * frame.gc
    ca := frame.gc⁻¹ * connection.ca * frame.ga
  }

/-- Ordered transport along a → b → c. -/
def pathOrderedTransport {G : Type*} [Group G]
    (connection : NonAbelianConnection G) : G :=
  connection.ab * connection.bc

/-- The reversed product is retained explicitly because multiplication need not commute. -/
def reverseOrderedTransport {G : Type*} [Group G]
    (connection : NonAbelianConnection G) : G :=
  connection.bc * connection.ab

/-- Wilson-loop holonomy around a → b → c → a. -/
def holonomy {G : Type*} [Group G]
    (connection : NonAbelianConnection G) : G :=
  connection.ab * connection.bc * connection.ca

/-- Non-Abelian holonomy is gauge covariant: it transforms by conjugation at the base chart. -/
theorem holonomy_gauge_covariant {G : Type*} [Group G]
    (connection : NonAbelianConnection G) (frame : GaugeFrame G) :
    holonomy (gaugeTransform connection frame) =
      frame.ga⁻¹ * holonomy connection * frame.ga := by
  simp [holonomy, gaugeTransform, mul_assoc]

/-- Explicit conjugacy relation used as the representation-independent fusion class. -/
def GaugeConjugate {G : Type*} [Group G] (x y : G) : Prop :=
  ∃ g : G, x = g⁻¹ * y * g

/-- Gauge-related holonomies are conjugate. -/
theorem holonomy_gauge_conjugate {G : Type*} [Group G]
    (connection : NonAbelianConnection G) (frame : GaugeFrame G) :
    GaugeConjugate (holonomy (gaugeTransform connection frame))
      (holonomy connection) := by
  exact ⟨frame.ga, holonomy_gauge_covariant connection frame⟩

/-- A class function is any observable that is invariant under conjugation. -/
structure ClassFunction (G : Type*) [Group G] (R : Type*) where
  toFun : G → R
  conjugationInvariant : ∀ g h : G, toFun (g⁻¹ * h * g) = toFun h

/-- Wilson-loop observable induced by a class function. -/
def wilsonLoop {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (connection : NonAbelianConnection G) : R :=
  χ.toFun (holonomy connection)

/-- Every class-function Wilson loop is gauge invariant. -/
theorem wilson_loop_gauge_invariant {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R)
    (connection : NonAbelianConnection G) (frame : GaugeFrame G) :
    wilsonLoop χ (gaugeTransform connection frame) = wilsonLoop χ connection := by
  unfold wilsonLoop
  rw [holonomy_gauge_covariant]
  exact χ.conjugationInvariant frame.ga (holonomy connection)

/-- Gauge-invariant multi-chart fusion predicate. -/
def FusionConsistent {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (neutral : R)
    (connection : NonAbelianConnection G) : Prop :=
  wilsonLoop χ connection = neutral

/-- Fusion consistency is independent of all local frame choices. -/
theorem fusion_consistent_gauge_invariant {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (neutral : R)
    (connection : NonAbelianConnection G) (frame : GaugeFrame G) :
    FusionConsistent χ neutral (gaugeTransform connection frame) ↔
      FusionConsistent χ neutral connection := by
  unfold FusionConsistent
  rw [wilson_loop_gauge_invariant]

/-- Constructive non-Abelian tree gauge on the a-b-c spanning tree. -/
def treeGauge {G : Type*} [Group G]
    (connection : NonAbelianConnection G) : GaugeFrame G :=
  {
    ga := 1
    gb := connection.ab⁻¹
    gc := (connection.ab * connection.bc)⁻¹
  }

/-- Tree gauge removes the first ordered link. -/
theorem tree_gauge_ab_one {G : Type*} [Group G]
    (connection : NonAbelianConnection G) :
    (gaugeTransform connection (treeGauge connection)).ab = 1 := by
  simp [gaugeTransform, treeGauge, mul_assoc]

/-- Tree gauge removes the second ordered link. -/
theorem tree_gauge_bc_one {G : Type*} [Group G]
    (connection : NonAbelianConnection G) :
    (gaugeTransform connection (treeGauge connection)).bc = 1 := by
  simp [gaugeTransform, treeGauge, mul_assoc]

/-- The closing link left after tree gauge fixing is exactly the ordered holonomy. -/
theorem tree_gauge_ca_eq_holonomy {G : Type*} [Group G]
    (connection : NonAbelianConnection G) :
    (gaugeTransform connection (treeGauge connection)).ca = holonomy connection := by
  simp [gaugeTransform, treeGauge, holonomy, mul_assoc]

/-- Closing the indirect a → b → c path reproduces the Wilson-loop holonomy. -/
theorem ordered_path_closure_eq_holonomy {G : Type*} [Group G]
    (connection : NonAbelianConnection G) :
    pathOrderedTransport connection * connection.ca = holonomy connection := by
  rfl

/-- Conjugation preserves identity exactly. -/
theorem conjugate_eq_one_iff {G : Type*} [Group G] (g h : G) :
    g⁻¹ * h * g = 1 ↔ h = 1 := by
  constructor
  · intro hconj
    calc
      h = g * (g⁻¹ * h * g) * g⁻¹ := by simp [mul_assoc]
      _ = 1 := by simp [hconj]
  · rintro rfl
    simp

/-- A simple rational class observable: three for trivial holonomy, zero otherwise. -/
def identityWilsonValue {G : Type*} [Group G] [DecidableEq G] (h : G) : ℚ :=
  if h = 1 then 3 else 0

theorem identity_wilson_value_conjugation {G : Type*} [Group G] [DecidableEq G]
    (g h : G) :
    identityWilsonValue (g⁻¹ * h * g) = identityWilsonValue h := by
  simp [identityWilsonValue, conjugate_eq_one_iff]

def identityWilsonClass (G : Type*) [Group G] [DecidableEq G] : ClassFunction G ℚ :=
  {
    toFun := identityWilsonValue
    conjugationInvariant := identity_wilson_value_conjugation
  }

/-- Gauge-invariant Wilson deficit penalty. -/
def wilsonPenalty {G : Type*} [Group G]
    (χ : ClassFunction G ℚ) (maxValue scale : ℚ)
    (connection : NonAbelianConnection G) : ℚ :=
  (maxValue - wilsonLoop χ connection) / scale

/-- Gauge-adjusted confidence uses only the class invariant, never a local link component. -/
def gaugeAdjustedConfidence {G : Type*} [Group G]
    (χ : ClassFunction G ℚ) (maxValue scale base : ℚ)
    (connection : NonAbelianConnection G) : ℚ :=
  base - wilsonPenalty χ maxValue scale connection

theorem wilson_penalty_gauge_invariant {G : Type*} [Group G]
    (χ : ClassFunction G ℚ) (maxValue scale : ℚ)
    (connection : NonAbelianConnection G) (frame : GaugeFrame G) :
    wilsonPenalty χ maxValue scale (gaugeTransform connection frame) =
      wilsonPenalty χ maxValue scale connection := by
  unfold wilsonPenalty
  rw [wilson_loop_gauge_invariant]

theorem gauge_adjusted_confidence_gauge_invariant {G : Type*} [Group G]
    (χ : ClassFunction G ℚ) (maxValue scale base : ℚ)
    (connection : NonAbelianConnection G) (frame : GaugeFrame G) :
    gaugeAdjustedConfidence χ maxValue scale base
        (gaugeTransform connection frame) =
      gaugeAdjustedConfidence χ maxValue scale base connection := by
  unfold gaugeAdjustedConfidence
  rw [wilson_penalty_gauge_invariant]

theorem gauge_adjusted_confidence_mem_unit_interval {G : Type*} [Group G]
    (χ : ClassFunction G ℚ) (maxValue scale base : ℚ)
    (connection : NonAbelianConnection G)
    (hbase0 : 0 ≤ base) (hbase1 : base ≤ 1)
    (hpen0 : 0 ≤ wilsonPenalty χ maxValue scale connection)
    (hpen : wilsonPenalty χ maxValue scale connection ≤ base) :
    gaugeAdjustedConfidence χ maxValue scale base connection ∈ Set.Icc (0 : ℚ) 1 := by
  unfold gaugeAdjustedConfidence
  constructor <;> linarith

/-- Canonical finite non-Abelian gauge group. -/
abbrev S3 := Equiv.Perm (Fin 3)

def swap01 : S3 := Equiv.swap (0 : Fin 3) (1 : Fin 3)
def swap12 : S3 := Equiv.swap (1 : Fin 3) (2 : Fin 3)

def flatS3Connection : NonAbelianConnection S3 :=
  { ab := 1, bc := 1, ca := 1 }

def nonAbelianS3Connection : NonAbelianConnection S3 :=
  { ab := swap01, bc := swap12, ca := 1 }

def canonicalS3Gauge : GaugeFrame S3 :=
  { ga := swap01, gb := swap12, gc := swap01 * swap12 }

/-- The canonical path ordering is genuinely noncommutative. -/
theorem canonical_path_order_noncommutative :
    pathOrderedTransport nonAbelianS3Connection ≠
      reverseOrderedTransport nonAbelianS3Connection := by
  native_decide

/-- The canonical Wilson-loop holonomy is nontrivial. -/
theorem canonical_nonabelian_holonomy_nontrivial :
    holonomy nonAbelianS3Connection ≠ 1 := by
  native_decide

/-- A local frame change can change the holonomy representative in a non-Abelian theory. -/
theorem canonical_transformed_holonomy_not_equal :
    holonomy (gaugeTransform nonAbelianS3Connection canonicalS3Gauge) ≠
      holonomy nonAbelianS3Connection := by
  native_decide

/-- Yet the transformed representative remains in the same conjugacy class. -/
theorem canonical_transformed_holonomy_conjugate :
    GaugeConjugate
      (holonomy (gaugeTransform nonAbelianS3Connection canonicalS3Gauge))
      (holonomy nonAbelianS3Connection) := by
  exact holonomy_gauge_conjugate _ _

/-- Flat and nontrivial canonical Wilson values. -/
theorem canonical_flat_identity_wilson :
    wilsonLoop (identityWilsonClass S3) flatS3Connection = 3 := by
  native_decide

theorem canonical_nonabelian_identity_wilson :
    wilsonLoop (identityWilsonClass S3) nonAbelianS3Connection = 0 := by
  native_decide

/-- The class observable is unchanged even though the holonomy representative changes. -/
theorem canonical_wilson_gauge_invariant :
    wilsonLoop (identityWilsonClass S3)
        (gaugeTransform nonAbelianS3Connection canonicalS3Gauge) = 0 := by
  rw [wilson_loop_gauge_invariant]
  exact canonical_nonabelian_identity_wilson

/-- Exact canonical penalty and confidence inherited from the v0.71 base confidence 2/3. -/
theorem canonical_nonabelian_wilson_penalty :
    wilsonPenalty (identityWilsonClass S3) 3 18 nonAbelianS3Connection = 1 / 6 := by
  native_decide

theorem canonical_nonabelian_gauge_adjusted_confidence :
    gaugeAdjustedConfidence (identityWilsonClass S3) 3 18 (2 / 3)
      nonAbelianS3Connection = 1 / 2 := by
  native_decide

structure NonAbelianWilsonLoopCertificate where
  sourceMemoryOSV071Bound : Bool
  nonAbelianConnectionExact : Bool
  pathOrderingExact : Bool
  holonomyConjugacyExact : Bool
  WilsonClassInvariantExact : Bool
  treeGaugeFixingExact : Bool
  multiChartFusionExact : Bool
  nonAbelianPhysicalGaugeFieldClaimed : Bool
  candidateRankingPerformed : Bool
  executionPermission : Bool
  persistentWorldStateMutated : Bool
  truthAuthorityGranted : Bool

end KUOS.OpenHorizon.MemoryOSNonAbelianWilsonLoopV0_72
