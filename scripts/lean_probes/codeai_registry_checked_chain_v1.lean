import artifacts.«olean-r81».FiniteChainR81

/- R82 R1 candidate. UNCHECKED: no Lean/MCP/independent CI execution.
Pure candidate construction; no live registry writes or proof/action authority.
Preserve the whole pending suffix, including the first rejected batch. -/
namespace KuuOSR82
open KuuOSR69 KuuOSR72 KuuOSR73 KuuOSR74 KuuOSR79 KuuOSR80 KuuOSR81
universe u v w

abbrev Registry (κ : Type v) (α : Type u) := κ → Option (Basis α)
abbrev Batch (κ : Type v) (α : Type u) := List (κ × Basis α)

-- Result: all successful candidate states, followed by the untouched pending suffix.
def checkBatches {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) : List (Batch κ α) →
      List (Registry κ α) × List (Batch κ α)
  | [] => ([], [])
  | b :: bs =>
      match checkedBatch reg b with
      | none => ([], b :: bs)
      | some next =>
          let rest := checkBatches next bs
          (next :: rest.1, rest.2)

-- A relational specification that distinguishes success from first failure.
inductive CheckedTrace {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α] :
    Registry κ α → List (Batch κ α) → List (Registry κ α) → List (Batch κ α) → Prop
  | done (reg : Registry κ α) : CheckedTrace reg [] [] []
  | hold (reg : Registry κ α) (b : Batch κ α) (bs : List (Batch κ α))
      (bad : checkedBatch reg b = none) : CheckedTrace reg (b :: bs) [] (b :: bs)
  | step (reg next : Registry κ α) (b : Batch κ α) (bs : List (Batch κ α))
      (updates : List (Registry κ α)) (pending : List (Batch κ α))
      (ok : checkedBatch reg b = some next)
      (tail : CheckedTrace next bs updates pending) :
      CheckedTrace reg (b :: bs) (next :: updates) pending

def PendingBlocked {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) : List (Batch κ α) → Prop
  | [] => True
  | b :: _ => checkedBatch reg b = none ∧ ¬ BatchReady reg b

