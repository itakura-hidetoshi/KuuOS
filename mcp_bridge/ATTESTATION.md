# KuuOS MCP deployment attestation

`kuuos-mcp-attest` verifies the public, non-secret `/healthz` receipt of a deployed KuuOS Chat–Work MCP bridge. It is intentionally independent of the deployment provider and uses only the Python standard library at runtime.

The verifier fails closed unless the health response contains the full contract:

- `ok`
- `mode`
- `backend`
- `version`
- `oauth_enabled`
- `oauth_mode`
- `write_ready`
- `canonical_sha`

It always requires an exact expected canonical SHA. Optional expectations can additionally pin the backend, OAuth mode, OAuth enablement, read/write mode, and write readiness.

Example for a staging deployment that has PostgreSQL and embedded OAuth configured but deliberately keeps write tools disabled:

```bash
kuuos-mcp-attest 'https://staging.example' \
  --expected-canonical-sha '<exact-canonical-sha>' \
  --expected-backend 'PostgresStateStore' \
  --expected-oauth-enabled true \
  --expected-oauth-mode embedded \
  --expected-mode read-only \
  --expected-write-ready false
```

The verifier also enforces internal consistency independent of the requested expectations. Embedded OAuth cannot attest against a non-PostgreSQL backend. `write_ready=true` requires read-write mode, PostgreSQL, and OAuth. OAuth enablement and OAuth mode must agree. The state version must be a non-negative integer.

Remote attestation requires HTTPS. Plain HTTP is accepted only for localhost/loopback when `--allow-http-localhost` is explicitly supplied. Credential-bearing URLs, cross-origin redirects, non-JSON responses, and oversized health receipts are rejected.

The command emits a small JSON receipt containing only the health URL and the non-secret observed fields. On any mismatch it exits non-zero and writes a compact JSON error receipt to stderr.

## Staging observation workflow

`.github/workflows/mcp-staging-attestation.yml` observes the current public Replit staging endpoint from a GitHub-hosted runner whenever MCP bridge code changes. The observation is deliberately non-gating: a stale or temporarily unavailable staging deployment is recorded without invalidating repository code CI. On pull requests the expected canonical SHA is the PR base SHA, so the check asks whether staging is still synchronized with the authoritative base rather than with unmerged code.

The same workflow can be dispatched manually with an arbitrary HTTPS base URL and expected SHA. Production promotion should still require a human- or automation-reviewed successful attestation before write enablement.
