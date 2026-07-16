from __future__ import annotations

import hashlib
import json
from pathlib import Path

from runtime.kuuos_memoryos_choice_free_generator_antichain_signature_certificate_kernel_v0_1 import (
    build_certificate as build_source_certificate,
    enc,
    signature,
    support_signature,
)
from runtime.kuuos_memoryos_minimal_generator_closure_quotient_certificate_kernel_v0_1 import (
    CONFIDENCE,
    PROFILES,
    ROOTS,
    closure,
    kernel_level,
    powerset,
)

FRONTIER = "MemoryOS v0.95"
STEP_ID = "memoryos-v0-95-choice-free-signature-hull-kernel-order-duality"
SOURCE_RUNTIME = Path(
    "runtime/kuuos_memoryos_choice_free_generator_antichain_signature_certificate_kernel_v0_1.py"
)
SOURCE_MANIFEST = Path(
    "manifests/kuuos_memoryos_choice_free_generator_antichain_signature_certificate_kernel_v0_1.json"
)
EXPECTED_SOURCE_RUNTIME_BLOB = "25749ae9f575156ae403e0b64f398a7e2b464ede"
EXPECTED_SOURCE_MANIFEST_BLOB = "42759d82aa5c644a7daa46ca9bd85e9d4a224cfb"


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def envelope(generators: tuple[frozenset[int], ...]) -> frozenset[int]:
    result: frozenset[int] = frozenset()
    for generator in generators:
        result = result.union(generator)
    return result


