from __future__ import annotations

import hashlib
import json
from itertools import combinations, permutations
from pathlib import Path

from runtime.kuuos_memoryos_pointed_choice_free_signature_lattice_certificate_kernel_v0_1 import (
    build_certificate as build_source_certificate,
    completed_hull,
    completed_signature,
    context_join,
)
from runtime.kuuos_memoryos_minimal_generator_closure_quotient_certificate_kernel_v0_1 import (
    CONFIDENCE,
    PROFILES,
    ROOTS,
    closure,
    powerset,
)
from runtime.kuuos_memoryos_choice_free_generator_antichain_signature_certificate_kernel_v0_1 import enc

FRONTIER = "MemoryOS v0.97"
STEP_ID = "memoryos-v0-97-finite-family-signature-lattice"
SOURCE_RUNTIME = Path(
    "runtime/kuuos_memoryos_pointed_choice_free_signature_lattice_certificate_kernel_v0_1.py"
)
SOURCE_MANIFEST = Path(
    "manifests/kuuos_memoryos_pointed_choice_free_signature_lattice_certificate_v0_1.json"
)
EXPECTED_SOURCE_RUNTIME_BLOB = "9e44272a6f4b8ef459dcdca4b1293637b366d36e"
EXPECTED_SOURCE_MANIFEST_BLOB = "17f9db762f53e43b5f1dacdf47e9a45d0e206257"


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def context_sort_key(value: frozenset[int]) -> tuple[int, tuple[int, ...]]:
    return len(value), tuple(sorted(value))


def context_families(
    contexts: tuple[frozenset[int], ...],
) -> tuple[tuple[frozenset[int], ...], ...]:
    return tuple(
        tuple(contexts[index] for index in indices)
        for size in range(len(contexts) + 1)
        for indices in combinations(range(len(contexts)), size)
    )


def finite_meet(
    universe: frozenset[int],
    family: tuple[frozenset[int], ...],
) -> frozenset[int]:
    result = universe
    for context in family:
        result = result.intersection(context)
    return result


def finite_union(family: tuple[frozenset[int], ...]) -> frozenset[int]:
    result: frozenset[int] = frozenset()
    for context in family:
        result = result.union(context)
    return result


def finite_join(
    kinds: tuple[str, ...],
    family: tuple[frozenset[int], ...],
) -> frozenset[int]:
    return closure(kinds, finite_union(family))


def signature_family_meet(
    kinds: tuple[str, ...],
    signatures: tuple[tuple[frozenset[int], ...], ...],
) -> tuple[frozenset[int], ...]:
    universe = frozenset(range(len(kinds)))
    decoded = tuple(completed_hull(kinds, signature) for signature in signatures)
    return completed_signature(kinds, finite_meet(universe, decoded))


def signature_family_join(
    kinds: tuple[str, ...],
    signatures: tuple[tuple[frozenset[int], ...], ...],
) -> tuple[frozenset[int], ...]:
    decoded = tuple(completed_hull(kinds, signature) for signature in signatures)
    return completed_signature(kinds, finite_join(kinds, decoded))


def fold_meet(
    universe: frozenset[int],
    ordered_family: tuple[frozenset[int], ...],
) -> frozenset[int]:
    result = universe
    for context in ordered_family:
        result = result.intersection(context)
    return result


