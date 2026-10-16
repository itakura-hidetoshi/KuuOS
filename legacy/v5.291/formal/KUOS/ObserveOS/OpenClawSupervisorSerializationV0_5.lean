import Mathlib
import KUOS.ObserveOS.OpenClawSupervisorV0_5

namespace KUOS
namespace ObserveOS

structure OpenClawSupervisorAuditSerializationBoundary where
  initialWriterUsesSharedLock : Bool
  periodicWriterUsesSharedLock : Bool
  triggeredWriterUsesSharedLock : Bool
  sharedLockSingleWriter : Bool
  initialRequired : initialWriterUsesSharedLock = true
  periodicRequired : periodicWriterUsesSharedLock = true
  triggeredRequired : triggeredWriterUsesSharedLock = true
  singleWriterRequired : sharedLockSingleWriter = true

theorem openclaw_supervisor_internal_audit_writers_share_one_lock
    (boundary : OpenClawSupervisorAuditSerializationBoundary) :
    boundary.initialWriterUsesSharedLock = true ∧
      boundary.periodicWriterUsesSharedLock = true ∧
      boundary.triggeredWriterUsesSharedLock = true ∧
      boundary.sharedLockSingleWriter = true := by
  exact ⟨boundary.initialRequired, boundary.periodicRequired,
    boundary.triggeredRequired, boundary.singleWriterRequired⟩


structure OpenClawSupervisorJsonlTailBoundary where
  tailTerminated : Bool
  parseAttempted : Bool
  tailDeferred : Bool
  unterminated : tailTerminated = false
  noParseBeforeTermination : tailTerminated = false → parseAttempted = false
  deferBeforeTermination : tailTerminated = false → tailDeferred = true

theorem openclaw_supervisor_unterminated_tail_is_deferred
    (boundary : OpenClawSupervisorJsonlTailBoundary) :
    boundary.parseAttempted = false ∧ boundary.tailDeferred = true := by
  exact ⟨boundary.noParseBeforeTermination boundary.unterminated,
    boundary.deferBeforeTermination boundary.unterminated⟩

end ObserveOS
end KUOS
