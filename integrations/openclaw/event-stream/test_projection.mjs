import assert from "node:assert/strict";
import {
  digestIdentity,
  extractRunSequence,
  makeControlRecord,
  projectEventFrame,
  projectPayload,
} from "./projection.mjs";

{
  const projected = projectPayload({
    sessionKey: "agent:main:private-peer",
    sessionId: "private-session",
    runId: "run-1",
    status: "started",
    message: { content: "secret transcript" },
    text: "secret text",
    toolArgs: { path: "/secret" },
    result: "secret result",
    activeRunIds: ["run-1", "run-2"],
  });
  assert.equal(projected.runId, "run-1");
  assert.equal(projected.status, "started");
  assert.equal(projected.sessionKeyDigest, digestIdentity("agent:main:private-peer"));
  assert.equal(projected.sessionIdDigest, digestIdentity("private-session"));
  assert.equal(projected.rawPayloadPersisted, false);
  assert.ok(projected.redactedContentFieldsPresent.includes("message"));
  assert.ok(projected.redactedContentFieldsPresent.includes("text"));
  assert.ok(projected.redactedContentFieldsPresent.includes("toolArgs"));
  assert.ok(projected.redactedContentFieldsPresent.includes("result"));
  assert.equal("message" in projected, false);
  assert.equal("text" in projected, false);
  assert.equal("toolArgs" in projected, false);
  assert.equal("result" in projected, false);
  assert.deepEqual(projected.activeRunIdDigests, [digestIdentity("run-1"), digestIdentity("run-2")]);
}

{
  const hint = projectEventFrame({
    type: "event",
    event: "session.message",
    seq: 17,
    payload: {
      sessionKey: "agent:main:main",
      message: { role: "assistant", content: "never persist" },
    },
  }, 3);
  assert.equal(hint.recordType, "openclaw_gateway_event_hint");
  assert.equal(hint.connectionEpoch, 3);
  assert.equal(hint.outerSequence, 17);
  assert.equal(hint.semantics.durableHistoryAuthority, false);
  assert.equal(hint.semantics.auditReconciliationRequired, true);
  assert.equal(hint.semantics.observeCommitPerformed, false);
  assert.equal(hint.semantics.verificationCreated, false);
  assert.equal(hint.semantics.automaticPlanCompletion, false);
  assert.equal(hint.semantics.automaticRollback, false);
}

{
  assert.equal(projectEventFrame({ type: "event", event: "tick", seq: 1, payload: { ts: 1 } }, 1), null);
  assert.deepEqual(extractRunSequence({
    type: "event",
    event: "agent",
    payload: { runId: "run-9", seq: 4, text: "secret" },
  }), { runId: "run-9", seq: 4 });
}

{
  const record = makeControlRecord("openclaw_gateway_connection_sequence_gap", {
    expectedOuterSequence: 10,
    receivedOuterSequence: 12,
  }, 2);
  assert.equal(record.semantics.auditReconciliationRequired, true);
  assert.equal(record.semantics.worldCommitAuthority, false);
  assert.equal(record.semantics.truthPromotionAuthority, false);
  assert.equal(record.semantics.memoryOverwriteAuthority, false);
}

console.log("kuuos_openclaw_gateway_event_subscriber_v0_4 projection tests: OK");
