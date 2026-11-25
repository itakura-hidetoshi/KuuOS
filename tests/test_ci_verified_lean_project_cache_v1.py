"""Authority and transport tests. Fixtures grant no proof authority."""
import copy
from datetime import datetime,timedelta,timezone
import io
import json
from pathlib import Path
import tarfile
import tempfile
import unittest
from unittest.mock import patch
import zipfile
from scripts import ci_verified_lean_project_cache_v1 as c

NOW=datetime(2026,11,25,tzinfo=timezone.utc)
HEAD="a"*40
BASE="b"*40
SCOPE={"fixture":True}
ROOT=Path(__file__).resolve().parents[1]

def fixture():
    a={"id":9,"name":c.PREFIX+c.digest(SCOPE),"expired":False,
       "expires_at":(NOW+timedelta(days=20)).isoformat(),"digest":"sha256:"+"c"*64,
       "size_in_bytes":100,"workflow_run":{"id":7,"repository_id":c.REPO_ID,
       "head_repository_id":c.REPO_ID,"head_branch":"main","head_sha":HEAD}}
    r={"id":7,"workflow_id":3,"head_sha":HEAD,"head_branch":"main","event":"push",
       "repository":{"id":c.REPO_ID},"head_repository":{"id":c.REPO_ID},
       "status":"completed","conclusion":"success","path":c.PUBLISHER,"run_attempt":2}
    j={"id":8,"name":c.JOB,"head_sha":HEAD,"status":"completed","conclusion":"success",
       "steps":[{"name":n,"status":"completed","conclusion":"success"} for n in c.STEPS]}
    data={"actions/runs/7":r,"actions/runs/7/attempts/2/jobs?per_page=100":
          {"total_count":1,"jobs":[j]},"actions/artifacts/9":copy.deepcopy(a)}
    return a,r,j,data

class Authority(unittest.TestCase):
    def admit(self,a,d,ancestry=True,scope=SCOPE):
        with patch.object(c,"ancestor",return_value=ancestry),patch.object(c,"remote_scope",return_value=scope):
            return c.admit_artifact(d.__getitem__,a,SCOPE,BASE,3,now=NOW)
    def test_exact_green(self):
        a,r,j,d=fixture()
        self.assertEqual(self.admit(a,d)["artifact_id"],9)
    def test_reject_red_pr_fork_or_wrong_workflow(self):
        for k,v in [("event","pull_request"),("head_branch","research"),("conclusion","failure"),
                    ("status","in_progress"),("workflow_id",4),("path","other.yml"),("head_sha",BASE)]:
            a,r,j,d=fixture()
            r[k]=v
            with self.subTest(k=k),self.assertRaises(c.Miss):
                self.admit(a,d)
        a,r,j,d=fixture()
        j["steps"][0]["conclusion"]="skipped"
        with self.assertRaises(c.Miss):
            self.admit(a,d)
        a,r,j,d=fixture()
        a["workflow_run"]["head_repository_id"]=123
        with self.assertRaises(c.Miss):
            self.admit(a,d)
    def test_reject_expired_missing_digest_or_metadata_drift(self):
        for k,v in [("expired",True),("digest",None),("name","other"),("size_in_bytes",0)]:
            a,r,j,d=fixture()
            a[k]=v
            with self.subTest(k=k),self.assertRaises(c.Miss):
                self.admit(a,d)
        a,r,j,d=fixture()
        d["actions/artifacts/9"]["digest"]="sha256:"+"d"*64
        with self.assertRaises(c.Miss):
            self.admit(a,d)
    def test_wrong_scope_and_nonancestor(self):
        a,r,j,d=fixture()
        for kwargs in [{"ancestry":False},{"scope":{"different":True}}]:
            with self.assertRaises(c.Miss):
                self.admit(a,d,**kwargs)
        def never(path):
            raise AssertionError("discovery after scope mismatch")
        with patch.object(c,"remote_scope",return_value={"changed":True}):
            with self.assertRaises(c.Miss):
                c.find_artifact(never,SCOPE,BASE)
    def test_scope_key_binds_formal_and_pins_not_commit(self):
        entries={p:("040000","tree","d"*40) if p in ("formal","lean")
                 else ("100644","blob",c.FIXED.get(p,"c"*40)) for p in c.PATHS}
        original=c.make_scope(entries)
        self.assertEqual(c.digest(original),c.digest(c.make_scope(dict(entries))))
        self.assertNotEqual(c.digest(original),c.digest(c.make_scope(dict(entries,formal=("040000","tree","e"*40)))))
        changed=dict(entries)
        changed["lake-manifest.json"]=("100644","blob","e"*40)
        with self.assertRaises(c.Miss):
            c.make_scope(changed)

