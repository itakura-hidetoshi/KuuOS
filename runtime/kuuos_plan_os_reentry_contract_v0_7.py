from __future__ import annotations

from runtime.kuuos_plan_os_reentry_types_v0_7 import BOUNDARY, NON_AUTHORITY, VERSION

CONTRACT = {
    "version": VERSION,
    "boundary": dict(BOUNDARY),
    "non_authority": dict(NON_AUTHORITY),
    "resume_source_status": "HOLD",
    "handover_source_status": "HANDOVER",
    "forbidden_source_status": "STOPPED",
    "target_status": "ACTIVE",
}
