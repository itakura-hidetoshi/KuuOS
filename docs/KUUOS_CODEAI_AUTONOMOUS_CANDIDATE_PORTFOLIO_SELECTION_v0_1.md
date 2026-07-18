# KuuOS CodeAI Autonomous Candidate Portfolio Selection v0.1

Status: additive bounded-selection sibling

Version: v0.1

Predecessors: CodeAI Autonomous Unified Diff Candidates v0.1 and CodeAI Autonomous Structured Edit Synthesis v0.1

## 1. Purpose

This surface lets CodeAI choose exactly one generated patch candidate as the next
**independent-verification target**. It consumes a ranked portfolio produced by
either the direct structured-edit route or the provider-backed structured-edit
route, proves exact portfolio correspondence, applies a sealed admissibility
policy, and selects the least-change admissible candidate.

```text
ranked Candidate Patch-supported portfolio
  + sealed selection request
  + sealed selection policy
  -> exact portfolio correspondence check
  -> candidate admissibility filtering
  -> deterministic least-change selection
  -> one selected independent-verification target or no-selection receipt
```

Selection is intentionally narrower than verification. The selected candidate is
not treated as correct, verified, applied, executable, mergeable, or deployable.
No verification lease, patch application, repository mutation, Git effect,
deployment, secret access, or successor authority is produced.

## 2. Source portfolios

The runtime accepts either:

- an `Autonomous Unified Diff Candidates v0.1` synthesis receipt; or
- an `Autonomous Structured Edit Synthesis v0.1` receipt whose candidate list is
  the downstream unified-diff portfolio.

The source must be proposal-only, recorded, synthesized, non-empty, and still
unselected. Exactly one recognized source receipt digest field must be present.
The digest is recomputed before any candidate is evaluated.

## 3. Exact portfolio correspondence

Every candidate must be a `GeneratedUnifiedDiffCandidate` carrying:

- a positive, unique, contiguous upstream rank;
- a candidate identifier equal to the proposal identifier;
- a canonical Candidate Patch digest;
- a unified-diff artifact whose digest equals the declared artifact digest;
- positive patch-byte and changed-path counts;
- exact changed-path accounting;
- unique risk labels and unresolved-question identifiers;
- a Candidate Patch receipt with `candidate_patch_ready = true` and
  `candidate_patch_supported` disposition.

The candidate list must exactly match the source receipt's generated candidate
count, ordered candidate identifiers, and ordered candidate digests. Reordering,
substitution, duplicate ranks, duplicate identifiers, duplicate digests, or
artifact tampering blocks selection before a receipt is issued.

## 4. Selection request

The sealed request binds:

- request identifier and revision;
- exact source portfolio receipt digest;
- selection purpose `independent_verification`;
- requesting actor identifier;
- request creation epoch.

The request does not claim correctness or provide verification evidence. It
requests only bounded selection under the supplied policy.

## 5. Selection policy

The sealed policy binds:

- expected source portfolio receipt digest;
- maximum portfolio candidate count;
- maximum patch bytes per candidate;
- maximum changed paths per candidate;
- allowed and forbidden risk labels;
- whether unresolved candidate questions are forbidden;
- allowed and forbidden changed-path prefixes;
- strategy `least_change_admissible`;
- evaluation epoch and maximum request age.

A candidate is admissible only when all limits and scope constraints pass.
Forbidden risk labels remain forbidden even when also present in the allowed-label
vocabulary. A changed path must satisfy at least one allowed prefix and no
forbidden prefix.

## 6. Deterministic selection

Admissible candidates are ordered lexicographically by:

1. declared changed-path count;
2. patch size in bytes;
3. risk-label count;
4. upstream rank;
5. candidate identifier.

The first admissible candidate is selected. The key is deterministic and favors
the smallest supported change, but it is not a correctness score. If no candidate
is admissible, the kernel emits a `no_admissible_candidate` receipt and selects
nothing.

## 7. Receipt semantics

A successful receipt records:

- all evaluated candidate identifiers and digests;
- all admissible candidate identifiers;
- rejected candidates and explicit rejection reasons;
- selected candidate identifier, digest, artifact digest, upstream rank, and
  selection key;
- `candidate_selected = true`;
- `selected_for_independent_verification = true`;
- `selection_authority_consumed_by_kernel = true`.

It also records:

```text
successor_selection_authority_granted = false
verification_lease_issued = false
execution_lease_issued = false
patch_applied = false
repository_mutation_performed = false
git_ref_changed = false
selected_candidate_treated_as_correct = false
ranking_treated_as_correctness_proof = false
selection_treated_as_verification = false
```

A no-admissible receipt records the same evaluated and rejected evidence with no
selected identifier and no consumed selection authority.

## 8. Boundary table

| Boundary | Preserved meaning |
|---|---|
| ranking | advisory upstream order, not selection |
| selection | one verification target, not verification |
| verification target | candidate to test, not a passed patch |
| selected candidate | not correct, applied, committed, or merged |
| selection authority | not verification or execution authority |
| no admissible candidate | explicit no-selection, not evidence deletion |
| validation | not a correctness proof |

## 9. Formal kernel

The Lean surface proves:

- a selected route has exactly one selected candidate;
- selected count is at most one and bounded by the admissible count;
- a no-admissible route selects nothing;
- selection grants no verification, execution, merge, deployment, or secret
  authority;
- selection performs no patch, repository, Git, deployment, or secret effect;
- the selected candidate is neither treated as correct nor treated as verified.

The formal root is compiled with `warningAsError` and `sorryAsError`.

## 10. Example

`examples/codeai_autonomous_candidate_portfolio_selection_v0_1.json` is a
request/policy template. The checker replaces
`$UPSTREAM_PORTFOLIO_RECEIPT_DIGEST` with the deterministic upstream receipt
digest and seals both objects before calling the runtime.

## 11. Files

- runtime: `runtime/kuuos_codeai_autonomous_candidate_portfolio_selection_v0_1.py`
- checker: `scripts/check_codeai_autonomous_candidate_portfolio_selection_v0_1.py`
- tests: `tests/test_kuuos_codeai_autonomous_candidate_portfolio_selection_v0_1.py`
- example: `examples/codeai_autonomous_candidate_portfolio_selection_v0_1.json`
- manifest: `manifests/kuuos_codeai_autonomous_candidate_portfolio_selection_v0_1.json`
- Lean kernel: `formal/KUOS/CodeAI/AutonomousCandidatePortfolioSelectionV0_1.lean`
- Lean root: `formal/KuuOSCodeAIAutonomousCandidatePortfolioSelectionV0_1.lean`
- workflow: `.github/workflows/codeai-autonomous-candidate-portfolio-selection-v0-1.yml`

## 12. Non-goals

This version does not own:

- provider inference or candidate generation;
- verification command execution;
- verification evidence adjudication;
- candidate repair or regeneration;
- patch application or working-tree mutation;
- branch, commit, push, pull request, readiness, merge, release, or deployment;
- secret access or mutation;
- persistent truth or correctness memory.
