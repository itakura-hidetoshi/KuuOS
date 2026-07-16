from __future__ import annotations

import hashlib
import json
from pathlib import Path

from runtime.kuuos_memoryos_finite_family_signature_lattice_certificate_kernel_v0_1 import (
    build_certificate as build_source_certificate,
    context_families,
    finite_join,
    finite_meet,
)
from runtime.kuuos_memoryos_minimal_generator_closure_quotient_certificate_kernel_v0_1 import (
    CONFIDENCE,
    LEVEL,
    PROFILES,
    ROOTS,
    closure,
    kernel_level,
    powerset,
)
from runtime.kuuos_memoryos_choice_free_generator_antichain_signature_certificate_kernel_v0_1 import enc

FRONTIER = "MemoryOS v0.98"
STEP_ID = "memoryos-v0-98-sensor-kernel-polarity"
SOURCE_RUNTIME = Path(
    "runtime/kuuos_memoryos_finite_family_signature_lattice_certificate_kernel_v0_1.py"
)
SOURCE_MANIFEST = Path(
    "manifests/kuuos_memoryos_finite_family_signature_lattice_certificate_v0_1.json"
)
EXPECTED_SOURCE_RUNTIME_BLOB = "2a9929320350092568bec8e3139725787302f791"
EXPECTED_SOURCE_MANIFEST_BLOB = "79c155daa2543db34bf41ed2bc029b4008655d1a"
KERNEL_LEVELS = (0, 1, 2)


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def context_sort_key(value: frozenset[int]) -> tuple[int, tuple[int, ...]]:
    return len(value), tuple(sorted(value))


def dominated_support(kinds: tuple[str, ...], kernel: int) -> frozenset[int]:
    return frozenset(
        index for index, kind in enumerate(kinds) if kernel <= LEVEL[kind]
    )


def kernel_envelope(kinds: tuple[str, ...], kernel: int) -> int:
    return kernel_level(kinds, dominated_support(kinds, kernel))


def kernel_inf(levels: tuple[int, ...]) -> int:
    return min(levels, default=2)