class Transport(unittest.TestCase):
    def payload(self,p):
        build=p/"build"
        (build/c.SENTINEL.parent).mkdir(parents=True)
        (build/c.SENTINEL).write_bytes(b"fixture only")
        log=p/"log"
        log.write_text("Build completed successfully (1 jobs).\n")
        out=p/"payload"
        c.pack_payload(build,out,SCOPE,HEAD,7,2,log)
        return out,{"source_head":HEAD,"run_id":7,"run_attempt":2,"scope_digest":c.digest(SCOPE)}
    def test_round_trip(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)
            out,e=self.payload(p)
            c.verify_payload(out,p/"restored",SCOPE,e)
            self.assertEqual((p/"restored"/c.SENTINEL).read_bytes(),b"fixture only")
            self.assertFalse(json.loads((out/"manifest.json").read_text())["proof_authority"])
    def test_digest_and_authority_tamper(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)
            out,e=self.payload(p)
            with (out/"build.tar.gz").open("ab") as f:
                f.write(b"tamper")
            with self.assertRaises(c.Miss):
                c.verify_payload(out,p/"restored",SCOPE,e)
            self.assertFalse((p/"restored").exists())
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)
            out,e=self.payload(p)
            m=json.loads((out/"manifest.json").read_text())
            m["proof_authority"]=True
            (out/"manifest.json").write_text(json.dumps(m))
            with self.assertRaises(c.Miss):
                c.verify_payload(out,p/"restored",SCOPE,e)
    def test_reject_traversal_links_duplicates(self):
        for name,kind in [("../escape",tarfile.REGTYPE),("/absolute",tarfile.REGTYPE),
                          ("link",tarfile.SYMTYPE),("hard",tarfile.LNKTYPE),("same",tarfile.REGTYPE)]:
            with self.subTest(name=name),tempfile.TemporaryDirectory() as t:
                p=Path(t)/"bad.tar.gz"
                with tarfile.open(p,"w:gz") as f:
                    m=tarfile.TarInfo(name)
                    m.type=kind
                    m.linkname="../escape"
                    f.addfile(m,io.BytesIO(b""))
                    if name=="same":
                        f.addfile(m,io.BytesIO(b""))
                with tarfile.open(p,"r:gz") as f:
                    with self.assertRaises(c.Miss):
                        c.safe_members(f)
    def test_invalid_zip_and_red_log(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)
            with zipfile.ZipFile(p/"bad.zip","w") as z:
                z.writestr("../escape","x")
            with self.assertRaises(c.Miss):
                c.unpack_zip(p/"bad.zip",p/"out")
            log=p/"log"
            log.write_text("timeout\n")
            with self.assertRaises(c.Miss):
                c.strict_log_ok(log)

