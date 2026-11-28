# VerifyOS claim-evidence binding v0.3

Append-only continuation of v0.1 execution receipt binding and v0.2 controlled answer publication. Instead of certifying free-form prose, project a finite, typed vocabulary of claims from an admitted execution receipt. Each observed claim carries the exact bundle and receipt digest, process index, gate identifier, source field path, process digest, and stdout digest. No model-supplied claim value is used.

## Host contract

The trusted host obtains the private snapshot and anchors independently, issues and publishes through v0.2, and freezes an ordered claim plan, for example `{"claim_ids":["rule_count","scope_held_count","current_tip"]}`. This plan is a separate trusted input to both publication and display; a packet's self-declared list is not trusted. The host retains the original plan and exact request/context. Each field projection is selected by a fixed registry, not a user-provided path. Unknown or duplicate IDs, altered plan or packet, invalid prior admission, or context mismatch fail closed. Missing, ill-typed or unsupported claim values are explicitly HOLD, never guessed. Partial output keeps all requested IDs in order and does not grant a global pass.

```sh
python -B -m runtime.kuuos_verifyos_claim_evidence_binding_v0_3 publish --request request.json --context context.json --key-file HOST_KEY --evidence-dir PRIVATE_EVIDENCE --prior-packet prior.json --plan plan.json > claims.json
python -B -m runtime.kuuos_verifyos_claim_evidence_binding_v0_3 display --request request.json --context context.json --key-file HOST_KEY --evidence-dir PRIVATE_EVIDENCE --prior-packet prior.json --plan plan.json --packet claims.json
```

The output is the canonical authenticated packet, or a fixed HOLD packet. Display recomputes the entire packet from the host inputs. Exit 0 means ALL_OBSERVED for that plan alone; PARTIAL and HOLD return 2. A valid PARTIAL packet still contains the supported observations and the unresolved claims. It is not a failed mathematical proposition. Raw evidence and host keys remain private.

## Certified scope and remaining boundaries

13 registered projections: two gate statuses, two exit codes, snapshot sequence and tip, rule/withdrawal/obstruction/research-certificate counts, and three review counts. Five explicitly unsupported claims: fresh current tip, external truth, Lean proof, new-context validity and action permission. Even a successful count is an observed value in a locally admitted receipt, not a proof of general correctness. The trusted host must keep the plan, request, key, pinned code, execution environment, and verification-result channel isolated from generated prose. No guarantee of question-to-plan completeness, public signature, freshness, global replay protection, actual external tool execution, or integration with ChatGPT itself is supplied. The HMAC is a shared-host authentication mechanism, not a third-party attestation. The tests use real subprocesses with synthetic pinned gates; actual private-ledger replay is separate and is not uploaded. No Lean source or preceding runtime is changed.
