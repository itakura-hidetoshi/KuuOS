"""Regression: retiring Gray as foundation must not unpublish existing proofs."""
from pathlib import Path
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]

# Each allowed current-source change is an exact, reviewable lint-only edit of
# the frozen v5.291 bytes. All other historical theorem bytes must remain equal.
LINT_ONLY_SOURCE_EDITS = {
    "KUOS/DependentOriginationContextualCoreV1_0.lean": (
        ("    simpa using D.transport_id_apply X x".encode("utf-8"), "    simp".encode("utf-8")),
        ("    simpa using D.transport_id_apply Y y".encode("utf-8"), "    simp".encode("utf-8")),
    ),
    "KUOS/CodeAI/GeneratedPatchErrorBaselineReplayEvaluationV0_1.lean": (
        ("  simpa [hZero] using hPositive".encode("utf-8"), "  simp [hZero] at hPositive".encode("utf-8")),
    ),
    "KUOS/DependentOriginationFunctorialTransportV0_1.lean": (
        ("  simpa [transport] using congrFun (D.state.map_id X) x".encode("utf-8"), "  simp [transport]".encode("utf-8")),
        ("  simpa [transport] using congrFun (D.state.map_comp f g) x".encode("utf-8"), "  simp [transport]".encode("utf-8")),
    ),
    "KUOS/VerifyOS/MiddleWayConditionalContinuityVerificationV0_4.lean": (
        ("    (kind : certificate.transitionKind = .supersedeWithLineage)".encode("utf-8"), "    (_kind : certificate.transitionKind = .supersedeWithLineage)".encode("utf-8")),
        ("    (kind : certificate.transitionKind = .terminate)".encode("utf-8"), "    (_kind : certificate.transitionKind = .terminate)".encode("utf-8")),
    ),
    "KUOS/Architecture/QiWorldLicensedMultiCycleChainInductionV2_1.lean": (
        ("    simpa [w.target_is_immediate_successor]".encode("utf-8"), "    simp [w.target_is_immediate_successor]".encode("utf-8")),
    ),
    "KUOS/WORLD/KuuVacuumCentralReferenceStateBridgeV0_54.lean": (
        ("def centralReferenceState\n    (Central : WorldKuuVacuumCentralReferenceStateBridge K)".encode("utf-8"), "def centralReferenceState\n    (_Central : WorldKuuVacuumCentralReferenceStateBridge K)".encode("utf-8")),
        ("def excitationVector\n    (Central : WorldKuuVacuumCentralReferenceStateBridge K)".encode("utf-8"), "def excitationVector\n    (_Central : WorldKuuVacuumCentralReferenceStateBridge K)".encode("utf-8")),
        ("def vacuumRelativeEntropyLocal\n    (Central : WorldKuuVacuumCentralReferenceStateBridge K)".encode("utf-8"), "def vacuumRelativeEntropyLocal\n    (_Central : WorldKuuVacuumCentralReferenceStateBridge K)".encode("utf-8")),
        ("def vacuumRelativeEntropyGlobal\n    (Central : WorldKuuVacuumCentralReferenceStateBridge K)".encode("utf-8"), "def vacuumRelativeEntropyGlobal\n    (_Central : WorldKuuVacuumCentralReferenceStateBridge K)".encode("utf-8")),
        ("    (nonzeroWeight : Central.vacuumTwoPoint creator creator ≠ 0)\n    (observable : B.A) : ℂ :=".encode("utf-8"), "    (_nonzeroWeight : Central.vacuumTwoPoint creator creator ≠ 0)\n    (observable : B.A) : ℂ :=".encode("utf-8")),
    ),
    "KUOS/WORLD/KuuVacuumInformationGeometryBridgeV0_55.lean": (
        ("def vacuumTangentExcitation\n    (Geom : WorldKuuVacuumInformationGeometryBridge Central)".encode("utf-8"), "def vacuumTangentExcitation\n    (_Geom : WorldKuuVacuumInformationGeometryBridge Central)".encode("utf-8")),
    ),
    "KUOS/DependentOriginationLinearTransferConnectedReadoutV0_3.lean": (
        ("def centeredState\n    (L : D.LinearTransferRealization)".encode("utf-8"), "def centeredState\n    (_L : D.LinearTransferRealization)".encode("utf-8")),
        ("def connectedReadout\n    (L : D.LinearTransferRealization)".encode("utf-8"), "def connectedReadout\n    (_L : D.LinearTransferRealization)".encode("utf-8")),
        ("def connectedReadoutTwoStep\n    (L : D.LinearTransferRealization)".encode("utf-8"), "def connectedReadoutTwoStep\n    (_L : D.LinearTransferRealization)".encode("utf-8")),
    ),
    "KUOS/DependentOriginationFiniteTransferWordV0_4.lean": (
        (("/-- The decay product of a finite word is exactly the decay factor at total time. -/\n"
          "theorem wordDecayProduct_eq_totalTime").encode("utf-8"),
         ("-- The decay identity needs the normed additive structure, not an additional\n"
          "-- real vector-space instance. Keep it out of this theorem's implicit API.\n"
          "omit [NormedSpace ℝ State] in\n"
          "/-- The decay product of a finite word is exactly the decay factor at total time. -/\n"
          "theorem wordDecayProduct_eq_totalTime").encode("utf-8")),
    ),
}

