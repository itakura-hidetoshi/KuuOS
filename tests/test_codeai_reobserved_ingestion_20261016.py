"""Independent, fail-closed tests for renewed exact external evidence lineage."""
from __future__ import annotations

import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from runtime.kuuos_codeai_external_result_process_evidence_ingestion_schema_v0_1 import canonical_digest, PACK_DIGEST_FIELD
from scripts.build_codeai_external_result_process_evidence_ingestion_fixture_v0_1 import build_fixture
from scripts.check_codeai_external_result_process_evidence_ingestion_v0_1 import (
    verify_artifact, build_reobserved_fixture, validate_live_binding,
)


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


class ReobservedEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        d = self.root / 'codeai-bounded-official-external-artifacts'
        d.mkdir()
        report = {"sympy__sympy-20590": {
            "patch_successfully_applied": True, "resolved": False,
            "tests_status": {"FAIL_TO_PASS": {"success": [], "failure": ["private-example"]},
                             "PASS_TO_PASS": {"success": list(range(21)), "failure": []}}}}
        (d / 'report.json').write_text(json.dumps(report))
        (d / 'test_output.txt').write_bytes(b'private test data, never printed\n')
        (d / 'run_instance.log').write_bytes(b'private process data, never printed\n')
        file_hashes = {
            "report_digest": digest((d / 'report.json').read_bytes()),
            "test_output_digest": digest((d / 'test_output.txt').read_bytes()),
            "instance_log_digest": digest((d / 'run_instance.log').read_bytes()),
        }
        from scripts.build_codeai_bounded_official_harness_execution_fixture_v0_1 import build_fixture as bounded
        base = bounded()['observation']
        for k,v in file_hashes.items():
            base[k] = v
        base.pop('bounded_execution_observation_digest')
        observation_seal = canonical_digest(base)
        base['bounded_execution_observation_digest'] = observation_seal
        (self.root / 'codeai-bounded-official-external-observation-v0-1.json').write_text(json.dumps(base))
        self.binding = {
            "schema_version": "kuuos.external-evidence.reobservation.v1",
            "predecessor_workflow_run_id": 123456789,
            "predecessor_workflow_run_attempt": 1,
            "predecessor_workflow_head_sha": "a" * 40,
            "predecessor_artifact_id": 123456,
            "predecessor_artifact_name": "codeai-bounded-official-external-v0-1-123456789-1",
            "predecessor_artifact_digest": "b" * 64,
            "external_observation_digest": observation_seal,
            "prediction_digest": build_fixture()['request']['prediction_digest'],
            **file_hashes,
        }
        self.metadata = self.root/'artifact-metadata.json'
        self.run_metadata = self.root/'run-metadata.json'
        self.meta = {
            "id": self.binding['predecessor_artifact_id'],
            "name": self.binding['predecessor_artifact_name'],
            "digest": 'sha256:'+self.binding['predecessor_artifact_digest'],
            "expired": False,
            "workflow_run": {"id":self.binding['predecessor_workflow_run_id'], "head_sha":self.binding['predecessor_workflow_head_sha']},
        }
        self.run = {
            "id": self.binding['predecessor_workflow_run_id'],
            "head_sha": self.binding['predecessor_workflow_head_sha'],
            "run_attempt": 1, "status": "completed", "conclusion": "success",
            "event": "pull_request",
            "repository": {"full_name":"itakura-hidetoshi/KuuOS"},
        }
        self.flush()

    def flush(self):
        self.metadata.write_text(json.dumps(self.meta))
        self.run_metadata.write_text(json.dumps(self.run))

    def verify(self, binding=None):
        return verify_artifact(self.root, self.metadata, live_binding=self.binding if binding is None else binding,
                               workflow_metadata=self.run_metadata)

    def test_new_binding_admitted_without_mutating_historical_fixture(self):
        old = build_fixture()
        old_digest = old['ingestion_pack'][PACK_DIGEST_FIELD]
        verified = self.verify()
        fresh = build_reobserved_fixture(self.binding)
        self.assertTrue(verified['resolved'] is False)
        self.assertNotEqual(fresh['ingestion_pack'][PACK_DIGEST_FIELD], old_digest)
        self.assertEqual(build_fixture()['ingestion_pack'][PACK_DIGEST_FIELD], old_digest)
        self.assertEqual(fresh['request']['predecessor_workflow_run_id'],123456789)
        self.assertFalse(fresh['receipt']['correctness_claimed'])
        self.assertFalse(fresh['receipt']['git_authority_granted'])

    def test_changed_run_head_rejected(self):
        self.run['head_sha'] = 'c'*40;self.flush()
        with self.assertRaises(SystemExit): self.verify()

    def test_changed_artifact_id_rejected(self):
        self.meta['id'] += 1;self.flush()
        with self.assertRaises(SystemExit): self.verify()

    def test_changed_artifact_name_rejected(self):
        self.meta['name'] = 'different';self.flush()
        with self.assertRaises(SystemExit): self.verify()

    def test_wrong_digest_rejected(self):
        self.meta['digest'] = 'sha256:'+'e'*64;self.flush()
        with self.assertRaises(SystemExit): self.verify()

    def test_expired_artifact_rejected(self):
        self.meta['expired'] = True;self.flush()
        with self.assertRaises(SystemExit): self.verify()

    def test_incomplete_run_rejected(self):
        self.run['status'] = 'in_progress';self.flush()
        with self.assertRaises(SystemExit): self.verify()

    def test_failed_run_rejected(self):
        self.run['conclusion'] = 'failure';self.flush()
        with self.assertRaises(SystemExit): self.verify()

    def test_wrong_attempt_rejected(self):
        self.run['run_attempt'] = 2;self.flush()
        with self.assertRaises(SystemExit): self.verify()

    def test_observation_tampered_rejected(self):
        p=self.root/'codeai-bounded-official-external-observation-v0-1.json'
        obj=json.loads(p.read_text());obj['resolved']=True;p.write_text(json.dumps(obj))
        with self.assertRaises(SystemExit): self.verify()

    def test_observation_wrong_prediction_rejected_even_when_resealed(self):
        p=self.root/'codeai-bounded-official-external-observation-v0-1.json'
        obj=json.loads(p.read_text());obj.pop('bounded_execution_observation_digest')
        obj['prediction_digest']='c'*64;obj['bounded_execution_observation_digest']=canonical_digest(obj)
        p.write_text(json.dumps(obj))
        with self.assertRaises(SystemExit): self.verify()

    def test_observation_forbidden_authority_rejected_even_when_resealed(self):
        p=self.root/'codeai-bounded-official-external-observation-v0-1.json'
        obj=json.loads(p.read_text());obj.pop('bounded_execution_observation_digest')
        obj['git_authority']=True;obj['bounded_execution_observation_digest']=canonical_digest(obj)
        p.write_text(json.dumps(obj))
        with self.assertRaises(SystemExit): self.verify()

    def test_mismatched_report_rejected(self):
        p=self.root/'codeai-bounded-official-external-artifacts/report.json'
        p.write_text('{}')
        with self.assertRaises(SystemExit): self.verify()

    def test_extra_binding_field_rejected(self):
        b=dict(self.binding, arbitrary='value')
        with self.assertRaises(SystemExit): validate_live_binding(b)

    def test_binding_bad_run_attempt_rejected(self):
        b=dict(self.binding, predecessor_workflow_run_attempt=0)
        with self.assertRaises(SystemExit): validate_live_binding(b)

    def test_original_unavailable_binding_not_replaced_implicitly(self):
        self.assertEqual(build_fixture()['request']['predecessor_workflow_run_id'],29894633457)
        self.assertEqual(build_fixture()['request']['predecessor_artifact_id'],8520539325)

if __name__=='__main__': unittest.main()
