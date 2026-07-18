# KuuOS CodeAI Autonomous Structured Edit Synthesis v0.1

Status: additive provider-orchestration sibling

Version: v0.1

Predecessors: AI Provider Boundary Runtime v0.1 and CodeAI Autonomous Unified Diff Candidates v0.1

## 1. Purpose

This surface closes the remaining semantic-generation gap in the CodeAI patch path.
A caller supplies one or more provider-neutral adapters. The runtime constructs a
bounded prompt packet from the user intent and a read-only repository snapshot,
invokes the adapters in deterministic adapter-id order, evaluates every raw
response through the KuuOS AI Provider Boundary, parses only governed
`CANDIDATE` JSON objects into structured edits, and forwards those edits to
Autonomous Unified Diff Candidates v0.1.

```text
supported repository observation receipt
  + sealed structured-edit synthesis request
  + read-only, path-bounded repository text snapshot
  + provider-neutral generation adapters
  + sealed synthesis policy
  + sealed Candidate Patch policy
  -> provider calls
  -> CANDIDATE / HOLD / REPAIR / REJECT / QUARANTINE
  -> governed structured edit proposals
  -> deterministic unified diff candidates
  -> Candidate Patch validation and advisory ranking
```

The runtime can therefore generate candidate diffs from intent without asking a
model to handcraft hunk syntax. It still does not select, apply, commit, push,
merge, deploy, or treat a provider response as correct.

## 2. Provider-neutral adapter contract

An adapter is a callable with three identity fields:

- `adapter_id` — unique within one synthesis evaluation;
- `provider_id` — policy-scoped provider family such as GPT, Gemini, Claude, or a local model;
- `model_id` — concrete model or routing identifier.

The callback receives one immutable mapping containing:

- the sealed synthesis request digest;
- the user intent;
- the read-only repository snapshot and its digest;
- the provider/model identity;
- the attempt index;
- a strict JSON output contract;
- explicit non-authority flags.

The callback returns one response mapping. SDK choice, authentication, network
transport, retries inside a provider client, and provider-specific rate limiting
remain outside this kernel. The kernel owns orchestration order, policy bounds,
boundary routing, response accounting, structured parsing, and downstream
candidate generation.

## 3. Raw output contract

A provider response carries:

- response and producer-session identifiers;
- response creation epoch;
- raw UTF-8 output;
- `claims_authority`;
- `hides_uncertainty`;
- `bypasses_governance`;
- `evidence_missing`.

The raw output is accepted only as a JSON object with exactly:

```json
{
  "proposal_id": "...",
  "candidate_revision": "...",
  "edits": [
    {
      "path": "relative/repository/path",
      "operation": "add | modify | delete",
      "new_content": "complete new file content or null for delete"
    }
  ],
  "risk_labels": [],
  "unresolved_candidate_questions": []
}
```

Provider output does not supply requirement traces, test-plan identifiers,
provenance lineage, producer identity, or candidate timestamps. Those fields are
bound by the sealed synthesis request and the observed response envelope.

## 4. AI Provider Boundary routing

The route order is fail-closed:

| Priority | Condition | Status | Structured proposal |
|---:|---|---|---|
| 1 | bypasses governance | `QUARANTINE` | no |
| 2 | claims authority | `REJECT` | no |
| 3 | hides uncertainty | `REPAIR` | no |
| 4 | required evidence missing | `HOLD` | no |
| 5 | stale/future response | `HOLD` | no |
| 6 | output budget exceeded | `REJECT` | no |
| 7 | malformed JSON/schema | `REPAIR` | no |
| 8 | bounded candidate material | `CANDIDATE` | yes |

Only `CANDIDATE` material may become a structured proposal. The receipt records a
digest, size, status, reason, response/session IDs, and whether a proposal was
produced. Raw provider text is not copied into the receipt.

## 5. Autonomous portfolio generation

Adapters are sorted by `adapter_id`. The runtime calls at most the minimum of:

- requested candidate count;
- policy maximum provider calls;
- number of supplied adapters.

A provider exception becomes a rejected attempt receipt and does not erase a
supported sibling attempt. Duplicate response or producer-session identifiers
reject the later attempt. Valid structured proposals are sent together to
Autonomous Unified Diff Candidates v0.1, which renders deterministic Git diffs,
runs Candidate Patch preflight, and returns the existing least-change advisory
ranking.

## 6. Repository and prompt bounds

Before any provider callback executes, the runtime validates:

- exact request and policy field sets and canonical digests;
- supported read-only source observation state;
- Candidate Patch policy correspondence to source receipt, repository, and commit;
- request freshness;
- canonical LF text and repository-relative paths;
- intent and repository snapshot byte budgets;
- allowed and forbidden provider-visible path prefixes;
- provider allowlist and unique adapter IDs;
- requested candidate and provider-call limits.

A forbidden path blocks the entire generation call before any model can observe
it. This is distinct from the Candidate Patch output-path policy, which governs
what a candidate may change.

## 7. Preserved invariants

```text
provider name != authority
raw provider output != truth
raw provider output != structured proposal
CANDIDATE != selected candidate
HOLD / REPAIR / REJECT / QUARANTINE -> no structured proposal
structured proposal != unified diff
unified diff generation != patch application
candidate ranking != candidate selection
provider call != repository mutation
provider exception != sibling evidence deletion
validation != correctness proof
```

Every receipt records false for selection, verification/execution leases, patch
application, repository/Git effects, merge, deployment, secret access, successor
authorities, provider correctness, candidate correctness, and correctness proof.
Provider inference calls are recorded explicitly rather than hidden under a
false “no external effect” claim.

## 8. Formal kernel

The Lean surface proves:

- every non-`candidate` attempt produces no structured proposal;
- candidate material is the only route that can be parsed into a proposal;
- generated candidate count is bounded by provider-call count;
- raw output and provider identity grant no authority;
- synthesis has no repository/Git/deployment/secret effect;
- synthesis claims neither correctness nor candidate selection.

The formal root is compiled with `warningAsError` and `sorryAsError`.

## 9. Files

- runtime: `runtime/kuuos_codeai_autonomous_structured_edit_synthesis_v0_1.py`
- validation/types support: `runtime/kuuos_codeai_autonomous_structured_edit_types_v0_1.py`
- provider-boundary parser: `runtime/kuuos_codeai_autonomous_structured_edit_provider_v0_1.py`
- checker: `scripts/check_codeai_autonomous_structured_edit_synthesis_v0_1.py`
- tests: `tests/test_kuuos_codeai_autonomous_structured_edit_synthesis_v0_1.py`
- example: `examples/codeai_autonomous_structured_edit_synthesis_v0_1.json`
- manifest: `manifests/kuuos_codeai_autonomous_structured_edit_synthesis_v0_1.json`
- Lean kernel: `formal/KUOS/CodeAI/AutonomousStructuredEditSynthesisV0_1.lean`
- Lean root: `formal/KuuOSCodeAIAutonomousStructuredEditSynthesisV0_1.lean`
- workflow: `.github/workflows/codeai-autonomous-structured-edit-synthesis-v0-1.yml`

## 10. Non-goals

This version does not own:

- provider credentials or secret retrieval;
- provider-specific SDK construction;
- autonomous candidate selection;
- test execution or correctness adjudication;
- patch application or working-tree mutation;
- branch, commit, push, pull-request, readiness, or merge authority;
- deployment or secret mutation;
- long-term provider output memory.

Those remain separate governed surfaces.
