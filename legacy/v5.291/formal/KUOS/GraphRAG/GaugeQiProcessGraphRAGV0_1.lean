import Mathlib

namespace KUOS.GraphRAG

universe u v w

structure GaugeConnection (Vertex : Type u) (Gauge : Type v) [Group Gauge] where
  transport : Vertex → Vertex → Gauge

def GaugeConnection.gaugeTransform
    {Vertex : Type u} {Gauge : Type v} [Group Gauge]
    (connection : GaugeConnection Vertex Gauge)
    (frame : Vertex → Gauge) : GaugeConnection Vertex Gauge where
  transport source target :=
    frame target * connection.transport source target * (frame source)⁻¹

def pathEndpoint {Vertex : Type u} (start : Vertex) : List Vertex → Vertex
  | [] => start
  | target :: rest => pathEndpoint target rest

def pathTransport
    {Vertex : Type u} {Gauge : Type v} [Group Gauge]
    (connection : GaugeConnection Vertex Gauge) : Vertex → List Vertex → Gauge
  | _, [] => 1
  | source, target :: rest =>
      pathTransport connection target rest * connection.transport source target

theorem pathTransport_gaugeCovariant
    {Vertex : Type u} {Gauge : Type v} [Group Gauge]
    (connection : GaugeConnection Vertex Gauge)
    (frame : Vertex → Gauge) (start : Vertex) (tail : List Vertex) :
    pathTransport (connection.gaugeTransform frame) start tail =
      frame (pathEndpoint start tail) * pathTransport connection start tail *
        (frame start)⁻¹ := by
  induction tail generalizing start with
  | nil => simp [pathTransport, pathEndpoint]
  | cons target rest ih =>
      change
        pathTransport (connection.gaugeTransform frame) target rest *
            (connection.gaugeTransform frame).transport start target =
          frame (pathEndpoint target rest) *
              (pathTransport connection target rest *
                connection.transport start target) *
            (frame start)⁻¹
      rw [ih target]
      simp only [GaugeConnection.gaugeTransform]
      group

def loopHolonomy
    {Vertex : Type u} {Gauge : Type v} [Group Gauge]
    (connection : GaugeConnection Vertex Gauge)
    (start : Vertex) (tail : List Vertex) : Gauge :=
  pathTransport connection start tail

theorem loopHolonomy_conjugates
    {Vertex : Type u} {Gauge : Type v} [Group Gauge]
    (connection : GaugeConnection Vertex Gauge)
    (frame : Vertex → Gauge) (start : Vertex) (tail : List Vertex)
    (closed : pathEndpoint start tail = start) :
    loopHolonomy (connection.gaugeTransform frame) start tail =
      frame start * loopHolonomy connection start tail * (frame start)⁻¹ := by
  unfold loopHolonomy
  rw [pathTransport_gaugeCovariant, closed]

def ConjugationInvariant
    {Gauge : Type v} [Group Gauge] {Result : Type w}
    (observable : Gauge → Result) : Prop :=
  ∀ gauge element, observable (gauge * element * gauge⁻¹) = observable element

theorem loopObservable_gaugeInvariant
    {Vertex : Type u} {Gauge : Type v} [Group Gauge] {Result : Type w}
    (connection : GaugeConnection Vertex Gauge)
    (frame : Vertex → Gauge) (observable : Gauge → Result)
    (invariant : ConjugationInvariant observable)
    (start : Vertex) (tail : List Vertex)
    (closed : pathEndpoint start tail = start) :
    observable (loopHolonomy (connection.gaugeTransform frame) start tail) =
      observable (loopHolonomy connection start tail) := by
  rw [loopHolonomy_conjugates connection frame start tail closed]
  exact invariant (frame start) (loopHolonomy connection start tail)

structure UnitScore where
  value : ℝ
  nonnegative : 0 ≤ value
  atMostOne : value ≤ 1

def UnitScore.mul (left right : UnitScore) : UnitScore where
  value := left.value * right.value
  nonnegative := mul_nonneg left.nonnegative right.nonnegative
  atMostOne := by
    calc
      left.value * right.value ≤ 1 * right.value :=
        mul_le_mul_of_nonneg_right left.atMostOne right.nonnegative
      _ = right.value := one_mul right.value
      _ ≤ 1 := right.atMostOne

