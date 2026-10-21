"""Offline public contract: unresolved PR metadata must never advance a cursor.

The public APIs and on-disk checkpoint bytes are the assertions. External reads,
POSTs and durable writes are mocked; real sockets and urllib are denied before
importing the system under test and throughout each test.
"""
from __future__ import annotations

import copy
import importlib
import json
import pathlib
import socket
import tempfile
import unittest
import urllib.request
from contextlib import ExitStack
from unittest.mock import patch


def deny_network(*args, **kwargs):
    raise AssertionError("OFFLINE CONTRACT: real network access is forbidden")


def block_network(stack):
    for target in ("socket.socket", "socket.create_connection", "socket.getaddrinfo",
                   "urllib.request.urlopen", "urllib.request.OpenerDirector.open"):
        stack.enter_context(patch(target, side_effect=deny_network))


with ExitStack() as _import_guards:
    block_network(_import_guards)
    poller = importlib.import_module("runtime.kuuos_github_public_ci_completion_poller_v1_2")


SHA = "a" * 40
SOURCE_ID = 700
PR_NUMBER = 17
TERMINAL = ("success", "failure", "cancelled", "timed_out", "neutral", "skipped",
            "stale", "action_required", "startup_failure")


def repository(full_name=None, repo_id=SOURCE_ID):
    full_name = poller.SOURCE_REPO if full_name is None else full_name
    return {"id": repo_id, "full_name": full_name, "name": full_name.split("/")[1],
            "url": f"https://api.github.com/repos/{full_name}", "node_id": f"R_test_{repo_id}"}


def run(run_id=101, conclusion="success"):
    return {"id": run_id, "name": poller.SOURCE_WORKFLOW_NAME, "event": "pull_request",
            "status": "completed", "conclusion": conclusion, "run_attempt": 1,
            "head_sha": SHA, "head_branch": "synthetic/topic-1", "repository": repository(),
            "head_repository": repository(), "pull_requests": [{"number": PR_NUMBER,
                "url": f"https://api.github.com/repos/{poller.SOURCE_REPO}/pulls/{PR_NUMBER}",
                "base": {"ref": poller.CANONICAL_BASE, "repo": repository()},
                "head": {"sha": SHA, "ref": "synthetic/topic-1", "repo": repository()}}]}


def jobs(run_id=101):
    return {"total_count": 1, "jobs": [{"id": run_id * 10, "run_id": run_id,
        "run_attempt": 1, "head_sha": SHA, "name": poller.REQUIRED_JOB,
        "status": "completed", "conclusion": "success", "steps": [{
            "name": poller.REQUIRED_STEP, "status": "completed", "conclusion": "success"}]}]}


def set_path(value, path, new):
    cursor = value
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = new
    return value


