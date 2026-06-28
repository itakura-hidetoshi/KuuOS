#!/usr/bin/env python3
from __future__ import annotations

from runtime.kuuos_memory_family_evaluation_v0_73 import SELECTED
from runtime.kuuos_memory_selection_v0_73 import (
    MemorySelectionRecord,
    selection_record_digest,
)


def selection_review_issues(selection: MemorySelectionRecord) -> tuple[str, ...]:
    issues: list[str] = []
    if selection.record_digest != selection_record_digest(selection):
        issues.append("memory_selection_record_digest_mismatch")
    if selection.status != SELECTED:
        issues.append("memory_selection_status_not_selected")
    if selection.accepted_count <= 0:
        issues.append("memory_selection_has_no_accepted_member")
    bindings = (
        selection.selected_member_digest,
        selection.selected_deformation_digest,
        selection.selected_kernel_digest,
        selection.selected_connection_digest,
    )
    if any(not value for value in bindings):
        issues.append("memory_selection_binding_missing")
    if not selection.source_history_unchanged:
        issues.append("memory_selection_source_history_not_preserved")
    if not selection.source_kernel_unchanged:
        issues.append("memory_selection_source_kernel_not_preserved")
    if not selection.candidate_only:
        issues.append("memory_selection_not_candidate_only")
    if selection.writes_enabled:
        issues.append("memory_selection_writes_enabled")
    if selection.live_application_enabled:
        issues.append("memory_selection_live_application_enabled")
    if selection.permission_expansion_enabled:
        issues.append("memory_selection_permission_expansion_enabled")
    if selection.issues:
        issues.append("memory_selection_contains_issues")
    return tuple(dict.fromkeys(issues))
