import artifacts.«olean-r82».CheckedChainR82

/- R83 candidate: composition of checked batch chunks.
Only previously checked candidate states are reused. A blocked left chunk
retains its first failing batch and does not inspect the appended chunk.
No live registration or proof/action authority is implied. -/
namespace KuuOSR83
open KuuOSR69 KuuOSR72 KuuOSR73 KuuOSR74 KuuOSR79 KuuOSR80 KuuOSR81 KuuOSR82
universe u v w

def appendChecked {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α)
    (prior : List (Registry κ α) × List (Batch κ α))
    (ys : List (Batch κ α)) :
    List (Registry κ α) × List (Batch κ α) :=
  match prior.2 with
  | [] =>
      let later := checkBatches (chainEnd reg prior.1) ys
      (prior.1 ++ later.1, later.2)
  | b :: bs => (prior.1, b :: (bs ++ ys))

theorem trace_append {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    {reg : Registry κ α} {xs pending : List (Batch κ α)}
    {updates : List (Registry κ α)} (h : CheckedTrace reg xs updates pending)
    (ys : List (Batch κ α)) :
    CheckedTrace reg (xs ++ ys)
      (appendChecked reg (updates, pending) ys).1
      (appendChecked reg (updates, pending) ys).2 := by
  induction h with
  | done reg =>
      exact check_batches_trace reg ys
  | hold reg b bs bad =>
      exact CheckedTrace.hold reg b (bs ++ ys) bad
  | step reg next b bs updates pending ok tail ih =>
      cases pending with
      | nil =>
          exact CheckedTrace.step reg next b (bs ++ ys)
            (updates ++ (checkBatches (chainEnd next updates) ys).1)
            (checkBatches (chainEnd next updates) ys).2 ok ih
      | cons first rest =>
          exact CheckedTrace.step reg next b (bs ++ ys)
            updates (first :: (rest ++ ys)) ok ih

theorem check_batches_append {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (xs ys : List (Batch κ α)) :
    checkBatches reg (xs ++ ys) = appendChecked reg (checkBatches reg xs) ys := by
  exact trace_deterministic (trace_append (check_batches_trace reg xs) ys)

theorem append_after_complete {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (xs ys : List (Batch κ α))
    (h : (checkBatches reg xs).2 = []) :
    checkBatches reg (xs ++ ys) =
      ((checkBatches reg xs).1 ++
          (checkBatches (chainEnd reg (checkBatches reg xs).1) ys).1,
        (checkBatches (chainEnd reg (checkBatches reg xs).1) ys).2) := by
  rw [check_batches_append reg xs ys]
  unfold appendChecked
  rw [h]

theorem append_after_hold {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (xs ys : List (Batch κ α))
    (b : Batch κ α) (bs : List (Batch κ α))
    (h : (checkBatches reg xs).2 = b :: bs) :
    checkBatches reg (xs ++ ys) = ((checkBatches reg xs).1, b :: (bs ++ ys)) := by
  rw [check_batches_append reg xs ys]
  unfold appendChecked
  rw [h]

theorem hold_append_terminal {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (xs ys : List (Batch κ α))
    (b : Batch κ α) (bs : List (Batch κ α))
    (h : (checkBatches reg xs).2 = b :: bs) :
    chainEnd reg (checkBatches reg (xs ++ ys)).1 =
      chainEnd reg (checkBatches reg xs).1 :=
  congrArg (fun p => chainEnd reg p.1) (append_after_hold reg xs ys b bs h)

theorem hold_append_cache {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (routes : List (ι × Batch κ α))
    (xs ys : List (Batch κ α)) (b : Batch κ α) (bs : List (Batch κ α))
    (h : (checkBatches reg xs).2 = b :: bs) :
    refreshChain (setRoutePlans reg routes) (checkBatches reg (xs ++ ys)).1 =
      refreshChain (setRoutePlans reg routes) (checkBatches reg xs).1 :=
  congrArg (fun p => refreshChain (setRoutePlans reg routes) p.1)
    (append_after_hold reg xs ys b bs h)

theorem hold_append_first_failure {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (xs ys : List (Batch κ α))
    (b : Batch κ α) (bs : List (Batch κ α))
    (h : (checkBatches reg xs).2 = b :: bs) :
    checkedBatch (chainEnd reg (checkBatches reg (xs ++ ys)).1) b = none ∧
      failureFlags (chainEnd reg (checkBatches reg (xs ++ ys)).1) b ≠ (false, false) := by
  rw [hold_append_terminal reg xs ys b bs h]
  have ht := check_batches_trace reg xs
  rw [h] at ht
  exact trace_first_failure ht

theorem complete_append_terminal {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (xs ys : List (Batch κ α))
    (h : (checkBatches reg xs).2 = []) :
    chainEnd reg (checkBatches reg (xs ++ ys)).1 =
      chainEnd (chainEnd reg (checkBatches reg xs).1)
        (checkBatches (chainEnd reg (checkBatches reg xs).1) ys).1 := by
  calc
    _ = chainEnd reg ((checkBatches reg xs).1 ++
        (checkBatches (chainEnd reg (checkBatches reg xs).1) ys).1) :=
      congrArg (fun p => chainEnd reg p.1) (append_after_complete reg xs ys h)
    _ = _ := chain_end_append reg (checkBatches reg xs).1
      (checkBatches (chainEnd reg (checkBatches reg xs).1) ys).1

theorem complete_append_cache {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (routes : List (ι × Batch κ α))
    (xs ys : List (Batch κ α)) (h : (checkBatches reg xs).2 = []) :
    refreshChain (setRoutePlans reg routes) (checkBatches reg (xs ++ ys)).1 =
      refreshChain (refreshChain (setRoutePlans reg routes) (checkBatches reg xs).1)
        (checkBatches (chainEnd reg (checkBatches reg xs).1) ys).1 := by
  calc
    _ = refreshChain (setRoutePlans reg routes) ((checkBatches reg xs).1 ++
        (checkBatches (chainEnd reg (checkBatches reg xs).1) ys).1) :=
      congrArg (fun p => refreshChain (setRoutePlans reg routes) p.1)
        (append_after_complete reg xs ys h)
    _ = _ := refresh_chain_append (setRoutePlans reg routes) (checkBatches reg xs).1
      (checkBatches (chainEnd reg (checkBatches reg xs).1) ys).1

theorem checked_chunks_associative {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (xs ys zs : List (Batch κ α)) :
    appendChecked reg (appendChecked reg (checkBatches reg xs) ys) zs =
      appendChecked reg (checkBatches reg xs) (ys ++ zs) := by
  calc
    _ = appendChecked reg (checkBatches reg (xs ++ ys)) zs :=
      congrArg (fun p => appendChecked reg p zs) (check_batches_append reg xs ys).symm
    _ = checkBatches reg ((xs ++ ys) ++ zs) :=
      (check_batches_append reg (xs ++ ys) zs).symm
    _ = checkBatches reg (xs ++ (ys ++ zs)) :=
      congrArg (checkBatches reg) (List.append_assoc xs ys zs)
    _ = _ := check_batches_append reg xs (ys ++ zs)

theorem actual_hold_append_cache
    (reg : Registry (String × String) Nat) (xs ys : List (Batch (String × String) Nat))
    (b : Batch (String × String) Nat) (bs : List (Batch (String × String) Nat))
    (h : (checkBatches reg xs).2 = b :: bs) :
    refreshChain (setRoutePlans reg KuuOSR77.actualRoutes) (checkBatches reg (xs ++ ys)).1 =
      refreshChain (setRoutePlans reg KuuOSR77.actualRoutes) (checkBatches reg xs).1 :=
  hold_append_cache reg KuuOSR77.actualRoutes xs ys b bs h

theorem actual_complete_append_cache
    (reg : Registry (String × String) Nat) (xs ys : List (Batch (String × String) Nat))
    (h : (checkBatches reg xs).2 = []) :
    refreshChain (setRoutePlans reg KuuOSR77.actualRoutes) (checkBatches reg (xs ++ ys)).1 =
      refreshChain (refreshChain (setRoutePlans reg KuuOSR77.actualRoutes) (checkBatches reg xs).1)
        (checkBatches (chainEnd reg (checkBatches reg xs).1) ys).1 :=
  complete_append_cache reg KuuOSR77.actualRoutes xs ys h

end KuuOSR83
