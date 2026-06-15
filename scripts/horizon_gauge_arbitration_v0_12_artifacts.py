import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]


def check_artifacts():
    formal = (
        ROOT / "formal/KUOS/OpenHorizon/HorizonGaugeArbitrationV0_12.lean"
    ).read_text(encoding="utf-8")
    for token in (
        "connectionResidual",
        "arbitrationCurvature",
        "transportWithFloor",
        "transport_floor_preserved",
        "oneHorizonChild",
        "arbitrationHolonomy_strict",
    ):
        assert token in formal
    manifest = json.loads(
        (ROOT / "manifests/kuuos_horizon_gauge_arbitration_v0_12.json").read_text(
            encoding="utf-8"
        )
    )
    for group in ("runtime", "scripts", "formal", "docs", "examples", "workflows"):
        for relative in manifest[group]:
            assert (ROOT / relative).is_file(), relative
