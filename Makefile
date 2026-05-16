.PHONY: ai-provider-boundary-checks ai-yogacara-checks ai-yogacara-build-bundle ai-yogacara-validate-bundle mandala-checks bodhisattva-checks paramita-router-checks dukkha-checks dukkha-qi-checks formal-invariant-checks super-relativity-checks invariant-matrix-checks invariant-gate-checks invariant-pipeline-checks invariant-pipeline-build-bundle invariant-pipeline-validate-bundle invariant-pipeline-attest invariant-pipeline-release-closure invariant-pipeline-finality gpt-github-integration-checks memoryos-github-external-memory-checks emptiness-two-truths-runtime-audit-checks core-governance-checks all-governance-checks

ai-provider-boundary-checks:
	python3 scripts/validate_ai_provider_boundary_runtime_v0_1.py
	python3 scripts/validate_ai_provider_boundary_audit_event_v0_1.py

ai-yogacara-checks:
	python3 scripts/run_ai_yogacara_full_checks_v0_1.py

ai-yogacara-build-bundle:
	python3 scripts/build_ai_yogacara_release_bundle_manifest_v0_1.py

ai-yogacara-validate-bundle:
	python3 scripts/validate_ai_yogacara_release_bundle_manifest_v0_1.py

mandala-checks:
	python3 scripts/validate_mandala_multi_world_v0_1.py

bodhisattva-checks:
	python3 scripts/validate_bodhisattva_ten_paramita_v0_1.py

paramita-router-checks:
	python3 scripts/validate_paramita_repair_router_v0_1.py
	python3 scripts/validate_paramita_repair_router_fixtures_v0_1.py

dukkha-checks:
	python3 scripts/validate_dukkha_mathematical_model_v0_1.py
	python3 scripts/validate_dukkha_model_fixtures_v0_1.py

dukkha-qi-checks:
	python3 scripts/validate_dukkha_as_qi_mode_v0_1.py

formal-invariant-checks:
	python3 scripts/validate_formal_invariant_spine_v0_1.py

super-relativity-checks:
	python3 scripts/validate_super_relativity_invariant_bridge_v0_1.py

invariant-matrix-checks:
	python3 scripts/validate_invariant_preservation_matrix_v0_1.py
	python3 scripts/validate_invariant_preservation_matrix_fixtures_v0_1.py

invariant-gate-checks:
	python3 scripts/validate_invariant_gate_fixtures_v0_1.py

invariant-pipeline-build-bundle:
	python3 scripts/build_invariant_pipeline_release_bundle_manifest_v0_1.py

invariant-pipeline-validate-bundle:
	python3 scripts/validate_invariant_pipeline_release_bundle_manifest_v0_1.py
	python3 scripts/validate_invariant_pipeline_bundle_closure_inclusion_v0_1.py

invariant-pipeline-attest:
	python3 scripts/validate_invariant_pipeline_release_attestation_v0_1.py

invariant-pipeline-release-closure:
	python3 scripts/validate_invariant_pipeline_release_closure_packet_v0_1.py
	python3 scripts/validate_invariant_pipeline_bundle_closure_inclusion_v0_1.py

invariant-pipeline-finality:
	python3 scripts/check_invariant_pipeline_finality_packet_v0_1.py

invariant-pipeline-checks:
	python3 scripts/validate_invariant_governance_pipeline_v0_1.py
	python3 scripts/validate_invariant_governance_pipeline_fixtures_v0_1.py
	python3 scripts/validate_invariant_pipeline_audit_event_v0_1.py
	python3 scripts/validate_invariant_pipeline_audit_hash_chain_v0_1.py
	python3 scripts/validate_invariant_pipeline_audit_worm_export_receipt_v0_1.py
	python3 scripts/validate_invariant_pipeline_release_bundle_manifest_v0_1.py
	python3 scripts/validate_invariant_pipeline_bundle_closure_inclusion_v0_1.py
	python3 scripts/validate_invariant_pipeline_release_attestation_v0_1.py
	python3 scripts/validate_invariant_pipeline_release_closure_packet_v0_1.py
	python3 scripts/check_invariant_pipeline_finality_packet_v0_1.py

gpt-github-integration-checks:
	python3 scripts/validate_gpt_github_integration_v0_1.py

memoryos-github-external-memory-checks:
	python3 scripts/validate_memoryos_github_external_memory_v0_1.py

emptiness-two-truths-runtime-audit-checks:
	python3 scripts/export_emptiness_do_two_truths_runtime_audit_v0_1.py
	python3 scripts/build_emptiness_do_two_truths_runtime_audit_chain_v0_1.py
	python3 scripts/check_emptiness_do_two_truths_runtime_audit_chain_v0_1.py
	python3 scripts/run_emptiness_do_two_truths_runtime_checks_v0_1.py

core-governance-checks:
	python3 scripts/run_core_governance_full_checks_v0_1.py

all-governance-checks:
	python3 scripts/run_all_governance_full_checks_v0_1.py