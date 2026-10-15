import Mathlib
import KUOS.PlanOS.FiniteNormalBallCoverHopfRinowWitnessV1_13

namespace KUOS.PlanOS.FiniteCoverNerveCechPathHomotopyV1_14

structure NerveEdge (α : Type) where
  left : α
  right : α

structure CechTriangle (α : Type) where
  first : α
  second : α
  third : α

structure FiniteCoverNerveCechPathHomotopyCertificate where
  finiteCoverVerticesRetained : Bool
  nerveEdgesRecomputedFromOverlapWitnesses : Bool
  cechTwoSimplicesRecomputedFromTripleOverlapWitnesses : Bool
  triangleBoundariesPresentInNerve : Bool
  finiteNerveConnectedFromReferenceRoot : Bool
  retainedSamplesCoveredByAssignedVertices : Bool
  nervePathsEdgeValid : Bool
  elementaryTrianglePathHomotopyVerified : Bool
  pathHomotopyEndpointsPreserved : Bool
  localToGlobalFiniteTopologicalCoherence : Bool
  finiteComplexOnly : Bool
  classicalNerveTheoremNotClaimed : Bool
  coverHomotopyEquivalenceNotClaimed : Bool
  fundamentalGroupNotComputed : Bool
  globalPathHomotopyClassificationNotClaimed : Bool
  globalTopologicalInvariantNotClaimed : Bool
  candidateIdentityRetained : Bool
  sourceFiniteCoverCertificateNotMutated : Bool
  sourceAtlasCertificateNotMutated : Bool
  persistentWorldStateUnchanged : Bool
  decisionSelectionPerformed : Bool
  historyReadOnly : Bool
  nerveComplexGrantsNoAuthority : Bool
  cechOverlapGrantsNoAuthority : Bool
  pathHomotopyGrantsNoAuthority : Bool
  topologicalCoherenceGrantsNoAuthority : Bool
  futureOnly : Bool
  activeNow : Bool
  executionPermission : Bool

/-- A retained normal ball remains strictly inside its source injectivity bound. -/
def NormalBallWitness (radius injectivityRadius : ℝ) : Prop :=
  0 < radius ∧ radius < injectivityRadius

/-- A finite sample set is explicitly assigned to covering vertices. -/
def FiniteIndexedCover {ι α : Type} [Fintype ι]
    (covers : ι → α → Prop)
    (samples : Finset α) : Prop :=
  ∀ point ∈ samples, ∃ index, covers index point

/-- The three pairwise edges forming the boundary of a Čech 2-simplex. -/
def TriangleBoundary {α : Type}
    (edge : α → α → Prop)
    (first second third : α) : Prop :=
  edge first second ∧ edge second third ∧ edge first third

/-- Edge-valid finite paths in a retained nerve graph. -/
def PathValid {α : Type}
    (edge : α → α → Prop) : List α → Prop
  | [] => True
  | [_] => True
  | first :: second :: rest =>
      edge first second ∧ PathValid edge (second :: rest)

/-- Two explicit finite paths have the same retained endpoints. -/
def SameEndpoints {α : Type}
    (source target : List α) : Prop :=
  ∃ start finish sourceMiddle targetMiddle,
    source = start :: sourceMiddle ++ [finish] ∧
      target = start :: targetMiddle ++ [finish]

/-- One elementary triangle contraction removes the middle vertex of a 2-simplex boundary path. -/
def TriangleContraction {α : Type}
    (edge : α → α → Prop)
    (first second third : α)
    (source target : List α) : Prop :=
  source = [first, second, third] ∧
    target = [first, third] ∧
    TriangleBoundary edge first second third

/-- Reachability in the finite nerve graph. -/
def NerveReachable {α : Type}
    (edge : α → α → Prop)
    (start finish : α) : Prop :=
  Relation.ReflTransGen edge start finish

/-- A retained normal-ball witness implies a positive source injectivity radius. -/
theorem injectivityRadius_positive_of_normalBallWitness
    {radius injectivityRadius : ℝ}
    (hball : NormalBallWitness radius injectivityRadius) :
    0 < injectivityRadius := by
  exact lt_trans hball.1 hball.2

/-- Shrinking a positive retained normal ball preserves inclusion in the source bound. -/
theorem normalBallWitness_mono
    {smaller larger injectivityRadius : ℝ}
    (hsmaller : 0 < smaller)
    (horder : smaller ≤ larger)
    (hlarger : NormalBallWitness larger injectivityRadius) :
    NormalBallWitness smaller injectivityRadius := by
  exact ⟨hsmaller, lt_of_le_of_lt horder hlarger.2⟩

/-- An explicit finite assignment proves the retained finite cover. -/
theorem finiteIndexedCover_of_assignment
    {ι α : Type} [Fintype ι]
    (covers : ι → α → Prop)
    (samples : Finset α)
    (assign : α → ι)
    (hassign : ∀ point ∈ samples, covers (assign point) point) :
    FiniteIndexedCover covers samples := by
  intro point hpoint
  exact ⟨assign point, hassign point hpoint⟩

