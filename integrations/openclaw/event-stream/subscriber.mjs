#!/usr/bin/env node
import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import process from "node:process";
import { parseArgs } from "node:util";

import { GatewayClient } from "@openclaw/gateway-client";
import {
  GATEWAY_CLIENT_CAPS,
  GATEWAY_CLIENT_MODES,
  GATEWAY_CLIENT_NAMES,
} from "@openclaw/gateway-protocol/client-info";
import { PROTOCOL_VERSION } from "@openclaw/gateway-protocol/version";

import {
  VERSION,
  digest,
  digestIdentity,
  extractRunSequence,
  makeControlRecord,
  projectEventFrame,
} from "./projection.mjs";

const DEFAULT_GATEWAY_URL = "ws://127.0.0.1:18789";
const DEFAULT_DATA_DIR = path.join(os.homedir(), ".kuuos", "openclaw");
const IDENTITY_FILE = "gateway-event-device-identity.json";
const TOKEN_FILE = "gateway-event-device-token.json";
const HINT_LEDGER_FILE = "gateway-event-hints.jsonl";

function ensurePrivateDir(directory) {
  fs.mkdirSync(directory, { recursive: true, mode: 0o700 });
  try {
    fs.chmodSync(directory, 0o700);
  } catch {
    // Best effort on platforms without POSIX mode semantics.
  }
}

function atomicWritePrivateJson(filePath, value) {
  const directory = path.dirname(filePath);
  ensurePrivateDir(directory);
  const tempPath = `${filePath}.tmp-${process.pid}-${crypto.randomBytes(6).toString("hex")}`;
  fs.writeFileSync(tempPath, `${JSON.stringify(value, null, 2)}\n`, { encoding: "utf8", mode: 0o600 });
  try {
    fs.chmodSync(tempPath, 0o600);
  } catch {
    // Best effort on platforms without POSIX mode semantics.
  }
  fs.renameSync(tempPath, filePath);
}

function publicKeyRawBase64UrlFromPem(publicKeyPem) {
  const key = crypto.createPublicKey(publicKeyPem);
  if (key.asymmetricKeyType !== "ed25519") {
    throw new Error("stored Gateway event identity is not Ed25519");
  }
  const jwk = key.export({ format: "jwk" });
  if (jwk.kty !== "OKP" || jwk.crv !== "Ed25519" || typeof jwk.x !== "string") {
    throw new Error("unable to export canonical Ed25519 public key")
  }
  return jwk.x;
}

function deriveDeviceId(publicKeyPem) {
  const raw = Buffer.from(publicKeyRawBase64UrlFromPem(publicKeyPem), "base64url");
  return crypto.createHash("sha256").update(raw).digest("hex");
}

function signDevicePayload(privateKeyPem, payload) {
  const key = crypto.createPrivateKey(privateKeyPem);
  if (key.asymmetricKeyType !== "ed25519") {
    throw new Error("stored Gateway event identity private key is not Ed25519");
  }
  return crypto.sign(null, Buffer.from(payload, "utf8"), key).toString("base64url");
}

class EventSubscriberState {
  constructor(dataDir) {
    this.dataDir = dataDir;
    ensurePrivateDir(dataDir);
    this.identityPath = path.join(dataDir, IDENTITY_FILE);
    this.tokenPath = path.join(dataDir, TOKEN_FILE);
    this.ledgerPath = path.join(dataDir, HINT_LEDGER_FILE);
  }

  loadOrCreateDeviceIdentity() {
    if (fs.existsSync(this.identityPath)) {
      const value = JSON.parse(fs.readFileSync(this.identityPath, "utf8"));
      if (
        !value ||
        typeof value.deviceId !== "string" ||
        typeof value.publicKeyPem !== "string" ||
        typeof value.privateKeyPem !== "string"
      ) {
        throw new Error("invalid KuuOS OpenClaw event subscriber identity file");
      }
      const derived = deriveDeviceId(value.publicKeyPem);
      if (derived !== value.deviceId) {
        throw new Error("KuuOS OpenClaw event subscriber identity deviceId mismatch");
      }
      return value;
    }

    const { publicKey, privateKey } = crypto.generateKeyPairSync("ed25519");
    const publicKeyPem = publicKey.export({ type: "spki", format: "pem" }).toString();
    const privateKeyPem = privateKey.export({ type: "pkcs8", format: "pem" }).toString();
    const identity = {
      deviceId: deriveDeviceId(publicKeyPem),
      publicKeyPem,
      privateKeyPem,
    };
    atomicWritePrivateJson(this.identityPath, identity);
    return identity;
  }

