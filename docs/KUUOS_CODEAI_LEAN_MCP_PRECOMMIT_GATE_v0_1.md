# CodeAI → Lean MCP direct verification precommit gate v0.1

Status: additive, fail-closed, exact-source precommit evidence; **not** independent CI, kernel proof, or merge authority.

## Contract

CodeAI **proposal-only** candidate and isolated application is not an authorization to edit a Lean proof. A candidate is locally eligible for subsequent human/GitHub-MCP review only after the exact source HEAD, Git tree, original/candidate Git blob and all five digest-sealed CodeAI receipts are mutually consistent, and both the following independent tests have completed:

1. Actual pinned Lean MCP `lean_diagnostic_messages`, `lean_goal`, `lean_multi_attempt`, followed by post-candidate zero-error diagnostics, source restoration, identical declaration signatures/imports, no new forbidden constructs and a successful MCP local `lake env lean` gate.
2. A second, independent `lake env lean -DwarningAsError=true -Dweak.sorryAsError=true` direct compilation against the **exact same candidate bytes**, with exit code 0, matching SHA-256 log, and an .olean emitted in an isolated temporary directory.

The runtime is `runtime/kuuos_codeai_lean_mcp_precommit_gate_v0_1.py`, CLI `scripts/check_codeai_lean_mcp_precommit_gate_v0_1.py`, ten fail-closed tests `tests/test_kuuos_codeai_lean_mcp_precommit_gate_v0_1.py`.

The parent #3522 current `.github/workflows/lean-mcp-live-parent-head-v2.yml` runs the actual CodeAI producer on the current immutable checkout. The Lean MCP precommit step reuses the resulting five signed-by-digest receipt *claims* (not external authentication), observes the complete changed-source and import closure, tries the isolated candidate and restores the source, then separately invokes the gate. The gate writes an append-only `codeai_lean_mcp_gate_receipt.json` even when blocked; its status is `LOCAL_PRECOMMIT_NOT_CERTIFIED` unless every check succeeds.

The pending v1.95 round-5 candidate has a known `change` tactic elaboration failure. It must **not** be committed as a proof repair. Its CodeAI candidate/isolation success does not override the fixed Lean compiler result. This is the immediate test that the gate rejects.

## Authority

The gate never mutates Git, does not call paid providers, and never emits independent-CI or merge authority. Even a local precommit-green receipt must be followed by a separate exact-source GitHub-MCP commit, full dependency closure, Strict Lean completed/SUCCESS, `#print axioms`/sorryAx audit, public roots test and source/test-merge tree equality. KuuOS main, root 107, legacy/v5.291 and protected #1558 remain unchanged.

PIN: Lean v4.30.0-rc2; mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6. Observed failure and NO_DATA remain recorded, not promoted to success.

## Round-8 actual pinned-Lean-green candidate
The `round7-finite-concrete-rfl` experiment generated the exact Git blob
`bbbbf480721aa6d0a834c7fd5ad7690d0daff04e` and obtained exit code 0
with an .olean under pinned Lean and warning/sorry errors in run #43658543815.
This is not by itself a CodeAI admission, an MCP verification or independent
CI certification. The new workflow deliberately reexecutes the actual CodeAI
five-stage selection and the Lean MCP/full-source/direct Lean gate before
allowing any source edit. Expected source blob remains
`f7dcf6d9cddf3820b78c91375f0ec460874a7734`.

## Two candidate serialization paths (exact-source repair case)

The standalone externally supplied Candidate Patch receipt and the autonomous
unified-diff-generated selected candidate have separate (legitimate) candidate
and diff digests. Their receipt identifiers MUST NOT be equated. This gate
instead verifies the selected generated candidate packet, its own sealed
Candidate Patch receipt, portfolio membership, selection and isolated
application, and the exact resulting Lean Git blob and canonical snapshot
digest. A failure to distinguish the two routes is a compatibility obstruction,
not a reason to lower the requirement for independent Lean verification.
