#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_memoryos_log_sobolev_hypercontractive_mixing_certificate_kernel_v0_1 import (
    issue_log_sobolev_hypercontractive_mixing_certificate,
)
from runtime.kuuos_memoryos_modified_log_sobolev_hellinger_separation_certificate_kernel_v0_1 import (
    SCHEMA_VERSION,
    _derive_observables,
    canonical_digest,
    issue_modified_log_sobolev_hellinger_separation_certificate,
)
from scripts.check_planos_memoryos_log_sobolev_hypercontractive_mixing_certificate_kernel_v0_1 import (
    build_reference_payload as build_memoryos_v059_payload,
)


def source_memoryos_v059_certificate() -> dict[str, Any]:
    result = issue_log_sobolev_hypercontractive_mixing_certificate(
        build_memoryos_v059_payload()
    )
    assert result["accepted"], result["blockers"]
    return result


def build_reference_payload() -> dict[str, Any]:
    source = source_memoryos_v059_certificate()
    return {
        "schema_version": SCHEMA_VERSION,
        "source_memoryos_v059_certificate": source,
        "claims": _derive_observables(source),
    }


def _resign(certificate: dict[str, Any]) -> None:
    certificate.pop("certificate_digest", None)
    certificate["certificate_digest"] = canonical_digest(certificate)


def main() -> int:
    payload = build_reference_payload()
    result = issue_modified_log_sobolev_hellinger_separation_certificate(payload)
    assert result["accepted"], result["blockers"]
    obs = result["observables"]

    assert obs["modified_log_sobolev_entropy_decay_record_count"] == 16
    assert obs["symbolic_hellinger_profile_record_count"] == 16
    assert obs["exact_separation_profile_record_count"] == 16
    assert obs["separation_threshold_record_count"] == 2
    assert obs["full_rank_transport_entropy_metric_record_count"] == 8
    assert obs["singular_atomic_entropy_metric_record_count"] == 4
    assert obs["rank_one_source_boundary_count"] == 3
    assert obs["entropy_decay_coefficient"] == {"numerator": 9, "denominator": 16}
    assert obs["all_entropy_decay_envelopes_exact"] is True
    assert obs["all_separation_values_exact"] is True
    assert obs["all_separation_thresholds_exact"] is True
    assert obs["all_hellinger_square_roots_symbolic"] is True
    assert obs["no_hellinger_floating_point_approximation"] is True
    assert obs["all_full_rank_transport_entropy_metrics_commute"] is True
    assert obs["singular_atomic_entropy_metrics_retained"] is True

    p_records = [
        item for item in obs["exact_separation_profile_records"]
        if item["distribution_id"] == "reference_p"
    ]
    expected = [
        {"numerator": 9, "denominator": 20},
        {"numerator": 27, "denominator": 80},
        {"numerator": 81, "denominator": 320},
        {"numerator": 243, "denominator": 1280},
        {"numerator": 729, "denominator": 5120},
        {"numerator": 2187, "denominator": 20480},
        {"numerator": 6561, "denominator": 81920},
        {"numerator": 19683, "denominator": 327680},
    ]
    assert [item["separation_to_uniform"] for item in p_records] == expected

    thresholds = {
        item["threshold_id"]: item
        for item in obs["separation_threshold_records"]
    }
    assert thresholds["reference-separation-three-twentieths"]["first_certified_time"] == 4
    assert thresholds["reference-separation-one-sixteenth"]["first_certified_time"] == 7

    tampered = copy.deepcopy(payload)
    tampered["claims"]["entropy_decay_coefficient"] = {"numerator": 1, "denominator": 2}
    rejected = issue_modified_log_sobolev_hellinger_separation_certificate(tampered)
    assert not rejected["accepted"]
    assert "claim_mismatch" in rejected["blockers"]

    tampered = copy.deepcopy(payload)
    tampered["source_memoryos_v059_certificate"]["observables"]["future_only"] = False
    _resign(tampered["source_memoryos_v059_certificate"])
    rejected = issue_modified_log_sobolev_hellinger_separation_certificate(tampered)
    assert not rejected["accepted"]
    assert "source_memoryos_v059_required_future_only" in rejected["blockers"]

    tampered = copy.deepcopy(payload)
    tampered["claims"]["candidate_selection_performed"] = True
    rejected = issue_modified_log_sobolev_hellinger_separation_certificate(tampered)
    assert not rejected["accepted"]
    assert "claim_mismatch" in rejected["blockers"]

    print(json.dumps({
        "status": "PASS",
        "schema_version": result["schema_version"],
        "certificate_digest": result["certificate_digest"],
        "entropy_decay_coefficient": obs["entropy_decay_coefficient"],
        "separation_profile_digest": canonical_digest(obs["exact_separation_profile_records"]),
        "hellinger_profile_digest": canonical_digest(obs["symbolic_hellinger_profile_records"]),
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
