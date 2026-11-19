# Lean→Python v0.42 — original BeliefOS gerbe stored origin and last receipt

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Authority and exact source

Canonical: itakura-hidetoshi/KuuOS \`main\`, parent
\`0272779f97c0513f8922e8e1e4c3c645cfab3810\` (v0.41 merged).
Pinned Lean v4.30.0-rc2 and mathlib
\`5450b53e5ddc75d46418fabb605edbf36bd0beb6\`.

Source Lean theorem file, left **unchanged**:
\`formal/KUOS/BeliefOS/ContextGerbeCoherenceV0_3.lean\`.
Its \`SurfaceHolonomyHistory\` and \`appendSurfaceHolonomy\`
establish implications of an explicitly declared structure. They do not
formally establish correctness of every Python \`BeliefGerbeStore\`.

The original native Belief files, also **unchanged**, are:
\`runtime/kuuos_belief_os_gerbe_store_v0_3.py\`,
\`runtime/kuuos_belief_os_gerbe_types_v0_3.py\`,
\`runtime/kuuos_belief_os_gerbe_coherence_v0_3.py\`.

The existing verified-by-Python **v0.18** \`_replay_belief_ledger\`
already reconstructs original source receipts by invoking the unchanged
original Belief native packet kernel. This v0.42 work **reuses** that
audit instead of duplicating the original kernel/receipt reconstruction.

## Actual missing connection

The v0.41 selected local auditor binds a separately supplied
\`BeliefOSReceipt\` digest into the original DecisionOS genesis, then
replays Decision, Plural, Wa and Plan persisted histories. It does not
compare the supplied Belief receipt to the original BeliefStore ledger
that issued it. A locally consistent but ungrounded source receipt is
not equivalent to an actual replayed local native receipt.

The original v1.3 BeliefStore holds three files:
\`belief-gerbe-genesis.json\`, \`belief-gerbe-ledger.jsonl\`, and
\`belief-gerbe-snapshot.json\`. The committed final state and last
receipt are linked to the original packet(s), not simply the sender's
claimed hash.

## New bounded read-only construction

- Require separately supplied **original** native Belief final state,
  Belief last receipt, Decision/Plural/Wa/Plan final states, the
  original Wa→Plan replan receipt, and five original store roots.
  Do not generate absent receipts, packets, or authorities.
- Require each root concrete, unaliased, nonnested, without root/parent
  symlinks or lexical traversal. Capture the three BeliefStore persisted
  file bytes once. Reject malformed and non-finite raw JSON, including
  duplicate-key-shadowed \`NaN\` / \`Infinity\` / \`1e999\`.
- Run the **unchanged** original \`BeliefGerbeStore._recover_unlocked\`
  kernel against only those captured bytes, including the original
  ledger, packet, receipt and state digest chains. Validate strictly
  dense integer commit indices, exact original final/snapshot,
  and exact type-sensitive equality with the supplied Belief state.
- Rebuild Belief genesis with the unchanged
  \`build_initial_gerbe_state\` constructor and compare all fields;
  its lineage/time arguments are observed from the persisted genesis,
  not authenticated settings.
- Call existing v0.18 \`_replay_belief_ledger\` with the original
  genesis, actual commit records and replayed final. Bind the resulting
  **entire** final receipt to the supplied Belief receipt with
  type-sensitive equality. The replayed receipt must match both its
  original packet and original stored commit digest.
- Check local Python counters/history against the Lean
  \`SurfaceHolonomyHistory\` naming layer, including original zero
  genesis, event/run/commit counts, each per-event receipt digest and
  processed packet identity. This is a tested runtime data condition,
  not a formal Lean/Python refinement theorem.
- Reuse unchanged v0.41 original Decision/Plural/Wa/Plan audit on
  **the same supplied Belief receipt**. Preserve its staged typed
  edge checks and its numeric time obstruction without promoting
  time labels into one causal clock.
- Re-read all original Belief persisted files and compare bytes with
  the first capture. Distinct stores are audited at distinct read
  times; this is not an atomic five-store snapshot.

Positive status
\`SCOPED_BELIEF_DECISION_PLURAL_WA_PLAN_ORIGINS_COMPATIBLE\`
means only these particular observations pass.

\`NO_DATA\` means required source or original Belief ledger events were
not observed, e.g. a newly initialized store starting at a valid prior
final state but with zero original commits. \`BLOCKED\` is an observed
contradiction for the selected local conditions; it is not universal
proof of impossibility.

## Real fixture regressions and negative controls

The tests use the unchanged \`build_native_full_cycle_receipt\` v1.3
fixture. Its original BeliefStore contains one real committed packet,
so a nontrivial first-event suffix with retained later events cannot
be created from that fixture. Instead the test constructs a real
native-valid **empty-history alternative store initialized at the
committed final**. Its \`recover()\` returns the same final Belief state,
while the selected v0.42 original-commit obligation remains NO_DATA.
This distinguishes a valid state snapshot from a persisted history.

Other regressions cover forged and self-resealed last receipt, missing
original file/receipt, source state mismatch, strict native commit-index
typing, path/root symlinks, malformed files, shadowed non-finite JSON,
native JSONL whitespace, first-capture replay, time obstructions, source
file nonmutation and absence of execution/clinical/truth/host/Git/
memory-overwrite authorities.

## Run and publication gate

From the repository root:

    python3 -m scripts.check_kuuos_lean_python_belief_gerbe_store_sources_v0_42

    python3 -m unittest discover -s tests/lean_python_extensions -p 'test_belief_gerbe_store_*v0_42.py' -v

Nine original Lean/native Git blobs are independently pinned, and all
v0.41-and-earlier static pins remain binding.

Commit only five new files, never alter the Lean source, native kernel,
original stores, previous adapters, original CI workflows or #1558.
Use independent GitHub exact-head Runtime and Governance
workflow/job/step/receipt SUCCESS, and tested PR merge tree equality,
before merging. Python/docs-only means skip Strict Lean. After merge,
independently verify canonical-main push Runtime, full Governance and
Docs before declaring full stage certified.

## Noncertifications / remaining obstructions

No external transport/packet/receipt issuer authentication, source
provenance beyond the selected local files, global causal clock,
global temporal or multi-world descent, atomically observed
cross-store snapshot, complete Lean/Python refinement theorem,
ActOS actual numeric job/slice witness, clinical/institutional/Git
authority, truth or execution authority, or history overwrite
authority is granted.

A readable, reproducible, locally valid source record is not a
formal theorem about the world. Interpretations of the names
"Belief", "emptiness", and "dependent origination" remain distinct
from what Lean's exact predicates actually prove.

Maintain append-only / tighten-only / overwrite-forbidden /
same-root, GitHub MCP priority, pinned dependencies, and protect
validation-only PR #1558 Draft/Open/unmerged.
