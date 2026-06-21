import Mathlib

namespace KUOS.OpenHorizon

structure QiLineagePersistenceV029 where
  appendOnly : Bool
  duplicateReplay : Bool
  packetReuse : Bool
  immutableDigest : Bool
  rootOverwrite : Bool
  appendRequired : appendOnly = true
  replayRequired : duplicateReplay = true
  reuseBoundary : packetReuse = false
  digestRequired : immutableDigest = true
  overwriteBoundary : rootOverwrite = false

namespace QiCandidateLineageBinding

theorem lineage_persistence_is_bounded (p : QiLineagePersistenceV029) :
    p.appendOnly = true ∧
      p.duplicateReplay = true ∧
      p.packetReuse = false ∧
      p.immutableDigest = true ∧
      p.rootOverwrite = false := by
  exact ⟨p.appendRequired, p.replayRequired,
    p.reuseBoundary, p.digestRequired,
    p.overwriteBoundary⟩

end QiCandidateLineageBinding

end KUOS.OpenHorizon
