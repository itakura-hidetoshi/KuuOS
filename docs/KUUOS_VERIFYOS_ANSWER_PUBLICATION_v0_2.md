# VerifyOS controlled answer publication v0.2

Append-only continuation of `kuuos_verifyos_execution_answer_binding_v0_1.py`. The trusted host runs the pinned gates, admits only its own observed execution bundle, binds admission to the exact request, question digest, turn, challenge and private verification audience, and then uses a separate egress verifier. A language model is not the publisher.

## Host protocol

The host obtains the expected hashes and tip independently of model output and prepares a private immutable snapshot as in v0.1. It creates a fresh request challenge and a context containing `turn_id`, `question_sha256`, `challenge`, `request_sha256` and `audience` (`private_verification_channel`). The first four fields are lowercase 64-digit hex strings; the challenge and request digest must match the request. The 32-byte HMAC key is generated and stored by the trusted host, never committed or exposed to the model. All JSON inputs are canonical UTF-8 with a trailing newline.

```
python -B -m runtime.kuuos_verifyos_answer_publication_v0_2 issue --request request.json --context context.json --key-file HOST_KEY --evidence-dir NEW_PRIVATE_DIR --snapshot SNAPSHOT
python -B -m runtime.kuuos_verifyos_answer_publication_v0_2 publish --request request.json --context context.json --key-file HOST_KEY --evidence-dir NEW_PRIVATE_DIR > packet.json
python -B -m runtime.kuuos_verifyos_answer_publication_v0_2 display --request request.json --context context.json --key-file HOST_KEY --evidence-dir NEW_PRIVATE_DIR --packet packet.json
```

The issue path executes both gates through v0.1, preserves the local bundle in an exclusively created file, and only issues a domain-separated HMAC admission for a successful verified bundle. It accepts no incoming model receipt for signing. Publication verifies the admission, exact request/context/bundle binding, and v0.1 correspondence again. The publication packet contains a fixed Japanese statement and explicit non-authority flags, not arbitrary model prose. Display recomputes the entire packet and emits only the fixed statement or HOLD. Editing or appending text to the packet fails byte equality. Missing evidence, wrong key, altered bundle, wrong question, turn, challenge or audience, and failed gates cannot publish success. Same-turn replay is idempotent, not an at-most-once delivery guarantee.

## Trust and limits

The key is shared within the trusted issuer/publisher/consumer domain, not a public signature or independent runner attestation. Host isolation, pinned runtime/interpreter, actual independently sourced anchors, immutable input snapshots, key isolation, and exclusive control of the verification-result output channel are deployment prerequisites. Model/tool access to the key or replacement of the trusted context invalidates the security argument. This is a local egress API/CLI, not a modification of ChatGPT, not a general natural-language truth checker and not a proof or action authority. No fresh external anchor observation or new-context validity is certified. Fresh current-state claims require separate before/after observation; global replay protection requires a trusted delivery store. Private bundles, keys, context and live ledger data are never committed. Regression fixtures exercise actual subprocesses with synthetic gate scripts; they do not certify the real ledger or Lean. No prior receipt or code is modified.
