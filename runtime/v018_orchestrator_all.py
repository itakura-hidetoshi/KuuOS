from runtime.v018_orchestrator_edges import run_edge_cases
from runtime.v018_orchestrator_hardening import run_hardening_cases
from runtime.v018_orchestrator_io_kernel import main as run_io_kernel
from runtime.v018_orchestrator_kernel import main as run_main_kernel


def main() -> bool:
    assert run_main_kernel() is True
    assert run_edge_cases() is True
    assert run_hardening_cases() is True
    assert run_io_kernel() is True
    print("PASS: durable host invocation orchestrator v0.18 kernel")
    return True


if __name__ == "__main__":
    main()
