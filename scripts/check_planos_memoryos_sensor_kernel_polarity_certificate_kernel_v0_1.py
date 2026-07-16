from __future__ import annotations

import copy
import json

from runtime.kuuos_memoryos_sensor_kernel_polarity_certificate_kernel_v0_1 import build_certificate


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
        and not boundary["infinite_family_sup_inf_claimed"]
        and not boundary["all_subgroups_sensor_representable_claimed"]
        and not boundary["truth_authority"]
        and not boundary["execution"]
    )


def main() -> int:
    certificate = build_certificate()
    require(accepted(certificate), "v0.98 certificate was not accepted")
    counts = certificate["record_counts"]
    require(
        counts["support_kernel_polarity_records"] == 81,
        "unexpected support-kernel polarity enumeration",
    )
    require(
        counts["kernel_envelope_records"] == 24,
        "unexpected kernel-envelope enumeration",
    )
    require(
        counts["closed_support_fixed_point_records"] == 16,
        "unexpected closed-support fixed-point enumeration",
    )
    require(
        counts["closed_support_order_duality_records"] == 36,
        "unexpected closed-support order-duality enumeration",
    )
    require(
        counts["finite_family_kernel_transport_records"] == 36,
        "unexpected finite-family kernel transport enumeration",
    )
    require(
        counts["polarity_root_independence_records"] == 1296,
        "unexpected polarity root-independence enumeration",
    )
    require(
        counts["kernel_envelope_root_independence_records"] == 384,
        "unexpected kernel-envelope root-independence enumeration",
    )

    mutations: list[tuple[str, dict[str, object]]] = []

    tampered = copy.deepcopy(certificate)
    tampered["accepted"] = False
    mutations.append(("acceptance", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["source_binding"]["accepted"] = False
    mutations.append(("source binding", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["record_counts"]["support_kernel_polarity_records"] += 1
    mutations.append(("record count", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["laws"]["support_kernel_maps_form_exact_antitone_polarity"] = False
    mutations.append(("polarity law", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["laws"]["kernel_envelope_is_extensive_monotone_idempotent"] = False
    mutations.append(("kernel envelope law", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["laws"]["finite_support_meet_transports_to_enveloped_kernel_supremum"] = False
    mutations.append(("finite transport", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["confidence_policy"]["new_penalty"] = {
        "numerator": 1,
        "denominator": 100,
    }
    mutations.append(("confidence penalty", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["authority_boundary"]["all_subgroups_sensor_representable_claimed"] = True
    mutations.append(("universal representability claim", tampered))

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
                "checker": "MemoryOS v0.98 sensor-kernel polarity",
                "accepted": True,
                "tamper_tests": [label for label, _ in mutations],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
