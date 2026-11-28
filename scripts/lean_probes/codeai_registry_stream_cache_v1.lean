import artifacts.«olean-r83».CheckedChunksR83

/- R84 candidate: finite streaming of checked batch chunks with a carried
route cache. Only a successful new prefix refreshes the cache. A blocked
state preserves the entire pending suffix and does not inspect new batches.
The stream result is a pure candidate, not an authentication or authority. -/
namespace KuuOSR84
open KuuOSR69 KuuOSR72 KuuOSR73 KuuOSR74 KuuOSR79 KuuOSR80 KuuOSR81 KuuOSR82 KuuOSR83
universe u v w

abbrev TraceResult (κ : Type v) (α : Type u) :=
  List (Registry κ α) × List (Batch κ α)
abbrev RouteCache (ι : Type w) (κ : Type v) (α : Type u) :=
  List (ι × Option (Finset (κ × Basis α)))
abbrev StreamState (ι : Type w) (κ : Type v) (α : Type u) :=
  TraceResult κ α × RouteCache ι κ α

def canonicalStream {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (routes : List (ι × Batch κ α))
    (xs : List (Batch κ α)) : StreamState ι κ α :=
  let t := checkBatches reg xs
  (t, refreshChain (setRoutePlans reg routes) t.1)

def startStream {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (routes : List (ι × Batch κ α)) : StreamState ι κ α :=
  canonicalStream reg routes []

def advanceStream {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (s : StreamState ι κ α)
    (ys : List (Batch κ α)) : StreamState ι κ α :=
  match s.1.2 with
  | [] =>
      let later := checkBatches (chainEnd reg s.1.1) ys
      ((s.1.1 ++ later.1, later.2), refreshChain s.2 later.1)
  | b :: bs => ((s.1.1, b :: (bs ++ ys)), s.2)

def streamChunks {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (s : StreamState ι κ α) :
    List (List (Batch κ α)) → StreamState ι κ α
  | [] => s
  | c :: cs => streamChunks reg (advanceStream reg s c) cs

theorem advance_stream_hold {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (s : StreamState ι κ α)
    (ys : List (Batch κ α)) (b : Batch κ α) (bs : List (Batch κ α))
    (h : s.1.2 = b :: bs) :
    advanceStream reg s ys = ((s.1.1, b :: (bs ++ ys)), s.2) := by
  unfold advanceStream
  rw [h]

theorem advance_stream_complete {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (s : StreamState ι κ α)
    (ys : List (Batch κ α)) (h : s.1.2 = []) :
    advanceStream reg s ys =
      ((s.1.1 ++ (checkBatches (chainEnd reg s.1.1) ys).1,
        (checkBatches (chainEnd reg s.1.1) ys).2),
       refreshChain s.2 (checkBatches (chainEnd reg s.1.1) ys).1) := by
  unfold advanceStream
  rw [h]

theorem advance_stream_exact {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (routes : List (ι × Batch κ α))
    (xs ys : List (Batch κ α)) :
    advanceStream reg (canonicalStream reg routes xs) ys =
      canonicalStream reg routes (xs ++ ys) := by
  cases h : (checkBatches reg xs).2 with
  | nil =>
      have ha := advance_stream_complete reg (canonicalStream reg routes xs) ys h
      exact ha.trans (Prod.ext (append_after_complete reg xs ys h).symm
        (complete_append_cache reg routes xs ys h).symm)
  | cons b bs =>
      have ha := advance_stream_hold reg (canonicalStream reg routes xs) ys b bs h
      exact ha.trans (Prod.ext (append_after_hold reg xs ys b bs h).symm
        (hold_append_cache reg routes xs ys b bs h).symm)

theorem stream_chunks_append {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (s : StreamState ι κ α)
    (xs ys : List (List (Batch κ α))) :
    streamChunks reg s (xs ++ ys) =
      streamChunks reg (streamChunks reg s xs) ys := by
  induction xs generalizing s with
  | nil => rfl
  | cons c cs ih => exact ih (advanceStream reg s c)

theorem stream_chunks_from {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (routes : List (ι × Batch κ α))
    (xs : List (Batch κ α)) (chunks : List (List (Batch κ α))) :
    streamChunks reg (canonicalStream reg routes xs) chunks =
      canonicalStream reg routes (xs ++ chunks.flatten) := by
  induction chunks generalizing xs with
  | nil =>
      simp only [streamChunks, List.flatten_nil, List.append_nil]
  | cons c cs ih =>
      calc
        _ = streamChunks reg (canonicalStream reg routes (xs ++ c)) cs :=
          congrArg (fun s => streamChunks reg s cs) (advance_stream_exact reg routes xs c)
        _ = canonicalStream reg routes ((xs ++ c) ++ cs.flatten) := ih (xs ++ c)
        _ = _ := congrArg (canonicalStream reg routes) (List.append_assoc xs c cs.flatten)

theorem stream_chunks_exact {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (routes : List (ι × Batch κ α))
    (chunks : List (List (Batch κ α))) :
    streamChunks reg (startStream reg routes) chunks =
      canonicalStream reg routes chunks.flatten :=
  stream_chunks_from reg routes [] chunks

theorem stream_trace_exact {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (routes : List (ι × Batch κ α))
    (chunks : List (List (Batch κ α))) :
    (streamChunks reg (startStream reg routes) chunks).1 =
      checkBatches reg chunks.flatten :=
  congrArg (fun s => s.1) (stream_chunks_exact reg routes chunks)

theorem stream_cache_fresh {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (routes : List (ι × Batch κ α))
    (chunks : List (List (Batch κ α))) :
    (streamChunks reg (startStream reg routes) chunks).2 =
      setRoutePlans (chainEnd reg (checkBatches reg chunks.flatten).1) routes :=
  (congrArg (fun s => s.2) (stream_chunks_exact reg routes chunks)).trans
    (checked_chain_cache_exact reg routes chunks.flatten)

theorem stream_frontier_fresh {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (routes : List (ι × Batch κ α))
    (chunks : List (List (Batch κ α))) :
    setFrontier (presentPlans (streamChunks reg (startStream reg routes) chunks).2) =
      freshSetFrontier (chainEnd reg (checkBatches reg chunks.flatten).1) routes :=
  (congrArg (fun s => setFrontier (presentPlans s.2))
    (stream_chunks_exact reg routes chunks)).trans
    (checked_chain_frontier_exact reg routes chunks.flatten)

theorem stream_registry_extends {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (routes : List (ι × Batch κ α))
    (chunks : List (List (Batch κ α))) :
    RegistryExtends reg (chainEnd reg (streamChunks reg (startStream reg routes) chunks).1.1) := by
  rw [stream_trace_exact reg routes chunks]
  exact checked_chain_extends reg chunks.flatten

theorem stream_hold_cache {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (routes : List (ι × Batch κ α))
    (xs : List (Batch κ α)) (chunks : List (List (Batch κ α)))
    (b : Batch κ α) (bs : List (Batch κ α))
    (h : (checkBatches reg xs).2 = b :: bs) :
    (streamChunks reg (canonicalStream reg routes xs) chunks).2 =
      (canonicalStream reg routes xs).2 :=
  (congrArg (fun s => s.2) (stream_chunks_from reg routes xs chunks)).trans
    (hold_append_cache reg routes xs chunks.flatten b bs h)

theorem stream_hold_suffix {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (routes : List (ι × Batch κ α))
    (xs : List (Batch κ α)) (chunks : List (List (Batch κ α)))
    (b : Batch κ α) (bs : List (Batch κ α))
    (h : (checkBatches reg xs).2 = b :: bs) :
    (streamChunks reg (canonicalStream reg routes xs) chunks).1.2 =
      b :: (bs ++ chunks.flatten) :=
  (congrArg (fun s => s.1.2) (stream_chunks_from reg routes xs chunks)).trans
    (congrArg (fun t => t.2) (append_after_hold reg xs chunks.flatten b bs h))

theorem actual_stream_cache_fresh
    (reg : Registry (String × String) Nat)
    (chunks : List (List (Batch (String × String) Nat))) :
    (streamChunks reg (startStream reg KuuOSR77.actualRoutes) chunks).2 =
      setRoutePlans (chainEnd reg (checkBatches reg chunks.flatten).1) KuuOSR77.actualRoutes :=
  stream_cache_fresh reg KuuOSR77.actualRoutes chunks

theorem actual_stream_frontier_fresh
    (reg : Registry (String × String) Nat)
    (chunks : List (List (Batch (String × String) Nat))) :
    setFrontier (presentPlans (streamChunks reg (startStream reg KuuOSR77.actualRoutes) chunks).2) =
      freshSetFrontier (chainEnd reg (checkBatches reg chunks.flatten).1) KuuOSR77.actualRoutes :=
  stream_frontier_fresh reg KuuOSR77.actualRoutes chunks

end KuuOSR84
