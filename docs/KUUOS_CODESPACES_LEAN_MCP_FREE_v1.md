# KuuOS Lean MCP on GitHub Codespaces — opt-in free tier v1

## Status and objective

This additive development environment is an **opt-in** Codespaces configuration
for the existing KuuOS Lean-LSP MCP activation PR. It is not a Codespace that
has already been created or connected to ChatGPT.

Read this with:
- `docs/KUUOS_LEAN_LSP_MCP_COMPATIBILITY_v7_17.md`: pinned MCP/LSP compatibility receipt;
- `docs/KUUOS_LEAN_MCP_CHATGPT_TUNNEL_v1.md`: private ChatGPT tunnel setup;
- `scripts/run_kuuos_lean_mcp_stdio_v1.sh`: fail-closed Lean MCP launcher;
- `scripts/check_kuuos_lean_lsp_mcp_multi_attempt_v1.py`: real MCP goal/trial probe.

Fixed KuuOS pins:
- Lean `leanprover/lean4:v4.30.0-rc2`.
- mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`.
- published root count 107, main is canonical.

There is **no** alteration of existing Lean source, mathlib manifest, imports,
root registrations, or GitHub Actions certification standards.

## Creating a Codespace (requires a user-owned GitHub account action)

1. Open https://github.com/itakura-hidetoshi/KuuOS/pull/3535
   and choose the PR head branch:
   `feat/lean-mcp-chatgpt-tunnel-pinned-v1-20261113`.
2. Choose **Code > Codespaces > Create codespace / New with options**.
3. Select the **KuuOS — pinned Lean MCP** configuration
   (`.devcontainer/lean-mcp/devcontainer.json`), **2-core machine**,
   and check **who pays** before creating it.
4. The post-create hook automatically checks the pins, installs the exact Lean
   toolchain, installs uv/lean-lsp-mcp==0.30.0, and fetches the pinned
   Mathlib build cache. It intentionally does NOT compile the full KuuOS
   10k+ module closure.
5. Run the *actual* local semantic smoke test in the Codespaces terminal:

       bash scripts/bootstrap_kuuos_codespaces_lean_mcp_v1.sh --smoke

   This uses existing `DependentOriginationFunctorialTransportV0_1.lean`
   and invokes `lean_goal` and `lean_multi_attempt` with three tactic
   candidates through real stdio MCP. The generated receipt in the
   Codespace workspace is untracked; do not commit it as theorem authority.

If the Mathlib cache cannot be fetched due to disk/network limits, leave the
failure visible. Repeated installs and post-create retries do not change the
repository's pins. Set `KUUOS_CODESPACES_SKIP_MATHLIB_CACHE=1` before
the installer only as a consciously **incomplete** initialization; then
fetch the cache before attempting the live smoke test.

## Cost / automatic stop

GitHub's personal **Free** included quota (subject to account settings) is
120 core-hours and 15 GB-month storage, not 120 wall-clock hours on 2 CPU.
A 2-core Codespace therefore uses 2 core-hours per running hour
(approximately 60 wall-clock hours maximum before other usage).

Review remaining allowance and billing in GitHub Settings > Billing &
plans / Usage and budgets. Set spending limit to 0 or stop usage at the budget
limit if required. **A successful setup does not establish cost-free operation
indefinitely.** Storage usage continues while Codespace is stopped.

The default idle timeout is 30 minutes. Actively stop the Codespace when a
session ends. Do not run tunnel-client as a 24-hour daemon on free Codespaces;
the idle timeout disconnects the tunnel and uninterrupted uptime is not
promised. Avoid prebuilds and delete unused Codespaces to reduce storage cost.

## ChatGPT connection — separate acceptance step

After local smoke success, follow OpenAI's official private tunnel setup:
https://developers.openai.com/api/docs/guides/secure-mcp-tunnels

- The ChatGPT/Platform account must have permission to create/use a tunnel.
- The runtime API key and tunnel ID are entered only into the live Codespace
  environment via trusted secret-management paths, never in tracked files.
- Run `tunnel-client doctor` and `tunnel-client run` as in the linked
  activation runbook while Codespaces is active.
- In ChatGPT web Plugins, add a private custom MCP server using Tunnel.
- Verify a `lean_goal` call from ChatGPT, **not** merely a local MCP call.

The GitHub MCP connection available in ChatGPT has no Codespaces create/start
action in this workflow. No Codespace is created by PR construction.

## Proof repair and certification

A successful local smoke does not certify PR #3522 or #3530. It validates only
the representative test file. The PR #3522 head, imports, dependent signatures,
pinned mathlib API, and complete failing source must be checked in the new
Codespace before attempting repair.

In a running Codespace do not silently apply a fix to the main branch. Use
the GitHub MCP-authorized source mutation route and exact-source CI, preserving
append-only/tighten-only/same-root policy and the protected #1558 PR state.

Status vocabulary:
- `codespaces_profile_static_verified`: only JSON, Bash and pin preflight.
- `codespaces_instance_live`: actual user-created Codespace observed.
- `mcp_semantics_live`: real `lean_goal` and `lean_multi_attempt` observed.
- `chatgpt_tunnel_connected`: successful ChatGPT-initiated tool invocation.
- `theorem_certified`: independent fixed-HEAD Strict Lean and axiom audit.

These are different evidence levels. Local compatibility ≠ remote availability
≠ theorem proof.

Sources:
- GitHub Free Codespaces billing: https://docs.github.com/en/billing/concepts/product-billing/github-codespaces
- Included-usage guidance: https://docs.github.com/en/codespaces/troubleshooting/troubleshooting-included-usage
- Codespaces dev containers: https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers
- OpenAI Secure MCP Tunnel: https://developers.openai.com/api/docs/guides/secure-mcp-tunnels
