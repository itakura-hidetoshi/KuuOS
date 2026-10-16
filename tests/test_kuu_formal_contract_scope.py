"""Historical formal facts must not be promoted to current Kuu by repair."""
import json
import unittest
from runtime.kuuos_repository_structure_types_v0_79 import RepositorySnapshot
from runtime.kuuos_repository_structure_observer_v0_79 import observe_repository_structure
from runtime.kuuos_repository_repair_candidates_v0_79 import generate_repository_repair_candidates

class KuuFormalContractScopeTests(unittest.TestCase):
    def snapshot(self, package='legacy-v5.291', include_legacy=True):
        contract={'repository_autorepair_contract':True,'validator':'scripts/check_old.py',
                  'strict_formal_root':'KuuOSOld','aggregate_lean_modules':['KUOS.Old'], 'runtime_modules':[]}
        if package is not None: contract['formal_package']=package
        texts={
            'manifests/old.json':json.dumps(contract),
            'scripts/check_old.py':'pass\n',
            'scripts/run_kuuos_runtime_full_check_v0_55.py':'scripts/check_old.py',
            'formal/KuuOSFormal.lean':'import KuuOSStrict\n',
            'lakefile.toml':'roots = [\n "KuuOSFormal", "KuuOSStrict", "Kuu"\n]\n',
        }
        if include_legacy:
            texts['legacy/v5.291/formal/KuuOSFormal.lean']='import KUOS.Old\n'
            texts['legacy/v5.291/lakefile.toml']='roots = ["KuuOSOld"]\n'
        return RepositorySnapshot('migration-fixture',tuple(sorted(texts)),tuple(sorted(texts.items())))

    def test_explicit_legacy_contract_is_checked_in_its_package(self):
        observation=observe_repository_structure(self.snapshot())
        self.assertEqual(observation.weighted_defect_score,0)

    def test_no_implicit_fallback_to_archived_theorem(self):
        observation=observe_repository_structure(self.snapshot(package=None))
        self.assertIn('KuuOSOld', observation.missing_lake_roots)
        self.assertIn('KUOS.Old', observation.missing_aggregate_imports)

    def test_missing_legacy_remains_an_obstruction_not_current_import(self):
        snapshot=self.snapshot(include_legacy=False)
        observation=observe_repository_structure(snapshot)
        self.assertGreater(observation.weighted_defect_score,0)
        candidates=generate_repository_repair_candidates(snapshot,observation)
        self.assertEqual(candidates,())

    def test_unknown_scope_is_not_accepted_as_current(self):
        observation=observe_repository_structure(self.snapshot(package='unknown'))
        self.assertEqual(observation.malformed_contracts,('manifests/old.json',))

if __name__=='__main__':unittest.main()
