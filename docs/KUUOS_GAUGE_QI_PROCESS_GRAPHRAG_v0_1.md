# KuuOS Gauge–Qi Process GraphRAG v0.1

Gauge–Qi Process GraphRAG v0.1 is a bounded, query-specific evidence-transport layer for KuuOS. It combines local gauge transport with a history-bearing Qi process tensor without turning the Context Gauge Atlas into a persistent global search graph.

```text
GraphRAG retrieval candidate != truth
query-specific evidence bundle != global context graph
local patch != universal ontology node
connection != permanent graph edge
path score != global winner
curvature != veto
holonomy != sovereign memory
Qi-history compatibility != authority
receipt != execution or clinical license
```

## 1. Position in KuuOS

```text
source documents / observations / tool receipts
        ↓
query-specific local evidence patches
        ↓
declared gauge connections and declared paths
        ↓
Gauge–Qi Process GraphRAG v0.1
        ├─ path transport and endpoint alignment
        ├─ cycle holonomy and curvature residual
        ├─ provenance and temporal consistency
        ├─ Qi process-history conditioning
        ├─ observation debt and recoverability
        └─ plurality-preserving advisory receipt
        ↓
Observe / Verify / Learn evidence
        ↓
v0.21 Replan-only activation boundary
```

The layer is downstream of the v0.13 Context Gauge Atlas and the Qi process-tensor surfaces. It does not replace either constitutional structure.

## 2. Why gauge theory is operational here

Each evidence patch has a local semantic frame. A source may use a clinical vocabulary, another an ontology vocabulary, and another a query-specific answer frame. The local vector stored in one patch is not assumed to be globally canonical.

For a declared connection from patch `u` to patch `v`, v0.1 stores a two-dimensional orthogonal transport matrix

```text
U(v <- u)
```

that transports a local vector from the source frame into the target frame. Under independent orthogonal frame changes `g(u)` and `g(v)`, the connection transforms as

```text
U'(v <- u) = g(v) U(v <- u) g(u)^T.
```

A declared path transport is the ordered product of its connections. The endpoint-alignment residual and closed-cycle holonomy residual are invariant under these local orthogonal frame changes. The runtime validates this numerically; the Lean surface proves the corresponding abstract group-valued covariance and loop-observable invariance.

This makes gauge structure more than metaphor:

- local terminology may change without changing gauge-invariant diagnostics;
- inconsistent transport can be localized to declared connections or cycles;
- nontrivial holonomy remains visible as path dependence;
- local frames do not become a universal semantic coordinate system.

## 3. Why the Qi process tensor is operational here

KuuOS treats Qi as history-bearing relational flow and the process tensor as its multi-time, non-Markov structure. v0.1 consumes a bounded Qi process window containing:

```text
process_tensor_digest
history_window_digest
history_depth
transition_continuity
memory_continuity
nonmarkov_link_density
recoverability_branching_capacity
observation_debt_pressure
intervention_residue
```

The Qi window conditions path assessment. It does not create evidence and does not grant authority.

```text
Qi compatibility may widen or narrow advisory confidence.
Qi compatibility may not promote a claim to truth.
Qi debt may request observation or repair.
Qi debt may not punish, diagnose, or veto by itself.
Recoverability describes available repair branches.
Recoverability is not permission to execute an intervention.
```

## 4. Query-specific evidence bundle

One bundle exists only for one declared query. It contains:

- `query_id`, query text, and query digest;
- finite local evidence patches;
- finite declared gauge connections;
- finite caller-declared paths;
- finite caller-declared cycles;
- one Qi process-history window;
- explicit non-authority boundaries.

The runtime performs no corpus crawl, no network call, no shortest-path search, no graph centrality calculation, no persistent global-context graph mutation, and no universal winner selection.

The caller supplies candidate paths. v0.1 evaluates all supplied paths and preserves the set of admissible paths rather than collapsing them to one universal route.

## 5. Local evidence patch

Each patch records:

```text
patch_id
context_id
evidence_digest
source_digest
local_vector[2]
relevance
source_confidence
provenance_completeness
uncertainty
observed_at
rollback_ref
```

The local vector is a conventional coordinate. The source and evidence digests are the trace anchors. A rollback reference contributes to recoverability but does not itself authorize a rollback.

## 6. Declared gauge connection

Each connection records:

```text
connection_id
source_patch
target_patch
transport[2 x 2]
overlap
confidence
provenance_digest
```

The transport matrix must be orthogonal within the runtime tolerance. `overlap` and `confidence` remain separate so semantic applicability and evidential support are not collapsed.

