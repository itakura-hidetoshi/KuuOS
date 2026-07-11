#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Mapping

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
SOURCE_DIGEST_FIELD = "actos_dukkha_supported_bounded_plan_materialization_intake_receipt_digest"
RECEIPT_DIGEST_FIELD = "actos_dukkha_preserving_adapter_binding_authorization_intake_receipt_digest"

DISPOSITION_READY = "activation_authorization_ready"
DISPOSITION_WORLD_REFRESH = "world_refresh_required"
DISPOSITION_FRESHNESS_REFRESH = "freshness_refresh_required"
DISPOSITION_REGISTRY_REPAIR = "adapter_registry_repair_required"
DISPOSITION_LEASE_REFRESH = "lease_refresh_required"
DISPOSITION_REPLAY_REJECTED = "replay_conflict_rejected"
DISPOSITION_REVERIFY = "verifyos_step_reverification_required"

FORBIDDEN_EFFECTS = frozenset({
    "active_now", "candidate_substitution", "execution_permission",
    "external_side_effect", "persistent_world_mutation",
    "selection_authority_transfer", "tool_invocation",
    "unreviewed_scope_expansion",
})

CANDIDATE_FIELDS = {
    "materialization_candidate_id", "source_step_id", "sequence_index",
    "source_action_class", "materialization_class",
    "source_action_spec_digest", "precondition_digests",
    "expected_effect_digests", "effect_tags", "evidence_lineage_digests",
    "stop_condition_digests", "reversible", "irreversible",
    "checkpoint_step_id", "branch_ids", "candidate_state",
    "adapter_binding_digest", "tool_invocation_requested",
    "external_side_effect_requested", "execution_permission_requested",
    "active_now_requested", "materialization_payload_digest",
    "materialization_candidate_digest",
}
REGISTRY_FIELDS = {"registry_version", "issued_epoch", "entries", "registry_snapshot_digest"}
ENTRY_FIELDS = {
    "adapter_id", "adapter_class", "supported_materialization_classes",
    "capability_digest", "scope_policy_digest", "effect_ceiling_tags",
    "active", "revoked", "lease_id", "remaining_uses", "entry_digest",
}
BINDING_FIELDS = {
    "materialization_candidate_id", "adapter_id",
    "adapter_registry_entry_digest", "capability_digest", "scope_digest",
    "effect_ceiling_digest", "lease_id", "requested_effect_tags",
    "binding_state", "binding_digest",
}
CONTEXT_FIELDS = {
    "current_world_binding_digest", "current_world_model_state_digest",
    "current_world_model_revision", "current_world_lineage_digest",
    "source_observed_epoch", "current_epoch", "maximum_freshness_age",
    "completed_materialization_candidate_ids",
    "requested_frontier_candidate_id", "session_id", "intent_digest",
    "authorization_nonce_digest", "prior_session_ids",
    "prior_intent_digests", "prior_authorization_nonce_digests",
    "verifyos_step_reverification_digest", "freshness_observation_digest",
    "exact_act_cycle_digest", "authorization_context_digest",
}


@dataclass
class ActOSDukkhaPreservingAdapterAuthorizationResult:
    status: str
    blockers: list[str]
    receipt: dict | None


