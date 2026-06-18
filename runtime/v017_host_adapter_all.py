from runtime.v017_host_adapter_edges import run_edge_cases
from runtime.v017_host_adapter_io_kernel import main as run_io_kernel
from runtime.v017_host_adapter_kernel import main as run_main_kernel


def main() -> bool:
    assert run_main_kernel() is True
    assert run_edge_cases() is True
    assert run_io_kernel() is True
    print("PASS: cooperative host adapter v0.17 kernel")
    return True


if __name__ == "__main__":
    main()
