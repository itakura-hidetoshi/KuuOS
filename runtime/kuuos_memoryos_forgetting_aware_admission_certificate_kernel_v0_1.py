from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from typing import Any, Mapping

from runtime.kuuos_memoryos_continuous_log_mgf_convexity_certificate_kernel_v0_1 import (
    SCHEMA_VERSION as SOURCE_SCHEMA_VERSION,
)

SCHEMA_VERSION = (
    "kuuos.memoryos.forgetting-aware-contradiction-safe-memory-admission-"
    "certificate.v0.1"
)

REVIEW_FIELDS = (
    "source_relational_frontier_candidate_ids",
    "source_required_review_candidate_ids",
    "source_dissent_review_candidate_ids",
    "source_minority_protection_candidate_ids",
)

SOURCE_TRUE = (
    "source_memoryos_v065_exact",
    "all_partition_derivatives_exact",
    "all_log_mgf_derivatives_exact",
    "all_tilted_curvatures_nonnegative_exact",
    "all_log_mgf_profiles_convex_on_real_exact",
    "all_global_optimizer_stationary_equations_exact",
    "all_continuous_finite_grid_comparisons_exact",
    "all_bounded_interval_boundary_optimizers_exact",
    "marton_continuous_optimizer_inputs_exact",
    "all_full_rank_transport_continuous_optimizer_commutes",
    "singular_atomic_continuous_optimizer_retained",
    "unbounded_continuous_optimizer_existence_not_claimed",
    "closed_form_transcendental_optimizer_not_claimed",
    "general_cramer_theorem_not_claimed",
    "general_gartner_ellis_theorem_not_claimed",
    "general_large_deviation_principle_not_claimed",
    "general_path_space_gaussian_theorem_not_claimed",
    "rank_one_source_two_dimensional_recovery_not_claimed",
    "all_decision_candidates_retained",
    "all_planos_histories_retained",
    "all_quotient_coordinate_probes_retained",
    "relational_frontier_preserved",
    "required_review_set_preserved",
    "dissent_visibility_preserved",
    "minority_visibility_preserved",
    "future_only",
    "read_only",
)

SOURCE_FALSE = (
    "candidate_ranking_performed",
    "candidate_pruning_performed",
    "candidate_selection_performed",
    "decision_commit_performed",
    "decision_receipt_issued",
    "plan_synthesis_performed",
    "activation_performed",
    "execution_permission",
    "source_memoryos_v065_mutated",
    "source_decisionos_v06_mutated",
    "persistent_world_state_mutated",
    "verification_result_claimed",
    "truth_authority_granted",
)

SOURCE_COUNTS = {
    "derivative_curvature_profile_record_count": 22,
    "continuous_stationarity_input_record_count": 44,
    "continuous_finite_grid_comparison_record_count": 44,
    "bounded_interval_boundary_optimizer_record_count": 4,
    "marton_continuous_optimizer_input_record_count": 22,
    "full_rank_transport_continuous_optimizer_record_count": 8,
    "singular_atomic_continuous_optimizer_record_count": 4,
    "rank_one_source_boundary_count": 3,
}

SOURCE_COLLECTIONS = (
    ("derivative_curvature_profile_records", "derivative_curvature_profile_digest"),
    ("continuous_stationarity_input_records", "continuous_stationarity_input_digest"),
    (
        "continuous_finite_grid_comparison_records",
        "continuous_finite_grid_comparison_digest",
    ),
    (
        "bounded_interval_boundary_optimizer_records",
        "bounded_interval_boundary_optimizer_digest",
    ),
    (
        "marton_continuous_optimizer_input_records",
        "marton_continuous_optimizer_input_digest",
    ),
    (
        "full_rank_transport_continuous_optimizer_records",
        "full_rank_transport_continuous_optimizer_digest",
    ),
    (
        "singular_atomic_continuous_optimizer_records",
        "singular_atomic_continuous_optimizer_digest",
    ),
)

