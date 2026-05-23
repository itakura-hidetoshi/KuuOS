import unittest

from runtime.kuuos_runtime_daemon_v0_1 import KuuOSDaemonResult


class QiProcessTensorClosedLoopReceiptDaemonResultFieldsTests(unittest.TestCase):
    def test_daemon_result_contains_closed_loop_receipt_fields(self):
        fields = KuuOSDaemonResult.__dataclass_fields__
        self.assertIn("qi_process_tensor_closed_loop_receipt_path", fields)
        self.assertIn("closed_loop_receipt_status", fields)
        self.assertIn("closed_loop_next_state", fields)
        self.assertIn("closed_loop_observation_required", fields)
        self.assertIn("closed_loop_compact_required", fields)


if __name__ == "__main__":
    unittest.main()
