import artifacts.«olean-r84».StreamCacheR84

/- R84 candidate comparisons. Sampled registry observations are not used
as a substitute for the general equality of function-valued traces. -/
namespace KuuOSR84
open KuuOSR69 KuuOSR72 KuuOSR73 KuuOSR77 KuuOSR79 KuuOSR80 KuuOSR81 KuuOSR82 KuuOSR83

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
  let start := startStream reg routes
  let chunks := [[],xs,ys,[],zs]
  let full := streamChunks reg start chunks
  let direct := canonicalStream reg routes chunks.flatten
  let chunked := streamChunks reg (streamChunks reg start [[],xs]) [ys,[],zs]
  let blocked := streamChunks reg start [xs,bad]
  let continued := streamChunks reg blocked [[],ys,zs]
  let blockedDirect := canonicalStream reg routes ([xs,bad,[],ys,zs]).flatten
  let snapshot := fun (rs : List (Registry Nat Nat)) =>
    rs.map (fun r => [r 0,r 1,r 2,r 3])
  let sameRows := fun (a b : RouteCache Nat Nat Nat) =>
    decide (a.map Prod.fst = b.map Prod.fst) && decide (a.map Prod.snd = b.map Prod.snd)
  let same := fun (a b : StreamState Nat Nat Nat) =>
    decide (snapshot a.1.1 = snapshot b.1.1) &&
      decide (a.1.2 = b.1.2) && sameRows a.2 b.2
  let last := chainEnd reg full.1.1
  let stop := chainEnd reg continued.1.1
  let realRoutes := KuuOSR77.actualRoutes
  let some first := realRoutes.head? | throwError "R84 missing actual route"
  let some req := first.2.head? | throwError "R84 missing actual requirement"
  let realReg := KuuOSR71.observedRegistry
  let missing := fun k => if k = req.1 then none else realReg k
  let realStart := startStream missing realRoutes
  let realChunks := [[ [req] ], [ [] ], []]
  let realFull := streamChunks missing realStart realChunks
  let realDirect := canonicalStream missing realRoutes realChunks.flatten
  let realHold := streamChunks missing realStart [[[req]],[[req]]]
  let realMore := streamChunks missing realHold [[[]]]
  let realFinal := chainEnd missing realFull.1.1
  let checks : List (String × Bool) := [
    ("empty_stream", same (streamChunks reg start []) start),
    ("empty_chunk", same (advanceStream reg start []) start),
    ("finite_stream_exact", same full direct),
    ("chunk_split_exact", same full chunked),
    ("complete_trace_length", decide (full.1.1.length = chunks.flatten.length) && full.1.2.isEmpty),
    ("complete_terminal_bindings", decide (last 0 = some e) && decide (last 1 = some e) && decide (last 3 = some e)),
    ("fresh_cache_exact", sameRows full.2 (setRoutePlans last routes)),
    ("fresh_frontier_exact", decide (setFrontier (presentPlans full.2) = freshSetFrontier last routes)),
    ("blocked_stream_exact", same continued blockedDirect),
    ("blocked_pending_suffix", decide (continued.1.2 = bad ++ ys ++ zs)),
    ("blocked_cache_unchanged", sameRows continued.2 blocked.2),
    ("blocked_position_unchanged", decide (continued.1.1.length = 2) && decide (blocked.1.1.length = continued.1.1.length)),
    ("blocked_atomic_no_later", decide (stop 1 = some e) && decide (stop 0 = none) && decide (stop 2 = none) && decide (stop 3 = none)),
    ("none_is_not_empty", decide (full.2.map Prod.snd = [some ∅,some ∅,none])),
    ("actual_stream_cache_exact", decide (realFull.2.map Prod.fst = realDirect.2.map Prod.fst) && decide (realFull.2.map Prod.snd = realDirect.2.map Prod.snd) && realFull.1.2.isEmpty && decide (realFinal req.1 = some req.2)),
    ("actual_stream_hold_and_frontier", decide (realMore.1.2 = [[req],[]]) && decide (realMore.2.map Prod.fst = realHold.2.map Prod.fst) && decide (realMore.2.map Prod.snd = realHold.2.map Prod.snd) && decide (setFrontier (presentPlans realFull.2) = freshSetFrontier realFinal realRoutes))]
  for (name, ok) in checks do
    unless ok do throwError "R84 failed comparison: {name}"
  let payload := Lean.Json.mkObj (checks.map (fun (name, ok) => (name, Lean.toJson ok)))
  Lean.Elab.Command.liftIO <| IO.println ("KUUOS_R84_COMPUTE " ++ payload.compress)

end KuuOSR84
