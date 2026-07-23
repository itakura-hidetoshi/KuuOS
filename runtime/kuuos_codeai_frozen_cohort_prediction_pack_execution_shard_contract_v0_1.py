from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any

SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Frozen Cohort Prediction-Pack and Execution-Shard Contract v0.1"
DECISION = "frozen_cohort_prediction_pack_execution_shard_contract_admitted"
COHORTS = (
    "baseline-deterministic-patch",
    "codeai-full",
    "ablation-no-repair-memory",
    "ablation-no-specialist-routing",
    "ablation-no-evidence-weighted-selection",
)
TARGET = 100
SHARD_SIZE = 10
PREDECESSOR_MAIN = "083ee7ef65d53bd1a8e231c73b82e4946dd1eaf7"
PREDECESSOR_PACK = "aee1ad7919af50124c79cb27b86fc8c6d9a54192237e963b62e1869d986fdf23"
PREDECESSOR_RECEIPT = "1629e68f87175bf0ce7393e652d58df6bd3611832db84995feb1566644fd2ce4"
SAMPLE_BINDING = "d3162c78a1552f22411b87c019271cfbc692ffa048a039067f4c83c65d42012c"
HOLDOUT = "b88c73c43b0a14c23cdd58269ccba3c5437ffba3651c0f3dc2ceb7aa7ebcf2e6"
COMPARISON_CONTRACT = "f99ae02bd48c51563060a7b0de6be53f9ea98278efe0e837ab73bdd77e4c7016"
SMOKE_PREDICTION = "9a2aeff25ca565214ecbae781f20df4c23eea20db72b135702aa56d5de238050"


def digest(value: Any) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return hashlib.sha256(data).hexdigest()


def _variant(cohort: str) -> dict[str, Any]:
    flags = {
        COHORTS[0]: (False, False, False, True),
        COHORTS[1]: (True, True, True, False),
        COHORTS[2]: (False, True, True, False),
        COHORTS[3]: (True, False, True, False),
        COHORTS[4]: (True, True, False, False),
    }[cohort]
    material = {
        "cohort": cohort,
        "repair_memory": flags[0],
        "specialist_routing": flags[1],
        "evidence_weighted_selection": flags[2],
        "deterministic_baseline": flags[3],
        "sample_binding": SAMPLE_BINDING,
        "holdout": HOLDOUT,
    }
    return {**material, "variant_digest": digest(material)}


def build_contract() -> dict[str, Any]:
    slots = [digest({"sample_binding": SAMPLE_BINDING, "holdout": HOLDOUT, "slot": i}) for i in range(TARGET)]
    variants = [_variant(c) for c in COHORTS]
    packs = []
    shards = []
    for variant in variants:
        cohort = variant["cohort"]
        smoke = 1 if cohort == "codeai-full" else 0
        pack_material = {
            "cohort": cohort,
            "variant_digest": variant["variant_digest"],
            "target_predictions": TARGET,
            "authentic_predictions": 0,
            "smoke_predictions": smoke,
            "smoke_prediction_digest": SMOKE_PREDICTION if smoke else None,
            "smoke_counts_as_performance": False,
            "label_only_relabeling": False,
            "gold_derived": False,
            "raw_test_names": False,
            "raw_logs": False,
            "complete": False,
        }
        pack = {**pack_material, "pack_digest": digest(pack_material)}
        packs.append(pack)
        for shard_index in range(TARGET // SHARD_SIZE):
            start = shard_index * SHARD_SIZE
            shards.append({
                "shard_id": f"{cohort}-{shard_index:02d}",
                "cohort": cohort,
                "start_slot": start,
                "end_slot_exclusive": start + SHARD_SIZE,
                "sample_count": SHARD_SIZE,
                "pack_digest": pack["pack_digest"],
                "state": "pending-prediction-pack",
                "external_harness_only": True,
            })
    contract_material = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "decision": DECISION,
        "predecessor_main": PREDECESSOR_MAIN,
        "predecessor_comparison_pack": PREDECESSOR_PACK,
        "predecessor_receipt": PREDECESSOR_RECEIPT,
        "sample_binding": SAMPLE_BINDING,
        "holdout_partition": HOLDOUT,
        "comparison_contract": COMPARISON_CONTRACT,
        "cohorts": variants,
        "opaque_slot_digests": slots,
        "prediction_packs": packs,
        "execution_shards": shards,
        "dataset_materialized": False,
        "prediction_packs_complete": False,
        "execution_shards_ready": False,
        "external_execution_ready": False,
        "external_execution_authority": False,
        "kernel_execution_authority": False,
        "raw_gold_visible": False,
        "raw_test_names_visible": False,
        "raw_logs_visible": False,
        "repository_mutation_authority": False,
        "git_authority": False,
        "correctness_claimed": False,
        "performance_claimed": False,
    }
    return {**contract_material, "contract_digest": digest(contract_material)}


