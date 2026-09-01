import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";

const VERSION = "kuuos_openclaw_control_bridge_v0_1";
const DEFAULT_POLICY_URL = "http://127.0.0.1:8765";
const DEFAULT_TIMEOUT_MS = 5000;
const DEFAULT_APPROVAL_TIMEOUT_MS = 120000;
const DEFAULT_MAX_PAYLOAD_CHARS = 8192;
const SECRET_KEY = /(authorization|cookie|token|secret|password|passwd|api[-_]?key|credential)/i;

function clampInt(value, fallback, min, max) {
  const n = Number(value);
  return Number.isFinite(n) ? Math.max(min, Math.min(max, Math.trunc(n))) : fallback;
}

function configFrom(api) {
  const raw = api.pluginConfig ?? {};
  return {
    policyUrl: typeof raw.policyUrl === "string" && raw.policyUrl.trim()
      ? raw.policyUrl.replace(/\/+$/, "")
      : DEFAULT_POLICY_URL,
    policyToken: typeof raw.policyToken === "string" ? raw.policyToken : "",
    allowRemotePolicyUrl: raw.allowRemotePolicyUrl === true,
    failClosed: raw.failClosed !== false,
    policyTimeoutMs: clampInt(raw.policyTimeoutMs, DEFAULT_TIMEOUT_MS, 100, 15000),
    approvalTimeoutMs: clampInt(
      raw.approvalTimeoutMs,
      DEFAULT_APPROVAL_TIMEOUT_MS,
      1000,
      600000,
    ),
    maxPayloadChars: clampInt(
      raw.maxPayloadChars,
      DEFAULT_MAX_PAYLOAD_CHARS,
      512,
      32768,
    ),
  };
}

function isLoopbackUrl(raw) {
  try {
    const url = new URL(raw);
    return (
      (url.protocol === "http:" || url.protocol === "https:") &&
      (url.hostname === "127.0.0.1" ||
        url.hostname === "localhost" ||
        url.hostname === "::1" ||
        url.hostname === "[::1]")
    );
  } catch {
    return false;
  }
}

function sanitize(value, depth = 0) {
  if (depth > 5) return "[depth-limit]";
  if (value === null || value === undefined) return value;
  if (typeof value === "string") return value.length > 2048 ? `${value.slice(0, 2048)}…` : value;
  if (typeof value === "number" || typeof value === "boolean") return value;
  if (Array.isArray(value)) return value.slice(0, 64).map((item) => sanitize(item, depth + 1));
  if (typeof value === "object") {
    const out = {};
    for (const [key, item] of Object.entries(value).slice(0, 128)) {
      out[key] = SECRET_KEY.test(key) ? "[redacted]" : sanitize(item, depth + 1);
    }
    return out;
  }
  return String(value);
}

function boundedPayload(value, maxChars) {
  const sanitized = sanitize(value);
  const encoded = JSON.stringify(sanitized);
  if (encoded.length <= maxChars) return sanitized;
  return {
    truncated: true,
    originalChars: encoded.length,
    preview: encoded.slice(0, maxChars),
  };
}

async function postJson(cfg, path, payload, signal) {
  const ownController = new AbortController();
  const timer = setTimeout(() => ownController.abort(), cfg.policyTimeoutMs);
  const onAbort = () => ownController.abort();
  signal?.addEventListener?.("abort", onAbort, { once: true });
  try {
    const headers = { "content-type": "application/json" };
    if (cfg.policyToken) headers.authorization = `Bearer ${cfg.policyToken}`;
    const response = await fetch(`${cfg.policyUrl}${path}`, {
      method: "POST",
      headers,
      body: JSON.stringify(payload),
      signal: ownController.signal,
    });
    if (!response.ok) throw new Error(`KuuOS policy HTTP ${response.status}`);
    return await response.json();
  } finally {
    clearTimeout(timer);
    signal?.removeEventListener?.("abort", onAbort);
  }
}

