import crypto from "node:crypto";

export const VERSION = "kuuos_openclaw_gateway_event_subscriber_v0_4";
export const SOURCE = "openclaw.gateway.websocket.events";
export const SUPPORTED_EVENTS = new Set([
  "sessions.changed",
  "session.message",
  "session.operation",
  "session.tool",
  "agent",
  "shutdown",
]);

const SAFE_STRING_FIELDS = [
  "runId",
  "agentId",
  "toolCallId",
  "toolName",
  "status",
  "phase",
  "action",
  "kind",
  "operationId",
  "operation",
  "reasonCode",
  "errorCode",
  "channel",
  "direction",
];
const SENSITIVE_IDENTITY_FIELDS = ["sessionKey", "sessionId"];
const CONTENT_FIELDS = [
  "message",
  "messages",
  "text",
  "deltaText",
  "content",
  "prompt",
  "toolArgs",
  "args",
  "result",
  "output",
  "error",
  "errorText",
];

export function canonicalJson(value) {
  if (value === null || typeof value !== "object") {
    return JSON.stringify(value);
  }
  if (Array.isArray(value)) {
    return `[${value.map((item) => canonicalJson(item)).join(",")}]`;
  }
  const keys = Object.keys(value).sort();
  return `{${keys.map((key) => `${JSON.stringify(key)}:${canonicalJson(value[key])}`).join(",")}}`;
}

export function digest(value) {
  return crypto.createHash("sha256").update(canonicalJson(value), "utf8").digest("hex");
}

export function digestIdentity(value) {
  return digest({ identity: String(value) });
}

function isRecord(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

export function projectPayload(payload) {
  if (!isRecord(payload)) {
    return {
      payloadKind: payload === undefined ? "absent" : Array.isArray(payload) ? "array" : typeof payload,
      rawPayloadPersisted: false,
    };
  }

  const projected = {
    payloadKind: "object",
    payloadTopLevelKeys: Object.keys(payload).sort().slice(0, 128),
    rawPayloadPersisted: false,
  };

  for (const key of SAFE_STRING_FIELDS) {
    const value = payload[key];
    if (typeof value === "string" && value.length > 0 && value.length <= 512) {
      projected[key] = value;
    }
  }
  for (const key of SENSITIVE_IDENTITY_FIELDS) {
    const value = payload[key];
    if (typeof value === "string" && value.length > 0) {
      projected[`${key}Digest`] = digestIdentity(value);
    }
  }
  if (typeof payload.hasActiveRun === "boolean") {
    projected.hasActiveRun = payload.hasActiveRun;
  }
  if (Array.isArray(payload.activeRunIds)) {
    projected.activeRunIdDigests = payload.activeRunIds
      .filter((value) => typeof value === "string" && value.length > 0)
      .slice(0, 128)
      .map((value) => digestIdentity(value));
  }
  if (Number.isSafeInteger(payload.seq) && payload.seq >= 0) {
    projected.runSequence = payload.seq;
  }
  if (Number.isSafeInteger(payload.ts) && payload.ts >= 0) {
    projected.sourceTimestamp = payload.ts;
  }
  projected.redactedContentFieldsPresent = CONTENT_FIELDS.filter((key) => key in payload);
  return projected;
}

export function projectEventFrame(frame, connectionEpoch) {
  if (!isRecord(frame) || frame.type !== "event" || typeof frame.event !== "string") {
    throw new Error("invalid OpenClaw Gateway event frame");
  }
  if (!SUPPORTED_EVENTS.has(frame.event)) {
    return null;
  }
  if (frame.seq !== undefined && (!Number.isSafeInteger(frame.seq) || frame.seq < 0)) {
    throw new Error("invalid OpenClaw Gateway outer event sequence");
  }
  return {
    version: VERSION,
    recordType: "openclaw_gateway_event_hint",
    source: SOURCE,
    eventName: frame.event,
    connectionEpoch,
    outerSequence: frame.seq ?? null,
    payload: projectPayload(frame.payload),
    semantics: {
      lowLatencyHint: true,
      durableHistoryAuthority: false,
      auditReconciliationRequired: true,
      observeOwnerReviewRequired: true,
      observeCommitPerformed: false,
      verificationCreated: false,
      worldCommitAuthority: false,
      truthPromotionAuthority: false,
      planCompletionAuthority: false,
      automaticPlanCompletion: false,
      rollbackProofAuthority: false,
      automaticRollback: false,
      memoryOverwriteAuthority: false,
    },
  };
}

export function extractRunSequence(frame) {
  if (!isRecord(frame) || frame.event !== "agent" || !isRecord(frame.payload)) {
    return null;
  }
  const runId = frame.payload.runId;
  const seq = frame.payload.seq;
  if (typeof runId !== "string" || !runId || !Number.isSafeInteger(seq) || seq < 0) {
    return null;
  }
  return { runId, seq };
}

export function makeControlRecord(kind, payload, connectionEpoch) {
  return {
    version: VERSION,
    recordType: kind,
    source: SOURCE,
    connectionEpoch,
    payload,
    semantics: {
      lowLatencyHint: true,
      durableHistoryAuthority: false,
      auditReconciliationRequired: true,
      observeCommitPerformed: false,
      verificationCreated: false,
      worldCommitAuthority: false,
      truthPromotionAuthority: false,
      automaticPlanCompletion: false,
      automaticRollback: false,
      memoryOverwriteAuthority: false,
    },
  };
}
