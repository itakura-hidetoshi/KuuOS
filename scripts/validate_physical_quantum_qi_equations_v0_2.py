#!/usr/bin/env python3
"""Validate equation-level content for Physical Quantum Qi v0.2."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / "docs" / "PHYSICAL_QUANTUM_QI_EQUATIONS_v0_2.md"

REQUIRED_SECTIONS = [
    "## 1. SK/FV Qi path integral",
    "## 2. Qi current and Ward/leak identity",
    "## 3. DPI recoverability margin",
    "## 4. IndraNet gauge transport",
    "## 5. KuString-Qi emergence from relational difference",
    "## 5.6 Qi phase to KuuOS handoff surface",
    "## 6. Minimal equation packet keys",
]

REQUIRED_EQUATION_TOKENS = [
    "Z_{\\mathrm{Qi}}[J_+,J_-]",
    "S_{\\mathrm{IF}}[q_+,q_-]",
    "\\Delta q(t)=q_+(t)-q_-(t)",
    "D_R(t,t')",
    "N(t,t')",
    "J^\\mu_{\\mathrm{Qi}}(x)",
    "\\frac{\\delta S_{\\mathrm{Qi}}}{\\delta A_\\mu(x)}",
    "D_\\mu\\langle J^\\mu_{\\mathrm{Qi}}\\rangle",
    "\\mathcal L_{\\mathrm{leak}}",
    "\\mathcal A_{\\mathrm{anom}}",
    "\\Delta_{\\mathrm{DPI}}",
    "\\mathcal R_{\\mathrm{Qi}}",
    "\\eta_{\\mathrm{Qi}}",
    "\\delta_{\\mathrm{rec}}",
    "F_{\\mu\\nu}",
    "U_\\gamma",
    "W(C)",
    "\\delta_{\\mathrm{rel}}\\in K^\\perp",
    "X:\\Sigma\\to\\mathcal M",
    "S_{\\mathrm{string}}",
    "\\partial\\Sigma\\subset B",
    "\\Pi_{\\mathrm{gauge}}",
    "\\frac{\\delta S_{\\mathrm{eff}}}{\\delta A_\\mu}",
]

REQUIRED_PHRASES = [
    "Qi does not emerge directly from `K`.",
    "The MGAP4D internal-normalized `33/20` gap is a stability floor",
    "It is not a Qi source.",
    "graph-edge flow",
    "connection-dependent parallel transport",
    "Recoverability is a quantitative margin, not a label.",
    "Qi current is not asserted by naming a flow.",
    "history-sensitive open-system path surface",
    "Qi phase classification is a routing surface, not an authority grant.",
    "The key point is that `FullPathQi` is recordable and analyzable, but not executable by itself.",
]

REQUIRED_HANDOFF_TOKENS = [
    "BeliefOS.observation_candidate",
    "PlanOS.preparation_surface",
    "PlanOS.boundary_candidate",
    "PlanOS.transport_candidate",
    "DecisionOS.safety_evaluable_candidate",
    "MemoryOS.recordable_history_candidate",
    "ReflectionOS.residue_analysis_candidate",
    "execution_authority",
    "commit_authority",
    "belief_root_commit_authority",
    "memory_overwrite_authority",
    "world_root_rewrite_authority",
    "clinical_authority",
    "proof_authority",
    "ontology_authority",
    "truth_authority",
    "safety_override_authority",
]

REQUIRED_PACKET_KEYS = [
    "Z_Qi_SKFV",
    "S_sys",
    "S_IF",
    "Delta_q",
    "Sigma_q",
    "D_R_kernel",
    "N_noise_kernel",
    "J_Qi_variation_from_A",
    "Ward_closed_identity",
    "Ward_open_leak_identity",
    "Delta_DPI",
    "R_Qi",
    "eta_Qi",
    "delta_rec",
    "A_mu",
    "F_munu",
    "U_gamma",
    "W_C",
    "K_non_reification",
    "delta_rel_in_K_perp",
    "StringMode_worldsheet",
    "BraneBoundary",
    "A_mu_projection_from_string_brane",
    "J_Qi_from_effective_action",
    "Qi_OS_handoff",
    "mass_gap_33_20_floor_not_source",
]

FORBIDDEN_COLLAPSES = [
    "K_identified_as_Qi",
    "string_reified_as_substance",
    "brane_reified_as_creator",
    "mass_gap_claimed_as_Qi_source",
]


def require_all(text: str, items: List[str], label: str) -> List[str]:
    return [f"missing {label}: {item}" for item in items if item not in text]


def main() -> int:
    text = DOC_PATH.read_text(encoding="utf-8")
    errors: List[str] = []
    errors.extend(require_all(text, REQUIRED_SECTIONS, "section"))
    errors.extend(require_all(text, REQUIRED_EQUATION_TOKENS, "equation token"))
    errors.extend(require_all(text, REQUIRED_PHRASES, "phrase"))
    errors.extend(require_all(text, REQUIRED_HANDOFF_TOKENS, "handoff token"))
    errors.extend(require_all(text, REQUIRED_PACKET_KEYS, "minimal equation packet key"))
    errors.extend(require_all(text, FORBIDDEN_COLLAPSES, "forbidden collapse marker"))

    if "K\n  -> delta_rel in K_perp\n  -> StringMode\n  -> BraneBoundary\n  -> A_mu\n  -> F_munu\n  -> J_Qi_mu\n  -> Z_Qi\n  -> Physical Quantum Qi" not in text:
        errors.append("missing complete KuString-Qi emergence lineage")

    if errors:
        print("Physical Quantum Qi equations v0.2 validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Physical Quantum Qi equations v0.2 validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