structure QiProcessWindow where
  transitionContinuity : UnitScore
  memoryContinuity : UnitScore
  nonMarkovVisibility : UnitScore
  recoverability : UnitScore
  debtRelease : UnitScore
  residueRelease : UnitScore

def QiProcessWindow.compatibility (window : QiProcessWindow) : UnitScore :=
  (((window.transitionContinuity.mul window.memoryContinuity).mul
      window.nonMarkovVisibility).mul window.recoverability).mul
        (window.debtRelease.mul window.residueRelease)

theorem qiProcessCompatibility_bounded (window : QiProcessWindow) :
    0 ≤ window.compatibility.value ∧ window.compatibility.value ≤ 1 :=
  ⟨window.compatibility.nonnegative, window.compatibility.atMostOne⟩

structure EvidencePathScores where
  relevance : UnitScore
  sourceConfidence : UnitScore
  provenance : UnitScore
  transportReliability : UnitScore
  temporalConsistency : UnitScore
  qiCompatibility : UnitScore
  recoverability : UnitScore

def EvidencePathScores.jointSupport (scores : EvidencePathScores) : UnitScore :=
  (((((scores.relevance.mul scores.sourceConfidence).mul scores.provenance).mul
      scores.transportReliability).mul scores.temporalConsistency).mul
        scores.qiCompatibility).mul scores.recoverability

theorem evidencePathJointSupport_bounded (scores : EvidencePathScores) :
    0 ≤ scores.jointSupport.value ∧ scores.jointSupport.value ≤ 1 :=
  ⟨scores.jointSupport.nonnegative, scores.jointSupport.atMostOne⟩

structure GaugeQiGraphRAGBoundary where
  querySpecificEvidenceBundle : Bool
  persistentGlobalContextGraph : Bool
  globalWinnerSelected : Bool
  globalTruthGranted : Bool
  executionAuthorityGranted : Bool
  qiHistoryAuthorityGranted : Bool
  curvatureVetoGranted : Bool
  querySpecificRequired : querySpecificEvidenceBundle = true
  persistentGlobalGraphForbidden : persistentGlobalContextGraph = false
  globalWinnerForbidden : globalWinnerSelected = false
  globalTruthForbidden : globalTruthGranted = false
  executionAuthorityForbidden : executionAuthorityGranted = false
  qiAuthorityForbidden : qiHistoryAuthorityGranted = false
  curvatureVetoForbidden : curvatureVetoGranted = false

theorem gaugeQiGraphRAG_preserves_boundaries
    (boundary : GaugeQiGraphRAGBoundary) :
    boundary.querySpecificEvidenceBundle = true ∧
    boundary.persistentGlobalContextGraph = false ∧
    boundary.globalWinnerSelected = false ∧
    boundary.globalTruthGranted = false ∧
    boundary.executionAuthorityGranted = false ∧
    boundary.qiHistoryAuthorityGranted = false ∧
    boundary.curvatureVetoGranted = false := by
  exact ⟨boundary.querySpecificRequired,
    boundary.persistentGlobalGraphForbidden,
    boundary.globalWinnerForbidden,
    boundary.globalTruthForbidden,
    boundary.executionAuthorityForbidden,
    boundary.qiAuthorityForbidden,
    boundary.curvatureVetoForbidden⟩

structure PluralityReceipt where
  declaredPathCount : ℕ
  retainedPathCount : ℕ
  retainedNotGreater : retainedPathCount ≤ declaredPathCount
  noUniversalWinner : Bool
  universalWinnerForbidden : noUniversalWinner = true

theorem pluralityReceipt_preserves_finite_plurality
    (receipt : PluralityReceipt) :
    receipt.retainedPathCount ≤ receipt.declaredPathCount ∧
      receipt.noUniversalWinner = true :=
  ⟨receipt.retainedNotGreater, receipt.universalWinnerForbidden⟩

end KUOS.GraphRAG
