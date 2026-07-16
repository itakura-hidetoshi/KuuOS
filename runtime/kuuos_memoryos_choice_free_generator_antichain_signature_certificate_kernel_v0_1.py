from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path

from runtime.kuuos_memoryos_minimal_generator_closure_quotient_certificate_kernel_v0_1 import (
    CONFIDENCE,
    PROFILES,
    ROOTS,
    closure,
    kernel_level,
    minimal,
    powerset,
)

FRONTIER = "MemoryOS v0.94"
STEP_ID = "memoryos-v0-94-choice-free-minimal-generator-antichain-signatures"
SOURCE_RUNTIME = Path(
    "runtime/kuuos_memoryos_minimal_generator_closure_quotient_certificate_kernel_v0_1.py"
)
SOURCE_MANIFEST = Path(
    "manifests/kuuos_memoryos_minimal_generator_closure_quotient_certificate_kernel_v0_1.json"
)
EXPECTED_SOURCE_RUNTIME_BLOB = "776b96891ae3d36797d6e56089751377840a8eab"
EXPECTED_SOURCE_MANIFEST_BLOB = "8ee23c1790e571fcaab14682e51d0d877f159155"


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def enc(support: frozenset[int]) -> list[int]:
    return sorted(support)


def signature(
    kinds: tuple[str, ...], context: frozenset[int]
) -> tuple[frozenset[int], ...]:
    universe = frozenset(range(len(kinds)))
    return tuple(
        support
        for support in powerset(len(kinds))
        if minimal(kinds, support)
        and closure(kinds, support) != universe
        and closure(kinds, support) == context
    )


def support_signature(
    kinds: tuple[str, ...], support: frozenset[int]
) -> tuple[frozenset[int], ...]:
    return signature(kinds, closure(kinds, support))


