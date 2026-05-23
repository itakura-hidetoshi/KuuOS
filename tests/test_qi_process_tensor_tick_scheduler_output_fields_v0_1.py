import unittest

from runtime.kuuos_runtime_daemon_v0_1 import KuuOSDaemonResult


class QiProcessTensorTickSchedulerOutputFieldsTests(unittest.TestCase):
    def test_daemon_result_contains_scheduler_fields(self):
        fields = KuuOSDaemonResult.__dataclass_fields__
        self.assertIn("qi_process_tensor_tick_scheduler_path", fields)
        self.assertIn("scheduled_next_sleep_seconds_hint", fields)
        self.assertIn("scheduled_next_max_ticks_hint", fields)
        self.assertIn("scheduled_next_max_steps_per_tick_hint", fields)
        self.assertIn("scheduled_compact_before_next_tick", fields)
        self.assertIn("scheduled_reobserve_before_next_tick", fields)
        self.assertIn("scheduled_hold_until_observation", fields)


if __name__ == "__main__":
    unittest.main()
