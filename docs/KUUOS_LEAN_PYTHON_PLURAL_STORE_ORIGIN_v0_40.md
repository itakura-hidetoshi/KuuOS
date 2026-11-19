# KuuOS Lean→Python v0.40 — original Plural store full origin

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Canonical source and boundary

This is a strict additive Python/source-check extension of the independently
merged and push-certified v0.39 main HEAD
aabd1f2d9be0405624c464eb437e5d8acac68a8e.

The unchanged proof source is
formal/KUOS/DecisionOS/PluralHarmonyAppealKernelV0_2.lean.
The exact original runtime sources are
runtime/kuuos_decision_os_plural_kernel_v0_2.py,
runtime/kuuos_decision_os_plural_store_v0_2.py,
runtime/kuuos_decision_os_plural_types_v0_2.py, and
runtime/kuuos_lean_python_plural_native_binding_v0_29.py.

The Lean source proves conditional properties of explicitly defined structures:
PluralDecisionPhase transitions, PluralDecisionHistory commit-summary alignment,
the non-authority boundaries and further local statements. It does NOT prove
that the Python runtime implements those structures in all cases. Our new check
of selected JSON fields is an interpretation and runtime test, not a new Lean
theorem, compilation refinement or universal correctness proof.

## Newly observed gap

The original PluralDecisionStore is implemented and used by the native v1.3
full-cycle fixture, under the plural directory. v0.39 checked the original
Plural *final-state packet* only; its persisted genesis, all ledger events and
snapshot were not independently replayed and bound to the original DecisionOS.

A native-valid Plural state after the first event can be installed as the
genesis of an alternative store, and the remaining original events replayed.
The resulting final state is identical. The v0.39 audit and the original
DecisionOS-to-Plural typed data link cannot exclude that suffix substitution.

## New bounded audit

1. Require separately supplied native DecisionOS and Plural final packets,
   the final Wa/Plan packets, the original Wa replan activation receipt,
   and all three actual Plural/Wa/Plan store roots. Missing input is NO_DATA.
   No missing receipt or history is synthesized in the production auditor.
2. Require concrete, non-overlapping roots, with no root/ancestor/file
   symlinks or traversal. Read and capture the three original Plural files
   once; use the unchanged original PluralDecisionStore._recover_unlocked
   through captured readers, not a simplified duplicate replay.
3. Check the complete genesis, ledger and snapshot as finite plain JSON,
   including values before duplicate keys shadow them. Check strict dense
   integer commit indices, exact snapshot equality and exact supplied final.
   The captured reader preserves the native JSONL newline/whitespace behavior.
4. Rebuild the original genesis using build_initial_plural_state with the
   supplied original committed DecisionOS state; take the original Plural
   ID, lineage ID, thresholds and time from the *observed* genesis and
   compare all fields with type-preserving equality. Those observed settings
   are not externally authenticated.
5. For an initially empty original Plural history, check:
   final.event_index = original ledger length;
   final.plural_version = final.completed_plural_deliberations =
   final.plural_summaries length = count of actual commit-phase events.
   Bind each summary's commit-event digest and ordinal to the replayed
   commit event. This is a selected Python analogue of the Lean
   PluralDecisionHistory shape, not a proof of Lean-to-Python refinement.
6. Check the historical Decision final -> Plural genesis typed link using
   the original registered v0.6 edge. Reuse v0.39 unchanged for the
   Plural final -> Wa genesis and Wa final -> Plan genesis links and both
   original Wa and Plan store origins. The intermediate incoming and outgoing
   states are distinct: no single contemporaneous four-node path is inferred.
7. Recheck the Plural root and all its original bytes after the downstream
   v0.39 audit. Requiring two observations to match does not prove an
   atomic three-store snapshot or detect a change restored between reads.

A successful SCOPED_DECISION_PLURAL_WA_PLAN_ORIGINS_COMPATIBLE means precisely
these selected local checks passed. A contradictory source is BLOCKED.
Missing evidence or an uncommitted observed final is NO_DATA. Neither is a
universal theorem of impossibility.

## Tests and negative controls

Use the ORIGINAL native v1.3 full-cycle fixture; original stores and kernels
are neither reimplemented nor edited. Construct a real first-event suffix
counterexample by applying the remaining seven original events to a new
separate store. Confirm identical final states and acceptance of the earlier
local Wa/Plan and typed-edge checks, but rejection by the original Plural
genesis comparison. No forged/plausible record is accepted as a replacement
for absent source.

Other regressions cover missing files, incomplete histories, wrong types,
forged Decision/Plural/activation receipts, root aliasing and nested roots,
parent and file symlinks, cycles and traversal, damaged ledger/snapshot,
strict commit-index typing, shadowed NaN/Infinity/overflow numbers, universal
newline/whitespace behavior, exact first-capture replay, mid-audit changes,
unmutated originals and explicit non-authority fields.

The source checker inherits every v0.39 and earlier pin and adds nine fixed
original code, Lean and previous-audit Git blobs.

From the repository root:

    python3 -m scripts.check_kuuos_lean_python_plural_store_origin_sources_v0_40

    python3 -m unittest discover -s tests/lean_python_extensions -p 'test_plural_store_*v0_40.py' -v

Independent GitHub Governance/Runtime on the exact submitted head is the
integration gate. A Python/docs-only addition must not dispatch Strict Lean.
On successful exact-head certification, merge via the same PR only, then
separately verify the actual merge-head Runtime, Governance and Docs jobs.

## Unproved or unobserved

The entire original DecisionOS persisted history has not been replayed here.
The actual ActOS execution/job counts, external issuer authenticity, a
globally atomic multi-store snapshot, global descent, full Lean/Python
semantic refinement, and all execution/host/clinical/legal/truth/Git/overwrite
authority remain unproved or ungranted.

Canonical main, pinned Lean v4.30.0-rc2 and mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6, append-only,
tighten-only, overwrite-forbidden and same-root remain binding.
The validation-only PR #1558 remains Draft/Open/unmerged.
