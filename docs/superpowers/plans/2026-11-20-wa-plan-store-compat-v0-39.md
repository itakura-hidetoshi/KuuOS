# Wa→Plan Store Origins v0.39 Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans task by task.
> User-authorized GitHub MCP operations replace git/gh CLI commands.

**Goal:** Detect supplied Wa/Plan histories whose observed genesis is not
the original constructor's full-origin state.

**Architecture:** Reuse original replay kernels with readers bound to one
captured byte set, original constructors and existing scoped auditors. Add a
separate audit and source checker; preserve all previous files.

**Tech Stack:** Python standard library, unittest, GitHub MCP and existing CI.

**Spec:** `docs/KUUOS_LEAN_PYTHON_WA_PLAN_STORE_COMPAT_v0_39.md`

## Global Constraints

- Base SHA `1930ef2bed45e8c577c21f62f4812546f5ab597e`.
- Lean `v4.30.0-rc2`; mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`.
- append-only / tighten-only / overwrite-forbidden / same-root.
- Keep PR #1558 Draft/Open/unmerged; use GitHub MCP, no git/gh.
- No original Lean/runtime/workflow source edits and no Strict Lean dispatch.
- Original missing receipt stays NO_DATA; all proof/issuer/authority flags false.

## Review Focus

- A valid suffix history can pass earlier replay and edge audits.
- Wa genesis and Wa final differ and cannot be substituted.
- Bool/float values must not silently equal integer state fields.
- Custom path hooks, symlinks and aliases must not become trusted roots.
- Missing or changing store bytes must not yield scoped success.

## Task 1: Native audit and real-history regressions

**Create:** `runtime/kuuos_lean_python_wa_plan_store_compat_v0_39.py`
and `tests/lean_python_extensions/test_wa_plan_store_compat_v0_39.py`.

**Interface:** `audit_native_wa_plan_store_compatibility(plural_state, wa_state,
plan_state, replan_activation_receipt, original_wa_store_root,
original_plan_store_root) -> NativeWaPlanStoreAudit`.
Results expose `status`, `issues`, original source/genesis/final digests,
two commit counts, staged edge statuses and bounded positive-check flags.

- [ ] Write real full-cycle positive and two suffix rejection tests first.
- [ ] Run tests and record missing-auditor RED evidence.
- [ ] Implement finite input copying, original replay, final checks, complete
      genesis reconstruction, two staged typed edges and six-file recheck.
- [ ] Cover the five review focus cases with real inputs and temporary files.
- [ ] Run focused tests; expected all pass and no original bytes changed.

## Task 2: Source continuity and scope documentation

**Create:** `scripts/check_kuuos_lean_python_wa_plan_store_sources_v0_39.py`
and `tests/lean_python_extensions/test_wa_plan_store_sources_v0_39.py`.
**Consumes:** public audit symbols in Task 1, v0.38 checker.
**Produces:** `check_sources(root=ROOT)`, `test_inventory(root=ROOT)`, and
a source-pinned additive inventory.

- [ ] Write tests for original source drift, missing required files,
      inherited pins and absence of authority promotion.
- [ ] Run tests and record missing-checker RED evidence.
- [ ] Implement inherited checks and exact Git-blob pins.
- [ ] Run both new test modules and retained nearby regression modules.
- [ ] Finish the scope/design document and independent source review.

## Task 3: Publish and independently certify

- [ ] Verify v0.38 post-merge Runtime/Governance/Docs terminal success.
- [ ] Review the complete six-file addition in a fresh agent context.
- [ ] Create a branch from the exact base via MCP, commit the reviewed tree
      and open one draft PR; use the same PR for any necessary corrections.
- [ ] Audit all exact submitted-head CI jobs/steps and real logs.
- [ ] Confirm base/head/tree, protected PR and pins, then mark ready and merge.
- [ ] Audit exact merge-head push workflows; append qualified observations.

## Review decisions

The prepublication review identified root-ancestor links, cyclic roots,
independent inner byte samples, nonfinite ledger metadata and inconsistent
source-root checks. Added regressions failed before the fixes and passed
afterward. Replay now consumes only the captured bytes; its native kernel is
unchanged. Both checker entry points share the same concrete, non-symlink
root condition. The supported checker entry is the documented module form.
Follow-up reader checks preserve native boundary whitespace and reject
nonfinite constants or overflow at parse time, before duplicate names can
shadow a value. Both behaviors have real-store regression evidence.
External issuer authenticity, actual Act counts, persisted Plural history,
global atomicity and formal descent/refinement remain explicitly out of scope.
