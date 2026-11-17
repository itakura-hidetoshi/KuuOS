#!/usr/bin/env python3
"""Selected source pins and declared test inventory for the Wa gate boundary.

This static checker imports no runtime or test modules. It retains the selected
original sources, fixed v0.12 loader/hook, and all seven v0.13 additions. Pins
cover the listed bytes, not a transitive closure, external authenticity, gate
semantics, or a Lean/Python refinement.

The seven v0.14 files are required when this checker is invoked. The unchanged
v0.12 loader does not unconditionally require every future version's tests.
Declared test names are syntax only: publication must separately verify the
submitted tree and actual CI test IDs, counts, and outcomes. Use a quiescent
checkout; this is not a race-safe filesystem authenticity mechanism.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import stat

ROOT = Path(__file__).resolve().parents[1]
SOURCE_MAIN = "05693ef17179ebddb974f23021be2e7d352b4fbb"
SOURCE_BLOBS = {
    "runtime/kuuos_lean_python_contract_bridge_v0_1.py": "f6c3f570a996f9fc6c65f026b2fb001ae03c0097",
    "runtime/kuuos_lean_python_os_path_composition_v0_6.py": "068158c2e4f90f5040f83504218e60752a5472ed",
    "runtime/kuuos_lean_python_native_cycle_ledger_replay_v0_7.py": "e1d4cdc5dd698b7c1aad1f2fcc3a9499a0eced49",
    "runtime/kuuos_lean_python_native_cycle_receipt_capture_v0_8.py": "219ace2ec190cd8bf91284d413914afa4c696aef",
    "runtime/kuuos_lean_python_isolated_native_receipt_evidence_v0_9.py": "4cfda1477ba5beac6b469668228cd3dda789c31c",
    "runtime/kuuos_qi_world_native_full_cycle_v1_3.py": "9830b98746fbe8cf550562a0719374471ed6e0e5",
    "runtime/kuuos_decision_os_kernel_v0_1.py": "7fbe347c0ae22f7efea0cb0147f1e1934ee743d4",
    "runtime/kuuos_decision_os_types_v0_1.py": "7a8432fad3eca3d04ac14e17cc4178833fd3c9aa",
    "runtime/kuuos_decision_os_store_v0_1.py": "7ddcc08cc7f3d4a6e274ff0406805ef632457931",
    "runtime/kuuos_plan_os_kernel_v0_1.py": "6942b32353b476fe8848d39c548d3cd2fe93ccff",
    "runtime/kuuos_plan_os_types_v0_1.py": "fa3945092610c38d748342e0c7aba1c7cebf08dc",
    "runtime/kuuos_plan_os_store_v0_1.py": "106a4adae2750bc543786c1ff36cd746a4d838d4",
    "runtime/kuuos_act_os_kernel_v0_1.py": "db91d45cefd8982309f4a8d58e792f0df0c2c5d4",
    "runtime/kuuos_act_os_types_v0_1.py": "6894f380cfbeee008610cf93d5357daac38e93cc",
    "runtime/kuuos_act_os_store_v0_1.py": "24ebc89667c493498926e8d03bb21f952f448cce",
    "runtime/kuuos_observe_os_kernel_v0_1.py": "670b205f975149cacc3d6a82c3f27edcded8c4ca",
    "runtime/kuuos_observe_os_types_v0_1.py": "2bed5ca44ad3de69daa0ac0d2cc3c462ea30c0c9",
    "runtime/kuuos_observe_os_store_v0_1.py": "7c6433b04fe83da4ac669a93d85f447591117897",
    "runtime/kuuos_verify_os_kernel_v0_1.py": "81a415d4eac83d0e828dca2a9e23a0dcfaedf4f0",
    "runtime/kuuos_verify_os_types_v0_1.py": "2889e0963f2171842e49ec477eec23e3a705eb6c",
    "runtime/kuuos_verify_os_store_v0_1.py": "6f08033b55fdde4d36cf2cb491da48cc4c40d00d",
    "runtime/kuuos_learn_os_kernel_v0_1.py": "8eeaf80af8522df2dc99a1df546b3145aafa2612",
    "runtime/kuuos_learn_os_types_v0_1.py": "3e74b2e672064c435ff785e03ea85b8c6ab5f5eb",
    "runtime/kuuos_learn_os_store_v0_1.py": "1a462212f9488c2b3dc2ca2ec96efcd7a20e0713",
    "runtime/kuuos_decision_os_state_v0_1.py": "80ea719c2a77fb30cef488fe5f9f1f9ae597991a",
    "runtime/kuuos_plan_os_state_v0_1.py": "20ebe52c2d8696281968fb4870f1904c976dac37",
    "scripts/run_kuuos_runtime_full_check_v0_55.py": "e529fca18f44687c271c3c958890dfb3940bc62a",
    "formal/KUOS/DecisionOS/RelationalDeliberationKernelV0_1.lean": "9891ab2aa20c8d2ea4df08abe3bf12d99aad6726",
    "formal/KUOS/PlanOS/ReplanBoundSynthesisV0_1.lean": "0ff6a060bbe52bee4d4bcbe1ebbbd319689f5676",
    "formal/KUOS/ActOS/AuthorityBoundInvocationV0_1.lean": "c08c8412d435553d9c2a20e309c7cdd4d649f360",
    "formal/KUOS/ObserveOS/EffectGroundedObservationV0_1.lean": "0dccacb16696fc05a8c0f8d70bc09c34a50828f5",
    "formal/KUOS/VerifyOS/EvidenceBoundVerificationV0_1.lean": "cb022ee1b0d43d5a67f38f879cc7e06f60092f9c",
    "formal/KUOS/LearnOS/FutureOnlyEvidenceLearningV0_1.lean": "6dc7ba9d3bf1b4d12ca11e21560ab94d664e8097",
    "runtime/kuuos_lean_python_checked_transition_v0_10.py": "5559bd9ca0e22ebc7809522e886188d9f61bc51b",
    "runtime/kuuos_lean_python_guarded_native_cycle_v0_10.py": "870e1620a7f5eea0c7ce5125be71f0aeb45c27a1",
    "scripts/check_kuuos_lean_python_checked_transition_sources_v0_10.py": "355c4c4080712cac468d0ccc3041a21c3a4165c7",
    "runtime/kuuos_act_os_fixture_v0_1.py": "dbb1bc7426172f98d41ebc38186be16ef6199808",
    "runtime/v01_act_os_authority_bound_invocation.py": "971949dd22fae9f029b153ec6ebe68ab4d91c9f8",
    "runtime/kuuos_cooperative_host_adapter_v0_17.py": "189a3a88c26337feb74522331df99ed9501fec19",
    "runtime/kuuos_cooperative_host_adapter_license_v0_17.py": "1701fc1a802ed1fa3c630e71f735ddbf3e343d33",
    "runtime/kuuos_cooperative_host_adapter_types_v0_17.py": "cd8706c47f1fe63c2347e7faf9669e2eecfb01b9",
    "runtime/kuuos_cooperative_execution_supervisor_types_v0_16.py": "0d5db8bd890d768466d768dd5d4a2a01badf978b",
    "runtime/v017_host_adapter_fixtures.py": "0c2b20c5079783d1ff26c0a61a930d6e5c6d3405",
    "runtime/kuuos_cooperative_host_adapter_idempotent_tick_v0_17.py": "d0b10d202c24d256aa893b5778fc844e71e3c8da",
    "runtime/kuuos_cooperative_host_adapter_tick_v0_17.py": "ce97b8ba695c877fb8851dc2526892c994865f1c",
    "runtime/kuuos_cooperative_host_adapter_projection_v0_17.py": "94ebae36cda5d0d4c4598a68fed0409e638b0288",
    "runtime/kuuos_cooperative_execution_supervisor_job_v0_16.py": "84460b7cdde00044a58eef7f085ad56f7e6d7ed5",
    "runtime/kuuos_resumable_execution_handoff_types_v0_15.py": "f83a58221d0fcd349faf90284b75c2a4a87527d3",
    "runtime/kuuos_cooperative_execution_supervisor_step_precheck_v0_16.py": "2fb286c549790917aa29296dbbc7c41a69bb8fd1",
    "runtime/kuuos_lean_python_pre_host_guard_v0_11.py": "c35c8a0ecf52c855432dedf1b840b92ca60cb4a8",
    "runtime/kuuos_lean_python_pre_host_native_cycle_v0_11.py": "d9c64475a0036a2c2e9a1b2e51738b58bda7d2a7",
    "scripts/check_kuuos_lean_python_pre_host_sources_v0_11.py": "5daab02ebed750547a8013ed3b263bd1f1d73619",
    "tests/test_kuuos_lean_python_os_registry_v0_5.py": "6acec6634ae5da2e197d2d497cadbd854ee91e65",
    "runtime/kuuos_decision_os_plural_kernel_v0_2.py": "fd7a336640c5f25e6596be5ec29ec36ff7fce03d",
    "runtime/kuuos_decision_os_plural_types_v0_2.py": "2fa6dced94e4cf296ff8243c6101e343807385da",
    "runtime/kuuos_decision_os_plural_store_v0_2.py": "45fb12e558c5ee6c442e4806022f2677c8ce777e",
    "runtime/kuuos_decision_os_wa_kernel_v0_3.py": "0ebc222ac5c73da86fea8c4e09f03782f84314b3",
    "runtime/kuuos_decision_os_wa_types_v0_3.py": "9c1a67003adf61b340c3ff5a8266706fd3ea19d7",
    "runtime/kuuos_decision_os_wa_store_v0_3.py": "7cd55ee49358df4e1b4e048195b258fd7bdd612b",
    "runtime/kuuos_decision_os_wa_state_v0_3.py": "b0e6ea237d14f3b41e7cd2caf9cc1813d0918734",
    "formal/KUOS/DecisionOS/PluralHarmonyAppealKernelV0_2.lean": "4b6588305193fb8d41e1fef9c66433a8b5ea67e5",
    "formal/KUOS/DecisionOS/WaRelationalHarmonyV0_3.lean": "c278f21eb3459bef28df8f99c42e5f6cccedc22e",
    "runtime/v02_decision_os_plural_harmony_appeal.py": "43d8819f32d5290f72bfb753656dbbcb4f2ab214",
    "runtime/v03_decision_os_wa_relational_harmony.py": "2ae49fbf54e4cb77c53a2e82371c35669d5863eb",
    "scripts/check_kuuos_lean_python_plan_act_bindings_v0_4.py": "1605b2e16c8d8c5a124c7a60102b4fc188993f63",
    "scripts/check_kuuos_lean_python_os_registry_v0_5.py": "e9b3fd5b02822302b8851f2990d0ac6dd4788af2",
    "docs/KUUOS_LEAN_PYTHON_MEDIATOR_TRANSITIONS_v0_12.md": "faf744996a90cf2c5ce3cfe65a250c93d2f14aee",
    "tests/lean_python_extensions/test_mediated_native_cycle_v0_12.py": "6160f9dc15c8713cd7aa9c98b2424bce51cf684f",
    "tests/lean_python_extensions/test_mediator_sources_v0_12.py": "f18bc2af6bca5de379932671156fc33669ab3f21",
    "tests/lean_python_extensions/test_mediator_transition_v0_12.py": "c4811fce15cd7a4241fabe076d6c293270b470b6",
    "tests/test_kuuos_lean_python_plan_act_native_v0_4.py": "684c32ecb69130ad82ee08d0606835cadffcb90e",
    "runtime/kuuos_belief_os_types_v0_1.py": "32eac0fa0b1cb52a999f0a17e67015905a541ba7",
    "runtime/kuuos_lean_python_mediated_native_cycle_v0_12.py": "5e6f4668b15305e6978eb66e43d9c6dda82f5fb3",
    "runtime/kuuos_lean_python_mediator_transition_v0_12.py": "e096451961294dc5b42b3fe4b96dfcc4104ece7b",
    "scripts/check_kuuos_lean_python_mediator_sources_v0_12.py": "63566ab97221bbf6b48a30919b6db24676fd648e",
    "tests/lean_python_extensions/__init__.py": "a6c9e8d6b5be760a9d25ad6d9c6e84ad64194249",
    "docs/KUUOS_LEAN_PYTHON_WA_NUMERIC_BOUNDARY_v0_13.md": "026b9169d4711485bcd4a9330df83170469a22ba",
    "runtime/kuuos_lean_python_wa_numeric_guard_v0_13.py": "37f2f1568aa2caa5ffa0e923866a274170faecd5",
    "runtime/kuuos_lean_python_wa_numeric_native_cycle_v0_13.py": "900bd7a880c3c0ab41323f783868733b05763d85",
    "scripts/check_kuuos_lean_python_wa_numeric_sources_v0_13.py": "ea7694edcdc2f06661fe6ea5a7229300e5221e8e",
    "tests/lean_python_extensions/test_wa_numeric_guard_v0_13.py": "d2e54e038d9a06faab9c9144832c734cf3cda125",
    "tests/lean_python_extensions/test_wa_numeric_native_cycle_v0_13.py": "a479fc1fb4dadc1843303fc07bb3edf3fa90cca1",
    "tests/lean_python_extensions/test_wa_numeric_sources_v0_13.py": "184f71e13a63db72a8872b4491d7c7eeeebda942"
}
REQUIRED_PATHS = (
    "runtime/kuuos_lean_python_wa_gate_guard_v0_14.py",
    "runtime/kuuos_lean_python_wa_gate_native_cycle_v0_14.py",
    "scripts/check_kuuos_lean_python_wa_gate_sources_v0_14.py",
    "tests/lean_python_extensions/test_wa_gate_guard_v0_14.py",
    "tests/lean_python_extensions/test_wa_gate_native_cycle_v0_14.py",
    "tests/lean_python_extensions/test_wa_gate_sources_v0_14.py",
    "docs/KUUOS_LEAN_PYTHON_WA_GATE_BOUNDARY_v0_14.md",
)
TEST_CLASSES = {
    "tests/lean_python_extensions/test_wa_gate_guard_v0_14.py": "WaGateGuardTests",
    "tests/lean_python_extensions/test_wa_gate_native_cycle_v0_14.py": "WaGateNativeCycleTests",
    "tests/lean_python_extensions/test_wa_gate_sources_v0_14.py": "WaGateSourceTests"
}


def _git_blob(raw: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw
    ).hexdigest()


def _read_file(root: Path, relative: str) -> tuple[bytes | None, str | None]:
    """Read regular bytes only, rejecting symlinks in every path component."""
    path = (root / relative).absolute()
    try:
        for parent in reversed(path.parents):
            mode = parent.lstat().st_mode
            if stat.S_ISLNK(mode):
                return None, "symlink_not_allowed"
            if not stat.S_ISDIR(mode):
                return None, "not_regular_file"
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            return None, "symlink_not_allowed"
        if not stat.S_ISREG(mode):
            return None, "not_regular_file"
        return path.read_bytes(), None
    except FileNotFoundError:
        return None, "missing"
    except OSError:
        return None, "unreadable"


def _test_inventory(root: Path) -> tuple[dict[str, tuple[str, ...]], list[str]]:
    inventory: dict[str, tuple[str, ...]] = {}
    issues: list[str] = []
    for relative, expected_class in TEST_CLASSES.items():
        raw, issue = _read_file(root, relative)
        if issue:
            issues.append("test_source_" + issue + ":" + relative)
            continue
        try:
            body = ast.parse(raw.decode("utf-8")).body
        except (SyntaxError, UnicodeError, ValueError, RecursionError):
            issues.append("test_source_invalid:" + relative)
            continue
        classes = [
            node for node in body
            if isinstance(node, ast.ClassDef) and node.name == expected_class
        ]
        location = relative + ":" + expected_class
        if len(classes) != 1:
            issues.append("required_test_class_missing_or_nonunique:" + location)
            continue
        methods = [
            node.name for node in classes[0].body
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")
        ]
        if not methods:
            issues.append("required_test_methods_missing:" + location)
            continue
        if len(methods) != len(set(methods)):
            issues.append("duplicate_test_method_name:" + location)
            continue
        name = relative.removesuffix(".py").replace("/", ".") + "." + expected_class
        inventory[name] = tuple(sorted(methods))
    return inventory, issues


def declared_test_inventory(root: Path = ROOT) -> dict[str, tuple[str, ...]]:
    """Return ordinary direct test method declarations without importing code.

    Keys are module/class names; values are sorted method names. Invalid or
    absent declarations are omitted; check_sources returns their diagnostics.
    This inventory does not establish TestCase inheritance, decorator effects,
    runtime rebinding, discovery, absence of skips, or actual test execution.
    """
    if not isinstance(root, Path):
        return {}
    inventory, _ = _test_inventory(root)
    return inventory


def check_sources(root: Path = ROOT) -> tuple[str, ...]:
    """Check selected fixed bytes, v0.14 file inventory, and test declarations.

    All 76 v0.13 source pins remain, together with the seven v0.13 additions.
    The original runner, loader, native hook, and prior checkers are unchanged.
    This requires the new files only when called; it does not change or extend
    the immutable loader's own mandatory-module list.
    """
    if not isinstance(root, Path):
        return ("root:trusted_path_required",)
    issues: list[str] = []
    for relative, expected in SOURCE_BLOBS.items():
        raw, issue = _read_file(root, relative)
        if issue:
            issues.append("source_" + issue + ":" + relative)
        elif _git_blob(raw) != expected:
            issues.append("source_byte_drift:" + relative)
    for relative in REQUIRED_PATHS:
        _, issue = _read_file(root, relative)
        if issue:
            issues.append("required_v014_file_" + issue + ":" + relative)
    _, test_issues = _test_inventory(root)
    issues.extend(test_issues)
    return tuple(sorted(set(issues)))


def main() -> int:
    issues = check_sources()
    for issue in issues:
        print("BLOCKED:", issue)
    if not issues:
        print(
            f"STATIC_MATCH: {len(SOURCE_BLOBS)} selected original Git blobs, "
            "v0.14 inventory and declared test classes; "
            "no test execution, host invocation, transitive authentication "
            "or formal refinement"
        )
        for name, methods in sorted(declared_test_inventory().items()):
            print(f"DECLARED_TEST_CLASS: {name} methods={len(methods)}")
    return int(bool(issues))


if __name__ == "__main__":
    raise SystemExit(main())
