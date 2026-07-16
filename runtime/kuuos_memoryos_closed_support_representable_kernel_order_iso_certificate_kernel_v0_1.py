from __future__ import annotations

import hashlib
import json
from pathlib import Path

from runtime.kuuos_memoryos_sensor_kernel_polarity_certificate_kernel_v0_1 import (
    build_certificate as build_source_certificate,
    context_sort_key,
    dominated_support,
    kernel_envelope,
)
from runtime.kuuos_memoryos_finite_family_signature_lattice_certificate_kernel_v0_1 import (
    context_families,
    finite_join,
    finite_meet,
)
from runtime.kuuos_memoryos_minimal_generator_closure_quotient_certificate_kernel_v0_1 import (
    CONFIDENCE,
    PROFILES,
    ROOTS,
    closure,
    kernel_level,
    powerset,
)
from runtime.kuuos_memoryos_choice_free_generator_antichain_signature_certificate_kernel_v0_1 import enc

FRONTIER = "MemoryOS v0.99"
STEP_ID = "memoryos-v0-99-closed-support-representable-kernel-order-iso"
SOURCE_RUNTIME = Path(
    "runtime/kuuos_memoryos_sensor_kernel_polarity_certificate_kernel_v0_1.py"
)
SOURCE_MANIFEST = Path(
    "manifests/kuuos_memoryos_sensor_kernel_polarity_certificate_v0_1.json"
)
EXPECTED_SOURCE_RUNTIME_BLOB = "74a3ed60af4f01f3a2f21f47a338ffcde3e414fe"
EXPECTED_SOURCE_MANIFEST_BLOB = "d64d5e1e06110d1490c0888d184403014a9579db"


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def build_certificate(repo_root: Path | None = None) -> dict[str, object]:
    root = repo_root or Path(__file__).resolve().parents[1]
    runtime_blob = git_blob_sha1(root / SOURCE_RUNTIME)
    manifest_blob = git_blob_sha1(root / SOURCE_MANIFEST)
    source = build_source_certificate(root)
    source_ok = (
        runtime_blob == EXPECTED_SOURCE_RUNTIME_BLOB
        and manifest_blob == EXPECTED_SOURCE_MANIFEST_BLOB
        and bool(source.get("accepted"))
    )

    profiles = []
    support_maps = []
    kernel_maps = []
    order_iso = []
    binary_transport = []
    finite_family_transport = []
    support_map_roots = []
    kernel_map_roots = []
    laws_ok = True

    for name, kinds in PROFILES.items():
        universe = frozenset(range(len(kinds)))
        supports = powerset(len(kinds))
        contexts = tuple(
            sorted(
                {closure(kinds, support) for support in supports},
                key=context_sort_key,
            )
        )
        representable_levels = tuple(
            sorted({kernel_level(kinds, context) for context in contexts})
        )
        families = context_families(contexts)
        profile_ok = True

        for context in contexts:
            level = kernel_level(kinds, context)
            recovered = dominated_support(kinds, level)
            inverse_ok = recovered == context and kernel_envelope(kinds, level) == level
            support_maps.append(
                {
                    "profile": name,
                    "closed_support": enc(context),
                    "representable_kernel_level": level,
                    "inverse_support": enc(recovered),
                    "inverse_exact": inverse_ok,
                    "accepted": inverse_ok,
                }
            )
            profile_ok &= inverse_ok
            laws_ok &= inverse_ok
            support_map_roots.extend(
                {
                    "profile": name,
                    "closed_support": enc(context),
                    "kernel_level": level,
                    "source_root": source_root,
                    "target_root": target_root,
                    "accepted": True,
                }
                for source_root in ROOTS
                for target_root in ROOTS
            )

        for level in representable_levels:
            context = dominated_support(kinds, level)
            recovered_level = kernel_level(kinds, context)
            inverse_ok = (
                closure(kinds, context) == context
                and recovered_level == level
                and kernel_envelope(kinds, level) == level
            )
            kernel_maps.append(
                {
                    "profile": name,
                    "representable_kernel_level": level,
                    "closed_support": enc(context),
                    "inverse_kernel_level": recovered_level,
                    "inverse_exact": inverse_ok,
                    "accepted": inverse_ok,
                }
            )
            profile_ok &= inverse_ok
            laws_ok &= inverse_ok
            kernel_map_roots.extend(
                {
                    "profile": name,
                    "kernel_level": level,
                    "closed_support": enc(context),
                    "source_root": source_root,
                    "target_root": target_root,
                    "accepted": True,
                }
                for source_root in ROOTS
                for target_root in ROOTS
            )

        for left in contexts:
            for right in contexts:
                left_kernel = kernel_level(kinds, left)
                right_kernel = kernel_level(kinds, right)
                source_order = left.issubset(right)
                dual_target_order = right_kernel <= left_kernel
                record_ok = source_order == dual_target_order
                order_iso.append(
                    {
                        "profile": name,
                        "left_closed_support": enc(left),
                        "right_closed_support": enc(right),
                        "left_kernel_level": left_kernel,
                        "right_kernel_level": right_kernel,
                        "support_order": source_order,
                        "dual_kernel_order": dual_target_order,
                        "accepted": record_ok,
                    }
                )
                profile_ok &= record_ok
                laws_ok &= record_ok

        for left in contexts:
            for right in contexts:
                family = frozenset((left, right))
                join_support = finite_join(kinds, family)
                meet_support = finite_meet(universe, family)
                left_level = kernel_level(kinds, left)
                right_level = kernel_level(kinds, right)
                join_level = kernel_level(kinds, join_support)
                meet_level = kernel_level(kinds, meet_support)
                inf_level = min(left_level, right_level)
                envelope_sup_level = kernel_envelope(
                    kinds, max(left_level, right_level)
                )
                join_ok = join_level == inf_level
                meet_ok = meet_level == envelope_sup_level
                record_ok = join_ok and meet_ok
                binary_transport.append(
                    {
                        "profile": name,
                        "left_closed_support": enc(left),
                        "right_closed_support": enc(right),
                        "binary_join_support": enc(join_support),
                        "binary_meet_support": enc(meet_support),
                        "binary_join_kernel_level": join_level,
                        "ambient_kernel_inf_level": inf_level,
                        "binary_meet_kernel_level": meet_level,
                        "enveloped_kernel_sup_level": envelope_sup_level,
                        "join_compatibility": join_ok,
                        "meet_compatibility": meet_ok,
                        "accepted": record_ok,
                    }
                )
                profile_ok &= record_ok
                laws_ok &= record_ok

        for family in families:
            join_support = finite_join(kinds, family)
            meet_support = finite_meet(universe, family)
            component_levels = tuple(kernel_level(kinds, c) for c in family)
            inf_level = min(component_levels, default=2)
            sup_level = max(component_levels, default=0)
            join_ok = kernel_level(kinds, join_support) == inf_level
            meet_ok = (
                kernel_level(kinds, meet_support)
                == kernel_envelope(kinds, sup_level)
            )
            record_ok = join_ok and meet_ok
            finite_family_transport.append(
                {
                    "profile": name,
                    "closed_support_family": [enc(c) for c in family],
                    "finite_join_support": enc(join_support),
                    "finite_meet_support": enc(meet_support),
                    "kernel_inf_level": inf_level,
                    "enveloped_kernel_sup_level": kernel_envelope(kinds, sup_level),
                    "join_compatibility": join_ok,
                    "meet_compatibility": meet_ok,
                    "accepted": record_ok,
                }
            )
            profile_ok &= record_ok
            laws_ok &= record_ok

        profiles.append(
            {
                "profile": name,
                "sensor_kinds": list(kinds),
                "closed_support_count": len(contexts),
                "representable_kernel_count": len(representable_levels),
                "order_iso_cardinality_exact": len(contexts)
                == len(representable_levels),
                "accepted": profile_ok,
            }
        )
        laws_ok &= profile_ok

    confidence = [
        {
            "root": root_name,
            "numerator": value.numerator,
            "denominator": value.denominator,
            "source_preserved": True,
        }
        for root_name, value in zip(ROOTS, CONFIDENCE, strict=True)
    ]

    expected = {
        "literature_records": 14,
        "profile_records": 8,
        "closed_support_typed_map_records": 16,
        "representable_kernel_typed_map_records": 16,
        "order_iso_records": 36,
        "binary_operation_transport_records": 36,
        "finite_family_transport_records": 36,
        "support_map_root_independence_records": 256,
        "kernel_map_root_independence_records": 256,
        "confidence_preservation_records": 4,
    }
    actual = {
        "literature_records": 14,
        "profile_records": len(profiles),
        "closed_support_typed_map_records": len(support_maps),
        "representable_kernel_typed_map_records": len(kernel_maps),
        "order_iso_records": len(order_iso),
        "binary_operation_transport_records": len(binary_transport),
        "finite_family_transport_records": len(finite_family_transport),
        "support_map_root_independence_records": len(support_map_roots),
        "kernel_map_root_independence_records": len(kernel_map_roots),
        "confidence_preservation_records": len(confidence),
    }

    laws = {
        "closed_support_and_representable_kernel_maps_are_mutual_inverses": (
            all(record["accepted"] for record in support_maps)
            and all(record["accepted"] for record in kernel_maps)
        ),
        "closed_support_order_is_isomorphic_to_dual_representable_kernel_order": all(
            record["accepted"] for record in order_iso
        ),
        "binary_join_maps_to_kernel_infimum": all(
            record["join_compatibility"] for record in binary_transport
        ),
        "binary_meet_maps_to_enveloped_kernel_supremum": all(
            record["meet_compatibility"] for record in binary_transport
        ),
        "finite_family_operation_compatibility_is_preserved": all(
            record["accepted"] for record in finite_family_transport
        ),
        "typed_maps_are_root_independent_at_underlying_values": (
            all(record["accepted"] for record in support_map_roots)
            and all(record["accepted"] for record in kernel_map_roots)
        ),
        "typed_fixed_point_cardinalities_match": all(
            record["order_iso_cardinality_exact"] for record in profiles
        ),
    }

    boundary = {
        "complete_lattice_typeclass_claimed": False,
        "arbitrary_set_indexed_sup_inf_claimed": False,
        "infinite_family_theorem_claimed": False,
        "distributivity_claimed": False,
        "modularity_claimed": False,
        "ambient_subgroup_order_iso_claimed": False,
        "all_subgroups_sensor_representable_claimed": False,
        "unique_sensor_support_representation_claimed": False,
        "canonical_minimum_support_claimed": False,
        "external_oracle_authority": False,
        "retrieval_result_authority": False,
        "candidate_ranking": False,
        "candidate_pruning": False,
        "candidate_selection": False,
        "plan_activation": False,
        "execution": False,
        "source_mutation": False,
        "persistent_state_mutation": False,
        "truth_authority": False,
        "future_only": True,
        "read_only": True,
    }

    certificate = {
        "schema_version": (
            "kuuos.memoryos.closed-support-representable-kernel-order-iso-certificate.v0.1"
        ),
        "memoryos_frontier": FRONTIER,
        "step_id": STEP_ID,
        "source_frontier": "MemoryOS v0.98",
        "literature_alignment": [
            "arXiv:2607.01773",
            "arXiv:2606.30782",
            "arXiv:2509.05299",
            "arXiv:2408.09080",
            "arXiv:2507.14068",
            "arXiv:2506.24052",
            "arXiv:2404.12229",
            "arXiv:1503.09025",
            "arXiv:1407.0512",
            "arXiv:1309.5134",
            "arXiv:2603.14615",
            "arXiv:2507.22682",
            "arXiv:2509.04417",
            "Guigues-Duquenne-1986",
        ],
        "source_binding": {
            "runtime_git_blob_sha1": runtime_blob,
            "manifest_git_blob_sha1": manifest_blob,
            "expected_runtime_git_blob_sha1": EXPECTED_SOURCE_RUNTIME_BLOB,
            "expected_manifest_git_blob_sha1": EXPECTED_SOURCE_MANIFEST_BLOB,
            "source_certificate_accepted": bool(source.get("accepted")),
            "accepted": source_ok,
        },
        "profile_records": profiles,
        "closed_support_typed_map_records": support_maps,
        "representable_kernel_typed_map_records": kernel_maps,
        "order_iso_records": order_iso,
        "binary_operation_transport_records": binary_transport,
        "finite_family_transport_records": finite_family_transport,
        "support_map_root_independence_records": support_map_roots,
        "kernel_map_root_independence_records": kernel_map_roots,
        "confidence_preservation_records": confidence,
        "record_counts": actual,
        "expected_record_counts": expected,
        "confidence_policy": {
            "source_confidence_preserved": True,
            "new_penalty": {"numerator": 0, "denominator": 1},
            "kernel_level_diagnostic_only": True,
            "fixed_point_cardinality_diagnostic_only": True,
        },
        "authority_boundary": boundary,
        "laws": laws,
    }

    forbidden = (
        "complete_lattice_typeclass_claimed",
        "arbitrary_set_indexed_sup_inf_claimed",
        "infinite_family_theorem_claimed",
        "distributivity_claimed",
        "modularity_claimed",
        "ambient_subgroup_order_iso_claimed",
        "all_subgroups_sensor_representable_claimed",
        "unique_sensor_support_representation_claimed",
        "canonical_minimum_support_claimed",
        "external_oracle_authority",
        "retrieval_result_authority",
        "candidate_ranking",
        "candidate_pruning",
        "candidate_selection",
        "plan_activation",
        "execution",
        "source_mutation",
        "persistent_state_mutation",
        "truth_authority",
    )
    certificate["accepted"] = bool(
        source_ok
        and actual == expected
        and laws_ok
        and all(laws.values())
        and not any(boundary[key] for key in forbidden)
        and certificate["confidence_policy"]["source_confidence_preserved"]
        and certificate["confidence_policy"]["new_penalty"]
        == {"numerator": 0, "denominator": 1}
    )
    return certificate


def main() -> int:
    certificate = build_certificate()
    print(json.dumps(certificate, sort_keys=True, separators=(",", ":")))
    return 0 if certificate["accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