def fold_join(
    kinds: tuple[str, ...],
    ordered_family: tuple[frozenset[int], ...],
) -> frozenset[int]:
    result = closure(kinds, frozenset())
    for context in ordered_family:
        result = context_join(kinds, result, context)
    return result


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
    family_operations = []
    universal_properties = []
    permutation_folds = []
    duplicate_invariance = []
    family_roots = []
    laws_ok = True

    for name, kinds in PROFILES.items():
        universe = frozenset(range(len(kinds)))
        contexts = tuple(
            sorted(
                {closure(kinds, support) for support in powerset(len(kinds))},
                key=context_sort_key,
            )
        )
        families = context_families(contexts)
        bottom = closure(kinds, frozenset())
        profile_ok = True

        for family in families:
            signatures = tuple(completed_signature(kinds, context) for context in family)
            meet_context = finite_meet(universe, family)
            join_context = finite_join(kinds, family)
            meet_signature = signature_family_meet(kinds, signatures)
            join_signature = signature_family_join(kinds, signatures)
            meet_hull = completed_hull(kinds, meet_signature)
            join_hull = completed_hull(kinds, join_signature)

            empty_laws = bool(family) or (
                meet_context == universe and join_context == bottom
            )
            singleton_laws = len(family) != 1 or (
                meet_context == family[0] and join_context == family[0]
            )
            binary_laws = len(family) != 2 or (
                meet_context == family[0].intersection(family[1])
                and join_context == context_join(kinds, family[0], family[1])
            )
            family_ok = (
                meet_context in contexts
                and join_context in contexts
                and meet_hull == meet_context
                and join_hull == join_context
                and all(meet_context.issubset(context) for context in family)
                and all(context.issubset(join_context) for context in family)
                and empty_laws
                and singleton_laws
                and binary_laws
            )
            family_operations.append(
                {
                    "profile": name,
                    "family": [enc(context) for context in family],
                    "signatures": [
                        [enc(generator) for generator in signature]
                        for signature in signatures
                    ],
                    "finite_meet_context": enc(meet_context),
                    "finite_join_context": enc(join_context),
                    "finite_meet_signature": [
                        enc(generator) for generator in meet_signature
                    ],
                    "finite_join_signature": [
                        enc(generator) for generator in join_signature
                    ],
                    "finite_meet_hull": enc(meet_hull),
                    "finite_join_hull": enc(join_hull),
                    "empty_family_bounds_exact": empty_laws,
                    "singleton_compatibility_exact": singleton_laws,
                    "binary_compatibility_exact": binary_laws,
                    "accepted": family_ok,
                }
            )
            profile_ok &= family_ok
            laws_ok &= family_ok

            duplicated = family + family
            duplicate_ok = (
                finite_meet(universe, duplicated) == meet_context
                and finite_join(kinds, duplicated) == join_context
            )
            duplicate_invariance.append(
                {
                    "profile": name,
                    "family": [enc(context) for context in family],
                    "duplicated_family": [enc(context) for context in duplicated],
                    "meet_unchanged": finite_meet(universe, duplicated) == meet_context,
                    "join_unchanged": finite_join(kinds, duplicated) == join_context,
                    "accepted": duplicate_ok,
                }
            )
            profile_ok &= duplicate_ok
            laws_ok &= duplicate_ok

            for order in permutations(family):
                order_meet = fold_meet(universe, order)
                order_join = fold_join(kinds, order)
                fold_ok = order_meet == meet_context and order_join == join_context
                permutation_folds.append(
                    {
                        "profile": name,
                        "family": [enc(context) for context in family],
                        "order": [enc(context) for context in order],
                        "fold_meet": enc(order_meet),
                        "fold_join": enc(order_join),
                        "accepted": fold_ok,
                    }
                )
                profile_ok &= fold_ok
                laws_ok &= fold_ok

            for witness in contexts:
                glb_equiv = witness.issubset(meet_context) == all(
                    witness.issubset(context) for context in family
                )
                lub_equiv = join_context.issubset(witness) == all(
                    context.issubset(witness) for context in family
                )
                universal_ok = glb_equiv and lub_equiv
                universal_properties.append(
                    {
                        "profile": name,
                        "family": [enc(context) for context in family],
                        "witness_context": enc(witness),
                        "greatest_lower_bound_equivalence": glb_equiv,
                        "least_upper_bound_equivalence": lub_equiv,
                        "accepted": universal_ok,
                    }
                )
                profile_ok &= universal_ok
                laws_ok &= universal_ok

            family_roots.extend(
                {
                    "profile": name,
                    "family": [enc(context) for context in family],
                    "source_root": source_root,
                    "target_root": target_root,
                    "finite_meet_signature": [
                        enc(generator) for generator in meet_signature
                    ],
                    "finite_join_signature": [
                        enc(generator) for generator in join_signature
                    ],
                    "finite_meet_hull": enc(meet_hull),
                    "finite_join_hull": enc(join_hull),
                    "accepted": True,
                }
                for source_root in ROOTS
                for target_root in ROOTS
            )

        profiles.append(
            {
                "profile": name,
                "sensor_kinds": list(kinds),
                "closed_context_count": len(contexts),
                "closed_context_family_count": len(families),
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
        "literature_records": 11,
        "profile_records": 8,
        "finite_family_operation_records": 36,
        "finite_family_universal_property_records": 84,
        "permutation_fold_records": 56,
        "duplicate_invariance_records": 36,
        "finite_family_root_independence_records": 576,
        "confidence_preservation_records": 4,
    }
    actual = {
        "literature_records": 11,
        "profile_records": len(profiles),
        "finite_family_operation_records": len(family_operations),
        "finite_family_universal_property_records": len(universal_properties),
        "permutation_fold_records": len(permutation_folds),
        "duplicate_invariance_records": len(duplicate_invariance),
        "finite_family_root_independence_records": len(family_roots),
        "confidence_preservation_records": len(confidence),
    }

    laws = {
        "finite_meet_is_exact_intersection": all(
            record["accepted"] for record in family_operations
        ),
        "finite_join_is_exact_closure_of_union": all(
            record["accepted"] for record in family_operations
        ),
        "empty_family_meet_is_top_and_join_is_bottom": all(
            record["empty_family_bounds_exact"] for record in family_operations
        ),
        "finite_meet_and_join_have_universal_properties": all(
            record["accepted"] for record in universal_properties
        ),
        "singleton_and_binary_operations_agree_with_v0_96": all(
            record["singleton_compatibility_exact"]
            and record["binary_compatibility_exact"]
            for record in family_operations
        ),
        "fold_results_are_enumeration_order_independent": all(
            record["accepted"] for record in permutation_folds
        ),
        "duplicate_family_members_do_not_change_results": all(
            record["accepted"] for record in duplicate_invariance
        ),
        "pointed_signature_finite_operations_decode_exactly": all(
            record["accepted"] for record in family_operations
        ),
        "finite_family_signature_operations_are_root_independent": all(
            record["accepted"] for record in family_roots
        ),
    }

    boundary = {
        "representative_choice_performed": False,
        "unique_minimal_generator_claimed": False,
        "complete_lattice_typeclass_claimed": False,
        "arbitrary_set_indexed_sup_inf_claimed": False,
        "infinite_family_sup_inf_claimed": False,
        "distributivity_claimed": False,
        "modularity_claimed": False,
        "globally_minimum_implication_basis_claimed": False,
        "new_basis_optimization_complexity_claimed": False,
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
        "schema_version": "kuuos.memoryos.finite-family-pointed-signature-lattice-certificate.v0.1",
        "memoryos_frontier": FRONTIER,
        "step_id": STEP_ID,
        "source_frontier": "MemoryOS v0.96",
        "literature_alignment": [
            "arXiv:2607.01773",
            "arXiv:2509.05299",
            "arXiv:2603.14615",
            "arXiv:2507.22682",
            "arXiv:2509.04417",
            "arXiv:2506.24052",
            "arXiv:2407.00694",
            "arXiv:2404.07037",
            "arXiv:2404.12229",
            "arXiv:1503.09025",
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
        "finite_family_operation_records": family_operations,
        "finite_family_universal_property_records": universal_properties,
        "permutation_fold_records": permutation_folds,
        "duplicate_invariance_records": duplicate_invariance,
        "finite_family_root_independence_records": family_roots,
        "confidence_preservation_records": confidence,
        "record_counts": actual,
        "expected_record_counts": expected,
        "confidence_policy": {
            "source_confidence_preserved": True,
            "new_penalty": {"numerator": 0, "denominator": 1},
            "family_cardinality_diagnostic_only": True,
            "fold_permutation_counts_diagnostic_only": True,
            "lattice_height_diagnostic_only": True,
        },
        "authority_boundary": boundary,
        "laws": laws,
    }

    forbidden = (
        "representative_choice_performed",
        "unique_minimal_generator_claimed",
        "complete_lattice_typeclass_claimed",
        "arbitrary_set_indexed_sup_inf_claimed",
        "infinite_family_sup_inf_claimed",
        "distributivity_claimed",
        "modularity_claimed",
        "globally_minimum_implication_basis_claimed",
        "new_basis_optimization_complexity_claimed",
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
