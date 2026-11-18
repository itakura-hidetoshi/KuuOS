# KuuOS Lean→Python v0.16: committed Plural source witness and Wa profile binding

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.

## Observed baseline and accepted scope

The canonical main baseline is
\`9bbd82a95a579a8091a1cb5d7e7f7b92eb254924\`
(v0.15, PR #3576). The source of authority is the current GitHub
tree and retained Lean declarations, not this prose.

v0.15 checks that supplied normalized Wa profiles, local weights and
thresholds yield the exact stored Python-float evaluation intervals.
It intentionally cannot distinguish a profile whose score and digest
have both been changed consistently from a genuine original input.
v0.16 connects Wa's source projection to an explicitly supplied,
already-committed Plural state, and independently checks each stored
normalized Wa profile's complete canonical digest. The native fixture
obtains its source from the actual local Plural store's recovery, rather
than trusting a copied string-valued source digest.

The pure new entrypoint is:

    checked_apply_wa_profile_source_event(state, event, source_plural_state)

It validates the supplied local Plural witness, 19 Wa projection fields and
normalized profile schema/digest before and after one **unchanged** v0.15
adapter call. The existing v0.12 mediator already recalculates
wa_profile_digest; v0.16 is an additional independent schema/hash
cross-check, not the first detection of stale profile hashes.
All input objects are copied as finite builtin JSON.
The native result, source fields, scores, digests and existing history are
never repaired, overwritten or resealed by the new guard.

### Exact committed source projection

The 14 directly copied Plural fields comprise lineage, plural identity,
plural state/commit digests, Plural and Decision basis digests, the committed
Decision digest, mission contract, route, selected option, source option IDs,
retained alternatives, options digest and stakeholder registry digest.
Option IDs and digests are independently reconstructed as an exact map
from the source's original option records. Four section digests are
recomputed from the actual Plural **utility, veto, aggregate and appeal**
arrays. Total: 14 direct fields + 1 option map + 4 section digests = 19.

The source witness must have phase \`commit\`, an exact canonical
Plural state digest, and pass the original Plural \`validate_plural_state\`
validator without mutation. It must not be promoted from a \`bind\`,
\`adjudicate\`, or other noncommitted state.

These comparisons are local and point-in-time. The \`sha256\` canonical
digest is a consistency check, NOT a digital signature from the
stakeholder, a trusted issuer, or any outside source. A jointly forged
Plural genesis + all ledger entries, or a false-but-self-consistent
stakeholder record, is not ruled out by this boundary.

### Complete normalized Wa profile digest

On and after \`profile\`, the new guard requires all 11 original normalized
fields and no extra keys:

    option_id, option_digest, positive_intervals, alert_intervals,
    dissent_considered, minority_preserved, dissent_evidence_digests,
    minority_stakeholder_digests, dialogue_receipt_digest,
    indra_network_receipt_digest, wa_profile_digest

The profile hash must match the exact canonical JSON of these fields
excluding \`wa_profile_digest\`. The v0.12 mediator already checks the
profile hash and membership in the local Wa option map. v0.16 adds an
exact eleven-field inventory and compares the Wa map to a distinct
recovered committed Plural store witness. Receipt strings,
exact Boolean flags, list syntax and duplicate evidence digests are
checked, with no semantic interpretation of those opaque references.
The original v0.13 finite-interval and v0.15 recomputed-score checks
remain in the prior adapters. The previous v0.14 local false-harmony,
plurality and gate conditions also remain unchanged.

A missing supplied source witness is \`NO_DATA\` and stops before the prior
Wa call. An explicitly mismatched source/projection, invalid profile hash
or incompatible original Plural state is \`BLOCKED\`. A preexisting invalid
snapshot is checked even if a later event would be \`REPLAYED\` or
\`REJECTED\`. Valid native replays and rejections preserve all original
diagnostics. Post-result failures stop before a participating store
append/update; the original pure native adapter may already have run.

### Selected actual child and read-only postflight

The native wrapper
\`runtime/kuuos_lean_python_wa_profile_source_native_cycle_v0_16.py\`
runs one explicit fixture in an independent Python process. It temporarily
wraps only v0.15's imported pure checked evaluator. The original eight
OS routes, selected Act pre-host check and v0.9 write-once receipt are
unchanged.

On its first Wa call the child executes real Plural store
\`recover(require_snapshot_match=True)\` against
\`root/plural/plural-genesis.json\`,
\`root/plural/plural-ledger.jsonl\` and the original snapshot.
It captures a fixed local witness for the selected Wa cycle, not an
arbitrary URL or an unsigned value supplied directly by the Wa caller.
Successful source-guard returns are counted; this count must equal
the nested Wa evaluation, gate, numeric and state guard counts.
Earlier Plural replay guards may run again during the source recovery;
counter equality is asserted only for the Wa path.

After the child exits, the parent independently re-runs the local
Plural recovery and compares its witness digest with the child's
reported digest. The v0.9 evidence audit is reused unchanged and
remains read-only. This does not authenticate when the child actually
performed every guard: child stdout counters are unsigned.
Caching the witness creates a known time-of-check boundary and does
not establish concurrency safety or cross-run immutability. A partial
child failure leaves partial local evidence, without retry or rollback.

## Formal sources and limits

The original
\`formal/KUOS/DecisionOS/PluralHarmonyAppealKernelV0_2.lean\`
and
\`formal/KUOS/DecisionOS/WaRelationalHarmonyV0_3.lean\`
are left unmodified. Their theorem statements have explicit
assumptions about Plural source and Wa local conditions; their
interpretive names do not themselves prove that these Python
constructors correctly implement the abstract statements.
The exact Python 3.12 tests and CI validate only the tested
local source/projection/hash edge, not a Lean/Python refinement proof.

Even a self-consistent altered \`dialogue_receipt_digest\` can pass when
its profile digest and all downstream calculated records are adjusted,
because no external issuer is authenticated. That limitation is tested
explicitly rather than silently treated as provenance. The guard
does not verify an external stakeholder's consent, clinical facts,
truth, legal permission, an independent issuing certificate,
all filesystem operations, host rollback or host/store atomicity.
It grants no new execution, truth, institutional, moral or Git merge
authority. The protected validation-only PR #1558 stays Draft/Open.

## Repository preservation and certification workflow

The original v0.15 source checker pins 90 historical blobs. The
new v0.16 checker adds all seven v0.15 file hashes: 97 retained
selected Git blobs in total. It requires the seven new v0.16 files,
checks ordinary AST test declarations but does not run them.
Existing test loader, CI workflows, native kernels, stores,
Lean sources and mathlib pin are unchanged.

Acceptance requires the new tests to actually execute with exact
declared ID sets, no skips, source/checker pins, an exact Git tree
comparison of submitted source / PR test merge / formal integration,
independent successful PR Governance and postmerge main Runtime /
Sharded Governance with terminal run, job and check receipts.
A Python/docs-only Strict Lean SKIPPED is expected and does not
produce a new proof. If required CI fails, keep the PR open and
unmerged rather than asserting that a likely repair is certified.

This scoped source witness is stronger than trusting bare local
hash strings. It is not an end-to-end provenance attestation of
the system, since hashes, local ledgers and the observer's own
authority have separate prerequisites.
