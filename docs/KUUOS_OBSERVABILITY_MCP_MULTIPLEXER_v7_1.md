# KuuOS Observability MCP Multiplexer v7.1

## 1. Purpose

v7.1 generalizes the v7.0 GitHub Actions bounded live-log work into a provider-independent observability boundary.

The key design rule is:

```text
provider availability != KuuOS authority
provider response != truth
one unavailable provider != global observation failure
```

The runtime therefore does not hard-wire one vendor as the canonical source of observability.

## 2. Active provider surfaces

The v7.1 registry supports these read-only provider operations:

### GitHub Actions

```text
GitHub.fetch_workflow_job_logs
```

This remains compatible with the existing v7.0 bounded live-log observer, which provides the stronger exact-head temporal polling semantics.

### Vercel

```text
Vercel.get_runtime_logs
Vercel.get_runtime_errors
Vercel.get_deployment_build_logs
```

Runtime logs and build logs permit bounded repeated observation by an external orchestrator. Runtime error clusters are marked one-shot preferred.

### Supabase

```text
Supabase.query_logs
```

The tool exposes a read-only log query surface. v7.1 additionally rejects plans whose SQL does not begin with `SELECT` or `WITH`, contains obvious write/DDL keywords, or contains multiple statements.

The tool contract says that polling this surface in a loop should not be used, so its registry policy is `one_shot_only`.

### Neon

```text
Neon.query_logs
```

The adapter validates the important contract constraints:

- `since` and `start_time` are mutually exclusive;
- `logql` is not combined with structured filters;
- `limit` stays in the provider range.

## 3. Datadog

Datadog is optional in v7.1.

Its availability is treated as a runtime environmental observation rather than a structural dependency. Connection, account, region and tenant compatibility may differ between environments.

A plan selecting an optional but unrouted provider returns:

```text
KUUOS_OBSERVABILITY_MCP_PROVIDER_UNAVAILABLE
```

without transferring authority and without blocking the registry paths of GitHub, Vercel, Supabase or Neon.

This is deliberate: the multiplexer must degrade by provider, not collapse globally.

## 4. Two-stage boundary

The multiplexer has two explicit stages.

### prepare

```text
typed plan
  -> provider/operation allowlist
  -> provider-specific payload validation
  -> typed external connector request
```

The runtime emits a request packet only. It does not call the connector inside the KuuOS kernel.

### ingest

```text
typed request
  + host connector result
  + exact request digest
  -> stale-result check
  -> normalized observation envelope
```

The host result must carry the exact digest of the request that produced it. A stale or crossed result is rejected before normalization.

## 5. No raw-log persistence

Provider results may contain application logs, errors, paths, request identifiers or other operational details.

The normalized observation does not reproduce those raw values.

Instead it persists:

- provider and operation;
- connector action;
- polling policy;
- data class;
- request digest;
- raw result digest;
- observed value digest;
- result kind;
- bounded top-level schema;
- item count when recognizable;
- error-signal count;
- first/last timestamp hints.

The raw host result remains a separate handoff artifact and is not copied into the normalized observation, receipt or audit record by this multiplexer.

## 6. Authority separation

Every valid plan requires:

```text
read_only = true
persist_raw_result = false
source_authority_transfer_allowed = false
```

The provider result contributes evidence only.

No provider result grants:

- merge authority;
- rerun authority;
- deployment authority;
- database mutation authority;
- theorem authority;
- institutional authority.

## 7. Provider-specific obstructions

v7.1 makes incompatibilities explicit instead of coercing one provider schema into another.

Examples:

```text
supabase_sql_not_read_only_query
supabase_sql_forbidden_keyword
neon_since_and_start_time_mutually_exclusive
neon_logql_and_structured_filters_mutually_exclusive
vercel_limit_out_of_bounds
github_job_id_invalid
raw_result_source_request_digest_mismatch
```

These are local obstructions. They do not imply that another provider is unavailable.

## 8. Relationship to v7.0

v7.0 is specialized and stronger for GitHub Actions temporal CI observation:

```text
exact HEAD SHA
  -> current run
  -> current job
  -> bounded tail
  -> delta
  -> terminal re-observation
```

v7.1 does not replace that logic.

Instead:

```text
v7.0 GitHub temporal observer
               \
                +--> v7.1 provider-normalized observation layer
               /
Vercel/Supabase/Neon snapshots
```

This preserves a specialized exact-head path where it matters while allowing other observability sources to descend into a common representation.

## 9. Validation

The focused checker verifies:

1. GitHub Actions request preparation;
2. Vercel prepare -> host result -> normalized ingest;
3. raw Vercel log message content is absent from normalized observation and receipt;
4. Supabase mutation-shaped SQL is rejected;
5. Neon LogQL/structured-filter incompatibility is rejected;
6. Datadog can be unavailable without producing a global blocker;
7. a raw result carrying the wrong request digest is rejected.

This is a runtime-only change. No Lean theorem files are modified, so Strict Lean is intentionally not required for the focused validation.

## 10. Next descent

The next useful layer is not another provider-specific adapter.

It is a temporal correlation layer:

```text
GitHub CI observation
Vercel runtime observation
Supabase log observation
Neon branch observation
        |
        v
provider-normalized envelopes
        |
        v
time-window compatibility
        |
        v
cross-provider correlation packet
```

That layer should preserve uncertainty: correlation is evidence of co-occurrence, not proof of causation.
