#!/usr/bin/env python3
"""Verified main-only project build transport. A cache is never proof authority."""
from __future__ import annotations
import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import platform
import re
import shutil
import stat
import subprocess
import tarfile
import tempfile
from urllib.error import HTTPError
from urllib.parse import urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener, urlopen
import zipfile

ROOT = Path(__file__).resolve().parents[1]
REPO = "itakura-hidetoshi/KuuOS"
REPO_ID = 1235298309
API = "https://api.github.com/repos/" + REPO
PUBLISHER = ".github/workflows/lean-certified-project-cache-v1.yml"
SCRIPT = "scripts/ci_verified_lean_project_cache_v1.py"
SCHEMA = "kuuos.verified-main-lean-project-cache.v1"
PREFIX = "kuuos-verified-lean-project-v1-"
JOB = "Build and publish certified canonical Lean project"
STEPS = ("Compile full strict Lean project",
         "Verify exact source and pack certified overlay",
         "Publish canonical project artifact")
STRICT = ["lake", "-KleanArgs=-DwarningAsError=true",
          "-KleanArgs=-DsorryAsError=true", "build", "KuuOSFormal"]
PATHS = ("formal", "lean", "lakefile.toml", "lake-manifest.json",
         "lean-toolchain", "scripts/bootstrap_pinned_lean_ci.sh",
         "scripts/build_lean4.sh", SCRIPT, PUBLISHER)
FIXED = {"lakefile.toml": "947bac41f9535a7ba2ef03a93081cdfbc1b946f7",
         "lake-manifest.json": "4b795033645fd37e42e67014abc3e0d5925a227c",
         "lean-toolchain": "6c7e31fffe3e03be3e0d7021acd9cd848e44db26"}
HEX40 = re.compile(r"[0-9a-f]{40}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
MAX_ZIP = 3 * 1024**3
MAX_LOG = 100 * 1024**2
MAX_TAR = 12 * 1024**3
SENTINEL = Path("lib/lean/KuuOSFormal.olean")
PAYLOAD = {"manifest.json", "build.tar.gz", "strict.log"}


class Miss(ValueError):
    pass


def need(ok, reason):
    if not ok:
        raise Miss(reason)


def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":"),
                                    ensure_ascii=False).encode()).hexdigest()


def sha_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024**2), b""):
            h.update(chunk)
    return h.hexdigest()


def git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


def make_scope(entries):
    need(set(entries) == set(PATHS), "incomplete source inventory")
    for path, (mode, kind, sha) in entries.items():
        need(isinstance(sha, str) and HEX40.fullmatch(sha), "bad source identity")
        need((mode, kind) == ("040000", "tree") if path in ("formal", "lean")
             else (mode, kind) in (("100644", "blob"), ("100755", "blob")),
             "unexpected source kind")
    need(all(entries[p][2] == v for p, v in FIXED.items()), "unsupported pinned configuration")
    return {"schema": SCHEMA, "repository": REPO, "runner": "ubuntu-24.04/Linux/X64",
            "strict_command": STRICT, "entries": {p: list(entries[p]) for p in sorted(entries)}}


def local_scope(root, head):
    need(HEX40.fullmatch(head) and git(root, "rev-parse", "HEAD") == head,
         "checkout head mismatch")
    need(platform.system() == "Linux" and platform.machine() == "x86_64",
         "unsupported platform")
    need(not (root / "lakefile.lean").exists(), "alternate Lake configuration")
    need(not git(root, "status", "--porcelain", "--untracked-files=all", "--", *PATHS),
         "dirty proof inputs")
    entries = {}
    for path in PATHS:
        line = git(root, "ls-tree", head, "--", path)
        need("\t" in line and "\n" not in line, "missing source input")
        meta, name = line.split("\t", 1)
        need(name == path, "unexpected source path")
        entries[path] = tuple(meta.split())
    return make_scope(entries)


