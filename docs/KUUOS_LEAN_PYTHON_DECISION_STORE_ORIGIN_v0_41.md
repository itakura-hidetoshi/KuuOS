# Lean→Python v0.41 — original DecisionOS store origin and source Belief receipt

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Exact base and source hierarchy

Canonical GitHub repository: itakura-hidetoshi/KuuOS, main.
Parent main: 7d9396aa06ccb59f0b2359406ed58ba12d169aad (v0.40).
Lean v4.30.0-rc2; mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only / tighten-only / overwrite-forbidden / same-root.

Unchanged Lean formal scope:
formal/KUOS/DecisionOS/RelationalDeliberationKernelV0_1.lean.
Its DecisionHistory structure states that its declared commit count and
summary count coincide. It does not prove automatic correspondence to
arbitrary Python runtime states. Runtime field checks in this extension
are a selected data interpretation, not a new Lean theorem or a compiler
correctness proof.

Unchanged source implementations:
runtime/kuuos_decision_os_state_v0_1.py,
runtime/kuuos_decision_os_kernel_v0_1.py,
runtime/kuuos_decision_os_store_v0_1.py,
runtime/kuuos_decision_os_types_v0_1.py,
runtime/kuuos_belief_os_gerbe_types_v0_3.py.
Inherited v0.40/v0.39 source pins remain enforced.

## Original problem and genuine counterexample

v0.40 replays the original Plural, Wa and Plan stores and binds the supplied
original committed DecisionOS final packet to the Plural genesis, but does
not replay the original DecisionOS persisted genesis, event ledger and
snapshot.

The original DecisionStore accepts any valid DecisionOS initial state. In
the original v1.3 native fixture, the state after the first event can
replace the genesis of a separately initialized store. Replaying the
remaining original events reaches the identical DecisionOS final state.
v0.40 cannot distinguish this truncated history from the full original.
v0.41 adds an exact original-constructor genesis gate.

## Audited data and selected local obligations

The production auditor requires separately supplied original native
BeliefOSReceipt, DecisionOS final, Plural final, Wa final, Plan final, Wa
replan activation receipt, and four distinct original store roots. It does
not create a missing receipt, initialize a missing store, or change native
code or files.

For DecisionOS persisted root, capture three file byte strings:
decision-genesis.json, decision-ledger.jsonl, decision-snapshot.json.
Reject link/ancestor/traversal/nested roots. Re-run the unchanged original
DecisionStore._recover_unlocked against captured bytes, enforcing full
original native replay, finite JSON on raw input (including values shadowed
by duplicate keys), exact integer dense ledger commit indices, exact
snapshot equality and exact supplied Decision final.

Reconstruct the complete first DecisionOS state using the original
build_initial_decision_state. Parameters other than the source Belief
receipt digest are taken from the observed genesis itself; the source
digest is taken from the separately supplied BeliefOS receipt. Require
type-sensitive equality of the entire reconstructed and stored genesis.
No caller-supplied authorization can substitute for missing evidence.

On a genuinely empty original Decision history, check the selected Python
data analogue of Lean DecisionHistory: zero initial event/decision counters
and summary history, the final event count equal to actual ledger length,
and decision version, completed deliberation count, summary count and
commit-phase event count equal, with ordinal and exact commit-event digest
bindings for each summary. This is NOT a theorem of Lean→Python refinement.

Check the supplied BeliefOS receipt's locally derived receipt digest and
version, candidate route, planning support, lineage, non-authority and
future-only/no-overwrite conditions. This proves neither external issuer
authenticity nor original BeliefOS history; it checks only supplied JSON.
Then reuse unchanged v0.40 for historical Decision final→Plural genesis
and two later historical edges, and all original Plural/Wa/Plan store
origins. No simultaneous four-store snapshot is inferred.

A second read of all original Decision store files detects changes present
between observations. It cannot detect a change that was restored before
the second read, and does not establish atomic multi-store finality.

## Material source-time obstruction: retain it

In the original v1.3 fixture the source BeliefOS receipt carries the
numeric created_at_ms = 5000 while the original DecisionOS genesis carries
updated_at_ms = 1000. These literal values have an inverted numerical
order when read in a single common coordinate. **No shared causal clock
has been established for the two labels.**

The runtime therefore returns a separate
SOURCE_RECEIPT_NUMERICALLY_AFTER_DECISION_GENESIS marker and both
common_source_decision_clock_proved=false and
global_temporal_descent_proved=false. It does not silently normalize,
discard, or re-time these original inputs. Scoped structural compatibility
is not promoted to a temporal gluing claim.

## Interpretation of status

SCOPED_DECISION_ORIGIN_AND_PLURAL_WA_PLAN_COMPATIBLE:
the selected source packets, recorded Decision genesis/history, original
replay, local decision-history data conditions, staged typed edges, and
v0.40 downstream records passed the specified local checks.

BLOCKED: a contradiction was observed in the selected supplied data.
NO_DATA: required input is absent or a required committed state is not
observed. Neither conclusion proves general mathematical impossibility.

Independent exact-head Runtime/Governance CI on an unchanged five-file
additive PR is the merge gate; Strict Lean is not dispatched because
existing formal Lean source is unchanged. The actual merged main HEAD
then requires separate push Runtime, Sharded Governance and Docs success.

## Reproducibility and negative controls

From repository root:

    python3 -m scripts.check_kuuos_lean_python_decision_store_origin_sources_v0_41
    python3 -m unittest discover -s tests/lean_python_extensions -p 'test_decision_store_*v0_41.py' -v

The real v1.3 fixture is used. The test suite includes an actual native
first-event suffix counterexample and stored-file replay equality; exact
source Belief receipt tamper and re-seal cases; source time inversion;
missing original files; malformed metadata; strict commit index types;
shadowed NaN/Infinity/overflow; JSONL line endings; exact captured-byte
replay; root/path/symlink rejection; postcheck mutation; and explicit
absence of all external, proof, execution and overwrite authority.

## Retained NO_DATA / obstruction / authority limitations

The original BeliefOS gerbe store itself is NOT replayed, the externally
supplied receipt is NOT authenticated, the numerical time values are NOT
proven comparable on a causal clock, and there is no globally atomic
snapshot of four stores.

No global descent, complete Lean/Python semantic equivalence, ActOS
numeric execution witness completeness, institutional/clinical/legal
validation, truth, execution, host licensing, git/write or memory
overwrite authority is provided.

The protected validation-only PR #1558 remains Draft/Open/unmerged.