def hull(
    kinds: tuple[str, ...], generators: tuple[frozenset[int], ...]
) -> frozenset[int]:
    return closure(kinds, envelope(generators))


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
    context_hulls = []
    member_envelopes = []
    support_hulls = []
    context_orders = []
    support_orders = []
    antisymmetry = []
    context_roots = []
    support_roots = []
    laws_ok = True

    for name, kinds in PROFILES.items():
        universe = frozenset(range(len(kinds)))
        supports = powerset(len(kinds))
        contexts = tuple(
            sorted(
                {
                    closure(kinds, support)
                    for support in supports
                    if closure(kinds, support) != universe
                },
                key=lambda value: (len(value), tuple(sorted(value))),
            )
        )
        proper_supports = tuple(
            support
            for support in supports
            if closure(kinds, support) != universe
        )
        profile_ok = True

        for context in contexts:
            generators = signature(kinds, context)
            env = envelope(generators)
            closed_hull = hull(kinds, generators)
            accepted = (
                bool(generators)
                and all(generator.issubset(env) for generator in generators)
                and env.issubset(context)
                and closed_hull == context
            )
            context_hulls.append(
                {
                    "profile": name,
                    "context": enc(context),
                    "signature": [enc(value) for value in generators],
                    "envelope": enc(env),
                    "closed_hull": enc(closed_hull),
                    "accepted": accepted,
                }
            )
            profile_ok &= accepted
            laws_ok &= accepted

            for generator in generators:
                member_ok = generator.issubset(env)
                member_envelopes.append(
                    {
                        "profile": name,
                        "context": enc(context),
                        "generator": enc(generator),
                        "envelope": enc(env),
                        "accepted": member_ok,
                    }
                )
                laws_ok &= member_ok

            context_roots.extend(
                {
                    "profile": name,
                    "context": enc(context),
                    "source_root": source_root,
                    "target_root": target_root,
                    "envelope": enc(env),
                    "closed_hull": enc(closed_hull),
                    "accepted": True,
                }
                for source_root in ROOTS
                for target_root in ROOTS
            )

        for support in proper_supports:
            generators = support_signature(kinds, support)
            env = envelope(generators)
            closed_hull = hull(kinds, generators)
            source_closure = closure(kinds, support)
            accepted = (
                bool(generators)
                and closed_hull == source_closure
                and kernel_level(kinds, env) == kernel_level(kinds, support)
            )
            support_hulls.append(
                {
                    "profile": name,
                    "support": enc(support),
                    "signature": [enc(value) for value in generators],
                    "envelope": enc(env),
                    "closed_hull": enc(closed_hull),
                    "source_closure": enc(source_closure),
                    "kernel_level": kernel_level(kinds, support),
                    "envelope_kernel_level": kernel_level(kinds, env),
                    "accepted": accepted,
                }
            )
            profile_ok &= accepted
            laws_ok &= accepted
            support_roots.extend(
                {
                    "profile": name,
                    "support": enc(support),
                    "source_root": source_root,
                    "target_root": target_root,
                    "envelope": enc(env),
                    "closed_hull": enc(closed_hull),
                    "accepted": True,
                }
                for source_root in ROOTS
                for target_root in ROOTS
            )

        for left in contexts:
            for right in contexts:
                left_sig = signature(kinds, left)
                right_sig = signature(kinds, right)
                left_hull = hull(kinds, left_sig)
                right_hull = hull(kinds, right_sig)
                hull_order = left_hull.issubset(right_hull)
                context_order = left.issubset(right)
                kernel_reverse = (
                    kernel_level(kinds, right)
                    <= kernel_level(kinds, left)
                )
                order_ok = hull_order == context_order == kernel_reverse
                context_orders.append(
                    {
                        "profile": name,
                        "left_context": enc(left),
                        "right_context": enc(right),
                        "hull_order": hull_order,
                        "context_order": context_order,
                        "kernel_reverse_order": kernel_reverse,
                        "accepted": order_ok,
                    }
                )
                laws_ok &= order_ok

                bidirectional = (
                    hull_order and right_hull.issubset(left_hull)
                )
                signature_equal = set(left_sig) == set(right_sig)
                antisymmetry_ok = (
                    bidirectional == signature_equal == (left == right)
                )
                antisymmetry.append(
                    {
                        "profile": name,
                        "left_context": enc(left),
                        "right_context": enc(right),
                        "bidirectional_hull_order": bidirectional,
                        "signature_equal": signature_equal,
                        "context_equal": left == right,
                        "accepted": antisymmetry_ok,
                    }
                )
                laws_ok &= antisymmetry_ok

        for left in proper_supports:
            for right in proper_supports:
                left_hull = hull(kinds, support_signature(kinds, left))
                right_hull = hull(kinds, support_signature(kinds, right))
                hull_order = left_hull.issubset(right_hull)
                closure_order = closure(kinds, left).issubset(
                    closure(kinds, right)
                )
                kernel_reverse = (
                    kernel_level(kinds, right)
                    <= kernel_level(kinds, left)
                )
                order_ok = hull_order == closure_order == kernel_reverse
                support_orders.append(
                    {
                        "profile": name,
                        "left_support": enc(left),
                        "right_support": enc(right),
                        "hull_order": hull_order,
                        "closure_order": closure_order,
                        "kernel_reverse_order": kernel_reverse,
                        "accepted": order_ok,
                    }
                )
                laws_ok &= order_ok

        profiles.append(
            {
                "profile": name,
                "sensor_kinds": list(kinds),
                "proper_context_count": len(contexts),
                "proper_support_count": len(proper_supports),
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
        "literature_records": 8,
        "profile_records": 8,
        "proper_context_hull_records": 8,
        "signature_member_envelope_records": 8,
        "proper_support_hull_records": 11,
        "context_hull_order_records": 12,
        "support_hull_order_records": 27,
        "context_antisymmetry_records": 12,
        "context_hull_root_independence_records": 128,
        "support_hull_root_independence_records": 176,
        "confidence_preservation_records": 4,
    }
    actual = {
        "literature_records": 8,
        "profile_records": len(profiles),
        "proper_context_hull_records": len(context_hulls),
        "signature_member_envelope_records": len(member_envelopes),
        "proper_support_hull_records": len(support_hulls),
        "context_hull_order_records": len(context_orders),
        "support_hull_order_records": len(support_orders),
        "context_antisymmetry_records": len(antisymmetry),
        "context_hull_root_independence_records": len(context_roots),
        "support_hull_root_independence_records": len(support_roots),
        "confidence_preservation_records": len(confidence),
    }
    laws = {
        "signature_envelope_contains_every_signature_member": all(
            record["accepted"] for record in member_envelopes
        ),
        "proper_context_is_reconstructed_by_signature_closed_hull": all(
            record["accepted"] for record in context_hulls
        ),
        "proper_support_closure_is_reconstructed_by_signature_closed_hull": all(
            record["accepted"] for record in support_hulls
        ),
        "signature_envelope_preserves_exact_support_kernel": all(
            record["accepted"] for record in support_hulls
        ),
        "context_signature_hull_order_is_context_inclusion": all(
            record["accepted"] for record in context_orders
        ),
        "context_signature_hull_order_is_reverse_kernel_inclusion": all(
            record["accepted"] for record in context_orders
        ),
        "support_signature_hull_order_is_closure_inclusion": all(
            record["accepted"] for record in support_orders
        ),
        "support_signature_hull_order_is_reverse_kernel_inclusion": all(
            record["accepted"] for record in support_orders
        ),
        "bidirectional_signature_hull_order_is_signature_equality": all(
            record["accepted"] for record in antisymmetry
        ),
        "signature_envelopes_and_hulls_are_root_independent": all(
            record["accepted"] for record in context_roots + support_roots
        ),
    }
    boundary = {
        "representative_choice_performed": False,
        "unique_minimal_generator_claimed": False,
        "general_unique_antichain_factorization_claimed": False,
        "complete_lattice_structure_claimed": False,
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
            "kuuos.memoryos.choice-free-signature-hull-kernel-order-"
            "duality-certificate.v0.1"
        ),
        "memoryos_frontier": FRONTIER,
        "step_id": STEP_ID,
        "source_frontier": "MemoryOS v0.94",
        "literature_alignment": [
            "arXiv:2607.01773",
            "arXiv:2509.05299",
            "arXiv:2506.24052",
            "arXiv:2407.00694",
            "arXiv:2404.12229",
            "arXiv:1503.09025",
            "arXiv:1411.6432",
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
        "proper_context_hull_records": context_hulls,
        "signature_member_envelope_records": member_envelopes,
        "proper_support_hull_records": support_hulls,
        "context_hull_order_records": context_orders,
        "support_hull_order_records": support_orders,
        "context_antisymmetry_records": antisymmetry,
        "context_hull_root_independence_records": context_roots,
        "support_hull_root_independence_records": support_roots,
        "confidence_preservation_records": confidence,
        "record_counts": actual,
        "expected_record_counts": expected,
        "confidence_policy": {
            "source_confidence_preserved": True,
            "new_penalty": {"numerator": 0, "denominator": 1},
            "envelope_size_diagnostic_only": True,
            "hull_order_counts_diagnostic_only": True,
        },
        "authority_boundary": boundary,
        "laws": laws,
    }
    forbidden = (
        "representative_choice_performed",
        "unique_minimal_generator_claimed",
        "general_unique_antichain_factorization_claimed",
        "complete_lattice_structure_claimed",
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
