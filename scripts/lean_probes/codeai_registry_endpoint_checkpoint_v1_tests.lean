import artifacts.«olean-r85».EndpointCheckpointR85

/- R85 controls compare finite observations, exact suffixes, and cache
projections. The generic theorem, not the sampled observations, establishes
equality for constructed checkpoint states. -/
namespace KuuOSR85
open KuuOSR69 KuuOSR72 KuuOSR73 KuuOSR77 KuuOSR79 KuuOSR80 KuuOSR81 KuuOSR82 KuuOSR83 KuuOSR84

set_option maxRecDepth 16384 in
set_option maxHeartbeats 12000000 in
run_cmd do
  let e : Basis Nat := ∅
  let g : Basis Nat := {∅}
  let reg : Registry Nat Nat := fun _ => none
  let routes : List (Nat × Batch Nat Nat) :=
    [(0,[(0,e),(1,e)]),(1,[(0,e)]),(2,[(0,e),(0,g)])]
  let xs : List (Batch Nat Nat) := [[],[(1,e)]]
  let ys : List (Batch Nat Nat) := [[(0,e)],[]]
  let zs : List (Batch Nat Nat) := [[(3,e)]]
  let bad : List (Batch Nat Nat) := [[(2,e),(1,g)],[(0,e)]]
  let start := startCheckpoint reg routes
  let chunks := [[],xs,ys,[],zs]
  let full := checkpointChunks start chunks
  let direct := liftCheckpoint reg (canonicalStream reg routes chunks.flatten)
  let chunked := checkpointChunks (checkpointChunks start [[],xs]) [ys,[],zs]
  let blocked := checkpointChunks start [xs,bad]
  let continued := checkpointChunks blocked [[],ys,zs]
  let blockedDirect := liftCheckpoint reg (canonicalStream reg routes ([xs,bad,[],ys,zs]).flatten)
  let observe := fun (r : Registry Nat Nat) => [r 0,r 1,r 2,r 3]
  let snapshot := fun (rs : List (Registry Nat Nat)) => rs.map observe
  let sameRows := fun (a b : RouteCache Nat Nat Nat) =>
    decide (a.map Prod.fst = b.map Prod.fst) && decide (a.map Prod.snd = b.map Prod.snd)
  let same := fun (a b : Checkpoint Nat Nat Nat) =>
    decide (observe a.1 = observe b.1) &&
      decide (snapshot a.2.1.1 = snapshot b.2.1.1) &&
      decide (a.2.1.2 = b.2.1.2) && sameRows a.2.2 b.2.2
  let forged : Checkpoint Nat Nat Nat := (setBinding reg 0 e,start.2)
  let rejected := advanceCheckpoint forged [[(0,e)]]
  let admitted := advanceCheckpoint start [[(0,e)]]
  let realRoutes := KuuOSR77.actualRoutes
  let some first := realRoutes.head? | throwError "R85 missing actual route"
  let some req := first.2.head? | throwError "R85 missing actual requirement"
  let realReg := KuuOSR71.observedRegistry
  let missing := fun k => if k = req.1 then none else realReg k
  let realStart := startCheckpoint missing realRoutes
  let realChunks := [[[req]],[[]],[]]
  let realFull := checkpointChunks realStart realChunks
  let realDirect := liftCheckpoint missing (canonicalStream missing realRoutes realChunks.flatten)
  let realHold := checkpointChunks realStart [[[req]],[[req]]]
  let realMore := checkpointChunks realHold [[[]]]
  let checks : List (String × Bool) := [
    ("empty_checkpoint_stream", same (checkpointChunks start []) start),
    ("empty_checkpoint_chunk", same (advanceCheckpoint start []) start),
    ("finite_checkpoint_exact", same full direct),
    ("checkpoint_split_exact", same full chunked),
    ("terminal_consistency_observed", decide (observe full.1 = observe (chainEnd reg full.2.1.1))),
    ("terminal_bindings", decide (full.1 0 = some e) && decide (full.1 1 = some e) && decide (full.1 3 = some e)),
    ("fresh_cache_exact", sameRows full.2.2 (setRoutePlans full.1 routes)),
    ("fresh_frontier_exact", decide (setFrontier (presentPlans full.2.2) = freshSetFrontier full.1 routes)),
    ("blocked_checkpoint_exact", same continued blockedDirect),
    ("blocked_suffix_and_position", decide (continued.2.1.2 = bad ++ ys ++ zs) && decide (continued.2.1.1.length = 2)),
    ("blocked_cache_and_terminal_unchanged", sameRows continued.2.2 blocked.2.2 && decide (observe continued.1 = observe blocked.1)),
    ("blocked_atomic_no_later", decide (continued.1 1 = some e) && decide (continued.1 0 = none) && decide (continued.1 2 = none) && decide (continued.1 3 = none)),
    ("none_is_not_empty", decide (full.2.2.map Prod.snd = [some ∅,some ∅,none])),
    ("inconsistent_endpoint_changes_result", decide (forged.1 0 ≠ chainEnd reg forged.2.1.1 0) && decide (rejected.2.1.2 = [[(0,e)]]) && admitted.2.1.2.isEmpty),
    ("actual_checkpoint_cache_exact", decide (realFull.2.2.map Prod.fst = realDirect.2.2.map Prod.fst) && decide (realFull.2.2.map Prod.snd = realDirect.2.2.map Prod.snd) && decide (realFull.1 req.1 = some req.2)),
    ("actual_checkpoint_hold_and_frontier", decide (realMore.2.1.2 = [[req],[]]) && decide (realMore.2.2.map Prod.fst = realHold.2.2.map Prod.fst) && decide (realMore.2.2.map Prod.snd = realHold.2.2.map Prod.snd) && decide (setFrontier (presentPlans realFull.2.2) = freshSetFrontier realFull.1 realRoutes))]
  for (name, ok) in checks do
    unless ok do throwError "R85 failed comparison: {name}"
  let payload := Lean.Json.mkObj (checks.map (fun (name, ok) => (name, Lean.toJson ok)))
  Lean.Elab.Command.liftIO <| IO.println ("KUUOS_R85_COMPUTE " ++ payload.compress)

end KuuOSR85
