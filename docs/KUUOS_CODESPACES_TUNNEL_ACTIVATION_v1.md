# KuuOS / Codespaces / Secure MCP Tunnel: CLI activation v1

**Current status:** local tooling preparation only. ChatGPT-initiated remote
Lean calls have not been observed.

## Install the official client inside the running Codespace

The Codespaces Dev Container setup already checked the pinned KuuOS toolchain,
and the real KuuOS Lean-LSP MCP trial has been certified by GitHub Actions.

From the KuuOS repository root:

    bash scripts/install_kuuos_tunnel_client_v1.sh --install
    export PATH="$HOME/.local/bin:$PATH"
    bash scripts/install_kuuos_tunnel_client_v1.sh --check

This installs an OpenAI tunnel-client v0.0.20 **Linux** binary from the official
release, checks the matching upstream SHA256SUMS entry and only then copies
the executable under the user's home. It neither starts a tunnel nor writes
credentials. Failure to obtain an exact checksum is a hard failure.
Checking a checksum from the same release does not itself guarantee signed
provenance; use the official release signature separately if required.

Official release: https://github.com/openai/tunnel-client/releases/tag/v0.0.20

## Account-side private tunnel setup

The user needs an authorized Platform tunnel ID and a runtime API key.
Tunnels Read + Manage and Read + Use permissions are separate from permission
to create custom MCP plugins in the target ChatGPT workspace.
Do not add keys, IDs, secrets or account metadata to tracked files, PR comments
or GitHub Actions logs. The private tunnel uses outbound HTTPS:443 and does
not require a public MCP port.

Once a Codespace exists, the client is installed, and the required
permissions and credentials are available, follow the official instructions:

https://developers.openai.com/api/docs/guides/secure-mcp-tunnels

Example to run **locally within an active Codespace**, without writing a key:

    # Set TUNNEL_ID and CONTROL_PLANE_API_KEY securely outside tracked source.
    tunnel-client init --sample sample_mcp_stdio_local --profile kuuos-lean --tunnel-id "$TUNNEL_ID" --mcp-command "bash $PWD/scripts/run_kuuos_lean_mcp_stdio_v1.sh $PWD"
    tunnel-client doctor --profile kuuos-lean --explain
    tunnel-client run --profile kuuos-lean

Then in ChatGPT web: Plugins > Add custom MCP server > Tunnel.
Select the associated tunnel, review the risk warning, and connect the private
plugin. Actual availability depends on workspace permissions.

Codespaces stop on idle by default; they are not 24-hour server infrastructure.
GitHub Free personal-account compute: 120 core-hours/month; storage:
15 GB-month. Platform API key usage/billing is **not** included in that quota.

## Evidence boundaries

- Pinned Lean-LSP MCP on real KuuOS sample: passed, GitHub Actions.
- Dev Container runtime and same MCP trial: passed, GitHub Actions.
- OpenAI tunnel-client local CLI installation: subject to this PR's CI.
- Actual Codespace: not created through GitHub MCP in this conversation.
- Live Secure MCP Tunnel and ChatGPT MCP calls: not certified.
- PR #3522 / #3530 theorem correctness: independent Lean certification.

All 107 public roots, Lean v4.30.0-rc2, fixed mathlib SHA,
and protected PR #1558 remain unchanged.

## Zero-copy installation in Codespaces (added after first tunnel-client CI)

The opt-in Codespaces `postCreateCommand` now automatically invokes the
checksum-verified `scripts/install_kuuos_tunnel_client_v1.sh --install`
after the pinned Lean-LSP MCP installation. A user no longer needs to run
the CLI install manually when the setup succeeds; the commands in the earlier
section can be used to revalidate or recover a failed install. Set
`KUUOS_CODESPACES_SKIP_TUNNEL_CLIENT=1` only to deliberately create an
incomplete Codespace without the client. Automatic CLI installation does
not create an OpenAI Platform tunnel, runtime key or ChatGPT plugin.

Success for the Dev Container auto-install must be observed in the newest
`KuuOS Codespaces Lean MCP container runtime v1` CI run, not inferred
from the earlier standalone CLI-install CI.