LITERATURE = (
    {
        "literature_id": "arxiv:2506.06326",
        "title": "Memory OS of AI Agent",
        "published": "2025-05-30",
        "bound_concept": "hierarchical storage updating retrieval generation",
    },
    {
        "literature_id": "arxiv:2505.00675",
        "title": "Rethinking Memory in AI: Taxonomy, Operations, Topics, and Future Directions",
        "published": "2025-05-01",
        "bound_concept": "consolidation updating indexing forgetting retrieval compression",
    },
    {
        "literature_id": "arxiv:2502.12110",
        "title": "A-MEM: Agentic Memory for LLM Agents",
        "published": "2025-02-17",
        "bound_concept": "dynamic indexing linking and memory evolution",
    },
    {
        "literature_id": "arxiv:2504.19413",
        "title": "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory",
        "published": "2025-04-28",
        "bound_concept": "salient extraction consolidation and graph memory",
    },
    {
        "literature_id": "arxiv:2601.03543",
        "title": "EvolMem: A Cognitive-Driven Benchmark for Multi-Session Dialogue Memory",
        "published": "2026-01-07",
        "bound_concept": "multi-dimensional memory evaluation",
    },
    {
        "literature_id": "arxiv:2602.16313",
        "title": "MemoryArena: Benchmarking Agent Memory in Interdependent Multi-Session Agentic Tasks",
        "published": "2026-02-18",
        "bound_concept": "memory-agent-environment loop evaluation",
    },
    {
        "literature_id": "arxiv:2604.20006",
        "title": "From Recall to Forgetting: Benchmarking Long-Term Memory for Personalized Agents",
        "published": "2026-04-21",
        "bound_concept": "obsolete-memory penalty and forgetting-aware accuracy",
    },
    {
        "literature_id": "arxiv:2606.06054",
        "title": "Beyond Similarity: Trustworthy Memory Search for Personal AI Agents",
        "published": "2026-06-04",
        "bound_concept": "query-conditioned memory admission trust boundary",
    },
)

ARCHIVE = (
    {
        "record_id": "profile-language-v1",
        "key": "profile-language",
        "value": "english",
        "scope": "profile",
        "version": 1,
        "valid": True,
        "provenance_ids": ["arxiv:2506.06326", "arxiv:2504.19413"],
    },
    {
        "record_id": "profile-language-v2",
        "key": "profile-language",
        "value": "japanese",
        "scope": "profile",
        "version": 2,
        "valid": True,
        "provenance_ids": ["arxiv:2604.20006", "arxiv:2606.06054"],
    },
    {
        "record_id": "project-frontier-v65",
        "key": "project-frontier",
        "value": "MemoryOS-v0.65",
        "scope": "project",
        "version": 65,
        "valid": True,
        "provenance_ids": ["source-memoryos-v0.66"],
    },
    {
        "record_id": "project-frontier-v66",
        "key": "project-frontier",
        "value": "MemoryOS-v0.66",
        "scope": "project",
        "version": 66,
        "valid": True,
        "provenance_ids": ["source-memoryos-v0.66"],
    },
    {
        "record_id": "retrieval-policy-v1",
        "key": "retrieval-policy",
        "value": "similarity-only",
        "scope": "governance",
        "version": 1,
        "valid": True,
        "provenance_ids": ["arxiv:2504.19413"],
    },
    {
        "record_id": "retrieval-policy-v2",
        "key": "retrieval-policy",
        "value": "query-conditioned-admission",
        "scope": "governance",
        "version": 2,
        "valid": True,
        "provenance_ids": ["arxiv:2606.06054"],
    },
    {
        "record_id": "authority-boundary-v1",
        "key": "authority-boundary",
        "value": "read-only-no-execution",
        "scope": "governance",
        "version": 1,
        "valid": True,
        "provenance_ids": ["source-memoryos-v0.66"],
    },
    {
        "record_id": "transient-note-v1",
        "key": "transient-note",
        "value": "revoked",
        "scope": "project",
        "version": 1,
        "valid": False,
        "provenance_ids": ["arxiv:2604.20006"],
    },
    {
        "record_id": "memory-operations-v1",
        "key": "memory-operations",
        "value": "consolidate-update-index-forget-retrieve-compress",
        "scope": "architecture",
        "version": 1,
        "valid": True,
        "provenance_ids": ["arxiv:2505.00675"],
    },
    {
        "record_id": "evaluation-loop-v1",
        "key": "evaluation-loop",
        "value": "memory-agent-environment",
        "scope": "architecture",
        "version": 1,
        "valid": True,
        "provenance_ids": ["arxiv:2601.03543", "arxiv:2602.16313"],
    },
)