-- The two flags can both be true. A duplicate existing key is not overwritten.
def failureFlags {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (b : Batch κ α) : Bool × Bool :=
  (!(b.all (fun x => decide (reg x.1 = none))), !(decide ((b.map Prod.fst).Nodup)))

-- Candidate general theorems (not certified).
theorem check_batches_trace {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (bs : List (Batch κ α)) :
    CheckedTrace reg bs (checkBatches reg bs).1 (checkBatches reg bs).2 := by
  induction bs generalizing reg with
  | nil => exact CheckedTrace.done reg
  | cons b tail ih =>
      cases h : checkedBatch reg b with
      | none =>
          simpa only [checkBatches, h] using CheckedTrace.hold reg b tail h
      | some next =>
          simpa only [checkBatches, h] using
            CheckedTrace.step reg next b tail (checkBatches next tail).1
              (checkBatches next tail).2 h (ih next)

theorem trace_deterministic {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    {reg : Registry κ α} {bs pending : List (Batch κ α)}
    {updates : List (Registry κ α)} (h : CheckedTrace reg bs updates pending) :
    checkBatches reg bs = (updates, pending) := by
  induction h with
  | done reg => rfl
  | hold reg b bs bad => simp only [checkBatches, bad]
  | step reg next b bs updates pending ok tail ih =>
      simp only [checkBatches, ok, ih]

theorem trace_registry_chain {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    {reg : Registry κ α} {bs pending : List (Batch κ α)}
    {updates : List (Registry κ α)} (h : CheckedTrace reg bs updates pending) :
    RegistryChain reg updates := by
  induction h with
  | done reg => exact True.intro
  | hold reg b bs bad => exact True.intro
  | step reg next b bs updates pending ok tail ih =>
      exact ⟨checked_batch_extends reg next b ok, ih⟩

theorem trace_suffix {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    {reg : Registry κ α} {bs pending : List (Batch κ α)}
    {updates : List (Registry κ α)} (h : CheckedTrace reg bs updates pending) :
    bs.drop updates.length = pending := by
  induction h with
  | done reg => rfl
  | hold reg b bs bad => rfl
  | step reg next b bs updates pending ok tail ih => exact ih

theorem trace_length {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    {reg : Registry κ α} {bs pending : List (Batch κ α)}
    {updates : List (Registry κ α)} (h : CheckedTrace reg bs updates pending) :
    updates.length + pending.length = bs.length := by
  induction h with
  | done reg => rfl
  | hold reg b bs bad => rfl
  | step reg next b bs updates pending ok tail ih =>
      simp only [List.length_cons]
      omega

theorem trace_pending_blocked {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    {reg : Registry κ α} {bs pending : List (Batch κ α)}
    {updates : List (Registry κ α)} (h : CheckedTrace reg bs updates pending) :
    PendingBlocked (chainEnd reg updates) pending := by
  induction h with
  | done reg => exact True.intro
  | hold reg b bs bad => exact ⟨bad, (checked_batch_hold_iff reg b).mp bad⟩
  | step reg next b bs updates pending ok tail ih => exact ih

theorem failure_flags_exact {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (b : Batch κ α) :
    failureFlags reg b = (false, false) ↔ BatchReady reg b := by
  have hb : failureFlags reg b = (false, false) ↔ batchReadyCheck reg b = true := by
    unfold failureFlags batchReadyCheck
    generalize (b.all (fun x => decide (reg x.1 = none))) = fresh
    generalize (decide ((b.map Prod.fst).Nodup)) = unique
    cases fresh <;> cases unique <;> decide
  exact hb.trans (batch_ready_check_iff reg b)

theorem trace_first_failure {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    {reg : Registry κ α} {bs : List (Batch κ α)} {updates : List (Registry κ α)}
    {b : Batch κ α} {rest : List (Batch κ α)}
    (h : CheckedTrace reg bs updates (b :: rest)) :
    checkedBatch (chainEnd reg updates) b = none ∧
      failureFlags (chainEnd reg updates) b ≠ (false, false) := by
  have hb := trace_pending_blocked h
  change checkedBatch (chainEnd reg updates) b = none ∧
    ¬ BatchReady (chainEnd reg updates) b at hb
  exact ⟨hb.1, fun hf => hb.2 ((failure_flags_exact (chainEnd reg updates) b).mp hf)⟩

-- Every accepted batch is represented in the prefix; no later batch is applied.
theorem trace_prefix_flatten {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    {reg : Registry κ α} {bs pending : List (Batch κ α)}
    {updates : List (Registry κ α)} (h : CheckedTrace reg bs updates pending) :
    checkedBatch reg ((bs.take updates.length).flatten) = some (chainEnd reg updates) := by
  induction h with
  | done reg => rfl
  | hold reg b bs bad => rfl
  | step reg next b bs updates pending ok tail ih =>
      change checkedBatch reg (b ++ (bs.take updates.length).flatten) =
        some (chainEnd next updates)
      rw [checked_batch_append, ok]
      exact ih

theorem trace_complete_flatten {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    {reg : Registry κ α} {bs pending : List (Batch κ α)}
    {updates : List (Registry κ α)} (h : CheckedTrace reg bs updates pending) :
    pending = [] → checkedBatch reg bs.flatten = some (chainEnd reg updates) := by
  induction h with
  | done reg => intro _; rfl
  | hold reg b bs bad => intro hn; cases hn
  | step reg next b bs updates pending ok tail ih =>
      intro hn
      change checkedBatch reg (b ++ bs.flatten) = some (chainEnd next updates)
      rw [checked_batch_append, ok]
      exact ih hn

theorem checked_chain_extends {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (bs : List (Batch κ α)) :
    RegistryExtends reg (chainEnd reg (checkBatches reg bs).1) :=
  chain_end_extends reg (checkBatches reg bs).1 (trace_registry_chain (check_batches_trace reg bs))

theorem checked_chain_cache_exact {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (routes : List (ι × Batch κ α)) (bs : List (Batch κ α)) :
    refreshChain (setRoutePlans reg routes) (checkBatches reg bs).1 =
      setRoutePlans (chainEnd reg (checkBatches reg bs).1) routes :=
  refresh_chain_exact reg routes (checkBatches reg bs).1
    (trace_registry_chain (check_batches_trace reg bs))

theorem checked_chain_one_shot {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (routes : List (ι × Batch κ α)) (bs : List (Batch κ α)) :
    refreshChain (setRoutePlans reg routes) (checkBatches reg bs).1 =
      refreshSetCache (chainEnd reg (checkBatches reg bs).1) (setRoutePlans reg routes) :=
  refresh_chain_one_shot reg routes (checkBatches reg bs).1
    (trace_registry_chain (check_batches_trace reg bs))

theorem checked_chain_frontier_exact {ι : Type w} {κ : Type v} {α : Type u}
    [DecidableEq κ] [DecidableEq α]
    (reg : Registry κ α) (routes : List (ι × Batch κ α)) (bs : List (Batch κ α)) :
    setFrontier (presentPlans (refreshChain (setRoutePlans reg routes) (checkBatches reg bs).1)) =
      freshSetFrontier (chainEnd reg (checkBatches reg bs).1) routes :=
  refresh_chain_frontier_exact reg routes (checkBatches reg bs).1
    (trace_registry_chain (check_batches_trace reg bs))

-- Real-data route specializations; input registries remain counterfactual candidates.
theorem actual_checked_chain_cache_exact
    (reg : Registry (String × String) Nat) (bs : List (Batch (String × String) Nat)) :
    refreshChain (setRoutePlans reg KuuOSR77.actualRoutes) (checkBatches reg bs).1 =
      setRoutePlans (chainEnd reg (checkBatches reg bs).1) KuuOSR77.actualRoutes :=
  checked_chain_cache_exact reg KuuOSR77.actualRoutes bs

theorem actual_checked_chain_frontier_exact
    (reg : Registry (String × String) Nat) (bs : List (Batch (String × String) Nat)) :
    setFrontier (presentPlans (refreshChain (setRoutePlans reg KuuOSR77.actualRoutes)
      (checkBatches reg bs).1)) =
      freshSetFrontier (chainEnd reg (checkBatches reg bs).1) KuuOSR77.actualRoutes :=
  checked_chain_frontier_exact reg KuuOSR77.actualRoutes bs

end KuuOSR82
