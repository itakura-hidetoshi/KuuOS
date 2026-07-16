from __future__ import annotations

import copy
import json

from runtime.kuuos_memoryos_minimal_generator_closure_quotient_certificate_kernel_v0_1 import (
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
        and not certificate["authority_boundary"][
            "unique_minimal_generator_claimed"
        ]
        and not certificate["authority_boundary"][
            "global_minimum_implication_basis_claimed"
        ]
        and not certificate["authority_boundary"]["truth_authority"]
        and not certificate["authority_boundary"]["execution"]
    )


def main() -> int:
    certificate = build_certificate()
    require(accepted(certificate), "v0.93 certificate was not accepted")
    require(
        certificate["record_counts"]["support_records"] == 27,
        "unexpected support enumeration",
    )
    require(
        certificate["record_counts"]["minimal_generator_records"] == 17,
        "unexpected minimal-generator enumeration",
    )
    require(
        certificate["record_counts"]["proper_minimal_generator_records"] == 8,
        "unexpected proper minimal-generator enumeration",
    )
    require(
        certificate["record_counts"]["proper_context_coverage_records"] == 8,
        "proper closed contexts were not covered exactly",
    )
    require(
        certificate["record_counts"]["nonminimal_reduction_records"] == 3,
        "unexpected nonminimal reduction ledger",
    )
    require(
        certificate["record_counts"]["nonunique_minimal_class_records"] == 1,
        "the finite non-uniqueness witness was not retained",
    )

    mutations: list[tuple[str, dict[str, object]]] = []

    tampered = copy.deepcopy(certificate)
    tampered["accepted"] = False
    mutations.append(("acceptance", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["source_binding"]["accepted"] = False
    mutations.append(("source binding", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["record_counts"]["proper_minimal_generator_records"] += 1
    mutations.append(("record count", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["laws"][
        "proper_minimal_generators_cover_all_proper_closed_contexts"
    ] = False
    mutations.append(("coverage law", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["confidence_policy"]["new_penalty"] = {
        "numerator": 1,
        "denominator": 100,
    }
    mutations.append(("confidence penalty", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["authority_boundary"]["unique_minimal_generator_claimed"] = True
    mutations.append(("uniqueness authority", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["authority_boundary"]["execution"] = True
    mutations.append(("execution authority", tampered))

    for label, mutation in mutations:
        require(not accepted(mutation), f"tamper test failed: {label}")

    print(
        json.dumps(
            {
                "checker": "MemoryOS v0.93 minimal-generator closure quotient",
                "accepted": True,
                "tamper_tests": [label for label, _ in mutations],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
