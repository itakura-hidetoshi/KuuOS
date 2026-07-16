from __future__ import annotations

import copy
import json

from runtime.kuuos_memoryos_closed_support_representable_kernel_order_iso_certificate_kernel_v0_1 import build_certificate


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
        and not boundary["ambient_subgroup_order_iso_claimed"]
        and not boundary["all_subgroups_sensor_representable_claimed"]
        and not boundary["truth_authority"]
        and not boundary["execution"]
    )


def main() -> int:
    certificate = build_certificate()
    require(accepted(certificate), "v0.99 certificate was not accepted")
    counts = certificate["record_counts"]
    require(
        counts["closed_support_typed_map_records"] == 16,
        "unexpected closed-support typed-map enumeration",
    )
    require(
        counts["representable_kernel_typed_map_records"] == 16,
        "unexpected representable-kernel typed-map enumeration",
    )
    require(
        counts["order_iso_records"] == 36,
        "unexpected order-isomorphism enumeration",
    )
    require(
        counts["binary_operation_transport_records"] == 36,
        "unexpected binary-operation transport enumeration",
    )
    require(
        counts["finite_family_transport_records"] == 36,
        "unexpected finite-family transport enumeration",
    )
    require(
        counts["support_map_root_independence_records"] == 256,
        "unexpected support-map root-independence enumeration",
    )
    require(
        counts["kernel_map_root_independence_records"] == 256,
        "unexpected kernel-map root-independence enumeration",
    )

    mutations: list[tuple[str, dict[str, object]]] = []

    tampered = copy.deepcopy(certificate)
    tampered["accepted"] = False
    mutations.append(("acceptance", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["source_binding"]["accepted"] = False
    mutations.append(("source binding", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["record_counts"]["order_iso_records"] += 1
    mutations.append(("record count", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["laws"][
        "closed_support_order_is_isomorphic_to_dual_representable_kernel_order"
    ] = False
    mutations.append(("typed order isomorphism law", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["laws"]["binary_meet_maps_to_enveloped_kernel_supremum"] = False
    mutations.append(("binary meet transport", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["confidence_policy"]["new_penalty"] = {
        "numerator": 1,
        "denominator": 100,
    }
    mutations.append(("confidence penalty", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["authority_boundary"]["ambient_subgroup_order_iso_claimed"] = True
    mutations.append(("ambient subgroup order-isomorphism claim", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["authority_boundary"]["complete_lattice_typeclass_claimed"] = True
    mutations.append(("complete lattice claim", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["authority_boundary"]["execution"] = True
    mutations.append(("execution authority", tampered))

    for label, mutation in mutations:
        require(not accepted(mutation), f"tamper test failed: {label}")

    print(
        json.dumps(
            {
                "checker": (
                    "MemoryOS v0.99 typed closed-support / "
                    "representable-kernel order anti-isomorphism"
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
