# Lean→Python v0.29 — Native Belief→Decision→Plural→Wa proof-condition data bridge

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Purpose and fixed source

Canonical KuuOS parent main:
`66a9f5b2d895d2182f6ee9462f18c6a2a3832e4a`
(v0.28 merged; native Plan/Act/Observe/Verify/Learn bindings).
Lean `v4.30.0-rc2`; mathlib
`5450b53e5ddc75d46418fabb605edbf36bd0beb6`.
Append-only / tighten-only / overwrite-forbidden / same-root.

**Research goal:** connect *original Lean-proven data conditions* to actual
native Python data in the corresponding KuuOS OS. Not an arbitrary
new Wa-numerical proof, and not replacement of original Lean definitions,
runtime state machines, stored evidence, receipts, hosts or CI.

This stage adds nine files only, and source-pins sixteen original Lean/
Python blobs alongside inherited v0.27/v0.28 exact-source checks.
The source and target tree for the PR must match; the final exact HEAD
needs independent Python Runtime and all terminal Governance jobs to
succeed. Strict Lean is not invoked for Python-only edits.

## Four native modules and their status

| OS | New Python file | Original source and selected theorem-data conditions |
|---|---|---|
| BeliefOS | `kuuos_lean_python_belief_gerbe_native_binding_v0_29.py` | actual v0.3 gerbe state, last stored receipt and downstream Decision source digest; **NO_DATA** for equivalence with v0.1 `FutureOnlyBeliefCommit` |
| DecisionOS | `kuuos_lean_python_decision_native_binding_v0_29.py` | original v0.1 selected admitted option, all `ConstraintGate.admissible` values, external evidence existence, original commit-event payload, and linked gerbe receipt |
| DecisionOSPlural | `kuuos_lean_python_plural_native_binding_v0_29.py` | native typed Decision→Plural handoff; original selected consensus aggregate, exact support/opposition/worst-case bounds, exclusion of validated veto, and no truth authority |
| DecisionOSWa | `kuuos_lean_python_wa_native_binding_v0_29.py` | original typed Plural→Wa handoff, selected endorsement, false-harmony/minority/dissent fields, original source option identity and exact observed Wa/weakest floors |

All modules are importable separately and read only original source
snapshots. The shared bounded helper
`runtime/kuuos_lean_python_decision_mediator_source_v0_29.py`
wraps real v0.2/v0.3 native validators without falsely upgrading
the older edge-only `audit_os` interface to a full-source audit.

### DecisionOS — source event required

The genuine v0.1 DecisionOS state records only a hash-linked history
summary, not the complete commit payload. Its original local
`DecisionStore` ledger contains the actual original `event` with
`future_only`, `memory_overwrite` and
`decision_not_execution`, which are matched to the stored
`decision_event_digest`, index, timestamp and identity. Without a
supplied original commit event the source projection returns NO_DATA.

The original selected option is checked against the source option
field, its original option digest, its admitted ID, and the original
`_constraint_reasons`. The exact source data then form a
`DecisionOS` v0.27 `audit_witness` input. The original option's
required evidence must be **nonempty** and present in the available
evidence set; a vacuous empty set is not silently promoted to evidence
existence. Other admissible but unselected options are not certified
by this selected-candidate projection.

The native fixture carries an original gerbe v0.3 receipt, not a
typed `BeliefOS` v0.1 transition. Source hashes/lineage are compared,
but the missing formal gerbe→v0.1 refinement is NOT fabricated.

### PluralOS — exact boundary, not fabricated validated veto

The v0.27 PluralOS module described a *validated protective veto*
theorem, but the native consensus candidate normally has no validated
veto. An empty veto list is NOT a constructed `ValidatedProtectiveVeto`.

Instead v0.29 checks the actual Lean
`BroadAcceptabilityBoundary.eligible` selected consensus conditions,
with corresponding `consensusCertificate_*` theorem names:

- no validated veto blocks the selected option;
- the original support weight meets the lower floor;
- the opposition weight lies below its ceiling;
- the worst-case lower value meets its mathematical floor;
- consensus is not truth or host authority.

The three mathematical comparisons use exact `Fraction` values
converted from the already observed native finite floats.
No original `+1e-12` float tolerance is mistaken for Lean's exact
`≤` relation. The original `_adjudicate` function is rerun
read-only with its source data for local route/selection compatibility.
The `ConsensusCertificate` Lean proof fields, and unique-top evidence
for every possible external context, are NOT constructed.

### DecisionOSWa — original selected endorsement only

The module requires the original Plural→Wa source handoff and
`route=ENDORSE`; a `REPAIR`, `REOBSERVE`, `QUARANTINE`, etc.
route does not create an endorsement witness.

The original selected Wa profile digest, source-selected option,
plurality-preservation flags, false-harmony record, minority/dissent
facts, and stored finite raw Wa/weakest threshold comparisons are
checked. The existing v0.25 source-bound Wa finite extrema observer is
reused, then the existing v0.27
`DecisionOSWa.audit_witness` executes the selected Lean-derived
conditions. No score, weight, option, or history is rewritten.

### BeliefOS — retain the actual type obstruction

The original v0.3 Belief gerbe context-coherence state has its own
source-provenance, receipt history, and lineage, but is NOT the same
type as v0.1 Lean `BeliefOS.FutureOnlyBeliefCommit`. An exact
local state/receipt/Decision source check therefore returns
`NO_DATA` for this v0.1 theorem projection rather than PASS.
The result records which original fields matched.

This is a **legitimate unresolved proof/modeling obligation**, not
a failure of source integrity, a Lean impossibility theorem, or a
permission to delete the existing gerbe code.

## Full original fixture test

```sh
python3 scripts/check_kuuos_lean_python_native_decision_mediator_sources_v0_29.py
python3 -m unittest -v tests.lean_python_extensions.test_native_decision_mediator_bindings_v0_29
python3 -m unittest -v tests.lean_python_extensions.test_native_decision_mediator_sources_v0_29
```

Uses original `build_native_full_cycle_receipt` and original
`DecisionStore(root/decision)._read_ledger()` from an isolated
temporary fixture. Original KuuOS code validates the full cycle
independently. No monkey-patched fake-positive source validators.
Negative tests modify *copies* of original states or events and require
BLOCKED/NO_DATA. The original fixture receipt and decision ledger bytes
must remain unchanged after the new auditors run.

## Remaining boundaries and next goal

Neither an exact Python contract nor a source-linked receipt provides
a Lean proof term, universal CPython semantics, external issuer
authentication, generalized context descent, actual execution/host
permission, or moral/truth/clinical authority.

The remaining specialized MemoryOS/CodeAI/WORLD mappings still need
full-source typed correspondence, and the Belief gerbe v0.3→v0.1
semantic bridge remains explicitly unproven. Future work should
continue mapping actually existing OS sources, not add more Wa-only
arithmetic releases.

**Release gate:** use the exact final PR source SHA, GitHub test-merge
Git tree identity, full paginated Python Runtime/Governance receipts,
source lint and terminal workflow completed/SUCCESS. Keep the PR
Draft and DO NOT MERGE while any stage is pending or failed.
