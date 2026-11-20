#!/usr/bin/env python3
"""v0.47 original imported DecisionOS Lean type bridge source audit.

This is a read-only structural/pinning audit, NOT elaboration or CPython
refinement. Verify strict Lean and exact-head CI independently.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
"""
from __future__ import annotations

import ast
from pathlib import Path
import re

from scripts import (
    check_kuuos_lean_python_decision_verify_plan_sources_v0_46 as prior,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PARENT = "410037a3bd8af5d78defb83e72b65f8b319caf3f"
ORIGINAL_LAKE_BLOB = "b347dc9615089258d2bd9e265c4919810a7468e3"
LEGACY_TEMPERATURE_SOURCE = (
    "legacy/v5.291/formal/KuuOS/"
    "PlanOSTemperatureTrajectoryStabilityCertificateKernelV01.lean"
)
ACTIVE_TEMPERATURE_SOURCE = (
    "formal/KuuOS/PlanOSTemperatureTrajectoryStabilityCertificateKernelV01.lean"
)
ORIGINAL_TEMPERATURE_BLOB = "46d8a67594af17e6aa63f13600f90b9ab34c8ff8"
ACTIVE_TEMPERATURE_BLOB = "a3d7e25d585da29e17eaef8f8c11d972948dbb40"
TEMPERATURE_OLD_PROOF = (
    b"  | cons step steps ih =>\n"
    b"      simp [totalVariation, abs_nonneg, ih]"
)
TEMPERATURE_NEW_PROOF = (
    b"  | cons step steps ih =>\n"
    b"      simp only [totalVariation]\n"
    b"      exact add_nonneg (abs_nonneg step) ih"
)
NEW = (
    "formal/KUOS/Architecture/LeanPythonOriginalDecisionTypeBridgeV0_47.lean",
    "scripts/check_kuuos_lean_python_original_decision_type_sources_v0_47.py",
    "tests/lean_python_extensions/test_original_decision_type_sources_v0_47.py",
    "docs/KUUOS_LEAN_PYTHON_ORIGINAL_DECISION_TYPE_BRIDGE_v0_47.md",
)
PINNED = {
    "formal/KUOS/DecisionOS/BoundedPlanSynthesisRequestHandoffV0_8.lean":
        "43770afe9e74a4d2a578f6f31c1482756eb118f7",
    "formal/KUOS/Architecture/LeanPythonDecisionVerifyPlanNativeHandoffV0_46.lean":
        "643abf14773231b81f0843d08f121c41a9d472d7",
    "formal/KUOS/Architecture/LeanPythonVerifyPlanSixRoutesV0_45.lean":
        "633d471f8ea1624f143b7068f98c9eb126efc85c",
}
LEAN_IMPORTS = (
    "import Mathlib",
    "import KUOS.DecisionOS.BoundedPlanSynthesisRequestHandoffV0_8",
    "import KUOS.Architecture.LeanPythonDecisionVerifyPlanNativeHandoffV0_46",
)
LEAN_DECLARATIONS = (
    "def originalToMapped",
    "def mappedToOriginal",
    "def originalReceiptEquiv",
    "theorem originalValid_iff_mappedValid",
    "theorem originalDecisionBoundaries",
    "theorem originalDecisionSixRouteConditionalWitness",
    "theorem originalHandoffNeverLicensesHostExecution",
)

# The only allowed lakefile change is the exact additive ten-module
# registration below. Removing it must recover the exact prior Git blob.
LAKE_INSERT = (
    "  # v0.47: exact build registration only for original DecisionOS v0.8\n"
    "  # dependency closure; no new published roots or wildcard expansion.\n"
    "  \"KuuOS.PlanOSV098\",\n"
    "  \"KuuOS.PlanOSV099\",\n"
    "  \"KuuOS.PlanOSV100\",\n"
    "  \"KuuOS.PlanOSV101\",\n"
    "  \"KuuOS.PlanOSV102\",\n"
    "  \"KuuOS.PlanOSTemperatureTrajectoryStabilityCertificateKernelV01\",\n"
    "  \"KuuOS.PlanOSQiConditionedInformationMetricCertificateKernelV01\",\n"
    "  \"KuuOS.PlanOSWorldConditionedPathProjectionPullbackMetricKernelV01\",\n"
    "  \"KuuOS.PlanOSWorldConditionedObjectiveDistributionUpdateKernelV01\",\n"
    "  \"KuuOS.PlanOSWorldConditionedDistributionDecisionHandoffCertificateKernelV01\",\n"
)
LEGACY_MODULES = (
    "KuuOS.PlanOSV098",
    "KuuOS.PlanOSV099",
    "KuuOS.PlanOSV100",
    "KuuOS.PlanOSV101",
    "KuuOS.PlanOSV102",
    "KuuOS.PlanOSTemperatureTrajectoryStabilityCertificateKernelV01",
    "KuuOS.PlanOSQiConditionedInformationMetricCertificateKernelV01",
    "KuuOS.PlanOSWorldConditionedPathProjectionPullbackMetricKernelV01",
    "KuuOS.PlanOSWorldConditionedObjectiveDistributionUpdateKernelV01",
    "KuuOS.PlanOSWorldConditionedDistributionDecisionHandoffCertificateKernelV01",
)


def _read(root: Path, path: str):
    return prior._read(root, path)


def _blob(raw: bytes) -> str:
    return prior._blob(raw)


def _trusted_root(root: Path) -> bool:
    return prior._trusted_root(root)


def _block(source: str, first: str, second: str) -> str:
    start = source.find(first)
    if start == -1:
        raise ValueError("start_declaration_missing")
    start += len(first)
    end = source.find(second, start)
    if end == -1:
        raise ValueError("end_declaration_missing")
    return source[start:end]


def _original_fields(source: str) -> tuple[str, ...]:
    body = _block(
        source, "structure BoundedPlanSynthesisRequestHandoffReceipt where",
        "structure BoundedPlanSynthesisRequestHandoffValid",
    )
    return tuple(re.findall(r"^  ([a-zA-Z_]\w*) : (?:Bool|Prop)$", body, re.M))


def _original_validity_fields(source: str) -> tuple[str, ...]:
    body = _block(
        source,
        "(r : BoundedPlanSynthesisRequestHandoffReceipt) : Prop where",
        "theorem handoff_preserves_selected_candidate_and_decision_ownership",
    )
    return tuple(re.findall(r"^  ([a-zA-Z_]\w*)\s*:", body, re.M))


def _mapped_fields(source: str) -> tuple[str, ...]:
    body = _block(
        source, "structure SourceMappedDecisionHandoffReceipt where",
        "structure SourceMappedDecisionHandoffValid",
    )
    return tuple(re.findall(r"^  ([a-zA-Z_]\w*) : (?:Bool|Prop)$", body, re.M))


def _mapped_validity_fields(source: str) -> tuple[str, ...]:
    body = _block(
        source,
        "(r : SourceMappedDecisionHandoffReceipt) : Prop where",
        "/-- Source-mapped DecisionOS keeps its five",
    )
    return tuple(re.findall(r"^  ([a-zA-Z_]\w*)\s*:", body, re.M))


def check_sources(root: Path = ROOT) -> tuple[str, ...]:
    if not _trusted_root(root):
        return ("root:trusted_path_required",)
    issues = list(prior.check_sources(root))

    for path, sha in PINNED.items():
        raw, problem = _read(root, path)
        if problem:
            issues.append("v047_original_source_missing:" + path)
        elif _blob(raw) != sha:
            issues.append("v047_original_source_changed:" + path)

    # Existing active historical source is repaired by one proof-term change.
    # Preserve byte-for-byte legacy snapshot; require exact single substitution.
    archive_raw, archive_problem = _read(root, LEGACY_TEMPERATURE_SOURCE)
    active_raw, active_problem = _read(root, ACTIVE_TEMPERATURE_SOURCE)
    if archive_problem or active_problem:
        issues.append("v047_historical_temperature_source_missing")
    elif (_blob(archive_raw) != ORIGINAL_TEMPERATURE_BLOB
          or archive_raw.count(TEMPERATURE_OLD_PROOF) != 1
          or _blob(active_raw) != ACTIVE_TEMPERATURE_BLOB
          or active_raw != archive_raw.replace(
              TEMPERATURE_OLD_PROOF, TEMPERATURE_NEW_PROOF, 1)):
        issues.append("v047_historical_temperature_proof_uncontrolled_change")

    raw_lake, lake_problem = _read(root, "lakefile.toml")
    if lake_problem:
        issues.append("v047_lakefile_missing")
    elif raw_lake.count(LAKE_INSERT.encode("utf-8")) != 1:
        issues.append("v047_legacy_registration_incorrect")
    elif _blob(raw_lake.replace(LAKE_INSERT.encode("utf-8"), b"", 1)) != ORIGINAL_LAKE_BLOB:
        issues.append("v047_canonical_lakefile_modified_outside_tight_addition")
    else:
        for module in LEGACY_MODULES:
            raw, problem = _read(root, "formal/" + module.replace(".", "/") + ".lean")
            if problem:
                issues.append("v047_legacy_module_missing:" + module)

    for path in NEW:
        raw, problem = _read(root, path)
        if problem:
            issues.append("v047_new_file_missing:" + path)
            continue
        if not path.endswith(".py"):
            continue
        try:
            ast.parse(raw.decode("utf-8"))
        except (UnicodeError, SyntaxError, ValueError, RecursionError):
            issues.append("v047_python_unparsable:" + path)

    raw, problem = _read(root, NEW[0])
    if not problem:
        try:
            source = raw.decode("utf-8")
            lines = tuple(line.strip() for line in source.splitlines())
            code = prior.prior._lean_code_without_comments_or_strings(source)
            lines_code = tuple(line.strip() for line in code.splitlines())
        except (UnicodeError, ValueError):
            issues.append("v047_lean_lexical_scan_incomplete")
        else:
            for name in LEAN_IMPORTS:
                if name not in lines:
                    issues.append("v047_missing_lean_import:" + name)
            for name in LEAN_DECLARATIONS:
                if not any(
                    line == name or line.startswith(name + " ")
                    or line.startswith(name + ":") for line in lines_code
                ):
                    issues.append("v047_missing_lean_declaration:" + name)
            if prior.prior._contains_unproved_lean(source):
                issues.append("v047_unproved_lean_source")

            original_raw, err_orig = _read(
                root, "formal/KUOS/DecisionOS/BoundedPlanSynthesisRequestHandoffV0_8.lean",
            )
            mapped_raw, err_mapped = _read(
                root, "formal/KUOS/Architecture/LeanPythonDecisionVerifyPlanNativeHandoffV0_46.lean",
            )
            if not err_orig and not err_mapped:
                try:
                    fields = _original_fields(original_raw.decode("utf-8"))
                    mapped = _mapped_fields(mapped_raw.decode("utf-8"))
                    valid = _original_validity_fields(original_raw.decode("utf-8"))
                    mapped_valid = _mapped_validity_fields(mapped_raw.decode("utf-8"))
                    if (len(fields) != 35 or fields != mapped
                            or len(valid) != 35 or valid != mapped_valid):
                        issues.append("v047_source_mapped_schema_not_identical")
                    for name in fields:
                        if code.count(f"{name} := r.{name}") != 2:
                            issues.append("v047_both_original_maps_required:" + name)
                    for name in valid:
                        if code.count(f"{name} := h.{name}") != 2:
                            issues.append("v047_both_validity_proofs_required:" + name)
                except (UnicodeError, ValueError):
                    issues.append("v047_source_schema_extraction_failed")

    raw_tests, err_tests = _read(root, NEW[2])
    if not err_tests:
        try:
            tree = ast.parse(raw_tests.decode("utf-8"))
            classes = [x for x in tree.body
                       if isinstance(x, ast.ClassDef)
                       and x.name == "OriginalDecisionTypeSourceTests"]
            methods = [x.name for x in classes[0].body
                       if isinstance(x, ast.FunctionDef)
                       and x.name.startswith("test_")] if len(classes) == 1 else []
            if len(methods) < 10 or len(methods) != len(set(methods)):
                issues.append("v047_test_inventory_incomplete")
        except (UnicodeError, SyntaxError, ValueError, RecursionError):
            issues.append("v047_test_inventory_unparseable")
    return tuple(sorted(set(issues)))


def main() -> int:
    issues = check_sources()
    for issue in issues:
        print("BLOCKED:", issue)
    if not issues:
        print("STATIC_MATCH: exactly 10 nonpublished legacy module registrations")
        print("STATIC_MATCH: preserved historic temperature proof snapshot, exact repair")
        print("STATIC_MATCH: entire original 35-field and 35-premise receipt model")
        print("NOT_PROOF: only Strict Lean can certify original type equivalence")
    return int(bool(issues))


if __name__ == "__main__":
    raise SystemExit(main())
