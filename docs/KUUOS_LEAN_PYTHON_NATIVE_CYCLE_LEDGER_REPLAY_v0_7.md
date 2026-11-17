# KuuOS Lean→Python v0.7 — same-origin native full-cycle ledger replay

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Canonical branch and preserved proof status

Repository: https://github.com/itakura-hidetoshi/KuuOS
Baseline canonical main: 489f7dcc80c892965f36cf0915669283ee14f679.
Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6 remain fixed. The
Lean declarations and proofs, original OS kernels, native v1.3 fixture,
GitHub workflows, public formal root and protected PR #1558 are untouched.

The v0.6 documentation correctly noted that **its own independent
subpath tests** did not establish one full original-source witness.
A more relevant pre-existing source was then observed:
runtime/kuuos_qi_world_native_full_cycle_v1_3.py. It already
constructs and validates all eight **final** OS states in one real
native fixture run, preserving their exact lineage and state digests.
Its build_native_full_cycle_receipt() contains native_artifacts for
BeliefOSState, BeliefOSReceipt and
DecisionOS → DecisionOSPlural → DecisionOSWa → PlanOS →
ActOS → ObserveOS → VerifyOS → LearnOS.
This is an original-source runtime fixture; it is not a Lean theorem
or execution in an unconstrained real-world environment.

## What is new

The read-only entry point:

- runtime/kuuos_lean_python_native_cycle_ledger_replay_v0_7.py
- audit_native_cycle_ledger(root: pathlib.Path, native_receipt: dict)

It examines **one complete original native v1.3 fixture** and the
**actual ActOS store under the same fixture root**. The function
does not invoke a host, create a state/event/authorization,
write an artifact, repair the ledger, or mutate its arguments.
The fixture builder itself, called by the genuine native tests
before the read-only audit, runs only the repository's local bounded
host adapter and creates test store files in a TemporaryDirectory.
Do not call this routine on a live concurrently modified store.

The native full-cycle receipt includes final OS snapshots, but the
existing v1.3 constructor does not retain either raw intermediate
Wa→Plan replan activation receipt or Plan→Act plan-phase activation
receipt in native_artifacts. This difference is preserved:
NO_DATA for raw originally-issued receipt authenticity.

For deterministic **source binding** only, v0.7 reconstructs the
two receipts with the current original builders and their exact
source-pinned v1.3 fixture parameters. It requires the reconstructed
Wa receipt digest to equal the actual PlanOS state's
replan_activation_receipt_digest, and the reconstructed Plan
receipt digest to equal the actual final ActOS state's
plan_activation_receipt_digest. Source-byte drift of the original
fixture and seven dependent modules is checked separately.
Digest equality is **not** a signature, proof of issuance, or
authentication of an external authority.

Critically, Plan→Act admission is only valid for the **initial ActOS
bind snapshot**, not for the final committed ActOS snapshot. The
auditor reads actual persisted act-genesis.json, replays every applied
event in act-ledger.jsonl using the **original ActStore._recover_unlocked**
and original apply_act_event/commit digest logic, and compares the
result byte-for-byte at the parsed-data level with both the saved
snapshot and the ActOS final state in native_artifacts.
It binds genesis and final ActOS by exact act_id, lineage, mission,
source plan IDs/digests and activation receipt reference. The replay
must begin at the exact genesis and finish at commit with a recorded
effect, with event count matched to the final state.

The already integrated v0.6 typed path auditor then checks three
distinct, *connected by original state and replay evidence* segments:

1. DecisionOS → DecisionOSPlural → DecisionOSWa → PlanOS,
   with deterministic reconstruction of the Wa replan receipt.
2. PlanOS → **persisted ActOS genesis** (exact admission),
   with deterministic reconstruction of the Plan activation receipt.
3. **Persisted final ActOS** → ObserveOS → VerifyOS → LearnOS,
   using the original full-cycle artifacts and original validators.

This is a materially stronger **runtime fixture** witness than five
independently constructed positive subpaths. The persisted Act ledger
joins the initial admission and final committed effect under the same
source. It still does **not** constitute a mathematical proof of
higher descent/gluing or semantic Lean→Python refinement.

## Outcome distinctions

- NATIVE_FIXTURE_LINKS_REPLAYED: original native full-cycle validator
  succeeds, reproducible activation-reference bindings match,
  persisted Act ledger and snapshot replay match, all 3 contiguous
  segments pass all original runtime validators, and the original
  source state identities/lineage stay compatible.
- NO_DATA: required existing original native packet or local Act
  ledger files are not available.
- BLOCKED: native packet/ledger/step/state/source binding is invalid,
  the ledger cannot replay or a source/target mismatch is observed.

A runtime BLOCKED is not a Lean theorem of impossibility.
Observed contradictions override missing evidence without erasing it.
Never interpret preference or runtime compatibility as execution or
Git merge authority.

All result flags remain False:
formal_descent_certified,
lean_python_refinement_proved,
external_receipt_authenticated,
execution_authority_granted,
truth_authority_granted,
merge_authority_granted.

## Static pins, tests, independent CI

The checker scripts/check_kuuos_lean_python_native_cycle_sources_v0_7.py
validates original Git *blob bytes* for the native v1.3 builder, Act
store and kernel, Plan and Wa activation builders, the SHA primitive,
the v0.5 OS registry and v0.6 path auditor. This catches unrelated
source drift that would otherwise silently invalidate deterministic
reconstruction constants. It is not Lean elaboration or proof.

The suite tests/test_kuuos_lean_python_native_cycle_ledger_replay_v0_7.py
includes the original native full-cycle fixture and original-Act-ledger
positive join, read-only preservation, strict non-authority,
missing data, resealed substitution, bad receipt, corrupted genesis/
journal/snapshot and source-pin drift. The positive test uses **one**
full original native cycle, not five separately-generated positive
subpaths.

The v0.5 cumulative runtime checker still requires its exact
original runner registration. To preserve all older guarantees
without weakening it, v0.7 test classes are **imported additively**
by tests.test_kuuos_lean_python_os_registry_v0_5, which is already
required by the cumulative runner. The static source pin test runs
under that same registered suite. No original runner/validator is
deleted, skipped or loosened.

Run from the real repository:

~~~sh
python3 scripts/check_kuuos_lean_python_native_cycle_sources_v0_7.py
python3 -m unittest -v tests.test_kuuos_lean_python_os_registry_v0_5
python3 scripts/run_kuuos_runtime_full_check_v0_55.py
~~~

The PR's exact-head independent Governance CI, job and step logs,
genuine native tests, source/test-merge tree identity and merged
main's independent push CI must be observed before claiming
integration. Python-only code does not require Strict Lean, and its
SKIPPED status is not reported as Lean machine validation.

## Remaining obstructions

1. Native-generated deterministic receipt contents do not certify
   an external issuer's signature or the receipt's prior existence;
   the packet holds digest references rather than raw receipt objects.
2. Local bounded fixture host effects do not imply permission for
   any real-world host action, nor do they prove causal truth.
3. The complete native fixture replay is a strong scoped Python
   check, not a formal Lean descent or Python semantic refinement
   proof. The conditional interpretation of 空／縁起 stays distinct
   from the content of the Lean statements.
4. WORLD, MemoryOS, CodeAI and general arbitrary OS routing
   retain their own separate source/authority boundaries.
