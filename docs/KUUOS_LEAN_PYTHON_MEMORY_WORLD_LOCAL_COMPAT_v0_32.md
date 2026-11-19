# KuuOS Lean→Python v0.32 — original MemoryOS↔WORLD local compatibility

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Canonical research progression and release boundary

Goal: carry actual previously proved Lean conditions into each OS's
original Python runtime, retaining local conditions and genuine
compatibility obstructions.

This stage is based on canonical main `e005206372b5a0a0d2e70d05c7342d8048d938e7`,
after v0.31 PR #3592 passed exact-head independent Runtime and the full
95-job terminal Governance (94 SUCCESS, 1 intentional skip) and was
MERGED. Its independently validated source HEAD was `5c072a1a914b2e1c7a0083866af87398b56e879a`.
The v0.32 staging branch is reconciled through append-only GitHub
MCP commit ancestry, without force rewriting.
Lean v4.30.0-rc2 and mathlib
`5450b53e5ddc75d46418fabb605edbf36bd0beb6` remain pinned.
Append-only / tighten-only / overwrite-forbidden / same-root.

No original Lean, MemoryOS, WORLD, CodeAI, host code, store, or
existing source pin checker is changed by v0.32. Five new files
provide one source-linked compatibility module, a static checker,
two test modules, and this document.

## What is locally checked (NOT formal descent)

The source objects must be:
1. An original valid MemoryOS v0.35 snapshot,
2. Its original read-only retrieval reconstructed from that snapshot,
3. An original validated WORLD v0.34 store envelope.

This is NOT a generic name-based comparison. The existing v0.31
MemoryOS native auditor must return `SOURCE_BOUND_LOCAL_CHECKED`
under its own source preconditions. The original WORLD
`validate_world_store` must validate its store, including the
full persisted commit chain. The following source-keyed equalities
are checked **exactly**, not approximately:

| MemoryOS snapshot field | Original WORLD store field |
|---|---|
| `source_world_store_digest` | full envelope `body_digest` |
| `world_context.world_store_id` | `world_store_id` |
| `world_context.root_lineage_digest` | `root_lineage_digest` |
| `world_context.generation` | `generation` |
| `world_context.current_world_fragment_digest` | `current_world_fragment_digest` |
| `world_context.last_commit_digest` | `last_commit_digest` |
| `world_context.commit_history_length` | count of stored commit receipts |

Only if all match does the adapter return
`SCOPED_MEMORY_WORLD_STORE_COMPATIBLE`.
Mismatched locally valid sources are `BLOCKED`. Missing sources
or incomplete blocker evidence remain `NO_DATA`.

If the separately supplied *original* disposition,
authorization, request, and recorded commit receipt are all present,
the original v0.31 WORLD source-bound atomic receipt audit must also
pass. This upgrades **only the local source-scope result** to
`SCOPED_MEMORY_WORLD_COMMIT_COMPATIBLE`.
Partial original commit provenance stays `NO_DATA`. It does not
permit a new WORLD commit, infer an external issuer, prove formal
descent or join unrelated source histories.

The local scope result carries explicit false fields:

- `formal_descent_certified = false`
- `global_gluing_proved = false`
- `whole_program_lean_python_refinement_proved = false`
- `complete_external_issuer_authenticated = false`
- `memory_upstream_blocker_authenticated = false`
- `world_commit_performed_by_auditor = false`
- no execution, truth, root rewrite or history delete authority.

A source match is compatibility of *specific observed native records*,
not authority to paste independent local states into a global truth.

## Independent native regression source scope

The new runtime tests use the **original native WORLD v0.34
disposition→authorization→request→commit kernel and persisted
file-backed WORLD store**, with original WORLD validators (no mocked
WORLD validation). In that same isolated temporary test root, the
original MemoryOS v0.35 builder is given the actual WORLD store.

Only MemoryOS's **upstream non-Markov cognitive episode and blocker
certificate validators** are mocked in the fixture. The native
MemoryOS builder and WORLD native validator are real; the upstream
fixture sources are not externally authenticated. The suite explicitly
asserts `memory_upstream_blocker_authenticated=false` even after
a successful local source relationship.

Negative tests verify source missingness, incompatible but valid
genesis-vs-committed WORLD source, forged snapshot root/digest,
tampered WORLD commit/source, partial commit provenance and the
absence of authority escalation or modification to original stored
WORLD bytes.

## Source provenance and release gate

```sh
python3 scripts/check_kuuos_lean_python_memory_world_local_compat_sources_v0_32.py
python3 -m unittest -v tests.lean_python_extensions.test_memory_world_local_compat_v0_32
python3 -m unittest -v tests.lean_python_extensions.test_memory_world_local_compat_sources_v0_32
```

Original v0.31 source checker pins are inherited; the new checker
adds nine exact original MemoryOS/WORLD/Lean/native source blobs,
the new Python entrypoint and two test class inventories.
New regression tests: 10 scoped compatibility tests + 9 source-pin
tests = 19. Native original CI and exact source/test-merge tree
must be observed on the eventually submitted PR's *same HEAD*.

No Lean source was changed; Strict Lean skipped is not a new theorem
certification. Do not interpret the source checks as constructive
Lean proof terms or general interpreter semantic equivalence.

**v0.32 PR release gate:** append-only ancestry reconciliation
is completed. Keep Draft and no main merge until the exact HEAD
passes independent v0.32 Runtime/Governance terminal SUCCESS and
Git-tree/source-receipt matching. Repair failures in that same PR.