class MetadataContractTests(unittest.TestCase):
    def setUp(self):
        self.guards = ExitStack()
        self.addCleanup(self.guards.close)
        block_network(self.guards)
        self.temp = tempfile.TemporaryDirectory(prefix="kuuos-metadata-")
        self.addCleanup(self.temp.cleanup)
        self.state = pathlib.Path(self.temp.name) / "checkpoint.json"
        poller._save_state(self.state, 100)
        self.before = self.state.read_bytes()

    def classified(self, value):
        try:
            result = poller.classify_run(value)
        except Exception as exc:
            self.fail(f"classify_run must return a disposition, not {type(exc).__name__}: {exc}")
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[1], list)
        return result

    def assert_unresolved(self, value):
        disposition, reasons = self.classified(value)
        self.assertEqual(disposition, "unresolved", reasons)
        self.assertTrue(reasons, "Unresolved metadata needs a useful reason")
        self.assert_payload_rejected(value)

    def assert_payload_rejected(self, value):
        try:
            poller.make_dispatch_payload(value)
        except RuntimeError:
            return
        except Exception as exc:
            self.fail(f"Expected deliberate RuntimeError, not {type(exc).__name__}: {exc}")
        self.fail("make_dispatch_payload accepted unresolved or excluded metadata")

    def test_complete_identity_is_candidate(self):
        self.assertEqual(self.classified(run()), ("candidate", []))
        completion = poller.make_dispatch_payload(run())["completion"]
        self.assertEqual(completion["source_pr_number"], PR_NUMBER)
        self.assertEqual(completion["head_sha"], SHA)
        self.assertEqual(completion["head_branch"], "synthetic/topic-1")
        self.assertEqual(completion["source_base_ref"], poller.CANONICAL_BASE)
        self.assertFalse(completion["wakeup_is_success_evidence"])
        self.assertTrue(completion["fresh_mcp_reobservation_required"])

    def test_absent_pr_association_is_unresolved(self):
        value = run()
        value.pop("pull_requests")
        self.assert_unresolved(value)

    def test_ambiguous_pr_associations_are_unresolved(self):
        value = run()
        value["pull_requests"].append(copy.deepcopy(value["pull_requests"][0]))
        self.assert_unresolved(value)

    def test_missing_head_repository_is_unresolved_not_fork(self):
        value = run()
        value.pop("head_repository")
        self.assert_unresolved(value)

    def test_missing_head_sha_is_unresolved(self):
        value = run()
        value.pop("head_sha")
        self.assert_unresolved(value)

    def test_payload_builder_revalidates_missing_metadata(self):
        value = run()
        value["pull_requests"] = []
        self.assert_payload_rejected(value)

    def test_association_head_sha_contradiction_is_unresolved(self):
        value = set_path(run(), ("pull_requests", 0, "head", "sha"), "b" * 40)
        self.assert_unresolved(value)

    def test_same_name_conflicting_repository_id_is_unresolved(self):
        value = set_path(run(), ("pull_requests", 0, "head", "repo", "id"), 999)
        self.assert_unresolved(value)


    def test_pr_association_container_and_cardinality_are_strict(self):
        for associations in (None, {}, "17", 17, [], [None], [17], ["17"],
                             [run()["pull_requests"][0], None]):
            with self.subTest(associations=associations):
                self.assert_unresolved(set_path(run(), ("pull_requests",), associations))

    def test_pr_number_must_be_strict_positive_integer(self):
        for number in (None, False, True, 0, -1, "17", " 17 ", 17.0, [], {}):
            with self.subTest(number=number):
                self.assert_unresolved(set_path(run(), ("pull_requests", 0, "number"), number))
        value = run()
        del value["pull_requests"][0]["number"]
        self.assert_unresolved(value)

    def test_supplied_pr_api_url_must_match_exact_source_and_number(self):
        expected = run()["pull_requests"][0]["url"]
        for url in (None, "", 17, [], {}, expected + "/", expected + "?x=1",
                    expected + "#fragment", expected.replace("/17", "/18"),
                    expected.replace(poller.SOURCE_REPO, "other/project"),
                    expected.replace("api.github.com", "api.github.com.evil.invalid"),
                    expected.replace("https:", "http:"),
                    expected.replace("/pulls/", "/issues/"),
                    expected.replace("api.github.com/", "user@api.github.com/")):
            with self.subTest(url=url):
                self.assert_unresolved(set_path(run(), ("pull_requests", 0, "url"), url))

    def test_absent_optional_pr_url_and_association_head_are_supported(self):
        value = run()
        value["pull_requests"][0].pop("url")
        value["pull_requests"][0].pop("head")
        self.assertEqual(self.classified(value), ("candidate", []))

    def test_head_sha_must_be_well_formed_string(self):
        for sha in (None, "", [], {}, True, 123, "a" * 39, "a" * 41, "g" * 40,
                    " " + SHA, SHA + "\n"):
            with self.subTest(sha=sha):
                self.assert_unresolved(set_path(run(), ("head_sha",), sha))

    def test_uppercase_hex_sha_is_normalized_without_losing_identity(self):
        value = run()
        value["head_sha"] = SHA.upper()
        value["pull_requests"][0]["head"]["sha"] = SHA.upper()
        self.assertEqual(self.classified(value), ("candidate", []))
        self.assertEqual(poller.make_dispatch_payload(value)["completion"]["head_sha"], SHA)

    def test_head_repository_requires_valid_full_name_without_fallback(self):
        for head_repo in (None, [], "owner/repo", {}, {"id": SOURCE_ID},
                          {"full_name": None}, {"full_name": []}, {"full_name": ""},
                          {"full_name": "missing-slash"}, {"full_name": "owner/repo/extra"}):
            with self.subTest(head_repository=head_repo):
                self.assert_unresolved(set_path(run(), ("head_repository",), head_repo))

    def test_base_metadata_is_required_and_not_coerced(self):
        for base in (None, [], "main", {}, {"ref": None}, {"ref": []}, {"ref": ""}):
            with self.subTest(base=base):
                self.assert_unresolved(set_path(run(), ("pull_requests", 0, "base"), base))

    def test_association_head_ref_sha_and_container_must_be_consistent(self):
        paths_and_values = [
            (("pull_requests", 0, "head"), None),
            (("pull_requests", 0, "head"), []),
            (("pull_requests", 0, "head", "sha"), None),
            (("pull_requests", 0, "head", "sha"), []),
            (("pull_requests", 0, "head", "sha"), "b" * 40),
            (("pull_requests", 0, "head", "ref"), None),
            (("pull_requests", 0, "head", "ref"), "other/topic"),
            (("pull_requests", 0, "head", "repo"), None),
            (("pull_requests", 0, "head", "repo"), []),
        ]
        for path, value in paths_and_values:
            with self.subTest(path=path, value=value):
                self.assert_unresolved(set_path(run(), path, value))

    def test_every_supplied_repository_identity_component_is_checked(self):
        for prefix in (("repository",), ("head_repository",),
                       ("pull_requests", 0, "base", "repo"),
                       ("pull_requests", 0, "head", "repo")):
            for field, value in (("id", 999), ("id", True), ("id", "700"),
                                 ("name", "different"), ("url", "https://api.github.com/repos/other/repo"),
                                 ("node_id", "R_different"), ("full_name", "other/repo")):
                with self.subTest(prefix=prefix, field=field, value=value):
                    self.assert_unresolved(set_path(run(), prefix + (field,), value))

    def test_supplied_source_repository_cannot_be_malformed(self):
        for value in (None, [], "owner/repo", {"full_name": None}, {"id": False},
                      {"full_name": poller.SOURCE_REPO, "url": None}):
            with self.subTest(repository=value):
                self.assert_unresolved(set_path(run(), ("repository",), value))

    def test_compact_github_association_repositories_are_accepted(self):
        value = run()
        for side in ("base", "head"):
            repo = value["pull_requests"][0][side]["repo"]
            value["pull_requests"][0][side]["repo"] = {
                key: repo[key] for key in ("id", "url", "name")}
        self.assertEqual(self.classified(value), ("candidate", []))
        self.assertEqual(poller.make_dispatch_payload(value)["completion"]["source_pr_number"], PR_NUMBER)

    def test_minimal_noncontradictory_repository_identity_is_accepted(self):
        value = run()
        value.pop("repository")
        value["head_repository"] = {"full_name": poller.SOURCE_REPO}
        value["pull_requests"][0]["base"].pop("repo")
        value["pull_requests"][0]["head"].pop("repo")
        self.assertEqual(self.classified(value), ("candidate", []))

    def test_different_name_with_same_id_is_unresolved_not_fork(self):
        value = run()
        value["head_repository"] = repository("fork-owner/fork-repo", SOURCE_ID)
        value["pull_requests"][0]["head"]["repo"] = copy.deepcopy(value["head_repository"])
        self.assert_unresolved(value)

    def test_coherent_actual_fork_is_ignored_not_unresolved(self):
        value = self.fork_run()
        disposition, reasons = self.classified(value)
        self.assertEqual(disposition, "ignored")
        self.assertIn("head_repository_not_source_repository", reasons)
        self.assert_payload_rejected(value)

    def test_malformed_fork_owners_cannot_be_checkpointed_as_exclusions(self):
        for owner in ("-fork", "fork-", "fork--owner", "f" * 40,
                      "mona_ab", "mona_abcdefghi"):
            with self.subTest(owner=owner):
                value = run()
                # full_name and the API URL agree, so a rejection must not rely
                # on a fabricated name/URL or head/association contradiction.
                value["head_repository"] = repository(owner + "/fork-repo", 701)
                value["pull_requests"][0]["head"]["repo"] = copy.deepcopy(value["head_repository"])
                self.assert_unresolved(value)
                self.assert_payload_rejected(value)
                self.assert_metadata_stop(value)

    def test_supported_ordinary_and_managed_fork_owners_remain_excluded(self):
        # GitHub.com managed logins have an enterprise suffix after an
        # underscore. Underscores are not universally invalid owner names.
        for owner in ("fork-owner", "FORK9", "f" * 39, "mona_acme", "Mona-Lisa_acme",
                      "mona_abc", "mona_abcdefgh"):
            with self.subTest(owner=owner):
                value = run()
                value["head_repository"] = repository(owner + "/fork-repo", 701)
                value["pull_requests"][0]["head"]["repo"] = copy.deepcopy(value["head_repository"])
                self.assertEqual(self.classified(value),
                                 ("ignored", ["head_repository_not_source_repository"]))
                self.assert_payload_rejected(value)

    def test_coherent_wrong_base_is_ignored_not_unresolved(self):
        value = set_path(run(), ("pull_requests", 0, "base", "ref"), "main")
        disposition, reasons = self.classified(value)
        self.assertEqual(disposition, "ignored")
        self.assertIn("canonical_base_mismatch", reasons)
        self.assert_payload_rejected(value)

    def test_contradiction_is_unresolved_even_when_other_metadata_excludes_run(self):
        for excluded in (self.fork_run(), set_path(run(), ("pull_requests", 0, "base", "ref"), "main")):
            excluded["pull_requests"][0]["head"]["sha"] = "b" * 40
            with self.subTest(head_repository=excluded["head_repository"]):
                self.assert_unresolved(excluded)

    def test_head_branch_is_required_and_uses_conservative_ascii_subset(self):
        invalid = (None, [], {}, 1, True, "", "HEAD", "éclair", "topic/日本語", "topic/\u200bhidden",
                   "topic name", "topic\nname", "topic\tname", "a\\b", "a..b", "a//b",
                   "/topic", "topic/", ".hidden/topic", "topic/.hidden", "topic.lock",
                   "topic/x.lock", "topic.", "a@{b", "a?b", "a*b", "a[b", "a:b", "a~b", "a^b")
        for branch in invalid:
            with self.subTest(branch=branch):
                value = set_path(run(), ("head_branch",), branch)
                value["pull_requests"][0]["head"]["ref"] = branch
                self.assert_unresolved(value)
        value = run()
        value.pop("head_branch")
        self.assert_unresolved(value)

    def test_representative_ascii_branch_names_are_accepted(self):
        for branch in ("topic", "feature/FIX-123", "release/v1.2", "topic_name", "a/b-c_d.1"):
            with self.subTest(branch=branch):
                value = run()
                value["head_branch"] = branch
                value["pull_requests"][0]["head"]["ref"] = branch
                self.assertEqual(self.classified(value), ("candidate", []))

    def test_public_payload_rejects_every_non_dispatchable_disposition(self):
        values = [self.fork_run(), set_path(run(), ("pull_requests", 0, "base", "ref"), "main"),
                  set_path(run(), ("head_sha",), "bad"), set_path(run(), ("head_branch",), ""),
                  set_path(run(), ("pull_requests",), []),
                  set_path(run(), ("pull_requests", 0, "number"), True),
                  set_path(run(), ("status",), "in_progress"),
                  set_path(run(), ("conclusion",), "unknown_future_value"),
                  set_path(run(), ("name",), "Unrelated workflow"),
                  set_path(run(), ("event",), "push")]
        for value in values:
            with self.subTest(value=value):
                self.assert_payload_rejected(value)

    def test_every_terminal_conclusion_is_wakeup_only(self):
        for conclusion in TERMINAL:
            with self.subTest(conclusion=conclusion):
                value = run(conclusion=conclusion)
                self.assertEqual(self.classified(value), ("candidate", []))
                payload = poller.make_dispatch_payload(value)
                self.assertLessEqual(len(payload), 10)
                self.assertEqual(payload["schema_version"], 2)
                completion = payload["completion"]
                self.assertEqual(completion["conclusion"], conclusion)
                self.assertFalse(completion["wakeup_is_success_evidence"])
                self.assertTrue(completion["fresh_mcp_reobservation_required"])

    @staticmethod
    def fork_run(run_id=101):
        value = run(run_id)
        value["head_repository"] = repository("fork-owner/fork-repo", 701)
        value["pull_requests"][0]["head"]["repo"] = copy.deepcopy(value["head_repository"])
        return value

    def poll_case(self, runs, *, job_data=None, on_jobs=None, failure=None, durable=True):
        events = []
        snapshots = []
        payloads = []
        initial = json.loads(self.state.read_bytes())
        class Store:
            value = copy.deepcopy(initial)
            def load(store):
                return copy.deepcopy(store.value)
            def save(store, value):
                rid = value["last_processed_run_id"]
                events.append(("durable", rid))
                if failure == ("durable", rid):
                    raise RuntimeError("synthetic_durable_failure")
                store.value = copy.deepcopy(value)
        store = Store()
        real_save = poller._save_state
        def save(path, rid, outcome=None):
            events.append(("local", rid))
            if failure == ("local", rid):
                raise RuntimeError("synthetic_local_failure")
            real_save(path, rid, outcome)
            snapshots.append((rid, path.read_bytes()))
        def get(url):
            if "/jobs?" in url:
                rid = int(url.split("/runs/")[1].split("/")[0])
                events.append(("jobs", rid))
                if on_jobs is not None:
                    on_jobs(rid)
                return copy.deepcopy(jobs(rid) if job_data is None else job_data)
            return {"total_count": len(runs), "workflow_runs": runs}
        def dispatch(repo, token, payload):
            rid = payload["completion"]["run_id"]
            events.append(("dispatch", rid))
            if failure == ("dispatch", rid):
                raise RuntimeError("synthetic_dispatch_failure")
            payloads.append(copy.deepcopy(payload))
        summary = error = None
        with patch.object(poller, "_http_json", side_effect=get), \
                patch.object(poller, "_post_self_dispatch", side_effect=dispatch), \
                patch.object(poller, "_save_state", side_effect=save):
            try:
                summary = poller.poll_once(state_file=self.state, target_repo="example/target",
                    dispatch_token="offline-test-never-send", state_store=store if durable else None)
            except RuntimeError as exc:
                error = exc
            except Exception as exc:
                self.fail(f"poll_once raised accidental {type(exc).__name__}: {exc}")
        return summary, error, events, store, snapshots, payloads

    def assert_metadata_stop(self, value, *, job_data=None):
        before = self.state.read_bytes()
        summary, error, events, store, snapshots, payloads = self.poll_case(
            [value, run(102)], job_data=job_data)
        self.assertIsNotNone(error, "Unresolved metadata must stop polling with RuntimeError")
        self.assertRegex(str(error), "source_run_metadata_unresolved")
        self.assertIsNone(summary)
        self.assertEqual(events, [], "No jobs, dispatch, durable save, or local save is allowed")
        self.assertEqual(snapshots, [])
        self.assertEqual(payloads, [])
        self.assertEqual(store.value["last_processed_run_id"], 100)
        self.assertEqual(self.state.read_bytes(), before)

    def test_unresolved_first_record_stops_before_any_effect_or_later_record(self):
        cases = [set_path(run(), ("pull_requests",), []),
                 set_path(run(), ("head_repository",), {}),
                 set_path(run(), ("head_sha",), "bad"),
                 set_path(run(), ("pull_requests", 0, "number"), "17"),
                 set_path(run(), ("pull_requests", 0, "head", "sha"), "b" * 40)]
        for value in cases:
            with self.subTest(value=value):
                self.state.write_bytes(self.before)
                self.assert_metadata_stop(value)

    def test_unresolved_cancelled_record_cannot_quarantine(self):
        value = run(conclusion="cancelled")
        value["pull_requests"] = []
        self.assert_metadata_stop(value, job_data={"total_count": 0, "jobs": []})

    def test_valid_prefix_checkpoint_bytes_survive_unresolved_successor(self):
        invalid = set_path(run(102), ("pull_requests",), [])
        summary, error, events, store, snapshots, payloads = self.poll_case([run(101), invalid, run(103)])
        self.assertIsNotNone(error)
        self.assertRegex(str(error), "source_run_metadata_unresolved")
        self.assertEqual(events, [("jobs", 101), ("dispatch", 101), ("durable", 101), ("local", 101)])
        self.assertEqual(len(snapshots), 1)
        self.assertEqual(self.state.read_bytes(), snapshots[0][1])
        self.assertEqual(json.loads(self.state.read_bytes())["last_processed_run_id"], 101)
        self.assertEqual(store.value["last_processed_run_id"], 101)
        self.assertEqual([p["completion"]["run_id"] for p in payloads], [101])

    def test_pending_gate_precedes_metadata_and_preserves_checkpoint(self):
        value = set_path(run(), ("status",), "in_progress")
        value["conclusion"] = None
        value["pull_requests"] = []
        summary, error, events, store, snapshots, payloads = self.poll_case([value, run(102)])
        self.assertIsNone(error)
        self.assertEqual(summary.pending_run_ids, [101])
        self.assertEqual(summary.final_run_id, 100)
        self.assertEqual(events, [])
        self.assertEqual(self.state.read_bytes(), self.before)

    def test_unknown_conclusion_gate_precedes_metadata_and_preserves_checkpoint(self):
        for conclusion in (None, "", "future_unknown", [], {}):
            with self.subTest(conclusion=conclusion):
                value = run(conclusion=conclusion)
                value["pull_requests"] = []
                summary, error, events, store, snapshots, payloads = self.poll_case([value, run(102)])
                self.assertIsNotNone(error)
                self.assertRegex(str(error), "source_workflow_conclusion_not_terminal")
                self.assertEqual(events, [])
                self.assertEqual(self.state.read_bytes(), self.before)

    def test_coherent_exclusions_checkpoint_without_jobs_or_dispatch(self):
        wrong_base = set_path(run(102), ("pull_requests", 0, "base", "ref"), "main")
        summary, error, events, store, snapshots, payloads = self.poll_case([self.fork_run(), wrong_base])
        self.assertIsNone(error)
        self.assertEqual(summary.ignored_run_ids, [101, 102])
        self.assertEqual(summary.final_run_id, 102)
        self.assertEqual(events, [("durable", 101), ("local", 101), ("durable", 102), ("local", 102)])
        self.assertEqual(store.value["last_outcome"]["disposition"], "ignored")
        self.assertEqual(payloads, [])

    def test_dispatch_then_durable_then_local_order_is_preserved(self):
        summary, error, events, store, snapshots, payloads = self.poll_case([run(101), run(102)])
        self.assertIsNone(error)
        self.assertEqual(summary.dispatched_run_ids, [101, 102])
        self.assertEqual(events, [(kind, rid) for rid in (101, 102)
                                 for kind in ("jobs", "dispatch", "durable", "local")])
        self.assertEqual(store.value, json.loads(self.state.read_bytes()))

    def test_dispatch_failure_preserves_last_confirmed_prefix(self):
        summary, error, events, store, snapshots, payloads = self.poll_case(
            [run(101), run(102), run(103)], failure=("dispatch", 102))
        self.assertRegex(str(error), "synthetic_dispatch_failure")
        self.assertEqual(events, [("jobs", 101), ("dispatch", 101), ("durable", 101), ("local", 101),
                                  ("jobs", 102), ("dispatch", 102)])
        self.assertEqual(store.value["last_processed_run_id"], 101)
        self.assertEqual(self.state.read_bytes(), snapshots[0][1])

    def test_durable_failure_blocks_local_save_and_later_records(self):
        summary, error, events, store, snapshots, payloads = self.poll_case(
            [run(101), run(102)], failure=("durable", 101))
        self.assertRegex(str(error), "synthetic_durable_failure")
        self.assertEqual(events, [("jobs", 101), ("dispatch", 101), ("durable", 101)])
        self.assertEqual(store.value["last_processed_run_id"], 100)
        self.assertEqual(self.state.read_bytes(), self.before)
        self.assertEqual(len(payloads), 1)

    def test_local_failure_after_durable_success_stops_later_records(self):
        summary, error, events, store, snapshots, payloads = self.poll_case(
            [run(101), run(102)], failure=("local", 101))
        self.assertRegex(str(error), "synthetic_local_failure")
        self.assertEqual(events, [("jobs", 101), ("dispatch", 101), ("durable", 101), ("local", 101)])
        self.assertEqual(store.value["last_processed_run_id"], 101)
        self.assertEqual(self.state.read_bytes(), self.before)
        self.assertEqual(len(payloads), 1)

    def test_cancelled_quarantine_requires_valid_metadata(self):
        summary, error, events, store, snapshots, payloads = self.poll_case(
            [run(conclusion="cancelled")], job_data={"total_count": 0, "jobs": []})
        self.assertIsNone(error)
        self.assertEqual(summary.quarantined_run_ids, [101])
        self.assertEqual(events, [("jobs", 101), ("durable", 101), ("local", 101)])
        self.assertEqual(store.value["last_outcome"]["disposition"], "quarantined")
        self.assertEqual(payloads, [])

    def test_poll_uses_validated_identity_snapshot_after_jobs_read(self):
        value = run()
        def mutate_after_validation(rid):
            value["pull_requests"][0]["number"] = 999
            value["pull_requests"][0]["base"]["ref"] = "mutated-base"
            value["pull_requests"][0]["head"]["sha"] = "b" * 40
        summary, error, events, store, snapshots, payloads = self.poll_case(
            [value], on_jobs=mutate_after_validation)
        self.assertIsNone(error, "A validated identity snapshot must not be reparsed from later mutated input")
        self.assertEqual(summary.dispatched_run_ids, [101])
        completion = payloads[0]["completion"]
        self.assertEqual(completion["source_pr_number"], PR_NUMBER)
        self.assertEqual(completion["source_base_ref"], poller.CANONICAL_BASE)
        self.assertEqual(completion["head_sha"], SHA)

    def test_all_terminal_workflow_conclusions_pass_through_poll_as_wakeups(self):
        for conclusion in TERMINAL:
            with self.subTest(conclusion=conclusion):
                self.state.write_bytes(self.before)
                summary, error, events, store, snapshots, payloads = self.poll_case([run(conclusion=conclusion)])
                self.assertIsNone(error)
                self.assertEqual(summary.dispatched_run_ids, [101])
                completion = payloads[0]["completion"]
                self.assertEqual(completion["conclusion"], conclusion)
                self.assertFalse(completion["wakeup_is_success_evidence"])
                self.assertTrue(completion["fresh_mcp_reobservation_required"])


    def test_base_ref_uses_the_same_safe_ascii_branch_contract(self):
        for ref in ("HEAD", "rélease", "topic/日本語", "a..b", "a//b", "/main", "main/",
                    "topic.lock", ".hidden", "main\n", "a@{b", "a\\b"):
            with self.subTest(ref=ref):
                self.assert_unresolved(set_path(run(), ("pull_requests", 0, "base", "ref"), ref))

    def test_unresolved_local_only_poll_preserves_exact_checkpoint_bytes(self):
        value = set_path(run(), ("pull_requests",), [])
        summary, error, events, store, snapshots, payloads = self.poll_case([value, run(102)], durable=False)
        self.assertIsNotNone(error)
        self.assertRegex(str(error), "source_run_metadata_unresolved")
        self.assertEqual(events, [])
        self.assertEqual(self.state.read_bytes(), self.before)

    def test_ignored_prefix_is_retained_before_unresolved_successor(self):
        invalid = set_path(run(102), ("head_repository",), None)
        summary, error, events, store, snapshots, payloads = self.poll_case([self.fork_run(), invalid, run(103)])
        self.assertIsNotNone(error)
        self.assertRegex(str(error), "source_run_metadata_unresolved")
        self.assertEqual(events, [("durable", 101), ("local", 101)])
        self.assertEqual(self.state.read_bytes(), snapshots[0][1])
        self.assertEqual(store.value["last_outcome"]["disposition"], "ignored")
        self.assertEqual(store.value["last_processed_run_id"], 101)

    def test_all_terminal_job_and_step_conclusions_remain_wakeup_only(self):
        for job_conclusion in TERMINAL:
            for step_conclusion in TERMINAL:
                with self.subTest(job=job_conclusion, step=step_conclusion):
                    self.state.write_bytes(self.before)
                    value = jobs()
                    value["jobs"][0]["conclusion"] = job_conclusion
                    value["jobs"][0]["steps"][0]["conclusion"] = step_conclusion
                    summary, error, events, store, snapshots, payloads = self.poll_case([run()], job_data=value)
                    self.assertIsNone(error)
                    self.assertEqual(summary.dispatched_run_ids, [101])
                    self.assertFalse(payloads[0]["completion"]["wakeup_is_success_evidence"])
                    self.assertTrue(payloads[0]["completion"]["fresh_mcp_reobservation_required"])


    def test_compact_associations_cannot_hide_same_name_conflicting_ids(self):
        value = run()
        value["repository"] = {"full_name": poller.SOURCE_REPO}
        value["head_repository"] = {"full_name": poller.SOURCE_REPO}
        name = poller.SOURCE_REPO.split("/")[1]
        value["pull_requests"][0]["base"]["repo"] = {"id": SOURCE_ID, "name": name}
        value["pull_requests"][0]["head"]["repo"] = {"id": SOURCE_ID + 1, "name": name}
        self.assert_unresolved(value)

    def test_compact_associations_cannot_hide_different_names_with_same_id(self):
        value = self.fork_run()
        value["repository"] = {"full_name": poller.SOURCE_REPO}
        value["pull_requests"][0]["base"]["repo"] = {
            "id": 701, "name": poller.SOURCE_REPO.split("/")[1]}
        value["pull_requests"][0]["head"]["repo"] = {"id": 701, "name": "fork-repo"}
        self.assert_unresolved(value)


if __name__ == "__main__":
    unittest.main()