@dataclass(frozen=True)
class Validation:
    admitted: bool
    reasons: tuple[str, ...]
    ready: bool


def validate_contract(contract: dict[str, Any]) -> Validation:
    reasons: list[str] = []
    material = {k: v for k, v in contract.items() if k != "contract_digest"}
    if digest(material) != contract.get("contract_digest"):
        return Validation(False, ("contract digest mismatch",), False)
    if contract.get("decision") != DECISION:
        reasons.append("decision mismatch")
    if tuple(v.get("cohort") for v in contract.get("cohorts", ())) != COHORTS:
        reasons.append("cohort registry mismatch")
    slots = contract.get("opaque_slot_digests", ())
    if len(slots) != TARGET or len(set(slots)) != TARGET:
        reasons.append("opaque sample-slot ledger invalid")
    packs = {p.get("cohort"): p for p in contract.get("prediction_packs", ())}
    if set(packs) != set(COHORTS):
        reasons.append("prediction-pack registry mismatch")
    else:
        for cohort in COHORTS:
            pack = packs[cohort]
            if pack["target_predictions"] != TARGET:
                reasons.append(f"target mismatch:{cohort}")
            if pack["authentic_predictions"] > TARGET:
                reasons.append(f"authentic count overflow:{cohort}")
            if pack["label_only_relabeling"]:
                reasons.append(f"label-only relabeling:{cohort}")
            if pack["gold_derived"] or pack["raw_test_names"] or pack["raw_logs"]:
                reasons.append(f"evidence boundary breach:{cohort}")
            if pack["smoke_predictions"] and pack["smoke_counts_as_performance"]:
                reasons.append(f"smoke promoted to performance:{cohort}")
            if pack["complete"] != (pack["authentic_predictions"] == TARGET):
                reasons.append(f"pack completeness mismatch:{cohort}")
    shards = contract.get("execution_shards", ())
    if len(shards) != 50:
        reasons.append("shard count mismatch")
    else:
        by_cohort = {c: [] for c in COHORTS}
        for shard in shards:
            if shard.get("cohort") not in by_cohort:
                reasons.append("unknown shard cohort")
                continue
            by_cohort[shard["cohort"]].append(shard)
            if not shard.get("external_harness_only"):
                reasons.append(f"kernel shard:{shard.get('shard_id')}")
        for cohort, items in by_cohort.items():
            items.sort(key=lambda x: x["start_slot"])
            expected = 0
            for shard in items:
                if shard["start_slot"] != expected:
                    reasons.append(f"shard gap or overlap:{cohort}")
                if shard["sample_count"] != SHARD_SIZE:
                    reasons.append(f"shard size mismatch:{cohort}")
                if shard["end_slot_exclusive"] - shard["start_slot"] != SHARD_SIZE:
                    reasons.append(f"shard range mismatch:{cohort}")
                expected = shard["end_slot_exclusive"]
            if expected != TARGET:
                reasons.append(f"shard coverage mismatch:{cohort}")
    for field in (
        "external_execution_authority", "kernel_execution_authority", "raw_gold_visible",
        "raw_test_names_visible", "raw_logs_visible", "repository_mutation_authority",
        "git_authority", "correctness_claimed", "performance_claimed",
    ):
        if contract.get(field):
            reasons.append(f"authority boundary breach:{field}")
    ready = bool(
        contract.get("dataset_materialized")
        and contract.get("prediction_packs_complete")
        and contract.get("execution_shards_ready")
    )
    if contract.get("external_execution_ready") != ready:
        reasons.append("readiness mismatch")
    return Validation(not reasons, tuple(sorted(set(reasons))), ready)


if __name__ == "__main__":
    print(json.dumps(build_contract(), indent=2, sort_keys=True))
