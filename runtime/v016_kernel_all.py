from runtime.v016_kernel_check import main as run_main_flow
from runtime.v016_kernel_edges import run_edge_cases


def main():
    assert run_main_flow() is True
    assert run_edge_cases() is True
    print("PASS: cooperative execution supervisor v0.16 kernel")


if __name__ == "__main__":
    main()