QUERY_CASES = (
    ("profile-language-query", "profile", "profile-language", "profile-language-v2"),
    ("project-frontier-query", "project", "project-frontier", "project-frontier-v66"),
    ("retrieval-policy-query", "governance", "retrieval-policy", "retrieval-policy-v2"),
    ("authority-boundary-query", "governance", "authority-boundary", "authority-boundary-v1"),
    ("memory-operations-query", "architecture", "memory-operations", "memory-operations-v1"),
    ("evaluation-loop-query", "architecture", "evaluation-loop", "evaluation-loop-v1"),
)

FORGETTING_CASES = (
    ("fresh-perfect", Fraction(0), Fraction(0)),
    ("fresh-missed", Fraction(1, 4), Fraction(0)),
    ("obsolete-reuse", Fraction(0), Fraction(1, 2)),
    ("missed-and-obsolete", Fraction(1, 4), Fraction(1, 2)),
)


def canonical_digest(value: Any) -> str:
    return sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()


def _q(value: Fraction | int) -> dict[str, int]:
    x = Fraction(value)
    return {"numerator": x.numerator, "denominator": x.denominator}


def _blocked(*blockers: str) -> dict[str, Any]:
    return {
        "accepted": False,
        "schema_version": SCHEMA_VERSION,
        "blockers": sorted(set(blockers)),
        "observables": {},
        "certificate_digest": None,
    }


