# v1.103 exact-source four-gate Lean certification

The ordered and source-bound process is:
1. CodeAI generates six candidate proof patches on parent #3522 exact original source HEAD 2ee48e0e55509ec30f955dae2274a2e5b5dd4aa1, tree 34026cc3341b57711c301ef775c46f47afd3119c. This stage is proposal-only, not mathematical proof.
2. Pinned Lean v4.30.0-rc2 and mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6 directly checks ALL six candidates. Run #43683314843 reported two with exit=0, .olean present and error_count=0; four directly failed. Preserve all failures.
3. Only candidates with direct-Lean SUCCESS enter real Lean MCP diagnosis. Selected round2-congr-rw had real lean_diagnostic_messages success/errors=0, lean_goal and lean_multi_attempt receipts at lines 183 and 198, then another direct Lean compile exit=0, source restored. Its byte-exact Git blob is ff2e6a09e2c064a23207ee1323bc14182c86d7cd. This remains local admission, NOT independent CI.
4. Only after exact GitHub MCP source promotion does a separate independent Strict Lean CI build the complete pinned dependency closure and audit all 15 v1.103 declarations with Lean #check / #print axioms. The source and candidate blobs must agree. The independent CI is certified only if its actual job and Lean steps are completed/SUCCESS, with no sorryAx and no nonstandard axioms.

Executable control: scripts/kuuos_v1103_four_stage_gate_v1.py verifies the prior authenticated GitHub Actions CodeAI producer run, archived candidate and MCP receipts, original source/tree, selected green direct Lean candidate, real Lean MCP status and exact promoted blob. It intentionally reports only STAGES_1_2_3_VERIFIED_READY_FOR_INDEPENDENT_CI, never full certification.

The workflow .github/workflows/kuuos-v1103-four-stage-gated-certification-v1.yml uses needs: precommit-codeai-direct-lean-mcp-admission so that independent Strict Lean CANNOT start until stages 1-3 have been checked. The workflow itself has contents read-only and no Git writes. No test-merge tree identity is implied.

Preserve canonical main, draft parent #3522, validation child #3530, protected #1558 draft/open/unmerged, all imported signatures, no theorem weakening, no new sorry or axioms. append-only/tighten-only/overwrite-forbidden/same-root. A locally preferred candidate is not enough for independent certification or merge authority.
