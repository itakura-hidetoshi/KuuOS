import json
import unittest

from runtime.kuuos_self_organization_review_packet_v0_85 import (
    REVIEW_PACKET_PATH,
    expected_packet_sources,
    expected_review_packet,
    load_review_packet,
    review_packet_issues,
    review_packet_json,
    verify_review_packet,
)


class KuuOSReviewPacketV085Test(unittest.TestCase):
    def test_review_packet_verifies(self):
        self.assertEqual((), review_packet_issues())
        self.assertTrue(verify_review_packet())

    def test_review_packet_path(self):
        self.assertEqual("status/self_organization_review_packet_v0_85.json", REVIEW_PACKET_PATH)

    def test_review_packet_matches_expected(self):
        self.assertEqual(expected_review_packet(), load_review_packet())

    def test_review_packet_json_round_trips(self):
        self.assertEqual(load_review_packet(), json.loads(review_packet_json()))

    def test_review_packet_is_review_only(self):
        packet = load_review_packet()
        self.assertEqual("review_packet_not_grant", packet["authority_boundary"])
        self.assertEqual("review_only", packet["packet_mode"])
        self.assertEqual("v0.86", packet["requested_next_stage"])
        self.assertEqual(expected_packet_sources(), packet["packet_sources"])


if __name__ == "__main__":
    unittest.main()