def api(path):
    token = os.environ.get("GH_TOKEN")
    need(token, "missing read token")
    req = Request(API + "/" + path, headers={"Authorization": "Bearer " + token,
        "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "KuuOS-verified-cache-v1"})
    with urlopen(req, timeout=40) as f:
        data = f.read(16 * 1024**2 + 1)
    need(len(data) <= 16 * 1024**2, "oversized metadata")
    return json.loads(data)


def remote_scope(get, head):
    need(HEX40.fullmatch(head), "bad remote head")
    commit = get("git/commits/" + head)
    need(commit["sha"] == head, "remote commit mismatch")
    trees = {}
    def tree(sha):
        if sha not in trees:
            d = get("git/trees/" + sha)
            need(d["sha"] == sha and d["truncated"] is False, "incomplete remote tree")
            trees[sha] = {v["path"]: v for v in d["tree"]}
            need(len(trees[sha]) == len(d["tree"]), "duplicate tree entry")
        return trees[sha]
    root = commit["tree"]["sha"]
    need("lakefile.lean" not in tree(root), "alternate remote Lake configuration")
    entries = {}
    for path in PATHS:
        sha = root
        parts = path.split("/")
        for i, part in enumerate(parts):
            row = tree(sha)[part]
            sha = row["sha"]
            if i < len(parts)-1:
                need(row["type"] == "tree", "non-tree parent")
        entries[path] = (row["mode"], row["type"], row["sha"])
    return make_scope(entries)


def ancestor(get, head, base):
    if head == base:
        return True
    c = get("compare/" + head + "..." + base + "?per_page=1")
    return (c.get("status") in ("ahead", "identical")
            and c.get("base_commit", {}).get("sha") == head
            and c.get("merge_base_commit", {}).get("sha") == head)


def admit_artifact(get, a, scope, base, workflow_id, min_days=0, now=None):
    now = now or datetime.now(timezone.utc)
    need(a.get("name") == PREFIX + digest(scope) and a.get("expired") is False,
         "wrong or expired artifact")
    need(datetime.fromisoformat(a["expires_at"].replace("Z", "+00:00"))
         > now + timedelta(days=min_days), "artifact too near expiry")
    need(type(a["id"]) is int and a["id"] > 0 and type(a["size_in_bytes"]) is int
         and 0 < a["size_in_bytes"] <= MAX_ZIP, "invalid artifact identity/size")
    d = a.get("digest")
    need(isinstance(d, str) and d.startswith("sha256:") and HEX64.fullmatch(d[7:]),
         "missing artifact digest")
    w = a["workflow_run"]
    need(w["repository_id"] == w["head_repository_id"] == REPO_ID
         and w["head_branch"] == "main", "noncanonical artifact origin")
    head = w["head_sha"]
    need(HEX40.fullmatch(head), "bad producer head")
    run = get("actions/runs/" + str(w["id"]))
    need(run["id"] == w["id"] and run["workflow_id"] == workflow_id
         and run["head_sha"] == head and run["head_branch"] == "main"
         and run["event"] in ("push", "workflow_dispatch")
         and run["repository"]["id"] == run["head_repository"]["id"] == REPO_ID
         and run["status"] == "completed" and run["conclusion"] == "success"
         and run["path"].split("@",1)[0] == PUBLISHER, "producer not exact canonical green")
    attempt = run["run_attempt"]
    need(type(attempt) is int and attempt > 0, "invalid producer attempt")
    jobs = get("actions/runs/" + str(run["id"]) + "/attempts/" + str(attempt)
               + "/jobs?per_page=100")
    need(jobs["total_count"] == len(jobs["jobs"]), "incomplete job inventory")
    js = [j for j in jobs["jobs"] if j["name"] == JOB]
    need(len(js) == 1, "missing/ambiguous producer job")
    j = js[0]
    need(j["head_sha"] == head and j["status"] == "completed"
         and j["conclusion"] == "success", "producer job not green")
    ss = {s["name"]: s for s in j["steps"]}
    for name in STEPS:
        need(ss[name]["status"] == "completed" and ss[name]["conclusion"] == "success",
             "publisher step not green")
    need(ancestor(get, head, base) and remote_scope(get, head) == scope,
         "producer ancestry/source scope mismatch")
    exact = get("actions/artifacts/" + str(a["id"]))
    for k in ("id", "name", "digest", "size_in_bytes", "expired", "workflow_run", "expires_at"):
        need(exact[k] == a[k], "artifact metadata drift")
    return {"artifact_id": a["id"], "artifact_digest": d[7:], "artifact_size": a["size_in_bytes"],
            "source_head": head, "run_id": run["id"], "run_attempt": attempt,
            "job_id": j["id"], "scope_digest": digest(scope)}


def find_artifact(get, scope, base, min_days=0):
    need(HEX40.fullmatch(base) and remote_scope(get, base) == scope,
         "current proof scope differs from actual base")
    workflow = get("actions/workflows/" + Path(PUBLISHER).name)
    need(workflow["path"] == PUBLISHER, "wrong producer workflow")
    results = get("actions/artifacts?" + urlencode({"name": PREFIX+digest(scope), "per_page":100}))
    need(results["total_count"] <= len(results["artifacts"]), "artifact discovery truncated")
    for a in sorted(results["artifacts"], key=lambda x:x["id"], reverse=True):
        try:
            return admit_artifact(get, a, scope, base, workflow["id"], min_days)
        except (Miss, KeyError, TypeError, ValueError, HTTPError):
            continue
    raise Miss("no admissible canonical artifact")


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def download_zip(e, path):
    # GitHub token is never sent to the signed storage URL.
    req = Request(API + "/actions/artifacts/" + str(e["artifact_id"]) + "/zip",
                  headers={"Authorization":"Bearer "+os.environ["GH_TOKEN"],
                           "Accept":"application/vnd.github+json",
                           "User-Agent":"KuuOS-verified-cache-v1"})
    try:
        with build_opener(NoRedirect()).open(req, timeout=45):
            raise Miss("download did not redirect")
    except HTTPError as exc:
        need(exc.code in (301,302,303,307,308), "download rejected")
        url = exc.headers["Location"]
        exc.close()
    u = urlsplit(url)
    need(u.scheme == "https" and u.hostname and not u.username and not u.password,
         "invalid signed download location")
    h = hashlib.sha256()
    size = 0
    with urlopen(Request(url, headers={"User-Agent":"KuuOS-cache-v1"}), timeout=90) as src:
        need(urlsplit(src.geturl()).scheme == "https", "non-HTTPS archive")
        with path.open("xb") as f:
            for chunk in iter(lambda:src.read(1024**2),b""):
                size += len(chunk)
                need(size <= MAX_ZIP, "oversized download")
                h.update(chunk)
                f.write(chunk)
    need(size == e["artifact_size"] and h.hexdigest() == e["artifact_digest"],
         "archive SHA256/size mismatch")


def strict_log_ok(log):
    need(0 < log.stat().st_size <= MAX_LOG, "invalid strict log")
    lines = log.read_text(encoding="utf-8", errors="replace").splitlines()
    need(any(re.fullmatch(r"Build completed successfully \(\d+ jobs\)\.", l.strip())
             for l in lines), "missing successful build marker")
    need(not any("PANIC at " in l and not re.search(
         r"PANIC at _private\.Lean\.LibrarySuggestions\.(SymbolFrequency|SineQuaNon)\.",l)
         for l in lines), "unexpected Lean panic")


def pack_payload(build, out, scope, head, run_id, attempt, log):
    need(build.is_dir() and not build.is_symlink() and (build/SENTINEL).is_file(),
         "missing complete project overlay")
    strict_log_ok(log)
    for p in build.rglob("*"):
        m = p.lstat().st_mode
        need(stat.S_ISREG(m) or stat.S_ISDIR(m), "unsafe overlay source")
    out.mkdir(parents=True, exist_ok=False)
    archive = out/"build.tar.gz"
    with tarfile.open(archive,"w:gz",compresslevel=1,dereference=True) as t:
        for p in sorted(build.iterdir()):
            t.add(p,arcname=p.name,recursive=True)
    need(archive.stat().st_size <= MAX_ZIP, "oversized project archive")
    shutil.copyfile(log,out/"strict.log")
    m = {"schema":SCHEMA,"scope":scope,"scope_digest":digest(scope),"source_head":head,
         "run_id":run_id,"run_attempt":attempt,"strict_command":STRICT,
         "archive_sha256":sha_file(archive),"archive_size":archive.stat().st_size,
         "strict_log_sha256":sha_file(out/"strict.log"),"proof_authority":False}
    (out/"manifest.json").write_text(json.dumps(m,sort_keys=True)+"\n")


def safe_members(t):
    rows = t.getmembers()
    need(0 < len(rows) <= 150000, "invalid archive inventory")
    seen = set()
    total = 0
    for m in rows:
        p = m.name
        need(p and not PurePosixPath(p).is_absolute() and "\\" not in p
             and all(x not in ("", ".", "..") for x in p.split("/")), "unsafe archive path")
        need(p not in seen and (m.isfile() or m.isdir()) and not (m.mode & 0o7000),
             "duplicate/link/special/privileged archive member")
        seen.add(p)
        total += m.size
        need(total <= MAX_TAR, "oversized expanded archive")
    return rows


def verify_payload(payload, dest, scope, e):
    mf = payload/"manifest.json"
    need(0 < mf.stat().st_size <= 256*1024, "invalid manifest size")
    m = json.loads(mf.read_text())
    need(m["schema"] == SCHEMA and m["scope"] == scope
         and m["scope_digest"] == e["scope_digest"] == digest(scope)
         and m["source_head"] == e["source_head"] and m["run_id"] == e["run_id"]
         and m["run_attempt"] == e["run_attempt"] and m["strict_command"] == STRICT
         and m["proof_authority"] is False, "manifest identity/authority mismatch")
    archive,log = payload/"build.tar.gz",payload/"strict.log"
    need(0 < archive.stat().st_size == m["archive_size"] <= MAX_ZIP
         and sha_file(archive) == m["archive_sha256"], "project digest mismatch")
    need(0 < log.stat().st_size <= MAX_LOG and sha_file(log) == m["strict_log_sha256"],
         "strict log digest mismatch")
    strict_log_ok(log)
    dest.mkdir()
    with tarfile.open(archive,"r:gz") as t:
        t.extractall(dest,members=safe_members(t),filter="data")
    need((dest/SENTINEL).is_file(), "missing restored project root")


def unpack_zip(archive,payload):
    payload.mkdir()
    with zipfile.ZipFile(archive) as z:
        infos=z.infolist()
        need(len(infos)==3 and {i.filename for i in infos}==PAYLOAD,"unexpected ZIP inventory")
        for i in infos:
            cap={"manifest.json":256*1024,"strict.log":MAX_LOG,"build.tar.gz":MAX_ZIP}[i.filename]
            need(0<i.file_size<=cap and not i.is_dir(),"invalid ZIP member")
            with z.open(i) as src,(payload/i.filename).open("xb") as dst:
                shutil.copyfileobj(src,dst)


def restore(root,scope,e):
    lake=root/".lake"
    need(not lake.is_symlink(),"unsafe Lake path")
    lake.mkdir(exist_ok=True)
    build=lake/"build"
    need(not build.is_symlink() and (not build.exists() or build.is_dir()),"unsafe destination")
    # Stage entirely before replacing any existing project build.
    with tempfile.TemporaryDirectory(prefix="verified-project-",dir=lake) as td:
        tmp=Path(td)
        download_zip(e,tmp/"artifact.zip")
        unpack_zip(tmp/"artifact.zip",tmp/"payload")
        verify_payload(tmp/"payload",tmp/"new",scope,e)
        old=tmp/"old"
        if build.exists():
            build.rename(old)
        try:
            (tmp/"new").rename(build)
        except BaseException:
            if old.exists():
                old.rename(build)
            raise
    print("KUUOS_VERIFIED_LEAN_PROJECT_RESTORED",json.dumps(e,sort_keys=True))


def outputs(**items):
    path=os.environ.get("GITHUB_OUTPUT")
    if path:
        with open(path,"a",encoding="utf-8") as f:
            for k,v in items.items():
                f.write(f"{k}={v}\n")


def main():
    p=argparse.ArgumentParser()
    p.add_argument("mode",choices=("probe","restore","pack"))
    p.add_argument("--base")
    p.add_argument("--min-days",type=int,default=0)
    p.add_argument("--out",type=Path)
    p.add_argument("--log",type=Path)
    a=p.parse_args()
    head=os.environ["GITHUB_SHA"]
    try:
        scope=local_scope(ROOT,head)
    except (Miss,OSError,ValueError,subprocess.SubprocessError) as exc:
        if a.mode=="pack":
            raise
        print("KUUOS_VERIFIED_CACHE_MISS: unsupported local scope",type(exc).__name__)
        outputs(eligible="false",available="false",restored="false")
        return
    outputs(eligible="true",scope_digest=digest(scope))
    if a.mode=="pack":
        need(os.environ.get("GITHUB_REPOSITORY")==REPO
             and os.environ.get("GITHUB_REF")=="refs/heads/main"
             and os.environ.get("GITHUB_EVENT_NAME") in ("push","workflow_dispatch"),
             "noncanonical publication forbidden")
        need(a.out and a.log,"missing pack paths")
        need(remote_scope(api,head)==scope,"canonical GitHub source mismatch")
        pack_payload(ROOT/".lake/build",a.out,scope,head,int(os.environ["GITHUB_RUN_ID"]),
                     int(os.environ["GITHUB_RUN_ATTEMPT"]),a.log)
        print("KUUOS_VERIFIED_LEAN_PROJECT_PACKED",digest(scope))
        return
    try:
        need(a.base is not None,"missing exact base")
        evidence=find_artifact(api,scope,a.base,a.min_days)
        if a.mode=="restore":
            restore(ROOT,scope,evidence)
        else:
            print("KUUOS_VERIFIED_LEAN_PROJECT_AVAILABLE",json.dumps(evidence,sort_keys=True))
        outputs(available="true",restored="true" if a.mode=="restore" else "false")
    except (OSError,KeyError,TypeError,ValueError,zipfile.BadZipFile,tarfile.TarError,
            EOFError,subprocess.SubprocessError) as exc:
        # No signed URLs, credentials or invented success on a miss.
        print("KUUOS_VERIFIED_CACHE_MISS",type(exc).__name__,str(exc) if isinstance(exc,Miss) else "")
        outputs(available="false",restored="false")


if __name__=="__main__":
    main()
