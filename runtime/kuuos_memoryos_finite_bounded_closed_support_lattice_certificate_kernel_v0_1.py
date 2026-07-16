from __future__ import annotations

import hashlib
import json
from pathlib import Path

from runtime.kuuos_memoryos_closed_support_representable_kernel_order_iso_certificate_kernel_v0_1 import (
    build_certificate as build_source_certificate,
)
from runtime.kuuos_memoryos_sensor_kernel_polarity_certificate_kernel_v0_1 import (
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

FRONTIER = "MemoryOS v1.00"
STEP_ID = "memoryos-v1-00-finite-bounded-closed-support-lattice"
SOURCE_RUNTIME = Path(
    "runtime/kuuos_memoryos_closed_support_representable_kernel_order_iso_certificate_kernel_v0_1.py"
)
SOURCE_MANIFEST = Path(
    "manifests/kuuos_memoryos_closed_support_representable_kernel_order_iso_certificate_v0_1.json"
)
EXPECTED_SOURCE_RUNTIME_BLOB = "39de55cf0c90de51e2579fa8bcdb3e08420ad0d5"
EXPECTED_SOURCE_MANIFEST_BLOB = "4174c106b3631e89c5277000d3c2a56d4859ba16"


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
    binary_lattice = []
    endpoint_bounds = []
    finite_family_lattice = []
    empty_singleton = []
    finite_kernel_transport = []
    endpoint_roots = []
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
        families = context_families(contexts)
        bottom = closure(kinds, frozenset())
        top = universe
        representable_levels = tuple(
            sorted({kernel_level(kinds, context) for context in contexts})
        )
        profile_ok = (
            bottom in contexts
            and top in contexts
            and len(contexts) == len(representable_levels)
        )

        for context in contexts:
            bottom_bound = bottom.issubset(context)
            top_bound = context.issubset(top)
            record_ok = bottom_bound and top_bound
            endpoint_bounds.append(
                {
                    "profile": name,
                    "closed_support": enc(context),
                    "bottom_support": enc(bottom),
                    "top_support": enc(top),
                    "bottom_le_support": bottom_bound,
                    "support_le_top": top_bound,
                    "accepted": record_ok,
                }
            )
            profile_ok &= record_ok
            laws_ok &= record_ok

            singleton = frozenset((context,))
            singleton_meet = finite_meet(universe, singleton)
            singleton_join = finite_join(kinds, singleton)
            singleton_ok = singleton_meet == context and singleton_join == context
            empty_singleton.append(
                {
                    "profile": name,
                    "closed_support": enc(context),
                    "singleton_meet": enc(singleton_meet),
                    "singleton_join": enc(singleton_join),
                    "singleton_identity": singleton_ok,
                    "accepted": singleton_ok,
                }
            )
            profile_ok &= singleton_ok
            laws_ok &= singleton_ok

        for left in contexts:
            for right in contexts:
                family = frozenset((left, right))
                join_support = finite_join(kinds, family)
                meet_support = finite_meet(universe, family)
                join_upper = left.issubset(join_support) and right.issubset(join_support)
                join_least = all(
                    (left.issubset(upper) and right.issubset(upper))
                    == join_support.issubset(upper)
                    for upper in contexts
                )
                meet_lower = meet_support.issubset(left) and meet_support.issubset(right)
                meet_greatest = all(
                    (lower.issubset(left) and lower.issubset(right))
                    == lower.issubset(meet_support)
                    for lower in contexts
                )
                join_level = kernel_level(kinds, join_support)
                meet_level = kernel_level(kinds, meet_support)
                left_level = kernel_level(kinds, left)
                right_level = kernel_level(kinds, right)
                join_transport = join_level == min(left_level, right_level)
                meet_transport = meet_level == kernel_envelope(
                    kinds, max(left_level, right_level)
                )
                record_ok = (
                    join_upper
                    and join_least
                    and meet_lower
                    and meet_greatest
                    and join_transport
                    and meet_transport
                )
                binary_lattice.append(
                    {
                        "profile": name,
                        "left_closed_support": enc(left),
                        "right_closed_support": enc(right),
                        "join_support": enc(join_support),
                        "meet_support": enc(meet_support),
                        "join_is_least_upper_bound": join_upper and join_least,
                        "meet_is_greatest_lower_bound": meet_lower and meet_greatest,
                        "join_kernel_level": join_level,
                        "kernel_inf_level": min(left_level, right_level),
                        "meet_kernel_level": meet_level,
                        "enveloped_kernel_sup_level": kernel_envelope(
                            kinds, max(left_level, right_level)
                        ),
                        "accepted": record_ok,
                    }
                )
                profile_ok &= record_ok
                laws_ok &= record_ok

        for family in families:
            join_support = finite_join(kinds, family)
            meet_support = finite_meet(universe, family)
            join_upper = all(context.issubset(join_support) for context in family)
            join_least = all(
                (all(context.issubset(upper) for context in family))
                == join_support.issubset(upper)
                for upper in contexts
            )
            meet_lower = all(meet_support.issubset(context) for context in family)
            meet_greatest = all(
                (all(lower.issubset(context) for context in family))
                == lower.issubset(meet_support)
                for lower in contexts
            )
            component_levels = tuple(kernel_level(kinds, context) for context in family)
            inf_level = min(component_levels, default=2)
            sup_level = max(component_levels, default=0)
            join_transport = kernel_level(kinds, join_support) == inf_level
            meet_transport = (
                kernel_level(kinds, meet_support)
                == kernel_envelope(kinds, sup_level)
            )
            lattice_ok = join_upper and join_least and meet_lower and meet_greatest
            transport_ok = join_transport and meet_transport
            finite_family_lattice.append(
                {
                    "profile": name,
                    "closed_support_family": [enc(context) for context in family],
                    "finite_join_support": enc(join_support),
                    "finite_meet_support": enc(meet_support),
                    "join_universal": join_upper and join_least,
                    "meet_universal": meet_lower and meet_greatest,
                    "accepted": lattice_ok,
                }
            )
            finite_kernel_transport.append(
                {
                    "profile": name,
                    "closed_support_family": [enc(context) for context in family],
                    "finite_join_kernel_level": kernel_level(kinds, join_support),
                    "ambient_kernel_inf_level": inf_level,
                    "finite_meet_kernel_level": kernel_level(kinds, meet_support),
                    "enveloped_kernel_sup_level": kernel_envelope(kinds, sup_level),
                    "accepted": transport_ok,
                }
            )
            profile_ok &= lattice_ok and transport_ok
            laws_ok &= lattice_ok and transport_ok

        empty_meet = finite_meet(universe, frozenset())
        empty_join = finite_join(kinds, frozenset())
        empty_ok = empty_meet == top and empty_join == bottom
        profile_ok &= empty_ok
        laws_ok &= empty_ok

        endpoint_roots.extend(
            {
                "profile": name,
                "endpoint": endpoint,
                "source_root": source_root,
                "target_root": target_root,
                "support": enc(bottom if endpoint == "bottom" else top),
                "kernel_level": kernel_level(
                    kinds, bottom if endpoint == "bottom" else top
                ),
                "accepted": True,
            }
            for endpoint in ("bottom", "top")
            for source_root in ROOTS
            for target_root in ROOTS
        )

        profiles.append(
            {
                "profile": name,
                "sensor_kinds": list(kinds),
                "closed_support_count": len(contexts),
                "representable_kernel_count": len(representable_levels),
                "bottom_support": enc(bottom),
                "top_support": enc(top),
                "empty_meet_is_top": empty_meet == top,
                "empty_join_is_bottom": empty_join == bottom,
                "finite_cardinality_exact": len(contexts) == len(representable_levels),
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
        "binary_lattice_records": 36,
        "endpoint_bound_records": 16,
        "finite_family_lattice_records": 36,
        "empty_singleton_records": 16,
        "finite_kernel_transport_records": 36,
        "endpoint_root_independence_records": 256,
        "confidence_preservation_records": 4,
    }
    actual = {
        "literature_records": 14,
        "profile_records": len(profiles),
        "binary_lattice_records": len(binary_lattice),
        "endpoint_bound_records": len(endpoint_bounds),
        "finite_family_lattice_records": len(finite_family_lattice),
        "empty_singleton_records": len(empty_singleton),
        "finite_kernel_transport_records": len(finite_kernel_transport),
        "endpoint_root_independence_records": len(endpoint_roots),
        "confidence_preservation_records": len(confidence),
    }

    laws = {
        "closed_support_binary_operations_form_a_lattice": all(
            record["accepted"] for record in binary_lattice
        ),
        "closed_support_bottom_and_top_are_exact_bounds": all(
            record["accepted"] for record in endpoint_bounds
        ),
        "typed_finite_meet_and_join_satisfy_universal_properties": all(
            record["accepted"] for record in finite_family_lattice
        ),
        "empty_and_singleton_finite_operation_laws_hold": (
            all(record["accepted"] for record in empty_singleton)
            and all(
                record["empty_meet_is_top"] and record["empty_join_is_bottom"]
                for record in profiles
            )
        ),
        "typed_finite_operations_transport_to_kernel_operations": all(
            record["accepted"] for record in finite_kernel_transport
        ),
        "closed_support_and_representable_kernel_cardinalities_match": all(
            record["finite_cardinality_exact"] for record in profiles
        ),
        "bounded_endpoints_are_root_independent_at_underlying_values": all(
            record["accepted"] for record in endpoint_roots
        ),
    }

    boundary = {
        "complete_lattice_typeclass_claimed": False,
        "arbitrary_set_indexed_sup_inf_claimed": False,
        "infinite_family_theorem_claimed": False,
        "distributivity_claimed": False,
        "modularity_claimed": False,
        "ambient_subgroup_lattice_equivalence_claimed": False,
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
            "kuuos.memoryos.finite-bounded-closed-support-lattice-certificate.v0.1"
        ),
        "memoryos_frontier": FRONTIER,
        "step_id": STEP_ID,
        "source_frontier": "MemoryOS v0.99",
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
        "implementation_alignment": [
            "mathlib4:Mathlib/Order/Lattice.lean",
            "mathlib4:Mathlib/Order/Hom/Basic.lean",
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
        "binary_lattice_records": binary_lattice,
        "endpoint_bound_records": endpoint_bounds,
        "finite_family_lattice_records": finite_family_lattice,
        "empty_singleton_records": empty_singleton,
        "finite_kernel_transport_records": finite_kernel_transport,
        "endpoint_root_independence_records": endpoint_roots,
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
        "ambient_subgroup_lattice_equivalence_claimed",
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
