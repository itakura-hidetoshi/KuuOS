# KuuOS ActOS Authority-Bound Invocation v0.1

ActOS v0.1 is the narrow bridge from a committed PlanOS `act_candidate` to one explicitly licensed, bounded v0.17 host-adapter invocation. It never converts planning, approval, or a successful host receipt into unrestricted execution authority or truth.

```text
PlanOS committed PLAN_CANDIDATE
  + Plan-phase activation receipt
  + exact act_candidate step
  + explicit Act-phase receipt
  + step authorization / human approval
  + valid v0.17 host license
  + exact read-only host projection
        ↓
ActOS v0.1 authority-bound invocation
        ↓
one v0.17 host tick / one job / one bounded slice
        ↓
canonical v0.17 host receipt
        ↓
EFFECT_RECORDED / BLOCKED / REPLAYED
        ↓
mandatory observation and verification debt
```

## 1. Role boundary

ActOS executes no operation by itself. It validates and records a single call into the already bounded cooperative host adapter v0.17.

```text
plan activation != Act authorization
Act authorization != host license
host license != successful invocation
successful invocation != truth of intended effect
host receipt != clinical / legal / institutional authority
```

The v0.17 host receipt remains the canonical lower-authority execution receipt. ActOS only adds exact upstream bindings and an append-only audit surface.

## 2. Fivefold binding

An invocation is admissible only when all five surfaces agree:

1. committed PlanOS state and Plan activation receipt;
2. exact `act_candidate` step identity and digest;
3. explicit Act-phase receipt and step authorization;
4. valid v0.17 host license and allowed operation;
5. exact v0.17 projection, source bundle, job, checkpoint, step, and operation.

Any mismatch is blocked before invocation.

## 3. Strict phases

```text
BIND
  ↓
SELECT
  ↓
AUTHORIZE
  ↓
PROJECT
  ↓
INVOKE
  ↓
VERIFY
  ↓
COMMIT
```

Phase skipping, stale state, event-index regression, time regression, digest mismatch, step substitution, operation substitution, absent approval, absent or expired license, projection mismatch, and receipt mismatch are rejected.

## 4. Selected step requirements

The selected PlanOS step must satisfy:

```text
plan route = PLAN_CANDIDATE
step_class = act_candidate
effectful = true
source option identity preserved
stop conditions nonempty
expected observation digest present
verification criterion digest present
```

Only one PlanOS step is selected per ActOS instance.

## 5. Authorization packet

The step authorization packet binds:

```text
authorization_id
plan state digest
committed plan digest
plan basis digest
plan activation receipt digest
selected step ID and digest
operation ID
operation input digest
Act-phase receipt digest
human approver / approval receipt when required
host license digest
issued and expiry times
single_use = true
```

The authorization packet cannot issue a host license and cannot widen the license allowlist, step bound, cost bound, or lease duration.

## 6. Host license and projection

ActOS delegates lower execution to v0.17 without weakening it. The existing host adapter continues to enforce:

- explicit unexpired host license;
- one job per invocation;
- one bounded slice per invocation;
- licensed operation allowlist;
- trusted executor registry;
- source bundle digest binding;
- ticket/checkpoint binding;
- read-only projection;
- duplicate invocation idempotence;
- no in-place input overwrite by default.

ActOS additionally requires the projected operation to equal the operation bound by the selected PlanOS step authorization.

## 7. Invocation result routes

### EFFECT_RECORDED

The v0.17 host adapter returned `READY`, the host tick and host receipt digests are canonical, and all source/result bindings match. This records that one licensed bounded slice was committed.

It does not establish that the intended real-world effect is true, sufficient, safe in all contexts, or complete.

### BLOCKED

The invocation was not admitted or the lower adapter returned `BLOCKED`. The source bundle remains the operative source state and no effect is inferred.

### REPLAYED

The lower adapter identified the exact invocation digest as already processed. ActOS records replay without creating a second effect record.

## 8. Observation and verification debt

After `EFFECT_RECORDED`:

```text
observation_required = true
verification_required = true
automatic_truth_promotion = false
automatic_plan_completion = false
automatic_rollback = false
```

The required observation digest and verification criterion are inherited from the selected PlanOS step. A host receipt is evidence for the next Observe phase, not a substitute for it.

## 9. Persistence

```text
act-genesis.json
act-ledger.jsonl
act-snapshot.json
.act-os.lock
```

The ledger is append-only authority. The snapshot is derived and repairable. The store provides exclusive writer locking, digest chains, fsync, atomic snapshot replacement, replay idempotence, restart reconstruction, and snapshot repair from verified ledger history.

## 10. Non-authority boundary

ActOS never grants:

```text
truth authority
final commitment authority
memory overwrite authority
clinical authority
legal authority
institutional authority
theorem authority
unrestricted tool / shell / network authority
```

The only exercised authority is the exact, temporary, operation-bounded authority already present in the external v0.17 host license.

## 11. Formal surface

The Lean surface proves:

- strict phase progression and event-index growth;
- no invocation without Plan binding, selected step, Act-phase receipt, authorization, license, and projection;
- selected executable step is an effectful `act_candidate`;
- one invocation contains at most one job and one bounded slice;
- successful receipt does not imply truth or final authority;
- replay does not duplicate an effect record;
- blocked invocation records no successful effect;
- lower authority is preserved;
- observation and verification debt remain after a recorded effect;
- commit does not overwrite memory or erase source lineage;
- append-only recovery count equals committed ActOS record count.

## 12. Public boundary

ActOS v0.1 is an execution-boundary and audit kernel. It is not medical advice, treatment authorization, legal approval, institutional authorization, theorem authority, or permission for unrestricted autonomous action.
