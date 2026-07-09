#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.check_actos_bounded_adapter_invocation_v0_4 import main as check_actos_v04
from scripts.check_actos_activation_authorization_intake_v0_3 import main as check_actos_v03
from scripts.check_planos_literature_grounded_selective_foresight_gate_v0_40 import main as check_planos_v040
from scripts.check_planos_actos_invocation_receipt_v0_39 import main as check_planos_v039
from scripts.check_planos_activation_authorization_grant_v0_38 import main as check_planos_v038
from scripts.check_planos_activation_authorization_request_v0_37 import main as check_planos_v037
from scripts.check_planos_materialization_execution_receipt_v0_36 import main as check_planos_v036
from scripts.check_planos_materialization_authorization_grant_v0_35 import main as check_planos_v035
from scripts.check_planos_materialization_authorization_request_receipt_v0_34 import main as check_planos_v034
from scripts.check_planos_materialization_authorization_request_v0_33 import main as check_planos_v033
from scripts.check_planos_selected_candidate_materialization_preflight_v0_32 import main as check_planos_v032
from scripts.check_planos_selected_candidate_synthesis_receipt_v0_31 import main as check_planos_v031
from scripts.check_planos_selected_candidate_synthesis_request_v0_30 import main as check_planos_v030
from scripts.check_planos_decisionos_selection_receipt_intake_v0_29 import main as check_planos_v029
from scripts.check_planos_decisionos_selection_request_v0_28 import main as check_planos_v028
from scripts.check_planos_decision_review_intake_v0_27 import main as check_planos_v027
from scripts.check_planos_weighted_decision_evidence_handoff_v0_26 import main as check_planos_v026
from scripts.check_planos_path_integral_candidate_weighting_v0_25 import main as check_planos_v025
from scripts.check_planos_qi_blocker_foresight_plan_gate_v0_24 import main as check_planos_v024
from scripts.check_planos_activation_admission_actos_handoff_v0_23 import main as check_planos_v023
from scripts.check_planos_compiler_materialization_v0_22 import main as check_planos_v022
from scripts.check_planos_selected_candidate_next_cycle_synthesis_v0_21 import main as check_planos_v021
from scripts.check_decisionos_admissible_candidate_selection_v0_4 import main as check_decisionos_v04
from scripts.check_planos_hysteresis_constraint_decision_handoff_v0_20 import main as check_planos_v020
from scripts.check_planos_history_qi_candidate_generation_v0_19 import main as check_planos_v019
from scripts.check_planos_vacuum_expectation_learning_replan_intake_v0_18 import main as check_planos_v018
from scripts.check_learnos_vacuum_expectation_verification_future_only_delta_v0_3 import main as check_learnos_v03
from scripts.check_verifyos_vacuum_expectation_commit_verification_receipt_v0_3 import main as check_verifyos_v03
from scripts.check_observeos_vacuum_expectation_intake_commit_receipt_v0_3 import main as check_observeos_v03
from scripts.check_world_vacuum_expectation_observeos_evidence_intake_v0_51 import main as check_v051
from scripts.run_kuuos_runtime_full_check_v0_50 import main as run_v050_full_check


def main() -> int:
    checks = (
        check_actos_v04,
        check_actos_v03,
        check_planos_v040,
        check_planos_v039,
        check_planos_v038,
        check_planos_v037,
        check_planos_v036,
        check_planos_v035,
        check_planos_v034,
        check_planos_v033,
        check_planos_v032,
        check_planos_v031,
        check_planos_v030,
        check_planos_v029,
        check_planos_v028,
        check_planos_v027,
        check_planos_v026,
        check_planos_v025,
        check_planos_v024,
        check_planos_v023,
        check_planos_v022,
        check_planos_v021,
        check_decisionos_v04,
        check_planos_v020,
        check_planos_v019,
        check_planos_v018,
        check_learnos_v03,
        check_verifyos_v03,
        check_observeos_v03,
        check_v051,
    )
    for check in checks:
        if check() != 0:
            return 1
    return run_v050_full_check()


if __name__ == "__main__":
    raise SystemExit(main())