class Workflow(unittest.TestCase):
    def test_main_only_and_unchanged_required_pr_build(self):
        pub=(ROOT/c.PUBLISHER).read_text()
        gate=(ROOT/".github/workflows/pr-governance-gate.yml").read_text()
        self.assertIn("branches: [main]",pub)
        self.assertIn("github.ref == 'refs/heads/main'",pub)
        self.assertIn("steps.strict.outcome == 'success'",pub)
        self.assertNotIn("pull_request_target:",pub)
        self.assertIn("scripts/build_lean4.sh --no-update --no-cache --target KuuOSFormal",pub)
        self.assertIn("steps.lean-pr-build-cache.outputs.cache-matched-key == ''",gate)
        self.assertLess(gate.index("Restore verified canonical Lean project artifact"),gate.index("Run selected Lean check"))
        self.assertIn("-KleanArgs=-DwarningAsError=true",gate)
        self.assertIn("-KleanArgs=-DsorryAsError=true",gate)
        self.assertIn("Save PR-local Lean build overlay",gate)


class ProductionRoutingRegression(unittest.TestCase):
    """Retain old overlay on failure; discover only admitted live artifacts."""
    def test_discovery_skips_newer_noncanonical_candidate(self):
        a,r,j,data=fixture()
        a["expires_at"]=(datetime.now(timezone.utc)+timedelta(days=10)).isoformat()
        data["actions/artifacts/9"]=copy.deepcopy(a)
        bad=copy.deepcopy(a)
        bad["id"]=10
        bad["workflow_run"]["head_branch"]="research"
        data["actions/workflows/"+Path(c.PUBLISHER).name]={"id":3,"path":c.PUBLISHER}
        listing="actions/artifacts?name="+c.PREFIX+c.digest(SCOPE)+"&per_page=100"
        data[listing]={"total_count":2,"artifacts":[a,bad]}
        with patch.object(c,"remote_scope",return_value=SCOPE),patch.object(c,"ancestor",return_value=True):
            selected=c.find_artifact(data.__getitem__,SCOPE,BASE)
        self.assertEqual(selected["artifact_id"],9)
        self.assertEqual(selected["run_id"],7)

    def test_truncated_discovery_is_a_miss_before_admission(self):
        a,r,j,data=fixture()
        data["actions/workflows/"+Path(c.PUBLISHER).name]={"id":3,"path":c.PUBLISHER}
        listing="actions/artifacts?name="+c.PREFIX+c.digest(SCOPE)+"&per_page=100"
        data[listing]={"total_count":2,"artifacts":[a]}
        with patch.object(c,"remote_scope",return_value=SCOPE),patch.object(c,"admit_artifact") as admit:
            with self.assertRaisesRegex(c.Miss,"truncated"):
                c.find_artifact(data.__getitem__,SCOPE,BASE)
            admit.assert_not_called()

    def test_invalid_archive_preserves_existing_project_overlay(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)
            source=p/"source"
            (source/c.SENTINEL.parent).mkdir(parents=True)
            (source/c.SENTINEL).write_bytes(b"isolated fixture, not proof")
            log=p/"log"
            log.write_text("Build completed successfully (1 jobs).\n")
            payload=p/"payload"
            c.pack_payload(source,payload,SCOPE,HEAD,7,2,log)
            with (payload/"build.tar.gz").open("ab") as f:
                f.write(b"tamper")
            archive=p/"invalid.zip"
            with zipfile.ZipFile(archive,"w") as z:
                for item in sorted(payload.iterdir()):
                    z.write(item,arcname=item.name)
            root=p/"checkout"
            old=root/".lake/build"
            old.mkdir(parents=True)
            marker=old/"existing.trace"
            marker.write_bytes(b"preserve exact existing overlay")
            def copy_archive(e,dst):
                dst.write_bytes(archive.read_bytes())
            e={"source_head":HEAD,"run_id":7,"run_attempt":2,"scope_digest":c.digest(SCOPE)}
            with patch.object(c,"download_zip",side_effect=copy_archive):
                with self.assertRaisesRegex(c.Miss,"project digest mismatch"):
                    c.restore(root,SCOPE,e)
            self.assertEqual(marker.read_bytes(),b"preserve exact existing overlay")
            self.assertFalse((old/c.SENTINEL).exists())
            self.assertEqual(sorted(x.name for x in (root/".lake").iterdir()),["build"])

if __name__=="__main__":
    unittest.main()
