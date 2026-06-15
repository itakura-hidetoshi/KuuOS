import pathlib
import tempfile
from scripts.delayed_credit_multihorizon_v0_11_smoke import first_two
from scripts.delayed_credit_multihorizon_v0_11_smoke_b import last_two
from scripts.delayed_credit_multihorizon_v0_11_stale import check_stale
from scripts.delayed_credit_multihorizon_v0_11_test_support import experiment_registry, root_packet

def run_scenario():
    with tempfile.TemporaryDirectory() as directory:
        runtime_root = pathlib.Path(directory)
        root = root_packet()
        registry = experiment_registry()
        portfolio, snap2 = first_two(runtime_root, root, registry)
        snap4 = last_two(runtime_root, root, registry, portfolio, snap2)
        check_stale(runtime_root, root, registry, snap4)
    return 0
