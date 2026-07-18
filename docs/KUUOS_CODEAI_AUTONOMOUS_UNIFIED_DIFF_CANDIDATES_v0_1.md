# KuuOS CodeAI Autonomous Unified Diff Candidates v0.1

Status: additive proposal-generation sibling

Version: v0.1

Predecessors: CodeAI Intent/Repository Observation v0.1 and CodeAI Candidate Patch v0.1

## 1. Purpose

This surface lets CodeAI produce valid Git-style unified diff candidates without
requiring the model to handcraft diff syntax. The model emits one or more
structured edit proposals. The runtime deterministically renders each proposal
as a unified diff, constructs the exact Candidate Patch v0.1 metadata, and sends
the result through the existing Candidate Patch envelope.

```text
read-only repository snapshot
  + structured add / modify / delete proposals
  + supported observation receipt
  + bounded Candidate Patch policy
  -> deterministic unified diff candidates
  -> Candidate Patch v0.1 validation receipts
  -> advisory deterministic ranking
```

The output remains proposal-only. Ranking is not selection. Generation does not
apply a patch, mutate a file, create a Git object, move a ref, or grant any
successor authority.

## 2. Why structured edits

Language models are better used for semantic edits than for manually maintaining
hunk coordinates, file markers, and path accounting. This sibling therefore
accepts complete intended file content in a small edit algebra:

- `add(path, new_content)`;
- `modify(path, new_content)`;
- `delete(path)`.

The renderer owns path ordering, `diff --git` headers, file-mode markers,
`---` / `+++` labels, hunks, byte counts, artifact digests, and changed-path
accounting. Candidate Patch v0.1 remains the independent downstream parser and
policy router.

## 3. Inputs

The runtime consumes four values:

1. a supported CodeAI Intent/Repository Observation v0.1 receipt;
2. a read-only mapping of observed repository paths to UTF-8 text;
3. a non-empty list of structured proposals;
4. a sealed CodeAI Candidate Patch v0.1 policy.

Each proposal carries:

- stable proposal, revision, producer, and producer-session identifiers;
- creation epoch and replay lineage;
- one or more unique path edits;
- requirement traces, test-plan identifiers, risk labels, and unresolved
  questions.

Text v0.1 is LF-only and must be empty or newline-terminated. Binary files,
renames, submodules, mode changes, and partial hunks are not generated.

## 4. Deterministic generation

Edits are sorted by canonical repository path before rendering. For a fixed
repository snapshot and proposal, the patch artifact, artifact digest, candidate
digest, and ranking key are deterministic.

The renderer emits:

- `new file mode 100644` for additions;
- ordinary `--- a/path` and `+++ b/path` hunks for modifications;
- `deleted file mode 100644` for deletions.

The generated Candidate Patch object explicitly records that the downstream
Candidate Patch kernel did not generate it. The synthesis receipt separately
records that this sibling generated the unified diff.

## 5. Validation and rejection

Every rendered proposal is submitted to
`build_codeai_candidate_patch_envelope`. A proposal enters the returned candidate
portfolio only when the downstream receipt has `candidate_patch_ready = true`.

The following fail closed or remain visible as proposal rejection issues:

- non-canonical or repeated paths;
- add to an observed path;
- modify or delete of an unobserved path;
- no-op modification;
- malformed text or edit fields;
- stale provenance or replay conflicts;
- path-scope, feature, byte, or changed-path budget violations;
- missing required trace/test evidence;
- unknown or handover risk labels;
- any Candidate Patch disposition other than `candidate_patch_supported`.

One rejected proposal does not erase another supported proposal. If none are
supported, the result is blocked and retains a proposal-generation receipt with
the rejection issues.

## 6. Ranking

Supported candidates are ordered by the following stable key:

1. changed-path count;
2. patch byte size;
3. risk-label count;
4. candidate identifier.

This is an advisory least-change ordering only. The receipt always records:

```text
candidate_selected = false
selection_authority_granted = false
verification_authority_granted = false
execution_authority_granted = false
```

A later selector may consume the ranked portfolio under its own explicit policy.

## 7. Preserved invariants

```text
structured edit proposal != unified diff candidate
unified diff candidate != selected patch
rank 1 != selected patch
candidate support != verification
candidate support != correctness proof
generation != patch application
repository snapshot != mutable working tree
patch artifact != Git effect authority
```

The synthesis receipt additionally fixes all repository, Git, merge, deployment,
and secret effects to false.

## 8. Implementation map

- Runtime: `runtime/kuuos_codeai_autonomous_unified_diff_candidates_v0_1.py`
- Checker: `scripts/check_codeai_autonomous_unified_diff_candidates_v0_1.py`
- Tests: `tests/test_kuuos_codeai_autonomous_unified_diff_candidates_v0_1.py`
- Example proposals: `examples/codeai_autonomous_unified_diff_candidates_v0_1.json`
- Manifest: `manifests/kuuos_codeai_autonomous_unified_diff_candidates_v0_1.json`
- Formal kernel: `formal/KUOS/CodeAI/AutonomousUnifiedDiffCandidatesV0_1.lean`
- Formal root: `formal/KuuOSCodeAIAutonomousUnifiedDiffCandidatesV0_1.lean`
- Workflow: `.github/workflows/codeai-autonomous-unified-diff-candidates-v0-1.yml`

## 9. Minimal Python use

```python
from runtime.kuuos_codeai_autonomous_unified_diff_candidates_v0_1 import (
    build_codeai_autonomous_unified_diff_candidates,
)

result = build_codeai_autonomous_unified_diff_candidates(
    source_observation_receipt=source_receipt,
    repository_files={"src/app.py": "print('old')\n"},
    proposals=[
        {
            "proposal_id": "candidate-1",
            "candidate_revision": "r1",
            "producer_id": "codeai",
            "producer_session_id": "session-1",
            "candidate_created_epoch": now,
            "edits": [
                {
                    "path": "src/app.py",
                    "operation": "modify",
                    "new_content": "print('new')\n",
                }
            ],
            "requirement_trace_ids": ["requirement:1"],
            "test_plan_ids": ["test:unit"],
            "risk_labels": ["application"],
            "unresolved_candidate_questions": [],
            "prior_candidate_digests": [],
            "prior_producer_session_ids": [],
        }
    ],
    candidate_policy=candidate_policy,
)

patch = result.candidates[0].patch_artifact
```