class PublicRootRestorationTests(unittest.TestCase):
    def test_every_previous_public_root_remains_published(self):
        old = tomllib.loads((ROOT / 'legacy/v5.291/lakefile.toml').read_text())
        new = tomllib.loads((ROOT / 'lakefile.toml').read_text())
        wanted = {r for lib in old['lean_lib'] for r in lib.get('roots', [])}
        actual = {r for lib in new['lean_lib'] for r in lib.get('roots', [])}
        self.assertEqual(wanted - actual, set(),
                         'Existing public proofs were blanket-excluded from the current Lake package')

class RestoredWiringTests(unittest.TestCase):
    def test_internal_kuu_module_is_built_with_one_public_target(self):
        config = tomllib.loads((ROOT / 'lakefile.toml').read_text())
        self.assertEqual(config['defaultTargets'], ['KuuOSFormal'])
        libraries = config['lean_lib']
        self.assertEqual(len(libraries), 1)
        self.assertEqual(libraries[0]['name'], 'KuuOSFormal')
        self.assertNotIn('KuuOSStrict', libraries[0]['roots'])
        self.assertNotIn('Kuu', libraries[0]['roots'])
        # A module can be local to a library through its globs without being
        # a published root; no distinct Lean library is introduced.
        self.assertEqual(libraries[0].get('needs', []), [])
        self.assertTrue(set(libraries[0]['roots']).issubset(set(libraries[0]['globs'])))
        self.assertIn('KuuOSStrict', libraries[0]['globs'])
        self.assertIn('Kuu.*', libraries[0]['globs'])
        workflow = (ROOT / '.github/workflows/kuu-independent-foundation.yml').read_text()
        self.assertIn('build +KuuOSStrict', workflow)
        self.assertNotIn('build KuuOSStrict', workflow)

    def test_publication_and_consumer_routes_are_restored(self):
        from scripts.check_public_proof_roots import check
        report = check(ROOT)
        self.assertTrue(report['ok'], report['errors'])
        self.assertEqual(report['previous_public_roots'], 107)

    def test_original_theorem_files_preserve_archived_bytes_except_exact_lint_edits(self):
        # Keep every frozen historical source untouched. Only the exact
        # reviewed linter corrections listed above are accepted in current.
        before = ROOT / 'legacy/v5.291/formal'
        self.assertTrue(before.is_dir(), 'historical proof snapshot missing')
        archived = list(before.rglob('*.lean'))
        self.assertTrue(archived, 'historical proof snapshot empty')
        seen = set()
        for old in archived:
            rel = old.relative_to(before)
            if rel.as_posix() == 'KuuOSFormal.lean':
                continue  # public import aggregate intentionally extends historical imports
            with self.subTest(path=rel.as_posix()):
                expected = old.read_bytes()
                edits = LINT_ONLY_SOURCE_EDITS.get(rel.as_posix(), ())
                if edits:
                    seen.add(rel.as_posix())
                for old_fragment, new_fragment in edits:
                    self.assertEqual(expected.count(old_fragment), 1,
                                     f'unique archived lint edit required: {rel}')
                    expected = expected.replace(old_fragment, new_fragment, 1)
                self.assertEqual((ROOT / 'formal' / rel).read_bytes(), expected,
                                 f'unapproved mathematical source change: {rel}')
        self.assertEqual(seen, set(LINT_ONLY_SOURCE_EDITS),
                         'reviewed lint edit targets must all exist in historical roots')

    def test_lean_mathlib_pins_are_unchanged(self):
        for name in ('lean-toolchain', 'lake-manifest.json'):
            self.assertEqual((ROOT / name).read_bytes(),
                             (ROOT / 'legacy/v5.291' / name).read_bytes())

    def test_retained_theorems_are_current_package_targets(self):
        from scripts.formal_package_boundary import validate_targets, CURRENT
        validate_targets(ROOT, CURRENT, [
            'KUOS.DependentOriginationContextualCoreV1_0',
            'KUOS.DependentOriginationAdmissibleNonfactorizationV4_01',
            'KuuOSCodeAIV0_1'])

    def test_gray_is_not_a_prerequisite_of_independent_core(self):
        from scripts.check_kuu_foundation import check
        report = check(ROOT)
        self.assertTrue(report['ok'], report['errors'])
        self.assertNotIn('KuuOSFormal', report['current_modules'])

if __name__ == '__main__':
    unittest.main()
