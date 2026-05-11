.PHONY: ai-yogacara-checks ai-yogacara-build-bundle ai-yogacara-validate-bundle mandala-checks bodhisattva-checks paramita-router-checks dukkha-checks core-governance-checks

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

core-governance-checks: ai-yogacara-checks mandala-checks bodhisattva-checks paramita-router-checks dukkha-checks
