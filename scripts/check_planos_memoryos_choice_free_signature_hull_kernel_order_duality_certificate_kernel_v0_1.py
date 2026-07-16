from __future__ import annotations

import copy
import json

from runtime.kuuos_memoryos_choice_free_signature_hull_kernel_order_duality_certificate_kernel_v0_1 import (
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
        and not boundary["complete_lattice_structure_claimed"]
        and not boundary["truth_authority"]
        and not boundary["execution"]
    )


def main() -> int:
    certificate = build_certificate()
    require(accepted(certificate), "v0.95 certificate was not accepted")
    counts = certificate["record_counts"]
    require(
        counts["proper_context_hull_records"] == 8,
        "unexpected proper-context hull enumeration",
    )
    require(
        counts["proper_support_hull_records"] == 11,
        "unexpected proper-support hull enumeration",
    )
    require(
        counts["context_hull_order_records"] == 12,
        "unexpected context hull-order enumeration",
    )
    require(
        counts["support_hull_order_records"] == 27,
        "unexpected support hull-order enumeration",
    )
    require(
        counts["context_hull_root_independence_records"] == 128,
        "unexpected context root-independence enumeration",
    )
    require(
        counts["support_hull_root_independence_records"] == 176,
        "unexpected support root-independence enumeration",
    )

    mutations: list[tuple[str, dict[str, object]]] = []

    tampered = copy.deepcopy(certificate)
    tampered["accepted"] = False
    mutations.append(("acceptance", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["source_binding"]["accepted"] = False
    mutations.append(("source binding", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["record_counts"]["proper_context_hull_records"] += 1
    mutations.append(("record count", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["laws"][
        "proper_context_is_reconstructed_by_signature_closed_hull"
    ] = False
    mutations.append(("context reconstruction law", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["laws"][
        "support_signature_hull_order_is_reverse_kernel_inclusion"
    ] = False
    mutations.append(("kernel order-duality law", tampered))

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
                    "MemoryOS v0.95 choice-free signature hull "
                    "kernel-order duality"
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
