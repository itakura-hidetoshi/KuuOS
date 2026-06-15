import pathlib
import json

ROOT = pathlib.Path(__file__).resolve().parents[1]

def check_artifacts():
    formal = (ROOT / "formal/KUOS/OpenHorizon/DelayedCreditMultiHorizonV0_11.lean").read_text(encoding="utf-8")
    for token in ("Horizon", "decayCredit", "updateCredit", "aggregateHorizonSupport", "credit_nonnegative", "credit_upper_bound", "oneRegretChild"):
        assert token in formal
    manifest = json.loads((ROOT / "manifests/kuuos_delayed_credit_multihorizon_v0_11.json").read_text(encoding="utf-8"))
    for group in ("runtime", "scripts", "formal", "docs", "examples", "workflows"):
        for relative in manifest[group]:
            assert (ROOT / relative).is_file(), relative
