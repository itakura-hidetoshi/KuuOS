import unittest
from pathlib import Path


README = Path("README.md")


class KuuOSReadmeSurfaceStatusV078Test(unittest.TestCase):
    def test_readme_mentions_surface_exposure_frontier(self):
        text = README.read_text(encoding="utf-8")
        self.assertIn("KuuOS README Surface Exposure v0.78", text)
        self.assertIn("kuuos_current_root_sequence_v0_78", text)
        self.assertIn("docs/kuuos_readme_surface_exposure_v0_78.md", text)

    def test_readme_mentions_current_surface_paths(self):
        text = README.read_text(encoding="utf-8")
        self.assertIn("runtime/kuuos_current_surface.py", text)
        self.assertIn("runtime/kuuos_current_surface_entrypoint_v0_77.py", text)
        self.assertIn("status/current.surface.index.json", text)
        self.assertIn("status/current.surface.json", text)
        self.assertIn("status/current.resolved.json", text)
        self.assertIn("status/current.manifest.json", text)

    def test_readme_mentions_surface_command(self):
        text = README.read_text(encoding="utf-8")
        self.assertIn("PYTHONPATH=. python3 runtime/kuuos_current_surface.py", text)
        self.assertIn("PYTHONPATH=. python3 runtime/kuuos_current_check.py", text)

    def test_readme_preserves_surface_boundaries(self):
        text = README.read_text(encoding="utf-8")
        self.assertIn("current surface CLI != authority grant", text)
        self.assertIn("current surface index != authority grant", text)
        self.assertIn("current surface artifact != authority grant", text)
        self.assertIn("README surface exposure != authority grant", text)

    def test_readme_preserves_legacy_v066_tokens(self):
        text = README.read_text(encoding="utf-8")
        self.assertIn("KuuOS README Public Status v0.66", text)
        self.assertIn("KuuOS Current Root Execution Connection v0.65", text)
        self.assertIn("docs/kuuos_readme_public_status_v0_66.md", text)
        self.assertIn("self_organization_active: true", text)


if __name__ == "__main__":
    unittest.main()