function preflightEnvelope(event, ctx, cfg) {
  return {
    version: VERSION,
    boundary: "ActOS.bounded_adapter_invocation",
    operation: "preflight",
    tool: {
      name: event.toolName,
      kind: event.toolKind ?? ctx.toolKind ?? null,
      inputKind: event.toolInputKind ?? ctx.toolInputKind ?? null,
      params: boundedPayload(event.params ?? {}, cfg.maxPayloadChars),
      derivedPaths: boundedPayload(event.derivedPaths ?? [], cfg.maxPayloadChars),
    },
    correlation: {
      runId: event.runId ?? ctx.runId ?? null,
      toolCallId: event.toolCallId ?? null,
      agentId: ctx.agentId ?? null,
      sessionKey: ctx.sessionKey ?? null,
      sessionId: ctx.sessionId ?? null,
    },
    requester: boundedPayload(ctx.requester ?? null, cfg.maxPayloadChars),
    invariants: {
      projectedOnly: true,
      worldCommit: false,
      automaticTruthPromotion: false,
      automaticPlanCompletion: false,
      automaticRollback: false,
    },
  };
}

function block(reason) {
  return {
    block: true,
    blockReason: reason || "Blocked by KuuOS policy.",
  };
}

export default definePluginEntry({
  id: "kuuos-control",
  name: "KuuOS Control Plane",
  description: "KuuOS fail-closed policy gate for OpenClaw tool execution.",
  register(api) {
    const cfg = configFrom(api);
    const remoteUrlAllowed = cfg.allowRemotePolicyUrl || isLoopbackUrl(cfg.policyUrl);

    api.on(
      "before_tool_call",
      async (event, ctx) => {
        if (!remoteUrlAllowed) {
          return block("KuuOS policy URL is non-loopback and allowRemotePolicyUrl is false.");
        }

        const envelope = preflightEnvelope(event, ctx, cfg);
        let policy;
        try {
          policy = await postJson(cfg, "/v1/preflight", envelope, ctx.abortSignal);
        } catch (error) {
          if (!cfg.failClosed) {
            api.logger?.warn?.(`KuuOS preflight unavailable; failClosed=false: ${String(error)}`);
            return;
          }
          return block(`KuuOS preflight unavailable: ${String(error)}`);
        }

        if (policy?.decision === "allow") return;

        if (policy?.decision === "approval") {
          const receiptId = typeof policy.receiptId === "string" ? policy.receiptId : null;
          return {
            requireApproval: {
              title: typeof policy.title === "string" ? policy.title : `KuuOS: ${event.toolName}`,
              description:
                typeof policy.description === "string"
                  ? policy.description
                  : "KuuOS requires explicit approval for this bounded external effect.",
              severity:
                policy.severity === "info" ||
                policy.severity === "warning" ||
                policy.severity === "critical"
                  ? policy.severity
                  : "warning",
              timeoutMs: cfg.approvalTimeoutMs,
              allowedDecisions: ["allow-once", "allow-always", "deny"],
              onResolution: async (decision) => {
                try {
                  await postJson(cfg, "/v1/approval-resolution", {
                    version: VERSION,
                    receiptId,
                    decision,
                    toolName: event.toolName,
                    runId: event.runId ?? ctx.runId ?? null,
                    toolCallId: event.toolCallId ?? null,
                  });
                } catch (error) {
                  api.logger?.warn?.(`KuuOS approval receipt failed: ${String(error)}`);
                }
              },
            },
          };
        }

        if (policy?.decision === "deny") {
          return block(typeof policy.reason === "string" ? policy.reason : "Denied by KuuOS policy.");
        }

        return cfg.failClosed
          ? block("KuuOS preflight returned an invalid decision.")
          : undefined;
      },
      { priority: 1000, timeoutMs: cfg.policyTimeoutMs },
    );

    api.on(
      "after_tool_call",
      async (event, ctx) => {
        if (!remoteUrlAllowed) return;
        const payload = {
          version: VERSION,
          boundary: "ActOS.canonical_host_receipt",
          operation: "post-effect",
          toolName: event.toolName,
          runId: event.runId ?? ctx.runId ?? null,
          toolCallId: event.toolCallId ?? null,
          durationMs: event.durationMs ?? null,
          error: boundedPayload(event.error ?? null, cfg.maxPayloadChars),
          result: boundedPayload(event.result ?? null, cfg.maxPayloadChars),
          invariants: {
            hostReceiptIsWorldCommit: false,
            hostReceiptIsWorldTruth: false,
            observationRequired: true,
            verificationRequired: true,
            automaticPlanCompletion: false,
            automaticRollback: false,
          },
        };
        try {
          await postJson(cfg, "/v1/post-effect", payload);
        } catch (error) {
          api.logger?.warn?.(
            `KuuOS post-effect receipt failed; observation/verification debt remains open: ${String(error)}`,
          );
        }
      },
      { priority: 1000, timeoutMs: cfg.policyTimeoutMs },
    );
  },
});
