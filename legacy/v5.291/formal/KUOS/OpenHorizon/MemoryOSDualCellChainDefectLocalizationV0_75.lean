import Mathlib
import KUOS.OpenHorizon.MemoryOSDualTwoComplexStokesGluingV0_74

namespace KUOS.OpenHorizon.MemoryOSDualCellChainDefectLocalizationV0_75

open KUOS.OpenHorizon.MemoryOSNonAbelianWilsonLoopV0_72
open KUOS.OpenHorizon.MemoryOSTetrahedralBianchiCurvatureV0_73
open KUOS.OpenHorizon.MemoryOSDualTwoComplexStokesGluingV0_74

/-- One dual edge in a finite cell chain, carrying its transport and local seam defect. -/
structure DualCellLink (G : Type*) [Group G] where
  seamTransport : G
  localSeamDefect : G

/-- Bind a v0.74 glued two-cell certificate into one link of a longer dual chain. -/
def linkOfGluedPair {G : Type*} [Group G]
    (pair : GluedTetrahedra G) : DualCellLink G :=
  {
    seamTransport := pair.seamTransport
    localSeamDefect := seamGluingDefect pair
  }

/-- A seam is compatible exactly when its local defect is the identity. -/
def DualCellLink.Compatible {G : Type*} [Group G]
    (link : DualCellLink G) : Prop :=
  link.localSeamDefect = 1

theorem link_of_glued_pair_compatible {G : Type*} [Group G]
    (pair : GluedTetrahedra G) (h : SharedFaceCompatible pair) :
    (linkOfGluedPair pair).Compatible := by
  unfold DualCellLink.Compatible linkOfGluedPair
  exact seam_gluing_defect_identity_of_compatible pair h

/-- A finite, path-ordered chain of dual links. -/
structure DualCellChain (G : Type*) [Group G] where
  links : List (DualCellLink G)

/--
Transport each local seam defect to the initial basepoint by the accumulated
ordered seam transport, then multiply the transported defects in chain order.
-/
def pathOrderedLocalizedDefectProductAux {G : Type*} [Group G]
    (prefix : G) : List (DualCellLink G) → G
  | [] => 1
  | link :: rest =>
      (prefix * link.localSeamDefect * prefix⁻¹) *
        pathOrderedLocalizedDefectProductAux
          (prefix * link.seamTransport) rest

/-- Global outer-boundary holonomy of the finite chain certificate. -/
def globalOuterBoundary {G : Type*} [Group G]
    (chain : DualCellChain G) : G :=
  pathOrderedLocalizedDefectProductAux 1 chain.links

theorem global_outer_boundary_eq_path_ordered_localized_defects
    {G : Type*} [Group G] (chain : DualCellChain G) :
    globalOuterBoundary chain =
      pathOrderedLocalizedDefectProductAux 1 chain.links := rfl

/-- Every seam in the chain has trivial local defect. -/
def AllSeamsCompatible {G : Type*} [Group G]
    (chain : DualCellChain G) : Prop :=
  ∀ link ∈ chain.links, link.Compatible

theorem path_ordered_localized_defects_identity_of_compatible
    {G : Type*} [Group G]
    (prefix : G) (links : List (DualCellLink G))
    (h : ∀ link ∈ links, link.Compatible) :
    pathOrderedLocalizedDefectProductAux prefix links = 1 := by
  induction links generalizing prefix with
  | nil => simp [pathOrderedLocalizedDefectProductAux]
  | cons link rest ih =>
      have hlink : link.Compatible := h link (by simp)
      have hrest : ∀ candidate ∈ rest, candidate.Compatible := by
        intro candidate hmem
        exact h candidate (by simp [hmem])
      have htail := ih (prefix := prefix * link.seamTransport) hrest
      unfold DualCellLink.Compatible at hlink
      simp [pathOrderedLocalizedDefectProductAux, hlink, htail]

/-- Compatible seams close the finite dual-cell chain globally. -/
theorem compatible_chain_global_closure {G : Type*} [Group G]
    (chain : DualCellChain G) (h : AllSeamsCompatible chain) :
    globalOuterBoundary chain = 1 := by
  unfold globalOuterBoundary AllSeamsCompatible at *
  exact path_ordered_localized_defects_identity_of_compatible 1 chain.links h

/-- Three-link chain used for exact localization of one middle mismatch. -/
def threeLinkChain {G : Type*} [Group G]
    (first middle last : DualCellLink G) : DualCellChain G :=
  { links := [first, middle, last] }

