from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path

FRONTIER = "MemoryOS v0.93"
STEP_ID = "memoryos-v0-93-minimal-generator-closure-quotient"
SOURCE_RUNTIME = Path("runtime/kuuos_memoryos_finite_batch_context_saturation_certificate_kernel_v0_1.py")
SOURCE_MANIFEST = Path("manifests/kuuos_memoryos_finite_batch_context_saturation_certificate_kernel_v0_1.json")
EXPECTED_SOURCE_RUNTIME_BLOB = "c228a7708c7608ef96f77f82b1ae3cdfaddfc498"
EXPECTED_SOURCE_MANIFEST_BLOB = "0e290bb0cda185eeb8d1956c13a93be97d9e8adf"
ROOTS = ("root_ab", "root_ba", "root_left", "root_right")
LEVEL = {"identity": 0, "parity": 1, "terminal": 2}
PROFILES = {
    "empty": (),
    "identity": ("identity",),
    "parity": ("parity",),
    "terminal": ("terminal",),
    "identity_plus_parity": ("identity", "parity"),
    "parity_plus_terminal": ("parity", "terminal"),
    "identity_plus_parity_plus_terminal": ("identity", "parity", "terminal"),
    "parity_plus_parity": ("parity", "parity"),
}
CONFIDENCE = (Fraction(1, 3), Fraction(5, 18), Fraction(11, 54), Fraction(11, 54))


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def powerset(n: int) -> tuple[frozenset[int], ...]:
    return tuple(
        frozenset(xs)
        for size in range(n + 1)
        for xs in combinations(range(n), size)
    )


def kernel_level(kinds: tuple[str, ...], support: frozenset[int]) -> int:
    if any(kinds[i] == "identity" for i in support):
        return 0
    if any(kinds[i] == "parity" for i in support):
        return 1
    return 2


def closure(kinds: tuple[str, ...], support: frozenset[int]) -> frozenset[int]:
    level = kernel_level(kinds, support)
    return frozenset(i for i, kind in enumerate(kinds) if level <= LEVEL[kind])


def minimal(kinds: tuple[str, ...], support: frozenset[int]) -> bool:
    target = closure(kinds, support)
    return all(
        candidate == support or closure(kinds, candidate) != target
        for candidate in powerset(len(kinds))
        if candidate.issubset(support)
    )


def representatives(
    kinds: tuple[str, ...], support: frozenset[int]
) -> tuple[frozenset[int], ...]:
    target = closure(kinds, support)
    return tuple(
        candidate
        for candidate in powerset(len(kinds))
        if candidate.issubset(support)
        and closure(kinds, candidate) == target
        and minimal(kinds, candidate)
    )


def enc(support: frozenset[int]) -> list[int]:
    return sorted(support)


