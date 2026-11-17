# KuuOS Lean→Python v0.9 — process-isolated native receipt evidence

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Source, conditions, and authority

Repository: https://github.com/itakura-hidetoshi/KuuOS
Canonical main observed at afcb9cd7d84ba6beee45b2fcfc704473f593df25.

Lean v4.30.0-rc2 and mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6 are unchanged.
No original Lean proof, OS runtime kernel, native v1.3 source, v0.1–v0.8
adapter, public root, existing cumulative runner, CI workflow or protected
PR #1558 is replaced or modified. The new module lives in runtime alongside
the previous proof/runtime contract adapters.

Source links:

- runtime/kuuos_lean_python_native_cycle_receipt_capture_v0_8.py:
  original native v1.3 Wa/Plan receipt function-return observation.
- runtime/kuuos_lean_python_native_cycle_ledger_replay_v0_7.py:
  original ActOS genesis, applied event ledger and saved snapshot replay.
- runtime/kuuos_lean_python_os_path_composition_v0_6.py:
  seven typed OS handoff boundaries and explicit obstruction.
- runtime/kuuos_lean_python_os_registry_v0_5.py:
  selected original Lean/Python sources and theorem names.

All the mathematical statements and their conditions remain in the
original Lean files. Runtime source correspondence, hash consistency
and the output of a Python validator are not a Lean proof of Python,
formal descent, unconditional gluing, or truth.

## What is strengthened over v0.8

v0.8 observed actual return objects by temporarily instrumenting two
original receipt functions in one process. These original functions
were never replaced by simulated successful results; the wrappers
called the originals. Their temporary module-global references,
however, required the documented no-concurrent-call assumption.

v0.9 invokes that v0.8 fixture builder in a **separate child Python
interpreter** with argv (no shell). Instrumentation remains inside
the local child, isolated from the parent process's original
native module imports. No alteration to the original v1.3 builder,
Lean theorem or OS kernel is required.

The child explicitly constructs a fresh **bounded local native test
fixture** with the original v1.3 cooperative host test adapter.
These controlled local fixture effects already exist in v1.3/v0.8;
the v0.9 audit never triggers them. This is NOT a production execution
interface and it does not grant external host permission.

## Two separate interfaces

Implementation:
runtime/kuuos_lean_python_isolated_native_receipt_evidence_v0_9.py

- build_isolated_fixture_evidence(root):
  Explicit **effectful local test builder**. The provided existing
  TemporaryDirectory must be empty, non-symlinked, and not previously
  initialized. The builder launches a separate interpreter with
  explicit "--fixture-child" mode. This child invokes the original
  bounded v1.3 native cycle, observes original Wa→Plan / Plan→Act
  function returns via v0.8, and independently checks v0.7/v0.8
  native-state/ledger/receipt consistency before publishing evidence.
  It uses a staged file and atomic hard link with no-replace
  semantics: the fixed local evidence filename cannot overwrite an
  earlier published record. It calls fsync on file and directory.
  Failure does not certify the record, and reuse of a nonempty
  root is rejected before any new fixture effects.
- audit_isolated_evidence(root):
  **Read-only** audit of that one local record, the original native
  snapshot objects and the original ActOS genesis/journal/snapshot.
  No child process, event application, host call or store mutation.
  It verifies the version, exact record-field inventory, finite
  built-in JSON, SHA-256 of the record's contents, root path binding,
  native receipt digest, captured full original raw receipts,
  and inherited v0.8 and v0.7 exact checks. Reading a live
  concurrently modified store is unsupported.

The fixed local record contains:

- full original native v1.3 cycle receipt (ten native artifacts);
- full local v0.8 captured original Wa/Plan return objects, in order;
- their existing digest references and a record SHA-256;
- a checksum of the local fixture root pathname, plus version and
  source-baseline identifiers.

The single record is stored *only in the isolated fixture directory*,
not as a generated artifact or file attached to this conversation.
The source code and tests are committed to GitHub.

## Explicit evidence boundary

Status ISOLATED_LOCAL_FIXTURE_EVIDENCE_REPLAYED means only:
local original native data, read-only Act journal replay, captured
return packets and record consistency passed their named Python
checks on the supplied local fixture. NO_DATA means required original
record/ledger input is absent. BLOCKED means an observed malformed
record, source/context/receipt mismatch, changed local ledger, or
other violated check. BLOCKED is an audit outcome, not a Lean theorem
of mathematical impossibility.

Importantly, the record's SHA-256 and root pathname checksum are
**not independently signed**. A local writer who can change the
entire directory can also change the record and recompute both
checksums. The test suite explicitly demonstrates this limitation:
a copied fixture with a coherently recalculated root binding can
still pass the local audit. It must not be described as authentic
third-party issuance provenance or independent historical proof.

All successes retain these flags as False:

- external_issuer_authenticated
- historical_issuance_proved
- lean_python_refinement_proved
- formal_descent_certified
- execution_authority_granted
- truth_authority_granted
- git_merge_authority_granted

This also preserves Preference ⇏ Descent ⇏ Authority.
Process isolation is an engineering safety improvement, not
the discovery of a new mathematical theorem about 空 or 縁起.

## Validation and independent certification

New tests:
tests/test_kuuos_lean_python_isolated_native_evidence_v0_9.py.
They include one real child-process original native full-cycle
positive fixture, original Act ledger replay, absence and corruption
cases, non-overwrite semantics, symlinks, self-consistent local
copy/forge limitation, fixed-checksum drift, original receipt
substitution, provenance/non-authority restrictions, read-only
audit and source checker negative tests.

Static-source guard:
scripts/check_kuuos_lean_python_isolated_evidence_sources_v0_9.py
pins seven original source Git blobs by bytes and verifies that the
two new test classes are actually imported by the existing
cumulative unittest module using Python AST, not a comment.
The original cumulative runtime runner/checker is untouched;
v0.9 test classes are additively imported by
tests/test_kuuos_lean_python_os_registry_v0_5.py, retaining
every v0.1–v0.8 test.

In a complete repository checkout:

~~~sh
python3 scripts/check_kuuos_lean_python_isolated_evidence_sources_v0_9.py
python3 -m unittest -v tests.test_kuuos_lean_python_os_registry_v0_5
python3 scripts/run_kuuos_runtime_full_check_v0_55.py
~~~

Independent exact-head GitHub workflow/job/step completion, actual
unskipped native tests, source vs test-merge Git tree equality,
unchanged canonical base, and post-merge independent push CI are
required before integration. Python/docs-only changes do not justify
claiming a new Strict Lean proof; Strict Lean should be SKIPPED.

## Unresolved

Third-party external issuer authenticity, signed append-only audit
receipts, independent time/history attestation, formal Lean/Python
semantic refinement, mathematical descent for the full runtime,
non-test host effects, and general WORLD/MemoryOS/CodeAI connections
are all still unproved or unverified here (NO_DATA).
