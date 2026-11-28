# VerifyOS execution-to-answer binding v0.1

Append-only candidate. Extends the separation already present in `runtime/kuuos_verifyos_independent_evidence_verification_v0_1.py` and `runtime/kuuos_codeai_external_result_process_evidence_ingestion_v0_1.py`; does not replace PlanOS's execution authorization receipt. The D-group obstruction was acquisition reported as execution despite absent process evidence. Missing evidence is HOLD, not a refutation or historical execution failure.

## Trust boundary and operation

A trusted host obtains the expected tip, registry digest and both gate digests from its separately stored anchor; materializes the exact base/ledger/gates file sets into a private isolated snapshot; assigns a fresh 256-bit challenge per request. The model must not provide these trusted values. `request.json` has `challenge`, `seq`, `tip`, `expected_hashes` (keys `base/kuuos_continuation_20261128_v15.json`, `gates/kuuos_inheritance_gate_v16.py`, `gates/kuuos_scope_guard_v16_1.py`).

```sh
python -B -m runtime.kuuos_verifyos_execution_answer_binding_v0_1 run --request request.json --snapshot snapshot --bundle receipt.json
python -B -m runtime.kuuos_verifyos_execution_answer_binding_v0_1 verify --request request.json --bundle receipt.json --trusted-bundle-sha256 "$HOST_OBSERVED_SHA256"
```

The runner starts both pinned gate subprocesses with fixed argument construction; captures exit status, stdout/stderr bytes (strict UTF-8), stream hashes, timestamps, pre/post inventory and request binding. It writes a new bundle only. The renderer derives a closed JSON answer from the receipt; the verifier checks the externally admitted bundle digest, exact request/challenge, and byte-identical canonical answer. The host must publish **only the verified answer** in the verification-result channel. Missing/changed evidence produces HOLD; a model-authored PASS is never a receipt. The host must check its actual process/tool output and admit the digest from that channel, not hash a model-provided bundle to obtain an anchor. Fresh current-state claims additionally require separately observing the saved anchor before and after execution, including its revision; this module never claims freshness. No private logs, ledger, user identifiers or live anchors belong in the public repository.

Only `PASS_LOCAL_EXECUTION_STRUCTURE_ONLY` is possible on success. It conveys no external authenticity, new-context validity, Lean proof or action authority. Structural acceptance assumes a trusted host/interpreter, pinned trusted gate code and isolated immutable snapshot; pre/post hashes alone do not defend against transient concurrent mutation or a compromised host. The verifier cannot authenticate a self-issued digest or compel ordinary ChatGPT to use the publication boundary. No arbitrary natural-language truth checking, independent mathematical proof, or global product integration is claimed. Synthetic regression fixtures exercise real subprocesses, but do not certify actual inheritance records. Actual daily workflow and separate host integration remain open.