def canonical_digest(value: Any) -> str:
    return sha256(json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()


def compute_registry_snapshot_digest(snapshot: Mapping[str, Any]) -> str:
    value = dict(snapshot)
    value.pop("registry_snapshot_digest", None)
    return canonical_digest(value)


def compute_authorization_context_digest(context: Mapping[str, Any]) -> str:
    value = dict(context)
    value.pop("authorization_context_digest", None)
    return canonical_digest(value)


def compute_adapter_binding_authorization_bundle_digest(**fields: Any) -> str:
    return canonical_digest(fields)


def compute_materialization_payload_digest(candidate: Mapping[str, Any]) -> str:
    keys = (
        "source_step_id", "sequence_index", "source_action_class",
        "materialization_class", "source_action_spec_digest",
        "precondition_digests", "expected_effect_digests", "effect_tags",
        "evidence_lineage_digests", "stop_condition_digests", "reversible",
        "irreversible", "checkpoint_step_id", "branch_ids",
    )
    return canonical_digest({key: candidate.get(key) for key in keys})


def compute_binding_scope_digest(candidate: Mapping[str, Any]) -> str:
    keys = (
        "materialization_candidate_id", "materialization_class",
        "precondition_digests", "stop_condition_digests",
        "evidence_lineage_digests", "branch_ids",
    )
    return canonical_digest({key: candidate.get(key) for key in keys})


def compute_effect_ceiling_digest(
    candidate: Mapping[str, Any], entry: Mapping[str, Any]
) -> str:
    return canonical_digest({
        "requested_effect_tags": candidate.get("effect_tags"),
        "registry_effect_ceiling_tags": entry.get("effect_ceiling_tags"),
    })


def compute_exact_intent_digest(
    source: Mapping[str, Any], frontier: Mapping[str, Any]
) -> str:
    return canonical_digest({
        "selected_candidate_id": source.get("selected_candidate_id"),
        "selected_candidate_plan_intent_digest":
            source.get("selected_candidate_plan_intent_digest"),
        "materialization_candidate_id":
            frontier.get("materialization_candidate_id"),
        "source_action_spec_digest": frontier.get("source_action_spec_digest"),
    })


def compute_freshness_observation_digest(
    source: Mapping[str, Any], context: Mapping[str, Any]
) -> str:
    return canonical_digest({
        "source_receipt_digest": source.get(SOURCE_DIGEST_FIELD),
        "source_world_binding_digest": source.get("source_world_binding_digest"),
        "source_world_model_state_digest":
            source.get("source_world_model_state_digest"),
        "source_world_model_revision":
            source.get("source_world_model_revision"),
        "source_world_lineage_digest": source.get("source_world_lineage_digest"),
        "source_observed_epoch": context.get("source_observed_epoch"),
        "current_epoch": context.get("current_epoch"),
    })


def compute_exact_act_cycle_digest(
    source: Mapping[str, Any],
    context: Mapping[str, Any],
    frontier: Mapping[str, Any],
) -> str:
    return canonical_digest({
        "source_receipt_digest": source.get(SOURCE_DIGEST_FIELD),
        "frontier_candidate_id":
            frontier.get("materialization_candidate_id"),
        "source_world_model_revision":
            source.get("source_world_model_revision"),
        "current_world_model_revision":
            context.get("current_world_model_revision"),
        "session_id": context.get("session_id"),
        "intent_digest": context.get("intent_digest"),
        "authorization_nonce_digest":
            context.get("authorization_nonce_digest"),
    })


def _strings(value: Any, *, empty: bool = False) -> tuple[bool, list[str]]:
    if not isinstance(value, list) or (not empty and not value):
        return False, []
    if any(not isinstance(item, str) or not item for item in value):
        return False, []
    if value != sorted(value) or len(value) != len(set(value)):
        return False, []
    return True, list(value)


def _bound_digest(
    obj: dict, field: str, expected: str, prefix: str, blockers: list[str]
) -> str:
    digest = obj.get(field)
    if not isinstance(digest, str) or not digest:
        blockers.append(f"{prefix}_digest_missing")
        return ""
    unsigned = dict(obj)
    unsigned.pop(field, None)
    if digest != canonical_digest(unsigned):
        blockers.append(f"{prefix}_digest_mismatch")
    if digest != expected:
        blockers.append(f"{prefix}_expected_binding_mismatch")
    return digest


def _verify_source(
    source: dict, expected: str, blockers: list[str]
) -> tuple[str, list[dict], list[str], list[str]]:
    if not source:
        blockers.append("source_materialization_receipt_missing")
        return "", [], [], []
    headers = {
        "kernel": "ActOS Dukkha-Supported Bounded Plan Materialization Intake Kernel",
        "kernel_version": "v0.1",
        "actos_version": "v0.5",
        "status": "ACTOS_DUKKHA_SUPPORTED_BOUNDED_PLAN_MATERIALIZATION_INTAKE_READY",
    }
    for field, value in headers.items():
        if source.get(field) != value:
            blockers.append(f"source_{field}_invalid")
    digest = _bound_digest(
        source, SOURCE_DIGEST_FIELD, expected,
        "source_materialization_receipt", blockers,
    )
    true_fields = (
        "materialization_intake_performed", "materialization_candidates_issued",
        "all_plan_steps_materialized", "one_to_one_step_mapping_preserved",
        "step_sequence_preserved", "checkpoint_guards_preserved",
        "stop_conditions_preserved", "evidence_lineage_preserved",
        "alternative_candidates_preserved", "dissent_preserved",
        "minority_preserved", "dukkha_reduction_support_preserved",
        "protected_group_nonexternalization_preserved",
        "future_nonexternalization_preserved", "revision_capacity_preserved",
        "persistent_loop_reduction_preserved",
        "selection_remains_decisionos_owned",
        "persistent_world_state_unchanged", "world_model_prediction_not_truth",
        "world_mutation_not_granted", "history_read_only",
        "qi_grants_no_authority", "future_only",
    )
    false_fields = (
        "selection_authority_granted_to_actos",
        "plan_revision_authority_granted_to_actos",
        "dukkha_minimization_authority_granted_to_actos", "plan_activated",
        "adapter_binding_performed", "adapter_invocation_performed",
        "tool_invocation_performed", "external_side_effect_performed",
        "execution_authority_granted", "execution_permission", "active_now",
    )
    for field in true_fields:
        if source.get(field) is not True:
            blockers.append(f"source_boundary_{field}_missing")
    for field in false_fields:
        if source.get(field) is not False:
            blockers.append(f"source_boundary_{field}_promoted")

    raw_candidates = source.get("materialization_candidates")
    if not isinstance(raw_candidates, list) or not raw_candidates:
        blockers.append("source_materialization_candidates_invalid")
        raw_candidates = []
    if source.get("materialization_candidate_count") != len(raw_candidates):
        blockers.append("source_materialization_candidate_count_mismatch")
    candidates: list[dict] = []
    ids: list[str] = []
    for index, raw in enumerate(raw_candidates, start=1):
        if not isinstance(raw, Mapping) or set(raw) != CANDIDATE_FIELDS:
            blockers.append(f"source_candidate_schema_invalid_{index}")
            continue
        candidate = dict(raw)
        candidate_id = candidate.get("materialization_candidate_id")
        if not isinstance(candidate_id, str) or not candidate_id:
            blockers.append(f"source_candidate_id_invalid_{index}")
        ids.append(str(candidate_id))
        if candidate.get("sequence_index") != index:
            blockers.append(f"source_candidate_sequence_invalid_{index}")
        for field, empty in (
            ("precondition_digests", False),
            ("expected_effect_digests", True),
            ("effect_tags", True),
            ("evidence_lineage_digests", False),
            ("stop_condition_digests", False),
            ("branch_ids", True),
        ):
            valid, _ = _strings(candidate.get(field), empty=empty)
            if not valid:
                blockers.append(f"source_candidate_{field}_invalid_{index}")
        effects = candidate.get("effect_tags")
        if isinstance(effects, list) and FORBIDDEN_EFFECTS.intersection(effects):
            blockers.append(f"source_candidate_forbidden_effect_{index}")
        reversible = candidate.get("reversible")
        irreversible = candidate.get("irreversible")
        if not isinstance(reversible, bool) or not isinstance(irreversible, bool):
            blockers.append(f"source_candidate_reversibility_invalid_{index}")
        elif reversible == irreversible:
            blockers.append(f"source_candidate_reversibility_not_exclusive_{index}")
        if candidate.get("candidate_state") != "prepared_not_activated":
            blockers.append(f"source_candidate_state_invalid_{index}")
        if candidate.get("adapter_binding_digest") != "":
            blockers.append(f"source_candidate_already_bound_{index}")
        for field in (
            "tool_invocation_requested", "external_side_effect_requested",
            "execution_permission_requested", "active_now_requested",
        ):
            if candidate.get(field) is not False:
                blockers.append(f"source_candidate_{field}_promoted_{index}")
        if candidate.get("materialization_payload_digest") != (
            compute_materialization_payload_digest(candidate)
        ):
            blockers.append(f"source_candidate_payload_digest_mismatch_{index}")
        unsigned = dict(candidate)
        supplied = unsigned.pop("materialization_candidate_digest", None)
        if supplied != canonical_digest(unsigned):
            blockers.append(f"source_candidate_digest_mismatch_{index}")
        candidates.append(candidate)
    if len(ids) != len(set(ids)):
        blockers.append("source_candidate_ids_not_unique")
    if source.get("materialization_candidate_set_digest") != canonical_digest(candidates):
        blockers.append("source_candidate_set_digest_mismatch")
    lineage_ok, lineage = _strings(source.get("resulting_lineage_digests"))
    responsibility_ok, responsibility = _strings(
        source.get("resulting_responsibility_lineage_digests")
    )
    if not lineage_ok:
        blockers.append("source_resulting_lineage_invalid")
    if not responsibility_ok:
        blockers.append("source_resulting_responsibility_invalid")
    return digest, candidates, lineage, responsibility


def _verify_registry(
    registry: dict, expected: str, blockers: list[str]
) -> tuple[str, dict[str, dict]]:
    if not registry:
        blockers.append("adapter_registry_snapshot_missing")
        return "", {}
    if set(registry) != REGISTRY_FIELDS:
        blockers.append("adapter_registry_snapshot_schema_invalid")
    digest = registry.get("registry_snapshot_digest")
    if not isinstance(digest, str) or not digest:
        blockers.append("adapter_registry_snapshot_digest_missing")
        digest = ""
    else:
        if digest != compute_registry_snapshot_digest(registry):
            blockers.append("adapter_registry_snapshot_digest_mismatch")
        if digest != expected:
            blockers.append("adapter_registry_snapshot_expected_binding_mismatch")
    if registry.get("registry_version") != "v0.1":
        blockers.append("adapter_registry_version_invalid")
    issued = registry.get("issued_epoch")
    if not isinstance(issued, int) or isinstance(issued, bool) or issued < 0:
        blockers.append("adapter_registry_issued_epoch_invalid")
    raw_entries = registry.get("entries")
    if not isinstance(raw_entries, list) or not raw_entries:
        blockers.append("adapter_registry_entries_invalid")
        return digest, {}
    adapter_ids = [
        raw.get("adapter_id") if isinstance(raw, Mapping) else None
        for raw in raw_entries
    ]
    if (
        any(not isinstance(item, str) or not item for item in adapter_ids)
        or adapter_ids != sorted(item for item in adapter_ids if isinstance(item, str))
        or len(adapter_ids) != len(set(adapter_ids))
    ):
        blockers.append("adapter_registry_entries_not_canonical")
    entries: dict[str, dict] = {}
    for index, raw in enumerate(raw_entries):
        if not isinstance(raw, Mapping) or set(raw) != ENTRY_FIELDS:
            blockers.append(f"adapter_registry_entry_schema_invalid_{index}")
            continue
        entry = dict(raw)
        adapter_id = entry.get("adapter_id")
        if not isinstance(adapter_id, str) or not adapter_id:
            blockers.append(f"adapter_registry_adapter_id_invalid_{index}")
            continue
        for field in ("adapter_class", "capability_digest", "scope_policy_digest", "lease_id"):
            if not isinstance(entry.get(field), str) or not entry.get(field):
                blockers.append(f"adapter_registry_{field}_invalid_{adapter_id}")
        if not _strings(entry.get("supported_materialization_classes"))[0]:
            blockers.append(f"adapter_registry_classes_invalid_{adapter_id}")
        if not _strings(entry.get("effect_ceiling_tags"), empty=True)[0]:
            blockers.append(f"adapter_registry_effects_invalid_{adapter_id}")
        if not isinstance(entry.get("active"), bool):
            blockers.append(f"adapter_registry_active_invalid_{adapter_id}")
        if not isinstance(entry.get("revoked"), bool):
            blockers.append(f"adapter_registry_revoked_invalid_{adapter_id}")
        remaining = entry.get("remaining_uses")
        if (
            not isinstance(remaining, int) or isinstance(remaining, bool)
            or not 0 <= remaining <= 1024
        ):
            blockers.append(f"adapter_registry_remaining_invalid_{adapter_id}")
        unsigned = dict(entry)
        supplied = unsigned.pop("entry_digest", None)
        if supplied != canonical_digest(unsigned):
            blockers.append(f"adapter_registry_entry_digest_mismatch_{adapter_id}")
        entries[adapter_id] = entry
    return digest, entries


def _verify_context(
    context: dict, expected: str, source: dict, candidates: list[dict],
    blockers: list[str],
) -> tuple[str, list[str], dict]:
    if not context:
        blockers.append("authorization_context_missing")
        return "", [], {}
    if set(context) != CONTEXT_FIELDS:
        blockers.append("authorization_context_schema_invalid")
    digest = context.get("authorization_context_digest")
    if not isinstance(digest, str) or not digest:
        blockers.append("authorization_context_digest_missing")
        digest = ""
    else:
        if digest != compute_authorization_context_digest(context):
            blockers.append("authorization_context_digest_mismatch")
        if digest != expected:
            blockers.append("authorization_context_expected_binding_mismatch")
    string_fields = (
        "current_world_binding_digest", "current_world_model_state_digest",
        "current_world_lineage_digest", "requested_frontier_candidate_id",
        "session_id", "intent_digest", "authorization_nonce_digest",
        "freshness_observation_digest", "exact_act_cycle_digest",
    )
    for field in string_fields:
        if not isinstance(context.get(field), str) or not context.get(field):
            blockers.append(f"authorization_context_{field}_invalid")
    for field in (
        "source_observed_epoch", "current_epoch", "maximum_freshness_age",
        "current_world_model_revision",
    ):
        value = context.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            blockers.append(f"authorization_context_{field}_invalid")
    bound = context.get("maximum_freshness_age")
    if not isinstance(bound, int) or isinstance(bound, bool) or not 1 <= bound <= 64:
        blockers.append("authorization_context_freshness_bound_invalid")
    list_values: dict[str, list[str]] = {}
    for field in (
        "completed_materialization_candidate_ids", "prior_session_ids",
        "prior_intent_digests", "prior_authorization_nonce_digests",
    ):
        valid, values = _strings(context.get(field), empty=True)
        if not valid:
            blockers.append(f"authorization_context_{field}_invalid")
        list_values[field] = values
    completed = list_values["completed_materialization_candidate_ids"]
    candidate_ids = [item["materialization_candidate_id"] for item in candidates]
    if completed != candidate_ids[:len(completed)]:
        blockers.append("completed_candidates_not_contiguous_prefix")
    if len(completed) >= len(candidate_ids):
        blockers.append("activation_frontier_missing")
        return digest, completed, {}
    frontier = candidates[len(completed)]
    if context.get("requested_frontier_candidate_id") != (
        frontier.get("materialization_candidate_id")
    ):
        blockers.append("requested_frontier_candidate_mismatch")
    if context.get("intent_digest") != compute_exact_intent_digest(source, frontier):
        blockers.append("authorization_intent_digest_mismatch")
    if context.get("freshness_observation_digest") != (
        compute_freshness_observation_digest(source, context)
    ):
        blockers.append("freshness_observation_digest_mismatch")
    if context.get("exact_act_cycle_digest") != (
        compute_exact_act_cycle_digest(source, context, frontier)
    ):
        blockers.append("exact_act_cycle_digest_mismatch")
    if not isinstance(context.get("verifyos_step_reverification_digest"), str):
        blockers.append("verifyos_step_reverification_digest_invalid")
    return digest, completed, frontier


def _verify_bindings(
    raw_bindings: Any, candidates: list[dict], entries: dict[str, dict],
    blockers: list[str],
) -> tuple[list[dict], bool]:
    if not isinstance(raw_bindings, list) or len(raw_bindings) != len(candidates):
        blockers.append("adapter_bindings_invalid")
        return [], False
    bindings: list[dict] = []
    registry_ready = True
    for index, (raw, candidate) in enumerate(zip(raw_bindings, candidates), start=1):
        if not isinstance(raw, Mapping) or set(raw) != BINDING_FIELDS:
            blockers.append(f"adapter_binding_schema_invalid_{index}")
            continue
        binding = dict(raw)
        if binding.get("materialization_candidate_id") != (
            candidate["materialization_candidate_id"]
        ):
            blockers.append(f"adapter_binding_candidate_mismatch_{index}")
        entry = entries.get(str(binding.get("adapter_id")))
        if entry is None:
            blockers.append(f"adapter_binding_registry_entry_missing_{index}")
            continue
        classes = entry.get("supported_materialization_classes")
        if not isinstance(classes, list) or candidate["materialization_class"] not in classes:
            blockers.append(f"adapter_binding_class_unsupported_{index}")
        valid_effects, requested = _strings(
            binding.get("requested_effect_tags"), empty=True
        )
        if not valid_effects:
            blockers.append(f"adapter_binding_effects_invalid_{index}")
            requested = []
        if requested != candidate["effect_tags"]:
            blockers.append(f"adapter_binding_effects_mismatch_{index}")
        ceilings = entry.get("effect_ceiling_tags")
        if not isinstance(ceilings, list) or not set(requested).issubset(set(ceilings)):
            blockers.append(f"adapter_binding_effect_ceiling_exceeded_{index}")
        if FORBIDDEN_EFFECTS.intersection(requested):
            blockers.append(f"adapter_binding_forbidden_effect_{index}")
        expected_fields = {
            "adapter_registry_entry_digest": entry.get("entry_digest"),
            "capability_digest": entry.get("capability_digest"),
            "scope_digest": compute_binding_scope_digest(candidate),
            "effect_ceiling_digest": compute_effect_ceiling_digest(candidate, entry),
            "lease_id": entry.get("lease_id"),
            "binding_state": "bound_not_invoked",
        }
        for field, value in expected_fields.items():
            if binding.get(field) != value:
                blockers.append(f"adapter_binding_{field}_mismatch_{index}")
        unsigned = dict(binding)
        supplied = unsigned.pop("binding_digest", None)
        if supplied != canonical_digest(unsigned):
            blockers.append(f"adapter_binding_digest_mismatch_{index}")
        if entry.get("active") is not True or entry.get("revoked") is not False:
            registry_ready = False
        bindings.append(binding)
    if [item.get("materialization_candidate_id") for item in bindings] != [
        item["materialization_candidate_id"] for item in candidates
    ]:
        blockers.append("adapter_bindings_not_candidate_ordered")
    return bindings, registry_ready


def build_actos_dukkha_preserving_adapter_binding_authorization_intake(
    *,
    source_materialization_receipt: Mapping[str, Any],
    expected_source_materialization_receipt_digest: str,
    adapter_registry_snapshot: Mapping[str, Any],
    expected_adapter_registry_snapshot_digest: str,
    adapter_bindings: list[Mapping[str, Any]],
    authorization_context: Mapping[str, Any],
    expected_authorization_context_digest: str,
    authorization_policy_digest: str,
    actos_authorization_responsibility_digest: str,
    authorization_request_id: str,
    authorization_bundle_digest: str,
) -> ActOSDukkhaPreservingAdapterAuthorizationResult:
    blockers: list[str] = []
    source = dict(source_materialization_receipt) if isinstance(
        source_materialization_receipt, Mapping
    ) else {}
    registry = dict(adapter_registry_snapshot) if isinstance(
        adapter_registry_snapshot, Mapping
    ) else {}
    context = dict(authorization_context) if isinstance(
        authorization_context, Mapping
    ) else {}
    required_strings = {
        "expected_source_materialization_receipt_digest":
            expected_source_materialization_receipt_digest,
        "expected_adapter_registry_snapshot_digest":
            expected_adapter_registry_snapshot_digest,
        "expected_authorization_context_digest":
            expected_authorization_context_digest,
        "authorization_policy_digest": authorization_policy_digest,
        "actos_authorization_responsibility_digest":
            actos_authorization_responsibility_digest,
        "authorization_request_id": authorization_request_id,
        "authorization_bundle_digest": authorization_bundle_digest,
    }
    for name, value in required_strings.items():
        if not isinstance(value, str) or not value:
            blockers.append(f"{name}_missing")

    source_digest, candidates, source_lineage, source_responsibility = (
        _verify_source(
            source, expected_source_materialization_receipt_digest, blockers
        )
    )
    registry_digest, entries = _verify_registry(
        registry, expected_adapter_registry_snapshot_digest, blockers
    )
    context_digest, completed, frontier = _verify_context(
        context, expected_authorization_context_digest,
        source, candidates, blockers,
    )
    bindings, registry_ready = _verify_bindings(
        adapter_bindings, candidates, entries, blockers
    )
    binding_set_digest = canonical_digest(bindings)
    if not blockers:
        expected_bundle = compute_adapter_binding_authorization_bundle_digest(
            source_materialization_receipt_digest=source_digest,
            expected_source_materialization_receipt_digest=
                expected_source_materialization_receipt_digest,
            adapter_registry_snapshot_digest=registry_digest,
            expected_adapter_registry_snapshot_digest=
                expected_adapter_registry_snapshot_digest,
            adapter_binding_set_digest=binding_set_digest,
            authorization_context_digest=context_digest,
            expected_authorization_context_digest=
                expected_authorization_context_digest,
            authorization_policy_digest=authorization_policy_digest,
            actos_authorization_responsibility_digest=
                actos_authorization_responsibility_digest,
            authorization_request_id=authorization_request_id,
        )
        if authorization_bundle_digest != expected_bundle:
            blockers.append("authorization_bundle_digest_mismatch")
    if blockers:
        return ActOSDukkhaPreservingAdapterAuthorizationResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    frontier_binding = bindings[len(completed)]
    frontier_entry = entries[frontier_binding["adapter_id"]]
    world_current = (
        context["current_world_binding_digest"] ==
            source["source_world_binding_digest"]
        and context["current_world_model_state_digest"] ==
            source["source_world_model_state_digest"]
        and context["current_world_model_revision"] ==
            source["source_world_model_revision"]
        and context["current_world_lineage_digest"] ==
            source["source_world_lineage_digest"]
    )
    age = context["current_epoch"] - context["source_observed_epoch"]
    freshness_current = 0 <= age <= context["maximum_freshness_age"]
    replay_fresh = (
        context["session_id"] not in context["prior_session_ids"]
        and context["intent_digest"] not in context["prior_intent_digests"]
        and context["authorization_nonce_digest"] not in
            context["prior_authorization_nonce_digests"]
    )
    lease_available = frontier_entry["remaining_uses"] >= 1
    irreversible_reverified = (
        frontier["reversible"] is True
        or bool(context["verifyos_step_reverification_digest"])
    )
    if not world_current:
        disposition = DISPOSITION_WORLD_REFRESH
    elif not freshness_current:
        disposition = DISPOSITION_FRESHNESS_REFRESH
    elif not registry_ready:
        disposition = DISPOSITION_REGISTRY_REPAIR
    elif not lease_available:
        disposition = DISPOSITION_LEASE_REFRESH
    elif not replay_fresh:
        disposition = DISPOSITION_REPLAY_REJECTED
    elif not irreversible_reverified:
        disposition = DISPOSITION_REVERIFY
    else:
        disposition = DISPOSITION_READY

    admitted = disposition == DISPOSITION_READY
    remaining_before = frontier_entry["remaining_uses"]
    remaining_after = remaining_before - 1 if admitted else remaining_before
    authorization_record = {
        "frontier_materialization_candidate_id":
            frontier["materialization_candidate_id"],
        "frontier_adapter_id": frontier_binding["adapter_id"],
        "frontier_binding_digest": frontier_binding["binding_digest"],
        "frontier_lease_id": frontier_binding["lease_id"],
        "session_id": context["session_id"],
        "intent_digest": context["intent_digest"],
        "authorization_nonce_digest": context["authorization_nonce_digest"],
        "exact_act_cycle_digest": context["exact_act_cycle_digest"],
        "authorization_disposition": disposition,
        "activation_authorization_admitted": admitted,
        "remaining_uses_before_reservation": remaining_before,
        "remaining_uses_after_reservation": remaining_after,
    }
    authorization_record_digest = canonical_digest(authorization_record)
    token_digest = canonical_digest({
        **authorization_record,
        "authorization_policy_digest": authorization_policy_digest,
        "authorization_request_id": authorization_request_id,
    }) if admitted else ""
    resulting_lineage = sorted(set(source_lineage) | {
        source_digest, registry_digest, context_digest, binding_set_digest,
        authorization_record_digest, authorization_bundle_digest,
    } | ({token_digest} if token_digest else set()))
    resulting_responsibility = sorted(
        set(source_responsibility) | {actos_authorization_responsibility_digest}
    )

    receipt = {
        "kernel": "ActOS Dukkha-Preserving Adapter Binding and Activation Authorization Intake Kernel",
        "kernel_version": "v0.1",
        "actos_version": "v0.6",
        "status": "ACTOS_DUKKHA_PRESERVING_ADAPTER_BINDING_AUTHORIZATION_ROUTED",
        "source_materialization_receipt_digest": source_digest,
        "source_verifyos_dukkha_certificate_digest":
            source["source_verifyos_dukkha_certificate_digest"],
        "source_plan_receipt_digest": source["source_plan_receipt_digest"],
        "source_concrete_plan_digest": source["source_concrete_plan_digest"],
        "source_world_binding_digest": source["source_world_binding_digest"],
        "source_world_model_state_digest":
            source["source_world_model_state_digest"],
        "source_world_model_revision": source["source_world_model_revision"],
        "source_world_lineage_digest": source["source_world_lineage_digest"],
        "selected_candidate_id": source["selected_candidate_id"],
        "selected_candidate_plan_intent_digest":
            source["selected_candidate_plan_intent_digest"],
        "dukkha_assessment_digest": source["dukkha_assessment_digest"],
        "reference_plan_digest": source["reference_plan_digest"],
        "adapter_registry_snapshot_digest": registry_digest,
        "authorization_context_digest": context_digest,
        "authorization_policy_digest": authorization_policy_digest,
        "actos_authorization_responsibility_digest":
            actos_authorization_responsibility_digest,
        "authorization_request_id": authorization_request_id,
        "authorization_bundle_digest": authorization_bundle_digest,
        "adapter_bindings": bindings,
        "adapter_binding_count": len(bindings),
        "adapter_binding_set_digest": binding_set_digest,
        "completed_materialization_candidate_ids": completed,
        "activation_frontier_candidate_id":
            frontier["materialization_candidate_id"],
        "frontier_adapter_id": frontier_binding["adapter_id"],
        "frontier_lease_id": frontier_binding["lease_id"],
        "frontier_candidate_reversible": frontier["reversible"],
        "frontier_candidate_irreversible": frontier["irreversible"],
        "authorization_disposition": disposition,
        "activation_authorization_admitted": admitted,
        "activation_authorization_receipt_issued": admitted,
        "activation_authorization_token_digest": token_digest,
        "authorization_record": authorization_record,
        "authorization_record_digest": authorization_record_digest,
        "remaining_uses_before_reservation": remaining_before,
        "remaining_uses_after_reservation": remaining_after,
        "single_use_authorization_reserved": admitted,
        "lease_use_consumed": False,
        "adapter_registry_snapshot_unchanged": True,
        "world_conditions_current": world_current,
        "freshness_current": freshness_current,
        "adapter_registry_ready": registry_ready,
        "frontier_lease_available": lease_available,
        "session_intent_nonce_replay_fresh": replay_fresh,
        "irreversible_step_reverification_satisfied":
            irreversible_reverified,
        "adapter_binding_performed": True,
        "all_materialization_candidates_bound": len(bindings) == len(candidates),
        "one_to_one_candidate_binding_preserved": True,
        "activation_frontier_sequence_preserved": True,
        "scope_and_effect_ceiling_exact": True,
        "checkpoint_guards_preserved": True,
        "stop_conditions_preserved": True,
        "evidence_lineage_preserved": True,
        "alternative_candidates_preserved": True,
        "dissent_preserved": True,
        "minority_preserved": True,
        "dukkha_reduction_support_preserved": True,
        "protected_group_nonexternalization_preserved": True,
        "future_nonexternalization_preserved": True,
        "revision_capacity_preserved": True,
        "persistent_loop_reduction_preserved": True,
        "single_scalar_utility_not_introduced": True,
        "selection_remains_decisionos_owned": True,
        "selection_authority_granted_to_actos": False,
        "plan_revision_authority_granted_to_actos": False,
        "dukkha_minimization_authority_granted_to_actos": False,
        "plan_activated": False,
        "adapter_invocation_performed": False,
        "tool_invocation_performed": False,
        "external_side_effect_performed": False,
        "execution_authority_granted": False,
        "execution_permission": False,
        "persistent_world_state_unchanged": True,
        "world_model_prediction_not_truth": True,
        "world_mutation_not_granted": True,
        "history_read_only": True,
        "qi_grants_no_authority": True,
        "future_only": True,
        "active_now": False,
        "resulting_lineage_digests": resulting_lineage,
        "resulting_responsibility_lineage_digests": resulting_responsibility,
    }
    receipt[RECEIPT_DIGEST_FIELD] = canonical_digest(receipt)
    return ActOSDukkhaPreservingAdapterAuthorizationResult(
        STATUS_READY, [], receipt
    )
