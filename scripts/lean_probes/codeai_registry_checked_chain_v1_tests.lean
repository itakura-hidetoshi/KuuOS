import artifacts.«olean-r82».CheckedChainR82

/- R82 R1 test candidate. Expected assertions, not observed results.
The runner must fail if any comparison is false. -/
namespace KuuOSR82
open KuuOSR69 KuuOSR72 KuuOSR73 KuuOSR77 KuuOSR79 KuuOSR80 KuuOSR81

set_option maxRecDepth 16384 in
set_option maxHeartbeats 12000000 in
run_cmd do
  let e : Basis Nat := ∅
  let g : Basis Nat := {∅}
  let reg : Registry Nat Nat := fun _ => none
  let routes : List (Nat × Batch Nat Nat) :=
    [(0, [(0,e),(1,e)]), (1, [(0,e)]), (2, [(0,e),(0,g)])]
  let complete : List (Batch Nat Nat) := [[], [(1,e)], [(0,e)], []]
  let t := checkBatches reg complete
  let ending := chainEnd reg t.1
  let initial := setRoutePlans reg routes
  let updated := refreshChain initial t.1
  let fresh := setRoutePlans ending routes
  let reject : List (Batch Nat Nat) := [[(1,e)], [(2,e),(1,g)], [(0,e)]]
  let stopped := checkBatches reg reject
  let stopReg := chainEnd reg stopped.1
  let dup : Batch Nat Nat := [(3,e),(3,g)]
  let dupResult := checkBatches reg [dup, [(0,e)]]
  let stoppedRows := refreshChain initial stopped.1
  let stoppedFresh := setRoutePlans stopReg routes
  let realRoutes := KuuOSR77.actualRoutes
  let some first := realRoutes.head? | throwError "R82 missing actual route"
  let some req := first.2.head? | throwError "R82 missing actual requirement"
  let realReg := KuuOSR71.observedRegistry
  let missing := fun k => if k = req.1 then none else realReg k
  let realGood := checkBatches missing [[req], []]
  let realBad := checkBatches missing [[req], [req], []]
  let realEnd := chainEnd missing realGood.1
  let realStop := chainEnd missing realBad.1
  let realInitial := setRoutePlans missing realRoutes
  let realFresh := setRoutePlans realEnd realRoutes
  let realUpdated := refreshChain realInitial realGood.1
  let realStopped := refreshChain realInitial realBad.1
  let realStoppedFresh := setRoutePlans realStop realRoutes
  let checks : List (String × Bool) := [
    ("empty_input", (checkBatches reg []).1.isEmpty && (checkBatches reg []).2.isEmpty),
    ("all_batches_accepted_including_empty", decide (t.1.length = 4) && t.2.isEmpty),
    ("exact_terminal_bindings", decide (ending 0 = some e) && decide (ending 1 = some e)),
    ("exact_suffix_and_position", decide (stopped.1.length = 1) && decide (stopped.2 = reject.drop 1)),
    ("atomic_failure_and_no_later_application", decide (stopReg 1 = some e) && decide (stopReg 2 = none) && decide (stopReg 0 = none)),
    ("existing_key_reason", decide (failureFlags stopReg [(2,e),(1,g)] = (true,false))),
    ("duplicate_reason_and_no_progress", dupResult.1.isEmpty && decide (dupResult.2 = [dup,[(0,e)]]) && decide (failureFlags reg dup = (false,true))),
    ("both_failure_flags", decide (failureFlags stopReg [(1,e),(1,g)] = (true,true))),
    ("full_cache_exact", decide (updated.map Prod.fst = fresh.map Prod.fst) && decide (updated.map Prod.snd = fresh.map Prod.snd)),
    ("prefix_cache_exact", decide (stoppedRows.map Prod.fst = stoppedFresh.map Prod.fst) && decide (stoppedRows.map Prod.snd = stoppedFresh.map Prod.snd)),
    ("frontier_exact", decide (setFrontier (presentPlans updated) = freshSetFrontier ending routes)),
    ("none_is_not_empty", decide (updated.map Prod.snd = [some ∅,some ∅,none])),
    ("actual_good_and_bad_prefixes", decide (realGood.1.length = 2) && realGood.2.isEmpty && decide (realBad.1.length = 1) && decide (realBad.2 = [[req],[]])),
    ("actual_required_binding_preserved", decide (realEnd req.1 = some req.2) && decide (realStop req.1 = some req.2)),
    ("actual_cache_exact", decide (realUpdated.map Prod.fst = realFresh.map Prod.fst) && decide (realUpdated.map Prod.snd = realFresh.map Prod.snd)),
    ("actual_hold_prefix_exact", decide (realStopped.map Prod.fst = realStoppedFresh.map Prod.fst) && decide (realStopped.map Prod.snd = realStoppedFresh.map Prod.snd)),
    ("actual_frontier_exact", decide (setFrontier (presentPlans realUpdated) = freshSetFrontier realEnd realRoutes))]
  for (name, ok) in checks do
    unless ok do throwError "R82 failed comparison: {name}"
  let payload := Lean.Json.mkObj (checks.map (fun (name, ok) => (name, Lean.toJson ok)))
  Lean.Elab.Command.liftIO <| IO.println ("KUUOS_R82_COMPUTE " ++ payload.compress)

end KuuOSR82
