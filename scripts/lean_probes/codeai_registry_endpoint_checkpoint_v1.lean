import artifacts.«olean-r84».StreamCacheR84

/- R85: carry the terminal candidate registry as well as the trace and cache.
Endpoint consistency is a necessary equality, not a certificate of origin or
cache completeness. The step uses the stored endpoint, not the old chainEnd.
Neither the candidate nor its consistency grants registration authority. -/
namespace KuuOSR85
open KuuOSR69 KuuOSR72 KuuOSR73 KuuOSR74 KuuOSR79 KuuOSR80 KuuOSR81 KuuOSR82 KuuOSR83 KuuOSR84
universe u v w

abbrev Checkpoint (ι : Type w) (κ : Type v) (α : Type u) :=
  Registry κ α × StreamState ι κ α

def liftCheckpoint {ι : Type w} {κ : Type v} {α : Type u}
    (reg : Registry κ α) (s : StreamState ι κ α) : Checkpoint ι κ α :=
  (chainEnd reg s.1.1, s)

def EndpointConsistent {ι : Type w} {κ : Type v} {α : Type u}
    (reg : Registry κ α) (p : Checkpoint ι κ α) : Prop :=
  p.1 = chainEnd reg p.2.1.1

def startCheckpoint {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (routes : List (ι × Batch κ α)) : Checkpoint ι κ α :=
  liftCheckpoint reg (startStream reg routes)

def advanceCheckpoint {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (p : Checkpoint ι κ α) (ys : List (Batch κ α)) : Checkpoint ι κ α :=
  match p.2.1.2 with
  | [] =>
      let later := checkBatches p.1 ys
      (chainEnd p.1 later.1,
        ((p.2.1.1 ++ later.1, later.2), refreshChain p.2.2 later.1))
  | b :: bs => (p.1, ((p.2.1.1, b :: (bs ++ ys)), p.2.2))

def checkpointChunks {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (p : Checkpoint ι κ α) : List (List (Batch κ α)) → Checkpoint ι κ α
  | [] => p
  | c :: cs => checkpointChunks (advanceCheckpoint p c) cs

theorem advance_checkpoint_hold {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (p : Checkpoint ι κ α) (ys : List (Batch κ α))
    (b : Batch κ α) (bs : List (Batch κ α)) (h : p.2.1.2 = b :: bs) :
    advanceCheckpoint p ys = (p.1, ((p.2.1.1, b :: (bs ++ ys)), p.2.2)) := by
  unfold advanceCheckpoint
  rw [h]

theorem advance_checkpoint_lift {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (s : StreamState ι κ α) (ys : List (Batch κ α)) :
    advanceCheckpoint (liftCheckpoint reg s) ys =
      liftCheckpoint reg (advanceStream reg s ys) := by
  cases h : s.1.2 with
  | nil =>
      rw [advance_stream_complete reg s ys h]
      simp only [advanceCheckpoint, liftCheckpoint, h]
      exact Prod.ext
        (chain_end_append reg s.1.1 (checkBatches (chainEnd reg s.1.1) ys).1).symm rfl
  | cons b bs =>
      rw [advance_stream_hold reg s ys b bs h]
      simp only [advanceCheckpoint, liftCheckpoint, h]

theorem endpoint_consistent_iff {ι : Type w} {κ : Type v} {α : Type u}
    (reg : Registry κ α) (p : Checkpoint ι κ α) :
    EndpointConsistent reg p ↔ p = liftCheckpoint reg p.2 := by
  constructor
  · intro h
    exact Prod.ext h rfl
  · intro h
    exact congrArg Prod.fst h

theorem advance_endpoint_consistent {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (p : Checkpoint ι κ α) (ys : List (Batch κ α))
    (h : EndpointConsistent reg p) : EndpointConsistent reg (advanceCheckpoint p ys) := by
  have hp := (endpoint_consistent_iff reg p).mp h
  calc
    (advanceCheckpoint p ys).1 =
        (liftCheckpoint reg (advanceStream reg p.2 ys)).1 :=
      congrArg Prod.fst ((congrArg (fun q => advanceCheckpoint q ys) hp).trans
        (advance_checkpoint_lift reg p.2 ys))
    _ = chainEnd reg (advanceStream reg p.2 ys).1.1 := rfl
    _ = chainEnd reg (advanceCheckpoint p ys).2.1.1 :=
      congrArg (fun q => chainEnd reg q.2.1.1)
        ((congrArg (fun q => advanceCheckpoint q ys) hp).trans
          (advance_checkpoint_lift reg p.2 ys)).symm

theorem checkpoint_chunks_lift {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (s : StreamState ι κ α)
    (chunks : List (List (Batch κ α))) :
    checkpointChunks (liftCheckpoint reg s) chunks =
      liftCheckpoint reg (streamChunks reg s chunks) := by
  induction chunks generalizing s with
  | nil => rfl
  | cons c cs ih =>
      change checkpointChunks (advanceCheckpoint (liftCheckpoint reg s) c) cs =
        liftCheckpoint reg (streamChunks reg (advanceStream reg s c) cs)
      rw [advance_checkpoint_lift reg s c]
      exact ih (advanceStream reg s c)

theorem checkpoint_chunks_exact {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (routes : List (ι × Batch κ α))
    (chunks : List (List (Batch κ α))) :
    checkpointChunks (startCheckpoint reg routes) chunks =
      liftCheckpoint reg (canonicalStream reg routes chunks.flatten) :=
  (checkpoint_chunks_lift reg (startStream reg routes) chunks).trans
    (congrArg (liftCheckpoint reg) (stream_chunks_exact reg routes chunks))

theorem checkpoint_terminal_exact {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (routes : List (ι × Batch κ α))
    (chunks : List (List (Batch κ α))) :
    (checkpointChunks (startCheckpoint reg routes) chunks).1 =
      chainEnd reg (checkBatches reg chunks.flatten).1 :=
  congrArg Prod.fst (checkpoint_chunks_exact reg routes chunks)

theorem checkpoint_trace_exact {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (routes : List (ι × Batch κ α))
    (chunks : List (List (Batch κ α))) :
    (checkpointChunks (startCheckpoint reg routes) chunks).2.1 =
      checkBatches reg chunks.flatten :=
  congrArg (fun p => p.2.1) (checkpoint_chunks_exact reg routes chunks)

theorem checkpoint_cache_fresh {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (routes : List (ι × Batch κ α))
    (chunks : List (List (Batch κ α))) :
    (checkpointChunks (startCheckpoint reg routes) chunks).2.2 =
      setRoutePlans (chainEnd reg (checkBatches reg chunks.flatten).1) routes :=
  (congrArg (fun p => p.2.2) (checkpoint_chunks_lift reg (startStream reg routes) chunks)).trans
    (stream_cache_fresh reg routes chunks)

theorem checkpoint_frontier_fresh {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (routes : List (ι × Batch κ α))
    (chunks : List (List (Batch κ α))) :
    setFrontier (presentPlans (checkpointChunks (startCheckpoint reg routes) chunks).2.2) =
      freshSetFrontier (chainEnd reg (checkBatches reg chunks.flatten).1) routes :=
  (congrArg (fun p => setFrontier (presentPlans p.2.2))
    (checkpoint_chunks_lift reg (startStream reg routes) chunks)).trans
    (stream_frontier_fresh reg routes chunks)

theorem checkpoint_hold_cache {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (routes : List (ι × Batch κ α))
    (xs : List (Batch κ α)) (chunks : List (List (Batch κ α)))
    (b : Batch κ α) (bs : List (Batch κ α))
    (h : (checkBatches reg xs).2 = b :: bs) :
    (checkpointChunks (liftCheckpoint reg (canonicalStream reg routes xs)) chunks).2.2 =
      (canonicalStream reg routes xs).2 :=
  (congrArg (fun p => p.2.2)
    (checkpoint_chunks_lift reg (canonicalStream reg routes xs) chunks)).trans
    (stream_hold_cache reg routes xs chunks b bs h)

theorem checkpoint_hold_suffix {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (routes : List (ι × Batch κ α))
    (xs : List (Batch κ α)) (chunks : List (List (Batch κ α)))
    (b : Batch κ α) (bs : List (Batch κ α))
    (h : (checkBatches reg xs).2 = b :: bs) :
    (checkpointChunks (liftCheckpoint reg (canonicalStream reg routes xs)) chunks).2.1.2 =
      b :: (bs ++ chunks.flatten) :=
  (congrArg (fun p => p.2.1.2)
    (checkpoint_chunks_lift reg (canonicalStream reg routes xs) chunks)).trans
    (stream_hold_suffix reg routes xs chunks b bs h)

theorem actual_checkpoint_cache_fresh
    (reg : Registry (String × String) Nat)
    (chunks : List (List (Batch (String × String) Nat))) :
    (checkpointChunks (startCheckpoint reg KuuOSR77.actualRoutes) chunks).2.2 =
      setRoutePlans (chainEnd reg (checkBatches reg chunks.flatten).1) KuuOSR77.actualRoutes :=
  checkpoint_cache_fresh reg KuuOSR77.actualRoutes chunks

theorem actual_checkpoint_frontier_fresh
    (reg : Registry (String × String) Nat)
    (chunks : List (List (Batch (String × String) Nat))) :
    setFrontier (presentPlans (checkpointChunks (startCheckpoint reg KuuOSR77.actualRoutes) chunks).2.2) =
      freshSetFrontier (chainEnd reg (checkBatches reg chunks.flatten).1) KuuOSR77.actualRoutes :=
  checkpoint_frontier_fresh reg KuuOSR77.actualRoutes chunks

end KuuOSR85