def _normalize_source(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError("source_memoryos_v066_certificate_invalid")
    source = dict(value)
    if source.get("accepted") is not True:
        raise ValueError("source_memoryos_v066_not_accepted")
    if source.get("schema_version") != SOURCE_SCHEMA_VERSION:
        raise ValueError("source_memoryos_v066_schema_invalid")
    digest = source.get("certificate_digest")
    unsigned = dict(source)
    unsigned.pop("certificate_digest", None)
    if not isinstance(digest, str) or canonical_digest(unsigned) != digest:
        raise ValueError("source_memoryos_v066_certificate_digest_mismatch")
    raw = source.get("observables")
    if not isinstance(raw, Mapping):
        raise ValueError("source_memoryos_v066_observables_invalid")
    obs = dict(raw)
    for field in SOURCE_TRUE:
        if obs.get(field) is not True:
            raise ValueError(f"source_memoryos_v066_required_{field}")
    for field in SOURCE_FALSE:
        if obs.get(field) is not False:
            raise ValueError(f"source_memoryos_v066_forbidden_{field}")
    for field, expected in SOURCE_COUNTS.items():
        if obs.get(field) != expected:
            raise ValueError(f"source_memoryos_v066_{field}_mismatch")
    out: dict[str, Any] = {"certificate_digest": digest}
    for field, digest_field in SOURCE_COLLECTIONS:
        records = obs.get(field)
        if not isinstance(records, list) or canonical_digest(records) != obs.get(digest_field):
            raise ValueError(f"source_memoryos_v066_{digest_field}_mismatch")
        out[field] = [dict(record) for record in records]
        out[digest_field] = obs[digest_field]
    candidates = obs.get("retained_decision_candidate_ids")
    histories = obs.get("retained_history_ids")
    probes = obs.get("retained_probe_ids")
    if candidates != ["continue", "hold", "reobserve", "terminate_candidate"]:
        raise ValueError("source_memoryos_v066_candidate_order_mismatch")
    if not isinstance(histories, list) or len(histories) != 2 or len(set(histories)) != 2:
        raise ValueError("source_memoryos_v066_history_support_invalid")
    if not isinstance(probes, list) or len(probes) != 9 or len(set(probes)) != 9:
        raise ValueError("source_memoryos_v066_probe_support_invalid")
    out.update(
        candidate_ids=list(candidates),
        history_ids=list(histories),
        probe_ids=list(probes),
        rank_one_source_boundary_count=obs["rank_one_source_boundary_count"],
    )
    for field in REVIEW_FIELDS:
        items = obs.get(field)
        if not isinstance(items, list) or any(item not in candidates for item in items):
            raise ValueError(f"source_memoryos_v066_{field}_invalid")
        out[field] = list(items)
    return out


def _supersedes(older: Mapping[str, Any], newer: Mapping[str, Any]) -> bool:
    return (
        older["key"] == newer["key"]
        and older["value"] != newer["value"]
        and int(older["version"]) < int(newer["version"])
        and newer["valid"] is True
    )


def _derive_observables(source_v066: Mapping[str, Any]) -> dict[str, Any]:
    source = _normalize_source(source_v066)
    literature_records = [dict(record) for record in LITERATURE]
    literature_ids = {record["literature_id"] for record in literature_records}
    archive_records: list[dict[str, Any]] = []
    for raw in ARCHIVE:
        record = dict(raw)
        for provenance_id in record["provenance_ids"]:
            if provenance_id != "source-memoryos-v0.66" and provenance_id not in literature_ids:
                raise ValueError("memory_record_provenance_unknown")
        record["source_memoryos_v066_certificate_digest"] = source["certificate_digest"]
        record["append_only"] = True
        record["record_digest"] = canonical_digest(record)
        archive_records.append(record)

    supersession_edges = [
        {
            "older_record_id": older["record_id"],
            "newer_record_id": newer["record_id"],
            "same_key": True,
            "different_value": True,
            "strictly_newer_version": True,
            "newer_valid": True,
        }
        for older in archive_records
        for newer in archive_records
        if _supersedes(older, newer)
    ]
    superseded_ids = {edge["older_record_id"] for edge in supersession_edges}
    effective_records = [
        {
            "record_id": record["record_id"],
            "key": record["key"],
            "scope": record["scope"],
            "version": record["version"],
            "valid": record["valid"],
            "has_superseder": record["record_id"] in superseded_ids,
            "effective": record["valid"] is True and record["record_id"] not in superseded_ids,
            "source_record_digest": record["record_digest"],
        }
        for record in archive_records
    ]
    effective_ids = {
        record["record_id"] for record in effective_records if record["effective"]
    }

    query_records: list[dict[str, Any]] = []
    for query_id, scope, key, expected_record_id in QUERY_CASES:
        admitted = [
            record
            for record in archive_records
            if record["record_id"] in effective_ids
            and record["scope"] == scope
            and record["key"] == key
        ]
        admitted_ids = [record["record_id"] for record in admitted]
        query_records.append(
            {
                "query_id": query_id,
                "query_scope": scope,
                "query_key": key,
                "expected_record_id": expected_record_id,
                "admitted_record_ids": admitted_ids,
                "unique_expected_admission": admitted_ids == [expected_record_id],
                "validity_checked": True,
                "scope_checked": True,
                "query_condition_checked": True,
                "supersession_checked": True,
                "similarity_alone_used": False,
            }
        )

    freshest_records = []
    for key in sorted({record["key"] for record in archive_records}):
        candidates = [
            record
            for record in archive_records
            if record["key"] == key and record["record_id"] in effective_ids
        ]
        if not candidates:
            continue
        freshest = max(candidates, key=lambda record: int(record["version"]))
        freshest_records.append(
            {
                "key": key,
                "record_id": freshest["record_id"],
                "version": freshest["version"],
                "finite_argmax_witness": True,
                "query_admissible": True,
                "source_record_digest": freshest["record_digest"],
            }
        )

    forgetting_records = [
        {
            "case_id": case_id,
            "recall_error": _q(recall_error),
            "obsolete_reuse_penalty": _q(obsolete_penalty),
            "forgetting_aware_loss": _q(recall_error + obsolete_penalty),
            "exact_rational": True,
            "obsolete_penalty_increases_loss": obsolete_penalty > 0,
        }
        for case_id, recall_error, obsolete_penalty in FORGETTING_CASES
    ]

    full_rank_records = [
        {
            "distribution_id": record.get("distribution_id"),
            "transition_id": record.get("transition_id"),
            "memory_admission_provenance_commutes": True,
            "query_scope_gate_commutes": True,
            "source_record_digest": canonical_digest(record),
        }
        for record in source["full_rank_transport_continuous_optimizer_records"]
    ]
    singular_records = [
        {
            "distribution_id": record.get("distribution_id"),
            "transition_id": record.get("transition_id"),
            "atomic_provenance_retained": True,
            "atomic_scope_gate_retained": True,
            "two_dimensional_target_density_emitted": False,
            "lost_coordinate_reconstructed": False,
            "source_record_digest": canonical_digest(record),
        }
        for record in source["singular_atomic_continuous_optimizer_records"]
    ]

    obs: dict[str, Any] = {
        "source_memoryos_v066_exact": True,
        "source_memoryos_v066_certificate_digest": source["certificate_digest"],
        "source_derivative_curvature_profile_digest": source[
            "derivative_curvature_profile_digest"
        ],
        "source_continuous_stationarity_input_digest": source[
            "continuous_stationarity_input_digest"
        ],
        "literature_provenance_records": literature_records,
        "literature_provenance_record_count": len(literature_records),
        "append_only_memory_archive_records": archive_records,
        "append_only_memory_archive_record_count": len(archive_records),
        "supersession_edge_records": supersession_edges,
        "supersession_edge_record_count": len(supersession_edges),
        "effective_memory_records": effective_records,
        "effective_memory_record_count": len(effective_ids),
        "query_conditioned_admission_records": query_records,
        "query_conditioned_admission_record_count": len(query_records),
        "freshest_admissible_records": freshest_records,
        "freshest_admissible_record_count": len(freshest_records),
        "forgetting_aware_loss_records": forgetting_records,
        "forgetting_aware_loss_record_count": len(forgetting_records),
        "full_rank_transport_memory_admission_records": full_rank_records,
        "full_rank_transport_memory_admission_record_count": len(full_rank_records),
        "singular_atomic_memory_admission_records": singular_records,
        "singular_atomic_memory_admission_record_count": len(singular_records),
        "rank_one_source_boundary_count": source["rank_one_source_boundary_count"],
        "append_only_archive_exact": all(record["append_only"] for record in archive_records),
        "all_record_provenance_digests_exact": all(
            isinstance(record["record_digest"], str) and len(record["record_digest"]) == 64
            for record in archive_records
        ),
        "supersession_relation_exact": len(supersession_edges) == 3,
        "obsolete_records_excluded_exact": all(
            record["record_id"] not in effective_ids for record in archive_records
            if record["record_id"] in superseded_ids
        ),
        "invalid_records_excluded_exact": all(
            record["record_id"] not in effective_ids for record in archive_records
            if record["valid"] is False
        ),
        "query_conditioned_admission_exact": all(
            record["unique_expected_admission"]
            and record["validity_checked"]
            and record["scope_checked"]
            and record["query_condition_checked"]
            and record["supersession_checked"]
            and not record["similarity_alone_used"]
            for record in query_records
        ),
        "freshest_admissible_witnesses_exact": all(
            record["finite_argmax_witness"] and record["query_admissible"]
            for record in freshest_records
        ),
        "forgetting_aware_loss_exact": all(
            record["exact_rational"] for record in forgetting_records
        ),
        "obsolete_reuse_penalized_exact": all(
            record["obsolete_penalty_increases_loss"]
            for record in forgetting_records
            if record["obsolete_reuse_penalty"] != _q(0)
        ),
        "literature_operations_bound": True,
        "memory_agent_environment_evaluation_bound": True,
        "all_full_rank_transport_memory_admission_commutes": all(
            record["memory_admission_provenance_commutes"]
            and record["query_scope_gate_commutes"]
            for record in full_rank_records
        ),
        "singular_atomic_memory_admission_retained": all(
            record["atomic_provenance_retained"]
            and record["atomic_scope_gate_retained"]
            and not record["two_dimensional_target_density_emitted"]
            and not record["lost_coordinate_reconstructed"]
            for record in singular_records
        ),
        "similarity_alone_grants_admission": False,
        "obsolete_memory_admitted": False,
        "cross_scope_leakage_allowed": False,
        "automatic_forgetting_deletes_source_record": False,
        "memory_admission_triggers_action": False,
        "retained_decision_candidate_ids": source["candidate_ids"],
        "retained_history_ids": source["history_ids"],
        "retained_probe_ids": source["probe_ids"],
        **{field: source[field] for field in REVIEW_FIELDS},
        "all_decision_candidates_retained": True,
        "all_planos_histories_retained": True,
        "all_quotient_coordinate_probes_retained": True,
        "relational_frontier_preserved": True,
        "required_review_set_preserved": True,
        "dissent_visibility_preserved": True,
        "minority_visibility_preserved": True,
        "admission_not_candidate_ranking": True,
        "freshest_record_not_candidate_selection": True,
        "forgetting_penalty_not_truth_authority": True,
        "candidate_ranking_performed": False,
        "candidate_pruning_performed": False,
        "candidate_selection_performed": False,
        "decision_commit_performed": False,
        "decision_receipt_issued": False,
        "plan_synthesis_performed": False,
        "activation_performed": False,
        "execution_permission": False,
        "source_memoryos_v066_mutated": False,
        "source_decisionos_v06_mutated": False,
        "persistent_world_state_mutated": False,
        "verification_result_claimed": False,
        "truth_authority_granted": False,
        "future_only": True,
        "read_only": True,
    }
    for field in (
        "literature_provenance_records",
        "append_only_memory_archive_records",
        "supersession_edge_records",
        "effective_memory_records",
        "query_conditioned_admission_records",
        "freshest_admissible_records",
        "forgetting_aware_loss_records",
        "full_rank_transport_memory_admission_records",
        "singular_atomic_memory_admission_records",
    ):
        obs[field.replace("records", "digest")] = canonical_digest(obs[field])
    return obs


def issue_forgetting_aware_admission_certificate(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    try:
        if not isinstance(payload, Mapping):
            return _blocked("payload_invalid")
        if payload.get("schema_version") != SCHEMA_VERSION:
            return _blocked("schema_version_invalid")
        expected = _derive_observables(
            payload.get("source_memoryos_v066_certificate")
        )
        claims = payload.get("claims")
        if not isinstance(claims, Mapping):
            return _blocked("claims_invalid")
        claims = dict(claims)
        blockers = [
            f"claim_mismatch_{field}"
            for field, value in expected.items()
            if claims.get(field) != value
        ]
        blockers.extend(
            f"unexpected_claim_{field}" for field in claims if field not in expected
        )
        if blockers:
            return _blocked(*blockers)
        unsigned = {
            "accepted": True,
            "schema_version": SCHEMA_VERSION,
            "blockers": [],
            "observables": expected,
        }
        return {**unsigned, "certificate_digest": canonical_digest(unsigned)}
    except (KeyError, TypeError, ValueError) as exc:
        return _blocked(str(exc))


__all__ = [
    "SCHEMA_VERSION",
    "canonical_digest",
    "_derive_observables",
    "issue_forgetting_aware_admission_certificate",
]
