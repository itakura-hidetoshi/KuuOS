#!/usr/bin/env python3
from __future__ import annotations

from runtime.kuuos_planos_finite_temperature_concentration_certificate_kernel_v0_1 import (
    STATUS_READY,
    build_finite_temperature_concentration_certificate,
)


def main() -> int:
    source = {
        "minimal_action_candidate_ids": ["repair"],
        "zero_temperature_limit_distribution": {"repair": 1.0, "hold": 0.0, "reroute": 0.0},
        "authority_invariance_preserved": True,
        "history_read_only": True,
        "future_only": True,
        "active_now": False,
        "execution_permission": False,
    }
    actions = {"repair": 0.2, "hold": 1.2, "reroute": 1.7}
    result = build_finite_temperature_concentration_certificate(source, actions, temperature=0.1, epsilon=0.001)
    assert result.status == STATUS_READY
    assert result.blockers == []
    cert = result.certificate
    assert cert is not None
    assert cert["minimal_action_candidate_ids"] == ["repair"]
    assert abs(sum(cert["normalized_candidate_mass"].values()) - 1.0) < 1e-9
    assert cert["nonminimal_support_mass"] <= cert["nonminimal_mass_upper_bound"] + 1e-12
    assert cert["epsilon_concentration_certified"] is True
    assert cert["authority_invariance_preserved"] is True
    assert cert["history_read_only"] is True
    assert cert["future_only"] is True
    assert cert["active_now"] is False
    assert cert["execution_permission"] is False

    tied = build_finite_temperature_concentration_certificate(
        source,
        {"repair": 0.2, "hold": 0.2, "reroute": 1.2},
        temperature=0.1,
        epsilon=0.001,
    )
    assert tied.status == STATUS_READY
    assert tied.certificate is not None
    assert tied.certificate["minimal_action_candidate_ids"] == ["hold", "repair"]

    blocked = [
        build_finite_temperature_concentration_certificate({}, actions, 0.1, 0.1),
        build_finite_temperature_concentration_certificate(source, {}, 0.1, 0.1),
        build_finite_temperature_concentration_certificate(source, actions, 0.0, 0.1),
        build_finite_temperature_concentration_certificate(source, actions, 0.1, 0.0),
        build_finite_temperature_concentration_certificate(source, {"repair": -1.0}, 0.1, 0.1),
    ]
    for item in blocked:
        assert item.status != STATUS_READY
        assert item.blockers
        assert item.certificate is None

    print("PASS: PlanOS finite-temperature concentration certificate kernel v0.1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
