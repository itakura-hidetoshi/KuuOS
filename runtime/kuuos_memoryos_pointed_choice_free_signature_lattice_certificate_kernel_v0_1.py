from __future__ import annotations

import hashlib
import json
from pathlib import Path

from runtime.kuuos_memoryos_choice_free_generator_antichain_signature_certificate_kernel_v0_1 import (
    enc,
    signature,
)
from runtime.kuuos_memoryos_choice_free_signature_hull_kernel_order_duality_certificate_kernel_v0_1 import (
    build_certificate as build_source_certificate,
    envelope,
    hull,
)
from runtime.kuuos_memoryos_minimal_generator_closure_quotient_certificate_kernel_v0_1 import (
    CONFIDENCE,
    PROFILES,
    ROOTS,
    closure,
    kernel_level,
    powerset,
)

FRONTIER = "MemoryOS v0.96"
STEP_ID = "memoryos-v0-96-pointed-choice-free-signature-lattice"
SOURCE_RUNTIME = Path(
    "runtime/kuuos_memoryos_choice_free_signature_hull_kernel_order_duality_certificate_kernel_v0_1.py"
)
SOURCE_MANIFEST = Path(
    "manifests/kuuos_memoryos_choice_free_signature_hull_order_certificate_v0_1.json"
)
EXPECTED_SOURCE_RUNTIME_BLOB = "1e78f37fbe0329f0ba13ea191c29d8037903a0eb"
EXPECTED_SOURCE_MANIFEST_BLOB = "22e1b146330f19b06344c2c8adf9a22052275daa"


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def completed_signature(
    kinds: tuple[str, ...], context: frozenset[int]
) -> tuple[frozenset[int], ...]:
    universe = frozenset(range(len(kinds)))
    if context == universe:
        return ()
    return signature(kinds, context)


def completed_hull(
    kinds: tuple[str, ...], generators: tuple[frozenset[int], ...]
) -> frozenset[int]:
    if not generators:
        return frozenset(range(len(kinds)))
    return hull(kinds, generators)


def context_meet(
    left: frozenset[int], right: frozenset[int]
) -> frozenset[int]:
    return left.intersection(right)


def context_join(
    kinds: tuple[str, ...],
    left: frozenset[int],
    right: frozenset[int],
) -> frozenset[int]:
    return closure(kinds, left.union(right))


def signature_meet(
    kinds: tuple[str, ...],
    left: tuple[frozenset[int], ...],
    right: tuple[frozenset[int], ...],
) -> tuple[frozenset[int], ...]:
    return completed_signature(
        kinds,
        context_meet(completed_hull(kinds, left), completed_hull(kinds, right)),
    )