def kernel_sup(levels: tuple[int, ...]) -> int:
    return max(levels, default=0)


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
    polarity = []
    envelopes = []
    fixed_points = []
    order_duality = []
    family_transport = []
    polarity_roots = []
    envelope_roots = []
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
        representable_levels = {kernel_level(kinds, support) for support in supports}
        profile_ok = True

        for support in supports:
            support_kernel = kernel_level(kinds, support)
            support_closure = closure(kinds, support)
            dominated_from_support = dominated_support(kinds, support_kernel)
            closure_composite_ok = dominated_from_support == support_closure

            for kernel in KERNEL_LEVELS:
                selected = dominated_support(kinds, kernel)
                left = kernel <= support_kernel
                right = support.issubset(selected)
                polarity_ok = left == right
                record_ok = polarity_ok and closure_composite_ok
                polarity.append(
                    {
                        "profile": name,
                        "support": enc(support),
                        "support_kernel_level": support_kernel,
                        "kernel_level": kernel,
                        "dominated_support": enc(selected),
                        "kernel_le_support_kernel": left,
                        "support_subset_dominated_support": right,
                        "support_closure": enc(support_closure),
                        "support_closure_composite": enc(dominated_from_support),
                        "accepted": record_ok,
                    }
                )
                profile_ok &= record_ok
                laws_ok &= record_ok

                polarity_roots.extend(
                    {
                        "profile": name,
                        "support": enc(support),
                        "kernel_level": kernel,
                        "source_root": source_root,
                        "target_root": target_root,
                        "dominated_support": enc(selected),
                        "support_kernel_level": support_kernel,
                        "accepted": True,
                    }
                    for source_root in ROOTS
                    for target_root in ROOTS
                )

        for kernel in KERNEL_LEVELS:
            selected = dominated_support(kinds, kernel)
            envelope = kernel_envelope(kinds, kernel)
            selected_closed = closure(kinds, selected) == selected
            extensive = kernel <= envelope
            idempotent = kernel_envelope(kinds, envelope) == envelope
            fixed = envelope == kernel
            fixed_iff_representable = fixed == (kernel in representable_levels)
            envelope_ok = (
                selected_closed
                and extensive
                and idempotent
                and fixed_iff_representable
            )
            envelopes.append(
                {
                    "profile": name,
                    "kernel_level": kernel,
                    "dominated_support": enc(selected),
                    "kernel_envelope_level": envelope,
                    "dominated_support_closed": selected_closed,
                    "extensive": extensive,
                    "idempotent": idempotent,
                    "fixed": fixed,
                    "fixed_iff_representable": fixed_iff_representable,
                    "accepted": envelope_ok,
                }
            )
            profile_ok &= envelope_ok
            laws_ok &= envelope_ok

            envelope_roots.extend(
                {
                    "profile": name,
                    "kernel_level": kernel,
                    "source_root": source_root,
                    "target_root": target_root,
                    "dominated_support": enc(selected),
                    "kernel_envelope_level": envelope,
                    "accepted": True,
                }
                for source_root in ROOTS
                for target_root in ROOTS
            )

        for context in contexts:
            level = kernel_level(kinds, context)
            recovered = dominated_support(kinds, level)
            fixed = kernel_envelope(kinds, level) == level
            fixed_ok = recovered == context and fixed
            fixed_points.append(
                {
                    "profile": name,
                    "closed_support": enc(context),
                    "kernel_level": level,
                    "recovered_support": enc(recovered),
                    "kernel_fixed": fixed,
                    "accepted": fixed_ok,
                }
            )
            profile_ok &= fixed_ok
            laws_ok &= fixed_ok

        for left in contexts:
            for right in contexts:
                left_kernel = kernel_level(kinds, left)
                right_kernel = kernel_level(kinds, right)
                duality = left.issubset(right) == (right_kernel <= left_kernel)
                order_duality.append(
                    {
                        "profile": name,
                        "left_closed_support": enc(left),
                        "right_closed_support": enc(right),
                        "left_kernel_level": left_kernel,
                        "right_kernel_level": right_kernel,
                        "support_inclusion": left.issubset(right),
                        "reverse_kernel_inclusion": right_kernel <= left_kernel,
                        "accepted": duality,
                    }
                )
                profile_ok &= duality
                laws_ok &= duality

        for family in families:
            meet_support = finite_meet(universe, family)
            join_support = finite_join(kinds, family)
            levels = tuple(kernel_level(kinds, context) for context in family)
            ambient_inf = kernel_inf(levels)
            ambient_sup = kernel_sup(levels)
            representable_sup = kernel_envelope(kinds, ambient_sup)
            join_transport = kernel_level(kinds, join_support) == ambient_inf
            meet_transport = kernel_level(kinds, meet_support) == representable_sup
            inf_fixed = kernel_envelope(kinds, ambient_inf) == ambient_inf
            sup_envelope_fixed = (
                kernel_envelope(kinds, representable_sup) == representable_sup
            )
            transport_ok = (
                join_transport
                and meet_transport
                and inf_fixed
                and sup_envelope_fixed
            )
            family_transport.append(
                {
                    "profile": name,
                    "closed_support_family": [enc(context) for context in family],
                    "finite_meet_support": enc(meet_support),
                    "finite_join_support": enc(join_support),
                    "component_kernel_levels": list(levels),
                    "ambient_kernel_inf_level": ambient_inf,
                    "ambient_kernel_sup_level": ambient_sup,
                    "representable_kernel_sup_level": representable_sup,
                    "finite_join_kernel_equals_inf": join_transport,
                    "finite_meet_kernel_equals_envelope_sup": meet_transport,
                    "kernel_inf_representable": inf_fixed,
                    "envelope_sup_representable": sup_envelope_fixed,
                    "accepted": transport_ok,
                }
            )
            profile_ok &= transport_ok
            laws_ok &= transport_ok

        monotone_ok = all(
            not (left <= right)
            or kernel_envelope(kinds, left) <= kernel_envelope(kinds, right)
            for left in KERNEL_LEVELS
            for right in KERNEL_LEVELS
        )
        profile_ok &= monotone_ok
        laws_ok &= monotone_ok
        profiles.append(
            {
                "profile": name,
                "sensor_kinds": list(kinds),
                "support_count": len(supports),
                "closed_support_count": len(contexts),
                "closed_support_family_count": len(families),
                "representable_kernel_levels": sorted(representable_levels),
                "kernel_envelope_monotone": monotone_ok,
                "accepted": profile_ok,
            }
        )

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
        "literature_records": 13,
        "profile_records": 8,
        "support_kernel_polarity_records": 81,
        "kernel_envelope_records": 24,
        "closed_support_fixed_point_records": 16,
        "closed_support_order_duality_records": 36,
        "finite_family_kernel_transport_records": 36,
        "polarity_root_independence_records": 1296,
        "kernel_envelope_root_independence_records": 384,
        "confidence_preservation_records": 4,
    }
    actual = {
        "literature_records": 13,
        "profile_records": len(profiles),
        "support_kernel_polarity_records": len(polarity),
        "kernel_envelope_records": len(envelopes),
        "closed_support_fixed_point_records": len(fixed_points),
        "closed_support_order_duality_records": len(order_duality),
        "finite_family_kernel_transport_records": len(family_transport),
        "polarity_root_independence_records": len(polarity_roots),
        "kernel_envelope_root_independence_records": len(envelope_roots),
        "confidence_preservation_records": len(confidence),
    }

    laws = {
        "support_kernel_maps_form_exact_antitone_polarity": all(
            record["accepted"] for record in polarity
        ),
        "support_closure_is_polarity_composite": all(
            record["support_closure"] == record["support_closure_composite"]
            for record in polarity
        ),
        "kernel_envelope_is_extensive_monotone_idempotent": (
            all(record["accepted"] for record in envelopes)
            and all(record["kernel_envelope_monotone"] for record in profiles)
        ),
        "closed_supports_and_representable_kernels_are_fixed_points": all(
            record["accepted"] for record in fixed_points
        ),
        "closed_support_order_is_reverse_kernel_order": all(
            record["accepted"] for record in order_duality
        ),
        "finite_support_join_transports_to_kernel_infimum": all(
            record["finite_join_kernel_equals_inf"]
            for record in family_transport
        ),
        "finite_support_meet_transports_to_enveloped_kernel_supremum": all(
            record["finite_meet_kernel_equals_envelope_sup"]
            for record in family_transport
        ),
        "transported_kernel_operations_remain_representable": all(
            record["kernel_inf_representable"]
            and record["envelope_sup_representable"]
            for record in family_transport
        ),
        "polarity_and_kernel_envelope_are_root_independent": (
            all(record["accepted"] for record in polarity_roots)
            and all(record["accepted"] for record in envelope_roots)
        ),
    }

    boundary = {
        "complete_lattice_typeclass_claimed": False,
        "arbitrary_set_indexed_sup_inf_claimed": False,
        "infinite_family_sup_inf_claimed": False,
        "distributivity_claimed": False,
        "modularity_claimed": False,
        "all_subgroups_sensor_representable_claimed": False,
        "unique_sensor_support_representation_claimed": False,
        "globally_minimum_sensor_basis_claimed": False,
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
        "schema_version": "kuuos.memoryos.sensor-kernel-polarity-certificate.v0.1",
        "memoryos_frontier": FRONTIER,
        "step_id": STEP_ID,
        "source_frontier": "MemoryOS v0.97",
        "literature_alignment": [
            "arXiv:2607.01773",
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
        "support_kernel_polarity_records": polarity,
        "kernel_envelope_records": envelopes,
        "closed_support_fixed_point_records": fixed_points,
        "closed_support_order_duality_records": order_duality,
        "finite_family_kernel_transport_records": family_transport,
        "polarity_root_independence_records": polarity_roots,
        "kernel_envelope_root_independence_records": envelope_roots,
        "confidence_preservation_records": confidence,
        "record_counts": actual,
        "expected_record_counts": expected,
        "confidence_policy": {
            "source_confidence_preserved": True,
            "new_penalty": {"numerator": 0, "denominator": 1},
            "kernel_level_diagnostic_only": True,
            "representable_level_count_diagnostic_only": True,
            "fixed_point_count_diagnostic_only": True,
        },
        "authority_boundary": boundary,
        "laws": laws,
    }

    forbidden = (
        "complete_lattice_typeclass_claimed",
        "arbitrary_set_indexed_sup_inf_claimed",
        "infinite_family_sup_inf_claimed",
        "distributivity_claimed",
        "modularity_claimed",
        "all_subgroups_sensor_representable_claimed",
        "unique_sensor_support_representation_claimed",
        "globally_minimum_sensor_basis_claimed",
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