  loadDeviceAuthToken({ deviceId, role }) {
    if (!fs.existsSync(this.tokenPath)) {
      return null;
    }
    const value = JSON.parse(fs.readFileSync(this.tokenPath, "utf8"));
    if (
      !value ||
      value.deviceId !== deviceId ||
      value.role !== role ||
      typeof value.token !== "string" ||
      !Array.isArray(value.scopes)
    ) {
      return null;
    }
    return { token: value.token, scopes: value.scopes.filter((item) => typeof item === "string") };
  }

  storeDeviceAuthToken({ deviceId, role, token, scopes }) {
    atomicWritePrivateJson(this.tokenPath, {
      version: VERSION,
      deviceId,
      role,
      token,
      scopes,
      storedAtUnixMs: Date.now(),
    });
  }

  clearDeviceAuthToken({ deviceId, role }) {
    const current = this.loadDeviceAuthToken({ deviceId, role });
    if (current && fs.existsSync(this.tokenPath)) {
      fs.rmSync(this.tokenPath);
    }
  }

  append(record) {
    const nowNs = BigInt(Date.now()) * 1_000_000n + BigInt(process.hrtime.bigint() % 1_000_000n);
    const body = {
      ...record,
      recordedAtUnixNs: nowNs.toString(),
    };
    body.recordDigest = digest(body);
    body.recordId = `kuuos-oc-live-${body.recordedAtUnixNs}-${body.recordDigest.slice(0, 16)}`;
    fs.appendFileSync(this.ledgerPath, `${JSON.stringify(body)}\n`, { encoding: "utf8", mode: 0o600 });
    try {
      fs.chmodSync(this.ledgerPath, 0o600);
    } catch {
      // Best effort on platforms without POSIX mode semantics.
    }
    return body;
  }
}

function isLoopbackHostname(hostname) {
  return hostname === "127.0.0.1" || hostname === "localhost" || hostname === "::1";
}

function validateGatewayUrl(raw, allowRemote) {
  const url = new URL(raw);
  if (!new Set(["ws:", "wss:"]).has(url.protocol)) {
    throw new Error("Gateway URL must use ws:// or wss://");
  }
  if (url.username || url.password || url.search || url.hash) {
    throw new Error("Gateway URL must not contain credentials, query parameters, or fragments");
  }
  if (!isLoopbackHostname(url.hostname)) {
    if (!allowRemote) {
      throw new Error("remote Gateway requires explicit --allow-remote-gateway");
    }
    if (url.protocol !== "wss:") {
      throw new Error("remote Gateway requires wss://");
    }
  }
  return url.toString();
}

function parseOptions() {
  const { values } = parseArgs({
    options: {
      "gateway-url": { type: "string", default: process.env.OPENCLAW_GATEWAY_URL ?? DEFAULT_GATEWAY_URL },
      "allow-remote-gateway": { type: "boolean", default: false },
      "data-dir": { type: "string", default: process.env.KUUOS_OPENCLAW_DATA_DIR ?? DEFAULT_DATA_DIR },
      "session-key": { type: "string", multiple: true, default: [] },
      "session-limit": { type: "string", default: "60" },
    },
    strict: true,
    allowPositionals: false,
  });
  const sessionLimit = Number(values["session-limit"]);
  if (!Number.isSafeInteger(sessionLimit) || sessionLimit < 1 || sessionLimit > 200) {
    throw new Error("--session-limit must be an integer between 1 and 200");
  }
  const sessionKeys = [...new Set(values["session-key"].map((key) => key.trim()).filter(Boolean))];
  return {
    gatewayUrl: validateGatewayUrl(values["gateway-url"], values["allow-remote-gateway"]),
    dataDir: path.resolve(values["data-dir"].replace(/^~(?=$|\/)/, os.homedir())),
    sessionKeys,
    sessionLimit,
  };
}