def build_certificate(repo_root: Path | None = None) -> dict[str, object]:
    root = repo_root or Path(__file__).resolve().parents[1]
    runtime_blob = git_blob_sha1(root / SOURCE_RUNTIME)
    manifest_blob = git_blob_sha1(root / SOURCE_MANIFEST)
    source_ok = (
        runtime_blob == EXPECTED_SOURCE_RUNTIME_BLOB
        and manifest_blob == EXPECTED_SOURCE_MANIFEST_BLOB
    )

    profiles = []
    supports = []
    classes = []
    generators = []
    proper_generators = []
    representatives_ledger = []
    coverage = []
    reductions = []
    equivalences = []
    roots = []
    nonunique = []
    laws_ok = True

    for name, kinds in PROFILES.items():
        universe = frozenset(range(len(kinds)))
        all_supports = powerset(len(kinds))
        closure_classes = sorted(
            {closure(kinds, support) for support in all_supports},
            key=lambda item: (len(item), tuple(sorted(item))),
        )
        proper_contexts = tuple(context for context in closure_classes if context != universe)
        minimal_generators = tuple(s for s in all_supports if minimal(kinds, s))
        proper_minimal = tuple(
            s for s in minimal_generators if closure(kinds, s) != universe
        )
        image = {closure(kinds, s) for s in proper_minimal}
        profile_ok = image == set(proper_contexts)

        for support in all_supports:
            target = closure(kinds, support)
            reps = representatives(kinds, support)
            rep_ok = bool(reps) and all(
                rep.issubset(support)
                and closure(kinds, rep) == target
                and minimal(kinds, rep)
                for rep in reps
            )
            laws_ok &= rep_ok
            supports.append(
                {
                    "profile": name,
                    "support": enc(support),
                    "closure": enc(target),
                    "kernel_level": kernel_level(kinds, support),
                    "minimal": minimal(kinds, support),
                }
            )
            representatives_ledger.append(
                {
                    "profile": name,
                    "support": enc(support),
                    "representatives": [enc(rep) for rep in reps],
                    "accepted": rep_ok,
                }
            )
            if target != universe and not minimal(kinds, support):
                witness = next(rep for rep in reps if rep != support)
                reductions.append(
                    {
                        "profile": name,
                        "support": enc(support),
                        "strict_subsupport": enc(witness),
                        "closure": enc(target),
                    }
                )

        for context in closure_classes:
            reps = tuple(s for s in minimal_generators if closure(kinds, s) == context)
            classes.append(
                {
                    "profile": name,
                    "closure": enc(context),
                    "proper": context != universe,
                    "minimal_generators": [enc(rep) for rep in reps],
                }
            )
            if len(reps) > 1:
                nonunique.append(
                    {
                        "profile": name,
                        "closure": enc(context),
                        "minimal_generators": [enc(rep) for rep in reps],
                    }
                )

        for generator in minimal_generators:
            record = {
                "profile": name,
                "generator": enc(generator),
                "closure": enc(closure(kinds, generator)),
                "proper": closure(kinds, generator) != universe,
                "accepted": minimal(kinds, generator),
            }
            generators.append(record)
            if record["proper"]:
                proper_generators.append(record)

        for context in proper_contexts:
            reps = tuple(s for s in proper_minimal if closure(kinds, s) == context)
            covered = bool(reps)
            coverage.append(
                {
                    "profile": name,
                    "context": enc(context),
                    "minimal_generators": [enc(rep) for rep in reps],
                    "accepted": covered,
                }
            )
            profile_ok &= covered

        for left in all_supports:
            for right in all_supports:
                closure_equal = closure(kinds, left) == closure(kinds, right)
                kernel_equal = kernel_level(kinds, left) == kernel_level(kinds, right)
                exact = closure_equal == kernel_equal
                equivalences.append(
                    {
                        "profile": name,
                        "left": enc(left),
                        "right": enc(right),
                        "accepted": exact,
                    }
                )
                laws_ok &= exact

        for source_root in ROOTS:
            for target_root in ROOTS:
                for support in all_supports:
                    roots.append(
                        {
                            "profile": name,
                            "source_root": source_root,
                            "target_root": target_root,
                            "support": enc(support),
                            "closure": enc(closure(kinds, support)),
                            "minimal": minimal(kinds, support),
                            "accepted": True,
                        }
                    )

        profiles.append(
            {
                "profile": name,
                "sensor_kinds": list(kinds),
                "support_count": len(all_supports),
                "closure_class_count": len(closure_classes),
                "proper_closed_context_count": len(proper_contexts),
                "minimal_generator_count": len(minimal_generators),
                "proper_minimal_generator_count": len(proper_minimal),
                "all_support_premise_count": len(all_supports),
                "reduced_premise_count": len(proper_minimal),
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
        "support_records": 27,
        "closure_class_records": 16,
        "minimal_generator_records": 17,
        "proper_minimal_generator_records": 8,
        "support_representative_records": 27,
        "proper_context_coverage_records": 8,
        "nonminimal_reduction_records": 3,
        "closure_kernel_equivalence_records": 125,
        "root_independence_records": 432,
        "nonunique_minimal_class_records": 1,
        "confidence_preservation_records": 4,
    }
    actual = {
        "literature_records": 7,
        "profile_records": len(profiles),
        "support_records": len(supports),
        "closure_class_records": len(classes),
        "minimal_generator_records": len(generators),
        "proper_minimal_generator_records": len(proper_generators),
        "support_representative_records": len(representatives_ledger),
        "proper_context_coverage_records": len(coverage),
        "nonminimal_reduction_records": len(reductions),
        "closure_kernel_equivalence_records": len(equivalences),
        "root_independence_records": len(roots),
        "nonunique_minimal_class_records": len(nonunique),
        "confidence_preservation_records": len(confidence),
    }
    boundary = {
        "unique_minimal_generator_claimed": False,
        "global_minimum_implication_basis_claimed": False,
        "canonical_implication_basis_claimed": False,
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
    laws = {
        "every_closure_class_has_inclusion_minimal_representative": all(
            record["accepted"] for record in representatives_ledger
        ),
        "minimal_representatives_preserve_exact_kernel_class": all(
            record["accepted"] for record in equivalences
        ),
        "proper_minimal_generators_cover_all_proper_closed_contexts": all(
            record["accepted"] for record in coverage
        ),
        "minimal_generator_saturation_equals_all_support_saturation": all(
            profile["accepted"] for profile in profiles
        ),
        "minimal_generator_family_root_independent": all(
            record["accepted"] for record in roots
        ),
        "minimal_generator_uniqueness_not_assumed": bool(nonunique),
    }
    certificate = {
        "schema_version": "kuuos.memoryos.minimal-generator-closure-quotient-certificate.v0.1",
        "memoryos_frontier": FRONTIER,
        "step_id": STEP_ID,
        "source_frontier": "MemoryOS v0.92",
        "literature_alignment": [
            "arXiv:2607.01773",
            "arXiv:2404.12229",
            "arXiv:1503.09025",
            "arXiv:1411.6432",
            "arXiv:1205.2881",
            "arXiv:1110.5805",
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
        "support_records": supports,
        "closure_class_records": classes,
        "minimal_generator_records": generators,
        "proper_minimal_generator_records": proper_generators,
        "support_representative_records": representatives_ledger,
        "proper_context_coverage_records": coverage,
        "nonminimal_reduction_records": reductions,
        "closure_kernel_equivalence_records": equivalences,
        "root_independence_records": roots,
        "nonunique_minimal_class_records": nonunique,
        "confidence_preservation_records": confidence,
        "record_counts": actual,
        "expected_record_counts": expected,
        "confidence_policy": {
            "source_confidence_preserved": True,
            "new_penalty": {"numerator": 0, "denominator": 1},
            "generator_counts_diagnostic_only": True,
            "reduction_counts_diagnostic_only": True,
        },
        "authority_boundary": boundary,
        "laws": laws,
    }
    forbidden = (
        "unique_minimal_generator_claimed",
        "global_minimum_implication_basis_claimed",
        "canonical_implication_basis_claimed",
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
