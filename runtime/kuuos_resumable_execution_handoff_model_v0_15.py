from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_resumable_execution_handoff_types_v0_15 import (
    DETERMINISTIC_BUG_KINDS,
    TRANSIENT_ERROR_KINDS,
    USER_GUIDANCE_STATES,
)


def number(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float(default)


def integer(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return int(default)


def boolean(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "yes", "1", "on"}:
            return True
        if lowered in {"false", "no", "0", "off"}:
            return False
    return bool(value)


def bounded_progress(completed: Any, total: Any) -> float:
    done = max(0.0, number(completed, 0.0))
    whole = max(0.0, number(total, 0.0))
    if whole <= 0.0:
        return 0.0
    return round(max(0.0, min(1.0, done / whole)), 6)


def retry_delay_ms(retry_count: Any, base_ms: Any, maximum_ms: Any) -> int:
    count = max(0, min(30, integer(retry_count, 0)))
    base = max(0, integer(base_ms, 1000))
    maximum = max(base, integer(maximum_ms, 60000))
    return min(maximum, base * (2**count))


def _background_enabled(observation: Mapping[str, Any], plan: Mapping[str, Any]) -> bool:
    return (
        boolean(observation.get("background_capable"), False)
        and boolean(plan.get("background_handoff_enabled"), True)
    )


def _background_requested(
    observation: Mapping[str, Any],
    plan: Mapping[str, Any],
    auto_key: str,
) -> bool:
    return boolean(observation.get("background_requested"), False) or boolean(
        plan.get(auto_key), True
    )


def _result(
    *,
    state: str,
    reason_code: str,
    reason_summary: str,
    resume_condition: str,
    retry_after_ms: int = 0,
    background_disposition: str = "not_queued",
) -> dict[str, Any]:
    return {
        "execution_state": state,
        "reason_code": reason_code,
        "reason_summary": reason_summary,
        "resume_condition": resume_condition,
        "retry_after_ms": max(0, int(retry_after_ms)),
        "background_disposition": background_disposition,
        "foreground_prompt_released": state != "running",
        "resumable": state not in {"completed", "cancelled"},
        "requires_user_guidance": state in USER_GUIDANCE_STATES,
    }


def classify_execution(
    observation: Mapping[str, Any],
    plan: Mapping[str, Any],
) -> dict[str, Any]:
    if boolean(observation.get("completed"), False):
        return _result(
            state="completed",
            reason_code="work_completed",
            reason_summary="The requested work completed and no continuation is required.",
            resume_condition="none",
            background_disposition="not_applicable",
        )

    if boolean(observation.get("cancelled"), False):
        return _result(
            state="cancelled",
            reason_code="cancelled_by_user",
            reason_summary="Execution was cancelled by an explicit user or authority action.",
            resume_condition="new_attempt_required",
            background_disposition="not_applicable",
        )

    if boolean(observation.get("user_input_required"), False):
        return _result(
            state="needs_user_input",
            reason_code="user_input_required",
            reason_summary=str(
                observation.get(
                    "blocker_summary",
                    "Execution requires additional user input before it can continue.",
                )
            ),
            resume_condition="user_input_provided",
        )

    error_kind = str(observation.get("error_kind", "")).strip()
    if error_kind in DETERMINISTIC_BUG_KINDS:
        return _result(
            state="blocked_bug",
            reason_code=(
                "invariant_violation"
                if error_kind == "invariant_violation"
                else "deterministic_bug"
            ),
            reason_summary=str(
                observation.get(
                    "blocker_summary",
                    "A reproducible implementation or validation defect prevents progress.",
                )
            ),
            resume_condition="input_or_implementation_changed",
            background_disposition="not_queued_deterministic_failure",
        )

    if error_kind == "permission_denied":
        return _result(
            state="permission_blocked",
            reason_code="permission_denied",
            reason_summary=str(
                observation.get(
                    "blocker_summary",
                    "The required operation is not permitted by the current authority boundary.",
                )
            ),
            resume_condition="permission_granted_or_scope_changed",
        )

    retry_count = max(0, integer(observation.get("retry_count"), 0))
    max_retries = max(0, integer(plan.get("max_retries"), 3))
    if error_kind in TRANSIENT_ERROR_KINDS:
        reason_code = {
            "rate_limit": "rate_limited",
            "timeout": "timeout",
            "transient_error": "transient_error",
        }[error_kind]
        if retry_count >= max_retries:
            return _result(
                state="retry_exhausted",
                reason_code="retry_limit_reached",
                reason_summary=str(
                    observation.get(
                        "blocker_summary",
                        "The bounded retry limit was reached without successful continuation.",
                    )
                ),
                resume_condition="user_changes_retry_policy_or_scope",
            )
        delay = retry_delay_ms(
            retry_count,
            plan.get("retry_backoff_base_ms", 1000),
            plan.get("max_retry_backoff_ms", 60000),
        )
        if _background_enabled(observation, plan) and _background_requested(
            observation, plan, "auto_background_on_transient_error"
        ):
            return _result(
                state="background_queued",
                reason_code=reason_code,
                reason_summary=str(
                    observation.get(
                        "blocker_summary",
                        "A transient failure requires bounded retry backoff.",
                    )
                ),
                resume_condition="retry_delay_elapsed",
                retry_after_ms=delay,
                background_disposition="queued",
            )
        return _result(
            state="retry_backoff",
            reason_code=reason_code,
            reason_summary=str(
                observation.get(
                    "blocker_summary",
                    "A transient failure requires bounded retry backoff.",
                )
            ),
            resume_condition="retry_delay_elapsed",
            retry_after_ms=delay,
            background_disposition=(
                "unsupported"
                if not _background_enabled(observation, plan)
                else "not_requested"
            ),
        )

    remaining_cost = max(0.0, number(observation.get("remaining_cost_units"), 0.0))
    estimated_next = max(0.0, number(observation.get("estimated_next_cost_units"), 0.0))
    reserve = max(0.0, number(plan.get("cost_reserve_units"), 0.0))
    if estimated_next > 0.0 and remaining_cost < estimated_next + reserve:
        if _background_enabled(observation, plan) and _background_requested(
            observation, plan, "auto_background_on_budget_pause"
        ):
            return _result(
                state="background_queued",
                reason_code="cost_budget_exhausted",
                reason_summary="The remaining cost budget is insufficient for the next bounded operation.",
                resume_condition="budget_replenished",
                background_disposition="queued_waiting_budget",
            )
        return _result(
            state="budget_paused",
            reason_code="cost_budget_exhausted",
            reason_summary="The remaining cost budget is insufficient for the next bounded operation.",
            resume_condition="budget_replenished",
            background_disposition=(
                "unsupported"
                if not _background_enabled(observation, plan)
                else "not_requested"
            ),
        )

    wait_elapsed = max(0, integer(observation.get("wait_elapsed_ms"), 0))
    wait_threshold = max(0, integer(plan.get("foreground_wait_threshold_ms"), 10000))
    external_ready = boolean(observation.get("external_dependency_ready"), True)
    if not external_ready and wait_elapsed >= wait_threshold:
        retry_after = max(0, integer(plan.get("external_recheck_after_ms"), 5000))
        if _background_enabled(observation, plan) and _background_requested(
            observation, plan, "auto_background_on_external_wait"
        ):
            return _result(
                state="background_queued",
                reason_code="external_latency",
                reason_summary=str(
                    observation.get(
                        "blocker_summary",
                        "An external dependency exceeded the foreground waiting threshold.",
                    )
                ),
                resume_condition="external_dependency_ready",
                retry_after_ms=retry_after,
                background_disposition="queued",
            )
        return _result(
            state="waiting_external",
            reason_code="external_latency",
            reason_summary=str(
                observation.get(
                    "blocker_summary",
                    "An external dependency exceeded the foreground waiting threshold.",
                )
            ),
            resume_condition="external_dependency_ready",
            retry_after_ms=retry_after,
            background_disposition=(
                "unsupported"
                if not _background_enabled(observation, plan)
                else "not_requested"
            ),
        )

    return _result(
        state="running",
        reason_code="execution_active",
        reason_summary="Execution may continue in the foreground.",
        resume_condition="continue_now",
        background_disposition="not_needed",
    )
