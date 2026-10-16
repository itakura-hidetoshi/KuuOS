"""Run the real comparison shell step with real Git and an offline API fixture."""
from pathlib import Path
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / '.github/workflows/pr-governance-gate.yml'


def comparison_step():
    tail = WORKFLOW.read_text().split('      - name: Resolve comparison refs\n', 1)[1]
    block = tail.split('        run: |\n', 1)[1]
    lines = []
    for line in block.splitlines():
        if line and not line.startswith('          '):
            break
        lines.append(line[10:] if line else '')
    return '\n'.join(lines)


class ComparisonHistoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'scripts').mkdir()
        for name in ('ensure_ci_comparison.py', 'select_ci_incremental_base.py'):
            source = ROOT / 'scripts' / name
            if source.exists():
                shutil.copyfile(source, self.root / 'scripts' / name)
        self.git('init', '-q', '-b', 'feature')
        self.git('config', 'user.name', 'CI regression')
        self.git('config', 'user.email', 'ci@example.invalid')
        (self.root / 'formal').mkdir()
        (self.root / 'formal/Test.lean').write_text('def value := 0\n')
        (self.root / 'old.py').write_text('value = 0\n')
        self.base = self.commit('base')
        (self.root / 'prior.py').write_text('value = 1\n')
        self.candidate = self.commit('already tested non-Lean change')
        (self.root / 'formal/Test.lean').write_text('def value := 1\n')
        self.head = self.commit('Lean-only follow-up')
        self.run = {
            'id': 101, 'head_sha': self.candidate, 'status': 'completed',
            'event': 'pull_request', 'head_branch': 'feature', 'run_attempt': 1,
            'path': '.github/workflows/pr-governance-gate.yml',
            'head_repository': {'full_name': 'example/project'},
            'pull_requests': [{'base': {'sha': self.base}}],
        }
        self.jobs = [self.job(1, 'Select impacted audit checks'),
                     self.job(2, 'Independent boundary regression')]
        self.fixture = {'workflow_runs': [self.run], 'pages': [self.page(self.jobs)]}
        self.gh = self.root / 'gh'
        self.gh.write_text('#!' + sys.executable + '\n' + '''
import json, os, sys
from pathlib import Path
args = sys.argv[1:]
f = json.loads(Path('fixture.json').read_text())
with Path('api-calls.jsonl').open('a') as out:
    out.write(json.dumps(args) + '\\n')
is_jobs = any('/jobs' in arg for arg in args)
if f.get('failure') == ('jobs' if is_jobs else 'runs'):
    sys.exit('gh: Server Error (HTTP 502)')
if '--jq' in args:
    query = args[args.index('--jq') + 1]
    if not is_jobs:
        for run in f['workflow_runs']:
            print(str(run['id']) + '|' + run['head_sha'] + '|' + run['status'])
    elif f.get('jq_error'):
        sys.exit('failed to parse multi-field jq selector: unexpected token')
    else:
        ignored = {'Select impacted audit checks', 'Strict Lean formal validation',
                   'Governance gate and audit summary', 'Publish MCP Lean completion receipt',
                   'Publish MCP CI completion receipt'}
        jobs = [j for j in f['pages'][0]['jobs'] if j['name'] not in ignored]
        if '.conclusion' in query:
            jobs = [j for j in jobs if j['conclusion'] not in ('success', 'skipped')]
        print(len(jobs))
else:
    if f.get('malformed') and is_jobs:
        print('{broken json')
    else:
        print(json.dumps(f['pages'] if is_jobs else {'workflow_runs': f['workflow_runs']}))
''')
        self.gh.chmod(0o755)

    def git(self, *args):
        return subprocess.run(['git', *args], cwd=self.root, check=True,
                              capture_output=True, text=True).stdout.strip()

    def commit(self, message):
        self.git('add', 'formal', '*.py')
        self.git('commit', '-qm', message)
        return self.git('rev-parse', 'HEAD')

    def job(self, number, name='Check', conclusion='success'):
        return {'id': number, 'run_id': 101, 'run_attempt': 1,
                'head_sha': self.candidate, 'name': name,
                'status': 'completed', 'conclusion': conclusion}

    def page(self, jobs, total=None):
        return {'total_count': len(jobs) if total is None else total, 'jobs': jobs}

    def execute(self, **env_changes):
        (self.root / 'fixture.json').write_text(json.dumps(self.fixture))
        output = self.root / 'output'
        output.unlink(missing_ok=True)
        environment = dict(os.environ, PATH=str(self.root) + os.pathsep + os.environ['PATH'],
                           GITHUB_OUTPUT=str(output), GH_TOKEN='offline-fixture',
                           EVENT_NAME='pull_request', EVENT_ACTION='synchronize',
                           PR_BASE_SHA=self.base, PR_HEAD_SHA=self.head, PR_HEAD_REF='feature',
                           CURRENT_SHA=self.head, CURRENT_RUN_ID='202', REPOSITORY='example/project')
        environment.update(env_changes)
        result = subprocess.run(['bash', '-euo', 'pipefail', '-c', comparison_step()],
                                cwd=self.root, env=environment, capture_output=True,
                                text=True, timeout=15)
        values = dict(line.split('=', 1) for line in output.read_text().splitlines()) if output.exists() else {}
        return result, values

    def assert_mode(self, mode='full-pr'):
        result, values = self.execute()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(values, {'base': self.candidate if mode == 'validated-lean-incremental' else self.base,
                                  'head': self.head, 'mode': mode})

    def test_jq_parse_error_is_avoided_by_reading_json(self):
        self.fixture['jq_error'] = True
        self.assert_mode('validated-lean-incremental')

    def test_jobs_api_502_falls_back_to_full_exact_comparison(self):
        self.fixture['failure'] = 'jobs'
        self.assert_mode()

    def test_runs_api_502_falls_back_to_full_exact_comparison(self):
        self.fixture['failure'] = 'runs'
        self.assert_mode()

    def test_malformed_json_does_not_authorize_incremental(self):
        self.fixture['malformed'] = True
        self.assert_mode()

    def test_incomplete_page_is_not_treated_as_all_success(self):
        self.fixture['pages'][0]['total_count'] = 101
        self.assert_mode()

    def test_failure_on_second_page_is_not_hidden(self):
        first = self.jobs + [self.job(i) for i in range(3, 101)]
        second = [self.job(101, conclusion='failure')]
        self.fixture['pages'] = [self.page(first, 101), self.page(second, 101)]
        self.assert_mode()

    def test_complete_paginated_success_retains_fast_path(self):
        first = self.jobs + [self.job(i) for i in range(3, 101)]
        self.fixture['pages'] = [self.page(first, 101), self.page([self.job(101)], 101)]
        self.assert_mode('validated-lean-incremental')

    def test_duplicate_jobs_cannot_satisfy_total_count(self):
        self.fixture['pages'] = [self.page(self.jobs, 4), self.page(self.jobs, 4)]
        self.assert_mode()

    def test_skipped_only_checks_are_not_success_evidence(self):
        self.jobs[1]['conclusion'] = 'skipped'
        self.assert_mode()

    def test_pending_check_rejects_reuse(self):
        self.jobs[1]['status'] = 'in_progress'
        self.assert_mode()

    def test_failed_selection_rejects_reuse(self):
        self.jobs[0]['conclusion'] = 'failure'
        self.assert_mode()

    def test_different_run_binding_rejects_reuse(self):
        for key, wrong in [('run_id', 999), ('run_attempt', 2), ('head_sha', self.head)]:
            with self.subTest(key=key):
                old = self.jobs[1][key]
                self.jobs[1][key] = wrong
                self.assert_mode()
                self.jobs[1][key] = old

    def test_changed_base_rejects_reuse(self):
        self.run['pull_requests'][0]['base']['sha'] = 'a' * 40
        self.assert_mode()

    def test_foreign_branch_rejects_reuse(self):
        self.run['head_branch'] = 'other'
        self.assert_mode()

    def test_nonlean_followup_does_not_query_job_history(self):
        (self.root / 'prior.py').write_text('value = 2\n')
        self.head = self.commit('non-Lean follow-up')
        self.assert_mode()
        calls = (self.root / 'api-calls.jsonl').read_text()
        self.assertNotIn('/jobs', calls)

    def test_deleted_python_file_prevents_incremental(self):
        (self.root / 'old.py').unlink()
        self.head = self.commit('delete non-Lean file')
        self.assert_mode()

    def test_deleted_lean_file_requires_full_validation(self):
        (self.root / 'formal/Test.lean').unlink()
        self.head = self.commit('delete Lean file')
        self.assert_mode()

    def test_moved_nonlean_file_cannot_hide_behind_lean_extension(self):
        (self.root / 'old.py').rename(self.root / 'formal/Moved.lean')
        self.head = self.commit('move non-Lean file')
        self.assert_mode()

    def test_invalid_mandatory_head_remains_a_failure(self):
        result, values = self.execute(PR_HEAD_SHA='a' * 40)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(values, {})

    def test_non_synchronize_keeps_full_pr_without_api(self):
        result, values = self.execute(EVENT_ACTION='opened')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(values['mode'], 'full-pr')
        self.assertFalse((self.root / 'api-calls.jsonl').exists())


if __name__ == '__main__':
    unittest.main()