function safeErrorDescriptor(error) {
  const name = error instanceof Error ? error.name : "UnknownError";
  const message = error instanceof Error ? error.message : String(error);
  return {
    errorClass: name,
    errorMessageDigest: digest(message),
    pairingMayBeRequired: /pairing|required device|PAIRING_REQUIRED/i.test(message),
  };
}

async function main() {
  const options = parseOptions();
  const state = new EventSubscriberState(options.dataDir);
  let connectionEpoch = 0;
  const runSequences = new Map();
  let bootstrapSerial = 0;
  let stopped = false;

  const hostDeps = {
    loadOrCreateDeviceIdentity: () => state.loadOrCreateDeviceIdentity(),
    signDevicePayload,
    publicKeyRawBase64UrlFromPem,
    loadDeviceAuthToken: (params) => state.loadDeviceAuthToken(params),
    storeDeviceAuthToken: (params) => state.storeDeviceAuthToken(params),
    clearDeviceAuthToken: (params) => state.clearDeviceAuthToken(params),
    logDebug: () => {},
    logError: () => {},
    redactForLog: (message) => message.replace(/(token|password)=([^&\s]+)/gi, "$1=***"),
    normalizeTlsFingerprint: (fingerprint) => fingerprint?.trim().toLowerCase() ?? "",
  };

  let client;
  const subscribeForConnection = async (epoch, serial) => {
    try {
      const roster = await client.request("sessions.subscribe", {
        limit: options.sessionLimit,
        ownerFirst: true,
      });
      if (stopped || epoch !== connectionEpoch || serial !== bootstrapSerial) {
        return;
      }
      const list = roster && typeof roster === "object" && roster.list && typeof roster.list === "object"
        ? roster.list
        : null;
      const rows = list && Array.isArray(list.sessions)
        ? list.sessions
        : list && Array.isArray(list.rows)
          ? list.rows
          : [];
      state.append(makeControlRecord("openclaw_gateway_session_roster_subscribed", {
        sessionSnapshotRowCount: rows.length,
        rawSnapshotPersisted: false,
        auditReconciliationRequired: true,
      }, epoch));

      for (const key of options.sessionKeys) {
        const response = await client.request("sessions.messages.subscribe", { key });
        if (stopped || epoch !== connectionEpoch || serial !== bootstrapSerial) {
          return;
        }
        const canonicalKey = response && typeof response === "object" && typeof response.key === "string"
          ? response.key
          : key;
        state.append(makeControlRecord("openclaw_gateway_session_messages_subscribed", {
          requestedSessionKeyDigest: digestIdentity(key),
          canonicalSessionKeyDigest: digestIdentity(canonicalKey),
          includeApprovals: false,
          auditReconciliationRequired: true,
        }, epoch));
      }
    } catch (error) {
      if (!stopped && epoch === connectionEpoch && serial === bootstrapSerial) {
        state.append(makeControlRecord("openclaw_gateway_subscription_error", {
          ...safeErrorDescriptor(error),
          auditReconciliationRequired: true,
        }, epoch));
      }
    }
  };

  client = new GatewayClient({
    url: options.gatewayUrl,
    bootstrapToken: process.env.OPENCLAW_GATEWAY_BOOTSTRAP_TOKEN,
    password: process.env.OPENCLAW_GATEWAY_PASSWORD,
    clientName: GATEWAY_CLIENT_NAMES.GATEWAY_CLIENT,
    clientDisplayName: "KuuOS OpenClaw ObserveOS event subscriber",
    clientVersion: "0.4.0",
    platform: process.platform,
    mode: GATEWAY_CLIENT_MODES.BACKEND,
    role: "operator",
    scopes: ["operator.read"],
    caps: [
      GATEWAY_CLIENT_CAPS.SESSION_SCOPED_EVENTS,
      GATEWAY_CLIENT_CAPS.TOOL_EVENTS,
    ],
    minProtocol: PROTOCOL_VERSION,
    maxProtocol: PROTOCOL_VERSION,
    hostDeps,
    onHelloOk: (hello) => {
      connectionEpoch += 1;
      bootstrapSerial += 1;
      const epoch = connectionEpoch;
      const serial = bootstrapSerial;
      state.append(makeControlRecord("openclaw_gateway_connection_hello", {
        gatewayProtocol: hello.protocol,
        gatewayVersion: hello.server?.version ?? null,
        connectionIdDigest: hello.server?.connId ? digestIdentity(hello.server.connId) : null,
        requestedScopes: ["operator.read"],
        advertisedCapabilities: [
          GATEWAY_CLIENT_CAPS.SESSION_SCOPED_EVENTS,
          GATEWAY_CLIENT_CAPS.TOOL_EVENTS,
        ],
        rawHelloPersisted: false,
        auditReconciliationRequired: true,
      }, epoch));
      void subscribeForConnection(epoch, serial);
    },
    onEvent: (frame) => {
      try {
        const run = extractRunSequence(frame);
        if (run) {
          const previous = runSequences.get(run.runId);
          if (previous !== undefined && run.seq <= previous) {
            return;
          }
          if (previous !== undefined && run.seq > previous + 1) {
            state.append(makeControlRecord("openclaw_gateway_run_sequence_gap", {
              runId: run.runId,
              expectedRunSequence: previous + 1,
              receivedRunSequence: run.seq,
              auditReconciliationRequired: true,
            }, connectionEpoch));
          }
          runSequences.set(run.runId, run.seq);
        }
        const projected = projectEventFrame(frame, connectionEpoch);
        if (projected) {
          state.append(projected);
        }
      } catch (error) {
        state.append(makeControlRecord("openclaw_gateway_event_projection_error", {
          ...safeErrorDescriptor(error),
          eventName: frame && typeof frame.event === "string" ? frame.event : null,
          rawEventPersisted: false,
          auditReconciliationRequired: true,
        }, connectionEpoch));
      }
    },
    onGap: ({ expected, received }) => {
      state.append(makeControlRecord("openclaw_gateway_connection_sequence_gap", {
        expectedOuterSequence: expected,
        receivedOuterSequence: received,
        auditReconciliationRequired: true,
      }, connectionEpoch));
    },
    onConnectError: (error) => {
      state.append(makeControlRecord("openclaw_gateway_connect_error", {
        ...safeErrorDescriptor(error),
        auditReconciliationRequired: true,
      }, connectionEpoch));
    },
    onReconnectPaused: (info) => {
      state.append(makeControlRecord("openclaw_gateway_reconnect_paused", {
        closeCode: info.code,
        detailCode: info.detailCode ?? null,
        reasonDigest: digest(info.reason ?? ""),
        auditReconciliationRequired: true,
      }, connectionEpoch));
    },
    onClose: (code, reason, info) => {
      state.append(makeControlRecord("openclaw_gateway_connection_closed", {
        closeCode: code,
        closeReasonDigest: digest(reason ?? ""),
        phase: info?.phase ?? null,
        socketOpened: info?.socketOpened ?? null,
        transportValidated: info?.transportValidated ?? null,
        auditReconciliationRequired: true,
      }, connectionEpoch));
    },
  });

  state.append(makeControlRecord("openclaw_gateway_event_subscriber_started", {
    gatewayOriginDigest: digestIdentity(new URL(options.gatewayUrl).origin),
    targetedSessionCount: options.sessionKeys.length,
    bootstrapTokenSuppliedByEnvironment: Boolean(process.env.OPENCLAW_GATEWAY_BOOTSTRAP_TOKEN),
    passwordSuppliedByEnvironment: Boolean(process.env.OPENCLAW_GATEWAY_PASSWORD),
    credentialsPersistedInHintLedger: false,
    auditReconciliationRequired: true,
  }, connectionEpoch));

  client.start();

  await new Promise((resolve) => {
    const stop = () => {
      if (stopped) return;
      stopped = true;
      resolve();
    };
    process.once("SIGINT", stop);
    process.once("SIGTERM", stop);
  });

  try {
    await client.stopAndWait({ timeoutMs: 5000 });
  } finally {
    state.append(makeControlRecord("openclaw_gateway_event_subscriber_stopped", {
      auditReconciliationRequired: true,
    }, connectionEpoch));
  }
}

main().catch((error) => {
  console.error(`KuuOS OpenClaw event subscriber failed: ${error instanceof Error ? error.message : String(error)}`);
  process.exitCode = 2;
});
