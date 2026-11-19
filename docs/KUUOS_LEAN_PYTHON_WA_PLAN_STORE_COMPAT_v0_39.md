# KuuOS Lean→Python v0.39 — original Wa→Plan store origins

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Scope and source

Base: `1930ef2bed45e8c577c21f62f4812546f5ab597e` (v0.38).
This additive Python audit binds supplied original Plural, Wa and Plan records
and a separately supplied original Wa replan receipt to two persisted stores.
Its scope is local compatibility of the observed files and native constructors.

The retained Lean sources are
`formal/KUOS/DecisionOS/PluralHarmonyAppealKernelV0_2.lean`,
`formal/KUOS/DecisionOS/WaRelationalHarmonyV0_3.lean`, and
`formal/KUOS/PlanOS/ReplanBoundSynthesisV0_1.lean`.
Earlier native-to-Lean condition projections remain those of v0.33.
The new origin comparison is a Python implementation condition; it is not a
new Lean theorem or a complete semantic refinement proof.

## Observed gap

The original Wa and Plan stores permit initialization from any state accepted
by their respective native validators. A valid intermediate state can therefore
serve as the genesis of a new suffix ledger. Replaying the remaining original
events produces the same final state. v0.33's final-state compatibility and
v0.6's typed edge audit both accept the characterized suffix examples.
An exact reconstruction with the original initial-state constructor distinguishes
these examples from the selected full-origin history.

## Chosen design

1. Copy and validate only plain finite JSON inputs. Accept built-in string
   roots or the platform's concrete Path type; reject custom conversion hooks,
   root/ancestor symlinks, cycles and lexical parent traversal. A caller using
   a parent-relative path must explicitly supply its intended canonical path.
2. Hold Wa and Plan roots fixed and distinct. Read the six original
   genesis/ledger/snapshot files once. Run the unchanged original
   `_recover_unlocked` kernels with captured-input readers, so genesis,
   every ledger row/event and snapshot all come from those exact bytes.
   The readers preserve native universal-newline and boundary-whitespace
   JSONL semantics. Nonfinite constants and overflowing numbers are rejected
   during parsing, including values shadowed by duplicate object names.
   Require finite JSON for every object. Compare replayed finals to the supplied
   finals with exact type-sensitive equality. No alternate store is written.
3. Apply the unchanged v0.33 auditor to the supplied Plural final and the two
   replayed finals, with the supplied original replan receipt.
4. Reconstruct Wa genesis with the original `build_initial_wa_state`, using
   supplied Plural final and the persisted genesis's ID, weights, thresholds
   and time. Reconstruct Plan genesis with `build_initial_plan_state`, using
   replayed Wa final, the supplied receipt and the persisted genesis's ID,
   budget, risk limit and time. Compare every field, including types.
   Constructor arguments from genesis are explicitly observed configuration;
   this check does not independently authorize those settings or creation time.
5. Audit the two original typed edges separately:
   Plural final → Wa genesis, and Wa final → Plan genesis.
   Keep Wa genesis and Wa final distinct. No simultaneous three-node path is
   constructed from these historical versions.
6. Recheck path identities and re-read all six original files, requiring byte
   equality with the captured inputs. `store_bytes_stable_during_audit` means
   equality of these two observations; it cannot detect an unsampled change
   that is restored in between and does not establish an atomic snapshot.

The production auditor never creates a receipt, writes to a store, invokes a
host, or fills missing sources. `NO_DATA` means required input or history is
unobserved. `BLOCKED` identifies an observed contradiction to these selected
input conditions. Neither status proves universal mathematical impossibility.
`SCOPED_WA_PLAN_STORE_COMPATIBLE` certifies only the listed local checks.

## Alternatives considered

A plain wrapper around v0.33 and native replay would accept both characterized
suffix histories. It does not supply the missing origin condition.

ActOS recorded claim/slice evidence is another useful research direction, but
its present receipt lacks actual execution counters and its late-blocked route
can omit activity. v0.39 leaves those numeric and issuer obstructions intact.

The chosen bounded extension preserves every existing kernel, store, adapter,
Lean theorem, workflow and source pin. The original replan receipt must be
supplied: neither of the two stores persists its full packet. Tests reconstruct
that fixture packet with the original constructor and exact v1.3 parameters;
this is explicitly fixture generation, not issuer authentication.

## Validation

Use the real original v1.3 full-cycle fixture. For each suffix counterexample,
initialize an alternate temporary store from the first native event's result,
then apply the remaining original events. Confirm that native replay and the
earlier audits still pass and that the new origin check blocks the suffix.
Additional checks cover missing evidence, malformed JSON, forged receipts and
states, dense exact-integer commit indices, root aliasing, symlinks, corrupt
files, unchanged input/file bytes and retained non-authority flags.

The source checker inherits v0.38 and earlier checks and pins the exact
original constructors, stores, typed-path helper and relevant Lean modules.
A matching source inventory is static evidence, not execution or proof.

From the repository root, run the module entry points:

`python3 -m scripts.check_kuuos_lean_python_wa_plan_store_sources_v0_39`

`python3 -m unittest discover -s tests/lean_python_extensions -p 'test_wa_plan_store_*v0_39.py' -v`

Local prepublication checks passed 42 new tests plus 21 retained v0.33 and
35 retained v0.38 tests. Disabling both genesis comparisons made exactly the
two suffix-history regressions fail; restoring them returned the suite to
success. Review regressions were observed failing before the path, captured
reader and finite-ledger fixes. Real-store regressions also cover native
boundary whitespace and nonfinite values shadowed by duplicate names.
Independent CI remains an integration gate.

## Unproved and unauthenticated

External issuer authenticity, actual ActOS job/slice counts, a persisted
Plural history, a globally atomic multi-store snapshot, global descent,
complete Lean/Python semantic refinement and every execution/truth/clinical/
legal/Git/memory-overwrite authority remain outside this audit.

## Integration gate

Preserve Lean `v4.30.0-rc2` and mathlib
`5450b53e5ddc75d46418fabb605edbf36bd0beb6`.
Preserve append-only, tighten-only, overwrite-forbidden and same-root.
PR #1558 remains Draft/Open/unmerged. Python/docs-only changes do not require
Strict Lean. Publish only after v0.38 post-merge checks finish, and merge only
after independent exact-head Runtime/Governance checks and source review.
