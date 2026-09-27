# KuuOS CI Observation → MCP Routing v7.25

## Purpose

v7.24 knows which MCP planes should be used for a development task.

v7.25 connects that router to real bounded GitHub Actions observations.

The important KuuOS rule is:

```text
CI error line
=
locator

CI error line
!=
repair scope
```

For Lean failures, the repair scope is the full target Lean file.

## Input

v7.25 consumes the receipt produced by the existing v7.0 GitHub Actions bounded live-log observer.

That receipt already binds repository, exact expected HEAD, run ID, terminal state, conclusion, bounded log digest, and bounded delta excerpt. Raw logs remain unpersisted.

## Lean failure classification

The adapter recognizes `.lean` paths and common Lean diagnostics including unsolved goals, unknown identifiers, type mismatches, failed synthesis, `simp made no progress`, heartbeat/recursion failures, and Lake/Lean errors.

A Lean failure becomes `lean_ci_repair`, and v7.24 then selects:

```text
GitHub MCP      -> exact remote CI evidence
Filesystem MCP  -> full current target file
Lean-LSP MCP    -> semantic state for those current bytes
Git MCP         -> local diff/revision
```

## Full-file audit

For `lean_ci_repair` the packet explicitly records:

```text
full_target_file_audit_required = true
ci_error_line_is_locator_not_scope = true
```

This prevents the automation from degenerating into repeated one-line CI patching.

The intended workflow is:

```text
locate failing area
-> inspect full Lean file
-> identify the Lean/API pattern
-> repair structurally
-> re-observe semantics
-> review diff
-> exact-head CI
```

## MCP protocol signal inside Lean work

If a Lean CI failure also contains MCP protocol terms such as `tools/list`, `tools/call`, `protocolVersion`, `MCP-Protocol-Version`, or JSON-RPC method/parameter errors, v7.25 keeps the Lean repair route and additionally requests the official MCP Docs plane.

It does not replace local Lean evidence with external documentation.

## Browser failures

A browser-specific failure becomes `browser_debugging`, so Chrome DevTools is primary and Playwright is the functional reproduction plane.

## MCP-only failures

An MCP protocol failure without a Lean signal becomes `mcp_spec_research`: official MCP Docs is primary, Context7 is corroborating, and Fetch is fallback.

## Ambiguous failures

An unclassified CI failure is not guessed into a repair action. It remains `remote_repository_observation` with partial status and a warning.

## Authority

The live CI receipt is evidence about remote execution. It does not grant Filesystem, Git, Lean, or GitHub mutation authority.

If a later caller requests writes without the needed authority, the nested v7.24 route becomes `authority_required`, not rejected.

## Validation

Focused tests verify Lean routing, full-file audit semantics, Lean+MCP mixed failures, browser routing, MCP-only routing, ambiguous failure handling, successful CI handling, write-authority separation, and invalid receipt boundaries.

The central law is:

> **CI tells KuuOS where to investigate; current repository bytes and semantic observations determine what must actually be repaired.**