## 7. Path action

For every declared path `Gamma`, v0.1 computes:

```text
semantic_relevance
source_confidence
provenance_completeness
transport_reliability
endpoint_alignment_residual
temporal_consistency
qi_history_compatibility
recoverability
evidence_sufficiency
path_action
path_weight = exp(-3 * path_action)
```

The bounded action is

```text
S(Gamma) =
    0.20 * relevance_loss
  + 0.15 * source_confidence_loss
  + 0.15 * provenance_loss
  + 0.15 * transport_loss
  + 0.10 * alignment_residual
  + 0.05 * temporal_inconsistency
  + 0.10 * Qi_history_loss
  + 0.10 * irrecoverability.
```

The coefficients are a v0.1 operational policy, not a theorem and not a claim of universal calibration. Future revisions must preserve the visibility of every component rather than replacing the decomposition with an opaque scalar.

## 8. Holonomy and curvature residual

For a declared closed cycle `C`, v0.1 computes the ordered connection product

```text
H(C) = U_n ... U_2 U_1
```

and a bounded distance from the identity. This is exposed as `curvature_residual`.

```text
zero residual != truth
nonzero residual != falsehood
large residual != automatic veto
```

A nonzero residual means that the declared loop has path-dependent retained difference. It may indicate contradiction, ontology mismatch, temporal change, model residue, or a real context-dependent phenomenon. Interpretation remains an explicit downstream task.

## 9. Routes

The receipt uses the existing KuuOS advisory vocabulary:

```text
CANDIDATE
OBSERVE
HOLD
REPAIR
QUARANTINE
```

- `CANDIDATE`: all declared paths meet the bounded v0.1 evidence and action thresholds;
- `OBSERVE`: usable but one or more visible deficits remain;
- `HOLD`: observation debt or curvature is too high for promotion;
- `REPAIR`: provenance or recoverability is insufficient;
- `QUARANTINE`: a non-authority boundary was violated.

The route is not truth, proof, clinical authorization, treatment authorization, execution authority, or mission activation.

## 10. Next-observation target

v0.1 reports the largest visible deficit among:

```text
source_provenance
gauge_connection
semantic_alignment
recoverability
qi_history
cycle_curvature
```

This implements a minimal-observation orientation: identify which single category of additional observation would most directly reduce the current evidence action. It does not automatically perform the observation.

## 11. Gauge-invariance check

The demo applies independent local rotations to every patch, transforms every connection covariantly, and verifies that the following remain unchanged within numerical tolerance:

- endpoint-alignment residual;
- path action;
- closed-cycle curvature residual;
- final route and admissible-path set.

This validation is finite and numerical. It is not a substitute for the abstract Lean theorem.

## 12. Mission Cycle integration

The intended bridge is:

```text
Mission
  -> Plan declares finite evidence paths and cycles
  -> Act performs only separately licensed retrieval operations
  -> Observe creates local evidence patches and connection receipts
  -> Verify evaluates Gauge–Qi invariants and source provenance
  -> Learn records future-only evidence updates
  -> Replan may adopt the receipt as a next-plan basis
```

A v0.1 receipt does not skip `Observe`, `Verify`, `Learn`, or `Replan`. It does not add network, shell, repository, theorem, clinical, institutional, or memory-overwrite authority.

## 13. Formal surface

`formal/KUOS/GraphRAG/GaugeQiProcessGraphRAGV0_1.lean` proves:

- gauge-covariant transport along every finite declared path;
- loop holonomy changes only by conjugation;
- every conjugation-invariant loop observable is gauge invariant;
- products of bounded evidence scores remain bounded in `[0,1]`;
- query-specific locality and plurality boundaries remain explicit;
- GraphRAG, curvature, Qi history, and receipts do not grant global truth or execution authority.

## 14. Runtime validation

```bash
python -m runtime.v01_gauge_qi_process_graphrag
python scripts/check_gauge_qi_process_graphrag_v0_1.py
```

The checks cover:

- a valid two-path evidence bundle;
- independent local gauge-frame changes;
- CANDIDATE, HOLD, REPAIR, and QUARANTINE routes;
- malformed path alignment failing closed;
- digest-bearing receipt generation.

## 15. Public boundary

This v0.1 layer is a research, structural, governance, and proof-facing surface. It is not a production GraphRAG service, autonomous web retriever, universal knowledge graph, clinical decision system, diagnosis or treatment authorization system, theorem authority, or unrestricted execution engine.
