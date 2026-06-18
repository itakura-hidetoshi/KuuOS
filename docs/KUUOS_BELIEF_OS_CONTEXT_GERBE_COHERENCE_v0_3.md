# KuuOS BeliefOS Context-Gerbe Coherence v0.3

BeliefOS v0.3 lifts v0.2 conservative context-gauge credal transport into a higher coherence layer for triple overlaps, multiple declared paths, and path-dependent local disagreement.

```text
BeliefOS v0.1
  local conditional belief
        ↓
BeliefOS v0.2
  conservative chart-to-chart credal transport
        ↓
Context Gerbe Coherence v0.14
  two-cells, higher cocycle defects, surface holonomy
        ↓
BeliefOS v0.3
  credal two-cell comparison + coherence widening
        ↓
future-only Replan basis
```

v0.3 does not globally trivialize local beliefs. It preserves disagreement between direct and composite transports as an explicit coherence defect.

## 1. Non-collapse boundary

```text
direct path != composite path
path disagreement != automatic falsehood
coherence != equality forcing
two-cell residue != veto
higher defect != prohibition
surface holonomy != sovereign memory
gerbe receipt != truth authority
gerbe receipt != execution authority
```

A path-dependent difference remains observable even when the system can still reason conventionally with the resulting belief surface.

## 2. Source authorities

v0.3 accepts only:

- digest-valid BeliefOS v0.2 transport receipts as credal transport sources;
- a digest-valid Context Gerbe Coherence v0.14 decision as the higher-overlap observation source;
- declared paths already present in v0.2 receipts.

v0.3 does not invent paths, search a graph, rank charts globally, select a universal chart, or reinterpret the v0.14 gerbe decision.

## 3. Two-cell construction

For two v0.2 transported intervals with the same source context and target context,

```text
I_p = [l_p, u_p]
I_q = [l_q, u_q]
```

the interval coherence residue is

```text
rho(I_p, I_q) = max(|l_p - l_q|, |u_p - u_q|).
```

A two-cell is recorded only when the declared paths share sufficient local support. The receipt preserves both paths and both intervals; neither is overwritten by the other.

## 4. Higher witness

When three or more declared paths connect the same source and target, v0.3 records a higher witness over path triples. The higher coherence defect is the maximum pairwise interval residue within the triple.

This is a local witness of path dependence. It is not a proof that one path is globally correct or that all paths must be made identical.

## 5. Credal hull and coherence widening

All path intervals first form the plurality-preserving hull

```text
H = [min_i l_i, max_i u_i].
```

Let

```text
d = max(
  local_two_cell_residue,
  local_higher_defect,
  source_gerbe_two_curvature,
  source_higher_cocycle_defect
).
```

The coherent envelope is

```text
C_d(H) = [max(0, H.lower - d), min(1, H.upper + d)].
```

Therefore coherence processing may preserve or widen uncertainty, but may never narrow the source hull.

```text
coherent_lower <= hull_lower
hull_upper <= coherent_upper
```

## 6. Counterevidence and plurality

The coherence receipt preserves the union of:

- source v0.2 receipt digests;
- source belief-state digests;
- declared path digests;
- evidence digests;
- counterevidence digests;
- path intervals;
- two-cell residues;
- higher witnesses;
- v0.14 gerbe decision and bundle digests;
- surface-holonomy chain digest.

Counterevidence is append-only across coherence cycles.

## 7. Route

Visible interval width and coherence defects determine the route:

```text
CANDIDATE
OBSERVE
HOLD
REPAIR
REJECT
QUARANTINE
```

A large two-cell or higher defect may lead to OBSERVE, HOLD, or REPAIR. It does not directly force REJECT or QUARANTINE.

REJECT and QUARANTINE remain inherited from explicit source-state conditions, not inferred solely from curvature or path disagreement.

## 8. Qi process history

Qi-history compatibility remains inherited from v0.2 path receipts. Path-dependent Qi differences remain local conditioning information.

```text
Qi path agreement != truth
Qi path disagreement != falsehood
Qi history != authority source
```

v0.3 does not use Qi to choose a globally privileged path.

## 9. Two Truths and Middle Way

The receipt requires:

```text
paramartha_non_reified = true
two_truths_separated = true
locality_preserved = true
plurality_preserved = true
global_trivialization_used = false
```

The Middle Way boundary avoids both:

- reification: forcing one transport path to become globally real;
- nihilistic erasure: treating path dependence as a reason to discard all conventional reasoning.

## 10. Persistent surface-holonomy store

```text
belief-gerbe-genesis.json
belief-gerbe-ledger.jsonl
belief-gerbe-snapshot.json
.belief-gerbe.lock
```

The ledger is append-only and digest chained. The snapshot is derived. Every applied coherence packet appends one surface-holonomy record. Replayed packets do not append a second record.

Recovery validates:

- packet digest;
- v0.2 receipt digests;
- v0.14 gerbe decision digest;
- receipt digest;
- state chain;
- store-commit chain;
- surface-holonomy chain;
- snapshot/ledger agreement.

## 11. v0.21 activation boundary

The coherence receipt creates a next-revision basis only.

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

The activation receipt does not grant truth, proof, clinical, institutional, tool, shell, network, graph, memory-overwrite, or execution authority.

## 12. Formal surface

The Lean surface proves:

- coherence widening preserves interval validity;
- coherent lower bound does not exceed the hull lower bound;
- coherent upper bound does not fall below the hull upper bound;
- two-cell and higher defects remain non-authoritative;
- locality and plurality remain explicit;
- global trivialization is absent;
- counterevidence count is nondecreasing;
- one surface-holonomy record is appended per coherence commit;
- Replan is required before activation;
- activation is future-only and non-overwriting.

## 13. Public boundary

This is a structural, governance, and proof-facing kernel. It is not clinical authorization, treatment authorization, theorem authority, institutional approval, global context authority, or unrestricted autonomous execution authority.
