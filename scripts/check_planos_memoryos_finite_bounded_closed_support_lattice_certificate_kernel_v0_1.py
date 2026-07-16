from __future__ import annotations

import copy
import json

from runtime.kuuos_memoryos_finite_bounded_closed_support_lattice_certificate_kernel_v0_1 import (
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
        and certificate["record_counts"] == certificate["expected_record_counts"]
        and all(certificate["laws"].values())
        and certificate["confidence_policy"]["source_confidence_preserved"]
        and certificate["confidence_policy"]["new_penalty"]
        == {"numerator": 0, "denominator": 1}
        and not boundary["complete_lattice_typeclass_claimed"]
        and not boundary["infinite_family_theorem_claimed"]
        and not boundary["distributivity_claimed"]
        and not boundary["modularity_claimed"]
        and not boundary["ambient_subgroup_lattice_equivalence_claimed"]
        and not boundary["truth_authority"]
        and not boundary["execution"]
    )


def main() -> int:
    certificate = build_certificate()
    require(accepted(certificate), "v1.00 certificate was not accepted")
    counts = certificate["record_counts"]
    require(counts["binary_lattice_records"] == 36, "unexpected binary lattice count")
    require(counts["endpoint_bound_records"] == 16, "unexpected endpoint bound count")
    require(
        counts["finite_family_lattice_records"] == 36,
        "unexpected finite-family lattice count",
    )
    require(
        counts["empty_singleton_records"] == 16,
        "unexpected empty/singleton count",
    )
    require(
        counts["finite_kernel_transport_records"] == 36,
        "unexpected finite kernel transport count",
    )
    require(
        counts["endpoint_root_independence_records"] == 256,
        "unexpected endpoint root-independence count",
    )

    mutations: list[tuple[str, dict[str, object]]] = []

    tampered = copy.deepcopy(certificate)
    tampered["accepted"] = False
    mutations.append(("acceptance", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["source_binding"]["accepted"] = False
    mutations.append(("source binding", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["record_counts"]["binary_lattice_records"] += 1
    mutations.append(("record count", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["laws"]["closed_support_binary_operations_form_a_lattice"] = False
    mutations.append(("binary lattice law", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["laws"][
        "typed_finite_meet_and_join_satisfy_universal_properties"
    ] = False
    mutations.append(("finite universal law", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["laws"][
        "typed_finite_operations_transport_to_kernel_operations"
    ] = False
    mutations.append(("kernel transport law", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["confidence_policy"]["new_penalty"] = {
        "numerator": 1,
        "denominator": 100,
    }
    mutations.append(("confidence penalty", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["authority_boundary"]["complete_lattice_typeclass_claimed"] = True
    mutations.append(("complete lattice claim", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["authority_boundary"]["distributivity_claimed"] = True
    mutations.append(("distributivity claim", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["authority_boundary"][
        "ambient_subgroup_lattice_equivalence_claimed"
    ] = True
    mutations.append(("ambient subgroup lattice equivalence", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["authority_boundary"]["execution"] = True
    mutations.append(("execution authority", tampered))

    for label, mutation in mutations:
        require(not accepted(mutation), f"tamper test failed: {label}")

    print(
        json.dumps(
            {
                "checker": "MemoryOS v1.00 finite bounded closed-support lattice",
                "accepted": True,
                "tamper_tests": [label for label, _ in mutations],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