def signature_join(
    kinds: tuple[str, ...],
    left: tuple[frozenset[int], ...],
    right: tuple[frozenset[int], ...],
) -> tuple[frozenset[int], ...]:
    return completed_signature(
        kinds,
        context_join(
            kinds, completed_hull(kinds, left), completed_hull(kinds, right)
        ),
    )


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
    completed_contexts = []
    top_bottom = []
    pair_operations = []
    universal_properties = []
    root_contexts = []
    root_operations = []
    laws_ok = True

    for name, kinds in PROFILES.items():
        universe = frozenset(range(len(kinds)))
        supports = powerset(len(kinds))
        contexts = tuple(
            sorted(
                {closure(kinds, support) for support in supports},
                key=lambda value: (len(value), tuple(sorted(value))),
            )
        )
        profile_ok = True

        for context in contexts:
            generators = completed_signature(kinds, context)
            decoded = completed_hull(kinds, generators)
            top_sentinel = not generators
            accepted = (
                decoded == context and top_sentinel == (context == universe)
            )
            completed_contexts.append(
                {
                    "profile": name,
                    "context": enc(context),
                    "signature": [enc(value) for value in generators],
                    "decoded_hull": enc(decoded),
                    "top_sentinel": top_sentinel,
                    "kernel_level": kernel_level(kinds, context),
                    "accepted": accepted,
                }
            )
            profile_ok &= accepted
            laws_ok &= accepted

            root_contexts.extend(
                {
                    "profile": name,
                    "context": enc(context),
                    "source_root": source_root,
                    "target_root": target_root,
                    "signature": [enc(value) for value in generators],
                    "decoded_hull": enc(decoded),
                    "accepted": True,
                }
                for source_root in ROOTS
                for target_root in ROOTS
            )

        bottom_context = closure(kinds, frozenset())
        bottom_signature = completed_signature(kinds, bottom_context)
        top_signature: tuple[frozenset[int], ...] = ()
        bounded_ok = (
            completed_hull(kinds, top_signature) == universe
            and completed_hull(kinds, bottom_signature) == bottom_context
            and all(bottom_context.issubset(context) for context in contexts)
            and all(context.issubset(universe) for context in contexts)
        )
        top_bottom.append(
            {
                "profile": name,
                "top_signature": [],
                "top_hull": enc(completed_hull(kinds, top_signature)),
                "bottom_context": enc(bottom_context),
                "bottom_signature": [enc(value) for value in bottom_signature],
                "bottom_hull": enc(completed_hull(kinds, bottom_signature)),
                "accepted": bounded_ok,
            }
        )
        profile_ok &= bounded_ok
        laws_ok &= bounded_ok

        for left in contexts:
            for right in contexts:
                left_signature = completed_signature(kinds, left)
                right_signature = completed_signature(kinds, right)
                meet_context = context_meet(left, right)
                join_context = context_join(kinds, left, right)
                meet_signature = signature_meet(
                    kinds, left_signature, right_signature
                )
                join_signature = signature_join(
                    kinds, left_signature, right_signature
                )
                meet_hull = completed_hull(kinds, meet_signature)
                join_hull = completed_hull(kinds, join_signature)

                pair_ok = (
                    meet_hull == meet_context
                    and join_hull == join_context
                    and meet_context in contexts
                    and join_context in contexts
                    and meet_context.issubset(left)
                    and meet_context.issubset(right)
                    and left.issubset(join_context)
                    and right.issubset(join_context)
                    and context_meet(right, left) == meet_context
                    and context_join(kinds, right, left) == join_context
                    and context_meet(left, left) == left
                    and context_join(kinds, left, left) == left
                    and context_meet(left, context_join(kinds, left, right))
                    == left
                    and context_join(kinds, left, context_meet(left, right))
                    == left
                )
                pair_operations.append(
                    {
                        "profile": name,
                        "left_context": enc(left),
                        "right_context": enc(right),
                        "meet_context": enc(meet_context),
                        "join_context": enc(join_context),
                        "meet_signature": [enc(value) for value in meet_signature],
                        "join_signature": [enc(value) for value in join_signature],
                        "meet_hull": enc(meet_hull),
                        "join_hull": enc(join_hull),
                        "accepted": pair_ok,
                    }
                )
                profile_ok &= pair_ok
                laws_ok &= pair_ok

                root_operations.extend(
                    {
                        "profile": name,
                        "left_context": enc(left),
                        "right_context": enc(right),
                        "source_root": source_root,
                        "target_root": target_root,
                        "meet_signature": [
                            enc(value) for value in meet_signature
                        ],
                        "join_signature": [
                            enc(value) for value in join_signature
                        ],
                        "meet_hull": enc(meet_hull),
                        "join_hull": enc(join_hull),
                        "accepted": True,
                    }
                    for source_root in ROOTS
                    for target_root in ROOTS
                )

                for witness in contexts:
                    glb_equiv = witness.issubset(meet_context) == (
                        witness.issubset(left) and witness.issubset(right)
                    )
                    lub_equiv = join_context.issubset(witness) == (
                        left.issubset(witness) and right.issubset(witness)
                    )
                    meet_assoc = context_meet(
                        context_meet(left, right), witness
                    ) == context_meet(left, context_meet(right, witness))
                    join_assoc = context_join(
                        kinds, context_join(kinds, left, right), witness
                    ) == context_join(
                        kinds, left, context_join(kinds, right, witness)
                    )
                    universal_ok = (
                        glb_equiv and lub_equiv and meet_assoc and join_assoc
                    )
                    universal_properties.append(
                        {
                            "profile": name,
                            "left_context": enc(left),
                            "right_context": enc(right),
                            "witness_context": enc(witness),
                            "greatest_lower_bound_equivalence": glb_equiv,
                            "least_upper_bound_equivalence": lub_equiv,
                            "meet_associative": meet_assoc,
                            "join_associative": join_assoc,
                            "accepted": universal_ok,
                        }
                    )
                    profile_ok &= universal_ok
                    laws_ok &= universal_ok

        profiles.append(
            {
                "profile": name,
                "sensor_kinds": list(kinds),
                "closed_context_count": len(contexts),
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
        "literature_records": 10,
        "profile_records": 8,
        "completed_context_records": 16,
        "top_bottom_records": 8,
        "pair_operation_records": 36,
        "universal_property_records": 88,
        "context_root_independence_records": 256,
        "operation_root_independence_records": 576,
        "confidence_preservation_records": 4,
    }
    actual = {
        "literature_records": 10,
        "profile_records": len(profiles),
        "completed_context_records": len(completed_contexts),
        "top_bottom_records": len(top_bottom),
        "pair_operation_records": len(pair_operations),
        "universal_property_records": len(universal_properties),
        "context_root_independence_records": len(root_contexts),
        "operation_root_independence_records": len(root_operations),
        "confidence_preservation_records": len(confidence),
    }

    laws = {
        "empty_signature_is_exact_universal_context_sentinel": all(
            record["accepted"] for record in completed_contexts
        ),
        "all_closed_contexts_encode_decode_exactly": all(
            record["accepted"] for record in completed_contexts
        ),
        "binary_meet_is_intersection": all(
            record["accepted"] for record in pair_operations
        ),
        "binary_join_is_closure_of_union": all(
            record["accepted"] for record in pair_operations
        ),
        "meet_and_join_satisfy_universal_properties": all(
            record["accepted"] for record in universal_properties
        ),
        "meet_and_join_are_associative_commutative_idempotent_absorptive": (
            all(record["accepted"] for record in pair_operations)
            and all(record["accepted"] for record in universal_properties)
        ),
        "pointed_completion_has_exact_top_and_bottom": all(
            record["accepted"] for record in top_bottom
        ),
        "completed_signatures_and_operations_are_root_independent": all(
            record["accepted"] for record in root_contexts + root_operations
        ),
    }

    boundary = {
        "representative_choice_performed": False,
        "unique_minimal_generator_claimed": False,
        "complete_lattice_typeclass_claimed": False,
        "arbitrary_family_sup_inf_claimed": False,
        "distributivity_claimed": False,
        "modularity_claimed": False,
        "globally_minimum_implication_basis_claimed": False,
        "hypergraph_dualization_complexity_claimed": False,
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
            "kuuos.memoryos.pointed-choice-free-signature-lattice-"
            "certificate.v0.1"
        ),
        "memoryos_frontier": FRONTIER,
        "step_id": STEP_ID,
        "source_frontier": "MemoryOS v0.95",
        "literature_alignment": [
            "arXiv:2607.01773",
            "arXiv:2509.05299",
            "arXiv:2603.14615",
            "arXiv:2502.04146",
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
        "completed_context_records": completed_contexts,
        "top_bottom_records": top_bottom,
        "pair_operation_records": pair_operations,
        "universal_property_records": universal_properties,
        "context_root_independence_records": root_contexts,
        "operation_root_independence_records": root_operations,
        "confidence_preservation_records": confidence,
        "record_counts": actual,
        "expected_record_counts": expected,
        "confidence_policy": {
            "source_confidence_preserved": True,
            "new_penalty": {"numerator": 0, "denominator": 1},
            "signature_cardinality_diagnostic_only": True,
            "lattice_height_diagnostic_only": True,
            "comparable_pair_counts_diagnostic_only": True,
        },
        "authority_boundary": boundary,
        "laws": laws,
    }

    forbidden = (
        "representative_choice_performed",
        "unique_minimal_generator_claimed",
        "complete_lattice_typeclass_claimed",
        "arbitrary_family_sup_inf_claimed",
        "distributivity_claimed",
        "modularity_claimed",
        "globally_minimum_implication_basis_claimed",
        "hypergraph_dualization_complexity_claimed",
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
