"""v0.52: paired HMAC receipts are locally integrity checked, NOT issuer proof."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import hmac
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from runtime import (
    kuuos_lean_python_local_mac_bound_plan_claims_v0_52 as subject,
    kuuos_verifyos_middle_way_conditional_continuity_verification_v0_4 as verify,
    kuuos_planos_middle_way_bounded_synthesis_intake_kernel_v0_1 as plan,
)
from runtime.kuuos_lean_python_middle_way_verify_plan_six_routes_v0_45 import (
    NO_DATA, BLOCKED, ROUTES,
)
from tests.lean_python_extensions.test_original_verify_plan_certificate_seam_v0_48 import (
    native_certificates,
)
from tests.lean_python_extensions.test_two_declared_plan_result_claims_v0_51 import (
    two_claims,
)
from scripts import check_kuuos_lean_python_mac_bound_claims_sources_v0_52 as pins

# Only test fixtures hold shared keys. Neither source kernels nor verifier
# generate or retrieve keys from an untrusted envelope.
KEYS = {"key-a": b"A"*32, "key-b": b"B"*32}
CONTEXT = "research-only-v052"
SEQ = {"first": 7, "second": 8}
NONCE = {"first": "00112233445566778899aabbccddeeff",
         "second": "ffeeddccbbaa99887766554433221100"}


def fixtures_mac_claims(claims: dict, keys: dict = KEYS, *, context=CONTEXT,
                        seq=SEQ, nonce=NONCE) -> dict:
    out = {}
    for slot, keyid in (("first", "key-a"), ("second", "key-b")):
        r = {"schema_version": subject.SCHEMA, "key_id": keyid,
             "context_id": context, "sequence": seq[slot],
             "nonce_hex": nonce[slot]}
        message = {"domain": subject.DOMAIN,
                   "schema_version": subject.SCHEMA, "slot": slot,
                   "key_id": keyid, "context_id": r["context_id"],
                   "sequence": r["sequence"], "nonce_hex": r["nonce_hex"],
                   "declared_claim": claims[slot]}
        canonical = json.dumps(message, sort_keys=True, ensure_ascii=True,
                               separators=(",", ":"), allow_nan=False).encode("ascii")
        r["mac_sha256"] = hmac.new(keys[keyid], canonical, hashlib.sha256).hexdigest()
        out[slot] = r
    return out


class LocalMacBoundClaimsV052Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.native = {route: native_certificates(route)
                      for route, _, _, _ in ROUTES}

    def _inputs(self, kind="retain"):
        v, p = deepcopy(self.native[kind])
        claims = two_claims(v, p)
        receipts = fixtures_mac_claims(claims)
        return v, p, claims, receipts

    def _audit(self, v, p, claims, receipts, keys=KEYS,
               context=CONTEXT, sequences=SEQ):
        return subject.audit_locally_mac_bound_claims(
            v, p, claims, receipts, verification_keys=keys,
            expected_context=context, expected_sequences=sequences)

    def test_all_six_original_routes_mac_check_only_local_proposal(self):
        for route, _, _, _ in ROUTES:
            with self.subTest(route=route):
                v, p, c, r = self._inputs(route)
                z = self._audit(v, p, c, r)
                self.assertEqual(z.status, subject.MAC_CHECKED_PROPOSAL, z.issues)
                self.assertTrue(z.local_mac_verified)
                self.assertTrue(z.bounded_pairwise_agreement)
                self.assertFalse(z.independent_issuers_authenticated)
                self.assertFalse(z.original_result_sets_observed)
                self.assertFalse(z.original_lean_equality_proved)
                self.assertFalse(z.causal_event_identity_proved)
                self.assertFalse(z.host_execution_authorized)
                self.assertEqual(z.original_plan_result_state, NO_DATA)

    def test_mac_authenticated_disagreement_retains_lineage_obstruction(self):
        v, p, c, _ = self._inputs()
        c["second"]["supplied_result_evidence"]["resulting_lineage_digests"].append("zz-history")
        r = fixtures_mac_claims(c)
        z = self._audit(v, p, c, r)
        self.assertEqual(z.status, subject.MAC_CHECKED_OBSTRUCTION)
        self.assertEqual(z.conflicting_fields, ("resulting_lineage_digests",))
        self.assertTrue(z.local_mac_verified)
        self.assertFalse(z.bounded_pairwise_agreement)

    def test_mac_authenticated_multiple_obstructions_are_preserved(self):
        v, p, c, _ = self._inputs("suspend")
        for field in ("resulting_dissent_evidence_digests",
                      "resulting_minority_evidence_digests"):
            c["second"]["supplied_result_evidence"][field].append("zz-append")
        z = self._audit(v, p, c, fixtures_mac_claims(c))
        self.assertEqual(z.status, subject.MAC_CHECKED_OBSTRUCTION)
        self.assertEqual(len(z.conflicting_fields), 2)

    def test_missing_mac_is_no_data(self):
        v, p, c, _ = self._inputs()
        self.assertEqual(self._audit(v, p, c, None).status, NO_DATA)

    def test_unprovisioned_verification_keys_is_no_data(self):
        v, p, c, r = self._inputs()
        self.assertEqual(self._audit(v, p, c, r, None).status, NO_DATA)

    def test_wrong_mac_for_tampered_result_is_blocked(self):
        v, p, c, r = self._inputs()
        c["second"]["supplied_result_evidence"]["resulting_lineage_digests"].append("zz-tamper")
        self.assertEqual(self._audit(v, p, c, r).status, BLOCKED)

    def test_wrong_provisioned_key_fails_mac(self):
        v, p, c, r = self._inputs()
        self.assertEqual(self._audit(v, p, c, r,
                                     {"key-a": b"Q"*32, "key-b": KEYS["key-b"]}).status, BLOCKED)

    def test_wrong_context_cannot_reuse_authenticated_tag(self):
        v, p, c, r = self._inputs()
        self.assertEqual(self._audit(v, p, c, r, context="different-context").status,
                         BLOCKED)

    def test_wrong_independent_sequence_blocks(self):
        v, p, c, r = self._inputs()
        self.assertEqual(self._audit(v, p, c, r, sequences={"first": 7, "second": 9}).status,
                         BLOCKED)

    def test_missing_verifier_context_is_no_data(self):
        v, p, c, r = self._inputs()
        self.assertEqual(self._audit(v, p, c, r, context=None).status, NO_DATA)

    def test_unprovisioned_key_id_is_no_data(self):
        v, p, c, r = self._inputs()
        r["first"]["key_id"] = "unknown-key"
        self.assertEqual(self._audit(v, p, c, r).status, NO_DATA)

    def test_duplicate_key_id_disallowed(self):
        v, p, c, r = self._inputs()
        r["second"]["key_id"] = "key-a"
        self.assertEqual(self._audit(v, p, c, r).status, BLOCKED)

    def test_duplicate_nonce_disallowed_even_with_mac(self):
        v, p, c, r = self._inputs()
        r["second"]["nonce_hex"] = r["first"]["nonce_hex"]
        self.assertEqual(self._audit(v, p, c, r).status, BLOCKED)

    def test_receipt_schema_forged_authority_blocked(self):
        v, p, c, r = self._inputs()
        r["first"]["host_authority"] = True
        self.assertEqual(self._audit(v, p, c, r).status, BLOCKED)

    def test_integer_type_not_accepted_for_mac_tag(self):
        v, p, c, r = self._inputs()
        r["first"]["mac_sha256"] = 1
        self.assertEqual(self._audit(v, p, c, r).status, BLOCKED)

    def test_weak_key_material_not_accepted(self):
        v, p, c, r = self._inputs()
        self.assertEqual(self._audit(v, p, c, r,
                                     {"key-a": b"short", "key-b": KEYS["key-b"]}).status,
                         BLOCKED)

    def test_unknown_claim_permission_is_blocked_before_mac(self):
        v, p, c, r = self._inputs()
        c["first"]["authorized"] = True
        self.assertEqual(self._audit(v, p, c, r).status, BLOCKED)

    def test_finite_bad_envelope_type_blocked(self):
        v, p, c, r = self._inputs()
        for bad in ([], object(), "signed"):
            self.assertEqual(self._audit(v, p, c, bad).status, BLOCKED)

    def test_source_and_mac_receipts_read_only(self):
        v, p, c, r = self._inputs()
        before = deepcopy((v, p, c, r))
        self.assertEqual(self._audit(v, p, c, r).status, subject.MAC_CHECKED_PROPOSAL)
        self.assertEqual((v, p, c, r), before)

    def test_native_kernel_does_not_execute_during_audit(self):
        v, p, c, r = self._inputs()
        with patch.object(verify, "build_verifyos_middle_way_conditional_continuity_certificate",
                          side_effect=AssertionError("called verify")), patch.object(
                plan, "build_planos_middle_way_bounded_synthesis_intake_certificate",
                side_effect=AssertionError("called plan")):
            self.assertEqual(self._audit(v, p, c, r).status, subject.MAC_CHECKED_PROPOSAL)

    def test_same_pair_replay_without_ledger_remains_possible_not_certified(self):
        v, p, c, r = self._inputs()
        a = self._audit(v, p, c, r)
        b = self._audit(v, p, c, r)
        self.assertEqual(a.status, subject.MAC_CHECKED_PROPOSAL)
        self.assertEqual(b.status, subject.MAC_CHECKED_PROPOSAL)
        self.assertFalse(b.persistent_replay_protection_proved)

    def test_source_checker_runs_on_ci(self):
        self.assertEqual(pins.check(), ())

    def test_tampered_original_plan_source_rejected(self):
        target = pins.ROOT / "formal/KUOS/PlanOS/MiddleWayBoundedSynthesisIntakeV1_03.lean"
        old = Path.read_bytes
        def tampered(path):
            data = old(path)
            return data + b"\n" if path == target else data
        with patch.object(Path, "read_bytes", tampered):
            self.assertIn("changed_pinned_source:formal/KUOS/PlanOS/MiddleWayBoundedSynthesisIntakeV1_03.lean",
                          pins.check())


if __name__ == "__main__":
    unittest.main()
