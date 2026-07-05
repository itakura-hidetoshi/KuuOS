import unittest
from pathlib import Path


README = Path("README.md")


class KuuOSReadmePublicStatusV066Test(unittest.TestCase):
    def test_readme_mentions_public_status_frontier(self):
        text = README.read_text(encoding="utf-8")
        self.assertIn("KuuOS README Public Status v0.66", text)
        self.assertIn("kuuos_current_root_sequence_v0_66", text)
        self.assertIn("docs/kuuos_readme_public_status_v0_66.md", text)

    def test_readme_mentions_active_self_organization_frontier(self):
        text = README.read_text(encoding="utf-8")
        self.assertIn("KuuOS Current Root Execution Connection v0.65", text)
        self.assertIn("kuuos_current_root_sequence_v0_65", text)
        self.assertIn("docs/kuuos_self_organization_active_state.md", text)

    def test_readme_mentions_bounded_execution_tokens(self):
        text = README.read_text(encoding="utf-8")
        self.assertIn("self_organization_active: true", text)
        self.assertIn("execution_scope: publish_active_self_organization_state", text)
        self.assertIn("state_publication_applied: true", text)

    def test_readme_preserves_non_authority_boundary(self):
        text = README.read_text(encoding="utf-8")
        self.assertIn("active self-organization state != unbounded mutation authority", text)
        self.assertIn("current root execution != production deployment", text)
        self.assertIn("runtime success != external truth", text)
        self.assertIn("README public status != authority grant", text)


if __name__ == "__main__":
    unittest.main()
