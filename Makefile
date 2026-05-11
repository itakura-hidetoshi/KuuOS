.PHONY: ai-yogacara-checks ai-yogacara-build-bundle ai-yogacara-validate-bundle

ai-yogacara-checks:
	python3 scripts/run_ai_yogacara_full_checks_v0_1.py

ai-yogacara-build-bundle:
	python3 scripts/build_ai_yogacara_release_bundle_manifest_v0_1.py

ai-yogacara-validate-bundle:
	python3 scripts/validate_ai_yogacara_release_bundle_manifest_v0_1.py
