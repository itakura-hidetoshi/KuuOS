# KuuOS Lean→Python v0.17: actual local Decision witness and native receipt chain

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Baseline, new observation and boundary

Baseline canonical main is 9e1ce34bdf5f52faac28d741aa34dddda91bcba5
(v0.16, PR #3577). No original Lean statement, Python kernel/store,
prior adapter or CI runner is modified.

v0.16 already recovers the local committed Plural ledger and checks 19
Plural->Wa projections; v0.12 already checked Wa profile digests. The original
native v1.3 receipt already verifies its *internal* Decision->Plural and
Belief->Decision links. Neither check by itself compares a distinct recovered
Decision ledger with its copied Plural state and the original write-once
v0.9 native receipt. v0.17 adds that separate local witness path.

Pure checks:

    checked_apply_wa_decision_evidence_event(
        state, event, source_plural_state, source_decision_state)

    checked_local_decision_receipt_chain(
        source_decision_state, source_plural_state, evidence_record)

The first requires a committed canonical Decision state and its unchanged
original validator. It compares Decision's lineage, mission, state digest,
basis digest, committed digest, route, selected ID, admissible IDs, and exact
ordered original admissible option records/digest against Plural's source
fields. It then calls v0.16's original adapter once with finite JSON copies.
It checks those original inputs were not mutated and preserves native
APPLIED/REPLAYED/REJECTED results without attempting repair/resealing.
The existing v0.16 guard independently verifies Plural and Wa.

The second compares distinct recovered Decision and Plural states with the
*original* locally captured native_artifacts DecisionOS and DecisionOSPlural
in the original v0.9 write-once evidence record. It retains original native
v1.3 validation, original local receipt hash chain and the exact native
BeliefOSReceipt digest/version referenced by DecisionOS. A self-consistent
but jointly replaced local record may still pass: no external signature or
independently trusted issuer is verified.

## Actual native child and postflight

The v0.17 child builds the same original isolated eight-OS fixture through
v0.16, temporarily replacing only v0.16's imported pure checked evaluator.
Before each selected Wa event, it uses a fixed witness from real DecisionStore
recover(require_snapshot_match=True) on decision-genesis.json, the append-only
decision-ledger.jsonl and the original snapshot. Plural recovery remains v0.16.
All ledger writes, kernels, native receipt constructors and host routes are
unchanged. Recovery may replay earlier Decision/Plural events; guard counters
are only local child stdout and are not historical attestation.

After the v0.9 evidence record exists, the child independently recovers both
Decision and Plural and checks the complete local receipt linkage. The parent
repeats the same read-only audit on the exact untouched fixture root, compares
witness digests with the child report, and also reuses the preexisting v0.9
read-only audit. Missing upstream ledgers are NO_DATA; invalid local projection
and contradictory receipt are BLOCKED before the selected guarded Wa store
append. A prior host effect or an interrupted child is not rolled back.

The child always requires a fresh, empty, non-linked local fixture directory
and never overwrites existing ledger, snapshot or evidence record. Neither
child isolation nor two local reads establishes concurrent global consistency.

## Retained obstruction and acceptance

A matching digest authenticates **content within the local trust boundary**,
not the identity, consent or truth of external evidence issuers. Joint forgery
of the original genesis, ledger, receipt and dependent digest references is
not defeated. BeliefOSReceipt carries opaque evidence references. No full
Lean real-number to Python float refinement, global all-store-write coverage,
historical guard attestation, rollback, host/store atomicity, authority or
truth is established. A local CI SUCCESS remains a local test result only.

The new checker retains the prior 97 historical source pins and adds seven
v0.16 blob pins (104 selected original Git blobs). Seven new paths are
required and three test classes must declare unique ordinary tests. AST
presence never establishes test execution; independent CI must show executed
ID sets, zero missing/extra/skipped, exact source/test-merge Git tree equality,
then a separately successful main push Runtime and Sharded Governance.

No Lean files are modified, so Python/docs-only Strict Lean SKIPPED is not a
new Lean theorem. Protected validation-only PR #1558 remains separate and
must not be merged as part of this work.
