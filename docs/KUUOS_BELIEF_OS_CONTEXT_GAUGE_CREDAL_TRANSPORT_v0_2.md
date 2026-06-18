# KuuOS BeliefOS Context-Gauge Credal Transport v0.2

BeliefOS v0.2 transports committed v0.1 local belief sections between declared Context Gauge Atlas charts without turning chart overlap into graph routing, local agreement into global truth, or transport success into execution authority.

```text
local belief section != global belief
chart overlap != graph edge
transport != fact promotion
curvature != veto
cocycle defect != prohibition
holonomy != sovereign memory
transport receipt != mission activation
```

## 1. Position

```text
BeliefOS v0.1
  conditional local credal section
        ↓
Context Gauge Atlas v0.13
  declared chart overlap and local transport evidence
        ↓
BeliefOS v0.2
  conservative credal transport + plurality-preserving hull
        ↓
BeliefOS next-revision basis
        ↓
v0.21 Replan-only activation
```

v0.2 is downstream of the v0.1 BeliefOS authority boundary. It does not replace v0.1 as the canonical belief-state source and does not commit actions.

## 2. Declared local transport only

Every transition declares:

- source context;
- target context;
- a declared path supplied by the caller;
- atlas overlap;
- curvature;
- cocycle defect;
- holonomy residual;
- Qi-history compatibility;
- a transition digest.

The runtime performs no shortest-path search, no global chart ranking, no universal winner selection, and no graph centrality computation.

## 3. Conservative interval transport

For a source credal interval

```text
[l, u],  0 <= l <= u <= 1
```

and bounded transport reliability

```text
r = overlap
    * (1 - curvature)
    * (1 - cocycle_defect)
    * (1 - holonomy_residual)
    * qi_history_compatibility,
```

v0.2 transports the interval as

```text
T_r([l,u]) = [r*l, r*u + (1-r)].
```

This map is deliberately uncertainty-increasing:

```text
transported_lower <= source_lower
source_upper <= transported_upper
```

A context transition may preserve confidence, but it may not create certainty that was absent in the source section.

## 4. Plurality-preserving aggregation

For transported intervals `[l_i, u_i]`, v0.2 forms the hull

```text
[min_i l_i, max_i u_i]
```

rather than averaging sections into one falsely precise point estimate.

The receipt preserves:

- each source belief-state digest;
- each source chart and declared path;
- each transported interval;
- each reliability and residual component;
- unioned evidence and counterevidence digests;
- a conflict index;
- aggregate curvature, cocycle, holonomy, and Qi-history residuals.

Counterevidence is never dropped merely because another chart agrees with the claim.

## 5. Conflict and route

Pairwise interval separation is retained as a conflict index. The route is determined from visible aggregate width and conflict:

```text
CANDIDATE
OBSERVE
HOLD
REPAIR
REJECT
QUARANTINE
```

Curvature, cocycle defect, or holonomy residual do not directly veto a belief. They reduce transport reliability, widen the interval, and therefore may lead to OBSERVE, HOLD, or REPAIR through the ordinary uncertainty gate.

## 6. Qi process history

Qi remains a conventional, non-authoritative process surface. A transition includes a bounded Qi-history compatibility score. Low compatibility widens the transported credal interval and remains visible in the receipt.

```text
Qi-history mismatch != falsehood
Qi-history compatibility != truth
Qi transport signal != intervention license
```

## 7. Two Truths and Middle Way

Every receipt requires:

```text
paramartha_non_reified = true
two_truths_separated = true
locality_preserved = true
plurality_preserved = true
```

The Middle Way boundary rejects both:

- reification: one chart or one transport path becoming global truth;
- erasure: uncertainty or disagreement being used to deny all responsible conventional reasoning.

## 8. Persistent transport ledger

```text
belief-transport-genesis.json
belief-transport-ledger.jsonl
belief-transport-snapshot.json
.belief-transport.lock
```

The ledger is append-only and digest chained. The snapshot is a derived cache. Replayed packets do not append a second ledger record. Broken packet, receipt, state, or commit digests fail closed. Snapshot repair is allowed only from the verified ledger.

The transport state stores a holonomy chain digest so path-dependent history remains visible without becoming authority.

## 9. v0.21 activation boundary

A transport receipt produces a next-revision basis, not an active mission belief.

Activation requires:

```text
route = CANDIDATE
mission_cycle_phase = replan
mission_cycle_state_digest present
replan_receipt_digest present
next_plan_basis_digest present
future_only = true
memory_overwrite = false
```

The activation receipt does not alter v0.21 phase order or grant execution, tool, shell, network, truth, proof, clinical, institutional, or memory-overwrite authority.

## 10. Formal surface

The Lean surface proves:

- transport reliability is bounded in `[0,1]`;
- conservative transport lowers no lower-bound uncertainty and raises no upper-bound certainty;
- the transported interval remains valid;
- the hull contains every transported section;
- plurality and locality remain explicit;
- curvature and holonomy do not grant authority;
- counterevidence count is nondecreasing;
- transport history appends one holonomy record per commit;
- Replan is required before activation.

## 11. Public boundary

This implementation is a structural, governance, and proof-facing surface. It is not theorem authority, clinical authority, treatment authorization, medical-act authorization, institutional approval, global context authority, or unrestricted execution authority.