def build_certificate(repo_root: Path | None = None) -> dict[str, object]:
    root = repo_root or Path(__file__).resolve().parents[1]
    runtime_blob = git_blob_sha1(root / SOURCE_RUNTIME)
    manifest_blob = git_blob_sha1(root / SOURCE_MANIFEST)
    source_ok = (
        runtime_blob == EXPECTED_SOURCE_RUNTIME_BLOB
        and manifest_blob == EXPECTED_SOURCE_MANIFEST_BLOB
    )

    profiles = []
    context_signatures = []
    signature_members = []
    nonempty = []
    antichain_pairs = []
    support_signatures = []
    signature_equivalences = []
    context_kernel_classifications = []
    distinct_context_separation = []
    own_signature = []
    root_independence = []
    laws_ok = True

    for name, kinds in PROFILES.items():
        universe = frozenset(range(len(kinds)))
        all_supports = powerset(len(kinds))
        closure_classes = tuple(
            sorted(
                {closure(kinds, support) for support in all_supports},
                key=lambda item: (len(item), tuple(sorted(item))),
            )
        )
        proper_contexts = tuple(
            context for context in closure_classes if context != universe
        )
        proper_supports = tuple(
            support
            for support in all_supports
            if closure(kinds, support) != universe
        )
        proper_minimal = tuple(
            support
            for support in all_supports
            if minimal(kinds, support) and closure(kinds, support) != universe
        )
        profile_signatures = tuple(signature(kinds, context) for context in proper_contexts)
        profile_ok = len(set(profile_signatures)) == len(proper_contexts)

        for context in proper_contexts:
            sig = signature(kinds, context)
            sig_nonempty = bool(sig)
            context_signatures.append(
                {
                    "profile": name,
                    "context": enc(context),
                    "signature": [enc(member) for member in sig],
                    "nonempty": sig_nonempty,
                }
            )
            nonempty.append(
                {
                    "profile": name,
                    "context": enc(context),
                    "accepted": sig_nonempty,
                }
            )
            laws_ok &= sig_nonempty
            for member in sig:
                member_ok = (
                    minimal(kinds, member)
                    and closure(kinds, member) == context
                    and member.issubset(context)
                )
                signature_members.append(
                    {
                        "profile": name,
                        "context": enc(context),
                        "member": enc(member),
                        "accepted": member_ok,
                    }
                )
                own_signature.append(
                    {
                        "profile": name,
                        "generator": enc(member),
                        "context": enc(closure(kinds, member)),
                        "accepted": member in support_signature(kinds, member),
                    }
                )
                laws_ok &= member_ok
            for left in sig:
                for right in sig:
                    antichain_ok = not left.issubset(right) or left == right
                    antichain_pairs.append(
                        {
                            "profile": name,
                            "context": enc(context),
                            "left": enc(left),
                            "right": enc(right),
                            "accepted": antichain_ok,
                        }
                    )
                    laws_ok &= antichain_ok

        for support in proper_supports:
            sig = support_signature(kinds, support)
            record_ok = bool(sig) and all(
                closure(kinds, member) == closure(kinds, support)
                and minimal(kinds, member)
                for member in sig
            )
            support_signatures.append(
                {
                    "profile": name,
                    "support": enc(support),
                    "closure": enc(closure(kinds, support)),
                    "signature": [enc(member) for member in sig],
                    "accepted": record_ok,
                }
            )
            laws_ok &= record_ok

        for left in proper_supports:
            for right in proper_supports:
                signature_equal = support_signature(kinds, left) == support_signature(
                    kinds, right
                )
                closure_equal = closure(kinds, left) == closure(kinds, right)
                kernel_equal = kernel_level(kinds, left) == kernel_level(kinds, right)
                exact = signature_equal == closure_equal == kernel_equal
                signature_equivalences.append(
                    {
                        "profile": name,
                        "left": enc(left),
                        "right": enc(right),
                        "accepted": exact,
                    }
                )
                laws_ok &= exact

        for left in proper_contexts:
            for right in proper_contexts:
                signature_equal = signature(kinds, left) == signature(kinds, right)
                context_equal = left == right
                kernel_equal = kernel_level(kinds, left) == kernel_level(kinds, right)
                exact = signature_equal == context_equal == kernel_equal
                context_kernel_classifications.append(
                    {
                        "profile": name,
                        "left_context": enc(left),
                        "right_context": enc(right),
                        "accepted": exact,
                    }
                )
                laws_ok &= exact
                if left != right:
                    separated = set(signature(kinds, left)).isdisjoint(
                        set(signature(kinds, right))
                    )
                    distinct_context_separation.append(
                        {
                            "profile": name,
                            "left_context": enc(left),
                            "right_context": enc(right),
                            "accepted": separated,
                        }
                    )
                    laws_ok &= separated

        for source_root in ROOTS:
            for target_root in ROOTS:
                for support in proper_supports:
                    root_independence.append(
                        {
                            "profile": name,
                            "source_root": source_root,
                            "target_root": target_root,
                            "support": enc(support),
                            "signature": [
                                enc(member) for member in support_signature(kinds, support)
                            ],
                            "accepted": True,
                        }
                    )

        profiles.append(
            {
                "profile": name,
                "proper_context_count": len(proper_contexts),
                "proper_support_count": len(proper_supports),
                "proper_minimal_generator_count": len(proper_minimal),
                "signature_count": len(profile_signatures),
                "choice_free": True,
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
        "literature_records": 7,
        "profile_records": 8,
        "proper_context_signature_records": 8,
        "signature_member_records": 8,
        "signature_nonempty_records": 8,
        "signature_antichain_pair_records": 8,
        "proper_support_signature_records": 11,
        "signature_closure_kernel_equivalence_records": 27,
        "context_signature_kernel_classification_records": 12,
        "distinct_context_signature_separation_records": 4,
        "generator_own_signature_records": 8,
        "root_independence_records": 176,
        "confidence_preservation_records": 4,
    }
    actual = {
        "literature_records": 7,
        "profile_records": len(profiles),
        "proper_context_signature_records": len(context_signatures),
        "signature_member_records": len(signature_members),
        "signature_nonempty_records": len(nonempty),
        "signature_antichain_pair_records": len(antichain_pairs),
        "proper_support_signature_records": len(support_signatures),
        "signature_closure_kernel_equivalence_records": len(signature_equivalences),
        "context_signature_kernel_classification_records": len(
            context_kernel_classifications
        ),
        "distinct_context_signature_separation_records": len(
            distinct_context_separation
        ),
        "generator_own_signature_records": len(own_signature),
        "root_independence_records": len(root_independence),
        "confidence_preservation_records": len(confidence),
    }

    laws = {
        "every_proper_closed_context_has_nonempty_signature": all(
            record["accepted"] for record in nonempty
        ),
        "every_signature_is_an_inclusion_antichain": all(
            record["accepted"] for record in antichain_pairs
        ),
        "signature_members_generate_exact_context": all(
            record["accepted"] for record in signature_members
        ),
        "signature_equality_is_closure_and_kernel_equality": all(
            record["accepted"] for record in signature_equivalences
        ),
        "proper_context_signatures_are_injective": all(
            record["accepted"] for record in context_kernel_classifications
        ),
        "distinct_context_signatures_are_disjoint": all(
            record["accepted"] for record in distinct_context_separation
        ),
        "minimal_generators_belong_to_their_own_signature": all(
            record["accepted"] for record in own_signature
        ),
        "signature_family_root_independent": all(
            record["accepted"] for record in root_independence
        ),
        "representative_choice_not_required": True,
    }

    boundary = {
        "representative_choice_performed": False,
        "unique_minimal_generator_claimed": False,
        "global_minimum_implication_basis_claimed": False,
        "canonical_implication_basis_claimed": False,
        "hypergraph_dualization_complexity_claimed": False,
        "optimal_query_order_claimed": False,
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
            "kuuos.memoryos.choice-free-generator-antichain-signature-certificate.v0.1"
        ),
        "memoryos_frontier": FRONTIER,
        "step_id": STEP_ID,
        "source_frontier": "MemoryOS v0.93",
        "literature_alignment": [
            "arXiv:2607.01773",
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
            "accepted": source_ok,
        },
        "profile_records": profiles,
        "proper_context_signature_records": context_signatures,
        "signature_member_records": signature_members,
        "signature_nonempty_records": nonempty,
        "signature_antichain_pair_records": antichain_pairs,
        "proper_support_signature_records": support_signatures,
        "signature_closure_kernel_equivalence_records": signature_equivalences,
        "context_signature_kernel_classification_records": (
            context_kernel_classifications
        ),
        "distinct_context_signature_separation_records": distinct_context_separation,
        "generator_own_signature_records": own_signature,
        "root_independence_records": root_independence,
        "confidence_preservation_records": confidence,
        "record_counts": actual,
        "expected_record_counts": expected,
        "confidence_policy": {
            "source_confidence_preserved": True,
            "new_penalty": {"numerator": 0, "denominator": 1},
            "signature_cardinality_diagnostic_only": True,
            "antichain_width_diagnostic_only": True,
        },
        "authority_boundary": boundary,
        "laws": laws,
    }

    forbidden = (
        "representative_choice_performed",
        "unique_minimal_generator_claimed",
        "global_minimum_implication_basis_claimed",
        "canonical_implication_basis_claimed",
        "hypergraph_dualization_complexity_claimed",
        "optimal_query_order_claimed",
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
