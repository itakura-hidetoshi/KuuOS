from __future__ import annotations

import copy
import json

from runtime.kuuos_memoryos_choice_free_generator_antichain_signature_certificate_kernel_v0_1 import (
    build_certificate,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def accepted(certificate: dict[str, object]) -> bool:
    return bool(
        certificate.get("accepted")
        and certificate["source_binding"]["accepted"]
        and certificate["record_counts"] == certificate["expected_record_counts"]
        and all(certificate["laws"].values())
        and certificate["confidence_policy"]["source_confidence_preserved"]
        and certificate["confidence_policy"]["new_penalty"]
        == {"numerator": 0, "denominator": 1}
        and not certificate["authority_boundary"]["representative_choice_performed"]
        and not certificate["authority_boundary"]["unique_minimal_generator_claimed"]
        and not certificate["authority_boundary"][
            "global_minimum_implication_basis_claimed"
        ]
        and not certificate["authority_boundary"][
            "hypergraph_dualization_complexity_claimed"
        ]
        and not certificate["authority_boundary"]["truth_authority"]
        and not certificate["authority_boundary"]["execution"]
    )


def main() -> int:
    certificate = build_certificate()
    require(accepted(certificate), "v0.94 certificate was not accepted")
    counts = certificate["record_counts"]
    require(
        counts["proper_context_signature_records"] == 8,
        "unexpected proper-context signature enumeration",
    )
    require(
        counts["signature_member_records"] == 8,
        "unexpected signature-member enumeration",
    )
    require(
        counts["signature_closure_kernel_equivalence_records"] == 27,
        "closure/kernel signature classification was not exhaustive",
    )
    require(
        counts["context_signature_kernel_classification_records"] == 12,
        "proper-context signature classification was not exhaustive",
    )
    require(
        counts["distinct_context_signature_separation_records"] == 4,
        "distinct signature separation ledger changed",
    )
    require(
        counts["root_independence_records"] == 176,
        "root-independence ledger changed",
    )

    mutations: list[tuple[str, dict[str, object]]] = []

    tampered = copy.deepcopy(certificate)
    tampered["accepted"] = False
    mutations.append(("acceptance", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["source_binding"]["accepted"] = False
    mutations.append(("source binding", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["record_counts"]["proper_context_signature_records"] += 1
    mutations.append(("record count", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["laws"]["every_signature_is_an_inclusion_antichain"] = False
    mutations.append(("antichain law", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["laws"]["signature_equality_is_closure_and_kernel_equality"] = False
    mutations.append(("classification law", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["confidence_policy"]["new_penalty"] = {
        "numerator": 1,
        "denominator": 100,
    }
    mutations.append(("confidence penalty", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["authority_boundary"]["representative_choice_performed"] = True
    mutations.append(("representative choice", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["authority_boundary"]["execution"] = True
    mutations.append(("execution authority", tampered))

    for label, mutation in mutations:
        require(not accepted(mutation), f"tamper test failed: {label}")

    print(
        json.dumps(
            {
                "checker": (
                    "MemoryOS v0.94 choice-free minimal-generator antichain signatures"
                ),
                "accepted": True,
                "tamper_tests": [label for label, _ in mutations],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
