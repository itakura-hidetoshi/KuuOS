#!/usr/bin/env python3
"""Version-bound, append-only DIRECT Lean candidate loop for an isolated Sandbox.

No git/gh, GitHub API, CI dispatch, model API, source overwrite or merge.
Candidates are supplied by CodeAI/MCP or a researcher into an append-only inbox.
Local success is NOT independent CI or authority for downstream theorems.
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Any

VERSION = "kuuos_sandbox_lean_cycle_v1"
LEAN_PIN = "leanprover/lean4:v4.30.0-rc2"
MATHLIB_PIN = "5450b53e5ddc75d46418fabb605edbf36bd0beb6"
STANDARD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
SHA1_RE = re.compile(r"^[a-f0-9]{40}$")
HEX64_RE = re.compile(r"^[a-f0-9]{64}$")
DECL = re.compile(
    r"(?m)^[ \t]*(?:(private|protected)\s+)?"
    r"(?:(?:noncomputable|irreducible)\s+)?"
    r"(theorem|lemma|def|abbrev|structure|class|instance)\s+([A-Za-z_][\w']*)\b"
)
TRUST_BYPASS = re.compile(
    r"\b(?:sorry|admit|axiom|unsafe|native_decide|implemented_by)\b"
    r"|debug\.skipKernelTC|set_option\s+debug\.skipKernelTC"
)
ERROR = re.compile(r"(?m)^.*?(?:\.lean:\d+:\d+:\s*)?error(?:\([^)]*\))?:")
AXIOMS = re.compile(r"'([^']+)'\s+depends on axioms:\s*\[([^\]]*)\]", re.S)
NO_AXIOMS = re.compile(r"'([^']+)'\s+does not depend on any axioms", re.S)


class Hold(RuntimeError):
    pass


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def git_blob(b: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()


def without_comments_strings(source: str) -> str:
    """Mask Lean nested comments and strings while retaining newline positions."""
    out = []
    i = 0
    depth = 0
    quoted = False
    while i < len(source):
        c = source[i]
        pair = source[i:i + 2]
        if depth:
            if pair == "/-":
                depth += 1
                out.extend("  ")
                i += 2
                continue
            if pair == "-/":
                depth -= 1
                out.extend("  ")
                i += 2
                continue
            out.append("\n" if c == "\n" else " ")
            i += 1
            continue
        if quoted:
            if c == "\\" and i + 1 < len(source):
                out.extend("  ")
                i += 2
                continue
            if c == '"':
                quoted = False
            out.append("\n" if c == "\n" else " ")
            i += 1
            continue
        if pair == "--":
            j = source.find("\n", i)
            if j < 0:
                out.extend(" " * (len(source) - i))
                break
            out.extend(" " * (j - i))
            i = j
            continue
        if pair == "/-":
            depth = 1
            out.extend("  ")
            i += 2
            continue
        if c == '"':
            quoted = True
            out.append(" ")
            i += 1
            continue
        out.append(c)
        i += 1
    if depth or quoted:
        raise Hold("NO_DATA: unterminated Lean comment or string")
    return "".join(out)


def declarations(source: str) -> dict[str, str]:
    stripped = without_comments_strings(source)
    found = list(DECL.finditer(stripped))
    result: dict[str, str] = {}
    for index, match in enumerate(found):
        if match.group(1) == "private":
            continue
        name = match.group(3)
        if name in result:
            raise Hold("duplicate public declaration: " + name)
        stop = found[index + 1].start() if index + 1 < len(found) else len(stripped)
        text = stripped[match.start():stop]
        terminators = [p for p in (text.find(":="), text.find("\nwhere")) if p >= 0]
        if not terminators:
            raise Hold("NO_DATA: declaration boundary not recognized: " + name)
        signature = re.sub(r"\s+", " ", text[:min(terminators)]).strip()
        result[name] = signature
    if not result:
        raise Hold("NO_DATA: no named public declarations")
    return result


def imports(source: str) -> list[str]:
    return re.findall(r"(?m)^\s*import\s+([A-Za-z0-9_.]+)\s*$",
                      without_comments_strings(source))


def require_pins(root: Path, *, verify_binaries: bool = True) -> dict[str, str]:
    if (root / "lean-toolchain").read_text(encoding="utf8").strip() != LEAN_PIN:
        raise Hold("PIN_MISMATCH: lean-toolchain")
    manifest = json.loads((root / "lake-manifest.json").read_text(encoding="utf8"))
    versions = [p.get("rev") for p in manifest.get("packages", [])
                if isinstance(p, dict) and p.get("name") == "mathlib"]
    if versions != [MATHLIB_PIN]:
        raise Hold("PIN_MISMATCH: lake-manifest mathlib")
    if verify_binaries:
        for command, expected in ((["lean", "--version"], "4.30.0-rc2"),
                                  (["lake", "--version"], "4.30.0-rc2")):
            try:
                p = subprocess.run(command, cwd=root, capture_output=True,
                                   text=True, timeout=20, check=False)
            except (OSError, subprocess.TimeoutExpired) as exc:
                raise Hold("NO_DATA: binary missing or unresponsive: " + command[0]) from exc
            if p.returncode or expected not in p.stdout + p.stderr:
                raise Hold("PIN_MISMATCH: runtime " + command[0])
    return {"lean_toolchain": LEAN_PIN, "mathlib_sha": MATHLIB_PIN}


def read_admission(path: Path | None) -> tuple[dict[str, str], dict[str, str]]:
    if path is None:
        return {}, {}
    data = json.loads(path.read_text(encoding="utf8"))
    if not isinstance(data, dict) or set(data) != {"signature_changes", "import_additions"}:
        raise Hold("invalid admission manifest")
    entries = []
    result = []
    for key, out in (("signature_changes", entries), ("import_additions", result)):
        values = data[key]
        if not isinstance(values, list):
            raise Hold("invalid admission list: " + key)
        for obj in values:
            if not isinstance(obj, dict) or set(obj) != {"name", "reason"}:
                raise Hold("invalid admission entry")
            name, reason = obj["name"], obj["reason"]
            if not isinstance(name, str) or not isinstance(reason, str) or len(reason.strip()) < 12:
                raise Hold("admission must carry a substantive named reason")
            if name in [x[0] for x in out]:
                raise Hold("duplicate admission: " + name)
            out.append((name, reason))
    return dict(entries), dict(result)


def source_contract(original: str, candidate: str,
                    admitted_signatures: dict[str, str],
                    admitted_imports: dict[str, str]) -> dict[str, Any]:
    masked = without_comments_strings(candidate)
    if TRUST_BYPASS.search(masked):
        raise Hold("TRUST_BYPASS: candidate introduces or contains unsafe proof escape")
    lhs, rhs = declarations(original), declarations(candidate)
    if list(lhs) != list(rhs):
        raise Hold("DECLARATION_OBSTRUCTION: public names/order changed")
    changed = [name for name in lhs if lhs[name] != rhs[name]]
    if any(name not in admitted_signatures for name in changed):
        raise Hold("SIGNATURE_OBSTRUCTION: unreviewed change " +
                   ",".join(name for name in changed if name not in admitted_signatures))
    if any(name not in changed for name in admitted_signatures):
        raise Hold("SIGNATURE_OBSTRUCTION: stale or surplus admission")
    orig_imports, new_imports = imports(original), imports(candidate)
    missing = [x for x in orig_imports if x not in new_imports]
    added = [x for x in new_imports if x not in orig_imports]
    if missing:
        raise Hold("IMPORT_OBSTRUCTION: removed imports " + ",".join(missing))
    if any(x not in admitted_imports for x in added):
        raise Hold("IMPORT_OBSTRUCTION: unexplained imports " +
                   ",".join(x for x in added if x not in admitted_imports))
    if any(x not in added for x in admitted_imports):
        raise Hold("IMPORT_OBSTRUCTION: stale or surplus import admission")
    return {"public_declarations": list(lhs),
            "signature_changes": {k: admitted_signatures[k] for k in changed},
            "import_additions": {k: admitted_imports[k] for k in added},
            "declaration_statement_text_unchanged": not bool(changed)}


def run_lean(root: Path, script: Path, output: Path, *, seconds: int) -> dict[str, Any]:
    """Lake requires input inside the project root; use a disposable local copy.

    The authoritative source is never overwritten. The sandbox-only transient
    source is deleted unconditionally; the receipt and logs remain outside root.
    """
    output.mkdir(parents=True, exist_ok=False)
    with tempfile.TemporaryDirectory(prefix=".kuuos-lean-scratch-", dir=root) as scratch:
        staged = Path(scratch) / script.name
        staged.write_bytes(script.read_bytes())
        cmd = ["lake", "env", "lean", "-DwarningAsError=true",
               "-Dweak.sorryAsError=true", "-o", str(output / "candidate.olean"), str(staged)]
        with (output / "stdout.log").open("xb") as stdout, (output / "stderr.log").open("xb") as stderr:
            try:
                proc = subprocess.run(cmd, cwd=root, stdout=stdout, stderr=stderr,
                                      timeout=seconds, check=False)
                code = proc.returncode
                timed_out = False
            except subprocess.TimeoutExpired:
                code = None
                timed_out = True
            except OSError as exc:
                raise Hold("NO_DATA: lake/lean execution failed") from exc
    log = ((output / "stdout.log").read_text(encoding="utf8", errors="replace") +
           (output / "stderr.log").read_text(encoding="utf8", errors="replace"))
    errors = ERROR.findall(log)
    missing_diagnostics = code not in (0, None) and not errors
    return {"exit_code": code, "timed_out": timed_out, "error_count": len(errors),
            "first_errors": errors[:12], "log_sha256":sha256(log.encode()),
            "olean_created": (output / "candidate.olean").is_file(),
            "no_data_failure_diagnostics": missing_diagnostics,
            "direct_success": code == 0 and not timed_out and not errors
            and (output / "candidate.olean").is_file()}


def audit_axioms(log: str, names: list[str], namespace: str) -> dict[str, Any]:
    reports = dict(AXIOMS.findall(log))
    zero = NO_AXIOMS.findall(log)
    for name in zero:
        reports[name] = ""
    expected = [namespace + "." + name for name in names]
    if len(reports) != len(expected) or set(reports) != set(expected):
        raise Hold("AXIOM_NO_DATA: missing, additional, or duplicated declarations")
    used = {ax.strip() for value in reports.values()
            for ax in value.split(",") if ax.strip()}
    if "sorryAx" in log or used - STANDARD_AXIOMS:
        raise Hold("AXIOM_OBSTRUCTION: " + ",".join(sorted(used - STANDARD_AXIOMS)))
    return {"checked": len(reports), "allowed": sorted(used),
            "sorryAx": False, "nonstandard": []}


def attempt(root: Path, source_path: Path, candidate_file: Path,
            admission: tuple[dict[str, str], dict[str, str]], namespace: str,
            attempt_dir: Path, timeout: int) -> dict[str, Any]:
    original = source_path.read_bytes()
    if candidate_file.is_symlink() or not candidate_file.is_file():
        raise Hold("candidate not regular or is symlink")
    data = candidate_file.read_bytes()
    if not (0 < len(data) <= 2_000_000):
        raise Hold("candidate size invalid")
    if data == original:
        raise Hold("candidate unchanged")
    candidate = data.decode("utf8")
    contract = source_contract(original.decode("utf8"), candidate, *admission)
    attempt_dir.mkdir(parents=True, exist_ok=False)
    (attempt_dir / "candidate.lean").write_bytes(data)
    compiled = run_lean(root, attempt_dir / "candidate.lean",
                        attempt_dir / "direct", seconds=timeout)
    result: dict[str, Any] = {"candidate_sha256":sha256(data),
        "candidate_blob":git_blob(data), "candidate_bytes":len(data),
        "contract":contract, "direct_lean":compiled,
        "independent_ci_success":False, "git_write_performed":False,
        "merged":False, "authority":"LOCAL_ONLY"}
    if not compiled["direct_success"]:
        result["status"] = ("NO_DATA_TIMEOUT" if compiled["timed_out"] else
                            "NO_DATA_EXECUTION" if compiled["no_data_failure_diagnostics"]
                            else "DIRECT_LEAN_FAILED")
        return result
    audit_file = attempt_dir / "audit.lean"
    audit_file.write_text(candidate + "\n" +
        "\n".join("#print axioms " + namespace + "." + x
                  for x in contract["public_declarations"]) + "\n", encoding="utf8")
    audit = run_lean(root, audit_file, attempt_dir / "axiom_audit", seconds=timeout)
    result["axiom_run"] = audit
    if not audit["direct_success"]:
        result["status"] = "AXIOM_AUDIT_UNCERTIFIED"
        return result
    text = (attempt_dir / "axiom_audit" / "stdout.log").read_text(encoding="utf8", errors="replace")
    result["axioms"] = audit_axioms(text, contract["public_declarations"], namespace)
    result["status"] = "LOCAL_DIRECT_LEAN_AND_AXIOMS_GREEN_ONLY"
    return result


def append_receipt(ledger: Path, data: dict[str, Any]) -> None:
    line = json.dumps(data, sort_keys=True, ensure_ascii=False) + "\n"
    with ledger.open("a", encoding="utf8") as f:
        f.write(line)
        f.flush()
        os.fsync(f.fileno())


def run(args: argparse.Namespace) -> int:
    root = Path(args.project_root).resolve(strict=True)
    source = (root / args.source).resolve(strict=True)
    if not source.is_relative_to(root) or source.suffix != ".lean":
        raise Hold("SOURCE_OBSTRUCTION: outside root or not Lean")
    pin = require_pins(root)
    original = source.read_bytes()
    if not SHA1_RE.fullmatch(args.source_blob) or git_blob(original) != args.source_blob:
        raise Hold("SOURCE_OBSTRUCTION: exact original Git blob mismatch")
    inbox = Path(args.candidates_dir).resolve(strict=True)
    receipts = Path(args.receipt_dir).resolve()
    if inbox.is_relative_to(root) or receipts.is_relative_to(root):
        raise Hold("isolation failure: inbox and ledger must be outside project root")
    receipts.mkdir(parents=True, exist_ok=True)
    if inbox == receipts or inbox.is_relative_to(receipts) or receipts.is_relative_to(inbox):
        raise Hold("isolation failure: receipt and inbox overlap")
    if not re.fullmatch(r"[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*", args.namespace):
        raise Hold("invalid fully qualified namespace")
    admission = read_admission(Path(args.admission).resolve() if args.admission else None)
    with (receipts / ".single_writer.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        ledger = receipts / "ledger.jsonl"
        previous = [json.loads(line) for line in ledger.read_text().splitlines()] if ledger.exists() else []
        completed = {x["candidate_sha256"] for x in previous
                     if "candidate_sha256" in x}
        current = git_blob(original)
        if current != args.source_blob:
            raise Hold("SOURCE_OBSTRUCTION: source changed after reading")
        rounds = 0
        last_new = time.monotonic()
        while rounds < args.max_attempts:
            if git_blob(source.read_bytes()) != args.source_blob:
                raise Hold("SOURCE_OBSTRUCTION: source changed while running")
            available = sorted(inbox.glob("*.lean"))
            fresh = []
            for item in available:
                if item.is_symlink():
                    raise Hold("untrusted symlink candidate")
                h = sha256(item.read_bytes())
                if h not in completed:
                    fresh.append((item, h))
            if not fresh:
                if args.idle_seconds == 0 or time.monotonic() - last_new >= args.idle_seconds:
                    break
                time.sleep(min(args.poll_seconds, args.idle_seconds))
                continue
            item, h = fresh[0]
            rounds += 1
            last_new = time.monotonic()
            # A stopped Sandbox may leave a partial attempt directory but no
            # receipt. Never overwrite it or mistake its missing log for green.
            existing = [p for p in receipts.glob("attempt-*") if p.is_dir()]
            indices = []
            orphaned = []
            for p in existing:
                match = re.fullmatch(r"attempt-(\d{5})-[a-f0-9]{12}", p.name)
                if not match:
                    raise Hold("NO_DATA: unrecognized attempt directory " + p.name)
                indices.append(int(match.group(1)))
                if not (p / "receipt.json").exists():
                    orphaned.append(p.name)
            index = max([len(previous)] + indices) + 1
            directory = receipts / ("attempt-%05d-%s" % (index, h[:12]))
            record: dict[str, Any] = {
                "schema":VERSION, "attempt":index, "candidate_file":item.name,
                "candidate_sha256":h, "original_blob":current,
                "source":str(source.relative_to(root)), "namespace":args.namespace,
                "pin":pin, "claimed_source_head":args.source_head,
                "source_head_authority":"CALLER_DECLARED_NOT_GITHUB_REOBSERVED",
                "git_write_performed":False, "independent_ci_success":False,
                "merged":False, "authority":"LOCAL_ONLY",
                "orphaned_prior_attempt_dirs": orphaned}
            try:
                record.update(attempt(root, source, item, admission, args.namespace,
                                      directory, args.timeout_seconds))
            except (Hold, UnicodeError) as exc:
                record.update({"status":"BLOCKED", "obstruction":str(exc)})
            if sha256(item.read_bytes()) != h:
                raise Hold("candidate mutated during verification; receipt withheld")
            if git_blob(source.read_bytes()) != current:
                raise Hold("source mutated during verification; receipt withheld")
            receipt_file = directory / "receipt.json"
            directory.mkdir(parents=True, exist_ok=True)
            if receipt_file.exists():
                raise Hold("append-only violation: existing receipt")
            with receipt_file.open("x", encoding="utf8") as f:
                json.dump(record, f, indent=2, ensure_ascii=False, sort_keys=True)
                f.write("\n")
            append_receipt(ledger, record)
            previous.append(record)
            completed.add(h)
            print("KUUOS_SANDBOX_LOCAL_RECEIPT " + json.dumps(record, ensure_ascii=False),
                  flush=True)
            if record["status"] == "LOCAL_DIRECT_LEAN_AND_AXIOMS_GREEN_ONLY":
                return 0
        print("KUUOS_SANDBOX_HOLD " + json.dumps(
            {"status":"NO_LOCAL_GREEN","rounds_this_invocation":rounds,
             "source_blob":current,"independent_ci_success":False,
             "git_write_performed":False}), flush=True)
        return 2


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--project-root", default=".")
    p.add_argument("--source", required=True)
    p.add_argument("--source-blob", required=True)
    p.add_argument("--source-head", default=None,
                   help="caller-declared GitHub SHA; only GitHub MCP can confirm it")
    p.add_argument("--namespace", required=True)
    p.add_argument("--candidates-dir", required=True)
    p.add_argument("--receipt-dir", required=True)
    p.add_argument("--admission", default=None,
                   help="explicit reasons for changed signatures/imports")
    p.add_argument("--max-attempts", type=int, default=12)
    p.add_argument("--timeout-seconds", type=int, default=240)
    p.add_argument("--idle-seconds", type=int, default=0)
    p.add_argument("--poll-seconds", type=int, default=3)
    args = p.parse_args(argv)
    if not 1 <= args.max_attempts <= 100 or not 10 <= args.timeout_seconds <= 3600 \
            or not 0 <= args.idle_seconds <= 14400 or not 1 <= args.poll_seconds <= 300:
        p.error("out-of-range bounded attempt/timeout/poll configuration")
    try:
        return run(args)
    except (Hold, OSError, ValueError, json.JSONDecodeError) as exc:
        print("KUUOS_SANDBOX_HOLD " + json.dumps(
            {"status":"BLOCKED","obstruction":str(exc),
             "git_write_performed":False,"independent_ci_success":False}),
              file=sys.stderr,flush=True)
        return 2


if __name__ == "__main__":
    sys.exit(main())
