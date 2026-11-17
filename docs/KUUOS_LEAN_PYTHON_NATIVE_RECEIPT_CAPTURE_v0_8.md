# KuuOS Lean→Python v0.8 — original native receipt return capture

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Authoritative baseline and context

Canonical repository: https://github.com/itakura-hidetoshi/KuuOS
Baseline main HEAD: 8ac05b15890abef4a866d09ef97c59d1fb672f7c.
Original Lean v4.30.0-rc2 and mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6 are preserved.
The original Lean statements, all original OS runtime kernels,
native full-cycle source, public formal root and protected draft
PR #1558 remain unchanged.

Relevant original sources:

- runtime/kuuos_qi_world_native_full_cycle_v1_3.py
- runtime/kuuos_decision_os_wa_kernel_v0_3.py
- runtime/kuuos_plan_os_kernel_v0_1.py
- runtime/kuuos_act_os_store_v0_1.py

V0.7 proved by **runtime tests**, not Lean, that the original native v1.3
fixture's eight final OS states and the original persisted ActOS ledger
could be connected under source-pinned deterministic receipt reconstruction.

## Why this next stage is needed

The original native fixture source constructs the Wa→Plan activation receipt
and Plan→Act activation receipt as genuine local function return values in
its _build_plan function, but the returned full-cycle receipt retains only
their digest references, not their raw packet objects.

Therefore v0.7 recovered deterministic packets from source-pinned
constants, which was sufficient for a local runtime binding check
but not evidence that the specific raw original return values had
actually been observed at the time the fixture was constructed.

V0.8 adds **in-process return observation** without changing original
constructors or their outputs. It deliberately does **not** claim that
a locally captured object is authenticated by an independent external
issuer. A caller can fabricate an internally consistent capture packet.

## Implemented distinction: build vs audit

New module:
runtime/kuuos_lean_python_native_cycle_receipt_capture_v0_8.py.

Function A — build_captured_native_test_fixture(root: pathlib.Path):

1. Requires an existing fresh, isolated local test folder, with no prior
   native OS fixture subdirectories. It is an **explicit test fixture
   construction action**, not read-only and not a production OS executor.
2. Temporarily wraps exactly the original native module's two original
   activation receipt functions, calls **the actual original functions**,
   copies their unmodified return values as observations, and returns
   those exact original result values to the native builder.
3. Observes exactly one Wa→Plan return, followed by one Plan→Act return.
4. Calls the original bounded native v1.3 local full-cycle constructor,
   which retains its original local file writes and bounded host
   test-adapter behavior. No additional external host effects,
   authority or write behavior is inserted.
5. Restores both original global constructor references even on an
   exception. In-process instrumentation is serialized with a local
   lock; **other threads must not call that native module while the
   temporary wrappers are installed**.
6. Returns (original_native_cycle_receipt, local_capture_packet).
   The capture packet includes full original Wa/Plan receipt payloads,
   return order, the original cycle digest and a non-cryptographic-trust
   SHA-256 integrity checksum. It does not include an external signature.

Function B — audit_captured_native_receipts(root, native_receipt, capture):

1. Performs **read-only** checks on supplied snapshots and the quiescent
   local original ActOS ledger; never re-runs or invokes a host.
2. Calls the existing v0.7 original native full-cycle/ledger replay audit;
   requires that source and original states are valid.
3. Requires exact capture fields, schema version, source cycle digest,
   checksum, exactly two returns in the original function order,
   and original receipt digest-function consistency.
4. Regenerates *reference* packets with the same original constructor
   parameters and compares **full raw packet equality** to the actual
   captured objects. Checks original PlanOS and ActOS references and
   v0.7 independently replayed digest references.
5. Rejects substitutions, changed return order, unknown fields,
   mismatched whole payloads and tampered ledger as BLOCKED, while
   missing evidence remains NO_DATA. Contradiction does not get
   erased by an unrelated missing input.

Successful status LOCAL_NATIVE_RECEIPT_RETURNS_MATCHED means only that
the *caller-provided capture* is consistent with a source-pinned
local original builder's full receipt contents, v0.7 same-source
ledger replay and required typed OS boundaries.
Because the auditor cannot independently authenticate when and
by whom a capture packet was collected, its flag
original_constructor_returns_observed remains false in the **audit
result**. The builder itself does observe raw original return values
when it runs; this is a local test observation, not external
historical issuance provenance.

All results retain false:
external_issuer_authenticated, historical_receipt_issuance_proved,
formal_descent_certified, lean_python_refinement_proved,
execution_authority_granted, truth_authority_granted,
git_merge_authority_granted.

## Static / runtime certification

- Source-byte guard:
  scripts/check_kuuos_lean_python_native_capture_sources_v0_8.py
  checks eight original source Git blob identities (including v0.7)
  and mandatory v0.8 regression discovery via AST. It does not
  certify Lean, external issuer provenance or signatures.
- Native tests:
  tests/test_kuuos_lean_python_native_cycle_receipt_capture_v0_8.py
  invoke the original native fixture **once** using genuinely called
  original Wa/Plan return constructors under observation wrappers.
  They test the original full returned packet, original Act ledger
  compatibility, mutation/read-only preservation, restoring wrappers
  after failures, missing evidence, resealed return substitution,
  return-order swaps, checksum changes, native tampering and source
  drift.
- The existing tests.test_kuuos_lean_python_os_registry_v0_5
  explicitly imports v0.8 test classes additively. Its existing
  cumulative runtime runner/checker and all v0.1–v0.7 checks
  remain present. No previous checks are skipped or weakened.

Commands from a full checkout:

~~~sh
python3 scripts/check_kuuos_lean_python_native_capture_sources_v0_8.py
python3 -m unittest -v tests.test_kuuos_lean_python_os_registry_v0_5
python3 scripts/run_kuuos_runtime_full_check_v0_55.py
~~~

Never claim SUCCESS before completed exact source GitHub Governance CI,
original genuine native test execution and tree identity are observed.
For Python/docs-only changes, Strict Lean is expected to SKIP, not
certify new mathematics.

## What is still not proved

1. An independent external issuer's signature / original receipt
   authenticity; capture snapshots plus SHA-256 are forgeable by
   callers and cannot attest historical collection time.
2. The full Python code's semantic refinement by Lean or a new
   mathematical descent/gluing theorem.
3. Execution authority, causal physical truth, clinical application
   or unconditional KuuOS WORLD transport.

These are explicit NO_DATA/authority obstructions, not claims of
mathematical impossibility. The mapping of 空／縁起 to formal
structures remains an interpretive/naming layer distinct from the
actual Lean proof terms.