/--
If the first and last seams are compatible, the only middle mismatch reaches
the global boundary by conjugation with the preceding path transport.
-/
theorem three_link_middle_mismatch_localizes
    {G : Type*} [Group G]
    (first middle last : DualCellLink G)
    (hfirst : first.Compatible) (hlast : last.Compatible) :
    globalOuterBoundary (threeLinkChain first middle last) =
      first.seamTransport * middle.localSeamDefect *
        first.seamTransport⁻¹ := by
  unfold DualCellLink.Compatible at hfirst hlast
  simp [globalOuterBoundary, threeLinkChain,
    pathOrderedLocalizedDefectProductAux, hfirst, hlast]

/-- Class-function Wilson signature of the path-ordered global boundary. -/
def chainBoundaryWilson {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (chain : DualCellChain G) : R :=
  χ.toFun (globalOuterBoundary chain)

/-- The single localized defect is frame-independent at the conjugacy-class level. -/
theorem three_link_middle_mismatch_wilson_localizes
    {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R)
    (first middle last : DualCellLink G)
    (hfirst : first.Compatible) (hlast : last.Compatible) :
    chainBoundaryWilson χ (threeLinkChain first middle last) =
      χ.toFun middle.localSeamDefect := by
  unfold chainBoundaryWilson
  rw [three_link_middle_mismatch_localizes first middle last hfirst hlast]
  simpa using
    χ.conjugationInvariant first.seamTransport⁻¹ middle.localSeamDefect

/-- Advisory class-function penalty for the global chain defect. -/
def chainDefectPenalty {G : Type*} [Group G]
    (χ : ClassFunction G ℚ) (maxValue scale : ℚ)
    (chain : DualCellChain G) : ℚ :=
  (maxValue - chainBoundaryWilson χ chain) / scale

/-- Advisory confidence inherited from the source certificate. -/
def chainAdjustedConfidence {G : Type*} [Group G]
    (χ : ClassFunction G ℚ) (maxValue scale base : ℚ)
    (chain : DualCellChain G) : ℚ :=
  base - chainDefectPenalty χ maxValue scale chain

theorem three_link_middle_mismatch_confidence_localizes
    {G : Type*} [Group G]
    (χ : ClassFunction G ℚ) (maxValue scale base : ℚ)
    (first middle last : DualCellLink G)
    (hfirst : first.Compatible) (hlast : last.Compatible) :
    chainAdjustedConfidence χ maxValue scale base
        (threeLinkChain first middle last) =
      base - (maxValue - χ.toFun middle.localSeamDefect) / scale := by
  unfold chainAdjustedConfidence chainDefectPenalty
  rw [three_link_middle_mismatch_wilson_localizes χ first middle last hfirst hlast]

/-- A closed dual 3-cycle with independent local vertex frames. -/
structure DualTriangleCycle (G : Type*) [Group G] where
  edge01 : G
  edge12 : G
  edge20 : G

structure DualTriangleGaugeFrame (G : Type*) [Group G] where
  g0 : G
  g1 : G
  g2 : G

/-- Path-ordered holonomy around the dual cycle. -/
def dualCycleHolonomy {G : Type*} [Group G]
    (cycle : DualTriangleCycle G) : G :=
  cycle.edge01 * cycle.edge12 * cycle.edge20

/-- Independent endpoint-frame action on the three oriented dual edges. -/
def gaugeTransformDualCycle {G : Type*} [Group G]
    (cycle : DualTriangleCycle G) (frame : DualTriangleGaugeFrame G) :
    DualTriangleCycle G :=
  {
    edge01 := frame.g0⁻¹ * cycle.edge01 * frame.g1
    edge12 := frame.g1⁻¹ * cycle.edge12 * frame.g2
    edge20 := frame.g2⁻¹ * cycle.edge20 * frame.g0
  }

theorem dual_cycle_holonomy_gauge_covariant
    {G : Type*} [Group G]
    (cycle : DualTriangleCycle G) (frame : DualTriangleGaugeFrame G) :
    dualCycleHolonomy (gaugeTransformDualCycle cycle frame) =
      frame.g0⁻¹ * dualCycleHolonomy cycle * frame.g0 := by
  unfold dualCycleHolonomy gaugeTransformDualCycle
  group

/-- Class-function Wilson signature of the closed dual cycle. -/
def dualCycleWilson {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R) (cycle : DualTriangleCycle G) : R :=
  χ.toFun (dualCycleHolonomy cycle)

theorem dual_cycle_wilson_gauge_invariant
    {G : Type*} [Group G] {R : Type*}
    (χ : ClassFunction G R)
    (cycle : DualTriangleCycle G) (frame : DualTriangleGaugeFrame G) :
    dualCycleWilson χ (gaugeTransformDualCycle cycle frame) =
      dualCycleWilson χ cycle := by
  unfold dualCycleWilson
  rw [dual_cycle_holonomy_gauge_covariant]
  simpa using χ.conjugationInvariant frame.g0 (dualCycleHolonomy cycle)

/-- Canonical v0.74 links reused in the v0.75 chain. -/
def compatibleCurvedLink : DualCellLink S3 :=
  linkOfGluedPair compatibleCurvedPair

def mismatchedCurvedLink : DualCellLink S3 :=
  linkOfGluedPair mismatchedCurvedPair

theorem compatible_curved_link_compatible : compatibleCurvedLink.Compatible := by
  exact link_of_glued_pair_compatible compatibleCurvedPair
    canonical_compatible_shared_face

/-- Three compatible curved seams. -/
def canonicalCompatibleChain : DualCellChain S3 :=
  threeLinkChain compatibleCurvedLink compatibleCurvedLink compatibleCurvedLink

/-- One middle mismatch, bracketed by compatible seams. -/
def canonicalSingleMismatchChain : DualCellChain S3 :=
  threeLinkChain compatibleCurvedLink mismatchedCurvedLink compatibleCurvedLink

theorem canonical_compatible_chain_closure :
    globalOuterBoundary canonicalCompatibleChain = 1 := by
  native_decide

theorem canonical_single_middle_mismatch_boundary :
    globalOuterBoundary canonicalSingleMismatchChain = swap01 * swap12 := by
  native_decide

theorem canonical_single_middle_mismatch_wilson :
    chainBoundaryWilson (identityWilsonClass S3) canonicalSingleMismatchChain = 0 := by
  native_decide

theorem canonical_compatible_chain_confidence :
    chainAdjustedConfidence (identityWilsonClass S3) 3 18 (1 / 3)
      canonicalCompatibleChain = 1 / 3 := by
  native_decide

theorem canonical_single_mismatch_chain_confidence :
    chainAdjustedConfidence (identityWilsonClass S3) 3 18 (1 / 3)
      canonicalSingleMismatchChain = 1 / 6 := by
  native_decide

/-- Direct finite S3 links used to expose noncommutative order dependence. -/
def identityLink : DualCellLink S3 :=
  { seamTransport := 1, localSeamDefect := 1 }

def swap01DefectLink : DualCellLink S3 :=
  { seamTransport := 1, localSeamDefect := swap01 }

def swap12DefectLink : DualCellLink S3 :=
  { seamTransport := 1, localSeamDefect := swap12 }

def canonicalOrderedMismatchAB : DualCellChain S3 :=
  threeLinkChain swap01DefectLink swap12DefectLink identityLink

def canonicalOrderedMismatchBA : DualCellChain S3 :=
  threeLinkChain swap12DefectLink swap01DefectLink identityLink

theorem canonical_multiple_mismatch_order_dependence :
    globalOuterBoundary canonicalOrderedMismatchAB ≠
      globalOuterBoundary canonicalOrderedMismatchBA := by
  native_decide

theorem canonical_ordered_mismatch_ab_boundary :
    globalOuterBoundary canonicalOrderedMismatchAB = swap01 * swap12 := by
  native_decide

theorem canonical_ordered_mismatch_ba_boundary :
    globalOuterBoundary canonicalOrderedMismatchBA = swap12 * swap01 := by
  native_decide

/-- The permutation character sees the conjugacy class, not the ordered representative. -/
theorem canonical_ordered_mismatch_class_signature_limitation :
    chainBoundaryWilson (identityWilsonClass S3) canonicalOrderedMismatchAB =
      chainBoundaryWilson (identityWilsonClass S3) canonicalOrderedMismatchBA := by
  native_decide

/-- Canonical closed dual cycle. -/
def canonicalDualTriangleCycle : DualTriangleCycle S3 :=
  { edge01 := swap01, edge12 := swap12, edge20 := swap01 }

theorem canonical_dual_cycle_holonomy :
    dualCycleHolonomy canonicalDualTriangleCycle = swap01 * swap12 * swap01 := by
  rfl

structure DualCellChainDefectLocalizationCertificate where
  sourceMemoryOSV074Bound : Bool
  finiteDualCellChainExact : Bool
  pathOrderedTransportExact : Bool
  allCompatibleClosureExact : Bool
  singleMismatchLocalizationExact : Bool
  noncommutativeOrderDependenceExact : Bool
  dualCycleHolonomyExact : Bool
  classFunctionLocalizationExact : Bool
  continuumManifoldTheoremClaimed : Bool
  physicalGaugeFieldInferenceClaimed : Bool
  candidateRankingPerformed : Bool
  executionPermission : Bool
  persistentWorldStateMutated : Bool
  truthAuthorityGranted : Bool

end KUOS.OpenHorizon.MemoryOSDualCellChainDefectLocalizationV0_75
