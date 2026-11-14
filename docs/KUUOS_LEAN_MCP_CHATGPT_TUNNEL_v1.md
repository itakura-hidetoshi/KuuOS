# KuuOS Lean-LSP MCP -> ChatGPT Secure Tunnel, activation v1

## Scope and current evidence

This is an additive operator launcher for an existing project, not an installed
remote service. The previous v7.17 live MCP receipt established that
lean-lsp-mcp==0.30.0 can initialize and obtain real outline/diagnostics
from KuuOS with Lean v4.30.0-rc2 and mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.

That evidence did not test end-to-end ChatGPT access or
lean_multi_attempt. Neither is claimed certified by this document.

## What is added

scripts/run_kuuos_lean_mcp_stdio_v1.sh:
- Requires an absolute KuuOS checkout path.
- Rejects any other lean-toolchain or mathlib manifest revision.
- Launches the previously tested lean-lsp-mcp==0.30.0 over stdio.
- Leaves lean_goal, lean_diagnostic_messages, lean_file_outline,
  lean_multi_attempt, and lean_verify available.
- By default excludes lean_run_code, lean_build, external searches, and
  other high-effect tools. These controls do NOT sandbox Lean tactics:
  Lean tactic elaboration and imported initialization can still perform IO.
- Does not commit credentials, change Lean files, or grant GitHub write authority.

## Operator preflight on isolated Linux / existing Runpod Pod

Use an existing KuuOS project checkout. Do not replace its pinned toolchain
or regenerate lake-manifest.json. Do not point this launcher at a home directory.

    bash /absolute/KuuOS/scripts/run_kuuos_lean_mcp_stdio_v1.sh --check-pins /absolute/KuuOS

Ensure Python 3, uv (uvx), elan/Lake and the project's pinned Lean installation
are available. The existing v7.17 CI is the build/setup reference. From
inside the isolated project directory, populate Mathlib build caches with:

    lake exe cache get

To repeat the existing narrow v7.17 proof of interoperability:

    PYTHONPATH=. python3 scripts/check_kuuos_lean_lsp_mcp_compatibility_v7_17.py --repository-root . --live-probe --receipt /tmp/kuuos-lean-mcp-v7-17.json

The v7.17 compatibility probe disables lean_multi_attempt intentionally.
Its success cannot be relabeled as a multi-attempt or ChatGPT connection test.

## Secure connection from ChatGPT

Use OpenAI Secure MCP Tunnel, not a publicly exposed unauthenticated port.
The Linux/Runpod host requires outbound HTTPS to api.openai.com:443 and must
keep the tunnel client running. Install tunnel-client using the current
official OpenAI documentation: https://developers.openai.com/api/docs/guides/secure-mcp-tunnels

Create or reuse a tunnel in Platform tunnel settings; associate the correct
ChatGPT workspace and Platform organization, and verify the Tunnels permissions.
Supply the runtime CONTROL_PLANE_API_KEY securely through the host's secret
manager/environment, not in a command-line argument or repository file.

Set an operator-controlled TUNNEL_ID and use absolute paths:

    tunnel-client init --sample sample_mcp_stdio_local --profile kuuos-lean --tunnel-id "$TUNNEL_ID" --mcp-command "bash /absolute/KuuOS/scripts/run_kuuos_lean_mcp_stdio_v1.sh /absolute/KuuOS"
    tunnel-client doctor --profile kuuos-lean --explain
    tunnel-client run --profile kuuos-lean

Then on ChatGPT **web**, go to Plugins -> Add custom MCP server -> Connection:
Tunnel, select the same tunnel and create the private plugin. This explicit
account-side step cannot be performed by a GitHub commit.

A separate official Runpod infrastructure-management MCP server exists at
https://mcp.runpod.io/ . It can manage Pods when connected, but does not run
Lean by itself. It is not required for this launcher.

## Real proof-repair acceptance test (not yet performed)

1. On the exact selected PR #3522 HEAD, confirm the source file digest for
   formal/KUOS/DependentOriginationStandardTypeAScaledLeibnizPushoutV1_55.lean.
   Do not substitute a previous HEAD's cached analysis.
2. In ChatGPT call the newly connected Lean MCP tool listing, then
   lean_file_outline and lean_diagnostic_messages on that entire source file.
3. Call lean_goal on a currently observed proof line, then lean_multi_attempt
   using candidate tactics chosen from that actual proof context.
4. Reobserve diagnostics on the same source digest. Record actual goal,
   attempt diagnostics, selected source SHA, and whether any sorryAx exists.
5. Only after a matching exact-source GitHub Actions Strict Lean terminal
   SUCCESS, independent axiom audit, and tree reconciliation may source
   changes be called certified.

Success states are independent:
- package compatibility: existing v7.17 receipt;
- host launch: not yet observed;
- live tunnel: not yet observed;
- ChatGPT tool call: not yet observed;
- v1.55 repair: not certified by this installation work.

## Safety and governance

Use a dedicated unprivileged isolated Pod/container with minimum filesystem
and network access. Prefer read-only theorem source with separately writable
caches. No inbound public MCP port is needed. Never put runtime API keys
or TUNNEL_ID values in repository files or CI logs. Lean snippets/tactics
may perform IO even when the MCP server describes trials as in-memory.

Keep #3522 parent, #3530 validation child, and protected #1558 unchanged.
Respect append-only, tighten-only, overwrite-forbidden, same-root and the
107 published-root boundary. Compatibility and a successful proof candidate
do not confer repository-write authority or Lean theorem certification.
