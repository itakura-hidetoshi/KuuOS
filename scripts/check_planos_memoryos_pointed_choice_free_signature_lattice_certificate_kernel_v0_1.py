from __future__ import annotations

import copy
import json

from runtime.kuuos_memoryos_pointed_choice_free_signature_lattice_certificate_kernel_v0_1 import (
    build_certificate,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def accepted(certificate: dict[str, object]) -> bool:
    boundary = certificate["authority_boundary"]
    return bool(
        certificate.get("accepted")
        and certificate["source_binding"]["accepted"]
        and certificate["source_binding"]["source_certificate_accepted"]
        and certificate["record_counts"]
        == certificate["expected_record_counts"]
        and all(certificate["laws"].values())
        and certificate["confidence_policy"]["source_confidence_preserved"]
        and certificate["confidence_policy"]["new_penalty"]
        == {"numerator": 0, "denominator": 1}
        and not boundary["representative_choice_performed"]
        and not boundary["complete_lattice_typeclass_claimed"]
        and not boundary["arbitrary_family_sup_inf_claimed"]
        and not boundary["distributivity_claimed"]
        and not boundary["truth_authority"]
        and not boundary["execution"]
    )


def main() -> int:
    certificate = build_certificate()
    require(accepted(certificate), "v0.96 certificate was not accepted")
    counts = certificate["record_counts"]
    require(
        counts["completed_context_records"] == 16,
        "unexpected all-closed-context enumeration",
    )
    require(
        counts["top_bottom_records"] == 8,
        "unexpected pointed top/bottom enumeration",
    )
    require(
        counts["pair_operation_records"] == 36,
        "unexpected binary lattice-operation enumeration",
    )
    require(
        counts["universal_property_records"] == 88,
        "unexpected meet/join universal-property enumeration",
    )
    require(
        counts["context_root_independence_records"] == 256,
        "unexpected context root-independence enumeration",
    )
    require(
        counts["operation_root_independence_records"] == 576,
        "unexpected operation root-independence enumeration",
    )

    mutations: list[tuple[str, dict[str, object]]] = []

    tampered = copy.deepcopy(certificate)
    tampered["accepted"] = False
    mutations.append(("acceptance", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["source_binding"]["accepted"] = False
    mutations.append(("source binding", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["record_counts"]["completed_context_records"] += 1
    mutations.append(("record count", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["laws"][
        "empty_signature_is_exact_universal_context_sentinel"
    ] = False
    mutations.append(("top sentinel law", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["laws"][
        "meet_and_join_satisfy_universal_properties"
    ] = False
    mutations.append(("lattice universal property", tampered))

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
    tampered["authority_boundary"]["complete_lattice_typeclass_claimed"] = True
    mutations.append(("complete lattice overclaim", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["authority_boundary"]["execution"] = True
    mutations.append(("execution authority", tampered))

    for label, mutation in mutations:
        require(not accepted(mutation), f"tamper test failed: {label}")

    print(
        json.dumps(
            {
                "checker": (
                    "MemoryOS v0.96 pointed choice-free signature lattice"
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
