import Mathlib

namespace KUOS.OpenHorizon

structure CandidateLineageSourceBoundaryV029 where
  exactV027StateBound : Bool
  exactV027CheckpointBound : Bool
  missionPreserved : Bool
  lineagePreserved : Bool
  exactV028PacketBound : Bool
  exactV028ReportBound : Bool
  sourcePacketSubstituted : Bool
  stateRequired : exactV027StateBound = true
  checkpointRequired : exactV027CheckpointBound = true
  missionRequired : missionPreserved = true
  lineageRequired : lineagePreserved = true
  packetRequired : exactV028PacketBound = true
  reportRequired : exactV028ReportBound = true
  substitutionBoundary : sourcePacketSubstituted = false

namespace QiCandidateLineageBinding

theorem exact_v027_v028_lineage_is_preserved
    (s : CandidateLineageSourceBoundaryV029) :
    s.exactV027StateBound = true ∧
      s.exactV027CheckpointBound = true ∧
      s.missionPreserved = true ∧
      s.lineagePreserved = true ∧
      s.exactV028PacketBound = true ∧
      s.exactV028ReportBound = true ∧
      s.sourcePacketSubstituted = false := by
  exact ⟨s.stateRequired, s.checkpointRequired, s.missionRequired,
    s.lineageRequired, s.packetRequired, s.reportRequired,
    s.substitutionBoundary⟩

end QiCandidateLineageBinding

end KUOS.OpenHorizon
