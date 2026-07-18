# KuuOS VerifyOS Outcome Disposition Handoff v0.1

## Status

This package defines **VerifyOS v0.15** as a read-only handoff from a completed
VerifyOS v0.14 independent-evidence verification receipt to a governed outcome
disposition candidate.

It does not perform WORLD adoption, WORLD rejection, WORLD mutation, policy
activation, observation execution, or external execution.

## Architecture

```text
ObserveOS v0.7 sequential epistemic observability envelope
  -> VerifyOS v0.13 independent verification handoff
  -> VerifyOS v0.14 independent evidence verification
  -> VerifyOS v0.15 outcome disposition handoff
  -> separate WORLD-governed review and authorization
```

## Source qualification

The source must be a canonical VerifyOS v0.14 receipt with one of the three
completed outcome dispositions:

```text
passed
failed
indeterminate
```

The source receipt must preserve the v0.14 negative boundaries: no WORLD
candidate, no current-state mutation, no truth or causality claim, and no
downstream authority grant.

## Candidate mapping

```text
passed        -> adopt candidate
failed        -> reject candidate
indeterminate -> defer candidate or reobservation candidate
```

The mapping is exact and review-bound. A mismatched request is routed to
`verification_outcome_correspondence_repair_required`.

```text
passed != WORLD adoption
failed != WORLD rejection
indeterminate != evidence deletion
verification outcome != disposition authority
```

## Request artifact

The request binds:

- canonical source verification receipt and outcome;
- requested disposition candidate;
- an external governance-authority source digest;
- disposition policy and governance-review route;
- appeal route for reject candidates;
- evidence-preservation digest and exact source evidence artifacts;
- optional reobservation scope;
- verification-debt preservation;
- requester identity and bounded validity window;
- explicit negatives for state mutation, policy activation, execution, truth,
  and causal attribution.

The authority-source digest records the basis to be reviewed. It does not grant
WORLD authority to VerifyOS.

## Independent review

The review confirms:

- reviewer independence;
- exact outcome-to-candidate correspondence;
- adequacy of the authority source for creating a candidate only;
- preservation of source evidence;
- appeal-route availability for rejection;
- preservation of open verification debt for indeterminate outcomes;
- absence of WORLD mutation, policy activation, execution, truth, and causal
  authority.

This separation follows the accountability and documented oversight emphasis of
NIST AI RMF and the entity/activity/agent provenance separation of W3C PROV-O.

## Candidate semantics

### Adopt candidate

A passed verification may prepare an adopt candidate. The candidate still
requires governance review and fresh WORLD authorization.

### Reject candidate

A failed verification may prepare a reject candidate. Source evidence remains
preserved and an appeal/review route remains bound. No automatic rejection,
rollback, or evidence deletion occurs.

### Defer candidate

An indeterminate verification may prepare a defer candidate. Verification debt
and the reobservation requirement remain open.

### Reobservation candidate

An indeterminate verification may prepare a reobservation candidate with an
explicit scope. This is not observation execution authority and does not invoke
ObserveOS.

## Fourteen dispositions

```text
adopt_disposition_candidate_prepared
reject_disposition_candidate_prepared
defer_disposition_candidate_prepared
reobservation_disposition_candidate_prepared
source_verification_receipt_repair_required
verification_outcome_correspondence_repair_required
disposition_authority_review_repair_required
evidence_preservation_repair_required
appeal_route_repair_required
verification_debt_preservation_repair_required
disposition_window_repair_required
disposition_replay_conflict_rejected
current_state_mutation_rejected
authority_escalation_rejected
```

## Replay and time bounds

The handoff binds a session, nonce, request digest, review digest, operation
digest, exact cycle digest, and prior-consumption sets. Duplicate or conflicting
reuse is rejected. Request and review durations are bounded.

## Preserved state

All routes preserve:

```text
resulting WORLD revision = source WORLD revision
source lineage subset of resulting lineage
source responsibility subset of resulting responsibility
verification debt = source verification debt
reobservation requirement = source reobservation requirement
```

Candidate routes append handoff provenance and responsibility without changing
persistent WORLD state.

## Fixed non-authority boundary

```text
outcome disposition handoff != WORLD disposition completion
WORLD disposition candidate != WORLD commit
adopt candidate != adoption authority
reject candidate != rejection authority
reobservation candidate != observation execution authority
disposition receipt != policy activation
disposition receipt != execution authority
disposition receipt != truth or causality
```

## Implementation surfaces

| Surface | Path |
|---|---|
| Runtime | `runtime/kuuos_verifyos_outcome_disposition_handoff_v0_1.py` |
| Checker | `scripts/check_verifyos_outcome_disposition_handoff_v0_1.py` |
| Manifest | `manifests/kuuos_verifyos_outcome_disposition_handoff_v0_1.json` |
| Formal kernel | `formal/KUOS/VerifyOS/OutcomeDispositionHandoffV0_15.lean` |
| Formal root | `formal/KuuOSVerifyOSV0_15.lean` |
| Structured index | `docs/VerifyOS/README.md` |
| Workflow | `.github/workflows/verifyos-outcome-disposition-handoff-v0-1.yml` |

## Validation contract

The checker exercises all fourteen candidate, repair, and rejection routes and
verifies fail-closed rejection of a tampered request digest. The dedicated
workflow also runs the cumulative Evidence Cycle checks, the strict v0.15 Lean
root, and the repository aggregate formal root.
