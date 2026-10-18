"""Offline synthetic regressions for the public CI notification transport."""
import copy
import io
import json
import pathlib
import tempfile
import unittest
import urllib.error
from unittest.mock import patch

from runtime import kuuos_github_public_ci_completion_poller_v1_2 as poller


def run(run_id, conclusion='success', status='completed'):
    return {'id': run_id, 'name': poller.SOURCE_WORKFLOW_NAME,
            'event': 'pull_request', 'status': status, 'conclusion': conclusion,
            'run_attempt': 1, 'head_sha': 'a' * 40, 'head_branch': 'synthetic/test',
            'head_repository': {'full_name': poller.SOURCE_REPO},
            'pull_requests': [{'number': 1, 'base': {'ref': poller.CANONICAL_BASE}}]}


def jobs(run_id=101):
    return {'total_count': 1, 'jobs': [{'id': run_id * 10, 'run_id': run_id, 'head_sha': 'a' * 40, 'run_attempt': 1, 'name': poller.REQUIRED_JOB,
            'status': 'completed', 'conclusion': 'success', 'steps': [
            {'name': poller.REQUIRED_STEP, 'status': 'completed', 'conclusion': 'success'}]}]}


class ReliabilityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.state = pathlib.Path(self.temp.name) / 'state.json'
        poller._save_state(self.state, 100)

    def poll(self, runs, job_data=None, send=None):
        def get(url):
            if '/jobs?' in url:
                return jobs(int(url.split('/runs/')[1].split('/')[0])) if job_data is None else copy.deepcopy(job_data)
            return {'total_count': len(runs), 'workflow_runs': copy.deepcopy(runs)}
        with patch.object(poller, '_http_json', side_effect=get), patch.object(
                poller, '_post_self_dispatch', side_effect=send) as dispatch:
            result = poller.poll_once(state_file=self.state, target_repo='example/target', dispatch_token='synthetic')
            return result, dispatch

    def test_missing_state_cannot_silently_skip_completed_runs(self):
        self.state.unlink()
        with self.assertRaisesRegex(RuntimeError, 'state_missing'):
            self.poll([run(101)])
        self.assertFalse(self.state.exists())

    def test_corrupt_state_cannot_silently_skip_completed_runs(self):
        self.state.write_text('{broken')
        with self.assertRaisesRegex(RuntimeError, 'state_invalid'):
            self.poll([run(101)])
        self.assertEqual(self.state.read_text(), '{broken')

    def test_wrong_source_state_is_rejected(self):
        value = json.loads(self.state.read_text())
        value['source_repo'] = 'other/repository'
        self.state.write_text(json.dumps(value))
        with self.assertRaisesRegex(RuntimeError, 'state_identity_mismatch'):
            self.poll([run(101)])

    def test_cancelled_zero_jobs_is_quarantined_without_dispatch(self):
        summary, dispatch = self.poll([run(101, 'cancelled')], {'total_count': 0, 'jobs': []})
        self.assertEqual(summary.quarantined_run_ids, [101])
        self.assertEqual(summary.dispatched_run_ids, [])
        dispatch.assert_not_called()
        checkpoint = json.loads(self.state.read_text())
        self.assertEqual(checkpoint['last_processed_run_id'], 101)
        self.assertEqual(checkpoint['last_outcome']['reason'], 'cancelled_without_required_job')
        self.assertFalse(summary.wakeup_is_success_evidence)

    def test_success_without_required_job_remains_blocked(self):
        with self.assertRaisesRegex(RuntimeError, 'required_job_cardinality:0'):
            self.poll([run(101)], {'total_count': 0, 'jobs': []})
        self.assertEqual(poller._load_state(self.state), 100)

    def test_cancelled_with_exact_success_job_preserves_cancelled_conclusion(self):
        summary, dispatch = self.poll([run(101, 'cancelled')])
        self.assertEqual(summary.dispatched_run_ids, [101])
        self.assertEqual(dispatch.call_args.args[2]['completion']['conclusion'], 'cancelled')

    def test_partial_dispatch_failure_keeps_confirmed_progress(self):
        def send(repo, token, payload):
            rid = payload.get('completion', payload)['run_id']
            if rid == 102:
                raise RuntimeError('synthetic_dispatch_failure')
        with self.assertRaisesRegex(RuntimeError, 'synthetic_dispatch_failure'):
            self.poll([run(101), run(102)], send=send)
        self.assertEqual(poller._load_state(self.state), 101)

    def test_pending_older_run_prevents_later_completion_skips(self):
        summary, dispatch = self.poll([run(101, None, 'in_progress'), run(102)])
        self.assertEqual(summary.final_run_id, 100)
        self.assertEqual(summary.pending_run_ids, [101])
        dispatch.assert_not_called()
        summary, dispatch = self.poll([run(101), run(102)])
        self.assertEqual(summary.dispatched_run_ids, [101, 102])

    def test_incomplete_jobs_response_is_not_a_cancelled_quarantine(self):
        with self.assertRaisesRegex(RuntimeError, 'jobs_response_incomplete'):
            self.poll([run(101, 'cancelled')], {'total_count': 1, 'jobs': []})
        self.assertEqual(poller._load_state(self.state), 100)

    def test_page_overflow_does_not_skip_unlisted_runs(self):
        page1 = [run(i) for i in range(201, 301)]
        page2 = [run(i) for i in range(101, 201)]
        # A complete older boundary must be seen before processing newer entries.
        def get(url):
            if '/jobs?' in url:
                return jobs(int(url.split('/runs/')[1].split('/')[0]))
            return {'total_count': 201, 'workflow_runs': [run(100)] if 'page=3' in url else page2 if 'page=2' in url else page1}
        with patch.object(poller, '_http_json', side_effect=get), patch.object(poller, '_post_self_dispatch'):
            summary = poller.poll_once(state_file=self.state, target_repo='example/target', dispatch_token='synthetic')
        self.assertEqual(summary.dispatched_run_ids[0], 101)
        self.assertEqual(len(summary.dispatched_run_ids), 200)

    def test_durable_state_is_authoritative_and_saved_after_each_dispatch(self):
        class Store:
            def __init__(self, state):
                self.value = state
                self.saved = []
            def load(self):
                return copy.deepcopy(self.value)
            def save(self, value):
                self.value = copy.deepcopy(value)
                self.saved.append(value['last_processed_run_id'])
        store = Store(json.loads(self.state.read_text()))
        self.state.unlink()  # An ephemeral/cache miss cannot reset durable state.
        def get(url):
            return jobs(int(url.split('/runs/')[1].split('/')[0])) if '/jobs?' in url else {'total_count': 2, 'workflow_runs': [run(101), run(102)]}
        def send(repo, token, payload):
            if payload['completion']['run_id'] == 102:
                raise RuntimeError('synthetic_dispatch_failure')
        with patch.object(poller, '_http_json', side_effect=get), patch.object(poller, '_post_self_dispatch', side_effect=send):
            with self.assertRaisesRegex(RuntimeError, 'synthetic_dispatch_failure'):
                poller.poll_once(state_file=self.state, target_repo='example/target', dispatch_token='synthetic', state_store=store)
        self.assertEqual(store.saved, [101])
        self.assertEqual(store.value['last_processed_run_id'], 101)

    def test_cancelled_without_required_job_but_pending_other_job_blocks(self):
        unrelated = jobs()
        unrelated['jobs'][0].update(name='Other', status='in_progress', conclusion=None)
        with self.assertRaisesRegex(RuntimeError, 'cancelled_jobs_not_terminal'):
            self.poll([run(101, 'cancelled')], unrelated)
        self.assertEqual(poller._load_state(self.state), 100)

    def test_duplicate_paginated_jobs_do_not_prove_absence(self):
        first = [dict(jobs()['jobs'][0], id=i, name='Other') for i in range(1, 101)]
        def get(url):
            if '/jobs?' in url:
                return {'total_count': 101, 'jobs': [first[-1]] if 'page=2' in url else first}
            return {'total_count': 1, 'workflow_runs': [run(101, 'cancelled')]}
        with patch.object(poller, '_http_json', side_effect=get), patch.object(poller, '_post_self_dispatch') as send:
            with self.assertRaisesRegex(RuntimeError, 'source_jobs_duplicate_id'):
                poller.poll_once(state_file=self.state, target_repo='example/target', dispatch_token='synthetic')
        send.assert_not_called()
        self.assertEqual(poller._load_state(self.state), 100)

    def test_job_snapshot_must_match_run_identity_and_attempt(self):
        for field, value in [('run_id', 999), ('head_sha', 'b'*40), ('run_attempt', 2)]:
            with self.subTest(field=field):
                wrong = jobs()
                wrong['jobs'][0][field] = value
                with self.assertRaisesRegex(RuntimeError, 'source_job_identity_mismatch'):
                    self.poll([run(101)], wrong)
        self.assertEqual(poller._load_state(self.state), 100)

    def test_run_page_count_drift_cannot_skip_deleted_offset_neighbor(self):
        # Deleting run 300 between offset pages would otherwise omit run 200.
        def get(url):
            if '/jobs?' in url:
                return jobs(int(url.split('/runs/')[1].split('/')[0]))
            if 'page=2' in url:
                return {'total_count': 200, 'workflow_runs': [run(i) for i in range(100, 200)]}
            return {'total_count': 201, 'workflow_runs': [run(i) for i in range(201, 301)]}
        with patch.object(poller, '_http_json', side_effect=get), patch.object(poller, '_post_self_dispatch') as send:
            with self.assertRaisesRegex(RuntimeError, 'source_runs_count_changed'):
                poller.poll_once(state_file=self.state, target_repo='example/target', dispatch_token='synthetic')
        send.assert_not_called()
        self.assertEqual(poller._load_state(self.state), 100)

    def test_post_success_checkpoint_failure_stops_before_next_dispatch(self):
        class Store:
            def __init__(self, value):
                self.value = value
                self.fail = True
            def load(self):
                return self.value
            def save(self, value):
                if self.fail:
                    raise RuntimeError('synthetic_checkpoint_failure')
                self.value = value
        store = Store(json.loads(self.state.read_text()))
        sent = []
        def get(url):
            return jobs(int(url.split('/runs/')[1].split('/')[0])) if '/jobs?' in url else {'total_count': 2, 'workflow_runs': [run(101), run(102)]}
        def send(repo, token, payload):
            sent.append(payload['completion']['run_id'])
        with patch.object(poller, '_http_json', side_effect=get), patch.object(poller, '_post_self_dispatch', side_effect=send):
            with self.assertRaisesRegex(RuntimeError, 'synthetic_checkpoint_failure'):
                poller.poll_once(state_file=self.state, target_repo='example/target', dispatch_token='synthetic', state_store=store)
            self.assertEqual(sent, [101])
            self.assertEqual(store.value['last_processed_run_id'], 100)
            store.fail = False
            poller.poll_once(state_file=self.state, target_repo='example/target', dispatch_token='synthetic', state_store=store)
        self.assertEqual(sent, [101, 101, 102])
        self.assertEqual(store.value['last_processed_run_id'], 102)

    def test_payload_stays_inside_github_envelope_limits(self):
        payload = poller.make_dispatch_payload(run(101))
        self.assertLessEqual(len(payload), 10)
        self.assertEqual(payload['schema_version'], 2)
        self.assertFalse(payload['completion']['wakeup_is_success_evidence'])

    def test_oversized_payload_is_rejected_before_http(self):
        with patch.object(poller.urllib.request, 'urlopen') as http:
            with self.assertRaisesRegex(RuntimeError, 'self_dispatch_payload_too_large'):
                poller._post_self_dispatch('example/target', 'synthetic', {'data': 'x' * 65536})
        http.assert_not_called()

    def test_dispatch_http_diagnostic_is_sanitized(self):
        error = urllib.error.HTTPError('https://api.github.com/repos/example/target/dispatches', 422,
                                     'synthetic-secret', {'X-GitHub-Request-Id': 'ABCD:1234'},
                                     io.BytesIO(b'{"message":"synthetic-secret"}'))
        with patch.object(poller.urllib.request, 'urlopen', side_effect=error):
            with self.assertRaises(RuntimeError) as raised:
                poller._post_self_dispatch('example/target', 'synthetic-secret', {'event': 'test'})
        self.assertIn('422', str(raised.exception))
        self.assertIn('ABCD:1234', str(raised.exception))
        self.assertNotIn('synthetic-secret', str(raised.exception))


if __name__ == '__main__':
    unittest.main()