/-- A direct nerve edge gives finite nerve reachability. -/
theorem nerveReachable_of_edge
    {α : Type}
    (edge : α → α → Prop)
    {start finish : α}
    (hedge : edge start finish) :
    NerveReachable edge start finish := by
  exact Relation.ReflTransGen.single hedge

/-- A Čech triangle boundary makes both the long and contracted paths edge-valid. -/
theorem triangleBoundary_paths_valid
    {α : Type}
    (edge : α → α → Prop)
    (first second third : α)
    (hboundary : TriangleBoundary edge first second third) :
    PathValid edge [first, second, third] ∧
      PathValid edge [first, third] := by
  rcases hboundary with ⟨hfirstSecond, hsecondThird, hfirstThird⟩
  constructor <;> simp [PathValid, hfirstSecond, hsecondThird, hfirstThird]

/-- An elementary triangle contraction preserves edge-validity. -/
theorem triangleContraction_preserves_path_validity
    {α : Type}
    (edge : α → α → Prop)
    (first second third : α)
    (source target : List α)
    (hmove : TriangleContraction edge first second third source target) :
    PathValid edge source ∧ PathValid edge target := by
  rcases hmove with ⟨rfl, rfl, hboundary⟩
  exact triangleBoundary_paths_valid edge first second third hboundary

/-- The elementary triangle contraction preserves the retained path endpoints. -/
theorem triangleContraction_preserves_endpoints
    {α : Type}
    (edge : α → α → Prop)
    (first second third : α)
    (source target : List α)
    (hmove : TriangleContraction edge first second third source target) :
    SameEndpoints source target := by
  rcases hmove with ⟨rfl, rfl, _⟩
  refine ⟨first, third, [second], [], ?_, ?_⟩ <;> simp

/-- The boundary edges of a retained 2-simplex are explicit finite topological evidence. -/
theorem cech_triangle_boundary_evidence
    {α : Type}
    (edge : α → α → Prop)
    (triangle : CechTriangle α)
    (hboundary : TriangleBoundary edge triangle.first triangle.second triangle.third) :
    edge triangle.first triangle.second ∧
      edge triangle.second triangle.third ∧
      edge triangle.first triangle.third := by
  exact hboundary

/-- Finite cover, nerve, and path-homotopy evidence grants no authority. -/
theorem finite_topological_evidence_grants_no_authority
    (certificate : FiniteCoverNerveCechPathHomotopyCertificate)
    (hnerve : certificate.nerveComplexGrantsNoAuthority = true)
    (hcech : certificate.cechOverlapGrantsNoAuthority = true)
    (hpath : certificate.pathHomotopyGrantsNoAuthority = true)
    (hcoherence : certificate.topologicalCoherenceGrantsNoAuthority = true)
    (hselection : certificate.decisionSelectionPerformed = false)
    (hexecution : certificate.executionPermission = false) :
    certificate.nerveComplexGrantsNoAuthority = true ∧
      certificate.cechOverlapGrantsNoAuthority = true ∧
      certificate.pathHomotopyGrantsNoAuthority = true ∧
      certificate.topologicalCoherenceGrantsNoAuthority = true ∧
      certificate.decisionSelectionPerformed = false ∧
      certificate.executionPermission = false := by
  exact ⟨hnerve, hcech, hpath, hcoherence, hselection, hexecution⟩

/-- The v1.14 certificate remains finite, local, read-only, future-only, and inactive. -/
theorem finite_topological_certificate_is_bounded_future_only
    (certificate : FiniteCoverNerveCechPathHomotopyCertificate)
    (hfinite : certificate.finiteComplexOnly = true)
    (hnerve : certificate.classicalNerveTheoremNotClaimed = true)
    (hequiv : certificate.coverHomotopyEquivalenceNotClaimed = true)
    (hglobal : certificate.globalTopologicalInvariantNotClaimed = true)
    (hreadonly : certificate.historyReadOnly = true)
    (hfuture : certificate.futureOnly = true)
    (hactive : certificate.activeNow = false)
    (hexecution : certificate.executionPermission = false) :
    certificate.finiteComplexOnly = true ∧
      certificate.classicalNerveTheoremNotClaimed = true ∧
      certificate.coverHomotopyEquivalenceNotClaimed = true ∧
      certificate.globalTopologicalInvariantNotClaimed = true ∧
      certificate.historyReadOnly = true ∧
      certificate.futureOnly = true ∧
      certificate.activeNow = false ∧
      certificate.executionPermission = false := by
  exact ⟨hfinite, hnerve, hequiv, hglobal, hreadonly, hfuture, hactive, hexecution⟩

end KUOS.PlanOS.FiniteCoverNerveCechPathHomotopyV1_14
