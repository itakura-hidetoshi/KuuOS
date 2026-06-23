# KuString Runtime Chain Index v0.2

This index records the KuString-MGAP4D-Emptiness runtime implementation chain and its CI-green finality evidence.

## Chain order

1. Runtime evaluator
   - `examples/kustring_runtime_v0_2.py`

2. Runtime unit tests
   - `tests/test_kustring_runtime_v0_2.py`

3. Packet evaluator
   - `scripts/eval_kustring_runtime_packets_v0_2.py`
   - `specs/kustring_runtime_packets_v0_2.json`

4. Runtime audit event surface
   - `scripts/export_kustring_runtime_audit_v0_2.py`
   - `scripts/check_kustring_runtime_audit_v0_2.py`
   - `specs/kustring_runtime_audit_events_v0_2.generated.jsonl`

5. Runtime audit hash-chain surface
   - `scripts/build_kustring_runtime_audit_chain_v0_2.py`
   - `scripts/check_kustring_runtime_audit_chain_v0_2.py`
   - `specs/kustring_runtime_audit_chain_v0_2.generated.jsonl`

6. WORM receipt surface
   - `scripts/export_kustring_runtime_worm_receipt_v0_2.py`
   - `scripts/check_kustring_runtime_worm_receipt_v0_2.py`
   - `specs/kustring_runtime_worm_receipt_v0_2.generated.json`

7. Runtime bundle and attestation
   - `scripts/build_kustring_runtime_bundle_v0_2.py`
   - `scripts/check_kustring_runtime_bundle_v0_2.py`
   - `specs/kustring_runtime_bundle_v0_2.generated.json`
   - `scripts/build_kustring_runtime_attestation_v0_2.py`
   - `scripts/check_kustring_runtime_attestation_v0_2.py`
   - `specs/kustring_runtime_attestation_v0_2.generated.json`

8. Closure packet
   - `docs/KUSTRING_RUNTIME_CLOSURE_PACKET_v0_2.md`
   - `scripts/check_kustring_runtime_closure_v0_2.py`

9. Finality packet and report
   - `docs/KUSTRING_RUNTIME_FINALITY_PACKET_v0_2.md`
   - `scripts/check_kustring_runtime_finality_v0_2.py`
   - `scripts/build_kustring_runtime_finality_report_v0_2.py`
   - `scripts/check_kustring_runtime_finality_report_v0_2.py`

10. CI green ledger and finality report artifact
    - `docs/kustring_runtime_finality_ci_ledger_v0_2.md`
    - Workflow run ID: `25960729451`
    - Workflow job ID: `76315481134`
    - Head SHA: `8eae6d696b6128cfecb71430b19123ca6ed43003`
    - Artifact ID: `7033005445`
    - Artifact name: `kustring-runtime-finality-report-v0-2`
    - Artifact digest: `sha256:6f6bb5e4f204cbd63334625cc2295b54b33d10eddf610ce666547047fd0985ad`

## Boundary

This chain index records implementation-level runtime finality only.

It does not grant:

- proof authority
- truth authority
- clinical authority
- execution authority
- governance-bypass authority

CI success confirms configured CI passage for the referenced run. It does not convert runtime implementation into theorem truth or execution license.

## Append-only rule

Future changes must be added as same-root append-only entries or as a new versioned chain index. Destructive replacement of the CI-green evidence or authority boundary is forbidden.

Version: v0.2
Date: 2026-06-24
Author: Hidetoshi Itakura / 板倉英俊
