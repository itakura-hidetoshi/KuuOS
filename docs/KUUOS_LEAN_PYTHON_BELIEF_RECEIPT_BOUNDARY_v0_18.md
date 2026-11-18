# KuuOS Lean→Python v0.18: local Belief gerbe receipt and upstream ledger

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Original verified baseline and added local condition

Baseline canonical main is 157841103706f31b884bb8d3d691c7cb3d4899c0
(PR #3578 v0.17). No original OS core, Lean statement, store implementation,
prior v0.1–v0.17 adapter or CI runner is changed.

v0.17 already recovers actual Decision/Plural ledgers and compares their
committed states against v0.9's unchanged write-once native receipt. It
checks the BeliefOSReceipt's copied canonical digest and the DecisionOS
source field, but does not independently recover the **actual BeliefOS
gerbe ledger** and reconstruct the receipt that its original packet
applied. v0.18 closes this selected local gap, without treating the local
ledger or its hashes as trusted external signatures.

Candidate selection: matching only the supplied Belief latest digest
would be redundant with the original native receipt and v0.17. Instead
v0.18 combines a **pre-Wa state reference check** and a **postflight
original-kernel replay of the actual Belief genesis and entire ledger**.

Pure entrypoints:

    checked_apply_wa_belief_receipt_event(
        state, event, plural, decision, belief_recovered)

    checked_local_belief_receipt_chain(
        decision, plural, belief_genesis, belief_commits,
        belief_recovered, native_evidence_record)

The first checks original validate_gerbe_state, nonempty receipt history,
last committed local Belief receipt digest, Decision source binding and
lineage before exactly one unchanged v0.17 Wa adapter call. Native
REPLAYED/REJECTED/APPLIED and diagnostic status are preserved. This occurs
at the selected Wa store boundary; it cannot undo previous OS or host effects.

The second replays every supplied actual local Belief commit through the
original apply_gerbe_packet kernel from the real genesis. It verifies
dense original commit indices, original commit schema/version, predecessor
commit and state hashes, canonical store commit digest, original packet
digest, APPLIED result, reconstructed full receipt digest and result state.
The resulting entire final state must equal the original recover result
and the **BeliefOSState** copied in the v0.9 native evidence. The exact
last reconstructed receipt object (not just its hash string) must equal
the **BeliefOSReceipt** native artifact. The original Decision/Plural,
Decision→Belief and native evidence checks from v0.17 remain in force.

## Native scope and validation

The original independent Python child uses the original v0.17 full native
fixture and the original v0.9 write-once evidence. Before its first Wa
event it calls real BeliefGerbeStore(root/belief).recover with snapshot
matching. It keeps the resulting point-in-time source fixed for the
selected Wa cycle. Its temporary adapter binding is restored after use.
After original v0.9 evidence issuance, the child recovers the original
Belief/Decision/Plural stores and reads the actual Belief genesis/ledger,
then independently replays and cross-binds the exact original record.
The parent repeats postflight and compares exact child-report digests.

Read-only replay on an already-created fixture is distinct from global
concurrent consistency. Reading original store data at different moments
is not a transaction. Child stdout counters are unsigned; hash equality
does not establish historical guard execution. A partially failed child
cannot roll back already-issued host effects or native store updates.
The original preflight forbids reusing nonempty fixture roots.

A local source can be coherently replaced along with its genesis,
ledger, snapshot, receipt and all dependent hashes. This is NOT detected
as external forgery. A local Belief receipt with matching hash does not
prove an external source, consent, correct testimony or a trusted issuer.
Source transport receipts remain opaque external references. No Lean
real-number/Python floating-point refinement, formal descent, global
truth/authority, full store-write coverage, atomicity or external
signature certification follows.

## Independent acceptance

Seven new regular files only; selected old Git blobs: v0.17's 104,
plus seven exactly pinned v0.17 files, for 111 selected original blobs.
Three ordinary new unittest classes must run in the unchanged registered
extension loader; AST declaration inventory alone is not execution.
Require exact submitted/test-merge tree, all required PR governance and
new actual test IDs SUCCESS without skips, followed by exact main merge
tree and independent push Runtime and Sharded Governance success.
Strict Lean SKIPPED for Python/docs-only is not a Lean proof. Protected
PR #1558 stays Draft/Open/unmerged.
