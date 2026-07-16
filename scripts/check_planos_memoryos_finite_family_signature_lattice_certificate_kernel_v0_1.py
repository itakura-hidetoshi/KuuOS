from __future__ import annotations

import copy
import json

from runtime.kuuos_memoryos_finite_family_signature_lattice_certificate_kernel_v0_1 import build_certificate


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
        and not boundary["arbitrary_set_indexed_sup_inf_claimed"]
        and not boundary["distributivity_claimed"]
        and not boundary["truth_authority"]
        and not boundary["execution"]
    )


def main() -> int:
    certificate = build_certificate()
    require(accepted(certificate), "v0.97 certificate was not accepted")
    counts = certificate["record_counts"]
    require(
        counts["finite_family_operation_records"] == 36,
        "unexpected finite-family operation enumeration",
    )
    require(
        counts["finite_family_universal_property_records"] == 84,
        "unexpected finite-family universal-property enumeration",
    )
    require(
        counts["permutation_fold_records"] == 56,
        "unexpected permutation-fold enumeration",
    )
    require(
        counts["duplicate_invariance_records"] == 36,
        "unexpected duplicate-invariance enumeration",
    )
    require(
        counts["finite_family_root_independence_records"] == 576,
        "unexpected finite-family root-independence enumeration",
    )

    mutations: list[tuple[str, dict[str, object]]] = []

    tampered = copy.deepcopy(certificate)
    tampered["accepted"] = False
    mutations.append(("acceptance", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["source_binding"]["accepted"] = False
    mutations.append(("source binding", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["record_counts"]["finite_family_operation_records"] += 1
    mutations.append(("record count", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["laws"]["finite_meet_and_join_have_universal_properties"] = False
    mutations.append(("universal property", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["laws"]["fold_results_are_enumeration_order_independent"] = False
    mutations.append(("enumeration order", tampered))

    tampered = copy.deepcopy(certificate)
    tampered["laws"]["duplicate_family_members_do_not_change_results"] = False
    mutations.append(("duplicate invariance", tampered))

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
    tampered["authority_boundary"]["execution"] = True
    mutations.append(("execution authority", tampered))

    for label, mutation in mutations:
        require(not accepted(mutation), f"tamper test failed: {label}")

    print(
        json.dumps(
            {
                "checker": "MemoryOS v0.97 finite-family signature lattice",
                "accepted": True,
                "tamper_tests": [label for label, _ in mutations],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
