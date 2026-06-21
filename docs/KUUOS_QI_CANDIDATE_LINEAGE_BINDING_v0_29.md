# KuuOS Qi Candidate Lineage Binding v0.29

## Purpose

v0.29 binds each v0.28 candidate report to one exact v0.27 state and checkpoint.

```text
v0.27 finite-cycle state
+ exact checkpoint and lineage
+ v0.28 source packet
+ v0.28 plural candidate report
-> immutable lineage envelope
-> HOLD / REOBSERVE / REVIEW / TERMINATE / HANDOVER
```

This layer does not recompute the v0.28 recovery-window interval. It preserves the interval, plural candidates, counterevidence and uncertainty while making their provenance verifiable.

## Exact binding

Every envelope preserves:

- mission and lineage identifiers;
- cycle index and current source mode;
- exact v0.27 state digest;
- exact v0.27 checkpoint digest;
- exact v0.28 packet identifier and digest;
- exact v0.28 report digest;
- the complete plural candidate set;
- the current potential interval snapshot.

A packet bound to another v0.27 state is rejected. A modified report whose digest is stale is rejected.

## Review routes

The route is review-only and creates no plan activation or effect permission.

```text
v0.27 TERMINATED     -> TERMINATE
v0.27 HANDED_OVER    -> HANDOVER
v0.27 PAUSED         -> HOLD
v0.27 RENEWAL_REQUIRED -> HOLD
v0.28 review handoff -> REVIEW
v0.28 insufficient evidence -> REOBSERVE
other candidate states -> HOLD
```

`HOLD` does not close the future recovery window. It means that the current candidate report remains available for review without action activation.

## Plurality

```text
leading candidate != truth
ranked first != final conclusion
one checkpoint may retain multiple distinct reports
one source packet may be bound only once
```

Multiple reports may coexist on the same checkpoint when their source packets are distinct. This preserves reobservation and alternative candidate histories without permitting source-packet substitution.

## Persistence

The v0.29 ledger is:

```text
qi-candidate-lineage-ledger-v0-29.jsonl
```

It is append-only. An exact duplicate envelope returns `REPLAYED`. A second distinct envelope using the same v0.28 packet digest is rejected.

The stored form is an immutable body plus its canonical SHA-256 digest:

```text
{
  body: <lineage-bound candidate record>,
  body_digest: sha256(canonical(body))
}
```

## Runtime entry

```text
runtime/kuuos_qi_candidate_lineage_entry_v0_29.py
```

The entry validates the v0.27 state, v0.28 packet and v0.28 report, verifies their digest links, derives one bounded review route and returns the immutable envelope.

## Formalization

```text
KUOS.OpenHorizon.QiCandidateLineageV0_29
```

Formal surfaces prove:

- exact v0.27 state/checkpoint and v0.28 packet/report binding;
- plurality, countertrace and uncertainty preservation;
- bounded review with no activation;
- append-only replay, packet non-reuse and root non-overwrite.

## Validation

```bash
PYTHONPATH=. python scripts/run_qi_candidate_lineage_v0_29.py
PYTHONPATH=. python -m unittest -v tests.test_qi_candidate_lineage_v0_29
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true \
  build KUOS.OpenHorizon.QiCandidateLineageV0_29
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true \
  build KuuOSFormal
```

The dedicated workflow also reruns the v0.27 and v0.28 regressions.
