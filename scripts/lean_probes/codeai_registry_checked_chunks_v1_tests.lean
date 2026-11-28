import artifacts.«olean-r83».CheckedChunksR83

/- R83 candidate comparisons. Equality of function-valued traces is proved
by the general theorems; concrete computations compare sampled states,
exact pending batch lists and exact route-cache projections. -/
namespace KuuOSR83
open KuuOSR69 KuuOSR72 KuuOSR73 KuuOSR77 KuuOSR79 KuuOSR80 KuuOSR81 KuuOSR82

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
  let snapshot := fun (rs : List (Registry Nat Nat)) =>
    rs.map (fun r => [r 0,r 1,r 2,r 3])
  let same := fun (a b : List (Registry Nat Nat) × List (Batch Nat Nat)) =>
    decide (snapshot a.1 = snapshot b.1) && decide (a.2 = b.2)
  let left := checkBatches reg xs
  let joined := appendChecked reg left ys
  let all := checkBatches reg (xs ++ ys)
  let stopped := checkBatches reg (xs ++ bad)
  let appended := appendChecked reg stopped zs
  let wholeStop := checkBatches reg ((xs ++ bad) ++ zs)
  let endStop := chainEnd reg stopped.1
  let endAppend := chainEnd reg appended.1
  let initial := setRoutePlans reg routes
  let fullCache := refreshChain initial all.1
  let stagedCache := refreshChain (refreshChain initial left.1)
    (checkBatches (chainEnd reg left.1) ys).1
  let stopCache := refreshChain initial stopped.1
  let appendCache := refreshChain initial appended.1
  let lAssoc := appendChecked reg (appendChecked reg left ys) zs
  let rAssoc := appendChecked reg left (ys ++ zs)
  let realRoutes := KuuOSR77.actualRoutes
  let some first := realRoutes.head? | throwError "R83 missing actual route"
  let some req := first.2.head? | throwError "R83 missing actual requirement"
  let realReg := KuuOSR71.observedRegistry
  let missing := fun k => if k = req.1 then none else realReg k
  let realLeft := checkBatches missing [[req]]
  let realJoined := appendChecked missing realLeft [[]]
  let realAll := checkBatches missing [[req],[]]
  let realBlocked := checkBatches missing [[req],[req]]
  let realAppended := appendChecked missing realBlocked [[]]
  let realWhole := checkBatches missing [[req],[req],[]]
  let realInitial := setRoutePlans missing realRoutes
  let realA := refreshChain realInitial realAppended.1
  let realB := refreshChain realInitial realWhole.1
  let realC := refreshChain realInitial realJoined.1
  let realD := refreshChain realInitial realAll.1
  let checks : List (String × Bool) := [
    ("empty_left", same (appendChecked reg (checkBatches reg []) xs) left),
    ("empty_right", same (appendChecked reg left []) left),
    ("complete_chunk_exact", same joined all),
    ("complete_terminal_bindings", decide (chainEnd reg joined.1 0 = some e) && decide (chainEnd reg joined.1 1 = some e)),
    ("failure_in_right_chunk", same (appendChecked reg left bad) stopped),
    ("blocked_append_exact", same appended wholeStop),
    ("blocked_pending_order", decide (appended.2 = bad ++ zs)),
    ("blocked_position_retained", decide (appended.1.length = stopped.1.length) && decide (appended.1.length = 2)),
    ("blocked_atomic_and_later_untouched", decide (endAppend 1 = some e) && decide (endAppend 0 = none) && decide (endAppend 2 = none) && decide (endAppend 3 = none)),
    ("blocked_reason_retained", decide (failureFlags endStop [(2,e),(1,g)] = failureFlags endAppend [(2,e),(1,g)]) && decide (failureFlags endAppend [(2,e),(1,g)] = (true,false))),
    ("complete_cache_composition", decide (fullCache.map Prod.fst = stagedCache.map Prod.fst) && decide (fullCache.map Prod.snd = stagedCache.map Prod.snd)),
    ("blocked_cache_retained", decide (stopCache.map Prod.fst = appendCache.map Prod.fst) && decide (stopCache.map Prod.snd = appendCache.map Prod.snd)),
    ("chunk_association", same lAssoc rAssoc),
    ("none_is_not_empty", decide (fullCache.map Prod.snd = [some ∅,some ∅,none])),
    ("actual_complete_cache_exact", decide (realC.map Prod.fst = realD.map Prod.fst) && decide (realC.map Prod.snd = realD.map Prod.snd) && realJoined.2.isEmpty),
    ("actual_blocked_cache_exact", decide (realA.map Prod.fst = realB.map Prod.fst) && decide (realA.map Prod.snd = realB.map Prod.snd) && decide (realAppended.2 = [[req],[]]) && decide (realAppended.1.length = 1))]
  for (name, ok) in checks do
    unless ok do throwError "R83 failed comparison: {name}"
  let payload := Lean.Json.mkObj (checks.map (fun (name, ok) => (name, Lean.toJson ok)))
  Lean.Elab.Command.liftIO <| IO.println ("KUUOS_R83_COMPUTE " ++ payload.compress)

end KuuOSR83
